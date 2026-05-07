# Release Notes - V0.98 Closed-Loop Debug Training Seed

Status: founder-pilot candidate. Not team-wide pilot ready. Not V1.0.

## Goal

V0.98 adds a repeatable process for learning from public or user-provided debug records without simply copying final answers. Each record stores blind input, predicted debug tree, actual resolution, coverage score, and meta-reflection.

## Main Changes

- Added `training/closed_loop/` workflow, schema, candidate queue, and 5 reviewed records.
- Added 25 public debug candidate sources across power, I2C, SPI, clocks, CAN, and measurement.
- Added `debug_principle` asset type with `DP-` prefix.
- Added four seed debug principles:
  - `DP-MEASUREMENT-BEFORE-DESIGN-CHANGE`
  - `DP-CONTROL-AUTHORITY-BEFORE-TUNING`
  - `DP-DYNAMIC-EVIDENCE-BEFORE-STATIC-RATING`
  - `DP-CURRENT-LOOP-BEFORE-NAMED-NET`
- Added `scripts/lint_closed_loop.py`.
- Added regression structure cases for I2C reset-overlap stuck SDA, SPI all-0xFF, and MCU package power-mode debug.

## Known Limits

- Only 5 closed-loop records are reviewed so far; the target is 100.
- Public search snippets may leak part of a solution, so records include a blindness note.
- Regression is still structural, not an LLM-backed behavior runner.
- These records are training evidence, not validated real cases.

## Validation Summary

- Python compile: PASS
- Asset lint: PASS, 23 assets
- Regression suite structure: PASS, 13 tests
- Output validator smoke: PASS, 5 cases
- Closed-loop training lint: PASS, 5 records
