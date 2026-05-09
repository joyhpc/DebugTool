#!/usr/bin/env python3
"""
Offline markdown output validator for Debug Decision Tree Skill.

Scope for V0.96:
- validate required mode headings
- validate Node Explanation Table schema and row-level fields
- validate action node safety/cost/reversibility metadata
- validate S2/S3 node rows contain explicit safety language
- validate Mermaid decision-tree node IDs match the node table IDs

Usage:
  python scripts/output_validator.py --mode input_cleaning --file cleaned.md
  python scripts/output_validator.py --mode standard --file output.md
  python scripts/output_validator.py --mode knowledge_linked --file output.md
  python scripts/output_validator.py --mode fast_path --file output.md
  python scripts/output_validator.py --mode architecture_first --file output.md
  python scripts/output_validator.py --mode assumption_driven --file output.md
  python scripts/output_validator.py --mode evidence_audit --file audit.md
  python scripts/output_validator.py --mode skill_improvement --file review.md
  python scripts/output_validator.py --mode retrospective --file output.md

This is a structural validator, not an LLM quality judge. It cannot determine
whether the debug reasoning is correct; it catches contract drift, common unsafe wording, and unsafe or
incomplete output structure before a generated answer is reused as an asset.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import sys
from typing import Iterable

MODE_HEADINGS = {
    "input_cleaning": [
        "Raw Input Boundary", "Entity / Alias Normalization",
        "Observed / Confirmed Facts", "Judgments / Inferences / Hypotheses",
        "Actions Already Tried And Results", "Proposed Methods / Pending Actions",
        "Contradictions / Revisions", "Missing Information",
        "Router-Ready Case Brief",
    ],
    "standard": [
        "Problem Summary", "Input Cleaning Snapshot", "Context Mode", "Safety Gate",
        "Working Link Model / Scope", "Fact / Assumption Table",
        "Hypothesis Ranking", "Candidate Matching Report",
        "Adopted / Deferred / Not Applied", "Cost / Probability Ranking",
        "Optimal Troubleshooting Path", "Decision Tree", "Node Explanation Table",
        "Missing Information", "Next 3-5 Actions",
        "Stop / Escalation Conditions", "Retrospective Trigger",
    ],
    "knowledge_linked": [
        "Retrieval Summary", "Fact Table", "Project Context Model",
        "Fault-Domain Localization", "Candidate Matching Report",
        "Adopted / Deferred / Not Applied", "Optimal Troubleshooting Path",
        "Decision Tree", "Node Explanation Table", "Missing / Contradictory Context",
        "Next 3-5 Actions", "Stop / Escalation Conditions", "Retrospective Trigger",
    ],
    "fast_path": [
        "Mode / Signature / Confidence", "Safety Gate", "Quick Diagnosis",
        "Minimal Context Still Needed", "Top 3-5 Actions",
        "Stop / Escalate Conditions", "Mini Decision Tree",
        "Why Full Architecture Is Not Needed Yet", "When To Switch Modes",
    ],
    "architecture_first": [
        "Project Context Summary", "Input Cleaning Snapshot",
        "Architecture / Link Understanding", "Evidence-Aware Link Model",
        "Fact / Assumption Table", "Fault-Domain Localization",
        "Hypothesis Tree With Probabilities", "Candidate Matching Report",
        "Adopted / Deferred / Not Applied", "Cost / Probability Ranking",
        "Optimal Troubleshooting Path", "Decision Tree", "Node Explanation Table",
        "Missing Architecture Information", "Next 3-5 Actions",
        "Stop / Escalation Conditions", "Retrospective Trigger",
    ],
    "assumption_driven": [
        "Context Mode", "Proposed Link Model / Classic Architecture",
        "Assumptions To Confirm", "Fault Domains If Assumptions Hold",
        "Provisional Optimal Path", "Provisional Decision Tree",
        "What Would Change The Tree", "Next User Confirmation",
    ],
    "evidence_audit": [
        "Artifact Under Review", "Review Verdict", "Contract Compliance",
        "Evidence Integrity Findings", "Link Model Findings",
        "Probability And Ranking Findings", "Action Tree Findings",
        "Missing Or Overclaimed Information", "Required Fixes Before Publish",
        "Reviewer Decision",
    ],
    "skill_improvement": [
        "Improvement Objective", "Triggering Example Or Failure",
        "Skill Layer Diagnosis", "Target-Case Uncertainty vs Skill Defect",
        "Required Contract / Routing / Lifecycle Changes",
        "Regression Coverage To Add Or Update", "Changes Made",
        "Validation", "Residual Risks", "Next Skill Backlog",
    ],
    "retrospective": [
        "Root Cause Summary", "Effective Fix", "Strong Indicators",
        "Misleading / Low-Value Paths", "Case Record Draft",
        "Asset Update Proposal", "Regression Test Proposal",
        "Skill-Level Learning Proposal", "Promotion Recommendation",
    ],
}

MODES_REQUIRING_NODE_TABLE = {"standard", "knowledge_linked", "architecture_first"}
MODES_WITH_DECISION_TREE = {
    "standard", "knowledge_linked", "architecture_first",
    "fast_path", "assumption_driven",
}

DECISION_TREE_SECTION_BY_MODE = {
    "standard": "Decision Tree",
    "knowledge_linked": "Decision Tree",
    "architecture_first": "Decision Tree",
    "fast_path": "Mini Decision Tree",
    "assumption_driven": "Provisional Decision Tree",
}

REQUIRED_NODE_COLUMNS = [
    "id", "type", "action_type", "check_or_action", "tool_required",
    "expected_observation", "interpretation", "safety_level", "cost",
    "reversibility", "next_branch", "evidence_refs",
]

VALID_TYPE = {"decision", "action", "gate", "terminal"}
VALID_ACTION_TYPE = {
    "observe", "isolate", "perturb", "replace", "reconfigure",
    "reproduce", "rollback", "none", "n/a", "na", "-", "",
}
VALID_ACTION_ONLY_ACTION_TYPE = {
    "observe", "isolate", "perturb", "replace", "reconfigure", "reproduce", "rollback",
}
VALID_SAFETY_LEVEL = {"S0", "S1", "S2", "S3"}
VALID_COST = {"low", "medium", "high"}
VALID_REVERSIBILITY = {"reversible", "partial", "irreversible", "n/a", "na", "-", ""}
VALID_ACTION_ONLY_REVERSIBILITY = {"reversible", "partial", "irreversible"}
VALID_CONFIDENCE = {"high", "medium", "low"}
VALID_STALENESS = {"fresh", "requires_re_verification", "archived"}
VALID_EVIDENCE_AUDIT_VERDICTS = {"pass", "pass_with_minor_fixes", "needs_revision", "reject"}
VALID_PUBLISH_READY = {"yes", "no"}

SKILL_LAYER_KEYWORDS = {
    "intake", "routing", "route", "link_model_contract", "link model",
    "output_contract", "output contract", "evidence_audit", "evidence audit",
    "artifact_lifecycle", "artifact lifecycle", "lifecycle", "validator",
    "regression", "asset_coverage", "asset coverage",
}

INPUT_CLEANING_TABLES = [
    ("Observed / Confirmed Facts", ["id", "fact", "source_in_input", "confidence", "staleness", "affected_link_or_node"]),
    ("Judgments / Inferences / Hypotheses", ["id", "statement", "based_on", "confidence", "could_be_wrong_if"]),
    ("Actions Already Tried And Results", ["id", "action", "target", "result", "interpretation", "evidence_refs"]),
    ("Proposed Methods / Pending Actions", ["id", "proposed_action", "owner_if_known", "target", "expected_evidence", "hypothesis_or_link_node"]),
    ("Contradictions / Revisions", ["id", "previous_statement", "revised_statement", "why_revised", "impact_on_routing"]),
]

SAFETY_WORDS = {
    # Explicit warning / mitigation terms. Do not include bare hazard names like
    # "high voltage" because merely naming a hazard is not enough for an S2/S3 node.
    "warning", "caution", "hazard", "risk", "safe", "safety", "limit", "isolate",
    "disable", "de-energize", "deenergize", "current-limit", "current limit", "ppe",
    "e-stop", "fuse", "thermal limit", "destructive", "do not", "stop",
    "安全", "风险", "危险", "警告", "注意", "限流", "隔离", "断电", "防护", "禁止", "停止",
}

NODE_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")

FORBIDDEN_UNSAFE_PATTERNS = [
    (re.compile(r"(?:repeat\s+)?full[-\s]?power\s+hot[-\s]?plug(?:\s+reproduction)?", re.I), "unbounded full-power hot-plug reproduction"),
    (re.compile(r"bypass\s+(?:the\s+)?(?:fuse|efuse|current\s*limit|protection)", re.I), "bypassing protection/current limit"),
    (re.compile(r"short\s+(?:pg|fault|enable|en)\s+(?:to|high|low)", re.I), "forcing control/status pins without constraints"),
    (re.compile(r"remove\s+(?:the\s+)?current\s*limit", re.I), "removing current limit on an unsafe power fault"),
    (re.compile(r"无限流|取消限流|旁路(?:保险|保护|限流)|直接短接", re.I), "unsafe Chinese power-debug phrase"),
]

UNSAFE_MITIGATION_TERMS = [
    "do not", "must not", "never", "avoid", "stop", "not applied",
    "forbidden", "prohibited", "blocked", "instead",
    "current-limited", "current limited", "safe envelope", "precharge",
    "fuse-protected", "fused", "efuse", "e-fuse",
    "不要", "禁止", "停止", "避免", "限流", "安全边界", "安全包络",
]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


@dataclass
class MarkdownTable:
    start_line: int
    lines: list[str]
    columns: list[str]
    rows: list[dict[str, str]]


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]


def normalize_text(value: str) -> str:
    value = value.strip().strip("`").strip()
    value = value.replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")
    return value


def contains_any(text: str, needles: Iterable[str]) -> bool:
    haystack = text.lower()
    return any(needle.lower() in haystack for needle in needles)


def normalize_col(value: str) -> str:
    value = normalize_text(value).lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def split_md_row(line: str) -> list[str]:
    # Good enough for schema-level validation; escaped pipes are not expected
    # in contract tables.
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def is_separator_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and bool(re.fullmatch(r"[|:\-\s]+", stripped))


def heading_matches(raw_heading: str, expected: str) -> bool:
    # Allows headings like "## 8. Node Explanation Table" and exact headings.
    # Do not use suffix matching: "# Debug Decision Tree" must not satisfy
    # the required section heading "Decision Tree".
    heading = re.sub(r"^\d+[.)]?\s*", "", raw_heading.strip())
    return heading == expected


def find_heading_positions(text: str) -> list[tuple[int, int, str]]:
    positions: list[tuple[int, int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        m = HEADING_RE.match(line)
        if m:
            positions.append((line_no, len(m.group(1)), m.group(2).strip()))
    return positions


def find_heading(text: str, expected: str) -> tuple[int, str] | None:
    for line_no, _level, raw in find_heading_positions(text):
        if heading_matches(raw, expected):
            return line_no, raw
    return None


def extract_section(text: str, expected: str) -> str:
    """Return markdown between the expected heading and the next same/higher heading."""
    lines = text.splitlines()
    positions = find_heading_positions(text)
    for idx, (line_no, level, raw) in enumerate(positions):
        if not heading_matches(raw, expected):
            continue
        start_idx = line_no
        end_idx = len(lines)
        for next_line_no, next_level, _next_raw in positions[idx + 1 :]:
            if next_level <= level:
                end_idx = next_line_no - 1
                break
        return "\n".join(lines[start_idx:end_idx]).strip()
    return ""


def validate_required_headings(text: str, mode: str, errors: list[str]) -> None:
    positions: list[int] = []
    for heading in MODE_HEADINGS[mode]:
        found = find_heading(text, heading)
        if not found:
            errors.append(f"missing heading: {heading}")
        else:
            positions.append(found[0])

    if len(positions) == len(MODE_HEADINGS[mode]) and positions != sorted(positions):
        errors.append("required headings are present but out of contract order")


def find_table_with_columns(text: str, required_columns: list[str]) -> MarkdownTable | None:
    required = {normalize_col(c) for c in required_columns}
    for table in find_tables(text):
        if required.issubset(set(table.columns)):
            return table
    return None


def find_tables(text: str) -> list[MarkdownTable]:
    tables: list[MarkdownTable] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if lines[i].strip().startswith("|") and is_separator_row(lines[i + 1]):
            start = i
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            raw_table = lines[start:j]
            columns = [normalize_col(c) for c in split_md_row(raw_table[0])]
            rows: list[dict[str, str]] = []
            for raw in raw_table[2:]:
                cells = split_md_row(raw)
                if len(cells) < len(columns):
                    cells += [""] * (len(columns) - len(cells))
                if len(cells) > len(columns):
                    cells = cells[: len(columns) - 1] + [" | ".join(cells[len(columns) - 1 :])]
                rows.append(dict(zip(columns, cells)))
            tables.append(MarkdownTable(start_line=start + 1, lines=raw_table, columns=columns, rows=rows))
            i = j
        else:
            i += 1
    return tables


def find_node_table(text: str) -> MarkdownTable | None:
    tables = find_tables(text)
    best: MarkdownTable | None = None
    best_score = 0
    for table in tables:
        cols = set(table.columns)
        score = len(cols.intersection(REQUIRED_NODE_COLUMNS))
        if {"id", "safety_level"}.issubset(cols) and score > best_score:
            best = table
            best_score = score
    return best


def is_blank_like(value: str) -> bool:
    return normalize_text(value).lower() in {"", "-", "n/a", "na", "none", "null"}


def validate_enum(value: str, allowed: set[str], field: str, row_id: str, errors: list[str], *, case_sensitive: bool = False) -> None:
    cleaned = normalize_text(value)
    candidate = cleaned if case_sensitive else cleaned.lower()
    allowed_cmp = allowed if case_sensitive else {x.lower() for x in allowed}
    if candidate not in allowed_cmp:
        errors.append(f"node {row_id}: invalid {field} '{value}', allowed={sorted(allowed)}")


def validate_node_table(text: str, mode: str, errors: list[str], warnings: list[str]) -> tuple[set[str], MarkdownTable | None]:
    node_table = find_node_table(text)

    if not node_table:
        if mode in MODES_REQUIRING_NODE_TABLE:
            errors.append("Node Explanation Table required but no matching node table found")
        elif "Node Explanation Table" in text:
            errors.append("Node Explanation Table heading present but no matching node table found")
        return set(), None

    missing_cols = [c for c in REQUIRED_NODE_COLUMNS if c not in node_table.columns]
    if missing_cols:
        errors.append(f"node table missing columns: {missing_cols}")
        # Row-level checks need the required columns. Continue only for columns that exist.

    node_ids: set[str] = set()
    duplicate_ids: set[str] = set()

    for idx, row in enumerate(node_table.rows, start=1):
        row_id = normalize_text(row.get("id", "")) or f"row#{idx}"
        if row_id in node_ids:
            duplicate_ids.add(row_id)
        if row_id != f"row#{idx}":
            node_ids.add(row_id)

        if is_blank_like(row.get("id", "")):
            errors.append(f"node row {idx}: id is required")
            continue
        if not NODE_ID_RE.fullmatch(row_id):
            errors.append(f"node {row_id}: id must match [A-Za-z][A-Za-z0-9_-]*")

        node_type = normalize_text(row.get("type", "")).lower()
        if is_blank_like(node_type):
            errors.append(f"node {row_id}: type is required")
        else:
            validate_enum(node_type, VALID_TYPE, "type", row_id, errors)

        for required in ["check_or_action", "expected_observation", "interpretation", "safety_level", "cost", "next_branch"]:
            if required in node_table.columns and is_blank_like(row.get(required, "")):
                errors.append(f"node {row_id}: {required} is required")

        if "safety_level" in node_table.columns:
            safety_level = normalize_text(row.get("safety_level", "")).upper()
            if safety_level:
                validate_enum(safety_level, VALID_SAFETY_LEVEL, "safety_level", row_id, errors, case_sensitive=True)

        if "cost" in node_table.columns:
            validate_enum(row.get("cost", ""), VALID_COST, "cost", row_id, errors)

        if "action_type" in node_table.columns:
            action_type = normalize_text(row.get("action_type", "")).lower()
            validate_enum(action_type, VALID_ACTION_TYPE, "action_type", row_id, errors)
            if node_type == "action" and action_type not in VALID_ACTION_ONLY_ACTION_TYPE:
                errors.append(f"node {row_id}: action node requires action_type in {sorted(VALID_ACTION_ONLY_ACTION_TYPE)}")

        if "reversibility" in node_table.columns:
            reversibility = normalize_text(row.get("reversibility", "")).lower()
            validate_enum(reversibility, VALID_REVERSIBILITY, "reversibility", row_id, errors)
            if node_type == "action" and reversibility not in VALID_ACTION_ONLY_REVERSIBILITY:
                errors.append(f"node {row_id}: action node requires reversibility in {sorted(VALID_ACTION_ONLY_REVERSIBILITY)}")

        if node_type in {"action", "gate"} and "tool_required" in node_table.columns:
            if is_blank_like(row.get("tool_required", "")):
                errors.append(f"node {row_id}: {node_type} node requires tool_required")

        safety_level = normalize_text(row.get("safety_level", "")).upper()
        if safety_level in {"S2", "S3"}:
            combined = " ".join(row.values()).lower()
            if not any(word.lower() in combined for word in SAFETY_WORDS):
                errors.append(f"node {row_id}: {safety_level} node must contain explicit safety warning/mitigation language")

    if duplicate_ids:
        errors.append(f"duplicate node ids: {sorted(duplicate_ids)}")

    if not node_ids:
        warnings.append("node table found but contains no node rows")

    return node_ids, node_table


def fenced_code_blocks(text: str, language: str | None = None) -> list[str]:
    pattern = re.compile(r"```([^\n`]*)\n(.*?)```", re.S)
    blocks: list[str] = []
    for m in pattern.finditer(text):
        lang = m.group(1).strip().lower()
        if language is None or lang == language.lower():
            blocks.append(m.group(2))
    return blocks


def mermaid_node_ids(block: str) -> set[str]:
    ids: set[str] = set()
    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("%%"):
            continue
        if re.match(r"^(flowchart|graph|sequenceDiagram|stateDiagram|classDiagram|subgraph|end)\b", line, re.I):
            continue

        # Node declarations: A1[...], D1{...}, T1((...)), G1>...]
        decl = re.match(r"^([A-Za-z][A-Za-z0-9_-]*)\s*(?:\[|\{|\(|>)", line)
        if decl:
            ids.add(decl.group(1))

        # Edge left side: A1 --> B1, A1 -- pass --> B1, A1 -->|pass| B1
        edge_left = re.match(r"^([A-Za-z][A-Za-z0-9_-]*)\s*(?:-->|---|==>|-.->|--)", line)
        if edge_left:
            ids.add(edge_left.group(1))

        # Edge right side. Strip labels and grab the first node-like token after the arrow.
        if any(arrow in line for arrow in ["-->", "---", "==>", "-.->", "--"]):
            rhs = re.split(r"-->|---|==>|-\.->|--", line, maxsplit=1)[-1].strip()
            rhs = re.sub(r"^\|.*?\|", "", rhs).strip()
            rhs_node = re.match(r"^([A-Za-z][A-Za-z0-9_-]*)", rhs)
            if rhs_node:
                ids.add(rhs_node.group(1))
    return ids


def validate_mermaid_consistency(text: str, mode: str, node_ids: set[str], errors: list[str], warnings: list[str]) -> None:
    if mode not in MODES_WITH_DECISION_TREE:
        return

    section_name = DECISION_TREE_SECTION_BY_MODE.get(mode)
    tree_text = extract_section(text, section_name) if section_name else text
    blocks = fenced_code_blocks(tree_text, "mermaid")
    if not blocks:
        errors.append(f"{section_name or 'decision tree'} section requires a fenced ```mermaid block")
        return

    tree_ids: set[str] = set()
    for block in blocks:
        tree_ids.update(mermaid_node_ids(block))

    if not tree_ids:
        errors.append("mermaid decision tree contains no parseable node ids")
        return

    if node_ids:
        missing_in_table = sorted(tree_ids - node_ids)
        missing_in_tree = sorted(node_ids - tree_ids)
        if missing_in_table:
            errors.append(f"mermaid node ids missing from node table: {missing_in_table}")
        if missing_in_tree:
            errors.append(f"node table ids missing from mermaid decision tree: {missing_in_tree}")
    else:
        warnings.append("mermaid decision tree found but no node table is available for id consistency check")


def validate_case_record_draft(text: str, mode: str, errors: list[str]) -> None:
    if mode != "retrospective":
        return
    blocks = fenced_code_blocks(text, "yaml") + fenced_code_blocks(text, "yml")
    if not blocks:
        errors.append("retrospective output requires a fenced YAML Case Record Draft")
        return
    joined = "\n".join(blocks)
    for token in ["asset_type:", "case_record"]:
        if token not in joined:
            errors.append(f"case record draft missing token: {token}")


def validate_input_cleaning_contract(text: str, mode: str, errors: list[str]) -> None:
    if mode != "input_cleaning":
        return

    for heading, required_columns in INPUT_CLEANING_TABLES:
        section = extract_section(text, heading)
        table = find_table_with_columns(section, required_columns)
        if not table:
            errors.append(f"input cleaning section '{heading}' missing required table columns: {required_columns}")
            continue
        if not table.rows:
            errors.append(f"input cleaning section '{heading}' table must contain at least one explicit row")
            continue

        for idx, row in enumerate(table.rows, start=1):
            row_id = normalize_text(row.get("id", ""))
            if is_blank_like(row_id):
                errors.append(f"input cleaning section '{heading}' row {idx}: id is required")
            if "confidence" in table.columns:
                confidence = normalize_text(row.get("confidence", "")).lower()
                if confidence not in VALID_CONFIDENCE:
                    errors.append(
                        f"input cleaning section '{heading}' row {row_id or idx}: "
                        f"invalid confidence '{row.get('confidence', '')}'"
                    )
            if heading == "Observed / Confirmed Facts" and "staleness" in table.columns:
                staleness = normalize_text(row.get("staleness", "")).lower()
                if staleness not in VALID_STALENESS:
                    errors.append(
                        f"input cleaning section '{heading}' row {row_id or idx}: "
                        f"invalid staleness '{row.get('staleness', '')}', "
                        f"allowed={sorted(VALID_STALENESS)}"
                    )

            for column in required_columns:
                if is_blank_like(row.get(normalize_col(column), "")):
                    errors.append(f"input cleaning section '{heading}' row {row_id or idx}: {column} is required")

    for heading in ["Raw Input Boundary", "Entity / Alias Normalization", "Missing Information", "Router-Ready Case Brief"]:
        section = extract_section(text, heading)
        if len(re.sub(r"\s+", " ", section).strip()) < 20:
            errors.append(f"input cleaning section '{heading}' must contain useful content")


def validate_forbidden_unsafe_patterns(text: str, errors: list[str]) -> None:
    for pattern, description in FORBIDDEN_UNSAFE_PATTERNS:
        for match in pattern.finditer(text):
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_end = text.find("\n", match.end())
            if line_end == -1:
                line_end = len(text)
            context = text[line_start:line_end].lower()
            mitigated = any(token.lower() in context for token in UNSAFE_MITIGATION_TERMS)
            if not mitigated:
                errors.append(f"unsafe instruction appears without local mitigation: {description}")


def parse_probability_value(raw: str) -> float | None:
    cleaned = normalize_text(raw).lower()
    match = re.search(r"([0-9]+(?:\.[0-9]+)?)", cleaned)
    if not match:
        return None
    value = float(match.group(1))
    if "%" in cleaned or "percent" in cleaned or value > 1:
        value /= 100
    return value


def find_model_gap_probability(text: str) -> float | None:
    for table in find_tables(text):
        for row in table.rows:
            combined = " ".join(row.values())
            if not contains_any(combined, ["unknown / model gap", "unknown/model gap", "model gap", "模型缺口"]):
                continue
            for column, value in row.items():
                if "prob" in column or column in {"p", "probability"}:
                    parsed = parse_probability_value(value)
                    if parsed is not None:
                        return parsed
            # Fall back to scanning the row when the table uses a localized
            # probability column name that does not normalize to "prob".
            parsed = parse_probability_value(combined)
            if parsed is not None:
                return parsed
    return None


def validate_boundary_mechanism_tables(hypothesis_text: str, errors: list[str]) -> None:
    boundary_table = find_table_with_columns(hypothesis_text, ["id", "type", "first_fail_boundary", "p"])
    if not boundary_table:
        errors.append("architecture_first output must include a Boundary Distribution table with id, type, first_fail_boundary, and p columns")
    else:
        total = 0.0
        found_probability = False
        for idx, row in enumerate(boundary_table.rows, start=1):
            row_id = normalize_text(row.get("id", "")) or f"row#{idx}"
            row_type = normalize_text(row.get("type", "")).lower()
            if row_type != "boundary":
                errors.append(f"boundary row {row_id}: type must be boundary")
            probability = parse_probability_value(row.get("p", ""))
            if probability is None:
                errors.append(f"boundary row {row_id}: p must be a probability")
            else:
                found_probability = True
                total += probability
        if found_probability and abs(total - 1.0) > 0.02:
            errors.append(f"Boundary Distribution probabilities must sum to 1.00 ± 0.02, got {total:.3f}")

    mechanism_table = find_table_with_columns(hypothesis_text, ["id", "type", "mechanism", "p_active", "affects_boundaries"])
    if not mechanism_table:
        errors.append("architecture_first output must include a Mechanism Prior table with id, type, mechanism, p_active, and affects_boundaries columns")
    else:
        valid_types = {"mechanism", "observability_gap"}
        for idx, row in enumerate(mechanism_table.rows, start=1):
            row_id = normalize_text(row.get("id", "")) or f"row#{idx}"
            row_type = normalize_text(row.get("type", "")).lower()
            if row_type not in valid_types:
                errors.append(f"mechanism row {row_id}: type must be one of {sorted(valid_types)}")
            if parse_probability_value(row.get("p_active", "")) is None:
                errors.append(f"mechanism row {row_id}: p_active must be a probability")

    if not contains_any(hypothesis_text, ["Coverage Matrix", "coverage matrix", "覆盖矩阵"]):
        errors.append("architecture_first output must include a Coverage Matrix for mechanism-to-boundary likelihood")

    if not find_table_with_columns(hypothesis_text, ["evidence", "status", "affects"]):
        errors.append("architecture_first output must include an Evidence Ledger table with evidence, status, and affects columns")


def validate_cost_ranking_table(cost_text: str, errors: list[str]) -> None:
    required_columns = ["tier", "co_acquisition", "boundary_subset", "mechanism_subset", "p_hit", "p_exclude", "time_min"]
    cost_table = find_table_with_columns(cost_text, required_columns)
    if not cost_table:
        errors.append(
            "Cost / Probability Ranking must include a table with tier, co_acquisition, "
            "boundary_subset, mechanism_subset, p_hit, p_exclude, and time_min columns"
        )
        return

    for idx, row in enumerate(cost_table.rows, start=1):
        row_id = normalize_text(row.get("action_id", "") or row.get("node", "")) or f"row#{idx}"
        co_acquisition = normalize_text(row.get("co_acquisition", "")).lower()
        if co_acquisition not in {"true", "false", "yes", "no"}:
            errors.append(f"cost row {row_id}: co_acquisition must be true/false or yes/no")


def validate_architecture_first_semantics(text: str, mode: str, errors: list[str]) -> None:
    if mode != "architecture_first":
        return

    hypothesis_text = "\n".join(
        [
            extract_section(text, "Fault-Domain Localization"),
            extract_section(text, "Hypothesis Tree With Probabilities"),
        ]
    )
    validate_boundary_mechanism_tables(hypothesis_text, errors)

    if not contains_any(hypothesis_text, ["unknown / model gap", "unknown/model gap", "model gap", "模型缺口"]):
        errors.append("architecture_first output must include an explicit unknown / model gap hypothesis")
    else:
        model_gap_probability = find_model_gap_probability(hypothesis_text)
        if model_gap_probability is None:
            errors.append("architecture_first unknown / model gap hypothesis must include a probability")
        elif model_gap_probability < 0.02:
            errors.append("architecture_first unknown / model gap probability must be at least 0.02")

    if not contains_any(hypothesis_text, ["direct symptom", "simplest physical", "直接物理症状", "最简解释"]):
        errors.append("architecture_first output must explicitly justify direct-symptom simplest-interpretation ranking")
    if not contains_any(hypothesis_text, ["top two", "top-2", "top 2", "前二", "前两"]):
        errors.append("architecture_first output must state that the direct-symptom explanation is in the top two or explain demotion")

    cost_text = extract_section(text, "Cost / Probability Ranking")
    if not contains_any(cost_text, ["cost_priors.yaml", "cost prior", "local override", "成本先验", "本地覆盖"]):
        errors.append("Cost / Probability Ranking must cite cost_priors.yaml or a stated local override")
    validate_cost_ranking_table(cost_text, errors)

    for table in find_tables(text):
        columns = set(table.columns)
        if "owner" in columns and "candidate_owner" not in columns:
            errors.append("owner action tables must use candidate_owner instead of confirmed owner unless explicit assignment exists")
        if "candidate_owner" in columns and not contains_any(
            text,
            ["PM", "project lead", "项目负责人", "正式", "confirm", "确认"],
        ):
            errors.append("candidate_owner tables must state that PM/project lead confirmation is required")


def parse_key_value(section: str, key: str) -> str | None:
    pattern = re.compile(rf"(?im)^\s*{re.escape(key)}\s*:\s*([A-Za-z0-9_\-]+)\s*$")
    match = pattern.search(section)
    if not match:
        return None
    return normalize_text(match.group(1)).lower()


def validate_evidence_audit_contract(text: str, mode: str, errors: list[str]) -> None:
    if mode != "evidence_audit":
        return

    verdict_text = extract_section(text, "Review Verdict")
    if not contains_any(verdict_text, VALID_EVIDENCE_AUDIT_VERDICTS):
        errors.append(f"Review Verdict must include one of {sorted(VALID_EVIDENCE_AUDIT_VERDICTS)}")

    reviewer_decision = extract_section(text, "Reviewer Decision")
    decision = parse_key_value(reviewer_decision, "decision")
    publish_ready = parse_key_value(reviewer_decision, "publish_ready")
    if decision is None:
        errors.append("Reviewer Decision must include 'decision: ...'")
    elif decision not in VALID_EVIDENCE_AUDIT_VERDICTS:
        errors.append(f"Reviewer Decision has invalid decision '{decision}', allowed={sorted(VALID_EVIDENCE_AUDIT_VERDICTS)}")
    if publish_ready is None:
        errors.append("Reviewer Decision must include 'publish_ready: yes|no'")
    elif publish_ready not in VALID_PUBLISH_READY:
        errors.append(f"Reviewer Decision has invalid publish_ready '{publish_ready}', allowed={sorted(VALID_PUBLISH_READY)}")
    for required_key in ["required_fixes", "residual_risk"]:
        if not re.search(rf"(?im)^\s*{required_key}\s*:", reviewer_decision):
            errors.append(f"Reviewer Decision must include '{required_key}: ...'")

    semantic_checks = [
        ("fact vs inference split", ["fact", "inference", "事实", "推断"]),
        ("stale or non-same-interval evidence", ["stale", "staleness", "requires_re_verification", "非同故障窗口", "过期证据"]),
        ("direct symptom top-two ranking", ["direct symptom", "simplest physical", "top two", "top-2", "直接物理症状", "最简解释"]),
        ("boundary vs mechanism separation", ["boundary", "mechanism", "observability_gap", "边界", "机制", "观测缺口"]),
        ("unknown / model gap branch", ["unknown / model gap", "unknown/model gap", "model gap", "模型缺口"]),
        ("cost prior calibration", ["cost_priors.yaml", "cost prior", "成本先验", "local override"]),
        ("candidate owner vs assignment", ["candidate owner", "candidate_owner", "候选 owner", "正式分配", "PM"]),
    ]
    for label, tokens in semantic_checks:
        if not contains_any(text, tokens):
            errors.append(f"Evidence Audit must explicitly cover semantic check: {label}")


def validate_skill_improvement_contract(text: str, mode: str, errors: list[str]) -> None:
    if mode != "skill_improvement":
        return

    diagnosis = extract_section(text, "Skill Layer Diagnosis")
    if not contains_any(diagnosis, SKILL_LAYER_KEYWORDS):
        errors.append("Skill Layer Diagnosis must name at least one recognized skill layer")

    uncertainty_vs_defect = extract_section(text, "Target-Case Uncertainty vs Skill Defect")
    if not contains_any(uncertainty_vs_defect, ["target-case uncertainty", "target case uncertainty", "目标 case", "目标案例", "目标案"]):
        errors.append("Target-Case Uncertainty vs Skill Defect must explicitly state target-case uncertainty")
    if not contains_any(uncertainty_vs_defect, ["skill defect", "skill-design defect", "skill 缺陷", "工具缺陷", "机制缺陷"]):
        errors.append("Target-Case Uncertainty vs Skill Defect must explicitly state the skill defect")

    durable_change_text = "\n".join(
        [
            extract_section(text, "Required Contract / Routing / Lifecycle Changes"),
            extract_section(text, "Changes Made"),
        ]
    )
    if not contains_any(
        durable_change_text,
        ["routing", "route", "contract", "prompt", "lifecycle", "validator", "regression", "fixture", "asset"],
    ):
        errors.append("Skill Improvement review must identify at least one durable artifact class or explain why none changed")


def validate_text(text: str, mode: str) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    validate_required_headings(text, mode, errors)
    validate_input_cleaning_contract(text, mode, errors)
    node_ids, _node_table = validate_node_table(text, mode, errors, warnings)
    validate_mermaid_consistency(text, mode, node_ids, errors, warnings)
    validate_case_record_draft(text, mode, errors)
    validate_architecture_first_semantics(text, mode, errors)
    validate_evidence_audit_contract(text, mode, errors)
    validate_skill_improvement_contract(text, mode, errors)
    validate_forbidden_unsafe_patterns(text, errors)

    return ValidationResult(errors=errors, warnings=warnings)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate generated debug markdown against output contracts.")
    ap.add_argument("--mode", required=True, choices=sorted(MODE_HEADINGS))
    ap.add_argument("--file", required=True, help="Markdown file to validate")
    ap.add_argument("--quiet", action="store_true", help="Only print failures")
    ap.add_argument("--strict", action="store_true", help="Treat warnings as validation failures")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"OUTPUT VALIDATION FAILED\n- file not found: {path}", file=sys.stderr)
        return 2

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"OUTPUT VALIDATION FAILED\n- could not read file: {path}: {exc}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        print(f"OUTPUT VALIDATION FAILED\n- file is not valid UTF-8: {path}: {exc}", file=sys.stderr)
        return 2

    result = validate_text(text, args.mode)
    if args.strict and result.warnings:
        result.errors.extend(f"strict warning: {w}" for w in result.warnings)

    if result.errors:
        print("OUTPUT VALIDATION FAILED")
        for e in result.errors:
            print(f"- {e}")
        if result.warnings and not args.quiet:
            print("WARNINGS")
            for w in result.warnings:
                print(f"- {w}")
        return 1

    if not args.quiet:
        print("OUTPUT VALIDATION PASSED")
        if result.warnings:
            print("WARNINGS")
            for w in result.warnings:
                print(f"- {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
