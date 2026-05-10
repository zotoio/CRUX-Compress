"""memory-search tool — semantic search across memories."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from fastmcp import Context

if TYPE_CHECKING:
    from crux_mcp_server.server import ProjectRegistry


def register_search(server: "FastMCP", registry: ProjectRegistry) -> None:
    from fastmcp import FastMCP as _F  # noqa: F811

    @server.tool(
        name="memory-search",
        description="Semantic search across CRUX memories. Returns ranked results with frontmatter and file paths.",
    )
    async def memory_search(
        query: str,
        ctx: Context,
        limit: int = 10,
        types: list[str] | None = None,
        tags: list[str] | None = None,
        agentId: str | None = None,
        minStrength: int | None = None,
        includeContent: bool = False,
    ) -> list[dict[str, Any]]:
        partitions = await registry.resolve(ctx)
        if not partitions:
            return []

        multi = len(partitions) > 1
        all_results: list[tuple[float, dict[str, Any]]] = []

        for part in partitions:
            results = part.search_engine.search(query, limit=limit * 3)

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
                if multi:
                    item["project"] = str(part.config.project_root)
                if includeContent:
                    item["content"] = entry.body

                all_results.append((r.score, item))

        all_results.sort(key=lambda t: t[0], reverse=True)
        return [item for _, item in all_results[:limit]]
