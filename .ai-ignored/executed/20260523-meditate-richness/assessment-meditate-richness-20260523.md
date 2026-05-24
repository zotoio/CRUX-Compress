# Spec Assessment — Meditate Comprehensiveness + Init-Time Suggestions

- **Spec**: `specs/20260523-meditate-richness/spec-meditate-richness-20260523.md`
- **Date**: 2026-05-23
- **Reviewer**: `zoto-spec-judge`
- **Mode**: Spec assessment + auto-apply

## Executive Summary

The spec is structurally sound, mature, internally cross-referenced, and faithfully encodes the 6 user-confirmed decisions (K1–K2 / K4 / K6 / K9). The 9-subtask manifest cleanly maps to the spec's four concerns (default report richness raised; user-selectable comprehensiveness; init-time section + visualisation suggestions; init-time additional focus areas). Agent allocation respects the CRUX-Compress repo's project-internal rule — every subtask is bound to a CRUX-specific agent (`crux-platform-architect`, `crux-software-engineer`, `crux-cursor-rule-manager`, `docs-sync-agent`, `integrity-expert`); none default to `generalPurpose`. The patch matrix in subtask 02 / K3 is the central mechanism for handling the pre-decomposition vs post-decomposition landing surfaces and it is well structured.

The remaining gaps are wording-and-completeness in flavour, not architectural. Most have been auto-applied; a small set is surfaced for the human reviewer.

**Verdict**: `READY_WITH_FIXES` (post-fix).

## Per-Dimension Findings (against the 10 adversarial priorities)

### 1. Functional preservation of the frozen meditate contract — `SHOULD_FIX` (auto-applied)

K7 explicitly preserves every existing safeguard. The patch matrix in subtask 02 enumerates both pre-decomp and post-decomp targets per contract surface, and subtask 09 verifies the resolution at execution time. Pattern A vs Pattern B integrity is preserved (subagents never call `AskQuestion`; the combined Pattern-B askQuestion is owned by the calling agent).

One inconsistency found: `subtask-01-meditate-richness-contract-capture-20260523.md` §13 (Cost-ack expansion variant) said _"The new spec extends this with an optional 'keep comprehensiveness setting?' follow-up."_ This contradicts K6 ("set-once-per-invocation; no `--reset-richness` flag; expansion variant does NOT offer a 'keep richness setting?' follow-up — the answer is implicit"). Auto-applied: subtask 01 rewritten to align with K6.

### 2. Naming-collision risk for the level *named* `default` — `SHOULD_FIX` (auto-applied)

K1 has an explicit "Naming reconciliation" paragraph; subtask 03's decision-guidance prose for the `default` level calls out the dual meaning; subtask 07 (docs-sync) is instructed to call out the dual meaning. The main residual collision risk was the spec line in K2:

> Sub-Q1 — Richness level (single-select, default `default`)

The phrasing "default \`default\`" reads as a typo to a cold-reading executor. Auto-applied: tightened to _"Sub-Q1 — Richness level (single-select, preselected = the level literally named `default`)"_ and made the same fix in subtask 03 / subtask 06 / DoD where the same phrasing appeared verbatim.

### 3. Merged-gate cost-formula correctness — `MUST_FIX` (auto-applied)

K2 enumerates which subsystems gain richness multipliers but is silent on the **agent-count vs token-cost split** at the spec level. The phrasing "per-leaf citation-table generation passes (only at `exhaustive`), per-branch dedicated section pass (`detailed` and `exhaustive`), peer-review surfacing dedicated-section pass (`detailed` and `exhaustive`)" reads as if each of these spawns additional agents, but the trailing bullet ("the size of each leaf agent's output … affects token cost but not agent count") suggests the report-generation-side passes don't add agents either. An executor reading K2 cold cannot tell whether `detailed` and `exhaustive` actually spawn _more meditation agents_ or whether they only enlarge the report-generation skill's output.

Auto-applied to K2:
- Added an "agent-count vs token-cost" sentence that names which multipliers are agent-count (the per-leaf citation-table pass) and which are token-cost only (per-branch dedicated section pass and peer-review surfacing pass live inside the report-generation skill, not as extra agent spawns).
- Added a worked-example table for depth 3 × Research mode showing approximate per-tree agent count and approximate report-skill token cost per level so subtask 02 has a numeric starting point for the multiplier table.
- Cross-referenced the cost-re-presentation rule from K4 so executor knows exactly which acceptance modes trigger the re-presentation.

### 4. Respawn protocol non-infinite-loop guarantee — `PASS`

The proof is clean: ≤3 iteration cap × respawn-counts-as-1-iteration × deterministic respawn payload = bounded total work. ESCALATE is reachable when `reviewer_iteration == 3` and Dim 13 still fires. Subtask 02 has a written proof; subtask 06 has `TestMeditateRespawnFiniteIteration`; subtask 09 reconstructs the worst-case scenario as a verification step.

Open issue surfaced as a new tertiary OQ (see Open Questions section below): same-iteration interaction between Dim 1–11 in-place fixes and a Dim-13 `respawn_required` finding (does the in-place fix get applied before respawn, or is it overwritten by respawn output?). Recommended for subtask 02 to nail down — flagged as a new lower-severity OQ, not a blocker.

### 5. 4-mode opt-in completeness — `SHOULD_FIX` (auto-applied)

All four modes (`skip` / `additional_facet` / `report_section_only` / `additional_facet_AND_section`) have explicit downstream effects in K4 and per-subtask deliverables. One ambiguity: K4 says `additional_facet` (without `_AND_section`) "does not add a dedicated report section beyond what the new branch's findings naturally produce", but the spec doesn't say what "naturally produce" means at the `compact` and `default` levels (which per K5/subtask 05 have `per_branch_section_depth = consolidation_only` or `branch_summary`, neither of which is a dedicated section).

Auto-applied: K4 reworded to spell out that at `compact` / `default`, an `additional_facet`-only opt-in contributes its findings only via the across-branch consolidation prose; at `detailed`+, the standard per-branch section rule already covers it.

| Mode | Facet count change | Report section added | Cost-ack re-presentation trigger | Branch & Leaf Index placement | Subtask 06 coverage |
|------|-------------------|---------------------|----------------------------------|-------------------------------|---------------------|
| `skip` | no | no | no | not enumerated | `TestMeditateInitSuggestions` (4-mode enum) |
| `additional_facet` | yes | only via consolidation prose at `compact`/`default`; via per-branch section at `detailed`+ | yes | new Branch entry | `TestMeditateAdditionalFacetCostAck` + `TestMeditateCombinedFacetConfirmation` |
| `report_section_only` | no | yes — with `custom_report_section_title` | no | no Branch entry; section under `confirmed_sections` | same |
| `additional_facet_AND_section` | yes | yes — with `custom_report_section_title` | yes | new Branch entry + `confirmed_sections` entry | same |

### 6. Eval coverage — `SHOULD_FIX` (auto-applied)

K1–K7 / K9 have eval coverage via `TestMeditate*` classes in subtask 06. K8 (no new files added to dist / install / version-bump RELEASE_PATHS) was not covered by any test — auto-applied: added `TestMeditateNoNewDistFilesK8` to subtask 06's deliverable enumeration, with the assertion that `scripts/create-crux-zip.py`, `install.py`, `.github/workflows/version-bump.yml`, and `.crux/dist-manifest.json` are not modified by this spec's surfaces.

The pinned-numeric regression for `compact` is exemplary — it's the single best lever against future drift on the new default-when-unspecified behaviour, and it directly enforces the user's stated intent that `compact` reproduces today's minima byte-for-byte.

Two `NICE_TO_HAVE` items left for the human reviewer:
- No numeric pinning of the cost-formula multiplier table (only structural assertion that "prompt prose displays cost estimates per depth × richness × mode combination"). Pinning numbers would tighten regression catch but creates coupling.
- No structural test that a `report_section_only` opt-in produces a section in the rendered report at every level (the assertion lives only in `TestMeditateInitSuggestions` indirectly via the 4-mode enum). Could be tightened.

### 7. CRUX mirror freshness — `PASS`

Subtask 08 enumerates the candidate source rule files and their mirrors correctly. None of the modified files (`crux-meditate.md`, `crux-cursor-memory-manager.md`, `evals/*`, `README.md`, `AGENTS.md`, `docs/crux-memories.md`, `web/compress.md/memories.html`) have `.crux.md` / `.crux.mdc` mirrors in `.cursor/rules/`. `AGENTS.crux.md` is generated at zip-build time from the `<CRUX agents="always">` block (which subtask 07 explicitly says is NOT touched) — verified against `scripts/create-crux-zip.py` line 208. Subtask 08's "expected outcome: no mirrors require regeneration" is accurate.

Subtask 08 already correctly skips `AGENTS.md` per the existing `_CRUX-RULE.mdc` note about the source-file convention.

### 8. Docs sync completeness — `PASS`

Subtask 07 covers the docs-sync rule's three primary targets (`README.md`, `CONTRIBUTORS.md`, `web/compress.md/`) plus the spec's explicit additional surfaces (`AGENTS.md` project-internal section, `docs/crux-memories.md`, `web/compress.md/memories.html`). Verified that all four docs paths exist in the repo. Subtask 07 explicitly preserves the `<CRUX agents="always">` block (no consumer-side change) and the existing dist enumerations (no new files per K8). It also enumerates the dual-meaning-of-`default` plain-prose callout requirement.

### 9. Phase ordering & critical-path correctness — `SHOULD_FIX` (auto-applied)

Phase graph `01 → 02 → (03 ‖ 04) → 05 → (06 ‖ 07) → 08 → 09` is internally consistent — every dependency arrow is satisfied. One implicit dependency was not declared: subtask 05's "Inputs" section says _"Modified agent file (subtask 04 output) — pulls in the `init-suggestions-{ts}.yml` schema this subtask reads"_, but subtask 05's metadata lists Dependencies as only "03". The canonical schema lives in subtask 02's design doc, so technically both 04 and 05 read from 02 — but the cross-reference is fragile.

Auto-applied: in subtask 05 added an explicit "Schema source-of-truth" callout naming subtask 02's design doc as the canonical source; left subtask 05's hard dependency list unchanged (still 03) so phase ordering is preserved, but added a cross-reference for any executor reading 05 cold.

### 10. Definition-of-done specificity — `PASS`

Every DoD bullet is testable against the post-spec repo state and most map to a concrete test class in subtask 06 or to a verification step in subtask 09. The bullets are appropriately specific ("`compact` reproduces current minima exactly" rather than "richness mapping is correct"), and the few subjective items ("verified non-infinite-loop") are immediately followed by a subtask 09 dimension that owns the verification.

## Fixes Applied

Each fix is unambiguous, in scope, and improves clarity / completeness without restructuring subtasks, reversing user decisions, changing agent assignments, or adding/removing subtasks.

### 1. Subtask 01 — freeze item #13 reconciled with K6

**File**: `subtask-01-meditate-richness-contract-capture-20260523.md`

**Before**:
```
13. **Cost-ack expansion variant** (`Q-Cost-Acknowledgment-Expansion`,
    20260517 freeze §2.3 — cite). The new spec extends this with an
    optional "keep comprehensiveness setting?" follow-up.
```

**After**:
```
13. **Cost-ack expansion variant** (`Q-Cost-Acknowledgment-Expansion`,
    20260517 freeze §2.3 — cite). The new spec replaces this with the
    read-only-richness variant of the merged
    `Q-Cost-and-Richness-Acknowledgment` gate (richness shown locked
    per K6 — set-once-per-invocation). The expansion variant does NOT
    offer a "keep richness setting?" follow-up; richness is implicitly
    locked. The existing "keep deep-confirm setting?" follow-up is
    preserved unchanged.
```

### 2. Spec K2 — agent-count vs token-cost clarification + worked example

**File**: `spec-meditate-richness-20260523.md`

Added an explicit split between agent-count multipliers and token-cost multipliers; added a worked-example numeric table at depth 3 × Research mode so the architecture-design subtask has a numeric starting point. Tightened the "default `default`" preselection wording.

### 3. Spec K4 — `additional_facet`-only mode clarified at `compact`/`default`

**File**: `spec-meditate-richness-20260523.md`

Added two sentences to the `additional_facet` (without `_AND_section`) bullet explaining that "natural output" means consolidation prose at `compact`/`default` and a per-branch section at `detailed`+.

### 4. Spec K9 — `respawn_reason` schema clarified (sections + visualisations both possible)

**File**: `spec-meditate-richness-20260523.md`

Changed `respawn_reason` from a single enum to a list-typed field so a single respawn can carry both missing-section and missing-visualisation reasons (the current schema forced an executor to either chain two respawns or pick one).

### 5. Spec — 3 new tertiary Open Questions surfaced

**File**: `spec-meditate-richness-20260523.md`

Added OQ #7 (same-iteration Dim 1–11 fix + Dim 13 respawn ordering), OQ #8 (`init-suggestions-{ts}.yml` absent on expansion continuation from a pre-richness meditation), and OQ #9 (when both missing sections AND missing visualisations fire in one Dim-13 finding, are they bundled into one respawn or two?). All three marked as WARNING-level (not blockers), per the spec's existing OQ pattern.

### 6. Subtask 03 — preselection wording aligned with K2

**File**: `subtask-03-meditate-richness-coordinator-gates-20260523.md`

Tightened "Default richness preselection = `default` (the level literally named `default`)" — wording was OK but inconsistent across the file; replaced every occurrence with a single canonical phrase.

### 7. Subtask 05 — schema source-of-truth callout

**File**: `subtask-05-meditate-richness-report-contract-20260523.md`

Added "Schema source-of-truth" paragraph after the deliverables checklist explicitly naming subtask 02's design doc as the canonical `init-suggestions-{ts}.yml` schema; cross-referenced subtask 04 as the write-side implementation.

### 8. Subtask 06 — `TestMeditateNoNewDistFilesK8` added

**File**: `subtask-06-meditate-richness-evals-tests-20260523.md`

Added a new Python-only test class enumeration to the deliverables checklist so K8 has a regression test (asserts `scripts/create-crux-zip.py`, `install.py`, `.github/workflows/version-bump.yml`, `.crux/dist-manifest.json` content is unchanged in shape by this spec — verified via membership check on the meditate-touched files, not via byte-for-byte file diff which would conflict with other specs).

### 9. Spec DoD — preselection wording tightened to match K2

**File**: `spec-meditate-richness-20260523.md`

Replaced the DoD line phrasing to match the K2 / subtask 03 canonical phrasing for the preselected `default` level.

## Recommendations Not Auto-Applied

The following findings fall into the "do not auto-apply" bucket (would reverse a user decision, restructure subtasks, or change agent assignments). They are documented here for human-reviewer attention:

### R1. (NICE_TO_HAVE) Pin numeric cost-formula values in the eval suite

**Why not auto-applied**: pinning numeric values in subtask 06 risks coupling tests to the exact multiplier table subtask 02 produces; subtask 02 hasn't executed yet, so any value chosen now would be premature. If the human reviewer wants tighter regression catch, the recommended approach is to add the pinned values in subtask 06 _after_ subtask 02 lands the multiplier table.

**RECOMMENDATION**: Add a `TestMeditateCostFormulaNumericPinning` test class in subtask 06 _post-02-completion_ that pins the chosen multipliers to literal values, so future drift in the table is caught loudly.

### R2. (NICE_TO_HAVE) Structural test for `report_section_only` rendering at every level

**Why not auto-applied**: the existing assertion via `TestMeditateInitSuggestions` covers the 4-mode enum but not the cross-level invariant that `report_section_only` sections appear at `compact` too. Adding this is a small test addition but the wording of the assertion depends on subtask 05's final phrasing.

**RECOMMENDATION**: Either tighten `TestMeditateInitSuggestions` or add `TestMeditateReportSectionOnlyAtAllLevels` post-execution. Not a blocker.

### R3. (NICE_TO_HAVE) Anti-homogenisation regression at richer levels

**Why not auto-applied**: Anti-homogenisation rules are preserved per K7, but `exhaustive` reports with per-branch sections + per-leaf subsections + per-finding citation columns may inadvertently produce a "wall of dense default-AI prose" effect that the anti-homogenisation rule was designed to catch. Subtask 09 covers this implicitly via "Anti-Homogenisation Rules regression — confirm the full block-list is preserved verbatim across every level".

**RECOMMENDATION**: Subtask 09 could add a dedicated spot-check that at `exhaustive` level, the rendered report still passes Dim 8 (anti-homogenisation drift) on a sample meditation. Not a blocker — the existing dim 8 check covers the rule.

### R4. (NICE_TO_HAVE) Subtask 04 / 05 schema-consistency CI check

**Why not auto-applied**: would require a new fixture file consumed by both subtasks, which is structural. The fix in §7 above is a softer cross-reference that avoids touching execution-time machinery.

**RECOMMENDATION**: Consider adding a YAML schema fixture (`schemas/init-suggestions.yml`) that both write-side (subtask 04) and read-side (subtask 05) reference at runtime. Out of scope for this spec; could be a follow-up spec.

## Findings Summary

| Severity | Count |
|----------|-------|
| `BLOCKER` | 0 |
| `MUST_FIX` | 1 (cost formula clarification — auto-applied) |
| `SHOULD_FIX` | 6 (auto-applied) |
| `NICE_TO_HAVE` | 4 (documented; not auto-applied) |
| `INFO` / `PASS` | 4 (priorities 4, 7, 8, 10) |

## Top 3 Recommendations for the Human Reviewer

1. **Numerically pin the cost-formula multipliers in subtask 06 once subtask 02 lands.** The biggest residual risk is silent drift in cost calculus across future refactors — and a numeric pinned test is the single best lever (mirrors what `TestMeditateBackwardsCompatibility` does for `compact` minima). Recommended to add `TestMeditateCostFormulaNumericPinning` post-02-completion.

2. **Track the 3 new tertiary Open Questions (#7 / #8 / #9) added to the spec.** None are blockers, but they need explicit resolution in subtask 02's architecture design document (same-iteration Dim 1–11 + Dim 13 ordering; expansion-continuation when prior meditation has no `init-suggestions-{ts}.yml`; bundled vs split respawn when both sections AND visualisations are missing). The defaults chosen are sensible but subtask 09 should re-verify they were honoured.

3. **Confirm the `additional_facet` × cost-formula interaction is understood by subtask 02's architect.** The auto-applied K2 worked-example table is illustrative only — subtask 02 must produce the full multiplier table for every (depth × mode × richness × additional_facets_count) combination. If the architect treats the worked example as authoritative without re-deriving from first principles, the cost-ack prose may be wrong.

---

## Post-Assessment Addendum — K10 Added Outside the Judge Pass (2026-05-23, later)

> **Source**: User direction added after the judge's assessment + auto-fix
> pass. K10 was not present when the verdict above (`READY_WITH_FIXES`)
> was issued. This addendum records the addition for audit; **the
> verdict above was rendered against K1–K9 only and does not cover
> K10**.

### What Changed

- **K10 added** (split into K10a / K10b / K10c) covering the new
  post-consolidation / pre-adversarial-review
  `Q-Finalisation-Enhancements` gate:
  - K10a — gate timing (post-consolidation / pre-adversarial-review,
    fires in Research + Quick + Ensemble modes), scope (5-candidate
    multi-select, mixed-cost taxonomy with 7 cheap + 4 expensive
    types), and graceful-degradation rule when fewer than 5
    candidates clear the impact threshold.
  - K10b — accept-policy: cheap items respawn within the existing
    ≤3 review-cycle iteration cap (extends K9 `respawn_reasons:`
    list with `accepted_finalisation_enhancements`); expensive
    items default `queue` (writes `follow-up-{type}-{ts}.yml`),
    opt-in `spawn_now` triggers cost-ack re-presentation in
    read-only-richness mode.
  - K10c — `finalisation-enhancements.yml` persistence schema +
    impact × insight-value reflection rubric (with worked
    examples) + continuation-menu re-application of unchosen
    items + queued spawn-now of expensive items.
- **K9 schema extended** — `respawn_reasons:` list gains
  `accepted_finalisation_enhancements` value;
  `accepted_finalisation_enhancements: [...]` field added to the
  respawn payload schema; `finalisation_enhancements_payload`
  field added to carry the full `finalisation-enhancements.yml`
  contents.
- **All 8 implementation / verification subtasks updated** —
  subtasks 02 / 03 / 04 / 05 / 06 / 07 / 09 each gained
  K10-specific deliverables. Subtask 01 (contract capture) and
  subtask 08 (CRUX mirrors) were unchanged because K10 doesn't
  touch the contract surfaces they freeze / regenerate.
- **5 new K10-related Risks** (#7–#10) added to the Risks
  section.
- **5 new K10-related Open Questions** (#10–#14) added to the
  Open Questions section.

### What Did NOT Change

- **K1–K9 semantics** are unchanged. Only cross-references inside
  K9 (the respawn_reasons list extension) and inside the index's
  Phase descriptions / Definition of Done / Risks / Open
  Questions were updated to incorporate K10.
- **Subtask manifest** stays at 9 subtasks. K10 work was absorbed
  into existing subtasks rather than creating new ones, so the
  dependency graph and phase structure are unchanged.
- **Status** remains `Ready for Review`.

### Recommendation for the Human Reviewer

A **re-judge of the spec is recommended before execution** because
the verdict above was rendered against K1–K9 only and does not
cover K10. K10 introduces:

1. A new pre-spawn gate (`Q-Finalisation-Enhancements`) that
   should be re-audited for Pattern A/B integrity, decision-
   guidance prose quality, and cost-ack re-presentation
   precision.
2. A new respawn cause (`accepted_finalisation_enhancements`)
   that should be re-audited for the non-infinite-loop guarantee
   and the per-reason ordering rule.
3. New artefacts (`finalisation-enhancements.yml` and four
   `follow-up-{type}-{ts}.yml` patterns) that should be re-audited
   against K8 (no new dist/install enumerations needed because
   the artefacts live in the meditation working directory, not
   in `.cursor/`).
4. A new reflection rubric (impact × insight-value, configurable
   weights) that should be re-audited for deterministic LLM
   applicability.

Suggested re-judge command: `/zoto-spec-judge` against the
current spec state. Compare the new verdict against the prior
`READY_WITH_FIXES`; any new `MUST_FIX` or `BLOCKER` findings
specific to K10 should be auto-applied or surfaced as
NICE_TO_HAVE recommendations before the spec moves to execution.

### Files Modified in the K10 Pass

- `spec-meditate-richness-20260523.md` — added K10a/b/c block;
  extended K9 respawn payload; added requirements 16–22; added
  risks 7–10; added open questions 10–14; updated phase
  descriptions; updated Definition of Done.
- `subtask-02-meditate-richness-architecture-design-20260523.md`
  — added K10 design deliverables (gate ordering, Pattern-B
  handoff, YAML schemas, follow-up artefact schemas, reflection
  contract, cost-ack re-presentation prose, per-reason ordering,
  non-infinite-loop proof extension, patch matrix extension,
  eval-strategy extension).
- `subtask-03-meditate-richness-coordinator-gates-20260523.md`
  — added K10a/b/c implementation deliverables (askQuestion
  shape, per-item treatment sub-questions, cost-ack
  re-presentation, file persistence flow, continuation menu
  extension).
- `subtask-04-meditate-richness-agent-payload-scouting-20260523.md`
  — added consolidation reflection contract, rubric application,
  `finalisation-enhancements.yml` write logic, resume-handler
  logic, ensemble propagation rule.
- `subtask-05-meditate-richness-report-contract-20260523.md`
  — added per-cheap-type rendering contract, interaction with
  existing minima, per-reason ordering, Dim 13 extension,
  footer annotation extension.
- `subtask-06-meditate-richness-evals-tests-20260523.md`
  — added 11 new K10-specific test classes including a
  byte-for-byte backwards-compat regression for the skip-all
  path.
- `subtask-07-meditate-richness-docs-sync-20260523.md`
  — added K10 docs additions (README, docs/crux-memories.md,
  web/compress.md/memories.html, config schema for
  `cruxMemories.meditate.finalisationEnhancements`).
- `subtask-09-meditate-richness-integrity-review-20260523.md`
  — added 7 new K10 verification deliverables (gate timing,
  Pattern A/B, cost-ack precision, schema, reviewer extension,
  non-infinite-loop, continuation menu, backwards-compat).

---

## K10 Re-Judge — 2026-05-23

- **Spec**: `specs/20260523-meditate-richness/spec-meditate-richness-20260523.md`
- **Reviewer**: `zoto-spec-judge` (independent, fresh context)
- **Mode**: Spec assessment + auto-apply (re-judge)
- **Scope**: K10 a/b/c (added after the prior `READY_WITH_FIXES`
  verdict) + the two user-confirmed decisions documented in the
  re-judge prompt — Decision 1 (OQ #10 ensemble cadence →
  "both layered") and Decision 2 (Adversarial-reviewer Dim 13 vs
  Dim 14 → defer to subtask 02 at design-doc time).

### Overall verdict

**`READY_WITH_FIXES`** (post-fix).

The spec remains structurally sound; K10 is well-integrated;
the two user decisions are correctly applied. All `MUST_FIX`
and `SHOULD_FIX` findings from the K10-specific priorities
(11–19) have been auto-applied; the remaining items are
`NICE_TO_HAVE` recommendations for the human reviewer. The
spec is ready for execution **after the human reviewer
confirms the layered-cadence prose is wired through every
subtask consistently** (auto-applied here but worth a final
read-through given the depth of the change).

### Summary of K10 + ensemble-cadence changes applied (this round)

1. **Decision 1 (OQ #10 → "both layered") applied across the
   spec stack**: K10a's ensemble-cadence prose now explicitly
   documents per-tree consolidation reflection + cross-model
   root reflection + a single combined multi-select at
   ensemble root over the union of `(per-tree × N) +
   (cross-model × 5)`. K10c persistence paths now enumerate
   per-tree YAMLs (`{model-subdir}/finalisation-enhancements.yml`)
   AND the root YAML (`finalisation-enhancements.yml`).
   Subtask 02 has a new ensemble-layered-cadence design
   sub-section; subtask 04 has parallel per-tree + root write
   obligations; subtask 05 documents per-tree vs cross-model
   report respawn targeting; subtask 06 replaces the prior
   `TestMeditateK10EnsembleOnceAtRoot` with
   `TestMeditateK10EnsembleLayeredCadence` and adds
   `TestMeditateK10EnsembleContinuationMenuLayered`; subtask
   09 has a new layered-cadence verification step. The
   continuation menu surfaces per-tree-only unchosen items
   (`surfaced_to_root: false`) with provenance labels.

2. **Decision 2 (Dim 13 vs Dim 14 deferred) verified
   consistent**: subtask 05 lines 220–233 already documented
   the dual-option without pre-committing ("subtask 02 may
   judge that a separate Dim 14 … is cleaner. Either choice
   is acceptable; subtask 02 makes the call; subtask 05
   implements; subtask 06 covers either way"). Cross-checked
   K10b prose, subtask 06 test descriptions, and subtask 09
   verification — all consistently defer the choice. The
   re-judge changelog banner explicitly states the
   deferral. **No new auto-apply needed for Decision 2.**

3. **Schema completeness, rubric concreteness, backwards-compat
   tightening, cost-ack subsystem enumeration, OQ trail
   cleanup**: applied per priorities 11–19 below.

### Per-priority findings — K10 round (priorities 11–19)

#### Priority 11 — Pattern-B handoff correctness for the new gate — `PASS` (with auto-applied tightening)

The Pattern-B handoff dance for `Q-Finalisation-Enhancements`
is correctly designed:

1. Depth-0 manager (or post-decomp meditation-guide) writes
   `finalisation-enhancements.yml` after consolidation,
   returns `needs_user_input` block — does NOT call
   `AskQuestion` (Pattern B preserved).
2. Calling agent runs the multi-select askQuestion +
   per-item treatment sub-questions + (any) cost-ack
   re-presentation — owns ALL `AskQuestion` invocations
   (Pattern A preserved).
3. Calling agent updates `finalisation-enhancements.yml` in
   place with `accepted` / `treatment` / `decided_at_utc`
   fields, then resumes the depth-0 manager.
4. Depth-0 manager builds respawn payload entries from the
   updated file and proceeds to adversarial review.

Subtask 02 deliverables (lines 139–153) document this dance
verbatim. Subtask 03 (lines 154–169) implements the calling-
agent side. Subtask 04 (resume-handler logic deliverable)
implements the depth-0-manager side. The handoff is symmetric
and the "subagents never call `AskQuestion`" rule is
preserved.

**Auto-applied tightening (SHOULD_FIX)**: the layered ensemble
cadence (Decision 1) extends the handoff dance — both
per-tree consolidation agents AND the ensemble aggregator now
participate in the write side, while the calling agent still
owns the single root combined askQuestion. Added explicit
prose in subtask 02 ("K10 — Ensemble layered cadence design")
and subtask 04 ("K10 — Ensemble layered cadence") that
documents each participant's obligations + the resume-handler
contract at ensemble level.

#### Priority 12 — Cost-ack re-presentation correctness for `spawn_now` — `SHOULD_FIX` (auto-applied)

The cost-ack re-presentation template in subtask 02 (lines
197–210, pre-fix) said "{enumerated_types}" without breaking
down which subsystem(s) each accepted expensive type
contributes to. An executor implementing the prompt-prose
substitution couldn't deterministically render the new agent
count without consulting an external source.

**Auto-applied**: extended the cost-ack template in subtask
02 to enumerate per-expensive-type subsystem agent
contribution explicitly:

- `additional_meditation × M` → M nested `/crux-meditate`
  invocations (top-level only; nested cost-ack fires at the
  nested meditation's own gate)
- `extracted_spec × M` → M spec-generator agent(s)
- `extracted_memories × M` → M memory-extraction agent(s)
- `expanded_branch × M` → M branch-expansion subtrees (each
  ≈ 13 agents at depth-3 Research; per-mode factor from the
  cost-formula multiplier table)

**Read-only-richness shape** correctness verified: richness
is shown locked (per K6); only the proceed/cancel sub-question
is interactive. The locked-richness display is documented in
subtask 02 (lines 410–422 pre-fix; preserved).

**Cannot-infinite-loop guarantee for `spawn_now` cost-ack**:
added explicit prose to subtask 02 stating the re-presentation
is a single round trip — `re-acknowledge` proceeds to
scheduled post-cycle spawn; `cancel` drops treatments back to
`queue`. The re-presentation cannot re-fire within the same
invocation; treatment decisions are immutable for the
remainder of the invocation once the cost-ack closes. This
closes the priority-12 concern.

#### Priority 13 — Schema completeness for `finalisation-enhancements.yml` — `PASS`

Per-type `payload:` shapes are enumerated in subtask 02 for
every one of the **7 cheap and 4 expensive types** (lines
159–169 pre-fix; preserved). Cross-check against subtask 05's
rendering contract (lines 161–195 pre-fix):

| Cheap type | Subtask 02 `payload:` shape | Subtask 05 rendering contract |
|---|---|---|
| `executive_summary` | ✓ `{target_persona, max_paragraphs, anchor_findings}` | ✓ flowing prose, theming-respectful |
| `action_plan` | ✓ `{horizons, items_per_horizon, anchor_findings}` | ✓ horizon-grouped list + Gantt timeline ribbon |
| `risks_section` | ✓ `{risk_taxonomy_axes, anchor_findings}` | ✓ risk-meter + risk taxonomy table |
| `glossary` | ✓ `{term_count_estimate, anchor_branches}` | ✓ 2-column term/definition list |
| `decision_tree_infographic` | ✓ `{root_decision, depth, anchor_findings}` | ✓ SVG decision tree + print fallback |
| `reader_persona_tldrs` | ✓ `{personas, paragraphs_per_persona}` | ✓ per-persona card grid (non-homogenised) |
| `cross_branch_synthesis_section` | ✓ `{axes, anchor_findings_per_axis}` | ✓ two/three-column convergent/divergent layout |

| Expensive type | Subtask 02 `payload:` shape | Subtask 05 rendering contract |
|---|---|---|
| `additional_meditation` | ✓ `{proposed_topic, proposed_facet_seed, recommended_depth, recommended_mode}` | N/A (spawns nested meditation — no report-side rendering) |
| `extracted_spec` | ✓ `{proposed_slug, overview, candidate_subtasks, spec_template}` | N/A (writes a new spec — no report-side rendering) |
| `extracted_memories` | ✓ `{candidates: [{title, type, body_summary, source_signals}]}` | N/A (proposes memories — no report-side rendering) |
| `expanded_branch` | ✓ `{target_branch_index, recommended_new_depth, facet_emphasis_override, recommended_mode}` | N/A (re-runs a branch — no report-side rendering) |

No type has a `payload:` gap. No cheap type lacks a rendering
contract. Expensive types correctly have no report-side
rendering (they spawn follow-up work). **No auto-apply
needed.**

#### Priority 14 — Reflection rubric concreteness — `PASS`

Subtask 04 (lines 99–113 pre-fix) already documents anchor
descriptions at 2 / 5 / 9 for both `impact_score` and
`insight_value_score`. Anchor examples are concrete:

- `impact_score = 9`: "enhancement directly enables a
  high-stakes decision (e.g. exec summary unblocks board
  presentation)"
- `impact_score = 5`: "enhancement clarifies reading order
  but doesn't change recommended action"
- `impact_score = 2`: "cosmetic only"
- `insight_value_score = 9`: "surfaces a cross-branch
  synthesis no individual branch made visible"
- `insight_value_score = 5`: "re-organises content from one
  branch into a more readable form"
- `insight_value_score = 2`: "paraphrases content already
  prominent in existing sections"

Three anchor points per axis is adequate for deterministic
LLM application — the rubric is concrete enough. **No
auto-apply needed.**

**One INFO observation**: at the cross-model reflection step
(introduced by Decision 1's layered cadence), the rubric
applies equally well, but the "insight value" semantics are
naturally inflated at the cross-model layer (cross-tree
convergence is by construction high-insight signal). Subtask
02's design-doc guidance for the cross-model reflection
should note that the same 2/5/9 anchors apply, with
cross-tree convergence boosting `insight_value_score` to 7+
when applicable. **Surfaced as a NICE_TO_HAVE** for the human
reviewer; not auto-applied because it would be premature
prescription.

#### Priority 15 — Backwards-compat byte-for-byte for skip-all — `MUST_FIX` (auto-applied)

The prior `TestMeditateK10SkipAllBackwardsCompat` description
was structurally complete but didn't enumerate every byte-
level surface K10 could perturb. **Auto-applied**: tightened
the test description in subtask 06 to enumerate every
assertion that MUST hold on the skip-all path:

- Step-graph between consolidation and adversarial review
  unchanged.
- `respawn_reasons:` does NOT contain
  `accepted_finalisation_enhancements`.
- `accepted_finalisation_enhancements:` absent or `[]` in
  any respawn payload built on skip-all.
- No `follow-up-{type}-{ts}.yml` files written.
- Report HTML/PDF section list unchanged structurally vs
  pre-K10.
- **Footer `theme:` annotation omits the
  `finalisation-enhancements:` segment entirely when count
  == 0** (auto-applied parallel fix in subtask 05's footer
  rule).
- No additional adversarial-review iteration consumed by
  K10.
- The single new artefact `finalisation-enhancements.yml`
  has every candidate as `accepted: false, treatment:
  "unchosen_persisted"`; no other K10 artefacts appear.

This is the single best lever against silent K10-induced
regression and is now airtight.

#### Priority 16 — K8 honour — `PASS`

Verified:

- `finalisation-enhancements.yml` and the four
  `follow-up-{type}-{ts}.yml` artefacts live in the
  meditation working directory (`meditations/{slug}/...`),
  NOT in `.cursor/` or `scripts/`. K8's "no new dist
  enumerations" still holds.
- Subtask 07 (docs-sync) explicitly does NOT modify
  `scripts/create-crux-zip.py`, `install.py`,
  `.github/workflows/version-bump.yml`, or
  `.crux/dist-manifest.json` (lines 122–131 pre-fix).
- The new config key
  `cruxMemories.meditate.finalisationEnhancements` is
  documented in `docs/crux-memories.md` only; subtask 07
  explicitly states "Do NOT add to `install.py` config-write
  defaults" because the key is OPTIONAL with sensible
  defaults.
- `zip-contents-protection.crux.mdc` rule honoured — no new
  files added to the zip script's enumeration.

**No auto-apply needed.**

#### Priority 17 — OQ #11 (rubric weights configurable) — `PASS`

Verified config path consistency:

- `.crux/crux-memories.json` already has
  `cruxMemories.meditate.modelPool` and
  `cruxMemories.meditate.ensembleAggregatorModel` as
  established `cruxMemories.meditate.*` sibling keys.
- The new `cruxMemories.meditate.finalisationEnhancements`
  key follows the same `cruxMemories.meditate.*` pattern.
- Sub-keys (`weights: { impact, insight_value }`, `formula:
  "product" | "weighted_sum"`,
  `minimum_impact_threshold`) are documented in subtask 07
  with defaults — consistent with how
  `cruxMemories.meditate.modelPool` is structured.

**No auto-apply needed.**

#### Priority 18 — Continuation-menu surfacing (K10c) — `SHOULD_FIX` (auto-applied)

The pre-fix continuation-menu surfacing was correct for
single-model but didn't explicitly handle the layered
ensemble cadence (Decision 1) — per-tree-only unchosen items
(`surfaced_to_root: false`) weren't surfaced because they
weren't even in the data model.

**Auto-applied**: extended K10c continuation-menu prose to
handle the layered cadence:

- **Root unchosen items** (cross-model + per-tree that
  surfaced at root): labelled with provenance
  (`(cross-model)` or `(from tree: {model-label})`).
- **Per-tree-only unchosen items** (per-tree candidates with
  `surfaced_to_root: false`): aggregated across all per-tree
  YAMLs, labelled `(from tree: {model-label}, not surfaced
  at root)`.
- Selecting a per-tree-only item targets the **per-tree
  report respawn** for that tree (per subtask 05's layered
  targeting rule), not the cross-model synthesis report.

Subtask 06 gains a new test
`TestMeditateK10EnsembleContinuationMenuLayered` covering
this.

**Grouping under section headings** (per OQ #14 default):
verified subtask 03 lines 189–193 (pre-fix) and subtask 06
test assertion still document grouping. **No auto-apply
needed for OQ #14 specifically.**

#### Priority 19 — Resolved-OQ trail — `SHOULD_FIX` (auto-applied)

**Auto-applied**:

1. K10 OQ #10 (ensemble cadence) annotated as
   `RESOLVED 2026-05-23 (user decision)` with the full
   layered-cadence resolution prose in-place. Severity
   reclassified from `WARNING` (open) to `WARNING (resolved;
   preserved for history)`.
2. Added a **NUMBERING NOTE** banner at the top of the
   "Tertiary Open Questions" subsection explaining the
   pre-existing OQ numbering chaos (the original tertiary
   block has #7–#10; a later assessment block has #7–#9;
   the K10 block has #10–#14; the K10 #10 is now resolved).
   The duplicate numbering is preserved for audit
   compatibility with the prior assessment fixes; subtask
   09 (integrity review) is now documented as the canonical
   tie-breaker if ambiguity arises.
3. OQ #10 prose explicitly cross-references the subtasks
   that implement the resolution (02 / 04 / 05 / 06 / 09).

**OQ trail audit (post-fix)**:

| OQ ID | Block | Status | Resolution location |
|---|---|---|---|
| #1–#6 | Resolved-by-user | RESOLVED (pre-K10) | K1 / K2 / K4 / K6 / K9 |
| #7–#10 (tertiary judge OQs) | Tertiary | WARNING (open with defaults) | Subtask 02 / 09 |
| #7–#9 (post-assessment add) | Tertiary | WARNING (open with defaults) | Subtask 02 / 09 |
| #10 (K10 ensemble cadence) | K10 OQs | **RESOLVED 2026-05-23** | K10a layered cadence |
| #11–#14 (K10 OQs) | K10 OQs | WARNING (open with defaults) | Subtask 02 / 09 |

History preserved; resolved items distinguishable from open
items at a glance.

### Per-priority findings — re-check of priorities 1–10 (prior round)

Nothing has changed semantically for K1–K9 (per the user's
statement that "K1–K9 are semantically unchanged; only K9's
respawn-protocol schema gained a new value (`accepted_finalisation_enhancements`)
and a new payload entry"). Re-verified:

- **Priority 1 (functional preservation)** — `PASS`.
  Pre-fix correction in subtask 01 §13 still holds.
- **Priority 2 (naming-collision risk for `default`)** —
  `PASS`. Tightened wording still consistent.
- **Priority 3 (cost-formula correctness)** — `PASS`. The
  worked-example table in K2 still holds; the new cost-ack
  subsystem enumeration in K10 (priority 12 above)
  complements rather than contradicts the K2 formula.
- **Priority 4 (respawn non-infinite-loop guarantee)** —
  `PASS`. K10b extension of `respawn_reasons:` doesn't
  increase the bound (proof in subtask 02 K10 non-infinite-
  loop section); layered cadence (Decision 1) adds at most
  `N + 1` reflection writes (bounded by `modelPool` size)
  + 1 root user gate; total work still bounded.
- **Priority 5 (4-mode opt-in completeness)** — `PASS`.
- **Priority 6 (eval coverage)** — `PASS`. K10 round added
  6 new K10-specific test classes + 1 layered-cadence test
  + 1 continuation-menu layered test;
  `TestMeditateK10SkipAllBackwardsCompat` is now byte-for-
  byte airtight.
- **Priority 7 (CRUX mirror freshness)** — `PASS`. K10 adds
  no new source rule files; subtask 08's "no mirrors
  require regeneration" still holds.
- **Priority 8 (docs sync completeness)** — `PASS`. K10
  additions enumerated in subtask 07 (README,
  `docs/crux-memories.md`, `web/compress.md/memories.html`,
  config schema). No new docs files created.
- **Priority 9 (phase ordering)** — `PASS`. K10 work absorbed
  into existing subtasks; manifest unchanged at 9; phase
  ordering preserved.
- **Priority 10 (DoD specificity)** — `PASS`. K10 DoD
  bullets are testable; layered-cadence DoD line added
  (replaces the prior "once at ensemble level" bullet).

### Fixes Applied (K10 round)

Each fix is unambiguous, in scope, and improves clarity /
completeness / regression-catch without restructuring
subtasks, reversing user decisions, changing agent
assignments, or adding/removing subtasks.

#### F1. Spec changelog banner — K10 re-judge + Decision 1 + Decision 2

**File**: `spec-meditate-richness-20260523.md`

Added a new "Updated 2026-05-23 (K10 re-judge — user
decisions applied)" banner documenting both user decisions
and pointing to this assessment file.

#### F2. K10a — ensemble cadence prose rewritten for layered cadence (Decision 1)

**File**: `spec-meditate-richness-20260523.md`

K10a's "ensemble mode runs the gate once at ensemble level"
prose replaced with a full layered-cadence specification:
per-tree reflection (writes per-tree YAMLs), root
cross-model reflection (writes root combined YAML), single
combined multi-select at ensemble root over the union (with
the alternative architecture documented but flagged as
non-default). Single-model flows explicitly unchanged.

#### F3. K10c — persistence schema extended with per-tree paths + root cross-model paths

**File**: `spec-meditate-richness-20260523.md`

K10c persistence prose now enumerates BOTH per-tree YAML
write paths (`{model-subdir}/finalisation-enhancements.yml`)
AND the root combined YAML
(`finalisation-enhancements.yml`). Each per-tree candidate
carries `source_tree:` and `surfaced_to_root:` fields. Root
combined YAML structure documented
(`cross_model_candidates: [...]` + `union_candidates: [...]`).

#### F4. K10c — continuation-menu surfacing extended for layered cadence

**File**: `spec-meditate-richness-20260523.md`

K10c's continuation-menu prose now distinguishes root
unchosen items (cross-model + per-tree that surfaced at
root) from per-tree-only unchosen items
(`surfaced_to_root: false`), with provenance labels per
source.

#### F5. K10 OQ #10 annotated RESOLVED + numbering-note banner

**File**: `spec-meditate-richness-20260523.md`

OQ #10 rewritten with `RESOLVED 2026-05-23 (user decision)`
annotation and the full layered-cadence resolution prose.
Added a numbering-note banner at the top of the "Tertiary
Open Questions" subsection explaining the pre-existing
numbering chaos (per priority 19 cleanup).

#### F6. Spec Phase 3 description + DoD — ensemble cadence updated

**File**: `spec-meditate-richness-20260523.md`

Phase 3 subtask 04 description updated to mention per-tree
+ root reflection + per-tree vs cross-model report respawn
targeting. DoD "K10 ensemble fires once at ensemble level"
bullet rewritten as "K10 ensemble cadence layered: per-tree
internal write + aggregator root combined write + single
root askQuestion over the union".

#### F7. Subtask 02 — ensemble layered-cadence design sub-section + cost-ack subsystem enumeration

**File**: `subtask-02-meditate-richness-architecture-design-20260523.md`

Two parallel additions:
1. New deliverable "K10 — Ensemble layered cadence design"
   enumerating the per-tree reflection contract, per-tree
   YAML write path, root cross-model reflection contract,
   root combined YAML structure, single root askQuestion
   posture (with alternative documented), per-tree vs
   cross-model targeting, continuation-menu interaction,
   and an extended non-infinite-loop proof.
2. Cost-ack re-presentation prose template extended with
   per-expensive-type subsystem agent contribution
   enumeration (additional_meditation × M, extracted_spec
   × M, extracted_memories × M, expanded_branch × M) +
   explicit no-infinite-loop guarantee for the `spawn_now`
   cost-ack (single round trip; treatment decisions
   immutable after close).

#### F8. Subtask 04 — per-tree consolidation agents write per-tree YAMLs in ensemble mode; aggregator writes root YAML

**File**: `subtask-04-meditate-richness-agent-payload-scouting-20260523.md`

The prior "ensemble fires once at ensemble level; per-model
trees skip the gate entirely" deliverable replaced with
parallel per-tree + root obligations. Per-tree write
contract, root cross-model reflection contract, root
combined YAML schema, surfaced-to-root annotation, single
root askQuestion (recommended posture), and resume-handler
contract at ensemble level all documented.

#### F9. Subtask 05 — per-tree vs cross-model report respawn targeting + footer skip-all rule

**File**: `subtask-05-meditate-richness-report-contract-20260523.md`

Two parallel additions:
1. New deliverable "K10 — Ensemble layered-cadence respawn
   targeting" documenting that per-tree-sourced accepts
   target the per-tree report respawn AND cross-model-sourced
   accepts target the cross-model synthesis report respawn.
   Footer annotation per-tree vs cross-model rule. Dim 13
   (or new Dim 14) layered audit rule. Cost-ack
   re-presentation subsystem prose pointer.
2. Footer `theme:` annotation rule clarified: when 0
   enhancements were accepted at the gate, the footer MUST
   omit the `finalisation-enhancements:` segment entirely.

#### F10. Subtask 06 — `TestMeditateK10SkipAllBackwardsCompat` byte-for-byte assertion enumeration + `TestMeditateK10EnsembleLayeredCadence` replacement + `TestMeditateK10EnsembleContinuationMenuLayered` new

**File**: `subtask-06-meditate-richness-evals-tests-20260523.md`

Three changes:
1. `TestMeditateK10SkipAllBackwardsCompat` tightened with
   8 explicit pinned assertions covering every byte-level
   surface K10 could perturb.
2. `TestMeditateK10EnsembleOnceAtRoot` replaced with
   `TestMeditateK10EnsembleLayeredCadence` covering per-tree
   YAML writes, root combined YAML structure, surfaced-to-root
   annotation, single root askQuestion (or alternative if
   subtask 02 chose), root ranking by composite score across
   union, single-model backwards-compat, per-tree vs cross-
   model report respawn targeting.
3. New `TestMeditateK10EnsembleContinuationMenuLayered`
   covering per-tree-only unchosen item surfacing with
   provenance labels.

#### F11. Subtask 09 — ensemble layered cadence verification step added

**File**: `subtask-09-meditate-richness-integrity-review-20260523.md`

New verification deliverable "K10 verification — ensemble
layered cadence" covering per-tree YAML write contract, root
combined YAML write contract, surfaced-to-root annotation,
single root askQuestion, per-tree vs cross-model respawn
targeting (with cross-contamination flagged as BLOCKER),
continuation-menu layered surfacing, single-model
backwards-compat, and non-infinite-loop preservation. The
prior gate-timing verification deliverable kept its single-
model bullet but the ensemble half is now in the new step.

### Recommendations Not Auto-Applied (K10 round)

The following findings fall into the "do not auto-apply"
bucket per the re-judge prompt (would reverse a user
decision, restructure subtasks, change agent assignments,
or pre-commit the Dim 13 vs Dim 14 question). They are
documented for human-reviewer attention.

#### R5. (NICE_TO_HAVE) Cross-model reflection rubric calibration note

**Why not auto-applied**: priority 14 is already PASS; the
suggestion to note "cross-tree convergence boosts
`insight_value_score` to 7+ when applicable" at the
cross-model reflection layer is premature prescription that
subtask 02's architect should make at design-doc time. The
auto-applied prose in subtask 02 documents the cross-model
reflection inputs and ranking-preference cues (convergence
signal, cross-model-only synthesis); subtask 02's architect
can add the calibration note if they judge it useful.

**RECOMMENDATION**: subtask 02 design-doc author should add
a one-line "cross-tree convergence boosts insight_value_score
to ≥7" calibration in the cross-model reflection contract
section. Not a blocker.

#### R6. (NICE_TO_HAVE) Layered-cadence model-label resolution canonical source

**Why not auto-applied**: continuation-menu labels use
`{model-label}` resolved from
`cruxMemories.meditate.modelPool[i].label` (canonical). If
the `modelPool` changes between invocation and continuation,
the label may resolve to "Unknown model" for retired models.
Adding a fallback rule is a small touch but the auto-fix
would require subtask 02 to specify the fallback, which is
better as an architect call than an auto-applied default.

**RECOMMENDATION**: subtask 02 should specify a fallback
("Unknown model ({model-subdir})" if `modelPool` no longer
lists the slug) so retired-model continuations don't break.
Not a blocker.

#### R7. (NICE_TO_HAVE) Per-tree report respawn budget interaction

**Why not auto-applied**: per-tree-sourced accept targets the
per-tree report respawn; cross-model accept targets the
cross-model synthesis report respawn. Open question: does
each report (per-tree × N + cross-model × 1) get its OWN ≤3
iteration cap, or do they share a global ≤3 cap across the
ensemble? K9's "≤3 review-and-fix iteration cap" was written
pre-K10 and pre-Decision-1. The conservative reading is
that each report has its own ≤3 cap (today's per-tree
adversarial review cap already works this way pre-K10).
Subtask 02 should lock this in as part of the Decision 1
architecture design.

**RECOMMENDATION**: subtask 02 design-doc author should
explicitly state whether the ≤3 cap is per-report or
ensemble-global in the layered-cadence section.
Conservative default: per-report (matches today's per-tree
adversarial review cap pre-K10). Not a blocker.

#### R8. (NICE_TO_HAVE) Per-tree reflection cost folded into cost-ack

**Why not auto-applied**: Decision 1 adds per-tree
reflection writes (1 LLM thinking pass per tree) + 1 root
reflection write (1 LLM thinking pass at ensemble). These
add a small token cost that the K10b cost-ack re-
presentation doesn't currently surface (it surfaces only
`spawn_now` agent counts). If the user opts into ensemble
mode and accepts cheap enhancements, the per-tree
reflection cost is implicit. Risk #8 in the spec already
acknowledges consolidation-reflection cost; this is a
related but distinct cost.

**RECOMMENDATION**: subtask 02's cost-formula multiplier
table should add a small per-ensemble-tree reflection cost
line item (one LLM thinking pass per tree + one at root).
Magnitude is small (~1-2k tokens per reflection) but it's
worth surfacing for cost-acknowledgment accuracy. Not a
blocker.

### Findings Summary (K10 round)

| Severity | Count | Notes |
|----------|-------|-------|
| `BLOCKER` | 0 | — |
| `MUST_FIX` | 1 | Priority 15 (backwards-compat byte-for-byte tightening) — auto-applied |
| `SHOULD_FIX` | 4 | Priorities 11 (Pattern-B handoff at ensemble), 12 (cost-ack subsystem enumeration), 18 (continuation-menu layered surfacing), 19 (resolved-OQ trail) — all auto-applied |
| `NICE_TO_HAVE` | 4 | R5–R8 — documented for human reviewer; not auto-applied |
| `INFO` / `PASS` | 6 | Priorities 13, 14, 16, 17 (K10 round), plus all priorities 1–10 (re-verified) |

### Top 3 Recommendations for the Human Reviewer

1. **Confirm the layered ensemble-cadence prose reads
   coherently across subtasks 02 / 04 / 05 / 06 / 09 after
   the auto-apply pass.** The change touched 6 files with
   parallel additions; the auto-apply preserved each
   subtask's existing structure but the cross-references
   between them (per-tree write contract → root combined
   read contract → respawn targeting → continuation
   surfacing → integrity verification) deserve one final
   read-through to catch any subtle inconsistency before
   execution.

2. **Subtask 02 (architecture-design) must make four
   layered-cadence design calls at design-doc time** —
   surfaced as R5/R6/R7/R8 above:
   (a) cross-model reflection rubric calibration anchor (R5);
   (b) model-label resolution fallback for retired models (R6);
   (c) per-report vs ensemble-global ≤3 iteration cap (R7);
   (d) per-tree reflection cost folded into the cost-ack
   multiplier table (R8).
   None block execution but all four sharpen the layered-
   cadence story.

3. **Subtask 02 must also still resolve Decision 2 (Dim 13
   vs Dim 14)** — the spec consistently defers this choice
   to subtask 02 at design-doc time (verified consistent
   across K10b, subtask 05 lines 220–233, subtask 06 test
   descriptions, subtask 09 verification). Recommended:
   keep extending Dim 13 (simpler, fewer cross-references
   to update) unless the architect identifies a cleaner-
   separation argument for Dim 14. Either choice is
   architecturally sound; the spec is ready either way.

### Confirmation of User Decisions

- **Decision 1 (OQ #10 ensemble cadence → "both layered")**:
  ✅ APPLIED across the spec stack. K10a / K10c / OQ #10
  / Phase 3 / DoD / subtask 02 / subtask 04 / subtask 05 /
  subtask 06 / subtask 09 all updated. Per-tree YAMLs
  persisted at `{model-subdir}/finalisation-enhancements.yml`;
  root YAML at `finalisation-enhancements.yml` with
  `cross_model_candidates` + `union_candidates`. Single
  combined root askQuestion (recommended posture) over the
  union, capped at 0–5. Single-model flows unchanged.
  Continuation menu surfaces per-tree-only unchosen items.
  Per-tree vs cross-model report respawn targeting
  documented.
- **Decision 2 (Adversarial-reviewer Dim 13 vs Dim 14 →
  defer to subtask 02 at design-doc time)**:
  ✅ VERIFIED consistent. No spec-level pre-commit. Subtask
  05 lines 220–233 already documented the deferral
  (preserved verbatim). Re-judge changelog banner
  explicitly states the deferral. **No edit needed.**

---

