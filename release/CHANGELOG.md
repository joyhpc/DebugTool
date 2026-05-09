# Changelog

## V0.99.12 System Hardening

- Upgraded Architecture-First enforcement from prose contract to validator-backed checks: legacy flat normalized root-cause tables now fail validation, mechanism priors must not look forced to sum to 1.00, and coverage matrices must include rows for each physical mechanism.
- Replaced boolean co-acquisition with auditable `co_acq_group_id`, `same_failure_window`, and `capture_channel` fields in cost ranking tables; P0 rows without valid grouping now fail smoke validation.
- Made evidence ledgers mechanically joinable through `criticality`, `gates_boundaries`, and `gates_mechanisms`; missing critical evidence now caps gated boundary/mechanism probability at 0.50 unless a local override is stated.
- Added fact `provenance` to Input Cleaning and capped `team_attestation_unverified` facts at medium confidence until backed by raw artifacts, logs, waveforms, register dumps, or same-window measurement.
- Added negative smoke fixtures for flat root-cause tables, missing P0 co-acquisition groups, uncapped probabilities under missing evidence, and high-confidence unverified team attestation.

## V0.99.11 Boundary / Mechanism Separation

- Codified A57 Issue4 lessons into mandatory input-cleaning rules: major case-shape changes must appear in `Contradictions / Revisions`, repeated tests must split variables from invariants, and stale evidence must get a matching same-window re-verification gap.
- Reworked Architecture-First requirements to separate boundary distribution, mechanism priors, coverage matrix, and evidence ledger, preventing boundary observations and causal mechanisms from competing in one flat root-cause table.
- Tightened Architecture-First validator checks: `unknown / model gap` now reserves at least 2% probability, boundary probabilities must sum to 1.00, mechanism rows must declare `type=mechanism` or `type=observability_gap`, and cost ranking tables must expose `P0/P1/P2`, `co_acquisition`, `boundary_subset`, and `mechanism_subset`.
- Added local time-cost override policy to `reasoning/cost_priors.yaml` and `reasoning/probability_time_cost_model.md`.
- Made retrospective outputs include a Skill-Level Learning Proposal so solved cases explicitly decide whether to update reusable DebugTool rules.
- Reworked the A57 Issue4 latest output from a flat H table into boundary/mechanism/evidence/action-batch structure, with P0 same-window co-acquisition for DS90UB984 status, timing, Redriver state, and AU15P input/CDR/comma.

## V0.99.10 Semantic Validator Gate

- Hardened `scripts/output_validator.py` with mechanically checkable semantic gates for Architecture-First, Evidence Audit, Skill Improvement, and Input Cleaning staleness.
- Architecture-First validation now requires explicit direct-symptom top-two reasoning, an `unknown / model gap` hypothesis, `cost_priors.yaml` or local override citation, and a `p_hit` / `p_exclude` / `time_min` cost table.
- Evidence Audit validation now requires a parseable reviewer decision block and explicit coverage of fact-vs-inference, stale evidence, direct symptom ranking, model gap, cost priors, and candidate-owner assignment risk.
- Added a negative Evidence Audit smoke fixture so a heading-complete but semantically empty audit fails validation.

## V0.99.9 Semantic Prior Calibration

- Added mandatory rules for direct-symptom simplest-interpretation priority, stale-evidence quarantine, unknown/model-gap probability, candidate-owner wording, and cost-prior usage.
- Added `reasoning/cost_priors.yaml` with offline time estimates for lab captures, readback dumps, high-speed probing, multi-board matrices, firmware tracing, rework, and destructive reproduction.
- Updated Architecture-First and Evidence Audit contracts to check semantic probability ordering, stale evidence, model-gap hypotheses, cumulative path cost, point knowledge checks, and inferred owner risk.
- Added `staleness` to the Input Cleaning fact table contract and validator smoke fixture.

## V0.99.8 User-Language Output Contract

- Added an explicit output-language policy: user-facing prose follows the user's language, while fixed contract headings, schema fields, commands, paths, signals, and part numbers may stay in their required or original form.
- Added a regression fixture to keep Chinese user requests from producing English-heavy debug prose.
- Updated version metadata to align `SKILL.md`, `README.md`, and `release/VERSION.md`.

## V0.99.7 Skill Improvement Gate

- Added an explicit Skill Improvement request path so critiques of DebugTool behavior optimize the skill instead of continuing an unresolved hardware debug case.
- Added a `skill_improvement` output contract and prompt for routing, contract, validator, artifact lifecycle, and regression changes.
- Added case artifact hygiene rules for one current entry point per case/mode and archived superseded outputs.
- Promoted Evidence Audit from an ad hoc response into the expected publish-review gate for saved pilot/debug outputs.
- Added regression fixtures for skill-optimization intent and stalled-case handling.
- Updated version metadata to align `SKILL.md`, `README.md`, and `release/VERSION.md`.

## V0.99.6 Natural-Language Runtime Contract Hardening

- Added natural-language evidence-update routing so users can say "有新线索", "刚测到", or "帮我更新排查策略" without internal contract terms.
- Added optional external knowledge escalation with targeted, interactive, broad, and similar-problem exploration modes.
- Added portable knowledge-source resolution, knowledge request, external claim extraction, and high-value source registry contracts.
- Defined existing training queues as runtime source-registry seeds for broad and similar-problem exploration.
- Added regression prompts for default no-retrieval behavior, explicit wiki escalation, similar-case transfer limits, web-learning source priority, and natural evidence updates.
- Added machine-readable `version` and `api_version` to `SKILL.md`.
- Added V1.0 promotion criteria, `pyproject.toml`, dependency upper bound, pre-commit config, and CI validation workflow.
- Added MIT `LICENSE` and package license metadata for an explicit open-source posture.
- Reworked mode routing so available KB/docs do not automatically select Knowledge-Linked mode.
- Added `scripts/regression_run.py` as a closed-loop corpus baseline reporter and first step toward LLM-backed semantic regression.
- Added `release/OUTPUT_VALIDATOR_REVIEW.md` with validator coverage and known gaps.
- Hardened `scripts/output_validator.py` with `--strict` and read/UTF-8 error handling.

## V0.99.5 MIPI DSI/CSI Training Branch

- Added `training/dataset_1000/mipi_debug_queue.yaml` with 20 MIPI DSI/CSI debug candidates.
- Added `training/dataset_1000/mipi_debug_closure_index.yaml`.
- Extended `scripts/lint_dataset_1000.py` to validate the MIPI specialized queue and closure index.
- Added 10 MIPI closed-loop records covering DSI bridge initialization, SN65DSI8x no-output video, Jetson CSI mode settings, NVIDIA DRIVE CSI capture errors, AMD/Xilinx CSI-2 RX and D-PHY debug, Intel/Altera MIPI CSI-2 IP, Infineon CX3 unused-lane hardware requirement, NXP i.MX8 DSI host binding, and D-PHY LP/HS state classification.
- Added `LM-MIPI-DSI-CSI-DPHY`.
- Added `SIG-MIPI-DSI-BRIDGE-NO-VIDEO-LP11-HSCLK` and `SIG-MIPI-CSI-NO-FRAME-PACKET-COUNTERS-FIRST`.
- Expanded regression structure from 34 to 40 tests.
- Updated README, SKILL, release notes, and validation report.

## V0.99.4 Intel/Altera FPGA Training Branch

- Added `training/dataset_1000/intel_altera_fpga_queue.yaml` with 20 Intel/Altera FPGA debug candidates.
- Added `training/dataset_1000/intel_altera_fpga_closure_index.yaml`.
- Extended `scripts/lint_dataset_1000.py` to validate specialized source queues and closure indices.
- Added 9 Intel/Altera FPGA closed-loop records covering Quartus scan-chain failure, configuration status pins, JTAG signal integrity, Download Cable II, USB-Blaster/JTAGServer, Nios debug nodes, Nios ELF failures, and Arria 10 IOPLL lock behavior.
- Added `LM-FPGA-JTAG-CONFIG`.
- Added `SIG-QUARTUS-CABLE-SEEN-SCAN-CHAIN-FAIL` and `SIG-NIOS-ELF-AFTER-SOF-HARDWARE-MAP`.
- Expanded regression structure from 29 to 34 tests.
- Updated README, SKILL, release notes, and validation report.

## V0.99.3 1000-Unit Training Program Seed

- Added `training/dataset_1000/` with quality-tier targets, status tracking, public solved-case queue, and closure index.
- Added `scripts/lint_dataset_1000.py`.
- Added 20 public solved-case candidates.
- Closed 5 public solved cases into cost-aware reviewed records.
- Expanded regression suite from 24 to 29 tests.
- Updated README, SKILL, release notes, and validation report.

## V0.99.2 Authoritative Queue Closure

- Closed the 100-unit authoritative training queue.
- Added `scripts/close_authoritative_queue.py` for reproducible queue closure.
- Generated 88 additional reviewed official-source closed-loop records.
- Added `training/closed_loop/queue_closure_index.yaml` and `AUTHORITY_CLOSURE_SUMMARY.md`.
- Strengthened closed-loop linting to verify every authoritative unit maps to at least one reviewed record.
- Updated schema, README, SKILL, release notes, and validation report for queue closure state.

## V0.99.1 Closed-Loop Training Batch and Real Case Intake

- Promoted existing near-hit lessons into assets:
  - added I2C stuck-low follows-device / ESD-latch-up signature
  - added SPI all-0xFF transaction-shape signature
  - deepened I2C and SPI link models with counterexamples
- Added 8 reviewed authoritative closed-loop records from TI SCPA069 and Microchip TB3331.
- Expanded regression structure from 17 to 23 tests.
- Added real project case intake form, schema, folders, and linter.

## V0.99 Cost-Aware Closed-Loop Training

- Added probability/time-cost debug ordering in `reasoning/probability_time_cost_model.md`.
- Added 100-unit authoritative training queue in `training/closed_loop/authoritative_training_queue.yaml`.
- Extended closed-loop schema and linter to validate cost-aware reviewed records.
- Added five official-source reviewed closed-loop records and upgraded the previous five records with cost fields.
- Added `DP-EXPECTED-VALUE-BEFORE-HABIT` to make expected information per unit time a reusable principle.
- Expanded regression structure to 17 tests, including cost-aware ordering, false-clock I2C stuck bus, push-pull contention, and oscillator startup margin.

## V0.97 Seed Intake Structure

- Added closed-loop training workflow under `training/closed_loop/`.
- Added 25 public candidate debug sources and 5 reviewed closed-loop records.
- Added `debug_principle` as an asset type and four seed principles for measurement, control authority, dynamic evidence, and current-loop reasoning.
- Added `pattern_bundle` as an asset type for article/forum/app-note style experience bundles.
- Moved the user-provided power-debug pitfall article into `PBU-POWER-DEBUG-10-PITFALLS-SEED`.
- Added `PBU-HCNR201-ISOLATED-VOLTAGE-SAMPLING-SEED` from a user-provided HCNR201 / LM358 isolated analog sampling debug article.
- Extended asset source types with `public_article`, `public_forum`, `vendor_app_note`, and `user_provided_article`.
- Added regression structure case `REG-POWER-RIPPLE-MEASUREMENT-FIRST` to keep ripple debug measurement-first.
- Added regression structure case `REG-HCNR201-LM358-HEADROOM-FIRST` to keep linear optocoupler debug focused on op amp headroom, LED current, and virtual-short validity.
- Added regression structure cases for I2C reset-overlap stuck SDA, SPI all-0xFF link-layer debug, and MCU package power-mode debug.

## V0.96.1 Founder-Pilot Run Readiness

- Aligned `README.md` and `SKILL.md` with V0.96 founder-pilot closure status.
- Added `requirements.txt` to document PyYAML for asset and regression-suite linting.
- Normalized `3-5 Actions` contract headings to ASCII across validator, contracts, examples, and smoke cases.
- Hardened unsafe phrase validation so dangerous advice must have local mitigation on the same line, not merely a safety word elsewhere in the output.
- Added output-validator smoke runner and two unsafe-phrase smoke cases.
- Expanded `forms/founder_pilot_result_form.md` into an execution-ready run record with safety envelope, mode decision, asset use, evidence pack, promotion gate, and regression draft sections.
- Added `pilot_runs/` templates for the two initial founder-pilot loops: LA1010 / KingstVIS -105 and high-side MOSFET hot-swap / SOA.

## V0.95 Output Validator Hardening

- Expanded `scripts/output_validator.py` from skeleton to structural validator.
- Added required heading checks for standard, knowledge_linked, fast_path, architecture_first, assumption_driven, and retrospective modes.
- Added required heading order validation.
- Added 12-column Node Explanation Table validation.
- Added row-level enum validation for node type, action_type, safety_level, cost, and reversibility.
- Added action-node checks for action_type, tool_required, safety_level, cost, and reversibility.
- Added S2/S3 safety-warning/mitigation language check.
- Added Mermaid decision-tree node ID consistency check against the node table.
- Added retrospective YAML case_record draft check.
- Updated README and SKILL status to V0.95 founder-pilot candidate.

## V0.9.2 Critical Fix

- Fixed critical link_model `use_when == title` bug.
- Added real trigger conditions for all 9 link models.
- Added basic cross-link references between link models.
- Added lint rules for:
  - link_model use_when cannot equal title
  - safety_level enum validation
  - link_model causal_order required
  - signature top_actions and min_match_count required
- Restored explicit asset priority as `reasoning/asset_priority.md`.
- Renamed regression runner to honest `regression_suite_linter.py`, preserving wrapper.
- Added first offline `output_validator.py` skeleton.
- Cleaned release reports; removed runtime noise.
- Aligned lifecycle state machine and promotion policy.
