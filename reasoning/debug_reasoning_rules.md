# Debug Reasoning Rules

## Action Types

- observe: measure/log/read without changing system
- isolate: remove/disable one variable
- perturb: intentionally change one condition
- replace: swap part/cable/module
- reconfigure: change setting/firmware/config
- reproduce: attempt to trigger issue
- rollback: restore previous known-good state

## Priority Scoring

```text
score = information_gain - risk_weight*risk - cost_weight*cost + reversibility_bonus
```

## Stop Conditions

- root_cause_confidence >= high
- top 3 actions produce no evidence shift
- observation contradicts chosen signature
- safety level increases
- hidden architecture dependency appears

## Contradiction Handling

1. Keep both facts.
2. Mark one or both as contradicted.
3. Ask for targeted re-measurement.
4. Do not use contradicted facts as sole evidence.
