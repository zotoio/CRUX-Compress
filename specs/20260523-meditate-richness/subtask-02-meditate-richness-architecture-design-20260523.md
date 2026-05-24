# Subtask: Architecture & Design

## Metadata
- **Subtask ID**: 02
- **Feature**: Meditate Comprehensiveness + Init-Time Suggestions
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 01
- **Created**: 20260523

## Objective

Produce the design document that subsequent implementation subtasks
(03 coordinator gates, 04 agent payload + scouting, 05 report contract)
work from. The deliverable enumerates the calling-agent gate ordering
(with the merged `Q-Cost-and-Richness-Acknowledgment` gate), the
richness level → minima mapping table, the init-suggestion data flow,
the combined askQuestion shape (with 4-mode focus-area opt-in), the
adversarial-respawn protocol design, and a **patch matrix** that
resolves dual-target landing per contract surface.

## Deliverables Checklist

- [x] `meditate-richness-architecture-design-20260523.md` written into
      the spec directory.
- [x] **Calling-agent ordering diagram** (mermaid) showing pre-spawn
      gates: Depth Selection → merged
      `Q-Cost-and-Richness-Acknowledgment` (covering depth × richness
      × mode) → Theme Preflight → … → combined Pattern-B confirmation
      that fuses `Q-Confirm-1` / `Q-Confirm-2` with the
      init-suggestions confirmation. **No standalone
      `Q-Comprehensiveness` node.**
- [x] **Richness level mapping table** — for each of `compact` /
      `default` / `detailed` / `exhaustive`, deterministic values
      for every dimension listed in K5 of the spec index
      (`comprehensiveness:` payload schema). `compact` row reproduces
      today's minima exactly.
- [x] **Cost-formula multiplier table** — agent count and token cost
      contributions per richness level, accounting for: per-leaf
      citation-table generation pass (only at `exhaustive`),
      per-branch dedicated section pass (`detailed` and `exhaustive`),
      peer-review surfacing dedicated-section pass (`detailed` and
      `exhaustive`), per-leaf output length budget. Subtask 03 uses
      this to substitute `{N}` / `{runtime}` placeholders in the
      merged gate's prompt prose.
- [x] **Worked-example cost table** — at minimum, a concrete agent
      count and token-cost estimate for the canonical anchor case
      `(depth=3, mode=Research, 3 facets, no additional focus areas)`
      for **each** of the 4 richness levels. Format:
      | Level | Agents per tree | Estimated tokens | Notes |
      |---|---|---|---|
      | compact | … | … | reproduces today's count |
      | default | … | … | richness multiplier × baseline |
      | detailed | … | … | adds per-branch dedicated section pass |
      | exhaustive | … | … | adds per-leaf citation-table pass |
      Also include a worked example for the cost re-presentation
      case where the user accepts e.g. **2** `additional_facet`
      opt-ins (`5 facets × 13 agents = 65` at depth-3 + Research,
      multiplied by the richness factor). This worked example is
      what subtask 03's prompt-prose substitution renders verbatim.
- [x] **Merged `Q-Cost-and-Richness-Acknowledgment` schema** — full
      prompt template, all option lists, per-option decision-guidance
      prose, mode-swap interaction with richness sub-question
      (preserved across swap; see spec OQ #1 default), default
      preselection rules, non-interactive abort behaviour (preserved
      from today's cost-ack — non-interactive sessions abort with
      the existing error message), and the read-only-richness
      variant used for expansion + cost re-presentation paths.
- [x] **Init-suggestion data flow** sequence diagram — depth-0
      seed exploration → suggestion payload → calling-agent
      combined Pattern-B `askQuestion` → confirmed payload →
      `init-suggestions-{ts}.yml` → propagate to children + report
      skill.
- [x] **Combined Pattern-B `needs_user_input` schema** — exact shape
      returned by depth-0 manager combining facets + sections +
      visualisations + additional-focus-areas (4-mode opt-in:
      `skip` / `additional_facet` / `report_section_only` /
      `additional_facet_AND_section`) + deep-confirm.
- [x] **Combined Pattern-B `askQuestion` schema** — exact shape the
      calling agent uses (one prompt, multiple sub-questions, per-
      sub-question decision-guidance prose).
- [x] **Additional-focus-areas reconciliation logic** — for each of
      the 4 opt-in modes, define: facet-count change (yes for
      `additional_facet` and `additional_facet_AND_section`; no for
      `skip` and `report_section_only`); report-section addition
      (yes for `report_section_only` and
      `additional_facet_AND_section`; no for `skip` and pure
      `additional_facet`); how the new branch is named / sequenced;
      cost-ack re-presentation trigger.
- [x] **`init-suggestions-{ts}.yml` schema** — confirmed payload
      shape (including separate per-item `treatment` field that
      records which of the 4 modes was chosen for each
      additional-focus-area), where it's written, who reads it,
      audit-link rules.
- [x] **Backwards-compatibility analysis** — proof that `compact`
      level reproduces today's behaviour exactly across every
      dimension.
- [x] **Patch matrix** — for each affected contract surface (from
      subtask 01's freeze), a row listing the pre-decomposition target
      file/section AND the post-decomposition target file/section,
      with a brief edit summary. This drives execution-time
      target-resolution in subtasks 03–05.
- [x] **Adversarial reviewer extension spec** — exact wording of the
      two new dimensions (Dim 12: comprehensiveness fidelity; Dim 13:
      init-suggestion honour) and the level-conditional expansion of
      dimension 9 (peer-review thoroughness).
- [x] **Adversarial respawn protocol design** — full structured
      payload schema for the respawn (cite K9 verbatim and refine
      where necessary), iteration-budget accounting rule (respawn
      shares the existing ≤3 cap and counts as one iteration; OQ #3
      default = respawn-then-re-review on iteration N+1), severity-
      classification rule (`MUST_FIX` AND `respawn_required: true`
      bypasses standard in-place reviewer fix), and a written proof
      that the protocol cannot infinite-loop (cap × deterministic
      respawn budget = bounded number of iterations).
- [x] **Eval-strategy section** — enumerate per-test-class which
      assertions to add to `evals/test_q_meditate.py` and
      `evals/sdk/tests/q-meditate.test.ts`. Subtask 06 implements;
      this design doc is the contract. Include explicit coverage
      for: merged-gate structure, 4-mode focus-area handling, cost
      re-presentation triggers, set-once-per-invocation richness,
      respawn protocol payload + budget.
- [x] **Open issues / risks** carried over from spec index Open
      Questions section (the NEW set of OQs after the user
      resolution), with proposed resolutions or escalation triggers.
- [x] **K10 — `Q-Finalisation-Enhancements` gate design**:
  - **Calling-agent ordering update** — the existing diagram
    must show the new gate position: Depth Selection → merged
    `Q-Cost-and-Richness-Acknowledgment` → Theme Preflight →
    combined Pattern-B confirmation → tree spawn + branch
    polling + (Research) peer review → consolidation +
    Branch & Leaf Index → **`Q-Finalisation-Enhancements`
    multi-select gate (NEW per K10a)** → adversarial review-and-
    fix cycle (with extended `respawn_reasons` carrying
    `accepted_finalisation_enhancements`) → report verification
    → step 10 presentation → step 11 continuation menu (with
    K10c re-application + queued-spawn-now options) → step 12
    handle selection. **Ensemble mode (layered cadence per OQ
    #10 resolution 2026-05-23)**: per-tree consolidation
    reflection writes per-tree
    `{model-subdir}/finalisation-enhancements.yml` internally
    BEFORE the aggregator runs (no per-tree askQuestion); the
    aggregator runs a second reflection over per-tree
    consolidations + `cross-model-synthesis.md` and writes the
    root combined `finalisation-enhancements.yml` (with
    `cross_model_candidates` + `union_candidates`); the
    user-facing askQuestion fires **once** at ensemble root
    over the `union_candidates` (capped at 0–5). See the new
    "K10 — Ensemble layered cadence design" deliverable below
    for the full contract.
  - **Pattern-B handoff design** — concretely document the
    handoff dance: depth-0 manager (post-decomp:
    meditation-guide) writes `consolidation.md` +
    `finalisation-enhancements.yml`, returns a
    `needs_user_input` block to the calling agent containing
    the 5 (or fewer) candidate enhancements; calling agent runs
    the multi-select askQuestion + per-item treatment
    sub-questions for expensive items + cost-ack re-presentation
    if any `spawn_now`; calling agent updates
    `finalisation-enhancements.yml` in place with `accepted` +
    `treatment` + `decided_at_utc`; calling agent resumes the
    depth-0 manager with the updated payload; depth-0 manager
    proceeds to adversarial review with the accepted
    enhancements bundled into the next iteration's respawn
    payload.
  - **`finalisation-enhancements.yml` schema** — full YAML
    schema verbatim per K10c of the spec index (every field
    typed, every enum option enumerated). Define the
    type-specific `payload:` shape per cheap-taxonomy and
    expensive-taxonomy type:
    - `executive_summary.payload`: `{ target_persona, max_paragraphs, anchor_findings }`
    - `action_plan.payload`: `{ horizons: ["7d", "30d", "quarter"], items_per_horizon, anchor_findings }`
    - `risks_section.payload`: `{ risk_taxonomy_axes, anchor_findings }`
    - `glossary.payload`: `{ term_count_estimate, anchor_branches }`
    - `decision_tree_infographic.payload`: `{ root_decision, depth, anchor_findings }`
    - `reader_persona_tldrs.payload`: `{ personas: [...], paragraphs_per_persona }`
    - `cross_branch_synthesis_section.payload`: `{ axes: ["convergent", "divergent"], anchor_findings_per_axis }`
    - `additional_meditation.payload`: `{ proposed_topic, proposed_facet_seed, recommended_depth, recommended_mode }`
    - `extracted_spec.payload`: `{ proposed_slug, overview, candidate_subtasks: [{title, agent}], spec_template: "..." }`
    - `extracted_memories.payload`: `{ candidates: [{title, type: "learning|redflag|core|idea|goal", body_summary, source_signals}] }`
    - `expanded_branch.payload`: `{ target_branch_index, recommended_new_depth, facet_emphasis_override, recommended_mode }`
  - **Follow-up artefact schemas** — for queued expensive items:
    - `follow-up-meditation-{ts}.yml` schema (mirrors
      `additional_meditation.payload` shape + standard frontmatter)
    - `follow-up-spec-{ts}.yml` schema (mirrors
      `extracted_spec.payload`)
    - `follow-up-memories-{ts}.yml` schema (mirrors
      `extracted_memories.payload`)
    - `follow-up-expansion-{ts}.yml` schema (mirrors
      `expanded_branch.payload`)
  - **Reflection contract** (impact × insight-value rubric per
    K10c) — document with worked examples per axis:
    - `impact_score = 9` looks like: enhancement directly
      enables a high-stakes decision (e.g. exec summary unblocks
      board presentation)
    - `impact_score = 5` looks like: enhancement clarifies
      reading order but doesn't change recommended action
    - `impact_score = 2` looks like: cosmetic improvement only
    - `insight_value_score = 9` looks like: surfaces a
      cross-branch synthesis no individual branch made visible
    - `insight_value_score = 5` looks like: re-organises content
      from one branch into a more readable form
    - `insight_value_score = 2` looks like: paraphrases content
      already prominent in existing sections
    - Reflection happens in the SAME pass as consolidation
      (single read of inputs — branch files + peer reviews +
      citations index + consolidation prose); subtask 04
      implements.
  - **Cost-ack re-presentation prose for `spawn_now`** — exact
    template:
    ```
    You've accepted spawning {N} follow-up agent(s) for
    finalisation enhancements ({enumerated_types}). The new
    total agent count is ~{N_total} (current depth {D},
    richness {level}, mode {mode}, including {N_finalisation}
    spawn-now agents).

    Per-type subsystem agent contribution (must be enumerated
    verbatim in the prose so the user sees which subsystems gain
    work):
      - additional_meditation × M  → spawns M top-level
        /crux-meditate invocations (each itself a nested tree;
        the per-invocation cost is computed at that nested
        meditation's own Q-Cost-and-Richness-Acknowledgment
        gate — cost-ack here only shows the M top-level spawns)
      - extracted_spec × M         → spawns M spec-generator
        agent(s)
      - extracted_memories × M     → spawns M memory-extraction
        agent(s)
      - expanded_branch × M        → spawns M branch-expansion
        subtrees (each ≈ 13 agents at depth-3 Research; subtask
        02 derives the per-mode factor from the cost-formula
        multiplier table and folds it into N_finalisation)

    [Locked: richness = {level}]
    [Locked: depth = {D}]

    Re-acknowledge or cancel.
    ```

    **No re-presentation loop guarantee**: the cost-ack
    re-presentation for `spawn_now` is a single round trip —
    user picks `re-acknowledge` (proceeds to adversarial-review
    + scheduled post-cycle spawn) OR `cancel` (drops spawn-now
    treatments back to `queue` per K10b). The re-presentation
    cannot re-fire within the same invocation; user cannot
    re-edit the spawn_now set after the cost-ack closes (the
    `finalisation-enhancements.yml` is updated in place and
    treatment decisions are immutable for the remainder of the
    invocation). Subtask 03 enforces single-shot semantics in
    the resume-handler.
  - **Respawn-handler per-reason ordering** — when respawn
    payload carries `accepted_finalisation_enhancements` AND
    `missing_init_suggestion_sections` AND/OR
    `missing_init_suggestion_visualisations`, the report skill
    processes in this order: (1) accepted enhancements
    (additive new sections / charts); (2) missing
    visualisations (additive); (3) missing sections (may be
    auto-resolved by step 1 if the accepted enhancement
    overlaps with a missing init-suggestion section). Subtask
    05 implements; subtask 06 covers via a triple-reason-
    bundle test.
  - **Non-infinite-loop proof — extended for K10b**:
    - The `accepted_finalisation_enhancements` respawn cause
      can fire AT MOST once per meditation (because the
      finalisation gate fires once, post-consolidation
      pre-adversarial-review).
    - That single firing produces respawn payload entries that
      bundle into the **first** adversarial-review iteration
      (before any review-cycle fix has run). The reviewer
      then runs and either passes (≤PASS_WITH_ADVISORIES) or
      iterates with Dim 1–11 fixes; subsequent respawns
      (iterations 2 and 3) only fire from Dim 13 missing-
      init-suggestion findings.
    - Therefore: K10 cannot increase the maximum useful
      respawn count beyond what K9 already established (≤2
      useful respawns, one per iteration boundary, max 3
      iterations). Total bounded work unchanged.
- [x] **K10 — Ensemble layered cadence design** (per OQ #10
      resolution "both layered", 2026-05-23):
  - **Per-tree reflection contract** — each model tree's
    consolidation agents (the existing per-model consolidation
    step in the ensemble protocol) capture + reflect + rank up
    to 5 candidate enhancements internally during that tree's
    consolidation phase. Document the inputs the per-tree
    reflection reads (per-tree branch files + per-tree
    consolidation prose; per-tree peer reviews when Research
    mode) — these are the SAME inputs already gathered for the
    per-tree consolidation step, so reflection is in-pass and
    adds no extra read cost beyond the LLM thinking pass.
  - **Per-tree YAML write path** — each tree writes
    `meditations/{yyyymmdd}-{topic-slug}/{model-subdir}/finalisation-enhancements.yml`
    where `{model-subdir}` matches the existing per-model
    subdirectory convention. Each per-tree candidate carries
    `source_tree: "{model-subdir}"` so root-level provenance
    labelling is unambiguous. Per-tree YAMLs are write-only at
    the per-tree level (no per-tree askQuestion fires).
  - **Root cross-model reflection contract** — after
    `cross-model-synthesis.md` is written, the ensemble
    aggregator runs a SECOND reflection pass over: (a) all
    per-tree `consolidation.md` files; (b) all per-tree
    `finalisation-enhancements.yml` (so the aggregator sees
    what each tree surfaced); (c) `cross-model-synthesis.md`
    itself. The aggregator produces up to 5 **cross-model**
    candidates emergent from looking across all trees together
    — examples of what should rank high:
    - Patterns where ≥2 trees converged on the same
      enhancement type (cross-tree convergence is signal that
      the enhancement matters at the cross-model level).
    - Patterns visible only across models (e.g. a divergence
      between two trees that suggests an `extracted_spec`
      candidate one tree didn't see).
    - Cross-model synthesis-side opportunities (e.g.
      `cross_branch_synthesis_section` is naturally
      cross-tree).
    Cross-model candidates carry `source: "cross_model"`.
  - **Root combined YAML** — aggregator writes
    `meditations/{yyyymmdd}-{topic-slug}/finalisation-enhancements.yml`
    (no `{model-subdir}` segment) containing:
    - `cross_model_candidates: [...]` (5 ranked candidates from
      the aggregator's reflection)
    - `union_candidates: [...]` denormalised top-N (capped at
      5) by composite score across `(per_tree × N) + (cross_model
      × 5)`; each entry includes `source:
      "tree:{model-subdir}" | "cross_model"` and `composite_score`.
    - The aggregator writes `surfaced_to_root: true | false`
      back to each per-tree YAML's `candidates[].surfaced_to_root`
      field (an immutable annotation indicating whether that
      per-tree candidate made the root union cap).
  - **Root single combined gate (recommended posture)** — the
    calling agent runs a single multi-select askQuestion at
    ensemble root over `union_candidates`, capped at 0–5. Each
    option label includes provenance:
    `{title} [{cost_class}] ({source-label}) — composite={N}`
    where `{source-label}` is `"cross-model"` or
    `"from tree: {model-label}"` (model label resolved from
    `cruxMemories.meditate.modelPool[i].label`). Decision-guidance
    prose explains the per-tree vs cross-model provenance so the
    user can prefer one or the other.
  - **Alternative architecture (per-tree user gates)** —
    documented but NOT the default: per-tree askQuestions inside
    each tree's flow. The architect MUST justify in writing if
    they choose this alternative — the user-specified posture is
    single combined root gate. This design doc captures the
    final per-tree-vs-root presentation call.
  - **Single-model flow unchanged** — non-ensemble Research and
    Quick flows are unchanged from K10a's original semantics
    (gate fires once after that single tree's consolidation
    completes). Document explicitly in the architecture-design
    doc so executors don't confuse single-model with ensemble.
  - **Persistence + continuation-menu interaction** — per-tree
    YAMLs persist regardless of whether their candidates
    surfaced at the root combined gate. The continuation menu
    (K10c) reads BOTH the root YAML AND every per-tree YAML
    and surfaces unchosen items:
    - `accepted: false, treatment: "unchosen_persisted"` in the
      ROOT YAML → labelled `(was offered at ensemble root)`.
    - `surfaced_to_root: false` in a per-tree YAML (candidate
      never reached the root combined gate) → labelled
      `(from tree: {model-label}, not surfaced at root)`.
    Re-applying a per-tree-only unchosen item targets the
    per-tree report respawn (per subtask 05); re-applying a
    root unchosen item targets the cross-model synthesis report
    respawn unless the union entry's `source: "tree:..."`
    indicates otherwise (in which case it targets the per-tree
    report respawn for that tree).
  - **Non-infinite-loop proof — extended for layered cadence**:
    - Per-tree reflection writes happen exactly once per tree
      (bound by `modelPool` size, currently 3 — a constant).
    - Root combined reflection happens exactly once.
    - Root combined askQuestion happens exactly once per
      invocation (mirror of K10a single-model bound).
    - Therefore: layered cadence adds at most `N + 1` reflection
      writes (N = `modelPool` size) + 1 root user gate, all
      bounded. Cannot increase the K10b respawn bound (which
      remains ≤2 useful respawns, per K9 cap).
- [x] **Patch matrix extended for K10**: add rows to the patch
      matrix for:
  - `Q-Finalisation-Enhancements` insertion target (pre-decomp:
    new section in `.cursor/commands/crux-meditate.md` between
    the consolidation step description and the adversarial
    review section; post-decomp: new section in
    `crux-skill-memory-meditation-coordination/SKILL.md` OR a
    new `crux-skill-memory-meditation-finalisation/SKILL.md`
    if the architect judges that cleaner — flag as an
    architecture-design decision).
  - Consolidation reflection contract location (pre-decomp:
    extend `crux-cursor-memory-manager.md` Meditate Mode step
    8 sub-step list; post-decomp: add to
    `crux-skill-memory-meditation-research/SKILL.md` and
    `crux-skill-memory-meditation-quick/SKILL.md`).
  - Continuation-menu extension (pre-decomp: extend step 12 in
    coordinator command; post-decomp: extend coordinator
    command continuation-menu section).
  - `finalisation-enhancements.yml` artefact entry in
    Coordination Conventions filename table + Branch & Leaf
    Index Top-level artifacts enumeration.
- [x] **Eval-strategy section extended for K10**: enumerate the
      new test classes subtask 06 must add (per the spec index
      Requirements list 22).

## Definition of Done

- [x] Markdown-only artefact (no code edits).
- [x] Every dimension in K5's `comprehensiveness:` payload schema has
      a concrete value defined for every level (no "TBD" cells).
- [x] Patch matrix lists both pre- and post-decomposition targets for
      every contract item from subtask 01's freeze.
- [x] Combined askQuestion schema is concrete enough that subtask 03
      can implement without further clarification.
- [x] No linter errors introduced.

## Implementation Notes

### Comprehensiveness level mapping table — required dimensions

For each of `compact / default / detailed / exhaustive`, define:

1. `minima.charts.count` — minimum chart count (Chart.js + D3 combined).
2. `minima.charts.types_required` — required chart types or facet-kind coverage.
3. `minima.infographics.count` — minimum infographic count.
4. `minima.infographics.types_required` — required infographic types.
5. `minima.calculators.count` — minimum interactive calculator count.
6. `minima.calculators.scenarios_per` — minimum pre-computed
   what-if scenarios per calculator (today's contract is 3–5; level
   should set this).
7. `depth3_leaf_inclusion` — `elided` (depth-3 material lives only in
   branch files) / `summary` (depth-3 findings summarised in report)
   / `verbatim_quotes` (depth-3 leaves quoted with citation).
8. `per_branch_section_depth` — `consolidation_only` (no per-branch
   section) / `branch_summary` (one section per branch, summary level)
   / `per_leaf_detail` (one section per branch with per-leaf
   subsections).
9. `citation_density` — `warn_only` (Quick-mode-style) / `mandatory`
   (Research-mode-style — current default in Research) /
   `per_finding_table` (every finding cell in a table carries an
   inline citation column).
10. `peer_review_surfacing` — `consolidation_only` (peer-review folded
    into consolidation prose) / `named_section` (one report section
    presents reinforcements/contradictions/gaps cross-cutting all
    branches) / `per_branch_dedicated` (one named section per branch
    presenting that branch's reinforcements/contradictions/gaps).
11. `section_length_budget_tokens` — `{ hero, per_facet, citations }`
    target ranges so the report doesn't blow up at high levels.
12. `ensemble_cross_model_depth` — `synthesis_only` /
    `per_facet_cards` / `per_leaf_attribution`.

**Constraint**: `compact` level MUST reproduce the current behaviour.
That means:
- `minima.charts.count = 4` (matches current ≥4)
- `minima.infographics.count = 3` (matches current ≥3)
- `minima.calculators.count = 1` (matches current ≥1)
- `minima.calculators.scenarios_per = 3` (matches current 3–5)
- `depth3_leaf_inclusion = "summary"` (matches current behaviour where
  consolidation summarises but verbatim leaf quotes are rare)
- `per_branch_section_depth = "consolidation_only"` (matches today —
  consolidation is the primary input)
- `citation_density = "mandatory"` in Research mode / `warn_only` in
  Quick mode (matches current Quick / Research split — citation
  density is **mode-driven, preserved across every level**; see
  spec OQ #5 for the `exhaustive` × Quick carve-out)
- `peer_review_surfacing = "consolidation_only"` (matches today)
- `ensemble_cross_model_depth = "per_facet_cards"` (matches today's
  ensemble report extras)

`default` (the new default-when-unspecified — note the level is
literally named `default`) bumps every dimension at least one notch
above `compact` where there's headroom; `detailed` bumps further;
`exhaustive` maxes them all out.

### Patch matrix shape

| Contract item | Pre-decomp target | Post-decomp target | Edit summary |
|---|---|---|---|
| `Q-Depth-Selection` location | `.cursor/commands/crux-meditate.md` lines 55–105 | `.cursor/commands/crux-meditate.md` (thinned) — coordinator section | No edit; cited as anchor for the merged gate that follows |
| `Q-Cost-Acknowledgment` rename + merge | `.cursor/commands/crux-meditate.md` lines 106–189 | `.cursor/commands/crux-meditate.md` (thinned coordinator) | Rename section to `Q-Cost-and-Richness-Acknowledgment`; add richness Sub-Q1 (4-level enum, default `default`); update prompt prose to display depth × richness × mode in one round trip; update agent-count formula with richness multipliers; add read-only-richness variant for expansion + cost-re-presentation paths |
| `Q-Confirm-1` askQuestion | `.cursor/commands/crux-meditate.md` lines 295–337 | `.cursor/commands/crux-meditate.md` (thinned coordinator) | Replace with combined Pattern-B askQuestion (facets + sections + visualisations + 4-mode focus-area opt-in + deep-confirm) |
| `Q-Confirm-2` askQuestion | `.cursor/commands/crux-meditate.md` lines 338–361 | as above | Fold into combined Pattern-B askQuestion |
| Init-suggestions production (depth-0 step 4) | `.cursor/agents/crux-cursor-memory-manager.md` lines 360–446 | `.cursor/agents/crux-cursor-meditation-guide.md` + `crux-skill-memory-meditation-research/SKILL.md` | Extend step 4 to also produce sections / visualisations / additional-focus-areas (with per-item recommended treatment from the 4-mode set) |
| Report-generation minima | `.cursor/commands/crux-meditate.md` lines 1068–1172 | `.cursor/skills/crux-skill-memory-meditation-report/SKILL.md` | Replace fixed minima with level-driven mapping (`compact` row reproduces today's exactly) |
| Comprehensiveness payload propagation | both files (`comprehensiveness:` added to spawn prompt + propagated through Phase D / Quick step 3) | guide agent + research/quick skills | Add payload to every spawn-prompt enumeration; subagent abort rule mirrors `theming` |
| Adversarial reviewer 11 dims → 13 dims | `.cursor/commands/crux-meditate.md` lines 759–771 | `.cursor/skills/crux-skill-memory-meditation-review/SKILL.md` | Add Dim 12 (comprehensiveness fidelity) + Dim 13 (init-suggestion honour); level-conditional expansion of Dim 9 (peer-review thoroughness) |
| Adversarial respawn protocol (Dim 13) | `.cursor/commands/crux-meditate.md` Adversarial Review section + Report Generation section (cross-link) | `.cursor/skills/crux-skill-memory-meditation-review/SKILL.md` + `.cursor/skills/crux-skill-memory-meditation-report/SKILL.md` | Add respawn payload schema; iteration-budget rule (shares ≤3 cap; counts as 1 iteration; respawn-then-re-review semantics); severity rule (`respawn_required: true` bypasses in-place fix); written non-infinite-loop proof |
| Cost re-presentation on additional-facet acceptance | `.cursor/commands/crux-meditate.md` Facet Confirmation resume-handler section (lines ~360+) | as above (post-decomp coordinator) | Document the trigger (`additional_facet` or `additional_facet_AND_section` accepted) + the re-presented gate's read-only-richness shape |
| Branch & Leaf Index Top-level artifacts | `.cursor/commands/crux-meditate.md` lines 824–838 | `.cursor/skills/crux-skill-memory-meditation-coordination/SKILL.md` | Add `init-suggestions-{ts}.yml` link to Top-level artifacts enumeration |
| Set-once-per-invocation richness rule | `.cursor/commands/crux-meditate.md` `Q-Cost-Acknowledgment-Expansion` subsection + Re-spawn semantics subsection | as above | Document persistence rule (richness shown locked in expansion variant; reused unchanged on continuation; no `--reset-richness` flag) |
| Eval coverage | `evals/test_q_meditate.py` + `evals/sdk/tests/q-meditate.test.ts` | same files (evals are not decomposed by 20260517) | Extend with K1–K9 assertions including merged-gate structure, 4-mode focus-area, set-once persistence, respawn protocol, finite-iteration check |

(This is the SHAPE of the matrix; subtask 02 fills it in fully — the
example above is illustrative, not exhaustive.)

### Combined Pattern-B `askQuestion` design

Today's flow runs `Q-Confirm-1` then `Q-Confirm-2` as two separate
prompts. The new flow folds both into a single round trip with these
sub-questions in one `needs_user_input` block:

1. **Facets confirmation** (single-select, required) — same option set
   as today's `Q-Confirm-1`.
2. **Sections confirmation** (multi-select, defaults all checked) —
   each draft section has `[checked] {title} — {one-line rationale}`.
3. **Visualisations confirmation** (multi-select, defaults all
   checked) — each draft visualisation type has `[checked] {type} —
   {what it would show}`.
4. **Additional focus areas opt-in** (per-item single-select, default
   `skip`) — for each additional focus area: `skip` /
   `additional_facet` / `report_section_only` /
   `additional_facet_AND_section`. Decision-guidance prose MUST
   explain the cost difference between the four modes (cost change
   only when one of the two `additional_facet`-bearing modes is
   chosen → triggers cost-ack re-presentation).
5. **Deep-confirm enum** (single-select, default `none`) — same option
   set as today's `Q-Confirm-2`.

Subtask 03 implements; subtask 02 designs the prompt template, the
decision-guidance prose for each sub-question, and the resume-handler
contract.

### Merged `Q-Cost-and-Richness-Acknowledgment` design

The renamed gate runs as the second pre-spawn gate. It owns
**richness selection + cost acknowledgment + mode swap + cancel**
in a single round trip.

Sub-questions:

1. **Richness level** (single-select, required, default = `default`):
   `compact` / `default` / `detailed` / `exhaustive`. Decision-
   guidance text per option must concretely describe what the level
   means for the report (chart counts, depth-3 inclusion behaviour,
   length budgets) so the user is picking informedly.
2. **Proceed / mode-swap / cancel** (single-select, required, same
   option set as today's `Q-Cost-Acknowledgment`): `proceed` /
   `switch_to_quick` / `switch_to_research` / `switch_to_ensemble`
   / `switch_to_single` / `cancel`. Mode-swap PRESERVES the
   richness selection (per spec OQ #1 default).

Prompt prose displays:

- The depth selected in `Q-Depth-Selection`.
- For each richness level option, the resulting agent-count
  estimate × runtime estimate, computed via the cost-formula
  multiplier table (defined elsewhere in this design document).
- The cost summary for the **currently-highlighted** combination
  (depth × richness × mode), updated as the user changes their
  picks if the askQuestion UI supports it; otherwise show all
  combinations in a compact table.

**Read-only-richness variant** — used by:

- `Q-Cost-Acknowledgment-Expansion` (calling-agent step 12
  expansion path).
- Cost re-presentation on `additional_facet` or
  `additional_facet_AND_section` acceptance (per K2 + K4).

In the read-only-richness variant: Sub-Q1 is shown as a locked
display row (current richness level + lock icon / "(locked)"
notation), not a select; only Sub-Q2 is interactive. Prose
preamble names the trigger so the user understands why it's
re-presented (e.g. "Cost has changed because you accepted N
additional facets — please re-acknowledge or cancel.").

### Cost-ack re-presentation rule

If the combined Pattern-B askQuestion result includes any
`additional_focus_areas` opted into `additional_facet` OR
`additional_facet_AND_section`, the calling agent must:

1. Recompute the per-tree agent count using the new facet count
   (today's count assumes 3 facets; each additional facet adds
   `1 + 3 + 9 = 13` agents at depth 3 in Research mode, plus the
   richness multipliers from the cost-formula table).
2. Run the **read-only-richness variant** of
   `Q-Cost-and-Richness-Acknowledgment` with the updated count,
   framed as a re-confirmation. Richness is shown locked per K6
   (set-once-per-invocation).
3. If the user cancels at this point, abort the meditation and
   delete `facets-pending-{ts}.yml` and any pending
   init-suggestions coordination files (the not-yet-written
   `init-suggestions-{ts}.yml` is never created in the cancel
   path).

If only `report_section_only` or `skip` decisions were made, no
re-ack is needed (no agent-count change). `additional_facet_AND_section`
counts as a facet-bumping mode for re-ack purposes — the additional
report-section side-effect doesn't add agent cost beyond what the
new facet itself contributes.

### Adversarial respawn protocol — non-infinite-loop proof

Subtask 02 must include a written argument that the respawn
protocol cannot infinite-loop. Sketch:

- The adversarial review-and-fix cycle has a hard cap of ≤3
  iterations (frozen by 20260517).
- A respawn is bundled into the iteration that flagged Dim 13
  (per K9; per spec OQ #3 default = respawn-then-re-review on
  iteration N+1). The iteration counter advances once per
  review-and-fix cycle regardless of whether the cycle triggered
  a respawn; respawns do **not** carve out a separate retry
  budget.
- **Maximum useful respawns per meditation = 2.** Respawn can be
  triggered at the end of iteration 1 (its output is reviewed at
  iteration 2) and at the end of iteration 2 (its output is
  reviewed at iteration 3). A respawn at iteration 3 would have
  no iteration 4 to review the regenerated report, so iteration
  3 with Dim 13 still firing **always resolves to `ESCALATE`,
  never a respawn**. (An implementation that issues a wasted
  third respawn would still be bounded — total respawns ≤ 3 —
  but the intended control flow halts at `ESCALATE`.)
- After iteration 3, if Dim 13 still fires, verdict =
  `ESCALATE` (existing semantics — abort report generation;
  surface unresolved findings).
- The respawn payload is **deterministic** (function of
  `init-suggestions-{ts}.yml` + branch evidence pointers + prior
  report paths) — there is no source of non-termination in the
  payload itself.
- Therefore: respawn protocol ≤ 2 useful respawns × 1
  report-skill run each = bounded total work; cannot
  infinite-loop.

This proof is part of subtask 02's deliverable; subtask 09
(integrity review) verifies it.

### Inputs

- `meditate-richness-frozen-surface-20260523.md` (subtask 01 output)
- `meditate-frozen-contract-20260517.md` (sibling freeze line)
- Spec index `spec-meditate-richness-20260523.md`

### Outputs

- `specs/20260523-meditate-richness/meditate-richness-architecture-design-20260523.md`

## Testing Strategy

**IMPORTANT**: Do NOT trigger global test suites during parallel execution.

Documentation-only subtask. Verify by:

1. Confirming every dimension in the comprehensiveness mapping has a
   concrete value at every level (no "TBD" or "TODO").
2. Confirming the patch matrix covers every contract item listed in
   subtask 01's freeze.
3. Confirming the `compact` row matches today's behaviour exactly.
4. Confirming the combined askQuestion schema is detailed enough for
   subtask 03 implementation (per-question decision-guidance prose
   present, resume-handler contract specified, default values defined).
5. Confirming the eval-strategy section enumerates per-test-class
   assertions concretely (so subtask 06 can implement).

## Execution Notes

### Agent Session Info
- Agent: `crux-platform-architect` (subagent of spec executor)
- Started: 2026-05-23
- Completed: 2026-05-23

### Work Log

- Read subtask 02 deliverables checklist (15 top-level items, several with 6+ sub-items).
- Loaded subtask 01 freeze (`meditate-richness-frozen-surface-20260523.md`) and the spec index (`spec-meditate-richness-20260523.md` K1–K10c + Requirements + Open Questions + Risks + assessment file).
- Loaded sibling `meditate-frozen-contract-20260517.md` for cross-references.
- Confirmed pre-decomp branch live at HEAD (no `crux-cursor-meditation-guide.md`; no `crux-skill-memory-meditation-*` skills; `crux-meditate.md` 1493 lines; `crux-cursor-memory-manager.md` 946 lines).
- Authored `meditate-richness-architecture-design-20260523.md` covering all 15 Deliverables Checklist items + 4 DoD items.
- Resolved Decision 2 (Dim 13 vs Dim 14) → **extend Dim 13** (justification §14.5).
- Resolved post-decomp K10 gate location → extend `crux-skill-memory-meditation-coordination/SKILL.md` (per K8 spirit; no new skill directory).
- Folded assessment R5–R8 NICE_TO_HAVEs into architecture decisions (cross-model rubric calibration, model-label fallback, per-report ≤3 cap, per-tree reflection cost in cost-ack table).
- Patch matrix landed with 21 rows covering all 14 freeze items + cost-re-presentation + set-once + 4 K10 surfaces + eval coverage. Pre-decomp and post-decomp columns both populated with file:lines.

### Blockers Encountered
None.

### Files Modified
- `specs/20260523-meditate-richness/meditate-richness-architecture-design-20260523.md` (new file — sole architectural deliverable)
- `specs/20260523-meditate-richness/subtask-02-meditate-richness-architecture-design-20260523.md` (this file — Deliverables / DoD ticks + Execution Notes)
- `specs/20260523-meditate-richness/spec-meditate-richness-20260523.md` (Execution Notes / Cross-references — link added to the new architecture-design doc)

### Adversarial Verification (zoto-spec-judge, 2026-05-23 22:39 UTC+10)

Independent verification pass against the as-shipped
`meditate-richness-architecture-design-20260523.md` (2553 lines). All
15 top-level Deliverables Checklist items + 5 Definition of Done
items confirmed present, concrete, and K1–K10-faithful. Verdict:
**Verified**. Every tick above is authoritative per the judge.

**Spot-check results** (5 random pre-decomp `file:lines` anchors
from the patch matrix §13 cross-checked against live source):

| Anchor | File:lines | Result |
|--------|-----------|--------|
| `Q-Cost-Acknowledgment` options | `.cursor/commands/crux-meditate.md:158-166` | ✓ matches verbatim |
| `Q-Confirm-1` prompt + options | `.cursor/commands/crux-meditate.md:311-330` | ✓ matches verbatim |
| Chart minima ≥4 | `.cursor/commands/crux-meditate.md:1068-1070` | ✓ matches verbatim |
| Adversarial review 11 dimensions | `.cursor/commands/crux-meditate.md:759-771` | ✓ matches verbatim |
| Depth-0 Meditate Mode steps 1–13 | `.cursor/agents/crux-cursor-memory-manager.md:360-446` | ✓ matches verbatim (step 8 consolidation reads 3 depth-1 + 3 peer + citations-index per row #18 of patch matrix) |

**K1–K10 fidelity spot-checks**:

- §3 compact row deterministic values: `charts=4, infographics=3,
  calculators=1, scenarios_per=3, depth3_leaf_inclusion="summary",
  per_branch_section_depth="consolidation_only",
  citation_density` mode-driven (Research=mandatory; Quick=warn_only),
  `peer_review_surfacing="consolidation_only",
  ensemble_cross_model_depth="per_facet_cards"` — **all confirmed**.
- §5.1 K2 worked-example cost table covers all 4 richness levels ×
  (D=3, Research, 3 facets); §5.3 covers the
  `additional_facet × 2` re-presentation case (5 facets × ~72
  agents per tree); §5.4 covers `spawn_now` re-presentation — **all
  confirmed**.
- §8 combined Pattern-B `needs_user_input` schema enumerates
  facets + sections + visualisations + additional_focus_areas
  (4-mode) + deep_confirm — **confirmed**.
- §9 combined Pattern-B `askQuestion` schema includes all 5
  sub-questions with per-option `decision_guidance` prose,
  follow-up text inputs for `additional_facet_AND_section`, and
  `resume_handler.cost_change_check` rule — **confirmed concrete
  enough for subtask 03 to implement (DoD #4 satisfied)**.
- 4 modes verbatim: `skip` / `additional_facet` /
  `report_section_only` / `additional_facet_AND_section` —
  **confirmed in §9 + §10 + §11**.
- K6 set-once: §6.7 read-only-richness variant locks richness in
  expansion variant; no `--reset-richness` flag documented anywhere
  — **confirmed**.
- §15.1 respawn payload: `respawn_reasons` typed as a **list**
  carrying `missing_init_suggestion_sections`,
  `missing_init_suggestion_visualisations`,
  `accepted_finalisation_enhancements` — **confirmed**.
- Three non-infinite-loop proofs present:
  §15.5 (K9 base), §15.6 (K10b extension), §17.9 (K10 layered
  cadence) — **confirmed**.
- §16.3 enumerates all 11 type-specific `payload:` shapes
  (7 cheap: `executive_summary`, `action_plan`, `risks_section`,
  `glossary`, `decision_tree_infographic`, `reader_persona_tldrs`,
  `cross_branch_synthesis_section`; 4 expensive:
  `additional_meditation`, `extracted_spec`, `extracted_memories`,
  `expanded_branch`) — **confirmed**.
- §17 K10 layered cadence (OQ #10 "both layered"): per-tree YAML
  write path at `{model-subdir}/finalisation-enhancements.yml`
  (§17.2) + root cross-model reflection (§17.3) + root combined
  YAML with `cross_model_candidates` + `union_candidates` (§17.4)
  + root single combined askQuestion as recommended posture
  (§17.5 + §17.6 alternative documented and rejected) —
  **confirmed**.

**Patch matrix audit** (§13, 21 rows):

- All 14 freeze items from subtask 01 mapped to at least one row.
- 4 K10 sub-items added (rows #17 `Q-Finalisation-Enhancements`
  insertion, #18 consolidation reflection contract, #19
  continuation-menu extension, #20 `finalisation-enhancements.yml`
  artefact entry) — **confirmed**.
- Both pre-decomp AND post-decomp columns populated with concrete
  `file:lines` for every row — **confirmed (DoD #3 satisfied)**.

**Code-edit check**: `git status` shows the entire
`specs/20260523-meditate-richness/` directory as untracked (no
modifications to `.cursor/**`, `evals/**`, `scripts/**`,
`install.py`, `.crux/**`, `.github/**`, `web/**`, `docs/**`
attributable to subtask 02). The 20260517 changes in `git status`
predate this spec and are not subtask 02's doing — **confirmed
(DoD #1 satisfied)**.

**Lint check**: `ReadLints` on the new architecture-design file +
the modified subtask 02 file + the modified spec index returns
zero errors — **confirmed (DoD #5 satisfied)**.

**DoD #2 — K5 mapping table has concrete value at every level**:
§3 table renders all 12 dimensions × 4 levels = 48 cells with
concrete values; no "TBD" / "TODO" / "???" / placeholder text in
the cells (the only `TBD` / `no TBDs` literals in the document
are self-claiming meta-references in §1, §13 footer, and §19.4,
not actual mapping-table cells) — **confirmed**.

No deviations from K1–K10. Subtask 02 is approved for downstream
consumption by subtasks 03–09.
