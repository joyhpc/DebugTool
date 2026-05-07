# Release Notes - V0.96.1 Founder-Pilot Run Readiness

Status: founder-pilot candidate. Not team-wide pilot ready. Not V1.0.

## Goal

V0.96.1 is a narrow readiness pass after V0.96. It does not add more seed assets. It makes the package easier to run against real founder-pilot cases and closes a validator loophole around unsafe wording.

## Main Changes

### 1. Run-ready founder-pilot records

Expanded `forms/founder_pilot_result_form.md` with:

- pre-run safety envelope
- mode decision record
- asset use record
- execution log
- evidence pack
- outcome and retrospective sections
- promotion gate
- regression draft

Added initial run templates:

- `pilot_runs/PILOT-LA1010-KINGSTVIS-105.md`
- `pilot_runs/PILOT-HOTSWAP-MOSFET-SOA.md`

These files are blank execution records, not validated case records.

### 2. Unsafe phrase validator tightening

`scripts/output_validator.py` now requires dangerous advice to have local mitigation on the same line. A safety word elsewhere in the document no longer suppresses unsafe phrase errors.

Added smoke cases and runner:

- `regression/output_validator_smoke_cases/unsafe_phrase_mitigated_good.md`
- `regression/output_validator_smoke_cases/unsafe_phrase_bad_expected_fail.md`
- `scripts/run_output_validator_smoke.py`

### 3. Documentation and environment alignment

- Updated `README.md` and `SKILL.md` to V0.96.1 status.
- Added `requirements.txt` for PyYAML.
- Normalized `3-5 Actions` headings to ASCII across output contracts, validator, examples, and smoke cases.

## Validation Summary

- Python compile: PASS
- Hot-swap Architecture-First example: PASS
- LA1010 Fast Path example: PASS with expected warning because fast_path still does not require a Node Explanation Table
- Output-validator smoke runner: PASS, 5 cases
- Asset lint: PASS, 17 assets, with existing legacy-depth warnings
- Regression suite structure: PASS, 8 tests

## Known Limits

- This is still not an LLM-backed regression runner.
- Legacy link models still need real counterexamples.
- Hot-swap assets remain seed/founder-pilot assets until measured evidence exists.
- The next high-value action is running the two pilot records and promoting only evidence-backed learning.
