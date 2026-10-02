from dataclasses import dataclass, asdict
from pathlib import Path
import json

@dataclass
class Component:
    name: str
    responsibility: str
    boundary: str


ARCHITECTURE_COMPONENTS = [
    Component(
        name="brain",
        responsibility="Interprets the user request and decides what should happen next.",
        boundary="Does not directly execute tools or modify external systems.",
    ),
    Component(
        name="planner",
        responsibility="Breaks the request into ordered execution steps.",
        boundary="Creates plans only; execution is handled by the executor.",
    ),
    Component(
        name="executor",
        responsibility="Executes approved plan steps and tool calls.",
        boundary="Can only execute registered and validated actions.",
    ),
    Component(
        name="memory",
        responsibility="Stores and retrieves information required across agent steps.",
        boundary="Only validated information can be written to memory.",
    ),
    Component(
        name="tools",
        responsibility="Provides controlled capabilities such as order lookup or calculations.",
        boundary="Only registered tools with validated arguments can be executed.",
    ),
    Component(
        name="state",
        responsibility="Tracks current request, plan, results, errors, and progress.",
        boundary="Contains runtime state only and does not perform actions.",
    ),
    Component(
        name="control_loop",
        responsibility="Coordinates planning, execution, retries, and stopping conditions.",
        boundary="Must respect configured step and retry limits.",
    ),
    Component(
        name="communication",
        responsibility="Creates structured messages between components and the final response.",
        boundary="Messages must follow a defined communication contract.",
    ),
    Component(
        name="persistence",
        responsibility="Stores selected traces, reports, or persistent records.",
        boundary="Secrets and unvalidated sensitive data must not be persisted.",
    ),
    Component(
        name="deployment",
        responsibility="Defines how the agent is started and configured in its runtime environment.",
        boundary="Configuration and credentials must come from environment variables.",
    )]

def get_architecture_inventory() -> list[dict]:
    return [asdict(component) for component in ARCHITECTURE_COMPONENTS]

def validate_inventory(inventory: list[dict]) -> bool:
    required_fields = {"name", "responsibility", "boundary"}

    if not inventory:
        raise ValueError("Architecture inventory cannot be empty.")

    names = set()

    for component in inventory:
        if not required_fields.issubset(component):
            raise ValueError("Every component must contain name, responsibility, and boundary.")

        if not component["name"].strip():
            raise ValueError("Component name cannot be empty.")

        if component["name"] in names:
            raise ValueError(f"Duplicate component found: {component['name']}")

        names.add(component["name"])

    return True

def save_inventory(inventory: list[dict]) -> Path:
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "architecture_inventory.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=2)

    return output_path

if __name__ == "__main__":
    inventory = get_architecture_inventory()

    validate_inventory(inventory)

    output_path = save_inventory(inventory)

    print("Architecture Inventory")
    print("-" * 60)

    for component in inventory:
        print(f"\nComponent: {component['name']}")
        print(f"Responsibility: {component['responsibility']}")
        print(f"Boundary: {component['boundary']}")

    print(f"\nTotal components: {len(inventory)}")
    print(f"Inventory saved to: {output_path}")