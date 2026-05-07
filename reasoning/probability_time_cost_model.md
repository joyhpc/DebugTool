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
information_value = p_hit + 0.5 * p_exclude
cost = time_min + setup_min + risk_penalty
priority_score = information_value / max(cost, 1)
```

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

| Action type | Time prior | Notes |
|---|---:|---|
| visual / schematic review | 5-20 min | low risk, often high exclusion value |
| DMM static voltage / resistance check | 2-10 min | high value for power path and shorts |
| single oscilloscope capture | 10-30 min | setup-sensitive, high value for dynamic faults |
| logic analyzer capture | 10-40 min | high value for protocol/timing faults |
| component substitution | 20-120 min | should follow evidence unless socketed/trivial |
| layout rework / PCB cut | 30-240 min | partial/irreversible; require evidence |
| destructive reproduction | high/blocked | requires explicit safety envelope |

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
