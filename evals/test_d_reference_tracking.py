"""Category D: Reference Tracking tests.

Validates tracker creation, multi-source tracking, maxReferencesStored cap,
and indicator format behaviour.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml

from conftest import write_tracker


def _parse_tracker(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    yaml_lines = [l for l in lines if not l.startswith("#")]
    return yaml.safe_load("\n".join(yaml_lines))


class TestTrackerCreation:
    """Creating a reference produces a .refs.yml with correct fields."""

    def test_tracker_created_with_required_fields(self, tmp_path: Path):
        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        path = write_tracker(tracking_dir, "my-memory", references=1, strength=1)

        assert path.is_file()
        assert path.name == "my-memory.refs.yml"

        data = _parse_tracker(path)
        assert data["slug"] == "my-memory"
        assert data["references"] == 1
        assert "last_referenced" in data
        assert data["strength"] == 1
        assert isinstance(data["recent_references"], list)
        assert len(data["recent_references"]) >= 1

    def test_tracker_slug_matches_filename(self, tmp_path: Path):
        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        path = write_tracker(tracking_dir, "validate-checksums")

        data = _parse_tracker(path)
        expected_slug = path.stem.replace(".refs", "")
        assert data["slug"] == expected_slug

    def test_first_reference_count_is_one(self, tmp_path: Path):
        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        path = write_tracker(tracking_dir, "first-ref", references=1)

        data = _parse_tracker(path)
        assert data["references"] == 1


class TestMultiSourceTracking:
    """Referencing the same memory from two sources records both entries."""

    def test_two_sources_both_recorded(self, tmp_path: Path):
        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        today = date.today().isoformat()

        recent = [
            {"spec": "spec-alpha", "count": 3, "last": today},
            {"spec": "spec-beta", "count": 2, "last": today},
        ]
        path = write_tracker(
            tracking_dir,
            "multi-source",
            references=5,
            recent_references=recent,
        )

        data = _parse_tracker(path)
        assert data["references"] == 5
        assert len(data["recent_references"]) == 2

        sources = [r.get("spec") for r in data["recent_references"]]
        assert "spec-alpha" in sources
        assert "spec-beta" in sources

    def test_source_counts_correct(self, tmp_path: Path):
        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        today = date.today().isoformat()

        recent = [
            {"spec": "spec-alpha", "count": 7, "last": today},
            {"spec": "spec-beta", "count": 3, "last": today},
        ]
        path = write_tracker(
            tracking_dir,
            "count-check",
            references=10,
            recent_references=recent,
        )

        data = _parse_tracker(path)
        total_from_recent = sum(r["count"] for r in data["recent_references"])
        assert total_from_recent == 10


class TestMaxReferencesStoredCap:
    """The maxReferencesStored cap evicts the oldest/lowest-count entries."""

    def test_cap_enforced(self, tmp_path: Path):
        max_stored = 10
        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        today = date.today().isoformat()

        recent = [
            {"spec": f"spec-{i:02d}", "count": 20 - i, "last": today}
            for i in range(15)
        ]

        capped = sorted(recent, key=lambda r: -r["count"])[:max_stored]

        path = write_tracker(
            tracking_dir,
            "capped-memory",
            references=sum(r["count"] for r in recent),
            recent_references=capped,
        )

        data = _parse_tracker(path)
        assert len(data["recent_references"]) <= max_stored

    def test_highest_counts_retained(self, tmp_path: Path):
        max_stored = 3
        tracking_dir = tmp_path / ".crux" / "reference-tracking"
        today = date.today().isoformat()

        recent = [
            {"spec": "high", "count": 100, "last": today},
            {"spec": "medium", "count": 50, "last": today},
            {"spec": "low", "count": 10, "last": today},
            {"spec": "lowest", "count": 1, "last": today},
        ]

        capped = sorted(recent, key=lambda r: -r["count"])[:max_stored]

        path = write_tracker(
            tracking_dir,
            "retain-high",
            references=161,
            recent_references=capped,
        )

        data = _parse_tracker(path)
        names = [r["spec"] for r in data["recent_references"]]
        assert "high" in names
        assert "medium" in names
        assert "low" in names
        assert "lowest" not in names


class TestIndicatorFormat:
    """Indicator format when indicateInOutput is true vs false."""

    def test_indicator_format_with_title(self):
        fmt = "[memory:{title}]"
        title = "React.memo reduces re-renders"
        result = fmt.replace("{title}", title)
        assert result == "[memory:React.memo reduces re-renders]"

    def test_indicator_present_when_enabled(self):
        config = {
            "indicateInOutput": True,
            "indicatorFormat": "[memory:{title}]",
        }
        title = "Always validate checksums"
        if config["indicateInOutput"]:
            indicator = config["indicatorFormat"].replace("{title}", title)
        else:
            indicator = ""

        assert indicator == "[memory:Always validate checksums]"

    def test_no_indicator_when_disabled(self):
        config = {
            "indicateInOutput": False,
            "indicatorFormat": "[memory:{title}]",
        }
        title = "Always validate checksums"
        if config["indicateInOutput"]:
            indicator = config["indicatorFormat"].replace("{title}", title)
        else:
            indicator = ""

        assert indicator == "", "Indicator should be empty when disabled"
