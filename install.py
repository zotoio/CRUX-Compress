#!/usr/bin/env python3
"""CRUX Compress Installer.

Usage:
    curl -fsSL https://raw.githubusercontent.com/zotoio/CRUX-Compress/main/install.py | python3 -
    curl -fsSL https://cdn.jsdelivr.net/gh/zotoio/CRUX-Compress@main/install.py | python3 -
    curl -fsSL .../install.py | python3 - --backup --verbose
    python3 .crux/update.py [-y] [--force] [--backup] [--verbose]

Options:
    -y               Non-interactive mode, assume yes to all confirmations
    --force          Backup current installation and install regardless of version
    --backup         Create backups of existing files before overwriting
    --verbose        Show detailed progress
    --with-memories  Set up optional memory system scaffolding
    --help           Show this help message
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO_OWNER = "zotoio"
REPO_NAME = "CRUX-Compress"
GITHUB_API = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
DOWNLOAD_BASE = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/download"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main"
JSDELIVR_CDN = f"https://cdn.jsdelivr.net/gh/{REPO_OWNER}/{REPO_NAME}"
JSDELIVR_API = f"https://data.jsdelivr.com/v1/packages/gh/{REPO_OWNER}/{REPO_NAME}"

# ANSI colors
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
NC = "\033[0m"

VERBOSE = False
NON_INTERACTIVE = False


def log(msg: str) -> None:
    print(f"{BLUE}[CRUX]{NC} {msg}", file=sys.stderr)


def log_verbose(msg: str) -> None:
    if VERBOSE:
        log(msg)


def log_success(msg: str) -> None:
    print(f"{GREEN}[CRUX]{NC} {msg}", file=sys.stderr)


def log_warn(msg: str) -> None:
    print(f"{YELLOW}[CRUX]{NC} {msg}", file=sys.stderr)


def log_error(msg: str) -> None:
    print(f"{RED}[CRUX]{NC} {msg}", file=sys.stderr)


def confirm(prompt: str, default: str = "Y") -> bool:
    if NON_INTERACTIVE:
        return True
    hint = "[Y/n]" if default == "Y" else "[y/N]"
    try:
        reply = input(f"{prompt} {hint} ").strip()
    except EOFError:
        return default == "Y"
    if not reply:
        return default == "Y"
    return reply.lower().startswith("y")


def http_get(url: str, *, timeout: int = 30) -> bytes | None:
    try:
        req = Request(url, headers={"User-Agent": "CRUX-Compress-Installer"})
        with urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except (URLError, OSError, TimeoutError):
        return None


def http_get_text(url: str) -> str | None:
    data = http_get(url)
    return data.decode("utf-8") if data else None


# ── Version helpers ──


def get_latest_version() -> str:
    version = None

    body = http_get_text(GITHUB_API)
    if body:
        try:
            version = json.loads(body).get("tag_name", "")
        except json.JSONDecodeError:
            m = re.search(r'"tag_name"\s*:\s*"([^"]+)"', body)
            if m:
                version = m.group(1)

    if not version or version == "null":
        log_verbose("GitHub API unavailable, trying jsDelivr...")
        body = http_get_text(JSDELIVR_API)
        if body:
            try:
                data = json.loads(body)
                versions = data.get("versions", [])
                if versions:
                    version = versions[0]
            except json.JSONDecodeError:
                pass

    if not version or version == "null":
        log_error("Failed to fetch latest version from GitHub and jsDelivr")
        sys.exit(1)

    return version.lstrip("v")


def get_installed_version() -> str:
    p = Path(".crux/crux.json")
    if not p.is_file():
        return ""
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("version", "")
    except (json.JSONDecodeError, OSError):
        return ""


def compare_versions(v1: str, v2: str) -> int:
    """Return 0 if v1 > v2, 1 if equal, 2 if v1 < v2."""
    if v1 == v2:
        return 1
    parts1 = [int(x) for x in v1.split(".")]
    parts2 = [int(x) for x in v2.split(".")]
    max_len = max(len(parts1), len(parts2))
    for i in range(max_len):
        a = parts1[i] if i < len(parts1) else 0
        b = parts2[i] if i < len(parts2) else 0
        if a > b:
            return 0
        if a < b:
            return 2
    return 1


def get_version_change_type(old_ver: str, new_ver: str) -> str:
    old = [int(x) for x in old_ver.split(".")]
    new = [int(x) for x in new_ver.split(".")]
    old += [0] * (3 - len(old))
    new += [0] * (3 - len(new))
    if new[0] != old[0]:
        return "major"
    if new[1] != old[1]:
        return "minor"
    return "patch"


# ── File helpers ──


def get_checksum(filepath: str) -> str:
    p = Path(filepath)
    if not p.is_file():
        return ""
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def check_not_in_crux_repo() -> None:
    if (
        Path("CRUX.md").is_file()
        and Path("scripts/create-crux-zip.py").is_file()
        and Path("scripts").is_dir()
    ):
        try:
            if "CRUX Rule Compression Specification" in Path("CRUX.md").read_text(encoding="utf-8"):
                log_error("Cannot install CRUX-Compress within its own repository.")
                log_error("Run this script in a target project directory instead.")
                sys.exit(1)
        except OSError:
            pass


def detect_git_root() -> str:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=False,
        )
        return r.stdout.strip() if r.returncode == 0 else ""
    except FileNotFoundError:
        return ""


# ── Backup ──


def create_backup_zip() -> str:
    repo_name = Path.cwd().name
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_dir = Path(tempfile.gettempdir()) / "crux" / repo_name
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / f"crux-backup-{repo_name}-{ts}.zip"

    log("Creating backup...")

    standard_files = [
        "CRUX.md", "AGENTS.md", "install.crux.md",
        ".crux/crux.json", ".crux/crux-release-files.json",
        ".cursor/hooks.json", ".cursor/agents/crux-cursor-rule-manager.md",
        ".cursor/commands/crux-compress.md",
        ".cursor/hooks/crux-detect-changes.py", ".cursor/hooks/crux-session-start.py",
        ".cursor/rules/_CRUX-RULE.mdc",
        ".cursor/skills/crux-utils/SKILL.md", ".cursor/skills/crux-utils/scripts/crux-utils.py",
    ]

    files_to_backup: list[str] = []
    for f in standard_files:
        if Path(f).is_file():
            files_to_backup.append(f)

    for p in Path(".").rglob("*.crux.*"):
        if p.is_file():
            rel = str(p)
            if rel not in files_to_backup:
                files_to_backup.append(rel)

    if not files_to_backup:
        log_verbose("No files to backup")
        return ""

    try:
        with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files_to_backup:
                zf.write(f)
        log_verbose(f"Backup created: {backup_path}")
        return str(backup_path)
    except OSError:
        log_warn("Failed to create backup zip")
        return ""


# ── hooks.json merge ──


def merge_hooks_json(staging_hooks_path: str) -> None:
    target = Path(".cursor/hooks.json")
    staging = Path(staging_hooks_path)

    if not staging.is_file():
        log_warn("No hooks.json in staging, skipping hooks merge")
        return

    target.parent.mkdir(parents=True, exist_ok=True)

    if not target.is_file():
        shutil.copy2(str(staging), str(target))
        log_success(f"Created {target}")
        return

    log_verbose(f"Merging CRUX hooks into existing {target}...")

    try:
        existing = json.loads(target.read_text(encoding="utf-8"))
        new_data = json.loads(staging.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        log_warn(f"Failed to parse hooks.json: {e}")
        shutil.copy2(str(staging), str(target))
        return

    existing_hooks = existing.get("hooks", {}) or {}
    new_hooks = new_data.get("hooks", {}) or {}

    for lifecycle in ("sessionStart", "afterFileEdit", "stop"):
        exist_arr = existing_hooks.get(lifecycle) or []
        new_arr = new_hooks.get(lifecycle) or []
        existing_cmds = {h.get("command") for h in exist_arr if isinstance(h, dict)}
        for hook in new_arr:
            if isinstance(hook, dict) and hook.get("command") not in existing_cmds:
                exist_arr.append(hook)
        if exist_arr:
            existing_hooks[lifecycle] = exist_arr

    existing["hooks"] = existing_hooks
    target.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
    log_success(f"Merged CRUX hooks into {target}")


# ── AGENTS.md upsert ──


def upsert_agents_crux_block(crux_block_file: str) -> None:
    block_path = Path(crux_block_file)
    agents_path = Path("AGENTS.md")

    if not block_path.is_file():
        log_warn("No AGENTS.crux.md found, skipping AGENTS.md update")
        return

    new_block = block_path.read_text(encoding="utf-8")

    if agents_path.is_file():
        content = agents_path.read_text(encoding="utf-8")
        if "<CRUX" in content:
            before = content[: content.index("<CRUX")]
            after_match = re.search(r"</CRUX>\s*\n?", content)
            after = content[after_match.end():] if after_match else ""
            content = new_block.rstrip("\n") + "\n" + after.lstrip("\n")
            if before.strip():
                content = new_block.rstrip("\n") + "\n\n" + before.lstrip("\n") + after
            agents_path.write_text(content, encoding="utf-8")
            log_success("Updated CRUX block in AGENTS.md")
        else:
            agents_path.write_text(new_block + "\n" + content, encoding="utf-8")
            log_success("Added CRUX block to AGENTS.md")
    else:
        agents_path.write_text(new_block, encoding="utf-8")
        log_success("Created AGENTS.md with CRUX block")

    block_path.unlink(missing_ok=True)
    log_verbose("Removed AGENTS.crux.md")


# ── Deprecated file cleanup ──

DEPRECATED_FILES = [
    ".cursor/hooks/detect-crux-changes.sh",
    ".cursor/skills/CRUX-Utils/SKILL.md",
    ".cursor/skills/CRUX-Utils/scripts/crux-utils.sh",
    ".crux/update.sh",
]

DEPRECATED_HOOK_COMMANDS = {
    "bash .cursor/hooks/detect-crux-changes.sh",
    ".cursor/hooks/detect-crux-changes.sh",
    "sh .cursor/hooks/detect-crux-changes.sh",
}


def cleanup_deprecated_files() -> None:
    """Remove files from older CRUX versions that have been renamed or replaced."""
    removed = 0
    for filepath in DEPRECATED_FILES:
        p = Path(filepath)
        if p.is_file():
            p.unlink()
            removed += 1
            log_verbose(f"Removed deprecated: {filepath}")

    for filepath in DEPRECATED_FILES:
        parent = Path(filepath).parent
        while parent != Path(".") and parent.is_dir():
            try:
                parent.rmdir()
                log_verbose(f"Removed empty directory: {parent}")
                parent = parent.parent
            except OSError:
                break

    if removed:
        log_success(f"Cleaned up {removed} deprecated file(s) from previous versions")


def cleanup_deprecated_hooks() -> None:
    """Remove stale CRUX hook commands from hooks.json."""
    hooks_path = Path(".cursor/hooks.json")
    if not hooks_path.is_file():
        return

    try:
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return

    hooks = data.get("hooks", {})
    if not hooks:
        return

    changed = False
    for lifecycle in list(hooks.keys()):
        arr = hooks.get(lifecycle)
        if not isinstance(arr, list):
            continue
        original_len = len(arr)
        arr[:] = [
            h for h in arr
            if not (isinstance(h, dict) and h.get("command") in DEPRECATED_HOOK_COMMANDS)
        ]
        if len(arr) < original_len:
            changed = True
            removed = original_len - len(arr)
            log_verbose(f"Removed {removed} deprecated hook(s) from {lifecycle}")
        if not arr:
            del hooks[lifecycle]

    if changed:
        data["hooks"] = hooks
        hooks_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        log_success("Cleaned up deprecated hooks from .cursor/hooks.json")


# ── Download ──


RELEASE_FILES = [
    "CRUX.md", "install.crux.md", ".crux/crux.json", ".crux/crux-release-files.json",
    ".cursor/hooks.json", ".cursor/agents/crux-cursor-rule-manager.md",
    ".cursor/commands/crux-compress.md",
    ".cursor/hooks/crux-detect-changes.py", ".cursor/hooks/crux-session-start.py",
    ".cursor/rules/_CRUX-RULE.mdc",
    ".cursor/skills/crux-utils/SKILL.md", ".cursor/skills/crux-utils/scripts/crux-utils.py",
]


def download_from_cdn(version: str, target_dir: Path) -> None:
    cdn_base = f"{JSDELIVR_CDN}@v{version}"
    succeeded = failed = 0

    for f in RELEASE_FILES:
        dest = target_dir / f
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = http_get(f"{cdn_base}/{f}")
        if data:
            dest.write_bytes(data)
            succeeded += 1
            log_verbose(f"Downloaded: {f}")
        else:
            failed += 1
            log_verbose(f"Skipped (not found): {f}")

    agents_data = http_get(f"{cdn_base}/AGENTS.md")
    if agents_data:
        text = agents_data.decode("utf-8")
        m = re.search(r"(<CRUX.*?</CRUX>)", text, re.DOTALL)
        if m:
            (target_dir / "AGENTS.crux.md").write_text(m.group(1) + "\n", encoding="utf-8")
            succeeded += 1
            log_verbose("Extracted: AGENTS.crux.md from AGENTS.md")
        else:
            failed += 1
    else:
        failed += 1

    if succeeded == 0:
        log_error("Failed to download any files from jsDelivr CDN")
        sys.exit(1)

    log_success(f"Downloaded {succeeded} files via jsDelivr CDN")
    if failed > 0:
        log_warn(f"{failed} files were not available (may be optional)")


def download_and_stage(version: str) -> Path:
    zip_name = f"CRUX-Compress-v{version}.zip"
    download_url = f"{DOWNLOAD_BASE}/v{version}/{zip_name}"

    staging = Path(tempfile.mkdtemp())
    content_dir = staging / "content"
    content_dir.mkdir()

    log(f"Downloading CRUX Compress v{version}...")
    log_verbose(f"URL: {download_url}")

    data = http_get(download_url)
    if data:
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                zf.extractall(content_dir)
            return content_dir
        except zipfile.BadZipFile:
            log_warn("Downloaded file is not a valid zip")

    log_warn("GitHub download failed, trying jsDelivr CDN...")
    download_from_cdn(version, content_dir)
    return content_dir


# ── Preview ──


def preview_installation(staging_dir: Path, show_diff: bool = False) -> None:
    print("\nFiles to be installed/updated:\n")

    for root, _dirs, files in os.walk(staging_dir):
        for fname in sorted(files):
            full = Path(root) / fname
            rel = str(full.relative_to(staging_dir))
            existing = Path(rel)

            if existing.is_file():
                if get_checksum(str(existing)) == get_checksum(str(full)):
                    print(f"  {BLUE}[NO CHANGE]{NC} {rel}")
                else:
                    print(f"  {YELLOW}[UPDATE]{NC} {rel}")
                    if show_diff:
                        try:
                            subprocess.run(
                                ["diff", "--color=always", "-u", str(existing), str(full)],
                                check=False,
                            )
                        except FileNotFoundError:
                            pass
                        print()
            else:
                print(f"  {GREEN}[CREATE]{NC} {rel}")

    print()


# ── Install ──


def install_from_staging(staging_dir: Path) -> None:
    log("Installing CRUX files...")

    staging_hooks = None
    hooks_src = staging_dir / ".cursor" / "hooks.json"
    if hooks_src.is_file():
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        shutil.copy2(str(hooks_src), tmp.name)
        staging_hooks = tmp.name
        hooks_src.unlink()

    for root, _dirs, files in os.walk(staging_dir):
        for fname in files:
            src = Path(root) / fname
            rel = src.relative_to(staging_dir)
            dest = Path(rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(src), str(dest))

    if staging_hooks:
        merge_hooks_json(staging_hooks)
        os.unlink(staging_hooks)

    if Path("AGENTS.crux.md").is_file():
        upsert_agents_crux_block("AGENTS.crux.md")

    for script in [".cursor/skills/crux-utils/scripts/crux-utils.py"]:
        p = Path(script)
        if p.is_file():
            p.chmod(p.stat().st_mode | 0o111)


def download_update_script() -> None:
    Path(".crux").mkdir(parents=True, exist_ok=True)
    log_verbose("Downloading update script...")

    for url in [f"{RAW_BASE}/install.py", f"{JSDELIVR_CDN}@main/install.py"]:
        data = http_get(url)
        if data:
            update_path = Path(".crux/update.py")
            update_path.write_bytes(data)
            update_path.chmod(update_path.stat().st_mode | 0o111)
            log_verbose(f"Update script saved to {update_path}")
            break
    else:
        log_warn("Could not download update script")

    for url in [f"{RAW_BASE}/install.crux.md", f"{JSDELIVR_CDN}@main/install.crux.md"]:
        data = http_get(url)
        if data:
            Path("install.crux.md").write_bytes(data)
            log_verbose("Installer reference saved to install.crux.md")
            break


DEFAULT_MEMORIES_CONFIG = {
    "platform": "cursor",
    "flags": [
        {"enableMemories": "false"},
        {"enableMemoryCompression": "false"},
    ],
    "cruxMemories": {
        "enabled": "${flags.enableMemories}",
        "compression": "${flags.enableMemoryCompression}",
        "storage": {
            "memoriesDir": "memories",
            "agentMemoriesDir": "memories/agents",
            "archiveDir": ".ai-ignored/executed",
            "compressionSourceArchive": ".ai-ignored/memories/sources",
            "indexFile": ".crux/memory-index.yml",
        },
        "sizeUnit": "lines",
        "compressionMinLines": 500,
        "maxMemorySize": 1000,
        "compressionTarget": 33,
        "unitOfWork": "spec",
        "commands": {
            "dream": {
                "file": ".cursor/commands/crux-dream.md",
                "default": "/crux-dream",
                "description": "Post-execution memory extraction and consolidation",
            },
            "mindReader": {
                "file": ".cursor/commands/crux-mindreader.md",
                "default": "/crux-mindreader",
                "description": "Decompress and view memories in chat",
            },
        },
        "hooks": {
            "sessionStartNudge": {
                "trigger": "sessionStart",
                "watchDir": "specs",
                "threshold": 20,
                "message": (
                    "Agent: I need a nap to process what we've been working on. "
                    "Run /crux-dream in a fresh thinking agent. "
                    "I'll wake up fresh and ready for our next spec after that!"
                ),
            },
        },
        "dream": {
            "maxCandidateFacts": 5,
            "maxUnrelatedChanges": 50,
            "stateFile": "_execution-state.yml",
            "workDir": "specs",
            "summaryPattern": "dream-{slug}-{yyyymmdd}.md",
        },
        "typePriority": ["core", "redflag", "goal", "learning", "idea", "archived"],
        "typeTransitions": {
            "idea": {"promoteAt": 5, "promoteTo": "learning"},
            "learning": {"promoteAt": 15, "promoteTo": "core"},
            "redflag": {"promoteAt": 10, "promoteTo": "core"},
            "core": {"promoteAt": None},
            "goal": {"promoteAt": None},
        },
        "demoteAfterDaysUnreferenced": 90,
        "archiveAfterDaysUnreferenced": 180,
        "referenceTracking": {
            "enabled": True,
            "trackingDir": ".crux/reference-tracking",
            "indicateInOutput": True,
            "indicatorFormat": "[memory:{title}]",
            "promotionToRuleThreshold": 30,
            "maxReferencesStored": 10,
        },
        "scopeRanking": ["base", "agents", "shared"],
        "scopes": {
            "base": {"memoriesDir": "memories", "readonly": False},
            "agents": {
                "memoriesDir": "memories/agents/{agent-id}",
                "readonly": False,
                "writeOnlyDuringDream": True,
                "boostSameType": True,
            },
            "shared": [],
        },
    },
}


def setup_memories() -> bool:
    """Create memory system scaffolding. Returns True on success."""
    config_path = Path(".crux/crux-memories.json")
    memories_dir = Path("memories")
    agents_dir = Path("memories/agents")
    tracking_dir = Path(".crux/reference-tracking")

    if config_path.is_file():
        log_warn(f"{config_path} already exists, skipping memory config creation")
    else:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            json.dumps(DEFAULT_MEMORIES_CONFIG, indent=2) + "\n",
            encoding="utf-8",
        )
        log_success(f"Created {config_path}")

    for d in (memories_dir, agents_dir, tracking_dir):
        d.mkdir(parents=True, exist_ok=True)
        log_verbose(f"Created directory: {d}")

    print()
    print(f"{CYAN}Memory System Scaffolding{NC}")
    print(f"{'─' * 40}")
    print(f"  Config:   {config_path}")
    print(f"  Storage:  {memories_dir}/")
    print(f"  Tracking: {tracking_dir}/")
    print()
    print("To enable memories:")
    print(f"  1. Set {CYAN}enableMemories{NC} to {GREEN}\"true\"{NC} in {config_path}")
    print("  2. Optionally configure MCP server for semantic search")
    print("  3. Use /crux-dream after completing specs to extract learnings")
    print()

    return True


def show_completion_report(version: str, backup_zip: str, with_memories: bool = False) -> None:
    print()
    print(f"{GREEN}{'=' * 43}{NC}")
    print(f"{GREEN}     Installation Complete!{NC}")
    print(f"{GREEN}{'=' * 43}{NC}")
    print()
    log_success(f"CRUX Compress v{version} installed successfully!")
    print()

    if backup_zip and Path(backup_zip).is_file():
        print("Backup saved to:")
        print(f"  {backup_zip}")
        print()
        print("To revert this update:")
        print(f"  {CYAN}# Remove installed CRUX files{NC}")
        print("  rm -rf .crux .cursor/agents/crux-cursor-rule-manager.md \\")
        print("         .cursor/commands/crux-compress.md \\")
        print("         .cursor/hooks/crux-detect-changes.py \\")
        print("         .cursor/hooks/crux-session-start.py \\")
        print("         .cursor/rules/_CRUX-RULE.mdc \\")
        print("         .cursor/skills/crux-utils CRUX.md install.crux.md")
        print()
        print(f"  {CYAN}# Restore from backup{NC}")
        print(f"  unzip -o '{backup_zip}'")
        print()

    if with_memories:
        print(f"{CYAN}Memories:{NC}")
        print("  Memory system scaffolding installed (disabled by default).")
        print("  To enable: set enableMemories to \"true\" in .crux/crux-memories.json")
        print()

    print("Next steps:")
    print("  1. Ensure .cursor/hooks.json is recognized by Cursor")
    print("  2. Add 'crux: true' to any rule files you want to compress")
    print("  3. Use /crux-compress ALL to compress eligible files")
    if not with_memories:
        print("  4. Run with --with-memories to add optional memory system")
    print()
    print("For updates, run:")
    print("  python3 .crux/update.py")
    print()
    print(f"Documentation: https://github.com/{REPO_OWNER}/{REPO_NAME}")
    print()


# ── Main ──


def main() -> None:
    global VERBOSE, NON_INTERACTIVE

    parser = argparse.ArgumentParser(
        description="CRUX Compress Installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="This script installs CRUX Compress into the current directory.\n"
               "It will create/update .cursor/ directory structure and add core files.",
    )
    parser.add_argument("-y", action="store_true", help="Non-interactive mode")
    parser.add_argument("--force", action="store_true", help="Backup and install regardless of version")
    parser.add_argument("--backup", action="store_true", help="Create backups of existing files")
    parser.add_argument("--verbose", action="store_true", help="Show detailed progress")
    parser.add_argument("--with-memories", action="store_true",
                        help="Set up optional memory system scaffolding")
    args = parser.parse_args()

    VERBOSE = args.verbose
    NON_INTERACTIVE = args.y
    do_backup = args.backup
    force = args.force
    with_memories = args.with_memories
    if force:
        do_backup = True

    os.system("clear 2>/dev/null || true")
    print()
    print(f"{BLUE}{'=' * 43}{NC}")
    print(f"{BLUE}     CRUX Compress Installer{NC}")
    print(f"{BLUE}{'=' * 43}{NC}")
    print()

    check_not_in_crux_repo()

    for tool in ("curl",):
        if not shutil.which(tool):
            log_warn(f"{tool} not found (may be needed for fallback downloads)")

    git_root = detect_git_root()
    if git_root:
        log_verbose(f"Git repository detected: {git_root}")
        os.chdir(git_root)
    else:
        log_warn("Not in a git repository.")
        print("\nIt's recommended to run this script from an initialized git repository.")
        print("You can initialize one with: git init\n")
        if not confirm("Continue anyway and treat current directory as project root?"):
            log("Installation cancelled.")
            sys.exit(0)

    log("Checking for latest version...")
    latest_version = get_latest_version()
    installed_version = get_installed_version()

    backup_zip = ""

    if installed_version:
        log(f"Detected CRUX version: {installed_version}")
        log(f"Latest version: v{latest_version}")
        print()

        cmp = compare_versions(latest_version, installed_version)
        if cmp == 0:
            change_type = get_version_change_type(installed_version, latest_version)
            if change_type == "major":
                print(f"{YELLOW}MAJOR version update ({installed_version} -> {latest_version}){NC}")
                log_warn("This is a major version update!")
                print("After installation, regenerate all CRUX files using:")
                print("  /crux-compress ALL --force\n")
            elif change_type == "minor":
                print(f"{CYAN}Minor version update ({installed_version} -> {latest_version}){NC}\n")
            else:
                print(f"{GREEN}Patch update ({installed_version} -> {latest_version}){NC}\n")
        elif cmp == 1:
            log_warn(f"Already at latest version (v{installed_version})")
            if force:
                log("Force reinstall requested...")
            else:
                print("To reinstall anyway, run with --force")
                sys.exit(0)
        else:
            log_warn(f"Installed version (v{installed_version}) is newer than latest release (v{latest_version})")
            if not force and not confirm("Downgrade?"):
                log("Installation cancelled.")
                sys.exit(0)

        if do_backup:
            backup_zip = create_backup_zip()
            if backup_zip:
                log_success(f"Backup created: {backup_zip}")
    else:
        log(f"Fresh installation of v{latest_version}")

    staging_dir = download_and_stage(latest_version)
    preview_installation(staging_dir, VERBOSE)

    if not confirm("Proceed with installation?"):
        shutil.rmtree(staging_dir.parent, ignore_errors=True)
        log("Installation cancelled.")
        sys.exit(0)

    install_from_staging(staging_dir)
    shutil.rmtree(staging_dir.parent, ignore_errors=True)
    cleanup_deprecated_files()
    cleanup_deprecated_hooks()
    download_update_script()

    if with_memories:
        setup_memories()

    show_completion_report(latest_version, backup_zip, with_memories=with_memories)


if __name__ == "__main__":
    main()
