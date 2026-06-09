import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import get_db, AsyncSessionLocal
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.db.base_class import Base
from app.core.config import settings
import uuid

# Engine para SQLite in-memory
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    poolclass=StaticPool, # SQLite memory requires StaticPool
    connect_args={"check_same_thread": False},
    future=True
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture(scope="session", autouse=True)
async def setup_db_schema():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session():
    async with test_engine.connect() as conn:
        async with conn.begin() as trans:
            async with AsyncSession(bind=conn, expire_on_commit=False) as session:
                yield session
                await trans.rollback()

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture
async def client(db_session: AsyncSession):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()

async def _create_user(client: AsyncClient, role: str) -> dict:
    email = f"{role[:4]}_{uuid.uuid4().hex[:8]}@example.com"
    reg = await client.post(
        "/auth/register",
        json={"email": email, "password": "testpassword", "role": role},
    )
    user_id = reg.json()["id"]
    login = await client.post(
        "/auth/login",
        json={"email": email, "password": "testpassword"},
    )
    token = login.json()["access_token"]
    return {"headers": {"Authorization": f"Bearer {token}"}, "id": user_id}


@pytest.fixture
async def lojista(client: AsyncClient) -> dict:
    return await _create_user(client, "lojista")


@pytest.fixture
async def motorista(client: AsyncClient) -> dict:
    return await _create_user(client, "motorista")


@pytest.fixture
async def lojista_token_headers(lojista: dict) -> dict:
    return lojista["headers"]
