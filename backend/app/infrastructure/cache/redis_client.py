from typing import Optional
from redis.asyncio import Redis as AsyncRedis
from app.core.config import settings

_redis: Optional[AsyncRedis] = None


async def get_redis() -> AsyncRedis:
    global _redis
    if _redis is None:
        _redis = AsyncRedis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
    return _redis


async def close_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.close()
        _redis = None
