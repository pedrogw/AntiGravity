from app.domain.entities.chaos import ChaosEventLog as ChaosEventLogEntity
from app.domain.entities.alert import Alert as AlertEntity
from app.domain.repositories.delivery_repo import DeliveryRepositoryProtocol
from app.domain.repositories.chaos_repo import ChaosRepositoryProtocol
from app.domain.repositories.alert_repo import AlertRepositoryProtocol
from app.domain.repositories.eta_history_repo import EtaHistoryRepositoryProtocol
from app.domain.repositories.place_repo import PlaceRepositoryProtocol
from app.domain.repositories.idempotency_repo import IdempotencyRepositoryProtocol
from app.use_cases._eta_recalculation import recalculate_delivery_eta
from app.core.config import settings
from app.core.exceptions import EntityNotFoundException
from app.domain.events import AlertCreationRequested, EtaRecalculationRequested
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.events.bus import EventBus


class InjectChaosUseCase:
    def __init__(
        self,
        delivery_repo: DeliveryRepositoryProtocol,
        chaos_repo: ChaosRepositoryProtocol,
        alert_repo: AlertRepositoryProtocol,
        eta_history_repo: EtaHistoryRepositoryProtocol,
        place_repo: PlaceRepositoryProtocol,
        idempotency_repo: IdempotencyRepositoryProtocol | None = None,
        event_bus: "EventBus | None" = None,
    ):
        self.delivery_repo = delivery_repo
        self.chaos_repo = chaos_repo
        self.alert_repo = alert_repo
        self.eta_history_repo = eta_history_repo
        self.place_repo = place_repo
        self.idempotency_repo = idempotency_repo
        self.event_bus = event_bus

    async def execute(
        self,
        delivery_id: uuid.UUID,
        event_type: str,
        impact_factor: float = 1.0,
        delay_minutes: int = 0,
        lat_start: float | None = None,
        lng_start: float | None = None,
        lat_end: float | None = None,
        lng_end: float | None = None,
        idempotency_key: str | None = None,
    ) -> ChaosEventLogEntity:
        if idempotency_key and self.idempotency_repo:
            cached = await self.idempotency_repo.get(idempotency_key)
            if cached:
                return cached

        delivery = await self.delivery_repo.get_by_id(delivery_id)
        if not delivery:
            raise EntityNotFoundException("Entrega não encontrada")

        chaos_event = ChaosEventLogEntity(
            delivery_id=delivery_id,
            event_type=event_type,
            impact_factor=impact_factor,
            delay_minutes=delay_minutes,
            lat_start=lat_start,
            lng_start=lng_start,
            lat_end=lat_end,
            lng_end=lng_end,
        )
        created = await self.chaos_repo.create(chaos_event)

        if idempotency_key and self.idempotency_repo:
            await self.idempotency_repo.save(idempotency_key, created)

        if delivery.current_lat is not None and delivery.current_lng is not None:
            if self.event_bus and self.event_bus.worker_pool:
                await self.event_bus.publish(EtaRecalculationRequested(
                    delivery_id=delivery_id,
                    lat=delivery.current_lat,
                    lng=delivery.current_lng,
                    reason="caos_injetado",
                ))
            else:
                recalculated = await recalculate_delivery_eta(
                    delivery=delivery,
                    lat=delivery.current_lat,
                    lng=delivery.current_lng,
                    place_repo=self.place_repo,
                    chaos_repo=self.chaos_repo,
                    eta_history_repo=self.eta_history_repo,
                    reason="caos_injetado",
                )
                if recalculated:
                    await self.delivery_repo.update(delivery)

        parts = [f"Caos injetado: {event_type}"]
        if delay_minutes > 0:
            parts.append(f"atraso de {delay_minutes}min")
        if impact_factor > settings.CHAOS_CRITICAL_FACTOR_THRESHOLD:
            parts.append(f"fator {impact_factor}x")

        message = ", ".join(parts)
        alert = AlertEntity.from_chaos(
            delivery_id=delivery_id,
            message=message,
            impact_factor=impact_factor,
            delay_minutes=delay_minutes,
            factor_threshold=settings.CHAOS_CRITICAL_FACTOR_THRESHOLD,
            delay_threshold=settings.CHAOS_CRITICAL_DELAY_THRESHOLD,
        )
        if alert.is_critical:
            if self.event_bus and self.event_bus.worker_pool:
                await self.event_bus.publish(AlertCreationRequested(
                    delivery_id=alert.delivery_id,
                    message=alert.message,
                    is_critical=alert.is_critical,
                ))
            else:
                await self.alert_repo.create(alert)

        return created
