# End-to-End Replay

This directory records raw user prompts and the generated artifacts that should
survive the full DebugTool validation path.

The replay runner does not call an LLM in CI. Instead, it verifies that committed
replay outputs generated from the raw prompts:

- pass the relevant `scripts/output_validator.py` mode;
- preserve system-critical fields such as `provenance`, `co_acq_group_id`, and
  evidence-ledger gates;
- do not regress into known bad structures such as flat root-cause probability
  tables or stale evidence directly changing probabilities.

Run:

```bash
python scripts/run_end_to_end_replay.py
```

