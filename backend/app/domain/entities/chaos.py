import uuid
import datetime
from dataclasses import dataclass, field

@dataclass
class ChaosEventLog:
    delivery_id: uuid.UUID
    event_type: str
    impact_factor: float = 1.0
    delay_minutes: int = 0
    lat_start: float | None = None
    lng_start: float | None = None
    lat_end: float | None = None
    lng_end: float | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp_start: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    timestamp_end: datetime.datetime | None = None
