import uuid
import pytest
from unittest.mock import AsyncMock
from app.domain.events import DeliveryCreatedEvent, DeliveryStatusChangedEvent
from app.infrastructure.events.cache_invalidation_listener import (
    CacheInvalidationListener,
)
from app.infrastructure.cache.cache_service import CACHE_PREFIX


@pytest.fixture
def cache_service():
    return AsyncMock()


class TestCacheInvalidationListener:
    async def test_handle_delivery_created_invalidates(self, cache_service):
        listener = CacheInvalidationListener(cache_service)
        event = DeliveryCreatedEvent(
            delivery_id=uuid.uuid4(),
            factory_id=uuid.uuid4(),
            store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        await listener.handle(event)
        cache_service.invalidate_prefix.assert_awaited_once_with(CACHE_PREFIX)

    async def test_handle_status_changed_invalidates(self, cache_service):
        listener = CacheInvalidationListener(cache_service)
        event = DeliveryStatusChangedEvent(
            delivery_id=uuid.uuid4(),
            old_status="pendente",
            new_status="em_transito",
        )
        await listener.handle(event)
        cache_service.invalidate_prefix.assert_awaited_once_with(CACHE_PREFIX)
