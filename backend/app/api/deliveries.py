from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.delivery import DeliveryCreate, DeliveryResponse
from app.infrastructure.repositories.delivery_repo import DeliveryRepository
from app.use_cases.deliveries_use_cases import CreateDeliveryUseCase, ListDeliveriesUseCase

router = APIRouter()

@router.post("/", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
async def create_delivery(delivery_in: DeliveryCreate, db: AsyncSession = Depends(get_db)):
    repo = DeliveryRepository(db)
    use_case = CreateDeliveryUseCase(repo)
    return await use_case.execute(
        str(delivery_in.factory_id), 
        str(delivery_in.store_id), 
        str(delivery_in.driver_id)
    )

@router.get("/", response_model=List[DeliveryResponse])
async def list_deliveries(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    repo = DeliveryRepository(db)
    use_case = ListDeliveriesUseCase(repo)
    return await use_case.execute(limit=limit, offset=offset)
