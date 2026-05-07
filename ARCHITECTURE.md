# Project Architecture

```text
routing -> context acquisition -> assets -> reasoning -> output contracts -> safety -> lifecycle -> training feedback
```

## Layer Responsibilities

| Layer | Responsibility |
|---|---|
| routing/ | choose debug mode |
| prompts/ | user-facing invocation |
| forms/ | structured input |
| assets/ | reusable link models, signatures, pattern bundles, debug principles, and case records |
| reasoning/ | matching, scoring, evidence gates, contradictions, probability/time-cost ordering |
| output_contracts/ | output format and node table consistency |
| safety/ | safety gate and domain safety rules |
| lifecycle/ | retrospective, promotion, regression, maintenance |
| retrieval/ | project knowledge search and fact extraction |
| regression/ | test suites |
| training/ | blind closed-loop training records and authoritative-source queue |
| scripts/ | asset lint, closed-loop lint, regression suite lint, and output validation |

## Feedback Loop

1. Authoritative or user-provided source enters `training/closed_loop/`.
2. The initial symptom/background is converted into a blind input.
3. The skill generates a probability/time-cost ranked debug tree.
4. The actual resolution is revealed and scored as `hit`, `near_hit`, `miss`, or `blocked`.
5. Stable learning is promoted into assets or regression tests.
