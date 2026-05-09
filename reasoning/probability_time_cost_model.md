# Probability / Time-Cost Model

Purpose: rank debug actions by expected time-to-isolation, not by habit or narrative order.

## Core Idea

For each candidate action, estimate:

- `p_hit`: probability this action directly identifies or fixes the dominant fault.
- `p_exclude`: probability this action cleanly excludes a high-value fault domain.
- `time_min`: expected hands-on time in minutes.
- `setup_min`: setup / access time in minutes.
- `risk_penalty`: 0 for safe/reversible actions, higher for risky or disruptive actions.
- `reversibility`: reversible / partial / irreversible.
- `evidence_quality`: low / medium / high.

Then compute a simple priority score:

```text
information_value = p_hit + exclude_weight * p_exclude
cost = time_min + setup_min + risk_penalty
priority_score = information_value / max(cost, 1)
```

Default `exclude_weight`:

| mode | exclude_weight | rationale |
|---|---:|---|
| fast_path | 0.3 | confirmation of a strong signature is usually more valuable than broad exclusion |
| standard | 0.5 | balanced default |
| architecture_first | 0.7 | early architecture debug often gains more from excluding whole boundaries |
| knowledge_linked | 0.6 | documented claims can cheaply exclude mismatched branches, but target evidence still dominates |

Higher score should usually appear earlier in the troubleshooting path.

## Safety Override

Safety gates override probability. A destructive action with a high `p_hit` still cannot be selected before a safe envelope exists.

## Dependency Override

Some actions are prerequisites. If a later action depends on an earlier measurement, the prerequisite must appear first even if its standalone score is lower.

Example:

```text
Do not calculate MOSFET SOA from VDS * ID until VDS and ID are captured safely.
```

## Typical Cost Priors

Use `reasoning/cost_priors.yaml` as the offline prior table. If a case-specific estimate differs, state the reason explicitly.

Local override requirements:

- name the closest prior class or state that no matching prior exists;
- state the overridden `time_min` used in the ranking;
- give the concrete local reason, such as partial data already collected, fixture already set up, access constraints, missing probe points, or required alignment across instruments.

## Output Requirement

When producing a full debug tree, include either:

1. a compact `Cost / Probability Ranking` table before the tree, or
2. `p_hit`, `p_exclude`, and `time_min` columns in the Node Explanation Table.

Fast Path outputs may use a compact top-action ranking.

## Meta-Reflection Questions

After the actual resolution is known:

- Did the first three actions include the actual root-cause path?
- Was the actual fix hidden behind a low-probability assumption?
- Did a low-cost measurement exist that would have found it earlier?
- Did safety or dependency constraints correctly override the score?
- Should priors change for this class of fault?
