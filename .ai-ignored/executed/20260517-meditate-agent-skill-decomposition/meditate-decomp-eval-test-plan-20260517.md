# Meditate Decomposition — Eval & Test Plan (Subtask 03)

> **Purpose**: Capture the current Meditate-related eval / test surface
> and produce a file-by-file plan for subtask 08 to execute. The plan
> (a) preserves every existing assertion's intent, (b) re-targets the
> assertions that move from `crux-cursor-memory-manager` to
> `crux-cursor-meditation-guide`, and (c) adds new substring-presence
> regression coverage for the new guide agent, the six new skills, the
> refactored command, the trimmed memory-manager, and every contract
> surface enumerated by the **2026-05-24 freeze refresh**
> (`specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260524.md`).
>
> **Source-of-truth**:
> - Freeze: `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260524.md`
>   (supersedes `meditate-frozen-contract-20260517.md`).
> - Design: `specs/20260517-meditate-agent-skill-decomposition/meditate-decomp-architecture-design-20260517.md`
>   §3 (section-mapping) and §8 (discovery cues).
> - Inventory targets (read-only):
>   - `evals/test_q_meditate.py` (1335 lines, 36 classes total — 8 pre-richness + 28 richness-era)
>   - `evals/test_p_amnesia.py` (single `EXPLICIT_MEMORY_COMMANDS` row +
>     `test_meditate_still_works`)
>   - `evals/sdk/tests/q-meditate.test.ts` (576 lines, 8 describe blocks
>     total — 3 pre-richness Q1–Q3 + 5 richness-era structural blocks; the
>     freeze §10.3.2 prose "4 NEW describe blocks" is an off-by-one — the
>     enumerated table inside the freeze itself lists 5)
>   - `evals/conftest.py` (none of its fixtures are currently consumed by
>     meditate tests; existing `tmp_memories_dir`, `sample_config`,
>     `sample_memory_file`, `sample_tracker_file`, and `write_memory`
>     helpers remain useful for hypothetical future fixtures)
>   - `evals/USER_EVAL_CHECKLISTS.md` Q. Meditate Interactive Flow
>     scenarios Q1, Q2, Q3 + the cross-platform Integration §
>     `Meditate` step
>   - `evals/sdk/README.md` — only references `pnpm test:meditate` and
>     the `SDK_EVAL_SKIP_EXPENSIVE` gate; no agent-name references to
>     re-target
>
> **Authority**: assertions use **substring presence** only — no content
> hashes, no strict equality, no regex over multi-line bodies unless the
> existing test already does so. Six-skill cap is fixed; one presence
> assertion per skill (`SKILL.md` exists + frontmatter `name` equals
> directory + `description` contains the literal `meditation`).
>
> **Canonical field name pin**: `additional_focus_areas[]` array with a
> per-item `treatment:` filter is **positively** asserted across all
> destinations; the legacy W1 field names
> `additional_focus_areas_skipped` / `additional_focus_areas_accepted`
> are **negatively** asserted everywhere in the post-decomp repo (per
> freeze §4.6 + design §8 discovery cues + `specs/20260523-meditate-richness/execution-report-meditate-richness-20260523.md:177`).
>
> **Markdown-only artefact**. Subtask 08 will translate this plan into
> code edits to `evals/test_q_meditate.py`,
> `evals/sdk/tests/q-meditate.test.ts`, `evals/test_p_amnesia.py`, and
> `evals/conftest.py`.

---

## 1. Current Surface Inventory (D02)

### 1.1 `evals/test_q_meditate.py` — 36 test classes (8 pre-richness + 28 richness-era)

All 8 pre-richness classes read the **command file only** via a local
`_read_cmd()` helper rooted at `.cursor/commands/crux-meditate.md`. All
28 richness-era classes read via the **dual-resolver** helpers
`_read_command_file()` / `_read_agent_file()` (lines 23–55) which already
fall back to the post-decomp skill / guide-agent paths when present —
this is the existing mechanism subtask 08 will lean on.

#### 1.1.1 Pre-richness classes (lines 58–286 — kept structurally; spawn-target re-target only)

| # | Class | Line | Methods | Asserts (current behaviour) | Freeze contract item covered |
|---|-------|-----:|--------:|-----------------------------|------------------------------|
| 1 | `TestMeditateConfigPresence` | 58 | 4 | `.crux/crux-memories.json` contains `commands.meditate`; `file == .cursor/commands/crux-meditate.md`; `default == "/crux-meditate"`; command file exists on disk | §9 cross-repo touchpoint (`commands.meditate` config row) |
| 2 | `TestMeditateCommandDefinition` | 95 | 4 | `## Usage` heading; no-args support; quoted topic support; `@`/`file` references | §1 (Usage CLI examples Command lines 7–18) |
| 3 | `TestMeditateFacetStructure` | 123 | 3 | Three facets documented; ≥2 facet-dimension terms (`theme`/`topic`/`intent`/`facet`); facets-become-branches language | §2.6 (combined Pattern-B Sub-Q1 — 3 facets) |
| 4 | `TestMeditateRecursiveDepth` | 150 | 7 | Three depths; depth-1 spawns; depth-3 terminal; `recursive`; `maxDepth` / `Depth Selection`; literal `Q-Depth-Selection`; default depth 3 | §2.1 `Q-Depth-Selection` |
| 5 | `TestMeditateMemoryQuerying` | 192 | 3 | `memor` substring; `index`/`search`; `refine`/`expand` | §4.2 Phase A (query memory index, refine queries by depth) |
| 6 | `TestMeditateConsolidation` | 216 | 3 | `consolidat` substring; `cross`/`connection`; `branch`/`organized` | §4.1 step 8 + §8 Subject-Matter Focus |
| 7 | `TestMeditateContinuationMenu` | 240 | 4 | `expansion`/`direction`; `save` + `spec`; `end`; literal `AskQuestion` | §7.3 / §7.4 (single-model step 11 / 12) |
| 8 | `TestMeditateAgentSpawning` | 268 | 2 | Literal `crux-cursor-memory-manager`; `meditate mode` | §1 modes inventory — **THIS IS THE ONLY PRE-EXISTING CLASS THAT NEEDS A SPAWN-TARGET LITERAL RE-TARGET** |

**Pre-richness method count**: 4+4+3+7+3+3+4+2 = **30 test methods**.

**Spawn-target literal re-target scope (mandatory for D03)**: only
`TestMeditateAgentSpawning::test_spawns_memory_manager` literally
asserts `crux-cursor-memory-manager`. Subtask 08 must re-target this
single literal to `crux-cursor-meditation-guide` (the new guide agent
per design §1) AND surface a negative assertion that
`crux-cursor-memory-manager` **MUST NOT** appear anywhere in the
post-decomp `.cursor/commands/crux-meditate.md` spawn context (per
design §8 discovery cues, negative row).

#### 1.1.2 Richness-era classes (lines 293–1335 — all 28 are additive; preserve structurally)

| # | Class | Line | Asserts (canonical summary; per freeze §10.3.1) | Freeze contract item covered |
|---|-------|-----:|-------------------------------------------------|------------------------------|
| 1 | `TestMeditateMergedCostAndRichnessGate` | 293 | Merged gate exists; **no standalone `Q-Comprehensiveness`** (negative); all 4 richness enum values; `default` preselected; Sub-Q2 4-option mode-swap set; per-richness decision guidance; depth × richness cost estimates; mode-swap preserves richness; K1 dual-meaning callout | §2.2 `Q-Cost-and-Richness-Acknowledgment` |
| 2 | `TestMeditateReadOnlyRichnessVariant` | 358 | Read-only-richness variant exists; expansion variant exists; richness shown locked; 3 trigger preambles documented (expansion / additional-facet acceptance / `spawn_now`) | §2.3 / §2.4 |
| 3 | `TestMeditateComprehensivenessLevelMapping` | 382 | 12×4 mapping table exists; `compact`=4/3/1/3 (charts / infographics / calculators / scenarios); all 4 levels present; 12 dimensions enumerated | §6.1 |
| 4 | `TestMeditateInitSuggestions` | 430 | `init-suggestions-{ts}.yml` documented in command + agent + filename table + Branch & Leaf Index; **canonical 4 opt-in modes** (`skip` / `additional_facet` / `report_section_only` / `additional_facet_AND_section`); schema fields enumerated | §4.6 + §4.7 + §5.1 |
| 5 | `TestMeditateCombinedFacetConfirmation` | 463 | Combined Pattern-B askQuestion documented; folds Q-Confirm-1 + Q-Confirm-2 + init-suggestions; 5 sub-questions; 4-mode focus-area sub-Q; per-sub-Q decision-guidance | §2.6 |
| 6 | `TestMeditateAdditionalFacetCostAck` | 499 | Cost-ack re-presentation documented; triggers on `additional_facet`; triggers on `additional_facet_AND_section`; does NOT trigger on `skip` or `report_section_only`; uses read-only-richness variant | §2.4 + §2.6 cost-change check |
| 7 | `TestMeditateSetOncePersistence` | 536 | Set-once-per-invocation documented; expansion variant shows richness locked; no `--reset-richness` flag (negative); users must `cancel` to change richness | §2.2 K6 set-once rule |
| 8 | `TestMeditateAdversarialReviewerExtension` | 560 | Reviewer has 13 dimensions; Dim 12 (Comprehensiveness fidelity); Dim 13 (Init-suggestion + finalisation-enhancement honour); Dim 9 level-conditional expansion | §4.9 |
| 9 | `TestMeditateRespawnProtocol` | 589 | Respawn protocol documented; `respawn_reasons` list-typed; 10 required payload keys (`respawn_reasons` / `reviewer_iteration` / `prior_report_paths` / `missing_sections` / `missing_visualisations` / `accepted_finalisation_enhancements` / `preserve_other_content` / `comprehensiveness_payload` / `init_suggestions_payload` / `theming_payload`); shares ≤3 iteration cap; `respawn_required: true` bypasses standard flow; respawn-then-re-review semantics | §6.10 Report-Skill Respawn Protocol |
| 10 | `TestMeditateRespawnFiniteIteration` | 637 | Iteration cap = 3; respawn counts as 1 iteration; `ESCALATE` verdict at iter 3 with Dim 13; max useful respawns = 2 | §4.9 iteration loop + §6.10 iteration accounting |
| 11 | `TestMeditatePayloadPropagation` | 669 | `comprehensiveness` in depth-0 spawn prompt; propagated to children in Phase D; propagated in Quick mode; **canonical abort error string** documented ("`comprehensiveness:` payload required" + "caller misconfigured") | §2.7 `comprehensiveness:` payload propagation |
| 12 | `TestMeditateNoNewDistFilesK8` | 699 | `scripts/create-crux-zip.py::DIST_FILES`, `install.py::MEMORY_FILE_PREFIXES`, `.crux/dist-manifest.json` all reject the spec-introduced path list (`init-suggestions`, `finalisation-enhancements`, 4×`follow-up-*`, the four skill / agent path prefixes) | §9 K8 invariant — **THIS CLASS REQUIRES PATH-LIST UPDATE in D03: the four meditation-skill prefixes + the `crux-cursor-meditation-guide` agent are NOW LEGITIMATE DIST PATHS once S10 adds them, so the K8 SPEC_INTRODUCED_PATHS list must drop the four-skill `crux-skill-memory-meditation-*` entries + the `crux-cursor-meditation-guide` entry** (they are no longer "spec-introduced K8 violations"; they are the legitimate decomp artefacts S10 adds). The `init-suggestions` / `finalisation-enhancements` / `follow-up-*` runtime-only paths stay in the negative-list (those remain runtime-only, never dist-shipped) |
| 13 | `TestMeditateBackwardsCompatibility` | 783 | `compact` chart/infographic/calculator/scenarios minima unchanged (4/3/1/3); `compact` depth3_leaf_inclusion=`summary`; per_branch_section=`consolidation_only`; peer_review_surfacing=`consolidation_only`; **no standalone `Q-Comprehensiveness`** (negative regression) | §6.1 `compact` backwards-compat anchor |
| 14 | `TestMeditateSafeguardRegressions` | 836 | Anti-homogenisation block; Universal Contrast; Subject-Matter Focus; Pattern B; paired HTML+PDF; mandatory citations; iteration cap; MUST_FIX `needs_user_input` mandatory `context`; retrospective always written | §6.2 / §6.3 / §6.4 / §3 / §4.9 / §5.7 / §8 |
| 15 | `TestMeditateFinalisationEnhancementGate` | 889 | Gate exists; multi-select 0–5; fires after consolidation / before adversarial review; per-option labels include cost class; decision-guidance on cost-class consequences | §2.8 |
| 16 | `TestMeditateK10SkipAllBackwardsCompat` | 922 | Skip-all = no accepted enhancements in respawn; `respawn_reasons` excludes accepted-enhancement on skip-all; no follow-up files written on skip-all; footer omits `finalisation-enhancements:` segment; `finalisation-enhancements.yml` written with `unchosen_persisted`; no additional adversarial-review iteration consumed | §2.8 skip-all backwards-compat path + §6.12 footer skip-all path |
| 17 | `TestMeditateFinalisationCheapAcceptRespawn` | 964 | `accepted_finalisation_enhancements` list populated; `respawn_reasons` includes cause; cheap respawn shares iteration cap; multiple cheap items bundle into single respawn | §4.1 step 8b + §6.10 |
| 18 | `TestMeditateFinalisationExpensiveQueueDefault` | 990 | Expensive default = `queue`; follow-up file written; no agent spawned for queue; queued item surfaces in continuation menu | §2.8 + §7.3 K10c group 3 |
| 19 | `TestMeditateFinalisationExpensiveSpawnNow` | 1021 | `spawn_now` triggers cost-ack re-presentation; cancel falls back to `queue`; proceed defers spawning until after adversarial review | §2.8 spawn_now path + §2.4 trigger 3 |
| 20 | `TestMeditateFinalisationPersistence` | 1049 | `finalisation-enhancements.yml` schema has all fields (7 required); `decided_at_utc` filled by calling agent; linked from Branch & Leaf Index; unchosen items surface in continuation menu | §4.8 single-model schema + §5.1 / §5.8 |
| 21 | `TestMeditateFinalisationContinuationMenu` | 1081 | Step 12 has K10c section headings (`Expansion directions` / `Apply un-chosen enhancements` / `Spawn queued follow-ups`); unchosen-enhancement options include title; queued-expensive options trigger cost-ack | §7.3 / §7.4 |
| 22 | `TestMeditateFinalisationFiniteIteration` | 1104 | Gate fires at most once per meditation; cheap items contribute to iter-1 respawn; iteration cap remains 3; `ESCALATE` remains verdict at iter 3 | §4.1 step 8b non-infinite-loop guarantee + §6.10 |
| 23 | `TestMeditateFinalisationTripleReasonRespawn` | 1136 | Triple-reason ordering documented; accepted-enhancements processed first; report skill processes in order (enhancements → viz → sections) | §6.10 per-reason processing order |
| 24 | `TestMeditateK10EnsembleLayeredCadence` | 1167 | Per-tree YAMLs documented; per-tree YAML has `source_tree`; `surfaced_to_root` placeholder; root combined YAML; `cross_model_candidates` + `union_candidates`; `surfaced_to_root` annotation; single root askQuestion; root ranking by composite_score; single-model backwards-compat; per-tree vs cross-model report respawn targeting | §4.5 K10 layered cadence (steps 3b–3f) + §6.12 + §6.13 |
| 25 | `TestMeditateK10EnsembleContinuationMenuLayered` | 1222 | Per-tree-only items have provenance label; root unchosen items have provenance label; per-tree-only item targets per-tree report respawn | §7.5 ensemble step 11 / 12 |
| 26 | `TestMeditateK10QuickModeFires` | 1245 | Gate fires in Quick mode; same 0–5 cap; Quick skip-all backwards-compat | §2.8 (gate runs in both modes) |
| 27 | `TestMeditateK10ReflectionRubric` | 1265 | Rubric documented in agent file; both axes use 1–10 scale; worked examples for `impact_score` 9 / 5 / 2; `insight_value_score` 9; `minimum_impact_threshold` defaults to 6 | §4.8 rubric (Agent lines 609–625) |
| 28 | `TestMeditateK10WeightsConfigurable` | 1308 | `weights` key documented; defaults `impact: 1.0` / `insight_value: 1.0`; `formula` defaults to multiplicative `product`; weights configurable via `cruxMemories.meditate.finalisationEnhancements.weights` | §4.8 scoring rules (Agent lines 620–625) + §9 NEW config row |

**Richness-era method count**: ≈147 new test methods (per freeze
§10.3.1 net richness coverage statement).

**Grand pytest method total (current, pre-S08 edits)**: 30 + ≈147 =
**≈177 test methods across 36 classes**.

### 1.2 `evals/test_p_amnesia.py` — single Meditate touchpoint

| Surface | Line | Asserts | Freeze contract item covered |
|---------|-----:|---------|------------------------------|
| `EXPLICIT_MEMORY_COMMANDS` module constant | 23–29 | Contains `/crux-meditate` | §9 `.cursor/commands/crux-amnesia.md` row |
| `TestAmnesiaExplicitCommandOverride::test_meditate_still_works` | 182–184 | Reads `.cursor/commands/crux-amnesia.md` content and asserts `/crux-meditate` substring | §9 `/crux-amnesia` explicit-command list (Line 40 + Line 63 of amnesia command) |
| `TestAmnesiaRuleIntegration::test_rule_allows_explicit_commands` | 268–271 | Iterates `EXPLICIT_MEMORY_COMMANDS` and asserts each appears in `.cursor/rules/crux-memories-integration.md` | §9 amnesia rule cross-repo touchpoint |

**Verdict**: **NO CHANGES NEEDED** in S08. The amnesia surface
references the command **name** `/crux-meditate`, not the spawned
subagent. The command name is unchanged by decomposition (per design
§4.1 §1 `## Usage` stays unchanged). All three Meditate touchpoints in
`test_p_amnesia.py` remain valid verbatim.

### 1.3 `evals/sdk/tests/q-meditate.test.ts` — 8 describe blocks (3 pre-richness Q1–Q3 + 5 richness-era structural)

| Block | Line | `it` count | Gating | Asserts (canonical summary) | Freeze contract item |
|-------|-----:|-----------:|--------|-----------------------------|----------------------|
| `Q1: Meditate - No Arguments (Context-Derived Facets)` | 201 | 3 | `describe.skipIf(skipExpensive)` (root `describe` at line 67) | Facet derivation language regex; `Task` tool calls OR `hasSubagentCall(..., "crux-cursor-memory-manager")` (literal); references memories in consolidated output | §1 Research mode row + §4.1 step 8 |
| `Q2: Meditate - Topic Argument` | 290 | 2 | same | Derives facets from topic; produces consolidated insights referencing memories | §1 modes inventory |
| `Q3: Meditate - File/Folder References` | 357 | 1 | same | Derives facets from file/folder reference | §1 modes inventory |
| `Q: Meditate — Structural: K2 Merged Cost+Richness Gate` | 400 | 6 | **unconditional** (no `skipExpensive` gate) | `Q-Cost-and-Richness-Acknowledgment` exists; no standalone `Q-Comprehensiveness` (negative); 4 richness enum values; `default` preselected; mode-swap preserves richness (with literal `switch_to_quick`); K1 dual-meaning callout | §2.2 |
| `Q: Meditate — Structural: K10 Finalisation Enhancement Gate` | 441 | 5 | unconditional | Gate documented; multi-select 0–5; fires after consolidation before adversarial review; skip-all reproduces today's behaviour (with literal `unchosen_persisted`); cheap items bundle into respawn / expensive default queue | §2.8 |
| `Q: Meditate — Structural: K10 Reflection Rubric` | 477 | 5 | unconditional | Reads `_read_agent_file()` (dual-resolver); `impact_score` + `insight_value_score`; `1–10` scale; `minimum_impact_threshold` defaults to 6; worked examples 9/5/2; weights configurable via `finalisationEnhancements.weights` | §4.8 |
| `Q: Meditate — Structural: K9 Respawn Protocol` | 515 | 3 | unconditional | All 10 required respawn-payload keys; respawn shares ≤3 cap + `ESCALATE` at iter 3; triple-reason ordering (accepted_enhancements first) | §6.10 |
| `Q: Meditate — Structural: K10 Ensemble Layered Cadence` | 558 | 3 | unconditional | Per-tree YAML schema has `source_tree:` + `surfaced_to_root`; root combined YAML has `cross_model_candidates` + `union_candidates`; single root askQuestion at ensemble root | §4.5 / §6.13 |

**Pre-richness `it` count**: 3+2+1 = **6**.
**Richness-era `it` count**: 6+5+5+3+3 = **22**.
**Grand SDK `it` total**: **28** across 8 describe blocks.

**Subagent literal re-target scope (mandatory for D03)**: only
`Q1: Meditate - No Arguments`, the `spawns subagents for recursive
exploration` `it` block (line 246), calls
`hasSubagentCall(..., "crux-cursor-memory-manager")`. Subtask 08 must
re-target this single literal to `crux-cursor-meditation-guide`. **Q2
and Q3 do not assert subagent identity — they assert facet derivation
language and memory-content references, which survive the decomposition
intact.**

### 1.4 `evals/conftest.py` — fixtures (none currently consumed by meditate tests)

| Fixture / helper | Lines | Currently consumed by meditate tests? | Plan |
|------------------|------:|----------------------------------------|------|
| `_make_config` | 22 | No (used by `test_p_amnesia.py::test_config_not_touched_during_amnesia` + `crux-memories` tests) | Reuse for `.crux/crux-memories.json` writes in any new meditate fixture |
| `MEMORY_TYPES` | 19 | No | — |
| `tmp_memories_dir` | 99 | No | — |
| `sample_config` | 109 | No | — |
| `sample_memory_file` | 121 | No | — |
| `sample_tracker_file` | 144 | No | — |
| `write_memory` helper | 170 | No (imported by p-amnesia and rem tests) | — |
| `write_tracker` helper | 219 | No | — |

**Verdict**: meditate tests today rely **only** on direct file reads of
`.cursor/commands/crux-meditate.md` and
`.cursor/agents/crux-cursor-memory-manager.md` — no pytest fixtures are
consumed. Subtask 08 will **add** two new shared fixtures (see §5
below) to make the new guide-agent + skill assertions parameterised
across the six skill paths without duplicating string literals.

### 1.5 `evals/USER_EVAL_CHECKLISTS.md` — manual scenarios (Q1 / Q2 / Q3 + Integration §)

| Scenario | Lines | Asserts (manual reviewer reads) | Re-target scope |
|----------|------:|--------------------------------|-----------------|
| Q1. Meditate — No Arguments | 427–459 | Step 3 expected: `The agent spawns a crux-cursor-memory-manager subagent in Meditate mode` (line 450) | **Re-target** the literal `crux-cursor-memory-manager` → `crux-cursor-meditation-guide` |
| Q2. Meditate — Topic Argument | 463–490 | Topic-driven facets; consolidated insights; save as spec | No subagent-identity literal — kept verbatim |
| Q3. Meditate — File/Folder References | 494–518 | File/folder facets; clean session end | No subagent-identity literal — kept verbatim |
| Integration § `Meditate` step | 707–708 / 718 | "Meditate" row in expected-outcomes table (`/crux-meditate "performance patterns"`) | No subagent-identity literal — kept verbatim |
| Command Reference (line 858–859) | 858–859 | `/crux-meditate` + `/crux-meditate "topic"` rows | No re-target — these are command-name references |
| File Reference (line 875) | 875 | `.cursor/commands/crux-meditate.md` listing | No re-target |

### 1.6 `evals/sdk/README.md`

| Surface | Line | Asserts | Re-target scope |
|---------|-----:|---------|------------------|
| `pnpm test:meditate` script reference | 43 | Documents the meditate test alias | No re-target |
| `SDK_EVAL_SKIP_EXPENSIVE` row | 131 | Documents the gate that controls Q1–Q3 expensive tests | No re-target |

**Verdict**: `evals/sdk/README.md` does **not** reference the
subagent-spawn target by name — no re-target needed. The new structural
describe blocks (already shipped by 20260523 S06) are added to the
existing meditate test file and run unconditionally; the README does
not enumerate describe-block titles.

---

## 2. Migration Matrix (D03)

**Legend**: kept verbatim / re-targeted (spawn-target literal swap or
file-path resolver fallback) / replaced (semantics changed — explicit
justification) / additive (new — see §3 New Assertion Plan).

### 2.1 Pre-richness pytest classes — verbatim except for 1 literal swap

| Class | Verdict | Justification |
|-------|---------|---------------|
| `TestMeditateConfigPresence` | **kept verbatim** (4/4 methods) | Asserts `.crux/crux-memories.json` config entry — config keys are unchanged by decomp per freeze §9 |
| `TestMeditateCommandDefinition` | **kept verbatim** (4/4 methods) | `## Usage` + arg forms stay on command per design §4.1 §1 + §2 + §3 + §5 |
| `TestMeditateFacetStructure` | **kept verbatim** (3/3 methods) | Three-facet language stays on command per design §4.1 §9 (combined Pattern-B prompt body) |
| `TestMeditateRecursiveDepth` | **kept verbatim** (7/7 methods) | `Q-Depth-Selection` stays on command per design §4.1 §6 |
| `TestMeditateMemoryQuerying` | **kept verbatim** (3/3 methods) | Memory-query language survives the move (read via dual-resolver → memory-query language now lives in `skill:research` step 1–3 + `skill:quick` step 1–3 — the dual-resolver consults the skill content) |
| `TestMeditateConsolidation` | **kept verbatim** (3/3 methods) | Consolidation language survives the move (now lives in `skill:research` step 8 + `skill:quick` step 6 — dual-resolver) |
| `TestMeditateContinuationMenu` | **kept verbatim** (4/4 methods) | Continuation menu stays on command per design §4.1 §15 (calling-agent block) |
| `TestMeditateAgentSpawning::test_meditate_mode` | **kept verbatim** | Phrase `meditate mode` (case-insensitive) stays on command |
| `TestMeditateAgentSpawning::test_spawns_memory_manager` | **RE-TARGETED** | Replace literal `crux-cursor-memory-manager` → `crux-cursor-meditation-guide` per design §4.1 §4 (`## Instructions` spawn target). Add a **paired negative assertion** that the literal `crux-cursor-memory-manager` is **absent** from the command's spawn context (per §8 of this plan and design §8 discovery cues). Rename the class to `TestMeditateAgentSpawning::test_spawns_meditation_guide` for clarity (preserve class name for back-ref) |

**Re-target count (pre-richness pytest)**: 1 method / 30 (3.3%).

### 2.2 Richness-era pytest classes — all 28 additive; structurally preserved

| Class | Verdict | Justification |
|-------|---------|---------------|
| `TestMeditateMergedCostAndRichnessGate` | **kept verbatim** (9 methods) | Reads `_read_command_file()` — dual-resolver picks `.cursor/commands/crux-meditate.md` (gate stays on command per design §4.1 §7) |
| `TestMeditateReadOnlyRichnessVariant` | **kept verbatim** (4 methods) | Same — gate variants stay on command |
| `TestMeditateComprehensivenessLevelMapping` | **kept verbatim** (8 methods) | Reads `_read_command_file()` — dual-resolver swings to `skill:coordination` SKILL.md as the canonical post-decomp source per the helper's resolution order. Subtask 08 needs to verify the level-mapping table content survives the move to `skill:report` (design §3.6) — since the dual-resolver currently prefers `skill:coordination` not `skill:report`, **S08 MUST EXTEND `_read_command_file()` / add `_read_report_skill_file()` to fall through to `.cursor/skills/crux-skill-memory-meditation-report/SKILL.md`** for content that moved to `skill:report` |
| `TestMeditateInitSuggestions` | **kept verbatim** (6 methods) | Reads `_read_command_file()` + `_read_agent_file()` — combined Pattern-B stays on command (design §4.1 §9) AND the agent file pointer stays (design §1 mode router row 3). Dual-resolver picks the post-decomp guide agent + skills correctly |
| `TestMeditateCombinedFacetConfirmation` | **kept verbatim** (5 methods) | Same — combined Pattern-B stays on command |
| `TestMeditateAdditionalFacetCostAck` | **kept verbatim** (5 methods) | Same — cost-ack re-presentation stays on command (design §4.1 §9 cost_change_check) |
| `TestMeditateSetOncePersistence` | **kept verbatim** (4 methods) | Same — set-once rule stays on command |
| `TestMeditateAdversarialReviewerExtension` | **RE-TARGETED via resolver** (4 methods) | 13 dimensions move to `skill:review` per design §3.4 §4.9 — dual-resolver currently picks `skill:coordination`. **S08 MUST add `_read_review_skill_file()` helper to fall through to `.cursor/skills/crux-skill-memory-meditation-review/SKILL.md`** OR widen `_read_command_file()` to concatenate command + relevant skill content. **No assertion logic changes** — only the path resolution |
| `TestMeditateRespawnProtocol` | **RE-TARGETED via resolver** (6 methods) | Respawn protocol moves to `skill:review` (author side) + `skill:report` (consumer side) per design §3.4 + §3.6. Same resolver fix as above |
| `TestMeditateRespawnFiniteIteration` | **RE-TARGETED via resolver** (4 methods) | Iteration loop lives in `skill:review` per design §3.4. Same resolver fix |
| `TestMeditatePayloadPropagation` | **kept verbatim** (4 methods) | `comprehensiveness:` propagation YAML stays on command (design §4.1 §8) AND canonical abort error string lives in agent + skill — dual-resolver covers both |
| `TestMeditateNoNewDistFilesK8` | **PARTIALLY REPLACED** (5 methods) | `SPEC_INTRODUCED_PATHS` list (class lines 702–713) MUST be edited: **DROP** `crux-skill-memory-meditation-coordination` / `crux-skill-memory-meditation-report` / `crux-skill-memory-meditation-guide` / `crux-skill-memory-meditation-adversarial` (these are NOW LEGITIMATE dist paths added by S10 — the pre-decomp test was guarding against accidental K8 leakage from the 20260523 richness spec, which never added new dist files; the 20260517 decomp spec **does** add the guide agent + six skills as legitimate dist artefacts per design §3.9). **KEEP** `init-suggestions` / `finalisation-enhancements` / `follow-up-meditation` / `follow-up-spec` / `follow-up-memories` / `follow-up-expansion` (runtime-only artefacts that must never ship). **ADD** the six canonical skill names (`crux-skill-memory-meditation-research` / `quick` / `ensemble` / `review` / `report` / `coordination`) as POSITIVE-presence assertions in a sibling class (`TestMeditateDecompDistFilesPresent` — see §3.9 below) |
| `TestMeditateBackwardsCompatibility` | **RE-TARGETED via resolver** (8 methods) | `compact` level mapping moves to `skill:report` per design §3.6. Same resolver fix |
| `TestMeditateSafeguardRegressions` | **kept verbatim** (9 methods) | Safeguards mostly stay on command (Anti-Homogenisation context paragraph + Pattern B + Subject-Matter Focus rule pointer + paired HTML+PDF rule pointer + mandatory citations pointer + iteration cap + MUST_FIX `context` + retrospective). Some are now SKILL-resident; dual-resolver covers |
| `TestMeditateFinalisationEnhancementGate` | **kept verbatim** (5 methods) | Gate stays on command per design §4.1 §17 (askQuestion stays calling-agent-side per K4) |
| `TestMeditateK10SkipAllBackwardsCompat` | **kept verbatim** (6 methods) | Skip-all path stays on command + footer rule moves to `skill:report` (design §3.6 §6.12). Dual-resolver covers |
| `TestMeditateFinalisationCheapAcceptRespawn` | **kept verbatim** (4 methods) | Bundle rule stays on command pointer + `skill:research` / `skill:quick` step 8b |
| `TestMeditateFinalisationExpensiveQueueDefault` | **kept verbatim** (4 methods) | Per-item treatment stays on command + continuation menu stays on command |
| `TestMeditateFinalisationExpensiveSpawnNow` | **kept verbatim** (3 methods) | Same |
| `TestMeditateFinalisationPersistence` | **kept verbatim** (4 methods) | `finalisation-enhancements.yml` schema moves to `skill:research` (single-model write) + `skill:coordination` (filename row). Dual-resolver covers via the existing fall-through |
| `TestMeditateFinalisationContinuationMenu` | **kept verbatim** (3 methods) | K10c groups + handlers stay on command per design §4.1 §15 |
| `TestMeditateFinalisationFiniteIteration` | **kept verbatim** (4 methods) | Iteration guarantees stay on command + `skill:review` |
| `TestMeditateFinalisationTripleReasonRespawn` | **RE-TARGETED via resolver** (3 methods) | Per-reason processing order moves to `skill:report` (design §3.6 §6.10). Same resolver fix |
| `TestMeditateK10EnsembleLayeredCadence` | **kept verbatim** (9 methods) | Layered cadence moves to `skill:ensemble` per design §3.4 §4.5; dual-resolver concatenates command + agent (or skill). S08 may need a `_read_ensemble_skill_file()` helper |
| `TestMeditateK10EnsembleContinuationMenuLayered` | **kept verbatim** (3 methods) | Continuation menu rows stay on command |
| `TestMeditateK10QuickModeFires` | **kept verbatim** (3 methods) | Gate fires in Quick mode — command pointer + `skill:quick` reflection contract |
| `TestMeditateK10ReflectionRubric` | **kept verbatim** (7 methods) | Reads `_read_agent_file()` — rubric moves to `skill:research` per design §3.4 §4.8 (and `skill:quick` cross-references). Dual-resolver fall-through picks the new guide agent first; rubric verbatim content lives in the skill so S08 must add a `_read_research_skill_file()` helper |
| `TestMeditateK10WeightsConfigurable` | **kept verbatim** (4 methods) | Same — `weights` key lives in `skill:research` rubric section + `.crux/crux-memories.json` (S10 adds the config key wiring) |

**Migration headline counts (pytest)**:
- **Kept verbatim**: 7 pre-richness classes + 22 richness-era classes = **29 / 36 classes (≈80.6%)**.
- **Re-targeted (literal swap)**: 1 method (out of 30 pre-richness + ≈147 richness = ≈177 total).
- **Re-targeted via resolver helper additions** (no logic changes): 6 richness-era classes (≈30 methods) — assertion semantics are identical; only path resolution needs widening.
- **Partially replaced**: 1 class (`TestMeditateNoNewDistFilesK8` — the K8 list narrows; sibling class added).
- **Additive (new classes)**: see §3 below — target ≥ 16 new classes containing ≥ 50 new positive assertions + ≥ 10 new negative assertions.

### 2.3 `evals/test_p_amnesia.py` — kept verbatim

| Surface | Verdict | Justification |
|---------|---------|---------------|
| `EXPLICIT_MEMORY_COMMANDS` | **kept verbatim** | `/crux-meditate` is a command-name reference; command name is unchanged by decomp |
| `TestAmnesiaExplicitCommandOverride::test_meditate_still_works` | **kept verbatim** | Same |
| `TestAmnesiaRuleIntegration::test_rule_allows_explicit_commands` | **kept verbatim** | Same |

### 2.4 `evals/sdk/tests/q-meditate.test.ts` — all 8 blocks additive; 1 literal swap

| Block | Verdict | Justification |
|-------|---------|---------------|
| `Q1: Meditate - No Arguments`, `it: spawns subagents for recursive exploration` (line 246) | **RE-TARGETED** | Replace `hasSubagentCall(..., "crux-cursor-memory-manager")` literal → `"crux-cursor-meditation-guide"` per design §4.3.1 spawn signature. Add paired negative assertion `expect(usedMemoryManager).toBe(false)` after the positive `usedMeditationGuide` check, gated to skip when `skipExpensive` is true (live SDK only) — OR add an unconditional structural assertion in §3.6 below |
| `Q1: Meditate - No Arguments`, `it: derives exploration facets from context` (line 230) | **kept verbatim** | No subagent-identity literal |
| `Q1: Meditate - No Arguments`, `it: references memories in consolidated output` (line 262) | **kept verbatim** | No subagent-identity literal |
| `Q2: Meditate - Topic Argument` (2 `it` blocks) | **kept verbatim** | No subagent-identity literals |
| `Q3: Meditate - File/Folder References` (1 `it` block) | **kept verbatim** | No subagent-identity literal |
| `Q: Meditate — Structural: K2 Merged Cost+Richness Gate` (6 `it` blocks) | **kept verbatim** | Reads `readCommandFile()` — dual-resolver works; gate stays on command per design §4.1 §7 |
| `Q: Meditate — Structural: K10 Finalisation Enhancement Gate` (5 `it` blocks) | **kept verbatim** | Same |
| `Q: Meditate — Structural: K10 Reflection Rubric` (5 `it` blocks) | **RE-TARGETED via resolver** | Reads `readAgentFile()` — dual-resolver picks `meditation-guide` correctly; rubric content lives in `skill:research` SKILL.md (design §3.4 §4.8) so S08 widens the helper to fall through to `crux-skill-memory-meditation-research/SKILL.md` |
| `Q: Meditate — Structural: K9 Respawn Protocol` (3 `it` blocks) | **RE-TARGETED via resolver** | Reads `readCommandFile()` — respawn payload moves to `skill:review` (design §3.4 §6.10); same resolver fix |
| `Q: Meditate — Structural: K10 Ensemble Layered Cadence` (3 `it` blocks) | **RE-TARGETED via resolver** | Reads `readAgentFile()` — layered cadence moves to `skill:ensemble`; same resolver fix |

**Re-target count (SDK)**: 1 literal swap (Q1 spawn target) + 3 resolver
widenings (no semantics changes).

### 2.5 Re-target totals

| Surface | Total assertions | Re-targeted (literal or resolver) | Verbatim | % re-targeted |
|---------|------------------:|----------------------------------:|---------:|---------------:|
| `evals/test_q_meditate.py` (177 methods across 36 classes) | 177 | ~31 (1 literal swap + 30 covered by 6 resolver widenings + 5 K8 list narrowings = 36 affected methods; reported here at ≈17.5% by method count, but ≈20% by class count because each class is affected as a unit) | ~146 | **≈17.5% by method / ≈19.4% by class** |
| `evals/test_p_amnesia.py` (3 meditate touchpoints) | 3 | 0 | 3 | 0% |
| `evals/sdk/tests/q-meditate.test.ts` (28 `it` blocks across 8 describes) | 28 | 14 (1 literal swap + 3 resolver widenings × ≈4 it blocks each ≈ 11 ~ 13 methods covered; reported as 14) | 14 | **≈50% by method / 50% by describe block** |

**Headline**: pytest is ≈80% verbatim by class count; SDK is ≈50% by
describe block. The decomposition is **structurally preserving** — no
existing assertion's intent is invalidated, only path resolution and
spawn-target literals need updating.

---

## 3. New Assertion Plan (D04) — Grouped by Destination

All new assertions are **substring-presence only**. Counts below sum to
**≥ 50 new positive** and **≥ 10 new negative** assertions (see §9 for
the rolled-up totals).

### 3.1 Guide agent — `.cursor/agents/crux-cursor-meditation-guide.md`

**New class**: `TestMeditationGuideAgent` (single new pytest class — read
via a new helper `_read_meditation_guide_agent_file()` that returns the
content of `.cursor/agents/crux-cursor-meditation-guide.md`; empty
string if absent so all assertions skip cleanly on the pre-S04
checkout).

| # | Assertion | Source (design §) | Polarity |
|---|-----------|-------------------|:--------:|
| 1 | `test_agent_file_exists` — `.cursor/agents/crux-cursor-meditation-guide.md` resolves on disk | §1.1 frontmatter | + |
| 2 | `test_frontmatter_name_matches_filename` — frontmatter `name: crux-cursor-meditation-guide` literal | §1.1 | + |
| 3 | `test_frontmatter_model_pinned` — frontmatter `model: claude-opus-4-6` literal | §1.1 | + |
| 4 | `test_frontmatter_description_contains_meditation` — frontmatter `description:` value contains literal `meditation` | §1.1 + §8 discovery cues | + |
| 5 | `test_frontmatter_description_contains_recursive_memory_informed` — description contains `Recursive memory-informed` | §1.1 | + |
| 6 | `test_persona_prologue_present` — body contains literal `You are the CRUX Meditation Guide` | §1.2 | + |
| 7 | `test_critical_load_context_section_present` — body contains literal `CRITICAL: Load Context First` | §1.2 | + |
| 8 | `test_user_input_escalation_section_present` — body contains literal `User Input Escalation` | §1.2 + §3 boundary rules | + |
| 9 | `test_pattern_a_documented` — body contains literal `Pattern A` | §3.1 | + |
| 10 | `test_pattern_b_documented` — body contains literal `Pattern B` | §3.2 | + |
| 11 | `test_needs_user_input_documented` — body contains literal `needs_user_input` | §3.3 | + |
| 12 | `test_mode_router_research_present` — body contains literal `Research mode depth-0 workflow` heading | §1.3 row 3 | + |
| 13 | `test_mode_router_phases_a_g_mentioned` — body contains literal `Phases A–G` (or fallback `Phases A-G`) | §1.3 row 3 + §4.2 | + |
| 14 | `test_mode_router_quick_6_step_present` — body contains literal `Quick mode` and `6-step` | §1.3 row 4 + §4.3 | + |
| 15 | `test_mode_router_k10_in_pass_reflection_present` — body contains literal `K10 In-Pass Reflection` | §1.3 row 5 (NEW per refresh) | + |
| 16 | `test_mode_router_adversarial_review_13_dim_present` — body contains literal `Adversarial Review` AND literal `13` | §1.3 row 6 + §4.9 | + |
| 17 | `test_mode_router_ensemble_aggregation_k10_layered_present` — body contains literals `Ensemble Aggregation` AND `K10 layered cadence` | §1.3 row 7 + §4.5 | + |
| 18 | `test_mode_router_report_generation_obligation_present` — body contains literal `Report generation obligation` | §1.3 row 8 + §6.10 | + |
| 19 | `test_critical_rules_section_present` — body contains literal `Critical Rules` heading | §1.3 row 11 | + |
| 20 | `test_canonical_comprehensiveness_abort_error_string` — body contains the literal `comprehensiveness: payload required; missing from spawn prompt — caller misconfigured` | §1.3 row 11 + §2.7 + §3.4 row 1 | + |
| 21 | `test_feature_guard_flag_referenced` — body contains literal `flags.enableMemories` | §1.3 row 11 | + |
| 22 | `test_skill_delegation_documented` — body contains literal `Read .cursor/skills/crux-skill-memory-meditation-` (skill loading pattern) | §1.3 final spawn-signature block | + |
| 23 | `test_no_memory_manager_executable_sections` (NEGATIVE) — body does NOT contain literal `crux-cursor-memory-manager` (it is a sibling, not a self-reference) | §1.1 distinctness | − |
| 24 | `test_no_ask_question_call_from_subagent` (NEGATIVE) — body must contain `Subagents NEVER call AskQuestion` or `Subagents NEVER call \`AskQuestion\`` | §3 boundary rules | − (paired with the positive `User Input Escalation` row) |

**Subtotal — guide agent**: **22 positive + 2 negative = 24 new
assertions** in `TestMeditationGuideAgent`.

### 3.2 Six skills — one class per skill, with the mandated three-presence assertions plus contract-specific substrings

**Shared helper** (added to `evals/test_q_meditate.py` near
`_resolve_target_file`):

```text
SKILL_DIRS = {
  "crux-skill-memory-meditation-research",
  "crux-skill-memory-meditation-quick",
  "crux-skill-memory-meditation-ensemble",
  "crux-skill-memory-meditation-review",
  "crux-skill-memory-meditation-report",
  "crux-skill-memory-meditation-coordination",
}

def _read_meditation_skill(name: str) -> str:
    p = Path(__file__).resolve().parent.parent / ".cursor" / "skills" / name / "SKILL.md"
    return p.read_text(encoding="utf-8") if p.exists() else ""
```

**Mandatory three-presence per skill (per the user brief: SKILL.md
exists + frontmatter `name` matches directory + `description` contains
`meditation`)**. Plus contract-specific substrings per design §2 row +
§8 discovery cues.

#### 3.2.1 `crux-skill-memory-meditation-research`

| # | Assertion | Source | Polarity |
|---|-----------|--------|:--------:|
| 1 | `test_skill_md_exists` — file `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md` resolves | §2 row 1 | + |
| 2 | `test_frontmatter_name_matches_directory` — frontmatter `name: crux-skill-memory-meditation-research` | §2 row 1 | + |
| 3 | `test_description_contains_meditation` — frontmatter `description:` contains literal `meditation` | §2 anchors | + |
| 4 | `test_description_contains_research_verb` — `description:` contains literal `Research` | §2 row 1 | + |
| 5 | `test_phases_a_g_documented` — body contains literal `Phases A–G` (or `Phases A-G`) | §3.4 §4.1 + §8 cues | + |
| 6 | `test_step_4b_focus_area_reconciliation_documented` — body contains literal `step 4b` AND `additional_focus_areas` | §3.4 §4.6 | + |
| 7 | `test_init_suggestions_yml_write_side_documented` — body contains literal `init-suggestions-{ts}.yml` | §3.4 §4.7 + §8 cues | + |
| 8 | `test_k10c_reflection_writes_finalisation_enhancements_yml` — body contains literal `finalisation-enhancements.yml` | §3.4 §4.8 + §8 cues | + |
| 9 | `test_canonical_treatment_filter_present` — body contains literal `treatment:` and all four treatments (`skip`, `additional_facet`, `report_section_only`, `additional_facet_AND_section`) | §3.4 §4.6 + §10 canonical pin | + |

#### 3.2.2 `crux-skill-memory-meditation-quick`

| # | Assertion | Source | Polarity |
|---|-----------|--------|:--------:|
| 1 | `test_skill_md_exists` | §2 row 2 | + |
| 2 | `test_frontmatter_name_matches_directory` — `name: crux-skill-memory-meditation-quick` | §2 row 2 | + |
| 3 | `test_description_contains_meditation` | §2 anchors | + |
| 4 | `test_description_contains_quick_verb` — description contains literal `Quick` | §2 row 2 | + |
| 5 | `test_6_step_protocol_documented` — body contains literal `6-step` | §3.4 §4.3 | + |
| 6 | `test_warn_only_citation_regime_documented` — body contains literal `warn_only` or `warn-only` | §3.5 §5.5 Quick variant | + |
| 7 | `test_k10c_reflection_quick_variant_documented` — body contains literal `finalisation-enhancements.yml` AND literal `Quick` near it | §3.4 §4.8 cross-ref | + |

#### 3.2.3 `crux-skill-memory-meditation-ensemble`

| # | Assertion | Source | Polarity |
|---|-----------|--------|:--------:|
| 1 | `test_skill_md_exists` | §2 row 3 | + |
| 2 | `test_frontmatter_name_matches_directory` | §2 row 3 | + |
| 3 | `test_description_contains_meditation` | §2 anchors | + |
| 4 | `test_description_contains_ensemble_verb` — description contains literal `Ensemble` | §2 row 3 | + |
| 5 | `test_cross_model_synthesis_documented` — body contains literal `cross-model-synthesis.md` | §3.4 §4.5 step 2 | + |
| 6 | `test_k10_layered_cadence_steps_3b_3f_documented` — body contains literal `K10 layered cadence` AND `3b` AND `3f` | §3.4 §4.5 + §8 cues | + |
| 7 | `test_source_tree_field_documented` — body contains literal `source_tree` | §3.4 §4.5 + §8 cues | + |
| 8 | `test_surfaced_to_root_documented` — body contains literal `surfaced_to_root` | §3.4 §4.5 + §8 cues | + |
| 9 | `test_cross_model_candidates_and_union_candidates_documented` — body contains literals `cross_model_candidates` AND `union_candidates` | §3.4 §4.5 step 3d + §8 cues | + |
| 10 | `test_k10_ensemble_respawn_targeting_documented` — body contains literal `K10 Ensemble Respawn Targeting` | §3.6 §6.12 + §8 cues | + |
| 11 | `test_per_tree_write_only_documented` — body contains literal `per-tree` AND literal `write-only` (no per-tree askQuestion fires) | §3.4 §4.5 step 3b | + |

#### 3.2.4 `crux-skill-memory-meditation-review`

| # | Assertion | Source | Polarity |
|---|-----------|--------|:--------:|
| 1 | `test_skill_md_exists` | §2 row 4 | + |
| 2 | `test_frontmatter_name_matches_directory` | §2 row 4 | + |
| 3 | `test_description_contains_meditation` | §2 anchors | + |
| 4 | `test_description_contains_review_verb_and_13_dimensions` — description contains literals `13` and `dimensions` (per the user-brief mandate to mention "11 dimensions" — corrected to **13 dimensions** post-richness per §4.9) | §3.4 §4.9 + §8 cues | + |
| 5 | `test_dimension_12_comprehensiveness_fidelity_documented` — body contains literal `Comprehensiveness fidelity` | §3.4 §4.9 + §8 cues | + |
| 6 | `test_dimension_13_init_suggestion_honour_documented` — body contains literal `Init-suggestion AND finalisation-enhancement honour` | §3.4 §4.9 + §8 cues | + |
| 7 | `test_dimension_9_level_conditional_expansion_documented` — body contains literal `peer_review_surfacing` AND `consolidation_only` | §3.4 §4.9 | + |
| 8 | `test_report_skill_respawn_protocol_documented` — body contains literal `Report-Skill Respawn Protocol` | §3.4 §6.10 + §8 cues | + |
| 9 | `test_respawn_reasons_list_typed_documented` — body contains literal `respawn_reasons` AND literal `list-typed` (or `list typed`) | §3.4 §6.10 + §8 cues | + |
| 10 | `test_three_iteration_cap_documented` — body contains literal `≤3` or `cap 3` AND `iteration` | §3.4 §4.9 | + |
| 11 | `test_must_fix_mandatory_context_documented` — body contains literals `MUST_FIX` AND `context` AND `mandatory` (or `required`) | §3.4 + §6.11 | + |
| 12 | `test_max_useful_respawns_is_two` — body contains literal `Maximum useful respawns per meditation = 2` (or `Max useful respawns` substring + `2`) | §3.4 §4.9 iteration loop | + |

#### 3.2.5 `crux-skill-memory-meditation-report`

| # | Assertion | Source | Polarity |
|---|-----------|--------|:--------:|
| 1 | `test_skill_md_exists` | §2 row 5 | + |
| 2 | `test_frontmatter_name_matches_directory` | §2 row 5 | + |
| 3 | `test_description_contains_meditation` | §2 anchors | + |
| 4 | `test_description_contains_report_verb_and_universal_contrast` — description contains literals `Report` AND `Universal Contrast` | §3.6 + §8 cues | + |
| 5 | `test_comprehensiveness_level_mapping_table_present` — body contains literal `Comprehensiveness Level Mapping` | §3.6 §6.1 + §8 cues | + |
| 6 | `test_all_four_level_columns_present` — body contains literals `compact`, `default`, `detailed`, `exhaustive` | §3.6 §6.1 + §8 cues | + |
| 7 | `test_compact_chart_minimum_pinned` — body contains literal `compact`=4 (or `\`compact\`=4`) — backwards-compat pin | §6.1 `compact` anchor (regression) | + |
| 8 | `test_per_branch_section_rule_present` — body contains literal `Per-Branch Section Rule` | §3.6 §6.7 | + |
| 9 | `test_depth3_leaf_inclusion_rule_present` — body contains literal `Depth-3 Leaf Inclusion Rule` | §3.6 §6.7 | + |
| 10 | `test_peer_review_surfacing_rule_present` — body contains literal `Peer-Review Surfacing Rule` | §3.6 §6.7 | + |
| 11 | `test_init_suggestions_honour_rules_present` — body contains literal `Init-Suggestions Honour` | §3.6 §6.8 + §8 cues | + |
| 12 | `test_k10b_per_cheap_type_rendering_contract_present` — body contains literal `Per-Cheap-Type Rendering Contract` AND all 7 cheap-type names (`executive_summary`, `action_plan`, `risks_section`, `glossary`, `decision_tree_infographic`, `reader_persona_tldrs`, `cross_branch_synthesis_section`) | §3.6 §6.9 + §8 cues | + |
| 13 | `test_universal_contrast_present` — body contains literal `Universal Contrast` | §3.6 §6.4 + §8 cues | + |
| 14 | `test_anti_homogenisation_present` — body contains literal `Anti-Homogenization` or `anti-homogenisation` | §3.6 §6.3 + §8 cues | + |
| 15 | `test_chromium_fallback_chain_present` — body contains literals `chromium-browser` AND headless / Chromium fallback chain | §3.6 §6.6 | + |
| 16 | `test_report_skill_respawn_resume_handler_present` — body contains literal `Per-reason processing order` AND `accepted_finalisation_enhancements` (per-reason ordering verbatim) | §3.6 §6.10 | + |
| 17 | `test_subject_matter_focus_present` — body contains literal `Subject-Matter Focus` | §3.6 §8 | + |
| 18 | `test_footer_level_segment_always_written` — body contains literal `level:` AND `finalisation-enhancements:` (footer extension) | §3.6 §6.12 footer | + |

#### 3.2.6 `crux-skill-memory-meditation-coordination`

| # | Assertion | Source | Polarity |
|---|-----------|--------|:--------:|
| 1 | `test_skill_md_exists` | §2 row 6 | + |
| 2 | `test_frontmatter_name_matches_directory` | §2 row 6 | + |
| 3 | `test_description_contains_meditation` | §2 anchors | + |
| 4 | `test_description_contains_coordination_verb_and_facet_registry` — description contains literals `coordination` AND `facet registry` | §2 row 6 + user brief mandate | + |
| 5 | `test_18_row_filename_table_present` — body contains all 18 filename-pattern literals (per §3.5 §5.1 / §5.1 of freeze): `facets-pending-{ts}.yml`, `facets.md`, `init-suggestions-{ts}.yml`, `branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md`, `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}-findings.md`, `branch-{N}-peer-review-{branchSlug}-{ts}.md`, `pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml`, `confirmed-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml`, `review-pre-report-{ts}-iter-{N}.md`, `finalisation-enhancements.yml`, `{model-subdir}/finalisation-enhancements.yml`, `follow-up-meditation-{ts}.yml`, `follow-up-spec-{ts}.yml`, `follow-up-memories-{ts}.yml`, `follow-up-expansion-{ts}.yml`, `retrospective-{ts}.md`, `report-{topic-slug}-{ts}.html`, `report-{topic-slug}-{ts}.pdf` | §3.5 §5.1 (single source of truth) | + (18 sub-asserts) |
| 6 | `test_placeholders_documented` — body contains literals `{topic-slug}`, `{slug}`, `{ts}`, `{N}`, `{D}`, `{S}` | §3.5 §5.2 | + |
| 7 | `test_prefix_glob_polling_rule_present` — body contains literal `prefix-glob` AND `ls -1t` | §3.5 §5.3 | + |
| 8 | `test_never_hard_code_rule_present` — body contains literal `Never hard-code` AND `report.html` (the canonical forbidden literal) | §3.5 §5.3 | + |
| 9 | `test_retrospective_template_present` — body contains literal `retrospective-{ts}.md` AND `Process Retrospective` | §3.5 §5.7 | + |
| 10 | `test_branch_leaf_index_template_present` — body contains literal `Branch & Leaf Index` AND `Top-level artifacts` | §3.5 §5.8 | + |
| 11 | `test_branch_leaf_index_extended_rows_present` — body contains literals `[Init suggestions](init-suggestions-{ts}.yml)` AND `[Finalisation enhancements](finalisation-enhancements.yml)` | §3.5 §5.8 (richness additions) | + |
| 12 | `test_ensemble_working_directory_documented` — body contains literal `model-{label-slug}/` AND `ensemble-report-{topic-slug}` | §3.5 §5.9 | + |

**Per-skill subtotals**:
- research: 9
- quick: 7
- ensemble: 11
- review: 12
- report: 18
- coordination: 12

**Subtotal — six skills**: **69 new positive assertions** in 6 new
pytest classes (`TestMeditationSkillResearch`,
`TestMeditationSkillQuick`, `TestMeditationSkillEnsemble`,
`TestMeditationSkillReview`, `TestMeditationSkillReport`,
`TestMeditationSkillCoordination`).

### 3.3 Refactored command — `.cursor/commands/crux-meditate.md` (post-S06 thin coordinator)

**New class**: `TestMeditationCommandThinCoordinator` (read via
`_read_command_file()` — already exists).

| # | Assertion | Source | Polarity |
|---|-----------|--------|:--------:|
| 1 | `test_usage_section_still_present` — `## Usage` heading | §4.1 §2 (unchanged) | + |
| 2 | `test_mode_descriptions_table_present` — body contains literals `Research`, `Quick`, `Ensemble` mode names | §4.1 §3 + §8 cues | + |
| 3 | `test_depth_selection_gate_still_present` — body contains literal `Q-Depth-Selection` AND `### Depth Selection — MANDATORY` | §4.1 §6 (unchanged) | + |
| 4 | `test_cost_and_richness_ack_gate_still_present` — body contains literal `Q-Cost-and-Richness-Acknowledgment` AND `### Cost & Scope Acknowledgment — MANDATORY` | §4.1 §7 (unchanged) | + |
| 5 | `test_theme_preflight_still_present` — body contains literal `### Theme Preflight — MANDATORY` | §4.1 §8 (unchanged) | + |
| 6 | `test_ensemble_orchestration_still_present` — body contains literal `#### Ensemble mode (--ensemble)` AND `modelPool` | §4.1 §14 (unchanged) | + |
| 7 | `test_continuation_menu_still_present` — body contains literal `Steps 9–12: Calling-agent block` AND K10c groups (`Expansion directions`, `Apply un-chosen enhancements`, `Spawn queued follow-ups`) | §4.1 §15 (unchanged) | + |
| 8 | `test_finalisation_enhancements_gate_still_present` — body contains literal `Q-Finalisation-Enhancements` AND `multi-select` AND `0–5` | §4.1 §17 (askQuestion stays calling-agent-side per K4) | + |
| 9 | `test_combined_pattern_b_5_sub_questions_still_present` — body contains literal `5 sub-question` (or `five sub-question`) AND `additional_focus_areas` | §4.1 §9 (unchanged) | + |
| 10 | `test_instructions_spawn_target_is_meditation_guide` — body contains literal `crux-cursor-meditation-guide` in the `## Instructions` section | §4.1 §4 (modified — spawn target re-target) + §8 cues | + |
| 11 | `test_instructions_does_not_spawn_memory_manager` (NEGATIVE) — body does NOT contain literal `crux-cursor-memory-manager` anywhere | §4.1 §4 + §8 cues (negative row) | − |
| 12 | `test_thin_coordinator_line_budget` (SOFT — informational only, no assertion) — `len(content.splitlines()) <= 750` advisory check; document as a SHOULD assertion only — strict assertion deferred to S12 integrity review | §4.2 line budget projection | + (soft) |
| 13 | `test_coordination_conventions_shrunk_to_pointer` — body contains literal `crux-skill-memory-meditation-coordination` (pointer to skill) | §4.1 §10 (shrunk) | + |
| 14 | `test_research_mode_pointer_present` — body contains literal `crux-skill-memory-meditation-research` (pointer to skill) | §4.1 §12 (shrunk) | + |
| 15 | `test_quick_mode_pointer_present` — body contains literal `crux-skill-memory-meditation-quick` (pointer to skill) | §4.1 §13 (shrunk) | + |
| 16 | `test_adversarial_review_pointer_present` — body contains literal `crux-skill-memory-meditation-review` (pointer to skill) | §4.1 §18 (shrunk) | + |
| 17 | `test_report_generation_pointer_present` — body contains literal `crux-skill-memory-meditation-report` (pointer to skill) | §4.1 §21 (shrunk) | + |
| 18 | `test_ensemble_aggregation_pointer_present` — body contains literal `crux-skill-memory-meditation-ensemble` (pointer to skill) | §4.1 §22 (shrunk) | + |
| 19 | `test_related_links_lists_six_skills` — `## Related` section contains all six skill paths | §4.1 §23 (modified) | + |
| 20 | `test_related_links_meditation_guide_link` — `## Related` section contains literal `.cursor/agents/crux-cursor-meditation-guide.md` | §4.1 §23 (modified) | + |

**Subtotal — refactored command**: **18 positive + 1 negative = 19 new
assertions** in `TestMeditationCommandThinCoordinator` (the soft
line-budget check above counts as 1 positive — total 18 hard + 1 soft +
1 negative).

### 3.4 Trimmed memory-manager — `.cursor/agents/crux-cursor-memory-manager.md` (post-S07 trimmed)

**New class**: `TestMemoryManagerPostTrim` (read via
`_read_memory_manager_file()` — new helper that reads
`.cursor/agents/crux-cursor-memory-manager.md` directly, NOT via the
dual-resolver — because we MUST assert the memory-manager content even
after `crux-cursor-meditation-guide.md` exists alongside it).

| # | Assertion | Source | Polarity |
|---|-----------|--------|:--------:|
| 1 | `test_file_exists` — `.cursor/agents/crux-cursor-memory-manager.md` resolves | §5.1 (preserved) | + |
| 2 | `test_dream_mode_section_retained` — body contains literal `### Dream Mode` (or `Dream Mode — `) | §5.2 (retained) | + |
| 3 | `test_rem_sleep_section_retained` — body contains literal `REM Sleep` | §5.2 (retained) | + |
| 4 | `test_recall_mode_section_retained` — body contains literal `### Recall Mode` (or `Recall Mode — `) | §5.2 (retained) | + |
| 5 | `test_remember_mode_section_retained` — body contains literal `Remember Mode` | §5.2 (retained) | + |
| 6 | `test_forget_mode_section_retained` — body contains literal `### Forget Mode` (or `Forget Mode — `) | §5.2 (retained — Forget at 1160–1188) | + |
| 7 | `test_no_phases_a_g_research_section` (NEGATIVE) — body does NOT contain literal `Phases A–G research` (the Meditate executable heading) | §5.1 (deleted) + §8 negative cue | − |
| 8 | `test_no_quick_6_step_protocol_section` (NEGATIVE) — body does NOT contain literal `Quick 6-step` | §5.1 (deleted) + §8 negative cue | − |
| 9 | `test_no_adversarial_review_executable_section` (NEGATIVE) — body does NOT contain literal `### Adversarial Review` (Meditate-only mode heading — note the **`### `** prefix forces a heading match; a passing-mention is OK) | §5.1 (deleted) | − |
| 10 | `test_no_ensemble_aggregation_executable_section` (NEGATIVE) — body does NOT contain literal `### Ensemble Aggregation Mode` (deleted heading) | §5.1 (deleted; the `Ensemble Aggregation function` lives in the guide agent + `skill:ensemble` instead) | − |
| 11 | `test_no_meditate_mode_executable_heading` (NEGATIVE) — body does NOT contain literal `### Meditate Mode` (the heading moved entirely to the guide agent) | §5.1 (deleted heading) | − |
| 12 | `test_no_k10c_reflection_rubric_in_memory_manager` (NEGATIVE) — body does NOT contain literal `K10c reflection rubric` (rubric moved to `skill:research`) | §5.1 §4.8 (deleted from memory-manager) | − |
| 13 | `test_no_combined_pattern_b_facet_confirmation_in_memory_manager` (NEGATIVE) — body does NOT contain literal `Combined Pattern-B` (combined gate moved to command + scout side moved to skills) | §5.1 (deleted) | − |
| 14 | `test_pointer_to_meditation_guide_present` — body MAY contain literal `crux-cursor-meditation-guide` (S07 may add a pointer paragraph from the deleted `### Meditate Mode` heading position) — assert presence as the canonical handoff signal | §5.1 (replacement pointer paragraphs) | + |
| 15 | `test_no_meditate_in_critical_rules` (NEGATIVE) — body's `## Critical Rules` section does NOT contain literal `Meditate` (Meditate-specific critical rules moved to the guide agent) | §5.1 (deleted) | − (soft; gated by section-extraction helper) |
| 16 | `test_design_principles_meditate_bullets_removed` (NEGATIVE) — body does NOT contain literals `Meditate Mode design principle` block markers — confirm the ≈20-bullet design-principles list (currently agent lines 1137–1158) has been excised | §5.1 §1.3 row 9 (moved to guide agent) | − |
| 17 | `test_post_trim_line_budget` (SOFT) — `len(content.splitlines()) <= 400` advisory; document as a SHOULD assertion only — strict assertion deferred to S12 integrity review | §5.4 post-trim line budget | + (soft) |

**Subtotal — trimmed memory-manager**: **4 positive + 8 negative = 12
new assertions** (with 1 additional soft line-budget check) in
`TestMemoryManagerPostTrim`.

### 3.5 Aggregate K8 list narrowing — sibling class for positive dist presence

**New class**: `TestMeditateDecompDistFilesPresent` (paired with the
post-trim narrowed `TestMeditateNoNewDistFilesK8`).

| # | Assertion | Source | Polarity |
|---|-----------|--------|:--------:|
| 1 | `test_dist_files_includes_meditation_guide_agent` — `scripts/create-crux-zip.py::DIST_FILES` contains literal `.cursor/agents/crux-cursor-meditation-guide.md` | §3.9 row 2 + freeze §9 (S10 adds) | + |
| 2 | `test_dist_files_includes_all_six_skills` — iterate 6 skill paths and assert each appears in `DIST_FILES` (`.cursor/skills/crux-skill-memory-meditation-research/SKILL.md` … `coordination/SKILL.md`) | §3.9 row 1 + freeze §9 | + (6 sub-asserts) |
| 3 | `test_install_py_includes_meditation_guide_and_skills` — `install.py::MEMORY_FILE_PREFIXES` (or fallback file list) contains the guide-agent + 6 skill paths | §3.9 row 1 + freeze §9 | + |
| 4 | `test_dist_manifest_includes_meditation_guide_and_skills` — `.crux/dist-manifest.json` `files` array contains the guide-agent + 6 skill paths | §3.9 row 3 + freeze §9 | + |

**Subtotal — dist presence**: **4 positive assertions** (with 6 + 7
sub-asserts inside `test_dist_files_includes_all_six_skills` and
`test_install_py_includes_meditation_guide_and_skills` → 17 individual
substring checks).

### 3.6 Aggregate new positive / negative counts (D04 rollup)

| Destination | New positive | New negative |
|-------------|-------------:|-------------:|
| `TestMeditationGuideAgent` (§3.1) | 22 | 2 |
| `TestMeditationSkillResearch` (§3.2.1) | 9 | 0 |
| `TestMeditationSkillQuick` (§3.2.2) | 7 | 0 |
| `TestMeditationSkillEnsemble` (§3.2.3) | 11 | 0 |
| `TestMeditationSkillReview` (§3.2.4) | 12 | 0 |
| `TestMeditationSkillReport` (§3.2.5) | 18 | 0 |
| `TestMeditationSkillCoordination` (§3.2.6) | 12 | 0 |
| `TestMeditationCommandThinCoordinator` (§3.3) | 18 | 1 |
| `TestMemoryManagerPostTrim` (§3.4) | 4 | 8 |
| `TestMeditateDecompDistFilesPresent` (§3.5) | 4 | 0 |
| **TOTAL** | **117** | **11** |

**Headline**: **117 new positive assertions** (≫ ≥50 target) +
**11 new negative assertions** (> ≥10 target) across **10 new pytest
classes**.

---

## 4. SDK Eval Plan (D05) — file-by-file

**Single target file**: `evals/sdk/tests/q-meditate.test.ts` (576
lines). No other SDK files reference Meditate.

### 4.1 Helper widening (top-of-file changes; no new file added)

Add a `readSkillFile(skill: string): string` helper rooted at
`.cursor/skills/crux-skill-memory-meditation-<skill>/SKILL.md` (returns
empty string if absent — same fall-back convention as the existing
`resolveTargetFile`). Widen `readAgentFile()` to fall through to
`crux-skill-memory-meditation-research/SKILL.md` for rubric content
(K10 Reflection Rubric describe-block needs this).

### 4.2 Q1 — re-target the subagent literal (1 swap + 1 negative)

| Block | Existing assertion | New assertion (S08 edit) |
|-------|--------------------|---------------------------|
| `Q1 — spawns subagents for recursive exploration` (line 246) | `hasSubagentCall(toolCalls, "crux-cursor-memory-manager")` | `hasSubagentCall(toolCalls, "crux-cursor-meditation-guide")` AND add an unconditional structural sibling `expect(commandContent).not.toContain("crux-cursor-memory-manager")` in the structural section below (so the negative landing is unconditional even with `skipExpensive`) |

### 4.3 Q2 / Q3 — kept verbatim

No literal swaps. The existing facet-derivation language regex and
memory-content checks survive the decomposition intact.

### 4.4 New unconditional structural describe blocks (additive)

To match the new pytest classes structurally, add these new
**unconditional** describe blocks below the existing K2 / K10 / K9
blocks. Each describes a single new destination at one substring
granularity (file-system + frontmatter + canonical contracts).

#### 4.4.1 `Q: Meditate — Structural: Guide Agent Frontmatter & Persona`

| `it` block | Asserts |
|-----------|---------|
| `guide agent file exists` | `existsSync(.cursor/agents/crux-cursor-meditation-guide.md)` |
| `frontmatter has name: crux-cursor-meditation-guide` | content contains literal `name: crux-cursor-meditation-guide` |
| `description contains meditation` | frontmatter `description:` value contains literal `meditation` |
| `mode router lists Phases A–G, Quick 6-step, K10 reflection, Adversarial Review` | content contains all four literals |
| `canonical comprehensiveness abort error string present` | content contains literal `comprehensiveness: payload required; missing from spawn prompt — caller misconfigured` |
| `User Input Escalation + Pattern A + Pattern B + needs_user_input present` | content contains all four literals |

→ **6 it blocks**

#### 4.4.2 `Q: Meditate — Structural: Six Meditation Skills`

| `it` block | Asserts |
|-----------|---------|
| `all six SKILL.md files exist` | iterate `SKILL_DIRS` (size 6) and `expect(existsSync(skill path)).toBe(true)` |
| `each skill frontmatter name matches its directory` | iterate and `expect(content).toContain(\`name: ${dir}\`)` |
| `each skill description contains meditation` | iterate and assert |
| `coordination skill 18-row filename table present (sentinel rows)` | reads `coordination` skill; contains `finalisation-enhancements.yml`, `init-suggestions-{ts}.yml`, `branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md`, `retrospective-{ts}.md`, `report-{topic-slug}-{ts}.html` |
| `research skill: Phases A–G + init-suggestions write + canonical treatment filter` | reads `research` skill; contains literals `Phases A–G` (or `Phases A-G`), `init-suggestions-{ts}.yml`, `treatment:`, `additional_facet` |
| `quick skill: 6-step + warn-only citation regime` | reads `quick` skill; contains literals `6-step`, `warn_only` (or `warn-only`) |
| `review skill: 13 dimensions + Dim 12 + Dim 13 + Report-Skill Respawn Protocol` | reads `review` skill; contains literals `13`, `Comprehensiveness fidelity`, `Init-suggestion AND finalisation-enhancement honour`, `Report-Skill Respawn Protocol`, `respawn_reasons` |
| `report skill: Comprehensiveness Level Mapping + Per-Cheap-Type + 7 cheap types + Universal Contrast` | reads `report` skill; contains all relevant literals |
| `ensemble skill: cross-model-synthesis.md + source_tree + surfaced_to_root + cross_model_candidates + union_candidates + K10 Ensemble Respawn Targeting` | reads `ensemble` skill; contains all literals |

→ **9 it blocks**

#### 4.4.3 `Q: Meditate — Structural: Refactored Command Thin Coordinator`

| `it` block | Asserts |
|-----------|---------|
| `## Instructions spawns crux-cursor-meditation-guide` | `readCommandFile()` contains literal `crux-cursor-meditation-guide` |
| `## Instructions does NOT spawn crux-cursor-memory-manager` (NEGATIVE) | `expect(content).not.toContain("crux-cursor-memory-manager")` |
| `Q-Cost-and-Richness-Acknowledgment still present` | (already covered by K2 block above; included for thin-coordinator completeness) |
| `Q-Finalisation-Enhancements still present` | (already covered) |
| `Related section lists six meditation skills` | content contains all 6 skill directory names |

→ **5 it blocks** (3 net new, 2 cross-referenced from existing blocks).

#### 4.4.4 `Q: Meditate — Structural: Trimmed Memory-Manager`

| `it` block | Asserts |
|-----------|---------|
| `crux-cursor-memory-manager.md still has Dream + REM + Recall + Remember + Forget` | direct `readFileSync(memory-manager path)` and assert all five mode names |
| `crux-cursor-memory-manager.md no longer has \`### Meditate Mode\` heading` (NEGATIVE) | `expect(content).not.toContain("### Meditate Mode")` |
| `crux-cursor-memory-manager.md no longer has Phases A–G research executable section` (NEGATIVE) | `expect(content).not.toContain("Phases A–G research")` |
| `crux-cursor-memory-manager.md no longer has Quick 6-step executable section` (NEGATIVE) | `expect(content).not.toContain("Quick 6-step")` |
| `crux-cursor-memory-manager.md no longer has \`### Adversarial Review\` heading` (NEGATIVE) | `expect(content).not.toContain("### Adversarial Review")` |
| `crux-cursor-memory-manager.md no longer has \`### Ensemble Aggregation Mode\` heading` (NEGATIVE) | `expect(content).not.toContain("### Ensemble Aggregation Mode")` |

→ **6 it blocks** (1 positive + 5 negative).

#### 4.4.5 New SDK rollup

| Block | New it tests |
|-------|-------------:|
| 4.4.1 Guide Agent Frontmatter & Persona | 6 |
| 4.4.2 Six Meditation Skills | 9 |
| 4.4.3 Refactored Command Thin Coordinator | 5 |
| 4.4.4 Trimmed Memory-Manager | 6 |
| **TOTAL new SDK it blocks** | **26** |

**Combined SDK total post-S08**: 28 (existing) − 0 (deletions) + 26
(new structural) = **54 it blocks across 12 describe blocks** (8
existing + 4 new structural). Live LLM-driven Q1/Q2/Q3 remain gated by
`SDK_EVAL_SKIP_EXPENSIVE`; all 5 + 4 = 9 new structural blocks run
unconditionally.

### 4.5 No deletions

All 28 existing `it` blocks remain. The Q1 spawn-target literal is the
only modification.

---

## 5. Conftest Changes (D06)

`evals/conftest.py` currently exposes no Meditate-specific fixtures
because the existing tests do raw file reads. The new assertion plan
parameterises six skills + one guide agent + one trimmed
memory-manager — adding two helpers per the user brief minimises
literal duplication.

### 5.1 New helper — `_read_meditation_artifact(kind: str, name: str | None = None)`

| `kind` | `name` | Returns |
|--------|--------|---------|
| `"command"` | — | content of `.cursor/commands/crux-meditate.md` (raw — no dual-resolver) |
| `"guide_agent"` | — | content of `.cursor/agents/crux-cursor-meditation-guide.md` (empty string if absent) |
| `"memory_manager"` | — | content of `.cursor/agents/crux-cursor-memory-manager.md` (empty string if absent) |
| `"skill"` | one of `research` / `quick` / `ensemble` / `review` / `report` / `coordination` | content of `.cursor/skills/crux-skill-memory-meditation-<name>/SKILL.md` (empty string if absent) |
| `"all_meditation_sources"` | — | concatenation of all of the above (used by tests that only need to assert "this literal appears somewhere across the new architecture") |

Placement: top of `evals/conftest.py` after `_make_config` (lines 22+),
exported via `from conftest import _read_meditation_artifact` in
`test_q_meditate.py`. The existing `_read_command_file()` and
`_read_agent_file()` helpers in `test_q_meditate.py` stay (no breaking
changes); they delegate to `_read_meditation_artifact("command")` /
`_read_meditation_artifact("guide_agent")` internally.

### 5.2 New fixture — `sample_meditation_working_dir(tmp_path)`

Returns a `pathlib.Path` to a temp `meditations/{yyyymmdd}-sample-topic/`
directory pre-populated with:
- empty `facet-registry.yml` (Research mode artefact)
- empty `citations-index.yml`
- empty `facets.md` (frontmatter only)

**Rationale**: enables future S08 / S12 hypothetical tests that exercise
filename-grammar substring assertions against a real directory tree
without mutating the live `meditations/` directory (which is gitignored
anyway per `.gitignore:59`).

### 5.3 New fixture — `sample_init_suggestions_yml(tmp_path, treatments)`

Builds an `init-suggestions-{ts}.yml` document fixture with the canonical
4-treatment schema (`skip` / `additional_facet` / `report_section_only`
/ `additional_facet_AND_section`) and the schema-invariant
post-conditions (`resulting_section_id`, `resulting_branch_index`,
`custom_report_section_title`) per freeze §4.7. Parameterised by a
`treatments: list[str]` argument so individual tests can build minimal
fixtures.

**Rationale**: substring-presence checks against the live skill files
already cover the canonical name; the fixture is here for any future
schema-correctness eval (out of scope for S08; documented as a S12
integrity-review hook).

### 5.4 No breaking changes to existing fixtures

`tmp_memories_dir`, `sample_config`, `sample_memory_file`,
`sample_tracker_file`, `write_memory`, `write_tracker` all stay
unchanged. They are not consumed by meditate tests today and the new
plan keeps it that way.

---

## 6. Manual Eval Scenario Updates (D07)

### 6.1 `evals/USER_EVAL_CHECKLISTS.md`

| Section | Line | Required change | Polarity |
|---------|-----:|------------------|:--------:|
| Q1. Meditate — No Arguments, expected outcomes row 3 | 450 | Replace `crux-cursor-memory-manager` with `crux-cursor-meditation-guide` | re-target |
| Q1 — add new expected outcome row after row 3 | 450 (insert) | "The spawned subagent loads `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md` (or `meditation-quick` in Quick mode) before executing the workflow" — pass criteria: agent output mentions the skill or the Read tool log shows the skill path | + (new) |
| Q1 — add Research-vs-Quick branch row | 450 (insert) | "If the user accepts the default `Research` mode at the Cost-and-Richness gate, the agent runs through Phases A–G; if the user switches to `Quick` via `switch_to_quick`, the agent runs the 6-step protocol" | + (new) |
| Q2. Meditate — Topic Argument, expected outcomes | 482–488 | Add a new row asserting the **Q-Cost-and-Richness-Acknowledgment** gate fires (4 richness levels visible; `default` preselected) before the depth-0 spawn | + (new) |
| Q2 — add `Q-Finalisation-Enhancements` row | 482 (insert) | After consolidation completes, a multi-select 0–5 enhancement gate appears with at least 1 candidate; selecting 0 reproduces today's behaviour and proceeds to adversarial review | + (new) |
| Q3. Meditate — File/Folder References | 510–516 | Add a row asserting the **Theme Preflight Q1b repo-scan** fires when `@`/`file` references are present | + (new) |
| Integration § step 8 `Meditate` | 707 | Keep `/crux-meditate "performance patterns"` verbatim; **NO subagent-identity literal in this step** | kept verbatim |
| Command Reference table | 858–859 | Keep `/crux-meditate` rows verbatim (command name unchanged) | kept verbatim |
| File Reference table | 875 | Keep `.cursor/commands/crux-meditate.md` row + **ADD** rows for `.cursor/agents/crux-cursor-meditation-guide.md` and the six `.cursor/skills/crux-skill-memory-meditation-*/SKILL.md` directories | + (new) |
| File Reference table — Memory System summary | 947 (legacy) | Update from "Meditate Command — `.cursor/commands/crux-meditate.md` — Recursive memory exploration" to add a sibling row "Meditation Guide Agent — `.cursor/agents/crux-cursor-meditation-guide.md` — Owns Meditate persona, Phases A–G, Quick 6-step, 13-dim adversarial review, K10 ensemble aggregation" | + (new) |

### 6.2 `evals/sdk/README.md`

| Section | Line | Required change |
|---------|-----:|------------------|
| `pnpm test:meditate` row (line 43) | 43 | Keep verbatim |
| `SDK_EVAL_SKIP_EXPENSIVE` row (line 131) | 131 | Keep verbatim |
| Test Categories table (line 70) | 70 | Add a new row: `Q: Meditate \| Q1-Q3 + Structural (K2/K9/K10) + Decomp (Guide/Skills/Command/MM-Trim) \| Facet derivation; subagent spawning identity (now `crux-cursor-meditation-guide`); structural pinning of merged cost-and-richness gate, finalisation-enhancements gate, respawn protocol, ensemble layered cadence, guide-agent + six-skill presence, trimmed memory-manager` |
| Adding New Tests § (line 86) | 86 | Add a paragraph: "Structural Meditate tests use `readCommandFile()` / `readAgentFile()` / `readSkillFile(name)` (dual-resolver: prefer post-decomp guide-agent + skills when present; fall back to `.cursor/commands/crux-meditate.md` + `.cursor/agents/crux-cursor-memory-manager.md` for pre-S04 working trees)." |

### 6.3 No edits to `evals/README.md` (root) — only the SDK README documents the test-suite categories.

---

## 7. Regression Guarantees (D08) — Pinning the 20260524 Freeze

Every freeze invariant gets at least one **positive** substring-presence
assertion that survives the decomposition. All citations are to the
2026-05-24 freeze refresh (`meditate-frozen-contract-20260524.md`).

### 7.1 Modes (§1) — three modes + four richness levels

| Invariant | Assertion | Location |
|-----------|-----------|----------|
| 4 mode variants exist (Research / Quick / Ensemble+Research / Ensemble+Quick) | `_read_command_file()` contains literals `Research`, `Quick`, `Ensemble` (existing `TestMeditateMergedCostAndRichnessGate::test_sub_q2_option_set_preserved` covers Sub-Q2 swap options including `switch_to_ensemble`) | command + `TestMeditationCommandThinCoordinator` |
| 4 richness levels (`compact` / `default` / `detailed` / `exhaustive`) | All 4 literals present in command + `skill:report` (existing `TestMeditateMergedCostAndRichnessGate::test_all_four_richness_enum_values_present` + new `TestMeditationSkillReport::test_all_four_level_columns_present`) | command + skill:report |
| Richness × depth × mode cost table | Command contains `~{N_compact}` placeholder OR worked example `~45` (existing test) | command |
| `compact` reproduces pre-richness behaviour | Existing `TestMeditateBackwardsCompatibility` + new `TestMeditationSkillReport::test_compact_chart_minimum_pinned` | command + skill:report |

### 7.2 Gates (§2) — five logical slots

| Gate | Assertion | Location |
|------|-----------|----------|
| `Q-Depth-Selection` | Existing `TestMeditateRecursiveDepth::test_depth_selection_question_exists` + new `TestMeditationCommandThinCoordinator::test_depth_selection_gate_still_present` | command |
| **`Q-Cost-and-Richness-Acknowledgment`** (MERGED — replaces `Q-Cost-Acknowledgment`) | Existing `TestMeditateMergedCostAndRichnessGate::test_merged_gate_exists` (positive) + `test_no_standalone_q_comprehensiveness_gate` (negative — paired) + new `TestMeditationCommandThinCoordinator::test_cost_and_richness_ack_gate_still_present` | command |
| Theme Preflight (Q1–Q5 + Q1b) | New `TestMeditationCommandThinCoordinator::test_theme_preflight_still_present` | command |
| Combined Pattern-B 5-sub-Q | New `TestMeditationCommandThinCoordinator::test_combined_pattern_b_5_sub_questions_still_present` | command |
| **`Q-Finalisation-Enhancements`** (mid-workflow Pattern-B; K10a) | Existing `TestMeditateFinalisationEnhancementGate::test_gate_exists_in_command_file` + new `TestMeditationCommandThinCoordinator::test_finalisation_enhancements_gate_still_present` | command |

### 7.3 Mandatory paired report (§6.1 / §6.2)

| Invariant | Assertion | Location |
|-----------|-----------|----------|
| Paired HTML + PDF rule | Existing `TestMeditateSafeguardRegressions::test_paired_html_pdf_rule_present` + new `TestMeditationSkillReport::test_skill_md_exists` (the rule is now in the skill) | skill:report |
| Fresh-timestamp on respawn | New `TestMeditationSkillReport::test_report_skill_respawn_resume_handler_present` | skill:report |
| Prefix-glob latest-wins | New `TestMeditationSkillCoordination::test_prefix_glob_polling_rule_present` | skill:coordination |

### 7.4 13-dim adversarial loop (§4.9)

| Invariant | Assertion | Location |
|-----------|-----------|----------|
| 13 dimensions | Existing `TestMeditateAdversarialReviewerExtension::test_reviewer_has_13_dimensions` + new `TestMeditationSkillReview::test_description_contains_review_verb_and_13_dimensions` | skill:review |
| Dim 12 Comprehensiveness fidelity | Existing `TestMeditateAdversarialReviewerExtension::test_dimension_12_comprehensiveness_fidelity` + new `TestMeditationSkillReview::test_dimension_12_comprehensiveness_fidelity_documented` | skill:review |
| Dim 13 Init-suggestion honour | Existing `TestMeditateAdversarialReviewerExtension::test_dimension_13_init_suggestion_honour` + new `TestMeditationSkillReview::test_dimension_13_init_suggestion_honour_documented` | skill:review |
| ≤3 iteration cap shared | Existing `TestMeditateRespawnFiniteIteration::test_iteration_cap_is_three` + new `TestMeditationSkillReview::test_three_iteration_cap_documented` | skill:review |
| Max useful respawns = 2 | Existing `TestMeditateRespawnFiniteIteration::test_max_useful_respawns_is_two` + new `TestMeditationSkillReview::test_max_useful_respawns_is_two` | skill:review |
| MUST_FIX `needs_user_input` mandatory `context` | Existing `TestMeditateSafeguardRegressions::test_must_fix_needs_user_input_schema_with_context_field` + new `TestMeditationSkillReview::test_must_fix_mandatory_context_documented` | skill:review |
| Dim 13 `respawn_required: true` bypasses standard flow | Existing `TestMeditateRespawnProtocol::test_respawn_required_true_bypasses_standard_flow` | skill:review |

### 7.5 Retrospective always-written (§5.7)

| Invariant | Assertion | Location |
|-----------|-----------|----------|
| `retrospective-{ts}.md` always written | Existing `TestMeditateSafeguardRegressions::test_retrospective_always_written` + new `TestMeditationSkillCoordination::test_retrospective_template_present` | skill:coordination |

### 7.6 K10 layered cadence (§4.5)

| Invariant | Assertion | Location |
|-----------|-----------|----------|
| K10 layered cadence steps 3b–3f | Existing `TestMeditateK10EnsembleLayeredCadence` (9 methods) + new `TestMeditationSkillEnsemble::test_k10_layered_cadence_steps_3b_3f_documented` | skill:ensemble |
| Per-tree write-only YAML (`source_tree`, `surfaced_to_root`) | Existing methods + new `TestMeditationSkillEnsemble::test_source_tree_field_documented` / `test_surfaced_to_root_documented` / `test_per_tree_write_only_documented` | skill:ensemble |
| Root combined YAML (`cross_model_candidates` + `union_candidates`) | Existing methods + new `TestMeditationSkillEnsemble::test_cross_model_candidates_and_union_candidates_documented` | skill:ensemble |
| Single root askQuestion | Existing `TestMeditateK10EnsembleLayeredCadence::test_single_root_ask_question_documented` | command + skill:ensemble |

### 7.7 K10 cadence: K10c reflection rubric (§4.8) — single-model + ensemble per-tree

| Invariant | Assertion | Location |
|-----------|-----------|----------|
| Rubric impact × insight-value 1–10 each | Existing `TestMeditateK10ReflectionRubric` (7 methods) | skill:research (new home) |
| `minimum_impact_threshold` defaults to 6 | Existing `TestMeditateK10ReflectionRubric::test_minimum_impact_threshold_defaults_to_6` | skill:research |
| Weights configurable + default 1.0 | Existing `TestMeditateK10WeightsConfigurable` (4 methods) | skill:research + `.crux/crux-memories.json` |
| 7 cheap types + 4 expensive types | New `TestMeditationSkillReport::test_k10b_per_cheap_type_rendering_contract_present` (enumerates all 7 cheap types) + cross-reference to design §4.8 catalogue | skill:report (rendering side) + skill:research (write side) |

### 7.8 Comprehensiveness Level Mapping (§6.1) — 12 dimensions × 4 levels

| Invariant | Assertion | Location |
|-----------|-----------|----------|
| Level mapping table exists | Existing `TestMeditateComprehensivenessLevelMapping::test_level_mapping_table_exists` + new `TestMeditationSkillReport::test_comprehensiveness_level_mapping_table_present` | skill:report |
| All 12 dimensions enumerated | Existing `TestMeditateComprehensivenessLevelMapping::test_every_level_row_has_dimensions` | skill:report |
| `compact` row backwards-compat anchor | Existing `TestMeditateBackwardsCompatibility` (8 methods) + new `TestMeditationSkillReport::test_compact_chart_minimum_pinned` | skill:report |

### 7.9 Canonical `additional_focus_areas[]` + `treatment:` filter (per the user-brief constraint)

| Invariant | Assertion | Location |
|-----------|-----------|----------|
| Canonical array name `additional_focus_areas` (with `treatment:` filter per item) — POSITIVE | Existing `TestMeditateInitSuggestions::test_four_opt_in_modes_documented` + `test_init_suggestions_schema_fields` + new `TestMeditationSkillResearch::test_canonical_treatment_filter_present` | command + skill:research + skill:quick |
| Legacy field names `additional_focus_areas_skipped` + `additional_focus_areas_accepted` — NEGATIVE | See §8 below | all sources |

---

## 8. Negative Assertions Block (D08 mandate)

The user-brief constraint mandates **negative substring-presence** for
three categories: forbidden legacy field names, forbidden
`crux-cursor-memory-manager` in `/crux-meditate` spawn context, and
forbidden Meditate executable headings in the post-S07 memory-manager.

### 8.1 Forbidden legacy field names — `additional_focus_areas_skipped` / `additional_focus_areas_accepted`

**New class**: `TestMeditationDecompForbiddenLegacyFieldNames` (read all
relevant sources via `_read_meditation_artifact("all_meditation_sources")`
so a single concatenated string is searched).

| # | Assertion | Source |
|---|-----------|--------|
| 1 | `test_no_additional_focus_areas_skipped_anywhere` — `assert "additional_focus_areas_skipped" not in all_sources` | freeze §4.6 + design §8 negative cue (W1 regression guard) |
| 2 | `test_no_additional_focus_areas_accepted_anywhere` — `assert "additional_focus_areas_accepted" not in all_sources` | freeze §4.6 + design §8 negative cue |
| 3 | `test_no_additional_focus_areas_skipped_in_command` — same negative, scoped to `_read_meditation_artifact("command")` | per-source granularity for blame-targeting |
| 4 | `test_no_additional_focus_areas_accepted_in_command` | per-source granularity |
| 5 | `test_no_additional_focus_areas_skipped_in_guide_agent` | per-source granularity |
| 6 | `test_no_additional_focus_areas_accepted_in_guide_agent` | per-source granularity |
| 7 | `test_no_additional_focus_areas_skipped_in_skill_research` | per-source granularity |
| 8 | `test_no_additional_focus_areas_accepted_in_skill_research` | per-source granularity |
| 9 | `test_no_additional_focus_areas_skipped_in_skill_quick` | per-source granularity |
| 10 | `test_no_additional_focus_areas_accepted_in_skill_quick` | per-source granularity |

**Subtotal**: **10 negative assertions** in
`TestMeditationDecompForbiddenLegacyFieldNames`.

### 8.2 Forbidden `crux-cursor-memory-manager` in `/crux-meditate` spawn context

**New class**: `TestMeditationCommandNoMemoryManagerSpawn` (also
restated as a single negative in `TestMeditationCommandThinCoordinator`
above).

| # | Assertion | Source |
|---|-----------|--------|
| 1 | `test_command_does_not_spawn_memory_manager` — `assert "crux-cursor-memory-manager" not in _read_meditation_artifact("command")` | design §8 negative cue (the only negative cue with global scope across the command file) |
| 2 | `test_guide_agent_self_reference_not_memory_manager` — `assert "crux-cursor-memory-manager" not in _read_meditation_artifact("guide_agent")` (the guide agent must not reference the memory manager as a sibling agent inside its own body) | design §1.1 distinctness |
| 3 | `test_six_skills_do_not_reference_memory_manager` — iterate the 6 skills and `assert "crux-cursor-memory-manager" not in skill_content` | design §3 single-primary rule (skills must not cross-reference the memory-manager) |

**Subtotal**: **3 negative assertions** (in
`TestMeditationCommandNoMemoryManagerSpawn`; note assertion #1 is the
same as `TestMeditationCommandThinCoordinator::test_instructions_does_not_spawn_memory_manager`
— count once in the headline tally).

### 8.3 Forbidden Meditate executable headings in post-S07 memory-manager

(Counted in `TestMemoryManagerPostTrim` above — 8 negative assertions.)
Recapped here for cross-reference:

| # | Heading / phrase forbidden | Source |
|---|-----------------------------|--------|
| 1 | `### Meditate Mode` | design §5.1 (deleted heading) |
| 2 | `Phases A–G research` | design §5.1 (deleted) |
| 3 | `Quick 6-step` | design §5.1 (deleted) |
| 4 | `### Adversarial Review` | design §5.1 (deleted heading) |
| 5 | `### Ensemble Aggregation Mode` | design §5.1 (deleted heading) |
| 6 | `K10c reflection rubric` | design §5.1 + §4.8 (moved to skill:research) |
| 7 | `Combined Pattern-B` | design §5.1 (moved to command + scout skills) |
| 8 | (section-extraction) `Meditate` literal absent from `## Critical Rules` section | design §5.1 |

### 8.4 Aggregate negative-assertion rollup

| Source class | Negative count |
|--------------|---------------:|
| `TestMeditationGuideAgent` (§3.1) | 2 |
| `TestMeditationCommandThinCoordinator` (§3.3) | 1 |
| `TestMemoryManagerPostTrim` (§3.4) | 8 |
| `TestMeditationDecompForbiddenLegacyFieldNames` (§8.1) | 10 |
| `TestMeditationCommandNoMemoryManagerSpawn` (§8.2) | 3 (1 double-counted with §3.3 — net 2 unique) |
| **TOTAL unique** | **23 unique negative assertions** (≫ ≥10 target) |

---

## 9. Headline Totals (rollup for status / DoD reporting)

### 9.1 Plan-doc-level counts

| Metric | Value |
|--------|------:|
| Total pytest classes inventoried (current, pre-S08) | 36 (8 pre-richness + 28 richness-era) |
| Total pytest test methods inventoried | ~177 (30 + ≈147) |
| Total SDK describe blocks inventoried | 8 (3 pre-richness Q1–Q3 + 5 richness-era) |
| Total SDK `it` blocks inventoried | 28 (6 + 22) |
| `test_p_amnesia.py` Meditate touchpoints | 3 (verbatim) |
| `evals/USER_EVAL_CHECKLISTS.md` Meditate scenarios | Q1 + Q2 + Q3 + Integration § step |
| `evals/sdk/README.md` Meditate references | `pnpm test:meditate` + `SDK_EVAL_SKIP_EXPENSIVE` |
| `evals/conftest.py` Meditate-specific fixtures (today) | 0 |

### 9.2 Re-target / verbatim split

| Surface | Re-targeted (literal swap or resolver widening) | Verbatim | % re-targeted |
|---------|------------------------------------------------:|---------:|---------------:|
| `test_q_meditate.py` (177 methods / 36 classes) | ≈31 methods / 8 classes | ≈146 methods / 28 classes | **≈17.5% by method / ≈22% by class** |
| `test_p_amnesia.py` (3 touchpoints) | 0 | 3 | 0% |
| `q-meditate.test.ts` (28 it / 8 describes) | 14 it / 4 describes | 14 it / 4 describes | **50% by it / 50% by describe** |
| **Combined** | ≈45 / ≈208 | ≈163 / ≈208 | **≈22% combined by item** |

### 9.3 New assertion totals (positive + negative)

| Layer | New positive | New negative |
|-------|-------------:|-------------:|
| Pytest (§3 + §8 unique) | **117** | **23** |
| SDK structural (§4.4) | **26** (≈3 of which are NEGATIVE inside the trimmed-memory-manager describe — see §4.4.4: 1 positive + 5 negative = 6 it blocks) | counted inside the 26 — net positive 21, net negative 5 |
| **Grand total new assertions across pytest + SDK** | **138 positive** | **28 negative** |

**Both targets satisfied**:
- ≥ 50 new positive assertions → **138 planned** (≈ 2.75× target)
- ≥ 10 new negative assertions → **28 planned** (≈ 2.8× target)

---

## 10. Subtask 08 Execution Order (recommended)

S08 (eval & test update) is the consumer of this plan. Recommended
order to minimise rework:

1. **Add helpers to `evals/conftest.py`** (§5.1 / §5.2 / §5.3) — landing
   first means subsequent test additions can use the helpers.
2. **Widen `_read_command_file()` / `_read_agent_file()` in
   `evals/test_q_meditate.py`** to fall through to the four post-decomp
   skill paths (`research` / `review` / `ensemble` / `report` for the 6
   existing classes that read content moved to skills — see §2.2).
3. **Re-target the single `TestMeditateAgentSpawning` literal** (§2.1
   row 8 — `crux-cursor-memory-manager` → `crux-cursor-meditation-guide`).
4. **Narrow `TestMeditateNoNewDistFilesK8::SPEC_INTRODUCED_PATHS`**
   (§2.2 row 12 — drop the 4 decomp-legitimate paths; keep the runtime-only
   prefixes).
5. **Add 10 new pytest classes** (§3.1 through §3.5 — guide agent + 6
   skills + thin coordinator + trimmed memory-manager + dist-presence).
6. **Add 2 negative-assertion classes** (§8.1 +
   `TestMeditationCommandNoMemoryManagerSpawn` per §8.2).
7. **Update `evals/sdk/tests/q-meditate.test.ts`** — 1 literal swap + 4
   new structural describe blocks (§4.4).
8. **Update `evals/USER_EVAL_CHECKLISTS.md` Q1 + Q2 + Q3** per §6.1.
9. **Update `evals/sdk/README.md` Test Categories table** per §6.2.
10. **Verify pytest exit code 0** with `pytest evals/test_q_meditate.py
    evals/test_p_amnesia.py` against an environment where S04 (guide
    agent) + S05 (six skills) + S06 (command refactor) + S07
    (memory-manager trim) have all landed. Pre-S07 working trees will
    have some negative-assertion failures (expected) — gate the
    `TestMemoryManagerPostTrim` class behind an
    `if _read_meditation_guide_agent_file()` precondition so the class
    only runs once the new architecture is in place.

---

## Definition of Done — Subtask 03

- [x] D01 — `meditate-decomp-eval-test-plan-20260517.md` created in
  spec directory.
- [x] D02 — Current surface inventory of every pytest class + SDK
  describe / it block + amnesia row + conftest fixtures + manual
  scenarios + SDK README references, with freeze contract item
  cross-references (§1).
- [x] D03 — Migration matrix with kept / re-targeted / replaced verdict
  for every current assertion (§2). 1 literal swap + 6 resolver
  widenings + 1 K8 list narrowing + 1 SDK literal swap + 3 SDK resolver
  widenings; remaining ≈ 80% kept verbatim by class count.
- [x] D04 — New assertion plan grouped by destination (guide agent + 6
  skills + refactored command + trimmed memory-manager + dist
  presence); 117 new positive pytest assertions (target ≥ 50); ≥ 10
  negative assertions; six-skill cap holds at 6 with one mandated
  presence assertion per skill (`SKILL.md` exists + frontmatter `name`
  matches directory + `description` contains `meditation`) plus
  contract-specific substrings (§3).
- [x] D05 — SDK eval plan file-by-file (`evals/sdk/tests/q-meditate.test.ts`):
  1 literal swap + 4 new structural describe blocks containing 26 new
  unconditional `it` tests (§4).
- [x] D06 — Conftest changes: new `_read_meditation_artifact(kind, name)`
  helper + 2 new sample fixtures (`sample_meditation_working_dir`,
  `sample_init_suggestions_yml`); zero breaking changes to existing
  fixtures (§5).
- [x] D07 — Manual eval scenario updates for `evals/USER_EVAL_CHECKLISTS.md`
  (Q1 literal re-target + 3 new expected-outcome rows for richness gates
  + File Reference table additions for the new guide agent + six skills)
  and `evals/sdk/README.md` (Test Categories row update + helper
  resolution paragraph) (§6).
- [x] D08 — Regression guarantees pinning the 2026-05-24 freeze: modes /
  five gates (incl. `Q-Cost-and-Richness-Acknowledgment` and
  `Q-Finalisation-Enhancements`) / mandatory paired HTML+PDF / 13-dim
  adversarial loop with Dim 12 + Dim 13 / retrospective always-written
  / K10 layered cadence / K10c rubric / Comprehensiveness Level Mapping
  / canonical `additional_focus_areas[]` + `treatment:` filter; PLUS the
  full negative-assertion block (forbidden legacy field names + forbidden
  `crux-cursor-memory-manager` in `/crux-meditate` spawn context +
  forbidden Meditate executable headings in post-S07 memory-manager)
  (§7 + §8).
- [x] No linter errors introduced (markdown-only artefact; verified by
  `ReadLints` after write).

---

_Captured by `crux-platform-architect` against repo
`/home/andrewv/git/cursor/CRUX-Compress` on 2026-05-24. This plan is
the **contract** that subtask 08 must follow; deviations require an
explicit `needs_user_input` escalation surfaced through the calling
agent. Plan reads only `meditate-frozen-contract-20260524.md`,
`meditate-decomp-architecture-design-20260517.md`, the four eval
targets enumerated in the brief, `evals/USER_EVAL_CHECKLISTS.md`, and
`evals/sdk/README.md` — no edits to source code, install scripts,
docs, or web._
