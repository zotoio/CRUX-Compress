#!/usr/bin/env python3
"""CRUX Utils - Multi-purpose utility for CRUX compression workflows.

Usage:
    crux-utils.py --token-count <file>
    crux-utils.py --token-count --ratio <source_file> <crux_file> [--target <n>]
    crux-utils.py --cksum <file>

Modes:
    --token-count   Estimate token count for a file
    --cksum         Get checksum of a file (for sourceChecksum tracking)

Options:
    --target <n>    Set compression target percentage (1-100, default 25)
"""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

SPECIAL_CHARS = frozenset("«»⟨⟩→←≻≺⊤⊥∀∃¬∋⊳⊲≥≤≠ΔΡΛΠΚΓΦΩθ⊛◊")

PROSE_RATIO = 4.0
CODE_RATIO = 3.5


def _count_special_chars(text: str) -> int:
    return sum(1 for ch in text if ch in SPECIAL_CHARS)


def _extract_code_blocks(text: str) -> str:
    blocks: list[str] = []
    in_block = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_block = not in_block
            if not in_block:
                continue
            continue
        if in_block:
            blocks.append(line)
    return "\n".join(blocks)


def _extract_prose(text: str) -> str:
    lines: list[str] = []
    in_block = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_block = not in_block
            continue
        if not in_block:
            lines.append(line)
    return "\n".join(lines)


def _count_chars_without_special(text: str) -> int:
    return sum(1 for ch in text if ch not in SPECIAL_CHARS)


def _estimate_tokens(filepath: str) -> int:
    p = Path(filepath)
    if not p.is_file():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    text = p.read_text(encoding="utf-8")
    special_count = _count_special_chars(text)

    code_content = _extract_code_blocks(text)
    code_chars = _count_chars_without_special(code_content)

    prose_content = _extract_prose(text)
    prose_chars = _count_chars_without_special(prose_content)

    prose_tokens = math.ceil(prose_chars / PROSE_RATIO)
    code_tokens = math.ceil(code_chars / CODE_RATIO)
    total_tokens = prose_tokens + code_tokens + special_count

    print(f"=== Token Estimate: {p.name} ===")
    print(f"Prose tokens:      {prose_tokens}")
    print(f"Code tokens:       {code_tokens}")
    print(f"Special tokens:    {special_count}")
    print("---")
    print(f"TOTAL TOKENS:      {total_tokens}")

    return total_tokens


def _calculate_ratio(source_file: str, crux_file: str, target: int = 25) -> None:
    print("=== Compression Ratio Analysis ===")
    print()

    source_tokens = _estimate_tokens(source_file)
    print()
    crux_tokens = _estimate_tokens(crux_file)
    print()

    print("=== Compression Summary ===")
    print(f"Source tokens:     {source_tokens}")
    print(f"CRUX tokens:       {crux_tokens}")

    if source_tokens > 0:
        ratio = round((crux_tokens * 100) / source_tokens, 1)
        reduction = round(100 - ratio, 1)
        target_met = "YES" if ratio <= target else "NO"
        print(f"Ratio:             {ratio}% of original")
        print(f"Reduction:         {reduction}%")
        print(f"Target (≤{target}%):    {target_met}")


def _run_cksum(filepath: str) -> None:
    p = Path(filepath)
    if not p.is_file():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(
        ["cksum", filepath], capture_output=True, text=True, check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        stderr = result.stderr.strip() or "no stderr output"
        checksum = ""
        print(
            f"Warning: cksum failed for {filepath}: {stderr}",
            file=sys.stderr,
        )
    else:
        checksum = result.stdout.split()[0]

    print(f"=== Checksum: {p.name} ===")
    print(f"Checksum:          {checksum}")
    print("---")
    print(f'FRONTMATTER:       "{checksum}"')


def _show_help() -> None:
    print("""\
CRUX Utils - Multi-purpose utility for CRUX compression workflows

Usage:
  crux-utils.py --token-count <file>
  crux-utils.py --token-count --ratio <source_file> <crux_file> [--target <n>]
  crux-utils.py --cksum <file>

Modes:
  --token-count   Estimate token count for a file
                  Use --ratio to compare source vs CRUX files
  --cksum         Get checksum of a file (for sourceChecksum tracking)
                  Output format: "checksum" (for CRUX frontmatter)

Options:
  --target <n>    Set compression target percentage (1-100, default 25)
                  Only used with --ratio mode

Examples:
  crux-utils.py --token-count myfile.md
  crux-utils.py --token-count --ratio source.md source.crux.md
  crux-utils.py --token-count --ratio source.md source.crux.md --target 40
  crux-utils.py --cksum myfile.md""")


def main() -> None:
    args = sys.argv[1:]

    if not args:
        _show_help()
        sys.exit(0)

    if args[0] in ("--help", "-h"):
        _show_help()
        sys.exit(0)

    if args[0] == "--token-count":
        rest = args[1:]
        if not rest:
            print("Error: --token-count requires a file argument", file=sys.stderr)
            print("Usage: crux-utils.py --token-count <file>", file=sys.stderr)
            print("       crux-utils.py --token-count --ratio <source> <crux> [--target <n>]", file=sys.stderr)
            sys.exit(1)

        if rest[0] == "--ratio":
            ratio_args = rest[1:]
            target = 25
            if "--target" in ratio_args:
                ti = ratio_args.index("--target")
                if ti + 1 >= len(ratio_args):
                    print("Error: --target requires a numeric argument", file=sys.stderr)
                    sys.exit(1)
                try:
                    target = int(ratio_args[ti + 1])
                except ValueError:
                    print(f"Error: --target must be an integer, got '{ratio_args[ti + 1]}'", file=sys.stderr)
                    sys.exit(1)
                if target < 1 or target > 100:
                    print(f"Error: --target must be 1-100, got {target}", file=sys.stderr)
                    sys.exit(1)
                ratio_args = ratio_args[:ti] + ratio_args[ti + 2:]
            if len(ratio_args) != 2:
                print("Error: --ratio requires two file arguments", file=sys.stderr)
                print("Usage: crux-utils.py --token-count --ratio <source> <crux> [--target <n>]", file=sys.stderr)
                sys.exit(1)
            _calculate_ratio(ratio_args[0], ratio_args[1], target)
        else:
            _estimate_tokens(rest[0])

    elif args[0] == "--cksum":
        if len(args) < 2:
            print("Error: --cksum requires a file argument", file=sys.stderr)
            print("Usage: crux-utils.py --cksum <file>", file=sys.stderr)
            sys.exit(1)
        _run_cksum(args[1])

    else:
        print(f"Error: Unknown mode: {args[0]}", file=sys.stderr)
        print("Use --help for usage information", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
