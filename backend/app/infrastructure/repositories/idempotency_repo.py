from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json
from datetime import datetime, timezone
from app.infrastructure.orm.idempotency_key import IdempotencyKey as IdempotencyKeyModel
from app.domain.entities.chaos import ChaosEventLog as ChaosEventLogEntity
from app.core.config import settings


class IdempotencyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, key: str) -> ChaosEventLogEntity | None:
        result = await self.db.execute(
            select(IdempotencyKeyModel).where(IdempotencyKeyModel.key == key)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None

        cutoff = datetime.now(timezone.utc) - __import__("datetime").timedelta(hours=settings.IDEMPOTENCY_KEY_TTL_HOURS)
        if model.created_at.replace(tzinfo=timezone.utc) < cutoff:
            return None

        data = json.loads(model.response)
        return ChaosEventLogEntity(**data)

    async def save(self, key: str, entity: ChaosEventLogEntity) -> None:
        data = {
            "delivery_id": str(entity.delivery_id),
            "event_type": entity.event_type,
            "impact_factor": entity.impact_factor,
            "delay_minutes": entity.delay_minutes,
            "lat_start": entity.lat_start,
            "lng_start": entity.lng_start,
            "lat_end": entity.lat_end,
            "lng_end": entity.lng_end,
            "id": str(entity.id),
            "timestamp_start": entity.timestamp_start.isoformat(),
            "timestamp_end": entity.timestamp_end.isoformat() if entity.timestamp_end else None,
        }
        model = IdempotencyKeyModel(key=key, response=json.dumps(data, default=str))
        self.db.add(model)
        await self.db.commit()
