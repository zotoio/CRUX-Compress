"""Tests for create-crux-zip.py.

Validates that the distribution zip is created correctly with all required
files, correct versioning, and expected structure.
"""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREATE_ZIP = PROJECT_ROOT / "scripts" / "create-crux-zip.py"


def _run_zip(output_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CREATE_ZIP), str(output_dir)],
        capture_output=True, text=True, cwd=str(PROJECT_ROOT),
        check=False,
    )


def _get_zip_path(output_dir: Path) -> Path:
    zips = list(output_dir.glob("CRUX-Compress-v*.zip"))
    assert len(zips) == 1, f"Expected 1 zip, found {len(zips)}"
    return zips[0]


class TestZipCreation:
    def test_script_exists(self):
        assert CREATE_ZIP.is_file()

    def test_creates_versioned_zip(self, tmp_path: Path):
        result = _run_zip(tmp_path)
        assert result.returncode == 0, f"Failed: {result.stderr}"
        assert len(list(tmp_path.glob("CRUX-Compress-v*.zip"))) == 1

    def test_version_matches_config(self, tmp_path: Path):
        config = json.loads((PROJECT_ROOT / ".crux" / "crux.json").read_text())
        expected_version = config["version"]

        result = _run_zip(tmp_path)
        assert result.returncode == 0
        assert (tmp_path / f"CRUX-Compress-v{expected_version}.zip").is_file()


class TestZipContents:
    @pytest.fixture(scope="class")
    def zip_names(self, tmp_path_factory: pytest.TempPathFactory) -> list[str]:
        tmp_path = tmp_path_factory.mktemp("zip")
        result = _run_zip(tmp_path)
        assert result.returncode == 0
        zp = _get_zip_path(tmp_path)
        with zipfile.ZipFile(zp) as zf:
            return zf.namelist()

    def test_contains_crux_md(self, zip_names: list[str]):
        assert any("CRUX.md" in n for n in zip_names)

    def test_contains_agents_crux_md(self, zip_names: list[str]):
        assert any("AGENTS.crux.md" in n for n in zip_names)

    def test_contains_crux_json(self, zip_names: list[str]):
        assert any(".crux/crux.json" in n for n in zip_names)

    def test_contains_hooks_json(self, zip_names: list[str]):
        assert any(".cursor/hooks.json" in n for n in zip_names)

    def test_contains_rule_manager(self, zip_names: list[str]):
        assert ".cursor/agents/crux/crux-cursor-rule-manager.md" in zip_names

    def test_contains_crux_compress_command(self, zip_names: list[str]):
        assert ".cursor/commands/crux/crux-compress.md" in zip_names

    def test_contains_detect_changes_hook(self, zip_names: list[str]):
        assert any("crux-detect-changes.py" in n for n in zip_names)

    def test_contains_crux_rule(self, zip_names: list[str]):
        assert ".cursor/rules/crux/_CRUX-RULE.mdc" in zip_names

    def test_contains_crux_utils_skill(self, zip_names: list[str]):
        assert ".cursor/skills/crux/crux-utils/SKILL.md" in zip_names
        assert ".cursor/skills/crux/crux-utils/scripts/crux-utils.py" in zip_names

    def test_contains_thin_memory_agents(self, zip_names: list[str]):
        for agent in (
            "crux-memory-dream",
            "crux-memory-rem",
            "crux-memory-recall",
            "crux-memory-remember",
            "crux-memory-forget",
        ):
            assert f".cursor/agents/crux/{agent}.md" in zip_names

    def test_contains_memory_shared_surface(self, zip_names: list[str]):
        assert ".cursor/skills/crux/_memory-shared.md" in zip_names

    def test_contains_recall_canvas_template(self, zip_names: list[str]):
        assert ".cursor/agents/crux/templates/recall-canvas.tsx.md" in zip_names

    def test_contains_compress_prompts_template(self, zip_names: list[str]):
        assert ".cursor/commands/crux/templates/compress-prompts.md" in zip_names


class TestZipIntegrity:
    def test_agents_crux_md_has_crux_block(self, tmp_path: Path):
        result = _run_zip(tmp_path)
        assert result.returncode == 0
        zp = _get_zip_path(tmp_path)

        with zipfile.ZipFile(zp) as zf:
            agents_files = [n for n in zf.namelist() if n.endswith("AGENTS.crux.md")]
            assert agents_files, "AGENTS.crux.md not found in zip"
            content = zf.read(agents_files[0]).decode("utf-8")
            assert "<CRUX" in content

    def test_extracted_version_matches_source(self, tmp_path: Path):
        source_config = json.loads((PROJECT_ROOT / ".crux" / "crux.json").read_text())
        expected_version = source_config["version"]

        result = _run_zip(tmp_path)
        assert result.returncode == 0
        zp = _get_zip_path(tmp_path)

        with zipfile.ZipFile(zp) as zf:
            config_files = [n for n in zf.namelist() if n.endswith(".crux/crux.json")]
            assert config_files
            extracted_config = json.loads(zf.read(config_files[0]))
            assert extracted_config["version"] == expected_version

    def test_contains_release_manifest(self, tmp_path: Path):
        manifest = PROJECT_ROOT / ".crux" / "crux-release-files.json"
        if not manifest.is_file():
            return

        result = _run_zip(tmp_path)
        assert result.returncode == 0
        zp = _get_zip_path(tmp_path)

        with zipfile.ZipFile(zp) as zf:
            assert any("crux-release-files.json" in n for n in zf.namelist())


def _load_create_zip():
    import importlib.util

    spec = importlib.util.spec_from_file_location("create_crux_zip", str(CREATE_ZIP))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestPrimitiveReferenceRewrite:
    def test_rewrites_shipped_primitive_references(self):
        mod = _load_create_zip()
        text = (
            "tpl=.cursor/commands/templates/compress-prompts.md; "
            "see `.cursor/skills/_memory-shared.md#user-input-escalation` and "
            "`.cursor/agents/templates/recall-canvas.tsx.md`; "
            "run python3 .cursor/skills/crux-utils/scripts/crux-utils.py"
        )
        assert mod.rewrite_primitive_references(text) == (
            "tpl=.cursor/commands/crux/templates/compress-prompts.md; "
            "see `.cursor/skills/crux/_memory-shared.md#user-input-escalation` and "
            "`.cursor/agents/crux/templates/recall-canvas.tsx.md`; "
            "run python3 .cursor/skills/crux/crux-utils/scripts/crux-utils.py"
        )

    def test_leaves_project_and_nested_paths_alone(self):
        mod = _load_create_zip()
        text = (
            "compress `.cursor/rules/my-rule.md` and `.cursor/rules/`; "
            "`.cursor/skills/crux/_memory-shared.md`; `.cursor/hooks/crux-session-start.py`; "
            "`.cursor/skills/crux-utils-extra/SKILL.md`"
        )
        assert mod.rewrite_primitive_references(text) == text


class TestZipReferences:
    @pytest.fixture(scope="class")
    def extracted(self, tmp_path_factory: pytest.TempPathFactory) -> Path:
        tmp_path = tmp_path_factory.mktemp("zip-refs")
        result = _run_zip(tmp_path)
        assert result.returncode == 0, result.stderr
        out = tmp_path / "x"
        with zipfile.ZipFile(_get_zip_path(tmp_path)) as zf:
            zf.extractall(out)
        return out

    def test_contains_track_memory_references_hook(self, extracted: Path):
        hooks = json.loads((extracted / ".cursor" / "hooks.json").read_text(encoding="utf-8"))
        commands = [h["command"] for entries in hooks["hooks"].values() for h in entries]
        for command in commands:
            script = command.split()[-1]
            assert (extracted / script).is_file(), f"hooks.json runs {script}, which is not in the zip"

    def test_no_references_to_flat_primitive_paths(self, extracted: Path):
        mod = _load_create_zip()
        for path in (extracted / ".cursor").rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                assert not mod.MOVED_PRIMITIVE_RE.search(text), f"{path.relative_to(extracted)} has a flat-layout reference"

    def test_nested_references_resolve(self, extracted: Path):
        import re

        ref = re.compile(r"\.cursor/(?:agents|commands|rules|skills)/crux/[\w./-]+\.(?:mdc|md|py)\b")
        for path in (extracted / ".cursor").rglob("*"):
            if path.is_file():
                for match in ref.findall(path.read_text(encoding="utf-8")):
                    assert (extracted / match).is_file(), f"{path.relative_to(extracted)} references missing {match}"

    def test_release_checksums_match_zip_contents(self, extracted: Path):
        import hashlib

        manifest = json.loads((extracted / ".crux" / "crux-release-files.json").read_text(encoding="utf-8"))
        version = json.loads((extracted / ".crux" / "crux.json").read_text(encoding="utf-8"))["version"]
        for rel, meta in manifest["releases"][version]["files"].items():
            file = extracted / rel
            if file.is_file():
                assert hashlib.sha256(file.read_bytes()).hexdigest() == meta["checksum"], rel
