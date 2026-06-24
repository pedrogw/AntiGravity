import uuid
import datetime
from dataclasses import dataclass, field

@dataclass
class Alert:
    """Alerta gerado por condição crítica (ex: caos com fator > 2.0 ou atraso > 60min)."""
    delivery_id: uuid.UUID
    message: str
    is_critical: bool = False
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    @classmethod
    def from_chaos(
        cls,
        delivery_id: uuid.UUID,
        message: str,
        impact_factor: float,
        delay_minutes: int,
        factor_threshold: float = 2.0,
        delay_threshold: int = 60,
    ) -> "Alert":
        is_critical = impact_factor > factor_threshold or delay_minutes > delay_threshold
        return cls(
            delivery_id=delivery_id,
            message=message,
            is_critical=is_critical,
        )
