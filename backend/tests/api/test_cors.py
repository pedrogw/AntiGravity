import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

pytestmark = pytest.mark.anyio


class TestCORSMiddleware:
    async def test_cors_allows_localhost(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.options(
                "/auth/login",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                },
            )
            assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"

    async def test_cors_blocks_unknown_origins(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.options(
                "/auth/login",
                headers={
                    "Origin": "https://unknown-site.com",
                    "Access-Control-Request-Method": "POST",
                },
            )
            assert "access-control-allow-origin" not in response.headers

    async def test_cors_allows_vercel_previews(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.options(
                "/auth/login",
                headers={
                    "Origin": "https://anti-gravity-1ckysewhd-pgwms.vercel.app",
                    "Access-Control-Request-Method": "POST",
                },
            )
            assert response.headers.get("access-control-allow-origin") == "https://anti-gravity-1ckysewhd-pgwms.vercel.app"
