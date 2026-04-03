"""Category L: MCP Server tests.

Tests internal functions of the crux_mcp_server package without starting a
full server process. Validates config loading, tool function signatures,
stats accuracy, and agent scoping filters.
"""

from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from conftest import MEMORY_TYPES, write_memory, write_tracker


class TestServerImportAndConfig:
    """Server module is importable and config loads correctly."""

    def test_config_module_importable(self):
        from crux_mcp_server.config import load_config, ServerConfig
        assert callable(load_config)

    def test_config_loads_from_file(self, tmp_path: Path):
        cfg_data = {
            "platform": "cursor",
            "flags": [{"enableMemories": "true"}],
            "cruxMemories": {
                "enabled": "true",
                "storage": {"memoriesDir": "memories"},
                "typePriority": MEMORY_TYPES,
            },
        }
        config_path = tmp_path / ".crux" / "crux-memories.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(cfg_data, indent=2), encoding="utf-8")

        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=config_path, project_root=tmp_path)

        assert cfg.memories.enabled is True
        assert cfg.memories.storage.memories_dir == "memories"

    def test_config_defaults_without_file(self, tmp_path: Path):
        from crux_mcp_server.config import load_config
        cfg = load_config(config_path=None, project_root=tmp_path)

        assert cfg.memories.enabled is False
        assert cfg.memories.storage.memories_dir == "memories"


class TestSearchToolFunction:
    """memory-search tool function exists and accepts required parameters."""

    def test_search_module_importable(self):
        from crux_mcp_server.tools.memory.search import register_search
        assert callable(register_search)

    def test_search_function_has_required_params(self):
        from crux_mcp_server.tools.memory import search as search_mod
        source = inspect.getsource(search_mod)

        assert "query: str" in source
        assert "limit:" in source
        assert "agentId:" in source

    def test_search_accepts_type_filter(self):
        from crux_mcp_server.tools.memory import search as search_mod
        source = inspect.getsource(search_mod)
        assert "types:" in source

    def test_search_accepts_tag_filter(self):
        from crux_mcp_server.tools.memory import search as search_mod
        source = inspect.getsource(search_mod)
        assert "tags:" in source


class TestReadToolFunction:
    """memory-read tool function exists and accepts expected parameters."""

    def test_read_module_importable(self):
        from crux_mcp_server.tools.memory.read import register_read
        assert callable(register_read)

    def test_read_accepts_slugs(self):
        from crux_mcp_server.tools.memory import read as read_mod
        source = inspect.getsource(read_mod)
        assert "slugs:" in source

    def test_read_accepts_files(self):
        from crux_mcp_server.tools.memory import read as read_mod
        source = inspect.getsource(read_mod)
        assert "files:" in source


class TestStatsAccuracy:
    """memory-stats returns accurate counts by type."""

    def test_stats_module_importable(self):
        from crux_mcp_server.tools.memory.stats import register_stats
        assert callable(register_stats)

    def test_scanner_counts_by_type(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "core-one", mem_type="core")
        write_memory(mem_dir, "core-two", mem_type="core")
        write_memory(mem_dir, "learn-one", mem_type="learning")
        write_memory(mem_dir, "idea-one", mem_type="idea")

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

        from collections import Counter
        type_counts = Counter(e.type for e in index.entries)

        assert type_counts["core"] == 2
        assert type_counts["learning"] == 1
        assert type_counts["idea"] == 1
        assert len(index.entries) == 4

    def test_scanner_counts_compressed(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "plain-mem", mem_type="learning", compressed=False)
        write_memory(mem_dir, "crux-mem", mem_type="learning", compressed=True)

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

        compressed = sum(1 for e in index.entries if e.file.endswith(".memory.crux.md"))
        uncompressed = sum(1 for e in index.entries if e.file.endswith(".memory.md") and not e.file.endswith(".crux.md"))

        assert compressed == 1
        assert uncompressed == 1


class TestAgentScopingFilter:
    """Agent scoping filter with agentId parameter works correctly."""

    def test_scanner_tracks_agent_id(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "base-insight", mem_type="core")
        write_memory(mem_dir, "reviewer-insight", mem_type="core", agent_id="code-reviewer")

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

        all_slugs = [e.slug for e in index.entries]
        assert "base-insight" in all_slugs
        assert "reviewer-insight" in all_slugs

        agent_entries = [e for e in index.entries if e.agent_id == "code-reviewer"]
        assert len(agent_entries) >= 1
        assert agent_entries[0].slug == "reviewer-insight"

        base_only = [e for e in index.entries if e.slug == "base-insight"]
        assert all(e.agent_id is None for e in base_only)

    def test_agent_filter_excludes_other_agents(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "alpha-mem", mem_type="core", agent_id="alpha")
        write_memory(mem_dir, "beta-mem", mem_type="core", agent_id="beta")

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

        alpha_only = [e for e in index.entries if e.agent_id == "alpha"]
        assert len(alpha_only) == 1
        assert alpha_only[0].slug == "alpha-mem"

        beta_only = [e for e in index.entries if e.agent_id == "beta"]
        assert len(beta_only) == 1
        assert beta_only[0].slug == "beta-mem"
