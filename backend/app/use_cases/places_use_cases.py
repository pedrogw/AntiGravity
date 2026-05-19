import uuid
from typing import List
from app.domain.entities.place import Factory as FactoryEntity, Store as StoreEntity
from app.domain.value_objects.coordinates import Coordinates
from app.domain.repositories.place_repo import PlaceRepositoryProtocol

class CreateFactoryUseCase:
    def __init__(self, repo: PlaceRepositoryProtocol):
        self.repo = repo

    async def execute(self, name: str, lat: float, lng: float) -> FactoryEntity:
        factory = FactoryEntity(name=name, location=Coordinates(lat=lat, lng=lng))
        return await self.repo.create_factory(factory)

class ListFactoriesUseCase:
    def __init__(self, repo: PlaceRepositoryProtocol):
        self.repo = repo

    async def execute(self, limit: int = 50, offset: int = 0) -> List[FactoryEntity]:
        return await self.repo.list_factories(limit=limit, offset=offset)

class CreateStoreUseCase:
    def __init__(self, repo: PlaceRepositoryProtocol):
        self.repo = repo

    async def execute(self, name: str, lat: float, lng: float, owner_id: uuid.UUID) -> StoreEntity:
        store = StoreEntity(name=name, location=Coordinates(lat=lat, lng=lng), owner_id=owner_id)
        return await self.repo.create_store(store)

class ListStoresUseCase:
    def __init__(self, repo: PlaceRepositoryProtocol):
        self.repo = repo

    async def execute(self, limit: int = 50, offset: int = 0) -> List[StoreEntity]:
        return await self.repo.list_stores(limit=limit, offset=offset)
