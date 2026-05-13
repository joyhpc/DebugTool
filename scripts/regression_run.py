#!/usr/bin/env python3
"""Generate a lightweight regression signal report.

Default output is intentionally based on real regression signal surfaces:

- blind-eval fixtures, optionally scored against generated outputs
- frozen artifact replay fixtures

Synthetic closed-loop closures are excluded unless --include-synthetic is set.
They remain useful as training priors, but they must not inflate regression
hit-rate claims.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        _reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORDS = ROOT / "training" / "closed_loop" / "records"
DEFAULT_SYNTHETIC = ROOT / "training" / "closed_loop" / "synthetic_closures"
DEFAULT_BLIND_MANIFEST = ROOT / "regression" / "blind_eval" / "manifest.yaml"
DEFAULT_FROZEN_MANIFEST = ROOT / "regression" / "frozen_artifact_replay" / "manifest.yaml"
VALID_RESULTS = {"hit", "near_hit", "miss", "blocked"}


@dataclass
class CorpusCase:
    case_id: str
    path: Path
    domain: str
    source_type: str
    status: str
    result: str
    blind_input: str
    actual_resolution: str
    predicted_nodes: int
    has_cost_model: bool
    errors: list[str]


@dataclass
class BlindEvalScore:
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


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def pct(value: float | None) -> str:
    if value is None:
        return "not scored"
    return f"{value * 100:.1f}%"


def collect_case_paths(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    if not root.exists():
        raise FileNotFoundError(root)
    return sorted(root.glob("*.yaml"))


def blind_input_text(blind: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ["symptom", "background"]:
        value = blind.get(key)
        if value:
            parts.append(str(value))
    for key in ["observations", "constraints"]:
        values = [str(v) for v in as_list(blind.get(key)) if v]
        if values:
            parts.extend(values)
    return "\n".join(parts)


def load_case(path: Path) -> CorpusCase:
    errors: list[str] = []
    try:
        data = load_yaml(path)
    except Exception as exc:
        return CorpusCase(
            case_id=path.stem,
            path=path,
            domain="unknown",
            source_type="unknown",
            status="parse_error",
            result="blocked",
            blind_input="",
            actual_resolution="",
            predicted_nodes=0,
            has_cost_model=False,
            errors=[f"failed to read/parse YAML: {exc}"],
        )

    case_id = str(data.get("id") or path.stem)
    source = data.get("source") or {}
    coverage = data.get("coverage") or {}
    blind = data.get("blind_input") or {}
    actual = data.get("actual_resolution") or {}
    tree = as_list(data.get("predicted_debug_tree"))
    cost_model = data.get("cost_model") or {}

    result = str(coverage.get("result") or "blocked")
    if result not in VALID_RESULTS:
        errors.append(f"coverage.result must be one of {sorted(VALID_RESULTS)}")
        result = "blocked"

    if not blind.get("symptom"):
        errors.append("blind_input.symptom is required")
    if not actual.get("summary"):
        errors.append("actual_resolution.summary is required")
    if len(tree) < 3:
        errors.append("predicted_debug_tree must include at least 3 nodes")
    if data.get("status") in {"reviewed", "promoted"} and not cost_model:
        errors.append("reviewed/promoted record must include cost_model")

    return CorpusCase(
        case_id=case_id,
        path=path,
        domain=str(data.get("domain") or "unknown"),
        source_type=str(source.get("type") or "unknown"),
        status=str(data.get("status") or "unknown"),
        result=result,
        blind_input=blind_input_text(blind),
        actual_resolution=str(actual.get("summary") or ""),
        predicted_nodes=len(tree),
        has_cost_model=bool(cost_model),
        errors=errors,
    )


def summarize_corpus(cases: list[CorpusCase]) -> dict[str, Any]:
    total = len(cases)
    counts = Counter(case.result for case in cases)
    by_domain: dict[str, Counter[str]] = defaultdict(Counter)
    by_source: dict[str, Counter[str]] = defaultdict(Counter)
    errors = {case.case_id: case.errors for case in cases if case.errors}

    for case in cases:
        by_domain[case.domain][case.result] += 1
        by_source[case.source_type][case.result] += 1

    return {
        "total": total,
        "counts": dict(counts),
        "hit_rate": ratio(counts["hit"], total),
        "near_hit_rate": ratio(counts["near_hit"], total),
        "miss_rate": ratio(counts["miss"], total),
        "blocked_rate": ratio(counts["blocked"], total),
        "with_cost_model": sum(1 for case in cases if case.has_cost_model),
        "by_domain": {key: dict(value) for key, value in sorted(by_domain.items())},
        "by_source_type": {key: dict(value) for key, value in sorted(by_source.items())},
        "case_errors": errors,
    }


def load_manifest_cases(
    manifest_path: Path, required_keys: list[str]
) -> tuple[list[dict[str, Any]], list[str]]:
    failures: list[str] = []
    if not manifest_path.exists():
        return [], [f"manifest not found: {rel(manifest_path)}"]

    manifest = load_yaml(manifest_path)
    cases = as_list(manifest.get("cases"))
    if not cases:
        failures.append(f"{rel(manifest_path)} has no cases")
        return [], failures

    seen: set[str] = set()
    valid_cases: list[dict[str, Any]] = []
    for idx, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            failures.append(f"{rel(manifest_path)} case[{idx}] must be a mapping")
            continue
        case_id = str(case.get("id") or "")
        if not case_id:
            failures.append(f"{rel(manifest_path)} case[{idx}] missing id")
            continue
        if case_id in seen:
            failures.append(f"{rel(manifest_path)} duplicate case id {case_id}")
        seen.add(case_id)
        for key in required_keys:
            value = case.get(key)
            if not value:
                failures.append(f"{case_id}: missing {key}")
                continue
            path = ROOT / str(value)
            if not path.exists():
                failures.append(f"{case_id}: missing {key} path {rel(path)}")
        valid_cases.append(case)
    return valid_cases, failures


def contains_casefold(text: str, needle: str) -> bool:
    return needle.casefold() in text.casefold()


def find_output(outputs_dir: Path, case_id: str) -> Path | None:
    for suffix in [".md", ".markdown", ".txt"]:
        path = outputs_dir / f"{case_id}{suffix}"
        if path.exists():
            return path
    return None


def score_blind_eval(case: dict[str, Any], outputs_dir: Path) -> BlindEvalScore:
    case_id = str(case["id"])
    output_path = find_output(outputs_dir, case_id)
    expected = load_yaml(ROOT / str(case["expected"]))
    criteria = expected.get("hit_criteria") or {}
    required = [str(item) for item in as_list(criteria.get("must_include"))]
    forbidden = [str(item) for item in as_list(criteria.get("must_not_include"))]
    threshold = float(criteria.get("near_hit_min_fraction", 0.7))

    if output_path is None:
        return BlindEvalScore(
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

    return BlindEvalScore(
        case_id=case_id,
        result=result,
        required_hits=required_hits,
        required_total=len(required),
        forbidden_hits=forbidden_hits,
        missing_required=missing_required,
        output_path=output_path,
    )


def summarize_blind_eval(
    cases: list[dict[str, Any]], scores: list[BlindEvalScore] | None
) -> dict[str, Any]:
    if scores is None:
        return {
            "total": len(cases),
            "scored": False,
            "hit_rate": None,
            "near_hit_rate": None,
            "miss_rate": None,
            "missing_output": None,
            "counts": {},
        }

    counts = Counter(score.result for score in scores)
    denominator = len(scores)
    return {
        "total": len(cases),
        "scored": True,
        "hit_rate": ratio(counts["hit"], denominator),
        "near_hit_rate": ratio(counts["near_hit"], denominator),
        "miss_rate": ratio(counts["miss"], denominator),
        "missing_output": counts["missing_output"],
        "counts": dict(counts),
        "scores": [
            {
                "id": score.case_id,
                "result": score.result,
                "required_hits": score.required_hits,
                "required_total": score.required_total,
                "missing_required": score.missing_required,
                "forbidden_hits": score.forbidden_hits,
                "output_path": rel(score.output_path) if score.output_path else None,
            }
            for score in scores
        ],
    }


def load_baseline(path: Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def delta(current: float | None, baseline: dict[str, Any] | None, key: str) -> str:
    if current is None:
        return "n/a"
    blind_summary = (baseline or {}).get("summary", {}).get("blind_eval", {})
    if key not in blind_summary or blind_summary[key] is None:
        return "n/a"
    previous = float(blind_summary[key])
    return f"{(current - previous) * 100:+.1f} pt"


def render_corpus_section(title: str, summary: dict[str, Any]) -> list[str]:
    lines = [
        f"## {title}",
        "",
        f"**Cases**: {summary['total']}",
        "",
        "| Metric | Result |",
        "|---|---:|",
        f"| Hit rate | {pct(float(summary['hit_rate']))} |",
        f"| Near-hit rate | {pct(float(summary['near_hit_rate']))} |",
        f"| Miss rate | {pct(float(summary['miss_rate']))} |",
        f"| Blocked rate | {pct(float(summary['blocked_rate']))} |",
        f"| Records with cost model | {summary['with_cost_model']} / {summary['total']} |",
        "",
    ]
    failed = summary.get("case_errors") or {}
    if failed:
        lines.extend(["### Invalid Cases", ""])
        for case_id, errors in failed.items():
            lines.append(f"- `{case_id}`: {'; '.join(errors)}")
        lines.append("")
    return lines


def render_markdown(payload: dict[str, Any], baseline: dict[str, Any] | None) -> str:
    blind = payload["summary"]["blind_eval"]
    frozen = payload["summary"]["frozen_replay"]
    lines = [
        f"# Regression Signal Report - {datetime.now(timezone.utc).isoformat()}",
        "",
        "Default metrics exclude synthetic closed-loop closures. Use `--include-synthetic` to inspect them as a separate, non-gating appendix.",
        "",
        "## Default Signal",
        "",
        "| Signal | Cases | Status |",
        "|---|---:|---|",
        f"| Blind eval | {blind['total']} | {'scored' if blind['scored'] else 'corpus only; outputs not supplied'} |",
        f"| Frozen artifact replay | {frozen['total']} | committed artifact stability |",
        "",
        "## Blind Eval Output Score",
        "",
        "| Metric | Result | vs Baseline |",
        "|---|---:|---:|",
        f"| Hit rate | {pct(blind['hit_rate'])} | {delta(blind['hit_rate'], baseline, 'hit_rate')} |",
        f"| Near-hit rate | {pct(blind['near_hit_rate'])} | {delta(blind['near_hit_rate'], baseline, 'near_hit_rate')} |",
        f"| Miss rate | {pct(blind['miss_rate'])} | {delta(blind['miss_rate'], baseline, 'miss_rate')} |",
        f"| Missing outputs | {blind['missing_output'] if blind['missing_output'] is not None else 'n/a'} | n/a |",
        "",
    ]

    if not blind["scored"]:
        lines.extend(
            [
                "No generated outputs were supplied, so no hit-rate gate was applied.",
                "Run with `--blind-outputs <dir>` to score `<case_id>.md` outputs.",
                "",
            ]
        )
    else:
        lines.extend(["### Case Scores", ""])
        for score in blind.get("scores", []):
            lines.append(
                f"- `{score['id']}`: {score['result']} "
                f"({score['required_hits']}/{score['required_total']})"
            )
        lines.append("")

    if "closed_loop" in payload["summary"]:
        lines.extend(
            render_corpus_section("Reviewed Closed-Loop Records", payload["summary"]["closed_loop"])
        )
    if "synthetic_closures" in payload["summary"]:
        lines.extend(
            render_corpus_section(
                "Synthetic Closures (Excluded From Default Gate)",
                payload["summary"]["synthetic_closures"],
            )
        )

    return "\n".join(lines).rstrip() + "\n"


def write_outputs(
    payload: dict[str, Any],
    baseline: dict[str, Any] | None,
    md_path: Path | None,
    json_path: Path | None,
) -> None:
    if md_path:
        md_path.write_text(render_markdown(payload, baseline), encoding="utf-8")
    if json_path:
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if not md_path and not json_path:
        print(render_markdown(payload, baseline))


def add_corpus_summary(
    payload: dict[str, Any], key: str, path: Path, invalid: dict[str, list[str]]
) -> None:
    paths = collect_case_paths(path)
    cases = [load_case(case_path) for case_path in paths]
    summary = summarize_corpus(cases)
    payload["summary"][key] = summary
    for case in cases:
        if case.errors:
            invalid[case.case_id] = case.errors
    payload["cases"][key] = [
        {
            "id": case.case_id,
            "path": rel(case.path),
            "domain": case.domain,
            "source_type": case.source_type,
            "status": case.status,
            "result": case.result,
            "predicted_nodes": case.predicted_nodes,
            "has_cost_model": case.has_cost_model,
            "errors": case.errors,
        }
        for case in cases
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize DebugTool regression signal.")
    parser.add_argument(
        "--cases",
        help="YAML file or directory of non-synthetic closed-loop records to include",
    )
    parser.add_argument(
        "--include-closed-loop",
        action="store_true",
        help="Include training/closed_loop/records as a non-synthetic corpus appendix",
    )
    parser.add_argument(
        "--include-synthetic",
        action="store_true",
        help="Include synthetic closures as a non-gating appendix",
    )
    parser.add_argument("--blind-manifest", default=str(DEFAULT_BLIND_MANIFEST))
    parser.add_argument("--frozen-manifest", default=str(DEFAULT_FROZEN_MANIFEST))
    parser.add_argument("--blind-outputs", help="Directory containing generated blind eval outputs")
    parser.add_argument("--output", help="Markdown report path")
    parser.add_argument("--json", help="JSON report path")
    parser.add_argument("--baseline", help="Prior JSON report for metric deltas")
    parser.add_argument("--fail-under", type=float, default=0.0, help="Minimum blind hit rate")
    parser.add_argument(
        "--max-blocked-pct",
        type=float,
        default=1.0,
        help="Maximum blocked rate for included closed-loop corpora",
    )
    parser.add_argument("--list-cases", action="store_true", help="List case ids and results")
    parser.add_argument("--validate-cases", action="store_true", help="Validate selected corpora")
    args = parser.parse_args()

    blind_manifest = Path(args.blind_manifest)
    if not blind_manifest.is_absolute():
        blind_manifest = ROOT / blind_manifest
    frozen_manifest = Path(args.frozen_manifest)
    if not frozen_manifest.is_absolute():
        frozen_manifest = ROOT / frozen_manifest

    blind_cases, blind_failures = load_manifest_cases(
        blind_manifest, ["source_record", "raw_input", "expected"]
    )
    frozen_cases, frozen_failures = load_manifest_cases(frozen_manifest, ["raw_input"])
    for case in frozen_cases:
        if not as_list(case.get("outputs")):
            frozen_failures.append(f"{case.get('id')}: missing outputs")

    outputs_dir = Path(args.blind_outputs) if args.blind_outputs else None
    if outputs_dir is not None and not outputs_dir.is_absolute():
        outputs_dir = ROOT / outputs_dir
    scores = [score_blind_eval(case, outputs_dir) for case in blind_cases] if outputs_dir else None

    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "blind_eval": summarize_blind_eval(blind_cases, scores),
            "frozen_replay": {"total": len(frozen_cases)},
        },
        "cases": {
            "blind_eval": [str(case.get("id")) for case in blind_cases],
            "frozen_replay": [str(case.get("id")) for case in frozen_cases],
        },
        "errors": blind_failures + frozen_failures,
    }

    invalid: dict[str, list[str]] = {}
    try:
        if args.cases:
            case_path = Path(args.cases)
            if not case_path.is_absolute():
                case_path = ROOT / case_path
            add_corpus_summary(payload, "closed_loop", case_path, invalid)
        elif args.include_closed_loop:
            add_corpus_summary(payload, "closed_loop", DEFAULT_RECORDS, invalid)
        if args.include_synthetic:
            add_corpus_summary(payload, "synthetic_closures", DEFAULT_SYNTHETIC, invalid)
    except FileNotFoundError as exc:
        print(f"REGRESSION RUN FAILED: cases path not found: {exc}", file=sys.stderr)
        return 3

    if args.list_cases:
        for case_id in payload["cases"]["blind_eval"]:
            print(f"{case_id}\tblind_eval")
        for case_id in payload["cases"]["frozen_replay"]:
            print(f"{case_id}\tfrozen_replay")
        for key in ["closed_loop", "synthetic_closures"]:
            for case in payload["cases"].get(key, []):
                print(f"{case['id']}\t{key}\t{case['result']}\t{case['path']}")

    if args.validate_cases and (payload["errors"] or invalid):
        print("REGRESSION SIGNAL VALIDATION FAILED")
        for error in payload["errors"]:
            print(f"- {error}")
        for case_id, errors in invalid.items():
            for error in errors:
                print(f"- {case_id}: {error}")
        return 3

    baseline = load_baseline(Path(args.baseline)) if args.baseline else None
    write_outputs(
        payload=payload,
        baseline=baseline,
        md_path=Path(args.output) if args.output else None,
        json_path=Path(args.json) if args.json else None,
    )

    if payload["errors"]:
        print(
            f"REGRESSION SIGNAL WARNINGS: {len(payload['errors'])} manifest issues",
            file=sys.stderr,
        )

    blind = payload["summary"]["blind_eval"]
    if blind["hit_rate"] is not None and blind["hit_rate"] < args.fail_under:
        print(
            f"REGRESSION RUN FAILED: blind hit rate {blind['hit_rate']:.3f} "
            f"< fail-under {args.fail_under:.3f}",
            file=sys.stderr,
        )
        return 1

    for key in ["closed_loop", "synthetic_closures"]:
        summary = payload["summary"].get(key)
        if summary and summary["blocked_rate"] > args.max_blocked_pct:
            print(
                f"REGRESSION RUN FAILED: {key} blocked rate {summary['blocked_rate']:.3f} "
                f"> max {args.max_blocked_pct:.3f}",
                file=sys.stderr,
            )
            return 2

    hit_rate = pct(blind["hit_rate"])
    print(
        "REGRESSION SIGNAL REPORT PASSED: "
        f"blind_eval={blind['total']} cases, frozen_replay={len(frozen_cases)} cases, "
        f"blind_hit_rate={hit_rate}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
