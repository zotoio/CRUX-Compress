#!/usr/bin/env python3
"""Run all tests (bats + pytest + optional crux-test).

Usage: python3 scripts/test.py [--crux-test]

Options:
    --crux-test    Also run /crux-test via cursor-agent (requires cursor-agent CLI)
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    run_crux_test = False
    tests_run = False

    for arg in sys.argv[1:]:
        if arg == "--crux-test":
            run_crux_test = True
        elif arg in ("--help", "-h"):
            print("Usage: python3 scripts/test.py [--crux-test]")
            print()
            print("Options:")
            print("  --crux-test    Also run /crux-test via cursor-agent (requires cursor-agent CLI)")
            print("  --help         Show this help message")
            return 0
        else:
            print(f"{RED}Unknown option: {arg}{NC}")
            return 1

    bats_files = sorted(PROJECT_ROOT.glob("tests/*.bats"))
    bats = shutil.which("bats")
    if bats_files and bats:
        print("=== Running bats tests ===")
        print()
        result = subprocess.run(
            [bats, *[str(f) for f in bats_files]],
            cwd=PROJECT_ROOT,
            check=False,
        )
        if result.returncode != 0:
            return result.returncode
        tests_run = True
    elif bats_files:
        print(f"{YELLOW}Warning: bats not found, skipping bats tests{NC}")

    if run_crux_test:
        print()
        print("=== Running /crux-test via cursor-agent ===")
        print()

        cursor_agent = shutil.which("cursor-agent")
        if cursor_agent:
            result = subprocess.run(
                [
                    cursor_agent,
                    "--model", "opus-4.5-thinking",
                    "--print",
                    "--output-format", "stream-json",
                    "--workspace", str(PROJECT_ROOT),
                    "/crux-test",
                ],
                cwd=PROJECT_ROOT,
                check=False,
            )
            if result.returncode != 0:
                return result.returncode
        else:
            print(f"{YELLOW}Warning: cursor-agent not found, skipping crux-test{NC}")

    print()
    print("=== Running pytest ===")
    print()

    pytest_bin = shutil.which("pytest")
    if pytest_bin:
        result = subprocess.run(
            [pytest_bin, "evals/", "-v"],
            cwd=PROJECT_ROOT,
            check=False,
        )
        if result.returncode != 0:
            return result.returncode
        tests_run = True
    else:
        print(f"{YELLOW}Warning: pytest not found, skipping tests{NC}")
        print(f"{YELLOW}Install with: pip install -r evals/requirements.txt{NC}")

    print()
    if tests_run:
        print(f"{GREEN}\u2713 All tests passed{NC}")
    else:
        print(f"{YELLOW}\u2713 No automated tests were run{NC}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
