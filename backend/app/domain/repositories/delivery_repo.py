from typing import Protocol, List
from app.domain.entities.delivery import Delivery as DeliveryEntity

class DeliveryRepositoryProtocol(Protocol):
    async def create(self, entity: DeliveryEntity) -> DeliveryEntity: ...

    async def list_all(self, limit: int = 50, offset: int = 0) -> List[DeliveryEntity]: ...
