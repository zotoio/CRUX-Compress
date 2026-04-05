"""Lightweight CRUX decompression for memory bodies.

This is a *partial* decompressor that handles common CRUX symbols found in
compressed memory files.  Full decompression requires an LLM; this module
provides a best-effort expansion so that memory content is more readable when
served through ``memory-read``.
"""

from __future__ import annotations

import re

SYMBOL_MAP: dict[str, str] = {
    "→": " leads to ",
    "←": " derived from ",
    "¬": "not ",
    "⊤": "true",
    "⊥": "false",
    "∀": "for all ",
    "∃": "there exists ",
    "⊕": " and also ",
    "≻": " preferred over ",
    "≺": " less preferred than ",
    "⊲": "before ",
    "⊳": "after ",
    "∋": " contains ",
    "»": " then ",
    "⊛": "important: ",
    "Δ": "change ",
    "↑": "increase ",
    "↓": "decrease ",
}

BLOCK_LABELS: dict[str, str] = {
    "Ρ": "Purpose",
    "Κ": "Definitions",
    "R": "Rules",
    "Λ": "Triggers",
    "P": "Prohibitions",
    "E": "Exports",
    "Γ": "Dependencies",
    "Π": "Principles",
    "M": "Manifest",
    "Ω": "Notes",
}

_CRUX_BLOCK_RE = re.compile(r"⟦CRUX:[^\n]*\n(.*?)⟧", re.DOTALL)


def decompress(text: str) -> str:
    """Best-effort expansion of CRUX notation to readable text.

    Strips block delimiters and expands common symbols.
    """
    match = _CRUX_BLOCK_RE.search(text)
    inner = match.group(1) if match else text

    result = inner
    for sym, expansion in SYMBOL_MAP.items():
        result = result.replace(sym, expansion)

    for short, label in BLOCK_LABELS.items():
        result = re.sub(rf"^{re.escape(short)}(?:\.[\w]+)?\{{", f"[{label}] ", result, flags=re.MULTILINE)

    result = result.replace("}", "")
    return result.strip()


def is_compressed(text: str) -> bool:
    """Return True if *text* looks like a CRUX-compressed memory body."""
    return "⟦CRUX:" in text
