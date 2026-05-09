# Evidence Audit Output Contract

Use this contract when the user asks whether a generated debug output, conclusion, probability ranking, or action plan is reliable.

This is a semantic review layer. It does not replace `scripts/output_validator.py`; it runs after structural validation or when the user challenges output quality.

```md
# Evidence Audit

## 1. Artifact Under Review
## 2. Review Verdict
## 3. Contract Compliance
## 4. Evidence Integrity Findings
## 5. Link Model Findings
## 6. Probability And Ranking Findings
## 7. Action Tree Findings
## 8. Missing Or Overclaimed Information
## 9. Required Fixes Before Publish
## 10. Reviewer Decision
```

## Review Verdict

Use one of:

- `pass` - suitable to publish or execute with no material edits.
- `pass_with_minor_fixes` - usable after local wording, ordering, or traceability fixes.
- `needs_revision` - structure may pass, but evidence, model, ranking, or action mapping has material issues.
- `reject` - unsafe, misleading, unsupported, or not actionable.

## Evidence Integrity Checks

Check every material claim against one of these labels:

- fact from user input
- measured evidence
- documented claim
- assumption
- inference
- missing information

Flag:

- inference written as fact;
- source-free adopted assets or knowledge claims;
- stale evidence used as if it were same-interval evidence;
- single-board evidence written as common issue;
- normal control-path evidence used to prove data-path validity;
- root cause language before a falsifying measurement exists.
- stale or non-same-interval evidence changing probabilities.
- chat participants being converted into confirmed owners without explicit assignment.

## Link Model Checks

Verify that the model:

- represents all material control, power/reset/clock, main data, and receiver/downstream paths;
- includes comparison/reference paths when the case depends on front-vs-rear or good-vs-fault asymmetry;
- states known, inferred, unknown, and boundary-moving evidence for each material node;
- preserves weak but relevant clues, even if they are not top probability branches.
- gives model-gap uncertainty a small explicit branch when the architecture could be incomplete.

## Probability And Ranking Checks

Verify that:

- probabilities are marked as engineering priors, not measured truth;
- overlapping hypotheses are called out when probabilities are normalized;
- every probability has evidence that raises and lowers it;
- action ranking is consistent with stated score or explicitly explains exceptions;
- cost estimates are calibrated against `reasoning/cost_priors.yaml` or a stated local override;
- the simplest physical interpretation of the direct symptom is not buried below more remote control/config hypotheses without evidence;
- high-cost actions are gated behind cheaper split measurements unless safety or schedule requires otherwise.

## Required Semantic Checklist

The audit must explicitly state whether these checks pass, fail, or are not applicable:

- fact vs inference split;
- stale or non-same-interval evidence handling;
- direct-symptom simplest-interpretation top-two rule;
- `unknown / model gap` branch presence;
- `reasoning/cost_priors.yaml` usage or a stated local override;
- candidate owner wording vs confirmed assignment.

These phrases are intentionally stable because `scripts/output_validator.py --mode evidence_audit` checks for them mechanically.

## Action Tree Checks

Verify that:

- early actions split competing hypotheses rather than repeat known checks;
- node table IDs match the Mermaid action tree;
- every action has expected observation and interpretation;
- stop/escalation conditions prevent stale or destructive loops;
- owners are assigned only where the source discussion or project context supports assignment.

## Reviewer Decision

The reviewer must end with:

```text
decision: pass | pass_with_minor_fixes | needs_revision | reject
publish_ready: yes | no
required_fixes:
  - ...
residual_risk:
  - ...
```
