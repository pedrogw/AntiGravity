from typing import Type
from app.core.events.base import DomainEvent, EventHandler


class EventBus:
    def __init__(self):
        self._handlers: dict[Type[DomainEvent], list[EventHandler]] = {}

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        handlers = self._handlers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)

    async def publish(self, event: DomainEvent) -> None:
        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            try:
                await handler.handle(event)
            except Exception:
                pass


event_bus = EventBus()
