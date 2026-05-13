#!/usr/bin/env python3
"""Lint real project case intake records when present."""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REAL = ROOT / "training" / "real_project_cases"
VALID_STATUS = {"draft", "sanitized", "reviewed", "promoted", "blocked"}
VALID_RESULTS = {"hit", "near_hit", "miss", "blocked"}

errors: list[str] = []
warnings: list[str] = []


def fail(path: Path, msg: str) -> None:
    errors.append(f"{path}: {msg}")


def warn(path: Path, msg: str) -> None:
    warnings.append(f"{path}: {msg}")


def as_list(value):
    return value if isinstance(value, list) else []


for required in ["README.md", "intake_schema.yaml"]:
    path = REAL / required
    if not path.exists():
        fail(path, "missing real project case intake file")

case_paths = sorted(
    p for folder in ["sanitized", "reviewed"] for p in (REAL / folder).glob("*.yaml")
)

for path in case_paths:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    cid = data.get("id")
    if not cid:
        fail(path, "missing id")
    elif not str(cid).startswith("RPC-"):
        fail(path, "id should start with RPC-")

    if data.get("status") not in VALID_STATUS:
        fail(path, f"status must be one of {sorted(VALID_STATUS)}")

    confidentiality = data.get("confidentiality") or {}
    if path.parent.name == "reviewed":
        if confidentiality.get("anonymized") is not True:
            fail(path, "reviewed real project case must be anonymized")
        if not (data.get("initial_problem") or {}).get("symptom"):
            fail(path, "initial_problem.symptom is required")
        if len(as_list(data.get("blind_debug_tree"))) < 3:
            fail(path, "blind_debug_tree must include at least 3 nodes")
        coverage = data.get("coverage") or {}
        if coverage.get("result") not in VALID_RESULTS:
            fail(path, f"coverage.result must be one of {sorted(VALID_RESULTS)}")
        actual = data.get("actual_resolution") or {}
        if not actual.get("root_cause"):
            fail(path, "actual_resolution.root_cause is required for reviewed cases")

    if data.get("status") == "promoted":
        gate = data.get("promotion_gate") or {}
        if gate.get("ready_for_case_record") is not True:
            fail(path, "promoted case must set promotion_gate.ready_for_case_record true")

if errors:
    print("REAL PROJECT CASE LINT FAILED")
    for e in errors:
        print("-", e)
    if warnings:
        print("WARNINGS")
        for w in warnings:
            print("-", w)
    sys.exit(1)

print(f"REAL PROJECT CASE LINT PASSED: {len(case_paths)} case files")
if warnings:
    print("WARNINGS")
    for w in warnings:
        print("-", w)
