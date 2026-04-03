"""Tests for the crux-detect-changes.py hook.

Validates file detection, queue management, frontmatter parsing,
and filtering logic for the CRUX compression change detection hook.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HOOK_SCRIPT = PROJECT_ROOT / ".cursor" / "hooks" / "crux-detect-changes.py"


def _run_hook(cwd: Path, file_path: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(HOOK_SCRIPT)],
        capture_output=True, text=True,
        input=json.dumps({"file_path": file_path}),
        cwd=str(cwd),
    )


def _create_rule(tmp_path: Path, name: str, frontmatter: str) -> None:
    rules_dir = tmp_path / ".cursor" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    (rules_dir / name).write_text(f"---\n{frontmatter}\n---\n\n# Rule\n", encoding="utf-8")


def _setup(tmp_path: Path) -> None:
    (tmp_path / ".cursor" / "rules").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".cursor" / "hooks").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".crux").mkdir(parents=True, exist_ok=True)


class TestHookExists:
    def test_hook_script_exists(self):
        assert HOOK_SCRIPT.is_file()


class TestQueuesValidFiles:
    def test_queues_crux_true(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "test-rule.md", "crux: true")
        _run_hook(tmp_path, ".cursor/rules/test-rule.md")

        pending = tmp_path / ".crux" / "pending-compression.json"
        assert pending.is_file()
        data = json.loads(pending.read_text())
        assert ".cursor/rules/test-rule.md" in data["files"]

    def test_queues_crux_with_spaces(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "spaced.md", "crux:   true")
        _run_hook(tmp_path, ".cursor/rules/spaced.md")
        assert (tmp_path / ".crux" / "pending-compression.json").is_file()

    def test_queues_numeric_crux_value(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "numeric.md", "crux: 40")
        _run_hook(tmp_path, ".cursor/rules/numeric.md")

        pending = tmp_path / ".crux" / "pending-compression.json"
        data = json.loads(pending.read_text())
        assert ".cursor/rules/numeric.md" in data["files"]

    def test_queues_crux_100(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "max.md", "crux: 100")
        _run_hook(tmp_path, ".cursor/rules/max.md")

        data = json.loads((tmp_path / ".crux" / "pending-compression.json").read_text())
        assert ".cursor/rules/max.md" in data["files"]

    def test_queues_crux_1(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "min.md", "crux: 1")
        _run_hook(tmp_path, ".cursor/rules/min.md")

        data = json.loads((tmp_path / ".crux" / "pending-compression.json").read_text())
        assert ".cursor/rules/min.md" in data["files"]


class TestIgnoresInvalidFiles:
    def test_ignores_no_crux_frontmatter(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "no-crux.md", "alwaysApply: true")
        _run_hook(tmp_path, ".cursor/rules/no-crux.md")
        assert not (tmp_path / ".crux" / "pending-compression.json").is_file()

    def test_ignores_crux_md(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "test.crux.md", "crux: true\ngenerated: 2024-01-01")
        _run_hook(tmp_path, ".cursor/rules/test.crux.md")
        assert not (tmp_path / ".crux" / "pending-compression.json").is_file()

    def test_ignores_crux_mdc(self, tmp_path: Path):
        _setup(tmp_path)
        rules = tmp_path / ".cursor" / "rules"
        rules.mkdir(parents=True, exist_ok=True)
        (rules / "test.crux.mdc").write_text("---\ncrux: true\n---\n", encoding="utf-8")
        _run_hook(tmp_path, ".cursor/rules/test.crux.mdc")
        assert not (tmp_path / ".crux" / "pending-compression.json").is_file()

    def test_ignores_outside_rules(self, tmp_path: Path):
        _setup(tmp_path)
        docs = tmp_path / "docs"
        docs.mkdir(parents=True, exist_ok=True)
        (docs / "test.md").write_text("---\ncrux: true\n---\n", encoding="utf-8")
        _run_hook(tmp_path, "docs/test.md")
        assert not (tmp_path / ".crux" / "pending-compression.json").is_file()

    def test_ignores_crux_0(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "zero.md", "crux: 0")
        _run_hook(tmp_path, ".cursor/rules/zero.md")
        assert not (tmp_path / ".crux" / "pending-compression.json").is_file()

    def test_ignores_crux_false(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "false.md", "crux: false")
        _run_hook(tmp_path, ".cursor/rules/false.md")
        assert not (tmp_path / ".crux" / "pending-compression.json").is_file()

    def test_ignores_crux_string(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "string.md", "crux: something")
        _run_hook(tmp_path, ".cursor/rules/string.md")
        assert not (tmp_path / ".crux" / "pending-compression.json").is_file()


class TestQueueManagement:
    def test_avoids_duplicates(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "test-rule.md", "crux: true")
        _run_hook(tmp_path, ".cursor/rules/test-rule.md")
        _run_hook(tmp_path, ".cursor/rules/test-rule.md")

        data = json.loads((tmp_path / ".crux" / "pending-compression.json").read_text())
        assert data["files"].count(".cursor/rules/test-rule.md") == 1

    def test_creates_valid_json(self, tmp_path: Path):
        _setup(tmp_path)
        _create_rule(tmp_path, "test-rule.md", "crux: true")
        _run_hook(tmp_path, ".cursor/rules/test-rule.md")

        data = json.loads((tmp_path / ".crux" / "pending-compression.json").read_text())
        assert "files" in data
        assert isinstance(data["files"], list)
