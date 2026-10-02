import json
from pathlib import Path
from typing import Any


ORDERS = {"88213": {"status": "shipped", "amount": 1200.0}}

def get_order(order_id: str) -> dict:
    """Return order information for a known order."""

    if not order_id:
        raise ValueError("order_id is required")

    order = ORDERS.get(order_id)

    if order is None:
        return {
            "status": "not_found",
            "order_id": order_id,
        }

    return {
        "status": "completed",
        "order_id": order_id,
        "order": order,
    }

TOOL_REGISTRY = {"get_order": get_order}

def safe_execute(tool_name: str, arguments: dict[str, Any]) -> dict:
    """ Safely execute a registered tool.
    Fix: Validate the requested tool before accessing the registry.  """

    if not tool_name:
        return {
            "status": "rejected",
            "reason": "tool_name_required",
        }

    if tool_name not in TOOL_REGISTRY:
        return {
            "status": "rejected",
            "reason": "unsupported_tool",
            "tool_name": tool_name,
        }

    if not isinstance(arguments, dict):
        return {
            "status": "rejected",
            "reason": "invalid_arguments",
        }

    tool = TOOL_REGISTRY[tool_name]

    try:
        return tool(**arguments)

    except TypeError as error:
        return {
            "status": "rejected",
            "reason": "invalid_tool_arguments",
            "error": str(error),
        }

def create_remediation_evidence() -> dict:
    """ Compare the previous weakness with the remediated behavior. """

    result = safe_execute(tool_name="delete_order", arguments={"order_id": "88213"})

    return {
        "finding": "Executor did not validate tool names before execution.",
        "severity": "high",
        "remediation": "Added tool registry validation before execution.",
        "before": {
            "behavior": "Unsupported tool raised KeyError.",
            "status": "unsafe_failure"
        },
        "after": {
            "behavior": result,
            "status": "safe_rejection"
        },
        "fixed": result["status"] == "rejected" and result["reason"] == "unsupported_tool",
        "residual_risk": "Tool arguments still depend on each tool's validation rules."
    }

def save_evidence(evidence: dict) -> Path:
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "finding_after.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(evidence, file, indent=2)

    return output_path

if __name__ == "__main__":

    print("Focused Remediation")
    print("-" * 50)

    valid_result = safe_execute(tool_name="get_order", arguments={"order_id": "88213"})

    print("\nValid tool execution:")
    print(valid_result)

    invalid_result = safe_execute(tool_name="delete_order", arguments={"order_id": "88213"})

    print("\nUnsupported tool execution:")
    print(invalid_result)

    evidence = create_remediation_evidence()

    print("\nRemediation Summary")
    print(f"Finding: {evidence['finding']}")
    print(f"Severity: {evidence['severity']}")
    print(f"Remediation: {evidence['remediation']}")
    print(f"Fixed: {evidence['fixed']}")
    print(f"Residual risk: {evidence['residual_risk']}")

    output_path = save_evidence(evidence)

    print(f"\nEvidence saved to: {output_path}")