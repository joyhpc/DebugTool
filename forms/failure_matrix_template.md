# Failure Matrix Template

Use this template when a debug case depends on distribution across samples, units, channels, lanes, ports, rails, configurations, or operation sequences.

Keep this template generic. Put project-specific names in the Case Vocabulary table, not in the schema. Add rows for observed entities instead of adding fixed columns for a fixed channel count.

## 1. Case Vocabulary

| generic_field | case_alias | allowed_values_or_source | notes |
|---|---|---|---|
| sample_id |  |  | Physical board, module, fixture, cable, or tested unit. |
| subsystem_id |  |  | Chip, endpoint, rail group, connector, port group, or logical block. |
| channel_id |  |  | Lane, output, input, rail, port, sensor, or interface instance. |
| operation_id |  |  | User action, script, switching mode, reinit loop, power cycle, or command sequence. |
| config_id |  |  | Firmware build, register script, ini file, bitstream, tuning profile, or hardware strap set. |
| test_window_id |  |  | Timestamp, run number, batch id, or reproduction window. |
| failure_signature_id |  |  | Short label for the observed failure mode. |
| evidence_batch_id |  |  | Same-window evidence batch that can explain or bound this row. |

## 2. Axis Definition

| axis_id | generic_field | why_this_axis_matters | fixed_values | open_values_source |
|---|---|---|---|---|
| AX1 | sample_id |  |  |  |
| AX2 | subsystem_id |  |  |  |
| AX3 | channel_id |  |  |  |
| AX4 | operation_id |  |  |  |
| AX5 | config_id |  |  |  |

## 3. Failure Matrix

| matrix_id | sample_id | subsystem_id | channel_id | operation_id | config_id | test_window_id | test_count | pass_count | fail_count | failure_rate | failure_signature_id | evidence_batch_id | confidence | notes |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|
| MX-001 |  |  |  |  |  |  |  |  |  |  |  |  | low/medium/high |  |

## 4. Operation / Config Ledger

| id | type | description | changed_between_runs | controlled_or_observed | evidence_source |
|---|---|---|---|---|---|
| OP-001 | operation |  | yes/no/unknown | controlled/observed/inferred |  |
| CFG-001 | config |  | yes/no/unknown | controlled/observed/inferred |  |

## 5. Failure Signature Ledger

| failure_signature_id | symptom | pass_marker | fail_marker | how_detected | can_be_stale |
|---|---|---|---|---|---|
| FS-001 |  |  |  | user observation/log/register/scope/status | yes/no |

## 6. Interpretation Rules

- A matrix row is evidence about distribution, not proof of root cause by itself.
- Treat `test_count`, `pass_count`, and `fail_count` as missing if the values are estimated from memory rather than logged.
- A repeated channel-specific failure across samples raises channel/path/lane/config hypotheses.
- A repeated sample-specific failure across channels raises board/sample/assembly/prerequisite hypotheses.
- A failure-rate change tied to `operation_id` raises sequence, reinit, timing, or ownership hypotheses.
- A failure-rate change tied to `config_id` raises configuration, retention, and readback hypotheses, but only if the config was read back or otherwise verified.
- Do not demote a branch using old evidence unless `test_window_id` and `evidence_batch_id` show it belongs to the same failure window.

## 7. Minimum Completeness Gate

Before using the matrix to update hypothesis priority, fill at least:

- `sample_id`
- `channel_id` or the relevant per-instance axis
- `operation_id`
- `config_id` or an explicit `unknown`
- `test_count`
- `fail_count`
- `failure_signature_id`
- `test_window_id` or `evidence_batch_id`
