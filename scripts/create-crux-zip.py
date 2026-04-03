#!/usr/bin/env python3
"""Create CRUX distribution zip file.

Usage: python3 scripts/create-crux-zip.py [output-dir]

Packages all CRUX-related files for distribution.
Output: CRUX-Compress-v{version}.zip (version read from .crux/crux.json)
"""

from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

DIST_FILES = [
    "CRUX.md",
    ".crux/crux.json",
    ".cursor/hooks.json",
    ".cursor/agents/crux-cursor-rule-manager.md",
    ".cursor/commands/crux-compress.md",
    ".cursor/hooks/crux-detect-changes.py",
    ".cursor/hooks/crux-session-start.py",
    ".cursor/rules/_CRUX-RULE.mdc",
    ".cursor/skills/crux-utils/SKILL.md",
    ".cursor/skills/crux-utils/scripts/crux-utils.py",
]


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    output_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()

    config = json.loads((project_root / ".crux" / "crux.json").read_text(encoding="utf-8"))
    version = config["version"]
    zip_name = f"CRUX-Compress-v{version}.zip"

    print(f"Creating CRUX distribution package v{version}...")
    print(f"Output: {output_dir / zip_name}")

    zip_path = output_dir / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        print("Copying core files...")
        for rel in DIST_FILES:
            src = project_root / rel
            if src.is_file():
                zf.write(src, rel)

        manifest = project_root / ".crux" / "crux-release-files.json"
        if manifest.is_file():
            zf.write(manifest, ".crux/crux-release-files.json")
            print("Included release manifest")

        print("Extracting CRUX block from AGENTS.md...")
        agents_text = (project_root / "AGENTS.md").read_text(encoding="utf-8")
        match = re.search(r"(<CRUX.*?</CRUX>)", agents_text, re.DOTALL)
        if match:
            crux_block = match.group(1)
        else:
            idx = agents_text.find("<CRUX")
            if idx == -1:
                print("ERROR: Could not extract CRUX block from AGENTS.md")
                sys.exit(1)
            crux_block = agents_text[idx:].rstrip()
        zf.writestr("AGENTS.crux.md", crux_block + "\n")

    print(f"\nDone! Created: {zip_path}\n")
    print("Contents:")
    with zipfile.ZipFile(zip_path) as zf:
        zf.printdir()


if __name__ == "__main__":
    main()
