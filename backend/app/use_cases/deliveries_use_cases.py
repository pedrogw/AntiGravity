from typing import List, Optional, TYPE_CHECKING
from datetime import datetime, timezone
from app.domain.entities.delivery import (
    Delivery as DeliveryEntity,
    VALID_TRANSITIONS,
)
from app.domain.repositories.delivery_repo import DeliveryRepositoryProtocol
from app.domain.repositories.place_repo import PlaceRepositoryProtocol
from app.domain.repositories.eta_history_repo import EtaHistoryRepositoryProtocol
from app.domain.repositories.chaos_repo import ChaosRepositoryProtocol
from app.domain.services.eta_service import calculate_eta_between_coordinates
from app.domain.haversine import add_hours_to_now
from app.core.config import settings
from app.core.exceptions import EntityNotFoundException, InvalidTransitionException
from app.domain.events import DeliveryCreatedEvent
from app.use_cases._eta_recalculation import recalculate_delivery_eta
from app.infrastructure.cache.cache_service import CACHE_PREFIX
import uuid

if TYPE_CHECKING:
    from app.core.events.bus import EventBus
    from app.infrastructure.cache.cache_service import CacheService

class CreateDeliveryUseCase:
    def __init__(
        self,
        repo: DeliveryRepositoryProtocol,
        place_repo: PlaceRepositoryProtocol,
        event_bus: Optional["EventBus"] = None,
    ):
        self.repo = repo
        self.place_repo = place_repo
        self.event_bus = event_bus

    async def execute(self, factory_id: uuid.UUID, store_id: uuid.UUID, driver_id: uuid.UUID) -> DeliveryEntity:
        factory = await self.place_repo.get_factory_by_id(factory_id)
        if not factory:
            raise EntityNotFoundException("Fábrica não encontrada")

        store = await self.place_repo.get_store_by_id(store_id)
        if not store:
            raise EntityNotFoundException("Loja não encontrada")

        eta_hours = calculate_eta_between_coordinates(
            factory.location, store.location, settings.DEFAULT_SPEED_KMH,
        )
        eta = add_hours_to_now(eta_hours) if eta_hours > 0 else None

        delivery = DeliveryEntity(
            factory_id=factory_id,
            store_id=store_id,
            driver_id=driver_id,
            eta_original=eta,
            eta_current=eta,
        )
        result = await self.repo.create(delivery)

        if self.event_bus:
            await self.event_bus.publish(DeliveryCreatedEvent(
                delivery_id=result.id,
                factory_id=result.factory_id,
                store_id=result.store_id,
                driver_id=result.driver_id,
                eta_original_iso=result.eta_original.isoformat() if result.eta_original else None,
            ))

        return result

class ListDeliveriesUseCase:
    def __init__(self, repo: DeliveryRepositoryProtocol, cache_service: Optional["CacheService"] = None):
        self.repo = repo
        self.cache_service = cache_service

    async def execute(self, limit: int = 50, offset: int = 0) -> List[DeliveryEntity]:
        if not self.cache_service:
            return await self.repo.list_all(limit=limit, offset=offset)

        cache_key = f"{CACHE_PREFIX}:{limit}:{offset}"
        cached = await self.cache_service.get_json(cache_key)
        if cached is not None:
            return [DeliveryEntity(**item) for item in cached]

        entities = await self.repo.list_all(limit=limit, offset=offset)
        if entities:
            await self.cache_service.set_json(
                cache_key,
                [{
                    "id": str(e.id),
                    "factory_id": str(e.factory_id),
                    "store_id": str(e.store_id),
                    "driver_id": str(e.driver_id),
                    "status": e.status,
                    "eta_original": e.eta_original.isoformat() if e.eta_original else None,
                    "eta_current": e.eta_current.isoformat() if e.eta_current else None,
                    "departed_at": e.departed_at.isoformat() if e.departed_at else None,
                    "current_lat": e.current_lat,
                    "current_lng": e.current_lng,
                } for e in entities],
            )
        return entities

class UpdateDeliveryUseCase:
    """Atualiza status (com máquina de estados) e/ou posição do motorista com recálculo de ETA e aplicação de caos ativo."""
    def __init__(
        self,
        delivery_repo: DeliveryRepositoryProtocol,
        place_repo: PlaceRepositoryProtocol,
        eta_history_repo: EtaHistoryRepositoryProtocol,
        chaos_repo: ChaosRepositoryProtocol,
    ):
        self.delivery_repo = delivery_repo
        self.place_repo = place_repo
        self.eta_history_repo = eta_history_repo
        self.chaos_repo = chaos_repo

    async def execute(
        self,
        delivery_id: uuid.UUID,
        status: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
    ) -> DeliveryEntity:
        delivery = await self.delivery_repo.get_by_id(delivery_id)
        if not delivery:
            raise EntityNotFoundException("Entrega não encontrada")

        now = datetime.now(timezone.utc)

        if status:
            allowed = VALID_TRANSITIONS.get(delivery.status, [])
            if status not in allowed:
                raise InvalidTransitionException(
                    f"Transição inválida: {delivery.status} -> {status}. "
                    f"Transições permitidas: {allowed}",
                )
            delivery.status = status
            if status == "em_transito" and not delivery.departed_at:
                delivery.departed_at = now

        if lat is not None and lng is not None:
            delivery.current_lat = lat
            delivery.current_lng = lng

            await recalculate_delivery_eta(
                delivery=delivery,
                lat=lat,
                lng=lng,
                place_repo=self.place_repo,
                chaos_repo=self.chaos_repo,
                eta_history_repo=self.eta_history_repo,
                reason="posicao_atualizada",
            )

        return await self.delivery_repo.update(delivery)
