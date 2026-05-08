# Skill Improvement Review

## 1. Improvement Objective

Improve DebugTool routing so skill-optimization requests do not trigger another same-case debug rerun.

## 2. Triggering Example Or Failure

The user clarified that the A57 case is stalled and should be used to improve the skill.

## 3. Skill Layer Diagnosis

Routing and lifecycle handling need stronger rules.

## 4. Target-Case Uncertainty vs Skill Defect

- Target-case uncertainty: no new A57 measurements exist.
- Skill defect: DebugTool must not rerun the case when the user asks to optimize the skill.

## 5. Required Contract / Routing / Lifecycle Changes

- Add Skill Improvement route.
- Add case artifact hygiene.

## 6. Regression Coverage To Add Or Update

- Add natural-language fixture for skill-optimization intent.

## 7. Changes Made

- Updated routing and lifecycle rules.

## 8. Validation

- Structural validator passes.

## 9. Residual Risks

- No LLM-backed semantic judge exists yet.

## 10. Next Skill Backlog

- Add deeper validator checks for Evidence Audit and Skill Improvement.
