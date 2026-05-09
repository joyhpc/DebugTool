# Skill Improvement Output Contract

Use this contract when the user wants to optimize DebugTool itself: routing, contracts, prompts, validators, lifecycle rules, regression coverage, asset organization, or saved-output quality.

Do not treat the referenced debug case as needing another root-cause analysis unless the user explicitly asks. The case is a fixture for improving the skill.

```md
# Skill Improvement Review

## 1. Improvement Objective
## 2. Triggering Example Or Failure
## 3. Skill Layer Diagnosis
## 4. Target-Case Uncertainty vs Skill Defect
## 5. Required Contract / Routing / Lifecycle Changes
## 6. Regression Coverage To Add Or Update
## 7. Changes Made
## 8. Validation
## 9. Residual Risks
## 10. Next Skill Backlog
```

## Layer Diagnosis

Classify each issue into one or more layers:

- intake: raw user input cleaning, fact/judgment separation, or missing-context handling
- routing: wrong mode, wrong escalation, or failure to recognize user intent
- link_model_contract: missing nodes, boundaries, or evidence-to-move-boundary requirements
- output_contract: missing required section, unclear field, or poor traceability
- evidence_audit: semantic review missing, too weak, or not applied at publish time
- artifact_lifecycle: duplicate outputs, unclear latest file, missing archive/index, or stale saved artifact
- validator: structural check missing, false pass, false fail, or unclear error
- regression: missing fixture that would catch the behavior
- asset_coverage: missing link model, signature, case record, pattern bundle, or principle

Use these layer names or clear equivalents in `Skill Layer Diagnosis`; `scripts/output_validator.py --mode skill_improvement` checks that at least one recognized layer is named.

## Target-Case Uncertainty vs Skill Defect

Always separate:

- target-case uncertainty: facts the real debug team has not measured yet
- skill defect: DebugTool behavior that should be improved even without new target-case evidence

If no new evidence exists, do not invent better probabilities. Improve the process.

## Required Changes

Prefer durable changes in this order:

1. routing rule
2. output contract
3. prompt
4. lifecycle rule
5. validator or linter
6. regression fixture
7. asset update

Do not add broad new complexity when a narrow contract or routing rule fixes the failure.

## Completion Criteria

The improvement is complete only when:

- the failure is stated in skill terms;
- at least one durable skill artifact changed, or a reason for no change is explicit;
- validation commands are run where applicable;
- residual risks and next backlog are clear.
