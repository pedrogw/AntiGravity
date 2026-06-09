from fastapi import HTTPException, status as http_status
from app.domain.entities.chaos import ChaosEventLog as ChaosEventLogEntity
from app.domain.entities.alert import Alert as AlertEntity
from app.domain.repositories.delivery_repo import DeliveryRepositoryProtocol
from app.domain.repositories.chaos_repo import ChaosRepositoryProtocol
from app.domain.repositories.alert_repo import AlertRepositoryProtocol
from app.domain.repositories.eta_history_repo import EtaHistoryRepositoryProtocol
from app.domain.repositories.place_repo import PlaceRepositoryProtocol
from app.use_cases._eta_recalculation import recalculate_delivery_eta
from app.core.config import settings
import uuid


class InjectChaosUseCase:
    """Injeta evento de caos em uma entrega; recalcula ETA se houver posição e gera alerta se crítico."""
    def __init__(
        self,
        delivery_repo: DeliveryRepositoryProtocol,
        chaos_repo: ChaosRepositoryProtocol,
        alert_repo: AlertRepositoryProtocol,
        eta_history_repo: EtaHistoryRepositoryProtocol,
        place_repo: PlaceRepositoryProtocol,
    ):
        self.delivery_repo = delivery_repo
        self.chaos_repo = chaos_repo
        self.alert_repo = alert_repo
        self.eta_history_repo = eta_history_repo
        self.place_repo = place_repo

    async def execute(
        self,
        delivery_id: uuid.UUID,
        event_type: str,
        impact_factor: float = 1.0,
        delay_minutes: int = 0,
        lat_start: float | None = None,
        lng_start: float | None = None,
        lat_end: float | None = None,
        lng_end: float | None = None,
    ) -> ChaosEventLogEntity:
        delivery = await self.delivery_repo.get_by_id(delivery_id)
        if not delivery:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Entrega não encontrada",
            )

        chaos_event = ChaosEventLogEntity(
            delivery_id=delivery_id,
            event_type=event_type,
            impact_factor=impact_factor,
            delay_minutes=delay_minutes,
            lat_start=lat_start,
            lng_start=lng_start,
            lat_end=lat_end,
            lng_end=lng_end,
        )
        created = await self.chaos_repo.create(chaos_event)

        if delivery.current_lat is not None and delivery.current_lng is not None:
            recalculated = await recalculate_delivery_eta(
                delivery=delivery,
                lat=delivery.current_lat,
                lng=delivery.current_lng,
                place_repo=self.place_repo,
                chaos_repo=self.chaos_repo,
                eta_history_repo=self.eta_history_repo,
                reason="caos_injetado",
            )
            if recalculated:
                await self.delivery_repo.update(delivery)

        is_critical = (
            impact_factor > settings.CHAOS_CRITICAL_FACTOR_THRESHOLD
            or delay_minutes > settings.CHAOS_CRITICAL_DELAY_THRESHOLD
        )
        if is_critical:
            parts = [f"Caos injetado: {event_type}"]
            if delay_minutes > 0:
                parts.append(f"atraso de {delay_minutes}min")
            if impact_factor > settings.CHAOS_CRITICAL_FACTOR_THRESHOLD:
                parts.append(f"fator {impact_factor}x")
            alert = AlertEntity(
                delivery_id=delivery_id,
                message=", ".join(parts),
                is_critical=True,
            )
            await self.alert_repo.create(alert)

        return created
