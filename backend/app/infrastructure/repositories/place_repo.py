from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.infrastructure.orm.place import Factory as FactoryModel, Store as StoreModel
from app.domain.entities.place import Factory as FactoryEntity, Store as StoreEntity

class PlaceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_factory(self, factory_entity: FactoryEntity) -> FactoryEntity:
        db_factory = FactoryModel(
            id=factory_entity.id,
            name=factory_entity.name,
            lat=factory_entity.lat,
            lng=factory_entity.lng
        )
        self.db.add(db_factory)
        await self.db.commit()
        await self.db.refresh(db_factory)
        return self._factory_to_entity(db_factory)

    async def list_factories(self, limit: int = 50, offset: int = 0) -> List[FactoryEntity]:
        result = await self.db.execute(select(FactoryModel).offset(offset).limit(limit))
        models = result.scalars().all()
        return [self._factory_to_entity(m) for m in models]

    async def create_store(self, store_entity: StoreEntity) -> StoreEntity:
        db_store = StoreModel(
            id=store_entity.id,
            name=store_entity.name,
            lat=store_entity.lat,
            lng=store_entity.lng,
            owner_id=store_entity.owner_id
        )
        self.db.add(db_store)
        await self.db.commit()
        await self.db.refresh(db_store)
        return self._store_to_entity(db_store)

    async def list_stores(self, limit: int = 50, offset: int = 0) -> List[StoreEntity]:
        result = await self.db.execute(select(StoreModel).offset(offset).limit(limit))
        models = result.scalars().all()
        return [self._store_to_entity(m) for m in models]

    def _factory_to_entity(self, model: FactoryModel) -> FactoryEntity:
        return FactoryEntity(
            id=model.id,
            name=model.name,
            lat=model.lat,
            lng=model.lng
        )

    def _store_to_entity(self, model: StoreModel) -> StoreEntity:
        return StoreEntity(
            id=model.id,
            name=model.name,
            lat=model.lat,
            lng=model.lng,
            owner_id=model.owner_id
        )
