import json
import logging
import uuid
from datetime import datetime
from typing import Any

from arq.connections import ArqRedis, RedisSettings

from app.core.config import settings
from app.core.events.base import DomainEvent
from app.domain.events import (
    AlertCreationRequested,
    DeliveryCreatedEvent,
    DeliveryStatusChangedEvent,
    EtaRecalculationRequested,
)
from app.infrastructure.cache.cache_service import CacheService
from app.infrastructure.events.audit_listener import AuditListener
from app.infrastructure.events.cache_invalidation_listener import (
    CacheInvalidationListener,
)

logger = logging.getLogger("antigravity.worker")

_EVENT_TYPE_MAP: dict[str, type[DomainEvent]] = {
    "AlertCreationRequested": AlertCreationRequested,
    "DeliveryCreatedEvent": DeliveryCreatedEvent,
    "DeliveryStatusChangedEvent": DeliveryStatusChangedEvent,
    "EtaRecalculationRequested": EtaRecalculationRequested,
}

_FIELD_SERIALIZERS = {
    uuid.UUID: str,
    datetime: lambda v: v.isoformat(),
}


def serialize_event(event: DomainEvent) -> str:
    data: dict[str, Any] = {
        "id": str(event.id),
        "occurred_at": event.occurred_at.isoformat(),
    }
    for field_name in event.__dataclass_fields__:
        val = getattr(event, field_name)
        for typ, serializer in _FIELD_SERIALIZERS.items():
            if isinstance(val, typ):
                data[field_name] = serializer(val)
                break
        else:
            data[field_name] = val
    return json.dumps({"event_type": type(event).__name__, "event_data": data})


def deserialize_event(payload: str) -> DomainEvent | None:
    try:
        raw = json.loads(payload)
        event_type_name = raw["event_type"]
        event_data: dict[str, Any] = raw["event_data"]
        cls = _EVENT_TYPE_MAP.get(event_type_name)
        if not cls:
            logger.warning("Unknown event type: %s", event_type_name)
            return None
        for key, val in event_data.items():
            if key in ("id", "delivery_id", "factory_id", "store_id", "driver_id"):
                if val is not None:
                    event_data[key] = uuid.UUID(val)
            elif key == "occurred_at" and isinstance(val, str):
                event_data[key] = datetime.fromisoformat(val)
        return cls(**event_data)
    except Exception:
        logger.exception("Failed to deserialize event")
        return None


async def handle_domain_event(ctx: dict[str, Any], event_payload: str) -> None:
    event = deserialize_event(event_payload)
    if not event:
        return

    if isinstance(event, DeliveryCreatedEvent | DeliveryStatusChangedEvent):
        await AuditListener().handle(event)

    if isinstance(event, DeliveryCreatedEvent):
        try:
            redis = ctx.get("redis")
            if redis is not None:
                cache_service = CacheService(redis)
                await CacheInvalidationListener(cache_service).handle(event)
        except Exception:
            logger.exception("Cache invalidation failed in worker")

    if isinstance(event, EtaRecalculationRequested):
        await handle_eta_recalculation(
            ctx,
            str(event.delivery_id),
            event.lat,
            event.lng,
            event.reason,
        )

    if isinstance(event, AlertCreationRequested):
        await handle_alert_creation(
            ctx,
            str(event.delivery_id),
            event.message,
            event.is_critical,
        )


async def handle_alert_creation(
    ctx: dict[str, Any],
    delivery_id: str,
    message: str,
    is_critical: bool,
) -> None:
    from app.db.session import AsyncSessionLocal
    from app.infrastructure.repositories.alert_repo import AlertRepository
    from app.domain.entities.alert import Alert as AlertEntity

    async with AsyncSessionLocal() as session:
        alert = AlertEntity(
            delivery_id=uuid.UUID(delivery_id),
            message=message,
            is_critical=is_critical,
        )
        await AlertRepository(session).create(alert)


async def handle_eta_recalculation(
    ctx: dict[str, Any],
    delivery_id: str,
    lat: float,
    lng: float,
    reason: str,
) -> None:
    from app.db.session import AsyncSessionLocal
    from app.infrastructure.repositories.delivery_repo import DeliveryRepository
    from app.infrastructure.repositories.place_repo import PlaceRepository
    from app.infrastructure.repositories.chaos_repo import ChaosRepository
    from app.infrastructure.repositories.eta_history_repo import EtaHistoryRepository
    from app.use_cases._eta_recalculation import recalculate_delivery_eta

    async with AsyncSessionLocal() as session:
        delivery_repo = DeliveryRepository(session)
        delivery = await delivery_repo.get_by_id(uuid.UUID(delivery_id))
        if not delivery:
            logger.warning("Delivery %s not found for ETA recalculation", delivery_id)
            return
        await recalculate_delivery_eta(
            delivery=delivery,
            lat=lat,
            lng=lng,
            place_repo=PlaceRepository(session),
            chaos_repo=ChaosRepository(session),
            eta_history_repo=EtaHistoryRepository(session),
            reason=reason,
        )
        await delivery_repo.update(delivery)


async def enqueue_event(event: DomainEvent, pool: ArqRedis) -> None:
    payload = serialize_event(event)
    await pool.enqueue_job("handle_domain_event", payload)


class WorkerSettings:
    functions = [handle_domain_event]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
