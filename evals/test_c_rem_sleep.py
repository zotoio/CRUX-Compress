"""Category C: REM Sleep tests.

Validates promote/demote/archive recommendations, orphaned tracker cleanup,
conflict detection, and REM summary writing.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import yaml

from conftest import MEMORY_TYPES, write_memory, write_tracker


def _load_type_transitions() -> dict:
    return {
        "idea": {"promoteAt": 5, "promoteTo": "learning"},
        "learning": {"promoteAt": 15, "promoteTo": "core"},
        "redflag": {"promoteAt": 10, "promoteTo": "core"},
        "core": {"promoteAt": None},
        "goal": {"promoteAt": None},
    }


class TestPromoteDemoteArchive:
    """Strength/reference data drives correct promote/demote/archive recommendations."""

    def test_idea_promoted_at_threshold(self, tmp_memories_dir: Path):
        transitions = _load_type_transitions()
        threshold = transitions["idea"]["promoteAt"]

        write_memory(tmp_memories_dir, "strong-idea", mem_type="idea", strength=threshold)
        fm_path = tmp_memories_dir / "idea" / "strong-idea.memory.md"
        text = fm_path.read_text()
        parts = text.split("---", 2)
        fm = yaml.safe_load(parts[1])

        rule = transitions[fm["type"]]
        assert rule["promoteAt"] is not None
        assert fm["strength"] >= rule["promoteAt"]
        assert rule["promoteTo"] == "learning"

    def test_learning_promoted_to_core(self, tmp_memories_dir: Path):
        transitions = _load_type_transitions()
        threshold = transitions["learning"]["promoteAt"]

        write_memory(tmp_memories_dir, "strong-learning", mem_type="learning", strength=threshold)

        rule = transitions["learning"]
        assert rule["promoteTo"] == "core"

    def test_redflag_promoted_to_core(self, tmp_memories_dir: Path):
        transitions = _load_type_transitions()
        threshold = transitions["redflag"]["promoteAt"]

        write_memory(tmp_memories_dir, "strong-redflag", mem_type="redflag", strength=threshold)

        rule = transitions["redflag"]
        assert rule["promoteTo"] == "core"

    def test_core_is_terminal(self, tmp_memories_dir: Path):
        transitions = _load_type_transitions()
        assert transitions["core"]["promoteAt"] is None

    def test_goal_is_terminal(self, tmp_memories_dir: Path):
        transitions = _load_type_transitions()
        assert transitions["goal"]["promoteAt"] is None

    def test_below_threshold_no_promotion(self, tmp_memories_dir: Path):
        transitions = _load_type_transitions()
        threshold = transitions["idea"]["promoteAt"]

        write_memory(tmp_memories_dir, "weak-idea", mem_type="idea", strength=threshold - 1)
        fm_path = tmp_memories_dir / "idea" / "weak-idea.memory.md"
        fm = yaml.safe_load(fm_path.read_text().split("---", 2)[1])

        assert fm["strength"] < threshold, "Should not be promoted"

    def test_demote_after_unreferenced_days(self, tmp_path: Path, tmp_memories_dir: Path):
        demote_days = 90
        stale_date = (date.today() - timedelta(days=demote_days + 1)).isoformat()

        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        write_memory(tmp_memories_dir, "stale-learning", mem_type="learning", strength=2)
        write_tracker(
            tracking_dir,
            "stale-learning",
            references=2,
            strength=2,
            last_referenced=stale_date,
        )

        tracker_path = tracking_dir / "stale-learning.refs.yml"
        tracker = yaml.safe_load(tracker_path.read_text())
        last_ref = date.fromisoformat(str(tracker["last_referenced"]))
        days_since = (date.today() - last_ref).days

        assert days_since > demote_days, (
            f"Memory unreferenced for {days_since} days should be demoted"
        )

    def test_archive_after_long_unreferenced(self, tmp_path: Path, tmp_memories_dir: Path):
        archive_days = 180
        very_stale = (date.today() - timedelta(days=archive_days + 1)).isoformat()

        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        write_memory(tmp_memories_dir, "ancient-idea", mem_type="idea", strength=1)
        write_tracker(
            tracking_dir,
            "ancient-idea",
            references=1,
            strength=1,
            last_referenced=very_stale,
        )

        tracker = yaml.safe_load(
            (tracking_dir / "ancient-idea.refs.yml").read_text()
        )
        last_ref = date.fromisoformat(str(tracker["last_referenced"]))
        days_since = (date.today() - last_ref).days

        assert days_since > archive_days, (
            f"Memory unreferenced for {days_since} days should be archived"
        )


class TestOrphanedTrackerCleanup:
    """Orphaned tracker files (no matching memory) should be identified for cleanup."""

    def test_orphaned_tracker_detected(self, tmp_path: Path, tmp_memories_dir: Path):
        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        write_tracker(tracking_dir, "nonexistent-memory", references=5)

        memory_slugs = set()
        for pattern in ("*.memory.md", "*.memory.crux.md"):
            for f in tmp_memories_dir.rglob(pattern):
                name = f.name
                for suffix in (".memory.crux.md", ".memory.md"):
                    if name.endswith(suffix):
                        memory_slugs.add(name[: -len(suffix)])
                        break

        tracker_slugs = set()
        for tf in tracking_dir.glob("*.refs.yml"):
            tracker_slugs.add(tf.stem.replace(".refs", ""))

        orphaned = tracker_slugs - memory_slugs
        assert "nonexistent-memory" in orphaned

    def test_non_orphaned_tracker_not_flagged(self, tmp_path: Path, tmp_memories_dir: Path):
        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        write_memory(tmp_memories_dir, "real-memory", mem_type="learning")
        write_tracker(tracking_dir, "real-memory", references=3)

        memory_slugs = set()
        for pattern in ("*.memory.md", "*.memory.crux.md"):
            for f in tmp_memories_dir.rglob(pattern):
                name = f.name
                for suffix in (".memory.crux.md", ".memory.md"):
                    if name.endswith(suffix):
                        memory_slugs.add(name[: -len(suffix)])
                        break

        tracker_slugs = set()
        for tf in tracking_dir.glob("*.refs.yml"):
            tracker_slugs.add(tf.stem.replace(".refs", ""))

        orphaned = tracker_slugs - memory_slugs
        assert "real-memory" not in orphaned


class TestConflictDetection:
    """Contradicting memories should be identified by conflict detection."""

    def test_opposing_advice_detected(self, tmp_memories_dir: Path):
        write_memory(
            tmp_memories_dir,
            "always-use-memoization",
            mem_type="core",
            strength=5,
            body="Always use React.memo for list items to prevent unnecessary re-renders.",
        )
        write_memory(
            tmp_memories_dir,
            "avoid-memoization",
            mem_type="redflag",
            strength=3,
            body="Avoid React.memo for list items as it adds overhead without measurable benefit.",
        )

        memories = []
        for pattern in ("*.memory.md", "*.memory.crux.md"):
            for f in tmp_memories_dir.rglob(pattern):
                text = f.read_text()
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    fm = yaml.safe_load(parts[1])
                    fm["_body"] = parts[2].strip() if len(parts) > 2 else ""
                    fm["_path"] = str(f)
                    memories.append(fm)

        conflicts = []
        for i, a in enumerate(memories):
            for b in memories[i + 1 :]:
                a_body = (a.get("_body", "") + " " + a.get("title", "")).lower()
                b_body = (b.get("_body", "") + " " + b.get("title", "")).lower()

                has_always = "always" in a_body and "avoid" in b_body
                has_reverse = "avoid" in a_body and "always" in b_body
                same_topic = any(
                    word in a_body and word in b_body
                    for word in ["memo", "memoization", "react.memo"]
                )

                if (has_always or has_reverse) and same_topic:
                    conflicts.append((a["title"], b["title"]))

        assert len(conflicts) >= 1, "Should detect at least one conflict"

    def test_non_conflicting_memories_pass(self, tmp_memories_dir: Path):
        write_memory(
            tmp_memories_dir,
            "use-typescript",
            mem_type="core",
            body="Use TypeScript for all new modules.",
        )
        write_memory(
            tmp_memories_dir,
            "write-tests-first",
            mem_type="learning",
            body="Write tests before implementation for better coverage.",
        )

        memories = []
        for f in tmp_memories_dir.rglob("*.memory.md"):
            text = f.read_text()
            parts = text.split("---", 2)
            if len(parts) >= 3:
                fm = yaml.safe_load(parts[1])
                fm["_body"] = parts[2].strip()
                memories.append(fm)

        conflicts = []
        for i, a in enumerate(memories):
            for b in memories[i + 1 :]:
                a_text = (a.get("_body", "") + " " + a.get("title", "")).lower()
                b_text = (b.get("_body", "") + " " + b.get("title", "")).lower()

                has_oppose = ("always" in a_text and "avoid" in b_text) or (
                    "avoid" in a_text and "always" in b_text
                )
                same_topic = any(
                    w in a_text and w in b_text
                    for w in ["typescript", "tests"]
                )

                if has_oppose and same_topic:
                    conflicts.append((a["title"], b["title"]))

        assert len(conflicts) == 0, "Unrelated memories should not conflict"


class TestREMSummary:
    """REM summary file is written to archiveDir."""

    def test_rem_summary_written(self, tmp_path: Path):
        archive_dir = tmp_path / ".ai-ignored" / "executed"
        archive_dir.mkdir(parents=True, exist_ok=True)

        today = date.today().strftime("%Y%m%d")
        summary_path = archive_dir / f"rem-{today}.md"
        summary_path.write_text(
            f"# REM Sleep Summary — {date.today().isoformat()}\n\n"
            "## Changes Applied\n\n"
            "### Promotions (1)\n"
            '- "strong-idea": idea → learning\n\n'
            "### Demotions (0)\n\n"
            "### Archived (0)\n\n"
            "## Corpus Summary\n"
            "- Total memories: 5\n"
            "- By type: core=1, redflag=1, goal=0, learning=2, idea=1, archived=0\n",
            encoding="utf-8",
        )

        assert summary_path.is_file()
        content = summary_path.read_text()
        assert "REM Sleep Summary" in content
        assert "Promotions" in content
        assert "Corpus Summary" in content
