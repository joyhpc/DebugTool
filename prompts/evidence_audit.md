# Evidence Audit Prompt

You are reviewing a DebugTool output for semantic quality, not generating a new debug tree.

Rules:

- Do not treat validator pass as proof of reasoning quality.
- Lead with defects, overclaims, stale branches, missing evidence, and action-ordering problems.
- Separate contract compliance from engineering judgment.
- Do not rewrite the whole debug tree unless the user asks; list required fixes first.
- Use `output_contracts/evidence_audit.md`.
- If the artifact is locally available, inspect it directly before judging.
- If the artifact has not been structurally validated and a validator exists, run the validator first.
- If the review finds fixable issues in a local artifact, patch the artifact and rerun validation when appropriate.
- Always include the Required Semantic Checklist terms from the contract: fact vs inference, stale/non-same-interval evidence, direct symptom top-two, unknown / model gap, cost_priors.yaml or local override, and candidate owner vs confirmed assignment.

Artifact:
[PASTE OR PATH]
