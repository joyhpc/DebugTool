---
name: debug-decision-tree
version: "0.99.13"
api_version: "1"
description: Hardware debug reasoning skill for natural-language bug reports, link-model analysis, hypothesis trees, action decision trees, probability/time-cost ranked troubleshooting, input cleaning, safety gating, and retrospective asset promotion. Use when the assistant needs to analyze a hardware, FPGA, embedded, power, high-speed interface, video, I2C, SPI, MIPI, eDP, PCIe, USB, JTAG, or system bring-up/debug issue; when the user asks for possible causes, probabilities, measurements, debug plan, decision tree, link model, or reusable case learning; or when a terse user bug report needs a complete first-pass debug deliverable.
---

# Debug Decision Tree Skill - V0.99.13 Frozen Artifact Replay

## Purpose

Generate complete hardware debug deliverables from ordinary user language. The user does not need to know the internal modes, asset types, or forms.

This package is still an early-internal-pilot candidate, not V1.0 and not a formally validated operations system. Treat its probabilities as decision priors unless calibrated by solved-case regression.

## Default User Experience

When the user gives any debug symptom, issue note, waveform description, chat excerpt, or "help me debug this" request:

1. Run Input Cleaning using `output_contracts/input_cleaning.md`.
2. If the workspace has `pilot_runs/CASE_INDEX.md`, check it for same-case aliases before deciding this is a new case or answering where to record it.
3. Run Safety Gate before recommending actions.
4. Route using `routing/mode_router.md`.
5. Build the first link model and hypothesis tree from cleaned user input, explicit assumptions, and built-in assets.
6. Treat external workspace knowledge as an escalation path, not the default path.
7. When escalation is triggered, resolve workspace knowledge sources using `retrieval/knowledge_source_resolution.md` and extract compact documented claims using `output_contracts/wiki_claim_extraction.md`.
8. Load only relevant assets after checking `reasoning/asset_priority.md`.
9. Deliver through `output_contracts/default_debug_delivery.md` and the selected mode contract.
10. Include a link model or influence map whenever the failure spans more than one component, interface, power domain, clock/reset path, or software-control boundary.
11. Include possible causes with probability estimates whenever root cause is not confirmed.
12. Include a hypothesis tree and an action decision tree in full debug outputs.
13. If details are missing, make assumptions explicit and ask at most three high-value questions after giving the first safe evidence-gathering actions.

Do not respond with only a questionnaire unless any action would be unsafe.

## Output Language Policy

Match the user's language for user-facing prose. If the user writes the case, critique, or update in Chinese, write explanations, judgments, action items, evidence summaries, audit findings, and final recommendations in Chinese.

Keep fixed contract headings, schema field names, file paths, commands, register names, net names, signal names, and part numbers in their required or original form when changing them would break validation or traceability. When useful, preserve English technical terms in parentheses after Chinese wording.

## Natural Evidence Updates

Users should not need to remember internal terms. Treat ordinary update language as enough to update the debug tree:

```text
有新线索：...
补充一下现场情况：...
刚测到：...
示波器看到：...
寄存器读到：...
这是不是说明方向要改？
帮我更新一下排查策略。
下一步怎么查？
```

For these requests, run the same internal update flow:

1. Preserve the previous case context. If the case is not explicit, use `pilot_runs/CASE_INDEX.md` aliases to find the existing current entry before creating any new artifact.
2. Clean the new information into fact / judgment / method / missing-result buckets.
3. Mark which old assumptions or branches are now weaker, stronger, or unchanged.
4. Update the link model only where the new information changes a node, edge, observable, or downstream effect.
5. Re-rank hypotheses using engineering priors; do not pretend precision.
6. Output the next 1-3 actions in plain language before any full tree detail.

## Skill Improvement Requests

When the user is discussing DebugTool behavior, output quality, routing, contracts, validators, pilot artifacts, or how to improve this skill, do not continue debugging the underlying hardware case unless explicitly asked.

Treat the referenced case as a test fixture:

1. Identify which skill layer failed or needs improvement: intake, routing, link-model contract, output contract, evidence audit, artifact lifecycle, validator, regression, or asset coverage.
2. Separate target-case uncertainty from skill-design defects.
3. Patch skill contracts, prompts, routing, lifecycle rules, validators, or regression fixtures when the improvement is actionable.
4. Do not generate another same-case debug output just to demonstrate progress unless the user asks for a before/after example.
5. Keep artifact directories clean: one current entry point per case/mode; archive superseded outputs.

## Mandatory Rules

0. Run Input Cleaning before Safety Gate, mode routing, candidate matching, or debug-tree generation.
1. Preserve facts, judgments, actions tried, proposed methods, revisions, and missing information separately.
2. Run Safety Gate before any debug action.
3. Do not repeat destructive reproduction without a changed hypothesis and a documented safety envelope.
4. Use current observations over generic experience.
5. Use link models when experience is absent.
6. Do not adopt narrow assets without required evidence.
7. Do not query external knowledge unless the user asks for it or a high-impact gap makes the first-pass model/action ranking unstable.
8. When external knowledge is used, resolve sources without hard-coding machine-local absolute paths.
9. Keep raw external knowledge in the external workspace source; cite source paths and extracted claims inside DebugTool outputs.
10. Always list Adopted / Deferred / Not Applied for full-tree modes.
11. Always put the optimal path before the full tree.
12. Every action node must use `output_contracts/node_table_schema.md`.
13. Every action node must include `action_type`, `tool_required`, `safety_level`, `cost`, `reversibility`, and `evidence_refs`.
14. S2/S3 nodes must include explicit safety warning or mitigation language.
15. Mermaid decision-tree node IDs must match Node Explanation Table IDs.
16. Every knowledge-linked claim must include fact source and confidence.
17. Solved cases must produce a case_record draft, regression candidate, and a Skill-Level Learning Proposal that says whether the case changes reusable rules or remains target-specific.
18. Before promoting or saving an output, run `scripts/output_validator.py` with the correct mode.
19. Full debug trees must rank early actions by probability, time cost, safety risk, and exclusion value.
20. Multi-link failures must load and apply the relevant domain link model from `assets/link_models/` before blind tuning or component replacement.
21. Domain-specific stage requirements belong in link-model assets, not in the top-level skill contract.
22. When the user asks whether an output, conclusion, or probability ranking is reliable, run Evidence Audit using `output_contracts/evidence_audit.md`; structural validation is not enough.
23. When saving or publishing a pilot/debug output, apply the artifact hygiene rules in `lifecycle/case_artifact_hygiene.md`.
24. When optimizing this skill, use `output_contracts/skill_improvement.md` and prefer contract/routing/regression changes over re-running the same unresolved debug case.
25. Match the user's language for prose output; contract headings and machine-checked field names may remain in the required language.
26. When ranking hypotheses, the simplest physical interpretation of the direct symptom must appear in the top two unless explicit contrary evidence demotes it.
27. Stale or non-same-interval facts must not lower or raise probabilities directly; list them as `requires_re_verification` and add a matching missing-information item until refreshed.
28. In unresolved Architecture-First outputs, include an `unknown / model gap` hypothesis and reserve at least 2% probability.
29. Treat people named in chat as candidate owners only unless the input explicitly assigns responsibility.
30. Use `reasoning/cost_priors.yaml` and `reasoning/probability_time_cost_model.md` for time-cost estimates; do not invent optimistic lab times for multi-instrument captures. Any local override must state the base prior class, overridden time, and reason.
31. Evidence Audit and Architecture-First outputs must make mechanically checkable semantic guardrails explicit: stale-evidence handling, direct-symptom top-two reasoning, model-gap branch, cost-prior source, and candidate-owner wording when applicable.
32. Major case-shape changes must appear in Input Cleaning `Contradictions / Revisions`, not only in narrative summary. Examples: symptom scope changes, architecture mapping changes, a former baseline channel fails, or an old repeated-test variable becomes invariant.
33. When a case involves repeated tests, Input Cleaning must separately list repeated variables, invariants, and unknown invariants before routing.
34. Architecture-First outputs must not mix `boundary`, `mechanism`, and `observability_gap` rows in one mutually exclusive probability table. Use boundary distribution, mechanism prior, coverage matrix, and evidence ledger when the case is unresolved; validators must reject legacy flat root-cause probability tables.
35. Observability gaps such as missing fault-state readback are diagnostic gaps, not physical root causes; their actions improve measurement quality rather than changing hardware.
36. If an Architecture-First hypothesis bundles multiple physical mechanisms because data is insufficient, add the evidence trigger that will split it into separate branches.
37. `Cost / Probability Ranking` must expose priority tiers (`P0/P1/P2`) and explicit co-acquisition grouping through `co_acq_group_id`, `same_failure_window`, and `capture_channel`, because execution owners scan tiers faster than scores and same-window actions must be auditable.
38. Input Cleaning facts must carry `provenance`; `team_attestation_unverified` facts are capped at `medium` confidence until backed by a raw artifact, instrument log, waveform, register dump, or same-window measurement.
39. Architecture-First evidence ledgers must be mechanically linked: each evidence row states `criticality`, `gates_boundaries`, and `gates_mechanisms`; missing critical evidence caps gated boundary/mechanism probabilities at `0.50` unless a local override explains the cap, new value, and reason.
40. Before creating a new pilot/debug artifact, answering where to record a case update, or processing a short follow-up with case-like tokens, check `pilot_runs/CASE_INDEX.md` when present. A strong or probable index match must update the existing case current entry point instead of creating or suggesting a new standalone record.
41. If a user says a follow-up should have matched an earlier case, treat it as a routing/artifact-lifecycle defect. Add or correct the case-index aliases and update lifecycle/routing rules before committing the fix.

## Mode Selection Order

```text
0. Input Cleaning
1. Safety Gate
2. Signature-Based Fast Path
3. Architecture-First
4. Knowledge-Linked
5. Assumption-Driven
6. Heuristic Context
7. Retrospective after solution
```

Use `prompts/context_router.md` for general natural-language requests. Use `prompts/architecture_first.md` when the user provides a chain, module list, register state, waveform relationship, or updated debug conclusion.

Use `routing/natural_language_intent_map.md` to translate ordinary user wording into internal behavior without exposing mode names.

Use `prompts/skill_improvement.md` when the user asks to improve DebugTool itself or critiques how the skill behaved.

## Optional External Knowledge Escalation

DebugTool is portable and must not assume a fixed wiki location.

Default behavior: do not query external workspace knowledge. A normal first pass should rely on cleaned user input, built-in assets, explicit assumptions, and safe first measurements.

Escalate to external knowledge only when:

- the user explicitly asks to use a wiki, knowledge base, schematic, datasheet, repo, or prior record;
- the user explicitly asks to learn from the web, search online, broadly explore references, or build the model from external material;
- a high-impact knowledge gap would change the first two actions, safety envelope, link model boundary, or top hypothesis ranking;
- built-in model knowledge is insufficient to identify the relevant components, pins, protocols, or observable evidence;
- the cleaned input conflicts with existing naming or architecture and the conflict blocks a stable plan.

When the user explicitly requests knowledge exploration, support two expanded behaviors:

- Interactive exploration: produce a Knowledge Request, source plan, extracted claims, and updated model in stages; pause at meaningful checkpoints when the next retrieval scope or model direction is ambiguous.
- Broad exploration: search workspace knowledge, existing source-registry seeds, and/or online sources to learn enough domain/project context to build the model; prefer project-specific sources, reviewed closed-loop records, vendor documentation, standards, official app notes, and user-provided material over generic articles.
- Similar problem expansion: find cases with matching interface family, failure signature, link-model stage, or evidence/action shape; extract transferable tactics and architecture stages, not copied conclusions.

Online or wiki-derived material is documented evidence, not target-system fact. It may update the link model and priors, but board-level measurements, logs, or direct user confirmations remain stronger.

Resolve external knowledge in this order:

1. user-provided path
2. user-provided URL or explicit online search instruction
3. `DEBUGTOOL_KB_ROOT`
4. local `knowledge_sources.yaml`
5. workspace sibling discovery
6. official/public web sources when online exploration is requested or needed
7. unavailable fallback

Use `retrieval/knowledge_sources.example.yaml` as a template. Keep private local paths out of committed files.

When escalation is triggered, extract claims rather than copying source material:

```text
claim: Redriver PWDN is low-enable
source_path: ../my-wiki/...
state: documented
needs_confirmation: board-level voltage measurement
```

## Asset Types

```text
link_model       causal / architecture / dependency model
signature        strong symptom -> fast-path action cluster
case_record      solved retrospective / validated experience
pattern_bundle   article/forum/app-note pitfall or debug-pattern bundle
debug_principle  generalized cross-domain debug rule
```

## Output Expectations

Full debug outputs must distinguish:

- symptom: what failed
- root cause: only after evidence proves it
- measurement: what was observed and where
- hypothesis: plausible explanation with probability and falsifier
- action: next measurement/change with expected evidence

For unclear user input, produce a provisional result instead of blocking:

- cleaned understanding
- assumptions
- top possible causes with probabilities
- first safe measurements
- action decision tree
- missing information that would change the plan

## Validator Commands

```bash
python scripts/output_validator.py --mode input_cleaning --file cleaned.md
python scripts/output_validator.py --mode standard --file output.md
python scripts/output_validator.py --mode knowledge_linked --file output.md
python scripts/output_validator.py --mode architecture_first --file output.md
python scripts/output_validator.py --mode fast_path --file output.md
python scripts/output_validator.py --mode assumption_driven --file output.md
python scripts/output_validator.py --mode retrospective --file retrospective.md
python scripts/output_validator.py --mode evidence_audit --file audit.md
python scripts/output_validator.py --mode skill_improvement --file review.md
```

Structural validation means the output matches the contract. It does not prove the reasoning is correct.
