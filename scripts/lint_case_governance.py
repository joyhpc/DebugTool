#!/usr/bin/env python3
"""Lint lifecycle governance for saved pilot/debug case artifacts."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        _reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

CASE_ROOT = "pilot_runs"
GLOBAL_SCAN_DIRS = ("forms", "output_contracts", "scripts")
GLOBAL_SCAN_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".toml"}
CURRENT_ARTIFACT_RE = re.compile(
    r"^(latest-.+\.md|visual-architecture-brief\.md|field-action-plan\.md)$"
)
CASE_REF_RE = re.compile(r"`([^`]+\.(?:md|yaml|yml|json|txt|toml))`")

STALE_TRIGGERS = [
    "stale",
    "old",
    "older",
    "previous",
    "prior",
    "earlier",
    "superseded",
    "retracted",
    "旧",
    "早期",
    "之前",
    "历史",
]
STALE_GOVERNANCE_MARKERS = [
    "staleness",
    "requires_re_verification",
    "stale state",
    "stale status",
    "stale value",
    "superseded",
    "retracted",
    "contradictions / revisions",
    "previous_statement",
    "revised_statement",
    "archive/",
    "do not use",
    "not use",
    "停止",
    "旧证据",
]

BASE_HIGH_ATTENTION_PATTERNS = [
    re.compile(r"\bhot[- ]?plug\b", re.I),
    re.compile(r"\bfuse\b|\befuse\b", re.I),
    re.compile(r"\bshort\b", re.I),
    re.compile(r"\bburn(?:s|ed|ing)?\b", re.I),
    re.compile(r"\bCDR\b", re.I),
    re.compile(r"\bcomma\b", re.I),
    re.compile(r"\bpacket[- ]?loss\b", re.I),
]
HIGH_ATTENTION_MARKERS = [
    "evidence_id",
    "evidence_refs",
    "same_window",
    "same-window",
    "staleness",
    "status",
    "next",
    "stop condition",
    "stop / escalation",
    "candidate_owner",
    "owner candidate",
    "requires_re_verification",
    "同窗口",
    "证据",
    "停止",
]

FIELD_ACTION_REQUIRED_SECTIONS = [
    ("Executive Architecture Gate",),
    ("Case Configuration",),
    ("Failure Matrix",),
    ("Same-Window Evidence", "Evidence Batch"),
    ("Stop Conditions",),
]

VISUAL_BRIEF_REQUIRED_SECTIONS = [
    "Executive Frame",
    "System Placement",
    "Subsystem Architecture",
    "Mode Gate",
    "High-Signal Evidence Stack",
    "Field Brief",
]


@dataclass(frozen=True)
class CaseGovernanceConfig:
    aliases: tuple[str, ...]
    attention_patterns: tuple[str, ...]


@dataclass(frozen=True)
class LintMessage:
    path: Path
    message: str
    line: int | None = None

    def format(self, root: Path) -> str:
        location = self.path.relative_to(root).as_posix()
        if self.line is not None:
            location = f"{location}:{self.line}"
        return f"{location}: {self.message}"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path} is not valid UTF-8: {exc}") from exc


def as_list(value: object) -> list[object]:
    return value if isinstance(value, list) else []


def literal_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(term.strip())
    if not escaped:
        escaped = r"a^"
    return re.compile(rf"(?<![A-Za-z0-9_]){escaped}(?![A-Za-z0-9_])", re.I)


def load_case_governance_configs(root: Path) -> list[CaseGovernanceConfig]:
    configs: list[CaseGovernanceConfig] = []
    for case_dir in case_directories(root):
        path = case_dir / "case_config.yaml"
        if not path.exists():
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        aliases = tuple(str(item) for item in as_list(data.get("aliases")) if str(item).strip())
        attention = tuple(
            str(item) for item in as_list(data.get("attention_patterns")) if str(item).strip()
        )
        configs.append(CaseGovernanceConfig(aliases=aliases, attention_patterns=attention))
    return configs


def case_specific_patterns(root: Path) -> list[re.Pattern[str]]:
    patterns: list[re.Pattern[str]] = []
    for config in load_case_governance_configs(root):
        patterns.extend(literal_pattern(alias) for alias in config.aliases)
    return patterns


def high_attention_patterns(root: Path) -> list[re.Pattern[str]]:
    patterns = list(BASE_HIGH_ATTENTION_PATTERNS)
    for config in load_case_governance_configs(root):
        patterns.extend(literal_pattern(term) for term in config.attention_patterns)
    return patterns


def contains_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle.lower() in lowered for needle in needles)


def contains_trigger(text: str, triggers: list[str]) -> bool:
    for trigger in triggers:
        if re.fullmatch(r"[A-Za-z_ -]+", trigger):
            if re.search(rf"(?<![A-Za-z]){re.escape(trigger)}(?![A-Za-z])", text, re.I):
                return True
        elif trigger in text:
            return True
    return False


def iter_files(root: Path, dirname: str, suffixes: set[str]) -> list[Path]:
    scan_root = root / dirname
    if not scan_root.exists():
        return []
    return sorted(
        path for path in scan_root.rglob("*") if path.is_file() and path.suffix in suffixes
    )


def case_directories(root: Path) -> list[Path]:
    pilot_root = root / CASE_ROOT
    if not pilot_root.exists():
        return []
    return sorted(path for path in pilot_root.iterdir() if path.is_dir() and path.name != "archive")


def reference_exists(root: Path, case_dir: Path, ref: str) -> bool:
    normalized = ref.replace("\\", "/").strip()
    candidates = [case_dir / normalized, root / normalized]
    return any(candidate.exists() for candidate in candidates)


def lint_global_case_specific_leaks(root: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []
    self_path = (root / "scripts" / "lint_case_governance.py").resolve()
    patterns = case_specific_patterns(root)
    for dirname in GLOBAL_SCAN_DIRS:
        for path in iter_files(root, dirname, GLOBAL_SCAN_SUFFIXES):
            if path.resolve() == self_path:
                continue
            text = read_text(path)
            for line_no, line in enumerate(text.splitlines(), start=1):
                for pattern in patterns:
                    if pattern.search(line):
                        messages.append(
                            LintMessage(
                                path,
                                "case-specific term leaked into generic artifact; move it into the case directory or use a generic placeholder",
                                line_no,
                            )
                        )
                        break
    return messages


def lint_case_readmes(root: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for case_dir in case_directories(root):
        case_files = sorted(path for path in case_dir.glob("*.md") if path.is_file())
        current_files = [path for path in case_files if CURRENT_ARTIFACT_RE.fullmatch(path.name)]
        if len(case_files) <= 1 and not current_files:
            continue

        readme = case_dir / "README.md"
        if not readme.exists():
            messages.append(
                LintMessage(readme, "case directory with multiple artifacts needs README.md")
            )
            continue

        text = read_text(readme)
        for current in current_files:
            if f"`{current.name}`" not in text:
                messages.append(
                    LintMessage(readme, f"README must list current artifact `{current.name}`")
                )

        for match in CASE_REF_RE.finditer(text):
            ref = match.group(1)
            if not reference_exists(root, case_dir, ref):
                line_no = text[: match.start()].count("\n") + 1
                messages.append(
                    LintMessage(readme, f"README references missing file `{ref}`", line_no)
                )

        archive_dir = case_dir / "archive"
        if archive_dir.exists():
            for archived in sorted(archive_dir.glob("*.md")):
                archive_ref = f"`archive/{archived.name}`"
                if archive_ref not in text:
                    messages.append(
                        LintMessage(
                            readme,
                            f"README must list archived artifact `{archive_ref.strip('`')}`",
                        )
                    )

        if "synthetic dry-run" in text.lower() and not contains_any(
            text,
            ["must not be promoted", "do not promote", "not be promoted"],
        ):
            messages.append(
                LintMessage(
                    readme,
                    "synthetic dry-run README must state that it must not be promoted without real evidence",
                )
            )
    return messages


def lint_current_artifact_governance(root: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []
    patterns = high_attention_patterns(root)
    for case_dir in case_directories(root):
        for path in sorted(case_dir.glob("*.md")):
            if not CURRENT_ARTIFACT_RE.fullmatch(path.name):
                continue
            text = read_text(path)
            has_stale_trigger = contains_trigger(text, STALE_TRIGGERS)
            if has_stale_trigger and not contains_any(text, STALE_GOVERNANCE_MARKERS):
                messages.append(
                    LintMessage(
                        path,
                        "current artifact mentions old/stale/superseded information without staleness, retraction, or revision governance markers",
                    )
                )

            high_attention_terms = [pattern.pattern for pattern in patterns if pattern.search(text)]
            if high_attention_terms and not contains_any(text, HIGH_ATTENTION_MARKERS):
                messages.append(
                    LintMessage(
                        path,
                        "current artifact contains high-attention debug terms without evidence/status/next-action/stop-condition handling",
                    )
                )

            if contains_any(
                text, ["candidate_owner", "owner candidate", "candidate owner"]
            ) and not contains_any(
                text, ["pm/project lead", "project lead confirmation", "pm confirmation"]
            ):
                messages.append(
                    LintMessage(
                        path,
                        "candidate owners must be explicitly gated on PM/project lead confirmation",
                    )
                )
    return messages


def lint_field_action_plans(root: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for case_dir in case_directories(root):
        path = case_dir / "field-action-plan.md"
        if not path.exists():
            continue
        text = read_text(path)
        for template in [
            "forms/failure_matrix_template.md",
            "forms/same_window_evidence_batch_checklist.md",
        ]:
            if template not in text:
                messages.append(LintMessage(path, f"field action plan must cite `{template}`"))
        for section_options in FIELD_ACTION_REQUIRED_SECTIONS:
            if not any(section.lower() in text.lower() for section in section_options):
                section_label = " / ".join(section_options)
                messages.append(
                    LintMessage(
                        path, f"field action plan missing governance section: {section_label}"
                    )
                )
    return messages


def case_is_complex(root: Path, case_dir: Path) -> bool:
    has_architecture = (case_dir / "latest-architecture-first.md").exists()
    has_field_plan = (case_dir / "field-action-plan.md").exists()
    if has_architecture and has_field_plan:
        return True
    current_text = "\n".join(
        read_text(path)
        for path in sorted(case_dir.glob("*.md"))
        if CURRENT_ARTIFACT_RE.fullmatch(path.name)
    )
    if contains_any(current_text, ["mode gate", "subsystem", "same-window", "同窗口"]):
        return True
    return any(pattern.search(current_text) for pattern in high_attention_patterns(root))


def lint_visual_architecture_briefs(root: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for case_dir in case_directories(root):
        brief = case_dir / "visual-architecture-brief.md"
        if case_is_complex(root, case_dir) and not brief.exists():
            messages.append(
                LintMessage(
                    brief,
                    "complex case needs `visual-architecture-brief.md` with system placement, subsystem diagram, mode gate, evidence stack, and field brief",
                )
            )
            continue
        if not brief.exists():
            continue

        text = read_text(brief)
        for section in VISUAL_BRIEF_REQUIRED_SECTIONS:
            if section.lower() not in text.lower():
                messages.append(
                    LintMessage(brief, f"visual architecture brief missing section: {section}")
                )
        if text.count("```mermaid") < 2:
            messages.append(
                LintMessage(
                    brief,
                    "visual architecture brief must include at least two mermaid diagrams: system placement and subsystem or mode gate",
                )
            )
        if "stop condition" not in text.lower() and "stop 条件" not in text.lower():
            messages.append(
                LintMessage(brief, "visual architecture brief must include stop conditions")
            )
    return messages


def lint_all(root: Path = ROOT) -> list[LintMessage]:
    root = root.resolve()
    messages: list[LintMessage] = []
    messages.extend(lint_global_case_specific_leaks(root))
    messages.extend(lint_case_readmes(root))
    messages.extend(lint_current_artifact_governance(root))
    messages.extend(lint_field_action_plans(root))
    messages.extend(lint_visual_architecture_briefs(root))
    return messages


def main() -> int:
    try:
        messages = lint_all(ROOT)
    except ValueError as exc:
        print("CASE GOVERNANCE LINT FAILED")
        print(f"- {exc}")
        return 1

    if messages:
        print("CASE GOVERNANCE LINT FAILED")
        for message in messages:
            print(f"- {message.format(ROOT)}")
        return 1

    print("CASE GOVERNANCE LINT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
