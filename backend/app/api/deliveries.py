from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.session import get_db
from app.models.delivery import Delivery
from app.schemas.delivery import DeliveryCreate, DeliveryResponse

router = APIRouter()

@router.post("/", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
async def create_delivery(delivery_in: DeliveryCreate, db: AsyncSession = Depends(get_db)):
    db_delivery = Delivery(**delivery_in.model_dump())
    db.add(db_delivery)
    await db.commit()
    await db.refresh(db_delivery)
    return db_delivery

@router.get("/", response_model=List[DeliveryResponse])
async def list_deliveries(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Delivery).offset(offset).limit(limit))
    return result.scalars().all()
