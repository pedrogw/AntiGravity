from typing import List, Optional
import uuid
from app.domain.entities.alert import Alert as AlertEntity
from app.domain.repositories.alert_repo import AlertRepositoryProtocol


class ListAlertsUseCase:
    """Retorna alertas com filtro opcional por delivery_id e paginação."""
    def __init__(self, alert_repo: AlertRepositoryProtocol):
        self.alert_repo = alert_repo

    async def execute(
        self,
        delivery_id: Optional[uuid.UUID] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[AlertEntity]:
        return await self.alert_repo.list_all(
            delivery_id=delivery_id, limit=limit, offset=offset,
        )
