# Real Project Case Intake

Purpose: ingest real project debug material without mixing confidential raw notes, blind training records, and promoted assets.

## Directory Flow

```text
inbox/ -> sanitized/ -> reviewed/ -> promoted assets/regression
```

- `inbox/`: raw user-provided material or placeholders. Keep confidential files local and anonymized before promotion.
- `sanitized/`: cleaned case facts with product/customer identifiers removed.
- `reviewed/`: closed-loop records after blind prediction, reveal, coverage score, and meta-reflection.

## Required Loop

1. Capture the initial symptom, context, constraints, and available observations.
2. Generate a blind debug tree before looking at the final fix.
3. Estimate `p_hit`, `p_exclude`, `time_min`, `setup_min`, `risk_penalty`, and `priority_score`.
4. Reveal the real resolution and score coverage as `hit`, `near_hit`, `miss`, or `blocked`.
5. Convert every `near_hit` or `miss` into one of:
   - link model refinement
   - signature
   - debug principle
   - regression test
   - explicit counterexample

## Real-Case Rule

Only evidence-backed, anonymized, solved project records can become `case_record` assets with `source.type: real_case`.
