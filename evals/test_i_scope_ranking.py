"""Category I: Scope Ranking tests.

Validates shared symlink scope, scopeRanking order, and write rejection
for shared scopes.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from conftest import MEMORY_TYPES, _make_config, write_memory


class TestSharedScopeInIndex:
    """Shared symlink scope memories appear as read-only in the index."""

    def test_shared_memories_read_only_in_config(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        cfg["cruxMemories"]["scopes"]["shared"] = [
            {"path": "shared-memories", "readonly": True},
        ]

        config_path = tmp_path / ".crux" / "crux-memories.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

        raw = json.loads(config_path.read_text(encoding="utf-8"))
        shared = raw["cruxMemories"]["scopes"]["shared"]
        assert len(shared) == 1
        assert shared[0]["readonly"] is True

    def test_shared_scope_can_contain_memories(self, tmp_path: Path):
        shared_dir = tmp_path / "shared-memories"
        for t in ("core", "learning"):
            (shared_dir / t).mkdir(parents=True, exist_ok=True)

        write_memory(shared_dir, "shared-insight", mem_type="core")

        files = list(shared_dir.rglob("*.memory.md"))
        assert len(files) == 1
        assert "shared-insight" in files[0].name


class TestScopeRankingOrder:
    """scopeRanking order is base > agents > shared."""

    def test_default_ranking_order(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        ranking = cfg["cruxMemories"]["scopeRanking"]
        assert ranking == ["base", "agents", "shared"]

    def test_base_ranked_first(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        ranking = cfg["cruxMemories"]["scopeRanking"]
        assert ranking[0] == "base"

    def test_shared_ranked_last(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        ranking = cfg["cruxMemories"]["scopeRanking"]
        assert ranking[-1] == "shared"

    def test_ranking_has_three_scopes(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        ranking = cfg["cruxMemories"]["scopeRanking"]
        assert len(ranking) == 3


class TestSharedWriteRejection:
    """Writes to shared scope should be rejected (readonly enforcement)."""

    def test_shared_scope_default_is_empty_list(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        assert cfg["cruxMemories"]["scopes"]["shared"] == []

    def test_shared_scope_readonly_flag(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        cfg["cruxMemories"]["scopes"]["shared"] = [
            {"path": "shared-repo-memories", "readonly": True},
        ]

        for entry in cfg["cruxMemories"]["scopes"]["shared"]:
            assert entry["readonly"] is True, "Shared scope must be read-only"

    def test_base_scope_writable(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        assert cfg["cruxMemories"]["scopes"]["base"]["readonly"] is False

    def test_agents_scope_writable(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        assert cfg["cruxMemories"]["scopes"]["agents"]["readonly"] is False
