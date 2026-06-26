import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import datetime

pytestmark = pytest.mark.anyio


class TestAuth:
    async def test_register_user(self, client: AsyncClient):
        email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        response = await client.post(
            "/auth/register",
            json={"email": email, "password": "testpassword", "role": "lojista"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == email
        assert data["role"] == "lojista"
        assert "id" in data
        assert "password" not in data
        assert "password_hash" not in data

    async def test_login_success(self, client: AsyncClient):
        email = f"login_{uuid.uuid4().hex[:8]}@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": "testpassword", "role": "lojista"}
        )
        response = await client.post(
            "/auth/login",
            json={"email": email, "password": "testpassword"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert len(data["access_token"]) > 20
        assert len(data["refresh_token"]) > 20
        assert data["token_type"] == "bearer"

    async def test_login_invalid_credentials(self, client: AsyncClient):
        response = await client.post(
            "/auth/login",
            json={"email": "nonexistent@example.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Credenciais inválidas"

    async def test_register_duplicate_email_returns_409(self, client: AsyncClient):
        email = f"dup_{uuid.uuid4().hex[:8]}@example.com"
        payload = {"email": email, "password": "pass", "role": "lojista"}
        await client.post("/auth/register", json=payload)
        response = await client.post("/auth/register", json=payload)
        assert response.status_code == 409
        assert response.json()["detail"] == "Email já cadastrado"

    async def test_refresh_token_returns_new_tokens(self, client: AsyncClient):
        email = f"refresh_{uuid.uuid4().hex[:8]}@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": "testpassword", "role": "motorista"}
        )
        login_resp = await client.post(
            "/auth/login",
            json={"email": email, "password": "testpassword"}
        )
        refresh_token = login_resp.json()["refresh_token"]

        refresh_resp = await client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert refresh_resp.status_code == 200
        data = refresh_resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert len(data["access_token"]) > 20
        assert len(data["refresh_token"]) > 20
        assert data["token_type"] == "bearer"

        new_access = data["access_token"]
        resp = await client.get(
            "/dashboard",
            headers={"Authorization": f"Bearer {new_access}"}
        )
        assert resp.status_code == 200

    async def test_refresh_with_invalid_token_returns_401(self, client: AsyncClient):
        refresh_resp = await client.post(
            "/auth/refresh",
            json={"refresh_token": "invalid_token_123"}
        )
        assert refresh_resp.status_code == 401
        assert refresh_resp.json()["detail"] == "Refresh token inválido ou expirado"

    async def test_access_token_cannot_be_used_as_refresh(self, client: AsyncClient):
        email = f"refresh_invalid_{uuid.uuid4().hex[:8]}@example.com"
        await client.post(
            "/auth/register",
            json={"email": email, "password": "testpassword", "role": "lojista"}
        )
        login_resp = await client.post(
            "/auth/login",
            json={"email": email, "password": "testpassword"}
        )
        access_token = login_resp.json()["access_token"]

        refresh_resp = await client.post(
            "/auth/refresh",
            json={"refresh_token": access_token}
        )
        assert refresh_resp.status_code == 401


class TestPlaces:
    async def test_create_factory(self, client: AsyncClient, lojista: dict):
        factory_data = {"name": "Test Factory", "lat": -23.1234, "lng": -46.5678}
        response = await client.post(
            "/places/factories",
            json=factory_data,
            headers=lojista["headers"]
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == factory_data["name"]
        assert data["lat"] == factory_data["lat"]
        assert data["lng"] == factory_data["lng"]
        assert "id" in data

    async def test_list_factories(self, client: AsyncClient, lojista: dict):
        await client.post(
            "/places/factories",
            json={"name": "F1", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"]
        )
        response = await client.get("/places/factories", headers=lojista["headers"])
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "name" in data[0]
        assert "lat" in data[0]
        assert "lng" in data[0]

    async def test_create_store(self, client: AsyncClient, lojista: dict):
        store_data = {
            "name": "Loja Centro",
            "lat": -23.5505,
            "lng": -46.6333,
            "owner_id": lojista["id"],
        }
        response = await client.post(
            "/places/stores",
            json=store_data,
            headers=lojista["headers"]
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == store_data["name"]
        assert data["owner_id"] == lojista["id"]

    async def test_list_stores(self, client: AsyncClient, lojista: dict):
        await client.post(
            "/places/stores",
            json={"name": "S1", "lat": -23.0, "lng": -46.0, "owner_id": lojista["id"]},
            headers=lojista["headers"]
        )
        response = await client.get("/places/stores", headers=lojista["headers"])
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    async def test_get_store_by_id(self, client: AsyncClient, lojista: dict):
        create_resp = await client.post(
            "/places/stores",
            json={"name": "Loja Teste", "lat": -23.5505, "lng": -46.6333, "owner_id": lojista["id"]},
            headers=lojista["headers"]
        )
        assert create_resp.status_code == 201
        store_id = create_resp.json()["id"]

        response = await client.get(f"/places/stores/{store_id}", headers=lojista["headers"])
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == store_id
        assert data["name"] == "Loja Teste"
        assert data["lat"] == -23.5505
        assert data["lng"] == -46.6333

    async def test_get_store_by_id_not_found(self, client: AsyncClient, lojista: dict):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/places/stores/{fake_id}", headers=lojista["headers"])
        assert response.status_code == 404


class TestDeliveries:
    async def test_create_and_list_deliveries(self, client: AsyncClient, lojista: dict, motorista: dict):
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
        create_resp = await client.post("/deliveries/", json=delivery_data, headers=lojista["headers"])
        assert create_resp.status_code == 201
        created = create_resp.json()
        assert created["status"] == "pendente"
        assert created["factory_id"] == factory_id
        assert created["store_id"] == store_id
        assert created["driver_id"] == motorista["id"]

        list_resp = await client.get("/deliveries/", headers=lojista["headers"])
        assert list_resp.status_code == 200
        deliveries = list_resp.json()
        assert isinstance(deliveries, list)
        assert any(d["id"] == created["id"] for d in deliveries)

    async def test_update_delivery_status(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "Loja", "lat": -23.5, "lng": -46.6, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        accept_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "aceita"},
            headers=motorista["headers"],
        )
        assert accept_resp.status_code == 200
        assert accept_resp.json()["status"] == "aceita"

        update_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "em_transito"},
            headers=motorista["headers"],
        )
        assert update_resp.status_code == 200
        updated = update_resp.json()
        assert updated["status"] == "em_transito"
        assert updated["departed_at"] is not None

    async def test_update_delivery_location_recalculates_eta(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F2", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "Loja Destino", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        accept_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "aceita"},
            headers=motorista["headers"],
        )
        assert accept_resp.status_code == 200

        update_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "em_transito", "lat": -23.55, "lng": -46.63},
            headers=motorista["headers"],
        )
        assert update_resp.status_code == 200
        updated = update_resp.json()
        assert updated["eta_current"] is not None

    async def test_update_nonexistent_delivery_returns_404(self, client: AsyncClient, lojista: dict):
        update_resp = await client.patch(
            f"/deliveries/{uuid.uuid4()}",
            json={"status": "aceita"},
            headers=lojista["headers"],
        )
        assert update_resp.status_code == 404

    async def test_cancel_delivery_aceita_succeeds(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F-cancel", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S-cancel", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "aceita"},
            headers=motorista["headers"],
        )

        cancel_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "cancelada"},
            headers=motorista["headers"],
        )
        assert cancel_resp.status_code == 200
        assert cancel_resp.json()["status"] == "cancelada"

    async def test_cancel_delivery_em_transito_fails(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F-cancel2", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S-cancel2", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "aceita"},
            headers=motorista["headers"],
        )
        await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "em_transito", "lat": -23.5, "lng": -46.6},
            headers=motorista["headers"],
        )

        cancel_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "cancelada"},
            headers=motorista["headers"],
        )
        assert cancel_resp.status_code == 422

    async def test_lojista_cannot_update_delivery(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        update_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "aceita"},
            headers=lojista["headers"],
        )
        assert update_resp.status_code == 403
        assert update_resp.json()["detail"] == "Apenas o motorista responsável pode atualizar a entrega"

    async def test_wrong_motorista_cannot_update_delivery(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F2", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S2", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        outro_motorista = await client.post(
            "/auth/register",
            json={"email": f"outro_motorista_{uuid.uuid4().hex[:8]}@example.com", "password": "testpassword", "role": "motorista"},
        )
        outro_login = await client.post(
            "/auth/login",
            json={"email": outro_motorista.json()["email"], "password": "testpassword"},
        )
        outro_headers = {"Authorization": f"Bearer {outro_login.json()['access_token']}"}

        update_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "aceita"},
            headers=outro_headers,
        )
        assert update_resp.status_code == 403
        assert update_resp.json()["detail"] == "Apenas o motorista responsável pode atualizar a entrega"


class TestChaosInjection:
    async def test_inject_chaos_creates_event(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        chaos_resp = await client.post(
            f"/deliveries/{delivery_id}/chaos",
            json={"event_type": "engarrafamento", "impact_factor": 1.5, "delay_minutes": 15},
            headers=lojista["headers"],
        )
        assert chaos_resp.status_code == 201
        data = chaos_resp.json()
        assert data["event_type"] == "engarrafamento"
        assert data["delivery_id"] == delivery_id
        assert data["impact_factor"] == 1.5
        assert data["delay_minutes"] == 15
        assert "id" in data
        assert "timestamp_start" in data

    async def test_inject_chaos_on_nonexistent_delivery_returns_404(self, client: AsyncClient, lojista: dict):
        chaos_resp = await client.post(
            f"/deliveries/{uuid.uuid4()}/chaos",
            json={"event_type": "acidente"},
            headers=lojista["headers"],
        )
        assert chaos_resp.status_code == 404

    async def test_inject_critical_chaos_creates_alert(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F2", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S2", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        chaos_resp = await client.post(
            f"/deliveries/{delivery_id}/chaos",
            json={"event_type": "deslizamento", "impact_factor": 3.0, "delay_minutes": 90},
            headers=lojista["headers"],
        )
        assert chaos_resp.status_code == 201

    async def test_inject_chaos_recalculates_eta_when_delivery_has_position(
        self, client: AsyncClient, lojista: dict, motorista: dict
    ):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F3", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S3", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "aceita"},
            headers=motorista["headers"],
        )
        await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "em_transito", "lat": -23.55, "lng": -46.63},
            headers=motorista["headers"],
        )

        chaos_resp = await client.post(
            f"/deliveries/{delivery_id}/chaos",
            json={"event_type": "engarrafamento", "impact_factor": 1.5, "delay_minutes": 30},
            headers=lojista["headers"],
        )
        assert chaos_resp.status_code == 201

        get_resp = await client.get("/deliveries/", headers=lojista["headers"])
        deliveries = get_resp.json()
        updated = next(d for d in deliveries if d["id"] == delivery_id)
        assert updated["eta_current"] is not None

    async def test_inject_chaos_idempotency_returns_same_on_repeat(
        self, client: AsyncClient, lojista: dict, motorista: dict
    ):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F-idem", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S-idem", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]
        idem_key = str(uuid.uuid4())

        first = await client.post(
            f"/deliveries/{delivery_id}/chaos",
            json={"event_type": "acidente", "impact_factor": 1.5, "delay_minutes": 10},
            headers={**lojista["headers"], "Idempotency-Key": idem_key},
        )
        assert first.status_code == 201
        first_data = first.json()

        second = await client.post(
            f"/deliveries/{delivery_id}/chaos",
            json={"event_type": "acidente", "impact_factor": 1.5, "delay_minutes": 10},
            headers={**lojista["headers"], "Idempotency-Key": idem_key},
        )
        assert second.status_code == 201
        second_data = second.json()

        assert second_data["id"] == first_data["id"]
        assert second_data["event_type"] == first_data["event_type"]


class TestAlerts:
    async def test_list_alerts_empty(self, client: AsyncClient, lojista: dict):
        resp = await client.get("/alerts", headers=lojista["headers"])
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_list_alerts_after_critical_chaos(self, client: AsyncClient, lojista: dict, motorista: dict):
        store_resp = await client.post(
            "/places/stores",
            json={"name": "Loja Alerta", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        await client.post(
            f"/deliveries/{delivery_id}/chaos",
            json={"event_type": "deslizamento", "impact_factor": 3.0, "delay_minutes": 90},
            headers=lojista["headers"],
        )

        alerts_resp = await client.get("/alerts", headers=lojista["headers"])
        assert alerts_resp.status_code == 200
        data = alerts_resp.json()
        assert len(data) >= 1
        assert data[0]["delivery_id"] == delivery_id
        assert data[0]["is_critical"] is True

    async def test_list_alerts_filter_by_delivery(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F4", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S4", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        await client.post(
            f"/deliveries/{delivery_id}/chaos",
            json={"event_type": "deslizamento", "impact_factor": 3.0, "delay_minutes": 90},
            headers=lojista["headers"],
        )

        resp = await client.get(f"/alerts?delivery_id={delivery_id}", headers=lojista["headers"])
        assert resp.status_code == 200
        data = resp.json()
        assert all(a["delivery_id"] == delivery_id for a in data)

    async def test_list_alerts_requires_auth(self, client: AsyncClient):
        resp = await client.get("/alerts")
        assert resp.status_code in (401, 403)

    async def test_dismissed_alert_not_in_list(self, client: AsyncClient, lojista: dict, motorista: dict):
        store_resp = await client.post(
            "/places/stores",
            json={"name": "Loja Dismiss", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F-Dismiss", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        await client.post(
            f"/deliveries/{delivery_id}/chaos",
            json={"event_type": "deslizamento", "impact_factor": 3.0, "delay_minutes": 90},
            headers=lojista["headers"],
        )

        alerts_resp = await client.get("/alerts", headers=lojista["headers"])
        assert alerts_resp.status_code == 200
        alerts = alerts_resp.json()
        assert len(alerts) >= 1
        alert_id = alerts[0]["id"]

        dismiss_resp = await client.patch(f"/alerts/{alert_id}/dismiss", headers=lojista["headers"])
        assert dismiss_resp.status_code == 200
        assert dismiss_resp.json()["dismissed_at"] is not None

        final_resp = await client.get("/alerts", headers=lojista["headers"])
        assert final_resp.status_code == 200
        final_alerts = final_resp.json()
        assert all(a["id"] != alert_id for a in final_alerts)

    async def test_old_alert_not_in_list(self, client: AsyncClient, lojista: dict, db_session: AsyncSession):
        from app.infrastructure.orm.alert import Alert as AlertModel

        old_alert = AlertModel(
            id=uuid.uuid4(),
            delivery_id=uuid.uuid4(),
            message="Alerta antigo além do TTL",
            is_critical=False,
            created_at=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30),
            dismissed_at=None,
        )
        db_session.add(old_alert)
        await db_session.commit()

        resp = await client.get("/alerts", headers=lojista["headers"])
        assert resp.status_code == 200
        data = resp.json()
        assert all(a["id"] != str(old_alert.id) for a in data)

    async def test_count_all_excludes_dismissed(self, client: AsyncClient, lojista: dict, motorista: dict):
        store_resp = await client.post(
            "/places/stores",
            json={"name": "Loja Count", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F-Count", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        await client.post(
            f"/deliveries/{delivery_id}/chaos",
            json={"event_type": "deslizamento", "impact_factor": 3.0, "delay_minutes": 90},
            headers=lojista["headers"],
        )

        alerts_resp = await client.get("/alerts", headers=lojista["headers"])
        assert alerts_resp.status_code == 200
        pre_alerts = alerts_resp.json()
        pre_count = len(pre_alerts)

        alert_id = pre_alerts[0]["id"]
        await client.patch(f"/alerts/{alert_id}/dismiss", headers=lojista["headers"])

        final_resp = await client.get("/alerts", headers=lojista["headers"])
        assert final_resp.status_code == 200
        final_alerts = final_resp.json()
        assert len(final_alerts) == pre_count - 1


class TestFullDeliveryCycle:
    async def test_full_delivery_cycle(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "Fábrica Ciclo", "lat": -19.9191, "lng": -43.9386},
            headers=lojista["headers"],
        )
        factory_id = factory_resp.json()["id"]

        store_resp = await client.post(
            "/places/stores",
            json={"name": "Loja Ciclo", "lat": -23.5505, "lng": -46.6333, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        store_id = store_resp.json()["id"]

        # Step 1: Create → pendente
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_id, "store_id": store_id, "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        assert create_resp.status_code == 201
        delivery = create_resp.json()
        delivery_id = delivery["id"]
        assert delivery["status"] == "pendente"
        assert delivery["departed_at"] is None

        # Step 2: Aceitar → aceita
        accept_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "aceita"},
            headers=motorista["headers"],
        )
        assert accept_resp.status_code == 200
        assert accept_resp.json()["status"] == "aceita"
        assert accept_resp.json()["departed_at"] is None

        # Step 3: Iniciar rota → em_transito
        transit_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "em_transito", "lat": -23.5, "lng": -46.6},
            headers=motorista["headers"],
        )
        assert transit_resp.status_code == 200
        assert transit_resp.json()["status"] == "em_transito"
        assert transit_resp.json()["departed_at"] is not None
        assert transit_resp.json()["eta_current"] is not None

        # Step 4: Entregar → entregue
        deliver_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "entregue"},
            headers=motorista["headers"],
        )
        assert deliver_resp.status_code == 200
        assert deliver_resp.json()["status"] == "entregue"

        # Step 5: Concluir → concluida
        complete_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "concluida"},
            headers=motorista["headers"],
        )
        assert complete_resp.status_code == 200
        assert complete_resp.json()["status"] == "concluida"

        # Step 6: Verify final state via GET
        get_resp = await client.get("/deliveries/", headers=lojista["headers"])
        assert get_resp.status_code == 200
        deliveries = get_resp.json()
        final = next(d for d in deliveries if d["id"] == delivery_id)
        assert final["status"] == "concluida"
        assert final["factory_id"] == factory_id
        assert final["store_id"] == store_id
        assert final["driver_id"] == motorista["id"]

        # Step 7: concluida cannot transition further
        invalid_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "pendente"},
            headers=motorista["headers"],
        )
        assert invalid_resp.status_code == 422

    async def test_direct_em_transito_to_concluida(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "Fábrica Direta", "lat": -19.9, "lng": -43.9},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "Loja Direta", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        # pendente → aceita → em_transito
        await client.patch(f"/deliveries/{delivery_id}", json={"status": "aceita"}, headers=motorista["headers"])
        await client.patch(f"/deliveries/{delivery_id}", json={"status": "em_transito", "lat": -23.5, "lng": -46.6}, headers=motorista["headers"])

        # em_transito → concluida (direct, G.1 hotfix)
        direct_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "concluida"},
            headers=motorista["headers"],
        )
        assert direct_resp.status_code == 200
        assert direct_resp.json()["status"] == "concluida"

    async def test_rejects_invalid_transition(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "F-invalida", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "S-invalida", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        create_resp = await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )
        delivery_id = create_resp.json()["id"]

        # pendente → entregue (invalid, should skip aceita and em_transito)
        invalid_resp = await client.patch(
            f"/deliveries/{delivery_id}",
            json={"status": "entregue"},
            headers=motorista["headers"],
        )
        assert invalid_resp.status_code == 422


class TestDashboard:
    async def test_dashboard_returns_summary(self, client: AsyncClient, lojista: dict, motorista: dict):
        factory_resp = await client.post(
            "/places/factories",
            json={"name": "FDash", "lat": -23.0, "lng": -46.0},
            headers=lojista["headers"],
        )
        store_resp = await client.post(
            "/places/stores",
            json={"name": "SDash", "lat": -23.55, "lng": -46.63, "owner_id": lojista["id"]},
            headers=lojista["headers"],
        )
        await client.post(
            "/deliveries/",
            json={"factory_id": factory_resp.json()["id"], "store_id": store_resp.json()["id"], "driver_id": motorista["id"]},
            headers=lojista["headers"],
        )

        resp = await client.get("/dashboard", headers=lojista["headers"])
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_deliveries"] >= 1
        assert isinstance(data["deliveries_by_status"], list)
        assert data["delayed_deliveries"] >= 0
        assert data["total_alerts"] >= 0
        assert data["critical_alerts"] >= 0
        assert data["active_chaos_events"] >= 0
        assert isinstance(data["chaos_by_type"], list)
