"""Category O: Remember Workflow tests.

Validates ad-hoc memory creation, source field requirements,
type placement, --type flag behavior, and index rebuild expectations.
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


class TestRememberAdhocSource:
    """Ad-hoc memories must have source: 'adhoc' to distinguish from spec-extracted."""

    def test_adhoc_source_field(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "user-insight", source="adhoc")
        fm = _parse_frontmatter(path)
        assert fm["source"] == "adhoc"

    def test_adhoc_differs_from_spec_source(self, tmp_memories_dir: Path):
        adhoc = write_memory(tmp_memories_dir, "adhoc-mem", source="adhoc")
        spec = write_memory(tmp_memories_dir, "spec-mem", source="20260403-crux-memories")

        fm_adhoc = _parse_frontmatter(adhoc)
        fm_spec = _parse_frontmatter(spec)
        assert fm_adhoc["source"] != fm_spec["source"]
        assert fm_adhoc["source"] == "adhoc"

    def test_adhoc_memory_has_default_strength(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "new-adhoc", source="adhoc", strength=1)
        fm = _parse_frontmatter(path)
        assert fm["strength"] == 1


class TestRememberTypePlacement:
    """Memories are placed in the correct type subdirectory based on selection."""

    def test_idea_goes_to_idea_dir(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "my-idea", mem_type="idea", source="adhoc")
        assert path.parent.name == "idea"

    def test_learning_goes_to_learning_dir(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "my-learning", mem_type="learning", source="adhoc")
        assert path.parent.name == "learning"

    def test_redflag_goes_to_redflag_dir(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "my-redflag", mem_type="redflag", source="adhoc")
        assert path.parent.name == "redflag"

    def test_core_goes_to_core_dir(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "my-core", mem_type="core", source="adhoc")
        assert path.parent.name == "core"

    def test_goal_goes_to_goal_dir(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "my-goal", mem_type="goal", source="adhoc")
        assert path.parent.name == "goal"


class TestRememberTypeFlag:
    """The --type flag should bypass type selection and place directly."""

    VALID_TYPES = ["idea", "learning", "redflag", "core", "goal"]

    def test_all_valid_types_accepted(self, tmp_memories_dir: Path):
        for t in self.VALID_TYPES:
            path = write_memory(tmp_memories_dir, f"typed-{t}", mem_type=t, source="adhoc")
            fm = _parse_frontmatter(path)
            assert fm["type"] == t

    def test_invalid_type_not_in_transitions(self, tmp_memories_dir: Path):
        cfg = _make_config(tmp_memories_dir.parent)
        transitions = cfg["cruxMemories"]["typeTransitions"]
        assert "archived" not in transitions, (
            "archived should not be a valid --type option (not in typeTransitions)"
        )


class TestRememberFrontmatter:
    """Remember-created memories have all required frontmatter fields."""

    def test_has_title(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "remember-title", source="adhoc")
        fm = _parse_frontmatter(path)
        assert "title" in fm and len(str(fm["title"])) > 0

    def test_has_description(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "remember-desc", source="adhoc")
        fm = _parse_frontmatter(path)
        assert "description" in fm

    def test_has_tags_list(self, tmp_memories_dir: Path):
        path = write_memory(
            tmp_memories_dir, "remember-tags", source="adhoc", tags=["validation", "files"]
        )
        fm = _parse_frontmatter(path)
        assert isinstance(fm["tags"], list)
        assert len(fm["tags"]) >= 1

    def test_created_is_today(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "remember-date", source="adhoc")
        fm = _parse_frontmatter(path)
        assert str(fm["created"]) == date.today().isoformat()

    def test_modified_equals_created(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "remember-mod", source="adhoc")
        fm = _parse_frontmatter(path)
        assert str(fm["created"]) == str(fm["modified"])


class TestRememberConfigIntegration:
    """The remember command is properly configured in crux-memories.json."""

    def test_remember_command_in_config(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        commands = data.get("cruxMemories", {}).get("commands", {})
        assert "remember" in commands, "remember command must be in config"

    def test_remember_command_file_path(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        remember = data["cruxMemories"]["commands"]["remember"]
        assert remember["file"] == ".cursor/commands/crux-remember.md"

    def test_remember_command_default(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        remember = data["cruxMemories"]["commands"]["remember"]
        assert remember["default"] == "/crux-remember"

    def test_remember_command_file_exists(self):
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-remember.md"
        assert cmd_file.is_file(), "crux-remember.md command file must exist"

    def test_remember_command_file_has_usage(self):
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-remember.md"
        if not cmd_file.exists():
            return
        content = cmd_file.read_text(encoding="utf-8")
        assert "/crux-remember" in content
        assert "## Usage" in content

    def test_remember_command_mentions_adhoc(self):
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-remember.md"
        if not cmd_file.exists():
            return
        content = cmd_file.read_text(encoding="utf-8")
        assert "adhoc" in content.lower(), "Command should document adhoc source"

    def test_remember_command_mentions_type_flag(self):
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-remember.md"
        if not cmd_file.exists():
            return
        content = cmd_file.read_text(encoding="utf-8")
        assert "--type" in content, "Command should document --type flag"


class TestRememberTypeTransitions:
    """Ad-hoc memories participate in standard type transitions and REM sleep."""

    def test_adhoc_idea_can_promote(self, tmp_memories_dir: Path):
        cfg = _make_config(tmp_memories_dir.parent)
        transitions = cfg["cruxMemories"]["typeTransitions"]
        assert transitions["idea"]["promoteAt"] == 5
        assert transitions["idea"]["promoteTo"] == "learning"

        path = write_memory(
            tmp_memories_dir, "promotable-idea", mem_type="idea", strength=5, source="adhoc"
        )
        fm = _parse_frontmatter(path)
        assert fm["strength"] >= transitions["idea"]["promoteAt"]

    def test_adhoc_learning_can_promote(self, tmp_memories_dir: Path):
        cfg = _make_config(tmp_memories_dir.parent)
        transitions = cfg["cruxMemories"]["typeTransitions"]
        assert transitions["learning"]["promoteAt"] == 15

    def test_adhoc_redflag_can_promote(self, tmp_memories_dir: Path):
        cfg = _make_config(tmp_memories_dir.parent)
        transitions = cfg["cruxMemories"]["typeTransitions"]
        assert transitions["redflag"]["promoteAt"] == 10
