# Input Cleaning Record

## 1. Raw Input Boundary

The raw input is a short user bug report: "rear video path sometimes has no image; AUX is confirmed alive; SerDes CDR does not lock after reset."

## 2. Entity / Alias Normalization

| raw_entity | normalized_entity | source_in_input | note |
|---|---|---|---|
| rear video path | failing video branch | user | Alias kept generic for routing |
| AUX | AUX control channel | user | Control path, not pixel data path |

## 3. Observed / Confirmed Facts

| id | fact | source_in_input | confidence | staleness | affected_link_or_node |
|---|---|---|---|---|---|
| F1 | Rear video path sometimes has no image | user report | high | fresh | video data path |
| F2 | AUX is confirmed alive | user report | high | fresh | control path |
| F3 | SerDes CDR does not lock after reset | user report | high | fresh | receiver CDR |

## 4. Judgments / Inferences / Hypotheses

| id | statement | based_on | confidence | could_be_wrong_if |
|---|---|---|---|---|
| J1 | Pixel-data source or receiver input validity is more suspicious than AUX | F2,F3 | medium | a later capture shows valid data at the receiver input |

## 5. Actions Already Tried And Results

| id | action | target | result | interpretation | evidence_refs |
|---|---|---|---|---|---|
| M1 | Reset SerDes | receiver CDR | no improvement | reset alone does not clear the observed lock failure | F3 |

## 6. Proposed Methods / Pending Actions

| id | proposed_action | owner_if_known | target | expected_evidence | hypothesis_or_link_node |
|---|---|---|---|---|---|
| P1 | Capture decoder output activity in failing state | not stated | data source output | valid or absent data activity | J1 |

## 7. Contradictions / Revisions

| id | previous_statement | revised_statement | why_revised | impact_on_routing |
|---|---|---|---|---|
| R1 | AUX might be blocked | AUX is confirmed alive | F2 | route away from AUX-first debug |

## 8. Missing Information

- Decoder register readback, output activity, power/reset timing, and lane mapping are not yet known.

## 9. Router-Ready Case Brief

Rear video path intermittently has no image. AUX control communication is confirmed alive, but receiver SerDes CDR does not lock and reset does not recover it. Current routing should prioritize architecture-first debug of the data-source output, receiver input validity, power/reset/clock sequencing, and physical data path rather than AUX-first protocol debug.
