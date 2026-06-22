import json
import pytest
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI, Request
from sqlalchemy.exc import OperationalError
from app.core.exceptions import DomainException
from app.core.events.bus import event_bus
from app.main import lifespan, domain_exception_handler, db_connection_exception_handler, unhandled_exception_handler, health_check


@pytest.fixture(autouse=True)
def reset_event_bus():
    event_bus.worker_pool = None
    yield


class TestLifespan:
    async def test_success_path_sets_cache_and_worker_pool(self):
        mock_app = AsyncMock(spec=FastAPI)
        mock_app.state = AsyncMock()
        mock_redis = AsyncMock()
        mock_pool = AsyncMock()
        mock_pool.close.return_value = None

        with (
            patch("app.main.get_redis", return_value=mock_redis),
            patch("app.main.create_pool", return_value=mock_pool),
            patch("app.main.close_redis"),
            patch("app.main.dispose_engine"),
        ):
            async with lifespan(mock_app):
                assert mock_app.state.cache_service is not None
                assert event_bus.worker_pool is mock_pool

        mock_redis.ping.assert_awaited_once()
        mock_pool.close.assert_called_once()

    async def test_failure_path_logs_fallback_warning(self, caplog):
        caplog.set_level("WARNING")
        mock_app = AsyncMock(spec=FastAPI)
        mock_app.state = AsyncMock()

        with (
            patch("app.main.get_redis", side_effect=ConnectionError("Redis down")),
            patch("app.main.close_redis"),
            patch("app.main.dispose_engine"),
        ):
            async with lifespan(mock_app):
                assert event_bus.worker_pool is None

        assert "Redis indisponível" in caplog.text


class TestDomainExceptionHandler:
    async def test_returns_json_response_with_status_and_detail(self):
        request = AsyncMock(spec=Request)
        request.state.request_id = "req-123"
        exc = DomainException(status_code=400, detail="Domain error test")
        response = await domain_exception_handler(request, exc)
        assert response.status_code == 400
        body = json.loads(response.body)
        assert body["detail"] == "Domain error test"


class TestDbConnectionExceptionHandler:
    async def test_returns_503_with_message(self):
        request = AsyncMock(spec=Request)
        request.state.request_id = "req-456"
        exc = OperationalError("stmt", {}, Exception("DB failure"))
        response = await db_connection_exception_handler(request, exc)
        assert response.status_code == 503
        body = json.loads(response.body)
        assert "Database Unavailable" in body["detail"]


class TestUnhandledExceptionHandler:
    async def test_returns_500_with_generic_message(self):
        request = AsyncMock(spec=Request)
        request.state.request_id = "req-789"
        exc = ValueError("something went wrong")
        response = await unhandled_exception_handler(request, exc)
        assert response.status_code == 500
        body = json.loads(response.body)
        assert body["detail"] == "Erro interno do servidor"


class TestHealthCheck:
    async def test_returns_ok(self):
        result = await health_check()
        assert result == {"status": "ok", "environment": "dev"}
