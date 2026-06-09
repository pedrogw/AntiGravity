import pytest
from app.domain.haversine import calculate_haversine_distance
from app.domain.safe_check import is_safe_check_expired
from app.domain.value_objects.coordinates import Coordinates


def test_haversine_polar_extremes():
    dist = calculate_haversine_distance(Coordinates(90.0, 0.0), Coordinates(-90.0, 0.0))
    assert 19900 < dist < 20100


def test_safe_check_none_ping():
    assert is_safe_check_expired(None) is True
