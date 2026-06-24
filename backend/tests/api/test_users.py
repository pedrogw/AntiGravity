from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient
from jose import jwt
import uuid

from app.core.config import settings

pytestmark = pytest.mark.anyio


class TestUsersDrivers:
    async def test_list_drivers_returns_only_motorista(self, client: AsyncClient):
        """Cria 2 lojistas e 2 motoristas — verifica que apenas motoristas são retornados."""
        lojista_email = f"loj_{uuid.uuid4().hex[:8]}@example.com"
        await client.post(
            "/auth/register",
            json={"email": lojista_email, "password": "pass", "role": "lojista"},
        )

        motorista_emails = []
        for _ in range(2):
            email = f"mot_{uuid.uuid4().hex[:8]}@example.com"
            await client.post(
                "/auth/register",
                json={"email": email, "password": "pass", "role": "motorista"},
            )
            motorista_emails.append(email)

        login = await client.post(
            "/auth/login",
            json={"email": lojista_email, "password": "pass"},
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = await client.get("/users/drivers", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        returned_emails = {u["email"] for u in data}
        assert returned_emails == set(motorista_emails)
        for user in data:
            assert user["role"] == "motorista"
            assert "id" in user
            assert "email" in user

    async def test_list_drivers_requires_auth(self, client: AsyncClient):
        response = await client.get("/users/drivers")
        assert response.status_code == 401

    async def test_list_drivers_empty_when_no_motorista(self, client: AsyncClient):
        email = f"loj_{uuid.uuid4().hex[:8]}@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": "pass", "role": "lojista"},
        )
        login = await client.post(
            "/auth/login",
            json={"email": email, "password": "pass"},
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = await client.get("/users/drivers", headers=headers)
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_drivers_respects_limit(self, client: AsyncClient):
        email = f"loj_{uuid.uuid4().hex[:8]}@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": "pass", "role": "lojista"},
        )
        for _ in range(3):
            mot_email = f"mot_{uuid.uuid4().hex[:8]}@example.com"
            await client.post(
                "/auth/register",
                json={"email": mot_email, "password": "pass", "role": "motorista"},
            )
        login = await client.post(
            "/auth/login",
            json={"email": email, "password": "pass"},
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = await client.get("/users/drivers?limit=1", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_list_drivers_respects_offset(self, client: AsyncClient):
        email = f"loj_{uuid.uuid4().hex[:8]}@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": "pass", "role": "lojista"},
        )
        for _ in range(3):
            mot_email = f"mot_{uuid.uuid4().hex[:8]}@example.com"
            await client.post(
                "/auth/register",
                json={"email": mot_email, "password": "pass", "role": "motorista"},
            )
        login = await client.post(
            "/auth/login",
            json={"email": email, "password": "pass"},
        )
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        response = await client.get("/users/drivers?offset=2", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_list_drivers_expired_token_returns_401(self, client: AsyncClient):
        payload = {
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
            "sub": str(uuid.uuid4()),
            "role": "lojista",
            "type": "access",
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get("/users/drivers", headers=headers)
        assert response.status_code == 401
