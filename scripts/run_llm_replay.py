#!/usr/bin/env python3
"""Run live LLM replay for blind-eval fixtures when an Anthropic key is available."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

for _stream in (sys.stdout, sys.stderr):
    _reconfigure = getattr(_stream, "reconfigure", None)
    if _reconfigure is not None:
        _reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "regression" / "blind_eval" / "manifest.yaml"
DEFAULT_OUTPUT_DIR = ROOT / "regression" / "blind_eval" / "live_outputs"
DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_VALIDATOR_MODE = "architecture_first"
VALIDATOR = ROOT / "scripts" / "output_validator.py"
BLIND_EVAL = ROOT / "scripts" / "run_blind_eval.py"


@dataclass
class ReplayResult:
    case_id: str
    output_path: str
    generated: bool
    validator_rc: int | None
    validator_stdout: str
    validator_stderr: str


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def selected_cases(
    cases: list[dict[str, Any]], requested: set[str], limit: int | None
) -> list[dict[str, Any]]:
    filtered = [case for case in cases if not requested or str(case.get("id")) in requested]
    if limit is not None:
        filtered = filtered[:limit]
    return filtered


def import_anthropic() -> Any:
    try:
        import anthropic
    except ImportError as exc:
        raise RuntimeError(
            "The `anthropic` package is required for live replay. "
            "Install it with `python -m pip install -e .[llm]`."
        ) from exc
    return anthropic


def response_text(message: Any) -> str:
    parts: list[str] = []
    for block in getattr(message, "content", []):
        text = getattr(block, "text", None)
        if isinstance(text, str):
            parts.append(text)
        elif isinstance(block, dict) and isinstance(block.get("text"), str):
            parts.append(str(block["text"]))
    return "\n".join(parts).strip()


def build_prompt(case_id: str, raw_input: str, validator_mode: str) -> str:
    return f"""Run DebugTool on this blind hardware-debug eval input.

Return only the generated markdown artifact for `{validator_mode}` mode. Do not
mention hidden scoring criteria, expected answers, or source records.

<blind_eval_input id="{case_id}">
{raw_input}
</blind_eval_input>
"""


def generate_output(
    client: Any,
    *,
    model: str,
    system_prompt: str,
    case_id: str,
    raw_input: str,
    validator_mode: str,
    max_tokens: int,
    temperature: float,
) -> str:
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": build_prompt(case_id, raw_input, validator_mode),
            }
        ],
    )
    text = response_text(message)
    if not text:
        raise RuntimeError(f"{case_id}: model returned no text content")
    return text


def run_validator(path: Path, mode: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), "--mode", mode, "--file", str(path), "--quiet"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def run_blind_eval(outputs_dir: Path) -> int:
    proc = subprocess.run(
        [sys.executable, str(BLIND_EVAL), "--outputs", str(outputs_dir)],
        cwd=ROOT,
        text=True,
    )
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate live Anthropic replay outputs for blind eval cases."
    )
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--model", default=os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL))
    parser.add_argument("--validator-mode", default=DEFAULT_VALIDATOR_MODE)
    parser.add_argument("--max-tokens", type=int, default=12000)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--case", action="append", default=[], help="Run only this case id")
    parser.add_argument("--limit", type=int, help="Run only the first N selected cases")
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="List work without calling the API")
    parser.add_argument("--no-validate", action="store_true", help="Generate only; skip validators")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir

    manifest = load_yaml(manifest_path)
    cases = as_list(manifest.get("cases"))
    if not cases:
        print(f"LLM REPLAY FAILED: no cases in {rel(manifest_path)}")
        return 2

    selected = selected_cases(cases, set(args.case), args.limit)
    if not selected:
        print("LLM REPLAY FAILED: selected zero cases")
        return 2

    if args.dry_run:
        print(f"LLM REPLAY DRY RUN: {len(selected)} cases -> {rel(output_dir)}")
        for case in selected:
            print(f"- {case.get('id')}")
        return 0

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("LLM REPLAY SKIPPED: ANTHROPIC_API_KEY is not set")
        return 0

    anthropic = import_anthropic()
    client = anthropic.Anthropic()
    system_prompt = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)

    results: list[ReplayResult] = []
    validator_failed = False
    for case in selected:
        case_id = str(case.get("id") or "")
        raw_input = ROOT / str(case.get("raw_input"))
        output_path = output_dir / f"{case_id}.md"

        generated = False
        if args.skip_existing and output_path.exists():
            print(f"SKIP existing output: {case_id}")
        else:
            print(f"GENERATE {case_id} with {args.model}")
            text = generate_output(
                client,
                model=args.model,
                system_prompt=system_prompt,
                case_id=case_id,
                raw_input=raw_input.read_text(encoding="utf-8"),
                validator_mode=args.validator_mode,
                max_tokens=args.max_tokens,
                temperature=args.temperature,
            )
            output_path.write_text(text.rstrip() + "\n", encoding="utf-8")
            generated = True

        validator_rc: int | None = None
        validator_stdout = ""
        validator_stderr = ""
        if not args.no_validate:
            validator_rc, validator_stdout, validator_stderr = run_validator(
                output_path, args.validator_mode
            )
            if validator_rc != 0:
                validator_failed = True
                print(f"VALIDATOR FAILED {case_id}: rc={validator_rc}")
                if validator_stdout.strip():
                    print(validator_stdout.strip())
                if validator_stderr.strip():
                    print(validator_stderr.strip(), file=sys.stderr)
            else:
                print(f"VALIDATOR PASSED {case_id}")

        results.append(
            ReplayResult(
                case_id=case_id,
                output_path=rel(output_path),
                generated=generated,
                validator_rc=validator_rc,
                validator_stdout=validator_stdout,
                validator_stderr=validator_stderr,
            )
        )

    summary_path = output_dir / "run_llm_replay_summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "model": args.model,
                "validator_mode": args.validator_mode,
                "results": [asdict(result) for result in results],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if not args.no_validate:
        blind_eval_rc = run_blind_eval(output_dir)
        if blind_eval_rc != 0:
            return blind_eval_rc
        if validator_failed:
            return 1

    print(f"LLM REPLAY PASSED: {len(results)} cases, summary={rel(summary_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
