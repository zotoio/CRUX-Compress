"""Category E: Memory Index tests.

Validates index building via memory-index.py subprocess, prioritisation order,
agent-scoped memory inclusion, and rebuild-after-delete.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

from conftest import write_memory, write_tracker

SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / ".cursor"
    / "skills"
    / "crux-skill-memory-index"
    / "scripts"
    / "memory-index.py"
)


def _make_config(tmp_path: Path, memories_dir: str = "memories") -> Path:
    crux_dir = tmp_path / ".crux"
    crux_dir.mkdir(parents=True, exist_ok=True)

    cfg = {
        "platform": "cursor",
        "flags": [{"enableMemories": "true"}],
        "cruxMemories": {
            "enabled": "true",
            "storage": {
                "memoriesDir": memories_dir,
                "agentMemoriesDir": f"{memories_dir}/agents",
                "archiveDir": ".ai-ignored/executed",
                "indexFile": ".crux/memory-index.yml",
            },
            "sizeUnit": "lines",
            "compressionMinLines": 500,
            "maxMemorySize": 1000,
            "unitOfWork": "spec",
            "typePriority": ["core", "redflag", "goal", "learning", "idea", "archived"],
            "referenceTracking": {
                "enabled": True,
                "trackingDir": ".crux/reference-tracking",
                "maxReferencesStored": 10,
            },
        },
    }
    config_path = crux_dir / "crux-memories.json"
    config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return config_path


def _run_index(config_path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--config", str(config_path)],
        capture_output=True,
        text=True,
        cwd=str(config_path.parent.parent),
    )


def _load_index(tmp_path: Path) -> dict:
    index_path = tmp_path / ".crux" / "memory-index.yml"
    return yaml.safe_load(index_path.read_text(encoding="utf-8"))


class TestIndexBuilding:
    """Creating memories across type directories and running the index script."""

    def test_index_created_with_entries(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        config_path = _make_config(tmp_path)

        write_memory(mem_dir, "core-insight", mem_type="core", strength=5)
        write_memory(mem_dir, "learning-one", mem_type="learning", strength=2)
        write_memory(mem_dir, "idea-one", mem_type="idea", strength=1)

        result = _run_index(config_path)
        assert result.returncode == 0, f"Index script failed: {result.stderr}"

        index = _load_index(tmp_path)
        assert "memories" in index
        assert len(index["memories"]) == 3

    def test_index_yaml_output_format(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        config_path = _make_config(tmp_path)

        write_memory(mem_dir, "format-check", mem_type="learning")

        _run_index(config_path)
        index = _load_index(tmp_path)

        entry = index["memories"][0]
        expected_keys = {"slug", "title", "description", "type", "strength", "references", "tags", "file"}
        assert expected_keys.issubset(entry.keys()), (
            f"Missing keys: {expected_keys - entry.keys()}"
        )


class TestPrioritisation:
    """Index entries are sorted by typePriority, then strength desc, then references desc."""

    def test_type_priority_order(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        config_path = _make_config(tmp_path)

        write_memory(mem_dir, "an-idea", mem_type="idea", strength=1)
        write_memory(mem_dir, "a-core", mem_type="core", strength=1)
        write_memory(mem_dir, "a-learning", mem_type="learning", strength=1)
        write_memory(mem_dir, "a-redflag", mem_type="redflag", strength=1)

        _run_index(config_path)
        index = _load_index(tmp_path)

        types = [e["type"] for e in index["memories"]]
        priority = ["core", "redflag", "goal", "learning", "idea", "archived"]
        type_ranks = {t: i for i, t in enumerate(priority)}
        ranks = [type_ranks[t] for t in types]
        assert ranks == sorted(ranks), f"Types not in priority order: {types}"

    def test_strength_descending_within_type(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        config_path = _make_config(tmp_path)

        write_memory(mem_dir, "weak-learning", mem_type="learning", strength=1)
        write_memory(mem_dir, "strong-learning", mem_type="learning", strength=10)
        write_memory(mem_dir, "mid-learning", mem_type="learning", strength=5)

        _run_index(config_path)
        index = _load_index(tmp_path)

        learnings = [e for e in index["memories"] if e["type"] == "learning"]
        strengths = [e["strength"] for e in learnings]
        assert strengths == sorted(strengths, reverse=True), (
            f"Strengths not descending: {strengths}"
        )

    def test_references_tiebreak(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        config_path = _make_config(tmp_path)

        write_memory(mem_dir, "few-refs", mem_type="learning", strength=5)
        write_memory(mem_dir, "many-refs", mem_type="learning", strength=5)

        write_tracker(tracking_dir, "few-refs", references=2, strength=5)
        write_tracker(tracking_dir, "many-refs", references=20, strength=5)

        _run_index(config_path)
        index = _load_index(tmp_path)

        learnings = [e for e in index["memories"] if e["type"] == "learning"]
        assert learnings[0]["slug"] == "many-refs", (
            "Higher reference count should sort first at same strength"
        )


class TestAgentScopedInclusion:
    """Agent-scoped memories are included in the index with correct paths."""

    def test_agent_memories_in_index(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        config_path = _make_config(tmp_path)

        write_memory(mem_dir, "base-mem", mem_type="core")
        write_memory(mem_dir, "agent-mem", mem_type="learning", agent_id="code-reviewer")

        _run_index(config_path)
        index = _load_index(tmp_path)

        slugs = [e["slug"] for e in index["memories"]]
        assert "base-mem" in slugs
        assert "agent-mem" in slugs

    def test_agent_memory_path_contains_agent_id(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        config_path = _make_config(tmp_path)

        write_memory(mem_dir, "reviewer-insight", mem_type="core", agent_id="code-reviewer")

        _run_index(config_path)
        index = _load_index(tmp_path)

        entry = next(e for e in index["memories"] if e["slug"] == "reviewer-insight")
        assert "agents/code-reviewer" in entry["file"]


class TestRebuildAfterDelete:
    """Deleting a memory and rebuilding the index removes it."""

    def test_deleted_memory_removed_from_index(self, tmp_path: Path):
        mem_dir = tmp_path / "memories"
        config_path = _make_config(tmp_path)

        write_memory(mem_dir, "keep-me", mem_type="core")
        doomed = write_memory(mem_dir, "delete-me", mem_type="idea")

        _run_index(config_path)
        index = _load_index(tmp_path)
        slugs = [e["slug"] for e in index["memories"]]
        assert "delete-me" in slugs

        doomed.unlink()

        _run_index(config_path)
        index = _load_index(tmp_path)
        slugs = [e["slug"] for e in index["memories"]]
        assert "delete-me" not in slugs
        assert "keep-me" in slugs
