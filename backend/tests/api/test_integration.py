import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import get_db, AsyncSessionLocal, engine
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
import uuid

# Create a test engine with NullPool to avoid connection sharing issues between tests/loops
test_engine = create_async_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,
    future=True
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

# Apply override
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

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
    factory_data = {
        "name": "Test Factory",
        "lat": -23.1234,
        "lng": -46.5678
    }
    response = await client.post("/places/factories", json=factory_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == factory_data["name"]
