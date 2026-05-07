# Founder-Pilot Result Form

Use one copy per real debug run. Keep seed/demo assumptions separate from measured evidence.

## Case Metadata

- pilot_id:
- date:
- project / board / revision:
- owner:
- reviewer:
- selected mode:
- generated output file / version:
- validator command:
- validator result:
- assets considered:

## Original Symptom

- symptom:
- first observed when:
- reproducibility:
- known-good baseline:
- impact / urgency:

## Context Provided

- architecture:
- schematic/log/measurement sources:
- project knowledge sources:
- assumptions:
- missing information:

## Pre-Run Safety Envelope

- safety level:
- hazardous domains:
- allowed actions:
- forbidden actions:
- current / voltage / energy / temperature limits:
- required protective devices:
- stop conditions:
- escalation owner:
- waiver required:

## Mode Decision Record

| Mode | Decision | Reason | Evidence Refs |
|---|---|---|---|
| Fast Path | adopted/deferred/not applied |  |  |
| Architecture-First | adopted/deferred/not applied |  |  |
| Knowledge-Linked | adopted/deferred/not applied |  |  |
| Assumption-Driven | adopted/deferred/not applied |  |  |

## Asset Use Record

| Asset ID | Type | Status | Decision | Reason | Evidence Refs |
|---|---|---|---|---|---|
|  | link_model/signature/case_record | seed/candidate/validated_real_case | adopted/deferred/not applied |  |  |

## Execution Log

| Step | Node ID | Hypothesis / Branch | Action | Safety Limit | Observation / Evidence Ref | Result | Next |
|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  | pass/fail/blocked |  |

## Evidence Pack

| Evidence ID | Source | Timestamp / Revision | Summary | Confidence |
|---|---|---|---|---|
| E1 | scope/log/photo/schematic/user report |  |  | low/medium/high |

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
id:
input:
must_select:
must_not_select:
must_include:
must_not_include:
notes:
```
