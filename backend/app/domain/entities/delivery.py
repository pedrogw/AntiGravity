import uuid
import datetime
from dataclasses import dataclass, field

@dataclass
class Delivery:
    factory_id: uuid.UUID
    store_id: uuid.UUID
    driver_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: str = "pendente"
    eta_original: datetime.datetime | None = None
    eta_current: datetime.datetime | None = None
    departed_at: datetime.datetime | None = None

@dataclass
class EtaHistory:
    delivery_id: uuid.UUID
    eta_before: datetime.datetime
    eta_after: datetime.datetime
    reason: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
