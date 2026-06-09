from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
import uuid
from app.infrastructure.orm.alert import Alert as AlertModel
from app.domain.entities.alert import Alert as AlertEntity

class AlertRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, entity: AlertEntity) -> AlertEntity:
        model = AlertModel(
            id=entity.id,
            delivery_id=entity.delivery_id,
            message=entity.message,
            is_critical=entity.is_critical,
            created_at=entity.created_at,
        )
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return entity

    async def list_all(self, delivery_id: Optional[uuid.UUID] = None, limit: int = 50, offset: int = 0) -> List[AlertEntity]:
        stmt = select(AlertModel).order_by(desc(AlertModel.created_at)).limit(limit).offset(offset)
        if delivery_id is not None:
            stmt = stmt.where(AlertModel.delivery_id == delivery_id)
        result = await self.db.execute(stmt)
        models = result.scalars().all()
        return [
            AlertEntity(
                id=m.id,
                delivery_id=m.delivery_id,
                message=m.message,
                is_critical=m.is_critical,
                created_at=m.created_at,
            )
            for m in models
        ]

    async def count_all(self, is_critical: Optional[bool] = None) -> int:
        stmt = select(func.count(AlertModel.id))
        if is_critical is not None:
            stmt = stmt.where(AlertModel.is_critical == is_critical)
        result = await self.db.execute(stmt)
        return result.scalar() or 0
