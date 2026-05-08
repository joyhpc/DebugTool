# Knowledge Source Resolution

Use this only after external knowledge escalation is triggered. The goal is to find external knowledge sources without hard-coding one machine's directory layout.

Do not run this in the normal first-pass debug flow. If no escalation trigger is present, keep missing project knowledge as an explicit assumption or missing fact.

If the user explicitly asks for online learning or broad exploration, include online sources in the resolution plan after local/project-specific sources unless the user requests web-first.

If the user asks for similar problems, include `retrieval/high_value_source_registry.md` and its registry seeds before open-ended web search.

## Resolution Order

1. User-provided path in the current request.
2. User-provided URL or explicit online search instruction.
3. `DEBUGTOOL_KB_ROOT` environment variable.
4. Local `knowledge_sources.yaml` if present.
5. Workspace sibling discovery.
6. Existing registry seeds from `retrieval/high_value_source_registry.md`.
7. Official/public web sources when online exploration is requested.
8. Unavailable fallback.

## Workspace Sibling Discovery

When no explicit source is provided, check common sibling directories relative to the DebugTool repository root:

```text
../my-wiki
../knowledge
../HW-knowledge-base
../wiki
../docs
```

## Required Output

```md
# Knowledge Source Resolution

| source_id | resolved_path | status | reason | priority |
|---|---|---|---|---|
| my-wiki | ../my-wiki | available/unavailable | user/env/config/sibling/not_found | 1 |
| registry-seeds | training/... queues | available/unavailable | similar_problem_or_broad_exploration | 6 |
| web-official | vendor/standards URLs | planned/unavailable | explicit_online_request | 7 |
```

## Rules

- Never hard-code machine-local absolute paths in committed DebugTool outputs.
- Prefer relative paths in committed examples and pilot records.
- Do not copy private wiki content into DebugTool.
- Cite source paths and extracted claims only.
- If a source is unavailable, keep the affected claims as missing or assumed; do not invent knowledge.
- If multiple knowledge sources are available, use project-specific sources before generic vendor or public sources.
- For online exploration, prefer primary sources: vendor documentation, standards bodies, official app notes, official driver/framework documentation, and authoritative errata.

## Fallback Text

Use this when no external knowledge source is found:

```text
Knowledge source unavailable:
- expected: user-provided path, DEBUGTOOL_KB_ROOT, knowledge_sources.yaml, or workspace sibling wiki/docs
- impact: project-specific claims remain missing or assumed
- next action: provide a knowledge source path or continue with explicitly marked assumptions
```
