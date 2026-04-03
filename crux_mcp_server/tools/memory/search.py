"""memory-search tool — semantic search across memories."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from crux_mcp_server.server import AppContext
    from fastmcp import FastMCP


def register_search(server: FastMCP, ctx: AppContext) -> None:
    @server.tool(
        name="memory-search",
        description="Semantic search across CRUX memories. Returns ranked results with frontmatter and file paths.",
    )
    def memory_search(
        query: str,
        limit: int = 10,
        types: list[str] | None = None,
        tags: list[str] | None = None,
        agentId: str | None = None,
        minStrength: int | None = None,
        includeContent: bool = False,
    ) -> list[dict[str, Any]]:
        results = ctx.search_engine.search(query, limit=limit * 3)

        filtered = []
        for r in results:
            entry = r.entry

            if types and entry.type not in types:
                continue
            if tags and not set(tags).intersection(entry.tags):
                continue
            if agentId is not None and entry.agent_id != agentId:
                continue
            if minStrength is not None and entry.strength < minStrength:
                continue

            item: dict[str, Any] = {
                "slug": entry.slug,
                "title": entry.title,
                "description": entry.description,
                "type": entry.type,
                "strength": entry.strength,
                "tags": entry.tags,
                "file": entry.file,
                "score": round(r.score, 4),
            }
            if includeContent:
                item["content"] = entry.body
            filtered.append(item)

            if len(filtered) >= limit:
                break

        return filtered
