# Frozen Artifact Replay

This directory records raw user prompts and frozen generated artifacts that
should survive the full DebugTool validation path.

The replay runner does not call an LLM in CI. Instead, it verifies that committed
frozen replay outputs paired with the raw prompts:

- pass the relevant `scripts/output_validator.py` mode;
- preserve system-critical fields such as `provenance`, `co_acq_group_id`, and
  evidence-ledger gates;
- do not regress into known bad structures such as flat root-cause probability
  tables or stale evidence directly changing probabilities.

Run:

```bash
python scripts/run_frozen_artifact_replay.py
```
