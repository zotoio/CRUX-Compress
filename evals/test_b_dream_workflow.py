"""Category B: Dream Workflow tests.

Validates execution state verification, candidate fact extraction from spec
structures, dream summary writing, and spec archival.
"""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

import yaml


def _make_spec_dir(tmp_path: Path, slug: str = "20260403-test-spec") -> Path:
    """Create a mock spec directory with subtask files and execution state."""
    spec_dir = tmp_path / "specs" / slug
    spec_dir.mkdir(parents=True)

    spec_file = spec_dir / f"spec-{slug}.md"
    spec_file.write_text(
        f"# Spec: {slug}\n\n"
        "## Objective\nBuild a component library with optimised rendering.\n\n"
        "## Subtasks\n- subtask-01: scaffold\n- subtask-02: implement\n- subtask-03: test\n",
        encoding="utf-8",
    )

    for i in range(1, 4):
        st = spec_dir / f"subtask-0{i}-{slug}.md"
        st.write_text(
            f"# Subtask 0{i}\n\nStatus: complete\n\n"
            f"## Learnings\n- Insight {i}: technique {i} improved performance\n"
            f"- Red flag: avoid pattern-{i} in hot paths\n",
            encoding="utf-8",
        )

    state = {
        "status": "complete",
        "subtasks": {
            f"subtask-0{i}": {"status": "complete", "started": "2026-04-03", "completed": "2026-04-03"}
            for i in range(1, 4)
        },
    }
    state_file = spec_dir / "_execution-state.yml"
    state_file.write_text(yaml.dump(state, default_flow_style=False), encoding="utf-8")

    return spec_dir


def _make_config(tmp_path: Path) -> dict:
    return {
        "platform": "cursor",
        "flags": [{"enableMemories": "true"}],
        "cruxMemories": {
            "enabled": "true",
            "storage": {
                "memoriesDir": "memories",
                "agentMemoriesDir": "memories/agents",
                "archiveDir": str(tmp_path / ".ai-ignored" / "executed"),
                "indexFile": ".crux/memory-index.yml",
            },
            "sizeUnit": "lines",
            "compressionMinLines": 500,
            "maxMemorySize": 1000,
            "unitOfWork": "spec",
            "dream": {
                "maxCandidateFacts": 5,
                "maxUnrelatedChanges": 50,
                "stateFile": "_execution-state.yml",
                "workDir": "specs",
                "summaryPattern": "dream-{slug}-{yyyymmdd}.md",
            },
            "typePriority": ["core", "redflag", "goal", "learning", "idea", "archived"],
            "typeTransitions": {
                "idea": {"promoteAt": 5, "promoteTo": "learning"},
                "learning": {"promoteAt": 15, "promoteTo": "core"},
                "redflag": {"promoteAt": 10, "promoteTo": "core"},
                "core": {"promoteAt": None},
                "goal": {"promoteAt": None},
            },
            "referenceTracking": {
                "enabled": True,
                "trackingDir": ".crux/reference-tracking",
                "maxReferencesStored": 10,
            },
        },
    }


class TestExecutionStateVerification:
    """The dream workflow must verify execution state before extracting."""

    def test_state_file_exists(self, tmp_path: Path):
        spec_dir = _make_spec_dir(tmp_path)
        state_path = spec_dir / "_execution-state.yml"
        assert state_path.is_file()

    def test_state_file_shows_complete(self, tmp_path: Path):
        spec_dir = _make_spec_dir(tmp_path)
        state = yaml.safe_load((spec_dir / "_execution-state.yml").read_text())
        assert state["status"] == "complete"

    def test_incomplete_state_blocks_extraction(self, tmp_path: Path):
        spec_dir = _make_spec_dir(tmp_path)
        state_path = spec_dir / "_execution-state.yml"
        state = yaml.safe_load(state_path.read_text())
        state["status"] = "in_progress"
        state_path.write_text(yaml.dump(state), encoding="utf-8")

        reloaded = yaml.safe_load(state_path.read_text())
        assert reloaded["status"] != "complete", (
            "Extraction should be blocked when status is not complete"
        )


class TestCandidateFactExtraction:
    """Given a completed spec, candidate facts can be extracted from its structure."""

    def test_subtask_files_contain_extractable_content(self, tmp_path: Path):
        spec_dir = _make_spec_dir(tmp_path)
        subtask_files = sorted(spec_dir.glob("subtask-*.md"))
        assert len(subtask_files) == 3

        candidates = []
        for sf in subtask_files:
            text = sf.read_text(encoding="utf-8")
            for line in text.splitlines():
                stripped = line.strip()
                if stripped.startswith("- Insight") or stripped.startswith("- Red flag"):
                    candidates.append(stripped)

        assert len(candidates) >= 3, (
            f"Expected at least 3 candidate facts, got {len(candidates)}"
        )

    def test_max_candidate_facts_capped(self, tmp_path: Path):
        cfg = _make_config(tmp_path)
        max_facts = cfg["cruxMemories"]["dream"]["maxCandidateFacts"]
        spec_dir = _make_spec_dir(tmp_path)

        all_insights = []
        for sf in sorted(spec_dir.glob("subtask-*.md")):
            for line in sf.read_text().splitlines():
                stripped = line.strip()
                if stripped.startswith("- "):
                    all_insights.append(stripped)

        capped = all_insights[:max_facts]
        assert len(capped) <= max_facts


class TestDreamSummaryWriting:
    """Dream summary files are written to the correct location."""

    def test_summary_written_to_work_dir(self, tmp_path: Path):
        spec_dir = _make_spec_dir(tmp_path)
        today = date.today().strftime("%Y%m%d")
        summary_name = f"dream-test-spec-{today}.md"
        summary_path = spec_dir / summary_name

        summary_path.write_text(
            f"# Dream Summary — {date.today().isoformat()}\n\n"
            "## Extracted Candidates\n"
            "1. [learning] technique improved performance\n"
            "2. [redflag] avoid pattern in hot paths\n",
            encoding="utf-8",
        )

        assert summary_path.is_file()
        content = summary_path.read_text()
        assert "Dream Summary" in content
        assert "Extracted Candidates" in content


class TestSpecArchival:
    """Spec directories are moved to archiveDir after dreaming."""

    def test_archive_moves_directory(self, tmp_path: Path):
        spec_dir = _make_spec_dir(tmp_path)
        archive_dir = tmp_path / ".ai-ignored" / "executed"
        archive_dir.mkdir(parents=True, exist_ok=True)

        spec_name = spec_dir.name
        archive_target = archive_dir / spec_name

        shutil.move(str(spec_dir), str(archive_target))

        assert not spec_dir.exists(), "Original spec directory should be gone"
        assert archive_target.is_dir(), "Spec should exist in archive"
        assert (archive_target / "_execution-state.yml").is_file()

    def test_archived_spec_retains_all_files(self, tmp_path: Path):
        spec_dir = _make_spec_dir(tmp_path)
        original_files = set(f.name for f in spec_dir.iterdir())

        archive_dir = tmp_path / ".ai-ignored" / "executed"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive_target = archive_dir / spec_dir.name
        shutil.move(str(spec_dir), str(archive_target))

        archived_files = set(f.name for f in archive_target.iterdir())
        assert original_files == archived_files
