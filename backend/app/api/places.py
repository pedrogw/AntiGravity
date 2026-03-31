from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.session import get_db
from app.models.place import Factory, Store
from app.schemas.place import FactoryCreate, FactoryResponse, StoreCreate, StoreResponse

router = APIRouter()

@router.post("/factories", response_model=FactoryResponse, status_code=status.HTTP_201_CREATED)
async def create_factory(factory_in: FactoryCreate, db: AsyncSession = Depends(get_db)):
    db_factory = Factory(**factory_in.model_dump())
    db.add(db_factory)
    await db.commit()
    await db.refresh(db_factory)
    return db_factory

@router.get("/factories", response_model=List[FactoryResponse])
async def list_factories(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Factory).offset(offset).limit(limit))
    return result.scalars().all()

@router.post("/stores", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(store_in: StoreCreate, db: AsyncSession = Depends(get_db)):
    db_store = Store(**store_in.model_dump())
    db.add(db_store)
    await db.commit()
    await db.refresh(db_store)
    return db_store

@router.get("/stores", response_model=List[StoreResponse])
async def list_stores(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Store).offset(offset).limit(limit))
    return result.scalars().all()
