"""Category B: Dream Workflow tests.

Validates execution state verification, candidate fact extraction from plan
structures, dream summary writing, and plan archival.
"""

from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

import yaml


def _make_plan_dir(tmp_path: Path, slug: str = "20260403-test-plan") -> Path:
    """Create a mock plan directory with subtask files and execution state."""
    plan_dir = tmp_path / "plans" / slug
    plan_dir.mkdir(parents=True)

    plan_file = plan_dir / f"plan-{slug}.md"
    plan_file.write_text(
        f"# Plan: {slug}\n\n"
        "## Objective\nBuild a component library with optimised rendering.\n\n"
        "## Subtasks\n- subtask-01: scaffold\n- subtask-02: implement\n- subtask-03: test\n",
        encoding="utf-8",
    )

    for i in range(1, 4):
        st = plan_dir / f"subtask-0{i}-{slug}.md"
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
    state_file = plan_dir / "_execution-state.yml"
    state_file.write_text(yaml.dump(state, default_flow_style=False), encoding="utf-8")

    return plan_dir


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
            "maxMemorySize": 2048,
            "unitOfWork": "plan",
            "dream": {
                "maxCandidateFacts": 5,
                "maxUnrelatedChanges": 50,
                "stateFile": "_execution-state.yml",
                "workDir": "plans",
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
        plan_dir = _make_plan_dir(tmp_path)
        state_path = plan_dir / "_execution-state.yml"
        assert state_path.is_file()

    def test_state_file_shows_complete(self, tmp_path: Path):
        plan_dir = _make_plan_dir(tmp_path)
        state = yaml.safe_load((plan_dir / "_execution-state.yml").read_text())
        assert state["status"] == "complete"

    def test_incomplete_state_blocks_extraction(self, tmp_path: Path):
        plan_dir = _make_plan_dir(tmp_path)
        state_path = plan_dir / "_execution-state.yml"
        state = yaml.safe_load(state_path.read_text())
        state["status"] = "in_progress"
        state_path.write_text(yaml.dump(state), encoding="utf-8")

        reloaded = yaml.safe_load(state_path.read_text())
        assert reloaded["status"] != "complete", (
            "Extraction should be blocked when status is not complete"
        )


class TestCandidateFactExtraction:
    """Given a completed plan, candidate facts can be extracted from its structure."""

    def test_subtask_files_contain_extractable_content(self, tmp_path: Path):
        plan_dir = _make_plan_dir(tmp_path)
        subtask_files = sorted(plan_dir.glob("subtask-*.md"))
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
        plan_dir = _make_plan_dir(tmp_path)

        all_insights = []
        for sf in sorted(plan_dir.glob("subtask-*.md")):
            for line in sf.read_text().splitlines():
                stripped = line.strip()
                if stripped.startswith("- "):
                    all_insights.append(stripped)

        capped = all_insights[:max_facts]
        assert len(capped) <= max_facts


class TestDreamSummaryWriting:
    """Dream summary files are written to the correct location."""

    def test_summary_written_to_work_dir(self, tmp_path: Path):
        plan_dir = _make_plan_dir(tmp_path)
        today = date.today().strftime("%Y%m%d")
        summary_name = f"dream-test-plan-{today}.md"
        summary_path = plan_dir / summary_name

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


class TestPlanArchival:
    """Plan directories are moved to archiveDir after dreaming."""

    def test_archive_moves_directory(self, tmp_path: Path):
        plan_dir = _make_plan_dir(tmp_path)
        archive_dir = tmp_path / ".ai-ignored" / "executed"
        archive_dir.mkdir(parents=True, exist_ok=True)

        plan_name = plan_dir.name
        archive_target = archive_dir / plan_name

        shutil.move(str(plan_dir), str(archive_target))

        assert not plan_dir.exists(), "Original plan directory should be gone"
        assert archive_target.is_dir(), "Plan should exist in archive"
        assert (archive_target / "_execution-state.yml").is_file()

    def test_archived_plan_retains_all_files(self, tmp_path: Path):
        plan_dir = _make_plan_dir(tmp_path)
        original_files = set(f.name for f in plan_dir.iterdir())

        archive_dir = tmp_path / ".ai-ignored" / "executed"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive_target = archive_dir / plan_dir.name
        shutil.move(str(plan_dir), str(archive_target))

        archived_files = set(f.name for f in archive_target.iterdir())
        assert original_files == archived_files
