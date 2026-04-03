"""Configuration loader for CRUX MCP Server."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_NAME = ".crux/crux-memories.json"

_DEFAULT_TYPE_PRIORITY = ["core", "redflag", "goal", "learning", "idea", "archived"]


@dataclass
class StorageConfig:
    memories_dir: str = "memories"
    agent_memories_dir: str = "memories/agents"
    archive_dir: str = ".ai-ignored/executed"
    index_file: str = ".crux/memory-index.yml"


@dataclass
class ReferenceTrackingConfig:
    enabled: bool = True
    tracking_dir: str = ".crux/reference-tracking"


@dataclass
class MemoriesConfig:
    enabled: bool = False
    compression: bool = False
    storage: StorageConfig = field(default_factory=StorageConfig)
    max_memory_size: int = 2048
    type_priority: list[str] = field(
        default_factory=lambda: list(_DEFAULT_TYPE_PRIORITY)
    )
    reference_tracking: ReferenceTrackingConfig = field(default_factory=ReferenceTrackingConfig)
    scope_ranking: list[str] = field(default_factory=lambda: ["base", "agents", "shared"])


@dataclass
class ServerConfig:
    project_root: Path = field(default_factory=Path.cwd)
    memories: MemoriesConfig = field(default_factory=MemoriesConfig)


def _resolve_flag(flags: list[dict], key: str) -> bool:
    for flag_dict in flags:
        if key in flag_dict:
            return str(flag_dict[key]).lower() == "true"
    return False


def load_config(config_path: Path | None = None, project_root: Path | None = None) -> ServerConfig:
    """Load configuration from crux-memories.json.

    Searches upward from *project_root* when *config_path* is not given.
    """
    root = project_root or Path.cwd()

    if config_path is None:
        config_path = _find_config(root)

    if config_path is None or not config_path.exists():
        logger.warning("Config file not found; using defaults (root=%s)", root)
        return ServerConfig(project_root=root)

    raw = json.loads(config_path.read_text(encoding="utf-8"))
    flags = raw.get("flags", [])
    cm = raw.get("cruxMemories", {})
    st = cm.get("storage", {})
    rt = cm.get("referenceTracking", {})

    storage = StorageConfig(
        memories_dir=st.get("memoriesDir", "memories"),
        agent_memories_dir=st.get("agentMemoriesDir", "memories/agents"),
        archive_dir=st.get("archiveDir", ".ai-ignored/executed"),
        index_file=st.get("indexFile", ".crux/memory-index.yml"),
    )

    ref_tracking = ReferenceTrackingConfig(
        enabled=rt.get("enabled", True),
        tracking_dir=rt.get("trackingDir", ".crux/reference-tracking"),
    )

    memories = MemoriesConfig(
        enabled=_resolve_flag(flags, "enableMemories"),
        compression=_resolve_flag(flags, "enableMemoryCompression"),
        storage=storage,
        max_memory_size=cm.get("maxMemorySize", 2048),
        type_priority=cm.get("typePriority", list(_DEFAULT_TYPE_PRIORITY)),
        reference_tracking=ref_tracking,
        scope_ranking=cm.get("scopeRanking", ["base", "agents", "shared"]),
    )

    return ServerConfig(project_root=root, memories=memories)


def _find_config(start: Path) -> Path | None:
    """Walk upward from *start* looking for the config file."""
    current = start.resolve()
    for _ in range(20):
        candidate = current / DEFAULT_CONFIG_NAME
        if candidate.exists():
            return candidate
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None
