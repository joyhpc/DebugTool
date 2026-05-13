#!/usr/bin/env python3
"""Validate committed frozen artifact replay artifacts.

The replay runner is intentionally offline: CI does not call an LLM. A human or
agent generates outputs from the raw inputs, commits them as frozen artifacts,
and this script checks that those artifacts pass their output validators and
preserve case-specific semantic guardrails.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "regression" / "frozen_artifact_replay" / "manifest.yaml"
VALIDATOR = ROOT / "scripts" / "output_validator.py"


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def contains_casefold(text: str, needle: str) -> bool:
    return needle.casefold() in text.casefold()


def run_validator(mode: str, path: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--mode",
            mode,
            "--file",
            str(path),
            "--quiet",
            "--strict",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    output = "\n".join(part for part in [proc.stdout.strip(), proc.stderr.strip()] if part)
    return proc.returncode, output


def validate_output(case_id: str, output_spec: dict[str, Any], failures: list[str]) -> None:
    mode = str(output_spec.get("mode") or "")
    raw_file = output_spec.get("file")
    if not mode:
        failures.append(f"{case_id}: output entry missing mode")
        return
    if not raw_file:
        failures.append(f"{case_id}: output entry missing file")
        return

    path = ROOT / str(raw_file)
    if not path.exists():
        failures.append(f"{case_id}: output file missing: {rel(path)}")
        return

    rc, validator_output = run_validator(mode, path)
    if rc != 0:
        failures.append(
            f"{case_id}: validator failed for {rel(path)} mode={mode}\n{validator_output}"
        )
        return

    text = path.read_text(encoding="utf-8")
    for phrase in as_list(output_spec.get("must_include")):
        needle = str(phrase)
        if not contains_casefold(text, needle):
            failures.append(f"{case_id}: {rel(path)} missing required phrase: {needle}")
    for phrase in as_list(output_spec.get("must_not_include")):
        needle = str(phrase)
        if contains_casefold(text, needle):
            failures.append(f"{case_id}: {rel(path)} contains forbidden phrase: {needle}")


def validate_case(case: dict[str, Any], failures: list[str]) -> None:
    case_id = str(case.get("id") or "<missing-id>")
    raw_input = case.get("raw_input")
    if not raw_input:
        failures.append(f"{case_id}: missing raw_input")
        return

    raw_path = ROOT / str(raw_input)
    if not raw_path.exists():
        failures.append(f"{case_id}: raw input file missing: {rel(raw_path)}")
        return
    raw_text = raw_path.read_text(encoding="utf-8").strip()
    if len(raw_text) < 40:
        failures.append(f"{case_id}: raw input is too short to be a replay fixture")

    outputs = as_list(case.get("outputs"))
    if not outputs:
        failures.append(f"{case_id}: no outputs listed")
        return
    for output_spec in outputs:
        if not isinstance(output_spec, dict):
            failures.append(f"{case_id}: output entry must be a mapping")
            continue
        validate_output(case_id, output_spec, failures)


def main() -> int:
    manifest_path = DEFAULT_MANIFEST
    if len(sys.argv) > 1:
        manifest_path = ROOT / sys.argv[1]
    if not manifest_path.exists():
        print(f"FROZEN ARTIFACT REPLAY FAILED\n- manifest not found: {rel(manifest_path)}")
        return 2

    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    cases = as_list(manifest.get("cases"))
    failures: list[str] = []
    if not cases:
        failures.append("manifest has no cases")
    for case in cases:
        if not isinstance(case, dict):
            failures.append("case entry must be a mapping")
            continue
        validate_case(case, failures)

    if failures:
        print("FROZEN ARTIFACT REPLAY FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"FROZEN ARTIFACT REPLAY PASSED: {len(cases)} cases")
    for case in cases:
        print(f"- {case.get('id')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
