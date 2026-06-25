from __future__ import annotations
import uuid
import datetime
from datetime import timedelta, timezone
from typing import ClassVar
from dataclasses import dataclass, field
from app.core.exceptions import InvalidTransitionException
from app.domain.value_objects.coordinates import Coordinates

@dataclass
class Delivery:
    """Entrega com rastreamento de status, posição do motorista e ETA."""
    VALID_TRANSITIONS: ClassVar[dict[str, list[str]]] = {
        "pendente": ["aceita"],
        "aceita": ["em_transito"],
        "em_transito": ["entregue", "cancelada"],
        "entregue": [],
        "cancelada": [],
    }

    factory_id: uuid.UUID
    store_id: uuid.UUID
    driver_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: str = "pendente"
    eta_original: datetime.datetime | None = None
    eta_current: datetime.datetime | None = None
    departed_at: datetime.datetime | None = None
    current_lat: float | None = None
    current_lng: float | None = None

    @staticmethod
    def apply_chaos(current_eta: datetime.datetime, impact_factor: float, delay_minutes: int) -> datetime.datetime:
        if impact_factor < 0:
            raise ValueError("Impact factor cannot be negative")
        if delay_minutes < 0:
            raise ValueError("Delay cannot be negative")

        now = datetime.datetime.now(timezone.utc)
        if current_eta <= now:
            return current_eta + timedelta(minutes=delay_minutes)

        remaining_time = current_eta - now
        new_remaining = remaining_time * impact_factor
        new_eta = now + new_remaining + timedelta(minutes=delay_minutes)
        return new_eta.replace(microsecond=0)

    def recalculate_eta(
        self,
        origin: Coordinates,
        store_location: Coordinates,
        speed_kmh: float,
        chaos_events: list | None = None,
        reason: str = "",
    ) -> EtaHistory | None:
        from app.domain.haversine import calculate_eta

        distance = origin.distance_to(store_location)
        eta_hours = calculate_eta(distance, speed_kmh)
        now = datetime.datetime.now(timezone.utc)
        new_eta = now + datetime.timedelta(hours=eta_hours)

        if chaos_events:
            from app.domain.entities.chaos import ChaosEventLog
            agg = ChaosEventLog.aggregate(chaos_events)
            new_eta = self.apply_chaos(new_eta, agg.total_impact_factor, agg.total_delay_minutes)

        eta_before = self.eta_current
        if not self.eta_original:
            self.eta_original = new_eta
        self.eta_current = new_eta

        if eta_before and eta_before != self.eta_current:
            return EtaHistory(
                delivery_id=self.id,
                eta_before=eta_before,
                eta_after=self.eta_current,
                reason=reason,
            )
        return None

    def update_position(self, lat: float, lng: float) -> None:
        self.current_lat = lat
        self.current_lng = lng

    def change_status(self, new_status: str) -> None:
        allowed = self.VALID_TRANSITIONS.get(self.status, [])
        if new_status not in allowed:
            raise InvalidTransitionException(
                f"Transição inválida: {self.status} -> {new_status}. "
                f"Transições permitidas: {allowed}",
            )
        self.status = new_status
        if new_status == "em_transito" and self.departed_at is None:
            self.departed_at = datetime.datetime.now(datetime.timezone.utc)

@dataclass
class EtaHistory:
    """Registro de alteração do ETA com motivo (posicao_atualizada, caos_injetado)."""
    delivery_id: uuid.UUID
    eta_before: datetime.datetime
    eta_after: datetime.datetime
    reason: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
