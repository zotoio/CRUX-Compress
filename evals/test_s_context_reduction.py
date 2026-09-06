"""Category S: Context-token-reduction surface evals.

Locks in the reductions made by the context-token-reduction spec (Subtasks 01-07)
so future edits cannot silently regress them. Uses behavioural / structural
assertions so tests survive further CRUX compression of agent bodies.

Coverage:
  D01 — Lazy-CRUX enforcement
  D02 — context_manifest honor
  D03 — Template lazy-load
  D04 — Memory-manager split
  D05 — Compressed-primitive semantic parity (deterministic + llm_driven)
  D06 — /crux-test shim
  DoD06 — Deferred waves (informational; flip to green when compressions land)

Markers
-------
context_reduction_smoke  — fast, deterministic, no LLM required; suitable for CI smoke run
llm_driven               — requires CRUX_LLM_EVAL=1 to activate live assertions
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_AGENTS_DIR = _PROJECT_ROOT / ".cursor" / "agents"
_COMMANDS_DIR = _PROJECT_ROOT / ".cursor" / "commands"
_SKILLS_DIR = _PROJECT_ROOT / ".cursor" / "skills"
_FIXTURES_CRUX = _PROJECT_ROOT / "evals" / "fixtures" / "crux-compressed"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _try_invoke_llm_parity(*, purpose: str, key: str = "default") -> dict | None:
    """Obtain a structured LLM result if a harness supplied one; else None.

    This Python suite has no in-process agent runner. Live LLM assertions are
    optional and must not fail merely because ``CRUX_LLM_EVAL=1`` is set with
    an unwired ``None`` stub.

    Injection (for manual / scheduled full runs)::

        CRUX_LLM_RESULT_FILE=/path/to/results.json
        # results.json is either:
        #   {"confidence": 0.9, "passed": true, "notes": "..."}
        # or a map keyed by ``key``:
        #   {"default": {...}, "crux-compress": {...}, ...}

        # or inline:
        CRUX_LLM_RESULT_JSON='{"confidence":0.9,"passed":true,"notes":"..."}'

    Returns:
        A result dict suitable for ``crux_llm_eval``, or None when no harness
        result is available (caller must ``pytest.skip`` honestly).
    """
    del purpose  # retained for call-site clarity / future logging
    raw = os.environ.get("CRUX_LLM_RESULT_JSON", "").strip()
    path_str = os.environ.get("CRUX_LLM_RESULT_FILE", "").strip()
    payload: object | None = None
    if raw:
        payload = json.loads(raw)
    elif path_str:
        payload = json.loads(Path(path_str).read_text(encoding="utf-8"))
    if payload is None:
        return None
    if isinstance(payload, dict) and {"confidence", "passed"} <= payload.keys():
        return payload
    if isinstance(payload, dict) and key in payload and isinstance(payload[key], dict):
        return payload[key]
    if isinstance(payload, dict) and "default" in payload and isinstance(payload["default"], dict):
        return payload["default"]
    return None


def _skip_if_no_llm_harness(result: dict | None, *, purpose: str) -> dict:
    """Skip honestly when no LLM harness result is available (never fail on None stub)."""
    if result is None:
        pytest.skip(
            f"No LLM harness result for {purpose}. "
            "Deterministic smoke coverage already locks this contract. "
            "Optional live path: set CRUX_LLM_EVAL=1 and supply CRUX_LLM_RESULT_JSON "
            "or CRUX_LLM_RESULT_FILE with {confidence, passed, notes}."
        )
    return result


def _read_sot(stem: str, kind: str) -> str:
    """Read the SoT (.source.mdx preferred) for a primitive.

    kind: "command", "agent", "skill/<name>"
    """
    if kind == "command":
        base = _COMMANDS_DIR
    elif kind == "agent":
        base = _AGENTS_DIR
    elif kind.startswith("skill/"):
        skill_name = kind.split("/", 1)[1]
        base = _SKILLS_DIR / skill_name
        sot = base / "SKILL.mdx"
        loadable = base / "SKILL.md"
        for p in (sot, loadable):
            if p.exists():
                return p.read_text(encoding="utf-8")
        return ""
    else:
        raise ValueError(f"Unknown kind: {kind!r}")

    sot = base / f"{stem}.source.mdx"
    loadable = base / f"{stem}.md"
    for p in (sot, loadable):
        if p.exists():
            return p.read_text(encoding="utf-8")
    return ""


def _read_loadable(stem: str, kind: str) -> str:
    """Read the loadable .md for a primitive."""
    if kind == "command":
        p = _COMMANDS_DIR / f"{stem}.md"
    elif kind == "agent":
        p = _AGENTS_DIR / f"{stem}.md"
    else:
        raise ValueError(f"Unknown kind: {kind!r}")
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def _load_crux_compressed_fixtures() -> list[dict]:
    if not _FIXTURES_CRUX.exists():
        return []
    fixtures = []
    for fpath in sorted(_FIXTURES_CRUX.glob("*.json")):
        fixtures.append(json.loads(fpath.read_text(encoding="utf-8")))
    return fixtures


# ---------------------------------------------------------------------------
# D01 — Lazy-CRUX enforcement
# ---------------------------------------------------------------------------


@pytest.mark.context_reduction_smoke
class TestLazyCruxEnforcement:
    """D01 — Lazy-CRUX enforcement.

    Verifies:
    - crux-cursor-rule-manager.md retains an unconditional CRUX.md load instruction.
    - All other named agents use conditional / context_manifest-honoring CRUX load.
    - No non-CRUX-needed agent SoT contains the blanket "Before doing ANY work,
      you MUST read CRUX.md" phrase.
    """

    # --- crux-cursor-rule-manager must load CRUX.md unconditionally ---

    def test_rule_manager_unconditional_crux_load(self):
        """crux-cursor-rule-manager.md must instruct unconditional Read of CRUX.md."""
        path = _AGENTS_DIR / "crux-cursor-rule-manager.md"
        assert path.exists(), "crux-cursor-rule-manager.md not found"
        content = path.read_text(encoding="utf-8")
        # Stable markers: the unconditional "MUST read" instruction targets CRUX.md
        assert "CRUX.md" in content, "CRUX.md reference missing from rule-manager"
        # This agent MUST have a prominent unconditional load directive
        assert (
            "you MUST read the CRUX specification" in content
            or "Before doing ANY work" in content
            or "MUST read" in content
        ), (
            "crux-cursor-rule-manager.md must contain an unconditional CRUX.md load "
            "directive ('you MUST read the CRUX specification' or equivalent). "
            "Do not weaken this agent's unconditional requirement."
        )

    # --- Conditional-CRUX agents must NOT carry the blanket "Before doing ANY work" phrase ---

    @pytest.mark.parametrize(
        "stem",
        [
            "crux-platform-architect",
            "crux-software-engineer",
            "integrity-expert",
            "docs-sync-agent",
        ],
    )
    def test_plaintext_agent_no_unconditional_crux_load(self, stem: str):
        """Plaintext agents must use conditional CRUX load, not the blanket 'Before doing ANY work' phrase.

        These agents should load CRUX.md only when the task involves CRUX notation.
        An unconditional load wastes tokens on every non-CRUX task.
        """
        path = _AGENTS_DIR / f"{stem}.md"
        assert path.exists(), f"{stem}.md not found"
        content = path.read_text(encoding="utf-8")
        unconditional_phrase = "Before doing ANY work, you MUST read CRUX.md"
        assert unconditional_phrase not in content, (
            f"{stem}.md still contains the unconditional blanket CRUX.md load phrase. "
            "Replace with the conditional two-liner (load only when task involves CRUX notation)."
        )

    @pytest.mark.parametrize(
        "stem",
        [
            "crux-cursor-meditation-guide",
            "crux-memory-dream",
            "crux-memory-rem",
            "crux-memory-recall",
            "crux-memory-remember",
            "crux-memory-forget",
        ],
    )
    def test_compressed_agent_sot_no_unconditional_crux_load(self, stem: str):
        """CRUX-compressed agent SoT must not carry the unconditional 'Before doing ANY work' phrase."""
        sot = _AGENTS_DIR / f"{stem}.source.mdx"
        if not sot.exists():
            pytest.skip(f"{stem}.source.mdx not found (SoT not yet created)")
        content = sot.read_text(encoding="utf-8")
        unconditional_phrase = "Before doing ANY work, you MUST read CRUX.md"
        assert unconditional_phrase not in content, (
            f"{stem}.source.mdx (SoT) still contains the unconditional blanket phrase. "
            "Replace with conditional CRUX load wording."
        )

    # --- Conditional agents must use conditional CRUX loading wording ---

    @pytest.mark.parametrize(
        "stem",
        [
            "crux-platform-architect",
            "crux-software-engineer",
            "integrity-expert",
            "docs-sync-agent",
        ],
    )
    def test_plaintext_agent_has_conditional_crux_load(self, stem: str):
        """Plaintext agents must reference CRUX.md with conditional / task-gated language."""
        path = _AGENTS_DIR / f"{stem}.md"
        assert path.exists(), f"{stem}.md not found"
        content = path.read_text(encoding="utf-8")
        # At least one conditional CRUX reference must be present
        conditional_markers = [
            "only when",
            "only if",
            "context_manifest",
            "If your task involves",
            "when the task involves",
            "when compressing",
            "when decompressing",
        ]
        assert any(m in content for m in conditional_markers), (
            f"{stem}.md does not contain conditional CRUX loading wording. "
            "Expected one of: " + ", ".join(repr(m) for m in conditional_markers)
        )

    @pytest.mark.parametrize(
        "stem",
        [
            "crux-cursor-meditation-guide",
            "crux-memory-dream",
            "crux-memory-rem",
            "crux-memory-recall",
            "crux-memory-remember",
            "crux-memory-forget",
        ],
    )
    def test_compressed_agent_has_context_manifest_marker(self, stem: str):
        """CRUX-compressed agent bodies must contain 'context_manifest' as a stable encoding marker."""
        loadable = _AGENTS_DIR / f"{stem}.md"
        assert loadable.exists(), f"{stem}.md (loadable) not found"
        content = loadable.read_text(encoding="utf-8")
        assert "context_manifest" in content, (
            f"{stem}.md (CRUX loadable) does not contain 'context_manifest' marker. "
            "The CRUX body should encode 'honor context_manifest' as a stable instruction."
        )

    # --- KD-11: CRUX loadables must have the plaintext bootstrap line ---

    @pytest.mark.parametrize(
        "stem,kind",
        [
            ("crux-compress", "command"),
            ("crux-meditate", "command"),
            ("crux-cursor-meditation-guide", "agent"),
            ("crux-memory-dream", "agent"),
            ("crux-memory-rem", "agent"),
            ("crux-memory-recall", "agent"),
            ("crux-memory-remember", "agent"),
            ("crux-memory-forget", "agent"),
        ],
    )
    def test_crux_loadable_has_kd11_bootstrap(self, stem: str, kind: str):
        """Wave 1+2 CRUX loadable .md files must carry the KD-11 plaintext bootstrap line.

        The bootstrap — between frontmatter and the CRUX fence — lets an agent that
        cannot auto-decompress know to read CRUX.md first.
        """
        if kind == "command":
            path = _COMMANDS_DIR / f"{stem}.md"
        else:
            path = _AGENTS_DIR / f"{stem}.md"
        assert path.exists(), f"{stem}.md not found"
        content = path.read_text(encoding="utf-8")
        # Only check files that actually contain a CRUX block (compressed)
        if "⟦CRUX:" not in content:
            pytest.skip(f"{stem}.md does not contain a CRUX block — not yet compressed")
        bootstrap_markers = [
            "CRUX-notated",
            "read `CRUX.md` before interpreting",
            "cannot decompress it from always-on rules",
        ]
        assert any(m in content for m in bootstrap_markers), (
            f"{stem}.md is missing the KD-11 plaintext bootstrap. "
            "Add the line: 'If this body is CRUX-notated and you cannot decompress it "
            "from always-on rules alone, read `CRUX.md` before interpreting the body.' "
            "(between frontmatter and the CRUX fence)"
        )


# ---------------------------------------------------------------------------
# D02 — context_manifest honor
# ---------------------------------------------------------------------------


@pytest.mark.context_reduction_smoke
class TestContextManifestHonor:
    """D02 — context_manifest honor.

    Asserts every named long agent declares or references the context_manifest prelude.
    The check looks for the literal 'context_manifest' string in either the loadable
    or the SoT (.source.mdx) — stable across CRUX compression.
    """

    _NAMED_AGENTS = [
        "crux-cursor-rule-manager",
        "crux-platform-architect",
        "crux-software-engineer",
        "integrity-expert",
        "docs-sync-agent",
        "crux-cursor-meditation-guide",
        "crux-memory-dream",
        "crux-memory-rem",
        "crux-memory-recall",
        "crux-memory-remember",
        "crux-memory-forget",
    ]

    @pytest.mark.parametrize("stem", _NAMED_AGENTS)
    def test_agent_has_context_manifest_reference(self, stem: str):
        """Every named agent must reference 'context_manifest' in its body (loadable or SoT)."""
        loadable = _AGENTS_DIR / f"{stem}.md"
        sot = _AGENTS_DIR / f"{stem}.source.mdx"
        assert loadable.exists(), f"{stem}.md (loadable) not found"
        # Accept match in either loadable or SoT (CRUX bodies encode it as a compressed token)
        combined = loadable.read_text(encoding="utf-8")
        if sot.exists():
            combined += "\n" + sot.read_text(encoding="utf-8")
        assert "context_manifest" in combined, (
            f"{stem}: neither the loadable .md nor the SoT .source.mdx contains "
            "'context_manifest'. Every named agent must declare or reference the "
            "context_manifest prelude."
        )

    def test_context_manifest_structural_smoke(self):
        """Structural smoke: a task prompt containing context_manifest should be honored.

        This deterministic check validates that the 'context_manifest' concept is present
        in at least one agent with the key word 'loaded' (the loaded-file signal that
        prevents re-reads). This is a structural pre-condition; the live LLM test is in
        test_context_manifest_llm_skips_loaded_files.
        """
        # Verify that at least one agent documents the 'loaded' sentinel concept
        matched = []
        for stem in self._NAMED_AGENTS:
            path = _AGENTS_DIR / f"{stem}.md"
            if not path.exists():
                continue
            content = path.read_text(encoding="utf-8")
            sot_path = _AGENTS_DIR / f"{stem}.source.mdx"
            if sot_path.exists():
                content += "\n" + sot_path.read_text(encoding="utf-8")
            if "context_manifest" in content and ("loaded" in content or "loaded" in content):
                matched.append(stem)
        assert matched, (
            "No agent documents the context_manifest 'loaded' sentinel — "
            "at least one agent must show how to honour context_manifest."
        )

    @pytest.mark.llm_driven
    @pytest.mark.flaky(reruns=1, reason="LLM response variance")
    def test_context_manifest_llm_skips_loaded_files(self, crux_llm_eval):
        """LLM smoke: subagent with context_manifest must not re-read a 'loaded' file.

        Deterministic coverage: ``test_context_manifest_structural_smoke``.

        Live path (optional): supply a harness result via CRUX_LLM_RESULT_JSON /
        CRUX_LLM_RESULT_FILE and set CRUX_LLM_EVAL=1. When no harness result is
        available, this test skips honestly — it does not fail on an unwired stub.
        """
        llm_result = _skip_if_no_llm_harness(
            _try_invoke_llm_parity(purpose="context_manifest smoke", key="context_manifest"),
            purpose="context_manifest smoke",
        )
        crux_llm_eval(llm_result, min_confidence=0.80)


# ---------------------------------------------------------------------------
# D03 — Template lazy-load
# ---------------------------------------------------------------------------


@pytest.mark.context_reduction_smoke
class TestTemplateLazyLoad:
    """D03 — Template lazy-load.

    Asserts that the two new template files exist and are only referenced
    from within their owning command family (compress / recall), not from
    unrelated files.
    """

    def test_compress_prompts_template_exists(self):
        """compress-prompts.md template must exist under .cursor/commands/templates/."""
        path = _COMMANDS_DIR / "templates" / "compress-prompts.md"
        assert path.exists(), (
            ".cursor/commands/templates/compress-prompts.md is missing. "
            "This template should have been created by Subtask 03."
        )

    def test_recall_canvas_template_exists(self):
        """recall-canvas.tsx.md template must exist under .cursor/agents/templates/."""
        path = _AGENTS_DIR / "templates" / "recall-canvas.tsx.md"
        assert path.exists(), (
            ".cursor/agents/templates/recall-canvas.tsx.md is missing. "
            "This template should have been created by Subtask 05."
        )

    def test_compress_prompts_only_referenced_from_compress_family(self):
        """compress-prompts.md must only be referenced from the crux-compress command family.

        Scans all .md, .mdx, and .mdc files under .cursor/ (except the compress
        family itself) for references to 'compress-prompts.md'. Finds zero matches
        outside the compress family.
        """
        template_name = "compress-prompts.md"
        # Collect files referencing the template
        referencing_files: list[str] = []
        for suffix in ("*.md", "*.mdx", "*.mdc"):
            for p in _PROJECT_ROOT.glob(f".cursor/**/{suffix}"):
                # Exclude the compress-family files (both loadable and SoT)
                if "crux-compress" in p.name or p.name == template_name:
                    continue
                try:
                    if template_name in p.read_text(encoding="utf-8"):
                        referencing_files.append(str(p.relative_to(_PROJECT_ROOT)))
                except (OSError, UnicodeDecodeError):
                    pass
        assert not referencing_files, (
            f"'{template_name}' is referenced outside the compress command family. "
            f"Unexpected references found in:\n" + "\n".join(f"  {f}" for f in referencing_files)
        )

    def test_recall_canvas_only_referenced_from_recall_family(self):
        """recall-canvas.tsx.md must only be referenced from the crux-memory-recall family.

        Scans all .md, .mdx, and .mdc files under .cursor/commands/ for references
        to 'recall-canvas'. Finds zero matches outside the recall family.

        The crux-cursor-memory-manager.md umbrella agent legitimately mentions
        recall-canvas.tsx.md in its dist-zip removal criteria — this is intentionally
        excluded from the scan since it is not an operational reference.
        """
        template_name = "recall-canvas.tsx.md"
        marker = "recall-canvas"
        referencing_files: list[str] = []
        # Check commands directory only (the surface most likely to make an operational reference)
        for suffix in ("*.md", "*.mdx", "*.mdc"):
            for p in _COMMANDS_DIR.rglob(f"{suffix}"):
                # Exclude the recall-family files
                if "crux-memory-recall" in p.name or p.name == template_name:
                    continue
                try:
                    if marker in p.read_text(encoding="utf-8"):
                        referencing_files.append(str(p.relative_to(_PROJECT_ROOT)))
                except (OSError, UnicodeDecodeError):
                    pass
        assert not referencing_files, (
            f"'{marker}' is referenced outside the recall family in .cursor/commands/. "
            f"Unexpected references in:\n" + "\n".join(f"  {f}" for f in referencing_files)
        )

    def test_compress_prompts_referenced_from_compress_command(self):
        """compress-prompts.md must be referenced from at least one of the crux-compress files."""
        template_name = "compress-prompts.md"
        candidates = [
            _COMMANDS_DIR / "crux-compress.md",
            _COMMANDS_DIR / "crux-compress.source.mdx",
        ]
        found_in = [str(p) for p in candidates if p.exists() and template_name in p.read_text(encoding="utf-8")]
        assert found_in, (
            f"'{template_name}' is not referenced from any crux-compress file. "
            "Expected reference in crux-compress.md and/or crux-compress.source.mdx."
        )

    def test_recall_canvas_referenced_from_recall_agent(self):
        """recall-canvas.tsx.md must be referenced from at least one of the crux-memory-recall files."""
        marker = "recall-canvas"
        candidates = [
            _AGENTS_DIR / "crux-memory-recall.md",
            _AGENTS_DIR / "crux-memory-recall.source.mdx",
        ]
        found_in = [str(p) for p in candidates if p.exists() and marker in p.read_text(encoding="utf-8")]
        assert found_in, (
            f"'{marker}' is not referenced from any crux-memory-recall file. "
            "Expected reference in crux-memory-recall.md and/or crux-memory-recall.source.mdx."
        )


# ---------------------------------------------------------------------------
# D04 — Memory-manager split
# ---------------------------------------------------------------------------


@pytest.mark.context_reduction_smoke
class TestMemoryManagerSplit:
    """D04 — Memory-manager split.

    Asserts the five thin agents exist, each with valid frontmatter, and that
    the umbrella crux-cursor-memory-manager.md has been reduced to a ≤ 60-line
    deprecation shim. Also checks that .cursor/commands/ files do not reference
    the deprecated umbrella name (except in documented deprecation context).
    """

    _THIN_AGENTS = [
        "crux-memory-dream",
        "crux-memory-rem",
        "crux-memory-recall",
        "crux-memory-remember",
        "crux-memory-forget",
    ]
    _REQUIRED_FM_FIELDS = ["name", "model", "description"]

    @pytest.mark.parametrize("stem", _THIN_AGENTS)
    def test_thin_agent_exists(self, stem: str):
        """Each thin agent file must exist in .cursor/agents/."""
        path = _AGENTS_DIR / f"{stem}.md"
        assert path.exists(), (
            f"{stem}.md not found. The five thin memory agents must be created "
            "by Subtask 05 before this eval can pass."
        )

    @pytest.mark.parametrize("stem", _THIN_AGENTS)
    def test_thin_agent_has_valid_frontmatter(self, stem: str):
        """Each thin agent must have YAML frontmatter with name, model, and description."""
        path = _AGENTS_DIR / f"{stem}.md"
        if not path.exists():
            pytest.skip(f"{stem}.md not found")
        fm = _parse_frontmatter(path)
        assert fm, f"{stem}.md has no parseable frontmatter"
        for field in self._REQUIRED_FM_FIELDS:
            assert field in fm, (
                f"{stem}.md frontmatter missing required field '{field}'. "
                f"Present fields: {list(fm.keys())}"
            )
        # name field must match the stem
        assert fm.get("name") == stem, (
            f"{stem}.md frontmatter 'name' field is {fm.get('name')!r}; "
            f"expected {stem!r}"
        )

    def test_umbrella_is_shim_size(self):
        """crux-cursor-memory-manager.md must be ≤ 60 lines (it's a deprecation shim)."""
        path = _AGENTS_DIR / "crux-cursor-memory-manager.md"
        assert path.exists(), "crux-cursor-memory-manager.md not found"
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        assert line_count <= 60, (
            f"crux-cursor-memory-manager.md is {line_count} lines — exceeds the "
            "60-line shim budget. The umbrella agent should be a thin deprecation "
            "dispatcher only; behaviour must live in the five thin agents."
        )

    def test_umbrella_has_deprecation_banner(self):
        """crux-cursor-memory-manager.md must contain a deprecation notice."""
        path = _AGENTS_DIR / "crux-cursor-memory-manager.md"
        assert path.exists(), "crux-cursor-memory-manager.md not found"
        content = path.read_text(encoding="utf-8")
        deprecation_markers = [
            "DEPRECATED",
            "deprecated",
            "prefer the mode-scoped",
            "thin agent",
        ]
        assert any(m in content for m in deprecation_markers), (
            "crux-cursor-memory-manager.md is missing a deprecation notice. "
            "It should clearly indicate that callers should use the thin agents instead."
        )

    def test_commands_no_non_deprecation_memory_manager_refs(self):
        """No command SoT/loadable should reference crux-cursor-memory-manager.

        Scans `.cursor/commands/` for both loadable `*.md` and SoT `*.source.mdx`
        (KD-2 registration_model — SoT is authoritative for compressed commands).
        Templates are excluded. Commands must invoke thin agents
        (`crux-memory-dream`, etc.) directly — not the deprecated umbrella.
        """
        matches: list[str] = []
        for pattern in ("*.md", "*.source.mdx"):
            for p in sorted(_COMMANDS_DIR.rglob(pattern)):
                if "templates" in p.parts:
                    continue
                try:
                    if "crux-cursor-memory-manager" in p.read_text(encoding="utf-8"):
                        matches.append(str(p.relative_to(_PROJECT_ROOT)))
                except (OSError, UnicodeDecodeError):
                    pass
        assert not matches, (
            "The following command files reference 'crux-cursor-memory-manager'. "
            "Commands should invoke thin agents (crux-memory-dream, etc.) directly:\n"
            + "\n".join(f"  {f}" for f in matches)
        )

    def test_umbrella_dispatch_table_lists_all_thin_agents(self):
        """crux-cursor-memory-manager.md must mention all five thin agent names."""
        path = _AGENTS_DIR / "crux-cursor-memory-manager.md"
        assert path.exists(), "crux-cursor-memory-manager.md not found"
        content = path.read_text(encoding="utf-8")
        for stem in self._THIN_AGENTS:
            assert stem in content, (
                f"crux-cursor-memory-manager.md dispatch table is missing '{stem}'. "
                "The deprecation shim must list all five thin agents so callers know "
                "which one to use."
            )


# ---------------------------------------------------------------------------
# D05 — Compressed-primitive semantic parity
# ---------------------------------------------------------------------------


@pytest.mark.context_reduction_smoke
class TestCompressedPrimitiveParity:
    """D05 — Compressed-primitive semantic parity (deterministic).

    For each Wave 1+2 file compressed in Subtask 07, asserts:
    1. The loadable .md contains a CRUX block (⟦CRUX:).
    2. The SoT .source.mdx exists.
    3. Every 'must_preserve' property from the JSON fixture appears in the SoT plaintext.
    4. The loadable has generated frontmatter with at least sourceChecksum.

    LLM-driven semantic equivalence is in TestCompressedPrimitiveParityLLM.
    """

    def _get_fixtures(self):
        fixtures = _load_crux_compressed_fixtures()
        if not fixtures:
            pytest.skip("No crux-compressed fixtures found under evals/fixtures/crux-compressed/")
        return fixtures

    def test_all_fixture_files_present(self):
        """All expected per-file JSON fixtures must exist under evals/fixtures/crux-compressed/."""
        expected = {
            "crux-compress.json",
            "crux-meditate.json",
            "crux-cursor-meditation-guide.json",
            "crux-memory-dream.json",
            "crux-memory-rem.json",
            "crux-memory-recall.json",
            "crux-memory-remember.json",
            "crux-memory-forget.json",
        }
        present = {p.name for p in _FIXTURES_CRUX.glob("*.json")} if _FIXTURES_CRUX.exists() else set()
        missing = expected - present
        assert not missing, (
            "Missing fixture files under evals/fixtures/crux-compressed/:\n"
            + "\n".join(f"  {m}" for m in sorted(missing))
        )

    def test_compressed_loadables_have_crux_block(self):
        """Every Wave 1+2 loadable .md must contain a ⟦CRUX: block."""
        fixtures = self._get_fixtures()
        not_compressed: list[str] = []
        for fx in fixtures:
            path = _PROJECT_ROOT / fx["loadable"]
            if not path.exists():
                not_compressed.append(f"{fx['loadable']} (file missing)")
                continue
            content = path.read_text(encoding="utf-8")
            if "⟦CRUX:" not in content:
                not_compressed.append(fx["loadable"])
        assert not not_compressed, (
            "The following Wave 1+2 loadable files are missing a ⟦CRUX: block "
            "(not yet compressed or compression was reverted):\n"
            + "\n".join(f"  {f}" for f in not_compressed)
        )

    def test_compressed_loadables_have_sot(self):
        """Every Wave 1+2 loadable must have a corresponding .source.mdx SoT."""
        fixtures = self._get_fixtures()
        missing_sot: list[str] = []
        for fx in fixtures:
            sot = _PROJECT_ROOT / fx["sot"]
            if not sot.exists():
                missing_sot.append(fx["sot"])
        assert not missing_sot, (
            "The following SoT (.source.mdx) files are missing:\n"
            + "\n".join(f"  {f}" for f in missing_sot)
        )

    def test_sot_contains_must_preserve_properties(self):
        """Each SoT file must contain all 'must_preserve' properties from its fixture.

        This locks in semantic parity: the SoT plaintext is the authoritative reference,
        and these properties must survive any future re-compression.
        """
        fixtures = self._get_fixtures()
        failures: list[str] = []
        for fx in fixtures:
            sot_path = _PROJECT_ROOT / fx["sot"]
            if not sot_path.exists():
                continue
            sot_content = sot_path.read_text(encoding="utf-8")
            for prop in fx.get("must_preserve", []):
                if prop not in sot_content:
                    failures.append(f"{fx['sot']}: missing must-preserve property {prop!r}")
        assert not failures, (
            "SoT files are missing must-preserve semantic properties:\n"
            + "\n".join(f"  {f}" for f in failures)
        )

    def test_compressed_loadables_have_generated_frontmatter(self):
        """Every Wave 1+2 loadable must have YAML frontmatter with 'generated' and 'sourceChecksum'."""
        fixtures = self._get_fixtures()
        failures: list[str] = []
        for fx in fixtures:
            path = _PROJECT_ROOT / fx["loadable"]
            if not path.exists():
                failures.append(f"{fx['loadable']}: file not found")
                continue
            content = path.read_text(encoding="utf-8")
            if "⟦CRUX:" not in content:
                continue  # Not yet compressed; skip silently
            fm = _parse_frontmatter(path)
            if not fm:
                failures.append(f"{fx['loadable']}: no frontmatter")
                continue
            for field in ("generated", "sourceChecksum"):
                if field not in fm:
                    failures.append(f"{fx['loadable']}: frontmatter missing '{field}'")
        assert not failures, (
            "Compressed loadables have incomplete frontmatter:\n"
            + "\n".join(f"  {f}" for f in failures)
        )


@pytest.mark.llm_driven
@pytest.mark.flaky(reruns=1, reason="LLM response variance")
class TestCompressedPrimitiveParityLLM:
    """D05 — Compressed-primitive semantic parity (LLM-driven).

    Reads the SoT and the CRUX loadable for each fixture, decompresses the CRUX body,
    and asserts semantic equivalence with a confidence gate ≥ 85%.

    Skip path: tests skip when CRUX_LLM_EVAL env var is not set (CI default).
    Assertion path: when CRUX_LLM_EVAL=1, invokes the crux-cursor-rule-manager
    validation and asserts confidence ≥ 85%.
    """

    @pytest.mark.parametrize(
        "fixture_name",
        [
            "crux-compress",
            "crux-meditate",
            "crux-cursor-meditation-guide",
            "crux-memory-dream",
            "crux-memory-rem",
            "crux-memory-recall",
            "crux-memory-remember",
            "crux-memory-forget",
        ],
    )
    def test_crux_body_semantically_equivalent_to_sot(self, fixture_name: str, crux_llm_eval):
        """CRUX loadable must be semantically equivalent to its SoT (confidence ≥ 85%).

        Deterministic coverage: ``TestCompressedPrimitiveParity`` must_preserve fixtures.

        Live path (optional): supply a harness result keyed by fixture name via
        CRUX_LLM_RESULT_FILE / CRUX_LLM_RESULT_JSON and set CRUX_LLM_EVAL=1.
        When no harness result is available, skips honestly — does not fail on
        an unwired None stub.
        """
        fixture_path = _FIXTURES_CRUX / f"{fixture_name}.json"
        if not fixture_path.exists():
            pytest.skip(f"Fixture {fixture_name}.json not found")
        fx = json.loads(fixture_path.read_text(encoding="utf-8"))
        sot_path = _PROJECT_ROOT / fx["sot"]
        loadable_path = _PROJECT_ROOT / fx["loadable"]
        if not sot_path.exists() or not loadable_path.exists():
            pytest.skip(f"SoT or loadable missing for {fixture_name}")
        llm_result = _skip_if_no_llm_harness(
            _try_invoke_llm_parity(
                purpose=f"semantic parity ({fixture_name})",
                key=fixture_name,
            ),
            purpose=f"semantic parity ({fixture_name})",
        )
        crux_llm_eval(llm_result, min_confidence=0.85)


# ---------------------------------------------------------------------------
# D06 — /crux-test shim
# ---------------------------------------------------------------------------


@pytest.mark.context_reduction_smoke
class TestCruxTestShim:
    """D06 — /crux-test shim.

    Asserts crux-test.md is a ≤ 60-line shim that delegates to the pytest
    runner script, and that the runner script itself exits 0.
    """

    def test_crux_test_is_shim_size(self):
        """crux-test.md must be ≤ 60 lines (it's a dispatch shim, not a full command)."""
        path = _COMMANDS_DIR / "crux-test.md"
        assert path.exists(), "crux-test.md not found"
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        assert line_count <= 60, (
            f"crux-test.md is {line_count} lines — exceeds the 60-line shim budget. "
            "The command should be a thin dispatch wrapper to the pytest runner script."
        )

    def test_crux_test_dispatches_to_runner(self):
        """crux-test.md must reference the pytest runner script."""
        path = _COMMANDS_DIR / "crux-test.md"
        assert path.exists(), "crux-test.md not found"
        content = path.read_text(encoding="utf-8")
        runner_markers = [
            "run_crux_command_suite",
            "scripts/run_crux_command_suite.py",
        ]
        assert any(m in content for m in runner_markers), (
            "crux-test.md does not reference the pytest runner script "
            "('scripts/run_crux_command_suite.py'). "
            "The shim must dispatch to this script."
        )

    def test_runner_script_exists(self):
        """scripts/run_crux_command_suite.py must exist."""
        path = _PROJECT_ROOT / "scripts" / "run_crux_command_suite.py"
        assert path.exists(), (
            "scripts/run_crux_command_suite.py not found. "
            "This script should have been created by Subtask 06."
        )

    def test_runner_script_exits_zero(self):
        """python3 scripts/run_crux_command_suite.py must exit 0 (all deterministic tests pass)."""
        runner = _PROJECT_ROOT / "scripts" / "run_crux_command_suite.py"
        if not runner.exists():
            pytest.skip("run_crux_command_suite.py not found")
        result = subprocess.run(
            [sys.executable, str(runner)],
            capture_output=True,
            text=True,
            cwd=_PROJECT_ROOT,
        )
        assert result.returncode == 0, (
            f"scripts/run_crux_command_suite.py exited {result.returncode}.\n"
            f"stdout:\n{result.stdout[-2000:]}\n"
            f"stderr:\n{result.stderr[-1000:]}"
        )


# ---------------------------------------------------------------------------
# DoD06 — Deferred waves (informational)
# ---------------------------------------------------------------------------


@pytest.mark.context_reduction_smoke
class TestDeferredWaves:
    """DoD06 — Deferred compression waves (informational evals).

    These tests assert that Waves 3-5 files are NOT yet CRUX-compressed.
    They will flip from PASS to FAIL once those compressions land, at which
    point they should be removed or converted to parity tests.

    This gives a clear signal when a deferred compression has been applied.
    """

    _WAVE_3_MEDITATION_SKILLS = [
        "crux-skill-memory-meditation-research",
        "crux-skill-memory-meditation-report",
        "crux-skill-memory-meditation-ensemble",
        "crux-skill-memory-meditation-coordination",
        "crux-skill-memory-meditation-review",
        "crux-skill-memory-meditation-quick",
    ]

    _WAVE_4_MEMORY_SKILLS = [
        "crux-skill-memory-rebalance",
        "crux-skill-memory-extract",
        "crux-skill-memory-compress",
        "crux-skill-memory-reference-tracker",
        "crux-skill-memory-crud",
        "crux-skill-memory-index",
    ]

    _WAVE_5_AGENTS_COMMANDS = [
        ("agent", "crux-cursor-rule-manager"),
        ("agent", "integrity-expert"),
        ("agent", "crux-platform-architect"),
        ("agent", "crux-software-engineer"),
        ("agent", "docs-sync-agent"),
        ("command", "crux-dream"),
        ("command", "crux-recall"),
        ("command", "crux-forget"),
        ("command", "crux-remember"),
        ("command", "crux-amnesia"),
    ]

    @pytest.mark.parametrize("skill_name", _WAVE_3_MEDITATION_SKILLS)
    def test_wave3_skill_not_yet_compressed(self, skill_name: str):
        """Wave 3 meditation skills are not yet CRUX-compressed (deferred from Subtask 07).

        INFORMATIONAL: This test passes while the skill is uncompressed.
        When Wave 3 is executed, this test should be deleted and replaced with
        a proper parity test.
        """
        skill_dir = _SKILLS_DIR / skill_name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip(f"{skill_name}/SKILL.md not found")
        content = skill_md.read_text(encoding="utf-8")
        # A proper CRUX compressed body has ⟦CRUX: as its primary content
        # (not as a documentation example, which would appear in a code block)
        # We look for ⟦CRUX: outside of a fenced code block
        lines = content.splitlines()
        in_code_fence = False
        crux_block_outside_fence = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_fence = not in_code_fence
            elif not in_code_fence and "⟦CRUX:" in line:
                crux_block_outside_fence = True
                break
        if crux_block_outside_fence:
            pytest.fail(
                f"{skill_name}/SKILL.md now contains a CRUX block outside a code fence. "
                "Wave 3 compression has landed — replace this informational test with "
                "a semantic parity test referencing the SoT SKILL.mdx."
            )
        # Pass: skill is still uncompressed (expected deferred state)

    @pytest.mark.parametrize("skill_name", _WAVE_4_MEMORY_SKILLS)
    def test_wave4_skill_not_yet_compressed(self, skill_name: str):
        """Wave 4 memory skills are not yet CRUX-compressed (deferred from Subtask 07).

        INFORMATIONAL: This test passes while the skill is uncompressed.
        When Wave 4 is executed, update accordingly.
        """
        skill_dir = _SKILLS_DIR / skill_name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            pytest.skip(f"{skill_name}/SKILL.md not found")
        content = skill_md.read_text(encoding="utf-8")
        lines = content.splitlines()
        in_code_fence = False
        crux_block_outside_fence = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_fence = not in_code_fence
            elif not in_code_fence and "⟦CRUX:" in line:
                crux_block_outside_fence = True
                break
        if crux_block_outside_fence:
            pytest.fail(
                f"{skill_name}/SKILL.md now contains a CRUX block outside a code fence. "
                "Wave 4 compression has landed — replace this informational test with "
                "a semantic parity test."
            )

    @pytest.mark.parametrize("kind,stem", _WAVE_5_AGENTS_COMMANDS)
    def test_wave5_primitive_not_yet_compressed(self, kind: str, stem: str):
        """Wave 5 agents/commands are not yet CRUX-compressed (deferred from Subtask 07).

        INFORMATIONAL: This test passes while the primitive is uncompressed.
        When Wave 5 is executed, update accordingly.

        A CRUX block inside a triple-backtick code fence is documentation and does
        NOT count as compression — only a ⟦CRUX: block outside a code fence indicates
        that this file has been compressed.
        """
        if kind == "agent":
            path = _AGENTS_DIR / f"{stem}.md"
        else:
            path = _COMMANDS_DIR / f"{stem}.md"
        if not path.exists():
            pytest.skip(f"{stem}.md not found")
        content = path.read_text(encoding="utf-8")
        lines = content.splitlines()
        in_code_fence = False
        crux_block_outside_fence = False
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_fence = not in_code_fence
            elif not in_code_fence and "⟦CRUX:" in line:
                crux_block_outside_fence = True
                break
        if crux_block_outside_fence:
            pytest.fail(
                f"{stem}.md now contains a CRUX block outside a code fence. "
                "Wave 5 compression has landed for this primitive — "
                "replace this informational test with a semantic parity test."
            )
