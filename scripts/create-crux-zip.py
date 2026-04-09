#!/usr/bin/env python3
"""Create CRUX distribution zip files.

Usage: python3 scripts/create-crux-zip.py [output-dir]

Single build step for CRUX releases. Produces:
  - CRUX-Compress-v{version}.zip              (core distribution archive)
  - CRUX-MCP-Server-v{version}.zip            (standalone MCP server archive)
  - .crux/dist-manifest.json                  (canonical file list for installer/CI)
  - .crux/crux-release-files.json             (per-version checksums, updated in place)

Version is read from .crux/crux.json.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import zipfile
from datetime import date
from pathlib import Path

DIST_FILES = [
    "CRUX.md",
    "install.crux.md",
    ".crux/crux.json",
    ".cursor/hooks.json",
    ".cursor/agents/crux-cursor-rule-manager.md",
    ".cursor/agents/crux-cursor-memory-manager.md",
    ".cursor/commands/crux-compress.md",
    ".cursor/commands/crux-dream.md",
    ".cursor/commands/crux-mindreader.md",
    ".cursor/commands/crux-forget.md",
    ".cursor/hooks/crux-detect-changes.py",
    ".cursor/hooks/crux-detect-memory-changes.py",
    ".cursor/hooks/crux-session-start.py",
    ".cursor/rules/_CRUX-RULE.mdc",
    ".cursor/rules/crux-memories-integration.crux.mdc",
    ".cursor/skills/crux-utils/SKILL.md",
    ".cursor/skills/crux-utils/scripts/crux-utils.py",
    ".cursor/skills/crux-skill-memory-crud/SKILL.md",
    ".cursor/skills/crux-skill-memory-compress/SKILL.md",
    ".cursor/skills/crux-skill-memory-extract/SKILL.md",
    ".cursor/skills/crux-skill-memory-index/SKILL.md",
    ".cursor/skills/crux-skill-memory-index/scripts/memory-index.py",
    ".cursor/skills/crux-skill-memory-index/scripts/post-dream.py",
    ".cursor/skills/crux-skill-memory-rebalance/SKILL.md",
    ".cursor/skills/crux-skill-memory-reference-tracker/SKILL.md",
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def update_release_manifest(project_root: Path, version: str) -> None:
    """Update crux-release-files.json with checksums for this version."""
    manifest_path = project_root / ".crux" / "crux-release-files.json"

    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        manifest = {
            "description": "CRUX release file manifest with checksums for verification and backup",
            "releases": {},
            "allFiles": {},
        }

    files_entry: dict[str, dict] = {}
    all_release_files = DIST_FILES + ["AGENTS.md"]

    for rel in all_release_files:
        src = project_root / rel
        if src.is_file():
            checksum = sha256_file(src)
            size = src.stat().st_size
            files_entry[rel] = {"checksum": checksum, "size": size}
            print(f"  {rel}: {checksum[:16]}... ({size} bytes)")

            all_files = manifest.setdefault("allFiles", {})
            versions = all_files.get(rel, [])
            if version not in versions:
                versions.append(version)
            all_files[rel] = versions

    manifest.setdefault("releases", {})[version] = {
        "date": date.today().isoformat(),
        "files": files_entry,
    }

    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {manifest_path.relative_to(project_root)} for v{version}")


def build_mcp_server_zip(project_root: Path, output_dir: Path, version: str) -> Path:
    """Build a standalone MCP server zip containing all server code and deps."""
    zip_name = f"CRUX-MCP-Server-v{version}.zip"
    zip_path = output_dir / zip_name
    mcp_dir = project_root / "crux_mcp_server"

    if not mcp_dir.is_dir():
        print(f"WARNING: {mcp_dir} not found, skipping MCP server zip")
        return zip_path

    print(f"\nCreating MCP server package v{version}...")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root_dir, _dirs, files in sorted(os.walk(mcp_dir)):
            root_path = Path(root_dir)
            for fname in sorted(files):
                src = root_path / fname
                if src.suffix == ".pyc" or "__pycache__" in str(src):
                    continue
                rel = str(src.relative_to(project_root))
                zf.write(src, rel)

        zf.writestr(
            "install-mcp-server.py",
            (project_root / "install.py").read_text(encoding="utf-8"),
        )

    print(f"Done! Created: {zip_path}\n")
    print("Contents:")
    with zipfile.ZipFile(zip_path) as zf:
        zf.printdir()

    return zip_path


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    output_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()

    config = json.loads((project_root / ".crux" / "crux.json").read_text(encoding="utf-8"))
    version = config["version"]
    zip_name = f"CRUX-Compress-v{version}.zip"

    print(f"Creating CRUX distribution package v{version}...")
    print(f"Output: {output_dir / zip_name}")

    # 1. Update dist-manifest.json (canonical file list)
    dist_manifest = project_root / ".crux" / "dist-manifest.json"
    dist_manifest.write_text(
        json.dumps({"version": version, "files": DIST_FILES}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Updated {dist_manifest.relative_to(project_root)}")

    # 2. Update crux-release-files.json (per-version checksums)
    print("Generating checksums...")
    update_release_manifest(project_root, version)

    # 3. Build the core distribution zip
    zip_path = output_dir / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        print("Packaging files...")
        for rel in DIST_FILES:
            src = project_root / rel
            if src.is_file():
                zf.write(src, rel)

        release_manifest = project_root / ".crux" / "crux-release-files.json"
        if release_manifest.is_file():
            zf.write(release_manifest, ".crux/crux-release-files.json")

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
            print(
                "WARNING: AGENTS.md is missing a closing </CRUX> tag; "
                "falling back to extracting the CRUX block from <CRUX to EOF",
            )
            crux_block = agents_text[idx:].rstrip()
        zf.writestr("AGENTS.crux.md", crux_block + "\n")

    print(f"\nDone! Created: {zip_path}\n")
    print("Contents:")
    with zipfile.ZipFile(zip_path) as zf:
        zf.printdir()

    # 4. Build the MCP server zip
    build_mcp_server_zip(project_root, output_dir, version)


if __name__ == "__main__":
    main()
