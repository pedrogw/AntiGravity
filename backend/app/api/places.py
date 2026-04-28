from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import get_db
from app.schemas.place import FactoryCreate, FactoryResponse, StoreCreate, StoreResponse
from app.infrastructure.repositories.place_repo import PlaceRepository
from app.use_cases.places_use_cases import (
    CreateFactoryUseCase, ListFactoriesUseCase,
    CreateStoreUseCase, ListStoresUseCase
)
from app.api.deps import require_role

router = APIRouter()

@router.post("/factories", response_model=FactoryResponse, status_code=status.HTTP_201_CREATED)
async def create_factory(
    factory_in: FactoryCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(require_role("lojista"))
):
    repo = PlaceRepository(db)
    use_case = CreateFactoryUseCase(repo)
    return await use_case.execute(factory_in.name, factory_in.lat, factory_in.lng)

@router.get("/factories", response_model=List[FactoryResponse])
async def list_factories(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    repo = PlaceRepository(db)
    use_case = ListFactoriesUseCase(repo)
    return await use_case.execute(limit=limit, offset=offset)

@router.post("/stores", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(
    store_in: StoreCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(require_role("lojista"))
):
    repo = PlaceRepository(db)
    use_case = CreateStoreUseCase(repo)
    return await use_case.execute(store_in.name, store_in.lat, store_in.lng, str(store_in.owner_id))

@router.get("/stores", response_model=List[StoreResponse])
async def list_stores(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    repo = PlaceRepository(db)
    use_case = ListStoresUseCase(repo)
    return await use_case.execute(limit=limit, offset=offset)
