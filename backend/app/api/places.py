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

def map_factory(f) -> FactoryResponse:
    return FactoryResponse(id=f.id, name=f.name, lat=f.location.lat, lng=f.location.lng)

def map_store(s) -> StoreResponse:
    return StoreResponse(id=s.id, name=s.name, lat=s.location.lat, lng=s.location.lng, owner_id=s.owner_id)

@router.post("/factories", response_model=FactoryResponse, status_code=status.HTTP_201_CREATED)
async def create_factory(
    factory_in: FactoryCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(require_role("lojista"))
):
    repo = PlaceRepository(db)
    use_case = CreateFactoryUseCase(repo)
    result = await use_case.execute(factory_in.name, factory_in.lat, factory_in.lng)
    return map_factory(result)

@router.get("/factories", response_model=List[FactoryResponse])
async def list_factories(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    repo = PlaceRepository(db)
    use_case = ListFactoriesUseCase(repo)
    results = await use_case.execute(limit=limit, offset=offset)
    return [map_factory(f) for f in results]

@router.post("/stores", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
async def create_store(
    store_in: StoreCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: dict = Depends(require_role("lojista"))
):
    repo = PlaceRepository(db)
    use_case = CreateStoreUseCase(repo)
    result = await use_case.execute(store_in.name, store_in.lat, store_in.lng, store_in.owner_id)
    return map_store(result)

@router.get("/stores", response_model=List[StoreResponse])
async def list_stores(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    repo = PlaceRepository(db)
    use_case = ListStoresUseCase(repo)
    results = await use_case.execute(limit=limit, offset=offset)
    return [map_store(s) for s in results]
