#!/usr/bin/env python3
"""Post-dream hook: rebuild memory index after dream extraction.

Invoked by the crux-dream command/skill after memory extraction completes.

1. Rebuilds .crux/memory-index.yml from all memory files
2. The MCP server's file watcher detects the index timestamp change automatically
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

MEMORIES_CONFIG = Path(".crux/crux-memories.json")
INDEX_SCRIPT = Path(".cursor/skills/crux-skill-memory-index/scripts/memory-index.py")


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
                print("Memories disabled \u2014 skipping index rebuild.")
                sys.exit(0)
        except (json.JSONDecodeError, OSError):
            pass

    print("Rebuilding memory index...")
    subprocess.run([sys.executable, str(INDEX_SCRIPT)], check=True)
    print("Memory index rebuilt. MCP server will detect the change automatically.")


if __name__ == "__main__":
    main()
