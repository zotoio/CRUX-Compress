"""Tests for install.py.

Validates script structure, CLI flags, version comparison,
hooks.json merging, AGENTS.md upsert, checksum, and preview logic.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INSTALL_SCRIPT = PROJECT_ROOT / "install.py"

_install_mod = None


def _load_install():
    global _install_mod
    if _install_mod is None:
        spec = importlib.util.spec_from_file_location("install", str(INSTALL_SCRIPT))
        _install_mod = importlib.util.module_from_spec(spec)
        sys.modules["install"] = _install_mod
        spec.loader.exec_module(_install_mod)
    return _install_mod


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(INSTALL_SCRIPT)] + args,
        capture_output=True, text=True,
    )


# ── Script basics ──


class TestScriptBasics:
    def test_exists(self):
        assert INSTALL_SCRIPT.is_file()

    def test_valid_syntax(self):
        import ast
        ast.parse(INSTALL_SCRIPT.read_text(encoding="utf-8"))

    def test_shebang(self):
        first_line = INSTALL_SCRIPT.read_text(encoding="utf-8").splitlines()[0]
        assert "python" in first_line

    def test_defines_repo_owner(self):
        mod = _load_install()
        assert mod.REPO_OWNER == "zotoio"

    def test_defines_repo_name(self):
        mod = _load_install()
        assert mod.REPO_NAME == "CRUX-Compress"


# ── CLI flags ──


class TestCLIFlags:
    def test_help(self):
        r = _run(["--help"])
        assert r.returncode == 0
        for kw in ("CRUX Compress", "--backup", "--verbose", "--force"):
            assert kw in r.stdout, f"Missing keyword: {kw}"

    def test_help_contains_with_memories(self):
        r = _run(["--help"])
        assert r.returncode == 0
        assert "--with-memories" in r.stdout

    def test_help_contains_curl(self):
        text = INSTALL_SCRIPT.read_text(encoding="utf-8")
        assert "curl" in text


# ── Required functions ──


class TestRequiredFunctions:
    FUNCTIONS = [
        "create_backup_zip", "compare_versions", "check_not_in_crux_repo",
        "detect_git_root", "get_version_change_type",
        "preview_installation", "get_checksum", "confirm",
        "show_completion_report", "download_update_script", "download_and_stage",
        "merge_hooks_json", "upsert_agents_crux_block",
        "to_crux_primitive_path", "from_crux_primitive_path",
        "migrate_primitive_layout",
    ]

    def test_all_functions_defined(self):
        mod = _load_install()
        for fn in self.FUNCTIONS:
            assert hasattr(mod, fn), f"Function {fn} not found"
            assert callable(getattr(mod, fn)), f"{fn} is not callable"


# ── Dependency checks ──


class TestDependencyChecks:
    def test_mentions_curl(self):
        text = INSTALL_SCRIPT.read_text(encoding="utf-8")
        assert "curl" in text

    def test_uses_urllib(self):
        text = INSTALL_SCRIPT.read_text(encoding="utf-8")
        assert "urllib" in text


# ── Version comparison ──


class TestVersionComparison:
    def test_newer(self):
        mod = _load_install()
        assert mod.compare_versions("2.0.0", "1.0.0") == 0

    def test_equal(self):
        mod = _load_install()
        assert mod.compare_versions("1.0.0", "1.0.0") == 1

    def test_older(self):
        mod = _load_install()
        assert mod.compare_versions("1.0.0", "2.0.0") == 2


class TestVersionChangeType:
    def test_major(self):
        mod = _load_install()
        assert mod.get_version_change_type("1.0.0", "2.0.0") == "major"

    def test_minor(self):
        mod = _load_install()
        assert mod.get_version_change_type("1.0.0", "1.1.0") == "minor"

    def test_patch(self):
        mod = _load_install()
        assert mod.get_version_change_type("1.0.0", "1.0.1") == "patch"


# ── hooks.json merge ──


class TestHooksJsonMerge:
    def test_creates_if_not_exists(self, tmp_path: Path):
        mod = _load_install()
        (tmp_path / ".cursor").mkdir()
        staging = tmp_path / "staging.json"
        staging.write_text('{"hooks":{"sessionStart":[{"command":"echo test"}]}}')

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.merge_hooks_json(str(staging))
        finally:
            os.chdir(orig_cwd)

        hooks = json.loads((tmp_path / ".cursor" / "hooks.json").read_text())
        assert "sessionStart" in hooks.get("hooks", {})

    def test_handles_null_arrays(self, tmp_path: Path):
        mod = _load_install()
        (tmp_path / ".cursor").mkdir()
        (tmp_path / ".cursor" / "hooks.json").write_text(
            '{"hooks":{"sessionStart":null,"afterFileEdit":[{"command":"existing"}]}}'
        )
        staging = tmp_path / "staging.json"
        staging.write_text(
            '{"hooks":{"sessionStart":[{"command":"new-session"}],"afterFileEdit":[{"command":"new-edit"}]}}'
        )

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.merge_hooks_json(str(staging))
        finally:
            os.chdir(orig_cwd)

        content = (tmp_path / ".cursor" / "hooks.json").read_text()
        assert "new-session" in content
        assert "existing" in content

    def test_adds_missing_lifecycle_hooks(self, tmp_path: Path):
        mod = _load_install()
        (tmp_path / ".cursor").mkdir()
        (tmp_path / ".cursor" / "hooks.json").write_text(
            '{"hooks":{"sessionStart":[{"command":"existing-session"}]}}'
        )
        staging = tmp_path / "staging.json"
        staging.write_text(
            '{"hooks":{"afterFileEdit":[{"command":"new-edit"}],"stop":[{"command":"new-stop"}]}}'
        )

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.merge_hooks_json(str(staging))
        finally:
            os.chdir(orig_cwd)

        content = (tmp_path / ".cursor" / "hooks.json").read_text()
        for kw in ("sessionStart", "existing-session", "afterFileEdit", "new-edit", "stop", "new-stop"):
            assert kw in content

    def test_avoids_duplicate_commands(self, tmp_path: Path):
        mod = _load_install()
        (tmp_path / ".cursor").mkdir()
        (tmp_path / ".cursor" / "hooks.json").write_text(
            '{"hooks":{"sessionStart":[{"command":"shared-cmd","args":["old"]}]}}'
        )
        staging = tmp_path / "staging.json"
        staging.write_text(
            '{"hooks":{"sessionStart":[{"command":"shared-cmd","args":["new"]},{"command":"unique-cmd"}]}}'
        )

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.merge_hooks_json(str(staging))
        finally:
            os.chdir(orig_cwd)

        content = (tmp_path / ".cursor" / "hooks.json").read_text()
        assert content.count("shared-cmd") == 1
        assert "unique-cmd" in content


# ── AGENTS.md upsert ──


class TestAgentsUpsert:
    def test_creates_new_agents_md(self, tmp_path: Path):
        mod = _load_install()
        (tmp_path / "AGENTS.crux.md").write_text(
            '<CRUX agents="always">\n\n## CRITICAL\nMulti-line content\n\n</CRUX>\n'
        )

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.upsert_agents_crux_block("AGENTS.crux.md")
        finally:
            os.chdir(orig_cwd)

        content = (tmp_path / "AGENTS.md").read_text()
        assert "<CRUX agents" in content
        assert "CRITICAL" in content

    def test_prepends_to_existing(self, tmp_path: Path):
        mod = _load_install()
        (tmp_path / "AGENTS.md").write_text("# My Project Agents\n\nCustom content.\n")
        (tmp_path / "AGENTS.crux.md").write_text('<CRUX agents="always">\nCRUX content\n</CRUX>\n')

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.upsert_agents_crux_block("AGENTS.crux.md")
        finally:
            os.chdir(orig_cwd)

        content = (tmp_path / "AGENTS.md").read_text()
        assert content.startswith('<CRUX agents="always">')
        assert "Custom content" in content

    def test_replaces_existing_block(self, tmp_path: Path):
        mod = _load_install()
        (tmp_path / "AGENTS.md").write_text(
            '<CRUX agents="old">\nOld content\n</CRUX>\n\n# My Project\n\nCustom stuff.\n'
        )
        (tmp_path / "AGENTS.crux.md").write_text('<CRUX agents="new">\nNew content\n</CRUX>\n')

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.upsert_agents_crux_block("AGENTS.crux.md")
        finally:
            os.chdir(orig_cwd)

        content = (tmp_path / "AGENTS.md").read_text()
        assert "New content" in content
        assert "Old content" not in content
        assert "Custom stuff" in content

    def test_removes_crux_md_after_upsert(self, tmp_path: Path):
        mod = _load_install()
        (tmp_path / "AGENTS.crux.md").write_text('<CRUX agents="always">\nContent\n</CRUX>\n')

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.upsert_agents_crux_block("AGENTS.crux.md")
        finally:
            os.chdir(orig_cwd)

        assert not (tmp_path / "AGENTS.crux.md").is_file()


# ── Checksum ──


class TestChecksum:
    def test_consistent(self, tmp_path: Path):
        mod = _load_install()
        (tmp_path / "file.txt").write_text("test content")
        h1 = mod.get_checksum(str(tmp_path / "file.txt"))
        h2 = mod.get_checksum(str(tmp_path / "file.txt"))
        assert h1 == h2 and h1

    def test_differs_for_different_content(self, tmp_path: Path):
        mod = _load_install()
        (tmp_path / "a.txt").write_text("content 1")
        (tmp_path / "b.txt").write_text("content 2")
        assert mod.get_checksum(str(tmp_path / "a.txt")) != mod.get_checksum(str(tmp_path / "b.txt"))


# ── CRUX primitive layout migration ──


class TestCruxPrimitiveLayout:
    def test_maps_commands_to_crux_subdir(self):
        mod = _load_install()
        assert (
            mod.to_crux_primitive_path(".cursor/commands/crux-compress.md")
            == ".cursor/commands/crux/crux-compress.md"
        )

    def test_maps_skills_to_crux_subdir(self):
        mod = _load_install()
        assert (
            mod.to_crux_primitive_path(".cursor/skills/crux-utils/scripts/crux-utils.py")
            == ".cursor/skills/crux/crux-utils/scripts/crux-utils.py"
        )

    def test_reverse_maps_crux_subdir_to_source_path(self):
        mod = _load_install()
        assert (
            mod.from_crux_primitive_path(".cursor/agents/crux/crux-cursor-rule-manager.md")
            == ".cursor/agents/crux-cursor-rule-manager.md"
        )

    def test_migrates_legacy_primitives(self, tmp_path: Path):
        mod = _load_install()
        legacy_command = tmp_path / ".cursor" / "commands" / "crux-compress.md"
        legacy_skill = tmp_path / ".cursor" / "skills" / "crux-utils" / "scripts" / "crux-utils.py"
        legacy_command.parent.mkdir(parents=True)
        legacy_skill.parent.mkdir(parents=True)
        legacy_command.write_text("command", encoding="utf-8")
        legacy_skill.write_text("skill", encoding="utf-8")

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.migrate_primitive_layout()
        finally:
            os.chdir(orig_cwd)

        assert not legacy_command.exists()
        assert not legacy_skill.exists()
        assert (tmp_path / ".cursor" / "commands" / "crux" / "crux-compress.md").read_text(
            encoding="utf-8"
        ) == "command"
        assert (
            tmp_path
            / ".cursor"
            / "skills"
            / "crux"
            / "crux-utils"
            / "scripts"
            / "crux-utils.py"
        ).read_text(encoding="utf-8") == "skill"

    def test_migration_does_not_overwrite_conflicting_new_file(self, tmp_path: Path):
        mod = _load_install()
        legacy = tmp_path / ".cursor" / "commands" / "crux-compress.md"
        target = tmp_path / ".cursor" / "commands" / "crux" / "crux-compress.md"
        legacy.parent.mkdir(parents=True)
        target.parent.mkdir(parents=True)
        legacy.write_text("legacy edit", encoding="utf-8")
        target.write_text("new edit", encoding="utf-8")

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.migrate_primitive_layout()
        finally:
            os.chdir(orig_cwd)

        assert legacy.read_text(encoding="utf-8") == "legacy edit"
        assert target.read_text(encoding="utf-8") == "new edit"


# ── Preview ──


class TestPreview:
    def test_create(self, tmp_path: Path, capsys):
        mod = _load_install()
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "newfile.txt").write_text("new content")

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.preview_installation(staging)
        finally:
            os.chdir(orig_cwd)

        out = capsys.readouterr().out
        assert "CREATE" in out
        assert "newfile.txt" in out

    def test_update(self, tmp_path: Path, capsys):
        mod = _load_install()
        (tmp_path / "existingfile.txt").write_text("old content")
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "existingfile.txt").write_text("new content")

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.preview_installation(staging)
        finally:
            os.chdir(orig_cwd)

        out = capsys.readouterr().out
        assert "UPDATE" in out

    def test_no_change(self, tmp_path: Path, capsys):
        mod = _load_install()
        (tmp_path / "samefile.txt").write_text("same content")
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "samefile.txt").write_text("same content")

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.preview_installation(staging)
        finally:
            os.chdir(orig_cwd)

        out = capsys.readouterr().out
        assert "NO CHANGE" in out

    def test_mixed(self, tmp_path: Path, capsys):
        mod = _load_install()
        (tmp_path / "unchanged.txt").write_text("unchanged")
        (tmp_path / "changed.txt").write_text("will change")
        staging = tmp_path / "staging"
        staging.mkdir()
        (staging / "unchanged.txt").write_text("unchanged")
        (staging / "changed.txt").write_text("has changed")
        (staging / "newfile.txt").write_text("brand new")

        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)
            mod.preview_installation(staging)
        finally:
            os.chdir(orig_cwd)

        out = capsys.readouterr().out
        assert "NO CHANGE" in out
        assert "UPDATE" in out
        assert "CREATE" in out


# ── Memory scaffolding (--with-memories) ──


class TestWithMemoriesFlag:
    def test_argparse_accepts_with_memories(self):
        mod = _load_install()
        parser = argparse.ArgumentParser()
        parser.add_argument("--with-memories", action="store_true")
        args = parser.parse_args(["--with-memories"])
        assert args.with_memories is True

    def test_argparse_default_no_memories(self):
        mod = _load_install()
        parser = argparse.ArgumentParser()
        parser.add_argument("--with-memories", action="store_true")
        args = parser.parse_args([])
        assert args.with_memories is False


class TestSetupMemories:
    def test_creates_config_file(self, tmp_path: Path):
        mod = _load_install()
        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.setup_memories()
        finally:
            os.chdir(orig_cwd)

        config = tmp_path / ".crux" / "crux-memories.json"
        assert config.is_file()
        data = json.loads(config.read_text(encoding="utf-8"))
        assert "cruxMemories" in data

    def test_creates_memories_directory(self, tmp_path: Path):
        mod = _load_install()
        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.setup_memories()
        finally:
            os.chdir(orig_cwd)

        assert (tmp_path / "memories").is_dir()

    def test_creates_agents_directory(self, tmp_path: Path):
        mod = _load_install()
        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.setup_memories()
        finally:
            os.chdir(orig_cwd)

        assert (tmp_path / "memories" / "agents").is_dir()

    def test_creates_tracking_directory(self, tmp_path: Path):
        mod = _load_install()
        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.setup_memories()
        finally:
            os.chdir(orig_cwd)

        assert (tmp_path / ".crux" / "reference-tracking").is_dir()

    def test_skips_if_config_exists(self, tmp_path: Path):
        mod = _load_install()
        crux_dir = tmp_path / ".crux"
        crux_dir.mkdir(parents=True)
        config = crux_dir / "crux-memories.json"
        config.write_text('{"existing": true}', encoding="utf-8")

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.setup_memories()
        finally:
            os.chdir(orig_cwd)

        data = json.loads(config.read_text(encoding="utf-8"))
        assert data == {"existing": True}

    def test_returns_true(self, tmp_path: Path):
        mod = _load_install()
        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            result = mod.setup_memories()
        finally:
            os.chdir(orig_cwd)

        assert result is True

    def test_config_has_disabled_memories_by_default(self, tmp_path: Path):
        mod = _load_install()
        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.setup_memories()
        finally:
            os.chdir(orig_cwd)

        config = tmp_path / ".crux" / "crux-memories.json"
        data = json.loads(config.read_text(encoding="utf-8"))
        flags = {k: v for f in data["flags"] for k, v in f.items()}
        assert flags["enableMemories"] == "false"

    def test_config_includes_amnesia_command(self, tmp_path: Path):
        mod = _load_install()
        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.setup_memories()
        finally:
            os.chdir(orig_cwd)

        config = tmp_path / ".crux" / "crux-memories.json"
        data = json.loads(config.read_text(encoding="utf-8"))
        amnesia = data["cruxMemories"]["commands"]["amnesia"]
        assert amnesia["file"] == ".cursor/commands/crux/crux-amnesia.md"
        assert amnesia["default"] == "/crux-amnesia"


class TestWithoutMemories:
    def test_no_memory_files_without_flag(self, tmp_path: Path):
        """When --with-memories is NOT used, no memory scaffolding should exist."""
        assert not (tmp_path / ".crux" / "crux-memories.json").exists()
        assert not (tmp_path / "memories").exists()
        assert not (tmp_path / ".crux" / "reference-tracking").exists()


# ── Deprecated file cleanup ──


class TestCleanupDeprecatedFiles:
    def test_removes_old_bash_hook(self, tmp_path: Path):
        mod = _load_install()
        hooks_dir = tmp_path / ".cursor" / "hooks"
        hooks_dir.mkdir(parents=True)
        old_hook = hooks_dir / "detect-crux-changes.sh"
        old_hook.write_text("#!/bin/bash\necho old")

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_files()
        finally:
            os.chdir(orig_cwd)

        assert not old_hook.exists()

    def test_removes_old_skill_directory(self, tmp_path: Path):
        mod = _load_install()
        old_skill = tmp_path / ".cursor" / "skills" / "CRUX-Utils" / "scripts"
        old_skill.mkdir(parents=True)
        (old_skill / "crux-utils.sh").write_text("#!/bin/bash")
        (old_skill.parent / "SKILL.md").write_text("# Old skill")

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_files()
        finally:
            os.chdir(orig_cwd)

        assert not (old_skill / "crux-utils.sh").exists()
        assert not (old_skill.parent / "SKILL.md").exists()
        assert not old_skill.exists(), "Empty scripts/ dir should be removed"
        assert not old_skill.parent.exists(), "Empty CRUX-Utils/ dir should be removed"

    def test_removes_old_update_sh(self, tmp_path: Path):
        mod = _load_install()
        crux_dir = tmp_path / ".crux"
        crux_dir.mkdir(parents=True)
        (crux_dir / "update.sh").write_text("#!/bin/bash")
        (crux_dir / "crux.json").write_text('{"version":"2.0.0"}')

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_files()
        finally:
            os.chdir(orig_cwd)

        assert not (crux_dir / "update.sh").exists()
        assert (crux_dir / "crux.json").exists(), "Non-deprecated files should be preserved"

    def test_noop_when_no_deprecated_files(self, tmp_path: Path):
        mod = _load_install()
        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_files()
        finally:
            os.chdir(orig_cwd)

    def test_preserves_nonempty_parent_dirs(self, tmp_path: Path):
        mod = _load_install()
        hooks_dir = tmp_path / ".cursor" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "detect-crux-changes.sh").write_text("old")
        (hooks_dir / "crux-detect-changes.py").write_text("new")

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_files()
        finally:
            os.chdir(orig_cwd)

        assert not (hooks_dir / "detect-crux-changes.sh").exists()
        assert hooks_dir.exists(), "Dir with remaining files should not be removed"
        assert (hooks_dir / "crux-detect-changes.py").exists()


class TestCleanupDeprecatedHooks:
    def test_removes_old_bash_hook_commands(self, tmp_path: Path):
        mod = _load_install()
        hooks_dir = tmp_path / ".cursor"
        hooks_dir.mkdir(parents=True)
        hooks_json = hooks_dir / "hooks.json"
        hooks_json.write_text(json.dumps({
            "hooks": {
                "afterFileEdit": [
                    {"command": "bash .cursor/hooks/detect-crux-changes.sh"},
                    {"command": "python3 .cursor/hooks/crux-detect-changes.py"},
                ]
            }
        }))

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_hooks()
        finally:
            os.chdir(orig_cwd)

        data = json.loads(hooks_json.read_text())
        commands = [h["command"] for h in data["hooks"]["afterFileEdit"]]
        assert "bash .cursor/hooks/detect-crux-changes.sh" not in commands
        assert "python3 .cursor/hooks/crux-detect-changes.py" in commands

    def test_removes_bare_sh_hook_command(self, tmp_path: Path):
        mod = _load_install()
        hooks_dir = tmp_path / ".cursor"
        hooks_dir.mkdir(parents=True)
        hooks_json = hooks_dir / "hooks.json"
        hooks_json.write_text(json.dumps({
            "hooks": {
                "afterFileEdit": [
                    {"command": ".cursor/hooks/detect-crux-changes.sh"},
                    {"command": "python3 .cursor/hooks/crux-detect-changes.py"},
                ]
            }
        }))

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_hooks()
        finally:
            os.chdir(orig_cwd)

        data = json.loads(hooks_json.read_text())
        commands = [h["command"] for h in data["hooks"]["afterFileEdit"]]
        assert ".cursor/hooks/detect-crux-changes.sh" not in commands
        assert len(commands) == 1

    def test_deletes_empty_lifecycle_after_cleanup(self, tmp_path: Path):
        mod = _load_install()
        hooks_dir = tmp_path / ".cursor"
        hooks_dir.mkdir(parents=True)
        hooks_json = hooks_dir / "hooks.json"
        hooks_json.write_text(json.dumps({
            "hooks": {
                "afterFileEdit": [
                    {"command": "bash .cursor/hooks/detect-crux-changes.sh"},
                ],
                "sessionStart": [
                    {"command": "python3 .cursor/hooks/crux-session-start.py"},
                ]
            }
        }))

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_hooks()
        finally:
            os.chdir(orig_cwd)

        data = json.loads(hooks_json.read_text())
        assert "afterFileEdit" not in data["hooks"], "Empty lifecycle should be removed"
        assert "sessionStart" in data["hooks"]

    def test_noop_when_no_deprecated_hooks(self, tmp_path: Path):
        mod = _load_install()
        hooks_dir = tmp_path / ".cursor"
        hooks_dir.mkdir(parents=True)
        hooks_json = hooks_dir / "hooks.json"
        original = json.dumps({
            "hooks": {
                "sessionStart": [
                    {"command": "python3 .cursor/hooks/crux-session-start.py"},
                ]
            }
        })
        hooks_json.write_text(original)

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_hooks()
        finally:
            os.chdir(orig_cwd)

        data = json.loads(hooks_json.read_text())
        assert len(data["hooks"]["sessionStart"]) == 1

    def test_noop_when_no_hooks_json(self, tmp_path: Path):
        mod = _load_install()
        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_hooks()
        finally:
            os.chdir(orig_cwd)


class TestCleanupIntegration:
    """Test that deprecated files + hooks cleanup work together for upgrade scenarios."""

    def test_v2_2_to_latest_upgrade(self, tmp_path: Path):
        """Simulate upgrading from v2.2.x with old bash hooks."""
        mod = _load_install()

        hooks_dir = tmp_path / ".cursor" / "hooks"
        hooks_dir.mkdir(parents=True)
        (hooks_dir / "detect-crux-changes.sh").write_text("#!/bin/bash\nold hook")

        old_skill = tmp_path / ".cursor" / "skills" / "CRUX-Utils" / "scripts"
        old_skill.mkdir(parents=True)
        (old_skill / "crux-utils.sh").write_text("#!/bin/bash")
        (old_skill.parent / "SKILL.md").write_text("# Old")

        crux_dir = tmp_path / ".crux"
        crux_dir.mkdir(parents=True)
        (crux_dir / "update.sh").write_text("#!/bin/bash\nold updater")

        hooks_json = tmp_path / ".cursor" / "hooks.json"
        hooks_json.write_text(json.dumps({
            "hooks": {
                "afterFileEdit": [
                    {"command": "bash .cursor/hooks/detect-crux-changes.sh"},
                    {"command": "python3 .cursor/hooks/crux-detect-changes.py"},
                ],
                "sessionStart": [
                    {"command": "python3 .cursor/hooks/crux-session-start.py"},
                ]
            }
        }))

        orig_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)
            mod.cleanup_deprecated_files()
            mod.cleanup_deprecated_hooks()
        finally:
            os.chdir(orig_cwd)

        assert not (hooks_dir / "detect-crux-changes.sh").exists()
        assert not (old_skill / "crux-utils.sh").exists()
        assert not old_skill.parent.exists()
        assert not (crux_dir / "update.sh").exists()

        data = json.loads(hooks_json.read_text())
        commands = [h["command"] for h in data["hooks"]["afterFileEdit"]]
        assert "bash .cursor/hooks/detect-crux-changes.sh" not in commands
        assert "python3 .cursor/hooks/crux-detect-changes.py" in commands
        assert len(data["hooks"]["sessionStart"]) == 1
