import pytest
from dataclasses import dataclass
from unittest.mock import AsyncMock
from app.core.events.base import DomainEvent
from app.core.events.bus import EventBus
from app.domain.events import DeliveryCreatedEvent, DeliveryStatusChangedEvent
import uuid


@dataclass(kw_only=True)
class FakeEvent(DomainEvent):
    value: str = ""


@pytest.fixture
def event_bus():
    return EventBus()


class TestEventBus:
    async def test_publish_dispatches_to_subscribed_handler(self, event_bus):
        handler = AsyncMock()
        event_bus.subscribe(FakeEvent, handler)
        event = FakeEvent(value="hello")
        await event_bus.publish(event)
        handler.handle.assert_awaited_once_with(event)

    async def test_publish_skips_unsubscribed_events(self, event_bus):
        handler = AsyncMock()
        event_bus.subscribe(FakeEvent, handler)
        event_bus.unsubscribe(FakeEvent, handler)
        await event_bus.publish(FakeEvent(value="x"))
        handler.handle.assert_not_awaited()

    async def test_publish_dispatches_to_multiple_handlers(self, event_bus):
        handler1 = AsyncMock()
        handler2 = AsyncMock()
        event_bus.subscribe(FakeEvent, handler1)
        event_bus.subscribe(FakeEvent, handler2)
        event = FakeEvent(value="multi")
        await event_bus.publish(event)
        handler1.handle.assert_awaited_once_with(event)
        handler2.handle.assert_awaited_once_with(event)

    async def test_publish_isolates_handler_failure(self, event_bus):
        good = AsyncMock()

        class FailingHandler:
            async def handle(self, event):  # type: ignore
                raise RuntimeError("fail")

        event_bus.subscribe(FakeEvent, FailingHandler())
        event_bus.subscribe(FakeEvent, good)
        event = FakeEvent(value="fail")
        await event_bus.publish(event)
        good.handle.assert_awaited_once_with(event)

    async def test_publish_no_handlers_does_nothing(self, event_bus):
        await event_bus.publish(FakeEvent(value="orphan"))


class TestDomainEvents:
    def test_delivery_created_event(self):
        e = DeliveryCreatedEvent(
            delivery_id=uuid.uuid4(),
            factory_id=uuid.uuid4(),
            store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        assert e.delivery_id is not None
        assert e.id is not None
        assert e.occurred_at is not None

    def test_delivery_status_changed_event(self):
        e = DeliveryStatusChangedEvent(
            delivery_id=uuid.uuid4(),
            old_status="pendente",
            new_status="em_transito",
        )
        assert e.old_status == "pendente"
        assert e.new_status == "em_transito"
