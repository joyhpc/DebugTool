#!/usr/bin/env python3
"""Validate and optionally score DebugTool blind-evaluation fixtures.

This runner does not call an LLM. It keeps the blind corpus reusable by
validating that each case has:

- a raw input that is safe to show before prediction
- hidden expected criteria for after-prediction scoring
- a trace back to the reviewed closed-loop source record

When --outputs is provided, the runner scores committed or generated outputs
named <case_id>.md in that directory using simple must-include / must-not-include
criteria. This is a coarse gate; human review is still required for capability
claims.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        _reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "regression" / "blind_eval" / "manifest.yaml"

RAW_LEAKAGE_PHRASES = [
    "actual_resolution",
    "actual resolution",
    "accepted answer",
    "hit_criteria",
    "must_include",
    "must_not_include",
]


@dataclass
class CaseScore:
    case_id: str
    result: str
    required_hits: int
    required_total: int
    forbidden_hits: list[str]
    missing_required: list[str]
    output_path: Path | None


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def contains_casefold(text: str, needle: str) -> bool:
    return needle.casefold() in text.casefold()


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def validate_expected(case_id: str, expected_path: Path, failures: list[str]) -> dict[str, Any]:
    if not expected_path.exists():
        failures.append(f"{case_id}: expected criteria missing: {rel(expected_path)}")
        return {}

    expected = load_yaml(expected_path)
    criteria = expected.get("hit_criteria") or {}
    required = [str(item) for item in as_list(criteria.get("must_include"))]
    forbidden = [str(item) for item in as_list(criteria.get("must_not_include"))]

    if expected.get("case_id") != case_id:
        failures.append(f"{case_id}: expected.case_id does not match manifest id")
    if not expected.get("actual_resolution_summary"):
        failures.append(f"{case_id}: expected file missing actual_resolution_summary")
    if len(required) < 5:
        failures.append(f"{case_id}: expected hit_criteria.must_include needs at least 5 phrases")
    if not forbidden:
        failures.append(f"{case_id}: expected hit_criteria.must_not_include must be non-empty")

    threshold = criteria.get("near_hit_min_fraction", 0.7)
    if not isinstance(threshold, (int, float)) or not 0 <= float(threshold) <= 1:
        failures.append(f"{case_id}: near_hit_min_fraction must be between 0 and 1")

    return expected


def validate_raw_input(case_id: str, raw_path: Path, failures: list[str]) -> str:
    if not raw_path.exists():
        failures.append(f"{case_id}: raw input missing: {rel(raw_path)}")
        return ""

    text = raw_path.read_text(encoding="utf-8")
    if len(text.strip()) < 80:
        failures.append(f"{case_id}: raw input is too short for a blind eval")
    for heading in ["## Symptom", "## Background", "## Observations", "## Constraints"]:
        if heading not in text:
            failures.append(f"{case_id}: raw input missing heading {heading}")
    for phrase in RAW_LEAKAGE_PHRASES:
        if contains_casefold(text, phrase):
            failures.append(f"{case_id}: raw input leaks scoring phrase '{phrase}'")
    return text


def validate_case(case: dict[str, Any], failures: list[str]) -> dict[str, Any] | None:
    case_id = str(case.get("id") or "")
    if not case_id:
        failures.append("case entry missing id")
        return None

    for key in ["source_record", "raw_input", "expected"]:
        if not case.get(key):
            failures.append(f"{case_id}: missing {key}")
            return None

    source_path = ROOT / str(case["source_record"])
    raw_path = ROOT / str(case["raw_input"])
    expected_path = ROOT / str(case["expected"])

    if not source_path.exists():
        failures.append(f"{case_id}: source record missing: {rel(source_path)}")
    validate_raw_input(case_id, raw_path, failures)
    expected = validate_expected(case_id, expected_path, failures)

    return {
        "id": case_id,
        "raw_path": raw_path,
        "expected_path": expected_path,
        "expected": expected,
    }


def find_output(outputs_dir: Path, case_id: str) -> Path | None:
    for suffix in [".md", ".markdown", ".txt"]:
        path = outputs_dir / f"{case_id}{suffix}"
        if path.exists():
            return path
    return None


def score_output(case_data: dict[str, Any], outputs_dir: Path) -> CaseScore:
    case_id = str(case_data["id"])
    output_path = find_output(outputs_dir, case_id)
    expected = case_data["expected"]
    criteria = expected.get("hit_criteria") or {}
    required = [str(item) for item in as_list(criteria.get("must_include"))]
    forbidden = [str(item) for item in as_list(criteria.get("must_not_include"))]
    threshold = float(criteria.get("near_hit_min_fraction", 0.7))

    if output_path is None:
        return CaseScore(
            case_id=case_id,
            result="missing_output",
            required_hits=0,
            required_total=len(required),
            forbidden_hits=[],
            missing_required=required,
            output_path=None,
        )

    text = output_path.read_text(encoding="utf-8")
    missing_required = [phrase for phrase in required if not contains_casefold(text, phrase)]
    forbidden_hits = [phrase for phrase in forbidden if contains_casefold(text, phrase)]
    required_hits = len(required) - len(missing_required)
    fraction = required_hits / len(required) if required else 0.0

    if forbidden_hits:
        result = "miss"
    elif not missing_required:
        result = "hit"
    elif fraction >= threshold:
        result = "near_hit"
    else:
        result = "miss"

    return CaseScore(
        case_id=case_id,
        result=result,
        required_hits=required_hits,
        required_total=len(required),
        forbidden_hits=forbidden_hits,
        missing_required=missing_required,
        output_path=output_path,
    )


def print_scores(scores: list[CaseScore]) -> None:
    print("BLIND EVAL OUTPUT SCORES")
    for score in scores:
        location = rel(score.output_path) if score.output_path else "<missing>"
        print(
            f"- {score.case_id}: {score.result} "
            f"required={score.required_hits}/{score.required_total} output={location}"
        )
        if score.missing_required:
            print(f"  missing_required: {', '.join(score.missing_required)}")
        if score.forbidden_hits:
            print(f"  forbidden_hits: {', '.join(score.forbidden_hits)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and score DebugTool blind eval cases.")
    parser.add_argument(
        "--manifest", default=str(DEFAULT_MANIFEST), help="Blind eval manifest path"
    )
    parser.add_argument("--outputs", help="Directory containing generated <case_id>.md outputs")
    parser.add_argument(
        "--allow-missing-outputs",
        action="store_true",
        help="When scoring outputs, do not fail if some case outputs are missing",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    if not manifest_path.exists():
        print(f"BLIND EVAL FAILED\n- manifest not found: {rel(manifest_path)}")
        return 2

    manifest = load_yaml(manifest_path)
    failures: list[str] = []
    cases = as_list(manifest.get("cases"))
    if not cases:
        failures.append("manifest has no cases")

    case_data: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict):
            failures.append("case entry must be a mapping")
            continue
        case_id = str(case.get("id") or "")
        if case_id in seen_ids:
            failures.append(f"{case_id}: duplicate case id")
        seen_ids.add(case_id)
        validated = validate_case(case, failures)
        if validated:
            case_data.append(validated)

    if failures:
        print("BLIND EVAL CORPUS FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"BLIND EVAL CORPUS PASSED: {len(case_data)} cases")

    if not args.outputs:
        return 0

    outputs_dir = Path(args.outputs)
    if not outputs_dir.is_absolute():
        outputs_dir = ROOT / outputs_dir
    scores = [score_output(case, outputs_dir) for case in case_data]
    print_scores(scores)

    bad = [score for score in scores if score.result in {"miss", "missing_output"}]
    if args.allow_missing_outputs:
        bad = [score for score in bad if score.result != "missing_output"]
    if bad:
        print(f"BLIND EVAL OUTPUT CHECK FAILED: {len(bad)} cases need review")
        return 3

    print("BLIND EVAL OUTPUT CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
