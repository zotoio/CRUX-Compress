#!/usr/bin/env python3
"""Run the CRUX command suite eval tests.

Usage:
  python3 scripts/run_crux_command_suite.py [--smoke] [--help]

Options:
  --smoke    Run only the crux_command_smoke-marked tests (fast, deterministic, CI-safe).
             Omit to run all non-LLM-driven tests in the suite.
  --help     Show this message and exit.

Exit codes:
  0  All selected tests passed.
  1  One or more tests failed.
  2  pytest not found or test file missing.

This wrapper invokes pytest against evals/test_r_crux_command_suite.py with
well-defined exit codes and a human-readable summary line.  It mirrors the
single Python entry point convention used elsewhere in scripts/.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
NC = "\033[0m"

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_EVAL_FILE = _PROJECT_ROOT / "evals" / "test_r_crux_command_suite.py"


def main() -> int:
    smoke_only = False

    for arg in sys.argv[1:]:
        if arg == "--smoke":
            smoke_only = True
        elif arg in ("--help", "-h"):
            print(__doc__)
            return 0
        else:
            print(f"{RED}Unknown option: {arg}{NC}")
            print("Run with --help for usage.")
            return 1

    pytest_bin = shutil.which("pytest") or shutil.which("py.test")
    if not pytest_bin:
        print(f"{RED}Error: pytest not found.{NC}")
        print(f"{YELLOW}Install with: pip install -r evals/requirements.txt{NC}")
        return 2

    if not _EVAL_FILE.exists():
        print(f"{RED}Error: eval file not found: {_EVAL_FILE}{NC}")
        return 2

    cmd = [pytest_bin, str(_EVAL_FILE), "-q", "--tb=short"]
    if smoke_only:
        cmd += ["-m", "crux_command_smoke"]
        print(f"=== Running CRUX command suite (smoke only) ===")
    else:
        cmd += ["-m", "not llm_driven"]
        print(f"=== Running CRUX command suite (all deterministic tests) ===")

    print()
    result = subprocess.run(cmd, cwd=_PROJECT_ROOT, check=False)

    print()
    if result.returncode == 0:
        print(f"{GREEN}\u2713 CRUX command suite passed{NC}")
    else:
        print(f"{RED}\u2717 CRUX command suite FAILED (exit {result.returncode}){NC}")

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
