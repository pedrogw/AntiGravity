import json
from typing import Optional, TypeVar, Type, Any
from pydantic import BaseModel
from redis.asyncio import Redis
from app.core.config import settings

T = TypeVar("T", bound=BaseModel)

CACHE_PREFIX = "deliveries:list"


class CacheService:
    def __init__(self, redis: Redis, ttl: int = settings.CACHE_TTL_SECONDS):
        self.redis = redis
        self.ttl = ttl

    async def get_json(self, key: str) -> Optional[Any]:
        raw = await self.redis.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set_json(self, key: str, value: Any) -> None:
        raw = json.dumps(value, default=str)
        await self.redis.set(key, raw, ex=self.ttl)

    async def get(self, key: str, model: Type[T]) -> Optional[T]:
        raw = await self.redis.get(key)
        if raw is None:
            return None
        return model.model_validate_json(raw)

    async def set(self, key: str, value: BaseModel) -> None:
        raw = value.model_dump_json()
        await self.redis.set(key, raw, ex=self.ttl)

    async def invalidate_prefix(self, prefix: str) -> int:
        cursor = 0
        deleted = 0
        while True:
            cursor, keys = await self.redis.scan(cursor=cursor, match=f"{prefix}:*")
            if keys:
                deleted += await self.redis.delete(*keys)
            if cursor == 0:
                break
        return deleted
