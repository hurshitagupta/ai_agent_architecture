# AI Agent Architecture Review

## Overview

This project is a capstone-style implementation and review of an AI agent architecture.

The goal is not to build a large end-user application, but to design, inspect, test, harden, and review the main architectural boundaries of an AI agent system.

The project covers:

- Brain
- Planner
- Executor
- Memory
- Tools
- State
- Control loop
- Communication
- Persistence
- Deployment

It also demonstrates how to identify a real architectural weakness, reproduce it with evidence, apply a focused remediation, review remaining operational risks, and generate a final engineering review using an LLM.

---

## Project Objective

The project follows an evidence-driven architecture review process:

1. Define and document the architecture.
2. Reproduce a real reliability or safety weakness.
3. Apply the smallest safe remediation.
4. Review operational risks across the wider system.
5. Generate a final engineering review using verified evidence.

The main weakness selected for this project is:

> The executor initially accepts a tool name without validating whether the tool exists in the registered tool set.

This can cause an unsupported tool request to fail with a `KeyError`.

The remediation adds registry-based tool validation before execution so unsupported tools are safely rejected.

---

## Project Structure

```text
ai_agent_architecture/
│
├── architecture_inventory.py
├── finding_reproduction.py
├── focused_remediation.py
├── operational_review.py
├── review_report.py
│
├── tests/
│   ├── test_architecture_inventory.py
│   ├── test_finding_reproduction.py
│   ├── test_focused_remediation.py
│   ├── test_operational_review.py
│   └── test_review_report.py
│
├── outputs/
│   ├── architecture_inventory.json
│   ├── finding_before.json
│   ├── finding_after.json
│   ├── operational_risk_register.json
│   ├── final_review_report.txt
│   └── final_review_report.json
│
├── docs/
│   └── architecture.md
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Task 1 — Architecture Inventory

## Goal

Document the major components of the AI agent system and clearly define their responsibilities and boundaries.

The inventory contains:

- Brain
- Planner
- Executor
- Memory
- Tools
- State
- Control loop
- Communication
- Persistence
- Deployment

Each component contains:

```text
name
responsibility
boundary
```

Example:

```text
Executor

Responsibility:
Executes approved plan steps and tool calls.

Boundary:
Can only execute registered and validated actions.
```

The architecture diagram is documented in:

```text
docs/architecture.md
```

Generated evidence:

```text
outputs/architecture_inventory.json
```

Run:

```bash
python architecture_inventory.py
```

Test:

```bash
pytest tests/test_architecture_inventory.py -v
```

---

# Task 2 — Finding Reproduction

## Goal

Reproduce one real reliability weakness in the architecture.

The selected finding is:

```text
Area: Tool Execution
Severity: High

Finding:
The executor does not validate tool names before accessing
the tool registry.
```

The original executor performs:

```python
tool = TOOL_REGISTRY[tool_name]
```

A supported tool such as:

```text
get_order
```

executes correctly.

However, an unsupported tool such as:

```text
delete_order
```

causes:

```text
KeyError: 'delete_order'
```

This proves that the implemented executor does not fully enforce the tool boundary defined during the architecture inventory.

Generated evidence:

```text
outputs/finding_before.json
```

Run:

```bash
python finding_reproduction.py
```

Test:

```bash
pytest tests/test_finding_reproduction.py -v
```

---

# Task 3 — Focused Remediation

## Goal

Apply the smallest safe fix for the weakness identified in Task 2.

Instead of redesigning the executor, tool validation is added before accessing the registry.

The remediation checks:

```python
if tool_name not in TOOL_REGISTRY:
```

Unsupported tools now return a controlled response:

```text
status: rejected
reason: unsupported_tool
```

Instead of:

```text
KeyError
```

## Before

```text
Unsupported Tool
        ↓
Tool Registry Lookup
        ↓
KeyError
        ↓
Execution Failure
```

## After

```text
Unsupported Tool
        ↓
Registry Validation
        ↓
Safe Rejection
```

The implementation also validates:

- Missing tool names
- Invalid argument structures
- Invalid tool arguments

Generated evidence:

```text
outputs/finding_after.json
```

Run:

```bash
python focused_remediation.py
```

Test:

```bash
pytest tests/test_focused_remediation.py -v
```

---

# Task 4 — Operational Review

## Goal

Review the wider AI agent architecture for operational risks.

The following areas are reviewed:

```text
Limits
Retries
Secrets
Memory
Tool Authority
Communication
Observability
Deployment
```

Each review item contains:

```text
area
control
evidence
severity
status
recommendation
```

Controls are classified as:

```text
controlled
open
```

Open risks are prioritized by severity.

The current review identifies controlled areas such as:

- Tool authority
- Secret handling expectations
- Retry boundaries
- Execution limits

It also records remaining risks such as:

- Memory retention rules
- Communication schema validation
- Runtime observability
- Deployment validation

The review also determines whether a critical open risk should block release.

Generated evidence:

```text
outputs/operational_risk_register.json
```

Run:

```bash
python operational_review.py
```

Test:

```bash
pytest tests/test_operational_review.py -v
```

---

# Task 5 — Final Engineering Review

## Goal

Generate a final engineering review using the verified evidence produced by Tasks 1–4.

This task uses a real LLM through OpenRouter.

The LLM receives:

```text
architecture_inventory.json
finding_before.json
finding_after.json
operational_risk_register.json
```

The LLM is instructed to use only the supplied evidence and produce:

1. Architecture Summary
2. Primary Finding
3. Impact
4. Remediation
5. Before vs After
6. Residual Risks
7. Recommended Next Action

The LLM is used for summarization and engineering review presentation.

Generated outputs:

```text
outputs/final_review_report.txt

outputs/final_review_report.json
```

Run:

```bash
python review_report.py
```

Test:

```bash
pytest tests/test_review_report.py -v
```

---

# Guardrails

The project includes several safety and reliability controls.

## Validation

Inputs and architecture evidence are validated before use.

Examples include:

- Architecture inventory validation
- Duplicate component rejection
- Tool-name validation
- Tool-argument validation
- Evidence validation
- LLM output validation

---

## Step and Execution Limits

The architecture defines bounded control-loop and retry behavior.

Unbounded loops or repeated tool execution are not permitted.

---

## Timeout

External LLM calls use a configured timeout:

```python
timeout=30.0
```

This prevents the application from waiting indefinitely for an external provider.

---

## Retry Boundary

Retries should only be used for temporary failures such as network or provider errors.

Invalid tool names or validation failures are not retried because they are deterministic failures rather than transient failures.

---

## Secret Hygiene

API credentials are loaded from environment variables.

Example:

```python
api_key = os.getenv("API_KEY")
```

Secrets are not stored directly in source code.

The `.env` file should remain excluded from Git.

---

## Tool Authority

Only tools registered in the tool registry can execute.

Unsupported tools are safely rejected before execution.

---

## Evidence and Traceability

Each stage generates reviewable evidence inside the `outputs/` directory.

---

# Setup

## 1. Create Virtual Environment

Windows:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`
---

## 3. Environment Configuration

Create a `.env` file:

```text
API_KEY=your_openrouter_api_key
BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=your_model_name
```

Do not commit `.env` to Git.

---

# Running the Complete Project

Run the tasks in order:

```bash
python architecture_inventory.py
python finding_reproduction.py
python focused_remediation.py
python operational_review.py
python review_report.py
```

This generates the evidence required by the final review.

---

# Running All Tests

Run:

```bash
pytest -v
```

---

# Architecture Review Flow

```text
Architecture Inventory
        ↓
Define component boundaries
        ↓
Finding Reproduction
        ↓
Unsupported tool causes failure
        ↓
Focused Remediation
        ↓
Registry validation added
        ↓
Regression Tests
        ↓
Operational Review
        ↓
Prioritized residual risks
        ↓
LLM Engineering Review
        ↓
Final Architecture Report
```

---

# Final Result

The project demonstrates an evidence-based approach to reviewing and hardening an AI agent architecture.

Rather than treating architecture quality as an opinion, the project uses:

```text
code
tests
failure reproduction
before/after evidence
risk analysis
traceability
LLM-supported engineering review
```

to evaluate the system.

The final result is a small but complete architecture-hardening workflow that demonstrates how an AI agent can be reviewed before moving toward production use.