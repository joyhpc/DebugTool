# Release Notes - V0.99.1 Closed-Loop Training Batch and Real Case Intake

## Summary

V0.99.1 continues the authoritative closed-loop training process, promotes existing near-hit lessons into reusable assets, and adds a real-project case intake path.

This is still a founder-pilot candidate. It is not team-wide pilot ready, not V1.0, and not a formally validated operations system.

## Added / Changed

- Upgraded `LM-I2C-BUS` with:
  - false-clock desynchronization
  - reset/transaction sequencing
  - recovery clocks / target reset / buffer recovery
  - device damage, latch-up, and ESD failure-analysis branch
  - counterexamples
- Upgraded `LM-SPI-TRANSACTION` with:
  - command/address phase
  - dummy clocks / turnaround
  - MISO electrical state
  - driver API transaction shape
  - multi-CS / tri-state assumptions
  - counterexamples
- Added signatures:
  - `SIG-I2C-STUCK-FOLLOWS-DEVICE`
  - `SIG-SPI-ALL-FF-TRANSACTION-SHAPE`
- Added real project case intake:
  - `forms/real_project_case_intake_form.md`
  - `training/real_project_cases/README.md`
  - `training/real_project_cases/intake_schema.yaml`
  - `scripts/lint_real_project_cases.py`

## Closed-Loop Training

Reviewed closed-loop records increased from 10 to 18:

- `CLR-011-TI-I2C-CROSSTALK-FALSE-CLOCK`
- `CLR-012-TI-I2C-HOT-INSERTION-STUCK-BUS`
- `CLR-013-TI-I2C-RECOVERY-BUFFER`
- `CLR-014-MICROCHIP-SERIAL-ABSTRACTION-LAYERS`
- `CLR-015-MICROCHIP-I2C-WEAK-PULLUPS-CAPACITANCE`
- `CLR-016-MICROCHIP-SPI-CONSTANT-0XFF-LAYERS`
- `CLR-017-MICROCHIP-MIXED-VOLTAGE-LOGIC-LEVELS`
- `CLR-018-MICROCHIP-SPI-TRISTATE-MULTICS`

Authoritative queue processed markers increased to 12 official training units.

## Regression

Regression structure expanded from 17 to 23 tests:

- `REG-I2C-STUCK-FOLLOWS-DEVICE`
- `REG-SPI-ALL-FF-API-FRAMING-FIRST`
- `REG-SERIAL-LAYERED-DEBUG-FIRST`
- `REG-I2C-RANDOM-NACK-RISETIME-FIRST`
- `REG-SERIAL-VOLTAGE-THRESHOLD-FIRST`
- `REG-SPI-MULTICS-TRISTATE-FIRST`

## Validation

- Python compile: PASS
- Asset lint: PASS, 26 assets, legacy warnings only
- Closed-loop lint: PASS, 18 records
- Regression suite structure: PASS, 23 tests
- Real project case lint: PASS, 0 case files
- Output validator smoke: PASS, 5 cases
