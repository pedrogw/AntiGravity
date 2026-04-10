import pytest
from app.domain.haversine import calculate_haversine_distance
from app.domain.chaos import apply_chaos_to_eta
from datetime import datetime
from app.domain.safe_check import is_safe_check_expired, evaluate_truck_speed_status

def test_haversine_zero_distance():
    # Same point distance should be exactly zero, shouldn't crash
    dist = calculate_haversine_distance(0.0, 0.0, 0.0, 0.0)
    assert dist == 0.0

def test_haversine_polar_extremes():
    # North pole to South pole
    dist = calculate_haversine_distance(90.0, 0.0, -90.0, 0.0)
    assert dist > 19000  # Should be roughly ~20000 km

def test_safe_check_none_ping():
    # Passing None should return True, not TypeError
    assert is_safe_check_expired(None) is True

def test_evaluate_truck_speed_negative():
    # Should raise error if negative
    with pytest.raises(ValueError):
        evaluate_truck_speed_status(-10.0)

def test_chaos_zero_factor():
    eta = datetime.utcnow()
    # Apply zero impact
    new_eta = apply_chaos_to_eta(current_eta=eta, impact_factor=0.0, delay_minutes=0)
    assert new_eta is not None
