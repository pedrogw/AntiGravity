import pytest
from httpx import AsyncClient
import uuid
from datetime import timedelta
from app.core.security import create_access_token

pytestmark = pytest.mark.anyio


class TestRoleBasedAccess:
    async def test_motorista_cannot_create_factory(self, client: AsyncClient):
        token = create_access_token(subject=uuid.uuid4(), role="motorista")
        response = await client.post(
            "/places/factories",
            json={"name": "Test", "lat": 10.0, "lng": 10.0},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Acesso negado: role insuficiente"

    async def test_motorista_cannot_create_store(self, client: AsyncClient):
        token = create_access_token(subject=uuid.uuid4(), role="motorista")
        response = await client.post(
            "/places/stores",
            json={"name": "S", "lat": 10.0, "lng": 10.0, "owner_id": str(uuid.uuid4())},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403

    async def test_motorista_cannot_create_delivery(self, client: AsyncClient):
        token = create_access_token(subject=uuid.uuid4(), role="motorista")
        response = await client.post(
            "/deliveries/",
            json={"factory_id": str(uuid.uuid4()), "store_id": str(uuid.uuid4()), "driver_id": str(uuid.uuid4())},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403


class TestTokenValidation:
    async def test_expired_token_returns_401(self, client: AsyncClient):
        token = create_access_token(
            subject=uuid.uuid4(), role="lojista",
            expires_delta=timedelta(seconds=-1)
        )
        response = await client.post(
            "/places/factories",
            json={"name": "Test", "lat": 10.0, "lng": 10.0},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 401

    async def test_missing_token_returns_403(self, client: AsyncClient):
        response = await client.post(
            "/places/factories",
            json={"name": "Test", "lat": 10.0, "lng": 10.0}
        )
        assert response.status_code in (401, 403)

    async def test_list_deliveries_requires_auth(self, client: AsyncClient):
        response = await client.get("/deliveries/")
        assert response.status_code in (401, 403)

    async def test_list_factories_requires_auth(self, client: AsyncClient):
        response = await client.get("/places/factories")
        assert response.status_code in (401, 403)

    async def test_list_stores_requires_auth(self, client: AsyncClient):
        response = await client.get("/places/stores")
        assert response.status_code in (401, 403)

    async def test_malformed_token_returns_401(self, client: AsyncClient):
        response = await client.post(
            "/places/factories",
            json={"name": "Test", "lat": 10.0, "lng": 10.0},
            headers={"Authorization": "Bearer invalid-token"}
        )
        assert response.status_code == 401
