# Output Validator Smoke Cases

These are small structural smoke cases for `scripts/output_validator.py`.

- `standard_good.md` should pass.
- `architecture_hotswap_good.md` should pass.
- `architecture_chinese_good.md` should pass. It covers Chinese Architecture-First prose with English contract headings.
- `architecture_spell_words_bad_expected_fail.md` should fail. It intentionally says "top two" and `cost_priors.yaml` without row-level evidence/cost provenance.
- `input_cleaning_good.md` should pass.
- `input_cleaning_bad_expected_fail.md` should fail. It intentionally omits the required cleaning tables and useful router-ready content.
- `unsafe_phrase_mitigated_good.md` should pass.
- `standard_bad_expected_fail.md` should fail. It intentionally omits required node columns, omits a Mermaid node from the table, and marks an S3 node without explicit safety mitigation language.
- `unsafe_phrase_bad_expected_fail.md` should fail. It intentionally includes an unsafe full-power hot-plug action with only global, not local, safety wording.
- `evidence_audit_spell_words_bad_expected_fail.md` should fail. It intentionally mentions semantic-check keywords without same-line pass/fail/n/a verdicts.

Commands:

```bash
python scripts/run_output_validator_smoke.py
```
