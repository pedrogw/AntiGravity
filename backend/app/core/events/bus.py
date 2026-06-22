from typing import Optional, Type
from arq.connections import ArqRedis
from app.core.events.base import DomainEvent, EventHandler


class EventBus:
    def __init__(self):
        self._handlers: dict[Type[DomainEvent], list[EventHandler]] = {}
        self.worker_pool: Optional[ArqRedis] = None

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def unsubscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        handlers = self._handlers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)

    async def publish(self, event: DomainEvent) -> None:
        if self.worker_pool is not None:
            from app.infrastructure.worker import enqueue_event
            await enqueue_event(event, self.worker_pool)
            return
        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            try:
                await handler.handle(event)
            except Exception:
                pass


event_bus = EventBus()
