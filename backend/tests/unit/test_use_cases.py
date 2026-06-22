import uuid
import pytest
from unittest.mock import AsyncMock
from datetime import datetime, timezone

from app.domain.entities.user import User, UserRole
from app.domain.entities.delivery import Delivery
from app.domain.entities.place import Factory, Store
from app.domain.events import AlertCreationRequested, EtaRecalculationRequested
from app.domain.value_objects.coordinates import Coordinates
from app.use_cases.auth_use_cases import RegisterUserUseCase, LoginUserUseCase
from app.use_cases.deliveries_use_cases import (
    CreateDeliveryUseCase, ListDeliveriesUseCase, UpdateDeliveryUseCase,
)
from app.use_cases.places_use_cases import CreateFactoryUseCase, ListFactoriesUseCase, CreateStoreUseCase, ListStoresUseCase


@pytest.fixture
def mock_user_repo():
    repo = AsyncMock()
    repo.get_by_email = AsyncMock()
    repo.create = AsyncMock()
    return repo


@pytest.fixture
def mock_delivery_repo():
    repo = AsyncMock()
    repo.create = AsyncMock()
    repo.list_all = AsyncMock()
    repo.get_by_id = AsyncMock()
    repo.update = AsyncMock()
    repo.count_by_status = AsyncMock()
    return repo


@pytest.fixture
def mock_place_repo():
    repo = AsyncMock()
    repo.create_factory = AsyncMock()
    repo.list_factories = AsyncMock()
    repo.create_store = AsyncMock()
    repo.list_stores = AsyncMock()
    repo.get_store_by_id = AsyncMock()
    repo.get_factory_by_id = AsyncMock()
    return repo


@pytest.fixture
def mock_eta_history_repo():
    repo = AsyncMock()
    repo.create = AsyncMock()
    return repo


@pytest.fixture
def mock_chaos_repo():
    repo = AsyncMock()
    repo.list_active_by_delivery = AsyncMock(return_value=[])
    repo.create = AsyncMock()
    return repo


@pytest.fixture
def mock_alert_repo():
    repo = AsyncMock()
    repo.create = AsyncMock()
    repo.list_all = AsyncMock()
    repo.count_all = AsyncMock()
    return repo


class TestRegisterUserUseCase:
    async def test_register_new_user(self, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None
        mock_user_repo.create.return_value = User(
            email="new@test.com", password_hash="hashed", role=UserRole.lojista
        )

        use_case = RegisterUserUseCase(mock_user_repo)
        result = await use_case.execute("new@test.com", "secret123", UserRole.lojista)

        mock_user_repo.get_by_email.assert_awaited_once_with("new@test.com")
        mock_user_repo.create.assert_awaited_once()
        assert result.email == "new@test.com"
        assert result.role == UserRole.lojista

    async def test_register_duplicate_email_raises_409(self, mock_user_repo):
        mock_user_repo.get_by_email.return_value = User(
            email="dup@test.com", password_hash="h", role=UserRole.lojista
        )

        use_case = RegisterUserUseCase(mock_user_repo)
        with pytest.raises(Exception) as exc:
            await use_case.execute("dup@test.com", "secret123", UserRole.lojista)

        assert exc.value.status_code == 409
        mock_user_repo.create.assert_not_awaited()


class TestLoginUserUseCase:
    async def test_login_success(self, mock_user_repo):
        from app.core.security import get_password_hash
        hashed = get_password_hash("correct_password")
        mock_user_repo.get_by_email.return_value = User(
            email="user@test.com", password_hash=hashed, role=UserRole.lojista
        )

        use_case = LoginUserUseCase(mock_user_repo)
        result = await use_case.execute("user@test.com", "correct_password")

        assert "access_token" in result
        assert result["token_type"] == "bearer"

    async def test_login_invalid_password(self, mock_user_repo):
        from app.core.security import get_password_hash
        hashed = get_password_hash("correct_password")
        mock_user_repo.get_by_email.return_value = User(
            email="user@test.com", password_hash=hashed, role=UserRole.lojista
        )

        use_case = LoginUserUseCase(mock_user_repo)
        with pytest.raises(Exception) as exc:
            await use_case.execute("user@test.com", "wrong_password")

        assert exc.value.status_code == 401

    async def test_login_nonexistent_user(self, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None

        use_case = LoginUserUseCase(mock_user_repo)
        with pytest.raises(Exception) as exc:
            await use_case.execute("nonexistent@test.com", "any_password")

        assert exc.value.status_code == 401


class TestCreateDeliveryUseCase:
    async def test_create_delivery(self, mock_delivery_repo, mock_place_repo):
        factory_id = uuid.uuid4()
        store_id = uuid.uuid4()
        driver_id = uuid.uuid4()
        from app.domain.entities.place import Factory, Store
        from app.domain.value_objects.coordinates import Coordinates
        mock_place_repo.get_factory_by_id = AsyncMock(return_value=Factory(
            name="Fábrica SP", location=Coordinates(lat=-23.55, lng=-46.63),
        ))
        mock_place_repo.get_store_by_id = AsyncMock(return_value=Store(
            name="Loja RJ", location=Coordinates(lat=-22.90, lng=-43.17),
            owner_id=uuid.uuid4(),
        ))
        expected = Delivery(factory_id=factory_id, store_id=store_id, driver_id=driver_id)
        mock_delivery_repo.create.return_value = expected

        use_case = CreateDeliveryUseCase(mock_delivery_repo, mock_place_repo)
        result = await use_case.execute(factory_id, store_id, driver_id)

        mock_place_repo.get_factory_by_id.assert_awaited_once_with(factory_id)
        mock_place_repo.get_store_by_id.assert_awaited_once_with(store_id)
        mock_delivery_repo.create.assert_awaited_once()
        assert result.factory_id == factory_id
        assert result.store_id == store_id
        assert result.driver_id == driver_id
        assert result.status == "pendente"

    async def test_create_delivery_nonexistent_factory_raises_404(self, mock_delivery_repo, mock_place_repo):
        mock_place_repo.get_factory_by_id = AsyncMock(return_value=None)
        use_case = CreateDeliveryUseCase(mock_delivery_repo, mock_place_repo)
        with pytest.raises(Exception) as exc:
            await use_case.execute(uuid.uuid4(), uuid.uuid4(), uuid.uuid4())
        assert exc.value.status_code == 404
        mock_delivery_repo.create.assert_not_awaited()

    async def test_create_delivery_nonexistent_store_raises_404(self, mock_delivery_repo, mock_place_repo):
        from app.domain.entities.place import Factory
        from app.domain.value_objects.coordinates import Coordinates
        mock_place_repo.get_factory_by_id = AsyncMock(return_value=Factory(
            name="Fábrica", location=Coordinates(lat=-23.0, lng=-46.0),
        ))
        mock_place_repo.get_store_by_id = AsyncMock(return_value=None)
        use_case = CreateDeliveryUseCase(mock_delivery_repo, mock_place_repo)
        with pytest.raises(Exception) as exc:
            await use_case.execute(uuid.uuid4(), uuid.uuid4(), uuid.uuid4())
        assert exc.value.status_code == 404
        mock_delivery_repo.create.assert_not_awaited()

    async def test_create_delivery_calculates_eta(self, mock_delivery_repo, mock_place_repo):
        factory_id = uuid.uuid4()
        store_id = uuid.uuid4()
        driver_id = uuid.uuid4()
        from app.domain.entities.place import Factory, Store
        from app.domain.value_objects.coordinates import Coordinates
        mock_place_repo.get_factory_by_id = AsyncMock(return_value=Factory(
            name="Fábrica SP", location=Coordinates(lat=-23.55, lng=-46.63),
        ))
        mock_place_repo.get_store_by_id = AsyncMock(return_value=Store(
            name="Loja RJ", location=Coordinates(lat=-22.90, lng=-43.17),
            owner_id=uuid.uuid4(),
        ))

        def create_side_effect(entity):
            return entity
        mock_delivery_repo.create.side_effect = create_side_effect

        use_case = CreateDeliveryUseCase(mock_delivery_repo, mock_place_repo)
        result = await use_case.execute(factory_id, store_id, driver_id)

        assert result.eta_original is not None
        assert result.eta_current is not None
        assert result.eta_original == result.eta_current


class TestListDeliveriesUseCase:
    async def test_list_deliveries(self, mock_delivery_repo):
        deliveries = [Delivery(factory_id=uuid.uuid4(), store_id=uuid.uuid4(), driver_id=uuid.uuid4())]
        mock_delivery_repo.list_all.return_value = deliveries

        use_case = ListDeliveriesUseCase(mock_delivery_repo)
        result = await use_case.execute(limit=10, offset=0)

        mock_delivery_repo.list_all.assert_awaited_once_with(limit=10, offset=0)
        assert len(result) == 1


class TestPlacesUseCases:
    async def test_create_factory(self, mock_place_repo):
        expected = Factory(name="F1", location=Coordinates(lat=-23.0, lng=-46.0))
        mock_place_repo.create_factory.return_value = expected

        use_case = CreateFactoryUseCase(mock_place_repo)
        result = await use_case.execute("F1", -23.0, -46.0)

        mock_place_repo.create_factory.assert_awaited_once()
        assert result.name == "F1"
        assert result.location.lat == -23.0

    async def test_list_factories(self, mock_place_repo):
        mock_place_repo.list_factories.return_value = [
            Factory(name="F1", location=Coordinates(lat=0.0, lng=0.0))
        ]
        use_case = ListFactoriesUseCase(mock_place_repo)
        result = await use_case.execute()
        assert len(result) == 1

    async def test_create_store(self, mock_place_repo):
        owner_id = uuid.uuid4()
        expected = Store(name="S1", location=Coordinates(lat=-23.0, lng=-46.0), owner_id=owner_id)
        mock_place_repo.create_store.return_value = expected

        use_case = CreateStoreUseCase(mock_place_repo)
        result = await use_case.execute("S1", -23.0, -46.0, owner_id)

        mock_place_repo.create_store.assert_awaited_once()
        assert result.owner_id == owner_id

    async def test_list_stores(self, mock_place_repo):
        mock_place_repo.list_stores.return_value = [
            Store(name="S1", location=Coordinates(lat=0.0, lng=0.0), owner_id=uuid.uuid4())
        ]
        use_case = ListStoresUseCase(mock_place_repo)
        result = await use_case.execute()
        assert len(result) == 1


class TestUpdateDeliveryUseCase:
    async def test_update_status_only(self, mock_delivery_repo, mock_place_repo, mock_eta_history_repo, mock_chaos_repo):
        delivery_id = uuid.uuid4()
        existing = Delivery(id=delivery_id, factory_id=uuid.uuid4(), store_id=uuid.uuid4(), driver_id=uuid.uuid4())
        mock_delivery_repo.get_by_id.return_value = existing
        mock_delivery_repo.update.return_value = Delivery(
            id=delivery_id, factory_id=existing.factory_id, store_id=existing.store_id,
            driver_id=existing.driver_id, status="em_transito",
            departed_at=datetime.now(timezone.utc),
        )

        driver_id = uuid.uuid4()
        existing.driver_id = driver_id
        use_case = UpdateDeliveryUseCase(mock_delivery_repo, mock_place_repo, mock_eta_history_repo, mock_chaos_repo, event_bus=None)
        result = await use_case.execute(delivery_id, current_user_id=driver_id, status="em_transito")

        mock_delivery_repo.get_by_id.assert_awaited_once_with(delivery_id)
        mock_delivery_repo.update.assert_awaited_once()
        assert result.status == "em_transito"

    async def test_update_nonexistent_raises_404(self, mock_delivery_repo, mock_place_repo, mock_eta_history_repo, mock_chaos_repo):
        mock_delivery_repo.get_by_id.return_value = None

        use_case = UpdateDeliveryUseCase(mock_delivery_repo, mock_place_repo, mock_eta_history_repo, mock_chaos_repo, event_bus=None)
        with pytest.raises(Exception) as exc:
            await use_case.execute(uuid.uuid4(), current_user_id=uuid.uuid4(), status="em_transito")

        assert exc.value.status_code == 404

    async def test_update_invalid_status_transition_raises_422(self, mock_delivery_repo, mock_place_repo, mock_eta_history_repo, mock_chaos_repo):
        delivery_id = uuid.uuid4()
        driver_id = uuid.uuid4()
        existing = Delivery(
            id=delivery_id, factory_id=uuid.uuid4(), store_id=uuid.uuid4(),
            driver_id=driver_id, status="entregue",
        )
        mock_delivery_repo.get_by_id.return_value = existing

        use_case = UpdateDeliveryUseCase(mock_delivery_repo, mock_place_repo, mock_eta_history_repo, mock_chaos_repo, event_bus=None)
        with pytest.raises(Exception) as exc:
            await use_case.execute(delivery_id, current_user_id=driver_id, status="pendente")

        assert exc.value.status_code == 422

    async def test_update_location_recalculates_eta(self, mock_delivery_repo, mock_place_repo, mock_eta_history_repo, mock_chaos_repo):
        store_id = uuid.uuid4()
        delivery_id = uuid.uuid4()
        driver_id = uuid.uuid4()
        existing = Delivery(id=delivery_id, factory_id=uuid.uuid4(), store_id=store_id, driver_id=driver_id)
        mock_delivery_repo.get_by_id.return_value = existing

        mock_place_repo.get_store_by_id.return_value = Store(
            name="Loja Destino", location=Coordinates(lat=-23.5, lng=-46.6), owner_id=uuid.uuid4(),
        )

        def update_side_effect(entity):
            return entity
        mock_delivery_repo.update.side_effect = update_side_effect

        use_case = UpdateDeliveryUseCase(mock_delivery_repo, mock_place_repo, mock_eta_history_repo, mock_chaos_repo, event_bus=None)
        result = await use_case.execute(delivery_id, current_user_id=driver_id, lat=-23.55, lng=-46.63)

        mock_place_repo.get_store_by_id.assert_awaited_once_with(store_id)
        mock_chaos_repo.list_active_by_delivery.assert_awaited_once_with(delivery_id)
        assert result.eta_current is not None
        assert result.eta_original is not None
        assert result.current_lat == -23.55
        assert result.current_lng == -46.63


class TestInjectChaosUseCase:
    async def test_inject_chaos_on_nonexistent_delivery_raises_404(
        self, mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
        mock_eta_history_repo, mock_place_repo,
    ):
        mock_delivery_repo.get_by_id.return_value = None
        from app.use_cases.chaos_use_cases import InjectChaosUseCase

        use_case = InjectChaosUseCase(
            mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
            mock_eta_history_repo, mock_place_repo,
            event_bus=None,
        )
        with pytest.raises(Exception) as exc:
            await use_case.execute(delivery_id=uuid.uuid4(), event_type="engarrafamento")

        assert exc.value.status_code == 404
        mock_chaos_repo.create.assert_not_awaited()

    async def test_inject_chaos_creates_event(
        self, mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
        mock_eta_history_repo, mock_place_repo,
    ):
        delivery_id = uuid.uuid4()
        existing = Delivery(
            id=delivery_id, factory_id=uuid.uuid4(), store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        mock_delivery_repo.get_by_id.return_value = existing
        from app.domain.entities.chaos import ChaosEventLog
        expected_entity = ChaosEventLog(delivery_id=delivery_id, event_type="acidente")
        mock_chaos_repo.create.return_value = expected_entity
        from app.use_cases.chaos_use_cases import InjectChaosUseCase

        use_case = InjectChaosUseCase(
            mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
            mock_eta_history_repo, mock_place_repo,
            event_bus=None,
        )
        result = await use_case.execute(delivery_id=delivery_id, event_type="acidente")

        mock_chaos_repo.create.assert_awaited_once()
        assert result.event_type == "acidente"
        assert result.delivery_id == delivery_id

    async def test_inject_chaos_recalculates_eta_when_delivery_has_position(
        self, mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
        mock_eta_history_repo, mock_place_repo,
    ):
        store_id = uuid.uuid4()
        delivery_id = uuid.uuid4()
        existing = Delivery(
            id=delivery_id, factory_id=uuid.uuid4(), store_id=store_id,
            driver_id=uuid.uuid4(), current_lat=-23.55, current_lng=-46.63,
        )
        mock_delivery_repo.get_by_id.return_value = existing
        from app.domain.entities.chaos import ChaosEventLog
        mock_chaos_repo.create.return_value = ChaosEventLog(
            delivery_id=delivery_id, event_type="acidente",
        )
        mock_chaos_repo.list_active_by_delivery.return_value = []
        mock_place_repo.get_store_by_id.return_value = Store(
            name="Loja", location=Coordinates(lat=-23.5, lng=-46.6),
            owner_id=uuid.uuid4(),
        )

        def update_side_effect(entity):
            return entity
        mock_delivery_repo.update.side_effect = update_side_effect
        from app.use_cases.chaos_use_cases import InjectChaosUseCase

        use_case = InjectChaosUseCase(
            mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
            mock_eta_history_repo, mock_place_repo,
            event_bus=None,
        )
        result = await use_case.execute(delivery_id=delivery_id, event_type="acidente")

        mock_delivery_repo.update.assert_awaited_once()
        assert result.event_type == "acidente"
        updated = mock_delivery_repo.update.call_args[0][0]
        assert updated.eta_current is not None

    async def test_inject_critical_chaos_creates_alert(
        self, mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
        mock_eta_history_repo, mock_place_repo,
    ):
        delivery_id = uuid.uuid4()
        existing = Delivery(
            id=delivery_id, factory_id=uuid.uuid4(), store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        mock_delivery_repo.get_by_id.return_value = existing
        from app.domain.entities.chaos import ChaosEventLog
        mock_chaos_repo.create.return_value = ChaosEventLog(
            delivery_id=delivery_id, event_type="deslizamento",
        )
        from app.use_cases.chaos_use_cases import InjectChaosUseCase

        use_case = InjectChaosUseCase(
            mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
            mock_eta_history_repo, mock_place_repo,
            event_bus=None,
        )
        await use_case.execute(
            delivery_id=delivery_id, event_type="deslizamento",
            impact_factor=3.0, delay_minutes=90,
        )

        mock_alert_repo.create.assert_awaited_once()

    async def test_inject_chaos_skips_alert_when_not_critical(
        self, mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
        mock_eta_history_repo, mock_place_repo,
    ):
        delivery_id = uuid.uuid4()
        existing = Delivery(
            id=delivery_id, factory_id=uuid.uuid4(), store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        mock_delivery_repo.get_by_id.return_value = existing
        from app.domain.entities.chaos import ChaosEventLog
        mock_chaos_repo.create.return_value = ChaosEventLog(
            delivery_id=delivery_id, event_type="chuva",
        )
        from app.use_cases.chaos_use_cases import InjectChaosUseCase

        use_case = InjectChaosUseCase(
            mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
            mock_eta_history_repo, mock_place_repo,
            event_bus=None,
        )
        await use_case.execute(
            delivery_id=delivery_id, event_type="chuva",
            impact_factor=1.5, delay_minutes=10,
        )

        mock_alert_repo.create.assert_not_awaited()

    async def test_inject_chaos_idempotency_key_returns_cached(
        self, mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
        mock_eta_history_repo, mock_place_repo,
    ):
        delivery_id = uuid.uuid4()
        existing = Delivery(
            id=delivery_id, factory_id=uuid.uuid4(), store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        mock_delivery_repo.get_by_id.return_value = existing
        from app.domain.entities.chaos import ChaosEventLog
        cached_entity = ChaosEventLog(delivery_id=delivery_id, event_type="acidente")
        mock_idempotency = AsyncMock()
        mock_idempotency.get.return_value = cached_entity
        from app.use_cases.chaos_use_cases import InjectChaosUseCase

        use_case = InjectChaosUseCase(
            mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
            mock_eta_history_repo, mock_place_repo,
            idempotency_repo=mock_idempotency, event_bus=None,
        )
        result = await use_case.execute(
            delivery_id=delivery_id, event_type="acidente",
            idempotency_key="key-123",
        )

        mock_idempotency.get.assert_awaited_once_with("key-123")
        mock_chaos_repo.create.assert_not_awaited()
        assert result is cached_entity

    async def test_inject_chaos_idempotency_key_saves_on_first_call(
        self, mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
        mock_eta_history_repo, mock_place_repo,
    ):
        delivery_id = uuid.uuid4()
        existing = Delivery(
            id=delivery_id, factory_id=uuid.uuid4(), store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        mock_delivery_repo.get_by_id.return_value = existing
        from app.domain.entities.chaos import ChaosEventLog
        expected_entity = ChaosEventLog(delivery_id=delivery_id, event_type="acidente")
        mock_chaos_repo.create.return_value = expected_entity
        mock_idempotency = AsyncMock()
        mock_idempotency.get.return_value = None
        from app.use_cases.chaos_use_cases import InjectChaosUseCase

        use_case = InjectChaosUseCase(
            mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
            mock_eta_history_repo, mock_place_repo,
            idempotency_repo=mock_idempotency, event_bus=None,
        )
        result = await use_case.execute(
            delivery_id=delivery_id, event_type="acidente",
            idempotency_key="key-456",
        )

        mock_idempotency.get.assert_awaited_once_with("key-456")
        mock_idempotency.save.assert_awaited_once()
        mock_chaos_repo.create.assert_awaited_once()
        assert result.event_type == "acidente"


class TestListAlertsUseCase:
    async def test_list_alerts_empty(self):
        from app.use_cases.alert_use_cases import ListAlertsUseCase
        mock_repo = AsyncMock()
        mock_repo.list_all = AsyncMock(return_value=[])

        use_case = ListAlertsUseCase(mock_repo)
        result = await use_case.execute()

        mock_repo.list_all.assert_awaited_once_with(delivery_id=None, limit=50, offset=0)
        assert result == []

    async def test_list_alerts_with_delivery_filter(self):
        delivery_id = uuid.uuid4()
        from app.domain.entities.alert import Alert
        from app.use_cases.alert_use_cases import ListAlertsUseCase
        mock_repo = AsyncMock()
        expected = [
            Alert(delivery_id=delivery_id, message="Alerta crítico", is_critical=True),
        ]
        mock_repo.list_all = AsyncMock(return_value=expected)

        use_case = ListAlertsUseCase(mock_repo)
        result = await use_case.execute(delivery_id=delivery_id)

        mock_repo.list_all.assert_awaited_once_with(delivery_id=delivery_id, limit=50, offset=0)
        assert len(result) == 1
        assert result[0].delivery_id == delivery_id
        assert result[0].message == "Alerta crítico"


class TestGetDashboardUseCase:
    async def test_dashboard_returns_aggregated_data(
        self, mock_delivery_repo, mock_alert_repo, mock_chaos_repo,
    ):
        mock_delivery_repo.count_by_status.return_value = {
            "pendente": 5, "em_transito": 3, "entregue": 10, "cancelada": 2,
        }
        mock_delivery_repo.count_delayed.return_value = 2
        mock_alert_repo.count_all.side_effect = [25, 3]
        mock_chaos_repo.count_active.return_value = 7
        mock_chaos_repo.count_by_type.return_value = {"deslizamento": 3, "engarrafamento": 4}
        from app.use_cases.dashboard_use_cases import GetDashboardUseCase

        use_case = GetDashboardUseCase(mock_delivery_repo, mock_alert_repo, mock_chaos_repo)
        result = await use_case.execute()

        assert result.total_deliveries == 20
        assert len(result.deliveries_by_status) == 4
        assert result.delayed_deliveries == 2
        assert result.total_alerts == 25
        assert result.critical_alerts == 3
        assert result.active_chaos_events == 7
        assert len(result.chaos_by_type) == 2
        mock_alert_repo.count_all.assert_any_call()
        mock_alert_repo.count_all.assert_any_call(is_critical=True)


class TestEtaRecalculationAsyncPath:
    """Testa o path assíncrono (event_bus.worker_pool setado) — enfileira evento em vez de recalcular inline."""

    async def test_update_delivery_enqueues_when_worker_pool_set(
        self, mock_delivery_repo, mock_place_repo, mock_eta_history_repo, mock_chaos_repo,
    ):
        delivery_id = uuid.uuid4()
        driver_id = uuid.uuid4()
        existing = Delivery(id=delivery_id, factory_id=uuid.uuid4(), store_id=uuid.uuid4(), driver_id=driver_id)
        mock_delivery_repo.get_by_id.return_value = existing
        mock_delivery_repo.update.side_effect = lambda e: e

        mock_event_bus = AsyncMock()
        mock_event_bus.worker_pool = AsyncMock()

        use_case = UpdateDeliveryUseCase(
            mock_delivery_repo, mock_place_repo, mock_eta_history_repo,
            mock_chaos_repo, event_bus=mock_event_bus,
        )
        result = await use_case.execute(delivery_id, current_user_id=driver_id, lat=-23.55, lng=-46.63)

        mock_event_bus.publish.assert_awaited_once()
        args = mock_event_bus.publish.call_args
        published = args[0][0]
        assert isinstance(published, EtaRecalculationRequested)
        assert published.delivery_id == delivery_id
        assert published.lat == -23.55
        assert published.lng == -46.63
        assert published.reason == "posicao_atualizada"
        mock_place_repo.get_store_by_id.assert_not_awaited()
        assert result.current_lat == -23.55
        assert result.current_lng == -46.63

    async def test_inject_chaos_enqueues_when_worker_pool_set(
        self, mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
        mock_eta_history_repo, mock_place_repo,
    ):
        delivery_id = uuid.uuid4()
        existing = Delivery(
            id=delivery_id, factory_id=uuid.uuid4(), store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(), current_lat=-23.55, current_lng=-46.63,
        )
        mock_delivery_repo.get_by_id.return_value = existing
        from app.domain.entities.chaos import ChaosEventLog
        mock_chaos_repo.create.return_value = ChaosEventLog(delivery_id=delivery_id, event_type="acidente")
        from app.use_cases.chaos_use_cases import InjectChaosUseCase

        mock_event_bus = AsyncMock()
        mock_event_bus.worker_pool = AsyncMock()

        use_case = InjectChaosUseCase(
            mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
            mock_eta_history_repo, mock_place_repo,
            event_bus=mock_event_bus,
        )
        result = await use_case.execute(delivery_id=delivery_id, event_type="acidente")

        mock_event_bus.publish.assert_awaited_once()
        args = mock_event_bus.publish.call_args
        published = args[0][0]
        assert isinstance(published, EtaRecalculationRequested)
        assert published.delivery_id == delivery_id
        assert published.lat == -23.55
        assert published.lng == -46.63
        assert published.reason == "caos_injetado"
        mock_delivery_repo.update.assert_not_awaited()
        mock_place_repo.get_store_by_id.assert_not_awaited()

    async def test_inject_critical_chaos_enqueues_alert_when_worker_pool_set(
        self, mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
        mock_eta_history_repo, mock_place_repo,
    ):
        delivery_id = uuid.uuid4()
        existing = Delivery(
            id=delivery_id, factory_id=uuid.uuid4(), store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        mock_delivery_repo.get_by_id.return_value = existing
        from app.domain.entities.chaos import ChaosEventLog
        mock_chaos_repo.create.return_value = ChaosEventLog(delivery_id=delivery_id, event_type="deslizamento")
        from app.use_cases.chaos_use_cases import InjectChaosUseCase

        mock_event_bus = AsyncMock()
        mock_event_bus.worker_pool = AsyncMock()

        use_case = InjectChaosUseCase(
            mock_delivery_repo, mock_chaos_repo, mock_alert_repo,
            mock_eta_history_repo, mock_place_repo,
            event_bus=mock_event_bus,
        )
        await use_case.execute(
            delivery_id=delivery_id, event_type="deslizamento",
            impact_factor=3.0, delay_minutes=90,
        )

        alert_published = [
            args[0][0] for args in mock_event_bus.publish.call_args_list
            if isinstance(args[0][0], AlertCreationRequested)
        ]
        assert len(alert_published) == 1
        assert alert_published[0].delivery_id == delivery_id
        assert alert_published[0].is_critical is True
        mock_alert_repo.create.assert_not_awaited()
