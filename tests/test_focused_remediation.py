from focused_remediation import safe_execute, create_remediation_evidence

def test_registered_tool_executes_successfully():

    result = safe_execute(tool_name="get_order", arguments={"order_id": "88213"})

    assert result["status"] == "completed"
    assert result["order_id"] == "88213"

def test_unsupported_tool_is_safely_rejected():

    result = safe_execute(tool_name="delete_order", arguments={"order_id": "88213"})

    assert result["status"] == "rejected"
    assert result["reason"] == "unsupported_tool"
    assert result["tool_name"] == "delete_order"

def test_missing_tool_name_is_rejected():

    result = safe_execute(tool_name="", arguments={"order_id": "88213"})

    assert result["status"] == "rejected"
    assert result["reason"] == "tool_name_required"

def test_invalid_argument_structure_is_rejected():

    result = safe_execute(tool_name="get_order", arguments="88213")

    assert result["status"] == "rejected"
    assert result["reason"] == "invalid_arguments"

def test_invalid_tool_arguments_are_rejected():

    result = safe_execute(tool_name="get_order", arguments={"wrong_field": "88213"})

    assert result["status"] == "rejected"
    assert result["reason"] == "invalid_tool_arguments"


def test_remediation_evidence_confirms_fix():

    evidence = create_remediation_evidence()

    assert evidence["fixed"] is True
    assert evidence["after"]["status"] == "safe_rejection"