import uuid
from unittest.mock import AsyncMock, patch


from app.domain.entities.delivery import Delivery
from app.domain.events import (
    AlertCreationRequested,
    DeliveryCreatedEvent,
    DeliveryStatusChangedEvent,
    EtaRecalculationRequested,
)
from app.infrastructure.worker import (
    deserialize_event,
    enqueue_event,
    handle_domain_event,
    serialize_event,
)


class TestSerialization:
    def test_roundtrip_delivery_created_event(self):
        original = DeliveryCreatedEvent(
            delivery_id=uuid.uuid4(),
            factory_id=uuid.uuid4(),
            store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
            eta_original_iso="2024-01-01T12:00:00+00:00",
        )
        payload = serialize_event(original)
        restored = deserialize_event(payload)
        assert restored is not None
        assert restored.id == original.id
        assert restored.delivery_id == original.delivery_id
        assert restored.factory_id == original.factory_id
        assert restored.store_id == original.store_id
        assert restored.driver_id == original.driver_id
        assert restored.eta_original_iso == original.eta_original_iso
        assert restored.occurred_at == original.occurred_at
        assert type(restored) is DeliveryCreatedEvent

    def test_roundtrip_delivery_created_event_without_eta(self):
        original = DeliveryCreatedEvent(
            delivery_id=uuid.uuid4(),
            factory_id=uuid.uuid4(),
            store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        payload = serialize_event(original)
        restored = deserialize_event(payload)
        assert restored is not None
        assert restored.eta_original_iso is None

    def test_roundtrip_delivery_status_changed_event(self):
        original = DeliveryStatusChangedEvent(
            delivery_id=uuid.uuid4(),
            old_status="pendente",
            new_status="em_transito",
        )
        payload = serialize_event(original)
        restored = deserialize_event(payload)
        assert restored is not None
        assert restored.id == original.id
        assert restored.delivery_id == original.delivery_id
        assert restored.old_status == original.old_status
        assert restored.new_status == original.new_status
        assert type(restored) is DeliveryStatusChangedEvent

    def test_deserialize_unknown_event_type_returns_none(self):
        payload = '{"event_type": "UnknownEvent", "event_data": {}}'
        assert deserialize_event(payload) is None

    def test_deserialize_invalid_json_returns_none(self):
        assert deserialize_event("not json") is None


class TestHandleDomainEvent:
    async def test_handle_delivery_created_event_logs_audit(self, caplog):
        caplog.set_level("INFO")
        event = DeliveryCreatedEvent(
            delivery_id=uuid.uuid4(),
            factory_id=uuid.uuid4(),
            store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        payload = serialize_event(event)
        await handle_domain_event({}, payload)
        assert "Audit: Entrega criada" in caplog.text
        assert str(event.delivery_id) in caplog.text

    async def test_handle_delivery_status_changed_event_logs_audit(self, caplog):
        caplog.set_level("INFO")
        event = DeliveryStatusChangedEvent(
            delivery_id=uuid.uuid4(),
            old_status="pendente",
            new_status="em_transito",
        )
        payload = serialize_event(event)
        await handle_domain_event({}, payload)
        assert "Audit: Status alterado" in caplog.text
        assert str(event.delivery_id) in caplog.text

    async def test_handle_eta_recalculation_requested_dispatches(self):
        delivery_id = uuid.uuid4()
        event = EtaRecalculationRequested(
            delivery_id=delivery_id,
            lat=-23.55,
            lng=-46.63,
            reason="caos_injetado",
        )
        payload = serialize_event(event)
        with (
            patch("app.infrastructure.worker.handle_eta_recalculation") as mock_handler,
        ):
            await handle_domain_event({}, payload)
            mock_handler.assert_awaited_once_with(
                {},
                str(delivery_id),
                -23.55,
                -46.63,
                "caos_injetado",
            )

    async def test_handle_delivery_created_with_redis_invalidates_cache(self):
        event = DeliveryCreatedEvent(
            delivery_id=uuid.uuid4(),
            factory_id=uuid.uuid4(),
            store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        payload = serialize_event(event)
        mock_redis = AsyncMock()

        with patch(
            "app.infrastructure.events.cache_invalidation_listener.CacheInvalidationListener.handle",
        ) as mock_listener_handle:
            await handle_domain_event({"redis": mock_redis}, payload)
            mock_listener_handle.assert_awaited_once()

    async def test_handle_delivery_created_cache_failure_logs_exception(self, caplog):
        caplog.set_level("ERROR")
        event = DeliveryCreatedEvent(
            delivery_id=uuid.uuid4(),
            factory_id=uuid.uuid4(),
            store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        payload = serialize_event(event)

        with patch(
            "app.infrastructure.events.cache_invalidation_listener.CacheInvalidationListener.handle",
            side_effect=RuntimeError("Redis connection lost"),
        ):
            await handle_domain_event({"redis": AsyncMock()}, payload)

        assert "Cache invalidation failed in worker" in caplog.text

    async def test_handle_delivery_created_without_redis_skips_cache(self):
        event = DeliveryCreatedEvent(
            delivery_id=uuid.uuid4(),
            factory_id=uuid.uuid4(),
            store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        payload = serialize_event(event)

        with patch(
            "app.infrastructure.events.cache_invalidation_listener.CacheInvalidationListener.handle",
        ) as mock_listener_handle:
            await handle_domain_event({}, payload)
            mock_listener_handle.assert_not_awaited()

    async def test_handle_alert_creation_requested_dispatches(self):
        delivery_id = uuid.uuid4()
        event = AlertCreationRequested(
            delivery_id=delivery_id,
            message="Caos injetado: deslizamento",
            is_critical=True,
        )
        payload = serialize_event(event)
        with (
            patch("app.infrastructure.worker.handle_alert_creation") as mock_handler,
        ):
            await handle_domain_event({}, payload)
            mock_handler.assert_awaited_once_with(
                {},
                str(delivery_id),
                "Caos injetado: deslizamento",
                True,
            )

    async def test_handle_invalid_payload_does_not_crash(self):
        await handle_domain_event({}, "invalid json")


class TestWorkerDbHandlers:
    async def test_handle_alert_creation_persists_alert(self):
        delivery_id = uuid.uuid4()
        message = "Caos injetado: deslizamento"
        mock_create = AsyncMock()

        with patch(
            "app.infrastructure.repositories.alert_repo.AlertRepository.create",
            mock_create,
        ):
            from app.infrastructure.worker import handle_alert_creation
            await handle_alert_creation({}, str(delivery_id), message, True)

        mock_create.assert_awaited_once()
        alert_arg = mock_create.call_args[0][0]
        assert alert_arg.delivery_id == delivery_id
        assert alert_arg.message == message
        assert alert_arg.is_critical is True

    async def test_handle_eta_recalculation_not_found_logs_warning(self, caplog):
        caplog.set_level("WARNING")
        delivery_id = uuid.uuid4()
        mock_get_by_id = AsyncMock(return_value=None)

        with patch(
            "app.infrastructure.repositories.delivery_repo.DeliveryRepository.get_by_id",
            mock_get_by_id,
        ):
            from app.infrastructure.worker import handle_eta_recalculation
            await handle_eta_recalculation({}, str(delivery_id), -23.55, -46.63, "test")

        assert "Delivery" in caplog.text
        assert str(delivery_id) in caplog.text

    async def test_handle_eta_recalculation_found_recalculates(self):
        delivery_id = uuid.uuid4()
        delivery = Delivery(
            factory_id=uuid.uuid4(),
            store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        # Override id to match the test delivery_id
        object.__setattr__(delivery, "id", delivery_id)

        mock_get_by_id = AsyncMock(return_value=delivery)
        mock_update = AsyncMock()
        mock_recalc = AsyncMock()

        with (
            patch(
                "app.infrastructure.repositories.delivery_repo.DeliveryRepository.get_by_id",
                mock_get_by_id,
            ),
            patch(
                "app.infrastructure.repositories.delivery_repo.DeliveryRepository.update",
                mock_update,
            ),
            patch(
                "app.use_cases._eta_recalculation.recalculate_delivery_eta",
                mock_recalc,
            ),
        ):
            from app.infrastructure.worker import handle_eta_recalculation
            await handle_eta_recalculation({}, str(delivery_id), -23.55, -46.63, "caos")

        mock_get_by_id.assert_awaited_once_with(delivery_id)
        mock_recalc.assert_awaited_once()
        mock_update.assert_awaited_once_with(delivery)


class TestEnqueueEvent:
    async def test_enqueue_event_calls_pool_with_correct_args(self):
        event = DeliveryCreatedEvent(
            delivery_id=uuid.uuid4(),
            factory_id=uuid.uuid4(),
            store_id=uuid.uuid4(),
            driver_id=uuid.uuid4(),
        )
        mock_pool = AsyncMock()
        await enqueue_event(event, mock_pool)
        mock_pool.enqueue_job.assert_awaited_once()
        args = mock_pool.enqueue_job.call_args
        assert args[0][0] == "handle_domain_event"
        payload = args[0][1]
        restored = deserialize_event(payload)
        assert restored is not None
        assert restored.id == event.id
