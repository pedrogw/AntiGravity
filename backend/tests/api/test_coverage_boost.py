import pytest
import uuid
from httpx import AsyncClient


# ─── helpers ────────────────────────────────────────────────────────────────

async def _create_lojista(client: AsyncClient) -> dict:
    """Register a lojista and return its login token headers + user_id."""
    email = f"loj_{uuid.uuid4().hex[:8]}@example.com"
    reg = await client.post(
        "/auth/register",
        json={"email": email, "password": "testpassword", "role": "lojista"},
    )
    user_id = reg.json()["id"]
    login = await client.post(
        "/auth/login",
        json={"email": email, "password": "testpassword"},
    )
    token = login.json()["access_token"]
    return {"headers": {"Authorization": f"Bearer {token}"}, "id": user_id}


async def _create_motorista(client: AsyncClient) -> dict:
    """Register a motorista and return its login token headers + user_id."""
    email = f"mot_{uuid.uuid4().hex[:8]}@example.com"
    reg = await client.post(
        "/auth/register",
        json={"email": email, "password": "testpassword", "role": "motorista"},
    )
    user_id = reg.json()["id"]
    login = await client.post(
        "/auth/login",
        json={"email": email, "password": "testpassword"},
    )
    token = login.json()["access_token"]
    return {"headers": {"Authorization": f"Bearer {token}"}, "id": user_id}


# ─── auth.py coverage ────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_register_duplicate_email_returns_409(client: AsyncClient):
    """Covers auth.py line 23-24: duplicate e-mail guard."""
    email = f"dup_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": email, "password": "pass", "role": "lojista"}
    await client.post("/auth/register", json=payload)
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Email já cadastrado"


@pytest.mark.anyio
async def test_login_returns_bearer_token(client: AsyncClient):
    """Covers auth.py lines 40-49: full login body execution."""
    lojista = await _create_lojista(client)
    assert "Authorization" in lojista["headers"]


# ─── places.py coverage ──────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_list_factories_returns_200(client: AsyncClient):
    """Covers places.py lines 22-23: list_factories body."""
    response = await client.get("/places/factories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_create_store_as_lojista(client: AsyncClient):
    """Covers places.py lines 27-31: create_store body."""
    lojista = await _create_lojista(client)
    owner_id = lojista["id"]

    store_data = {
        "name": "Minha Loja Centro",
        "lat": -23.5505,
        "lng": -46.6333,
        "owner_id": owner_id,
    }
    response = await client.post(
        "/places/stores", json=store_data, headers=lojista["headers"]
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == store_data["name"]


@pytest.mark.anyio
async def test_list_stores_returns_200(client: AsyncClient):
    """Covers places.py lines 35-36: list_stores body."""
    response = await client.get("/places/stores")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ─── deliveries.py coverage ──────────────────────────────────────────────────

@pytest.mark.anyio
async def test_create_and_list_deliveries(client: AsyncClient):
    """Covers deliveries.py lines 13-17 and 21-22: both route bodies."""
    # Need real UUIDs for FK constraints
    lojista = await _create_lojista(client)
    motorista = await _create_motorista(client)

    # Create factory and store
    factory_resp = await client.post(
        "/places/factories",
        json={"name": "Fábrica Teste", "lat": -19.9191, "lng": -43.9386},
        headers=lojista["headers"],
    )
    factory_id = factory_resp.json()["id"]

    store_resp = await client.post(
        "/places/stores",
        json={"name": "Loja Teste", "lat": -23.5505, "lng": -46.6333, "owner_id": lojista["id"]},
        headers=lojista["headers"],
    )
    store_id = store_resp.json()["id"]

    delivery_data = {
        "factory_id": factory_id,
        "store_id": store_id,
        "driver_id": motorista["id"],
    }

    # POST — create_delivery body (lines 13-17)
    create_resp = await client.post("/deliveries/", json=delivery_data)
    assert create_resp.status_code == 201
    assert create_resp.json()["status"] == "pendente"

    # GET — list_deliveries body (lines 21-22)
    list_resp = await client.get("/deliveries/")
    assert list_resp.status_code == 200
    assert isinstance(list_resp.json(), list)
    assert len(list_resp.json()) >= 1


# ─── session.py coverage ─────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_get_db_dependency_is_overridden(client: AsyncClient):
    """
    Ensures the get_db dependency is active via a real DB-hitting endpoint.
    Covers session.py lines 15-16 indirectly through the conftest override.
    """
    response = await client.get("/places/factories")
    assert response.status_code == 200
