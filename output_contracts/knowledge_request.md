# Knowledge Request Contract

Use this after input cleaning and first-pass link modeling only when external knowledge escalation is triggered.

Do not create a Knowledge Request for ordinary missing details. Ask a concise question or mark the item as an assumption unless the missing knowledge would change the first two actions, safety envelope, link model boundary, or top hypothesis ranking.

If the user explicitly asks for online learning, broad exploration, my-wiki learning, similar problems, or interactive model building, this contract becomes the staging point for that exploration.

```md
# Knowledge Request

## 1. Trigger
## 2. Exploration Mode
## 3. Knowledge Source Resolution
## 4. Knowledge Gaps
## 5. Queries
## 6. Expected Evidence
## 7. Affected Link Nodes / Hypotheses
## 8. Similar Problem Expansion
## 9. Checkpoints
## 10. Stop Condition
```

## Exploration Mode

| field | allowed_values |
|---|---|
| breadth | targeted / broad |
| interaction | one_pass / checkpointed |
| source_scope | user_provided / workspace / registry / web / mixed |

## Similar Problem Expansion Table

| field | description |
|---|---|
| match_axes | project/chip, interface family, failure signature, link-model stage, evidence/action shape |
| registry_seeds | authoritative queue, focused domain queue, public solved-case queue, candidate sources, workspace wiki |
| transfer_policy | transfer measurements/actions/model stages; do not transfer root cause without target evidence |

## Knowledge Gaps Table

| gap_id | missing_knowledge | why_needed | affects | current_state |
|---|---|---|---|---|
| KG1 | target conditioner enable polarity and board connection | distinguishes enable issue from downstream path issue | H5 / D_CONDITIONER | missing |

## Queries Table

| query_id | query | target_scope | source_priority | expected_evidence | affects |
|---|---|---|---|---|---|
| KQ1 | target board conditioner enable polarity and connection | project wiki, schematic, datasheet | project docs then vendor docs | schematic net or datasheet claim | KG1 |

## Rules

- Generate queries from entities, link nodes, missing facts, and high-impact hypotheses.
- Prefer project-specific knowledge over generic knowledge.
- For web exploration, prefer official/vendor/standards sources over blogs or forums.
- Separate "need datasheet behavior" from "need board-level measurement".
- Do not treat query results as facts until they are extracted into claims.
- If no knowledge source is available, list the unavailable source and keep the affected hypotheses assumption-bound.
