"""CRUX MCP Server — core setup and lifecycle."""

from __future__ import annotations

import asyncio
import logging
import threading
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlparse

from fastmcp import Context, FastMCP

from crux_mcp_server.config import DEFAULT_CONFIG_NAME, ServerConfig, load_config
from crux_mcp_server.indexer.scanner import MemoryIndex, scan
from crux_mcp_server.indexer.search_engine import SearchEngine
from crux_mcp_server.indexer.watcher import MemoryWatcher
from crux_mcp_server.tools import discover_and_register

logger = logging.getLogger(__name__)


@dataclass
class ProjectPartition:
    """Index, search engine, and watcher for a single project."""

    config: ServerConfig
    memory_index: MemoryIndex = field(default_factory=MemoryIndex)
    search_engine: SearchEngine = field(default_factory=SearchEngine)
    watcher: MemoryWatcher | None = None

    def rebuild_index(self) -> None:
        logger.info("Building memory index from %s", self.config.project_root)
        self.memory_index = scan(self.config)
        self.search_engine = SearchEngine()
        self.search_engine.build(self.memory_index)
        logger.info(
            "Index built: %d memories, search backend: %s",
            len(self.memory_index.entries),
            "embeddings" if self.search_engine._use_embeddings else "tfidf",
        )

    def start_watcher(self) -> None:
        self.watcher = MemoryWatcher(self.config, self.rebuild_index)
        try:
            self.watcher.start()
        except Exception:
            logger.warning("Could not start file watcher for %s", self.config.project_root, exc_info=True)

    def stop_watcher(self) -> None:
        if self.watcher is not None:
            self.watcher.stop()
            self.watcher = None


class ProjectRegistry:
    """Manages multiple project partitions, keyed by resolved root path."""

    def __init__(self, fallback_root: Path | None = None, fallback_config: Path | None = None) -> None:
        self._partitions: dict[Path, ProjectPartition] = {}
        self._lock = threading.Lock()
        self._fallback_root = fallback_root
        self._fallback_config = fallback_config

        if fallback_root is not None:
            self._load_partition(fallback_root.resolve(), fallback_config)

    async def resolve(self, ctx: Context) -> list[ProjectPartition]:
        """Return active partitions for the current MCP client session.

        Queries the client for workspace roots, discovers which ones
        have CRUX memory configs, and lazily loads partitions.
        """
        roots = await self._get_roots(ctx)

        if roots:
            partitions = []
            for root in roots:
                resolved = root.resolve()
                if resolved in self._partitions:
                    partitions.append(self._partitions[resolved])
                elif (resolved / DEFAULT_CONFIG_NAME).exists():
                    partitions.append(self._load_partition(resolved))
            if partitions:
                return partitions

        if self._fallback_root is not None:
            resolved = self._fallback_root.resolve()
            if resolved in self._partitions:
                return [self._partitions[resolved]]

        return []

    def get_all(self) -> list[ProjectPartition]:
        with self._lock:
            return list(self._partitions.values())

    def shutdown(self) -> None:
        with self._lock:
            for partition in self._partitions.values():
                partition.stop_watcher()
            self._partitions.clear()

    def _load_partition(self, root: Path, config_path: Path | None = None) -> ProjectPartition:
        with self._lock:
            if root in self._partitions:
                return self._partitions[root]

            config = load_config(config_path=config_path, project_root=root)
            partition = ProjectPartition(config=config)
            partition.rebuild_index()
            partition.start_watcher()
            self._partitions[root] = partition
            logger.info("Loaded project partition: %s (%d memories)", root, len(partition.memory_index.entries))
            return partition

    @staticmethod
    async def _get_roots(ctx: Context) -> list[Path]:
        try:
            roots = await asyncio.wait_for(ctx.list_roots(), timeout=5.0)
            paths: list[Path] = []
            for root in roots:
                uri = str(root.uri)
                if uri.startswith("file://"):
                    parsed = urlparse(uri)
                    paths.append(Path(unquote(parsed.path)))
            return paths
        except asyncio.TimeoutError:
            logger.debug("Timed out waiting for roots from client; using fallback")
            return []
        except Exception:
            logger.debug("Could not list roots from client", exc_info=True)
            return []


# Keep backward-compat alias for tool registration signatures
AppContext = ProjectPartition


def create_server(
    config_path: Path | None = None,
    project_root: Path | None = None,
) -> tuple[FastMCP, ProjectRegistry]:
    """Build and configure the MCP server, returning (server, registry)."""
    registry = ProjectRegistry(
        fallback_root=project_root,
        fallback_config=config_path,
    )

    server = FastMCP(
        name="crux-memory-server",
        instructions=(
            "CRUX Memory MCP Server. Provides read-only access to the project's "
            "CRUX memory corpus via search, read, and stats tools."
        ),
    )

    discover_and_register(server, registry)

    return server, registry
