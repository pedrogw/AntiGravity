import logging
from app.core.events.base import DomainEvent
from app.domain.events import DeliveryCreatedEvent, DeliveryStatusChangedEvent

logger = logging.getLogger("antigravity.audit")


class AuditListener:
    async def handle(self, event: DomainEvent) -> None:
        if isinstance(event, DeliveryCreatedEvent):
            logger.info(
                "Audit: Entrega criada | id=%s factory=%s store=%s driver=%s eta=%s",
                event.delivery_id, event.factory_id, event.store_id,
                event.driver_id, event.eta_original_iso,
            )
        elif isinstance(event, DeliveryStatusChangedEvent):
            logger.info(
                "Audit: Status alterado | id=%s de=%s para=%s",
                event.delivery_id, event.old_status, event.new_status,
            )
