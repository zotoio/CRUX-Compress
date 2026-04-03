"""Tests for create-crux-zip.sh.

Validates that the distribution zip is created correctly with all required
files, correct versioning, and expected structure.
"""

from __future__ import annotations

import json
import subprocess
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREATE_ZIP = PROJECT_ROOT / "scripts" / "create-crux-zip.sh"


def _run_zip(output_dir: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(CREATE_ZIP), str(output_dir)],
        capture_output=True, text=True, cwd=str(PROJECT_ROOT),
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
    def _get_names(self, tmp_path: Path) -> list[str]:
        result = _run_zip(tmp_path)
        assert result.returncode == 0
        zp = _get_zip_path(tmp_path)
        with zipfile.ZipFile(zp) as zf:
            return zf.namelist()

    def test_contains_crux_md(self, tmp_path: Path):
        names = self._get_names(tmp_path)
        assert any("CRUX.md" in n for n in names)

    def test_contains_agents_crux_md(self, tmp_path: Path):
        names = self._get_names(tmp_path)
        assert any("AGENTS.crux.md" in n for n in names)

    def test_contains_crux_json(self, tmp_path: Path):
        names = self._get_names(tmp_path)
        assert any(".crux/crux.json" in n for n in names)

    def test_contains_hooks_json(self, tmp_path: Path):
        names = self._get_names(tmp_path)
        assert any(".cursor/hooks.json" in n for n in names)

    def test_contains_rule_manager(self, tmp_path: Path):
        names = self._get_names(tmp_path)
        assert any("crux-cursor-rule-manager.md" in n for n in names)

    def test_contains_crux_compress_command(self, tmp_path: Path):
        names = self._get_names(tmp_path)
        assert any("crux-compress.md" in n for n in names)

    def test_contains_detect_changes_hook(self, tmp_path: Path):
        names = self._get_names(tmp_path)
        assert any("crux-detect-changes.py" in n for n in names)

    def test_contains_crux_rule(self, tmp_path: Path):
        names = self._get_names(tmp_path)
        assert any("_CRUX-RULE.mdc" in n for n in names)

    def test_contains_crux_utils_skill(self, tmp_path: Path):
        names = self._get_names(tmp_path)
        assert any("crux-utils/SKILL.md" in n for n in names)
        assert any("crux-utils.sh" in n for n in names)


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
