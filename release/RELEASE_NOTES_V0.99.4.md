# Release Notes - V0.99.4 Intel/Altera FPGA Training Branch

## Summary

V0.99.4 adds a focused Intel/Altera FPGA branch to the training program. The first batch emphasizes Quartus Programmer/JTAG scan-chain failures, configuration status pins, Download Cable II setup, JTAG signal integrity, Nios debug-node visibility, Nios ELF download failures, and Arria 10 IOPLL lock behavior.

This remains a founder-pilot candidate. It is not team-wide pilot ready, not V1.0, and not a formally validated operations system.

## Added / Changed

- Added `training/dataset_1000/intel_altera_fpga_queue.yaml` with 20 focused candidates.
- Added `training/dataset_1000/intel_altera_fpga_closure_index.yaml`.
- Extended `scripts/lint_dataset_1000.py` for specialized queues.
- Added 9 closed-loop records:
  - `CLR-112-INTEL-QUARTUS-UNABLE-SCAN-CHAIN`
  - `CLR-113-INTEL-FPGA-JTAG-ID-NOT-RECOGNIZED`
  - `CLR-114-INTEL-FPGA-CONFDONE-NSTATUS-CONFIG`
  - `CLR-115-INTEL-FPGA-JTAG-SIGNAL-INTEGRITY`
  - `CLR-116-INTEL-NIOS-JTAGCONFIG-NODES`
  - `CLR-117-INTEL-DOWNLOAD-CABLE-II-TARGET-PATH`
  - `CLR-118-INTEL-USB-BLASTER-DM-NOT-QUARTUS`
  - `CLR-119-INTEL-ARRIA10-IOPLL-LOCKED-BEHAVIOR`
  - `CLR-120-INTEL-NIOS-ELF-PIN-ASSIGNMENT`
- Added `LM-FPGA-JTAG-CONFIG`.
- Added two signatures:
  - `SIG-QUARTUS-CABLE-SEEN-SCAN-CHAIN-FAIL`
  - `SIG-NIOS-ELF-AFTER-SOF-HARDWARE-MAP`
- Added 5 regression tests:
  - `REG-INTEL-FPGA-QUARTUS-SCAN-CHAIN-PHYSICAL-FIRST`
  - `REG-INTEL-FPGA-JTAG-NCONFIG-NSTATUS-GATE`
  - `REG-INTEL-FPGA-CONFDONE-DCLK-DATA-FIRST`
  - `REG-INTEL-FPGA-NIOS-ELF-HARDWARE-MAP-FIRST`
  - `REG-INTEL-FPGA-IOPLL-LOCK-RESET-CLOCK-FIRST`

## Current Training State

- Closed-loop records: 120
- Official-source closures: 108
- Public/forum reviewed records: 11
- Real project reviewed cases: 1
- Regression tests: 34

## Validation

- Python compile: PASS
- Dataset 1000 lint: PASS
- Closed-loop lint: PASS, 120 records
- Regression suite structure: PASS, 34 tests
- Asset lint: PASS, 31 assets, legacy warnings only
- Real project case lint: PASS, 1 case
- Output validator smoke: PASS, 5 cases
