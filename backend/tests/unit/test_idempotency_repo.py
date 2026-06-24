import uuid
import pytest
from datetime import datetime, timezone
from app.domain.entities.chaos import ChaosEventLog as ChaosEventLogEntity
from app.infrastructure.repositories.idempotency_repo import IdempotencyRepository


pytestmark = pytest.mark.anyio


class TestIdempotencyRoundtrip:
    async def test_save_and_get_preserves_types(self, db_session):
        original = ChaosEventLogEntity(
            delivery_id=uuid.uuid4(),
            event_type="acidente",
            impact_factor=1.5,
            delay_minutes=30,
            lat_start=-23.55,
            lng_start=-46.63,
            lat_end=-23.57,
            lng_end=-46.65,
        )
        repo = IdempotencyRepository(db_session)
        key = str(uuid.uuid4())

        await repo.save(key, original)
        retrieved = await repo.get(key)

        assert retrieved is not None
        assert isinstance(retrieved.id, uuid.UUID)
        assert isinstance(retrieved.delivery_id, uuid.UUID)
        assert isinstance(retrieved.timestamp_start, datetime)
        assert retrieved.id == original.id
        assert retrieved.delivery_id == original.delivery_id
        assert retrieved.event_type == original.event_type
        assert retrieved.impact_factor == original.impact_factor
        assert retrieved.delay_minutes == original.delay_minutes
        assert retrieved.lat_start == original.lat_start
        assert retrieved.lng_start == original.lng_start
        assert retrieved.lat_end == original.lat_end
        assert retrieved.lng_end == original.lng_end

    async def test_save_and_get_with_nullable_fields(self, db_session):
        original = ChaosEventLogEntity(
            delivery_id=uuid.uuid4(),
            event_type="engavetamento",
            impact_factor=1.0,
            delay_minutes=0,
        )
        repo = IdempotencyRepository(db_session)
        key = str(uuid.uuid4())

        await repo.save(key, original)
        retrieved = await repo.get(key)

        assert retrieved is not None
        assert isinstance(retrieved.id, uuid.UUID)
        assert isinstance(retrieved.delivery_id, uuid.UUID)
        assert retrieved.lat_start is None
        assert retrieved.lng_start is None
        assert retrieved.lat_end is None
        assert retrieved.lng_end is None
        assert retrieved.timestamp_end is None

    async def test_get_nonexistent_key_returns_none(self, db_session):
        repo = IdempotencyRepository(db_session)
        result = await repo.get("nonexistent-key")
        assert result is None
