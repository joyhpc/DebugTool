# Input Cleaning Contract

Use this contract before safety gating, mode routing, candidate matching, or debug-tree generation.

The goal is not to summarize aggressively. The goal is to preserve all user-provided information while separating what was observed, what was inferred, what was judged, and what was proposed as a method.

```md
# Input Cleaning Record

## 1. Raw Input Boundary
## 2. Entity / Alias Normalization
## 3. Observed / Confirmed Facts
## 4. Judgments / Inferences / Hypotheses
## 5. Actions Already Tried And Results
## 6. Proposed Methods / Pending Actions
## 7. Contradictions / Revisions
## 8. Missing Information
## 9. Router-Ready Case Brief
```

## Required Tables

### Observed / Confirmed Facts

| id | fact | source_in_input | confidence | affected_link_or_node |
|---|---|---|---|---|
| F1 | directly observed or confirmed statement | user / log / waveform / doc | high/medium/low | link node or domain |

Rules:
- Put direct measurements, logs, confirmed communication status, known architecture, and reproducible symptoms here.
- Do not put root-cause guesses here.
- If the user says a prior belief was revised, preserve both the old belief and the revision in `Contradictions / Revisions`.
- If a section has no user-provided content, still include one explicit row such as `not stated` so downstream routing knows the absence was checked.

### Judgments / Inferences / Hypotheses

| id | statement | based_on | confidence | could_be_wrong_if |
|---|---|---|---|---|
| J1 | interpretation or root-cause suspicion | F1,F2 | high/medium/low | evidence that would lower or falsify it |

Rules:
- Put words like "likely", "suspect", "probably", "core problem", "not in X", and "should be Y" here unless directly measured.
- A judgment can drive action priority, but it must not be treated as a fact.

### Actions Already Tried And Results

| id | action | target | result | interpretation | evidence_refs |
|---|---|---|---|---|---|
| M1 | completed method or experiment | node/domain | observed result | what it does or does not prove | F1,F2 |

Rules:
- Separate the method from the interpretation.
- A failed action is still useful evidence if its scope is explicit.

### Proposed Methods / Pending Actions

| id | proposed_action | owner_if_known | target | expected_evidence | hypothesis_or_link_node |
|---|---|---|---|---|---|
| P1 | next proposed debug method | owner | node/domain | pass/fail evidence | H1 or node id |

Rules:
- Proposed actions are not evidence yet.
- Each method should have an expected observation before it is allowed into the debug tree.

### Contradictions / Revisions

| id | previous_statement | revised_statement | why_revised | impact_on_routing |
|---|---|---|---|---|
| R1 | old belief | new evidence-backed statement | F refs | how mode or priority changes |

Rules:
- Preserve important changes in understanding.
- Revisions should lower stale branches explicitly.

## Router-Ready Case Brief

Write a short, cleaned problem statement with:
- Architecture facts.
- Confirmed symptoms.
- Confirmed non-symptoms or excluded branches.
- Current competing hypotheses.
- Immediate evidence gaps.

This brief is the only text that should be passed into `routing/mode_router.md`.

## Natural-Language Intake Rule

The user does not need to fill a form. When the input is vague, keep the original wording, infer only a provisional system boundary, and mark missing facts explicitly. The cleaned brief must still be enough to produce a useful first debug plan with assumptions and targeted next measurements.
