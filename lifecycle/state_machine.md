# Asset State Machine

```text
draft → candidate → validated_seed → validated_real_case → generalized
   ↘ deprecated
```

## Transitions

- draft → candidate:
  - schema valid
  - fields complete
  - lint passes
- candidate → validated_seed:
  - used in one real case with correct outcome
  - has at least one regression candidate
- validated_seed → validated_real_case:
  - V0.99 founder-pilot threshold: backed by at least one real solved case, with evidence traceable to a `case_record`
  - V1.0 general-release threshold: reused in at least three independent cases
  - at least one negative test passes
  - promotion policy review passes
- validated_real_case → generalized:
  - reused across at least two projects/domains
- any → deprecated:
  - contradicted by validated case
  - stale
  - no longer useful
