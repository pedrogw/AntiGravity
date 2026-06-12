import uuid
import pytest
from unittest.mock import AsyncMock
from app.domain.entities.delivery import Delivery


class TestListDeliveriesWithCache:
    @pytest.fixture
    def mock_repo(self):
        repo = AsyncMock()
        repo.list_all = AsyncMock()
        return repo

    async def test_list_without_cache_queries_db(self, mock_repo):
        from app.use_cases.deliveries_use_cases import ListDeliveriesUseCase
        expected = [Delivery(factory_id=uuid.uuid4(), store_id=uuid.uuid4(), driver_id=uuid.uuid4())]
        mock_repo.list_all.return_value = expected

        use_case = ListDeliveriesUseCase(mock_repo)
        result = await use_case.execute(limit=10, offset=0)

        mock_repo.list_all.assert_awaited_once_with(limit=10, offset=0)
        assert len(result) == 1

    async def test_list_with_cache_hit(self, mock_repo, cache_service):
        from app.use_cases.deliveries_use_cases import ListDeliveriesUseCase
        delivery_id = str(uuid.uuid4())
        cached_data = [{
            "id": delivery_id,
            "factory_id": str(uuid.uuid4()),
            "store_id": str(uuid.uuid4()),
            "driver_id": str(uuid.uuid4()),
            "status": "pendente",
            "eta_original": None,
            "eta_current": None,
            "departed_at": None,
            "current_lat": None,
            "current_lng": None,
        }]
        await cache_service.set_json("deliveries:list:10:0", cached_data)

        use_case = ListDeliveriesUseCase(mock_repo, cache_service=cache_service)
        result = await use_case.execute(limit=10, offset=0)

        mock_repo.list_all.assert_not_awaited()
        assert len(result) == 1
        assert str(result[0].id) == delivery_id

    async def test_list_with_cache_miss(self, mock_repo, cache_service):
        from app.use_cases.deliveries_use_cases import ListDeliveriesUseCase
        expected = [Delivery(factory_id=uuid.uuid4(), store_id=uuid.uuid4(), driver_id=uuid.uuid4())]
        mock_repo.list_all.return_value = expected

        use_case = ListDeliveriesUseCase(mock_repo, cache_service=cache_service)
        result = await use_case.execute(limit=10, offset=0)

        mock_repo.list_all.assert_awaited_once_with(limit=10, offset=0)
        assert len(result) == 1

        cached = await cache_service.get_json("deliveries:list:10:0")
        assert cached is not None
        assert len(cached) == 1
