from typing import List
from app.domain.entities.delivery import Delivery as DeliveryEntity
from app.infrastructure.repositories.delivery_repo import DeliveryRepository

class CreateDeliveryUseCase:
    def __init__(self, repo: DeliveryRepository):
        self.repo = repo

    async def execute(self, factory_id: str, store_id: str, driver_id: str) -> DeliveryEntity:
        delivery = DeliveryEntity(
            factory_id=factory_id,
            store_id=store_id,
            driver_id=driver_id
        )
        return await self.repo.create(delivery)

class ListDeliveriesUseCase:
    def __init__(self, repo: DeliveryRepository):
        self.repo = repo

    async def execute(self, limit: int = 50, offset: int = 0) -> List[DeliveryEntity]:
        return await self.repo.list_all(limit=limit, offset=offset)
