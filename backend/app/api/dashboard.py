from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.dashboard import DashboardResponse
from app.infrastructure.repositories.delivery_repo import DeliveryRepository
from app.infrastructure.repositories.alert_repo import AlertRepository
from app.infrastructure.repositories.chaos_repo import ChaosRepository
from app.use_cases.dashboard_use_cases import GetDashboardUseCase
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    delivery_repo = DeliveryRepository(db)
    alert_repo = AlertRepository(db)
    chaos_repo = ChaosRepository(db)
    use_case = GetDashboardUseCase(delivery_repo, alert_repo, chaos_repo)
    return await use_case.execute()
