# Debug Decision Tree Skill - V0.99.8 User-Language Output Contract

## Status

Early-internal-pilot candidate. Not team-wide pilot ready. Not V1.0.

V0.99.8 keeps the project as a skill package and makes user-language output explicit. A user can provide a terse bug report, issue-sync note, waveform clue, chat extract, or critique of DebugTool behavior; the skill should either run the debug flow or, when the target is skill quality, treat the case as a fixture and improve routing, contracts, audit gates, lifecycle rules, or regression coverage. User-facing prose should follow the user's language, while fixed contract headings and machine-checked fields may remain in their required form.

The package is intended for 1-2 real early-internal-pilot debug loops before any wider rollout.

## Core Asset Types

```text
link_model       causal / architecture / dependency model
signature        strong symptom -> fast-path action cluster
case_record      retrospective / experience / validated case
pattern_bundle   article/forum/app-note style pitfall or debug-pattern bundle
debug_principle  generalized rule that applies across many hardware debug domains
```

## Recommended Skill Invocation

1. Accept the user's natural-language bug report as sufficient to start.
2. Clean the raw user input using `output_contracts/input_cleaning.md`.
3. Start with `prompts/context_router.md` using the cleaned router-ready brief.
4. Map the user's wording through `routing/natural_language_intent_map.md` and select the mode from `routing/mode_router.md`.
5. Build the first link model and hypothesis tree from the cleaned input and built-in assets.
6. Use external workspace knowledge only as an escalation path, not as the default path.
7. Deliver through `output_contracts/default_debug_delivery.md` plus the selected mode contract.
8. Load relevant assets from `assets/` only after checking `reasoning/asset_priority.md`.
9. Include probabilities, hypothesis tree, action decision tree, and first measurements whenever root cause is unknown.
10. Run `scripts/output_validator.py` before reusing or promoting the output, then run Evidence Audit before publishing saved pilot/debug artifacts.
11. Match the user's language for prose. For Chinese user input, write summaries, judgments, action items, and audit findings in Chinese while preserving validator-required headings and technical identifiers.

Structural validation passing means the output matches the contract. It does not prove the debug reasoning is correct.

## Optional External Knowledge Escalation

DebugTool should not own project knowledge. External workspace knowledge sources can hold schematics, datasheets, project notes, previous debug records, and raw documents.

Do not query external knowledge by default. First produce a stable debug deliverable from cleaned user input, built-in assets, and explicit assumptions. Escalate to external knowledge only when one of these triggers is present:

- The user explicitly asks to use a wiki, knowledge base, schematic, datasheet, repo, or prior debug record.
- The user explicitly asks to learn from the web, search online, broadly explore references, or build the model from external material.
- The link model has a high-impact gap that would change the first actions, safety envelope, or top hypothesis ranking.
- The model lacks enough domain/project knowledge to identify the relevant nodes or observable evidence.
- The first-pass debug output exposes a model conflict, such as uncertain chip mapping, board revision, signal ownership, or control polarity.

When escalation is triggered, resolve sources with `retrieval/knowledge_source_resolution.md`, issue `output_contracts/knowledge_request.md`, then extract compact documented claims with `output_contracts/wiki_claim_extraction.md`. Cite source paths or URLs, not large private source text.

Explicit knowledge exploration can be targeted, interactive, or broad:

| Mode | Trigger | Behavior |
|---|---|---|
| Targeted | "查一下 PWDN 极性" / "看 my-wiki 里这个板子的记录" | Query only the named gap/source, extract claims, update affected nodes |
| Interactive | "边查边确认" / "我们一起建模型" | Stage the work: request, source plan, claim extraction, model update, user checkpoint |
| Broad | "网上学习一下再建模" / "广泛探索这个接口" | Search workspace and/or online sources, prefer official/project-specific material, synthesize a model with applicability limits |

Online or wiki-derived material is documented evidence, not target-system fact. It can update model structure and priors, but direct measurements, logs, and user confirmations remain stronger.

Existing training queues are the first source-registry seeds for broad exploration:

- `training/closed_loop/authoritative_training_queue.yaml`
- `training/dataset_1000/mipi_debug_queue.yaml`
- `training/dataset_1000/intel_altera_fpga_queue.yaml`
- `training/dataset_1000/public_solved_case_queue.yaml`
- `training/closed_loop/candidate_sources.yaml`

Use `retrieval/high_value_source_registry.md` to select these sources and expand to similar problems before doing unbounded web search. Similar cases provide transferable tactics and architecture insight; they do not prove the current root cause.

Knowledge source resolution order:

1. User-provided path in the request.
2. User-provided URL or explicit online search instruction.
3. `DEBUGTOOL_KB_ROOT`.
4. Local `knowledge_sources.yaml`.
5. Workspace sibling discovery, such as `../my-wiki`, `../knowledge`, `../HW-knowledge-base`, `../wiki`, or `../docs`.
6. Official/public web sources when online exploration is requested or needed.
7. Unavailable fallback with explicit missing-knowledge impact.

Committed examples should use relative paths and should not hard-code machine-local absolute paths.

Use `retrieval/knowledge_sources.example.yaml` as a local configuration template. Do not commit private, machine-specific `knowledge_sources.yaml` files.

## Recommended Founder-Pilot Flow

1. Clean and normalize the raw user case using `output_contracts/input_cleaning.md`.
2. Use `prompts/context_router.md` to choose mode from the cleaned brief.
3. Generate a debug output using the selected output contract.
4. Escalate to external knowledge only if the first-pass link model cannot support stable actions.
5. Run `scripts/output_validator.py` on the generated markdown.
6. Execute only the actions inside the documented safety envelope.
7. Record results in `forms/founder_pilot_result_form.md`.
8. Run retrospective and propose a case_record/regression update only when evidence supports it.

## V1.0 Promotion Criteria

Do not promote this package to V1.0 based on design completeness alone.

V1.0 requires:

- at least 5 real project cases processed through `training/real_project_cases/`;
- top-3 hypothesis hit or near-hit rate at or above 70% on those real cases;
- no unresolved P0 safety or contract bugs for 30 consecutive days;
- all validators, linters, smoke cases, and regression-suite structure checks passing in CI;
- manual review showing safety-gate true positives at or above 90% on pilot cases;
- median time from cleaned input to first actionable measurement at or below 3 minutes in pilot operation;
- documented changelog entry for any breaking contract or output-format change.

These thresholds are provisional and may be revised only by an explicit release note.

## Natural Evidence Updates

The user should not need internal vocabulary such as input cleaning, link model, hypothesis probability, or action decision tree.

These ordinary phrases are sufficient:

```text
有新线索：...
补充一下现场情况：...
刚测到：...
示波器看到：...
寄存器读到：...
这个线索说明什么？
帮我更新一下排查策略。
下一步怎么查？
```

The skill should treat them as an evidence update: preserve prior context, separate fact from judgment, mark stale assumptions, revise hypothesis priority, and give the next checks in plain language.

## Python Dependency

`scripts/output_validator.py` uses only the Python standard library. Asset and regression-suite linting require PyYAML:

```bash
python -m pip install -r requirements.txt
```

## Example Commands

```bash
python scripts/output_validator.py --mode input_cleaning --file cleaned.md
python scripts/output_validator.py --mode standard --file output.md
python scripts/output_validator.py --mode knowledge_linked --file output.md
python scripts/output_validator.py --mode architecture_first --file output.md
python scripts/output_validator.py --mode fast_path --file output.md
python scripts/output_validator.py --mode assumption_driven --file output.md
python scripts/output_validator.py --mode retrospective --file retrospective.md
```

Run asset and suite checks:

```bash
python scripts/lint_assets.py
python scripts/regression_suite_linter.py
```

Run output-validator smoke cases:

```bash
python scripts/run_output_validator_smoke.py
```

Run closed-loop training record checks:

```bash
python scripts/lint_closed_loop.py
```

Run real project case intake checks:

```bash
python scripts/lint_real_project_cases.py
```

Run 1000-unit training program checks:

```bash
python scripts/lint_dataset_1000.py
```

## Closed-Loop Training

Use `training/closed_loop/` for public or user-provided debug records. The workflow is: extract the initial symptom/background, generate a predicted debug tree before using the final resolution, reveal the actual fix, score coverage, and promote only repeated learning into assets.

`training/closed_loop/authoritative_training_queue.yaml` contains 100 official training units from vendor application notes, official checklists, design guides, and training articles. As of V0.99.2 all 100 queue units are mapped in `training/closed_loop/queue_closure_index.yaml`. These are official-source training closures, not validated real project cases.

## Cost-Aware Ordering

Use `reasoning/probability_time_cost_model.md` to rank candidate actions by expected diagnostic value per minute. Safety gates and prerequisite measurements still override raw probability.

## Real Project Cases

Use `forms/real_project_case_intake_form.md` and `training/real_project_cases/` for real project material. Real cases must be anonymized, blind-predicted, revealed, scored, and reflected before promotion into `case_record`, `signature`, `link_model`, or regression.

## 1000-Unit Program

Use `training/dataset_1000/` to expand beyond official-source priors. The target mix is 300 official priors, 300 public solved cases, 150 vendor/FAE resolved cases, 100 real project cases, 100 near-hit/miss counterexamples, and 50 safety-high-risk cases.

`training/dataset_1000/intel_altera_fpga_queue.yaml` starts a focused Intel/Altera FPGA branch for JTAG, Quartus Programmer, configuration status pins, Download Cable II, Nios debug nodes, PLL lock, EMIF, and Platform Designer bring-up.

`training/dataset_1000/mipi_debug_queue.yaml` starts a focused MIPI DSI/CSI branch for D-PHY LP/HS state, DSI bridge no-video, CSI no-frame, packet counters, lane configuration, host graph binding, and bridge/camera timing.

Official vendor documents are treated as authoritative priors; public forum records are not promoted as real cases unless later calibrated by project evidence.

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

## Current Next Best Step

Validate the natural-language flow on real debug prompts: terse symptom only, issue-sync note, architecture-rich case, and updated-evidence case. A pilot counts as progress only if the first two recommended actions improve or the stale branch is explicitly demoted after new evidence.
