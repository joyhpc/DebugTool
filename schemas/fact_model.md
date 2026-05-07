# Fact Confidence Model

| State | Meaning |
|---|---|
| observed | directly measured or logged |
| documented | retrieved from project/source docs |
| inferred | derived from facts |
| assumed | provisional assumption |
| user_confirmed | confirmed by user |
| contradicted | conflicts with another fact |

Fact format:

```text
F1 | documented | source=power_tree_revC.md | confidence=high | 1.2V rail EN is driven by PG_3V3
```

Decision nodes should reference facts via `evidence_refs`.
