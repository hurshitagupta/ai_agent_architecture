import pytest
import review_report

def sample_evidence():
    return {
        "architecture_inventory": [{"name": "brain", "responsibility": "Interprets requests.", "boundary": "Does not execute tools."}],
        "finding_before": {"finding": "Executor did not validate tool names.", "severity": "high", "reproduced": True},
        "finding_after": {"remediation": "Added tool registry validation.", "fixed": True, "residual_risk": "Tool arguments require validation."},
        "operational_risk_register": {"open_risk_count": 2, "release_blocked": False, "risks": []}
            }

def test_valid_evidence_is_accepted():
    evidence = sample_evidence()

    assert review_report.validate_evidence(evidence) is True

def test_missing_evidence_is_rejected():

    evidence = sample_evidence()
    del evidence["finding_before"]

    with pytest.raises(ValueError, match="Missing review evidence"):
        review_report.validate_evidence(evidence)

def test_empty_architecture_inventory_is_rejected():

    evidence = sample_evidence()
    evidence["architecture_inventory"] = []

    with pytest.raises(ValueError, match="Architecture inventory cannot be empty"):
        review_report.validate_evidence(evidence)

def test_prompt_contains_project_evidence():

    evidence = sample_evidence()
    prompt = review_report.build_review_prompt(evidence)

    assert "Executor did not validate tool names" in prompt
    assert "Added tool registry validation" in prompt
    assert "Operational Risk Register" in prompt

def test_review_report_uses_llm_response(monkeypatch):

    evidence = sample_evidence()

    monkeypatch.setattr(review_report, "load_project_evidence", lambda: evidence)
    monkeypatch.setattr(review_report, "call_llm",
        lambda prompt: (
            "Architecture Summary\n"
            "The reviewed agent uses separated architecture boundaries.\n\n"
            "Primary Finding\n"
            "Unsupported tool names were not validated.\n\n"
            "Remediation\n"
            "Tool registry validation was added."
        ))

    result = review_report.create_review_report()

    assert result["status"] == "completed"
    assert "Unsupported tool names" in result["report"]


def test_empty_llm_response_is_rejected(monkeypatch):

    evidence = sample_evidence()

    monkeypatch.setattr(review_report, "load_project_evidence", lambda: evidence)
    monkeypatch.setattr(review_report, "call_llm", lambda prompt: "")

    with pytest.raises(ValueError, match="LLM returned an empty review report"):
        review_report.create_review_report()