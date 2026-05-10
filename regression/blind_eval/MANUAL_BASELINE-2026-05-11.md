# Manual Blind Baseline - 2026-05-11

## Scope

This baseline was created from 8 reviewed closed-loop records across FPGA,
MIPI/eDP, camera/display binding, and I2C field failure patterns.

During the blind pass, only the symptom/background/observation portion was used.
The accepted fix or final resolution was revealed only after the prediction was
frozen.

## Result

| Case | Domain | Blind Verdict | Main Boundary Tested |
|---|---|---:|---|
| BE-CLR-113-FPGA-JTAG-ID | FPGA JTAG | hit | scan-chain power/reset/JTAG integrity before software |
| BE-CLR-116-NIOS-JTAG-NODES | FPGA embedded debug | hit | system debug node exposure before ELF/tool retry |
| BE-CLR-119-ARRIA10-IOPLL-LOCKED | FPGA clocking | hit | lock indicator vs reset/clock dependency |
| BE-CLR-123-JETSON-CSI-TIMEOUT | MIPI CSI | hit | mode/device-tree alignment before sensor replacement |
| BE-CLR-126-MIPI-DPHY-HS | MIPI D-PHY | hit | LP11/stop-state/HS transition ordering |
| BE-CLR-128-CX3-UNUSED-LANES | MIPI CSI lane config | hit | unused lane termination/state before protocol blame |
| BE-CLR-129-IMX8-DSI-HOST-BINDING | MIPI DSI software binding | hit | host graph/binding before bridge silicon blame |
| BE-CLR-111-I2C-HUMIDITY-SHORT | I2C field failure | hit | physical contamination/short before bus recovery loops |

## Interpretation

This is a useful signal, not a capability proof.

What it supports:

- DebugTool can route several public/official-style hardware failures to the
  right first diagnostic boundary.
- It tends to avoid obvious false fast paths such as replacing silicon,
  re-running tools, or blaming protocol state before checking the physical or
  configuration boundary.
- The same cases can now be replayed with frozen raw inputs and hidden expected
  criteria.

What it does not support:

- It is not an automated LLM semantic replay.
- It does not prove probability estimates are calibrated.
- It does not prove the system can handle underspecified real project context.
- It does not prove root-cause identification without measurement updates.

## Promotion Rule

Do not cite this as V1.0 evidence unless future runs include generated outputs
scored by `scripts/run_blind_eval.py --outputs <dir>` and a human reviewer checks
whether each hit was based on valid evidence rather than lucky keyword matching.
