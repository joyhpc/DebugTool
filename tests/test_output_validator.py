from scripts import output_validator as ov


def render_node_table(row_id: str = "N1") -> str:
    values = {
        "id": row_id,
        "type": "decision",
        "action_type": "none",
        "check_or_action": "check status",
        "tool_required": "scope",
        "expected_observation": "signal is present",
        "interpretation": "link is alive",
        "safety_level": "S0",
        "cost": "low",
        "reversibility": "n/a",
        "next_branch": "T1",
        "evidence_refs": "E1",
    }
    header = "| " + " | ".join(ov.REQUIRED_NODE_COLUMNS) + " |"
    separator = "| " + " | ".join("---" for _ in ov.REQUIRED_NODE_COLUMNS) + " |"
    row = "| " + " | ".join(values[column] for column in ov.REQUIRED_NODE_COLUMNS) + " |"
    return "\n".join([header, separator, row])


def test_find_tables_pads_missing_cells_and_collapses_extra_cells() -> None:
    text = """
| ID | Safety Level | Notes |
| --- | --- | --- |
| N1 | S0 |
| N2 | S1 | alpha | beta |
"""

    tables = ov.find_tables(text)

    assert len(tables) == 1
    assert tables[0].rows[0] == {"id": "N1", "safety_level": "S0", "notes": ""}
    assert tables[0].rows[1]["notes"] == "alpha | beta"


def test_validate_node_table_reports_missing_required_columns() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    text = """
| id | safety_level |
| --- | --- |
| N1 | S0 |
"""

    node_ids, node_table = ov.validate_node_table(text, "standard", errors, warnings)

    assert node_ids == {"N1"}
    assert node_table is not None
    assert any("node table missing columns" in error for error in errors)


def test_validate_node_table_rejects_ambiguous_best_candidate_tables() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    text = "\n\n".join([render_node_table("N1"), render_node_table("N2")])

    node_ids, node_table = ov.validate_node_table(text, "standard", errors, warnings)

    assert node_ids == set()
    assert node_table is None
    assert any("ambiguous node table" in error for error in errors)


def test_mermaid_node_ids_supports_common_arrow_forms_without_label_ids() -> None:
    block = """
flowchart TD
A1[Start]
A1 -->|pass| B1[Probe]
B1 -- fail --> C1[Swap]
C1 -.-> D1((Done))
D1 --- E1
E1 ==> F1
"""

    ids = ov.mermaid_node_ids(block)

    assert ids == {"A1", "B1", "C1", "D1", "E1", "F1"}
    assert "pass" not in ids
    assert "fail" not in ids


def test_required_headings_reports_contract_order_violation() -> None:
    errors: list[str] = []
    text = "\n".join(f"## {heading}" for heading in reversed(ov.MODE_HEADINGS["fast_path"]))

    ov.validate_required_headings(text, "fast_path", errors)

    assert "required headings are present but out of contract order" in errors
