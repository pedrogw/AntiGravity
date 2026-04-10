import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.anyio
async def test_register_user(client: AsyncClient):
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    response = await client.post(
        "/auth/register",
        json={"email": email, "password": "testpassword", "role": "lojista"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email

@pytest.mark.anyio
async def test_login_success(client: AsyncClient):
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    # Registration
    await client.post(
        "/auth/register",
        json={"email": email, "password": "testpassword", "role": "lojista"}
    )
    
    # Login
    response = await client.post(
        "/auth/login",
        json={"email": email, "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.anyio
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"

@pytest.mark.anyio
async def test_create_factory(client: AsyncClient):
    email = f"fac_{uuid.uuid4().hex[:8]}@example.com"
    await client.post("/auth/register", json={"email": email, "password": "testpassword", "role": "lojista"})
    login_resp = await client.post("/auth/login", json={"email": email, "password": "testpassword"})
    token = login_resp.json()["access_token"]
    
    factory_data = {
        "name": "Test Factory",
        "lat": -23.1234,
        "lng": -46.5678
    }
    response = await client.post(
        "/places/factories", 
        json=factory_data, 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == factory_data["name"]
