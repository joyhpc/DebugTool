#!/usr/bin/env python3
"""Lint DebugTool contract identity and committed artifact portability."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VERSION_RE = re.compile(r"^version:\s*[\"']?([^\"'\s]+)", re.MULTILINE)
PYPROJECT_VERSION_RE = re.compile(r"^version\s*=\s*[\"']([^\"']+)[\"']", re.MULTILINE)
V_LINE_RE = re.compile(r"\bV(\d+\.\d+(?:\.\d+)?)\b")
PROMPT_VERSION_RE = re.compile(r"\bDebug Decision Tree Skill V(\d+\.\d+(?:\.\d+)?)\b")

PATH_LEAK_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]"),
    re.compile(r"/(?:Users|home)/[^\s`|)]+"),
    re.compile(r"~[\\/]"),
    re.compile(r"\.cursor[\\/]projects"),
]

PATH_SCAN_DIRS = ["examples", "pilot_runs", "regression"]
PATH_SCAN_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".toml", ".txt"}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path.relative_to(ROOT)} is not valid UTF-8: {exc}") from exc


def first_match(pattern: re.Pattern[str], text: str, label: str) -> str:
    match = pattern.search(text)
    if not match:
        raise ValueError(f"missing {label}")
    return match.group(1)


def skill_version() -> str:
    return first_match(VERSION_RE, read_text(ROOT / "SKILL.md"), "SKILL.md version")


def check_equal(errors: list[str], path: Path, found: str, expected: str, label: str) -> None:
    if found != expected:
        errors.append(f"{path.relative_to(ROOT)}: {label} is {found!r}, expected {expected!r}")


def check_required_version(
    errors: list[str],
    path: Path,
    pattern: re.Pattern[str],
    text: str,
    expected: str,
    label: str,
) -> None:
    match = pattern.search(text)
    if not match:
        errors.append(f"{path.relative_to(ROOT)}: missing {label}")
        return
    check_equal(errors, path, match.group(1), expected, label)


def lint_versions(expected: str) -> list[str]:
    errors: list[str] = []

    pyproject = ROOT / "pyproject.toml"
    check_required_version(
        errors, pyproject, PYPROJECT_VERSION_RE, read_text(pyproject), expected, "project.version"
    )

    readme = ROOT / "README.md"
    check_required_version(errors, readme, V_LINE_RE, read_text(readme), expected, "README version")

    version_md = ROOT / "release" / "VERSION.md"
    check_required_version(
        errors, version_md, V_LINE_RE, read_text(version_md), expected, "release version"
    )

    safety_rules = ROOT / "safety" / "safety_gate_rules.yaml"
    check_required_version(
        errors, safety_rules, VERSION_RE, read_text(safety_rules), expected, "safety rules version"
    )

    for path in sorted((ROOT / "prompts").glob("*.md")):
        header = "\n".join(read_text(path).splitlines()[:8])
        check_required_version(
            errors, path, PROMPT_VERSION_RE, header, expected, "prompt skill identity"
        )

    return errors


def lint_path_leaks() -> list[str]:
    errors: list[str] = []
    for dirname in PATH_SCAN_DIRS:
        root = ROOT / dirname
        if not root.exists():
            continue
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            if path.suffix.lower() not in PATH_SCAN_EXTENSIONS:
                continue
            text = read_text(path)
            for line_no, line in enumerate(text.splitlines(), start=1):
                for pattern in PATH_LEAK_PATTERNS:
                    if pattern.search(line):
                        errors.append(
                            f"{path.relative_to(ROOT)}:{line_no}: machine-local path leak: "
                            f"{line.strip()}"
                        )
                        break
    return errors


def main() -> int:
    errors: list[str] = []
    try:
        expected = skill_version()
        errors.extend(lint_versions(expected))
        errors.extend(lint_path_leaks())
    except ValueError as exc:
        errors.append(str(exc))

    if errors:
        print("CONTRACT LINT FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CONTRACT LINT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
