import pytest
from datetime import datetime, timedelta
from app.domain.haversine import calculate_haversine_distance, calculate_eta, add_hours_to_now

# ==== HAVERSINE / DISTANCE TESTS (10 tests) ====
def test_distance_zero_same_point():
    assert calculate_haversine_distance(-23.5505, -46.6333, -23.5505, -46.6333) == 0.0

def test_distance_sp_to_rj():
    dist = calculate_haversine_distance(-23.5505, -46.6333, -22.9068, -43.1729)
    assert 350 < dist < 370  # ~357 km

def test_distance_short_range():
    dist = calculate_haversine_distance(-23.5505, -46.6333, -23.5605, -46.6433)
    assert 1.0 < dist < 2.0

def test_distance_across_equator():
    dist = calculate_haversine_distance(1.0, -45.0, -1.0, -45.0)
    assert 220 < dist < 225

def test_distance_negative_coords():
    assert calculate_haversine_distance(-10.0, -10.0, -10.0, -10.0) == 0.0

def test_distance_long_range():
    # Brazil to Portugal roughly
    dist = calculate_haversine_distance(-23.5, -46.6, 38.7, -9.1)
    assert 7000 < dist < 8500

def test_distance_equator_meridian():
    # exactly at 0,0
    assert calculate_haversine_distance(0.0, 0.0, 0.0, 1.0) > 110.0

def test_distance_poles():
    # N pole to close
    dist = calculate_haversine_distance(90.0, 0.0, 89.0, 0.0)
    assert 110.0 < dist < 112.0

def test_distance_invalid_large_lat():
    with pytest.raises(ValueError):
        calculate_haversine_distance(100.0, 0, 0, 0)

def test_distance_invalid_large_lng():
    with pytest.raises(ValueError):
        calculate_haversine_distance(0, 200.0, 0, 0)

# ==== ETA TESTS (10 tests) ====
def test_eta_100km_100kmh():
    assert calculate_eta(100.0, 100.0) == 1.0

def test_eta_50km_100kmh():
    assert calculate_eta(50.0, 100.0) == 0.5

def test_eta_zero_distance():
    assert calculate_eta(0.0, 100.0) == 0.0

def test_eta_zero_speed():
    with pytest.raises(ValueError):
        calculate_eta(100.0, 0.0)

def test_eta_negative_distance():
    with pytest.raises(ValueError):
        calculate_eta(-10.0, 100.0)

def test_eta_negative_speed():
    with pytest.raises(ValueError):
        calculate_eta(100.0, -10.0)

def test_eta_large_decimals():
    eta = calculate_eta(333.333, 80.0)
    assert round(eta, 2) == 4.17

def test_eta_add_hours_returns_datetime():
    dt = add_hours_to_now(1.5)
    assert isinstance(dt, datetime)

def test_eta_add_hours_logic():
    now = datetime.utcnow()
    future = add_hours_to_now(2.0)
    diff = future - now
    assert diff.total_seconds() >= 7199

def test_eta_add_zero_hours():
    now = datetime.utcnow()
    res = add_hours_to_now(0.0)
    assert (res - now).total_seconds() < 1
