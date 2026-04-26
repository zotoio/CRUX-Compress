#!/usr/bin/env python3
"""Auto-track memory references from agent output annotations.

Triggered by: afterAgentResponse hook

Scans agent response text for [memory:{title}] annotations, resolves each
title to a memory slug via the memory index, and creates or updates the
corresponding .refs.yml tracker file.

See: https://github.com/zotoio/CRUX-Compress
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

MEMORIES_CONFIG = Path(".crux/crux-memories.json")
ANNOTATION_RE = re.compile(r"\[memory:([^\]]+)\]")


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


def _ref_tracking_config(cfg: dict) -> dict | None:
    rt = cfg.get("cruxMemories", {}).get("referenceTracking", {})
    if not rt.get("enabled", True):
        return None
    return rt


def _parse_index_entries(index_path: Path) -> list[dict]:
    """Parse memory-index.yml into a list of {slug, title, file, strength} dicts.

    Uses line-by-line parsing to avoid requiring pyyaml in hooks.
    """
    if not index_path.is_file():
        return []

    entries: list[dict] = []
    current: dict = {}

    for raw_line in index_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()

        if line.startswith("- id:"):
            if current.get("slug"):
                entries.append(current)
            current = {}
            continue

        stripped = line.lstrip()
        if stripped.startswith("slug:"):
            current["slug"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("title:"):
            current["title"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("file:"):
            current["file"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("strength:"):
            try:
                current["strength"] = int(stripped.split(":", 1)[1].strip())
            except ValueError:
                current["strength"] = 1

    if current.get("slug"):
        entries.append(current)

    return entries


def _normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip().lower())


def _resolve_title_to_entry(title: str, entries: list[dict]) -> dict | None:
    """Match an annotation title to an index entry (case-insensitive)."""
    norm = _normalize_title(title)
    for entry in entries:
        if _normalize_title(entry.get("title", "")) == norm:
            return entry
    return None


def _read_refs_yml(path: Path) -> dict:
    """Parse a .refs.yml tracker file into a dict.

    Returns a dict with keys: slug, references, last_referenced, strength,
    recent_references (list of dicts).
    """
    if not path.is_file():
        return {}

    data: dict = {}
    recent: list[dict] = []
    current_ref: dict | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if line.startswith("#"):
            continue

        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if indent == 0 and ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()
            if key == "slug":
                data["slug"] = val
            elif key == "references":
                data["references"] = int(val) if val.isdigit() else 0
            elif key == "last_referenced":
                data["last_referenced"] = val
            elif key == "strength":
                data["strength"] = int(val) if val.isdigit() else 1
            elif key == "recent_references":
                data["recent_references"] = recent
        elif stripped.startswith("- ") and ":" in stripped:
            if current_ref is not None:
                recent.append(current_ref)
            current_ref = {}
            entry_content = stripped[2:]
            k, _, v = entry_content.partition(":")
            k = k.strip()
            v = v.strip().strip('"')
            current_ref[k] = v
        elif indent >= 4 and current_ref is not None and ":" in stripped:
            k, _, v = stripped.partition(":")
            k = k.strip()
            v = v.strip().strip('"')
            if k == "count":
                current_ref[k] = int(v) if v.isdigit() else 1
            else:
                current_ref[k] = v

    if current_ref is not None:
        recent.append(current_ref)

    data.setdefault("recent_references", recent)
    return data


def _write_refs_yml(path: Path, data: dict) -> None:
    """Write a .refs.yml tracker file."""
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Managed by crux-skill-memory-reference-tracker — do not edit manually",
        f"slug: {data['slug']}",
        f"references: {data['references']}",
        f"last_referenced: {data['last_referenced']}",
        f"strength: {data['strength']}",
        "recent_references:",
    ]

    for ref in data.get("recent_references", []):
        source_key = None
        source_val = None
        for k in ref:
            if k not in ("count", "last", "context"):
                source_key = k
                source_val = ref[k]
                break
        if source_key and source_val:
            lines.append(f'  - {source_key}: "{source_val}"')
            lines.append(f"    count: {ref.get('count', 1)}")
            lines.append(f"    last: {ref.get('last', date.today().isoformat())}")
            if ref.get("context"):
                lines.append(f'    context: "{ref["context"]}"')

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _get_strength_from_memory(file_path: str) -> int:
    """Read the strength value from a memory file's frontmatter."""
    p = Path(file_path)
    if not p.is_file():
        return 1

    try:
        text = p.read_text(encoding="utf-8")
    except OSError:
        return 1

    in_frontmatter = False
    for line in text.splitlines():
        if line.strip() == "---":
            if in_frontmatter:
                break
            in_frontmatter = True
            continue
        if in_frontmatter and line.strip().startswith("strength:"):
            val = line.split(":", 1)[1].strip()
            try:
                return int(val)
            except ValueError:
                return 1

    return 1


def _update_tracker(
    tracking_dir: Path,
    slug: str,
    strength: int,
    max_refs_stored: int,
) -> None:
    """Create or update a .refs.yml tracker for the given slug."""
    tracker_path = tracking_dir / f"{slug}.refs.yml"
    today = date.today().isoformat()
    source_key = "conversation_id"
    source_val = f"auto-hook-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M')}"

    if tracker_path.is_file():
        data = _read_refs_yml(tracker_path)
        data["references"] = data.get("references", 0) + 1
        data["last_referenced"] = today
        data["strength"] = strength

        recent = data.get("recent_references", [])
        matched = False
        for ref in recent:
            if ref.get(source_key) == source_val:
                ref["count"] = ref.get("count", 0) + 1
                ref["last"] = today
                matched = True
                break

        if not matched:
            recent.append({
                source_key: source_val,
                "count": 1,
                "last": today,
            })

        recent.sort(key=lambda r: r.get("count", 0), reverse=True)
        data["recent_references"] = recent[:max_refs_stored]
    else:
        data = {
            "slug": slug,
            "references": 1,
            "last_referenced": today,
            "strength": strength,
            "recent_references": [
                {
                    source_key: source_val,
                    "count": 1,
                    "last": today,
                }
            ],
        }

    _write_refs_yml(tracker_path, data)


def main() -> None:
    raw_input = sys.stdin.readline()
    try:
        input_data = json.loads(raw_input)
    except (json.JSONDecodeError, ValueError):
        return

    response_text = input_data.get("text", "")
    if not response_text:
        return

    titles = ANNOTATION_RE.findall(response_text)
    if not titles:
        return

    cfg = _load_config()
    if cfg is None or not _memories_enabled(cfg):
        return

    rt_cfg = _ref_tracking_config(cfg)
    if rt_cfg is None:
        return

    storage = cfg.get("cruxMemories", {}).get("storage", {})
    index_path = Path(storage.get("indexFile", ".crux/memory-index.yml"))
    tracking_dir = Path(rt_cfg.get("trackingDir", ".crux/reference-tracking"))
    max_refs_stored = int(rt_cfg.get("maxReferencesStored", 10))

    entries = _parse_index_entries(index_path)
    if not entries:
        return

    seen_slugs: set[str] = set()
    for title in titles:
        entry = _resolve_title_to_entry(title, entries)
        if entry is None or entry["slug"] in seen_slugs:
            continue
        seen_slugs.add(entry["slug"])

        strength = _get_strength_from_memory(entry.get("file", ""))
        _update_tracker(tracking_dir, entry["slug"], strength, max_refs_stored)

    sys.stdout.write("{}\n")


if __name__ == "__main__":
    main()
