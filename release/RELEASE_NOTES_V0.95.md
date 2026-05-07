# Release Notes — V0.95 Output Validator Hardening

## Status

Founder-pilot candidate. Not team-wide pilot ready. Not V1.0.

## Release Goal

V0.95 focuses on the first high-value executable layer: making `scripts/output_validator.py` strong enough to catch common structural failures in generated debug outputs.

The release intentionally does not build a matcher, router, or full LLM-backed regression runner yet.

## Major Changes

### 1. Stronger Output Validator

`scripts/output_validator.py` now validates:

- required headings for all supported output modes
- heading order
- Node Explanation Table presence for full-tree modes
- required 12-column node table schema
- row-level enum values
- action-node metadata completeness
- S2/S3 safety-warning or mitigation language
- Mermaid decision-tree node IDs against node table IDs
- retrospective YAML case_record draft presence

### 2. Full Mode Coverage

Supported validation modes:

- `standard`
- `knowledge_linked`
- `fast_path`
- `architecture_first`
- `assumption_driven`
- `retrospective`

### 3. Founder-Pilot Operating Rule

Before using a generated debug answer as a real checklist or asset seed, run:

```bash
python scripts/output_validator.py --mode <mode> --file <output.md>
```

## Validation Results

- Asset lint: passed, 14 assets.
- Regression suite structure lint: passed, 6 tests.
- Output validator smoke test: passed on valid standard output.
- Output validator negative smoke test: failed as expected on missing node columns, missing Mermaid/table ID, and missing S3 safety mitigation.

## Known Limitations

- This validator checks structure, not debug correctness.
- Mermaid parser is intentionally conservative and supports common flowchart node/edge syntax only.
- It does not yet score reasoning quality, evidence sufficiency, or action priority.
- It does not run LLM-backed regression tests.

## Recommended Next Step

Run one real founder-pilot case and require the generated output to pass the validator before retrospective promotion.

Recommended cases:

1. LA1010 / KingstVIS -105 Fast Path.
2. Hot-swap MOSFET / SOA Safety Gate pilot.
