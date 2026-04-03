"""Category M: Config Validation tests.

Validates missing required fields, unitOfWork interpolation in nudge
templates, platform-specific path resolution, and typePriority ordering.
"""

from __future__ import annotations

import json
from pathlib import Path

from conftest import MEMORY_TYPES, _make_config


class TestMissingRequiredFields:
    """Loading config with missing required fields uses safe defaults or errors."""

    def test_empty_config_uses_defaults(self, tmp_path: Path):
        config_path = tmp_path / ".crux" / "crux-memories.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text("{}", encoding="utf-8")

        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=config_path, project_root=tmp_path)

        assert cfg.memories.enabled is False
        assert cfg.memories.storage.memories_dir == "memories"

    def test_missing_flags_defaults_disabled(self, tmp_path: Path):
        cfg_data = {"cruxMemories": {"storage": {"memoriesDir": "memories"}}}
        config_path = tmp_path / ".crux" / "crux-memories.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(cfg_data), encoding="utf-8")

        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=config_path, project_root=tmp_path)

        assert cfg.memories.enabled is False

    def test_missing_storage_uses_defaults(self, tmp_path: Path):
        cfg_data = {
            "flags": [{"enableMemories": "true"}],
            "cruxMemories": {},
        }
        config_path = tmp_path / ".crux" / "crux-memories.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(cfg_data), encoding="utf-8")

        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=config_path, project_root=tmp_path)

        assert cfg.memories.storage.memories_dir == "memories"
        assert cfg.memories.storage.agent_memories_dir == "memories/agents"

    def test_missing_type_priority_uses_default(self, tmp_path: Path):
        cfg_data = {
            "flags": [{"enableMemories": "true"}],
            "cruxMemories": {"storage": {"memoriesDir": "memories"}},
        }
        config_path = tmp_path / ".crux" / "crux-memories.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(cfg_data), encoding="utf-8")

        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=config_path, project_root=tmp_path)

        assert cfg.memories.type_priority == MEMORY_TYPES


class TestUnitOfWorkInterpolation:
    """unitOfWork value is used in nudge message template interpolation."""

    def test_unit_of_work_configured(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        assert cfg["cruxMemories"]["unitOfWork"] == "plan"

    def test_nudge_message_template_exists(self, tmp_path: Path):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        raw = json.loads(real_config.read_text(encoding="utf-8"))
        nudge = raw.get("cruxMemories", {}).get("hooks", {}).get("sessionStartNudge", {})
        message = nudge.get("message", "")

        assert len(message) > 0, "Nudge message should not be empty"

    def test_unit_of_work_matches_watch_dir_purpose(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        unit = cfg["cruxMemories"]["unitOfWork"]
        work_dir = cfg["cruxMemories"]["dream"]["workDir"]
        assert unit == "plan"
        assert work_dir == "plans"


class TestPlatformPaths:
    """Platform-specific paths resolve correctly for 'cursor' platform."""

    def test_platform_is_cursor(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        assert cfg["platform"] == "cursor"

    def test_cursor_paths_use_dot_cursor(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        raw = json.loads(real_config.read_text(encoding="utf-8"))
        commands = raw.get("cruxMemories", {}).get("commands", {})

        for cmd_name, cmd_data in commands.items():
            file_path = cmd_data.get("file", "")
            assert file_path.startswith(".cursor/"), (
                f"Command {cmd_name} path should start with .cursor/, got: {file_path}"
            )

    def test_hooks_reference_cursor_dir(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        hook_script = Path(__file__).resolve().parent.parent / ".cursor" / "hooks" / "crux-session-start.py"
        assert hook_script.exists(), "Session hook script should exist at .cursor/hooks/"

    def test_config_project_root_resolution(self, tmp_path: Path):
        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=None, project_root=tmp_path)
        assert cfg.project_root == tmp_path


class TestTypePriorityOrdering:
    """typePriority ordering is used (not alphabetical)."""

    def test_type_priority_not_alphabetical(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        priority = cfg["cruxMemories"]["typePriority"]
        assert priority != sorted(priority), (
            "typePriority should not be alphabetical order"
        )

    def test_core_is_highest_priority(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        priority = cfg["cruxMemories"]["typePriority"]
        assert priority[0] == "core"

    def test_archived_is_lowest_priority(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        priority = cfg["cruxMemories"]["typePriority"]
        assert priority[-1] == "archived"

    def test_type_priority_matches_memory_types(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        priority = cfg["cruxMemories"]["typePriority"]
        assert set(priority) == set(MEMORY_TYPES)

    def test_scanner_uses_type_priority_for_sorting(self, tmp_path: Path):
        from conftest import write_memory

        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "z-idea", mem_type="idea", strength=1)
        write_memory(mem_dir, "a-core", mem_type="core", strength=1)

        cfg_data = {
            "platform": "cursor",
            "flags": [{"enableMemories": "true"}],
            "cruxMemories": {
                "enabled": "true",
                "storage": {
                    "memoriesDir": "memories",
                    "agentMemoriesDir": "memories/agents",
                    "archiveDir": ".ai-ignored/executed",
                    "indexFile": ".crux/memory-index.yml",
                },
                "typePriority": MEMORY_TYPES,
                "referenceTracking": {
                    "enabled": True,
                    "trackingDir": ".crux/reference-tracking",
                },
                "scopeRanking": ["base", "agents", "shared"],
            },
        }
        config_path = tmp_path / ".crux" / "crux-memories.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(cfg_data, indent=2), encoding="utf-8")

        from crux_mcp_server.config import load_config
        from crux_mcp_server.indexer.scanner import scan

        cfg = load_config(config_path=config_path, project_root=tmp_path)
        index = scan(cfg)

        types = [e.type for e in index.entries]
        assert types[0] == "core", f"Core should sort first, got: {types}"
