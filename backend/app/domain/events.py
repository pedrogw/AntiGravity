from dataclasses import dataclass
import uuid
from app.core.events.base import DomainEvent


@dataclass(kw_only=True)
class DeliveryCreatedEvent(DomainEvent):
    delivery_id: uuid.UUID
    factory_id: uuid.UUID
    store_id: uuid.UUID
    driver_id: uuid.UUID
    eta_original_iso: str | None = None


@dataclass(kw_only=True)
class DeliveryStatusChangedEvent(DomainEvent):
    delivery_id: uuid.UUID
    old_status: str
    new_status: str


@dataclass(kw_only=True)
class EtaRecalculationRequested(DomainEvent):
    delivery_id: uuid.UUID
    lat: float
    lng: float
    reason: str


@dataclass(kw_only=True)
class AlertCreationRequested(DomainEvent):
    delivery_id: uuid.UUID
    message: str
    is_critical: bool
