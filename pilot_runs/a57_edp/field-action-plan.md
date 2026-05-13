# A57 eDP Field Action Plan

This is the field execution layer for the A57 eDP pilot. It uses the generic templates in `forms/failure_matrix_template.md` and `forms/same_window_evidence_batch_checklist.md`.

Do not promote A57-specific names into global scripts, validators, output contracts, or reusable templates. Treat the table below as case configuration.

## Artifact Navigation

- Start with `visual-architecture-brief.md` before assigning lab work.
- Use `latest-architecture-first.md` when a field result changes the boundary or mechanism ranking.
- Use `latest-input-cleaning.md` when new user/chat facts need provenance and staleness classification.
- Return to `README.md` after adding, archiving, or renaming any generated artifact.

## 0. Executive Architecture Gate

Current top-level conclusion: if the visible failure is `CR/EQ fail + training pattern looping + no image`, the primary debug system is the A57 Source training-control plane, not the main data path.

Why: CR/EQ status is synthesized by the FPGA/DPCD responder over AUX. It is not direct SerDes feedback. Therefore the first question is whether A57 Source read and accepted a complete DPCD training-pass state.

Use `visual-architecture-brief.md` as the first-page architecture map before assigning lab work.

| mode | visible symptom | first subsystem | P0 evidence batch | stop condition |
|---|---|---|---|---|
| Mode A | CR/EQ fail, training pattern loops, no image | AUX/DPCD/HPD/responder training-control plane | `CO-A57-AUX-CR-EQ-FAILWIN-1` | Do not prioritize AU15P/SerDes/Redriver until Source accepts CR/EQ pass. |
| Mode B | CR/EQ pass, still no image | DS90UB984 -> Redriver -> AU15P main data path | `CO-A57-EDP-FAILWIN-1` | Do not use Mode B evidence to explain CR/EQ fail unless Mode A is closed. |

## 1. Case Configuration

| generic_field | A57 alias | allowed values / source | notes |
|---|---|---|---|
| sample_id | decoder_board_id | board under test, four measured boards plus any added boards | Required for board-to-board distribution. |
| subsystem_id | decoder_chip_id | DS90UB984-A, DS90UB984-B | A maps to eDP1/eDP2; B maps to eDP3/eDP4 for this case only. |
| channel_id | edp_channel_id | eDP1, eDP2, eDP3, eDP4 | Add rows for actual tested channels; do not create fixed per-channel columns. |
| operation_id | operation_sequence_id | full test, single-selection test, decoder power cycle, decoder reconfig loop | Must describe what changed during reproduction. |
| config_id | config_profile_id | DS90UB984 script/ini id, Redriver static config id, FPGA build/status profile | `unknown` is allowed but must be explicit. |
| test_window_id | run_id_or_timestamp | lab run id, timestamp, or failure window id | Required before comparing pass and fail observations. |
| failure_signature_id | display_failure_signature | CR/EQ fail, training pattern loop, no image after CR/EQ pass, intermittent image, single-selection no image, other observed mode | Keep symptom labels separate from root-cause labels. |
| evidence_batch_id | same_window_batch_id | CO-A57-AUX-CR-EQ-FAILWIN-1, CO-A57-EDP-FAILWIN-1, etc. | Links matrix rows to same-window evidence. |

## 2. Current Working Hypothesis

Current highest-value question: which mode are we in?

If current symptom is Mode A, priority boundary order is:

| priority | boundary | current reason | evidence needed |
|---:|---|---|---|
| 1 | A57 driver fail reason | `CR/EQ fail` is currently too coarse to route. | Exact fail type: AUX timeout/NACK/DEFER, status bit fail, lane-align fail, HPD event, or generic timeout. |
| 2 | AUX transaction | Source may not read the synthetic pass state. | Pass/fail DPCD transaction diff with ACK/NACK/DEFER/timeout/retry/timestamp. |
| 3 | DPCD status-map | FPGA responder may return incomplete or semantically wrong training status. | CR_DONE, CHANNEL_EQ_DONE, SYMBOL_LOCKED, LANE_ALIGN_DONE, ADJUST_REQUEST, lane/rate mapping. |
| 4 | AUX/HPD physical layer | Temperature and mechanical sensitivity can affect AUX/HPD, not only SerDes. | AUX+/AUX-/HPD waveform, level, glitch, reset window, environmental tag. |
| 5 | FPGA responder timing | Probability can come from stale status or CDC/race. | Responder log with Source write/read, return value, status update time, HPD event. |

If current symptom is Mode B, priority boundary order remains:

| priority | boundary | current reason | evidence needed |
|---:|---|---|---|
| 1 | DS90UB984 internal state / per-channel state | Decoder power cycle and reconfiguration are the active repeat variables. | Fault-state raw readback, lock/status, output enable, stream state. |
| 2 | DS90UB984 output boundary | eDP1-4 can fail and same-chip channels are not strictly paired. | Per-channel output-valid, test-pattern/output activity, or safe proxy. |
| 3 | Board/channel/path/SI distribution | Four boards show different channel tendencies. | Standard matrix plus Redriver/AU15P boundary evidence. |
| 4 | Redriver static path | Redriver is not dynamically reconfigured during repeated tests, but static PWDN/I2C/EQ/path is not closed. | PWDN/I2C/EQ/static state and per-channel input/output activity. |
| 5 | AU15P receiver | Old CDR/comma evidence is stale until tied to the new eDP1-4 matrix. | AU15P input activity plus CDR/comma/lane status in the same failure window. |

## 3. Failure Matrix Working Table

Copy rows as needed. One row should represent one sample/subsystem/channel/config/operation slice.

| matrix_id | decoder_board_id | decoder_chip_id | edp_channel_id | operation_sequence_id | config_profile_id | run_id_or_timestamp | test_count | pass_count | fail_count | failure_rate | display_failure_signature | same_window_batch_id | confidence | notes |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|
| A57-MX-001 |  |  |  |  |  |  |  |  |  |  |  |  | low/medium/high |  |

Minimum before probability updates:

- `decoder_board_id`
- `decoder_chip_id`
- `edp_channel_id`
- `operation_sequence_id`
- `config_profile_id` or explicit `unknown`
- `test_count`
- `fail_count`
- `display_failure_signature`
- `run_id_or_timestamp`

## 4. Mode A P0 Training-Control Evidence Batch

Run this first when the failure is CR/EQ fail. All entries must share `CO-A57-AUX-CR-EQ-FAILWIN-1` and the same `run_id_or_timestamp`.

| evidence_id | boundary | capture | pass marker | fail marker | owner candidate | status |
|---|---|---|---|---|---|---|
| A57-TP0-01 | A57 driver fail reason | Verbose driver log with exact CR/EQ failure subtype. | Training completes or fail reason is classified. | Only generic "CR/EQ fail" with no subtype. | A57 software/driver owner | pending |
| A57-TP0-02 | AUX transaction | Pass/fail DPCD transaction diff, including addresses, data, ACK/NACK/DEFER, timeout, retry, timestamp. | Fail window reads the same complete pass state as pass window. | NACK/DEFER/timeout/retry spike, missing read, or byte-level status mismatch. | Wu Zhian / FPGA debug owner | pending |
| A57-TP0-03 | DPCD status-map | Audit responder returns for CR_DONE, CHANNEL_EQ_DONE, SYMBOL_LOCKED, LANE_ALIGN_DONE, ADJUST_REQUEST, lane/rate mapping. | Status bits match Source expectation for lane count, rate, and training stage. | Missing per-lane bit, wrong lane-align, wrong adjust request, wrong readback. | FPGA debug owner | pending |
| A57-TP0-04 | AUX/HPD physical | AUX+/AUX-/HPD waveform with temperature, airflow, mechanical condition, reset window. | Clean waveform and stable HPD across pass/fail. | Level/common-mode/glitch/HPD bounce correlates with fail. | Wu Feng / hardware owner | pending |
| A57-TP0-05 | FPGA responder timing | Source write/read log, return value, status update timestamp, HPD event. | Status stable before Source read, no stale/zero/race condition. | Read occurs before update, stale value returned, CDC/race suspected. | FPGA debug owner | pending |

## 5. Mode B P0 Main-Data-Path Evidence Batch

Run this only when CR/EQ is stable pass but no image remains. All entries must share `CO-A57-EDP-FAILWIN-1` and the same `run_id_or_timestamp`.

| evidence_id | boundary | capture | pass marker | fail marker | owner candidate | status |
|---|---|---|---|---|---|---|
| A57-EV-P0-01 | DS90UB984 raw status | Per-chip and per-channel register dump before any recovery action. | Status matches expected stream/output state. | Lock, stream, output enable, error, or retention state differs on failed channel. | Chen Bin | pending |
| A57-EV-P0-02 | DS90UB984 power/reset/refclk/PLL | Aligned waveform or status for rails, reset, refclk, PLL, SerDes reference. | Pass and fail windows meet timing and stability requirements. | Rail, reset, refclk, PLL, or reference timing differs or is marginal. | Wu Feng | pending |
| A57-EV-P0-03 | Redriver static config | PWDN, I2C/readback, EQ, path, and static enable state. | Static state is correct and unchanged through the decoder reinit loop. | PWDN/config/path differs, changes unexpectedly, or is unreadable. | Wu Feng | pending |
| A57-EV-P0-04 | Redriver input/output boundary | Per-channel input/output activity or safe proxy. | Input and output are valid on the failed channel. | Input valid but output invalid, or output valid but downstream invalid. | Wu Feng / FPGA debug owner | pending |
| A57-EV-P0-05 | AU15P input and receiver status | Per-channel input activity, CDR, comma, lane status, and counters. | Input activity and receiver status are valid. | Input missing, or input valid while CDR/comma/lane status fails. | FPGA debug owner | pending |

PM/project lead confirmation is required before treating owner candidates as formal assignments.

## 6. Decision Update Rules

- If current symptom is CR/EQ fail, do not demote the AUX/DPCD/HPD/responder branch until A57 driver fail reason and AUX transaction diff are present.
- If A57 Source fails because of AUX timeout/NACK/DEFER/HPD event, keep the branch on AUX/HPD physical layer or AUX front-end.
- If AUX transaction is clean but status bits are not accepted, keep the branch on DPCD status-map, training semantics, or responder timing.
- If A57 Source reads and accepts complete pass status and CR/EQ becomes stable pass, switch to Mode B.
- If DS90UB984 status or output is invalid in the same failure window, keep the branch on DS90UB984 timing, reconfig, retention, stream state, or output enable.
- If DS90UB984 output is valid but Redriver output is invalid, move to Redriver static path, PWDN, EQ, mux, or path.
- If Redriver output is valid but AU15P input is invalid, move to lane path, connector, AC coupling, SI, assembly, or mapping.
- If AU15P input is valid but CDR/comma fails, then and only then prioritize AU15P receiver refclk, rate, polarity, comma, or SerDes configuration.
- If evidence is not from the same failure window, mark it `stale` and do not use it to lower a current branch.

## 7. Stop Conditions

- Stop treating "CR/EQ fail" as a root-cause label; it must be split by driver fail reason.
- Stop saying FPGA has delivered training OK until the AUX transaction proves Source read and accepted the complete pass state.
- Stop AU15P/SerDes/Redriver-first work while CR/EQ still fails.
- Stop using front-channel versus rear-channel language until the matrix is complete enough to support it.
- Stop saying Redriver is excluded until static config and input/output are captured in the failure window.
- Stop AU15P tuning-first work until AU15P input is proven valid in the same failure window.
- Stop using old AUX/CDR/comma observations as current evidence until they are reverified against the new board/channel matrix.
