#!/usr/bin/env python3
"""Generate a lightweight semantic-regression corpus report.

This is not an LLM-backed judge yet. It summarizes reviewed closed-loop records
and enforces that the corpus has the fields needed for a future blind runner.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "training" / "closed_loop" / "records"
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


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


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
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # noqa: BLE001 - report all parse/read failures as corpus errors
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


def ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def summarize(cases: list[CorpusCase]) -> dict[str, Any]:
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


def load_baseline(path: Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def delta(current: float, baseline: dict[str, Any] | None, key: str) -> str:
    if not baseline or key not in baseline.get("summary", {}):
        return "n/a"
    previous = float(baseline["summary"][key])
    return f"{(current - previous) * 100:+.1f} pt"


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def render_markdown(cases: list[CorpusCase], summary: dict[str, Any], baseline: dict[str, Any] | None) -> str:
    lines = [
        f"# Regression Corpus Report - {datetime.now(timezone.utc).isoformat()}",
        "",
        f"**Cases**: {summary['total']}",
        "",
        "This report summarizes reviewed closed-loop records. It is a corpus baseline, not an LLM-backed semantic judge.",
        "",
        "## Summary",
        "",
        "| Metric | Result | vs Baseline |",
        "|---|---:|---:|",
        f"| Hit rate | {pct(summary['hit_rate'])} | {delta(summary['hit_rate'], baseline, 'hit_rate')} |",
        f"| Near-hit rate | {pct(summary['near_hit_rate'])} | {delta(summary['near_hit_rate'], baseline, 'near_hit_rate')} |",
        f"| Miss rate | {pct(summary['miss_rate'])} | {delta(summary['miss_rate'], baseline, 'miss_rate')} |",
        f"| Blocked rate | {pct(summary['blocked_rate'])} | {delta(summary['blocked_rate'], baseline, 'blocked_rate')} |",
        f"| Records with cost model | {summary['with_cost_model']} / {summary['total']} | n/a |",
        "",
        "## By Domain",
        "",
        "| Domain | N | Hit | Near | Miss | Blocked |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for domain, counts in summary["by_domain"].items():
        n = sum(counts.values())
        lines.append(
            f"| {domain} | {n} | {counts.get('hit', 0)} | {counts.get('near_hit', 0)} | "
            f"{counts.get('miss', 0)} | {counts.get('blocked', 0)} |"
        )

    failed = [case for case in cases if case.result in {"miss", "blocked"} or case.errors]
    lines.extend(["", "## Miss / Blocked / Invalid Cases", ""])
    if not failed:
        lines.append("None.")
    else:
        for case in failed[:20]:
            lines.extend(
                [
                    f"### {case.case_id} - {case.result}",
                    f"- path: `{case.path.relative_to(ROOT)}`",
                    f"- domain: `{case.domain}`",
                    f"- actual_resolution: {case.actual_resolution or 'missing'}",
                ]
            )
            for error in case.errors:
                lines.append(f"- corpus_error: {error}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_outputs(
    cases: list[CorpusCase],
    summary: dict[str, Any],
    baseline: dict[str, Any] | None,
    md_path: Path | None,
    json_path: Path | None,
) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "cases": [
            {
                "id": case.case_id,
                "path": str(case.path.relative_to(ROOT)),
                "domain": case.domain,
                "source_type": case.source_type,
                "status": case.status,
                "result": case.result,
                "predicted_nodes": case.predicted_nodes,
                "has_cost_model": case.has_cost_model,
                "errors": case.errors,
            }
            for case in cases
        ],
    }

    if md_path:
        md_path.write_text(render_markdown(cases, summary, baseline), encoding="utf-8")
    if json_path:
        json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if not md_path and not json_path:
        print(render_markdown(cases, summary, baseline))


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize DebugTool closed-loop regression corpus.")
    parser.add_argument("--cases", default=str(DEFAULT_CASES), help="YAML file or directory of closed-loop records")
    parser.add_argument("--output", help="Markdown report path")
    parser.add_argument("--json", help="JSON report path")
    parser.add_argument("--baseline", help="Prior JSON report for metric deltas")
    parser.add_argument("--fail-under", type=float, default=0.0, help="Minimum hit rate, 0.0-1.0")
    parser.add_argument("--max-blocked-pct", type=float, default=1.0, help="Maximum blocked rate, 0.0-1.0")
    parser.add_argument("--list-cases", action="store_true", help="List case ids and results")
    parser.add_argument("--validate-cases", action="store_true", help="Only validate corpus records")
    args = parser.parse_args()

    try:
        paths = collect_case_paths(Path(args.cases))
    except FileNotFoundError as exc:
        print(f"REGRESSION RUN FAILED: cases path not found: {exc}", file=sys.stderr)
        return 3

    cases = [load_case(path) for path in paths]
    summary = summarize(cases)
    baseline = load_baseline(Path(args.baseline)) if args.baseline else None

    if args.list_cases:
        for case in cases:
            print(f"{case.case_id}\t{case.domain}\t{case.result}\t{case.path.relative_to(ROOT)}")

    invalid = {case.case_id: case.errors for case in cases if case.errors}
    if args.validate_cases and invalid:
        print("REGRESSION CORPUS VALIDATION FAILED")
        for case_id, errors in invalid.items():
            for error in errors:
                print(f"- {case_id}: {error}")
        return 3

    write_outputs(
        cases=cases,
        summary=summary,
        baseline=baseline,
        md_path=Path(args.output) if args.output else None,
        json_path=Path(args.json) if args.json else None,
    )

    if invalid:
        print(f"REGRESSION CORPUS WARNINGS: {len(invalid)} records have corpus errors", file=sys.stderr)

    if summary["blocked_rate"] > args.max_blocked_pct:
        print(
            f"REGRESSION RUN FAILED: blocked rate {summary['blocked_rate']:.3f} "
            f"> max {args.max_blocked_pct:.3f}",
            file=sys.stderr,
        )
        return 2
    if summary["hit_rate"] < args.fail_under:
        print(
            f"REGRESSION RUN FAILED: hit rate {summary['hit_rate']:.3f} "
            f"< fail-under {args.fail_under:.3f}",
            file=sys.stderr,
        )
        return 1

    print(
        "REGRESSION CORPUS REPORT PASSED: "
        f"{summary['total']} cases, hit_rate={summary['hit_rate']:.3f}, "
        f"blocked_rate={summary['blocked_rate']:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
