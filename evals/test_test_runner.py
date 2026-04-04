"""Tests for scripts/test.py."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_SCRIPT = PROJECT_ROOT / "scripts" / "test.py"

_test_mod = None


def _load_test_script():
    global _test_mod
    if _test_mod is None:
        spec = importlib.util.spec_from_file_location("test_runner", str(TEST_SCRIPT))
        _test_mod = importlib.util.module_from_spec(spec)
        sys.modules["test_runner"] = _test_mod
        assert spec.loader is not None
        spec.loader.exec_module(_test_mod)
    return _test_mod


class TestTestRunner:
    def test_reports_no_automated_tests_when_pytest_missing(self, monkeypatch, capsys):
        mod = _load_test_script()

        def fake_which(name: str) -> str | None:
            return None if name == "pytest" else None

        monkeypatch.setattr(mod.shutil, "which", fake_which)
        monkeypatch.setattr(mod.sys, "argv", ["test.py"])

        result = mod.main()
        output = capsys.readouterr().out

        assert result == 0
        assert "Warning: pytest not found, skipping tests" in output
        assert "No automated tests were run" in output
        assert "All tests passed" not in output

    def test_reports_success_when_pytest_runs(self, monkeypatch, capsys):
        mod = _load_test_script()

        def fake_which(name: str) -> str | None:
            if name == "pytest":
                return "/usr/bin/pytest"
            return None

        def fake_run(*_args, **_kwargs):
            return subprocess.CompletedProcess(
                args=["/usr/bin/pytest", "evals/", "-v"],
                returncode=0,
            )

        monkeypatch.setattr(mod.shutil, "which", fake_which)
        monkeypatch.setattr(mod.subprocess, "run", fake_run)
        monkeypatch.setattr(mod.sys, "argv", ["test.py"])

        result = mod.main()
        output = capsys.readouterr().out

        assert result == 0
        assert "All tests passed" in output
        assert "No automated tests were run" not in output
