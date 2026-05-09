# Output Validator Review - 2026-05-08

Scope: local review of `scripts/output_validator.py` against the current DebugTool contract and the proposed reverse specification.

## Covered Now

| area | status |
|---|---|
| CLI mode/file contract | covered: `--mode` choices and `--file` are enforced |
| exit codes | covered: `0` pass, `1` validation failure, `2` file read/parse problem |
| required headings by mode | covered for all supported modes |
| heading order | covered for required headings |
| input-cleaning tables | covered for required tables, required columns, row ids, and confidence enum |
| input-cleaning staleness | covered for `fresh`, `requires_re_verification`, and `archived` enum values |
| node table schema | covered for required columns and row-level enums |
| action-node metadata | covered for action type, tool, safety, cost, reversibility, and evidence refs presence through table schema |
| S2/S3 mitigation language | covered with English and Chinese mitigation tokens |
| Mermaid / node table ID consistency | covered for parseable flowchart node ids |
| retrospective case_record draft presence | partially covered: fenced YAML and `asset_type: case_record` token are required |
| unsafe phrase blocking | covered for high-risk hot-plug/current-limit/shorting phrases |
| Architecture-First semantic guardrails | partially covered: direct-symptom top-two wording, `unknown / model gap`, cost-prior citation, and `p_hit`/`p_exclude`/`time_min` table are required |
| Evidence Audit semantic guardrails | partially covered: reviewer decision block and stable semantic checklist terms are required |
| Skill Improvement structure | partially covered: recognized layer naming, target-case uncertainty, skill defect, and durable artifact class are required |

## Important Gaps

| gap | impact | suggested priority |
|---|---|---|
| Markdown parsing is regex/table based, not a full Markdown AST | complex tables or code blocks can still create false positives/negatives | P1 if validator scope expands |
| Errors usually lack exact line numbers for row-level fields | CI failures are harder to fix quickly | P1 |
| No numeric probability/falsifier/order validation in generated hypothesis tables | structural pass does not prove debug-tree quality; V0.99.10 only checks stable semantic guardrail wording | P1/P2 |
| No knowledge-linked source existence/confidence validation | cited claims may be malformed even if headings pass | P1 |
| Retrospective YAML is not schema-linted against asset schema | draft may pass token check but fail asset promotion | P1 |
| No domain coverage enforcement for video/JTAG/etc. | covered by prompts/assets/regression, not validator | P2 |
| No LLM-backed semantic regression runner | validator cannot judge reasoning correctness | P1 via staged `scripts/regression_run.py` evolution |
| No verbose per-check trace | harder to debug validator behavior itself | P2 |

## Recent Hardening

- Added `--strict` to treat warnings as failures.
- Added read/UTF-8 error handling with exit code `2`.
- Added `scripts/regression_run.py` as a first corpus-reporting step toward semantic regression.
- Added V0.99.10 semantic guardrail checks for Architecture-First, Evidence Audit, Skill Improvement, and Input Cleaning staleness.

## Recommendation

Keep `output_validator.py` as an offline structural validator. Do not overload it with LLM-style semantic judgment. Add semantic quality through the regression corpus runner and reviewed case records, then feed repeated misses back into assets and prompt contracts.
