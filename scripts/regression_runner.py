#!/usr/bin/env python3
# Compatibility wrapper. Real LLM-backed regression runner is planned for V0.95.
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).with_name("regression_suite_linter.py")), run_name="__main__")
