from datetime import datetime, timezone
from app.domain.entities.delivery import Delivery, EtaHistory
from app.domain.entities.chaos import ChaosEventLog
from app.domain.value_objects.coordinates import Coordinates

_FACTORY_ID = "00000000-0000-0000-0000-000000000001"
_STORE_ID = "00000000-0000-0000-0000-000000000002"
_DRIVER_ID = "00000000-0000-0000-0000-000000000003"

_SP = Coordinates(lat=-23.5505, lng=-46.6333)
_RJ = Coordinates(lat=-22.9068, lng=-43.1729)


def _delivery(eta_current=None, eta_original=None) -> Delivery:
    return Delivery(
        factory_id=_FACTORY_ID,
        store_id=_STORE_ID,
        driver_id=_DRIVER_ID,
        eta_current=eta_current,
        eta_original=eta_original,
    )


def test_recalculate_eta_sets_current_and_original():
    d = _delivery()
    result = d.recalculate_eta(_SP, _RJ, 100.0)

    assert d.eta_original is not None
    assert d.eta_current is not None
    assert d.eta_current == d.eta_original
    assert result is None  # sem eta_before → sem history


def test_recalculate_eta_preserves_original_on_subsequent_calls():
    d = _delivery()
    d.recalculate_eta(_SP, _RJ, 100.0)
    original = d.eta_original

    d.recalculate_eta(_RJ, _RJ, 100.0)
    assert d.eta_original == original


def test_recalculate_eta_returns_history_when_eta_changes():
    d = _delivery()
    d.recalculate_eta(_SP, _RJ, 100.0)
    eta_before = d.eta_current

    result = d.recalculate_eta(_RJ, _SP, 100.0)
    assert isinstance(result, EtaHistory)
    assert result.eta_before == eta_before
    assert result.eta_after == d.eta_current


def test_recalculate_eta_returns_history_when_same_location_different_time():
    d = _delivery()
    d.recalculate_eta(_SP, _SP, 100.0)
    assert d.eta_current is not None

    result = d.recalculate_eta(_SP, _SP, 100.0)
    assert isinstance(result, EtaHistory)  # now muda entre chamadas


def test_recalculate_eta_zero_distance_yields_current_time():
    d = _delivery()
    before = datetime.now(timezone.utc)
    d.recalculate_eta(_SP, _SP, 100.0)
    after = datetime.now(timezone.utc)

    assert d.eta_current is not None
    assert before <= d.eta_current.replace(tzinfo=timezone.utc) <= after


def test_recalculate_eta_with_chaos_aggregation():
    events = [
        ChaosEventLog(
            delivery_id=_FACTORY_ID, event_type="acidente",
            impact_factor=1.5, delay_minutes=10,
        ),
        ChaosEventLog(
            delivery_id=_FACTORY_ID, event_type="engavetamento",
            impact_factor=2.0, delay_minutes=20,
        ),
    ]
    d = _delivery()

    d.recalculate_eta(_SP, _RJ, 100.0, chaos_events=events)
    assert d.eta_current is not None


def test_recalculate_eta_with_empty_chaos_list():
    d = _delivery()
    d.recalculate_eta(_SP, _RJ, 100.0, chaos_events=[])
    assert d.eta_current is not None


def test_recalculate_eta_forwards_reason_to_history():
    d = _delivery()
    d.recalculate_eta(_SP, _RJ, 100.0)

    result = d.recalculate_eta(_RJ, _SP, 100.0, reason="posicao_atualizada")
    assert result is not None
    assert result.reason == "posicao_atualizada"


def test_recalculate_eta_returns_none_when_no_before():
    d = _delivery(eta_current=None)
    result = d.recalculate_eta(_SP, _RJ, 100.0)
    assert result is None
    assert d.eta_current is not None


def test_change_status_pendente_to_aceita_succeeds():
    d = _delivery()
    d.change_status("aceita")
    assert d.status == "aceita"
    assert d.departed_at is None


def test_change_status_pendente_to_em_transito_fails():
    d = _delivery()
    from app.core.exceptions import InvalidTransitionException
    try:
        d.change_status("em_transito")
        assert False, "Deveria ter lançado InvalidTransitionException"
    except InvalidTransitionException:
        pass


def test_change_status_aceita_to_em_transito_succeeds():
    d = _delivery()
    d.change_status("aceita")
    d.change_status("em_transito")
    assert d.status == "em_transito"
    assert d.departed_at is not None


def test_change_status_aceita_to_em_transito_sets_departed_at_once():
    d = _delivery()
    d.change_status("aceita")
    d.change_status("em_transito")
    assert d.departed_at is not None

def test_change_status_em_transito_to_em_transito_fails():
    d = _delivery()
    d.change_status("aceita")
    d.change_status("em_transito")
    from app.core.exceptions import InvalidTransitionException
    try:
        d.change_status("em_transito")
        assert False, "Deveria ter lançado InvalidTransitionException"
    except InvalidTransitionException:
        pass


def test_change_status_aceita_to_pendente_fails():
    d = _delivery()
    d.change_status("aceita")
    from app.core.exceptions import InvalidTransitionException
    try:
        d.change_status("pendente")
        assert False, "Deveria ter lançado InvalidTransitionException"
    except InvalidTransitionException:
        pass


def _delivery_entregue() -> Delivery:
    d = _delivery()
    d.change_status("aceita")
    d.change_status("em_transito")
    d.change_status("entregue")
    return d


def test_change_status_entregue_to_concluida_succeeds():
    d = _delivery_entregue()
    d.change_status("concluida")
    assert d.status == "concluida"


def test_change_status_concluida_to_anything_fails():
    d = _delivery_entregue()
    d.change_status("concluida")
    from app.core.exceptions import InvalidTransitionException
    for invalid_status in ["pendente", "aceita", "em_transito", "entregue", "cancelada"]:
        try:
            d.change_status(invalid_status)
            assert False, f"Deveria ter lançado InvalidTransitionException para {invalid_status}"
        except InvalidTransitionException:
            pass


def test_change_status_em_transito_to_concluida_succeeds():
    d = _delivery()
    d.change_status("aceita")
    d.change_status("em_transito")
    d.change_status("concluida")
    assert d.status == "concluida"
