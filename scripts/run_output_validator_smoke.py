#!/usr/bin/env python3
"""Run output-validator smoke cases with expected pass/fail outcomes."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "output_validator.py"

CASES = [
    ("input_cleaning", "input_cleaning_good.md", 0),
    ("input_cleaning", "input_cleaning_bad_expected_fail.md", 1),
    ("standard", "standard_good.md", 0),
    ("architecture_first", "architecture_hotswap_good.md", 0),
    ("evidence_audit", "evidence_audit_good.md", 0),
    ("evidence_audit", "evidence_audit_semantic_bad_expected_fail.md", 1),
    ("skill_improvement", "skill_improvement_good.md", 0),
    ("fast_path", "unsafe_phrase_mitigated_good.md", 0),
    ("standard", "standard_bad_expected_fail.md", 1),
    ("fast_path", "unsafe_phrase_bad_expected_fail.md", 1),
]


def main() -> int:
    failures: list[str] = []
    case_dir = ROOT / "regression" / "output_validator_smoke_cases"

    for mode, filename, expected in CASES:
        path = case_dir / filename
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR), "--mode", mode, "--file", str(path), "--quiet"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        passed = proc.returncode == expected
        status = "PASS" if passed else "FAIL"
        print(f"{status}: {filename} expected rc={expected}, got rc={proc.returncode}")
        if not passed:
            output = "\n".join(part for part in [proc.stdout.strip(), proc.stderr.strip()] if part)
            failures.append(f"{filename}: expected rc={expected}, got rc={proc.returncode}\n{output}")

    if failures:
        print("OUTPUT VALIDATOR SMOKE FAILED")
        for failure in failures:
            print("-", failure)
        return 1

    print(f"OUTPUT VALIDATOR SMOKE PASSED: {len(CASES)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
