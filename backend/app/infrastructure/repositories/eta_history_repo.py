from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.orm.delivery import EtaHistory as EtaHistoryModel
from app.domain.entities.delivery import EtaHistory as EtaHistoryEntity

class EtaHistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, entity: EtaHistoryEntity) -> EtaHistoryEntity:
        db_record = EtaHistoryModel(
            id=entity.id,
            delivery_id=entity.delivery_id,
            eta_before=entity.eta_before,
            eta_after=entity.eta_after,
            reason=entity.reason,
            created_at=entity.created_at,
        )
        self.db.add(db_record)
        await self.db.commit()
        await self.db.refresh(db_record)
        return entity
