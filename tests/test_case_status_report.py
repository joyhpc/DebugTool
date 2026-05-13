from pathlib import Path

from scripts import case_status_report as csr


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_case_status_report_extracts_open_evidence_and_sections(tmp_path: Path) -> None:
    case_dir = tmp_path / "pilot_runs" / "case_a"
    write(
        case_dir / "README.md",
        """
# Case A

- `latest-architecture-first.md`
- `visual-architecture-brief.md`
- `field-action-plan.md`
""",
    )
    write(
        case_dir / "latest-architecture-first.md",
        """
# Output

Old CDR evidence is stale and requires_re_verification.

## 15. Next 3-5 Actions

1. Capture same-window receiver evidence.

## Stop / Escalation Conditions

- Stop tuning until input is proven valid.
""",
    )
    write(
        case_dir / "visual-architecture-brief.md",
        """
# Visual Brief

## Executive Frame
ok

## System Placement
```mermaid
flowchart LR
  A --> B
```

## Subsystem Architecture
```mermaid
flowchart TD
  A --> B
```

## Mode Gate
ok

## High-Signal Evidence Stack
ok

## Field Brief
stop condition
""",
    )
    write(
        case_dir / "field-action-plan.md",
        """
# Field Plan

forms/failure_matrix_template.md
forms/same_window_evidence_batch_checklist.md

## Executive Architecture Gate
ok

## Case Configuration
ok

## Failure Matrix
ok

## Same-Window Evidence

| evidence_id | boundary | capture | owner candidate | status |
|---|---|---|---|---|
| EV-P0-01 | receiver lock | CDR/comma status | lab owner | pending |

PM/project lead confirmation is required before treating owner candidates as formal assignments.

## Stop Conditions

- Stop changing config until capture is done.
""",
    )

    report = csr.build_case_report(tmp_path, "case_a")

    assert report.governance_messages == []
    assert report.open_evidence[0].evidence_id == "EV-P0-01"
    assert report.open_evidence[0].status == "pending"
    assert report.next_actions[0].text == "1. Capture same-window receiver evidence."
    assert any(
        item.text == "- Stop tuning until input is proven valid." for item in report.stop_conditions
    )
    assert any("Old CDR evidence" in item.text for item in report.stale_or_reverify)


def test_format_report_marks_governance_issues(tmp_path: Path) -> None:
    case_dir = tmp_path / "pilot_runs" / "case_a"
    write(case_dir / "README.md", "# Case A\n\n- `latest-architecture-first.md`\n")
    write(case_dir / "latest-architecture-first.md", "Old evidence says CDR failed.\n")

    report = csr.build_case_report(tmp_path, "case_a")
    rendered = csr.format_report(report)

    assert "Governance: ISSUES" in rendered
    assert "old/stale/superseded" in rendered


def test_main_lists_available_cases_when_missing_argument(tmp_path: Path, capsys) -> None:
    write(tmp_path / "pilot_runs" / "case_a" / "README.md", "# Case A\n")

    rc = csr.main(["--root", str(tmp_path)])

    output = capsys.readouterr().out
    assert rc == 2
    assert "available cases: case_a" in output
