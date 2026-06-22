from app.domain.entities.chaos import ChaosEventLog, ChaosAggregate


def test_aggregate_empty_list():
    result = ChaosEventLog.aggregate([])
    assert isinstance(result, ChaosAggregate)
    assert result.total_impact_factor == 1.0
    assert result.total_delay_minutes == 0
    assert result.event_count == 0
    assert result.count_by_type == {}


def test_aggregate_single_event():
    event = ChaosEventLog(
        delivery_id="00000000-0000-0000-0000-000000000001",
        event_type="acidente",
        impact_factor=1.5,
        delay_minutes=30,
    )
    result = ChaosEventLog.aggregate([event])
    assert result.total_impact_factor == 1.5
    assert result.total_delay_minutes == 30
    assert result.event_count == 1
    assert result.count_by_type == {"acidente": 1}


def test_aggregate_multiple_events():
    events = [
        ChaosEventLog(
            delivery_id="00000000-0000-0000-0000-000000000001",
            event_type="acidente", impact_factor=1.5, delay_minutes=30,
        ),
        ChaosEventLog(
            delivery_id="00000000-0000-0000-0000-000000000001",
            event_type="engavetamento", impact_factor=2.0, delay_minutes=60,
        ),
        ChaosEventLog(
            delivery_id="00000000-0000-0000-0000-000000000001",
            event_type="acidente", impact_factor=1.2, delay_minutes=10,
        ),
    ]
    result = ChaosEventLog.aggregate(events)
    assert result.total_impact_factor == 1.5 * 2.0 * 1.2
    assert result.total_delay_minutes == 30 + 60 + 10
    assert result.event_count == 3
    assert result.count_by_type == {"acidente": 2, "engavetamento": 1}


def test_aggregate_default_values():
    event = ChaosEventLog(
        delivery_id="00000000-0000-0000-0000-000000000001",
        event_type="acidente",
    )
    result = ChaosEventLog.aggregate([event])
    assert result.total_impact_factor == 1.0
    assert result.total_delay_minutes == 0
    assert result.count_by_type == {"acidente": 1}


def test_aggregate_single_event_impact_factor_1():
    event = ChaosEventLog(
        delivery_id="00000000-0000-0000-0000-000000000001",
        event_type="acidente",
        impact_factor=1.0,
        delay_minutes=0,
    )
    result = ChaosEventLog.aggregate([event])
    assert result.total_impact_factor == 1.0
    assert result.total_delay_minutes == 0
    assert result.count_by_type == {"acidente": 1}
