"""Category K: Session Hook tests.

Validates session-start nudge when plan count exceeds threshold and
that disabling memories suppresses the nudge.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

HOOK_SCRIPT = (
    Path(__file__).resolve().parent.parent / ".cursor" / "hooks" / "crux-session-start.py"
)


def _write_config(tmp_path: Path, *, enable_memories: str = "true", threshold: int = 2) -> Path:
    cfg = {
        "platform": "cursor",
        "flags": [{"enableMemories": enable_memories}],
        "cruxMemories": {
            "enabled": enable_memories,
            "hooks": {
                "sessionStartNudge": {
                    "trigger": "sessionStart",
                    "watchDir": str(tmp_path / "plans"),
                    "threshold": threshold,
                    "message": "Time to dream! Run /crux-dream.",
                }
            },
        },
    }
    config_path = tmp_path / ".crux" / "crux-memories.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return config_path


def _run_hook(config_path: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["python3", str(HOOK_SCRIPT)],
        capture_output=True,
        text=True,
        input="{}",
        env={
            "PATH": "/usr/bin:/bin:/usr/local/bin",
            "HOME": str(config_path.parent.parent),
        },
        cwd=str(config_path.parent.parent),
    )


class TestNudgeAboveThreshold:
    """When plan dirs exceed the threshold, a nudge message is emitted."""

    def test_nudge_emitted_above_threshold(self, tmp_path: Path):
        config_path = _write_config(tmp_path, threshold=2)

        plans_dir = tmp_path / "plans"
        plans_dir.mkdir(parents=True, exist_ok=True)
        for i in range(3):
            (plans_dir / f"plan-{i:03d}").mkdir()

        result = _run_hook(config_path)
        assert result.returncode == 0, f"Hook failed: {result.stderr}"

        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError:
            output = {}

        ctx = output.get("additional_context", "")
        assert "Memory Nudge" in ctx or "dream" in ctx.lower(), (
            f"Expected nudge in output, got: {ctx!r}"
        )

    def test_nudge_contains_count_info(self, tmp_path: Path):
        config_path = _write_config(tmp_path, threshold=2)

        plans_dir = tmp_path / "plans"
        plans_dir.mkdir(parents=True, exist_ok=True)
        for i in range(5):
            (plans_dir / f"plan-{i:03d}").mkdir()

        result = _run_hook(config_path)
        output = json.loads(result.stdout) if result.stdout.strip() else {}
        ctx = output.get("additional_context", "")

        assert "5" in ctx or "items detected" in ctx


class TestNudgeSuppressedWhenDisabled:
    """When enableMemories is false, no nudge is produced regardless of plan count."""

    def test_no_nudge_when_disabled(self, tmp_path: Path):
        config_path = _write_config(tmp_path, enable_memories="false", threshold=1)

        plans_dir = tmp_path / "plans"
        plans_dir.mkdir(parents=True, exist_ok=True)
        for i in range(10):
            (plans_dir / f"plan-{i:03d}").mkdir()

        result = _run_hook(config_path)
        assert result.returncode == 0

        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError:
            output = {}

        ctx = output.get("additional_context", "")
        assert "Memory Nudge" not in ctx, (
            f"Nudge should not appear when disabled, got: {ctx!r}"
        )

    def test_empty_output_when_disabled_and_no_pending(self, tmp_path: Path):
        config_path = _write_config(tmp_path, enable_memories="false", threshold=1)
        (tmp_path / "plans").mkdir(parents=True, exist_ok=True)

        result = _run_hook(config_path)
        assert result.returncode == 0

        output = json.loads(result.stdout) if result.stdout.strip() else {}
        assert output == {} or output.get("additional_context", "") == ""
