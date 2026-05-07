# Release Notes - V0.96 Founder-Pilot Closure

Status: founder-pilot candidate. Not team-wide pilot ready. Not V1.0.

## Goal

V0.96 reduces the largest remaining founder-pilot gaps after V0.95: shallow power assets, missing hot-swap safety model, missing founder-pilot execution artifacts, and weak asset linting.

## Main Changes

### 1. Reference-depth power model seed

Updated `assets/link_models/LM-POWER-CHAIN.yaml` from a shallow causal-order asset into a deeper seed model with:

- source capability and current limit stage
- input protection path stage
- EN/UVLO/soft-start/sequencing stage
- converter startup/switching stage
- feedback/sense/compensation stage
- load/downstream/backfeed stage
- PG/FAULT propagation stage
- measurement points, strong indicators, actions, counterexamples, and safety notes

### 2. New hot-swap / MOSFET / SOA assets

Added:

- `assets/link_models/LM-HOTSWAP-HIGHSIDE-MOSFET.yaml`
- `assets/signatures/SIG-HOTSWAP-INRUSH-SOA-RISK.yaml`
- `assets/case_records/CASE-HOTSWAP-MOSFET-SOA-SEED.yaml`

These are explicitly seed/founder-pilot assets, not validated real-case assets.

### 3. Founder-pilot execution kit

Added:

- `lifecycle/founder_pilot_playbook.md`
- `forms/founder_pilot_result_form.md`
- `examples/founder_pilot_la1010_fast_path.md`
- `examples/founder_pilot_hotswap_architecture_first.md`

### 4. Validator safety hardening

Updated `scripts/output_validator.py` to catch common unsafe phrases when they appear without explicit mitigation, especially:

- unbounded full-power hot-plug reproduction
- bypassing fuse/eFuse/current-limit/protection
- removing current limit
- unsafe Chinese power-debug phrases such as `无限流`, `取消限流`, `旁路保护`, `直接短接`

### 5. Asset linter hardening

Rewrote `scripts/lint_assets.py` with stricter checks for:

- ID prefix by asset type
- required fields
- enum values for status, safety level, source type, confidence, use_when weights, reference relations
- destructive boolean type
- non-empty use_when
- link_model causal_order depth
- candidate+ link_model debug_rules
- signature top_actions and min_match_count
- case_record root_cause and promotion constraints
- reference integrity

### 6. Regression suite expansion

Updated `regression/minimal_regression_suite.yaml` from 6 to 8 structural regression cases:

- `REG-POWER-CHAIN-NO-REGULATOR-FIRST`
- `REG-HOTSWAP-SOA-SAFE-ENVELOPE`

## Validation Summary

- output validator compile: PASS
- hot-swap architecture-first example: PASS
- LA1010 fast-path example: PASS with expected warning because fast_path contract does not require node table
- asset lint: PASS, 17 assets, with warnings for legacy shallow assets
- regression suite linter: PASS, 8 tests

## Known Limits

- This is still not an LLM-backed regression runner.
- Most legacy link models remain shallow and only produce linter warnings.
- Hot-swap assets are seed/founder-pilot assets, not validated real cases.
- The next major improvement requires actual founder-pilot execution and retrospective evidence.
