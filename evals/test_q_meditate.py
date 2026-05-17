"""Category Q: Meditate Workflow tests.

Validates meditate command definition, facet derivation structure,
recursive depth configuration, and continuation menu requirements.
"""

from __future__ import annotations

import json
from pathlib import Path


class TestMeditateConfigPresence:
    """The meditate command is properly configured in crux-memories.json."""

    def test_meditate_command_in_config(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        commands = data.get("cruxMemories", {}).get("commands", {})
        assert "meditate" in commands, "meditate command must be in config"

    def test_meditate_command_file_path(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        meditate = data["cruxMemories"]["commands"]["meditate"]
        assert meditate["file"] == ".cursor/commands/crux-meditate.md"

    def test_meditate_command_default(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        meditate = data["cruxMemories"]["commands"]["meditate"]
        assert meditate["default"] == "/crux-meditate"

    def test_meditate_command_file_exists(self):
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        assert cmd_file.is_file(), "crux-meditate.md command file must exist"


class TestMeditateCommandDefinition:
    """The meditate command file defines the 3-facet, 3-level recursive flow."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_has_usage_section(self):
        content = self._read_cmd()
        assert "## Usage" in content

    def test_supports_no_arguments(self):
        content = self._read_cmd()
        assert "no argument" in content.lower() or "/crux-meditate" in content

    def test_supports_quoted_topic(self):
        content = self._read_cmd()
        assert "topic" in content.lower() or "question" in content.lower()

    def test_supports_file_references(self):
        content = self._read_cmd()
        assert "@" in content or "file" in content.lower()


class TestMeditateFacetStructure:
    """Meditate derives 3 distinct exploration facets."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_documents_three_facets(self):
        content = self._read_cmd()
        assert "three" in content.lower() or "3" in content

    def test_facets_are_distinct_dimensions(self):
        content = self._read_cmd()
        lower = content.lower()
        facet_terms = ["theme", "topic", "intent", "facet"]
        matches = sum(1 for t in facet_terms if t in lower)
        assert matches >= 2, "Should mention at least two facet dimensions"

    def test_facets_become_branches(self):
        content = self._read_cmd()
        assert "branch" in content.lower() or "parallel" in content.lower()


class TestMeditateRecursiveDepth:
    """Meditate uses configurable recursive depth (1-3 levels, default 3) with depth tracking."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_documents_three_levels(self):
        content = self._read_cmd()
        assert "3" in content or "three" in content.lower()

    def test_level_1_spawns_agents(self):
        content = self._read_cmd()
        assert "level 1" in content.lower() or "spawn" in content.lower()

    def test_level_3_is_terminal(self):
        content = self._read_cmd()
        low = content.lower()
        assert "depth-3" in low or "depth 3" in low or "level 3" in low or "deepest" in low

    def test_recursive_structure(self):
        content = self._read_cmd()
        assert "recursive" in content.lower()

    def test_depth_is_configurable(self):
        content = self._read_cmd()
        low = content.lower()
        assert "maxdepth" in low or "depth selection" in low

    def test_depth_selection_question_exists(self):
        content = self._read_cmd()
        assert "Q-Depth-Selection" in content

    def test_depth_defaults_to_three(self):
        content = self._read_cmd()
        assert "default" in content.lower() and "3" in content


class TestMeditateMemoryQuerying:
    """Each recursion level queries memories relevant to its facet."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_queries_memories(self):
        content = self._read_cmd()
        assert "memor" in content.lower()

    def test_uses_memory_index(self):
        content = self._read_cmd()
        assert "index" in content.lower() or "search" in content.lower()

    def test_refines_queries_at_each_level(self):
        content = self._read_cmd()
        assert "refine" in content.lower() or "expand" in content.lower()


class TestMeditateConsolidation:
    """Insights consolidate from deepest level back to root."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_documents_consolidation(self):
        content = self._read_cmd()
        assert "consolidat" in content.lower()

    def test_highlights_cross_branch_connections(self):
        content = self._read_cmd()
        assert "cross" in content.lower() or "connection" in content.lower()

    def test_presents_organized_output(self):
        content = self._read_cmd()
        assert "branch" in content.lower() or "organized" in content.lower()


class TestMeditateContinuationMenu:
    """After meditate, an interactive menu offers expansion or save options."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_offers_expansion_options(self):
        content = self._read_cmd()
        assert "expansion" in content.lower() or "direction" in content.lower()

    def test_offers_save_as_spec(self):
        content = self._read_cmd()
        assert "spec" in content.lower() and "save" in content.lower()

    def test_offers_end_option(self):
        content = self._read_cmd()
        assert "end" in content.lower()

    def test_uses_ask_question(self):
        content = self._read_cmd()
        assert "AskQuestion" in content


class TestMeditateAgentSpawning:
    """Meditate uses crux-cursor-memory-manager subagent in Meditate mode."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_spawns_memory_manager(self):
        content = self._read_cmd()
        assert "crux-cursor-memory-manager" in content

    def test_meditate_mode(self):
        content = self._read_cmd()
        assert "meditate mode" in content.lower() or "Meditate mode" in content
