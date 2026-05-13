#!/usr/bin/env python3
"""Summarize current case state and attention items for pilot case directories."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import lint_case_governance as governance

ROOT = Path(__file__).resolve().parents[1]
PILOT_ROOT = "pilot_runs"
CURRENT_ARTIFACT_RE = re.compile(
    r"^(latest-.+\.md|visual-architecture-brief\.md|field-action-plan\.md)$"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
DONE_STATUSES = {"done", "complete", "completed", "closed", "pass", "passed", "present", "n/a"}


@dataclass(frozen=True)
class LineItem:
    file: str
    line: int
    text: str


@dataclass(frozen=True)
class EvidenceItem:
    file: str
    line: int
    evidence_id: str
    status: str
    boundary: str
    owner: str
    capture: str


@dataclass(frozen=True)
class CaseReport:
    case_name: str
    case_path: str
    current_artifacts: list[str]
    archived_artifacts: list[str]
    visual_brief: str | None
    governance_messages: list[str]
    open_evidence: list[EvidenceItem]
    stale_or_reverify: list[LineItem]
    high_attention: list[LineItem]
    next_actions: list[LineItem]
    stop_conditions: list[LineItem]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def normalize_col(value: str) -> str:
    value = value.strip().strip("`").lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def token_pattern(token: str) -> re.Pattern[str]:
    if re.fullmatch(r"[A-Za-z_ -]+", token):
        return re.compile(rf"(?<![A-Za-z]){re.escape(token)}(?![A-Za-z])", re.I)
    return re.compile(re.escape(token), re.I)


def split_md_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and bool(re.fullmatch(r"[|:\-\s]+", stripped))


def iter_table_rows(text: str) -> list[tuple[int, dict[str, str]]]:
    rows: list[tuple[int, dict[str, str]]] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if lines[i].strip().startswith("|") and is_separator_row(lines[i + 1]):
            columns = [normalize_col(cell) for cell in split_md_row(lines[i])]
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                cells = split_md_row(lines[j])
                if len(cells) < len(columns):
                    cells += [""] * (len(columns) - len(cells))
                if len(cells) > len(columns):
                    cells = [*cells[: len(columns) - 1], " | ".join(cells[len(columns) - 1 :])]
                rows.append((j + 1, dict(zip(columns, cells, strict=True))))
                j += 1
            i = j
        else:
            i += 1
    return rows


def current_artifacts(case_dir: Path) -> list[Path]:
    return sorted(
        path for path in case_dir.glob("*.md") if CURRENT_ARTIFACT_RE.fullmatch(path.name)
    )


def archived_artifacts(case_dir: Path) -> list[Path]:
    archive_dir = case_dir / "archive"
    if not archive_dir.exists():
        return []
    return sorted(path for path in archive_dir.glob("*.md"))


def visual_brief(case_dir: Path) -> Path | None:
    path = case_dir / "visual-architecture-brief.md"
    return path if path.exists() else None


def heading_positions(text: str) -> list[tuple[int, int, str]]:
    positions: list[tuple[int, int, str]] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        match = HEADING_RE.match(line)
        if match:
            positions.append((idx, len(match.group(1)), match.group(2).strip()))
    return positions


def section_lines(text: str, heading_fragments: tuple[str, ...]) -> list[tuple[int, str]]:
    lines = text.splitlines()
    positions = heading_positions(text)
    matches: list[tuple[int, str]] = []
    lowered_fragments = tuple(fragment.lower() for fragment in heading_fragments)
    for pos_idx, (line_no, level, raw_heading) in enumerate(positions):
        if not any(fragment in raw_heading.lower() for fragment in lowered_fragments):
            continue
        end_line = len(lines) + 1
        for next_line, next_level, _next_heading in positions[pos_idx + 1 :]:
            if next_level <= level:
                end_line = next_line
                break
        for item_line_no in range(line_no + 1, end_line):
            line = lines[item_line_no - 1].strip()
            if (
                line.startswith(("-", "*"))
                or re.match(r"^\d+[.)]\s+", line)
                or line.startswith("|")
            ):
                matches.append((item_line_no, line))
    return matches


def matching_lines(
    root: Path,
    path: Path,
    patterns: list[re.Pattern[str]],
    marker_needles: list[str] | None = None,
) -> list[LineItem]:
    items: list[LineItem] = []
    text = read_text(path)
    for line_no, line in enumerate(text.splitlines(), start=1):
        if not any(pattern.search(line) for pattern in patterns):
            continue
        if marker_needles and not governance.contains_any(line, marker_needles):
            continue
        items.append(LineItem(relative(path, root), line_no, line.strip()))
    return items


def open_evidence_items(root: Path, case_dir: Path) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    field_plan = case_dir / "field-action-plan.md"
    if not field_plan.exists():
        return items
    text = read_text(field_plan)
    for line_no, row in iter_table_rows(text):
        evidence_id = row.get("evidence_id", "")
        if not evidence_id:
            continue
        status = row.get("status", "").strip() or "unknown"
        if status.lower() in DONE_STATUSES:
            continue
        owner = row.get("candidate_owner") or row.get("owner_candidate") or row.get("owner") or ""
        capture = (
            row.get("capture") or row.get("capture_method") or row.get("expected_evidence") or ""
        )
        boundary = (
            row.get("boundary") or row.get("boundary_id") or row.get("generic_boundary") or ""
        )
        items.append(
            EvidenceItem(
                file=relative(field_plan, root),
                line=line_no,
                evidence_id=evidence_id,
                status=status,
                boundary=boundary,
                owner=owner,
                capture=capture,
            )
        )
    return items


def governance_messages_for_case(root: Path, case_dir: Path) -> list[str]:
    case_path = case_dir.resolve()
    messages = []
    for message in governance.lint_all(root):
        try:
            resolved = message.path.resolve()
        except OSError:
            resolved = message.path
        if resolved == case_path or case_path in resolved.parents:
            messages.append(message.format(root))
    return messages


def build_case_report(root: Path, case_name: str, *, max_items: int = 12) -> CaseReport:
    root = root.resolve()
    case_dir = root / PILOT_ROOT / case_name
    if not case_dir.exists() or not case_dir.is_dir():
        raise FileNotFoundError(f"case directory not found: {relative(case_dir, root)}")

    current = current_artifacts(case_dir)
    stale_patterns = [token_pattern(token) for token in governance.STALE_TRIGGERS]
    attention_patterns = governance.HIGH_ATTENTION_PATTERNS
    stale_items: list[LineItem] = []
    attention_items: list[LineItem] = []
    next_actions: list[LineItem] = []
    stop_conditions: list[LineItem] = []

    for path in current:
        stale_items.extend(matching_lines(root, path, stale_patterns))
        attention_items.extend(matching_lines(root, path, attention_patterns))
        text = read_text(path)
        next_actions.extend(
            LineItem(relative(path, root), line_no, line)
            for line_no, line in section_lines(text, ("next 3-5 actions", "next actions"))
        )
        stop_conditions.extend(
            LineItem(relative(path, root), line_no, line)
            for line_no, line in section_lines(text, ("stop conditions", "stop / escalation"))
        )

    visual_brief_path = visual_brief(case_dir)

    return CaseReport(
        case_name=case_name,
        case_path=relative(case_dir, root),
        current_artifacts=[relative(path, root) for path in current],
        archived_artifacts=[relative(path, root) for path in archived_artifacts(case_dir)],
        visual_brief=relative(visual_brief_path, root) if visual_brief_path is not None else None,
        governance_messages=governance_messages_for_case(root, case_dir),
        open_evidence=open_evidence_items(root, case_dir),
        stale_or_reverify=stale_items[:max_items],
        high_attention=attention_items[:max_items],
        next_actions=next_actions[:max_items],
        stop_conditions=stop_conditions[:max_items],
    )


def list_cases(root: Path) -> list[str]:
    pilot_root = root / PILOT_ROOT
    if not pilot_root.exists():
        return []
    return sorted(path.name for path in pilot_root.iterdir() if path.is_dir())


def format_line_items(items: list[LineItem], empty: str) -> list[str]:
    if not items:
        return [f"- {empty}"]
    return [f"- {item.file}:{item.line} {item.text}" for item in items]


def format_evidence(items: list[EvidenceItem]) -> list[str]:
    if not items:
        return ["- no open evidence rows found"]
    lines: list[str] = []
    for item in items:
        owner = f" | owner: {item.owner}" if item.owner else ""
        boundary = f" | boundary: {item.boundary}" if item.boundary else ""
        capture = f" | capture: {item.capture}" if item.capture else ""
        lines.append(
            f"- {item.file}:{item.line} {item.evidence_id} [{item.status}]{boundary}{owner}{capture}"
        )
    return lines


def format_report(report: CaseReport) -> str:
    lines = [
        f"# Case Status: {report.case_name}",
        "",
        f"Case path: `{report.case_path}`",
        f"Governance: {'PASS' if not report.governance_messages else 'ISSUES'}",
        "",
        "## Current Artifacts",
        *[f"- `{artifact}`" for artifact in report.current_artifacts],
        "",
        "## Visual Architecture",
        f"- `{report.visual_brief}`" if report.visual_brief else "- missing",
        "",
        "## Open Evidence",
        *format_evidence(report.open_evidence),
        "",
        "## Stale / Reverify Attention",
        *format_line_items(report.stale_or_reverify, "none found"),
        "",
        "## High Attention Signals",
        *format_line_items(report.high_attention, "none found"),
        "",
        "## Next Actions",
        *format_line_items(report.next_actions, "none found"),
        "",
        "## Stop Conditions",
        *format_line_items(report.stop_conditions, "none found"),
    ]
    if report.governance_messages:
        lines.extend(
            [
                "",
                "## Governance Issues",
                *[f"- {message}" for message in report.governance_messages],
            ]
        )
    return "\n".join(lines)


def report_to_json(report: CaseReport) -> str:
    return json.dumps(asdict(report), ensure_ascii=False, indent=2)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize current pilot case status.")
    parser.add_argument("case", nargs="?", help="Case directory name under pilot_runs/")
    parser.add_argument("--all", action="store_true", help="Print reports for all case directories")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown text")
    parser.add_argument(
        "--max-items", type=int, default=12, help="Maximum lines per attention section"
    )
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = args.root.resolve()

    try:
        case_names = list_cases(root) if args.all else ([args.case] if args.case else [])
        if not case_names:
            available = ", ".join(list_cases(root)) or "none"
            print(
                f"CASE STATUS REPORT FAILED\n- provide a case name or --all; available cases: {available}"
            )
            return 2
        reports = [
            build_case_report(root, case_name, max_items=args.max_items) for case_name in case_names
        ]
    except (FileNotFoundError, ValueError) as exc:
        print("CASE STATUS REPORT FAILED")
        print(f"- {exc}")
        return 1

    if args.json:
        payload: Any = [asdict(report) for report in reports] if args.all else asdict(reports[0])
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(format_report(report) for report in reports))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
