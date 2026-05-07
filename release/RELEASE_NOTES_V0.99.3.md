# Release Notes - V0.99.3 1000-Unit Training Program Seed

## Summary

V0.99.3 starts the 1000-unit quality-controlled debug training program. It does not simply scale official-source snippets; it adds tier targets, public solved-case queues, closure indexing, and a dataset linter.

This is still a founder-pilot candidate. It is not team-wide pilot ready, not V1.0, and not a formally validated operations system.

## Added / Changed

- Added `training/dataset_1000/`:
  - `target_mix.yaml`
  - `status.yaml`
  - `public_solved_case_queue.yaml`
  - `public_case_closure_index.yaml`
  - `README.md`
- Added `scripts/lint_dataset_1000.py`.
- Added 20 public solved-case candidates.
- Reviewed 5 public solved cases:
  - `CLR-107-PUBLIC-LSE-FLUX-RESIDUE`
  - `CLR-108-PUBLIC-SPI-ALL-FF-WRONG-CS-NODE`
  - `CLR-109-PUBLIC-I2C-ZEDBOARD-LOW-LEVEL`
  - `CLR-110-PUBLIC-I2C-KINETIS-BITBANG-WORKAROUND`
  - `CLR-111-PUBLIC-I2C-MOISTURE-RTC-SHORT`
- Added 5 regression tests:
  - `REG-LSE-PROBE-START-FLUX-LEAKAGE`
  - `REG-SPI-ALL-FF-CS-MAPPING-FIRST`
  - `REG-I2C-ACK-LOW-THRESHOLD-FIRST`
  - `REG-I2C-RECOVERY-FAILS-CONTROLLER-PERIPHERAL-BRANCH`
  - `REG-I2C-HUMIDITY-GPIO-POWERED-MODULE-DAMAGE`

## Current Training State

- Closed-loop records: 111
- Official-source closures: 100
- Public/forum reviewed records: 10
- Real project reviewed cases: 1
- Regression tests: 29

## Validation

- Python compile: PASS
- Dataset 1000 lint: PASS
- Closed-loop lint: PASS, 111 records
- Regression suite structure: PASS, 29 tests
- Asset lint: PASS, 28 assets, legacy warnings only
- Real project case lint: PASS, 1 case
- Output validator smoke: PASS, 5 cases
