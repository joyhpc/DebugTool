# Closed-Loop Debug Training

Purpose: turn public/user-provided debug records into stronger skill behavior without blindly copying final answers.

## Workflow

1. Collect a public debug record candidate.
2. Extract only the initial symptom, background, constraints, and observations into `blind_input`.
3. Generate a predicted debug tree before reading or using the final resolution.
4. Reveal the actual resolution.
5. Score whether the predicted tree contained the actual resolution path.
6. Record missing branches, misleading assumptions, and generalized principles.
7. Promote only stable learning into `debug_principle`, `pattern_bundle`, `signature`, `link_model`, or `case_record`.

## Target

Build toward 100 closed-loop records. Do not promote all 100 directly; use them to find repeated principles and failure modes.

## Authoritative Queue

`authoritative_training_queue.yaml` is the source queue for vendor application notes, datasheets, design guides, and official debug checklists. A queue item is not a validated case. It becomes training data only after a blind tree, reveal, coverage score, and meta-reflection are written into `records/`.

## Blindness Limits

Public search snippets and titles may leak part of the answer. Each record should note this risk. The goal is disciplined coverage review, not a laboratory-perfect blind test.

## Cost-Aware Ranking

New reviewed records should include `cost_model` and per-node estimates:

- `p_hit`: chance that the node directly identifies or fixes the dominant fault.
- `p_exclude`: chance that the node cleanly excludes a high-value fault domain.
- `time_min`: expected hands-on time.
- `setup_min`: setup/access time.
- `risk_penalty`: additional cost for risky, disruptive, or hard-to-reverse actions.
- `priority_score`: `(p_hit + 0.5 * p_exclude) / max(time_min + setup_min + risk_penalty, 1)`.

The top-ranked action is not always first: safety gates and prerequisite measurements override the raw score.

## Scoring

- `hit`: predicted tree directly included the actual resolution path.
- `near_hit`: predicted tree included the right fault domain but missed a key step.
- `miss`: predicted tree did not include the actual resolution path.
- `blocked`: source did not provide a usable actual resolution.
