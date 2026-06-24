import pytest
from httpx import AsyncClient
import uuid

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
        assert response.status_code in (401, 403)

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
