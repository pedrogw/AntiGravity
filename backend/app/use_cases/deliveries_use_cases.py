from typing import List
from app.domain.entities.delivery import Delivery as DeliveryEntity
from app.domain.repositories.delivery_repo import DeliveryRepositoryProtocol

import uuid

class CreateDeliveryUseCase:
    def __init__(self, repo: DeliveryRepositoryProtocol):
        self.repo = repo

    async def execute(self, factory_id: uuid.UUID, store_id: uuid.UUID, driver_id: uuid.UUID) -> DeliveryEntity:
        delivery = DeliveryEntity(
            factory_id=factory_id,
            store_id=store_id,
            driver_id=driver_id
        )
        return await self.repo.create(delivery)

class ListDeliveriesUseCase:
    def __init__(self, repo: DeliveryRepositoryProtocol):
        self.repo = repo

    async def execute(self, limit: int = 50, offset: int = 0) -> List[DeliveryEntity]:
        return await self.repo.list_all(limit=limit, offset=offset)
