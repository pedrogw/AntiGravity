from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.infrastructure.orm.delivery import Delivery as DeliveryModel
from app.domain.entities.delivery import Delivery as DeliveryEntity

class DeliveryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, entity: DeliveryEntity) -> DeliveryEntity:
        db_delivery = DeliveryModel(
            id=entity.id,
            factory_id=entity.factory_id,
            store_id=entity.store_id,
            driver_id=entity.driver_id,
            status=entity.status,
            eta_original=entity.eta_original,
            eta_current=entity.eta_current,
            departed_at=entity.departed_at
        )
        self.db.add(db_delivery)
        await self.db.commit()
        await self.db.refresh(db_delivery)
        return self._to_entity(db_delivery)

    async def list_all(self, limit: int = 50, offset: int = 0) -> List[DeliveryEntity]:
        result = await self.db.execute(select(DeliveryModel).offset(offset).limit(limit))
        models = result.scalars().all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: DeliveryModel) -> DeliveryEntity:
        return DeliveryEntity(
            id=model.id,
            factory_id=model.factory_id,
            store_id=model.store_id,
            driver_id=model.driver_id,
            status=model.status,
            eta_original=model.eta_original,
            eta_current=model.eta_current,
            departed_at=model.departed_at
        )
