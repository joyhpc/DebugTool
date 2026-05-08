# Project Knowledge Retrieval Plan

Use this plan only after external knowledge escalation is triggered. Normal first-pass debugging should not query workspace knowledge.

Escalation triggers:

- The user explicitly asks to use a wiki, knowledge base, schematic, datasheet, repo, log archive, or prior debug record.
- The user explicitly asks to learn from the web, search online, broadly explore references, find similar problems, or build the model from external material.
- A high-impact gap would change the first two actions, safety envelope, link model boundary, or top hypothesis ranking.
- Built-in model knowledge is insufficient to identify the relevant components, pins, protocols, or observable evidence.
- The cleaned input contains an architecture or naming conflict that blocks a stable plan.

Exploration modes:

| mode | use when | behavior |
|---|---|---|
| targeted | source or gap is named | narrow query, extract claims, update affected nodes |
| interactive | user asks to co-build or ambiguity is material | checkpoint after request, source plan, claim extraction, and model update |
| broad | user asks to learn online or explore widely | search workspace and/or online sources, then synthesize model boundaries and claims |
| similar_problem | user asks for similar cases or the current model lacks known tactics | use `retrieval/high_value_source_registry.md` to find analogs by symptom, interface, link stage, and evidence/action shape |

1. Resolve external knowledge sources using `retrieval/knowledge_source_resolution.md`.
2. Extract entities from the cleaned input: project, board, revision, chips, interfaces, signals, rails, errors, people, timestamps, and known-good comparisons.
3. Build a preliminary link model from the user's input before retrieval.
4. Identify knowledge gaps that affect high-value link nodes or hypotheses.
5. Generate a Knowledge Request using `output_contracts/knowledge_request.md`.
6. If broad or similar-problem exploration is requested, search `retrieval/high_value_source_registry.md` seeds before unbounded web search.
7. Query resolved knowledge sources. For local workspace sources, `rg` is sufficient for the first pass. For online exploration, prefer official/vendor/standards sources and cite URLs.
8. Reject stale sources: wrong revision, old architecture, superseded bring-up notes, unrelated board, wrong part number, or non-authoritative source when a primary source is available.
9. Extract compact claims using `output_contracts/wiki_claim_extraction.md`.
10. Classify claims as observed / documented / inferred / assumed / user_confirmed / contradicted.
11. For similar cases, extract match axis, transferable lesson, applicability limit, and action impact.
12. Build or update the project model using evidence_refs and source paths.
13. Generate or update the debug tree using only cleaned facts, documented claims, transferable tactics, and explicit assumptions.

## Local Query Pattern

Use relative paths when possible:

```bash
rg -n "A57|984|eDP|Redriver|PWDN|SerDes" ../my-wiki ../HW-knowledge-base
```

Do not commit machine-local absolute paths in generated pilot records.

## Knowledge Boundary

- DebugTool owns the retrieval request, claim extraction, and reasoning.
- External workspace knowledge sources own raw notes, datasheets, schematics, and history.
- Online sources own public reference material; DebugTool may cite URLs and extracted claims.
- DebugTool may cite source paths/URLs and extracted claims.
- DebugTool must not copy large private wiki content into committed outputs.
