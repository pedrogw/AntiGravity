from datetime import datetime, timedelta, timezone
from app.domain.entities.delivery import Delivery, EtaHistory
from app.domain.repositories.place_repo import PlaceRepositoryProtocol
from app.domain.repositories.chaos_repo import ChaosRepositoryProtocol
from app.domain.repositories.eta_history_repo import EtaHistoryRepositoryProtocol
from app.domain.value_objects.coordinates import Coordinates
from app.domain.haversine import calculate_haversine_distance, calculate_eta
from app.domain.chaos import apply_chaos_to_eta
from app.core.config import settings


async def recalculate_delivery_eta(
    delivery: Delivery,
    lat: float,
    lng: float,
    place_repo: PlaceRepositoryProtocol,
    chaos_repo: ChaosRepositoryProtocol,
    eta_history_repo: EtaHistoryRepositoryProtocol,
    reason: str,
) -> bool:
    store = await place_repo.get_store_by_id(delivery.store_id)
    if not store:
        return False

    distance = calculate_haversine_distance(
        Coordinates(lat=lat, lng=lng),
        store.location,
    )
    eta_hours = calculate_eta(distance, settings.DEFAULT_SPEED_KMH)
    now = datetime.now(timezone.utc)
    new_eta = now + timedelta(hours=eta_hours)

    active_chaos = await chaos_repo.list_active_by_delivery(delivery.id)
    if active_chaos:
        total_factor = 1.0
        total_delay = 0
        for event in active_chaos:
            total_factor *= event.impact_factor
            total_delay += event.delay_minutes
        new_eta = apply_chaos_to_eta(new_eta, total_factor, total_delay)

    eta_before = delivery.eta_current
    if not delivery.eta_original:
        delivery.eta_original = new_eta
    delivery.eta_current = new_eta

    if eta_before and eta_before != delivery.eta_current:
        history = EtaHistory(
            delivery_id=delivery.id,
            eta_before=eta_before,
            eta_after=delivery.eta_current,
            reason=reason,
        )
        await eta_history_repo.create(history)

    return True
