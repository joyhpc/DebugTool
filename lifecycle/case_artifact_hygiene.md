# Case Artifact Hygiene

Use this lifecycle rule whenever DebugTool saves pilot/debug outputs under `pilot_runs/` or a similar workspace directory.

## Directory Rule

Use one subdirectory per real case once a case has more than one generated artifact.

Example:

```text
pilot_runs/a57_edp/
  README.md
  latest-architecture-first.md
  archive/
    input-cleaning-2026-05-08.md
    architecture-first-initial-link-model.md
```

## Current Entry Rule

Keep one current entry point per case and mode:

- `latest-architecture-first.md`
- `latest-input-cleaning.md`
- `latest-knowledge-linked.md`
- `latest-evidence-audit.md`

Do not leave several same-case outputs at the top level of `pilot_runs/`.

## Case Index Rule

Maintain `pilot_runs/CASE_INDEX.md` as the quick-match table for active pilot/debug cases.

The index should include:

- `case_id`;
- aliases and quick-match tokens from real user wording;
- current entry points;
- status and last updated date;
- routing note for special branches.

Before creating a new case artifact, answering where a follow-up should be recorded, or saving a short evidence update, first check the index. If a strong or probable match exists, update the matched case's current entry point instead of creating a new standalone file.

Strong match examples:

- explicit case/project ID, such as `A57`;
- distinctive part number, such as `DS90UB984`;
- two or more aliases from the same index row, such as `AUX` + `CR/EQ` + `训练字`.

If multiple rows match, ask for confirmation before writing.

## Archive Rule

Move superseded outputs into `archive/`.

Do not overwrite archived outputs. If a new archive is needed, choose a filename that preserves the reason or date:

- `architecture-first-before-audit-2026-05-08.md`
- `input-cleaning-raw-chat-2026-05-08.md`

## README Rule

Every multi-artifact case directory should include a small `README.md` with:

- case name;
- current entry point;
- archived outputs;
- maintenance rule or owner notes.

Update `pilot_runs/CASE_INDEX.md` when a case directory is added, renamed, archived, or receives new aliases that users actually use.

## Publish Gate

Before publishing or sharing a saved pilot/debug output:

1. Run the relevant structural validator when one exists.
2. Run Evidence Audit when the output will guide a team, be sent to a project group, or become a reusable reference.
3. Save the reviewed current artifact in the case directory.
4. Archive older same-case outputs.

## Stalled Case Rule

When no new experiment data exists, do not create repeated same-case debug trees. Use the existing latest artifact as the fixture and improve DebugTool contracts, prompts, routing, audits, or regression coverage instead.

## Same-Case Retrieval Failure Rule

If a user points out that a follow-up was not associated with an earlier case, treat it as an artifact-lifecycle and routing defect. Fix the index, aliases, routing prompt, or lifecycle rule so the same wording would match next time.
