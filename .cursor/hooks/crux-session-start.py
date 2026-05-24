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
from datetime import datetime, timezone
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


def _read_stale_refs_nudge() -> str | None:
    """Warn when no .refs.yml tracker has been updated within the threshold window.

    This catches the silent-failure case where memories are enabled but agents are
    not annotating their output with [memory:Title] markers, which means the
    `afterAgentResponse` hook has nothing to record and reference tracking
    effectively stops without any visible signal.
    """
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

    rt_cfg = cfg.get("cruxMemories", {}).get("referenceTracking", {})
    if not rt_cfg.get("enabled", True):
        return None

    threshold_days = rt_cfg.get("warnIfStaleAfterDays")
    if threshold_days is None:
        return None

    try:
        threshold_days = int(threshold_days)
    except (TypeError, ValueError):
        return None
    if threshold_days <= 0:
        return None

    tracking_dir = Path(rt_cfg.get("trackingDir", ".crux/reference-tracking"))
    if not tracking_dir.is_dir():
        return None

    tracker_files = [p for p in tracking_dir.glob("*.refs.yml") if p.is_file()]

    now = datetime.now(timezone.utc).timestamp()
    threshold_seconds = threshold_days * 86400

    if not tracker_files:
        newest_age_days: float | None = None
    else:
        newest_mtime = max(p.stat().st_mtime for p in tracker_files)
        newest_age_days = (now - newest_mtime) / 86400
        if (now - newest_mtime) < threshold_seconds:
            return None

    if newest_age_days is None:
        body = (
            f"No memory reference trackers exist in {tracking_dir}/.\n"
            "This means no agent has emitted a [memory:Title] annotation that the "
            "afterAgentResponse hook could resolve against the memory index.\n"
        )
    else:
        body = (
            f"The most recent memory reference tracker in {tracking_dir}/ was updated "
            f"{newest_age_days:.1f} days ago (threshold: {threshold_days} days).\n"
            "This usually means agents are not annotating their output with "
            "[memory:Title] markers, so the afterAgentResponse hook has nothing to "
            "record.\n"
        )

    return (
        "[CRUX Memory Reference Tracking Stale]\n\n"
        f"{body}\n"
        "Likely causes:\n"
        "  - Agents are not discovering memories (no MCP `memory-search` calls, no "
        "reads of `.crux/memory-index.yml`).\n"
        "  - Agents discover memories but forget the `[memory:Exact Title]` "
        "annotation contract in `.cursor/rules/crux-memories-integration.md`.\n"
        "  - Subagents annotate but the parent agent strips or paraphrases away "
        "the markers before they reach the user-facing reply.\n\n"
        "Action: review the integration rule's Output Annotation and Subagent "
        "Annotation Passthrough sections, then proceed."
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

    stale_refs = _read_stale_refs_nudge()
    if stale_refs:
        parts.append(stale_refs)

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
