import uuid
import datetime
from app.domain.entities.alert import Alert


def test_from_chaos_with_critical_impact_factor():
    alert = Alert.from_chaos(
        delivery_id=uuid.uuid4(),
        message="Caos: deslizamento",
        impact_factor=3.0,
        delay_minutes=10,
    )
    assert alert.is_critical is True
    assert alert.message == "Caos: deslizamento"


def test_from_chaos_with_critical_delay():
    alert = Alert.from_chaos(
        delivery_id=uuid.uuid4(),
        message="Caos: engarrafamento",
        impact_factor=1.0,
        delay_minutes=90,
    )
    assert alert.is_critical is True


def test_from_chaos_with_both_critical():
    alert = Alert.from_chaos(
        delivery_id=uuid.uuid4(),
        message="Caos: deslizamento + engarrafamento",
        impact_factor=5.0,
        delay_minutes=120,
    )
    assert alert.is_critical is True


def test_from_chaos_not_critical():
    alert = Alert.from_chaos(
        delivery_id=uuid.uuid4(),
        message="Caos: chuva leve",
        impact_factor=1.5,
        delay_minutes=10,
    )
    assert alert.is_critical is False


def test_from_chaos_with_custom_thresholds():
    alert = Alert.from_chaos(
        delivery_id=uuid.uuid4(),
        message="Caos: vento",
        impact_factor=1.8,
        delay_minutes=5,
        factor_threshold=1.5,
        delay_threshold=10,
    )
    assert alert.is_critical is True


def test_from_chaos_with_edge_values_exactly_at_threshold():
    alert = Alert.from_chaos(
        delivery_id=uuid.uuid4(),
        message="Caos: exato",
        impact_factor=2.0,
        delay_minutes=60,
    )
    assert alert.is_critical is False


def test_from_chaos_uses_default_thresholds():
    alert_factor = Alert.from_chaos(
        delivery_id=uuid.uuid4(),
        message="Fator exato",
        impact_factor=2.0,
        delay_minutes=0,
    )
    assert alert_factor.is_critical is False

    alert_delay = Alert.from_chaos(
        delivery_id=uuid.uuid4(),
        message="Atraso exato",
        impact_factor=0.5,
        delay_minutes=60,
    )
    assert alert_delay.is_critical is False


def test_from_chaos_sets_delivery_id():
    delivery_id = uuid.uuid4()
    alert = Alert.from_chaos(
        delivery_id=delivery_id,
        message="test",
        impact_factor=0.5,
        delay_minutes=0,
    )
    assert alert.delivery_id == delivery_id


def test_dismiss_marks_dismissed_at():
    alert = Alert(delivery_id=uuid.uuid4(), message="teste")
    now = datetime.datetime.now(datetime.timezone.utc)
    alert.dismiss(now)
    assert alert.dismissed_at == now


def test_dismiss_twice_keeps_first():
    alert = Alert(delivery_id=uuid.uuid4(), message="teste")
    now = datetime.datetime.now(datetime.timezone.utc)
    later = now + datetime.timedelta(hours=1)
    alert.dismiss(now)
    alert.dismiss(later)
    assert alert.dismissed_at == now


def test_is_dismissed_returns_true_after_dismiss():
    alert = Alert(delivery_id=uuid.uuid4(), message="teste")
    assert alert.is_dismissed is False
    alert.dismiss(datetime.datetime.now(datetime.timezone.utc))
    assert alert.is_dismissed is True


def test_dismissed_at_is_none_by_default():
    alert = Alert(delivery_id=uuid.uuid4(), message="teste")
    assert alert.dismissed_at is None
