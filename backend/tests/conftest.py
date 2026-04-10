import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import get_db, AsyncSessionLocal, engine
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
import uuid

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

@pytest.fixture
async def lojista_token_headers(client: AsyncClient):
    email = f"fac_{uuid.uuid4().hex[:8]}@example.com"
    await client.post("/auth/register", json={"email": email, "password": "testpassword", "role": "lojista"})
    login_resp = await client.post("/auth/login", json={"email": email, "password": "testpassword"})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
