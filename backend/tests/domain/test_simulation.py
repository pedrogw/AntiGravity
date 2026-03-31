import pytest
from datetime import datetime, timedelta
from app.domain.chaos import apply_chaos_to_eta, remove_chaos_from_eta
from app.domain.safe_check import is_safe_check_expired, evaluate_truck_speed_status

# ==== CHAOS SIMULATION TESTS (8 tests) ====
def test_chaos_apply_delay_only():
    base = datetime(2030, 1, 1, 12, 0, 0)
    # Acidente: factor 1.0, delay 60
    new_eta = apply_chaos_to_eta(base, 1.0, 60)
    assert new_eta == datetime(2030, 1, 1, 13, 0, 0)

def test_chaos_apply_factor_only():
    base = datetime.utcnow() + timedelta(hours=1)
    # Chuva: factor 1.3
    new_eta = apply_chaos_to_eta(base, 1.3, 0)
    assert new_eta > base

def test_chaos_apply_factor_and_delay():
    base = datetime.utcnow() + timedelta(hours=2)
    new_eta = apply_chaos_to_eta(base, 1.5, 30)
    assert new_eta > base + timedelta(minutes=30)

def test_chaos_apply_zero_impact():
    base = datetime(2030, 1, 1, 12, 0, 0)
    new_eta = apply_chaos_to_eta(base, 1.0, 0)
    assert new_eta == base

def test_chaos_remove_delay():
    current = datetime(2030, 1, 1, 13, 0, 0)
    previous = datetime(2030, 1, 1, 12, 0, 0)
    reverted = remove_chaos_from_eta(current, previous, 1.0, 60)
    assert reverted == previous

def test_chaos_remove_factor():
    previous = datetime.utcnow() + timedelta(minutes=60)
    current = apply_chaos_to_eta(previous, 1.5, 0)
    reverted = remove_chaos_from_eta(current, previous, 1.5, 0)
    # Should revert close to previous
    assert abs((reverted - previous).total_seconds()) < 5

def test_chaos_apply_invalid_factor():
    base = datetime.utcnow()
    with pytest.raises(ValueError):
        apply_chaos_to_eta(base, -1.0, 0)

def test_chaos_apply_invalid_delay():
    base = datetime.utcnow()
    with pytest.raises(ValueError):
        apply_chaos_to_eta(base, 1.0, -10)


# ==== SAFE CHECK LAZY EVALUATION (6 tests) ====
def test_safe_check_not_expired():
    last_ping = datetime.utcnow() - timedelta(minutes=5)
    assert is_safe_check_expired(last_ping, 10) is False

def test_safe_check_expired():
    last_ping = datetime.utcnow() - timedelta(minutes=15)
    assert is_safe_check_expired(last_ping, 10) is True

def test_safe_check_edge_case():
    last_ping = datetime.utcnow() - timedelta(minutes=10)
    # depending on ms it might be True or False, we test > timeout
    assert is_safe_check_expired(last_ping, 9) is True

def test_safe_check_future_ping():
    last_ping = datetime.utcnow() + timedelta(minutes=5)
    assert is_safe_check_expired(last_ping, 10) is False

def test_truck_speed_moving():
    assert evaluate_truck_speed_status(60.0) == "moving"

def test_truck_speed_stopped():
    assert evaluate_truck_speed_status(0.0) == "stopped"

def test_truck_speed_negative():
    with pytest.raises(ValueError):
        evaluate_truck_speed_status(-5.0)
