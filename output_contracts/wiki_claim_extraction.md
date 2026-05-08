# External Claim Extraction Contract

Use this after querying an external workspace or online knowledge source through an explicit escalation.

The goal is to extract compact, citeable claims. Do not copy long source passages into DebugTool.

```md
# External Claim Extraction

## 1. Retrieval Summary
## 2. Sources Used
## 3. Sources Rejected
## 4. Extracted Claims
## 5. Similar Problem Candidates
## 6. Applicability Limits
## 7. Claims Requiring Board Confirmation
## 8. Impact On Debug Model
```

## Sources Used Table

| source_id | source_ref | source_type | why_used |
|---|---|---|---|
| S1 | ../my-wiki/wiki/... | project_note/datasheet/schematic/debug_record | contains Redriver PWDN behavior |
| S2 | https://vendor.example/... | vendor_doc/standard/app_note/errata | documents protocol behavior |

## Sources Rejected Table

| source_id | source_path | reason_rejected |
|---|---|---|
| R1 | ../my-wiki/raw/... | wrong board revision |

## Extracted Claims Table

| claim_id | claim | source_ref | source_type | confidence | applies_to | needs_confirmation |
|---|---|---|---|---|---|---|
| KC1 | Redriver PWDN is low-enable | ../my-wiki/wiki/... | datasheet | high | specific Redriver part and revision | board-level PWDN voltage |

## Similar Problem Candidates Table

| case_id | source_ref | match_axis | transferable_lesson | limits | action_impact |
|---|---|---|---|---|---|
| SIM1 | training/dataset_1000/mipi_debug_queue.yaml:MIPI-002 | no-output video bridge debug | split source/bridge/panel with test pattern and status registers | MIPI bridge case, not direct eDP evidence | add isolation branch |

## Claim State Rules

- `documented`: source says it, but project measurement has not confirmed it.
- `observed`: measured or logged on the target system.
- `inferred`: derived from documented and observed claims.
- `assumed`: provisional because no source or measurement exists.
- `contradicted`: conflicts with a stronger source or target measurement.

## Rules

- Prefer source paths or URLs over copied text.
- For online claims, cite URLs and prefer official/vendor/standards material.
- Record board revision, part number, firmware version, or document revision when available.
- Mark stale or wrong-revision sources as rejected.
- A datasheet claim can update the link model, but it cannot replace board-level measurement.
- A similar case can update action ordering or model coverage, but it cannot prove the current root cause.
- Explain which hypotheses or action nodes each claim raises, lowers, or leaves unchanged.
