"""CRUX MCP Server — core setup and lifecycle."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from fastmcp import FastMCP

from crux_mcp_server.config import ServerConfig, load_config
from crux_mcp_server.indexer.scanner import MemoryIndex, scan
from crux_mcp_server.indexer.search_engine import SearchEngine
from crux_mcp_server.indexer.watcher import MemoryWatcher
from crux_mcp_server.tools import discover_and_register

logger = logging.getLogger(__name__)


@dataclass
class AppContext:
    """Shared application state accessible to all tools."""

    config: ServerConfig
    memory_index: MemoryIndex = field(default_factory=MemoryIndex)
    search_engine: SearchEngine = field(default_factory=SearchEngine)
    watcher: MemoryWatcher | None = None


def create_server(
    config_path: Path | None = None,
    project_root: Path | None = None,
) -> tuple[FastMCP, AppContext]:
    """Build and configure the MCP server, returning (server, context)."""
    config = load_config(config_path=config_path, project_root=project_root)

    server = FastMCP(
        name="crux-memory-server",
        instructions=(
            "CRUX Memory MCP Server. Provides read-only access to the project's "
            "CRUX memory corpus via search, read, and stats tools."
        ),
    )

    ctx = AppContext(config=config)
    _rebuild_index(ctx)
    _start_watcher(ctx)
    discover_and_register(server, ctx)

    return server, ctx


def _rebuild_index(ctx: AppContext) -> None:
    logger.info("Building memory index from %s", ctx.config.project_root)
    ctx.memory_index = scan(ctx.config)
    ctx.search_engine = SearchEngine()
    ctx.search_engine.build(ctx.memory_index)
    logger.info(
        "Index built: %d memories, search backend: %s",
        len(ctx.memory_index.entries),
        "embeddings" if ctx.search_engine._use_embeddings else "tfidf",
    )


def _start_watcher(ctx: AppContext) -> None:
    def on_change() -> None:
        _rebuild_index(ctx)

    ctx.watcher = MemoryWatcher(ctx.config, on_change)
    try:
        ctx.watcher.start()
    except Exception:
        logger.warning("Could not start file watcher", exc_info=True)
