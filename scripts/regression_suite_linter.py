#!/usr/bin/env python3
import sys
from pathlib import Path

import yaml

for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        _reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
suite = yaml.safe_load(
    (ROOT / "regression" / "minimal_regression_suite.yaml").read_text(encoding="utf-8")
)
tests = suite.get("tests", [])
bad = []
for t in tests:
    for k in ["id", "input"]:
        if k not in t:
            bad.append(f"missing {k} in {t}")
    if not any(
        k in t for k in ["must_include", "must_not_include", "must_select", "must_not_select"]
    ):
        bad.append(f"{t.get('id')}: no assertions")
if bad:
    print("REGRESSION SUITE STRUCTURE FAILED")
    for b in bad:
        print("-", b)
    sys.exit(1)

print(f"REGRESSION SUITE STRUCTURE PASSED: {len(tests)} tests")
print("This is a suite linter, not a full LLM regression runner.")
for t in tests:
    print(f"- {t['id']}: {t['input']}")
