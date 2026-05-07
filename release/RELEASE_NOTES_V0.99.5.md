# Release Notes - V0.99.5 MIPI DSI/CSI Training Branch

## Summary

V0.99.5 adds a focused MIPI DSI/CSI branch to the training program. The first batch emphasizes D-PHY LP/HS state transitions, DSI bridge no-video debug, CSI no-frame packet counters, lane configuration, host graph binding, and packet-layer evidence such as data type, byte count, ECC, and CRC.

This remains a founder-pilot candidate. It is not team-wide pilot ready, not V1.0, and not a formally validated operations system.

## Added / Changed

- Added `training/dataset_1000/mipi_debug_queue.yaml` with 20 focused candidates.
- Added `training/dataset_1000/mipi_debug_closure_index.yaml`.
- Extended `scripts/lint_dataset_1000.py` for the MIPI specialized queue.
- Added 10 closed-loop records:
  - `CLR-121-TI-SN65DSI8X-INIT-LP11-HSCLK`
  - `CLR-122-TI-SN65DSI8X-NO-OUTPUT-VIDEO`
  - `CLR-123-NVIDIA-JETSON-CSI-MODE-SETTINGS`
  - `CLR-124-NVIDIA-DRIVE-CSI-CAPTURE-ERRORS`
  - `CLR-125-AMD-MIPI-CSI2-RX-PACKET-COUNTERS`
  - `CLR-126-AMD-MIPI-DPHY-LP11-STOPSTATE-HS`
  - `CLR-127-INTEL-MIPI-CSI2-IP-TROUBLESHOOTING`
  - `CLR-128-INFINEON-CX3-UNUSED-MIPI-LANES`
  - `CLR-129-NXP-IMX8-DSI-HOST-NODE-MISSING`
  - `CLR-130-MIPI-DPHY-LP-HS-TRANSITION-PRIOR`
- Added `LM-MIPI-DSI-CSI-DPHY`.
- Added two signatures:
  - `SIG-MIPI-DSI-BRIDGE-NO-VIDEO-LP11-HSCLK`
  - `SIG-MIPI-CSI-NO-FRAME-PACKET-COUNTERS-FIRST`
- Added 6 regression tests:
  - `REG-MIPI-DSI-BRIDGE-LP11-HSCLK-FIRST`
  - `REG-MIPI-DSI-TEST-PATTERN-LINE-TIME-FIRST`
  - `REG-MIPI-CSI-PACKET-COUNTERS-BEFORE-SETTLE`
  - `REG-MIPI-DPHY-LP11-STOPSTATE-HS-ORDER`
  - `REG-MIPI-CSI-UNUSED-LANES-NOT-FLOATING`
  - `REG-MIPI-DSI-NO-WAVEFORM-HOST-BINDING-FIRST`

## Current Training State

- Closed-loop records: 130
- Official-source closures: 116
- Public/forum reviewed records: 13
- Real project reviewed cases: 1
- Regression tests: 40

## Validation

- Python compile: PASS
- Dataset 1000 lint: PASS
- Closed-loop lint: PASS, 130 records
- Regression suite structure: PASS, 40 tests
- Asset lint: PASS, 34 assets, legacy warnings only
- Real project case lint: PASS, 1 case
- Output validator smoke: PASS, 5 cases
