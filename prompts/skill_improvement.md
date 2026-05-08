# Skill Improvement Prompt

You are improving DebugTool itself, not solving the referenced hardware case.

Rules:

- Use `output_contracts/skill_improvement.md`.
- Treat the hardware case as a fixture unless the user explicitly asks for new debug conclusions.
- If the case has no new measurements, do not rerun the same debug tree for a stronger-sounding answer.
- Identify the failing skill layer: intake, routing, link-model contract, output contract, evidence audit, artifact lifecycle, validator, regression, or asset coverage.
- Patch durable artifacts when possible: `SKILL.md`, `routing/`, `output_contracts/`, `prompts/`, `lifecycle/`, `scripts/`, `regression/`, or `assets/`.
- Keep SKILL.md concise; put detailed behavior into directly referenced contract, prompt, lifecycle, or reasoning files.
- Add or update regression fixtures when the user-intent failure should not recur.
- Run applicable validators and linters after changes.

Input:
[PASTE USER CRITIQUE OR FAILURE EXAMPLE]
