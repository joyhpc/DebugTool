"""Subprocess orchestration: drive the codex/claude CLI and stream its output.

This module owns the only place the web layer shells out. It never builds a
shell string; the user prompt is always passed as a single argv element.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import threading
from collections.abc import Iterator

from web.config import (
    CLI_PROFILES,
    CLI_STDIN_PROFILES,
    DELIVERABLE_BEGIN,
    DELIVERABLE_END,
    GUIDE_PROMPT_TEMPLATE,
    REPO_ROOT,
    REQUEST_TIMEOUT_SECONDS,
)

_MAX_LINE_PREVIEW = 500


def build_prompt(user_input: str, mode: str | None = None) -> str:
    """Wrap raw user input with the SKILL.md guidance prompt."""
    mode_instruction = ""
    if mode:
        mode_instruction = (
            f"Selected output mode: {mode}. Use this mode's output contract exactly, "
            "and make the final deliverable validate with "
            f"`python scripts/output_validator.py --mode {mode} --file <deliverable>`.\n\n"
        )
    return GUIDE_PROMPT_TEMPLATE.replace("{MODE_INSTRUCTION}", mode_instruction).replace(
        "{INPUT}", user_input
    )


def _collect_strings(obj: object, out: list[str]) -> None:
    """Recursively collect every string value from a parsed JSON event."""
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            _collect_strings(value, out)
    elif isinstance(obj, list):
        for value in obj:
            _collect_strings(value, out)


def _extract_deliverable(accumulated: str) -> tuple[str, bool]:
    """Pull the marker-wrapped deliverable out of the accumulated CLI text."""
    begin = accumulated.find(DELIVERABLE_BEGIN)
    if begin != -1:
        start = begin + len(DELIVERABLE_BEGIN)
        end = accumulated.find(DELIVERABLE_END, start)
        if end != -1:
            return accumulated[start:end].strip(), True
    return accumulated.strip(), False


def _build_argv(cli: str, prompt: str, resolved_executable: str) -> list[str]:
    """Materialize a CLI profile's argv template, substituting the prompt."""
    template = CLI_PROFILES[cli]["argv"]
    argv = [prompt if part == "{PROMPT}" else part for part in template]
    argv[0] = resolved_executable
    return argv


def run_debug(user_input: str, cli: str, mode: str | None = None) -> Iterator[dict]:
    """Run one debug loop via the chosen CLI, yielding progress/result events."""
    if cli not in CLI_PROFILES:
        yield {"type": "error", "message": f"unknown cli profile: {cli}"}
        return

    executable = CLI_PROFILES[cli]["argv"][0]
    resolved_executable = shutil.which(executable)
    if resolved_executable is None:
        yield {"type": "error", "message": f"CLI not found on PATH: {executable}"}
        return

    prompt = build_prompt(user_input, mode)
    argv = _build_argv(cli, prompt, resolved_executable)
    prompt_on_stdin = cli in CLI_STDIN_PROFILES

    try:
        proc = subprocess.Popen(
            argv,
            cwd=str(REPO_ROOT),
            stdin=subprocess.PIPE if prompt_on_stdin else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
    except OSError as exc:
        yield {"type": "error", "message": f"failed to start {executable}: {exc}"}
        return

    if prompt_on_stdin:
        assert proc.stdin is not None
        proc.stdin.write(prompt)
        proc.stdin.close()

    timed_out = threading.Event()

    def _kill_on_timeout() -> None:
        timed_out.set()
        if proc.poll() is None:
            proc.kill()

    timer = threading.Timer(REQUEST_TIMEOUT_SECONDS, _kill_on_timeout)
    timer.start()

    strings: list[str] = []
    plain_lines: list[str] = []
    try:
        assert proc.stdout is not None
        while True:
            raw_line = proc.stdout.readline()
            if not raw_line:
                break
            line = raw_line.rstrip("\n")
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                plain_lines.append(line)
            else:
                _collect_strings(event, strings)
            yield {"type": "progress", "text": line[:_MAX_LINE_PREVIEW]}
    finally:
        timer.cancel()
        if proc.poll() is None:
            proc.kill()
        proc.wait()

    if timed_out.is_set():
        yield {
            "type": "error",
            "message": f"debug run timed out after {REQUEST_TIMEOUT_SECONDS}s",
        }
        return

    if proc.returncode != 0:
        yield {
            "type": "error",
            "message": f"{executable} exited with code {proc.returncode}",
        }
        return

    markdown, found = _extract_deliverable("\n".join(strings or plain_lines))
    yield {"type": "deliverable", "markdown": markdown, "found": found}
