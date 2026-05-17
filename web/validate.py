"""Reuse the existing offline output validator without modifying scripts/.

web/__init__.py puts the repo root on sys.path, so importing scripts works
whether the server is started with `python -m web.server` or imported.
"""

from __future__ import annotations

from scripts.output_validator import MODE_HEADINGS, validate_text


def available_modes() -> list[str]:
    """Return the validator modes supported by scripts/output_validator.py."""
    return sorted(MODE_HEADINGS)


def run_validation(markdown: str, mode: str) -> dict:
    """Structurally validate a deliverable; return a JSON-friendly result."""
    if mode not in MODE_HEADINGS:
        return {
            "ok": False,
            "errors": [f"unknown validator mode: {mode}"],
            "warnings": [],
        }
    result = validate_text(markdown, mode)
    return {
        "ok": not result.errors,
        "errors": result.errors,
        "warnings": result.warnings,
    }
