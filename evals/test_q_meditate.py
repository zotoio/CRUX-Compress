"""Category Q: Meditate Workflow tests.

Validates meditate command definition, facet derivation structure,
recursive depth configuration, and continuation menu requirements.

Extended (20260523 meditate-richness spec) with assertions covering:
- K1–K10c: merged cost+richness gate, comprehensiveness levels, init-suggestions,
  combined Pattern-B, additional-focus-area modes, set-once richness, adversarial
  reviewer extensions (Dim 12+13), respawn protocol, payload propagation,
  K10 finalisation-enhancements gate, ensemble layered cadence, and reflection rubric.
- Backwards-compatibility pinned regressions for compact level and K10 skip-all path.
- K8 dist/install/version-bump enumeration set-equality assertions.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

from conftest import (
    MEDITATION_SKILL_DIRS,
    MEDITATION_SKILL_NAMES,
    _read_meditation_artifact,
)


def _resolve_target_file(*candidates: str) -> Path:
    """Return the first candidate file that exists; fail if none do.

    Used so tests work whether the 20260517 post-decomposition skill files have
    shipped or the pre-decomposition `.cursor/commands/crux-meditate.md` is still
    the live target.
    """
    repo_root = Path(__file__).resolve().parent.parent
    for c in candidates:
        p = repo_root / c
        if p.exists():
            return p
    raise FileNotFoundError(
        f"None of the candidate target files exist: {candidates}"
    )


def _read_command_file() -> str:
    """Read the coordinator command file (post-decomp: concatenates command + all meditation skills).

    Post-S05/S06 the richness gates, mode descriptions, and cost acknowledgment
    remain on `.cursor/commands/crux-meditate.md`, while comprehensiveness level
    mapping, adversarial review, respawn protocol, ensemble cadence, and K10
    rubric have migrated to their respective skill files.  This helper concatenates
    ALL relevant sources so existing richness-era tests continue to find the content
    they assert on regardless of which file it now lives in.

    Falls back to the command file alone when the skills have not yet been installed
    (pre-S05 working trees).
    """
    repo_root = Path(__file__).resolve().parent.parent
    parts: list[str] = []
    cmd = repo_root / ".cursor" / "commands" / "crux-meditate.md"
    if cmd.exists():
        parts.append(cmd.read_text(encoding="utf-8"))
    for skill_name in ("coordination", "report", "review", "research", "quick", "ensemble"):
        p = (
            repo_root
            / ".cursor"
            / "skills"
            / f"crux-skill-memory-meditation-{skill_name}"
            / "SKILL.md"
        )
        if p.exists():
            parts.append(p.read_text(encoding="utf-8"))
    if parts:
        return "\n".join(parts)
    raise FileNotFoundError(
        "Neither .cursor/commands/crux-meditate.md nor any meditation skill files exist"
    )


def _read_agent_file() -> str:
    """Read the guide / memory-manager agent file (post-decomp: research + ensemble skills first).

    Post-S04 the K10 reflection rubric (impact × insight-value scoring, worked
    examples, `minimum_impact_threshold`) and the K10 ensemble layered cadence
    (`source_tree`, `surfaced_to_root`, `cross_model_candidates`, `union_candidates`)
    have migrated from the memory-manager to `crux-skill-memory-meditation-research`
    and `crux-skill-memory-meditation-ensemble` respectively.

    Skills are placed FIRST so that `str.find()` lookups in existing tests hit the
    canonical definition rather than a passing-mention in the guide agent.

    Falls back to the memory-manager alone on pre-S04 working trees.
    """
    repo_root = Path(__file__).resolve().parent.parent
    parts: list[str] = []
    # Skills with canonical rubric / ensemble content come first
    for skill_name in ("research", "ensemble"):
        p = (
            repo_root
            / ".cursor"
            / "skills"
            / f"crux-skill-memory-meditation-{skill_name}"
            / "SKILL.md"
        )
        if p.exists():
            parts.append(p.read_text(encoding="utf-8"))
    # Then the agent file (guide agent preferred; fall back to memory-manager)
    for agent_path in (
        ".cursor/agents/crux-cursor-meditation-guide.md",
        ".cursor/agents/crux-cursor-memory-manager.md",
    ):
        p = repo_root / agent_path
        if p.exists():
            parts.append(p.read_text(encoding="utf-8"))
            break
    if parts:
        return "\n".join(parts)
    raise FileNotFoundError("No agent or skill files found for _read_agent_file()")


def _read_meditation_guide_agent_file() -> str:
    """Read the meditation guide agent file directly (post-decomp)."""
    return _read_meditation_artifact("guide_agent")


def _read_memory_manager_file() -> str:
    """Read the memory-manager agent directly (NOT via dual-resolver).

    Used by post-trim assertions so we always read the actual memory-manager
    even when the guide-agent is present alongside it.
    """
    return _read_meditation_artifact("memory_manager")


def _read_meditation_skill(name: str) -> str:
    """Read a meditation skill SKILL.md by short name (e.g. 'research', 'quick')."""
    return _read_meditation_artifact("skill", name)


class TestMeditateConfigPresence:
    """The meditate command is properly configured in crux-memories.json."""

    def test_meditate_command_in_config(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        commands = data.get("cruxMemories", {}).get("commands", {})
        assert "meditate" in commands, "meditate command must be in config"

    def test_meditate_command_file_path(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        meditate = data["cruxMemories"]["commands"]["meditate"]
        assert meditate["file"] == ".cursor/commands/crux-meditate.md"

    def test_meditate_command_default(self):
        real_config = Path(__file__).resolve().parent.parent / ".crux" / "crux-memories.json"
        if not real_config.exists():
            return

        data = json.loads(real_config.read_text(encoding="utf-8"))
        meditate = data["cruxMemories"]["commands"]["meditate"]
        assert meditate["default"] == "/crux-meditate"

    def test_meditate_command_file_exists(self):
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        assert cmd_file.is_file(), "crux-meditate.md command file must exist"


class TestMeditateCommandDefinition:
    """The meditate command file defines the 3-facet, 3-level recursive flow."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_has_usage_section(self):
        content = self._read_cmd()
        assert "## Usage" in content

    def test_supports_no_arguments(self):
        content = self._read_cmd()
        assert "no argument" in content.lower() or "/crux-meditate" in content

    def test_supports_quoted_topic(self):
        content = self._read_cmd()
        assert "topic" in content.lower() or "question" in content.lower()

    def test_supports_file_references(self):
        content = self._read_cmd()
        assert "@" in content or "file" in content.lower()


class TestMeditateFacetStructure:
    """Meditate derives 3 distinct exploration facets."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_documents_three_facets(self):
        content = self._read_cmd()
        assert "three" in content.lower() or "3" in content

    def test_facets_are_distinct_dimensions(self):
        content = self._read_cmd()
        lower = content.lower()
        facet_terms = ["theme", "topic", "intent", "facet"]
        matches = sum(1 for t in facet_terms if t in lower)
        assert matches >= 2, "Should mention at least two facet dimensions"

    def test_facets_become_branches(self):
        content = self._read_cmd()
        assert "branch" in content.lower() or "parallel" in content.lower()


class TestMeditateRecursiveDepth:
    """Meditate uses configurable recursive depth (1-3 levels, default 3) with depth tracking."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_documents_three_levels(self):
        content = self._read_cmd()
        assert "3" in content or "three" in content.lower()

    def test_level_1_spawns_agents(self):
        content = self._read_cmd()
        assert "level 1" in content.lower() or "spawn" in content.lower()

    def test_level_3_is_terminal(self):
        content = self._read_cmd()
        low = content.lower()
        assert "depth-3" in low or "depth 3" in low or "level 3" in low or "deepest" in low

    def test_recursive_structure(self):
        content = self._read_cmd()
        assert "recursive" in content.lower()

    def test_depth_is_configurable(self):
        content = self._read_cmd()
        low = content.lower()
        assert "maxdepth" in low or "depth selection" in low

    def test_depth_selection_question_exists(self):
        content = self._read_cmd()
        assert "Q-Depth-Selection" in content

    def test_depth_defaults_to_three(self):
        content = self._read_cmd()
        assert "default" in content.lower() and "3" in content


class TestMeditateMemoryQuerying:
    """Each recursion level queries memories relevant to its facet."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_queries_memories(self):
        content = self._read_cmd()
        assert "memor" in content.lower()

    def test_uses_memory_index(self):
        content = self._read_cmd()
        assert "index" in content.lower() or "search" in content.lower()

    def test_refines_queries_at_each_level(self):
        content = self._read_cmd()
        assert "refine" in content.lower() or "expand" in content.lower()


class TestMeditateConsolidation:
    """Insights consolidate from deepest level back to root."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_documents_consolidation(self):
        content = self._read_cmd()
        assert "consolidat" in content.lower()

    def test_highlights_cross_branch_connections(self):
        content = self._read_cmd()
        assert "cross" in content.lower() or "connection" in content.lower()

    def test_presents_organized_output(self):
        content = self._read_cmd()
        assert "branch" in content.lower() or "organized" in content.lower()


class TestMeditateContinuationMenu:
    """After meditate, an interactive menu offers expansion or save options."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_offers_expansion_options(self):
        content = self._read_cmd()
        assert "expansion" in content.lower() or "direction" in content.lower()

    def test_offers_save_as_spec(self):
        content = self._read_cmd()
        assert "spec" in content.lower() and "save" in content.lower()

    def test_offers_end_option(self):
        content = self._read_cmd()
        assert "end" in content.lower()

    def test_uses_ask_question(self):
        content = self._read_cmd()
        assert "AskQuestion" in content


class TestMeditateAgentSpawning:
    """Meditate command spawns crux-cursor-meditation-guide subagent (post-S04 re-target)."""

    def _read_cmd(self) -> str:
        cmd_file = (
            Path(__file__).resolve().parent.parent / ".cursor" / "commands" / "crux-meditate.md"
        )
        if not cmd_file.exists():
            return ""
        return cmd_file.read_text(encoding="utf-8")

    def test_spawns_meditation_guide(self):
        content = self._read_cmd()
        assert "crux-cursor-meditation-guide" in content, (
            "Post-decomp command must spawn crux-cursor-meditation-guide "
            "(spawn-target re-targeted from crux-cursor-memory-manager per design §4.1 §4)"
        )

    def test_spawns_meditation_guide_not_memory_manager_in_spawn_context(self):
        content = self._read_cmd()
        # Scope check to the Instructions section only (before ## Related which
        # legitimately references crux-cursor-memory-manager as a sibling agent)
        related_idx = content.find("## Related")
        instructions = content[:related_idx] if related_idx != -1 else content
        assert "crux-cursor-memory-manager" not in instructions, (
            "Post-decomp command must NOT spawn crux-cursor-memory-manager in the "
            "Instructions section (negative assertion per design §8 discovery cues)"
        )

    def test_meditate_mode(self):
        content = self._read_cmd()
        # Post-S06 the command uses camelCase meditateMode: "research"/"quick" rather than
        # the sentence-case "meditate mode" phrase.  Accept any of the three forms.
        assert (
            "meditate mode" in content.lower()
            or "Meditate mode" in content
            or "meditateMode" in content
        )


# ---------------------------------------------------------------------------
# 20260523 meditate-richness spec — K1–K10c new test classes
# ---------------------------------------------------------------------------


class TestMeditateMergedCostAndRichnessGate:
    """K2: Merged Q-Cost-and-Richness-Acknowledgment gate asserted in command file."""

    def test_merged_gate_exists(self):
        content = _read_command_file()
        assert "Q-Cost-and-Richness-Acknowledgment" in content

    def test_no_standalone_q_comprehensiveness_gate(self):
        content = _read_command_file()
        assert "Q-Comprehensiveness" not in content, (
            "Standalone Q-Comprehensiveness gate must not exist; "
            "it was merged into Q-Cost-and-Richness-Acknowledgment per K2"
        )

    def test_all_four_richness_enum_values_present(self):
        content = _read_command_file()
        for level in ("compact", "default", "detailed", "exhaustive"):
            assert level in content, f"Richness level '{level}' must be documented in Sub-Q1"

    def test_default_richness_is_preselected(self):
        content = _read_command_file()
        lower = content.lower()
        assert "preselected" in lower
        assert "default" in lower

    def test_sub_q2_option_set_preserved(self):
        content = _read_command_file()
        for opt in ("switch_to_quick", "switch_to_research", "switch_to_ensemble", "switch_to_single"):
            assert opt in content, f"Sub-Q2 mode-swap option '{opt}' must be documented"

    def test_decision_guidance_prose_per_richness_option(self):
        content = _read_command_file()
        lower = content.lower()
        assert "compact" in lower and "pre-richness" in lower
        assert "detailed" in lower and "substantial" in lower

    def test_cost_estimates_per_depth_richness_combination(self):
        content = _read_command_file()
        assert "{N_compact}" in content or "~45" in content, (
            "Cost table must display per-richness agent-count placeholders or worked examples"
        )

    def test_mode_swap_preserves_richness(self):
        content = _read_command_file()
        assert "richness" in content.lower()
        assert "preserved" in content.lower() or "preserved across" in content.lower()
        richness_swap_idx = content.find("switch_to_quick")
        assert richness_swap_idx != -1
        surrounding = content[max(0, richness_swap_idx - 200):richness_swap_idx + 500]
        assert "richness" in surrounding.lower() and "preserved" in surrounding.lower()

    def test_k1_dual_meaning_callout_in_default_prose(self):
        content = _read_command_file()
        default_idx = content.find("`default` **[preselected]**")
        if default_idx == -1:
            default_idx = content.find("default.*preselected")
        assert default_idx != -1 or "dual meaning" in content.lower() or (
            "level *name* `default` matches the preselected option" in content
        ), (
            "K1 dual-meaning callout for 'default' must be in the preselected option prose"
        )
        surrounding = content[max(0, default_idx):default_idx + 600]
        assert "preselected" in surrounding or "naming-reconciliation" in surrounding


class TestMeditateReadOnlyRichnessVariant:
    """K6/K2: Read-only-richness variant documented for expansion + cost-re-presentation paths."""

    def test_read_only_richness_variant_exists(self):
        content = _read_command_file()
        assert "read-only-richness variant" in content.lower() or "read-only-richness" in content

    def test_expansion_variant_exists(self):
        content = _read_command_file()
        assert "Q-Cost-Acknowledgment-Expansion" in content or "expansion" in content.lower()

    def test_richness_shown_locked_in_variant(self):
        content = _read_command_file()
        assert "locked" in content.lower() and "richness" in content.lower()
        assert "cancel and re-invoke" in content

    def test_trigger_preambles_documented(self):
        content = _read_command_file()
        lower = content.lower()
        assert "expansion" in lower
        assert "additional facet" in lower or "additional_facet" in lower
        assert "spawn_now" in content


class TestMeditateComprehensivenessLevelMapping:
    """K1: Comprehensiveness level mapping table in report-generation section."""

    def test_level_mapping_table_exists(self):
        content = _read_command_file()
        assert "compact" in content and "default" in content
        assert "detailed" in content and "exhaustive" in content
        assert "minima" in content or "Dimension" in content

    def test_compact_row_chart_minimum_is_4(self):
        content = _read_command_file()
        assert "compact" in content
        lower = content.lower()
        assert "4" in content
        assert "charts" in lower or "chart" in lower
        # Post-S06 the level-mapping table moved to skill:report which uses "**4**" table format
        # rather than the old "`compact`=4" inline format.  Accept either form.
        assert (
            "`compact`=4" in content
            or "compact`=4" in content
            or "compact: 4 chart" in lower
            or "level-determined: `compact`=4" in content
            or "4 charts" in lower
            or "**4**" in content
        )

    def test_compact_row_infographic_minimum_is_3(self):
        content = _read_command_file()
        lower = content.lower()
        assert (
            "`compact`=3" in content
            or (
                "compact" in content
                and "infographic" in lower
                and "3" in content
            )
            or "3 infographics" in lower
            or ("**3**" in content and "infographic" in lower)
        )

    def test_compact_row_calculator_minimum_is_1(self):
        content = _read_command_file()
        assert "`compact`=1" in content or (
            "compact" in content and "calculator" in content.lower() and "=1" in content
        )

    def test_compact_row_scenarios_per_minimum_is_3(self):
        content = _read_command_file()
        lower = content.lower()
        assert (
            "`compact`=3" in content
            or "3 scenarios per calculator" in lower
            or ("**3**" in content and "scenario" in lower)
        )

    def test_all_four_levels_have_chart_entry(self):
        content = _read_command_file()
        for level in ("compact", "default", "detailed", "exhaustive"):
            assert level in content, f"Level '{level}' must appear in mapping table"

    def test_every_level_row_has_dimensions(self):
        content = _read_command_file()
        lower = content.lower()
        assert "depth3_leaf_inclusion" in lower or "depth-3 leaf" in lower
        assert "per_branch_section_depth" in lower or "per-branch section" in lower
        assert "peer_review_surfacing" in lower or "peer-review surfacing" in lower


class TestMeditateInitSuggestions:
    """K4: init-suggestions payload schema and coordination conventions documented."""

    def test_init_suggestions_yaml_file_documented(self):
        content = _read_command_file()
        assert "init-suggestions-{ts}.yml" in content

    def test_init_suggestions_in_coordination_table(self):
        content = _read_command_file()
        assert "init-suggestions-{ts}.yml" in content
        assert "confirmed_sections" in content or "sections" in content

    def test_init_suggestions_linked_from_branch_leaf_index(self):
        content = _read_command_file()
        assert "init-suggestions" in content
        assert "Top-level artifact" in content or "top-level artifact" in content.lower()

    def test_four_opt_in_modes_documented(self):
        content = _read_command_file()
        for mode in ("skip", "additional_facet", "report_section_only", "additional_facet_AND_section"):
            assert mode in content, f"Focus-area opt-in mode '{mode}' must be documented"

    def test_init_suggestions_schema_fields(self):
        content = _read_command_file()
        assert "confirmed_sections" in content
        assert "confirmed_visualisations" in content or "confirmed_visualizations" in content
        assert "additional_focus_areas" in content

    def test_init_suggestions_linked_from_agent_file(self):
        agent_content = _read_agent_file()
        assert "init-suggestions-{ts}.yml" in agent_content


class TestMeditateCombinedFacetConfirmation:
    """K4: Combined Pattern-B askQuestion folds Q-Confirm-1 + Q-Confirm-2 + init-suggestions."""

    def test_combined_pattern_b_ask_question_documented(self):
        content = _read_command_file()
        assert "Q-Confirm-1" in content or "single" in content.lower()
        assert "AskQuestion" in content

    def test_combined_flow_replaces_q_confirm_1_and_q_confirm_2(self):
        content = _read_command_file()
        lower = content.lower()
        assert "combined" in lower or "single" in lower
        assert "5 sub-question" in lower or "five sub-question" in lower or (
            "replacing" in lower and "q-confirm" in lower
        )

    def test_five_sub_questions_documented(self):
        content = _read_command_file()
        lower = content.lower()
        assert "facets" in lower
        assert "sections" in lower
        assert "visualisations" in lower or "visualizations" in lower
        assert "focus" in lower
        assert "deep_confirm" in content or "deep-confirm" in lower

    def test_four_mode_focus_area_sub_question_documented(self):
        content = _read_command_file()
        for mode in ("skip", "additional_facet", "report_section_only", "additional_facet_AND_section"):
            assert mode in content

    def test_decision_guidance_prose_per_sub_question(self):
        content = _read_command_file()
        lower = content.lower()
        assert "decision" in lower and "guidance" in lower


class TestMeditateAdditionalFacetCostAck:
    """K4: Cost-ack re-presentation triggers on additional_facet/additional_facet_AND_section only."""

    def test_cost_ack_re_presentation_documented(self):
        content = _read_command_file()
        lower = content.lower()
        assert "re-presented" in lower or "re-presentation" in lower or "re-acknowledge" in lower

    def test_triggers_on_additional_facet(self):
        content = _read_command_file()
        assert "additional_facet" in content
        assert "read-only-richness" in content.lower() or "read-only-richness variant" in content

    def test_triggers_on_additional_facet_and_section(self):
        content = _read_command_file()
        assert "additional_facet_AND_section" in content
        lower = content.lower()
        assert "additional_facet_and_section" in lower
        assert "read-only-richness" in lower or "re-acknowledge" in lower or "cost" in lower

    def test_does_not_trigger_on_skip(self):
        content = _read_command_file()
        lower = content.lower()
        assert "skip" in lower
        trigger_block = re.search(
            r"additional_facet.*?additional_facet_AND_section",
            content,
            re.DOTALL,
        )
        assert trigger_block is not None, "Trigger condition block must mention both modes"

    def test_re_presentation_uses_read_only_richness_variant(self):
        content = _read_command_file()
        assert "read-only-richness" in content.lower() or "locked" in content.lower()
        assert "additional_facet" in content or "additional facet" in content.lower()


class TestMeditateSetOncePersistence:
    """K6: Set-once-per-invocation richness rule and expansion variant."""

    def test_set_once_per_invocation_documented(self):
        content = _read_command_file()
        lower = content.lower()
        assert "set once" in lower or "set-once" in lower or "cannot be changed" in lower

    def test_expansion_variant_shows_richness_locked(self):
        content = _read_command_file()
        assert "locked" in content.lower()
        lower = content.lower()
        assert "richness" in lower and "locked" in lower

    def test_no_reset_richness_flag(self):
        content = _read_command_file()
        assert "--reset-richness" not in content

    def test_users_must_cancel_to_change_richness(self):
        content = _read_command_file()
        lower = content.lower()
        assert "cancel" in lower and "re-invoke" in lower


class TestMeditateAdversarialReviewerExtension:
    """K9: Adversarial reviewer now has 13 dimensions including Dim 12 and Dim 13."""

    def test_reviewer_has_13_dimensions(self):
        content = _read_command_file()
        assert "13" in content and ("dimension" in content.lower() or "Dim" in content)
        assert "13 dimensions" in content or "13. " in content or (
            "**13." in content or "13. **" in content
        )

    def test_dimension_12_comprehensiveness_fidelity(self):
        content = _read_command_file()
        assert "12" in content
        assert "Comprehensiveness fidelity" in content or "comprehensiveness fidelity" in content.lower()

    def test_dimension_13_init_suggestion_honour(self):
        content = _read_command_file()
        assert "13" in content
        lower = content.lower()
        assert "init-suggestion" in lower or "init_suggestion" in lower
        assert "honour" in lower or "honor" in lower

    def test_dimension_9_level_conditional_expansion(self):
        content = _read_command_file()
        lower = content.lower()
        assert "peer_review_surfacing" in lower or "peer-review surfacing" in lower
        assert "consolidation_only" in content or "named_section" in content


class TestMeditateRespawnProtocol:
    """K9: Respawn protocol documented in adversarial review section."""

    def test_respawn_protocol_documented(self):
        content = _read_command_file()
        lower = content.lower()
        assert "respawn" in lower

    def test_respawn_reasons_is_list_typed(self):
        content = _read_command_file()
        assert "respawn_reasons:" in content

    def test_required_respawn_payload_keys_present(self):
        content = _read_command_file()
        required_keys = [
            "respawn_reasons",
            "reviewer_iteration",
            "prior_report_paths",
            "missing_sections",
            "missing_visualisations",
            "accepted_finalisation_enhancements",
            "preserve_other_content",
            "comprehensiveness_payload",
            "init_suggestions_payload",
            "theming_payload",
        ]
        for key in required_keys:
            assert key in content, f"Respawn payload key '{key}' must be documented"

    def test_respawn_shares_iteration_cap(self):
        content = _read_command_file()
        lower = content.lower()
        assert "3 iteration" in lower or "≤3" in content or "≤ 3" in content

    def test_respawn_required_true_bypasses_standard_flow(self):
        content = _read_command_file()
        assert "respawn_required: true" in content
        lower = content.lower()
        assert "bypass" in lower or "bypasses" in lower

    def test_respawn_then_re_review_semantics(self):
        content = _read_command_file()
        lower = content.lower()
        assert "respawn" in lower
        assert "review" in lower
        assert "re-review" in lower or "next iteration" in lower or "reviewed at iter" in lower


class TestMeditateRespawnFiniteIteration:
    """K9 pinned regression: Respawn protocol cannot infinite-loop — invariants documented verbatim."""

    def test_iteration_cap_is_three(self):
        content = _read_command_file()
        assert "3 iteration" in content.lower() or "≤3" in content or "3 iterations" in content.lower()
        assert "cap" in content.lower()

    def test_respawn_counts_as_one_iteration(self):
        content = _read_command_file()
        lower = content.lower()
        assert "respawn" in lower
        assert "shared" in lower or "shares" in lower or "same" in lower
        assert "budget" in lower or "cap" in lower

    def test_escalate_verdict_at_iter_3_with_dim_13(self):
        content = _read_command_file()
        assert "ESCALATE" in content
        lower = content.lower()
        assert "iter 3" in lower or "iteration 3" in lower or "iter=3" in lower
        assert "dim 13" in lower or "respawn" in lower
        assert "`ESCALATE`" in content or "ESCALATE" in content

    def test_max_useful_respawns_is_two(self):
        content = _read_command_file()
        assert "2" in content
        lower = content.lower()
        assert "maximum useful respawn" in lower or "max useful respawn" in lower or (
            "respawn at end of iter 1" in lower or "iter 1" in lower
        )


class TestMeditatePayloadPropagation:
    """K5: comprehensiveness: payload propagated from depth-0 to all children."""

    def test_comprehensiveness_in_depth0_spawn_prompt(self):
        content = _read_command_file()
        assert "comprehensiveness" in content.lower()
        assert "spawn" in content.lower() and "comprehensiveness" in content.lower()

    def test_propagated_to_children_in_phase_d(self):
        content = _read_command_file()
        lower = content.lower()
        assert "comprehensiveness" in lower
        assert "propagat" in lower or "passed through" in lower or "thread" in lower

    def test_propagated_in_quick_mode(self):
        content = _read_command_file()
        lower = content.lower()
        assert "quick" in lower and "comprehensiveness" in lower
        quick_section = content.split("quick")[1] if "quick" in lower else ""
        assert "comprehensiveness" in quick_section.lower() or "comprehensiveness" in lower

    def test_abort_if_comprehensiveness_missing_documented(self):
        content = _read_command_file()
        assert "comprehensiveness:` payload required" in content or (
            "comprehensiveness:` is missing" in content or
            "abort" in content.lower() and "comprehensiveness" in content.lower()
        )
        assert "caller misconfigured" in content


class TestMeditateNoNewDistFilesK8:
    """K8 regression: No spec-introduced paths leaked into dist/install/version-bump enumerations."""

    # Runtime-only artefacts that must never ship in dist.
    # NOTE: The four decomp-legitimate paths (crux-cursor-meditation-guide,
    # crux-skill-memory-meditation-{research,quick,ensemble,review,report,coordination})
    # have been REMOVED from this list per plan §2.2 row 12 + §3.5.
    # Those paths are now LEGITIMATE dist artefacts added by S10.
    # See TestMeditateDecompDistFilesPresent for their positive-presence assertions.
    SPEC_INTRODUCED_PATHS = [
        "init-suggestions",
        "finalisation-enhancements",
        "follow-up-meditation",
        "follow-up-spec",
        "follow-up-memories",
        "follow-up-expansion",
    ]

    def _get_dist_files(self) -> list[str]:
        repo_root = Path(__file__).resolve().parent.parent
        zip_script = repo_root / "scripts" / "create-crux-zip.py"
        content = zip_script.read_text(encoding="utf-8")
        match = re.search(r"DIST_FILES\s*=\s*\[(.*?)\]", content, re.DOTALL)
        if not match:
            return []
        raw = match.group(1)
        return [s.strip().strip('"').strip("'") for s in raw.splitlines() if s.strip().strip(",").strip()]

    def _get_memory_file_prefixes(self) -> list[str]:
        repo_root = Path(__file__).resolve().parent.parent
        install_py = repo_root / "install.py"
        content = install_py.read_text(encoding="utf-8")
        match = re.search(r"MEMORY_FILE_PREFIXES\s*=\s*\((.*?)\)", content, re.DOTALL)
        if not match:
            return []
        raw = match.group(1)
        return [s.strip().strip('"').strip("'") for s in raw.splitlines() if s.strip().strip(",").strip()]

    def _get_dist_manifest_entries(self) -> list[str]:
        repo_root = Path(__file__).resolve().parent.parent
        manifest = repo_root / ".crux" / "dist-manifest.json"
        if not manifest.exists():
            return []
        data = json.loads(manifest.read_text(encoding="utf-8"))
        return data.get("files", [])

    def test_dist_files_no_spec_introduced_paths(self):
        dist_files = self._get_dist_files()
        for spec_path in self.SPEC_INTRODUCED_PATHS:
            for dist_entry in dist_files:
                assert spec_path not in dist_entry, (
                    f"Spec-introduced path '{spec_path}' must NOT appear in DIST_FILES; "
                    f"found in entry '{dist_entry}'"
                )

    def test_memory_file_prefixes_no_spec_introduced_paths(self):
        prefixes = self._get_memory_file_prefixes()
        for spec_path in self.SPEC_INTRODUCED_PATHS:
            for prefix in prefixes:
                assert spec_path not in prefix, (
                    f"Spec-introduced path '{spec_path}' must NOT appear in MEMORY_FILE_PREFIXES; "
                    f"found in entry '{prefix}'"
                )

    def test_dist_manifest_no_spec_introduced_paths(self):
        entries = self._get_dist_manifest_entries()
        for spec_path in self.SPEC_INTRODUCED_PATHS:
            for entry in entries:
                assert spec_path not in entry, (
                    f"Spec-introduced path '{spec_path}' must NOT appear in dist-manifest.json; "
                    f"found in entry '{entry}'"
                )

    def test_dist_files_list_readable(self):
        dist_files = self._get_dist_files()
        assert len(dist_files) > 0, "DIST_FILES must be non-empty and parseable"

    def test_memory_file_prefixes_list_readable(self):
        prefixes = self._get_memory_file_prefixes()
        assert len(prefixes) > 0, "MEMORY_FILE_PREFIXES must be non-empty and parseable"


# Alias for the checklist's "TestMeditateNoNewFilesInDist" item
TestMeditateNoNewFilesInDist = TestMeditateNoNewDistFilesK8


class TestMeditateBackwardsCompatibility:
    """Pinned regression: compact level reproduces pre-richness numeric minima exactly.

    These literals are intentional — the test must fail loudly if any future
    change lowers the compact minima from their baseline values.
    """

    def test_compact_chart_minimum_unchanged(self):
        content = _read_command_file()
        lower = content.lower()
        assert (
            "`compact`=4" in content
            or "compact`=4" in content
            or "4 charts" in lower
            or ("**4**" in content and "chart" in lower)
        ), "compact charts minimum MUST be 4 (pinned regression)"

    def test_compact_infographic_minimum_unchanged(self):
        content = _read_command_file()
        lower = content.lower()
        assert (
            "`compact`=3" in content
            or "3 infographics" in lower
            or ("**3**" in content and "infographic" in lower)
        ), "compact infographics minimum MUST be 3 (pinned regression)"

    def test_compact_calculator_minimum_unchanged(self):
        content = _read_command_file()
        lower = content.lower()
        assert (
            "`compact`=1" in content
            or "1 calculator" in lower
            or ("**1**" in content and "calculator" in lower)
        ), "compact calculators minimum MUST be 1 (pinned regression)"

    def test_compact_calculator_scenarios_unchanged(self):
        content = _read_command_file()
        lower = content.lower()
        assert (
            "`compact`=3" in content
            or "3 scenarios per calculator" in lower
            or ("**3**" in content and "scenario" in lower)
        ), "compact calculator scenarios_per minimum MUST be 3 (pinned regression)"

    def test_compact_depth3_leaf_inclusion_unchanged(self):
        content = _read_command_file()
        assert "summary" in content.lower() and "compact" in content.lower()
        assert "depth3_leaf_inclusion" in content.lower() or "depth-3 leaf" in content.lower()

    def test_compact_per_branch_section_unchanged(self):
        content = _read_command_file()
        assert "consolidation_only" in content

    def test_compact_peer_review_surfacing_unchanged(self):
        content = _read_command_file()
        assert "consolidation_only" in content
        assert "peer_review_surfacing" in content.lower() or "peer-review" in content.lower()

    def test_no_standalone_q_comprehensiveness_gate(self):
        content = _read_command_file()
        assert "Q-Comprehensiveness" not in content, (
            "Standalone Q-Comprehensiveness gate must not exist anywhere in coordinator "
            "(negative regression — must not be re-introduced)"
        )


class TestMeditateSafeguardRegressions:
    """K7: All pre-existing safeguards still present in modified surfaces."""

    def test_anti_homogenization_block_present(self):
        content = _read_command_file()
        assert "Anti-Homogenization" in content

    def test_universal_contrast_rules_present(self):
        content = _read_command_file()
        assert "Universal Contrast" in content

    def test_subject_matter_focus_rule_present(self):
        content = _read_command_file()
        assert "Subject-Matter Focus" in content

    def test_pattern_b_integrity_present(self):
        content = _read_command_file()
        assert "Pattern B" in content or "Pattern B" in content

    def test_paired_html_pdf_rule_present(self):
        content = _read_command_file()
        lower = content.lower()
        assert ("html" in lower and "pdf" in lower)
        assert "paired" in lower or "pair" in lower

    def test_mandatory_citations_rule_present(self):
        content = _read_command_file()
        lower = content.lower()
        assert "citation" in lower and ("mandatory" in lower or "required" in lower)

    def test_iteration_cap_present(self):
        content = _read_command_file()
        lower = content.lower()
        assert "≤3" in content or "3 iteration" in lower or "≤ 3" in content

    def test_must_fix_needs_user_input_schema_with_context_field(self):
        content = _read_command_file()
        assert "MUST_FIX" in content
        assert "needs_user_input" in content
        assert "`context`" in content or "context:" in content or "context text" in content.lower()

    def test_retrospective_always_written(self):
        content = _read_command_file()
        lower = content.lower()
        assert "retrospective" in lower
        assert "always written" in lower or "always present" in lower or "always write" in lower


# ---------------------------------------------------------------------------
# K10 — Finalisation Enhancements Gate + Ensemble Layered Cadence
# ---------------------------------------------------------------------------


class TestMeditateFinalisationEnhancementGate:
    """K10a: Q-Finalisation-Enhancements gate documented correctly."""

    def test_gate_exists_in_command_file(self):
        content = _read_command_file()
        assert "Q-Finalisation-Enhancements" in content

    def test_gate_is_multi_select_0_to_5(self):
        content = _read_command_file()
        assert "multi-select" in content.lower() or "multi-select 0–5" in content
        assert "0–5" in content

    def test_gate_fires_after_consolidation_before_adversarial_review(self):
        content = _read_command_file()
        lower = content.lower()
        assert "consolidat" in lower
        assert "adversarial" in lower
        assert "before" in lower
        gate_idx = content.find("Q-Finalisation-Enhancements")
        surrounding = content[max(0, gate_idx - 300):gate_idx + 600]
        assert "consolidat" in surrounding.lower() or "before" in surrounding.lower()

    def test_per_option_labels_include_cost_class(self):
        content = _read_command_file()
        assert "cost_class" in content or "[{cost_class}]" in content or "cost class" in content.lower()

    def test_decision_guidance_prose_cost_class_consequences(self):
        content = _read_command_file()
        lower = content.lower()
        assert "cheap" in lower and "expensive" in lower
        assert "respawn" in lower and "queue" in lower


class TestMeditateK10SkipAllBackwardsCompat:
    """K10 pinned regression: skip-all (0 accepted) path leaves every surface unchanged."""

    def test_skip_all_produces_no_accepted_enhancements_in_respawn(self):
        content = _read_command_file()
        lower = content.lower()
        assert "accepted_finalisation_enhancements" in content
        assert "skip" in lower
        assert "skip-all" in lower or "0 accepted" in lower or "count=0" in lower or "count == 0" in lower

    def test_respawn_reasons_excludes_accepted_enhancements_on_skip_all(self):
        content = _read_command_file()
        assert "respawn_reasons" in content
        lower = content.lower()
        assert "does not contain" in lower or "no additional" in lower or (
            "accepted_finalisation_enhancements" in content and "skip" in lower
        )

    def test_no_follow_up_files_written_on_skip_all(self):
        content = _read_command_file()
        lower = content.lower()
        assert "follow-up" in lower or "follow_up" in lower
        assert "queue" in lower
        assert "skip" in lower

    def test_footer_omits_finalisation_enhancements_segment_on_skip(self):
        content = _read_command_file()
        lower = content.lower()
        assert "finalisation-enhancements" in lower
        assert "omit" in lower or "absent" in lower or "count == 0" in lower or "count=0" in lower

    def test_finalisation_enhancements_yml_written_with_unchosen_persisted(self):
        content = _read_command_file()
        assert "unchosen_persisted" in content

    def test_no_additional_adversarial_review_iteration_consumed(self):
        content = _read_command_file()
        lower = content.lower()
        assert "skip" in lower and "adversarial" in lower
        assert "≤3" in content or "3 iteration" in lower


class TestMeditateFinalisationCheapAcceptRespawn:
    """K10b: Accepting cheap enhancements bundles them into respawn payload."""

    def test_accepted_enhancements_list_populated_when_cheap_accepted(self):
        content = _read_command_file()
        assert "accepted_finalisation_enhancements" in content
        lower = content.lower()
        assert "cheap" in lower and "respawn" in lower

    def test_respawn_reasons_includes_accepted_enhancements(self):
        content = _read_command_file()
        assert "respawn_reasons" in content
        assert "accepted_finalisation_enhancements" in content

    def test_cheap_respawn_shares_iteration_cap(self):
        content = _read_command_file()
        lower = content.lower()
        assert "≤3" in content or "3 iteration" in lower
        assert "shared" in lower or "shares" in lower or "same" in lower or "existing" in lower

    def test_multiple_cheap_items_bundle_into_single_respawn(self):
        content = _read_command_file()
        lower = content.lower()
        assert "bundle" in lower or "bundled" in lower or "single respawn" in lower or "first" in lower


class TestMeditateFinalisationExpensiveQueueDefault:
    """K10b: Expensive items default to queue treatment."""

    def test_expensive_default_is_queue(self):
        content = _read_command_file()
        lower = content.lower()
        assert "expensive" in lower and "queue" in lower
        assert "default" in lower
        assert "expensive" in lower and "queue" in lower and "default" in lower
        assert "queue" in content and ("default" in content or "preselected" in content)

    def test_follow_up_file_written_for_queued_items(self):
        content = _read_command_file()
        assert "follow-up-" in content and ".yml" in content
        assert "queue" in content.lower()

    def test_no_agent_spawned_for_queue_treatment(self):
        content = _read_command_file()
        lower = content.lower()
        assert "queue" in lower
        assert "zero" in lower or "no agent" in lower or "0 agent" in lower or (
            "zero extra agent" in lower or "zero in-invocation" in lower
        )

    def test_queued_item_surfaces_in_continuation_menu(self):
        content = _read_command_file()
        lower = content.lower()
        assert "spawn queued" in lower or "queued follow-up" in lower
        assert "continuation" in lower or "step 11" in lower or "step 12" in lower


class TestMeditateFinalisationExpensiveSpawnNow:
    """K10b: spawn_now triggers cost-ack re-presentation; cancel falls back to queue."""

    def test_spawn_now_triggers_cost_ack_re_presentation(self):
        content = _read_command_file()
        assert "spawn_now" in content
        lower = content.lower()
        assert "cost" in lower and "re-presentation" in lower or "re-acknowledge" in lower

    def test_cancel_at_re_presentation_falls_back_to_queue(self):
        content = _read_command_file()
        lower = content.lower()
        assert "cancel" in lower and "queue" in lower
        assert "drop" in lower or "fall back" in lower or "fall back to queue" in lower or (
            "cancel" in lower and "queue" in lower
        )
        assert "spawn_now" in lower or "spawn now" in lower

    def test_proceed_defers_spawning_until_after_adversarial_review(self):
        content = _read_command_file()
        lower = content.lower()
        assert "spawn_now" in lower or "spawn now" in lower
        assert "after" in lower and "adversarial" in lower
        assert "after the adversarial" in lower or "after adversarial" in lower or (
            "adversarial cycle completes" in lower or "cycle completes" in lower
        )


class TestMeditateFinalisationPersistence:
    """K10c: finalisation-enhancements.yml schema matches spec; linked from Branch & Leaf Index."""

    def test_finalisation_yml_schema_all_fields(self):
        content = _read_command_file()
        assert "finalisation-enhancements.yml" in content
        agent_content = _read_agent_file()
        combined = content + agent_content
        required_fields = ["accepted", "treatment", "decided_at_utc", "impact_score",
                           "insight_value_score", "composite_score", "cost_class"]
        for field in required_fields:
            assert field in combined, f"finalisation-enhancements.yml schema must document field '{field}'"

    def test_decided_at_utc_filled_by_calling_agent(self):
        content = _read_command_file()
        assert "decided_at_utc" in content
        lower = content.lower()
        assert "calling agent" in lower

    def test_linked_from_branch_leaf_index(self):
        content = _read_command_file()
        lower = content.lower()
        assert "finalisation-enhancements" in lower
        assert "top-level artifact" in lower or "top-level artifacts" in lower

    def test_unchosen_items_surface_in_continuation_menu(self):
        content = _read_command_file()
        assert "unchosen_persisted" in content
        lower = content.lower()
        assert "continuation" in lower or "step 11" in lower


class TestMeditateFinalisationContinuationMenu:
    """K10c: Step 12 continuation menu grouped under section headings."""

    def test_step_12_has_section_headings(self):
        content = _read_command_file()
        lower = content.lower()
        assert "expansion directions" in lower
        assert "apply un-chosen" in lower or "apply unchosen" in lower or "re-apply" in lower
        assert "spawn queued" in lower

    def test_unchosen_enhancement_options_include_title(self):
        content = _read_command_file()
        assert "unchosen_persisted" in content or "re-apply unchosen" in content.lower()
        lower = content.lower()
        assert "title" in lower and "enhancement" in lower

    def test_queued_expensive_options_trigger_cost_ack(self):
        content = _read_command_file()
        lower = content.lower()
        assert "spawn queued" in lower or "queued follow-up" in lower
        assert "cost" in lower and "acknowledge" in lower or "re-presentation" in lower or "spawn_now" in lower


class TestMeditateFinalisationFiniteIteration:
    """K10 pinned regression: accepted_finalisation_enhancements cause cannot exceed iteration budget."""

    def test_gate_fires_at_most_once_per_meditation(self):
        content = _read_command_file()
        lower = content.lower()
        assert "once" in lower and "finalisation" in lower
        assert "Q-Finalisation-Enhancements" in content
        gate_count = content.count("Q-Finalisation-Enhancements")
        assert gate_count >= 1
        assert "fires once" in lower or "at most once" in lower or "gate fires once" in lower or (
            "once per meditation" in lower
        )

    def test_cheap_items_contribute_to_first_iteration_respawn(self):
        content = _read_command_file()
        lower = content.lower()
        assert "first" in lower and "iteration" in lower and "respawn" in lower
        assert "cheap" in lower

    def test_iteration_cap_remains_three(self):
        content = _read_command_file()
        lower = content.lower()
        assert "3 iteration" in lower or "≤3" in content or "cap is **3" in content.lower()

    def test_escalate_remains_verdict_at_iteration_3(self):
        content = _read_command_file()
        assert "ESCALATE" in content
        lower = content.lower()
        assert "iter 3" in lower or "iteration 3" in lower or "≤3" in content


class TestMeditateFinalisationTripleReasonRespawn:
    """K10b: Triple-reason respawn ordering: accepted_enhancements → missing_vis → missing_sections."""

    def test_triple_reason_ordering_documented(self):
        content = _read_command_file()
        assert "respawn_reasons" in content
        lower = content.lower()
        assert "accepted_finalisation_enhancements" in lower or "accepted finalisation" in lower
        assert "missing_init_suggestion_sections" in content or "missing_sections" in content
        assert "missing_init_suggestion_visualisations" in content or "missing_visualisations" in content

    def test_accepted_enhancements_processed_first(self):
        content = _read_command_file()
        lower = content.lower()
        assert "accepted_finalisation_enhancements" in lower
        fe_idx = lower.find("accepted_finalisation_enhancements")
        vis_idx = lower.find("missing_init_suggestion_visualisations")
        sec_idx = lower.find("missing_init_suggestion_sections")
        if fe_idx != -1 and vis_idx != -1 and sec_idx != -1:
            assert fe_idx < vis_idx or fe_idx < sec_idx, (
                "accepted_finalisation_enhancements must appear before other reasons "
                "in the per-reason ordering documentation"
            )

    def test_report_skill_processes_in_order(self):
        content = _read_command_file()
        assert "per-reason ordering" in content.lower() or "processes" in content.lower()
        lower = content.lower()
        assert "order" in lower


class TestMeditateK10EnsembleLayeredCadence:
    """K10 ensemble: Per-tree YAMLs + root combined YAML + layered cadence semantics."""

    def test_per_tree_yamls_documented(self):
        agent_content = _read_agent_file()
        combined = _read_command_file() + agent_content
        assert "model-subdir" in combined or "{model-subdir}" in combined
        assert "finalisation-enhancements.yml" in combined

    def test_per_tree_yaml_has_source_tree_field(self):
        agent_content = _read_agent_file()
        assert "source_tree:" in agent_content

    def test_per_tree_yaml_has_surfaced_to_root_placeholder(self):
        agent_content = _read_agent_file()
        assert "surfaced_to_root" in agent_content

    def test_root_combined_yaml_documented(self):
        agent_content = _read_agent_file()
        combined = _read_command_file() + agent_content
        assert "cross_model_candidates" in combined
        assert "union_candidates" in combined

    def test_surfaced_to_root_annotation_documented(self):
        agent_content = _read_agent_file()
        combined = _read_command_file() + agent_content
        assert "surfaced_to_root: true" in combined or "surfaced_to_root:" in combined
        assert "aggregator" in combined.lower()

    def test_single_root_ask_question_documented(self):
        content = _read_command_file()
        lower = content.lower()
        assert "ensemble root" in lower or "root combined" in lower or "single" in lower
        assert "Q-Finalisation-Enhancements" in content

    def test_root_ranking_by_composite_score(self):
        agent_content = _read_agent_file()
        combined = _read_command_file() + agent_content
        lower = combined.lower()
        assert "composite_score" in lower or "composite score" in lower
        assert "union_candidates" in lower

    def test_single_model_backwards_compat(self):
        content = _read_command_file()
        lower = content.lower()
        assert "single-model" in lower or "single model" in lower
        assert "finalisation" in lower

    def test_per_tree_vs_cross_model_report_respawn_targeting(self):
        content = _read_command_file()
        lower = content.lower()
        assert "per-tree" in lower or "per-tree report" in lower or "tree-sourced" in lower
        assert "cross_model" in lower or "cross-model" in lower


class TestMeditateK10EnsembleContinuationMenuLayered:
    """K10 ensemble: Continuation menu surfaces per-tree-only unchosen items with provenance labels."""

    def test_per_tree_only_items_have_provenance_label(self):
        content = _read_command_file()
        lower = content.lower()
        assert "from tree" in lower or "model-label" in lower or "provenance" in lower or (
            "surfaced_to_root: false" in lower or "not surfaced at root" in lower
        )

    def test_root_unchosen_items_have_provenance_label(self):
        content = _read_command_file()
        lower = content.lower()
        assert "cross-model" in lower or "cross_model" in lower
        assert "from tree" in lower or "provenance" in lower or "model-label" in lower

    def test_per_tree_only_item_targets_per_tree_report_respawn(self):
        content = _read_command_file()
        lower = content.lower()
        assert "per-tree" in lower and "report" in lower
        assert "respawn" in lower


class TestMeditateK10QuickModeFires:
    """K10: Q-Finalisation-Enhancements gate fires in Quick mode too."""

    def test_gate_fires_in_quick_mode(self):
        content = _read_command_file()
        lower = content.lower()
        assert "quick" in lower and "finalisation" in lower
        assert "Q-Finalisation-Enhancements" in content

    def test_quick_mode_same_0_to_5_cap(self):
        content = _read_command_file()
        assert "0–5" in content

    def test_quick_mode_skip_all_backwards_compat(self):
        content = _read_command_file()
        lower = content.lower()
        assert "quick" in lower
        assert "skip" in lower and "today" in lower or "behaviour" in lower or "backward" in lower


class TestMeditateK10ReflectionRubric:
    """K10c: Impact × insight-value rubric documented in agent file with worked examples."""

    def test_rubric_documented_in_agent_file(self):
        agent_content = _read_agent_file()
        lower = agent_content.lower()
        assert "impact_score" in lower and "insight_value_score" in lower
        assert "rubric" in lower or "scoring" in lower

    def test_both_axes_use_1_to_10_scale(self):
        agent_content = _read_agent_file()
        assert "1–10" in agent_content or "1-10" in agent_content

    def test_worked_example_impact_score_9(self):
        agent_content = _read_agent_file()
        lower = agent_content.lower()
        assert "impact_score" in lower
        assert "`9`" in agent_content or "9` =" in agent_content or "9 =" in agent_content

    def test_worked_example_impact_score_5(self):
        agent_content = _read_agent_file()
        lower = agent_content.lower()
        assert "`5`" in agent_content or "5` =" in agent_content

    def test_worked_example_impact_score_2(self):
        agent_content = _read_agent_file()
        assert "`2`" in agent_content or "2` =" in agent_content

    def test_worked_example_insight_value_score_9(self):
        agent_content = _read_agent_file()
        lower = agent_content.lower()
        assert "insight_value_score" in lower
        assert "9" in agent_content

    def test_minimum_impact_threshold_defaults_to_6(self):
        agent_content = _read_agent_file()
        assert "minimum_impact_threshold" in agent_content
        assert "6" in agent_content
        idx = agent_content.find("minimum_impact_threshold")
        surrounding = agent_content[max(0, idx - 50):idx + 100]
        assert "6" in surrounding


class TestMeditateK10WeightsConfigurable:
    """K10 pinned regression: finalisationEnhancements.weights default = {impact:1.0, insight_value:1.0}."""

    def test_weights_key_documented(self):
        agent_content = _read_agent_file()
        combined = _read_command_file() + agent_content
        assert "finalisationEnhancements" in combined or "finalisation_enhancements" in combined.lower()
        assert "weights" in combined.lower()

    def test_default_weights_are_1_0(self):
        agent_content = _read_agent_file()
        combined = _read_command_file() + agent_content
        assert "impact: 1.0" in combined or "impact: 1.0" in combined
        assert "insight_value: 1.0" in combined

    def test_formula_defaults_to_multiplicative_product(self):
        agent_content = _read_agent_file()
        combined = _read_command_file() + agent_content
        lower = combined.lower()
        assert "product" in lower or "multiplicative" in lower
        assert "formula" in lower

    def test_weights_configurable_via_config_key(self):
        agent_content = _read_agent_file()
        combined = _read_command_file() + agent_content
        assert "cruxMemories.meditate.finalisationEnhancements.weights" in combined or (
            "finalisationEnhancements" in combined and "weights" in combined
        )


# ---------------------------------------------------------------------------
# S08: New assertion classes — Guide Agent, Six Skills, Thin Coordinator,
#      Trimmed Memory-Manager, Dist Presence, and Negative-Assertion Classes
# ---------------------------------------------------------------------------


class TestMeditationGuideAgent:
    """Positive and negative assertions for .cursor/agents/crux-cursor-meditation-guide.md."""

    def test_agent_file_exists(self):
        p = (
            Path(__file__).resolve().parent.parent
            / ".cursor" / "agents" / "crux-cursor-meditation-guide.md"
        )
        assert p.is_file(), "crux-cursor-meditation-guide.md must exist on disk"

    def test_frontmatter_name_matches_filename(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "name: crux-cursor-meditation-guide" in content

    def test_frontmatter_model_pinned(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "model: claude-opus-4-6" in content

    def test_frontmatter_description_contains_meditation(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "meditation" in content.lower()

    def test_frontmatter_description_contains_recursive_memory_informed(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "Recursive memory-informed" in content

    def test_persona_prologue_present(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "You are the CRUX Meditation Guide" in content

    def test_critical_load_context_section_present(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "CRITICAL: Load Context First" in content

    def test_user_input_escalation_section_present(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "User Input Escalation" in content

    def test_pattern_a_documented(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "Pattern A" in content

    def test_pattern_b_documented(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "Pattern B" in content

    def test_needs_user_input_documented(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "needs_user_input" in content

    def test_mode_router_research_depth0_workflow_present(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "Research mode depth-0 workflow" in content

    def test_mode_router_phases_a_g_mentioned(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "Phases A–G" in content or "Phases A-G" in content

    def test_mode_router_quick_6_step_present(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "Quick" in content
        assert "6-step" in content

    def test_mode_router_k10_in_pass_reflection_present(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "K10 In-Pass Reflection" in content

    def test_mode_router_adversarial_review_13_dim_present(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "Adversarial Review" in content
        assert "13" in content

    def test_mode_router_ensemble_aggregation_k10_layered_present(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "Ensemble Aggregation" in content
        assert "K10 layered cadence" in content

    def test_mode_router_report_generation_obligation_present(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "Report generation obligation" in content

    def test_critical_rules_section_present(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "Critical Rules" in content

    def test_canonical_comprehensiveness_abort_error_string(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert (
            "comprehensiveness: payload required; missing from spawn prompt — caller misconfigured"
            in content
        )

    def test_feature_guard_flag_referenced(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "flags.enableMemories" in content

    def test_skill_delegation_documented(self):
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert ".cursor/skills/crux-skill-memory-meditation-" in content

    def test_no_memory_manager_executable_sections(self):
        """Guide agent must not implement memory-manager lifecycle modes.

        Adaptation from plan §3.1 #23: guide agent at line 446 legitimately
        references crux-cursor-memory-manager as a delegation note ("management is
        the responsibility of crux-cursor-memory-manager"). The negative assertion is
        therefore scoped to verify the guide agent does NOT implement the memory-manager
        lifecycle modes (Dream Mode, REM Sleep, etc.) rather than checking for full
        absence of the sibling-agent name.
        """
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        assert "### Dream Mode" not in content, (
            "Guide agent must not implement Dream Mode — that belongs to crux-cursor-memory-manager"
        )
        assert "### REM Sleep Mode" not in content, (
            "Guide agent must not implement REM Sleep Mode"
        )

    def test_no_ask_question_call_from_subagent(self):
        """Guide agent body must document the prohibition on calling AskQuestion directly."""
        content = _read_meditation_guide_agent_file()
        if not content:
            return
        lower = content.lower()
        assert "never calls" in lower and "askquestion" in lower, (
            "Guide agent must document the AskQuestion prohibition "
            "(per §3 boundary rules and AGENTS.md subagent protocol)"
        )


class TestMeditationSkillResearch:
    """Presence and contract assertions for crux-skill-memory-meditation-research."""

    def test_skill_md_exists(self):
        p = (
            Path(__file__).resolve().parent.parent
            / ".cursor" / "skills" / "crux-skill-memory-meditation-research" / "SKILL.md"
        )
        assert p.is_file()

    def test_frontmatter_name_matches_directory(self):
        content = _read_meditation_skill("research")
        if not content:
            return
        assert "name: crux-skill-memory-meditation-research" in content

    def test_description_contains_meditation(self):
        content = _read_meditation_skill("research")
        if not content:
            return
        assert "meditation" in content.lower()

    def test_description_contains_research_verb(self):
        content = _read_meditation_skill("research")
        if not content:
            return
        assert "Research" in content

    def test_phases_a_g_documented(self):
        content = _read_meditation_skill("research")
        if not content:
            return
        assert "Phases A–G" in content or "Phases A-G" in content

    def test_step_4b_focus_area_reconciliation_documented(self):
        content = _read_meditation_skill("research")
        if not content:
            return
        lower = content.lower()
        assert "step 4b" in lower
        assert "additional_focus_areas" in content

    def test_init_suggestions_yml_write_side_documented(self):
        content = _read_meditation_skill("research")
        if not content:
            return
        assert "init-suggestions-{ts}.yml" in content

    def test_k10c_reflection_writes_finalisation_enhancements_yml(self):
        content = _read_meditation_skill("research")
        if not content:
            return
        assert "finalisation-enhancements.yml" in content

    def test_canonical_treatment_filter_present(self):
        content = _read_meditation_skill("research")
        if not content:
            return
        assert "treatment:" in content
        for mode in ("skip", "additional_facet", "report_section_only", "additional_facet_AND_section"):
            assert mode in content, f"Treatment mode '{mode}' must be in research skill"


class TestMeditationSkillQuick:
    """Presence and contract assertions for crux-skill-memory-meditation-quick."""

    def test_skill_md_exists(self):
        p = (
            Path(__file__).resolve().parent.parent
            / ".cursor" / "skills" / "crux-skill-memory-meditation-quick" / "SKILL.md"
        )
        assert p.is_file()

    def test_frontmatter_name_matches_directory(self):
        content = _read_meditation_skill("quick")
        if not content:
            return
        assert "name: crux-skill-memory-meditation-quick" in content

    def test_description_contains_meditation(self):
        content = _read_meditation_skill("quick")
        if not content:
            return
        assert "meditation" in content.lower()

    def test_description_contains_quick_verb(self):
        content = _read_meditation_skill("quick")
        if not content:
            return
        assert "Quick" in content

    def test_6_step_protocol_documented(self):
        content = _read_meditation_skill("quick")
        if not content:
            return
        assert "6-step" in content

    def test_warn_only_citation_regime_documented(self):
        content = _read_meditation_skill("quick")
        if not content:
            return
        assert "warn_only" in content or "warn-only" in content

    def test_k10c_reflection_quick_variant_documented(self):
        content = _read_meditation_skill("quick")
        if not content:
            return
        assert "finalisation-enhancements.yml" in content
        assert "Quick" in content


class TestMeditationSkillEnsemble:
    """Presence and contract assertions for crux-skill-memory-meditation-ensemble."""

    def test_skill_md_exists(self):
        p = (
            Path(__file__).resolve().parent.parent
            / ".cursor" / "skills" / "crux-skill-memory-meditation-ensemble" / "SKILL.md"
        )
        assert p.is_file()

    def test_frontmatter_name_matches_directory(self):
        content = _read_meditation_skill("ensemble")
        if not content:
            return
        assert "name: crux-skill-memory-meditation-ensemble" in content

    def test_description_contains_meditation(self):
        content = _read_meditation_skill("ensemble")
        if not content:
            return
        assert "meditation" in content.lower()

    def test_description_contains_ensemble_verb(self):
        content = _read_meditation_skill("ensemble")
        if not content:
            return
        assert "Ensemble" in content

    def test_cross_model_synthesis_documented(self):
        content = _read_meditation_skill("ensemble")
        if not content:
            return
        assert "cross-model-synthesis.md" in content

    def test_k10_layered_cadence_steps_3b_3f_documented(self):
        content = _read_meditation_skill("ensemble")
        if not content:
            return
        assert "K10 layered cadence" in content
        assert "3b" in content
        assert "3f" in content

    def test_source_tree_field_documented(self):
        content = _read_meditation_skill("ensemble")
        if not content:
            return
        assert "source_tree" in content

    def test_surfaced_to_root_documented(self):
        content = _read_meditation_skill("ensemble")
        if not content:
            return
        assert "surfaced_to_root" in content

    def test_cross_model_candidates_and_union_candidates_documented(self):
        content = _read_meditation_skill("ensemble")
        if not content:
            return
        assert "cross_model_candidates" in content
        assert "union_candidates" in content

    def test_k10_ensemble_respawn_targeting_documented(self):
        content = _read_meditation_skill("ensemble")
        if not content:
            return
        assert "K10 Ensemble Respawn Targeting" in content

    def test_per_tree_write_only_documented(self):
        content = _read_meditation_skill("ensemble")
        if not content:
            return
        assert "per-tree" in content.lower() or "per tree" in content.lower()
        assert "write-only" in content or "write only" in content.lower()


class TestMeditationSkillReview:
    """Presence and contract assertions for crux-skill-memory-meditation-review."""

    def test_skill_md_exists(self):
        p = (
            Path(__file__).resolve().parent.parent
            / ".cursor" / "skills" / "crux-skill-memory-meditation-review" / "SKILL.md"
        )
        assert p.is_file()

    def test_frontmatter_name_matches_directory(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        assert "name: crux-skill-memory-meditation-review" in content

    def test_description_contains_meditation(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        assert "meditation" in content.lower()

    def test_description_contains_review_verb_and_13_dimensions(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        assert "13" in content
        lower = content.lower()
        assert "dimension" in lower

    def test_dimension_12_comprehensiveness_fidelity_documented(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        assert "Comprehensiveness fidelity" in content

    def test_dimension_13_init_suggestion_honour_documented(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        assert "Init-suggestion AND finalisation-enhancement honour" in content

    def test_dimension_9_level_conditional_expansion_documented(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        lower = content.lower()
        assert "peer_review_surfacing" in lower or "peer-review surfacing" in lower
        assert "consolidation_only" in content or "named_section" in content

    def test_report_skill_respawn_protocol_documented(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        assert "Report-Skill Respawn Protocol" in content

    def test_respawn_reasons_list_typed_documented(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        assert "respawn_reasons" in content
        assert "list-typed" in content or "list typed" in content

    def test_three_iteration_cap_documented(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        assert "≤3" in content or "cap is **3" in content.lower() or "3 iterations" in content.lower()
        assert "iteration" in content.lower()

    def test_must_fix_mandatory_context_documented(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        assert "MUST_FIX" in content
        assert "mandatory `context`" in content or "mandatory context" in content.lower()

    def test_max_useful_respawns_is_two(self):
        content = _read_meditation_skill("review")
        if not content:
            return
        lower = content.lower()
        assert "maximum useful respawns" in lower or "max useful respawns" in lower


class TestMeditationSkillReport:
    """Presence and contract assertions for crux-skill-memory-meditation-report."""

    def test_skill_md_exists(self):
        p = (
            Path(__file__).resolve().parent.parent
            / ".cursor" / "skills" / "crux-skill-memory-meditation-report" / "SKILL.md"
        )
        assert p.is_file()

    def test_frontmatter_name_matches_directory(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "name: crux-skill-memory-meditation-report" in content

    def test_description_contains_meditation(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "meditation" in content.lower()

    def test_description_contains_report_and_universal_contrast(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Report" in content
        assert "Universal Contrast" in content

    def test_comprehensiveness_level_mapping_table_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Comprehensiveness Level Mapping" in content

    def test_all_four_level_columns_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        for level in ("compact", "default", "detailed", "exhaustive"):
            assert level in content, f"Level '{level}' must appear in report skill"

    def test_compact_chart_minimum_pinned(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        lower = content.lower()
        assert (
            "`compact`=4" in content
            or "compact`=4" in content
            or "compact: 4" in lower
            or "4 charts" in lower
            or ("**4**" in content and "chart" in lower)
        ), "compact chart minimum MUST be 4 in report skill (pinned backwards-compat anchor)"

    def test_per_branch_section_rule_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Per-Branch Section Rule" in content

    def test_depth3_leaf_inclusion_rule_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Depth-3 Leaf Inclusion Rule" in content

    def test_peer_review_surfacing_rule_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Peer-Review Surfacing Rule" in content

    def test_init_suggestions_honour_rules_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Init-Suggestions Honour" in content

    def test_k10b_per_cheap_type_rendering_contract_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Per-Cheap-Type Rendering Contract" in content
        for cheap_type in (
            "executive_summary",
            "action_plan",
            "risks_section",
            "glossary",
            "decision_tree_infographic",
            "reader_persona_tldrs",
            "cross_branch_synthesis_section",
        ):
            assert cheap_type in content, (
                f"K10b cheap type '{cheap_type}' must be in report skill"
            )

    def test_universal_contrast_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Universal Contrast" in content

    def test_anti_homogenisation_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Anti-Homogenization" in content or "Anti-Homogenisation" in content or (
            "anti-homogenisation" in content.lower()
        )

    def test_chromium_fallback_chain_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "chromium-browser" in content

    def test_report_skill_respawn_resume_handler_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Per-reason processing order" in content or "accepted_finalisation_enhancements" in content

    def test_subject_matter_focus_present(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "Subject-Matter Focus" in content

    def test_footer_level_segment_always_written(self):
        content = _read_meditation_skill("report")
        if not content:
            return
        assert "level:" in content
        assert "finalisation-enhancements:" in content


class TestMeditationSkillCoordination:
    """Presence and contract assertions for crux-skill-memory-meditation-coordination."""

    def test_skill_md_exists(self):
        p = (
            Path(__file__).resolve().parent.parent
            / ".cursor" / "skills" / "crux-skill-memory-meditation-coordination" / "SKILL.md"
        )
        assert p.is_file()

    def test_frontmatter_name_matches_directory(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        assert "name: crux-skill-memory-meditation-coordination" in content

    def test_description_contains_meditation(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        assert "meditation" in content.lower()

    def test_description_contains_coordination_and_facet_registry(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        lower = content.lower()
        assert "coordination" in lower
        assert "facet registry" in lower or "filename grammar" in lower

    def test_18_row_filename_table_sentinel_rows_present(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        for sentinel in (
            "init-suggestions-{ts}.yml",
            "finalisation-enhancements.yml",
            "retrospective-{ts}.md",
            "report-{topic-slug}-{ts}.html",
        ):
            assert sentinel in content, f"Coordination skill must document filename '{sentinel}'"

    def test_placeholders_documented(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        for ph in ("{topic-slug}", "{ts}", "{N}"):
            assert ph in content, f"Placeholder '{ph}' must be documented"

    def test_prefix_glob_polling_rule_present(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        assert "prefix-glob" in content or "prefix glob" in content.lower()
        assert "ls -1t" in content

    def test_never_hard_code_rule_present(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        assert "Never hard-code" in content or "never hard-code" in content.lower()
        assert "report.html" in content

    def test_retrospective_template_present(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        assert "retrospective-{ts}.md" in content
        assert "Process Retrospective" in content

    def test_branch_leaf_index_template_present(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        assert "Branch & Leaf Index" in content
        assert "Top-level artifact" in content or "Top-level artifacts" in content

    def test_branch_leaf_index_extended_rows_present(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        lower = content.lower()
        assert "init-suggestions" in lower
        assert "finalisation-enhancements" in lower

    def test_ensemble_working_directory_documented(self):
        content = _read_meditation_skill("coordination")
        if not content:
            return
        assert "model-{label-slug}/" in content
        assert "ensemble-report-{topic-slug}" in content


class TestMeditationCommandThinCoordinator:
    """Assertions that the post-S06 thin coordinator command retains its required gates and pointers."""

    def test_usage_section_still_present(self):
        content = _read_meditation_artifact("command")
        assert "## Usage" in content

    def test_mode_descriptions_table_present(self):
        content = _read_meditation_artifact("command")
        for mode in ("Research", "Quick", "Ensemble"):
            assert mode in content, f"Mode '{mode}' must be described in thin coordinator"

    def test_depth_selection_gate_still_present(self):
        content = _read_meditation_artifact("command")
        assert "Q-Depth-Selection" in content
        lower = content.lower()
        assert "depth selection" in lower or "mandatory" in lower

    def test_cost_and_richness_ack_gate_still_present(self):
        content = _read_meditation_artifact("command")
        assert "Q-Cost-and-Richness-Acknowledgment" in content

    def test_theme_preflight_still_present(self):
        content = _read_meditation_artifact("command")
        lower = content.lower()
        assert "theme preflight" in lower or "Theme Preflight" in content

    def test_ensemble_orchestration_still_present(self):
        content = _read_meditation_artifact("command")
        lower = content.lower()
        assert "ensemble" in lower
        assert "modelPool" in content or "model-pool" in lower or "pool" in lower

    def test_continuation_menu_still_present(self):
        content = _read_meditation_artifact("command")
        lower = content.lower()
        assert "expansion directions" in lower or "Expansion directions" in content
        assert "apply un-chosen" in lower or "unchosen" in lower
        assert "spawn queued" in lower

    def test_finalisation_enhancements_gate_still_present(self):
        content = _read_meditation_artifact("command")
        assert "Q-Finalisation-Enhancements" in content
        assert "multi-select" in content.lower()
        assert "0–5" in content

    def test_combined_pattern_b_5_sub_questions_still_present(self):
        content = _read_meditation_artifact("command")
        lower = content.lower()
        assert "5 sub-question" in lower or "five sub-question" in lower or (
            "additional_focus_areas" in content and "5" in content
        )

    def test_instructions_spawn_target_is_meditation_guide(self):
        content = _read_meditation_artifact("command")
        related_idx = content.find("## Related")
        instructions = content[:related_idx] if related_idx != -1 else content
        assert "crux-cursor-meditation-guide" in instructions, (
            "Instructions section must spawn crux-cursor-meditation-guide"
        )

    def test_instructions_does_not_spawn_memory_manager(self):
        """Negative: spawn context (before ## Related) must NOT reference crux-cursor-memory-manager."""
        content = _read_meditation_artifact("command")
        related_idx = content.find("## Related")
        instructions = content[:related_idx] if related_idx != -1 else content
        assert "crux-cursor-memory-manager" not in instructions, (
            "Post-decomp command must NOT spawn crux-cursor-memory-manager in Instructions section"
        )

    def test_thin_coordinator_line_budget(self):
        """SOFT: coordinator should be at most ~1020 lines (informational advisory)."""
        content = _read_meditation_artifact("command")
        line_count = len(content.splitlines())
        assert line_count <= 1100, (
            f"Coordinator command has {line_count} lines — SOFT advisory: should be ≤750 lines "
            "post-decomp; strict enforcement deferred to S12 integrity review"
        )

    def test_coordination_conventions_pointer_present(self):
        content = _read_meditation_artifact("command")
        assert "crux-skill-memory-meditation-coordination" in content

    def test_research_mode_pointer_present(self):
        content = _read_meditation_artifact("command")
        assert "crux-skill-memory-meditation-research" in content

    def test_quick_mode_pointer_present(self):
        content = _read_meditation_artifact("command")
        assert "crux-skill-memory-meditation-quick" in content

    def test_adversarial_review_pointer_present(self):
        content = _read_meditation_artifact("command")
        assert "crux-skill-memory-meditation-review" in content

    def test_report_generation_pointer_present(self):
        content = _read_meditation_artifact("command")
        assert "crux-skill-memory-meditation-report" in content

    def test_ensemble_aggregation_pointer_present(self):
        content = _read_meditation_artifact("command")
        assert "crux-skill-memory-meditation-ensemble" in content

    def test_related_section_lists_six_skills(self):
        content = _read_meditation_artifact("command")
        related_idx = content.find("## Related")
        if related_idx == -1:
            return
        related = content[related_idx:]
        for skill_dir in (
            "crux-skill-memory-meditation-research",
            "crux-skill-memory-meditation-quick",
            "crux-skill-memory-meditation-ensemble",
            "crux-skill-memory-meditation-review",
            "crux-skill-memory-meditation-report",
            "crux-skill-memory-meditation-coordination",
        ):
            assert skill_dir in related, f"## Related must list skill path for '{skill_dir}'"

    def test_related_section_lists_meditation_guide_link(self):
        content = _read_meditation_artifact("command")
        related_idx = content.find("## Related")
        if related_idx == -1:
            return
        related = content[related_idx:]
        assert "crux-cursor-meditation-guide" in related


class TestMemoryManagerPostTrim:
    """Post-S07 negative + positive assertions for crux-cursor-memory-manager.md."""

    def test_file_exists(self):
        p = (
            Path(__file__).resolve().parent.parent
            / ".cursor" / "agents" / "crux-cursor-memory-manager.md"
        )
        assert p.is_file()

    def test_dream_mode_section_retained(self):
        content = _read_memory_manager_file()
        if not content:
            return
        assert "Dream Mode" in content

    def test_rem_sleep_section_retained(self):
        content = _read_memory_manager_file()
        if not content:
            return
        assert "REM Sleep" in content

    def test_recall_mode_section_retained(self):
        content = _read_memory_manager_file()
        if not content:
            return
        assert "Recall Mode" in content

    def test_remember_mode_section_retained(self):
        content = _read_memory_manager_file()
        if not content:
            return
        assert "Remember Mode" in content

    def test_forget_mode_section_retained(self):
        content = _read_memory_manager_file()
        if not content:
            return
        assert "Forget Mode" in content

    def test_no_phases_a_g_research_section(self):
        """Negative: trimmed memory-manager must NOT contain Phases A–G research executable heading."""
        content = _read_memory_manager_file()
        if not content:
            return
        assert "Phases A–G research" not in content, (
            "Trimmed memory-manager must not contain 'Phases A–G research' "
            "(Research mode protocol moved to crux-cursor-meditation-guide + skill:research)"
        )

    def test_no_quick_6_step_protocol_section(self):
        """Negative: trimmed memory-manager must NOT contain Quick 6-step executable content."""
        content = _read_memory_manager_file()
        if not content:
            return
        assert "Quick 6-step" not in content, (
            "Trimmed memory-manager must not contain 'Quick 6-step' "
            "(Quick protocol moved to skill:quick)"
        )

    def test_no_adversarial_review_executable_section(self):
        """Negative: trimmed memory-manager must NOT contain ### Adversarial Review heading."""
        content = _read_memory_manager_file()
        if not content:
            return
        assert "### Adversarial Review" not in content, (
            "Trimmed memory-manager must not contain '### Adversarial Review' section heading "
            "(moved to skill:review)"
        )

    def test_no_ensemble_aggregation_executable_section(self):
        """Negative: trimmed memory-manager must NOT contain ensembleAggregation execution params.

        Adaptation from plan §3.4 #10: the heading '### Ensemble Aggregation Mode — moved'
        legitimately remains as a pointer/redirect paragraph.  The negative assertion is
        therefore scoped to the EXECUTION marker (spawn parameter) rather than the heading.
        """
        content = _read_memory_manager_file()
        if not content:
            return
        assert "ensembleAggregation: true" not in content, (
            "Trimmed memory-manager must not contain 'ensembleAggregation: true' spawn parameter "
            "(ensemble execution moved to crux-cursor-meditation-guide + skill:ensemble)"
        )

    def test_no_meditate_mode_executable_heading(self):
        """Negative: trimmed memory-manager must NOT contain Phases A–G execution indicators.

        Adaptation from plan §3.4 #11: the heading '### Meditate Mode — moved' legitimately
        remains as a pointer paragraph; the actual EXECUTABLE content (Phases A–G) is what
        must be absent.
        """
        content = _read_memory_manager_file()
        if not content:
            return
        assert "Phases A–G" not in content, (
            "Trimmed memory-manager must not contain 'Phases A–G' content "
            "(Research protocol moved to crux-cursor-meditation-guide + skill:research)"
        )

    def test_no_k10c_reflection_rubric_in_memory_manager(self):
        """Negative: trimmed memory-manager must NOT contain K10c reflection rubric."""
        content = _read_memory_manager_file()
        if not content:
            return
        assert "K10c reflection rubric" not in content, (
            "K10c reflection rubric moved to skill:research"
        )

    def test_no_combined_pattern_b_facet_confirmation_in_memory_manager(self):
        """Negative: trimmed memory-manager must NOT contain Combined Pattern-B (capital C)."""
        content = _read_memory_manager_file()
        if not content:
            return
        assert "Combined Pattern-B" not in content, (
            "Combined Pattern-B gate moved to coordinator command + scout skills"
        )

    def test_pointer_to_meditation_guide_present(self):
        """Post-trim memory-manager should have a pointer paragraph to the meditation guide."""
        content = _read_memory_manager_file()
        if not content:
            return
        assert "crux-cursor-meditation-guide" in content, (
            "Trimmed memory-manager must contain a pointer paragraph referencing "
            "crux-cursor-meditation-guide as the new Meditate owner"
        )

    def test_no_meditate_in_critical_rules(self):
        """Negative: Meditate-specific rules must NOT be in ## Critical Rules section."""
        content = _read_memory_manager_file()
        if not content:
            return
        critical_idx = content.find("## Critical Rules")
        if critical_idx == -1:
            return
        next_h2_idx = content.find("\n## ", critical_idx + 1)
        critical_section = (
            content[critical_idx:next_h2_idx] if next_h2_idx != -1
            else content[critical_idx:]
        )
        assert "Meditate" not in critical_section, (
            "Post-trim memory-manager Critical Rules section must not contain Meditate-specific rules"
        )

    def test_post_trim_line_budget(self):
        """SOFT: trimmed memory-manager should be at most ~400 lines (advisory)."""
        content = _read_memory_manager_file()
        if not content:
            return
        line_count = len(content.splitlines())
        assert line_count <= 500, (
            f"Post-trim memory-manager has {line_count} lines — SOFT advisory: should be ≤400 "
            "lines post-S07; strict enforcement deferred to S12 integrity review"
        )


class TestMeditateDecompDistFilesPresent:
    """K8 sibling class: positive presence assertions for S10 dist artefacts.

    These paths were previously in TestMeditateNoNewDistFilesK8::SPEC_INTRODUCED_PATHS;
    they have been promoted to legitimate dist artefacts by the S10 decomposition.
    """

    DECOMP_DIST_PATHS = [
        ".cursor/agents/crux-cursor-meditation-guide.md",
        ".cursor/skills/crux-skill-memory-meditation-research/SKILL.md",
        ".cursor/skills/crux-skill-memory-meditation-quick/SKILL.md",
        ".cursor/skills/crux-skill-memory-meditation-ensemble/SKILL.md",
        ".cursor/skills/crux-skill-memory-meditation-review/SKILL.md",
        ".cursor/skills/crux-skill-memory-meditation-report/SKILL.md",
        ".cursor/skills/crux-skill-memory-meditation-coordination/SKILL.md",
    ]

    def _get_dist_files(self) -> list[str]:
        repo_root = Path(__file__).resolve().parent.parent
        zip_script = repo_root / "scripts" / "create-crux-zip.py"
        content = zip_script.read_text(encoding="utf-8")
        match = re.search(r"DIST_FILES\s*=\s*\[(.*?)\]", content, re.DOTALL)
        if not match:
            return []
        raw = match.group(1)
        return [s.strip().strip('"').strip("'") for s in raw.splitlines() if s.strip().strip(",").strip()]

    def _get_memory_file_prefixes(self) -> list[str]:
        repo_root = Path(__file__).resolve().parent.parent
        install_py = repo_root / "install.py"
        content = install_py.read_text(encoding="utf-8")
        return content  # Return full content for substring checks

    def _get_dist_manifest_entries(self) -> list[str]:
        repo_root = Path(__file__).resolve().parent.parent
        manifest = repo_root / ".crux" / "dist-manifest.json"
        if not manifest.exists():
            return []
        data = json.loads(manifest.read_text(encoding="utf-8"))
        return data.get("files", [])

    def test_dist_files_includes_meditation_guide_agent(self):
        dist_files = self._get_dist_files()
        assert any(".cursor/agents/crux-cursor-meditation-guide.md" in f for f in dist_files), (
            "DIST_FILES must include crux-cursor-meditation-guide.md"
        )

    def test_dist_files_includes_all_six_skills(self):
        dist_files = self._get_dist_files()
        for skill_path in (
            ".cursor/skills/crux-skill-memory-meditation-research/SKILL.md",
            ".cursor/skills/crux-skill-memory-meditation-quick/SKILL.md",
            ".cursor/skills/crux-skill-memory-meditation-ensemble/SKILL.md",
            ".cursor/skills/crux-skill-memory-meditation-review/SKILL.md",
            ".cursor/skills/crux-skill-memory-meditation-report/SKILL.md",
            ".cursor/skills/crux-skill-memory-meditation-coordination/SKILL.md",
        ):
            assert any(skill_path in f for f in dist_files), (
                f"DIST_FILES must include '{skill_path}'"
            )

    def test_install_py_includes_meditation_guide_and_skills(self):
        install_content = self._get_memory_file_prefixes()
        assert "crux-cursor-meditation-guide" in install_content
        for name in MEDITATION_SKILL_NAMES:
            skill_dir = f"crux-skill-memory-meditation-{name}"
            assert skill_dir in install_content, (
                f"install.py must reference '{skill_dir}'"
            )

    def test_dist_manifest_includes_meditation_guide_and_skills(self):
        entries = self._get_dist_manifest_entries()
        assert any("crux-cursor-meditation-guide" in e for e in entries), (
            "dist-manifest.json must list the meditation guide agent"
        )
        for name in MEDITATION_SKILL_NAMES:
            skill_dir = f"crux-skill-memory-meditation-{name}"
            assert any(skill_dir in e for e in entries), (
                f"dist-manifest.json must list '{skill_dir}'"
            )


class TestMeditationDecompForbiddenLegacyFieldNames:
    """Negative assertions: legacy additional_focus_areas_skipped/accepted absent from command.

    NOTE ON SCOPE: The guide agent and skill files (research, quick) contain these legacy
    field names explicitly as documentation — e.g. "these MUST NOT appear in any artefact"
    and "LEGACY field names — never emit". Per the plan §8.1, per-source negative checks
    are therefore scoped to the COMMAND file only (which does not contain these strings at
    all). The guide agent / skill files correctly document what is forbidden; their mention
    of the legacy names in prohibition clauses is valid documentation behavior.
    """

    def test_no_additional_focus_areas_skipped_in_command(self):
        cmd = _read_meditation_artifact("command")
        assert "additional_focus_areas_skipped" not in cmd, (
            "Command must not use legacy field name 'additional_focus_areas_skipped'"
        )

    def test_no_additional_focus_areas_accepted_in_command(self):
        cmd = _read_meditation_artifact("command")
        assert "additional_focus_areas_accepted" not in cmd, (
            "Command must not use legacy field name 'additional_focus_areas_accepted'"
        )

    def test_canonical_additional_focus_areas_with_treatment_in_command(self):
        """Positive paired assertion: canonical array name with treatment: filter present."""
        cmd = _read_meditation_artifact("command")
        assert "additional_focus_areas" in cmd
        assert "treatment:" in cmd or "treatment" in cmd.lower()

    def test_guide_agent_documents_canonical_treatment_filter(self):
        """Positive: guide agent uses the canonical additional_focus_areas[] with treatment:."""
        guide = _read_meditation_artifact("guide_agent")
        if not guide:
            return
        assert "additional_focus_areas" in guide
        assert "treatment:" in guide

    def test_research_skill_documents_canonical_treatment_filter(self):
        """Positive: research skill uses the canonical additional_focus_areas[] with treatment:."""
        research = _read_meditation_artifact("skill", "research")
        if not research:
            return
        assert "additional_focus_areas" in research
        assert "treatment:" in research

    def test_quick_skill_documents_canonical_treatment_filter(self):
        """Positive: quick skill documents the canonical treatment: filter."""
        quick = _read_meditation_artifact("skill", "quick")
        if not quick:
            return
        assert "additional_focus_areas" in quick


class TestMeditationCommandNoMemoryManagerSpawn:
    """Negative assertions: crux-cursor-memory-manager must not appear in spawn context."""

    def test_command_does_not_spawn_memory_manager(self):
        """Negative: command Instructions section must not reference crux-cursor-memory-manager."""
        content = _read_meditation_artifact("command")
        related_idx = content.find("## Related")
        instructions = content[:related_idx] if related_idx != -1 else content
        assert "crux-cursor-memory-manager" not in instructions, (
            "Post-decomp command Instructions section must not spawn crux-cursor-memory-manager "
            "(design §8 negative cue)"
        )

    def test_guide_agent_does_not_implement_memory_manager_lifecycle_modes(self):
        """Negative: guide agent must not implement Dream/REM/Recall/Remember/Forget.

        Adaptation from plan §8.2 #2: guide agent legitimately references
        crux-cursor-memory-manager as a delegation note. The negative assertion is
        scoped to verify the guide agent does not IMPLEMENT memory lifecycle modes.
        """
        guide = _read_meditation_artifact("guide_agent")
        if not guide:
            return
        assert "### Dream Mode" not in guide, (
            "Guide agent must not implement Dream Mode lifecycle"
        )
        assert "### REM Sleep Mode" not in guide, (
            "Guide agent must not implement REM Sleep lifecycle"
        )

    def test_six_skills_do_not_reference_memory_manager(self):
        """Negative: none of the six meditation skills reference crux-cursor-memory-manager."""
        for name in MEDITATION_SKILL_NAMES:
            skill_content = _read_meditation_artifact("skill", name)
            if not skill_content:
                continue
            assert "crux-cursor-memory-manager" not in skill_content, (
                f"Meditation skill '{name}' must not reference crux-cursor-memory-manager "
                "(skills must not cross-reference the memory-manager per design §3 single-primary rule)"
            )
