from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid
from app.db.session import get_db
from app.schemas.alert import AlertResponse
from app.infrastructure.repositories.alert_repo import AlertRepository
from app.use_cases.alert_use_cases import ListAlertsUseCase, DismissAlertUseCase
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/alerts", response_model=List[AlertResponse])
async def list_alerts(
    delivery_id: Optional[uuid.UUID] = Query(None, description="Filtrar por entrega"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = AlertRepository(db)
    use_case = ListAlertsUseCase(repo)
    return await use_case.execute(delivery_id=delivery_id, limit=limit, offset=offset)

@router.patch("/alerts/{alert_id}/dismiss", response_model=AlertResponse)
async def dismiss_alert(
    alert_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    repo = AlertRepository(db)
    use_case = DismissAlertUseCase(repo)
    result = await use_case.execute(alert_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    return result
