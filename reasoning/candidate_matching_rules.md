# Candidate Matching Rules

## Decisions

- Adopted: use_when satisfied, required_evidence present, no hard counterexample
- Deferred: plausible but missing required evidence
- Not Applied: counterexample present or wrong fault layer

## Signature Matching

A signature should define:

- min_match_count
- required_evidence
- forbid_match / do_not_use_when
- safety_level

Do not adopt a signature based on one vague keyword.
