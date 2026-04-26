"""memory-read tool — read full content of memory files."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from crux_mcp_server.utils.crux_decompress import decompress, is_compressed

if TYPE_CHECKING:
    from crux_mcp_server.server import AppContext
    from fastmcp import FastMCP


def register_read(server: FastMCP, ctx: AppContext) -> None:
    @server.tool(
        name="memory-read",
        description="Read full content of memory files by slug or path. Decompresses CRUX-compressed bodies automatically.",
    )
    def memory_read(
        slugs: list[str] | None = None,
        files: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        for slug in (slugs or []):
            entry = ctx.memory_index.by_slug.get(slug)
            if entry is None:
                results.append({"slug": slug, "error": "not found"})
                continue
            results.append(_read_entry(ctx, entry.file, slug=slug))

        for file_path in (files or []):
            entry = ctx.memory_index.by_file.get(file_path)
            if entry is not None:
                results.append(_read_entry(ctx, entry.file))
                continue

            abs_path = ctx.config.project_root / file_path
            if abs_path.is_file():
                results.append(_read_file(ctx, abs_path, file_path))
            else:
                results.append({"file": file_path, "error": "not found"})

        return results


def _read_entry(ctx: AppContext, rel_path: str, slug: str | None = None) -> dict[str, Any]:
    abs_path = ctx.config.project_root / rel_path
    return _read_file(ctx, abs_path, rel_path, slug)


def _read_file(
    ctx: AppContext,
    abs_path: Path,
    rel_path: str,
    slug: str | None = None,
) -> dict[str, Any]:
    try:
        text = abs_path.read_text(encoding="utf-8")
    except OSError as exc:
        return {"file": rel_path, "error": str(exc)}

    from crux_mcp_server.utils.frontmatter import parse
    parsed = parse(text)

    body = parsed.body
    if is_compressed(body):
        body = decompress(body)

    result: dict[str, Any] = {
        "file": rel_path,
        "frontmatter": parsed.frontmatter,
        "content": body,
    }
    if slug:
        result["slug"] = slug
    return result
