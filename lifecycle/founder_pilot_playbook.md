# Founder-Pilot Playbook

Purpose: run a small number of real debug cases before any team-wide rollout.

## Entry Criteria

A case is suitable for founder-pilot when:

1. The symptom is real, not invented only for demos.
2. The user can provide at least one of: architecture, schematic excerpt, log, measurement, screenshot, or known-good comparison.
3. The safety envelope is known or can be made conservative.
4. The expected output can be executed within one debug session or reviewed by an engineer.
5. The case can produce a retrospective, even if the root cause is not fully solved.

## Required Run Artifacts

For every founder-pilot case, capture:

- original user problem statement
- selected mode and rejected modes
- safety gate result
- adopted/deferred/not-applied assets
- generated debug output
- validator result if a node table is required
- evidence-audit result before publishing or sharing the saved output
- case artifact location following `lifecycle/case_artifact_hygiene.md`
- executed actions and observations
- final root cause, or current unresolved state
- retrospective and asset update proposal
- regression candidate

## Run Protocol

Before running:

1. Copy `forms/founder_pilot_result_form.md`.
2. Freeze the original symptom and context before generating a debug tree.
3. Record selected mode, rejected modes, and adopted/deferred/not-applied assets.
4. Define the safety envelope before any action, including hard stop conditions.
5. Run `scripts/output_validator.py` when the selected mode has an output contract.
6. Save outputs using `lifecycle/case_artifact_hygiene.md` when the case produces more than one artifact.

During the run:

1. Execute only the current node or explicitly documented branch.
2. Record each observation as an evidence item, not only as a conclusion.
3. If a measurement contradicts the selected link model, stop and reroute instead of forcing the tree.
4. For S2/S3 cases, treat any missing protection limit as a blocked step.

After the run:

1. Classify the outcome as confirmed root cause, excluded fault domain, or unresolved.
2. Write the retrospective before editing any asset.
3. Promote only evidence-backed learning; keep weak learning as a retrospective note.
4. Add or update a regression only when the expected behavior can be stated as assertions.
5. Run Evidence Audit before treating a generated output as publish-ready or as reusable reference material.

## Initial Target Pilots

Use these as the first two closure loops:

1. LA1010 / KingstVIS -105: validate Fast Path behavior and USB-not-connected signature usefulness.
2. High-side MOSFET hot-swap / SOA / large-capacitance inrush: validate Safety Gate, S2/S3 node handling, and hot-swap seed asset usefulness.

## Outcome Classification

- run-only: useful execution record, but no asset change.
- retrospective-note: learning exists, but evidence is not strong enough for promotion.
- promotion-candidate: evidence supports a case_record or link_model update.
- regression-added: a stable expected behavior is captured in the regression suite.

## Stop Conditions

Stop or downgrade a founder-pilot case when:

- a recommended step would require destructive reproduction without a safe envelope
- required measurement access is unavailable
- user-provided facts conflict with the selected link model
- the decision tree drifts into generic checklist behavior
- output validator fails and the failure is not intentionally waived
- no new evidence exists and the current work is really skill optimization, not case execution

## Promotion Rule

A founder-pilot case can strengthen an asset only when:

1. the root cause or excluded fault domain is backed by evidence
2. the asset changed the actual troubleshooting order
3. at least one misleading path was avoided
4. a regression test can be written
5. safety rules were followed

If those conditions are not met, keep the run as a retrospective note, not a promoted asset.
