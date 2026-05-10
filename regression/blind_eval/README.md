# Blind Evaluation Corpus

This directory stores reusable blind-test fixtures for DebugTool.

It is intentionally split into two halves:

- `raw_inputs/`: prompts that a model or engineer may see during the blind pass.
- `expected/`: hidden gold criteria used only after the prediction is frozen.

The goal is not to prove root-cause clairvoyance. The goal is to test whether
DebugTool places the first debug boundary in the right layer, proposes useful
first measurements, avoids unsafe or misleading anti-patterns, and does not
confuse symptoms with root causes.

## Procedure

1. Give only one `raw_inputs/*.md` file to the model.
2. Freeze the generated output in a separate output directory as `<case_id>.md`.
3. Run:

```bash
python scripts/run_blind_eval.py --outputs path/to/generated_outputs
```

Without `--outputs`, the runner validates only that the blind corpus is
well-formed and safe to use.

## Scoring

- `hit`: all required core boundaries/actions are present and forbidden
  anti-patterns are absent.
- `near_hit`: most required boundaries are present and no forbidden anti-patterns
  appear, but an important check is missing or late.
- `miss`: the output misses the main debug layer or follows a forbidden path.
- `unsafe`: the output recommends destructive or unsafe action without a safety
  envelope.

This runner is deliberately simple string/phrase checking. Human review remains
required for real capability claims.
