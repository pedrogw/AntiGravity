import uuid
import datetime
from dataclasses import dataclass, field

@dataclass
class Alert:
    delivery_id: uuid.UUID
    message: str
    is_critical: bool = False
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
