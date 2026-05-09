# Architecture-First Output Contract

```md
# Architecture-First Debug Decision Tree

## 1. Project Context Summary
## 2. Input Cleaning Snapshot
## 3. Architecture / Link Understanding
## 4. Evidence-Aware Link Model
## 5. Fact / Assumption Table
## 6. Fault-Domain Localization
## 7. Hypothesis Tree With Probabilities
## 8. Candidate Matching Report
## 9. Adopted / Deferred / Not Applied
## 10. Cost / Probability Ranking
## 11. Optimal Troubleshooting Path
## 12. Decision Tree
## 13. Node Explanation Table
## 14. Missing Architecture Information
## 15. Next 3-5 Actions
## 16. Stop / Escalation Conditions
## 17. Retrospective Trigger
```

## Evidence-Aware Link Model Requirements

Include a graph or structured table that separates at least these layers when applicable:

- control/configuration path
- power/reset/clock prerequisites
- data path
- receiver/consumer pipeline
- observation and measurement points

Each link node must state what is known, what is inferred, what is unknown, and what evidence would move the debug boundary.

## Hypothesis Requirements

Include a hypothesis tree or table with:

- root symptom
- competing fault domains
- probability estimate
- evidence that raises the hypothesis
- evidence that lowers or falsifies it
- first action that can distinguish it from neighbors

Probabilities are decision priors, not truth claims. Mark them as subjective unless calibrated by regression or solved-case statistics.

Probability rules:

- The simplest physical interpretation of the direct symptom should be in the top two unless explicit contrary evidence demotes it.
- Do not let "not yet measured" alone outrank the closest physical boundary indicated by the symptom.
- Stale facts or non-same-interval facts may appear as context, but must not directly raise or lower probabilities until re-verified.
- Include a small `unknown / model gap` hypothesis when the model may be incomplete.

## Action Decision Requirements

The `Decision Tree` section is the action decision tree. It must map each early action to the hypothesis or link boundary it confirms, falsifies, or excludes.

## Cost And Ownership Requirements

- Use `reasoning/cost_priors.yaml` or a stated local override for `time_min` estimates.
- Show cumulative path cost for the optimal path when more than three actions are chained.
- If owner names are inferred from chat participation, label them as candidate owners and state that PM/project lead confirmation is required.
- Distinguish broad knowledge retrieval from low-cost point checks such as datasheet polarity verification.
