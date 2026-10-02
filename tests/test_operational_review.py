import pytest
from operational_review import SYSTEM_CONTROLS, create_risk_register, validate_review

def test_complete_operational_review_is_valid():

    result = validate_review(SYSTEM_CONTROLS)
    assert result is True


def test_all_required_areas_are_reviewed():

    reviewed_areas = {item["area"] for item in SYSTEM_CONTROLS}
    expected_areas = {"limits", "retries", "secrets", "memory", "tool_authority", "communication", "observability", "deployment"}

    assert reviewed_areas == expected_areas


def test_missing_review_area_is_rejected():

    incomplete_controls = [item for item in SYSTEM_CONTROLS if item["area"] != "memory"]

    with pytest.raises(ValueError, match="Missing operational review areas"):
        validate_review(incomplete_controls)

def test_risk_register_contains_open_risks():

    register = create_risk_register(SYSTEM_CONTROLS)
    assert register["open_risk_count"] > 0
    assert len(register["risks"]) == register["open_risk_count"]


def test_no_critical_risk_means_release_not_blocked():

    register = create_risk_register(SYSTEM_CONTROLS)
    assert register["critical_blockers"] == 0
    assert register["release_blocked"] is False


def test_critical_risk_blocks_release():

    controls = [item.copy() for item in SYSTEM_CONTROLS]
    for item in controls:
        if item["area"] == "memory":
            item["severity"] = "critical"

    register = create_risk_register(controls)

    assert register["critical_blockers"] == 1
    assert register["release_blocked"] is True