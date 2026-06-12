import logging
from app.core.events.base import DomainEvent, EventHandler
from app.domain.events import DeliveryCreatedEvent
from app.infrastructure.cache.cache_service import CacheService, CACHE_PREFIX

logger = logging.getLogger("antigravity.cache")


class CacheInvalidationListener:
    def __init__(self, cache_service: CacheService):
        self.cache_service = cache_service

    async def handle(self, event: DomainEvent) -> None:
        if isinstance(event, DeliveryCreatedEvent):
            deleted = await self.cache_service.invalidate_prefix(CACHE_PREFIX)
            if deleted:
                logger.info("Cache invalidado | prefix=%s keys_removed=%d", CACHE_PREFIX, deleted)
