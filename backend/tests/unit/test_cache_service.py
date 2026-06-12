import pytest
from pydantic import BaseModel


class FakeModel(BaseModel):
    id: str
    value: int


class TestCacheService:
    async def test_set_and_get_json(self, cache_service):
        data = [{"id": "abc", "value": 42}]
        await cache_service.set_json("test:key", data)
        result = await cache_service.get_json("test:key")
        assert result == data

    async def test_get_json_miss(self, cache_service):
        result = await cache_service.get_json("nonexistent")
        assert result is None

    async def test_set_and_get_pydantic(self, cache_service):
        obj = FakeModel(id="x", value=99)
        await cache_service.set("test:pydantic", obj)
        result = await cache_service.get("test:pydantic", FakeModel)
        assert result is not None
        assert result.id == "x"
        assert result.value == 99

    async def test_ttl_expiry(self, cache_service):
        cache_service.ttl = 1
        await cache_service.set_json("test:ttl", "data")
        import asyncio
        await asyncio.sleep(1.5)
        result = await cache_service.get_json("test:ttl")
        assert result is None

    async def test_invalidate_prefix(self, cache_service):
        await cache_service.set_json("deliveries:list:10:0", "a")
        await cache_service.set_json("deliveries:list:50:0", "b")
        await cache_service.set_json("other:key", "c")

        deleted = await cache_service.invalidate_prefix("deliveries:list")
        assert deleted == 2

        assert await cache_service.get_json("deliveries:list:10:0") is None
        assert await cache_service.get_json("deliveries:list:50:0") is None
        assert await cache_service.get_json("other:key") == "c"
