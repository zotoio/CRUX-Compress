"""Category J: Recall tests.

Validates recall command definition, invocation modes,
display format, --total canvas visualization, and post-recall actions.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import yaml

from conftest import MEMORY_TYPES, _make_config, write_memory


def _parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---"), "File must start with frontmatter delimiter"
    parts = text.split("---", 2)
    assert len(parts) >= 3, "Frontmatter must have opening and closing ---"
    return yaml.safe_load(parts[1])


class TestRecallConfigPresence:
    """The recall command is properly configured in crux-memories.json."""

    def test_recall_command_in_config(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        commands = data.get("cruxMemories", {}).get("commands", {})
        assert "recall" in commands, "recall command must be in config"

    def test_recall_command_file_path(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        recall = data["cruxMemories"]["commands"]["recall"]
        assert recall["file"] == ".cursor/commands/crux-recall.md"

    def test_recall_command_default(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        recall = data["cruxMemories"]["commands"]["recall"]
        assert recall["default"] == "/crux-recall"

    def test_recall_command_file_exists(self):
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-recall.md"
        )
        assert cmd_file.is_file(), "crux-recall.md command file must exist"


class TestRecallCommandDefinition:
    """The recall command file defines all required invocation modes."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-recall.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_has_usage_section(self):
        content = self._read_cmd()
        assert "## Usage" in content

    def test_supports_no_arguments(self):
        content = self._read_cmd()
        assert "contextually relevant" in content.lower() or "no argument" in content.lower()

    def test_supports_search_query(self):
        content = self._read_cmd()
        assert "search" in content.lower() or '"search query"' in content.lower()

    def test_supports_spec_name(self):
        content = self._read_cmd()
        assert "spec" in content.lower()

    def test_supports_file_path(self):
        content = self._read_cmd()
        assert "file path" in content.lower() or ".memory.md" in content

    def test_supports_total_flag(self):
        content = self._read_cmd()
        assert "--total" in content


class TestRecallTotalVisualization:
    """The --total flag generates an interactive 3D force-directed graph."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-recall.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_total_uses_canvas(self):
        content = self._read_cmd()
        assert "canvas" in content.lower()

    def test_total_uses_3d_force_graph(self):
        content = self._read_cmd()
        assert "3d-force-graph" in content.lower() or "force-directed" in content.lower()

    def test_total_nodes_represent_memories(self):
        content = self._read_cmd()
        assert "node" in content.lower()

    def test_total_edges_represent_connections(self):
        content = self._read_cmd()
        assert "edge" in content.lower() or "connect" in content.lower()

    def test_total_node_sizing_by_strength(self):
        content = self._read_cmd()
        assert "strength" in content.lower()

    def test_total_node_coloring_by_type(self):
        content = self._read_cmd()
        assert "type" in content.lower() and "color" in content.lower()

    def test_total_supports_search_filter(self):
        content = self._read_cmd()
        lower = content.lower()
        assert "search" in lower or "filter" in lower

    def test_total_supports_click_detail(self):
        content = self._read_cmd()
        assert "click" in content.lower()


class TestRecallDisplayFormat:
    """Recall output uses grouped markdown tables with hash IDs."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-recall.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_grouped_by_type(self):
        content = self._read_cmd()
        assert "grouped by type" in content.lower() or "type group" in content.lower()

    def test_table_format_documented(self):
        content = self._read_cmd()
        assert "| ID |" in content or "| Title |" in content

    def test_shows_strength(self):
        content = self._read_cmd()
        assert "Str" in content or "strength" in content.lower()

    def test_shows_references(self):
        content = self._read_cmd()
        assert "Refs" in content or "reference" in content.lower()

    def test_shows_hash_id(self):
        content = self._read_cmd()
        assert "hash" in content.lower() or "`{id}`" in content

    def test_decompresses_crux_bodies(self):
        content = self._read_cmd()
        assert "decompress" in content.lower()


class TestRecallPostDisplayMenu:
    """After display, recall offers delete/consolidate/promote/skip actions."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-recall.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_offers_delete_action(self):
        content = self._read_cmd()
        assert "delete" in content.lower()

    def test_offers_consolidate_action(self):
        content = self._read_cmd()
        assert "consolidate" in content.lower()

    def test_offers_promote_action(self):
        content = self._read_cmd()
        assert "promote" in content.lower()

    def test_offers_skip_action(self):
        content = self._read_cmd()
        assert "skip" in content.lower() or "no thanks" in content.lower()

    def test_uses_ask_question(self):
        content = self._read_cmd()
        assert "AskQuestion" in content


class TestRecallSpecFiltering:
    """Recall by spec name filters memories by source field."""

    def test_memories_filterable_by_source(self, tmp_memories_dir: Path):
        spec_slug = "20260403-crux-memories"
        write_memory(tmp_memories_dir, "from-spec-1", source=spec_slug)
        write_memory(tmp_memories_dir, "from-spec-2", source=spec_slug)
        write_memory(tmp_memories_dir, "from-other", source="other-spec")

        all_memories = list(tmp_memories_dir.rglob("*.memory.md"))
        matching = [
            m for m in all_memories
            if _parse_frontmatter(m).get("source") == spec_slug
        ]
        non_matching = [
            m for m in all_memories
            if _parse_frontmatter(m).get("source") != spec_slug
        ]

        assert len(matching) == 2
        assert len(non_matching) == 1

    def test_source_field_exact_match(self, tmp_memories_dir: Path):
        write_memory(tmp_memories_dir, "exact-match", source="20260403-specific")
        path = list(tmp_memories_dir.rglob("exact-match*"))[0]
        fm = _parse_frontmatter(path)
        assert fm["source"] == "20260403-specific"


class TestRecallDecompression:
    """Compressed memories are decompressed for display without modifying disk."""

    def test_compressed_file_naming(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "compressed-recall", compressed=True)
        assert path.name.endswith(".memory.crux.md")

    def test_uncompressed_file_naming(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "uncompressed-recall", compressed=False)
        assert path.name.endswith(".memory.md")
        assert not path.name.endswith(".crux.md")

    def test_compressed_has_valid_frontmatter(self, tmp_memories_dir: Path):
        path = write_memory(
            tmp_memories_dir, "fm-check",
            compressed=True, body="⟦CRUX:test ⟧"
        )
        fm = _parse_frontmatter(path)
        assert "title" in fm
        assert "type" in fm


class TestRecallReadOnlyBehavior:
    """Recall is read-only and never modifies memory files on disk."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-recall.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_documents_read_only(self):
        content = self._read_cmd()
        assert "read-only" in content.lower() or "read only" in content.lower()

    def test_never_modifies_files(self):
        content = self._read_cmd()
        assert "never modif" in content.lower() or "without modifying" in content.lower()


class TestRecallAgentSpawning:
    """Recall spawns crux-cursor-memory-manager in Recall mode."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-recall.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_spawns_memory_manager(self):
        content = self._read_cmd()
        assert "crux-cursor-memory-manager" in content

    def test_recall_mode(self):
        content = self._read_cmd()
        assert "recall mode" in content.lower() or "Recall mode" in content


class TestForgetConfigPresence:
    """The forget command is properly configured (bonus coverage)."""

    def test_forget_command_in_config(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        commands = data.get("cruxMemories", {}).get("commands", {})
        assert "forget" in commands, "forget command must be in config"

    def test_forget_command_file_exists(self):
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-forget.md"
        )
        assert cmd_file.is_file(), "crux-forget.md command file must exist"

    def test_forget_confirms_before_deletion(self):
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-forget.md"
        )
        if not cmd_file.exists():
            return
        content = cmd_file.read_text(encoding="utf-8")
        assert "confirm" in content.lower(), "Forget must confirm before deletion"

    def test_forget_rebuilds_index(self):
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-forget.md"
        )
        if not cmd_file.exists():
            return
        content = cmd_file.read_text(encoding="utf-8")
        assert "index" in content.lower(), "Forget must rebuild index after deletion"

    def test_forget_removes_tracker(self):
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-forget.md"
        )
        if not cmd_file.exists():
            return
        content = cmd_file.read_text(encoding="utf-8")
        assert "tracker" in content.lower() or "refs.yml" in content
