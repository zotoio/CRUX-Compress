"""Tests that CRUX hooks resolve project state from the project root.

Cursor sends absolute file paths to afterFileEdit hooks and sets
CURSOR_PROJECT_DIR to the workspace root. Hooks installed by a plugin can
start in a different working directory, so each hook must use the project
root for its relative .crux/ paths.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HOOKS = PROJECT_ROOT / ".cursor" / "hooks"


def _run(script: str, cwd: Path, payload: dict, project_dir: Path | None = None) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if k not in ("CURSOR_PROJECT_DIR", "CLAUDE_PROJECT_DIR")}
    if project_dir is not None:
        env["CURSOR_PROJECT_DIR"] = str(project_dir)
    return subprocess.run(
        [sys.executable, str(HOOKS / script)],
        capture_output=True, text=True, input=json.dumps(payload),
        cwd=str(cwd), env=env, check=False,
    )


def _memory_project(tmp_path: Path) -> tuple[Path, Path]:
    project = tmp_path / "project"
    (project / ".crux").mkdir(parents=True)
    (project / "memories").mkdir()
    (project / ".crux" / "crux-memories.json").write_text(json.dumps({
        "flags": [{"enableMemories": "true"}],
        "cruxMemories": {"storage": {"memoriesDir": "memories", "agentMemoriesDir": "memories/agents"}},
    }), encoding="utf-8")
    memory = project / "memories" / "retry-backoff.memory.md"
    memory.write_text("---\ntitle: Retry backoff\n---\n", encoding="utf-8")
    return project, memory


def _crux_rule_project(tmp_path: Path) -> tuple[Path, Path]:
    project = tmp_path / "project"
    (project / ".crux").mkdir(parents=True)
    (project / ".cursor" / "rules").mkdir(parents=True)
    rule = project / ".cursor" / "rules" / "api.md"
    rule.write_text("---\ncrux: true\n---\n\n# Rule\n", encoding="utf-8")
    return project, rule


class TestMemoryHookAbsolutePaths:
    def test_absolute_memory_path_flags_rebuild(self, tmp_path: Path):
        project, memory = _memory_project(tmp_path)
        result = _run("crux-detect-memory-changes.py", project, {"file_path": str(memory)})
        assert result.returncode == 0, result.stderr
        pending = json.loads((project / ".crux" / "pending-index-rebuild.json").read_text(encoding="utf-8"))
        assert "memories/retry-backoff.memory.md" in pending["files"]

    def test_absolute_path_outside_memories_is_ignored(self, tmp_path: Path):
        project, _ = _memory_project(tmp_path)
        other = project / "README.md"
        other.write_text("readme", encoding="utf-8")
        _run("crux-detect-memory-changes.py", project, {"file_path": str(other)})
        assert not (project / ".crux" / "pending-index-rebuild.json").exists()


class TestHooksUseProjectDir:
    def test_memory_hook_writes_to_project_from_other_cwd(self, tmp_path: Path):
        project, memory = _memory_project(tmp_path)
        elsewhere = tmp_path / "plugin"
        elsewhere.mkdir()
        result = _run("crux-detect-memory-changes.py", elsewhere, {"file_path": str(memory)}, project_dir=project)
        assert result.returncode == 0, result.stderr
        assert (project / ".crux" / "pending-index-rebuild.json").is_file()
        assert not (elsewhere / ".crux").exists()

    def test_detect_changes_queues_into_project_from_other_cwd(self, tmp_path: Path):
        project, rule = _crux_rule_project(tmp_path)
        subprocess.run(["git", "init", "-q", str(project)], check=True)
        elsewhere = tmp_path / "plugin"
        elsewhere.mkdir()
        result = _run("crux-detect-changes.py", elsewhere, {"file_path": str(rule)}, project_dir=project)
        assert result.returncode == 0, result.stderr
        pending = json.loads((project / ".crux" / "pending-compression.json").read_text(encoding="utf-8"))
        assert ".cursor/rules/api.md" in pending["files"]
        assert not (elsewhere / ".crux").exists()

    def test_session_start_reads_project_queue_from_other_cwd(self, tmp_path: Path):
        project, _ = _crux_rule_project(tmp_path)
        (project / ".crux" / "pending-compression.json").write_text(
            json.dumps({"files": [".cursor/rules/api.md"]}), encoding="utf-8",
        )
        elsewhere = tmp_path / "plugin"
        elsewhere.mkdir()
        result = _run("crux-session-start.py", elsewhere, {}, project_dir=project)
        assert result.returncode == 0, result.stderr
        assert ".cursor/rules/api.md" in result.stdout

    def test_missing_project_dir_keeps_cwd(self, tmp_path: Path):
        project, memory = _memory_project(tmp_path)
        result = _run("crux-detect-memory-changes.py", project, {"file_path": "memories/retry-backoff.memory.md"},
                      project_dir=tmp_path / "does-not-exist")
        assert result.returncode == 0, result.stderr
        assert (project / ".crux" / "pending-index-rebuild.json").is_file()
