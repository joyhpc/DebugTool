# Project Architecture

```text
natural-language intake -> input cleaning -> safety -> routing -> link model -> assets -> reasoning -> output contracts -> lifecycle -> training feedback
                                                     \
                                                      optional knowledge escalation -> knowledge source resolution -> claim extraction
```

## Layer Responsibilities

| Layer | Responsibility |
|---|---|
| natural-language intake | accept terse user bug reports, issue notes, waveform descriptions, and chat extracts without requiring a form |
| input cleaning | preserve raw facts while separating observations, judgments, actions tried, proposed methods, revisions, and missing data |
| routing/ | choose debug mode |
| link model | identify system boundaries, assumptions, observable evidence, and knowledge gaps |
| optional knowledge escalation | enter retrieval only when user request or high-impact model gaps justify it |
| knowledge source resolution | find external workspace knowledge through user path, environment, config, or sibling discovery after escalation |
| claim extraction | convert retrieved wiki/docs material into compact documented claims with source paths after escalation |
| prompts/ | user-facing invocation |
| forms/ | structured input |
| assets/ | reusable link models, signatures, pattern bundles, debug principles, and case records |
| reasoning/ | matching, scoring, evidence gates, contradictions, probability/time-cost ordering |
| output_contracts/ | output format and node table consistency |
| safety/ | safety gate and domain safety rules |
| lifecycle/ | retrospective, promotion, regression, maintenance |
| retrieval/ | optional portable knowledge-source resolution, project knowledge search, and fact extraction |
| regression/ | test suites |
| training/ | blind closed-loop training records and authoritative-source queue |
| scripts/ | asset lint, closed-loop lint, regression suite lint, and output validation |

## Feedback Loop

1. Authoritative or user-provided source enters `training/closed_loop/`.
2. The initial symptom/background is converted into a blind input.
3. The skill generates a probability/time-cost ranked debug tree.
4. The actual resolution is revealed and scored as `hit`, `near_hit`, `miss`, or `blocked`.
5. Stable learning is promoted into assets or regression tests.

## Natural-Language Delivery Loop

1. User provides any bug report or issue-sync note.
2. The skill creates an Input Cleaning Record and Router-Ready Case Brief.
3. Safety and routing select the strongest mode.
4. A first-pass link model identifies assumptions, observables, and knowledge gaps.
5. External workspace knowledge is resolved and converted into documented claims only when escalation is triggered.
6. The output includes link model, fact/assumption split, hypothesis probabilities, and action decision tree.
7. New evidence updates the probabilities and demotes stale branches before new actions are proposed.
