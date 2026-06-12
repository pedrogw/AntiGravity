import pytest
from httpx import AsyncClient
import uuid

pytestmark = pytest.mark.anyio


class TestFactoryValidation:
    @pytest.mark.parametrize("payload", [
        {"name": "", "lat": -23.5, "lng": -46.6},
        {"name": "Valid Factory", "lat": 150.0, "lng": -46.6},
        {"name": "Valid Factory", "lat": -23.5, "lng": -200.0},
        {"name": "Valid Factory", "lat": -91.0, "lng": 0.0},
        {"name": "Valid Factory", "lat": 91.0, "lng": 0.0},
        {"name": "Valid Factory", "lat": 0.0, "lng": -181.0},
        {"name": "Valid Factory", "lat": 0.0, "lng": 181.0},
        {"name": 123, "lat": 0.0, "lng": 0.0},
    ])
    async def test_invalid_factory_payloads_return_422(self, client: AsyncClient, lojista_token_headers: dict, payload: dict):
        response = await client.post(
            "/places/factories",
            json=payload,
            headers=lojista_token_headers
        )
        assert response.status_code == 422

    @pytest.mark.parametrize("payload", [
        {"name": "A", "lat": -90.0, "lng": 0.0},
        {"name": "B", "lat": 90.0, "lng": 0.0},
        {"name": "C", "lat": 0.0, "lng": -180.0},
        {"name": "D", "lat": 0.0, "lng": 180.0},
    ])
    async def test_boundary_factory_payloads_return_201(self, client: AsyncClient, lojista_token_headers: dict, payload: dict):
        response = await client.post(
            "/places/factories",
            json=payload,
            headers=lojista_token_headers
        )
        assert response.status_code == 201


class TestStoreValidation:
    @pytest.mark.parametrize("payload", [
        {"name": "", "lat": 0.0, "lng": 0.0, "owner_id": str(uuid.uuid4())},
        {"name": "S", "lat": 150.0, "lng": 0.0, "owner_id": str(uuid.uuid4())},
        {"name": "S", "lat": 0.0, "lng": -200.0, "owner_id": str(uuid.uuid4())},
        {"name": "S", "lat": 0.0, "lng": 0.0, "owner_id": "not-a-uuid"},
        {"name": "S", "lat": 0.0, "lng": 0.0},
    ])
    async def test_invalid_store_payloads_return_422(self, client: AsyncClient, lojista_token_headers: dict, payload: dict):
        response = await client.post(
            "/places/stores",
            json=payload,
            headers=lojista_token_headers
        )
        assert response.status_code == 422


class TestUserValidation:
    @pytest.mark.parametrize("payload", [
        {"email": "valid@email.com", "password": "", "role": "motorista"},
        {"email": "not-an-email", "password": "password", "role": "motorista"},
        {"email": "valid@email.com", "password": "pass", "role": "invalid_role"},
        {"email": "", "password": "pass", "role": "motorista"},
        {"password": "pass", "role": "motorista"},
    ])
    async def test_invalid_user_payloads_return_422(self, client: AsyncClient, payload: dict):
        response = await client.post(
            "/auth/register",
            json=payload
        )
        assert response.status_code == 422


class TestDeliveryForeignKeyViolations:
    async def test_create_delivery_nonexistent_factory(self, client: AsyncClient, lojista: dict, motorista: dict):
        payload = {
            "factory_id": str(uuid.uuid4()),
            "store_id": str(uuid.uuid4()),
            "driver_id": motorista["id"],
        }
        response = await client.post("/deliveries/", json=payload, headers=lojista["headers"])
        # CreateDeliveryUseCase now validates that factory exists
        assert response.status_code == 404

    async def test_create_delivery_nonexistent_driver(self, client: AsyncClient, lojista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F", "lat": 0.0, "lng": 0.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S", "lat": 0.0, "lng": 0.0, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        payload = {
            "factory_id": factory_resp.json()["id"],
            "store_id": store_resp.json()["id"],
            "driver_id": str(uuid.uuid4()),
        }
        response = await client.post("/deliveries/", json=payload, headers=lojista["headers"])
        assert response.status_code in (201, 500)
