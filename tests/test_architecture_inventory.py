import pytest
from architecture_inventory import get_architecture_inventory, validate_inventory

def test_valid_architecture_inventory():
    inventory = get_architecture_inventory()

    assert validate_inventory(inventory) is True
    assert len(inventory) == 10

    component_names = {component["name"] for component in inventory}

    assert "brain" in component_names
    assert "planner" in component_names
    assert "executor" in component_names
    assert "memory" in component_names
    assert "tools" in component_names
    assert "state" in component_names
    assert "control_loop" in component_names
    assert "communication" in component_names
    assert "persistence" in component_names
    assert "deployment" in component_names


def test_empty_inventory_is_rejected():
    with pytest.raises(ValueError, match="cannot be empty"):
        validate_inventory([])

def test_duplicate_component_is_rejected():
    inventory = [{
            "name": "brain",
            "responsibility": "Processes requests.",
            "boundary": "Does not execute tools.",
        },
        {
            "name": "brain",
            "responsibility": "Duplicate brain.",
            "boundary": "Invalid duplicate component.",
        }]

    with pytest.raises(ValueError, match="Duplicate component"):
        validate_inventory(inventory)