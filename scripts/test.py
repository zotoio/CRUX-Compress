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
    if bats_files:
        print("=== Running bats tests ===")
        print()
        result = subprocess.run(
            ["bats"] + [str(f) for f in bats_files],
            cwd=PROJECT_ROOT,
        )
        if result.returncode != 0:
            return result.returncode

    if run_crux_test:
        print()
        print("=== Running /crux-test via cursor-agent ===")
        print()

        if shutil.which("cursor-agent"):
            result = subprocess.run(
                [
                    "cursor-agent",
                    "--model", "opus-4.5-thinking",
                    "--print",
                    "--output-format", "stream-json",
                    "--workspace", str(PROJECT_ROOT),
                    "/crux-test",
                ],
                cwd=PROJECT_ROOT,
            )
            if result.returncode != 0:
                return result.returncode
        else:
            print(f"{YELLOW}Warning: cursor-agent not found, skipping crux-test{NC}")

    print()
    print("=== Running pytest ===")
    print()

    if shutil.which("pytest"):
        result = subprocess.run(
            ["pytest", "evals/", "-v"],
            cwd=PROJECT_ROOT,
        )
        if result.returncode != 0:
            return result.returncode
    else:
        print(f"{YELLOW}Warning: pytest not found, skipping tests{NC}")
        print(f"{YELLOW}Install with: pip install -r evals/requirements.txt{NC}")

    print()
    print(f"{GREEN}\u2713 All tests passed{NC}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
