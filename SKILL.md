# Debug Decision Tree Skill - V0.99.5 MIPI DSI/CSI Training Branch

## Purpose

Generate efficient, context-aware debug decision trees under explicit safety, evidence, and output constraints.

V0.99.5 is a founder-pilot candidate. It is ready for tightly controlled real pilot runs, article-based seed intake, authoritative-source training, public solved-case training, real-project case intake, Intel/Altera FPGA JTAG/configuration training, MIPI DSI/CSI training, and cost-aware closed-loop debug records, but it is not team-wide pilot ready, not V1.0, and not a formally validated operations system.

## Mandatory Rules

1. Run Safety Gate before any debug action.
2. Do not repeat destructive reproduction without a changed hypothesis and a documented safety envelope.
3. Use current observations over generic experience.
4. Use link models when experience is absent.
5. Do not adopt narrow assets without required evidence.
6. Always list Adopted / Deferred / Not Applied for full-tree modes.
7. Always put the optimal path before the full tree.
8. Every action node must use `output_contracts/node_table_schema.md`.
9. Every action node must include `action_type`, `tool_required`, `safety_level`, `cost`, and `reversibility`.
10. S2/S3 nodes must include explicit safety warning or mitigation language.
11. Mermaid decision-tree node IDs must match Node Explanation Table IDs.
12. Every knowledge-linked claim must include fact source and confidence.
13. Solved cases must produce a case_record draft and regression candidate.
14. Before promoting or saving an output, run `scripts/output_validator.py` with the correct mode.
15. Article/forum/app-note experience bundles must enter as `pattern_bundle` assets before they can influence case_record promotion.
16. Public debug records used for training must preserve blind input, predicted tree, actual resolution, coverage score, and meta-reflection.
17. Full debug trees should rank early actions by probability, time cost, safety risk, and exclusion value.
18. Real project cases must be anonymized and processed through `training/real_project_cases/` before promotion into reusable assets.
19. FPGA JTAG/configuration failures must separate host cable visibility, target VREF, physical JTAG path, configuration-status pins, and internal debug-node visibility before bitstream or IDE changes.
20. MIPI DSI/CSI failures must separate control path, LP11/stopstate, HS clock, HS data, packet counters, VC/data type/ECC/CRC, host graph binding, and downstream display/capture pipeline before blind timing or driver changes.

## Mode Selection Order

```text
1. Safety Gate
2. Signature-Based Fast Path
3. Architecture-First
4. Knowledge-Linked
5. Assumption-Driven
6. Heuristic Context
7. Retrospective after solution
```

## Asset Priority

Use `reasoning/asset_priority.md` as the single source of truth for asset priority.

## Founder-Pilot Rule

Use `lifecycle/founder_pilot_playbook.md` and `forms/founder_pilot_result_form.md` for real runs. A seed asset can be promoted only when measured evidence changes the actual troubleshooting order and creates a regression candidate.

## Seed Intake Rule

Use `pattern_bundle` for user-provided articles, public forum threads, vendor app notes, or pitfall lists. Promote only single, evidence-backed solved runs into `case_record`.

## Closed-Loop Training Rule

Use `training/closed_loop/` for public debug records. A source is not "learned" until the predicted tree has been compared against the actual resolution and the miss/near-hit/hit has been recorded.

## Real Project Case Rule

Use `forms/real_project_case_intake_form.md` and `training/real_project_cases/` for private project cases. Do not promote a real case into `assets/case_records/` unless it is anonymized, evidence-backed, and reviewed.

## Cost-Aware Debug Rule

Use `reasoning/probability_time_cost_model.md` when ordering actions. The fastest theoretical path is the safe dependency-respecting path with the highest expected information per unit time.

## Validator Commands

```bash
python scripts/output_validator.py --mode standard --file output.md
python scripts/output_validator.py --mode knowledge_linked --file output.md
python scripts/output_validator.py --mode architecture_first --file output.md
python scripts/output_validator.py --mode fast_path --file output.md
python scripts/output_validator.py --mode assumption_driven --file output.md
python scripts/output_validator.py --mode retrospective --file retrospective.md
```
