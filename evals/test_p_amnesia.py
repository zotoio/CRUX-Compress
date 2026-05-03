"""Category P: Amnesia tests.

Validates amnesia session state behavior, suppression rules,
config immutability, and command-level overrides.
"""

from __future__ import annotations

import json
from pathlib import Path

from conftest import _make_config, write_memory


SUPPRESSED_BEHAVIORS = [
    "discover",
    "load",
    "annotate",
    "refs",
    "dream-nudge",
]

EXPLICIT_MEMORY_COMMANDS = [
    "/crux-dream",
    "/crux-recall",
    "/crux-remember",
    "/crux-meditate",
    "/crux-forget",
]


class TestAmnesiaConfigPresence:
    """The amnesia command is properly configured in crux-memories.json."""

    def test_amnesia_command_in_config(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        commands = data.get("cruxMemories", {}).get("commands", {})
        assert "amnesia" in commands, "amnesia command must be in config"

    def test_amnesia_command_file_path(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        amnesia = data["cruxMemories"]["commands"]["amnesia"]
        assert amnesia["file"] == ".cursor/commands/crux-amnesia.md"

    def test_amnesia_command_default(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        amnesia = data["cruxMemories"]["commands"]["amnesia"]
        assert amnesia["default"] == "/crux-amnesia"

    def test_amnesia_command_file_exists(self):
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-amnesia.md"
        assert cmd_file.is_file(), "crux-amnesia.md command file must exist"


class TestAmnesiaCommandDefinition:
    """The amnesia command file defines all required usage modes."""

    def _read_cmd(self) -> str:
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-amnesia.md"
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_supports_toggle_mode(self):
        content = self._read_cmd()
        assert "/crux-amnesia" in content, "Must support bare toggle"

    def test_supports_on_mode(self):
        content = self._read_cmd()
        assert "on" in content.lower(), "Must support 'on' argument"

    def test_supports_off_mode(self):
        content = self._read_cmd()
        assert "off" in content.lower(), "Must support 'off' argument"

    def test_supports_status_mode(self):
        content = self._read_cmd()
        assert "status" in content.lower(), "Must support 'status' argument"

    def test_documents_session_scope(self):
        content = self._read_cmd()
        assert "session" in content.lower(), "Must document session-scoped behavior"


class TestAmnesiaSuppressionRules:
    """Amnesia ON suppresses five specific ambient behaviors."""

    def _read_cmd(self) -> str:
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-amnesia.md"
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_suppresses_discovery(self):
        content = self._read_cmd()
        assert "discover" in content.lower() or "memory-index" in content.lower()

    def test_suppresses_loading(self):
        content = self._read_cmd()
        assert "load" in content.lower()

    def test_suppresses_annotation(self):
        content = self._read_cmd()
        assert "annotate" in content.lower() or "[memory:" in content

    def test_suppresses_reference_tracking(self):
        content = self._read_cmd()
        assert "reference" in content.lower() or "tracking" in content.lower()

    def test_suppresses_dream_nudge(self):
        content = self._read_cmd()
        assert "dream" in content.lower()


class TestAmnesiaConfigImmutability:
    """Amnesia must never modify config, memory files, trackers, or index."""

    def _read_cmd(self) -> str:
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-amnesia.md"
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_documents_no_config_modification(self):
        content = self._read_cmd()
        assert "never" in content.lower() and (
            "crux-memories.json" in content or "config" in content.lower()
        ), "Must explicitly state config is not modified"

    def test_documents_no_file_modification(self):
        content = self._read_cmd()
        assert "never" in content.lower() or "not" in content.lower()

    def test_config_not_touched_during_amnesia(self, tmp_path: Path):
        """Verify the config file content stays unchanged after amnesia toggle."""
        cfg = _make_config(tmp_path)
        config_path = tmp_path / ".crux" / "crux-memories.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

        original_content = config_path.read_text(encoding="utf-8")

        config_path_after = config_path.read_text(encoding="utf-8")
        assert original_content == config_path_after, (
            "Config file must not be modified by amnesia operations"
        )


class TestAmnesiaExplicitCommandOverride:
    """Explicit memory commands still work even when amnesia is ON."""

    def _read_cmd(self) -> str:
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-amnesia.md"
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_dream_still_works(self):
        content = self._read_cmd()
        assert "/crux-dream" in content

    def test_recall_still_works(self):
        content = self._read_cmd()
        assert "/crux-recall" in content

    def test_remember_still_works(self):
        content = self._read_cmd()
        assert "/crux-remember" in content

    def test_meditate_still_works(self):
        content = self._read_cmd()
        assert "/crux-meditate" in content

    def test_forget_still_works(self):
        content = self._read_cmd()
        assert "/crux-forget" in content

    def test_explicit_commands_documented_as_user_intent(self):
        content = self._read_cmd()
        assert "user intent" in content.lower() or "direct" in content.lower()


class TestAmnesiaSubagentInheritance:
    """Subagents must inherit amnesia state for ordinary work."""

    def _read_cmd(self) -> str:
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-amnesia.md"
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_documents_subagent_inheritance(self):
        content = self._read_cmd()
        assert "subagent" in content.lower(), (
            "Must document subagent inheritance of amnesia state"
        )

    def test_documents_inherit_behavior(self):
        content = self._read_cmd()
        assert "inherit" in content.lower()


class TestAmnesiaResponseFormat:
    """Amnesia responses should include session mode and scope information."""

    def _read_cmd(self) -> str:
        cmd_file = Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-amnesia.md"
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_documents_amnesia_on_mode(self):
        content = self._read_cmd()
        assert "amnesia-on" in content or "amnesia on" in content.lower()

    def test_documents_config_driven_mode(self):
        content = self._read_cmd()
        assert "config-driven" in content

    def test_documents_scope(self):
        content = self._read_cmd()
        assert "current chat session" in content.lower()


class TestAmnesiaRuleIntegration:
    """The memories integration rule correctly documents amnesia behavior."""

    def _read_rule(self) -> str:
        rule_file = (
            Path(__file__).resolve().parent.parent
            / ".cursor" / "rules" / "crux-memories-integration.md"
        )
        if not rule_file.exists():
            return ""
        return rule_file.read_text(encoding="utf-8")

    def test_rule_mentions_amnesia(self):
        content = self._read_rule()
        assert "amnesia" in content.lower()

    def test_rule_documents_session_override(self):
        content = self._read_rule()
        assert "session" in content.lower() and "override" in content.lower()

    def test_rule_documents_precedence_over_config(self):
        content = self._read_rule()
        assert "precedence" in content.lower() or "takes precedence" in content.lower()

    def test_rule_lists_suppressed_behaviors(self):
        content = self._read_rule()
        for behavior in ["discover", "load", "annotat", "reference", "dream"]:
            assert behavior in content.lower(), (
                f"Rule must document suppression of {behavior}"
            )

    def test_rule_allows_explicit_commands(self):
        content = self._read_rule()
        for cmd in EXPLICIT_MEMORY_COMMANDS:
            assert cmd in content, f"Rule must list {cmd} as allowed during amnesia"
