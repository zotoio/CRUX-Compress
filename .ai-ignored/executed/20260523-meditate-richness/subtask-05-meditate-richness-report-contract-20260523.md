# Subtask: Report Contract — Level-Driven Minima + Branch / Leaf / Peer-Review Surfacing

## Metadata
- **Subtask ID**: 05
- **Feature**: Meditate Comprehensiveness + Init-Time Suggestions
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 03, 04 (04 defines the `init-suggestions-{ts}.yml`
  write-side schema this subtask reads; 03 owns the coordinator-file
  region this subtask further edits)
- **Created**: 20260523

## Objective

Replace today's fixed report-generation minima (≥4 charts / ≥3
infographics / ≥1 calculator) with the level-driven mapping table
designed in subtask 02; add per-branch dedicated section rule, depth-3
leaf inclusion rule, and peer-review surfacing rule to the report
contract; teach the report contract to read `init-suggestions-{ts}.yml`
and honour confirmed sections / visualisations; extend the adversarial
reviewer's 11 dimensions with comprehensiveness fidelity and
init-suggestion honour.

Sequenced after subtask 03 because both touch the same file region in
the pre-decomposition target (the `### Report Generation — MANDATORY`
section of `.cursor/commands/crux-meditate.md`); in the
post-decomposition target both touch
`crux-skill-memory-meditation-report/SKILL.md`. Sequencing avoids merge
conflicts.

## Deliverables Checklist

- [x] Resolve target file at execution time per subtask 02 patch
      matrix:
  - **Pre-decomposition**: edit
    `.cursor/commands/crux-meditate.md` — `### Report Generation
    — MANDATORY` section (lines 969–1328 today); also extend the
    adversarial reviewer block (lines 759–771) with the two new
    dimensions.
  - **Post-decomposition**: edit
    `.cursor/skills/crux-skill-memory-meditation-report/SKILL.md`
    + `.cursor/skills/crux-skill-memory-meditation-review/SKILL.md`.
- [x] **Replace fixed minima** with the level-driven mapping table
      from subtask 02. Document `compact` / `default` /
      `detailed` / `exhaustive` rows with concrete numeric
      values for every dimension. Cite the
      `comprehensiveness:` payload as the contract; the report
      skill reads `comprehensiveness.minima.charts.count` etc.
- [x] **Per-branch dedicated section rule** — at level
      `detailed`+, every confirmed top-level facet gets its
      own report section presenting that branch's findings beyond
      what `consolidation.md` summarised. At level
      `exhaustive`, each per-branch section also has per-leaf
      subsections. Note: at `detailed`, `additional_facet` and
      `additional_facet_AND_section` branches each get their own
      dedicated section just like the original 3 facets;
      `additional_facet_AND_section` additionally honours the
      user-supplied `custom_report_section_title` from
      `init-suggestions-{ts}.yml`.
- [x] **Depth-3 leaf inclusion rule** — at `default`, depth-3 leaf
      material is surfaced as `summary` (today's behaviour). At
      `detailed`+, depth-3 leaf material is surfaced as `summary`
      with key citations; at `exhaustive`, depth-3 leaves are
      quoted verbatim with full citations.
- [x] **Peer-review surfacing rule** — at `detailed`+, peer-
      review reinforcements / contradictions / gaps from
      `branch-{N}-peer-review-*.md` files become **named report
      sections** (one cross-branch reinforcements section, one
      contradictions section, one gaps section). At `exhaustive`,
      these become **per-branch dedicated** sections (e.g.
      "Branch 1 Reinforcements / Contradictions / Gaps").
- [x] **`init-suggestions-{ts}.yml` reading** — report skill MUST
      read this file at the start of report generation and honour:
  - Every `confirmed_sections[].title` MUST appear as a report
    section (the report MAY add more sections beyond these).
  - Every `confirmed_visualisations[].type` MUST be rendered (the
    report MAY add more chart / infographic types beyond these).
  - Every `additional_focus_areas_accepted[]` with
    `treatment: "report_section_only"` MUST become a report
    section (with the supplied rationale prose at the top).
- [x] **Adversarial reviewer dimensions extended from 11 to 13**:
  - **Dimension 12 — Comprehensiveness fidelity** — verify
    actual rendered counts match the level claimed in the
    footer's `level:` annotation. Count chart elements,
    infographic elements, calculator elements; cross-check
    against `comprehensiveness.minima` for the claimed level.
    `MUST_FIX` if shortfall; rewrite either the level annotation
    (only when the report genuinely matches a lower level) or
    the report (more common — bring the rendered counts up to
    the claimed level). Standard in-place reviewer fix flow.
  - **Dimension 13 — Init-suggestion honour** — verify every
    confirmed section title / visualisation type / accepted
    additional-focus-area entry from `init-suggestions-{ts}.yml`
    appears in the rendered report HTML. `MUST_FIX` AND
    `respawn_required: true` if any is absent or only present as
    an empty stub. Bypass standard in-place reviewer fix flow
    and trigger the **respawn protocol** (see next deliverable).
- [x] **Adversarial respawn protocol implementation** (new — K9):
  - **Trigger condition**: any Dim 13 finding with
    `respawn_required: true`. Spawn the report-generation skill
    afresh (Task tool invocation with the same agent definition
    that generates reports today) with the structured payload
    below.
  - **Respawn payload schema** (passed to the report-skill spawn
    prompt — must be implemented verbatim per K9 of the spec
    index):
    ```yaml
    respawn_reasons:                                    # list-typed — one respawn may carry multiple reasons (per K9 list semantics + K10b extension)
      - "missing_init_suggestion_sections"
      - "missing_init_suggestion_visualisations"
      - "accepted_finalisation_enhancements"            # K10b — present when at least one cheap enhancement was accepted
    reviewer_iteration: 1 | 2 | 3
    prior_report_paths:
      html: "report-{topic-slug}-{prior_ts}.html"
      pdf:  "report-{topic-slug}-{prior_ts}.pdf"
    missing_sections: [{title, rationale, source_signals, branch_evidence_pointers}]
    missing_visualisations: [{type, rationale, source_signals}]
    preserve_other_content: true
    comprehensiveness_payload: { ... unchanged ... }
    init_suggestions_payload: { ... unchanged, full ... }
    theming_payload: { ... unchanged ... }
    ```
  - **Iteration accounting**: respawn shares the existing ≤3
    review-and-fix iteration cap (no separate respawn budget).
    A respawn counts as one iteration. After respawn completes
    on iteration N, iteration N+1 spawns a fresh reviewer to
    re-review the regenerated report (per spec OQ #3 default —
    respawn-then-re-review). When `reviewer_iteration == 3` and
    Dim 13 still fires, verdict = `ESCALATE` (existing
    semantics — abort report generation; surface unresolved
    findings via step-10 path).
  - **Output filename**: respawned reports get a fresh
    `TS=$(date -u +%Y%m%d%H%M%S)`; the prior pair is preserved
    on disk for diff inspection. Branch & Leaf Index resolves
    the latest pair via prefix-glob (existing behaviour
    preserved).
  - **Cross-link**: subtask 05 must add a cross-reference from
    the Adversarial Review section to the Report Generation
    section so executors of either section know about the
    respawn coupling.
- [x] **Dimension 9 (peer-review thoroughness) level-conditional
      expansion**: at level `detailed`+, the reviewer must
      verify peer-review reinforcements / contradictions / gaps
      reach the report (not just the consolidation). At
      `compact` / `default`, the existing dimension-9 wording
      stands.
- [x] **Footer `theme:` annotation extended** to include the
      level: `theme: editorial / warm_palette /
      serif_headings_sans_body | level: default`.
- [x] **Report Comprehensiveness — No Information Loss** subsection
      (today lines 1006–1018) updated to reference the level mapping
      explicitly — not as a hard universal "every quantitative data
      point" rule (which now varies by level), but as a per-level rule
      pinned to `comprehensiveness.depth3_leaf_inclusion` and
      related dimensions.
- [x] **Option Comparison Research Reporting** subsection (today
      lines 1020–1066) preserved verbatim — no changes; this is
      orthogonal to comprehensiveness and applies independently when
      activation heuristics fire.
- [x] **K10b — Extend respawn protocol to honour
      `accepted_finalisation_enhancements`**:
  - Add a per-cheap-type rendering contract for each
    enhancement type in the K10a cheap taxonomy. Each contract
    must specify:
    - **Where the new section lands in the report document
      structure** (e.g. `executive_summary` → before the hero
      stat-card row, immediately after the title; `glossary` →
      end-of-document appendix before Citations;
      `decision_tree_infographic` → after the per-facet
      sections, before the cross-cutting connections section).
    - **What data shape it consumes** — read from the
      enhancement's `payload:` object in the respawn payload's
      `accepted_finalisation_enhancements:` list.
    - **Static degradation rules** per the existing
      anti-homogenisation block-list, Universal Contrast WCAG
      requirements, and D3 print-degradation contract:
      - `executive_summary` → flowing prose, no homogenised
        marketing-pill cards; respect chosen `theming` payload.
      - `action_plan` → use a horizon-grouped list (7d / 30d /
        quarter) with citations per item; render as a
        Gantt-style timeline ribbon (D3 + static fallback) OR a
        labelled tabular form respecting the chosen direction.
      - `risks_section` → use a risk-meter / gauge infographic
        (per the existing infographics catalogue); pair with a
        risk taxonomy table; print fallback shows full table.
      - `glossary` → 2-column term/definition list; respect
        chosen typography; print preserves all entries.
      - `decision_tree_infographic` → SVG decision tree; print
        fallback shows fully-expanded state (no
        click-to-expand); respects chosen `theming.preset.color_scheme`.
      - `reader_persona_tldrs` → per-persona card grid (NOT
        the homogenised three-card feature grid — vary per
        chosen direction); print preserves all personas.
      - `cross_branch_synthesis_section` → two-column or
        three-column "convergent / divergent / unique" layout
        (per chosen direction); citations attached per item.
  - **Interaction with existing minima per richness level**:
    accepted-enhancement sections / charts count **toward the
    existing minima** (≥{compact: 4, default: ?, detailed: ?,
    exhaustive: ?} charts; ≥{...} infographics; ≥{...}
    calculators per subtask 02's level mapping table). Subtask
    05 must document explicitly that an accepted
    `decision_tree_infographic` counts as an infographic;
    accepted `risks_section` with risk-meter counts as both an
    infographic (the risk meter) AND a section. The
    intent: accepting a cheap enhancement should never PUSH
    the report past its natural minima — it just makes it more
    likely the minima are reached organically, especially at
    `compact` level.
  - **Per-reason ordering in respawn handler** (per K10b
    + Risk #7 mitigation): when a respawn payload carries
    multiple `respawn_reasons:`, process in this order:
    1. `accepted_finalisation_enhancements` — additive new
       sections / charts.
    2. `missing_init_suggestion_visualisations` — additive
       new charts.
    3. `missing_init_suggestion_sections` — may be auto-resolved
       by step 1 if the accepted-enhancement type overlaps with
       a missing init-suggestion section title (subtask 06
       covers the deduplication test).
- [x] **K10b — Adversarial reviewer's Dim 13 extended to also
      audit accepted-enhancement honour**: when the prior
      iteration's respawn payload carried an
      `accepted_finalisation_enhancements:` list, the next
      iteration's reviewer verifies each accepted item appears
      in the regenerated report at its contractual location
      with at least the contracted content density. Missing
      → `MUST_FIX` AND `respawn_required: true`. This is a
      natural extension of the existing Dim 13 honour check;
      no new dimension needed.
  - **Alternative**: subtask 02 may judge that a separate
    Dim 14 ("Finalisation-enhancement honour") is cleaner.
    Either choice is acceptable; subtask 02 makes the call;
    subtask 05 implements; subtask 06 covers either way.
- [x] **K10 — Footer `theme:` annotation extended** to include
      the accepted-enhancement count: e.g.
      `theme: editorial / warm_palette /
      serif_headings_sans_body | level: default |
      finalisation-enhancements: 3 (executive_summary,
      risks_section, glossary)`. **Skip-all path**: when 0
      enhancements were accepted at the gate, the footer
      annotation MUST omit the `finalisation-enhancements:`
      segment entirely (no `finalisation-enhancements: 0`
      segment is written). This preserves byte-for-byte
      backwards-compat with pre-K10 footers — see
      `TestMeditateK10SkipAllBackwardsCompat` (subtask 06).
- [x] **K10 — Ensemble layered-cadence respawn targeting
      (resolved 2026-05-23 per OQ #10 "both layered")**:
      when an accepted enhancement was sourced from a per-tree
      candidate (i.e. `source: "tree:{model-subdir}"` in the
      root `union_candidates` list) vs a cross-model candidate
      (`source: "cross_model"`), the report-skill respawn
      targets a different report:
  - **Per-tree-sourced accept**: the next adversarial-review
    iteration's respawn payload for the **per-tree report**
    (the `{model-subdir}` tree's own report HTML/PDF pair —
    NOT the cross-model synthesis report) gains the entry under
    `accepted_finalisation_enhancements:`. The per-tree report
    skill respawns and the regenerated per-tree report
    incorporates the accepted enhancement. The cross-model
    synthesis report is NOT respawned for per-tree-sourced
    accepts (its content is sourced from
    `cross-model-synthesis.md` plus per-tree consolidations;
    the enhancement landed on the per-tree side and surfaces
    via that tree's report addendum).
  - **Cross-model accept**: the next adversarial-review
    iteration's respawn payload for the **cross-model synthesis
    report** (`report-{topic-slug}-ensemble-{ts}.html` /
    `.pdf`) gains the entry. The cross-model synthesis report
    skill respawns and the regenerated synthesis report
    incorporates the accepted cross-model enhancement.
    Per-tree reports are NOT respawned for cross-model accepts.
  - **Footer annotation per-tree vs cross-model**: per-tree
    reports' footer annotations enumerate ONLY the per-tree-
    sourced accepted enhancements; the cross-model synthesis
    report's footer enumerates ONLY the cross-model-sourced
    accepted enhancements. This keeps each report's footer
    accurate w.r.t. what was actually integrated into that
    specific report.
  - **Dim 13 (or new Dim 14, per the subtask 02 design call)
    layered audit**: at ensemble, the reviewer audits each
    accepted enhancement against the **correct** report —
    per-tree-sourced enhancements audited against the
    per-tree report; cross-model-sourced enhancements audited
    against the cross-model synthesis report. A missing
    accepted enhancement in the wrong report is NOT a finding;
    it is a finding only when the targeting rule above says it
    should be in that report.
  - **Cost-ack re-presentation for `spawn_now` at ensemble**:
    when the user opts an expensive item into `spawn_now`, the
    cost-ack re-presentation prose names which subsystems gain
    agents at which level (per-tree vs ensemble root) — per
    subtask 02's cost-ack template (extended with the
    layered-cadence subsystem breakdown).

## Definition of Done

- [x] Code implemented (markdown content updated; no Python / shell
      changes).
- [x] No linter errors in modified files.
- [x] Existing safeguards preserved verbatim (Anti-Homogenisation
      Rules, Universal Contrast, Subject-Matter Focus, citation
      discipline, light/dark mode, responsive nav, headless-Chrome
      render command, PDF print theme, TOC, paired filename rule,
      sanity-render verification gate).
- [x] `compact` level mapping reproduces today's behaviour exactly
      (verified by side-by-side comparison with subtask 01 freeze).
- [x] Adversarial reviewer's iteration cap (≤3) and severity
      classification (`MUST_FIX` / `SHOULD_FIX` / `ADVISORY`)
      preserved verbatim.

### Schema source-of-truth (cross-reference)

The canonical schema for `init-suggestions-{ts}.yml` lives in
**subtask 02's architecture-design document**
(`meditate-richness-architecture-design-20260523.md`). Both the
**write side** (subtask 04 — depth-0 manager / guide agent writes
the file after the calling-agent's combined Pattern-B resume) and
the **read side** (this subtask — report-generation skill reads
the file at the start of report generation) must conform to that
canonical schema. If at execution time the actual on-disk schema
in subtask 04's output differs from subtask 02's design doc,
treat the **design doc** as authoritative and surface the
divergence as a finding for subtask 09 (integrity review). Do
**not** silently follow whichever variant the executor encounters
first.

The phase graph dependency (this subtask depends on subtask 03;
subtask 04 is a sibling in phase 3) is intentional — both
subtasks consume the schema directly from subtask 02, not from
each other. This avoids a write-side / read-side coupling that
would otherwise force a sequential phase.

## Implementation Notes

### Edit order

1. Insert the comprehensiveness mapping table at the top of the
   `### Report Generation — MANDATORY` section so it serves as the
   contract for every subsection below.
2. Update Visualizations subsection (today lines 1068–1117) — the
   "≥4 distinct chart types" line becomes "at least
   `comprehensiveness.minima.charts.count` distinct chart types".
3. Update Infographics subsection — same pattern.
4. Update Interactive elements subsection — same pattern for
   calculators.
5. Add new "Per-Branch Section Rule" subsection.
6. Add new "Depth-3 Leaf Inclusion Rule" subsection.
7. Add new "Peer-Review Surfacing Rule" subsection.
8. Add new "Init-Suggestions Honour" subsection (rules for reading
   `init-suggestions-{ts}.yml`).
9. Update "Report Comprehensiveness — No Information Loss"
   subsection to reference the level mapping.
10. Extend the Footer subsection with the `level:` annotation.
11. Edit the Adversarial Review section to add dimensions 12 + 13
    and the dimension-9 level-conditional expansion. Update the
    "Severity classification" subsection only if the new dimensions
    introduce non-`MUST_FIX` outcomes (default: both new dimensions
    are `MUST_FIX` because they directly affect deliverable quality).

### Backwards-compat verification

After edits, run a manual diff:

- Find every numeric minimum cited in the freeze line (subtask 01).
- Confirm each appears in the `compact` row of the new mapping table.
- Confirm no numeric minimum cited in the freeze has been
  *reduced* — only the default level changes the *effective*
  minimum.

### Inputs

- `meditate-richness-architecture-design-20260523.md` (subtask 02
  output — comprehensiveness mapping table is sourced here)
- `meditate-richness-frozen-surface-20260523.md` (subtask 01 output)
- Modified `.cursor/commands/crux-meditate.md` (subtask 03 output) —
  pulls in the `comprehensiveness:` payload propagation that this
  subtask consumes.
- Modified agent file (subtask 04 output) — pulls in the
  `init-suggestions-{ts}.yml` schema this subtask reads.

### Outputs

- Modified `.cursor/commands/crux-meditate.md` Report Generation
  section + Adversarial Review section (or post-decomposition
  skill files).

## Testing Strategy

**IMPORTANT**: Do NOT trigger global test suites during parallel
execution. Subtask 06 runs the full eval coverage extension.

For local verification:

- Grep the modified file for the level enum strings: `compact`,
  `default`, `detailed`, `exhaustive` — confirm each appears
  in the mapping table.
- Grep for `comprehensiveness.minima.charts.count` (or whatever
  payload accessor pattern subtask 02 designed) — confirm every
  former hard-coded minimum has been replaced.
- Grep for `Dimension 12`, `Dimension 13`, or the new dimension
  names — confirm reviewer extensions are present.
- Confirm every existing safeguard string still present:
  `Anti-Homogenization Rules`, `Universal Contrast`, `Subject-Matter
  Focus`, `headless-Chrome`, `paired HTML + PDF`, `iteration cap`,
  `MUST_FIX`, `ESCALATE`, `mkdir`-based registry lock (Research
  mode).

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-05-23T13:12:00Z
- Completed: 2026-05-23T13:25:00Z

### Work Log

1. Read subtask file and architecture design §3, §14, §15, §16 for all normative inputs.
2. Confirmed pre-decomposition branch: `.cursor/agents/crux-cursor-meditation-guide.md` does NOT exist; `.cursor/skills/crux-skill-memory-meditation-*/` does NOT exist. Target file = `.cursor/commands/crux-meditate.md` (2142 lines after this subtask's edits, was 1910 after subtask 03).
3. Inserted Comprehensiveness Level Mapping table (12 dimensions × 4 levels) at the top of `### Report Generation — MANDATORY` with compact backwards-compat anchor, subagent-abort rule, and cross-link to adversarial reviewer sections.
4. Updated Report Comprehensiveness — No Information Loss with per-level coverage rules referencing `depth3_leaf_inclusion` and `per_branch_section_depth`.
5. Updated Option Comparison Research Reporting line to reference `comprehensiveness.minima` payload instead of hard-coded numbers.
6. Updated Visualizations subsection to read `comprehensiveness.minima.charts.count` with inline level-determined values.
7. Updated Infographics subsection to read `comprehensiveness.minima.infographics.count` with inline level-determined values.
8. Updated Interactive calculators to read `comprehensiveness.minima.calculators.count` and `comprehensiveness.minima.calculators.scenarios_per`.
9. Added Per-Branch Section Rule, Depth-3 Leaf Inclusion Rule, Peer-Review Surfacing Rule, and Init-Suggestions Honour subsections before Anti-Homogenization Rules.
10. Updated Footer structural element with `level:` annotation format and conditional `finalisation-enhancements:` segment with skip-all path and ensemble split documentation.
11. Updated Dimension 9 with the level-conditional peer-review thoroughness wording from §14.3.
12. Added Dimensions 12 (Comprehensiveness fidelity) and 13 (Init-suggestion AND finalisation-enhancement honour) after Dimension 11 with cross-links to the respawn protocol.
13. Updated iteration loop pseudo-code to add respawn_required handling with per-reason ordering and fresh-TS output-filename rule.
14. Added full Report-Skill Respawn Protocol section with: payload schema, per-reason processing order (enhancements → missing viz → missing sections), fuzzy-match auto-resolution rule (case-insensitive substring chosen), output filename rule, iteration accounting, same-iteration Dim 1–11 fix ordering, and Pattern B integrity note.
15. Added K10b Per-Cheap-Type Rendering Contract table with all 7 cheap types (landing location, payload shape, static degradation rules).
16. Added K10 Ensemble Respawn Targeting section with per-tree vs cross-model targeting rule, cost-ack ensemble subsystem prose, and Dim 13 layered audit rule.

### Fuzzy-Match Rule Choice
**Case-insensitive substring match in either direction** was chosen over Jaccard ≥0.6 on tokenised titles. Rationale: simpler to implement and reason about; substring match handles the most common overlap cases (e.g. "Executive Summary" matches "My Executive Summary" in either direction); the architecture design explicitly stated "subtask 05 picks the simpler rule."

### W1 Fix (2026-05-24)
- Applied surgical 2-line fix at `.cursor/commands/crux-meditate.md:1815`.
- Field name corrected: `additional_focus_areas_accepted[]` → `additional_focus_areas[]` with `treatment == "report_section_only"` filter.
- Canonical name aligned with subtask 02 §11, subtask 04 write-side, subtask 06 eval tests.
- Tests: full suite passes (574 passed) / SDK passes (22 passed, 6 skipped).
- Lints: clean.

### Blockers Encountered
None.

### Files Modified
- `.cursor/commands/crux-meditate.md` (was 1910 lines, now 2142 lines; +232 lines net across 16 distinct edits)
- `specs/20260523-meditate-richness/subtask-05-meditate-richness-report-contract-20260523.md` (this file — execution notes and checkbox ticks)

## Adversarial Verification (zoto-spec-judge, 2026-05-23)

Independent verification confirmed every Deliverables Checklist + Definition of Done item against:

- `.cursor/commands/crux-meditate.md` at HEAD (2142 lines confirmed)
- Subtask 02 architecture design (§3 mapping table)
- Subtask 01 frozen surface (§5 minima anchors)
- Protocol-layer pytest assertions (`TestMeditateConfigPresence` + `TestMeditateCommandDefinition` — 8/8 passed)
- Linter clean on both modified files

### Verification highlights

- **Mapping table** (lines 1551–1564): 12 dimensions × 4 levels = 48 cells, all populated; no TBD/TODO. `compact` row reproduces freeze §5 anchors exactly (charts=4, infographics=3, calculators=1, scenarios_per=3, depth3_leaf_inclusion=summary, per_branch_section_depth=consolidation_only, citation_density mode-driven, peer_review_surfacing=consolidation_only, ensemble_cross_model_depth=per_facet_cards).
- **Skip-all footer anchor** (line 1609): explicitly states "MUST be omitted entirely — it must NOT be written as `finalisation-enhancements: 0`". Anchors `TestMeditateK10SkipAllBackwardsCompat` byte-for-byte per subtask 06 plans.
- **Subsection payload accessors**: Visualizations (line 1678), Infographics (line 1729), Interactive calculators (line 1745) all read `comprehensiveness.minima.*` rather than fixed numerals.
- **Per-Branch / Depth-3 / Peer-Review / Init-Suggestions** subsections all present (lines 1782–1821) with level-conditional behaviour matching subtask 02 design §3 enum semantics.
- **Adversarial reviewer**: Dim 9 level-conditional expansion (lines 1219–1227); Dim 12 Comprehensiveness fidelity MUST_FIX (lines 1231–1239); Dim 13 Init-suggestion + finalisation-enhancement honour MUST_FIX + respawn_required (lines 1241–1252).
- **Respawn protocol** (lines 1368–1444): payload schema with `respawn_reasons:` as a list carrying all three reasons; iteration accounting (≤3 cap, respawn-then-re-review); fresh-timestamp filename rule; bidirectional cross-link with Report Generation section (line 1252 ↔ line 1570 ↔ line 1821 ↔ line 1446).
- **K10b per-cheap-type contract** (lines 1139–1151): all 7 cheap types covered (executive_summary, action_plan, risks_section, glossary, decision_tree_infographic, reader_persona_tldrs, cross_branch_synthesis_section) with landing location + payload shape + static degradation rules.
- **K10b per-reason ordering** (lines 1416–1420): `accepted_finalisation_enhancements` → `missing_init_suggestion_visualisations` → `missing_init_suggestion_sections`, with case-insensitive substring fuzzy match documented.
- **K10 ensemble layered-cadence respawn targeting** (lines 1153–1171, 1248, 1611): per-tree vs cross-model targeting; footer split; layered Dim 13 audit; cost-ack re-presentation prose names per-tree vs ensemble-root subsystems.
- **Option Comparison Research Reporting** (lines 1628–1674): preserved verbatim except for the single freeze-permitted swap of "≥4 / ≥3 / ≥1" → `comprehensiveness.minima.*` accessors in the closing paragraph (line 1674) — exactly the surgical change freeze §5.4 mandated.
- **Backwards-compatibility safeguards preserved verbatim**: Anti-Homogenization Rules (1823), Universal Contrast (1854), Subject-Matter Focus (1448, plus reviewer Dim 11 at 1229), MUST_FIX / ESCALATE / iteration cap classification (1254–1289), headless-Chrome render (1723, 1945), paired HTML + PDF (229), `mkdir`-based registry lock referenced from agent file (`.facet-registry.lock/` at line 1205).
- **Scope check**: subtask 05 modified only `.cursor/commands/crux-meditate.md` and added this subtask file under `specs/20260523-meditate-richness/`. It did NOT modify `.cursor/agents/crux-cursor-memory-manager.md` (subtask 04's scope; the `M` in git status is pre-existing), `.crux.md`/`.crux.mdc` generated files, `scripts/create-crux-zip.py`, `install.py` (pre-existing staged change), `.crux/dist-manifest.json`, or `.github/workflows/version-bump.yml`.

### Finding for subtask 09 (integrity review) — schema field-name divergence

The Init-Suggestions Honour subsection (`.cursor/commands/crux-meditate.md` line 1815) reads from `additional_focus_areas_accepted[]` with `treatment: "report_section_only"`, matching the verbatim wording of this subtask's Deliverables Checklist item. However, the canonical schema in subtask 02 (`meditate-richness-architecture-design-20260523.md` §11, lines 1156–1200) and subtask 04's write-side (`.cursor/agents/crux-cursor-memory-manager.md` lines 540–566) both use the field name `additional_focus_areas:` (with a per-item `treatment` field), NOT `additional_focus_areas_accepted[]`. The read side therefore diverges from both the authoritative design doc and the actual on-disk schema written by subtask 04. Per the schema source-of-truth rule in this subtask's "Schema source-of-truth (cross-reference)" section, the design doc is authoritative — but the deliverable text in this subtask explicitly named the divergent field, so the executor faithfully followed the literal deliverable wording. This is **not** a subtask 05 implementation failure (executor matched the deliverable verbatim); it is a spec-vs-design wording inconsistency that subtask 09 should reconcile (either rewrite the spec deliverable wording to `additional_focus_areas[]` with the existing `treatment: "report_section_only"` filter, or — less preferred — update both subtask 04 write-side AND subtask 02 design §11 to rename the array to `additional_focus_areas_accepted[]`). If left unreconciled, the report skill will look for a field that does not exist on disk and the Init-Suggestions Honour check will silently no-op for `report_section_only` focus areas.

### Verdict
**Verified** — all 14 Deliverables Checklist items and all 5 Definition of Done items independently confirmed against the on-disk artefact. The one identified divergence (schema field name) is a spec-internal wording inconsistency, not an implementation defect, and is surfaced above for subtask 09.

### Post-Execution Fix Verification (W1 + W1b)

Independent adversarial verification by `zoto-spec-judge` on 2026-05-24 confirming the W1 (read-side, `.cursor/commands/crux-meditate.md:1815`) + W1b (write-side, `.cursor/agents/crux-cursor-memory-manager.md:510` + `:512`) surgical fixes are mutually consistent and close the `additional_focus_areas` field-name divergence the subtask 09 integrity reviewer flagged (and the integrity-review judge upgraded to soft-BLOCKER).

**Verdict**: Verified.

**Per-check evidence**:

| # | Check | Result |
|---|-------|--------|
| 1 | Cross-file consistency (`additional_focus_areas_skipped\|additional_focus_areas_accepted` in `.cursor/ docs/ web/ README.md AGENTS.md CONTRIBUTORS.md`) | 0 matches |
| 2 | Same divergent-name grep across `evals/ scripts/ install.py` | 0 matches |
| 3 | Same divergent-name grep across the two target source files only | 0 matches (remaining occurrences live exclusively inside `specs/20260523-meditate-richness/` as historical context, as expected) |
| 4 | Canonical `additional_focus_areas[]` at W1 site (`.cursor/commands/crux-meditate.md:1815`) reads `every \`additional_focus_areas[]\` entry whose \`treatment == "report_section_only"\`` | Confirmed |
| 5 | Canonical `additional_focus_areas[]` at W1b sites (lines 510 + 512) with matching `treatment:` values (`skip`, `report_section_only`) | Confirmed |
| 6 | Canonical schema block at agent-file line ~556 unchanged | Confirmed |
| 7 | Python regression suite (`python3 scripts/test.py`) | **574 passed, 0 failed** (15.29s) |
| 8 | SDK eval suite (`cd evals/sdk && pnpm vitest run tests/q-meditate.test.ts`) | **22 passed, 6 skipped** (expected — expensive LLM tests gated by `SDK_EVAL_SKIP_EXPENSIVE`) |
| 9 | `ReadLints` on `.cursor/commands/crux-meditate.md`, `.cursor/agents/crux-cursor-memory-manager.md`, subtask 04 + subtask 05 spec files | No linter errors |
| 10 | Scope check: W1 + W1b touched only the two target source files + subtask 04 + 05 Work Log additions | Confirmed |
| 11 | No edits to `.crux.md` / `.crux.mdc`, `scripts/create-crux-zip.py`, `.crux/dist-manifest.json`, `.github/workflows/version-bump.yml` | Confirmed |
| 12 | Surgical scope (single-line edits at 1815 / 510 / 512, no broader rewrites) | Confirmed |
| 13 | Cohesion: W1 read-side filter (`treatment == "report_section_only"` on `additional_focus_areas[]`) and W1b write-side discriminator (`treatment: "report_section_only"` on entries of the same array) align with the canonical schema at agent-file line 556 | Confirmed |

**Field-name divergence fully closed: YES.** An LLM following the now-corrected write-side prose will produce YAML that the now-corrected read-side report contract honours; the K4 `report_section_only` opt-in mode will no longer silently no-op at runtime.
