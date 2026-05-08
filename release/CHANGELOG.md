# Changelog

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
