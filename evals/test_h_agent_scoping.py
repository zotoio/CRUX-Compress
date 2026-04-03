"""Category H: Agent Scoping tests.

Validates agent-specific directory placement, general-purpose base placement,
agent isolation (cannot read other agent dirs), and dream-only write metadata.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

from conftest import MEMORY_TYPES, _make_config, write_memory


def _parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    return yaml.safe_load(parts[1])


class TestAgentDirectoryPlacement:
    """Agent-specific memories go to agents/{id}/{type}/."""

    def test_agent_memory_in_agent_dir(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        path = write_memory(
            mem_dir, "agent-finding", mem_type="learning", agent_id="code-reviewer",
        )

        rel = path.relative_to(mem_dir)
        parts = rel.parts
        assert parts[0] == "agents"
        assert parts[1] == "code-reviewer"
        assert parts[2] == "learning"

    def test_agent_memory_per_type(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        for t in ("core", "learning", "idea", "redflag"):
            path = write_memory(
                mem_dir, f"agent-{t}", mem_type=t, agent_id="planner",
            )
            assert path.parent.name == t
            assert "agents" in path.parts
            assert "planner" in path.parts

    def test_multiple_agents_separate_dirs(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        p1 = write_memory(mem_dir, "insight-a", mem_type="core", agent_id="agent-alpha")
        p2 = write_memory(mem_dir, "insight-b", mem_type="core", agent_id="agent-beta")

        assert "agent-alpha" in p1.parts
        assert "agent-beta" in p2.parts
        assert p1.parent != p2.parent


class TestBaseDirectoryPlacement:
    """General-purpose memories go to memories/{type}/ (no agent prefix)."""

    def test_base_memory_no_agents_dir(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        path = write_memory(mem_dir, "general-insight", mem_type="learning")

        rel = path.relative_to(mem_dir)
        assert "agents" not in rel.parts

    def test_base_memory_in_type_dir(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        for t in MEMORY_TYPES:
            if t == "archived":
                continue
            path = write_memory(mem_dir, f"base-{t}", mem_type=t)
            assert path.parent.name == t


class TestAgentIsolation:
    """An agent can only access its own directory and base; not other agent dirs."""

    def test_agent_reads_own_and_base(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        scopes = cfg["cruxMemories"]["scopes"]

        base_dir = tmp_path / scopes["base"]["memoriesDir"]
        agent_dir_template = scopes["agents"]["memoriesDir"]
        agent_dir = tmp_path / agent_dir_template.replace("{agent-id}", "code-reviewer")

        for d in (base_dir, agent_dir):
            for t in MEMORY_TYPES:
                (d / t).mkdir(parents=True, exist_ok=True)

        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "base-mem", mem_type="core")
        write_memory(mem_dir, "reviewer-mem", mem_type="core", agent_id="code-reviewer")

        base_files = list(base_dir.rglob("*.memory.md"))
        agent_files = list(agent_dir.rglob("*.memory.md"))

        accessible = base_files + agent_files
        assert len(accessible) >= 2

    def test_agent_cannot_see_other_agent(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        write_memory(mem_dir, "alpha-secret", mem_type="core", agent_id="agent-alpha")
        write_memory(mem_dir, "beta-secret", mem_type="core", agent_id="agent-beta")

        cfg = _make_config(tmp_path)
        agent_dir_template = cfg["cruxMemories"]["scopes"]["agents"]["memoriesDir"]

        beta_dir = tmp_path / agent_dir_template.replace("{agent-id}", "agent-beta")
        beta_files = list(beta_dir.rglob("*.memory.md"))
        beta_slugs = [p.stem.replace(".memory", "") for p in beta_files]

        assert "alpha-secret" not in beta_slugs
        assert any("beta-secret" in s for s in beta_slugs)


class TestDreamOnlyWrite:
    """Agent memories should only be written during dream (metadata check)."""

    def test_agent_scope_write_only_during_dream(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        agent_scope = cfg["cruxMemories"]["scopes"]["agents"]
        assert agent_scope.get("writeOnlyDuringDream") is True

    def test_agent_scope_boost_same_type(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        agent_scope = cfg["cruxMemories"]["scopes"]["agents"]
        assert agent_scope.get("boostSameType") is True

    def test_base_scope_no_dream_restriction(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        base_scope = cfg["cruxMemories"]["scopes"]["base"]
        assert "writeOnlyDuringDream" not in base_scope or base_scope["writeOnlyDuringDream"] is False
