# Release Notes - V0.99 Cost-Aware Closed-Loop Training

## Summary

V0.99 adds probability/time-cost decision ordering and starts an authoritative-source training queue for hardware debug skill development.

This is still a founder-pilot candidate. It is not team-wide pilot ready, not V1.0, and not a formally validated operations system.

## Added

- `reasoning/probability_time_cost_model.md`
  - Defines `p_hit`, `p_exclude`, `time_min`, `setup_min`, `risk_penalty`, and `priority_score`.
  - Safety and dependency constraints override raw score.
- `training/closed_loop/authoritative_training_queue.yaml`
  - 100 official training units from vendor app notes, design guides, checklists, and training material.
  - Queue units are candidates; only reviewed records are treated as learned.
- Cost-aware fields in `training/closed_loop/record_schema.yaml`.
- Cost-aware validation in `scripts/lint_closed_loop.py`.
- `assets/debug_principles/DP-EXPECTED-VALUE-BEFORE-HABIT.yaml`.

## Closed-Loop Training

Reviewed records increased from 5 to 10:

- `CLR-006-TI-I2C-STUCK-BUS-FALSE-CLOCK`
- `CLR-007-MICROCHIP-SERIAL-HIDDEN-SHORTS`
- `CLR-008-ST-OSCILLATOR-STARTUP-MARGIN`
- `CLR-009-TI-SWITCHING-RIPPLE-MEASUREMENT`
- `CLR-010-ADI-HOTSWAP-MOSFET-SOA`

The earlier five closed-loop records were upgraded with the same probability/time-cost fields.

## Regression

Regression structure expanded from 13 to 17 tests:

- `REG-I2C-STUCK-FALSE-CLOCK-RECOVERY`
- `REG-SERIAL-HIDDEN-PUSHPULL-CONTENTION`
- `REG-OSCILLATOR-NO-START-MARGIN-FIRST`
- `REG-COST-AWARE-DEBUG-ORDERING`

## Validation

- Python compile: PASS
- Asset lint: PASS, 24 assets, legacy warnings only
- Regression suite structure: PASS, 17 tests
- Output validator smoke: PASS, 5 cases
- Closed-loop lint: PASS, 10 records
