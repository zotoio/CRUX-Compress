"""memory-read tool — read full content of memory files."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from fastmcp import Context

from crux_mcp_server.utils.crux_decompress import decompress, is_compressed

if TYPE_CHECKING:
    from crux_mcp_server.server import ProjectPartition, ProjectRegistry


def register_read(server: "FastMCP", registry: ProjectRegistry) -> None:
    from fastmcp import FastMCP as _F  # noqa: F811

    @server.tool(
        name="memory-read",
        description="Read full content of memory files by slug or path. Decompresses CRUX-compressed bodies automatically.",
    )
    async def memory_read(
        ctx: Context,
        slugs: list[str] | None = None,
        files: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        partitions = await registry.resolve(ctx)
        if not partitions:
            return [{"error": "no project partitions available"}]

        multi = len(partitions) > 1
        results: list[dict[str, Any]] = []

        for slug in (slugs or []):
            found = False
            for part in partitions:
                entry = part.memory_index.by_slug.get(slug)
                if entry is not None:
                    item = _read_entry(part, entry.file, slug=slug)
                    if multi:
                        item["project"] = str(part.config.project_root)
                    results.append(item)
                    found = True
                    break
            if not found:
                results.append({"slug": slug, "error": "not found"})

        for file_path in (files or []):
            found = False
            for part in partitions:
                entry = part.memory_index.by_file.get(file_path)
                if entry is not None:
                    item = _read_entry(part, entry.file)
                    if multi:
                        item["project"] = str(part.config.project_root)
                    results.append(item)
                    found = True
                    break

                abs_path = part.config.project_root / file_path
                if abs_path.is_file():
                    item = _read_file(part, abs_path, file_path)
                    if multi:
                        item["project"] = str(part.config.project_root)
                    results.append(item)
                    found = True
                    break

            if not found:
                results.append({"file": file_path, "error": "not found"})

        return results


def _read_entry(part: ProjectPartition, rel_path: str, slug: str | None = None) -> dict[str, Any]:
    abs_path = part.config.project_root / rel_path
    return _read_file(part, abs_path, rel_path, slug)


def _read_file(
    part: ProjectPartition,
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
