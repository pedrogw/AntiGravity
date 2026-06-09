import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from app.domain.chaos import apply_chaos_to_eta, remove_chaos_from_eta
from app.domain.safe_check import is_safe_check_expired, evaluate_truck_speed_status

# ==== CHAOS SIMULATION TESTS (10 tests) ====

# apply_chaos_to_eta usa datetime.now(timezone.utc) internamente (aware).
# Usamos ETAs em 2050 para que current_eta >> now real,
# tornando o remaining_time essencialmente constante (~24 anos).

_FUTURE = datetime(2050, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
def _dt(y, m, d, h, mi, s=0):
    return datetime(y, m, d, h, mi, s, tzinfo=timezone.utc)

def test_chaos_apply_delay_only():
    base = _FUTURE
    new_eta = apply_chaos_to_eta(base, 1.0, 60)
    assert new_eta == _dt(2050, 6, 1, 13, 0, 0)

def test_chaos_apply_factor_only():
    base = _FUTURE
    new_eta = apply_chaos_to_eta(base, 1.3, 0)
    assert new_eta > base + timedelta(hours=0.3) - timedelta(seconds=5)

def test_chaos_apply_factor_and_delay():
    base = _FUTURE
    new_eta = apply_chaos_to_eta(base, 1.5, 30)
    assert new_eta > base + timedelta(minutes=30)

def test_chaos_apply_zero_impact():
    base = _FUTURE
    new_eta = apply_chaos_to_eta(base, 1.0, 0)
    assert new_eta == base.replace(microsecond=0)

def test_chaos_remove_delay():
    current = _FUTURE + timedelta(hours=1)
    previous = _FUTURE
    reverted = remove_chaos_from_eta(current, previous, 1.0, 60)
    assert reverted == previous

def test_chaos_remove_factor():
    previous = _FUTURE
    current = apply_chaos_to_eta(previous, 1.5, 0)
    reverted = remove_chaos_from_eta(current, previous, 1.5, 0)
    assert reverted == previous.replace(microsecond=0)

def test_chaos_past_eta_adds_delay_only():
    base = _dt(2020, 1, 1, 12, 0, 0)
    new_eta = apply_chaos_to_eta(base, 2.0, 30)
    assert new_eta == _dt(2020, 1, 1, 12, 30, 0)

def test_chaos_apply_invalid_factor():
    with pytest.raises(ValueError, match="Impact factor cannot be negative"):
        apply_chaos_to_eta(_dt(2030, 1, 1, 12, 0, 0), -1.0, 0)

def test_chaos_apply_invalid_delay():
    with pytest.raises(ValueError, match="Delay cannot be negative"):
        apply_chaos_to_eta(_dt(2030, 1, 1, 12, 0, 0), 1.0, -10)

def test_chaos_zero_factor():
    new_eta = apply_chaos_to_eta(_FUTURE, 0.0, 0)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    assert new_eta >= now - timedelta(seconds=2)
    assert new_eta <= now + timedelta(seconds=2)


# ==== SAFE CHECK (6 tests) ====

# is_safe_check_expired usa datetime.utcnow() internamente.
# Como utcnow() é C-level imutável, usamos unittest.mock.patch
# para substituir a referência ao módulo no namespace de safe_check.

def test_safe_check_not_expired():
    frozen = datetime(2030, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.domain.safe_check.datetime") as mock:
        mock.now.return_value = frozen
        mock.timezone = timezone
        mock.timedelta = timedelta
        mock.datetime = datetime
        last_ping = frozen - timedelta(minutes=5)
        assert is_safe_check_expired(last_ping, 10) is False

def test_safe_check_expired():
    frozen = datetime(2030, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.domain.safe_check.datetime") as mock:
        mock.now.return_value = frozen
        mock.timezone = timezone
        mock.timedelta = timedelta
        mock.datetime = datetime
        last_ping = frozen - timedelta(minutes=15)
        assert is_safe_check_expired(last_ping, 10) is True

def test_safe_check_exactly_at_boundary():
    frozen = datetime(2030, 6, 1, 12, 10, 0, tzinfo=timezone.utc)
    with patch("app.domain.safe_check.datetime") as mock:
        mock.now.return_value = frozen
        mock.timezone = timezone
        mock.timedelta = timedelta
        mock.datetime = datetime
        last_ping = frozen - timedelta(minutes=10)
        assert is_safe_check_expired(last_ping, 10) is False

def test_safe_check_future_ping():
    frozen = datetime(2030, 6, 1, 12, 0, 0, tzinfo=timezone.utc)
    with patch("app.domain.safe_check.datetime") as mock:
        mock.now.return_value = frozen
        mock.timezone = timezone
        mock.timedelta = timedelta
        mock.datetime = datetime
        last_ping = frozen + timedelta(minutes=5)
        assert is_safe_check_expired(last_ping, 10) is False

def test_safe_check_none_ping():
    assert is_safe_check_expired(None) is True

def test_truck_speed_moving():
    assert evaluate_truck_speed_status(60.0) == "moving"

def test_truck_speed_stopped():
    assert evaluate_truck_speed_status(0.0) == "stopped"

def test_truck_speed_negative():
    with pytest.raises(ValueError, match="Speed cannot be negative"):
        evaluate_truck_speed_status(-5.0)
