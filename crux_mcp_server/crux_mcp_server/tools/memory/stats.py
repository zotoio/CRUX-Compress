"""memory-stats tool — summary statistics about the memory corpus."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from crux_mcp_server.server import AppContext
    from fastmcp import FastMCP


def register_stats(server: FastMCP, ctx: AppContext) -> None:
    @server.tool(
        name="memory-stats",
        description="Summary statistics about the CRUX memory corpus: counts by type, total memories, and index freshness.",
    )
    def memory_stats() -> dict[str, Any]:
        entries = ctx.memory_index.entries
        type_counts = Counter(e.type for e in entries)

        index_path = (
            ctx.config.project_root / ctx.config.memories.storage.index_file
        )
        index_mtime: str | None = None
        if index_path.exists():
            from datetime import datetime, timezone
            mtime = index_path.stat().st_mtime
            index_mtime = datetime.fromtimestamp(mtime, tz=timezone.utc).isoformat()

        compressed_count = sum(
            1 for e in entries if e.file.endswith(".memory.crux.md")
        )

        return {
            "totalMemories": len(entries),
            "byType": dict(type_counts),
            "compressedCount": compressed_count,
            "uncompressedCount": len(entries) - compressed_count,
            "indexFile": str(ctx.config.memories.storage.index_file),
            "indexLastModified": index_mtime,
            "searchBackend": (
                "sentence-transformers" if ctx.search_engine._use_embeddings else "tfidf"
            ),
        }
