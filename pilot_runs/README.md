# Founder-Pilot Run Records

This directory holds real pilot execution records. Files here should be filled from measured evidence, logs, screenshots, schematics, or direct user observations.

Do not promote a pilot record into `assets/case_records/` until the promotion gate in `forms/founder_pilot_result_form.md` passes.

Initial run records:

- `CASE_INDEX.md` - quick-match table for routing short follow-ups to existing pilot cases.
- `PILOT-LA1010-KINGSTVIS-105.md`
- `PILOT-HOTSWAP-MOSFET-SOA.md`
- `a57_edp/latest-architecture-first.md`

Case workspace convention:

- Before creating a new pilot artifact or answering where a case update should be recorded, check `CASE_INDEX.md` for matching aliases.
- Use a subdirectory when a case has more than one generated artifact.
- For complex cases, make `visual-architecture-brief.md` the first reader-facing artifact: system placement, current subsystem, mode gate, evidence stack, and field brief.
- Keep one current entry point per case/mode, for example `a57_edp/latest-architecture-first.md`.
- Move superseded same-case outputs into that case's `archive/` directory instead of leaving duplicate files at the top level.
- Run `python scripts/case_status_report.py <case_dir>` to recover the current evidence, stale items, next actions, and stop conditions without rereading every artifact.

Recommended read order for complex cases:

1. case `README.md`;
2. `visual-architecture-brief.md`;
3. `latest-architecture-first.md`;
4. `field-action-plan.md`;
5. `latest-input-cleaning.md` when fact provenance or stale evidence matters.
