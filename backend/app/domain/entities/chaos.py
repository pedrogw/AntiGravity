import uuid
import datetime
from dataclasses import dataclass, field


@dataclass
class ChaosAggregate:
    """Resultado da agregação de múltiplos eventos de caos."""
    total_impact_factor: float
    total_delay_minutes: int
    event_count: int
    count_by_type: dict[str, int]


@dataclass
class ChaosEventLog:
    """Evento de caos ativo ou finalizado que impacta o ETA de uma entrega."""
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

    @staticmethod
    def aggregate(events: list["ChaosEventLog"]) -> ChaosAggregate:
        total_factor = 1.0
        total_delay = 0
        count_by_type: dict[str, int] = {}
        for event in events:
            total_factor *= event.impact_factor
            total_delay += event.delay_minutes
            count_by_type[event.event_type] = count_by_type.get(event.event_type, 0) + 1
        return ChaosAggregate(
            total_impact_factor=total_factor,
            total_delay_minutes=total_delay,
            event_count=len(events),
            count_by_type=count_by_type,
        )
