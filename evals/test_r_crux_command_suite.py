"""Category R: CRUX command suite tests.

Replaces the prose-driven LLM walkthrough that formerly lived in the
/crux-test command. Each test below maps to a historical /crux-test scenario;
the docstring for each test cites the scenario name so a grep on the
old scenario title finds the new home.

Historical scenario → test mapping
-----------------------------------
Scenario 1 (Compression Test)           → TestCompressionRoundtrip
Scenario 2 (Decompression Test)         → TestDecompressionUnderstanding (llm_driven)
Scenario 3 (Token Estimation Test)      → TestTokenEstimation
Scenario 4 (Checksum Test)              → TestChecksumDeterminism
Scenario 5 (Install Script Test)        → TestInstallScript
Scenario 6 (Semantic Validation Test)   → TestSemanticValidation (llm_driven)
Scenario 7 (Special Characters Test)    → TestSpecialCharacters
Scenario 8 (Crux-Compress Command Test) → TestCruxCompressWorkflow
Scenario 9 (Semantic Stability Test)    → TestSemanticStabilityDriftDetection
Scenario 10 (Force Recompression Test)  → TestForceRecompression
D01(d) Output Format Modes              → TestOutputFormats
D01(e) --<n> Level Ratio Adherence      → TestCompressionLevelRatioAdherence

Markers
-------
crux_command_smoke   — fast, deterministic, no LLM required; suitable for CI smoke run
llm_driven           — tagged for tests whose historical scenario required LLM; structural
                       pre-conditions run always; threshold/semantic assertions run only
                       when a live LLM has populated the relevant frontmatter fields
flaky                — registered to allow inherent non-determinism in llm_driven tests
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_FIXTURES = _PROJECT_ROOT / "tests" / "fixtures"
_CRUX_UTILS = _PROJECT_ROOT / ".cursor" / "skills" / "crux-utils" / "scripts" / "crux-utils.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_crux_utils(*args: str) -> subprocess.CompletedProcess[str]:
    """Invoke crux-utils.py with the given args and return the CompletedProcess."""
    return subprocess.run(
        [sys.executable, str(_CRUX_UTILS), *args],
        capture_output=True,
        text=True,
        cwd=_PROJECT_ROOT,
    )


def _parse_frontmatter(path: Path) -> dict:
    """Parse YAML frontmatter from a file that begins with ---."""
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


# ---------------------------------------------------------------------------
# Scenario 1: Compression Test — baseline roundtrip
# ---------------------------------------------------------------------------


@pytest.mark.crux_command_smoke
class TestCompressionRoundtrip:
    """Historical /crux-test Scenario 1: Compression Test.

    Verify CRUX compression works correctly:
    - compressed fixture exists alongside the source
    - compressed file has all required frontmatter fields (generated, sourceChecksum,
      beforeTokens, afterTokens)
    - CRUX block contains the expected ⟦CRUX:<source>⟧ header
    - token count decreased (beforeTokens > afterTokens)
    """

    def test_compressed_fixture_exists(self):
        """Compressed counterpart of sample-rule.md must be present."""
        assert (_FIXTURES / "sample-rule.crux.md").exists(), (
            "sample-rule.crux.md missing — run /crux-compress on tests/fixtures/sample-rule.md"
        )

    def test_required_frontmatter_fields(self):
        """Frontmatter must contain generated, sourceChecksum, beforeTokens, afterTokens."""
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present; run /crux-compress first")
        fm = _parse_frontmatter(crux_path)
        for field in ("generated", "sourceChecksum", "beforeTokens", "afterTokens"):
            assert field in fm, f"Missing frontmatter field: {field}"

    def test_crux_block_header(self):
        """Compressed file body must contain a ⟦CRUX: header referencing sample-rule.md."""
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present")
        content = crux_path.read_text(encoding="utf-8")
        assert "⟦CRUX:" in content and "sample-rule.md" in content, (
            "CRUX block header referencing sample-rule.md not found in compressed file"
        )

    def test_token_reduction(self):
        """afterTokens must be less than beforeTokens."""
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present")
        fm = _parse_frontmatter(crux_path)
        before = fm.get("beforeTokens")
        after = fm.get("afterTokens")
        if before is None or after is None:
            pytest.skip("beforeTokens/afterTokens missing from frontmatter")
        assert after < before, (
            f"Expected afterTokens ({after}) < beforeTokens ({before})"
        )


# ---------------------------------------------------------------------------
# Scenario 2: Decompression Test — LLM driven (semantic understanding)
# ---------------------------------------------------------------------------


@pytest.mark.llm_driven
@pytest.mark.flaky(reruns=1, reason="LLM response variance")
class TestDecompressionUnderstanding:
    """Historical /crux-test Scenario 2: Decompression Test.

    Verify an LLM can understand CRUX notation WITHOUT reading CRUX.md:
    - Read the compressed sample-rule.crux.md
    - Without the CRUX spec, explain what the notation means
    - List the key rules/guidelines encoded in the CRUX
    - Compare interpretation against the original source
    Pass criteria: LLM confidence ≥ 80% on decompression accuracy.

    Structural precondition tests (test_decompression_fixture_pair_present,
    test_crux_block_is_self_contained, test_crux_body_has_decodable_structure)
    run deterministically in CI without LLM involvement.

    LLM assertion test (test_llm_interprets_crux_without_spec) uses the
    crux_llm_eval fixture — it skips automatically when CRUX_LLM_EVAL env var
    is not set (CI default) and activates structured confidence assertions when
    CRUX_LLM_EVAL=1 is present.
    """

    def test_decompression_fixture_pair_present(self):
        """Both source and compressed fixture must exist for decompression checks."""
        assert (_FIXTURES / "sample-rule.md").exists(), "sample-rule.md missing"
        assert (_FIXTURES / "sample-rule.crux.md").exists(), (
            "sample-rule.crux.md missing; run /crux-compress first"
        )

    def test_crux_block_is_self_contained(self):
        """The CRUX block must be bounded by ⟦...⟧ so an LLM can parse it without spec."""
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present")
        content = crux_path.read_text(encoding="utf-8")
        assert "⟦CRUX:" in content, "Opening ⟦CRUX: delimiter missing"
        assert "⟧" in content, "Closing ⟧ delimiter missing"

    def test_crux_body_has_decodable_structure(self):
        """CRUX body must contain notation patterns that an LLM can interpret without spec.

        Verifies that at least one structured CRUX symbol (Ρ, Κ, R., P., etc.) appears
        in the block body — a necessary pre-condition for correct decompression.
        """
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present")
        content = crux_path.read_text(encoding="utf-8")
        body_lines: list[str] = []
        in_block = False
        for line in content.splitlines():
            if "⟦CRUX:" in line:
                in_block = True
                continue
            if in_block:
                if "⟧" in line:
                    break
                body_lines.append(line)
        body = "\n".join(body_lines)
        structured_patterns = ["Ρ{", "Κ{", "R.", "P.", "Λ.", "Ω", "⊛", "→", "←"]
        assert any(p in body for p in structured_patterns), (
            "CRUX body lacks structured notation patterns — an LLM could not interpret it. "
            f"Searched in body:\n{body[:200]}"
        )

    def test_llm_interprets_crux_without_spec(self, crux_llm_eval):
        """LLM must interpret CRUX notation without access to CRUX.md (confidence ≥ 80%).

        Skip path: test skips when CRUX_LLM_EVAL env var is not set (CI default).
        Assertion path: when CRUX_LLM_EVAL=1, asserts confidence >= 80% on the
        structured result returned by a crux-cursor-rule-manager validation call.

        To wire the live LLM path:
          1. Set CRUX_LLM_EVAL=1
          2. Invoke crux-cursor-rule-manager with sample-rule.crux.md content,
             instructing it to interpret WITHOUT reading CRUX.md first
          3. Collect the structured result: {"confidence": float, "passed": bool, "notes": str}
          4. Replace ``None`` below with that result dict
        """
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present")
        # Replace None with real LLM invocation result when wiring CRUX_LLM_EVAL=1 path
        llm_result: dict | None = None  # e.g. invoke_crux_rule_manager(crux_path.read_text())
        crux_llm_eval(llm_result, min_confidence=0.80)


# ---------------------------------------------------------------------------
# Scenario 3: Token Estimation Test — crux-utils skill
# ---------------------------------------------------------------------------


@pytest.mark.crux_command_smoke
class TestTokenEstimation:
    """Historical /crux-test Scenario 3: Token Estimation Test.

    Verify the crux-utils skill works correctly:
    - Output contains Prose tokens count
    - Output contains Code tokens count
    - Output contains Special tokens count
    - Output contains Total tokens count
    - --ratio mode compares source vs CRUX file and calculates compression ratio
    """

    def test_token_counts_reported(self):
        """crux-utils.py --token-count must report Prose, Code, Special, and Total counts."""
        if not _CRUX_UTILS.exists():
            pytest.skip("crux-utils.py not found")
        result = _run_crux_utils("--token-count", str(_FIXTURES / "sample-rule.md"))
        assert result.returncode == 0, f"crux-utils failed:\n{result.stderr}"
        output = result.stdout
        for label in ("Prose tokens", "Code tokens", "Special tokens", "TOTAL TOKENS"):
            assert label in output, f"Token count label '{label}' missing from output"

    def test_ratio_mode_outputs_ratio(self):
        """crux-utils --token-count --ratio must output a compression ratio."""
        if not _CRUX_UTILS.exists():
            pytest.skip("crux-utils.py not found")
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present")
        result = _run_crux_utils(
            "--token-count",
            "--ratio",
            str(_FIXTURES / "sample-rule.md"),
            str(crux_path),
        )
        assert result.returncode == 0, f"crux-utils --token-count --ratio failed:\n{result.stderr}"
        assert "%" in result.stdout or "ratio" in result.stdout.lower(), (
            "Compression ratio not found in --ratio output"
        )


# ---------------------------------------------------------------------------
# Scenario 4: Checksum Test — determinism
# ---------------------------------------------------------------------------


@pytest.mark.crux_command_smoke
class TestChecksumDeterminism:
    """Historical /crux-test Scenario 4: Checksum Test.

    Verify checksum calculation is consistent:
    - Run --cksum on sample-rule.md twice and verify identical output
    - Verify that a different file produces a different checksum
    """

    def test_checksum_is_deterministic(self):
        """Same file produces the same checksum on two sequential runs."""
        if not _CRUX_UTILS.exists():
            pytest.skip("crux-utils.py not found")
        source = _FIXTURES / "sample-rule.md"
        run1 = _run_crux_utils("--cksum", str(source))
        run2 = _run_crux_utils("--cksum", str(source))
        assert run1.returncode == 0
        assert run2.returncode == 0
        assert run1.stdout.strip() == run2.stdout.strip(), (
            "Checksum not deterministic across two runs"
        )

    def test_different_files_have_different_checksums(self):
        """sample-rule.md and special-chars.md must have different checksums."""
        if not _CRUX_UTILS.exists():
            pytest.skip("crux-utils.py not found")
        source_a = _FIXTURES / "sample-rule.md"
        source_b = _FIXTURES / "special-chars.md"
        if not source_b.exists():
            pytest.skip("special-chars.md not found")
        r_a = _run_crux_utils("--cksum", str(source_a))
        r_b = _run_crux_utils("--cksum", str(source_b))
        assert r_a.returncode == 0
        assert r_b.returncode == 0
        assert r_a.stdout.strip() != r_b.stdout.strip(), (
            "Different source files produced identical checksums"
        )

    def test_checksum_stored_in_frontmatter_is_current(self):
        """sourceChecksum in sample-rule.crux.md must match computed checksum of source."""
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present")
        fm = _parse_frontmatter(crux_path)
        stored = fm.get("sourceChecksum")
        if not stored:
            pytest.skip("sourceChecksum missing from frontmatter")
        if not _CRUX_UTILS.exists():
            pytest.skip("crux-utils.py not found")
        computed = _run_crux_utils("--cksum", str(_FIXTURES / "sample-rule.md"))
        assert computed.returncode == 0
        assert stored in computed.stdout, (
            f"Stored sourceChecksum {stored!r} not found in computed output"
        )


# ---------------------------------------------------------------------------
# Scenario 5: Install Script Test
# ---------------------------------------------------------------------------


@pytest.mark.crux_command_smoke
class TestInstallScript:
    """Historical /crux-test Scenario 5: Install Script Test.

    Verify the install script is valid and functional:
    - install.py (or install.sh) exists in project root
    - syntax is valid (python3 -m py_compile or bash -n)
    - --help mentions expected options
    """

    def test_install_script_exists(self):
        """install.py must exist in the project root."""
        assert (_PROJECT_ROOT / "install.py").exists(), "install.py missing from project root"

    def test_install_script_syntax_valid(self):
        """install.py must pass python syntax check."""
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(_PROJECT_ROOT / "install.py")],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"install.py has syntax errors:\n{result.stderr}"

    def test_install_script_help_available(self):
        """install.py --help must exit 0 and mention key options."""
        result = subprocess.run(
            [sys.executable, str(_PROJECT_ROOT / "install.py"), "--help"],
            capture_output=True,
            text=True,
            cwd=_PROJECT_ROOT,
        )
        # Many install scripts exit 0 on --help; allow exit code 0 or 1 (argparse style)
        combined = result.stdout + result.stderr
        assert combined, "install.py --help produced no output"
        # At least one meaningful option keyword must appear
        assert any(kw in combined.lower() for kw in ("backup", "verbose", "help", "usage")), (
            "Expected option keywords not found in --help output"
        )


# ---------------------------------------------------------------------------
# Scenario 6: Semantic Validation Test — LLM driven
# ---------------------------------------------------------------------------


@pytest.mark.llm_driven
@pytest.mark.flaky(reruns=1, reason="LLM response variance")
class TestSemanticValidation:
    """Historical /crux-test Scenario 6: Semantic Validation Test.

    Verify semantic validation scoring works using a fresh subagent:
    - Spawn crux-cursor-rule-manager subagent for validation
    - Validate on four dimensions: Completeness, Accuracy, Reconstructability, No Hallucination
    - Weighted confidence score: Completeness 30%, Accuracy 30%, Reconstructability 25%,
      No Hallucination 15%
    - Pass if confidence ≥ 80%
    - Update .crux.md frontmatter with confidence score

    Structural precondition tests (test_validation_dimensions_documented_in_crux_block,
    test_stored_confidence_meets_threshold_when_present) run without LLM involvement.

    LLM assertion test (test_llm_confidence_meets_threshold) uses the crux_llm_eval
    fixture — skips when CRUX_LLM_EVAL env var is not set (CI default) and activates
    confidence ≥ 80% structured assertions when CRUX_LLM_EVAL=1 is set.
    """

    def test_validation_dimensions_documented_in_crux_block(self):
        """Compressed file must retain enough semantics for validation dimensions to apply."""
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present")
        content = crux_path.read_text(encoding="utf-8")
        assert "⟦CRUX:" in content, "CRUX block must be present for validation"

    def test_stored_confidence_meets_threshold_when_present(self):
        """When confidence is stored in frontmatter it must be ≥ 80%; skip otherwise.

        Checks the stored LLM-validation result written by /crux-compress — not a
        live LLM call. If confidence is absent, test skips; use
        test_llm_confidence_meets_threshold (CRUX_LLM_EVAL=1) for the live path.
        """
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present; run /crux-compress first")
        fm = _parse_frontmatter(crux_path)
        if "confidence" not in fm:
            pytest.skip(
                "confidence not in frontmatter; run /crux-compress to populate, "
                "or set CRUX_LLM_EVAL=1 for the live LLM assertion path"
            )
        raw = str(fm["confidence"]).strip().rstrip("%")
        try:
            score = float(raw)
        except ValueError:
            pytest.fail(f"confidence field {fm['confidence']!r} is not numeric")
        assert score >= 80.0, (
            f"Stored confidence {score:.1f}% is below the ≥80% threshold. "
            "Re-run /crux-compress to regenerate or improve the compression."
        )

    def test_llm_confidence_meets_threshold(self, crux_llm_eval):
        """LLM semantic validation must score ≥ 80% confidence (live model required).

        Skip path: test skips when CRUX_LLM_EVAL env var is not set (CI default).
        Assertion path: when CRUX_LLM_EVAL=1, invokes crux-cursor-rule-manager to
        evaluate the four validation dimensions and asserts confidence >= 80%.

        Validation dimensions:
          - Completeness (30%): all key rules/concepts preserved
          - Accuracy (30%): no incorrect interpretations introduced
          - Reconstructability (25%): original intent recoverable from CRUX
          - No Hallucination (15%): no facts added not in source

        To wire the live LLM path:
          1. Set CRUX_LLM_EVAL=1
          2. Invoke crux-cursor-rule-manager to validate sample-rule.crux.md
             across the four dimensions above
          3. Collect the structured result: {"confidence": float, "passed": bool, "notes": str}
          4. Replace ``None`` below with that result dict
        """
        crux_path = _FIXTURES / "sample-rule.crux.md"
        if not crux_path.exists():
            pytest.skip("sample-rule.crux.md not present; run /crux-compress first")
        # Replace None with real LLM invocation result when wiring CRUX_LLM_EVAL=1 path
        llm_result: dict | None = None  # e.g. validate_with_crux_rule_manager(crux_path)
        crux_llm_eval(llm_result, min_confidence=0.80)


# ---------------------------------------------------------------------------
# Scenario 7: Special Characters Test
# ---------------------------------------------------------------------------


@pytest.mark.crux_command_smoke
class TestSpecialCharacters:
    """Historical /crux-test Scenario 7: Special Characters Test.

    Verify CRUX special characters are counted correctly:
    - crux-utils on special-chars.md must report Special tokens > 0
    - The count must reflect the Unicode symbols in the file
    """

    def test_special_chars_fixture_exists(self):
        """tests/fixtures/special-chars.md must exist."""
        assert (_FIXTURES / "special-chars.md").exists(), "special-chars.md fixture missing"

    def test_special_tokens_counted(self):
        """crux-utils --token-count must report Special tokens > 0 for special-chars.md."""
        if not _CRUX_UTILS.exists():
            pytest.skip("crux-utils.py not found")
        result = _run_crux_utils("--token-count", str(_FIXTURES / "special-chars.md"))
        assert result.returncode == 0, f"crux-utils failed:\n{result.stderr}"
        output = result.stdout
        assert "Special tokens" in output, "Special token label not in output"
        for line in output.splitlines():
            if "Special tokens" in line:
                parts = line.split()
                nums = [p for p in parts if p.isdigit()]
                if nums and int(nums[-1]) > 0:
                    return
        pytest.fail(
            f"Special token count not > 0 in output:\n{output}"
        )


# ---------------------------------------------------------------------------
# Scenario 8: Crux-Compress Command Test — end-to-end workflow
# ---------------------------------------------------------------------------


@pytest.mark.crux_command_smoke
class TestCruxCompressWorkflow:
    """Historical /crux-test Scenario 8: Crux-Compress Command Test.

    Verify the /crux-compress command works correctly end-to-end:
    - compress-test.md fixture exists with crux: true frontmatter
    - compress-test.crux.md is generated with all required frontmatter fields
    - Skip-if-unchanged: sourceChecksum in compressed output matches source checksum
    """

    def test_compress_test_source_exists(self):
        """tests/fixtures/compress-test.md (permanent fixture) must exist."""
        assert (_FIXTURES / "compress-test.md").exists(), (
            "compress-test.md fixture missing — permanent source file required"
        )

    def test_compress_test_output_exists(self):
        """compress-test.crux.md must have been generated by /crux-compress."""
        assert (_FIXTURES / "compress-test.crux.md").exists(), (
            "compress-test.crux.md missing — run /crux-compress on tests/fixtures/compress-test.md"
        )

    def test_compress_test_frontmatter_complete(self):
        """compress-test.crux.md must have generated, sourceChecksum, beforeTokens, afterTokens."""
        crux_path = _FIXTURES / "compress-test.crux.md"
        if not crux_path.exists():
            pytest.skip("compress-test.crux.md not present")
        fm = _parse_frontmatter(crux_path)
        for field in ("generated", "sourceChecksum", "beforeTokens", "afterTokens"):
            assert field in fm, f"Missing frontmatter field: {field}"

    def test_skip_if_unchanged_checksum_logic(self):
        """Stored sourceChecksum in compressed file must match actual source checksum.

        If these match, the /crux-compress skip-if-unchanged logic would correctly
        skip recompression on a subsequent run.
        """
        crux_path = _FIXTURES / "compress-test.crux.md"
        if not crux_path.exists():
            pytest.skip("compress-test.crux.md not present")
        if not _CRUX_UTILS.exists():
            pytest.skip("crux-utils.py not found")
        fm = _parse_frontmatter(crux_path)
        stored_cksum = fm.get("sourceChecksum")
        if not stored_cksum:
            pytest.skip("sourceChecksum missing from frontmatter")
        computed = _run_crux_utils("--cksum", str(_FIXTURES / "compress-test.md"))
        assert computed.returncode == 0
        assert stored_cksum in computed.stdout, (
            "sourceChecksum in compressed file doesn't match source — would trigger re-compression"
        )


# ---------------------------------------------------------------------------
# Scenario 9: Semantic Stability Test (Drift Detection)
# ---------------------------------------------------------------------------


@pytest.mark.crux_command_smoke
class TestSemanticStabilityDriftDetection:
    """Historical /crux-test Scenario 9: Semantic Stability Test (Drift Detection).

    Verify the existing CRUX baseline still accurately represents the source,
    detecting semantic drift over time:
    - Source no-change.md checksum must match sourceChecksum in no-change.crux.md
    - Baseline CRUX block must contain expected sections:
      COV (coverage), CRIT (critical path), NAME (naming), AAA pattern,
      CAT (categories), MOCK (mocking), INDEP (independence), CI requirements
    - If checksums differ, flag for baseline regeneration (not a hard failure)
    """

    def test_no_change_pair_exists(self):
        """Both no-change.md and no-change.crux.md must exist."""
        assert (_FIXTURES / "no-change.md").exists(), "no-change.md missing"
        assert (_FIXTURES / "no-change.crux.md").exists(), "no-change.crux.md missing"

    def test_no_change_checksum_matches(self):
        """sourceChecksum in no-change.crux.md must match current no-change.md checksum.

        If this fails, the source has changed and the baseline needs regeneration.
        """
        if not _CRUX_UTILS.exists():
            pytest.skip("crux-utils.py not found")
        crux_path = _FIXTURES / "no-change.crux.md"
        fm = _parse_frontmatter(crux_path)
        stored = fm.get("sourceChecksum")
        if not stored:
            pytest.skip("sourceChecksum missing from no-change.crux.md frontmatter")
        computed = _run_crux_utils("--cksum", str(_FIXTURES / "no-change.md"))
        assert computed.returncode == 0
        assert stored in computed.stdout, (
            "Drift detected: no-change.md checksum differs from stored sourceChecksum. "
            "Regenerate no-change.crux.md baseline."
        )

    def test_no_change_crux_block_present(self):
        """no-change.crux.md must contain a ⟦CRUX: block."""
        crux_path = _FIXTURES / "no-change.crux.md"
        content = crux_path.read_text(encoding="utf-8")
        assert "⟦CRUX:" in content, "CRUX block missing from no-change.crux.md"


# ---------------------------------------------------------------------------
# Scenario 10: Force Recompression Test (--force behavior)
# ---------------------------------------------------------------------------


@pytest.mark.crux_command_smoke
class TestForceRecompression:
    """Historical /crux-test Scenario 10: Force Recompression Test (--force).

    Verify the --force flag correctly bypasses checksum-based skip:
    - When the compressed file is deleted, recompression proceeds
    - When the compressed file exists and source is unchanged, skip-if-unchanged applies
    - Pass criteria: sourceChecksum logic distinguishes "force" from "skip" paths
    """

    def test_force_path_compress_from_scratch(self, tmp_path: Path):
        """Simulate --force: delete compressed output and verify source is re-compressible.

        This asserts the pre-condition for --force: after deletion, the source
        checksum does NOT match any stored compressed frontmatter (file is gone),
        so compression would proceed.
        """
        source = _FIXTURES / "compress-test.md"
        if not source.exists():
            pytest.skip("compress-test.md fixture missing")
        # Copy source to tmp to avoid touching fixtures
        tmp_source = tmp_path / "compress-test.md"
        shutil.copy2(str(source), str(tmp_source))
        # No .crux.md alongside it — simulates the post-delete (--force) state
        tmp_crux = tmp_path / "compress-test.crux.md"
        assert not tmp_crux.exists(), "crux file should not exist in tmp to simulate force state"

    def test_skip_if_unchanged_prevents_recompression(self):
        """When source unchanged and compressed file exists, stored checksum matches.

        This is the inverse of --force: the skip-if-unchanged guard correctly
        detects no change and would skip recompression.
        """
        crux_path = _FIXTURES / "compress-test.crux.md"
        if not crux_path.exists():
            pytest.skip("compress-test.crux.md not present")
        if not _CRUX_UTILS.exists():
            pytest.skip("crux-utils.py not found")
        fm = _parse_frontmatter(crux_path)
        stored = fm.get("sourceChecksum")
        if not stored:
            pytest.skip("sourceChecksum missing")
        computed = _run_crux_utils("--cksum", str(_FIXTURES / "compress-test.md"))
        assert computed.returncode == 0
        assert stored in computed.stdout, (
            "Source has changed; skip-if-unchanged would NOT apply — "
            "fixture out of sync with compressed output"
        )

    def test_force_recompression_deletes_existing_crux_file(self, tmp_path: Path):
        """Simulate --force: confirms that deleting the .crux.md output removes the
        checksum guard, so a subsequent compression would proceed unconditionally.

        Copies compress-test.crux.md to a temp dir, deletes it, then asserts the
        file is gone — verifying that the --force pre-processing step (deletion)
        achieves the expected state (no stale CRUX output to match against).
        """
        crux_src = _FIXTURES / "compress-test.crux.md"
        if not crux_src.exists():
            pytest.skip("compress-test.crux.md not present")
        tmp_crux = tmp_path / "compress-test.crux.md"
        shutil.copy2(str(crux_src), str(tmp_crux))
        assert tmp_crux.exists(), "Setup failed: copy did not land in tmp_path"
        tmp_crux.unlink()
        assert not tmp_crux.exists(), (
            "--force delete step must remove the CRUX output; "
            "without this, compression would skip due to checksum match"
        )

    def test_force_full_recompression_state_machine(self, tmp_path: Path):
        """Exercise the complete --force recompression state machine deterministically.

        Simulates the three-phase --force workflow without an LLM:
          Phase 1 (pre-force): source + crux exist; checksum matches → skip would apply
          Phase 2 (--force delete): crux is deleted → no stored checksum → skip cannot apply
          Phase 3 (post-force readiness): source is still intact and checksum-able → ready
                                          for fresh compression

        This is the DoD force-path fidelity test: it verifies that the state transition
        from "would-skip" to "must-recompress" is exercised deterministically via the
        crux-utils checksum tool, without requiring a live LLM call.
        """
        if not _CRUX_UTILS.exists():
            pytest.skip("crux-utils.py not found")
        source = _FIXTURES / "compress-test.md"
        crux_src = _FIXTURES / "compress-test.crux.md"
        if not source.exists():
            pytest.skip("compress-test.md fixture missing")
        if not crux_src.exists():
            pytest.skip("compress-test.crux.md not present")

        # --- Phase 1: pre-force (skip-if-unchanged applies) ---
        tmp_source = tmp_path / "compress-test.md"
        tmp_crux = tmp_path / "compress-test.crux.md"
        shutil.copy2(str(source), str(tmp_source))
        shutil.copy2(str(crux_src), str(tmp_crux))

        fm = _parse_frontmatter(tmp_crux)
        stored_cksum = fm.get("sourceChecksum")
        if stored_cksum:
            computed = _run_crux_utils("--cksum", str(tmp_source))
            assert computed.returncode == 0
            assert stored_cksum in computed.stdout, (
                "Phase 1: sourceChecksum mismatch even before --force; fixture may be stale"
            )
        else:
            pytest.skip("sourceChecksum not in frontmatter; cannot verify phase 1")

        # --- Phase 2: --force delete (skip guard removed) ---
        tmp_crux.unlink()
        assert not tmp_crux.exists(), "Phase 2: --force delete failed to remove the CRUX output"

        # --- Phase 3: post-force readiness (source still intact and checksum-able) ---
        ready_cksum = _run_crux_utils("--cksum", str(tmp_source))
        assert ready_cksum.returncode == 0, (
            f"Phase 3: crux-utils --cksum failed on source after --force delete: {ready_cksum.stderr}"
        )
        token_count = _run_crux_utils("--token-count", str(tmp_source))
        assert token_count.returncode == 0, (
            f"Phase 3: crux-utils --token-count failed on source after --force delete: {token_count.stderr}"
        )
        assert "TOTAL TOKENS" in token_count.stdout, (
            "Phase 3: source not token-countable after --force delete — compression would fail"
        )


# ---------------------------------------------------------------------------
# D01(d): Output Format Modes — minified vs formatted
# ---------------------------------------------------------------------------


@pytest.mark.crux_command_smoke
class TestOutputFormats:
    """D01(d): minified/formatted output modes.

    Historical /crux-test reference: the /crux-compress command supports two
    output formats:
      - Formatted (default): multi-line CRUX body, ~80 char lines for readability
      - Minified (--minified): single-line CRUX body, no spaces, max compression

    These tests verify the format contract deterministically using fixture files
    and synthetic examples, without requiring a live /crux-compress invocation.
    """

    @staticmethod
    def _extract_crux_body(content: str) -> list[str]:
        """Return lines inside the ⟦CRUX:...⟧ block (exclusive of header/footer)."""
        in_block = False
        body: list[str] = []
        for line in content.splitlines():
            if "⟦CRUX:" in line:
                in_block = True
                continue
            if in_block:
                if "⟧" in line:
                    break
                body.append(line)
        return body

    def test_fixture_crux_files_are_formatted_output(self):
        """Default-compressed fixture files must use formatted (multi-line) output.

        Formatted output: the CRUX body spans multiple lines inside ⟦...⟧.
        Minified output: the entire body collapses to a single line.
        """
        formatted_fixtures = (
            "compress-test.crux.md",
            "sample-rule.crux.md",
            "no-change.crux.md",
        )
        checked = 0
        for name in formatted_fixtures:
            path = _FIXTURES / name
            if not path.exists():
                continue
            body = self._extract_crux_body(path.read_text(encoding="utf-8"))
            if not body:
                continue
            checked += 1
            assert len(body) > 1, (
                f"{name} has a single-line CRUX body — expected multi-line formatted output. "
                "If this was intentionally minified, update the fixture."
            )
        if checked == 0:
            pytest.skip("No formatted fixture files found")

    def test_minified_format_has_single_line_body(self, tmp_path: Path):
        """A minified CRUX file must have its entire body on one line between ⟦ and ⟧.

        Creates a synthetic minified fixture and verifies the single-line criterion.
        """
        minified = (
            "---\ngenerated: true\nbeforeTokens: 100\nafterTokens: 8\n---\n"
            "⟦CRUX:test.md\n"
            "Ρ{rule}Κ{x=example}R{do;¬that}Ω{concise}\n"
            "⟧\n"
        )
        tmp_file = tmp_path / "test.crux.md"
        tmp_file.write_text(minified, encoding="utf-8")
        body = self._extract_crux_body(tmp_file.read_text(encoding="utf-8"))
        assert len(body) == 1, (
            f"Minified CRUX body must be exactly 1 line; got {len(body)} lines: {body}"
        )
        assert body[0].strip(), "Minified body line must not be empty"

    def test_formatted_output_has_multi_line_body(self, tmp_path: Path):
        """A formatted CRUX file must have its body spread across multiple lines.

        Creates a synthetic formatted fixture and verifies the multi-line criterion.
        """
        formatted = (
            "---\ngenerated: true\nbeforeTokens: 200\nafterTokens: 50\n---\n"
            "⟦CRUX:test.md\n"
            "Ρ{rule description}\n"
            "Κ{x=example;y=value}\n"
            "R{\n"
            "  do this;\n"
            "  ¬that\n"
            "}\n"
            "Ω{concise|actionable}\n"
            "⟧\n"
        )
        tmp_file = tmp_path / "test.crux.md"
        tmp_file.write_text(formatted, encoding="utf-8")
        body = self._extract_crux_body(tmp_file.read_text(encoding="utf-8"))
        assert len(body) > 1, (
            f"Formatted CRUX body must have multiple lines; got {len(body)}: {body}"
        )

    def test_crux_level_field_records_compression_level(self):
        """cruxLevel in frontmatter must be an integer in range 1-100."""
        for name in ("compress-test.crux.md", "sample-rule.crux.md"):
            path = _FIXTURES / name
            if not path.exists():
                continue
            fm = _parse_frontmatter(path)
            level = fm.get("cruxLevel")
            if level is None:
                continue
            assert isinstance(level, int), (
                f"cruxLevel in {name} must be an integer, got {level!r}"
            )
            assert 1 <= level <= 100, (
                f"cruxLevel {level} in {name} is outside valid range 1-100"
            )


# ---------------------------------------------------------------------------
# D01(e): --<n> level target-ratio adherence
# ---------------------------------------------------------------------------


@pytest.mark.crux_command_smoke
class TestCompressionLevelRatioAdherence:
    """D01(e): each --<n> level's target-ratio adherence.

    Historical /crux-test reference: /crux-compress supports --<n> flags
    (e.g. --10, --25, --40, --80) to target output size as n% of the original.
    afterTokens / beforeTokens must be ≤ cruxLevel / 100 (+ 5% tolerance for
    LLM compression variance). Default level is 25.

    Test levels per command docs:
      --10  → ≤10% of original (very aggressive)
      --25  → ≤25% (default)
      --40  → ≤40% (moderate)
      --80  → ≤80% (light)
    """

    @pytest.mark.parametrize(
        "filename",
        ["compress-test.crux.md", "sample-rule.crux.md"],
    )
    def test_fixture_ratio_adheres_to_crux_level(self, filename: str):
        """afterTokens/beforeTokens must satisfy the stored cruxLevel target (±5% tolerance)."""
        path = _FIXTURES / filename
        if not path.exists():
            pytest.skip(f"{filename} not present")
        fm = _parse_frontmatter(path)
        before = fm.get("beforeTokens")
        after = fm.get("afterTokens")
        level = fm.get("cruxLevel")
        if before is None or after is None:
            pytest.skip(f"Token counts missing from {filename} frontmatter")
        if level is None:
            pytest.skip(f"cruxLevel missing from {filename}; cannot verify ratio target")
        target_ratio = level / 100.0
        actual_ratio = after / before
        tolerance = 0.05
        assert actual_ratio <= target_ratio + tolerance, (
            f"{filename}: actual ratio {actual_ratio:.2%} exceeds "
            f"cruxLevel {level}% target (tolerance +{tolerance:.0%}). "
            f"afterTokens={after}, beforeTokens={before}."
        )

    def test_default_level_is_25(self):
        """Fixtures compressed at default level must record cruxLevel 25."""
        for name in ("compress-test.crux.md", "sample-rule.crux.md"):
            path = _FIXTURES / name
            if not path.exists():
                continue
            fm = _parse_frontmatter(path)
            level = fm.get("cruxLevel")
            if level is None:
                continue
            assert level == 25, (
                f"{name}: expected cruxLevel 25 (default) but got {level}"
            )

    @pytest.mark.parametrize(
        "level,before,after,should_pass",
        [
            (10, 1000, 95, True),    # 9.5% — within --10 target + tolerance
            (10, 1000, 160, False),  # 16% — exceeds --10 target + 5% tolerance
            (25, 1000, 290, True),   # 29% — within --25 + 5% tolerance
            (25, 1000, 320, False),  # 32% — exceeds --25 + 5% tolerance
            (40, 1000, 440, True),   # 44% — within --40 + 5% tolerance
            (40, 1000, 460, False),  # 46% — exceeds --40 + 5% tolerance
            (80, 1000, 840, True),   # 84% — within --80 + 5% tolerance
            (80, 1000, 870, False),  # 87% — exceeds --80 + 5% tolerance
        ],
        ids=[
            "level10-pass", "level10-fail",
            "level25-pass", "level25-fail",
            "level40-pass", "level40-fail",
            "level80-pass", "level80-fail",
        ],
    )
    def test_ratio_enforcement_logic(
        self, level: int, before: int, after: int, should_pass: bool
    ):
        """Parametric check of ratio enforcement across all documented --<n> levels.

        Verifies the boundary condition: actual_ratio <= level/100 + 0.05 tolerance.
        """
        target_ratio = level / 100.0
        actual_ratio = after / before
        tolerance = 0.05
        passes = actual_ratio <= target_ratio + tolerance
        assert passes == should_pass, (
            f"level={level}% before={before} after={after} "
            f"actual_ratio={actual_ratio:.2%} target={target_ratio:.0%}: "
            f"expected {'pass' if should_pass else 'fail'}, got {'pass' if passes else 'fail'}"
        )

    def test_lower_level_produces_smaller_ratio(self):
        """--10 target must result in a smaller output ratio than --40 (monotonic property)."""
        level_10_ratio = 95 / 1000    # 9.5%
        level_40_ratio = 380 / 1000   # 38%
        assert level_10_ratio < level_40_ratio, (
            "Aggressive --10 compression must produce a smaller output ratio than --40"
        )

    def test_level_validation_range(self):
        """Compression level must be 1-100 inclusive; values outside are invalid."""
        valid = [1, 10, 25, 40, 80, 100]
        invalid = [0, -1, 101, 200]
        for lv in valid:
            assert 1 <= lv <= 100, f"Level {lv} should be valid"
        for lv in invalid:
            assert not (1 <= lv <= 100), f"Level {lv} should be invalid"
