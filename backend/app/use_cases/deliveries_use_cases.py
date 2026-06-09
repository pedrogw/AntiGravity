from typing import List, Optional
from datetime import datetime, timezone
from fastapi import HTTPException, status as http_status
from app.domain.entities.delivery import (
    Delivery as DeliveryEntity,
    VALID_TRANSITIONS,
)
from app.domain.repositories.delivery_repo import DeliveryRepositoryProtocol
from app.domain.repositories.place_repo import PlaceRepositoryProtocol
from app.domain.repositories.eta_history_repo import EtaHistoryRepositoryProtocol
from app.domain.repositories.chaos_repo import ChaosRepositoryProtocol
from app.use_cases._eta_recalculation import recalculate_delivery_eta
import uuid

class CreateDeliveryUseCase:
    """Cria nova entrega com status inicial pendente."""
    def __init__(self, repo: DeliveryRepositoryProtocol):
        self.repo = repo

    async def execute(self, factory_id: uuid.UUID, store_id: uuid.UUID, driver_id: uuid.UUID) -> DeliveryEntity:
        delivery = DeliveryEntity(
            factory_id=factory_id,
            store_id=store_id,
            driver_id=driver_id
        )
        return await self.repo.create(delivery)

class ListDeliveriesUseCase:
    """Retorna lista paginada de entregas."""
    def __init__(self, repo: DeliveryRepositoryProtocol):
        self.repo = repo

    async def execute(self, limit: int = 50, offset: int = 0) -> List[DeliveryEntity]:
        return await self.repo.list_all(limit=limit, offset=offset)

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
            raise HTTPException(status_code=404, detail="Entrega não encontrada")

        now = datetime.now(timezone.utc)

        if status:
            allowed = VALID_TRANSITIONS.get(delivery.status, [])
            if status not in allowed:
                raise HTTPException(
                    status_code=422,
                    detail=f"Transição inválida: {delivery.status} -> {status}. "
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
