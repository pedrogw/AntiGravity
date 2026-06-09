from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid
from app.db.session import get_db
from app.schemas.delivery import DeliveryCreate, DeliveryUpdate, DeliveryResponse
from app.infrastructure.repositories.delivery_repo import DeliveryRepository
from app.infrastructure.repositories.place_repo import PlaceRepository
from app.infrastructure.repositories.eta_history_repo import EtaHistoryRepository
from app.infrastructure.repositories.chaos_repo import ChaosRepository
from app.use_cases.deliveries_use_cases import (
    CreateDeliveryUseCase, ListDeliveriesUseCase, UpdateDeliveryUseCase
)
from app.api.deps import require_role, get_current_user

router = APIRouter()

@router.post("/", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
async def create_delivery(
    delivery_in: DeliveryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("lojista"))
):
    repo = DeliveryRepository(db)
    use_case = CreateDeliveryUseCase(repo)
    return await use_case.execute(
        factory_id=delivery_in.factory_id,
        store_id=delivery_in.store_id,
        driver_id=delivery_in.driver_id
    )

@router.get("/", response_model=List[DeliveryResponse])
async def list_deliveries(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    repo = DeliveryRepository(db)
    use_case = ListDeliveriesUseCase(repo)
    return await use_case.execute(limit=limit, offset=offset)

@router.patch("/{delivery_id}", response_model=DeliveryResponse)
async def update_delivery(
    delivery_id: uuid.UUID,
    delivery_in: DeliveryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    delivery_repo = DeliveryRepository(db)
    place_repo = PlaceRepository(db)
    eta_history_repo = EtaHistoryRepository(db)
    chaos_repo = ChaosRepository(db)
    use_case = UpdateDeliveryUseCase(delivery_repo, place_repo, eta_history_repo, chaos_repo)
    return await use_case.execute(
        delivery_id=delivery_id,
        status=delivery_in.status,
        lat=delivery_in.lat,
        lng=delivery_in.lng,
    )
