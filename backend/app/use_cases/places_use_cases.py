from typing import List
from app.domain.entities.place import Factory as FactoryEntity, Store as StoreEntity
from app.infrastructure.repositories.place_repo import PlaceRepository

class CreateFactoryUseCase:
    def __init__(self, repo: PlaceRepository):
        self.repo = repo

    async def execute(self, name: str, lat: float, lng: float) -> FactoryEntity:
        factory = FactoryEntity(name=name, lat=lat, lng=lng)
        return await self.repo.create_factory(factory)

class ListFactoriesUseCase:
    def __init__(self, repo: PlaceRepository):
        self.repo = repo

    async def execute(self, limit: int = 50, offset: int = 0) -> List[FactoryEntity]:
        return await self.repo.list_factories(limit=limit, offset=offset)

class CreateStoreUseCase:
    def __init__(self, repo: PlaceRepository):
        self.repo = repo

    async def execute(self, name: str, lat: float, lng: float, owner_id: str) -> StoreEntity:
        store = StoreEntity(name=name, lat=lat, lng=lng, owner_id=owner_id)
        return await self.repo.create_store(store)

class ListStoresUseCase:
    def __init__(self, repo: PlaceRepository):
        self.repo = repo

    async def execute(self, limit: int = 50, offset: int = 0) -> List[StoreEntity]:
        return await self.repo.list_stores(limit=limit, offset=offset)
