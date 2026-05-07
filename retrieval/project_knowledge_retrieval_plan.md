# Project Knowledge Retrieval Plan

1. Extract entities: project, board, revision, chips, interfaces, signals, rails, errors.
2. Generate queries: architecture, power tree, clock/reset, involved interface, bring-up, known issue, board revision.
3. Reject stale sources: wrong revision, old architecture, superseded bring-up notes.
4. Extract facts into observed / documented / inferred / assumed / user_confirmed / contradicted.
5. Build project model.
6. Generate debug tree using evidence_refs.
