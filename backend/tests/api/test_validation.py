import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.anyio
@pytest.mark.parametrize("payload, expected_status", [
    # Factory validation tests
    (
        {"name": "", "lat": -23.5, "lng": -46.6},  # Empty name
        422
    ),
    (
        {"name": "Valid Factory", "lat": 150.0, "lng": -46.6},  # Invalid lat
        422
    ),
    (
        {"name": "Valid Factory", "lat": -23.5, "lng": -200.0},  # Invalid lng
        422
    )
])
async def test_factory_payload_validation(client: AsyncClient, lojista_token_headers: dict, payload: dict, expected_status: int):
    # Depending on how the factory creation route is defined, let's assume it accepts FactoryCreate
    response = await client.post(
        "/places/factories",
        json=payload,
        headers=lojista_token_headers
    )
    assert response.status_code == expected_status

@pytest.mark.anyio
@pytest.mark.parametrize("payload, expected_status", [
    # User validation tests
    (
        {"email": "valid@email.com", "password": "", "role": "motorista"},  # Empty password
        422
    ),
    (
        {"email": "not-an-email", "password": "password", "role": "motorista"},  # Invalid email
        422
    )
])
async def test_user_payload_validation(client: AsyncClient, payload: dict, expected_status: int):
    response = await client.post(
        "/auth/register",
        json=payload
    )
    assert response.status_code == expected_status
