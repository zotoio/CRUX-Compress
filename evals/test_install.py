"""Tests for install.py.

Validates script structure, CLI flags, version comparison,
hooks.json merging, AGENTS.md upsert, checksum, and preview logic.
"""

from __future__ import annotations

import importlib.util
import json
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
