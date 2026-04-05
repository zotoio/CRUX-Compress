#!/usr/bin/env python3
"""Build a prioritised memory index from memory files and reference trackers."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def load_config(config_path: Path) -> dict:
    """Load and return the cruxMemories config block."""
    if not config_path.is_file():
        print(f"Error: config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with config_path.open() as f:
        raw = json.load(f)

    cfg = raw.get("cruxMemories")
    if cfg is None:
        print("Error: 'cruxMemories' key missing from config", file=sys.stderr)
        sys.exit(1)

    return cfg


def parse_frontmatter(file_path: Path) -> dict | None:
    """Extract YAML frontmatter from a memory file.

    Returns the parsed dict, or None if frontmatter is missing/corrupt.
    """
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Warning: cannot read {file_path}: {exc}", file=sys.stderr)
        return None

    if not text.startswith("---"):
        print(f"Warning: no frontmatter found in {file_path}", file=sys.stderr)
        return None

    parts = text.split("---", 2)
    if len(parts) < 3:
        print(f"Warning: malformed frontmatter in {file_path}", file=sys.stderr)
        return None

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        print(f"Warning: YAML parse error in {file_path}: {exc}", file=sys.stderr)
        return None

    if not isinstance(fm, dict):
        print(f"Warning: frontmatter is not a mapping in {file_path}", file=sys.stderr)
        return None

    return fm


def slug_from_filename(file_path: Path) -> str:
    """Derive the memory slug from a filename.

    Strips .memory.crux.md or .memory.md suffix.
    """
    name = file_path.name
    for suffix in (".memory.crux.md", ".memory.md"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return file_path.stem


def load_tracker(tracking_dir: Path, slug: str) -> int:
    """Load the reference count for a slug from its tracker file."""
    tracker_path = tracking_dir / f"{slug}.refs.yml"
    if not tracker_path.is_file():
        return 0

    try:
        text = tracker_path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return int(data.get("references", 0))
    except (OSError, yaml.YAMLError, ValueError, TypeError) as exc:
        print(f"Warning: cannot parse tracker {tracker_path}: {exc}", file=sys.stderr)

    return 0


def scan_memories(memories_dir: Path) -> list[Path]:
    """Recursively find all memory files under a directory."""
    if not memories_dir.is_dir():
        return []

    files: list[Path] = []
    for pattern in ("*.memory.md", "*.memory.crux.md"):
        files.extend(memories_dir.rglob(pattern))
    return files


def build_index(cfg: dict, project_root: Path) -> list[dict]:
    """Scan memories, join with trackers, return sorted index entries."""
    storage = cfg.get("storage", {})
    memories_dir = project_root / storage.get("memoriesDir", "memories")
    tracking_dir = project_root / cfg.get("referenceTracking", {}).get(
        "trackingDir", ".crux/reference-tracking"
    )
    type_priority: list[str] = cfg.get(
        "typePriority", ["core", "redflag", "goal", "learning", "idea", "archived"]
    )
    type_rank = {t: i for i, t in enumerate(type_priority)}

    memory_files = scan_memories(memories_dir)

    seen_slugs: set[str] = set()
    entries: list[dict] = []

    for mf in memory_files:
        fm = parse_frontmatter(mf)
        if fm is None:
            continue

        slug = slug_from_filename(mf)

        if slug in seen_slugs:
            print(
                f"Warning: duplicate slug '{slug}' — skipping {mf}",
                file=sys.stderr,
            )
            continue
        seen_slugs.add(slug)

        title = fm.get("title", "")
        if not title:
            print(f"Warning: missing title in {mf}, skipping", file=sys.stderr)
            continue

        mem_type = fm.get("type", "idea")
        strength = fm.get("strength", 1)
        try:
            strength = int(strength)
        except (ValueError, TypeError):
            strength = 1

        references = load_tracker(tracking_dir, slug)
        tags = fm.get("tags", [])
        if not isinstance(tags, list):
            tags = []

        try:
            rel_path = mf.relative_to(project_root)
        except ValueError:
            rel_path = mf

        entry: dict = {}
        mem_id = fm.get("id")
        if mem_id:
            entry["id"] = str(mem_id)
        entry.update(
            {
                "slug": slug,
                "title": str(title),
                "description": str(fm.get("description", "")),
                "type": str(mem_type),
                "strength": strength,
                "references": references,
                "tags": tags,
                "file": str(rel_path),
                "_type_rank": type_rank.get(mem_type, len(type_priority)),
            }
        )

        entries.append(entry)

    entries.sort(key=lambda e: (e["_type_rank"], -e["strength"], -e["references"]))

    for e in entries:
        del e["_type_rank"]

    return entries


def write_index(index_path: Path, entries: list[dict]) -> None:
    """Write the memory index YAML file."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    index_path.parent.mkdir(parents=True, exist_ok=True)

    with index_path.open("w", encoding="utf-8") as f:
        f.write("# Generated by crux-skill-memory-index — do not edit manually\n")
        f.write(f"# Last rebuilt: {now}\n\n")
        yaml.dump(
            {"memories": entries},
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=120,
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a prioritised CRUX memory index."
    )
    parser.add_argument(
        "--config",
        default=".crux/crux-memories.json",
        help="Path to crux-memories.json config file (default: .crux/crux-memories.json)",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = Path.cwd() / config_path

    project_root = config_path.parent.parent
    if config_path.parent.name == ".crux":
        project_root = config_path.parent.parent
    else:
        project_root = Path.cwd()

    cfg = load_config(config_path)

    storage = cfg.get("storage", {})
    index_file = project_root / storage.get("indexFile", ".crux/memory-index.yml")

    entries = build_index(cfg, project_root)
    write_index(index_file, entries)

    print(f"Index rebuilt: {index_file} ({len(entries)} memories)")


if __name__ == "__main__":
    main()
