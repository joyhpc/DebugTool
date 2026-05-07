# Founder-Pilot Result Form

Use this record for the real LA1010 / KingstVIS -105 pilot. Leave fields blank until evidence exists.

## Case Metadata

- pilot_id: PILOT-LA1010-KINGSTVIS-105
- date:
- project / board / revision: LA1010 / KingstVIS
- owner:
- reviewer:
- selected mode: Fast Path
- generated output file / version: examples/founder_pilot_la1010_fast_path.md
- validator command: `python scripts/output_validator.py --mode fast_path --file examples/founder_pilot_la1010_fast_path.md`
- validator result:
- assets considered: SIG-USB-NOT-CONNECTED, CASE-LA1010-USB-CABLE

## Original Symptom

- symptom: LA1010 LED on, KingstVIS reports device not connected / error -105
- first observed when:
- reproducibility:
- known-good baseline:
- impact / urgency:

## Context Provided

- architecture: PC USB host -> USB cable -> LA1010 -> KingstVIS
- schematic/log/measurement sources:
- project knowledge sources:
- assumptions: LED on proves some power only; it does not prove USB data enumeration
- missing information: cable type, OS enumeration state, driver state, second-PC result

## Pre-Run Safety Envelope

- safety level: S0
- hazardous domains: none expected for USB enumeration debug
- allowed actions: replace cable, change USB port, inspect Device Manager, reinstall driver/software
- forbidden actions: target-board signal debug before analyzer enumeration is confirmed
- current / voltage / energy / temperature limits: normal USB-only operation
- required protective devices: normal USB host protection
- stop conditions: no enumeration on two known-good data cables and two PCs
- escalation owner:
- waiver required: no

## Mode Decision Record

| Mode | Decision | Reason | Evidence Refs |
|---|---|---|---|
| Fast Path | adopted | symptom matches strong USB-not-connected signature |  |
| Architecture-First | deferred | target-board architecture does not matter until LA1010 enumerates |  |
| Knowledge-Linked | not applied | no project KB needed for first checks |  |
| Assumption-Driven | not applied | enough direct symptom context exists |  |

## Asset Use Record

| Asset ID | Type | Status | Decision | Reason | Evidence Refs |
|---|---|---|---|---|---|
| SIG-USB-NOT-CONNECTED | signature | candidate | adopted | LED-on plus app-not-connected points to USB enumeration path first |  |
| CASE-LA1010-USB-CABLE | case_record | candidate | deferred | useful if cable/driver evidence matches |  |

## Execution Log

| Step | Node ID | Hypothesis / Branch | Action | Safety Limit | Observation / Evidence Ref | Result | Next |
|---|---|---|---|---|---|---|---|
| 1 | D1/A1 | cable may be power-only or faulty | replace with known-good USB data cable | S0 |  | pass/fail/blocked |  |
| 2 | D2/A2 | OS enumeration may fail by port/host | check direct USB port and second PC | S0 |  | pass/fail/blocked |  |
| 3 | D3/A3 | driver/app binding may fail | repair KingstVIS/driver if OS enumeration exists | S0 |  | pass/fail/blocked |  |

## Evidence Pack

| Evidence ID | Source | Timestamp / Revision | Summary | Confidence |
|---|---|---|---|---|
| E1 | Device Manager screenshot/log |  |  | low/medium/high |

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
id: REG-LA1010-KINGSTVIS-105-USB-FIRST
input: LA1010 LED on, KingstVIS reports device not connected / -105
must_select: Fast Path
must_not_select:
must_include:
  - USB
  - Device Manager
  - driver
must_not_include:
  - SPI CPOL/CPHA first
notes:
```
