"""YAML frontmatter parser for memory files."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import yaml


@dataclass
class ParsedMemory:
    frontmatter: dict[str, Any]
    body: str
    raw: str


def parse(text: str) -> ParsedMemory:
    """Split a memory file into frontmatter dict and body string.

    Expects the standard ``---`` delimited YAML frontmatter block.
    Returns empty frontmatter when delimiters are absent.
    """
    if not text.startswith("---"):
        return ParsedMemory(frontmatter={}, body=text, raw=text)

    parts = text.split("---", 2)
    if len(parts) < 3:
        return ParsedMemory(frontmatter={}, body=text, raw=text)

    fm_text = parts[1]
    body = parts[2].lstrip("\n")

    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        fm = {}

    return ParsedMemory(frontmatter=fm, body=body, raw=text)


def extract_searchable_text(fm: dict[str, Any], body: str) -> str:
    """Build a single string suitable for text search from frontmatter + body."""
    parts: list[str] = []
    if title := fm.get("title"):
        parts.append(str(title))
    if desc := fm.get("description"):
        parts.append(str(desc))
    if tags := fm.get("tags"):
        if isinstance(tags, list):
            parts.append(" ".join(str(t) for t in tags))
    parts.append(body)
    return " ".join(parts)
