"""Memory tools module — registers search, read, and stats tools."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from crux_mcp_server.server import ProjectRegistry
    from fastmcp import FastMCP


def register(server: FastMCP, registry: ProjectRegistry) -> None:
    from crux_mcp_server.tools.memory.search import register_search
    from crux_mcp_server.tools.memory.read import register_read
    from crux_mcp_server.tools.memory.stats import register_stats

    register_search(server, registry)
    register_read(server, registry)
    register_stats(server, registry)
