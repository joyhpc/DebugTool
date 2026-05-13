# Output Validator Rule Index

This index maps stable `V-*` validator IDs to their rationale and regression
coverage. Keep it updated whenever `scripts/output_validator.py` adds or changes
a named rule.

| rule_id | applies_to | rationale | covered_by |
|---|---|---|---|
| V-NO-FLAT-ROOTCAUSE | architecture_first | Prevent unresolved Architecture-First outputs from collapsing boundary, mechanism, and observability gaps into one normalized root-cause table. | `architecture_flat_table_bad_expected_fail.md` |
| V-COVERAGE-COMPLETE | architecture_first | Ensure every mechanism maps to the boundaries it can explain, so probability tables remain inspectable. | `architecture_hotswap_good.md`, architecture negative fixtures |
| V-EVIDENCE-LEDGER-LINKED | architecture_first | Ensure evidence rows gate at least one boundary or mechanism instead of becoming prose-only bookkeeping. | `architecture_hotswap_good.md` |
| V-EVIDENCE-CAP | architecture_first | Cap high-probability claims when critical same-window evidence is missing unless a local override explains the exception. | `architecture_evidence_cap_bad_expected_fail.md`, `architecture_evidence_override_bad_expected_fail.md` |
| V-BOUNDARY-SUM | architecture_first | Preserve explicit unknown/model-gap probability in the mutually exclusive boundary distribution. | `architecture_hotswap_good.md` |
| V-MECH-NO-FORCED-SUM | architecture_first | Prevent independent mechanism priors from being normalized as if only one mechanism can be active. | architecture negative fixtures |
| V-P0-CO-ACQ-GROUP | architecture_first | Force P0 same-window actions to declare co-acquisition grouping and standalone exceptions. | `architecture_p0_no_group_bad_expected_fail.md`, `architecture_hotswap_good.md` |
| V-DIRECT-SYMPTOM-EVIDENCE | architecture_first | Make top-two direct-symptom ranking mechanically traceable to observed fact IDs, not just the phrase “top two”. | `architecture_spell_words_bad_expected_fail.md`, `architecture_hotswap_good.md` |

## Evidence Audit Semantic Checks

Evidence-audit semantic checks are intentionally not `V-*` IDs yet, but they are
stronger than keyword search: each required semantic check must appear with a
same-line `pass`, `fail`, or `n/a` verdict. This is covered by:

- `evidence_audit_good.md`
- `evidence_audit_spell_words_bad_expected_fail.md`
- `evidence_audit_semantic_bad_expected_fail.md`
