# Case Governance Rules

Use this lifecycle rule for saved debug cases under `pilot_runs/`.

The goal is to keep case evidence useful over time: current facts stay current, stale information is labeled, wrong conclusions are retracted or archived, and high-attention signals are tied to evidence and next actions.

## Current Artifact Rules

- Current files are `latest-*.md`, `visual-architecture-brief.md`, and `field-action-plan.md`.
- Current files may mention old evidence only when they also include staleness, revision, retraction, or `requires_re_verification` handling.
- Current files that mention high-attention signals must also include evidence/status/next-action/stop-condition handling.
- Candidate owners are not formal assignments until PM/project lead confirmation is stated.

## Visual Architecture Brief Rules

Complex cases need a first-page architecture frame before detailed evidence tables. A case is complex when it has a saved Architecture-First artifact and either a field action plan, multiple mode gates, multiple subsystems, or high-attention debug signals.

Use `forms/visual_architecture_brief_template.md`.

A visual architecture brief must contain:

- executive frame with current conclusion, owning system/subsystem, route, and stop condition;
- system placement diagram;
- currently owning subsystem diagram;
- mode gate that separates current symptom routing from fallback routing;
- high-signal evidence stack;
- field brief with minimum same-window tasks and stop conditions.

The brief is allowed to be case-specific because it lives inside a case directory. It must not promote case-specific part numbers or project names into generic `forms/`, `scripts/`, or `output_contracts/`.

## Archive Rules

- Superseded artifacts go under `archive/`.
- Every archived artifact must be listed from the case `README.md`.
- Archive entries should preserve why the artifact was superseded, either in the README line or in the archived file name.

## Generic Artifact Boundary

Project-specific names, chip IDs, board aliases, and one-case signal names belong in the case directory.

Do not hardcode case-specific names into:

- `forms/`
- `output_contracts/`
- `scripts/`

Use generic placeholders such as `target device`, `conditioner enable pin`, `receiver lock signal`, `case-specific part`, or `project wiki query`.

## Field Action Plan Rules

A field action plan must cite:

- `forms/failure_matrix_template.md`
- `forms/same_window_evidence_batch_checklist.md`

It must also contain:

- executive architecture gate;
- case configuration;
- failure matrix;
- same-window evidence;
- stop conditions.

Run:

```bash
python scripts/lint_case_governance.py
```

For a quick recovery-oriented case summary, run:

```bash
python scripts/case_status_report.py a57_edp
```

## Maintenance Rules

Stop adding generic assets when they lack real cases, duplicate existing assets,
or do not change the optimal debug path.

## Regression Policy

Run regression when adding assets, changing routing, modifying output contracts,
safety rules, validators, or lifecycle governance.

## Retrospective Rules

Capture root cause, effective fix, strong indicators, misleading or low-value
paths, coverage scores, and regression candidates.
