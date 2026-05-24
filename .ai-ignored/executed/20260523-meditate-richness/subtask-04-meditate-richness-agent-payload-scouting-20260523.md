# Subtask: Agent / Guide — Payload Propagation + Init-Time Scouting

## Metadata
- **Subtask ID**: 04
- **Feature**: Meditate Comprehensiveness + Init-Time Suggestions
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 02
- **Created**: 20260523

## Objective

Implement the agent-side changes required for the new payload to flow
through the tree and for init-time suggestions to be produced as part
of the depth-0 seed exploration. Two concerns rolled into one subtask
because they touch the same file region (depth-0 manager step 4 +
child agent input parameters):

1. **Comprehensiveness payload propagation** — depth-0 manager
   receives `comprehensiveness:` from spawn prompt and forwards
   unchanged to every child agent (and every ensemble member tree).
2. **Init-time scouting** — depth-0 manager extends step 4 (facet
   derivation) to also produce a draft suggestions payload (sections,
   visualisations, additional focus areas) and includes it in the
   same Pattern-B `needs_user_input` block as the proposed facets.

## Deliverables Checklist

- [x] Resolve target file at execution time per subtask 02 patch matrix:
  - **Pre-decomposition**: edit `.cursor/agents/crux-cursor-memory-manager.md`
    Meditate Mode sections (lines 360–446 depth-0 workflow, lines
    472–550 Phases A–G, lines 552–593 Quick 6-step, lines 872–907
    Ensemble Aggregation).
  - **Post-decomposition**: edit `.cursor/agents/crux-cursor-meditation-guide.md`
    + `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md`
    + `.cursor/skills/crux-skill-memory-meditation-quick/SKILL.md`
    + `.cursor/skills/crux-skill-memory-meditation-ensemble/SKILL.md`.
- [x] **Depth-0 spawn-prompt input parameters extended** to include
      `comprehensiveness:` (alongside existing `theming:`,
      `confirmDeepFacets`, `meditateMode`, `maxDepth`, etc.). Subagent
      MUST abort with a clear error if missing.
- [x] **Depth-0 manager step 4 extended** to ALSO produce a draft
      suggestions payload during seed exploration:
  - `proposed_sections: [{title, rationale, source_signals: [...]}]`
    (3–8 items)
  - `proposed_visualisations: [{type, rationale, source_signals: [...]}]`
    (5–10 items, each from the existing Chart.js / D3 / infographic
    catalogue)
  - `additional_focus_areas: [{title, rationale, recommended_treatment: "skip" | "additional_facet" | "report_section_only" | "additional_facet_AND_section"}]`
    (0–5 items; recommend the cheaper `report_section_only` by
    default unless evidence justifies promoting to facet — the
    user can override per-item to any of the 4 modes including
    `additional_facet_AND_section` for both effects)
- [x] **Combined `needs_user_input` block** returned by depth-0
      manager — facets + sections + visualisations + additional focus
      areas + (existing) deep-confirm prompt — per the schema in
      subtask 02's design doc.
- [x] **Resume-handler logic** in depth-0 manager that consumes the
      calling agent's combined answers, applies facet decisions,
      writes confirmed sections / visualisations / additional-focus
      items, and propagates the resulting structured payload to
      every child agent spawn.
- [x] **Phase D / Quick step 3 / Ensemble step 7 spawn prompt
      enumerations** extended to include `comprehensiveness:` in the
      "child receives all parameters including" lists.
- [x] **Children honour comprehensiveness** in their output:
  - Depth-3 leaves include verbatim quotes when level ≥ `detailed`.
  - Output `## Discoveries` section length budget respects
    `section_length_budget_tokens.per_facet`.
  - Citation density adjusted per level (`per_finding_table` mode at
    `exhaustive` writes citation columns into every finding table).
  - Citation **validation** rule remains mode-driven (Quick = warn-
    only; Research = mandatory) at every level — see spec K7
    + OQ #5.
- [x] **Ensemble propagation** — `comprehensiveness:` shared across
      all model trees just like `theming` and `preConfirmedFacets`.
- [x] **`init-suggestions-{ts}.yml` write logic** — the depth-0
      manager (after the calling agent resumes it with confirmed
      sections / visualisations / additional-focus-areas) writes the
      confirmed payload to `init-suggestions-{ts}.yml` in the working
      directory. The audit file is NOT written by the calling agent;
      it is written by the depth-0 manager during the resume step
      (consistent with how confirmed facets become `facets.md`).
- [x] **K10c — Consolidation reflection contract** added at the
      tail of the depth-0 manager's consolidation step (currently
      step 8 sub-step 4 in the agent file pre-decomp; post-decomp:
      end of the consolidation skill's contract). The depth-0
      manager (or post-decomp meditation-guide invoking the
      coordination skill) must:
  - Read the same inputs already gathered for consolidation:
    branch files (all depths), peer-review files (Research mode),
    `citations-index.yml` (Research mode), `consolidation.md`
    just written.
  - Produce a candidate set of finalisation enhancements drawn
    from the K10a menu (cheap + expensive taxonomy). Caps:
    consider all menu types but materialise only those the
    branches' findings + consolidation surface as relevant.
  - Score each candidate on `impact_score` (1–10) and
    `insight_value_score` (1–10) using the rubric defined in
    K10c of the spec index. Worked examples per axis MUST be
    documented in the consolidation step's prose so an LLM
    agent can apply the rubric deterministically:
    - `impact_score = 9` → enhancement directly enables a
      high-stakes decision (e.g. exec summary unblocks board
      presentation)
    - `impact_score = 5` → enhancement clarifies reading order
      but doesn't change recommended action
    - `impact_score = 2` → cosmetic only
    - `insight_value_score = 9` → surfaces a cross-branch
      synthesis no individual branch made visible
    - `insight_value_score = 5` → re-organises content from
      one branch into a more readable form
    - `insight_value_score = 2` → paraphrases content already
      prominent in existing sections
  - Compute `composite_score = impact_score *
    insight_value_score` (multiplicative; configurable via
    `cruxMemories.meditate.finalisationEnhancements.weights`
    per K10 OQ #11; if `weights` set or `formula:
    "weighted_sum"` configured, use weighted-sum instead).
  - Filter out candidates below `minimum_impact_threshold`
    (default 6 per K10 OQ #12).
  - Take the top 5 by `composite_score` (descending). Tie-break
    on `cost_class: "cheap"` ahead of `expensive` (cheaper
    candidates promoted on tie — they're lower-risk to accept).
  - If fewer than 5 candidates clear the threshold, set
    `degradation_reason` accordingly and emit whatever count
    surfaced. If zero, set
    `degradation_reason: "no high-quality candidates surfaced"`
    and skip the askQuestion entirely (workflow proceeds to
    adversarial review unchanged).
- [x] **K10c — Write `finalisation-enhancements.yml`** in the
      working directory BEFORE returning control to the calling
      agent for the new askQuestion gate. Schema must match the
      K10c YAML verbatim (every required field populated:
      `generated_utc`, `topic_slug`, `rubric: { impact_score_max,
      insight_value_score_max, minimum_impact_threshold, weights }`,
      `degradation_reason`, `candidates: [{...}]`). Each
      candidate MUST carry: `id`, `type`, `cost_class`, `title`,
      `description`, `impact_score`, `insight_value_score`,
      `composite_score`, `source_signals: [...]`, `payload:
      {...type-specific...}`, and the three calling-agent-
      filled-later fields (`accepted: null`, `treatment: null`,
      `decided_at_utc: null`).
- [x] **K10c — Per-type payload shapes** documented per the
      catalogue in subtask 02's deliverables checklist (each
      cheap and expensive type has its own `payload:` shape).
      Subtask 04 implements the shape produced by the
      consolidation reflection step.
- [x] **K10b — Resume-handler logic for accepted enhancements**:
      when the calling agent resumes the depth-0 manager after
      the askQuestion + treatment sub-questions + (any) cost-ack
      re-presentation, the depth-0 manager:
  - Reads the updated `finalisation-enhancements.yml`.
  - For each `accepted: true, treatment: "respawn"` (cheap):
    builds an entry for the next adversarial-review
    iteration's respawn payload's
    `accepted_finalisation_enhancements:` list (per K9
    extended schema). Adds `accepted_finalisation_enhancements`
    to the iteration's `respawn_reasons:` list.
  - For each `accepted: true, treatment: "queue"` (expensive,
    default): writes the appropriate
    `follow-up-{type}-{ts}.yml` next to `consolidation.md` per
    the schemas defined in subtask 02. Does NOT spawn agents.
  - For each `accepted: true, treatment: "spawn_now"`
    (expensive, opt-in): defers spawning until AFTER the
    adversarial-review cycle completes (so the respawned
    report incorporates accepted cheap enhancements before
    expensive follow-ups run); returns a structured
    `pending_spawn_now: [...]` list to the calling agent on
    final return so the calling agent can spawn at the right
    moment.
- [x] **K10 — Ensemble layered cadence (resolved 2026-05-23
      per OQ #10 "both layered")**: the ensemble-aggregation
      function (today in `crux-cursor-memory-manager.md` lines
      872–907; post-decomp: `crux-skill-memory-meditation-ensemble/SKILL.md`)
      gains BOTH a per-tree reflection obligation AND a root
      cross-model reflection obligation:
  - **[x] Per-tree obligation**: every per-model tree's consolidation
    step now ends with a reflection pass that picks up to 5
    candidate enhancements scored on the same impact ×
    insight-value rubric (above). Each tree writes
    `meditations/{yyyymmdd}-{topic-slug}/{model-subdir}/finalisation-enhancements.yml`
    BEFORE the ensemble aggregator runs. The per-tree YAML
    schema mirrors the single-model schema with two extras:
    - Every `candidates[]` entry carries `source_tree:
      "{model-subdir}"` so root-level provenance labelling is
      unambiguous.
    - Each `candidates[]` entry gets a `surfaced_to_root: null`
      placeholder field that the aggregator fills with `true |
      false` later (indicating whether this per-tree candidate
      made the root combined gate's union cap).
    - No askQuestion fires at the per-tree level — per-tree
      YAMLs are write-only and audit-only at this stage.
  - **Root cross-model obligation**: AFTER `cross-model-synthesis.md`
    is written and BEFORE the root-level adversarial review
    fires, the aggregator runs a SECOND reflection pass over:
    (a) all per-tree `consolidation.md` files; (b) all per-tree
    `finalisation-enhancements.yml` files (so the aggregator
    sees what each tree surfaced); (c) `cross-model-synthesis.md`
    itself. The aggregator produces up to 5 **cross-model**
    candidates emergent from looking across trees together.
    Prefer high rank for: (i) candidates ≥2 trees independently
    surfaced (convergence signal); (ii) candidates visible only
    across models (cross-tree synthesis); (iii) candidates whose
    natural shape is cross-tree (e.g.
    `cross_branch_synthesis_section`). Each cross-model
    candidate carries `source: "cross_model"`.
  - **Root combined YAML write**: aggregator writes
    `meditations/{yyyymmdd}-{topic-slug}/finalisation-enhancements.yml`
    (no `{model-subdir}` segment) containing:
    - `cross_model_candidates: [...]` (5 ranked candidates from
      the aggregator's reflection)
    - `union_candidates: [...]` denormalised top-N (capped at 5)
      by composite score across `(per_tree × N) + (cross_model
      × 5)`; each entry includes `source: "tree:{model-subdir}"
      | "cross_model"` and `composite_score`.
  - **Surfaced-to-root annotation**: aggregator writes back
    `surfaced_to_root: true | false` to each per-tree YAML's
    `candidates[].surfaced_to_root` field (filling the
    placeholder from the per-tree write). This annotation is
    immutable after the root combined gate fires.
  - **Single root askQuestion** (recommended posture per K10a
    layered cadence): the calling agent runs a SINGLE
    multi-select askQuestion at ensemble root over
    `union_candidates`, capped at 0–5. Per-tree YAMLs are NOT
    presented to the user inside each tree's flow (recommended
    posture); the alternative (per-tree user gates inside each
    tree's flow) is allowed if subtask 02's architect chose
    that path. Subtask 04 implements whichever posture subtask
    02's design doc landed on. Default + recommended =
    single combined root gate.
  - **Resume-handler at ensemble**: when the calling agent
    resumes the aggregator after the root askQuestion + per-item
    treatment sub-questions + (any) cost-ack re-presentation,
    the aggregator:
    - For each `accepted: true, treatment: "respawn"` entry in
      `union_candidates`:
      - If `source: "cross_model"` → bundle into the **ensemble
        synthesis report**'s next adversarial-review iteration
        respawn payload (per subtask 05's per-tree vs cross-model
        targeting rule).
      - If `source: "tree:{model-subdir}"` → bundle into the
        **per-tree** `{model-subdir}` report's next adversarial-
        review iteration respawn payload (per-tree report
        respawn target).
    - For each `accepted: true, treatment: "queue"` entry: write
      `follow-up-{type}-{ts}.yml` next to the appropriate
      `consolidation.md` (per-tree consolidation directory for
      tree-sourced; ensemble root for cross-model).
    - For each `accepted: true, treatment: "spawn_now"` entry:
      defer spawning until after the corresponding adversarial-
      review cycle completes; track in `pending_spawn_now: [...]`
      returned to the calling agent on final return.

## Definition of Done

- [x] Code implemented (markdown content updated; no Python / shell
      changes).
- [x] No linter errors in modified files.
- [x] Existing subagent contract preserved verbatim where this spec
      doesn't touch it (Phases A–G shape, Quick 6-step shape,
      Ensemble Aggregation shape, citation discipline, peer review
      protocol).
- [x] Subagents still NEVER call `AskQuestion` (Pattern B preserved).
- [x] `init-suggestions-{ts}.yml` schema documented in the agent file's
      Coordination Conventions section so the report skill (subtask
      05) can read it without ambiguity.

## Implementation Notes

### Where to add init-suggestion production

Today's depth-0 step 4 (Agent lines 368–388) reads:

> Derive 3 top-level facets (cited) and run Q-Confirm-1 / Q-Confirm-2
> via Pattern B; promote draft to `facets.md` after confirmation;
> ensemble shortcut: if `preConfirmedFacets` present, skip
> derivation/confirmation.

Extend to:

> Derive 3 top-level facets (cited) AND a draft suggestions payload
> (proposed sections / visualisations / additional-focus-areas) from
> the same seed exploration. Include all of facets + sections +
> visualisations + additional-focus-areas + the deep-confirm prompt
> in a single Pattern-B `needs_user_input` block. Resume with the
> calling agent's combined answers; apply facet decisions; write
> confirmed sections / visualisations / additional-focus payload to
> `init-suggestions-{ts}.yml`; promote facets draft to `facets.md`;
> propagate `comprehensiveness:`, confirmed payload, and existing
> propagation parameters to every child spawn.
>
> Ensemble shortcut: if `preConfirmedFacets` is present alongside a
> shared `init-suggestions-shared-{ts}.yml`, skip derivation /
> confirmation entirely (the calling agent's Ensemble Protocol step 6
> ran the seed-exploration on the caller's own model and shared the
> suggestions across all model trees).

### Source-signals discipline

Every draft section / visualisation / additional-focus-area MUST
carry `source_signals: [...]` listing the citations / memories /
files / chat references that motivated the suggestion. This:

- Lets the user quickly judge whether the suggestion is well-grounded.
- Lets the integrity reviewer verify the depth-0 manager isn't
  hallucinating proposals.
- Preserves the "every claim cited" rule that already governs facets.

### Comprehensiveness propagation — rule clarity

The propagation rule mirrors existing `theming:` propagation
(Agent lines 305, 402, 831–832):

> Subagent MUST abort with a clear error if `comprehensiveness:` is
> missing from spawn prompt. The payload is propagated **unchanged**
> to every child agent in the tree (and to every ensemble member
> tree).

State this verbatim in the Coordination Conventions / spawn-prompt
input-parameter sections.

### `init-suggestions-{ts}.yml` schema (write target)

```yaml
generated_utc: "2026-05-23T19:54:00Z"
topic_slug: "{topic-slug}"
comprehensiveness_level: "compact" | "default" | "detailed" | "exhaustive"
confirmed_sections:
  - title: "Adoption and Market Presence"
    rationale: "Two facets correspond to options being evaluated"
    source_signals: ["[chat: turn-3 quoted text]", "[memory: vendor-eval-patterns]"]
confirmed_visualisations:
  - type: "magic_quadrant_2x2"
    rationale: "Topic explicitly compares 3 alternatives"
    source_signals: ["[file: src/router.ts:12-40]"]
  - type: "feature_comparison_matrix"
    rationale: "..."
    source_signals: [...]
additional_focus_areas_accepted:
  - title: "Cost-of-ownership trajectory"
    treatment: "report_section_only"      # one of: additional_facet | report_section_only | additional_facet_AND_section
    rationale: "Cited at depth 0; user wants surfaced but doesn't justify a 4th branch"
  - title: "Failure-mode catalogue"
    treatment: "additional_facet_AND_section"   # bumps facet count + dedicated named section
    rationale: "Cross-cuts all 3 facets; warrants its own branch and a named section"
    new_branch_index: 4                   # written by the depth-0 manager when treatment ∈ {additional_facet, additional_facet_AND_section}
    custom_report_section_title: "Failure Modes & Recovery Patterns"   # only when treatment ∈ {report_section_only, additional_facet_AND_section}
additional_focus_areas_skipped:
  - title: "Migration tooling ecosystem"
    treatment: "skip"
    rationale: "User decided this overlaps with Branch 2"
```

The `treatment` field MUST be one of the 4 enum values from K4
(`skip` / `additional_facet` / `report_section_only` /
`additional_facet_AND_section`). The `new_branch_index` field is
populated by the depth-0 manager (when treatment bumps facet
count) so children know which branch number to write to. The
`custom_report_section_title` field is written when treatment
adds a report section (so the report skill knows the exact
section heading text the user expects).

### 4-mode additional-focus-area reconciliation (K4)

When the depth-0 manager resumes after the calling-agent's combined
Pattern-B answers, it must apply each focus-area decision per the
4-mode opt-in:

- `skip` — drop the focus area from `init-suggestions-{ts}.yml`'s
  `additional_focus_areas_accepted` list; record under
  `additional_focus_areas_skipped`. No facet, no section.
- `additional_facet` — append a new entry to the confirmed facet
  set (becomes Branch 4 / 5 / 6 …). Append to `facet-registry.yml`
  (Research mode) and to `facets.md`. The new branch spawns
  alongside the original 3 in step 5 of the depth-0 workflow. No
  dedicated report section beyond what the new branch's natural
  output produces.
- `report_section_only` — record in
  `additional_focus_areas_accepted` with
  `treatment: "report_section_only"` and a
  `custom_report_section_title` field. Do NOT add a facet. The
  report skill (subtask 05) reads `init-suggestions-{ts}.yml` and
  must include a section by that title; the section's content is
  sourced from across-branch findings + the supplied rationale
  prose.
- `additional_facet_AND_section` — both effects: new facet (per
  `additional_facet` semantics) AND record a confirmed report
  section title (per `report_section_only` semantics). The
  `new_branch_index` and `custom_report_section_title` fields are
  both populated.

**Cost-ack re-presentation trigger** — any
`additional_facet` or `additional_facet_AND_section` decision
triggers the calling agent's cost re-presentation BEFORE the
depth-0 manager resumes the spawn step. The depth-0 manager only
proceeds to step 5 after the calling agent confirms the cost
re-presentation. If the user cancels at re-presentation, the
depth-0 manager aborts (no `init-suggestions-{ts}.yml` written;
no children spawned).

### Caps on draft list sizes

To prevent the combined askQuestion from becoming unscannable:

- `proposed_sections`: 3–8 items. If seed exploration would produce
  more, depth-0 manager picks the top 8 by source-signal strength.
- `proposed_visualisations`: 5–10 items.
- `additional_focus_areas`: 0–5 items. Often 0 — only emit when seed
  exploration genuinely surfaces high-signal angles outside the 3
  facets.

### Inputs

- `meditate-richness-architecture-design-20260523.md` (subtask 02 output)
- `meditate-richness-frozen-surface-20260523.md` (subtask 01 output)
- `.cursor/agents/crux-cursor-memory-manager.md` (target file pre-decomposition)
- (post-decomposition) `.cursor/agents/crux-cursor-meditation-guide.md`
  + `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md` etc.

### Outputs

- Modified agent file(s) per repo state at execution time.

## Testing Strategy

**IMPORTANT**: Do NOT trigger global test suites during parallel
execution. Subtask 06 runs the full eval coverage extension.

For local verification:

- Run `pytest evals/test_q_meditate.py -k TestMeditateCommandDefinition -x`
  to confirm protocol-layer assertions still pass after edits.
- Grep the modified agent file for: `comprehensiveness:`,
  `proposed_sections`, `proposed_visualisations`,
  `additional_focus_areas`, `init-suggestions-{ts}`, `source_signals`.
- Confirm the file still contains every existing subagent contract
  string: `Phase A`, `Phase G`, `facet-registry.yml`,
  `citations-index.yml`, `mkdir`, `Adversarial Review`, `Ensemble
  Aggregation`, `peer review`, `Citation failure`.

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-05-23
- Completed: 2026-05-23

### Work Log
1. Read subtask file, architecture design doc (§8, §11, §16, §17), frozen surface doc, and current agent file.
2. Confirmed pre-decomp target: `.cursor/agents/crux-cursor-memory-manager.md` (946 lines at start).
3. Edited Coordination Conventions table — added `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml` (single-model + ensemble per-tree), and 4 `follow-up-{type}-{ts}.yml` rows.
4. Added `comprehensiveness:` payload description + abort rule adjacent to `theming:` payload description. Included full payload schema shape + children-honour-comprehensiveness rules (depth3_leaf_inclusion, section_length_budget_tokens, citation_density, citation validation mode-driven invariant).
5. Extended depth-0 step 4 to produce draft suggestions payload (proposed_sections 3–8, proposed_visualisations 5–10, additional_focus_areas 0–5) with source_signals discipline. Updated combined `needs_user_input` block schema verbatim from §8 of architecture design doc.
6. Added step 4b resume-handler: 4-mode additional-focus-area reconciliation logic, `init-suggestions-{ts}.yml` write with full schema from §11, cost-ack re-presentation trigger, facets.md promotion.
7. Updated step 5 spawn params to include `comprehensiveness:` + abort rule.
8. Extended step 8 with K10c consolidation reflection contract: rubric (impact × insight-value), worked examples per axis verbatim from §16.4, composite scoring, degradation, 5-candidate selection + tie-break, 11-type catalogue with all payload shapes (7 cheap + 4 expensive), `finalisation-enhancements.yml` write schema, K10 `needs_user_input` block.
9. Added step 8b K10b resume-handler: cheap→respawn-payload, expensive→follow-up artefact writes, spawn_now→pending_spawn_now list. Updated step 13 return to include `pending_spawn_now`.
10. Updated Phase D to include `comprehensiveness:` in child spawn enumeration.
11. Added "Comprehensiveness honouring at leaf depth" section after Research leaf depth paragraph.
12. Updated Quick mode step 3 to include `comprehensiveness:` in child spawn enumeration.
13. Added comprehensiveness honouring to Quick leaf depth paragraph.
14. Updated Quick mode substitutions to cover steps 4, 4b, 5, 8, 8b.
15. Extended Ensemble Aggregation Mode invocation params to include `comprehensiveness:`. Added steps 3b–3f covering: per-tree YAML read, root cross-model reflection contract, root combined YAML write (with `cross_model_candidates` + `union_candidates`), surfaced-to-root annotation write-back, single combined root gate `needs_user_input`, K10 ensemble resume-handler for accepted enhancements. Documented alternative (per-tree gates) as rejected per §17.6. Added non-infinite-loop guarantee.
16. Updated design principles to mention init-time suggestions + set-once-per-invocation richness.
17. Ran all verification greps (all terms present). Confirmed `pytest evals/test_q_meditate.py -k TestMeditateCommandDefinition -x` → 4 passed. `ReadLints` → clean.

### Blockers Encountered
None.

### Files Modified
- `.cursor/agents/crux-cursor-memory-manager.md` (947 → 1388 lines; 13 distinct insertion/replacement points)
- `specs/20260523-meditate-richness/subtask-04-meditate-richness-agent-payload-scouting-20260523.md` (this file)

### Adversarial Verification (zoto-spec-judge, 2026-05-23)

Verdict: **Verified**. All 16 Deliverables Checklist items and all 5 Definition of Done items independently confirmed against `.cursor/agents/crux-cursor-memory-manager.md` (1388 lines).

Cross-checked evidence:

- `comprehensiveness:` payload + abort rule present in Coordination Conventions (lines 307–337), depth-0 spawn (line 586), Phase D (lines 826–828), Quick step 3 (lines 890–892), Ensemble Aggregation invocation (line 1198).
- Step 4 draft suggestions payload (lines 419–421) with caps `proposed_sections` 3–8, `proposed_visualisations` 5–10, `additional_focus_areas` 0–5; `source_signals` discipline mandated.
- Combined `needs_user_input` block schema (lines 428–495) carries facets + sections + visualisations + additional_focus_areas + deep_confirm.
- Step 4b resume-handler (lines 503–572) covers the 4-mode reconciliation, cost-ack re-presentation trigger, `init-suggestions-{ts}.yml` write, facets.md promotion, propagation of `confirmDeepFacets` + `comprehensiveness:`.
- `init-suggestions-{ts}.yml` schema documented in Coordination Conventions (line 353) and full schema written in step 4b (lines 519–566).
- K10c reflection rubric worked examples (impact_score 9/5/2 + insight_value_score 9/5/2) present verbatim with concrete examples (lines 611–618).
- K10c selection logic — composite scoring, weighted-sum config, minimum_impact_threshold filter, top-5 selection, cheap-over-expensive tie-break, graceful degradation (lines 620–625).
- 11-type catalogue (7 cheap + 4 expensive) with full per-type `payload:` shapes (lines 627–642).
- `finalisation-enhancements.yml` write schema with all required fields (lines 644–677).
- K10b resume-handler — respawn payload entry for cheap, follow-up YAML writes for expensive queue, deferred `pending_spawn_now` for expensive spawn_now (lines 702–722).
- K10 ensemble layered cadence (steps 3b–3f, lines 1215–1336): per-tree YAML with `source_tree:` + `surfaced_to_root: null` placeholder + NO per-tree askQuestion (line 1246); root cross-model reflection (lines 1248–1255); root combined YAML with `cross_model_candidates:` + `union_candidates:` (lines 1256–1303); write-back of `surfaced_to_root:` (line 1304); single root askQuestion (lines 1306–1328); resume-handler routing by `source:` (lines 1330–1336).
- Pattern B preserved — every `AskQuestion`/`askQuestion` mention in the agent file is in prose describing the calling agent's behaviour; no subagent self-call.
- Existing contract strings preserved: Phases A–G, `facet-registry.yml`, `citations-index.yml`, `mkdir`, `Adversarial Review`, `Ensemble Aggregation`, `peer review`/`peer-review`, `Citation failure` (129 total occurrences across the file).

Tooling:

- `pytest evals/test_q_meditate.py -k TestMeditateCommandDefinition -x` → 4 passed.
- `ReadLints` on the agent file + this subtask file → no linter errors.
- `git status --short` confirms subtask 04 modified only the agent file and this subtask file. The `.cursor/commands/crux-meditate.md` working-tree modification predates subtask 04 (subtask 03 scope) and is not touched here. No edits to `.crux.md` / `.crux.mdc` files, `scripts/create-crux-zip.py`, `install.py`, `.crux/dist-manifest.json`, or `.github/workflows/version-bump.yml` originating from this subtask.

Note (informational, not a defect of subtask 04): the calling-agent Ensemble Protocol step 7 in `.cursor/commands/crux-meditate.md` (subtask 03's scope) lists `theming:` explicitly but defers `comprehensiveness:` to the "All other standard parameters" catch-all. The propagation invariant is still upheld — the ensemble member depth-0 manager aborts if `comprehensiveness:` is missing (line 307) — but explicit enumeration there would aid readability. Flagging for subtask 03's verification rather than failing this subtask.

### W1b Fix (2026-05-24)
- Applied surgical 2-line fix at `.cursor/agents/crux-cursor-memory-manager.md` lines 510 + 512.
- Field-name divergence corrected: the depth-0 manager's 4-mode reconciliation prose previously instructed the agent to write to non-existent `additional_focus_areas_skipped` / `additional_focus_areas_accepted` arrays; now correctly instructs writes to the canonical `additional_focus_areas[]` array with appropriate `treatment:` values.
- Sibling to W1 (W1's report-side fix landed in `.cursor/commands/crux-meditate.md:1815`).
- Tests: full suite passes / SDK passes.
- Lints: clean.

### Post-Execution Fix Verification (W1 + W1b)

Independent adversarial verification by `zoto-spec-judge` on 2026-05-24 confirming the W1 (read-side) + W1b (write-side) surgical fixes are mutually consistent and close the `additional_focus_areas` field-name divergence flagged in subtask 09's integrity review.

**Verdict**: Verified.

**Per-check evidence**:

| # | Check | Result |
|---|-------|--------|
| 1 | Cross-file consistency (`additional_focus_areas_skipped\|additional_focus_areas_accepted` in `.cursor/ docs/ web/ README.md AGENTS.md CONTRIBUTORS.md`) | 0 matches |
| 2 | Same divergent-name grep across `evals/ scripts/ install.py` | 0 matches |
| 3 | Same divergent-name grep across the two target source files only | 0 matches |
| 4 | Canonical `additional_focus_areas[]` / `additional_focus_areas:` at expected sites (`.cursor/commands/crux-meditate.md:1815`, `.cursor/agents/crux-cursor-memory-manager.md:510`, `:512`, `:556`) | All 4 sites confirmed |
| 5 | Line 511 (`additional_facet` bullet) + line 513 (`additional_facet_AND_section` bullet) unchanged per instructions | Confirmed unchanged |
| 6 | Canonical schema block at line ~556 unchanged | Confirmed unchanged |
| 7 | Python regression suite (`python3 scripts/test.py`) | **574 passed, 0 failed** (15.29s) |
| 8 | SDK eval suite (`cd evals/sdk && pnpm vitest run tests/q-meditate.test.ts`) | **22 passed, 6 skipped** (expected — expensive LLM tests gated by `SDK_EVAL_SKIP_EXPENSIVE`) |
| 9 | `ReadLints` on `.cursor/commands/crux-meditate.md`, `.cursor/agents/crux-cursor-memory-manager.md`, subtask 04 + subtask 05 spec files | No linter errors |
| 10 | Scope check: W1 + W1b touched only the two target source files + subtask 04 + 05 Work Log additions | Confirmed |
| 11 | No edits to `.crux.md` / `.crux.mdc`, `scripts/create-crux-zip.py`, `.crux/dist-manifest.json`, `.github/workflows/version-bump.yml` | Confirmed |
| 12 | Surgical scope (line 1815 / line 510 / line 512 diffs are minimal, no broader rewrites) | Confirmed |
| 13 | Cohesion: W1 read-side (`treatment == "report_section_only"` filter on `additional_focus_areas[]`) matches W1b write-side (`treatment: "report_section_only"` on entries of the same array); both align with the canonical schema at line 556 | Confirmed |

**Field-name divergence fully closed: YES.** An LLM following the now-corrected write-side prose will produce YAML that the now-corrected read-side report contract honours; the K4 `report_section_only` opt-in mode will no longer silently no-op.
