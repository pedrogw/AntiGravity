import pytest
from app.domain.value_objects.coordinates import Coordinates
from app.domain.services.eta_service import calculate_eta_between_coordinates


class TestEtaService:
    def test_eta_sp_to_rj_at_80kmh(self):
        sp = Coordinates(lat=-23.5505, lng=-46.6333)
        rj = Coordinates(lat=-22.9068, lng=-43.1729)
        hours = calculate_eta_between_coordinates(sp, rj, 80)
        assert 4.0 <= hours <= 5.0

    def test_eta_zero_distance(self):
        point = Coordinates(lat=-23.55, lng=-46.63)
        hours = calculate_eta_between_coordinates(point, point, 80)
        assert hours == 0.0

    def test_eta_short_distance(self):
        a = Coordinates(lat=-23.55, lng=-46.63)
        b = Coordinates(lat=-23.56, lng=-46.64)
        hours = calculate_eta_between_coordinates(a, b, 40)
        assert 0 < hours < 1.0

    def test_eta_uses_speed_correctly(self):
        a = Coordinates(lat=-23.55, lng=-46.63)
        b = Coordinates(lat=-22.90, lng=-43.17)
        slow = calculate_eta_between_coordinates(a, b, 40)
        fast = calculate_eta_between_coordinates(a, b, 80)
        assert slow == pytest.approx(fast * 2, rel=0.1)

    def test_eta_negative_speed_raises_error(self):
        a = Coordinates(lat=0, lng=0)
        b = Coordinates(lat=1, lng=1)
        with pytest.raises(ValueError):
            calculate_eta_between_coordinates(a, b, -10)

    def test_eta_pure_no_side_effects(self):
        import inspect
        source = inspect.getsource(calculate_eta_between_coordinates)
        assert "httpx" not in source
        assert "sqlalchemy" not in source
        assert "fastapi" not in source
