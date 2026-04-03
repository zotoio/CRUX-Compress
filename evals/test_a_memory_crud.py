"""Category A: Memory CRUD tests.

Validates creation, update, naming conventions, directory placement, and
agent-scoped memory placement.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import yaml

from conftest import MEMORY_TYPES, write_memory

REQUIRED_FRONTMATTER_FIELDS = {
    "title",
    "description",
    "type",
    "strength",
    "created",
    "modified",
    "source",
    "tags",
}


def _parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---"), "File must start with frontmatter delimiter"
    parts = text.split("---", 2)
    assert len(parts) >= 3, "Frontmatter must have opening and closing ---"
    return yaml.safe_load(parts[1])


class TestCreateMemory:
    """Creating a memory file produces valid schema with all required fields."""

    def test_all_required_fields_present(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "test-insight", mem_type="learning")
        fm = _parse_frontmatter(path)
        assert REQUIRED_FRONTMATTER_FIELDS.issubset(fm.keys()), (
            f"Missing fields: {REQUIRED_FRONTMATTER_FIELDS - fm.keys()}"
        )

    def test_strength_starts_at_one(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "new-memory")
        fm = _parse_frontmatter(path)
        assert fm["strength"] == 1

    def test_created_and_modified_are_dates(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "date-check")
        fm = _parse_frontmatter(path)
        for field in ("created", "modified"):
            val = fm[field]
            if isinstance(val, str):
                date.fromisoformat(val)
            else:
                assert isinstance(val, date)

    def test_type_is_valid(self, tmp_memories_dir: Path):
        for t in MEMORY_TYPES:
            path = write_memory(tmp_memories_dir, f"type-{t}", mem_type=t)
            fm = _parse_frontmatter(path)
            assert fm["type"] == t

    def test_tags_is_list(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "tags-check", tags=["a", "b"])
        fm = _parse_frontmatter(path)
        assert isinstance(fm["tags"], list)


class TestUpdateMemory:
    """Updating a memory changes `modified` but never `created`."""

    def test_modified_changes_on_update(self, tmp_memories_dir: Path):
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        path = write_memory(
            tmp_memories_dir,
            "update-target",
            created=yesterday,
            modified=yesterday,
        )

        fm = _parse_frontmatter(path)
        original_created = str(fm["created"])
        original_modified = str(fm["modified"])

        today = date.today().isoformat()
        fm["modified"] = today
        fm["strength"] = 2

        content = "---\n" + yaml.dump(fm, default_flow_style=False, sort_keys=False) + "---\n"
        path.write_text(content, encoding="utf-8")

        fm2 = _parse_frontmatter(path)
        assert str(fm2["created"]) == original_created, "created must not change"
        assert str(fm2["modified"]) != original_modified, "modified must change"
        assert fm2["strength"] == 2

    def test_created_immutable_after_creation(self, tmp_memories_dir: Path):
        original_date = "2026-01-01"
        path = write_memory(
            tmp_memories_dir,
            "immutable-created",
            created=original_date,
        )
        fm = _parse_frontmatter(path)
        assert str(fm["created"]) == original_date


class TestNamingConventions:
    """Memory files must use .memory.md or .memory.crux.md extensions."""

    def test_uncompressed_naming(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "naming-test", compressed=False)
        assert path.name.endswith(".memory.md")

    def test_compressed_naming(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "compressed-test", compressed=True)
        assert path.name.endswith(".memory.crux.md")

    def test_slug_in_filename(self, tmp_memories_dir: Path):
        path = write_memory(tmp_memories_dir, "my-slug")
        assert "my-slug" in path.name


class TestDirectoryPlacement:
    """Memories are placed in the correct type subdirectory."""

    def test_base_memory_in_type_dir(self, tmp_memories_dir: Path):
        for t in ("core", "redflag", "learning", "idea"):
            path = write_memory(tmp_memories_dir, f"dir-{t}", mem_type=t)
            assert path.parent.name == t, f"Expected parent dir '{t}', got '{path.parent.name}'"

    def test_agent_scoped_memory_placement(self, tmp_memories_dir: Path):
        path = write_memory(
            tmp_memories_dir,
            "agent-insight",
            mem_type="core",
            agent_id="code-reviewer",
        )
        assert "agents" in path.parts
        assert "code-reviewer" in path.parts
        assert path.parent.name == "core"

    def test_agent_scoped_nested_path(self, tmp_memories_dir: Path):
        path = write_memory(
            tmp_memories_dir,
            "nested-check",
            mem_type="learning",
            agent_id="code-reviewer",
        )
        expected_parts = ("agents", "code-reviewer", "learning")
        rel = path.relative_to(tmp_memories_dir)
        for part in expected_parts:
            assert part in rel.parts, f"Expected '{part}' in path {rel}"
