"""Tests for the CRUX plugin registry.

Validates registry schema, required fields, enabledByDefault semantics,
and the compression-level plugin entry.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / ".crux" / "plugins" / "registry.json"

REQUIRED_PLUGIN_FIELDS = {"description", "hooks", "failClosed"}


class TestRegistryFile:
    def test_exists(self):
        assert REGISTRY_PATH.is_file()

    def test_valid_json(self):
        json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_has_plugins_key(self):
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        assert "plugins" in data
        assert isinstance(data["plugins"], dict)

    def test_not_empty(self):
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        assert len(data["plugins"]) > 0


class TestPluginSchema:
    def _plugins(self) -> dict:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))["plugins"]

    def test_all_plugins_have_required_fields(self):
        for name, entry in self._plugins().items():
            for field in REQUIRED_PLUGIN_FIELDS:
                assert field in entry, f"Plugin '{name}' missing required field '{field}'"

    def test_description_is_string(self):
        for name, entry in self._plugins().items():
            assert isinstance(entry["description"], str), f"Plugin '{name}' description is not a string"

    def test_hooks_is_list_of_strings(self):
        for name, entry in self._plugins().items():
            assert isinstance(entry["hooks"], list), f"Plugin '{name}' hooks is not a list"
            for hook in entry["hooks"]:
                assert isinstance(hook, str), f"Plugin '{name}' has non-string hook: {hook}"

    def test_failClosed_is_bool(self):
        for name, entry in self._plugins().items():
            assert isinstance(entry["failClosed"], bool), f"Plugin '{name}' failClosed is not a boolean"

    def test_enabledByDefault_is_bool_when_present(self):
        for name, entry in self._plugins().items():
            if "enabledByDefault" in entry:
                assert isinstance(entry["enabledByDefault"], bool), (
                    f"Plugin '{name}' enabledByDefault is not a boolean"
                )


class TestCompressionLevelPlugin:
    def _plugin(self) -> dict:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))["plugins"]["compression-level"]

    def test_exists(self):
        plugins = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))["plugins"]
        assert "compression-level" in plugins

    def test_enabled_by_default(self):
        assert self._plugin()["enabledByDefault"] is True

    def test_hooks(self):
        hooks = self._plugin()["hooks"]
        assert "beforeCompress" in hooks
        assert "afterCompress" in hooks

    def test_fail_closed_is_false(self):
        assert self._plugin()["failClosed"] is False


class TestExistingPluginsUnchanged:
    """Verify that non-compression-level plugins still have enabledByDefault: false."""

    def _plugins(self) -> dict:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))["plugins"]

    def test_other_plugins_not_enabled_by_default(self):
        for name, entry in self._plugins().items():
            if name == "compression-level":
                continue
            if "enabledByDefault" in entry:
                assert entry["enabledByDefault"] is False, (
                    f"Plugin '{name}' should have enabledByDefault: false"
                )

    def test_known_plugins_present(self):
        plugins = self._plugins()
        for name in ("frontmatter-tagger", "quality-gate", "release-notes"):
            assert name in plugins, f"Expected plugin '{name}' not found in registry"
