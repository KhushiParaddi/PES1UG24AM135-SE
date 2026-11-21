import math
from hypothesis import given, strategies as st

from processor import (
    parse_walk_schedule,
    compute_pace_per_pet,
    lookup_temperament_surcharge
)


@given(st.text() | st.none())
def test_parse_walk_schedule_no_crash(s):
    try:
        result = parse_walk_schedule(s)
        assert isinstance(result, str)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"parse_walk_schedule crashed with: {e}"


@given(st.text() | st.none())
def test_compute_pace_per_pet_safe(s):
    try:
        result = compute_pace_per_pet(s)
        assert isinstance(result, (int, float))
        assert math.isfinite(result)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"compute_pace_per_pet crashed with: {e}"


@given(st.text() | st.none())
def test_lookup_temperament_surcharge_safe(s):
    try:
        result = lookup_temperament_surcharge(s)
        assert isinstance(result, (int, float))
        assert math.isfinite(result)
    except ValueError:
        pass
    except Exception as e:
        assert False, f"lookup_temperament_surcharge crashed with: {e}"