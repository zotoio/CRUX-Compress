#!/usr/bin/env python3
"""Detect source file changes that need CRUX compression.

Triggered by: afterFileEdit hook

This hook queues modified source files (with crux: true) for compression.
Tracks pending files in .crux/pending-compression.json
Only operates on .md files under .cursor/rules/
See: https://github.com/zotoio/CRUX-Compress
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PENDING_FILE = Path(".crux/pending-compression.json")
CRUX_HEADER_RE = re.compile(r"crux:\s*(true|[1-9][0-9]?|100)\s*$", re.MULTILINE)


def _is_valid_crux_file(file_path: str) -> bool:
    """Check if a file is valid for CRUX compression."""
    p = Path(file_path)
    if not (
        file_path.startswith(".cursor/rules/")
        and file_path.endswith(".md")
        and not file_path.endswith(".crux.mdc")
        and not file_path.endswith(".crux.md")
        and p.is_file()
    ):
        return False

    try:
        lines = p.read_text(encoding="utf-8").splitlines()[:20]
        header = "\n".join(lines)
        return bool(CRUX_HEADER_RE.search(header))
    except OSError:
        return False


def _normalize_path(raw_path: str) -> str:
    """Normalize a path to repo-relative form."""
    path = raw_path
    if path.startswith("./"):
        path = path[2:]
    try:
        repo_root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=False,
        ).stdout.strip()
        if repo_root and path.startswith(repo_root + "/"):
            path = path[len(repo_root) + 1:]
    except FileNotFoundError:
        pass
    return path


def _load_pending() -> dict:
    if not PENDING_FILE.is_file():
        return {"files": []}
    try:
        data = json.loads(PENDING_FILE.read_text(encoding="utf-8"))
        if "files" not in data:
            return {"files": []}
        return data
    except (json.JSONDecodeError, OSError):
        return {"files": []}


def _save_pending(data: dict) -> None:
    PENDING_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["updated"] = datetime.now(timezone.utc).isoformat()
    PENDING_FILE.write_text(json.dumps(data, indent=None) + "\n", encoding="utf-8")


def _cleanup_invalid_entries() -> None:
    if not PENDING_FILE.is_file():
        return

    data = _load_pending()
    original = list(data["files"])
    data["files"] = [f for f in original if f and _is_valid_crux_file(f)]

    if data["files"] != original:
        _save_pending(data)


def main() -> None:
    raw_input = sys.stdin.readline()
    try:
        input_data = json.loads(raw_input)
    except (json.JSONDecodeError, ValueError):
        return

    raw_path = input_data.get("file_path", "")
    file_path = _normalize_path(raw_path)

    _cleanup_invalid_entries()

    if _is_valid_crux_file(file_path):
        data = _load_pending()
        if file_path not in data["files"]:
            data["files"].append(file_path)
            _save_pending(data)


if __name__ == "__main__":
    main()
