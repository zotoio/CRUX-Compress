"""memory-stats tool — summary statistics about the memory corpus."""

from __future__ import annotations

from collections import Counter
from typing import TYPE_CHECKING, Any

from fastmcp import Context

if TYPE_CHECKING:
    from crux_mcp_server.server import ProjectRegistry


def register_stats(server: "FastMCP", registry: ProjectRegistry) -> None:
    from fastmcp import FastMCP as _F  # noqa: F811 — needed for decorator

    @server.tool(
        name="memory-stats",
        description="Summary statistics about the CRUX memory corpus: counts by type, total memories, and index freshness.",
    )
    async def memory_stats(ctx: Context) -> dict[str, Any]:
        partitions = await registry.resolve(ctx)

        if not partitions:
            return {
                "totalMemories": 0,
                "byType": {},
                "compressedCount": 0,
                "uncompressedCount": 0,
                "projects": [],
                "searchBackend": "none",
            }

        projects: list[dict[str, Any]] = []
        for part in partitions:
            entries = part.memory_index.entries
            type_counts = Counter(e.type for e in entries)

            index_path = part.config.project_root / part.config.memories.storage.index_file
            index_mtime: str | None = None
            if index_path.exists():
                from datetime import datetime, timezone
                mtime = index_path.stat().st_mtime
                index_mtime = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()

            compressed = sum(1 for e in entries if e.file.endswith(".memory.crux.md"))

            projects.append({
                "project": str(part.config.project_root),
                "totalMemories": len(entries),
                "byType": dict(type_counts),
                "compressedCount": compressed,
                "uncompressedCount": len(entries) - compressed,
                "indexFile": str(part.config.memories.storage.index_file),
                "indexLastModified": index_mtime,
                "searchBackend": (
                    "sentence-transformers" if part.search_engine._use_embeddings else "tfidf"
                ),
            })

        if len(projects) == 1:
            return projects[0]

        total = sum(p["totalMemories"] for p in projects)
        merged_types: Counter[str] = Counter()
        for p in projects:
            merged_types.update(p["byType"])

        return {
            "totalMemories": total,
            "byType": dict(merged_types),
            "compressedCount": sum(p["compressedCount"] for p in projects),
            "uncompressedCount": sum(p["uncompressedCount"] for p in projects),
            "projects": projects,
        }
