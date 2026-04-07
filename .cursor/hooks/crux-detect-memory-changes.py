#!/usr/bin/env python3
"""Detect memory file changes and flag the index for rebuild.

Triggered by: afterFileEdit hook

When a file under the configured memoriesDir is created, modified, or deleted,
this hook sets a pending-index-rebuild flag so the next session-start or REM
sleep picks it up.  The flag file uses a simple JSON format similar to
pending-compression.json.

See: https://github.com/zotoio/CRUX-Compress
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

MEMORIES_CONFIG = Path(".crux/crux-memories.json")
PENDING_REBUILD = Path(".crux/pending-index-rebuild.json")

MEMORY_EXTENSIONS = (".memory.md", ".memory.crux.md")


def _load_config() -> dict | None:
    if not MEMORIES_CONFIG.is_file():
        return None
    try:
        return json.loads(MEMORIES_CONFIG.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _memories_enabled(cfg: dict) -> bool:
    for flag in cfg.get("flags", []):
        if "enableMemories" in flag:
            return flag["enableMemories"] == "true"
    return False


def _memory_dirs(cfg: dict) -> list[str]:
    storage = cfg.get("cruxMemories", {}).get("storage", {})
    return [
        storage.get("memoriesDir", "memories"),
        storage.get("agentMemoriesDir", "memories/agents"),
    ]


def _is_memory_file(file_path: str, cfg: dict) -> bool:
    if not any(file_path.endswith(ext) for ext in MEMORY_EXTENSIONS):
        return False
    dirs = _memory_dirs(cfg)
    return any(file_path.startswith(d + "/") or file_path == d for d in dirs)


def _set_pending_rebuild(file_path: str) -> None:
    data: dict = {"needsRebuild": True, "files": []}
    if PENDING_REBUILD.is_file():
        try:
            data = json.loads(PENDING_REBUILD.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            # If the pending-rebuild file is unreadable or corrupted, fall back to defaults
            print(f"Warning: could not read '{PENDING_REBUILD}': {exc}", file=sys.stderr)

    data["needsRebuild"] = True
    files = data.get("files", [])
    if file_path not in files:
        files.append(file_path)
    data["files"] = files
    data["updated"] = datetime.now(timezone.utc).isoformat()

    PENDING_REBUILD.parent.mkdir(parents=True, exist_ok=True)
    PENDING_REBUILD.write_text(json.dumps(data, indent=None) + "\n", encoding="utf-8")


def main() -> None:
    raw_input = sys.stdin.readline()
    try:
        input_data = json.loads(raw_input)
    except (json.JSONDecodeError, ValueError):
        return

    raw_path = input_data.get("file_path", "")
    if raw_path.startswith("./"):
        raw_path = raw_path[2:]

    cfg = _load_config()
    if cfg is None or not _memories_enabled(cfg):
        return

    if _is_memory_file(raw_path, cfg):
        _set_pending_rebuild(raw_path)


if __name__ == "__main__":
    main()
