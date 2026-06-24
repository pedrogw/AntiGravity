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

    async def test_set_and_get_list(self, cache_service):
        items = [FakeModel(id="a", value=1), FakeModel(id="b", value=2)]
        await cache_service.set_list("test:list", items)
        result = await cache_service.get_list("test:list", FakeModel)
        assert result is not None
        assert len(result) == 2
        assert result[0].id == "a"
        assert result[0].value == 1
        assert result[1].id == "b"
        assert result[1].value == 2

    async def test_get_list_miss(self, cache_service):
        result = await cache_service.get_list("nonexistent", FakeModel)
        assert result is None

    async def test_set_and_get_list_empty(self, cache_service):
        await cache_service.set_list("test:empty", [])
        result = await cache_service.get_list("test:empty", FakeModel)
        assert result is not None
        assert result == []
