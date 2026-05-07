# Node Table Schema

Every node table must include these columns:

| Column | Required | Values |
|---|---|---|
| id | yes | D1/A1/G1/T1 |
| type | yes | decision/action/gate/terminal |
| action_type | action only | observe/isolate/perturb/replace/reconfigure/reproduce/rollback |
| check_or_action | yes | short text |
| tool_required | action/gate | DMM/scope/LA/JTAG/log/tool/none |
| expected_observation | yes | pass condition |
| interpretation | yes | what pass/fail means |
| safety_level | yes | S0/S1/S2/S3 |
| cost | yes | low/medium/high |
| reversibility | action only | reversible/partial/irreversible |
| next_branch | yes | node id or terminal |
| evidence_refs | if facts exist | [F1,F2] |
| p_hit | recommended | 0.0-1.0 probability action directly identifies/fixes dominant fault |
| p_exclude | recommended | 0.0-1.0 probability action excludes a high-value fault domain |
| time_min | recommended | expected hands-on minutes |
| priority_score | optional | `(p_hit + 0.5 * p_exclude) / max(time_min + setup_min + risk_penalty, 1)` |
