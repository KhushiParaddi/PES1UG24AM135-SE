"""Line-coverage tests for pet_walking_service."""
import pytest

from pet_walking_service import inspect_gps_collars, process_walking_routes


def route(**overrides):
    value = {
        "route_confirmed": True,
        "session_type": "standard_30",
        "is_weekend": False,
        "walks": [{"num_pets": 1}],
    }
    value.update(overrides)
    return value


def test_rejects_invalid_routes_and_negative_fee():
    with pytest.raises(ValueError):
        process_walking_routes({}, 0)
    with pytest.raises(ValueError):
        process_walking_routes([], -0.01)


def test_ignores_unconfirmed_routes():
    assert process_walking_routes([route(route_confirmed=False)], 5) == {
        "total_revenue": 0.0, "status": "ZERO_EARNINGS"
    }


@pytest.mark.parametrize(("session", "expected"), [
    ("standard_60", 40.0), ("standard_30", 27.0), ("express_15", 19.0),
])
def test_each_supported_session_type(session, expected):
    result = process_walking_routes([route(session_type=session)], 5)
    assert result == {"total_revenue": expected, "status": "COMPLETED"}


def test_unknown_session_counts_incident_and_skips_route():
    assert process_walking_routes([route(session_type="unknown")], 5)["status"] == "ZERO_EARNINGS"


def test_invalid_walk_is_skipped_and_weekend_fee_applies():
    result = process_walking_routes(
        [route(is_weekend=True, walks=[{"num_pets": 0}, {"num_pets": 2}])], 5
    )
    assert result == {"total_revenue": 37.0, "status": "COMPLETED"}


def test_large_group_discount_and_medication_surcharge():
    result = process_walking_routes(
        [route(walks=[{"num_pets": 4, "needs_meds": True}])], 5
    )
    assert result["total_revenue"] == 54.6


def test_aggression_on_short_walk_skips_base_fee_but_keeps_medication_fee():
    result = process_walking_routes(
        [route(walks=[{"num_pets": 1, "aggression_alert": True, "needs_meds": True}])], 5
    )
    assert result["total_revenue"] == 6.0


def test_aggression_on_hour_walk_cancels_route_earnings():
    walks = [{"num_pets": 2}, {"num_pets": 1, "aggression_alert": True}, {"num_pets": 3}]
    assert process_walking_routes([route(session_type="standard_60", walks=walks)], 5) == {
        "total_revenue": 0.0, "status": "ZERO_EARNINGS"
    }


def test_incident_audit_takes_precedence_over_zero_earnings():
    many_bad_walks = [{"num_pets": 0} for _ in range(5)]
    assert process_walking_routes([route(walks=many_bad_walks)], 5)["status"] == "INCIDENT_AUDIT"


def test_no_walks_results_in_zero_earnings():
    assert process_walking_routes([route(walks=[])], 5)["status"] == "ZERO_EARNINGS"


def test_gps_no_data_and_online_signals():
    assert inspect_gps_collars([]) == "NO_DATA"
    assert inspect_gps_collars(None) == "NO_DATA"
    assert inspect_gps_collars([[20, 19, 20], [0, 20, 19]]) == "ONLINE"


def test_gps_alert_after_two_consecutive_weak_signals():
    assert inspect_gps_collars([[19, 19]]) == "LOST_SIGNAL_ALERT"
    assert inspect_gps_collars([[50], [19, 19]]) == "LOST_SIGNAL_ALERT"



def test_weekend_transport_is_rounded_to_cents():
    result = process_walking_routes(
        [route(is_weekend=True)], 1.237
    )
    assert result == {"total_revenue": 28.24, "status": "COMPLETED"}
