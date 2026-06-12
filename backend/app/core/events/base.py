from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol
import uuid


@dataclass(kw_only=True)
class DomainEvent:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EventHandler(Protocol):
    async def handle(self, event: DomainEvent) -> None: ...
