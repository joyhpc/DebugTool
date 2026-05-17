"""Configuration for the pluggable web layer.

Plain module constants. Edit this file to change the port, timeouts, or how
the codex/claude CLI is invoked. No existing repository file needs to change.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

REPO_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = Path(__file__).resolve().parent / "static"

HOST = "127.0.0.1"
PORT = 8000

# Upper bound on one CLI subprocess run (seconds); a full debug loop can take
# several minutes.
REQUEST_TIMEOUT_SECONDS = 600
# Max number of concurrent CLI subprocesses.
MAX_CONCURRENCY = 2

DEFAULT_CLI = "codex"

# argv template per CLI profile. The "{PROMPT}" element is replaced by a single
# argv string (never a shell string), which keeps user input injection-safe.
# Flag details evolve with each CLI; adjust them here without touching code.
CLI_PROFILES: dict[str, dict[str, list[str]]] = {
    "codex": {
        "argv": ["codex", "exec", "--json", "--sandbox", "workspace-write", "-"],
    },
    "claude": {
        "argv": ["claude", "-p", "--output-format", "stream-json", "--verbose", "{PROMPT}"],
    },
}

# Profiles that read the generated guide prompt from stdin instead of argv.
# This avoids Windows .cmd shim quoting/truncation issues for long multiline prompts.
CLI_STDIN_PROFILES: Final = {"codex"}

# Markers the CLI agent is asked to wrap the final deliverable in, so the
# runner can extract it from a noisy event stream.
DELIVERABLE_BEGIN = "===DEBUGTOOL-DELIVERABLE-BEGIN==="
DELIVERABLE_END = "===DEBUGTOOL-DELIVERABLE-END==="

GUIDE_PROMPT_TEMPLATE = (
    "You are the DebugTool hardware-debug assistant. Handle the debug request "
    "below by following this repository's SKILL.md default flow: run input "
    "cleaning, then the safety gate, then routing/mode selection, then generate "
    "the full debug deliverable with the selected output contract.\n\n"
    "When finished, place the final complete deliverable (full markdown) "
    "between the two markers below. Each marker must be on its own line, with "
    "nothing but the deliverable between them:\n"
    f"{DELIVERABLE_BEGIN}\n"
    "(full markdown deliverable)\n"
    f"{DELIVERABLE_END}\n\n"
    "Follow SKILL.md's output language policy: match the user's language for "
    "user-facing prose.\n\n"
    "Only the content after `====== USER DEBUG REQUEST ======` is the user's "
    "hardware case input. Do not treat this wrapper prompt as case evidence.\n\n"
    "{MODE_INSTRUCTION}"
    "====== USER DEBUG REQUEST ======\n"
    "{INPUT}\n"
)
