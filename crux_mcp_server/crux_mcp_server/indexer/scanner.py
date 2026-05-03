"""Scan memory directories and build an in-memory index."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from crux_mcp_server.config import ServerConfig
from crux_mcp_server.utils.frontmatter import parse

logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    slug: str
    title: str
    description: str
    type: str
    strength: int
    references: int
    tags: list[str]
    file: str
    body: str = ""
    agent_id: str | None = None


@dataclass
class MemoryIndex:
    entries: list[MemoryEntry] = field(default_factory=list)
    by_slug: dict[str, MemoryEntry] = field(default_factory=dict)
    by_file: dict[str, MemoryEntry] = field(default_factory=dict)


def scan(config: ServerConfig) -> MemoryIndex:
    """Scan all memory directories and return a populated MemoryIndex."""
    root = config.project_root
    index = MemoryIndex()

    yaml_index = _load_yaml_index(root / config.memories.storage.index_file)

    ref_counts = _load_reference_counts(
        root / config.memories.reference_tracking.tracking_dir
    )

    mem_dir = root / config.memories.storage.memories_dir
    if mem_dir.is_dir():
        _scan_directory(mem_dir, root, config, yaml_index, ref_counts, index, agent_id=None)

    agent_dir = root / config.memories.storage.agent_memories_dir
    if agent_dir.is_dir():
        for agent_subdir in sorted(agent_dir.iterdir()):
            if agent_subdir.is_dir() and agent_subdir.name != ".git":
                _scan_directory(
                    agent_subdir, root, config, yaml_index, ref_counts, index,
                    agent_id=agent_subdir.name,
                )

    _sort_index(index, config.memories.type_priority)
    return index


def _scan_directory(
    directory: Path,
    root: Path,
    config: ServerConfig,
    yaml_index: dict[str, dict],
    ref_counts: dict[str, int],
    index: MemoryIndex,
    agent_id: str | None,
) -> None:
    patterns = ["**/*.memory.md", "**/*.memory.crux.md"]
    for pattern in patterns:
        for path in directory.glob(pattern):
            if not path.is_file():
                continue
            try:
                _process_file(path, root, yaml_index, ref_counts, index, agent_id)
            except Exception:
                logger.warning("Skipping corrupt memory file: %s", path, exc_info=True)


def _process_file(
    path: Path,
    root: Path,
    yaml_index: dict[str, dict],
    ref_counts: dict[str, int],
    index: MemoryIndex,
    agent_id: str | None,
) -> None:
    text = path.read_text(encoding="utf-8")
    parsed = parse(text)
    fm = parsed.frontmatter

    slug = _extract_slug(path)
    rel_path = str(path.relative_to(root))

    yaml_entry = yaml_index.get(slug, {})

    entry = MemoryEntry(
        slug=slug,
        title=fm.get("title", yaml_entry.get("title", slug)),
        description=fm.get("description", yaml_entry.get("description", "")),
        type=fm.get("type", yaml_entry.get("type", "unknown")),
        strength=int(fm.get("strength", yaml_entry.get("strength", 0))),
        references=ref_counts.get(slug, yaml_entry.get("references", 0)),
        tags=fm.get("tags", yaml_entry.get("tags", [])),
        file=rel_path,
        body=parsed.body,
        agent_id=agent_id,
    )

    index.entries.append(entry)
    index.by_slug[slug] = entry
    index.by_file[rel_path] = entry


def _extract_slug(path: Path) -> str:
    name = path.name
    for suffix in (".memory.crux.md", ".memory.md"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def _load_yaml_index(index_path: Path) -> dict[str, dict[str, Any]]:
    """Load entries from .crux/memory-index.yml keyed by slug."""
    if not index_path.exists():
        return {}
    try:
        data = yaml.safe_load(index_path.read_text(encoding="utf-8")) or {}
        entries = data.get("memories", [])
        return {e["slug"]: e for e in entries if isinstance(e, dict) and "slug" in e}
    except Exception:
        logger.warning("Could not parse memory-index.yml", exc_info=True)
        return {}


def _load_reference_counts(tracking_dir: Path) -> dict[str, int]:
    """Read .refs.yml files and return slug -> total reference count."""
    counts: dict[str, int] = {}
    if not tracking_dir.is_dir():
        return counts
    for ref_file in tracking_dir.glob("*.refs.yml"):
        slug = ref_file.stem.replace(".refs", "")
        try:
            data = yaml.safe_load(ref_file.read_text(encoding="utf-8")) or {}
            total = data.get("totalReferences", 0)
            counts[slug] = int(total)
        except Exception:
            logger.debug("Skipping corrupt refs file: %s", ref_file)
    return counts


def _sort_index(index: MemoryIndex, type_priority: list[str]) -> None:
    """Sort entries by type priority, then strength desc, then references desc."""
    priority_map = {t: i for i, t in enumerate(type_priority)}
    max_priority = len(type_priority)

    index.entries.sort(
        key=lambda e: (
            priority_map.get(e.type, max_priority),
            -e.strength,
            -e.references,
        )
    )
