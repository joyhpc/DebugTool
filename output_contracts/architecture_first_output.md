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

## Boundary / Mechanism Probability Requirements

For unresolved multi-link cases, do not force every likely item into one flat root-cause probability table. Separate at least these tables:

- `Boundary Distribution`: where the signal or state first leaves spec. Rows must be `type=boundary`; probabilities are mutually exclusive and must sum to about 1.00. Include `evidence_refs` so each top-two physical boundary cites observed fact IDs from the Fact / Assumption Table.
- `Mechanism Prior`: mechanisms that could cause one or more boundaries. Rows must use `type=mechanism` or `type=observability_gap`; `p_active` values are independent and must not be forced to sum to 1.00.
- `Coverage Matrix`: each mechanism must state which boundaries it can explain using a compact scale such as `H/M/L/-`.
- `Evidence Ledger`: same-window evidence status for each key measurement. Required columns: `id`, `evidence`, `status`, `criticality`, `gates_boundaries`, `gates_mechanisms`, `probability_effect`, and `local_override`.

Probabilities are decision priors, not truth claims. Mark them as subjective unless calibrated by regression or solved-case statistics.

Probability rules:

- The simplest physical interpretation of the direct symptom should be in the top two unless explicit contrary evidence demotes it.
- Do not let "not yet measured" alone outrank the closest physical boundary indicated by the symptom.
- Stale facts or non-same-interval facts may appear as context, but must not directly raise or lower probabilities until re-verified.
- Include an `unknown / model gap` hypothesis in unresolved Architecture-First outputs. It must reserve at least 2% probability, so known branches do not silently consume all uncertainty.
- State the direct-symptom top-two reasoning explicitly, and bind the top-two physical boundary rows to observed fact IDs through `evidence_refs` so structural validation can catch silent drift.
- If a hypothesis intentionally bundles multiple physical mechanisms because data is insufficient, name the split trigger that will force it to become separate branches.
- Do not put `boundary`, `mechanism`, and `observability_gap` rows into the same mutually exclusive probability table.
- Observability gaps are measurement/diagnostic gaps. Their actions should improve evidence quality, not change hardware.
- If critical same-window evidence is missing, relevant boundary or mechanism probabilities must not exceed 0.50 unless the output explicitly states a local override and why. This must be mechanically joinable through `gates_boundaries` and `gates_mechanisms`, not only described in prose.

Evidence ledger rules:

- `status` must be one of `present`, `missing`, or `partial`.
- `criticality` must be one of `critical` or `supporting`.
- Each row must gate at least one boundary or mechanism.
- `local_override` may be `none`; if it raises a gated probability above 0.50, it must state the previous cap, new value, and reason.

## Action Decision Requirements

The `Decision Tree` section is the action decision tree. It must map each early action to the boundary subset and mechanism subset it confirms, falsifies, or excludes. If several P0 actions must be captured in the same failure reproduction, bind them as a co-acquisition batch instead of presenting them as a purely sequential ranking.

## Cost And Ownership Requirements

- Use `reasoning/cost_priors.yaml` or a stated local override for `time_min` estimates.
- Any local override must state the base prior or prior class, the overridden value, and the reason.
- Show cumulative path cost for the optimal path when more than three actions are chained.
- If owner names are inferred from chat participation, label them as candidate owners and state that PM/project lead confirmation is required.
- Distinguish broad knowledge retrieval from low-cost point checks such as datasheet polarity verification.
- `Cost / Probability Ranking` must include `tier`, `co_acq_group_id`, `same_failure_window`, `capture_channel`, `boundary_subset`, `mechanism_subset`, `prior_source`, `p_hit`, `p_exclude`, and `time_min` columns.
- Every cost row must cite `cost_priors.yaml` or a stated local override in `prior_source`.
- P0 rows must have a non-empty `co_acq_group_id`. Multi-row co-acquisition groups must set `same_failure_window=true` on every member. Single-row P0 groups are allowed only when the row explains why it is a standalone prerequisite or matrix-normalization action.

## Retrospective Trigger Requirements

Retrospective triggers must include both:

- target-case triggers, such as a branch being confirmed or a fix reducing failure rate;
- skill-level learning triggers, such as a solved case changing a reusable link-model rule, input-cleaning rule, ranking prior, cost prior, or evidence-audit check.
