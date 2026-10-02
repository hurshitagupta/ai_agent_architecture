import json
from pathlib import Path

REQUIRED_AREAS = {"limits", "retries", "secrets", "memory", "tool_authority", "communication", "observability", "deployment"}

SYSTEM_CONTROLS = [{
        "area": "limits",
        "control": "Control loop uses bounded execution and retry limits.",
        "evidence": "Architecture boundary requires hard step and retry limits.",
        "severity": "low",
        "status": "controlled",
        "recommendation": "Keep limits configurable and test limit exhaustion.",
    },
    {
        "area": "retries",
        "control": "Retries are allowed only for transient failures.",
        "evidence": "Invalid tool requests are rejected and are not retried.",
        "severity": "low",
        "status": "controlled",
        "recommendation": "Use capped retries for future external API calls.",
    },
    {
        "area": "secrets",
        "control": "Credentials must come from environment variables.",
        "evidence": "Architecture defines environment-based secret handling.",
        "severity": "low",
        "status": "controlled",
        "recommendation": "Keep .env excluded from source control.",
    },
    {
        "area": "memory",
        "control": "Only validated information should be written to memory.",
        "evidence": "Memory boundary exists, but no retention policy is defined.",
        "severity": "medium",
        "status": "open",
        "recommendation": "Add retention and deletion rules for persistent memory.",
    },
    {
        "area": "tool_authority",
        "control": "Only registered tools may be executed.",
        "evidence": "Task 3 added registry validation before tool execution.",
        "severity": "low",
        "status": "controlled",
        "recommendation": "Continue validating tool arguments and permissions.",
    },
    {
        "area": "communication",
        "control": "Messages should follow a defined communication contract.",
        "evidence": "Communication boundary is documented in architecture inventory.",
        "severity": "medium",
        "status": "open",
        "recommendation": "Add structured message schema validation.",
    },
    {
        "area": "observability",
        "control": "Execution evidence is saved to outputs.",
        "evidence": "Architecture inventory, finding reproduction, and remediation evidence are saved.",
        "severity": "medium",
        "status": "open",
        "recommendation": "Add structured runtime logs and request identifiers.",
    },
    {
        "area": "deployment",
        "control": "Runtime configuration should come from the environment.",
        "evidence": "Deployment boundary is documented, but deployment assumptions are not automated.",
        "severity": "medium",
        "status": "open",
        "recommendation": "Add startup configuration validation before deployment.",
    }]

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def validate_review(controls: list[dict]) -> bool:
    """Validate that the operational review covers all required areas."""

    if not controls:
        raise ValueError("Operational review cannot be empty.")

    reviewed_areas = {item.get("area") for item in controls}

    missing_areas = REQUIRED_AREAS - reviewed_areas

    if missing_areas:
        raise ValueError(f"Missing operational review areas: {sorted(missing_areas)}")

    required_fields = {"area", "control", "evidence", "severity", "status", "recommendation"}

    for item in controls:
        if not required_fields.issubset(item):
            raise ValueError(f"Operational review entry is incomplete: {item.get('area')}")

        if item["severity"] not in SEVERITY_ORDER:
            raise ValueError(f"Invalid severity: {item['severity']}")

        if item["status"] not in {"controlled", "open"}:
            raise ValueError(f"Invalid status: {item['status']}")

    return True


def create_risk_register(controls: list[dict]) -> dict:
    """Create a prioritized register containing the open risks."""

    validate_review(controls)

    open_risks = [item for item in controls if item["status"] == "open"]

    open_risks.sort(key=lambda item: SEVERITY_ORDER[item["severity"]])

    return {
        "areas_reviewed": len(controls),
        "open_risk_count": len(open_risks),
        "controlled_count": len(controls) - len(open_risks),
        "critical_blockers": sum(1 for item in open_risks if item["severity"] == "critical"),
        "release_blocked": any(item["severity"] == "critical" for item in open_risks),
        "risks": open_risks
    }

def save_risk_register(register: dict) -> Path:
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "operational_risk_register.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(register, file, indent=2)

    return output_path

if __name__ == "__main__":

    print("Operational Review")
    print("-" * 60)

    validate_review(SYSTEM_CONTROLS)

    for item in SYSTEM_CONTROLS:
        print(f"\nArea: {item['area']}")
        print(f"Status: {item['status']}")
        print(f"Severity: {item['severity']}")
        print(f"Evidence: {item['evidence']}")

    register = create_risk_register(SYSTEM_CONTROLS)

    print("\nRisk Summary")
    print("-" * 60)

    print(f"Areas reviewed: {register['areas_reviewed']}")
    print(f"Controlled areas: {register['controlled_count']}")
    print(f"Open risks: {register['open_risk_count']}")
    print(f"Critical blockers: {register['critical_blockers']}")
    print(f"Release blocked: {register['release_blocked']}")

    print("\nPrioritized Open Risks")

    for risk in register["risks"]:
        print(f"- [{risk['severity'].upper()}] {risk['area']}: {risk['recommendation']}")

    output_path = save_risk_register(register)

    print(f"\nRisk register saved to: {output_path}")