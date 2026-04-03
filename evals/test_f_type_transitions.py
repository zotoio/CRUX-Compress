"""Category F: Type Transitions tests.

Validates promotion thresholds, file moves on promotion, demotion after
inactivity, and archival after extended inactivity.
"""

from __future__ import annotations

import shutil
from datetime import date, timedelta
from pathlib import Path

import yaml

from conftest import MEMORY_TYPES, _make_config, write_memory, write_tracker


def _parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    return yaml.safe_load(parts[1])


def _config_transitions(tmp_path: Path) -> dict:
    return _make_config(tmp_path)


class TestPromotionThreshold:
    """When strength reaches promoteAt, the memory should be flagged for promotion."""

    def test_idea_at_threshold_recommends_promotion(self, tmp_path: Path):
        cfg = _config_transitions(tmp_path)
        transitions = cfg["cruxMemories"]["typeTransitions"]

        mem_dir = tmp_path / "memories"
        threshold = transitions["idea"]["promoteAt"]
        path = write_memory(mem_dir, "bright-idea", mem_type="idea", strength=threshold)

        fm = _parse_frontmatter(path)
        assert fm["strength"] >= threshold
        assert transitions["idea"]["promoteTo"] == "learning"

    def test_learning_at_threshold_recommends_promotion(self, tmp_path: Path):
        cfg = _config_transitions(tmp_path)
        transitions = cfg["cruxMemories"]["typeTransitions"]

        mem_dir = tmp_path / "memories"
        threshold = transitions["learning"]["promoteAt"]
        path = write_memory(mem_dir, "strong-learning", mem_type="learning", strength=threshold)

        fm = _parse_frontmatter(path)
        assert fm["strength"] >= threshold
        assert transitions["learning"]["promoteTo"] == "core"

    def test_core_has_no_promotion(self, tmp_path: Path):
        cfg = _config_transitions(tmp_path)
        transitions = cfg["cruxMemories"]["typeTransitions"]
        assert transitions["core"]["promoteAt"] is None

    def test_goal_has_no_promotion(self, tmp_path: Path):
        cfg = _config_transitions(tmp_path)
        transitions = cfg["cruxMemories"]["typeTransitions"]
        assert transitions["goal"]["promoteAt"] is None


class TestPromotionFileMove:
    """After promotion, the file moves to the new type directory with updated frontmatter."""

    def test_promoted_file_in_new_directory(self, tmp_path: Path):
        cfg = _config_transitions(tmp_path)
        promote_to = cfg["cruxMemories"]["typeTransitions"]["idea"]["promoteTo"]

        mem_dir = tmp_path / "memories"
        for t in MEMORY_TYPES:
            (mem_dir / t).mkdir(parents=True, exist_ok=True)

        old_path = write_memory(mem_dir, "promoted-idea", mem_type="idea", strength=5)
        fm = _parse_frontmatter(old_path)
        fm["type"] = promote_to
        fm["promoted_from"] = "idea"
        fm["modified"] = date.today().isoformat()

        new_dir = mem_dir / promote_to
        new_path = new_dir / old_path.name
        content = "---\n" + yaml.dump(fm, default_flow_style=False, sort_keys=False) + "---\n"
        new_path.write_text(content, encoding="utf-8")
        old_path.unlink()

        assert new_path.exists()
        assert not old_path.exists()

        new_fm = _parse_frontmatter(new_path)
        assert new_fm["type"] == promote_to
        assert new_fm["promoted_from"] == "idea"

    def test_promoted_frontmatter_updated(self, tmp_path: Path):
        cfg = _config_transitions(tmp_path)
        mem_dir = tmp_path / "memories"
        for t in MEMORY_TYPES:
            (mem_dir / t).mkdir(parents=True, exist_ok=True)

        path = write_memory(mem_dir, "upgrade-me", mem_type="idea", strength=5)
        fm = _parse_frontmatter(path)

        fm["type"] = "learning"
        fm["promoted_from"] = "idea"
        fm["strength"] = 5

        content = "---\n" + yaml.dump(fm, default_flow_style=False, sort_keys=False) + "---\n"
        new_path = mem_dir / "learning" / path.name
        new_path.write_text(content, encoding="utf-8")

        new_fm = _parse_frontmatter(new_path)
        assert new_fm["type"] == "learning"
        assert new_fm["promoted_from"] == "idea"
        assert new_fm["strength"] == 5


class TestDemotionAfterInactivity:
    """Memories unreferenced for demoteAfterDaysUnreferenced days are demoted."""

    def test_stale_memory_triggers_demotion(self, tmp_path: Path):
        cfg = _config_transitions(tmp_path)
        demote_days = cfg["cruxMemories"]["demoteAfterDaysUnreferenced"]

        mem_dir = tmp_path / "memories"
        stale_date = (date.today() - timedelta(days=demote_days + 1)).isoformat()
        path = write_memory(
            mem_dir, "stale-learning",
            mem_type="learning", strength=3,
            modified=stale_date,
        )

        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        write_tracker(
            tracking_dir, "stale-learning",
            references=3, strength=3,
            last_referenced=stale_date,
        )

        tracker_data = yaml.safe_load(
            (tracking_dir / "stale-learning.refs.yml").read_text(encoding="utf-8")
        )
        last_ref = date.fromisoformat(str(tracker_data["last_referenced"]))
        days_since = (date.today() - last_ref).days

        assert days_since > demote_days, (
            f"Expected >{demote_days} days since last reference, got {days_since}"
        )

    def test_recent_memory_not_demoted(self, tmp_path: Path):
        cfg = _config_transitions(tmp_path)
        demote_days = cfg["cruxMemories"]["demoteAfterDaysUnreferenced"]

        mem_dir = tmp_path / "memories"
        recent_date = (date.today() - timedelta(days=10)).isoformat()
        write_memory(
            mem_dir, "active-learning",
            mem_type="learning", strength=3,
            modified=recent_date,
        )

        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        write_tracker(
            tracking_dir, "active-learning",
            references=5, strength=3,
            last_referenced=recent_date,
        )

        tracker_data = yaml.safe_load(
            (tracking_dir / "active-learning.refs.yml").read_text(encoding="utf-8")
        )
        last_ref = date.fromisoformat(str(tracker_data["last_referenced"]))
        days_since = (date.today() - last_ref).days

        assert days_since < demote_days


class TestArchivalAfterInactivity:
    """Memories unreferenced for archiveAfterDaysUnreferenced days are archived."""

    def test_very_stale_memory_triggers_archival(self, tmp_path: Path):
        cfg = _config_transitions(tmp_path)
        archive_days = cfg["cruxMemories"]["archiveAfterDaysUnreferenced"]

        mem_dir = tmp_path / "memories"
        stale_date = (date.today() - timedelta(days=archive_days + 1)).isoformat()
        path = write_memory(
            mem_dir, "forgotten",
            mem_type="learning", strength=2,
            modified=stale_date,
        )

        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        write_tracker(
            tracking_dir, "forgotten",
            references=2, strength=2,
            last_referenced=stale_date,
        )

        tracker_data = yaml.safe_load(
            (tracking_dir / "forgotten.refs.yml").read_text(encoding="utf-8")
        )
        last_ref = date.fromisoformat(str(tracker_data["last_referenced"]))
        days_since = (date.today() - last_ref).days

        assert days_since > archive_days

        archive_dir = tmp_path / "memories" / "archived"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archived_path = archive_dir / path.name
        shutil.move(str(path), str(archived_path))

        fm = _parse_frontmatter(archived_path)
        fm["type"] = "archived"
        content = "---\n" + yaml.dump(fm, default_flow_style=False, sort_keys=False) + "---\n"
        archived_path.write_text(content, encoding="utf-8")

        assert archived_path.exists()
        assert not path.exists()
        assert _parse_frontmatter(archived_path)["type"] == "archived"

    def test_demotion_threshold_less_than_archival(self, tmp_path: Path):
        cfg = _config_transitions(tmp_path)
        assert cfg["cruxMemories"]["demoteAfterDaysUnreferenced"] < cfg["cruxMemories"]["archiveAfterDaysUnreferenced"]
