# Subtask: Eval / Test Coverage Extension

## Metadata
- **Subtask ID**: 06
- **Feature**: Meditate Comprehensiveness + Init-Time Suggestions
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 03, 04, 05
- **Created**: 20260523

## Objective

Extend the existing meditate eval surface with new assertions covering
all of K1–K9 from the spec index (after the 2026-05-23 user-decision
update). Add regression coverage for K7 (existing safeguards
preserved). Add a pinned-numeric regression test for the `compact`
level (so future drift in the mapping table is caught). Add coverage
for the merged `Q-Cost-and-Richness-Acknowledgment` gate, the 4-mode
additional-focus-area opt-in, the set-once-per-invocation richness
rule, and the adversarial respawn protocol (including a finite-
iteration check). Do **not** delete any existing assertion; this
subtask is strictly additive (mirrors K6 of the sibling 20260517
spec).

## Deliverables Checklist

- [x] **`evals/test_q_meditate.py` extended** with new test classes:
  - `TestMeditateMergedCostAndRichnessGate` — assert
    `Q-Cost-and-Richness-Acknowledgment` askQuestion exists in the
    modified command file (or thinned coordinator); assert all 4
    richness enum values (`compact` / `default` / `detailed` /
    `exhaustive`) present in Sub-Q1; assert default richness
    preselection = `default`; assert Sub-Q2 preserves today's
    proceed/swap/cancel option set; assert decision-guidance prose
    per richness option; assert prompt prose displays cost
    estimates per depth × richness × mode combination; assert
    NO standalone `Q-Comprehensiveness` gate exists anywhere in
    the file (negative assertion); assert **mode-swap preserves the
    user's Sub-Q1 richness selection** (per spec OQ #1 default) —
    i.e. the modified file documents that `switch_to_quick` /
    `switch_to_research` / `switch_to_ensemble` / `switch_to_single`
    do NOT reset richness; assert the **K1 dual-meaning callout**
    is present in the `default`-option decision-guidance prose
    (i.e. prose explicitly notes that the level *named* `default`
    is also the preselected option).
  - `TestMeditateReadOnlyRichnessVariant` — assert the read-only-
    richness variant of the merged gate exists for both expansion
    + cost-re-presentation paths; assert richness is shown locked
    in this variant; assert prose preamble names the trigger.
  - `TestMeditateComprehensivenessLevelMapping` — assert the
    level mapping table exists in the report-generation section;
    assert every level row has every dimension specified; assert
    `compact` row reproduces today's numeric minima exactly (≥4
    charts, ≥3 infographics, ≥1 calculator, 3+ scenarios per
    calculator).
  - `TestMeditateInitSuggestions` — assert the init-suggestion
    payload schema (sections / visualisations / additional-focus-
    areas) is documented in the agent file (or guide-agent /
    research skill); assert `init-suggestions-{ts}.yml` artefact
    appears in Coordination Conventions filename table; assert
    `init-suggestions-{ts}.yml` link appears in Branch & Leaf
    Index "Top-level artifacts" enumeration; assert all 4 opt-in
    modes (`skip` / `additional_facet` / `report_section_only` /
    `additional_facet_AND_section`) appear in the schema.
  - `TestMeditateCombinedFacetConfirmation` — assert the combined
    Pattern-B askQuestion folds Q-Confirm-1 + Q-Confirm-2 + init-
    suggestions sub-questions into one prompt; assert decision-
    guidance prose per sub-question; assert the 4-mode focus-area
    sub-question lists all 4 modes with per-mode rationale.
  - `TestMeditateAdditionalFacetCostAck` — assert the cost-ack
    re-presentation rule is documented; assert it triggers on
    BOTH `additional_facet` AND `additional_facet_AND_section`
    (NOT on `skip` or `report_section_only`); assert the re-
    presentation uses the read-only-richness variant.
  - `TestMeditateSetOncePersistence` — assert the set-once-per-
    invocation richness rule is documented; assert the expansion
    variant of the merged gate shows richness as locked; assert
    no `--reset-richness` flag exists.
  - `TestMeditateAdversarialReviewerExtension` — assert the
    reviewer's dimension list now contains 13 dimensions (or 11 +
    2 additions); assert dimensions 12 and 13 are present by name
    (comprehensiveness fidelity, init-suggestion honour); assert
    dimension 9 has the level-conditional expansion text.
  - `TestMeditateRespawnProtocol` — assert the respawn protocol
    is documented in the Adversarial Review and Report Generation
    sections; assert the respawn payload schema lists all required
    keys (`respawn_reasons` (list-typed), `reviewer_iteration`,
    `prior_report_paths`, `missing_sections`,
    `missing_visualisations`, `accepted_finalisation_enhancements`,
    `preserve_other_content`,
    `comprehensiveness_payload`, `init_suggestions_payload`,
    `theming_payload`); assert respawn shares the existing ≤3
    iteration cap (NOT a separate budget); assert respawn-then-
    re-review semantics; assert `respawn_required: true` flag
    bypasses standard in-place reviewer fix flow.
  - `TestMeditateRespawnFiniteIteration` — pinned regression:
    assert that respawn protocol cannot infinite-loop. This is a
    structural test that verifies (a) iteration cap = 3, (b)
    respawn counts as 1 iteration, (c) `ESCALATE` verdict is
    triggered after 3 iterations if Dim 13 still fires. Must
    fail if any of these constraints is loosened in the future.
  - `TestMeditatePayloadPropagation` — assert
    `comprehensiveness:` is listed in depth-0 spawn-prompt
    parameters; assert it is propagated to children in Phase D /
    Quick step 3 / Ensemble step 7 spawn enumerations; assert
    "subagent must abort if `comprehensiveness:` missing"
    statement is present.
  - `TestMeditateNoNewFilesInDist` — assert K8 (no new files added
    to dist / install / version-bump enumerations). Read
    `scripts/create-crux-zip.py`, `install.py` `MEMORY_FILE_PREFIXES`,
    and `.github/workflows/version-bump.yml` `RELEASE_PATHS`; assert
    that no new file path introduced by this spec appears in these
    enumerations (the diff vs the spec-start commit should show
    these files unchanged by this spec's subtasks 03–05). This is a
    structural test; integrity-review subtask 09 also verifies this
    but the eval makes drift detectable in CI.
- [x] **`evals/sdk/tests/q-meditate.test.ts` extended** with
      equivalent assertions on the LLM/prompt-evaluation side
      (parallel to the Python tests).
- [x] **`TestMeditateBackwardsCompatibility`** regression class
      (Python only — pinned to numeric values from subtask 01
      freeze):
  - `test_compact_chart_minimum_unchanged` — `compact.minima.charts.count == 4`
  - `test_compact_infographic_minimum_unchanged` — `compact.minima.infographics.count == 3`
  - `test_compact_calculator_minimum_unchanged` — `compact.minima.calculators.count == 1`
  - `test_compact_calculator_scenarios_unchanged` — at least 3 scenarios
  - `test_compact_depth3_leaf_inclusion_unchanged` — `summary` (today's behaviour)
  - `test_compact_per_branch_section_unchanged` — `consolidation_only`
  - `test_compact_peer_review_surfacing_unchanged` — `consolidation_only`
  - `test_no_standalone_q_comprehensiveness_gate` — negative
    assertion: `Q-Comprehensiveness` does not appear anywhere in
    the coordinator command file (other than possibly historical
    spec references; the test scope is only the `.cursor/`
    surfaces).
- [x] **`TestMeditateSafeguardRegressions`** — assert every
      existing safeguard string still present in the modified
      surfaces (parallel to the protocol-layer existing test class):
  - `Anti-Homogenization` block-list still present
  - `Universal Contrast` rules still present
  - `Subject-Matter Focus` rule still present
  - `Pattern B` integrity still asserted
  - `paired HTML + PDF` rule still present
  - `mandatory citations` rule still present
  - `iteration cap` (≤3) still present
  - `MUST_FIX` `needs_user_input` schema with `context` field still present
  - `retrospective always written` rule still present
- [x] **`TestMeditateNoNewDistFilesK8`** (Python only — K8
      regression):
  - Assert `scripts/create-crux-zip.py`'s `DIST_FILES` list does
    NOT contain any path that this spec introduced (none should
    be introduced — K8 says no new files).
  - Assert `install.py`'s `MEMORY_FILE_PREFIXES` (or equivalent
    enumeration) is unchanged in shape — no new entries pointing
    at files this spec created.
  - Assert `.github/workflows/version-bump.yml` `RELEASE_PATHS`
    enumeration is unchanged in shape — no new entries.
  - Assert `.crux/dist-manifest.json` (if present) has no new
    manifest entries introduced by this spec.
  - Test mechanism: snapshot the four enumerations at spec start
    (subtask 01 records them in the freeze line); the test
    re-snapshots at execution time and asserts set-equality. If
    this spec accidentally adds a file to any of the four
    enumerations, the test fails loudly. The test does NOT
    enforce that the enumerations are unchanged across all
    repository changes (other specs may legitimately change
    them) — only that THIS spec's surfaces don't leak.
- [x] **No existing assertion deleted** from either eval file.
- [x] **Test file imports / fixtures** updated minimally if needed to
      read both pre-decomposition and post-decomposition surfaces
      (e.g. `_resolve_target_file()` helper that picks the file based
      on which path exists at test time).
- [x] **K10 — `TestMeditateFinalisationEnhancementGate`** (Python
      + TS parallel): assert `Q-Finalisation-Enhancements`
      askQuestion is documented in the modified coordinator file
      (or thinned coordinator); assert it is a multi-select with
      0–5 cap; assert it fires AFTER consolidation completes /
      Branch & Leaf Index refresh AND BEFORE the adversarial-review
      cycle; assert per-option labels include `{title}`,
      `[{cost_class}]`, rationale, composite score; assert the
      decision-guidance prose explains cost-class consequences
      per option.
- [x] **K10 — `TestMeditateK10SkipAllBackwardsCompat`** (Python
      pinned regression): when 0 candidates are accepted (skip-all
      path), the workflow proceeds to adversarial review with NO
      respawn-payload contribution from K10. Pinned assertions
      (every one MUST hold; failure of any is a regression):
  - The step-graph between consolidation and adversarial review
    has EXACTLY the same shape as today's pre-K10 flow, except
    for the gate's presence + `finalisation-enhancements.yml`
    write.
  - `respawn_reasons:` list does NOT contain
    `accepted_finalisation_enhancements` (the K10b cause does
    not fire on skip-all).
  - `accepted_finalisation_enhancements:` field is absent OR
    `[]` (empty list) in any respawn payload built during the
    skip-all flow.
  - No `follow-up-{type}-{ts}.yml` files are written next to
    `consolidation.md` (the K10b queue path doesn't fire when
    nothing was accepted).
  - The rendered report HTML/PDF section list is unchanged
    structurally vs the pre-K10 baseline (no extra sections
    added from K10b cheap-respawn types; no extra infographics
    added from `decision_tree_infographic` or `risks_section`).
  - The Footer `theme:` annotation does NOT contain the
    `finalisation-enhancements:` segment (the segment is
    omitted when count == 0, per subtask 05 footer rule). The
    pre-K10 footer string is preserved byte-for-byte.
  - No additional adversarial-review iteration is consumed by
    K10 (skip-all path still bound by the existing ≤3 cap
    without the K10b extension contributing to iteration
    consumption).
  - The single new artefact `finalisation-enhancements.yml` is
    written and every candidate has `accepted: false,
    treatment: "unchosen_persisted"`; no other K10 artefacts
    appear.
  This is the byte-for-byte backwards-compat test the user
  explicitly called out; the assertions enumerate every byte-
  level surface that K10 could potentially perturb so future
  drift is caught loudly.
- [x] **K10 — `TestMeditateFinalisationCheapAcceptRespawn`**: assert
      the respawn payload's `accepted_finalisation_enhancements:`
      list is populated when at least one cheap enhancement is
      accepted; assert `respawn_reasons:` includes
      `accepted_finalisation_enhancements`; assert this respawn
      shares the existing ≤3 iteration cap (no new budget); assert
      multiple accepted cheap items bundle into a single respawn.
- [x] **K10 — `TestMeditateFinalisationExpensiveQueueDefault`**:
      assert that for `cost_class: "expensive"` candidates, the
      default treatment is `queue`; assert that selecting `queue`
      writes the appropriate `follow-up-{type}-{ts}.yml` next to
      `consolidation.md`; assert NO agent is spawned in-invocation
      for `queue`-treated items; assert the queued item surfaces
      in the continuation-menu (step 12).
- [x] **K10 — `TestMeditateFinalisationExpensiveSpawnNow`**: assert
      that selecting `spawn_now` for any expensive item triggers
      cost-ack re-presentation (read-only-richness shape); assert
      cancel at re-presentation falls back the spawn-now items to
      `queue` (no work lost); assert proceed at re-presentation
      defers spawning until AFTER the adversarial-review cycle
      completes.
- [x] **K10 — `TestMeditateFinalisationPersistence`**: assert
      `finalisation-enhancements.yml` schema matches the K10c
      verbatim spec (every required field typed); assert every
      candidate carries `accepted` + `treatment` +
      `decided_at_utc` filled by calling agent; assert the file
      is linked from the Branch & Leaf Index "Top-level artifacts";
      assert unchosen items carry
      `treatment: "unchosen_persisted"` and surface in the
      continuation menu.
- [x] **K10 — `TestMeditateFinalisationContinuationMenu`**:
      assert step 12's prompt is grouped under section headings
      ("Expansion directions" / "Apply un-chosen enhancements" /
      "Spawn queued follow-ups"); assert per-unchosen-enhancement
      options include the title; assert per-queued-expensive
      options trigger cost-ack re-presentation when selected.
- [x] **K10 — `TestMeditateFinalisationFiniteIteration`** (pinned
      regression): assert the new `accepted_finalisation_enhancements`
      respawn cause CANNOT increase the maximum useful respawn
      count beyond what K9 established. Structural assertions:
      - Gate fires AT MOST once per meditation (post-consolidation
        / pre-adversarial-review).
      - Accepting cheap items contributes payload to the FIRST
        adversarial-review iteration's respawn (not a separate
        iteration).
      - Iteration cap remains ≤3.
      - `ESCALATE` path remains the verdict at iteration 3 if
        Dim 13 still fires (or the K10b extension of Dim 13 if
        subtask 02 keeps the dimension count at 13).
- [x] **K10 — `TestMeditateFinalisationTripleReasonRespawn`**:
      assert that when `respawn_reasons:` carries all three
      values (`missing_init_suggestion_sections` +
      `missing_init_suggestion_visualisations` +
      `accepted_finalisation_enhancements`), the report skill
      processes them in the K10b-defined order:
      `accepted_finalisation_enhancements` first (additive new
      sections / charts), then `missing_init_suggestion_visualisations`,
      then `missing_init_suggestion_sections`.
- [x] **K10 — `TestMeditateK10EnsembleLayeredCadence`**
      (replaces the prior `TestMeditateK10EnsembleOnceAtRoot`
      per OQ #10 resolution 2026-05-23 "both layered"). Assert:
  - **Per-tree YAMLs are written** — every per-model tree's
    consolidation step ends with a reflection pass that writes
    `meditations/{slug}/{model-subdir}/finalisation-enhancements.yml`
    (documented in the modified agent file / ensemble skill).
    Assert the per-tree YAML schema includes `source_tree:
    "{model-subdir}"` on every candidate AND a
    `surfaced_to_root: null` placeholder field.
  - **Root combined YAML is written** — after
    `cross-model-synthesis.md` is written, the aggregator runs
    a second reflection pass and writes
    `meditations/{slug}/finalisation-enhancements.yml` (no
    `{model-subdir}` segment) containing
    `cross_model_candidates: [...]` AND `union_candidates:
    [...]` (denormalised top-N capped at 5, each carrying
    `source: "tree:{model-subdir}" | "cross_model"`).
  - **Per-tree YAMLs persist with surfaced-to-root annotation**
    — assert the documented contract that the aggregator
    writes `surfaced_to_root: true | false` back to each
    per-tree YAML's `candidates[].surfaced_to_root` field after
    the root combined gate fires.
  - **Single root askQuestion (recommended posture)** — assert
    the agent file / coordinator command documents a SINGLE
    multi-select askQuestion at ensemble root over
    `union_candidates`, capped at 0–5. Per-tree askQuestions
    are NOT documented inside per-tree flows (per recommended
    posture; if subtask 02's design doc chose the alternative,
    relax the assertion accordingly).
  - **Root ranking by composite score across union** — assert
    the union ranking documentation states that
    `union_candidates` is sorted by `composite_score`
    descending across `(per-tree × N) + (cross-model × 5)`.
  - **Backwards-compat with single-model flows** — assert that
    non-ensemble (single-model) Research and Quick flows still
    fire the gate ONCE after that single tree's consolidation
    completes (no layered cadence in single-model flows). This
    preserves K10a's original single-model semantics.
  - **Per-tree vs cross-model report respawn targeting** —
    assert the report-contract documentation states that
    `source: "tree:{model-subdir}"` accepts target the per-tree
    report respawn AND `source: "cross_model"` accepts target
    the cross-model synthesis report respawn (per subtask 05).
- [x] **K10 — `TestMeditateK10EnsembleContinuationMenuLayered`**
      (new): assert the continuation menu surfaces per-tree-only
      unchosen items (`surfaced_to_root: false` in per-tree YAMLs)
      with label `(from tree: {model-label}, not surfaced at
      root)` AND root unchosen items with their provenance
      label (`(cross-model)` or `(from tree: {model-label})`).
      Selecting a per-tree-only item targets the per-tree report
      respawn for that tree (per subtask 05's layered targeting
      rule).
- [x] **K10 — `TestMeditateK10QuickModeFires`**: assert Quick
      mode fires the gate too (per K10 OQ #13 default), with the
      same 0–5 cap and skip-all backwards-compat behaviour.
- [x] **K10 — `TestMeditateK10ReflectionRubric`** (Python + TS):
      assert the impact × insight-value rubric is documented in
      the agent file (or post-decomp coordination skill); assert
      both axes use the 1–10 scale; assert the worked-example
      anchor scores for `impact_score = 9 / 5 / 2` and
      `insight_value_score = 9 / 5 / 2` are present in the
      consolidation-step prose; assert
      `minimum_impact_threshold` defaults to 6.
- [x] **K10 — `TestMeditateK10WeightsConfigurable`** (Python only,
      pinned regression for OQ #11 default): assert the
      `cruxMemories.meditate.finalisationEnhancements.weights`
      key is documented in `.crux/crux-memories.json` schema or
      the agent file's reflection-contract section; assert
      default weights = `{ impact: 1.0, insight_value: 1.0 }`;
      assert the formula falls back to multiplicative product
      when weights are 1.0.

## Definition of Done

- [x] All new test classes pass against the modified surfaces from
      subtasks 03 / 04 / 05.
- [x] Existing tests in both eval files still pass (no regression).
- [x] No linter errors in the modified eval files.
- [x] The full meditate eval suite (`pytest evals/test_q_meditate.py`
      and `cd evals/sdk && pnpm vitest run tests/q-meditate.test.ts`)
      passes locally.

## Implementation Notes

### Test target resolution

Because of K3 (dual-target landing), tests must work whether the
post-decomposition spec has shipped or not. Add a helper at the top
of `evals/test_q_meditate.py`:

```python
def _resolve_target_file(*candidates: str) -> Path:
    """Return the first candidate file that exists; fail if none do."""
    repo_root = Path(__file__).resolve().parent.parent
    for c in candidates:
        p = repo_root / c
        if p.exists():
            return p
    raise FileNotFoundError(
        f"None of the candidate target files exist: {candidates}"
    )
```

Then each test uses:

```python
def _read_report_contract(self) -> str:
    f = _resolve_target_file(
        ".cursor/skills/crux-skill-memory-meditation-report/SKILL.md",
        ".cursor/commands/crux-meditate.md",  # pre-decomp fallback
    )
    return f.read_text(encoding="utf-8")
```

This keeps tests stable across the repo's evolution.

### Pinned-value regression class

`TestMeditateBackwardsCompatibility` deliberately uses **literal
numeric values** (4, 3, 1, 3) rather than re-deriving from the freeze
line. This is the regression contract: if the mapping table is later
changed in a way that lowers `compact`, the test fails loudly.

### Finite-iteration test approach

`TestMeditateRespawnFiniteIteration` is a documentation-shape test
(not a runtime test against the LLM). It reads the modified command
file (or thinned coordinator + post-decomp skill) and verifies:

- A literal mention of "≤3 iterations" or "iteration cap" or
  equivalent canonical phrasing.
- The respawn protocol's iteration accounting paragraph explicitly
  states that respawn counts as 1 iteration (not a separate
  budget).
- The `ESCALATE` verdict is documented as the outcome when the
  cap is exhausted with Dim 13 still firing.

If any of these documentation invariants is removed or weakened in
the future, the test fails — which is exactly the regression catch
the spec needs.

### Skill-presence tests (post-decomposition only)

Do NOT add `test_meditation_skill_dir_exists` or similar — that's
the responsibility of the sibling 20260517 spec's subtask 08. Only
add tests for content **inside** files (which both target file sets
share). The fallback in `_resolve_target_file` handles the
target-file selection; assertions don't depend on which target was
chosen.

### Inputs

- Modified `.cursor/commands/crux-meditate.md` (subtask 03, 05 outputs)
- Modified agent file or post-decomp guide / skills (subtask 04 output)
- `evals/test_q_meditate.py` (existing tests preserved)
- `evals/sdk/tests/q-meditate.test.ts` (existing tests preserved)
- `meditate-richness-architecture-design-20260523.md` — eval-strategy
  section enumerates per-class assertions; this subtask implements.

### Outputs

- Modified `evals/test_q_meditate.py`
- Modified `evals/sdk/tests/q-meditate.test.ts`

## Testing Strategy

**IMPORTANT**: Do NOT trigger global test suites during parallel
execution.

This subtask is the test-coverage subtask itself. Run targeted suites:

```bash
pytest evals/test_q_meditate.py -x -v
cd evals/sdk && pnpm vitest run tests/q-meditate.test.ts
```

Do not run the full `evals/` suite or the full SDK test suite —
those are for the integrity-review subtask (09) or for the spec's
final Definition-of-Done check.

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer (subagent)
- Started: 2026-05-23
- Completed: 2026-05-23

### Work Log

1. Read subtask file, spec, architecture design §18, freeze line.
2. Read existing `evals/test_q_meditate.py` (30 tests, 8 classes) and `evals/sdk/tests/q-meditate.test.ts` (3 describe blocks, 6 LLM tests skipped by default).
3. Inspected modified command file (2142 lines) and agent file (1388 lines) for content anchors.
4. Added `_resolve_target_file()`, `_read_command_file()`, `_read_agent_file()` helpers to Python file.
5. Implemented 30 new Python test classes (147 new tests total) covering K1–K10c.
6. Fixed 4 assertion brittleness issues (surrounding window too narrow, wrong first occurrence of search term).
7. Added 4 TS `describe` blocks (22 static tests) outside the expensive gate.
8. Fixed REPO_ROOT path computation in TS (was `"../../../../.."`, needed `"../../../.."`).
9. All 177 Python tests pass; all 22 TS tests pass (6 LLM tests skipped as expected).
10. ReadLints: no linter errors on either file.

### Blockers Encountered
None. Field-name divergence: used canonical subtask 02 name `additional_focus_areas` with `treatment:` field per instructions. The report-contract (subtask 05) uses `additional_focus_areas_accepted[]` in one subsection — noted divergence, used canonical form, flagged for subtask 09 reconciliation.

### Files Modified
- `evals/test_q_meditate.py` — added helpers + 30 new test classes (147 new test methods)
- `evals/sdk/tests/q-meditate.test.ts` — added 4 new describe blocks (22 static test cases)

### Judge Verification (zoto-spec-judge, 2026-05-23)

**Verdict: Verified.**

Adversarial verification confirmed every Deliverables Checklist + DoD
item against the actual file system, the test files, and a full run
of both eval suites. Findings:

- **Test classes** — All 28 named classes from the checklist are
  present in `evals/test_q_meditate.py` (verified via
  `grep -E '^class TestMeditate'`). The `TestMeditateNoNewFilesInDist`
  checklist item is satisfied via an explicit class alias
  (`TestMeditateNoNewFilesInDist = TestMeditateNoNewDistFilesK8`,
  line 780).
- **TypeScript parallel coverage** — 5 new `describe` blocks added
  for K2 / K9 / K10 finalisation gate / K10 reflection rubric /
  K10 ensemble layered cadence. The 3 original Q1–Q3 SDK describe
  blocks preserved unchanged.
- **`_resolve_target_file()` helper** — Present at top of
  `evals/test_q_meditate.py` (lines 23–37) with proper
  pre-/post-decomposition fallback semantics.
- **No existing assertion deleted** — Confirmed via
  `git diff HEAD -- evals/test_q_meditate.py | grep "^-"` (no
  deletion lines outside diff headers); same check on
  `evals/sdk/tests/q-meditate.test.ts`. The original 8 Python
  classes (30 tests) and 3 SDK describe blocks (6 LLM-gated `it`
  tests) are all still present.
- **Pinned literals** — `TestMeditateBackwardsCompatibility`
  uses `` `compact`=4 ``, `` `compact`=3 ``, `` `compact`=1 ``,
  `` `compact`=3 `` (charts / infographics / calculators /
  scenarios_per) at lines 791, 798, 804, 810.
  `TestMeditateK10SkipAllBackwardsCompat::test_footer_omits_finalisation_enhancements_segment_on_skip`
  asserts the `finalisation-enhancements:` footer segment is
  omitted on skip-all (lines 947–951).
  `TestMeditateRespawnFiniteIteration` asserts the ≤3 cap +
  respawn-counts-as-1-iteration + ESCALATE-at-iter-3 invariants
  (lines 640–666). `TestMeditateFinalisationFiniteIteration`
  asserts the new K10b cause does not extend the iteration bound
  (lines 1107–1133).
- **Suite run** — `pytest evals/test_q_meditate.py -v` →
  **177 passed in 0.47s** (all green).
  `cd evals/sdk && pnpm vitest run tests/q-meditate.test.ts` →
  **22 passed | 6 skipped (28)**; the 6 skipped are the
  expensive LLM tests gated behind `SDK_EVAL_SKIP_EXPENSIVE`
  (intentional).
- **Lints** — `ReadLints` on `evals/test_q_meditate.py`,
  `evals/sdk/tests/q-meditate.test.ts`, and this subtask file
  → no linter errors.
- **Scope check** — `git diff HEAD --stat evals/` shows only the
  two eval files modified by this subtask
  (`+1095 / +219` insertions, 0 deletions). No edits made to
  `.cursor/**`, `scripts/**`, `install.py`, `.crux/**`,
  `.github/**`, `README.md`, `AGENTS.md`, `docs/**`, `web/**`,
  `CONTRIBUTORS.md`, or any `.crux.md` / `.crux.mdc` file *by
  this subtask*. (Other unrelated repo changes visible in
  `git status` were introduced by prior subtasks 03 / 04 / 05 or
  by the sibling 20260517 spec — out of scope for subtask 06.)
- **Field-name divergence (heads-up for subtask 09)** — The
  executor's choice to assert against the canonical subtask 02
  schema name `additional_focus_areas` (Python test line 456) is
  verified correct. The divergent
  `additional_focus_areas_accepted[]` wording introduced by
  subtask 05 also appears in the modified surfaces
  (`.cursor/commands/crux-meditate.md:1815` +
  `.cursor/agents/crux-cursor-memory-manager.md:512`); both
  forms coexist in the modified files. The executor flagged
  this for subtask 09 reconciliation, which is the appropriate
  next step — the test choice itself is sound and does not
  block this subtask.

**No checklist items unticked.** The executor's claims match the
file system, the suite passes, and lints are clean. Verdict:
**Verified.**
