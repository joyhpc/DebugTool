"""Pluggable local web service layer for DebugTool.

This package only reads repository assets and imports scripts/. Nothing in the
existing skill package imports it, so deleting web/ restores the plain skill
repository with no behavior change.
"""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
