# Founder-Pilot Result Form

Use this record for the real high-side MOSFET hot-swap / SOA pilot. Leave fields blank until evidence exists.

## Case Metadata

- pilot_id: PILOT-HOTSWAP-MOSFET-SOA
- date:
- project / board / revision:
- owner:
- reviewer:
- selected mode: Architecture-First
- generated output file / version: examples/founder_pilot_hotswap_architecture_first.md
- validator command: `python scripts/output_validator.py --mode architecture_first --file examples/founder_pilot_hotswap_architecture_first.md`
- validator result:
- assets considered: LM-HOTSWAP-HIGHSIDE-MOSFET, SIG-HOTSWAP-INRUSH-SOA-RISK, LM-POWER-CHAIN

## Original Symptom

- symptom: high-side MOSFET burns, overheats, or fails during hot-plug/startup into large downstream capacitance
- first observed when:
- reproducibility:
- known-good baseline:
- impact / urgency:

## Context Provided

- architecture: source/protection -> high-side MOSFET -> downstream capacitance/load
- schematic/log/measurement sources:
- project knowledge sources:
- assumptions: startup SOA risk is plausible but not confirmed until VGS/VDS/ID evidence exists
- missing information: MOSFET part number, SOA curve, output capacitance, gate network, current limit/timer, VGS/VDS/ID waveforms

## Pre-Run Safety Envelope

- safety level: S3 until bounded
- hazardous domains: destructive hot-plug, MOSFET SOA, large-capacitance inrush, connector transient, overtemperature
- allowed actions: schematic review, datasheet SOA review, current-limited startup, precharge/reduced capacitance surrogate, thermal monitoring
- forbidden actions: uncontrolled full-power hot-plug, bypass fuse/eFuse/current limit, remove current limit, force PG/FAULT/EN without rail-order review
- current / voltage / energy / temperature limits:
- required protective devices: current-limited supply or fuse/eFuse/precharge path; thermal monitoring
- stop conditions: instant current-limit hit, VGS abs-max violation, MOSFET/connector heating, uncontrolled input collapse
- escalation owner:
- waiver required: yes for any destructive reproduction

## Mode Decision Record

| Mode | Decision | Reason | Evidence Refs |
|---|---|---|---|
| Fast Path | deferred | safety and architecture dominate before quick fixes |  |
| Architecture-First | adopted | stress path depends on source, gate, capacitance, SOA, and protection sequence |  |
| Knowledge-Linked | deferred | use if schematic/datasheet/project docs are available |  |
| Assumption-Driven | deferred | use only if architecture is missing |  |

## Asset Use Record

| Asset ID | Type | Status | Decision | Reason | Evidence Refs |
|---|---|---|---|---|---|
| LM-HOTSWAP-HIGHSIDE-MOSFET | link_model | candidate | adopted | maps source, gate ramp, capacitance, SOA, and protection sequence |  |
| SIG-HOTSWAP-INRUSH-SOA-RISK | signature | candidate | adopted | symptom matches hot-plug MOSFET failure and inrush risk |  |
| LM-POWER-CHAIN | link_model | candidate | adopted | supplies parent current-limited isolation model |  |

## Execution Log

| Step | Node ID | Hypothesis / Branch | Action | Safety Limit | Observation / Evidence Ref | Result | Next |
|---|---|---|---|---|---|---|---|
| 1 | D1/A1 | uncontrolled reproduction is unsafe | define current-limited safe envelope | current/energy/temp limits TBD |  | pass/fail/blocked |  |
| 2 | A2 | startup SOA may be exceeded | capture VIN, VOUT, VGS, VDS, ID in one controlled startup | S2/S3 envelope |  | pass/fail/blocked |  |
| 3 | A3 | VDS and ID overlap may exceed transient SOA | compare measured pulse to datasheet SOA and thermal impedance | no full-power retry |  | pass/fail/blocked |  |
| 4 | A4/A5 | capacitance, active load, or alternate damage path may dominate | test reduced capacitance/load or inspect polarity/clamp/TVS/short | current limit active |  | pass/fail/blocked |  |

## Evidence Pack

| Evidence ID | Source | Timestamp / Revision | Summary | Confidence |
|---|---|---|---|---|
| E1 | schematic excerpt |  | MOSFET orientation/gate/protection path | low/medium/high |
| E2 | scope capture |  | VIN/VOUT/VGS/VDS/ID startup event | low/medium/high |
| E3 | datasheet/SOA curve |  | transient SOA reference | low/medium/high |

## Outcome

- root cause status: confirmed / excluded fault domain / unresolved
- final root cause:
- effective fix:
- negative findings:
- unresolved branches:
- safety events / near misses:

## Retrospective Inputs

- strong indicators:
- misleading paths avoided:
- misleading paths taken:
- what changed the troubleshooting order:
- asset updates proposed:
- regression test proposal:

## Promotion Gate

| Gate | Pass? | Evidence |
|---|---|---|
| Root cause or excluded domain is evidence-backed | yes/no |  |
| Asset changed troubleshooting order | yes/no |  |
| At least one misleading path was avoided | yes/no |  |
| Regression candidate is writable | yes/no |  |
| Safety rules were followed | yes/no |  |

Promotion recommendation: no promotion / retrospective note only / promote case_record / update link_model / add regression.

## Regression Draft

```yaml
id: REG-HOTSWAP-REAL-SOA-EVIDENCE-FIRST
input: High-side MOSFET burns during hot-plug/startup into large downstream capacitance
must_select: Architecture-First
must_not_select:
must_include:
  - current-limited safe envelope
  - VGS
  - VDS
  - ID
  - SOA
must_not_include:
  - repeat full-power hot-plug
notes:
```
