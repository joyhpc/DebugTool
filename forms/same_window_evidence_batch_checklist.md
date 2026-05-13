# Same-Window Evidence Batch Checklist

Use this checklist when several observations must be tied to one fault occurrence before they can update a boundary or mechanism hypothesis.

Keep this checklist generic. Map project-specific blocks, chips, rails, links, and status names in the Boundary Vocabulary table.

## 1. Batch Metadata

- evidence_batch_id:
- linked_case_or_pilot_id:
- linked_matrix_ids:
- failure_window_id:
- capture_start_time:
- capture_end_time:
- trigger_condition:
- pass_or_fail_state:
- operator:
- safety_level:
- stop_conditions:

## 2. Boundary Vocabulary

| boundary_id | generic_boundary | case_alias | valid_upstream_marker | invalid_downstream_marker | preferred_tool_or_source |
|---|---|---|---|---|---|
| BD0 | sample / fixture / environment |  |  |  | log / visual / DMM |
| BD1 | control intent / command delivery |  |  |  | register log / bus trace |
| BD2 | power / reset / clock prerequisite |  |  |  | scope / DMM / status |
| BD3 | active device internal state |  |  |  | raw register dump / status log |
| BD4 | active device output boundary |  |  |  | scope / status proxy / test pattern |
| BD5 | intermediate path / conditioner / mux |  |  |  | scope / status / configuration readback |
| BD6 | receiver input boundary |  |  |  | scope / status proxy / receiver counters |
| BD7 | receiver lock / decode boundary |  |  |  | receiver status / counters |
| BD8 | downstream functional output |  |  |  | frame counter / application log / user-visible output |
| BD9 | unknown / model gap |  |  |  | evidence review |

## 3. Pre-Capture Gates

| gate_id | gate | pass_fail_unknown | notes |
|---|---|---|---|
| G1 | Reproduction trigger is defined and repeatable enough for capture. |  |  |
| G2 | Each capture source can be timestamped or tied to the same run id. |  |  |
| G3 | Safety limits and stop conditions are active before reproduction. |  |  |
| G4 | Good-state and fail-state labels are unambiguous. |  |  |
| G5 | Raw evidence can be preserved before interpretation. |  |  |

## 4. Evidence Capture Table

| evidence_id | boundary_id | same_failure_window | timestamp_or_run_id | capture_method | raw_artifact_path_or_ref | expected_pass_marker | observed_value | status | interpretation | next_branch |
|---|---|---|---|---|---|---|---|---|---|---|
| EV-001 |  | true/false/unknown |  |  |  |  |  | present/missing/stale/blocked |  |  |

## 5. First-Fail Boundary Rule

The first-fail boundary is the earliest boundary where:

1. Upstream evidence from the same failure window is valid or not yet contradicted.
2. This boundary has a missing, invalid, unstable, or contradictory marker.
3. Downstream symptoms can be explained by this boundary.
4. The evidence is `present`, not `stale`.

If two non-adjacent boundaries look invalid but intermediate evidence is missing, keep `BD9 unknown / model gap` active and collect the missing intermediate boundary first.

## 6. Evidence Status Rules

- `present`: captured in the current failure or pass window and linked to the batch id.
- `missing`: expected evidence was not captured.
- `stale`: evidence exists but belongs to an older window, older configuration, or different sample/channel context.
- `blocked`: capture is unsafe, unavailable, or requires an external owner/tool.

Do not use `stale` evidence to lower a current branch unless the batch explicitly proves the old condition still applies.

## 7. Output Update

After the batch, update:

- first-fail boundary
- mechanisms raised or lowered
- evidence gaps that remain
- next 1-3 actions
- branches that must stop until a missing boundary is captured
