# High-Value Source Registry

Use this only after external knowledge escalation is triggered. This is not a large bookmark dump. It is a runtime source-selection layer that reuses existing curated queues and expands to similar solved problems when useful.

## Existing Registry Seeds

| seed | path | use_as | trust_level |
|---|---|---|---|
| authoritative official-source queue | `training/closed_loop/authoritative_training_queue.yaml` | vendor app notes, official design guides, datasheets, checklists, training articles | high for general priors, not target-system fact |
| focused MIPI/video queue | `training/dataset_1000/mipi_debug_queue.yaml` | MIPI DSI/CSI bridge, PHY, packet counter, lane, host-binding, video debug analogs | medium-high when domain matches |
| focused Intel/Altera FPGA queue | `training/dataset_1000/intel_altera_fpga_queue.yaml` | FPGA config, JTAG, debug-node, PLL, EMIF, transceiver integration analogs | medium-high when domain matches |
| public solved-case queue | `training/dataset_1000/public_solved_case_queue.yaml` | symptom/investigation/resolution analogs | medium if resolution is visible, low if only forum hints |
| closed-loop records | `training/closed_loop/records/` | reviewed blind-prediction outcomes and promoted lessons | highest internal calibration among public/official-derived records |
| candidate sources | `training/closed_loop/candidate_sources.yaml` | discovery backlog for related symptoms | low until reviewed |
| workspace knowledge | configured wiki/docs paths from `retrieval/knowledge_source_resolution.md` | project-specific schematics, logs, notes, prior cases | high if same board/revision and directly observed |

## When To Use

Use the registry when:

- the user asks for online learning, broad exploration, my-wiki learning, similar cases, or deeper architecture understanding;
- the first-pass model has a high-impact knowledge gap;
- a case has weak project-specific evidence and needs stronger priors for what to measure next;
- an issue looks like a known symptom pattern but the exact root cause is not proven.

Do not use the registry in the normal first-pass flow.

## Similar Problem Expansion

Similar cases are used to widen the model and suggest transferable tactics. They must not be copied as conclusions.

Match in this order:

1. Same project, board, revision, chip, register block, or net name.
2. Same interface family or protocol layer, such as eDP/DisplayPort, MIPI DSI/CSI, SerDes, JTAG, I2C, SPI, PCIe, USB.
3. Same failure signature, such as "control path works but main data path is invalid", "CDR lock fails", "no packet count", "all 0xFF", "SDA stuck low", or "cable enumerates but target missing".
4. Same link-model stage, such as control, power/reset/clock, PHY, redriver/mux/path, receiver, packet/video pipeline, host driver, or downstream consumer.
5. Same evidence/action shape, such as test pattern split, register counter readback, board-to-board comparison, lane swap, reset ineffective, or source-output proof.

Penalize or reject:

- wrong board revision, wrong part, wrong direction, or wrong topology;
- case has no visible investigation path or resolution;
- only a generic article exists when an official or project-specific source is available;
- case conflicts with direct target measurements.

## Runtime Procedure

1. Start from the cleaned case entities and the preliminary link model.
2. Search existing registry seeds before broad web search.
3. Build a Similar Problem Candidate Table.
4. Extract only transferable claims: observed pattern, useful measurement, isolation tactic, or architecture stage.
5. Mark applicability limits and non-transferable parts.
6. Update the current link model only where the similar case changes nodes, observables, or action ordering.
7. Keep direct target evidence above similar-case priors.

## Similar Problem Candidate Table

| case_id | source | match_axis | transferable_lesson | applies_to_current_case | limits | action_impact |
|---|---|---|---|---|---|---|
| MIPI-002 | `training/dataset_1000/mipi_debug_queue.yaml` | no-output video bridge debug | use test pattern, timing, lane count, clock, error registers to split source/bridge/panel | possible analog for eDP decoder/receiver no-image | MIPI DSI/LVDS bridge, not eDP/DP; requires topology check | add split test / register counter branch |

## Source Strength

| source_type | strength | use |
|---|---|---|
| same-board measured record | strongest | can update facts if measurement conditions match |
| same-board schematic/datasheet/register guide | strong | can update link model and required observables |
| reviewed closed-loop record | strong prior | can update action ordering and known traps |
| official vendor/standards source | strong prior | can update protocol/device model |
| vendor forum with FAE resolution | medium prior | can suggest tactics, not conclusions |
| public forum/community answer | weak-medium prior | use only with clear symptom/resolution and mark limits |
| generic blog/article | weak | use only when no better source exists |

## eDP / Video Example Expansion Axes

For an eDP no-image or CDR-lock case, search similar cases by:

- control succeeds but data invalid: AUX/I2C ok, receiver lock fails, packet/video counters absent;
- bridge or decoder output proof: test pattern, output activity, error/status registers;
- power/reset/clock readiness: refclk, PWDN, reset release, PLL/lock bits;
- lane/path issues: polarity, lane mapping, AC coupling, redriver enable/EQ, connector/board variance;
- receiver-side observability: CDR lock, comma alignment, PCS lock, packet counters, video-valid status.
