import pytest
from httpx import AsyncClient
import uuid

pytestmark = pytest.mark.anyio


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    from app.core.rate_limiter import limiter
    yield
    limiter.reset()


class TestRateLimiting:
    async def test_login_rate_limit_returns_429(self, client: AsyncClient):
        from app.core.rate_limiter import limiter
        limiter.enabled = True
        limiter.reset()
        try:
            email = f"ratelimit_{uuid.uuid4().hex[:8]}@example.com"
            await client.post(
                "/auth/register",
                json={"email": email, "password": "testpassword", "role": "lojista"},
            )

            for _ in range(5):
                resp = await client.post(
                    "/auth/login",
                    json={"email": email, "password": "testpassword"},
                )
                assert resp.status_code == 200

            resp = await client.post(
                "/auth/login",
                json={"email": email, "password": "testpassword"},
            )
            assert resp.status_code == 429
        finally:
            limiter.enabled = False

    async def test_register_rate_limit_returns_429(self, client: AsyncClient):
        from app.core.rate_limiter import limiter
        limiter.enabled = True
        limiter.reset()
        try:
            for i in range(3):
                email = f"ratelimit_reg_{i}_{uuid.uuid4().hex[:8]}@example.com"
                resp = await client.post(
                    "/auth/register",
                    json={"email": email, "password": "testpassword", "role": "lojista"},
                )
                assert resp.status_code == 201

            email = f"ratelimit_reg_3_{uuid.uuid4().hex[:8]}@example.com"
            resp = await client.post(
                "/auth/register",
                json={"email": email, "password": "testpassword", "role": "lojista"},
            )
            assert resp.status_code == 429
        finally:
            limiter.enabled = False

    async def test_chaos_rate_limit_returns_429(self, client: AsyncClient, lojista: dict, motorista: dict):
        from app.core.rate_limiter import limiter
        limiter.enabled = True
        limiter.reset()
        try:
            factory_resp = await client.post(
                "/places/factories",
                json={"name": "F", "lat": -23.0, "lng": -46.0},
                headers=lojista["headers"],
            )
            store_resp = await client.post(
                "/places/stores",
                json={"name": "S", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
                headers=lojista["headers"],
            )
            create_resp = await client.post(
                "/deliveries/",
                json={
                    "factory_id": factory_resp.json()["id"],
                    "store_id": store_resp.json()["id"],
                    "driver_id": motorista["id"],
                },
                headers=lojista["headers"],
            )
            delivery_id = create_resp.json()["id"]

            for _ in range(10):
                resp = await client.post(
                    f"/deliveries/{delivery_id}/chaos",
                    json={"event_type": "engarrafamento", "impact_factor": 1.0, "delay_minutes": 0},
                    headers=lojista["headers"],
                )
                assert resp.status_code == 201

            resp = await client.post(
                f"/deliveries/{delivery_id}/chaos",
                json={"event_type": "engarrafamento", "impact_factor": 1.0, "delay_minutes": 0},
                headers=lojista["headers"],
            )
            assert resp.status_code == 429
        finally:
            limiter.enabled = False
