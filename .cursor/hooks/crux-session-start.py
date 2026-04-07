#!/usr/bin/env python3
"""Display pending CRUX compressions and memory nudges at session start.

Triggered by: sessionStart hook

1. Checks .crux/pending-compression.json for files left pending from previous sessions
2. Checks .crux/crux-memories.json for memory nudge conditions
See: https://github.com/zotoio/CRUX-Compress
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PENDING_FILE = Path(".crux/pending-compression.json")
PENDING_REBUILD = Path(".crux/pending-index-rebuild.json")
MEMORIES_CONFIG = Path(".crux/crux-memories.json")


def _read_pending_compression() -> str | None:
    if not PENDING_FILE.is_file():
        return None

    try:
        data = json.loads(PENDING_FILE.read_text(encoding="utf-8"))
        files = data.get("files", [])
    except (json.JSONDecodeError, OSError):
        return None

    if not files:
        return None

    count = len(files)
    file_list = "".join(f"  - {f}\n" for f in files)

    return (
        "[URGENT: CRUX Pending Compression]\n\n"
        "**IMPORTANT: Before responding to the user's message, you MUST first inform them:**\n\n"
        f"{count} source file(s) need CRUX compression:\n"
        f"{file_list}\n"
        'Start your response with: "Note: There are pending CRUX compressions from a previous session. '
        'Would you like me to run /crux-compress for these files?"\n\n'
        "Then proceed to answer their actual question."
    )


def _read_pending_index_rebuild() -> str | None:
    if not PENDING_REBUILD.is_file():
        return None

    try:
        data = json.loads(PENDING_REBUILD.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    if not data.get("needsRebuild"):
        return None

    files = data.get("files", [])
    count = len(files)
    file_list = "".join(f"  - {f}\n" for f in files[:10])
    if count > 10:
        file_list += f"  - ... and {count - 10} more\n"

    return (
        "[CRUX Memory Index Stale]\n\n"
        f"The memory index needs rebuilding — {count} memory file(s) changed since the last rebuild:\n"
        f"{file_list}\n"
        "Run: `python .cursor/skills/crux-skill-memory-index/scripts/memory-index.py`\n"
        "to rebuild, then delete `.crux/pending-index-rebuild.json`."
    )


def _read_memory_nudge() -> str | None:
    if not MEMORIES_CONFIG.is_file():
        return None

    try:
        cfg = json.loads(MEMORIES_CONFIG.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None

    enable_memories = None
    for flag in cfg.get("flags", []):
        if "enableMemories" in flag:
            enable_memories = flag["enableMemories"]
            break

    if enable_memories != "true":
        return None

    nudge_cfg = cfg.get("cruxMemories", {}).get("hooks", {}).get("sessionStartNudge", {})
    watch_dir = Path(nudge_cfg.get("watchDir", "specs"))
    threshold = int(nudge_cfg.get("threshold", 20))
    nudge_message = nudge_cfg.get("message", "")

    if not watch_dir.is_dir() or not nudge_message:
        return None

    dir_count = sum(1 for p in watch_dir.iterdir() if p.is_dir())

    if dir_count <= threshold:
        return None

    return (
        f"[CRUX Memory Nudge]\n\n"
        f"{nudge_message}\n\n"
        f"({dir_count} items detected in {watch_dir}/, threshold is {threshold})"
    )


def main() -> None:
    sys.stdin.readline()

    parts: list[str] = []

    pending = _read_pending_compression()
    if pending:
        parts.append(pending)

    rebuild = _read_pending_index_rebuild()
    if rebuild:
        parts.append(rebuild)

    nudge = _read_memory_nudge()
    if nudge:
        parts.append(nudge)

    if parts:
        additional_context = "\n\n---\n\n".join(parts)
        json.dump({"additional_context": additional_context}, sys.stdout)
    else:
        sys.stdout.write("{}")

    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
