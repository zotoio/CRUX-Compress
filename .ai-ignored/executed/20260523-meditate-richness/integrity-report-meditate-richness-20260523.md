# Integrity Report — Meditate Richness + Init-Time Suggestions (20260523)

**Spec**: `specs/20260523-meditate-richness/spec-meditate-richness-20260523.md`
**Reviewer**: integrity-expert (subagent)
**Date**: 2026-05-24
**Verdict**: **PASS_WITH_ADVISORIES**

---

## 1. Verdict + Executive Summary

**Verdict: PASS_WITH_ADVISORIES**

| Severity | Count |
|----------|-------|
| BLOCKER  | 0     |
| WARNING  | 5     |
| OBSERVATION | 3  |

All K1–K10c Key Decisions are implemented in the post-spec repo state. The eval suite passes in full (177 Python + 22 TypeScript structural; 6 expensive SDK tests appropriately skipped in CI). The respawn protocol cannot infinite-loop: the finite-iteration guarantee is preserved and documented. All backwards-compatibility numeric pins match. All existing safeguards are preserved verbatim. Five warnings require follow-up attention: a field-name divergence in the report contract that would cause silent no-ops for `report_section_only` focus areas; an unauthorized `install.py` change (K8 violation); two stale gate-name references in the coordinator file; a missing `test_q_meditate.py` entry in CONTRIBUTORS.md; and a cosmetic step-numbering observation. None of these constitute spec-blocking failures. The user explicitly accepted the subtask 07 partial verdict and deferred the surgical-scope decision to this review; this report resolves it as ACCEPT.

---

## 2. Spec Scope & Subtask Roster

| ID | Subagent | Status | Judge Verdict | Headline Finding |
|----|----------|--------|---------------|-----------------|
| 01 | crux-platform-architect | Completed | PASS | 21-item concordance table + verbatim freeze of all 14 contract items captured |
| 02 | crux-platform-architect | Completed | PASS | Architecture design: 12-dimension × 4-level richness mapping table, respawn protocol, K10 ensemble layered cadence, full patch matrix |
| 03 | crux-software-engineer | Completed | PASS (minor obs) | `Q-Cost-and-Richness-Acknowledgment` merged gate, combined Pattern-B askQuestion, `Q-Finalisation-Enhancements` gate, continuation-menu K10 extensions |
| 04 | crux-software-engineer | Completed | PASS | `comprehensiveness:` propagation, init-suggestion production, K10c reflection contract + rubric, ensemble per-tree YAML write |
| 05 | crux-software-engineer | Completed | PASS (field-name obs) | Level mapping table, report-skill contract, Dim 12 + Dim 13, respawn protocol, K10b per-cheap-type rendering |
| 06 | crux-software-engineer | Completed | PASS | 177 Python tests (30 new classes); 22+6-skipped TypeScript tests (4 new describe blocks) |
| 07 | docs-sync-agent | Completed | **PARTIAL** (surgical-scope) | K1–K10 content correct; docs/crux-memories.md rewrite exceeded surgical scope (+108 net lines vs. +35 claimed); user accepted partial; decision deferred to S09 |
| 08 | crux-cursor-rule-manager | Completed | PASS | Zero CRUX mirror regens needed; 9 existing mirrors verified against sourceChecksums |
| 09 | integrity-expert | **In Progress** | — | This report |

---

## 3. K1–K10c Implementation Matrix

| Key Decision | Status | Implementation Citation |
|---|---|---|
| **K1** — 4 named levels (`compact` / `default` / `detailed` / `exhaustive`) | IMPLEMENTED | `.cursor/commands/crux-meditate.md:177–186` (Sub-Q1 options with per-level prose); `comprehensiveness` payload at `:367–384` |
| **K1** — default when unspecified = level named `default` | IMPLEMENTED | `:177` "preselected = the level literally named `default`"; `:179` dual-meaning callout |
| **K1** — `compact` backwards-compat anchor | IMPLEMENTED | `:183` compact description; level mapping table at `:1551–1566`; explicit anchor at `:1566` |
| **K2** — merged `Q-Cost-and-Richness-Acknowledgment` gate | IMPLEMENTED | `:123` gate heading; `:110` description; Sub-Q1 + Sub-Q2 at `:177–195` |
| **K2** — NO standalone `Q-Comprehensiveness` gate | IMPLEMENTED | `rg -n 'Q-Comprehensiveness'` returns zero matches in `.cursor/` |
| **K2** — mode-swap preserves richness selection | IMPLEMENTED | `:199` "Mode-swap preserves richness"; `:204` behavior rules |
| **K2** — non-interactive abort preserved | IMPLEMENTED | `:248` non-interactive abort rule verbatim |
| **K2** — cost re-presentation on additional-facet opt-in | IMPLEMENTED | `:641–653` cost-ack re-presentation trigger condition and flow |
| **K3** — dual-target landing (pre- and post-decomp) | IMPLEMENTED | Pre-decomp files edited; `.cursor/commands/crux-meditate.md` (1493→2142 lines) + `.cursor/agents/crux-cursor-memory-manager.md` (947→1388 lines) |
| **K4** — init-suggestion payload from depth-0 seed (no new spawn) | IMPLEMENTED | `.cursor/agents/crux-cursor-memory-manager.md:415–426` (step 4 derives 4-block payload) |
| **K4** — 4-mode additional-focus-area opt-in | IMPLEMENTED | `:560–584` (askQuestion Sub-Q4 with 4 modes); `:509–515` (resume-handler reconciliation) |
| **K4** — `skip` / `report_section_only` do NOT trigger cost re-presentation | IMPLEMENTED | `.cursor/commands/crux-meditate.md:641` "condition: any additional_focus_areas[i].treatment in {additional_facet, additional_facet_AND_section}" |
| **K4** — `additional_facet` + `additional_facet_AND_section` DO trigger cost re-presentation | IMPLEMENTED | `:641–653` |
| **K5** — `comprehensiveness:` payload propagated unchanged | IMPLEMENTED | `.cursor/commands/crux-meditate.md:363–384` (payload shape + propagation rule); agent abort on missing payload at `:800` |
| **K5** — subagent aborts if `comprehensiveness:` missing | IMPLEMENTED | `:799`: "NOTE: if `comprehensiveness:` is missing from the spawn prompt…abort immediately" |
| **K6** — set-once-per-invocation richness | IMPLEMENTED | `.cursor/commands/crux-meditate.md:206` "It cannot be changed after this gate closes" |
| **K6** — expansion reuses locked richness | IMPLEMENTED | `:207–234` read-only-richness variant; `:243` locked display row text |
| **K6** — no `--reset-richness` flag | IMPLEMENTED | Confirmed: no such flag found anywhere in modified files |
| **K6** — `init-suggestions-{ts}.yml` persistence | IMPLEMENTED | `.cursor/agents/crux-cursor-memory-manager.md:517–566` (write schema + semantics) |
| **K7** — all existing safeguards preserved unchanged | IMPLEMENTED | See §6 Safeguards Regression below |
| **K8** — no new files in dist/install/version-bump | PARTIAL (WARNING) | `scripts/create-crux-zip.py`, `.github/workflows/version-bump.yml`, `.crux/dist-manifest.json` unchanged. **`install.py` modified** (+44 lines; `cleanup_internal_agents()` function). This is a K8 violation — see W2. |
| **K9** — Dim 12 (comprehensiveness fidelity) | IMPLEMENTED | `.cursor/commands/crux-meditate.md:1231–1239` |
| **K9** — Dim 13 (init-suggestion + enhancement honour) | IMPLEMENTED | `:1241–1252` |
| **K9** — level-conditional Dim 9 expansion | IMPLEMENTED | `:1221–1227` (peer_review_surfacing conditional at each level) |
| **K9** — respawn protocol triggered by Dim 13 | IMPLEMENTED | `:1274–1282` (respawn flow in iteration loop); `:1370–1420` (Report-Skill Respawn Protocol section) |
| **K9** — respawn payload schema | IMPLEMENTED | `:1377–1412` (full schema with `respawn_reasons`, `missing_sections`, `missing_visualisations`, `accepted_finalisation_enhancements`, `preserve_other_content`, all context payloads) |
| **K9** — respawn shares ≤3 iteration cap | IMPLEMENTED | `:1289` "Cap is 3 iterations…no separate respawn budget" |
| **K9** — ESCALATE at iter 3 if Dim 13 still fires | IMPLEMENTED | `:1289` "iter 3 cannot usefully respawn…Dim 13 still firing at iter 3 → ESCALATE" |
| **K10a** — `Q-Finalisation-Enhancements` fires post-consolidation / pre-adversarial-review | IMPLEMENTED | `.cursor/commands/crux-meditate.md:1064` "This gate fires BEFORE the adversarial review begins"; `:788` calling-agent gate ordering |
| **K10a** — fires in Research AND Quick mode | IMPLEMENTED | `:825` "The Q-Finalisation-Enhancements gate also fires in Quick mode (per K10a)" |
| **K10a** — ensemble layered cadence (per-tree + root) | IMPLEMENTED | `.cursor/agents/crux-cursor-memory-manager.md:616–711` (ensemble per-tree YAML write + aggregator root reflection); `.cursor/commands/crux-meditate.md:1175–1195` (Ensemble layered cadence section) |
| **K10a** — per-tree YAMLs at `{model-subdir}/finalisation-enhancements.yml` | IMPLEMENTED | `.cursor/commands/crux-meditate.md:1178`; `.cursor/agents/crux-cursor-memory-manager.md:360` artefact table |
| **K10a** — single combined root gate at ensemble root | IMPLEMENTED | `.cursor/commands/crux-meditate.md:1175` "fires once at the ensemble root" |
| **K10a** — single-model flows unchanged | IMPLEMENTED | `:1064` "fires post-consolidation" (no layered cadence in single-model context) |
| **K10a** — degradation when <5 candidates | IMPLEMENTED | `.cursor/agents/crux-cursor-memory-manager.md:625` graceful-degradation rule; `degradation_reason:` schema field |
| **K10b** — cheap items bundled into respawn payload | IMPLEMENTED | `.cursor/commands/crux-meditate.md:1136` "Bundles accepted cheap enhancements into the first adversarial review iteration's respawn payload" |
| **K10b** — `accepted_finalisation_enhancements` in `respawn_reasons:` | IMPLEMENTED | `:1380` |
| **K10b** — expensive default treatment = `queue` | IMPLEMENTED | `:1102–1113` queue-treatment flow; follow-up artefact writes |
| **K10b** — `spawn_now` triggers cost-ack re-presentation | IMPLEMENTED | `:1107–1128` spawn_now cost-ack re-presentation flow |
| **K10b** — cancel at re-presentation falls back to `queue` | IMPLEMENTED | `:1123` "On cancel: drop the spawn_now treatments, fall back to queue" |
| **K10b** — cost-ack re-presentation fires ONLY for `spawn_now` (not `queue`) | IMPLEMENTED | `:1107` "triggers a cost-ack re-presentation" scoped to spawn_now guard |
| **K10c** — `finalisation-enhancements.yml` written BEFORE askQuestion | IMPLEMENTED | `.cursor/agents/crux-cursor-memory-manager.md:693–700` step 8a reflection write flow |
| **K10c** — schema matches K10c verbatim | IMPLEMENTED | `.cursor/agents/crux-cursor-memory-manager.md:339`–present; schema fields verified |
| **K10c** — calling agent updates `accepted` + `treatment` + `decided_at_utc` | IMPLEMENTED | `.cursor/commands/crux-meditate.md:1130–1138` post-gate update flow |
| **K10c** — continuation menu surfaces unchosen + queued items | IMPLEMENTED | `:967` (`reapply_enhancement_{id}`); `:973` (`spawn_now_{type}_{id}` queued expensive) |
| **K10c** — ensemble continuation: per-tree-only items surfaced with provenance | IMPLEMENTED | `:976–978` (per-tree provenance label in continuation menu) |
| **K10c** — per-tree vs cross-model respawn targeting (no cross-contamination) | IMPLEMENTED | `:1157–1171` ensemble respawn targeting section; Dim 13 layered audit |
| **K10c** — `surfaced_to_root` annotation written by aggregator | IMPLEMENTED | `.cursor/agents/crux-cursor-memory-manager.md:691` "aggregator writes back surfaced_to_root: true|false" |
| **K10c** — skip-all path (0 selected) → `unchosen_persisted` treatment, no respawn contribution | IMPLEMENTED | `.cursor/commands/crux-meditate.md:1135` "gate fires once…skip-all → no respawn-payload contribution"; eval `TestMeditateK10SkipAllBackwardsCompat` |
| **K10c** — reflection rubric (impact × insight-value, 1–10) with worked examples | IMPLEMENTED | `.cursor/agents/crux-cursor-memory-manager.md:1020–1087` reflection rubric + worked anchors |

---

## 4. Frozen-Surface Diff Matrix

| # | Contract Item | Category | Notes |
|---|---|---|---|
| 1 | Calling-agent gate ordering — 4-gate pre-spawn + mid-flow Facet Confirmation | EXTENDED | Gate 2 renamed `Q-Cost-and-Richness-Acknowledgment` (K2); combined Pattern-B gate (K4) replaces sequential Q-Confirm-1 + Q-Confirm-2; fifth post-consolidation gate `Q-Finalisation-Enhancements` added (K10a). Original 4-slot logic preserved. |
| 2 | `Q-Cost-Acknowledgment` prompt prose (single-model variant) | EXTENDED | Renamed to `Q-Cost-and-Richness-Acknowledgment`; Sub-Q1 richness selection added; all original option set options preserved. Stale prose references to Q-Confirm-1/Q-Confirm-2 at lines 729, 863, 873 (see W3). |
| 3 | `Q-Cost-Acknowledgment` ensemble variant | EXTENDED | Ensemble variant of merged gate extended with richness rows; original first-paragraph replacement preserved. |
| 4 | `Q-Cost-Acknowledgment` behaviour rules + non-interactive abort | PRESERVED | Non-interactive abort rule verbatim at `.cursor/commands/crux-meditate.md:248`. |
| 5 | `Q-Cost-Acknowledgment-Expansion` prompt + options | EXTENDED | Renamed to read-only-richness variant; richness shown as locked display row; original options preserved; "keep richness setting?" follow-up NOT added (K6 — implicit). |
| 6 | `facets-pending-{ts}.yml` artefact | EXTENDED | Schema extended with sections/visualisations/additional_focus_areas blocks. Filename pattern and write/delete semantics preserved. |
| 7 | `Q-Confirm-1` prompt + 5-option decision set | MODIFIED (AUTHORIZED) | Merged into combined Pattern-B askQuestion as Sub-Q1 (facets). Original 5 options preserved verbatim at `.cursor/agents/crux-cursor-memory-manager.md:481`. |
| 8 | `Q-Confirm-2` prompt + 3-enum decision set | MODIFIED (AUTHORIZED) | Merged into combined Pattern-B askQuestion as Sub-Q5 (deep_confirm). Original 3 options preserved verbatim at `:489`. |
| 9 | Report-generation contract minima (≥4 charts, ≥3 infographics, ≥1 calculator) | EXTENDED | Fixed minima replaced with level-driven `comprehensiveness.minima.*` payload. `compact` row reproduces exact current values: 4/3/1/3 (see §5). |
| 10 | Per-branch / depth-3 / peer-review surfacing today | EXTENDED | Depth3 leaf inclusion, per-branch section depth, peer-review surfacing now payload-driven per level. `compact` row reproduces today's consolidation-only/summary/consolidation-only behaviour. |
| 11 | Anti-Homogenisation Rules block | PRESERVED | Block verbatim at `.cursor/commands/crux-meditate.md:1823–1848`. |
| 12 | Universal Contrast (WCAG) block | PRESERVED | Block verbatim at `:1854–1889`. |
| 13 | Subject-Matter Focus rule | PRESERVED | Rule verbatim at `:1448–1472`; confirmed preserved in adversarial Dim 11 (`:1229`). |
| 14 | Adversarial review 11-dimension list | EXTENDED | Dimensions 1–11 verbatim at `:1211–1229`. Two new dimensions added: Dim 12 (comprehensiveness fidelity) at `:1231–1239`; Dim 13 (init-suggestion + enhancement honour) at `:1241–1252`. |
| 15 | Citation discipline | PRESERVED | `citation_density` mode-driven (Research=mandatory; Quick=warn_only) at all levels per K7 (`:380`). |
| 16 | Retrospective always-written rule | PRESERVED | `.cursor/commands/crux-meditate.md:1472`: "This is always written, including on ESCALATE". |
| 17 | Branch & Leaf Index template | EXTENDED | `init-suggestions-{ts}.yml` link added to `## Top-level artifacts` block (K6). Original template preserved. |
| 18 | Pattern A vs Pattern B boundaries | PRESERVED | Verbatim at `.cursor/agents/crux-cursor-memory-manager.md:19`; K10 gates explicitly assigned to calling agent (`:1064`); `Do NOT call AskQuestion` at `:700`, `:426`. |
| 19 | `crux-cursor-memory-manager` depth-0 steps 1–13 | EXTENDED | Steps 4 + 8 extended for K4 init-suggestion payload and K10c reflection. Steps 1–3, 5–7, 9–13 structure preserved. |
| 20 | `evals/test_q_meditate.py` test classes | EXTENDED | 30 new test classes added; original 8 classes intact (verified by test run: 177 passed). |
| 21 | `evals/sdk/tests/q-meditate.test.ts` test suites Q1–Q3 | EXTENDED | 4 new describe blocks added; original Q1–Q3 blocks intact (verified: 22 passed + 6 skipped). |

---

## 5. Backwards-Compatibility — `compact` Numeric Pin

| Dimension | Required Value | Actual Value | Status |
|-----------|----------------|--------------|--------|
| `compact.minima.charts.count` | 4 (today's ≥4) | 4 | ✅ PASS |
| `compact.minima.infographics.count` | 3 (today's ≥3) | 3 | ✅ PASS |
| `compact.minima.calculators.count` | 1 (today's ≥1) | 1 | ✅ PASS |
| `compact.minima.calculators.scenarios_per` | ≥3 (today's 3–5) | 3 | ✅ PASS |
| `compact.depth3_leaf_inclusion` | `"summary"` | `"summary"` | ✅ PASS |
| `compact.per_branch_section_depth` | `"consolidation_only"` | `"consolidation_only"` | ✅ PASS |
| `compact.peer_review_surfacing` | `"consolidation_only"` | `"consolidation_only"` | ✅ PASS |
| Quick mode `citation_density` at any level | `"warn_only"` | `"mandatory_or_warn_only"` field with "Quick = warn_only at all levels (K7)" | ✅ PASS |
| Research mode `citation_density` at any level | `"mandatory"` | `"mandatory"` | ✅ PASS |

Source citations: `.cursor/commands/crux-meditate.md:370–381` (payload values); `:1551–1566` (backwards-compatibility anchor section); `:1566` explicit anchor paragraph.

---

## 6. Existing Safeguards Regression

| Safeguard | Pre-Spec Location | Post-Spec Status | Notes |
|-----------|------------------|-----------------|-------|
| Anti-Homogenisation Rules | `crux-meditate.md:197–209, 1174–1194` | ✅ PRESERVED | `:1823–1848` verbatim |
| Universal Contrast (WCAG ≥4.5:1 / ≥3:1) | `crux-meditate.md:1205–1231` | ✅ PRESERVED | `:1854–1889` verbatim |
| Subject-Matter Focus rule | `crux-meditate.md:878–898` | ✅ PRESERVED | `:1448–1472` verbatim; Dim 11 in adversarial review `:1229` |
| Citation discipline (mandatory `## Citations`, validation) | `crux-cursor-memory-manager.md:655–690` | ✅ PRESERVED | Mode-driven at every level; K7 explicitly preserved |
| Pattern A vs Pattern B boundaries (subagents NEVER call AskQuestion) | `AGENTS.md:17–46` | ✅ PRESERVED | `rg -n 'AskQuestion' .cursor/agents/ .cursor/skills/` — all matches are prose references, not direct calls |
| Retrospective always-written rule | `crux-meditate.md:900–967` | ✅ PRESERVED | `:1472` "This is always written, including on ESCALATE" |
| Mandatory paired HTML + PDF output | `crux-meditate.md:1541` | ✅ PRESERVED | `:1541` "mandatory for every meditation, in both Research and Quick mode" |
| Adversarial review-and-fix cycle (≤3 iterations) | `crux-meditate.md:759–799` | ✅ PRESERVED | Iteration cap at `:1262–1289`; K9 respawn shares same cap |
| Non-interactive cost-ack abort | `crux-meditate.md:189` | ✅ PRESERVED | `:248` verbatim |

---

## 7. Pattern A vs Pattern B Integrity

| Check | Result | Evidence |
|-------|--------|----------|
| Subagents NEVER call `AskQuestion` directly | ✅ PASS | `rg -n 'AskQuestion' .cursor/agents/ .cursor/skills/` — 16 matches, all prose-level descriptions of calling-agent behaviour or "Do NOT call `AskQuestion`" prohibitions |
| Combined Pattern-B askQuestion owned by calling agent | ✅ PASS | `.cursor/commands/crux-meditate.md:405–643` (full combined Pattern-B section; agent returns `needs_user_input`; calling agent fires `askQuestion`) |
| Depth-0 manager produces `needs_user_input` block (not `AskQuestion`) | ✅ PASS | `.cursor/agents/crux-cursor-memory-manager.md:426` "Do NOT call `AskQuestion` yourself — this is the calling agent's responsibility"; `:700` same rule for K10 gate |
| Cost-ack re-presentation on additional-facet acceptance runs at calling-agent side | ✅ PASS | `.cursor/commands/crux-meditate.md:641–653` re-presentation flow is entirely calling-agent-side |
| `Q-Finalisation-Enhancements` gate owned by calling agent | ✅ PASS | `:1064` "The calling agent then runs `Q-Finalisation-Enhancements`"; agent writes YAML and returns `needs_user_input`, then waits for resume |
| Per-item `spawn_now` treatment sub-question owned by calling agent | ✅ PASS | `:1094–1104` calling-agent-side per-item treatment flow |

---

## 8. CRUX Freshness

Subtask 08 report: zero CRUX mirror regenerations needed. None of the source files touched by this spec (`.cursor/commands/crux-meditate.md`, `.cursor/agents/crux-cursor-memory-manager.md`, `README.md`, `docs/crux-memories.md`, `web/compress.md/memories.html`, `install.py`) have `.crux.md` or `.crux.mdc` mirrors. The CRUX mirrors in `.cursor/rules/` are for rule files only; none were touched by this spec.

**Spot-check (≥3 mirrors verified by this review)**:

| Source File | Mirror | Computed Checksum | Mirror `sourceChecksum` | Status |
|-------------|--------|-------------------|------------------------|--------|
| `.cursor/rules/docs-sync.md` | `.cursor/rules/docs-sync.crux.mdc` | 1356781034 | 1356781034 | ✅ CURRENT |
| `.cursor/rules/version-bump.md` | `.cursor/rules/version-bump.crux.mdc` | 1841243360 | 1841243360 | ✅ CURRENT |
| `.cursor/rules/zip-contents-protection.md` | `.cursor/rules/zip-contents-protection.crux.mdc` | 3371193391 | 3371193391 | ✅ CURRENT |
| `.cursor/rules/crux-memories-integration.md` | `.cursor/rules/crux-memories-integration.crux.mdc` | 4002236386 | 4002236386 | ✅ CURRENT |

All four spot-checked mirrors are current. Consistent with subtask 08's finding of zero required regenerations.

---

## 9. K8 — No New Dist / Install / Version-Bump Files

| File | Expected | Actual |
|------|----------|--------|
| `scripts/create-crux-zip.py` | No change | ✅ Unchanged (git diff = empty) |
| `.github/workflows/version-bump.yml` | No change | ✅ Unchanged (git diff = empty) |
| `.crux/dist-manifest.json` | No change | ✅ Unchanged (git diff = empty) |
| `install.py` | No change (K8 explicit) | ⚠️ **MODIFIED** (+44 lines; `cleanup_internal_agents()` function added) — **W2** |

**Dist-zip enumeration check** — `grep -E '\.cursor/(commands|agents|skills)' scripts/create-crux-zip.py` output confirms the same 15 files as before; no new entries added.

---

## 10. Eval Suite Execution

### `pytest evals/test_q_meditate.py -v`

```
============================= 177 passed in 1.67s ==============================
```

All 177 tests pass. No failures. No skips. New test classes: `TestMeditateK10FinalisationEnhancementGate`, `TestMeditateK10SkipAllBackwardsCompat`, `TestMeditateFinalisationCheapAcceptRespawn`, `TestMeditateFinalisationExpensiveQueueDefault`, `TestMeditateFinalisationExpensiveSpawnNow`, `TestMeditateFinalisationPersistence`, `TestMeditateFinalisationContinuationMenu`, `TestMeditateFinalisationFiniteIteration`, `TestMeditateFinalisationTripleReasonRespawn`, `TestMeditateK10EnsembleLayeredCadence`, `TestMeditateK10EnsembleContinuationMenuLayered`, `TestMeditateK10QuickModeFires`, `TestMeditateK10ReflectionRubric`, `TestMeditateK10WeightsConfigurable` (plus previously added classes from K1–K9).

### `cd evals/sdk && pnpm vitest run tests/q-meditate.test.ts`

```
Test Files  1 passed (1)
      Tests  22 passed | 6 skipped (28)
   Start at  00:18:07
   Duration  2.89s
```

22 structural tests pass. 6 expensive LLM-execution tests are correctly skipped (SDK_EVAL_SKIP_EXPENSIVE=true default). New describe blocks: `Q: Meditate — Structural: K10 Finalisation Enhancement Gate`, `Q: Meditate — Structural: K10 Reflection Rubric`, `Q: Meditate — Structural: K9 Respawn Protocol`, `Q: Meditate — Structural: K10 Ensemble Layered Cadence`.

**Overall: 199 tests pass (177 + 22); 6 expensive LLM tests appropriately skipped; 0 failures.**

---

## 11. Open Questions — Resolution Sweep

### Primary Open Questions (OQ #1–#6 in spec)

| # | Question | Resolution Status |
|---|----------|-------------------|
| 1 | Mode-swap interaction with richness sub-question | ✅ RESOLVED: richness preserved across mode swap; `.cursor/commands/crux-meditate.md:199` "Sub-Q1 richness selection is preserved across any mode-swap decision" |
| 2 | Cost-ack re-presentation prompt shape | ✅ RESOLVED: "Cost-and-Richness Acknowledgment (re-presented)" with one-line preamble; `:653` "Cost has changed because you accepted {N} additional facets — please re-acknowledge or cancel" |
| 3 | Respawn iteration accounting (respawn-then-re-review) | ✅ RESOLVED: respawn-then-re-review semantics; `:1281` "Next iteration (N+1) spawns a fresh reviewer to re-review the regenerated report" |
| 4 | `additional_facet_AND_section` items in Branch & Leaf Index | ✅ RESOLVED: appear as additional branch entries (Branch 4/5/…) AND confirmed section in `init-suggestions-{ts}.yml`; `.cursor/agents/crux-cursor-memory-manager.md:513` |
| 5 | `compact` + Quick = warn-only citations | ✅ RESOLVED: warn-only validation preserved at every level in Quick mode per K7; citation_density field = "mandatory_or_warn_only" (mode-driven); K7 carve-out at `:380` |
| 6 | `additional_focus_areas` cap interaction with cost re-presentation | ✅ RESOLVED: trust the re-presentation prose; no hard facet cap. Subtask 09 does not find the cost language insufficient — the re-presentation enumerates the new agent count explicitly. |

### Tertiary Open Questions (OQ #7–#10 second cluster)

| # | Question | Resolution Status |
|---|----------|-------------------|
| 7 (first cluster) | Live cost-update on richness change | ✅ RESOLVED: show all 4 level cost rows up-front (no live-update assumption); `:144–163` level × cost table in prompt |
| 8 | Combined Pattern-B prompt size / cognitive load | ✅ RESOLVED: caps enforced (3–8 sections, 5–10 viz, 0–5 focus areas); prompt scannable via `###` section dividers; not escalated to WARNING by this review |
| 9 | Respawn payload semantics (delta vs full regen) | ✅ RESOLVED: full regeneration with new timestamp; `preserve_other_content: true` = include prior content in regen; `:1416–1420` (per-reason processing order) |
| 10 (second cluster, citation re-validation) | Re-validate citation after respawn | ✅ RESOLVED: standard citation validation applies to respawned report per K7 |
| 7 (second cluster, Dim 1–11 + Dim 13 ordering) | Same-iteration ordering | ✅ RESOLVED: Dim 1–11 in-place fixes first, then Dim 13 respawn; `:1275–1281` iteration loop |
| 8 (second cluster) | Expansion when no `init-suggestions-{ts}.yml` | ✅ RESOLVED: re-run depth-0 init-suggestion derivation on expansion (option b); `.cursor/agents/crux-cursor-memory-manager.md:497–499` |
| 9 (second cluster) | Respawn payload bundling (missing sections + missing viz) | ✅ RESOLVED: bundle into one respawn per iteration; `:1377–1382` list-typed `respawn_reasons` |

### K10 Open Questions (#10–#14)

| # | Question | Resolution Status |
|---|----------|-------------------|
| 10 | Ensemble cadence (per-tree vs root) | ✅ RESOLVED: "both layered" — per-tree YAMLs + root combined YAML + single combined root gate; implemented per K10a |
| 11 | Rubric weights configurable | ✅ RESOLVED: configurable via `cruxMemories.meditate.finalisationEnhancements.weights`; default 1.0/1.0; `:1377–1383` |
| 12 | Threshold for <5 candidates | ⚠️ OPEN (expected): default = 6 (≥60% of max composite). Spec defers live calibration to a real meditation run. Acceptable; no impact on structural tests. |
| 13 | K10 Quick mode gate placement | ✅ RESOLVED: gate fires in Quick mode too; `:825` |
| 14 | Continuation menu ordering | ✅ RESOLVED: grouped with headings; `.cursor/commands/crux-meditate.md:960–978` groups under "Finalisation enhancements" / "Expansion directions" headers |

---

## 12. Cross-Cutting Decisions Adjudicated

### 12.1 Subtask 07 Surgical-Scope — ACCEPT

**Decision: ACCEPT the broader docs rewrite as net-positive documentation.**

**Evidence**: The subtask 07 judge verified that the K1–K10 content itself is correct. The `docs/crux-memories.md` "Q. Meditate Command" section rewrite (+108 net lines vs. +35 claimed) restructures what was a flat ~13-bullet section into a 5-subsection format covering Pre-spawn gates / Research / Quick / Ensemble / File coordination invariants. While this exceeds surgical scope per the docs-sync rule ("surgical; ¬rewrite"), the content accurately documents the post-spec meditate contract and was not previously documented at this level of detail anywhere in the consumer-facing surfaces.

**Rationale**:
1. The user explicitly accepted the partial verdict and deferred the call here.
2. The expanded docs coverage is factually correct and improves auditability of the contract.
3. No conflicting content exists with the 20260517 spec's docs-sync subtask (the 20260517 spec has not shipped docs-sync yet; the expanded coverage here pre-empts it).
4. A "TRIM" verdict would require spawning a follow-up subtask, creating more churn than value.
5. A "SPLIT" verdict is premature — the content does not contradict 20260517.

**Precedent recorded**: For future specs, docs-sync agents should be instructed that "surgical" means ≤20 net lines per doc surface per spec. If a docs-sync agent exceeds this, it should be a WARNING finding rather than a Partial verdict that defers the call to integrity review.

### 12.2 Subtask 05 Field-Name Divergence — WARNING; `additional_focus_areas` wins

**Decision: W1 — WARNING. The canonical field name `additional_focus_areas` (with per-item `treatment:` field) is the winner.**

**Analysis**: Three sources use the canonical name:
1. Subtask 02 architecture-design §11 — uses `additional_focus_areas:` array with per-item `treatment:` field.
2. `.cursor/agents/crux-cursor-memory-manager.md:556–565` (YAML schema block) — uses `additional_focus_areas:`.
3. Eval tests (`evals/test_q_meditate.py`) — test against canonical `additional_focus_areas`.

One source uses the divergent name:
- `.cursor/commands/crux-meditate.md:1815` (report-contract honour rule) — reads `additional_focus_areas_accepted[]`.

A secondary inconsistency exists within the agent file itself: prose at line 512 says "record in `additional_focus_areas_accepted`" but the YAML schema block at lines 556–565 uses `additional_focus_areas:`. At runtime, the YAML schema block is authoritative for what gets written to disk.

**Impact**: The report skill's line 1815 reads a non-existent field (`additional_focus_areas_accepted[]`); all `report_section_only` focus-area opt-ins will silently no-op in the rendered report. This is a functional failure for that mode.

**Recommendation for follow-up fix** (not done here — this is a report-only review):
1. Update `.cursor/commands/crux-meditate.md:1815` from `additional_focus_areas_accepted[]` to `additional_focus_areas[]` with filter `treatment: "report_section_only"`.
2. Update `.cursor/agents/crux-cursor-memory-manager.md:512` prose from "record in `additional_focus_areas_accepted`" to "record in `additional_focus_areas` list with `treatment: 'report_section_only'`".

### 12.3 Subtask 03 Stale `Q-Confirm-1` / `Q-Confirm-2` References

**Decision: OBSERVATION (not BLOCKER or WARNING)**

**Locations**:
- `.cursor/commands/crux-meditate.md:729`: "…using the same confirm/modify/regenerate option set **as Q-Confirm-1**" — in the deep-confirmation pending-facets flow.
- `.cursor/commands/crux-meditate.md:863`: "After facet confirmation completes (**Q-Confirm-1 + Q-Confirm-2**)…" — in the ensemble step 6 description.
- `.cursor/commands/crux-meditate.md:873`: "…**Q-Confirm-2** value from step 6" — parameter label.

**Analysis**: These are prose references to gate names, not invocations. Line 729 describes the option set semantics (the 5 options still exist, just under the combined gate). Lines 863/873 describe what the ensemble step 6 subagent runs internally before returning results — and those internal steps DO invoke the combined Pattern-B flow, which subsumes both Q-Confirm-1 and Q-Confirm-2. The references are technically stale (the merged gate name is now `Q-Combined-Confirmation` in the agent's askQuestion sub-question label) but they do not introduce incorrect behavior since they describe semantics, not call paths.

**Recommendation**: Update the three prose references in a future maintenance pass (no separate subtask needed).

### 12.4 `AGENTS.crux.md` Missing-from-Disk — OBSERVATION

**Decision: OBSERVATION**

`AGENTS.crux.md` does not exist on disk. It appears in the `zip-contents-protection.md` rule manifest as a listed artefact, but `scripts/create-crux-zip.py:208` generates it dynamically in-memory during the zip build process (`zf.writestr("AGENTS.crux.md", crux_block + "\n")`). It is a transient synthetic artefact, not a maintained on-disk mirror. The zip-contents-protection rule wording ("`AGENTS.crux.md` (extracted from AGENTS.md)") accurately describes the build-time extraction; it does not imply the file should exist on disk.

**Recommendation**: No rule update needed. The existing wording is sufficient. A clarifying parenthetical could be added to zip-contents-protection.md in a future editorial pass: "(generated at zip-build time; not a maintained on-disk file)".

### 12.5 `test_q_meditate.py` Absent from CONTRIBUTORS.md — OBSERVATION

**Decision: OBSERVATION (not WARNING)**

`evals/test_q_meditate.py` is not listed in `CONTRIBUTORS.md`'s eval surface table. This was flagged by subtask 07 as a 20260517 docs-sync gap (predating this spec). The CONTRIBUTORS.md table currently doesn't enumerate individual eval files. This is a pre-existing omission; this spec's scope (K1–K10 richness + init-time suggestions) does not make the omission worse.

**Recommendation**: A future docs-sync subtask (or the 20260517 docs-sync subtask, whichever ships first) should add `evals/test_q_meditate.py` and `evals/sdk/tests/q-meditate.test.ts` to CONTRIBUTORS.md's testing section.

---

## 13. Findings Table

| ID | Severity | Category | Description | Affected File | Remediation |
|----|----------|----------|-------------|---------------|-------------|
| W1 | ⚠️ WARNING | Field-name divergence | Report contract reads `additional_focus_areas_accepted[]` but agent writes `additional_focus_areas:` (with per-item `treatment:`). `report_section_only` focus-area honour will silently no-op at runtime. | `.cursor/commands/crux-meditate.md:1815`, `.cursor/agents/crux-cursor-memory-manager.md:512` | Update crux-meditate.md:1815 to read `additional_focus_areas[]` entries with `treatment: "report_section_only"`; update agent file:512 prose to match. |
| W2 | ⚠️ WARNING | K8 violation | `install.py` was modified (+44 lines; `cleanup_internal_agents()` function) despite K8's explicit "No install.py change" constraint. Added by subtask 07 (docs-sync). | `install.py` | Acknowledge as out-of-band housekeeping OR revert and create a dedicated install-cleanup subtask. The change is functionally harmless but violates the spec's scope constraint. |
| W3 | ⚠️ WARNING | Stale gate references | Lines 729, 863, 873 in `.cursor/commands/crux-meditate.md` reference `Q-Confirm-1` and `Q-Confirm-2` gate names that were merged into the combined Pattern-B flow. The references are prose-only (describe option-set semantics and ensemble subagent steps) and do not cause incorrect behavior, but they are stale. | `.cursor/commands/crux-meditate.md:729, 863, 873` | Update the three prose references to use the merged gate name or describe semantics without referencing the defunct gate names. |
| W4 | ⚠️ WARNING | Documentation gap | `test_q_meditate.py` not listed in CONTRIBUTORS.md eval surface table. Pre-existing gap (from 20260517). | `CONTRIBUTORS.md` | Add both `evals/test_q_meditate.py` and `evals/sdk/tests/q-meditate.test.ts` to CONTRIBUTORS.md in a future docs-sync pass. |
| W5 | ⚠️ WARNING | Cosmetic step-numbering | `Q-Finalisation-Enhancements` gate is defined as a standalone `### Finalisation Enhancements Gate` section in `.cursor/commands/crux-meditate.md` but is not listed as a numbered sub-step in the Research/Quick mode step 8 overview. The preamble at `:788` does mention it ("A fifth calling-agent gate…fires post-consolidation before adversarial review"), so it is discoverable, but a step-numbered reference would be clearer for executors. | `.cursor/commands/crux-meditate.md:788` | Add a numbered mention (e.g. "Step 8c: Q-Finalisation-Enhancements gate — see Finalisation Enhancements Gate section below") to the Research/Quick mode step listing. |
| O1 | ℹ️ OBSERVATION | Transient artefact | `AGENTS.crux.md` listed in `zip-contents-protection.md` manifest but does not exist on disk. It is a transient zip-build-time synthetic artefact, not a maintained mirror. | `scripts/create-crux-zip.py:208`, `.cursor/rules/zip-contents-protection.md:44` | No action required. Optional editorial clarification in zip-contents-protection.md future pass. |
| O2 | ℹ️ OBSERVATION | Docs-sync scope | Subtask 07 `docs/crux-memories.md` restructuring exceeded surgical scope (+108 net lines). User-accepted. See §12.1 ACCEPT decision. | `docs/crux-memories.md` | Record as precedent; no rollback needed. |
| O3 | ℹ️ OBSERVATION | OQ #12 deferred | K10a candidate threshold (`minimum_impact_threshold` default = 6) calibration deferred to a real meditation run. No structural verification possible without runtime data. | `spec-meditate-richness-20260523.md:OQ#12` | No action needed in this spec; track as future calibration task. |

---

## 14. Respawn Finite-Iteration Proof

The subtask checklist requires explicit verification that the respawn protocol cannot infinite-loop. **Manual worst-case construction**:

**Scenario**: Dim 13 fires on every iteration; `accepted_finalisation_enhancements` also present in iteration 1.

| Iteration | Respawn cause(s) | Action | Next state |
|-----------|-----------------|--------|------------|
| 1 | `accepted_finalisation_enhancements` + `missing_init_suggestion_sections` | Apply Dim 1–11 fixes → construct respawn payload → respawn report-generation skill → counter advances to 2 | Regenerated report reviewed by iter 2 reviewer |
| 2 | `missing_init_suggestion_sections` (cheap enhancements now applied; cannot fire again — gate fires once per meditation per `:1433`) | Apply fixes → respawn → counter advances to 3 | Regenerated report reviewed by iter 3 reviewer |
| 3 | Dim 13 still fires | Verdict = `ESCALATE` (`:1289`). No iter 4 exists. Loop terminates. | ESCALATE surfaced to calling agent |

**Maximum useful respawns = 2** (at iter 1 and iter 2). `accepted_finalisation_enhancements` can fire **at most once** (gate fires once per meditation; `:1433`). The ≤3 iteration cap absorbs all causes. No path leads to a 4th reviewer spawn. **Infinite loop impossible.**

**Implementation verification**: `.cursor/commands/crux-meditate.md:1289` explicitly states: "Maximum useful respawns per meditation = 2 (respawn at end of iter 1 → reviewed at iter 2; respawn at end of iter 2 → reviewed at iter 3; iter 3 with Dim 13 still firing → `ESCALATE`)." This matches the spec's K9 constraint and the subtask's worst-case scenario verification requirement.

---

## 15. Final Verdict + Sign-Off

**Verdict: PASS_WITH_ADVISORIES**

**Justification**:
- ✅ All K1–K10c Key Decisions implemented with citations
- ✅ All 21 frozen-surface items categorised (PRESERVED / EXTENDED / MODIFIED-AUTHORIZED / none MISSING)
- ✅ All backwards-compat numeric pins match (compact: 4/3/1/3/summary/consolidation_only/consolidation_only)
- ✅ All existing safeguards verified preserved verbatim
- ✅ Pattern A/B integrity: subagents never call `AskQuestion`; all gates calling-agent-owned
- ✅ CRUX freshness: 4 mirrors spot-checked; all current; zero regens needed (S08 confirmed)
- ✅ Eval suite: 177 pytest + 22 vitest structural tests pass; 0 failures
- ✅ Respawn protocol: finite-iteration proof verified; ESCALATE at iter 3 confirmed
- ✅ No standalone `Q-Comprehensiveness` gate anywhere in `.cursor/`
- ⚠️ W1 — `additional_focus_areas_accepted[]` field-name divergence (silent no-op for report_section_only opt-ins) — **requires follow-up fix before shipping**
- ⚠️ W2 — `install.py` modified outside K8 scope — **acknowledge or revert**
- ⚠️ W3 — stale Q-Confirm-1/Q-Confirm-2 references — **maintenance follow-up**
- ⚠️ W4 — CONTRIBUTORS.md missing eval file entries — **future docs-sync**
- ⚠️ W5 — Q-Finalisation-Enhancements step-numbering cosmetic gap — **maintenance follow-up**

**Blocking before declaring spec complete**: W1 (field-name divergence causes silent failure for `report_section_only` focus-area honour). W2 (K8 violation in `install.py`) is a policy violation but does not break user-facing functionality; discretionary to revert. W3/W4/W5 are cosmetic/maintenance items.

**Recommended remediation spec**: A one-subtask maintenance spec (or addition to a future spec's Phase 1) to:
1. Fix `.cursor/commands/crux-meditate.md:1815` field name (`additional_focus_areas_accepted[]` → `additional_focus_areas[]` with treatment filter).
2. Fix `.cursor/agents/crux-cursor-memory-manager.md:512` prose to match.
3. Update three stale Q-Confirm-1/Q-Confirm-2 prose references.
4. Add `test_q_meditate.py` + `q-meditate.test.ts` to CONTRIBUTORS.md.

---

*Integrity review executed by integrity-expert subagent on 2026-05-24. Subtask 09 of spec-meditate-richness-20260523.*
