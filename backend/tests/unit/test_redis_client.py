import pytest
from unittest.mock import AsyncMock, patch
import app.infrastructure.cache.redis_client as redis_client_module
from app.core.config import settings


@pytest.fixture(autouse=True)
def reset_redis():
    original = redis_client_module._redis
    redis_client_module._redis = None
    yield
    redis_client_module._redis = original


class TestGetRedis:
    async def test_creates_when_none(self):
        mock_redis = AsyncMock()
        with patch.object(redis_client_module.AsyncRedis, "from_url", return_value=mock_redis):
            result = await redis_client_module.get_redis()
            assert result is mock_redis
            redis_client_module.AsyncRedis.from_url.assert_called_once_with(
                settings.REDIS_URL, decode_responses=True,
            )

    async def test_returns_existing_when_set(self):
        mock_redis = AsyncMock()
        redis_client_module._redis = mock_redis
        result = await redis_client_module.get_redis()
        assert result is mock_redis


class TestCloseRedis:
    async def test_closes_and_resets_when_not_none(self):
        mock_redis = AsyncMock()
        redis_client_module._redis = mock_redis
        await redis_client_module.close_redis()
        mock_redis.close.assert_awaited_once()
        assert redis_client_module._redis is None

    async def test_noop_when_already_none(self):
        redis_client_module._redis = None
        await redis_client_module.close_redis()
        assert redis_client_module._redis is None
