from pathlib import Path

from scripts import lint_case_governance as cg


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_global_case_specific_leak_is_rejected(tmp_path: Path) -> None:
    write(
        tmp_path / "pilot_runs" / "case_a" / "case_config.yaml",
        "case_id: case_a\naliases:\n  - A57\n  - Redriver PWDN\n",
    )
    write(tmp_path / "output_contracts" / "generic.md", "Query A57 Redriver PWDN\n")

    messages = cg.lint_global_case_specific_leaks(tmp_path)

    assert len(messages) == 1
    assert "case-specific term leaked" in messages[0].message


def test_case_readme_must_reference_existing_current_artifacts(tmp_path: Path) -> None:
    case_dir = tmp_path / "pilot_runs" / "case_a"
    write(case_dir / "latest-input-cleaning.md", "# Latest\n")
    write(case_dir / "README.md", "# Case\n\n- `latest-input-cleaning.md`\n- `missing.md`\n")

    messages = cg.lint_case_readmes(tmp_path)

    assert [message.message for message in messages] == [
        "README references missing file `missing.md`"
    ]


def test_current_artifact_requires_stale_governance_markers(tmp_path: Path) -> None:
    case_dir = tmp_path / "pilot_runs" / "case_a"
    write(case_dir / "README.md", "# Case\n\n- `latest-architecture-first.md`\n")
    write(case_dir / "latest-architecture-first.md", "Old evidence said the chip was bad.\n")

    messages = cg.lint_current_artifact_governance(tmp_path)

    assert any("old/stale/superseded" in message.message for message in messages)


def test_candidate_owner_requires_pm_confirmation(tmp_path: Path) -> None:
    case_dir = tmp_path / "pilot_runs" / "case_a"
    write(case_dir / "README.md", "# Case\n\n- `field-action-plan.md`\n")
    write(
        case_dir / "field-action-plan.md",
        """
# Field Plan

| evidence_id | owner candidate | status |
|---|---|---|
| EV1 | lab owner | pending |
""",
    )

    messages = cg.lint_current_artifact_governance(tmp_path)

    assert any("PM/project lead confirmation" in message.message for message in messages)


def test_field_action_plan_requires_templates_and_sections(tmp_path: Path) -> None:
    case_dir = tmp_path / "pilot_runs" / "case_a"
    write(case_dir / "README.md", "# Case\n\n- `field-action-plan.md`\n")
    write(case_dir / "field-action-plan.md", "# Field Plan\n\n## Case Configuration\n")

    messages = cg.lint_field_action_plans(tmp_path)

    assert any("failure_matrix_template" in message.message for message in messages)
    assert any("Same-Window Evidence" in message.message for message in messages)
