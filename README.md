# Debug Decision Tree Skill - V0.99.6 Natural-Language Agent Contract

## Status

Founder-pilot candidate. Not team-wide pilot ready. Not V1.0.

V0.99.6 keeps the project as a skill package and hardens the natural-language debug flow. A user can provide a terse bug report, issue-sync note, waveform clue, or chat extract; the skill should clean the input, route the case, build a link model, rank hypotheses, and return an action decision tree without requiring the user to know internal mode names.

The package is intended for 1-2 real founder-pilot debug loops before any wider rollout.

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
5. Deliver through `output_contracts/default_debug_delivery.md` plus the selected mode contract.
6. Load relevant assets from `assets/` only after checking `reasoning/asset_priority.md`.
7. Include probabilities, hypothesis tree, action decision tree, and first measurements whenever root cause is unknown.
8. Run `scripts/output_validator.py` before reusing or promoting the output.

Structural validation passing means the output matches the contract. It does not prove the debug reasoning is correct.

## Recommended Founder-Pilot Flow

1. Clean and normalize the raw user case using `output_contracts/input_cleaning.md`.
2. Use `prompts/context_router.md` to choose mode from the cleaned brief.
3. Generate a debug output using the selected output contract.
4. Run `scripts/output_validator.py` on the generated markdown.
5. Execute only the actions inside the documented safety envelope.
6. Record results in `forms/founder_pilot_result_form.md`.
7. Run retrospective and propose a case_record/regression update only when evidence supports it.

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
