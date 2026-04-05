#!/usr/bin/env python3
"""Update gallery manifest for the CRUX Compress website.

Scans web/compress.md/assets/ for .crux.md files, extracts frontmatter,
finds decompressed variants, and generates manifest.json.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ASSET_TYPES = ("rules", "code", "images", "urls")


def _extract_frontmatter_value(filepath: Path, key: str) -> str:
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return ""

    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return ""

    for line in match.group(1).splitlines():
        m = re.match(rf"^{re.escape(key)}:\s*(.*)", line)
        if m:
            return m.group(1).strip().strip("'\"").replace("~", "")
    return ""


def _extract_title(filepath: Path, fallback: str) -> str:
    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError:
        return fallback

    m = re.search(r"^# (.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()

    m = re.search(r"Ρ\{([^;}]+)", text)
    if m:
        title = m.group(1).split(",")[0].strip()
        return title[0].upper() + title[1:] if title else fallback

    return fallback


def _get_source_ext(directory: Path, shortname: str) -> str:
    has_md = False
    first_ext = ""
    for f in sorted(directory.glob(f"{shortname}.source.*")):
        ext = f.suffix.lstrip(".")
        if not first_ext:
            first_ext = ext
        if ext == "md":
            has_md = True
    return "md" if has_md else first_ext


def _find_decompressed(directory: Path, shortname: str) -> list[dict[str, str]]:
    prefix = f"{shortname}.decompressed-"
    results: list[dict[str, str]] = []
    for f in sorted(directory.glob(f"{prefix}*")):
        rest = f.name[len(prefix):]
        ext = f.suffix.lstrip(".")
        model = rest[: -(len(ext) + 1)] if ext else rest
        results.append({"model": model, "ext": ext})
    return results


def _build_meta(filepath: Path, asset_type: str) -> dict[str, str]:
    meta: dict[str, str] = {}

    if asset_type == "images":
        before = _extract_frontmatter_value(filepath, "beforeSize") or _extract_frontmatter_value(filepath, "originalSize")
        after = _extract_frontmatter_value(filepath, "afterSize")
        reduced = _extract_frontmatter_value(filepath, "reducedBy")
        if before:
            meta["beforeSize"] = before
        if after:
            meta["afterSize"] = after
        if reduced:
            meta["reduction"] = reduced
    else:
        before = _extract_frontmatter_value(filepath, "beforeTokens")
        after = _extract_frontmatter_value(filepath, "afterTokens")
        reduced = _extract_frontmatter_value(filepath, "reducedBy")
        decomp = _extract_frontmatter_value(filepath, "decompressedTokens")
        if before:
            meta["sourceTokens"] = f"~{before}"
        if after:
            meta["cruxTokens"] = f"~{after}"
        if decomp:
            meta["decompressedTokens"] = f"~{decomp}"
        if reduced:
            meta["reduction"] = reduced

    return meta


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    assets_dir = script_dir.parent / "assets"
    manifest_path = assets_dir / "manifest.json"

    print("Scanning asset directories...")

    result: dict[str, list[dict]] = {}

    for asset_type in ASSET_TYPES:
        type_dir = assets_dir / asset_type
        if not type_dir.is_dir():
            continue

        items: list[dict] = []
        for crux_file in sorted(type_dir.glob("*.crux.md")):
            shortname = crux_file.name.removesuffix(".crux.md")
            source_ext = _get_source_ext(type_dir, shortname)
            has_source = bool(source_ext)
            title = _extract_title(crux_file, shortname)
            decompressed = _find_decompressed(type_dir, shortname)
            meta = _build_meta(crux_file, asset_type)

            entry: dict = {
                "name": shortname,
                "title": title,
                "sourceExt": source_ext,
                "hasSource": has_source,
                "hasCrux": True,
                "decompressed": decompressed,
                "meta": meta,
            }

            if asset_type == "urls":
                entry["sourceUrl"] = _extract_frontmatter_value(crux_file, "sourceUrl")
                entry["hasScreenshot"] = (type_dir / f"{shortname}.screenshot.png").is_file()
                entry["hasSourceHtml"] = (type_dir / f"{shortname}.source.html").is_file()

            items.append(entry)
            print(f"  [{asset_type}] {shortname} -> {title}")

        result[asset_type] = items

    manifest_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print()
    print(f"Manifest written to: {manifest_path}")
    total = sum(len(v) for v in result.values())
    print(f"Total items: {total}")


if __name__ == "__main__":
    main()
