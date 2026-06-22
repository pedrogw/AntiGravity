from fastapi import APIRouter, Depends, status, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid
from app.db.session import get_db
from app.schemas.chaos import ChaosInject, ChaosResponse
from app.infrastructure.repositories.delivery_repo import DeliveryRepository
from app.infrastructure.repositories.chaos_repo import ChaosRepository
from app.infrastructure.repositories.alert_repo import AlertRepository
from app.infrastructure.repositories.eta_history_repo import EtaHistoryRepository
from app.infrastructure.repositories.place_repo import PlaceRepository
from app.infrastructure.repositories.idempotency_repo import IdempotencyRepository
from app.use_cases.chaos_use_cases import InjectChaosUseCase
from app.api.deps import get_current_user
from app.core.events.bus import event_bus
from app.core.rate_limiter import limiter

router = APIRouter()


@router.post("/deliveries/{delivery_id}/chaos", response_model=ChaosResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def inject_chaos(
    request: Request,
    delivery_id: uuid.UUID,
    chaos_in: ChaosInject,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
):
    delivery_repo = DeliveryRepository(db)
    chaos_repo = ChaosRepository(db)
    alert_repo = AlertRepository(db)
    eta_history_repo = EtaHistoryRepository(db)
    place_repo = PlaceRepository(db)
    idempotency_repo = IdempotencyRepository(db)
    use_case = InjectChaosUseCase(
        delivery_repo, chaos_repo, alert_repo, eta_history_repo, place_repo,
        idempotency_repo=idempotency_repo, event_bus=event_bus,
    )
    return await use_case.execute(
        delivery_id=delivery_id,
        event_type=chaos_in.event_type,
        impact_factor=chaos_in.impact_factor,
        delay_minutes=chaos_in.delay_minutes,
        lat_start=chaos_in.lat_start,
        lng_start=chaos_in.lng_start,
        lat_end=chaos_in.lat_end,
        lng_end=chaos_in.lng_end,
        idempotency_key=idempotency_key,
    )
