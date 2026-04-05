#!/usr/bin/env python3
"""Post-dream index rebuild: verify memories are enabled, then rebuild the index.

Called programmatically by the /crux-dream workflow after memory extraction
completes. This is NOT a Cursor event hook.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MEMORIES_CONFIG = Path(".crux/crux-memories.json")
INDEX_SCRIPT = Path(__file__).resolve().parent / "memory-index.py"


def main() -> None:
    if not INDEX_SCRIPT.is_file():
        print(f"Error: Memory index script not found at {INDEX_SCRIPT}", file=sys.stderr)
        sys.exit(1)

    if MEMORIES_CONFIG.is_file():
        try:
            cfg = json.loads(MEMORIES_CONFIG.read_text(encoding="utf-8"))
            enable_memories = None
            for flag in cfg.get("flags", []):
                if "enableMemories" in flag:
                    enable_memories = flag["enableMemories"]
                    break
            if enable_memories != "true":
                print("Memories disabled — skipping index rebuild.")
                sys.exit(0)
        except (json.JSONDecodeError, OSError):
            pass

    print("Rebuilding memory index...")
    subprocess.run([sys.executable, str(INDEX_SCRIPT)], check=True)
    print("Memory index rebuilt. MCP server will detect the change automatically.")


if __name__ == "__main__":
    main()
