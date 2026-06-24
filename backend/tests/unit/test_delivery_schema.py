import uuid
from datetime import datetime, timezone
from app.schemas.delivery import DeliveryCacheItem
from app.domain.entities.delivery import Delivery


def test_delivery_cache_item_from_entity():
    d = Delivery(
        factory_id=uuid.uuid4(),
        store_id=uuid.uuid4(),
        driver_id=uuid.uuid4(),
    )
    item = DeliveryCacheItem(
        id=d.id,
        factory_id=d.factory_id,
        store_id=d.store_id,
        driver_id=d.driver_id,
        status=d.status,
        eta_original=d.eta_original,
        eta_current=d.eta_current,
        departed_at=d.departed_at,
        current_lat=d.current_lat,
        current_lng=d.current_lng,
    )
    assert item.id == d.id
    assert item.status == "pendente"
    assert item.eta_original is None


def test_delivery_cache_item_roundtrip():
    now = datetime.now(timezone.utc)
    data = DeliveryCacheItem(
        id=uuid.uuid4(),
        factory_id=uuid.uuid4(),
        store_id=uuid.uuid4(),
        driver_id=uuid.uuid4(),
        status="em_transito",
        eta_original=now,
        eta_current=now,
        departed_at=now,
        current_lat=-23.5,
        current_lng=-46.6,
    )
    raw = data.model_dump_json()
    restored = DeliveryCacheItem.model_validate_json(raw)
    assert restored.id == data.id
    assert restored.status == "em_transito"
    assert restored.current_lat == -23.5
    assert restored.eta_original == data.eta_original
    assert restored.departed_at == data.departed_at


def test_delivery_cache_item_reconstructs_entity():
    item = DeliveryCacheItem(
        id=uuid.uuid4(),
        factory_id=uuid.uuid4(),
        store_id=uuid.uuid4(),
        driver_id=uuid.uuid4(),
        status="entregue",
    )
    entity = Delivery(**item.model_dump())
    assert entity.id == item.id
    assert entity.status == "entregue"
    assert entity.factory_id == item.factory_id


def test_delivery_cache_item_defaults():
    item = DeliveryCacheItem(
        id=uuid.uuid4(),
        factory_id=uuid.uuid4(),
        store_id=uuid.uuid4(),
        driver_id=uuid.uuid4(),
        status="pendente",
    )
    assert item.eta_original is None
    assert item.eta_current is None
    assert item.departed_at is None
    assert item.current_lat is None
    assert item.current_lng is None


def test_delivery_cache_item_with_partial_dates():
    now = datetime.now(timezone.utc)
    item = DeliveryCacheItem(
        id=uuid.uuid4(),
        factory_id=uuid.uuid4(),
        store_id=uuid.uuid4(),
        driver_id=uuid.uuid4(),
        status="em_transito",
        eta_current=now,
    )
    assert item.eta_original is None
    assert item.eta_current == now
    assert item.departed_at is None
