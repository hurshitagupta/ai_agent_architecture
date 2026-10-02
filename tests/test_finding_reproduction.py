import pytest
from finding_reproduction import get_order, vulnerable_execute, reproduce_finding

def test_valid_tool_executes_successfully():

    result = vulnerable_execute(tool_name="get_order", arguments={"order_id": "88213"})

    assert result["status"] == "completed"
    assert result["order_id"] == "88213"
    assert result["order"]["status"] == "shipped"

def test_unknown_order_is_handled():

    result = get_order("99999")

    assert result["status"] == "not_found"
    assert result["order_id"] == "99999"

def test_unsupported_tool_reproduces_failure():

    with pytest.raises(KeyError):
        vulnerable_execute(tool_name="delete_order", arguments={"order_id": "88213"})

def test_finding_is_recorded():

    finding = reproduce_finding()

    assert finding["reproduced"] is True
    assert finding["severity"] == "high"
    assert "KeyError" in finding["evidence"]