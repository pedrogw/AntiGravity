import pytest
from httpx import AsyncClient
import uuid
from datetime import timedelta
from jose import jwt
from app.core.config import settings
from app.core.security import create_access_token

@pytest.mark.anyio
async def test_access_denied_for_motorista(client: AsyncClient):
    # Generating motorista token
    token = create_access_token(subject=uuid.uuid4(), role="motorista")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try to create factory (requires lojista)
    factory_data = {"name": "Test", "lat": 10.0, "lng": 10.0}
    response = await client.post(
        "/places/factories",
        json=factory_data,
        headers=headers
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso negado: role insuficiente"

@pytest.mark.anyio
async def test_access_denied_for_expired_token(client: AsyncClient):
    # Expired token
    token = create_access_token(subject=uuid.uuid4(), role="lojista", expires_delta=timedelta(seconds=-1))
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try to create factory
    factory_data = {"name": "Test2", "lat": 10.0, "lng": 10.0}
    response = await client.post(
        "/places/factories",
        json=factory_data,
        headers=headers
    )
    assert response.status_code == 401
