# Subtask: Contract Capture / Freeze Line for Touched Meditate Surface

## Metadata
- **Subtask ID**: 01
- **Feature**: Meditate Comprehensiveness + Init-Time Suggestions
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: None
- **Created**: 20260523

## Objective

Capture an authoritative freeze line for **only the parts of the meditate
surface that this spec will modify**, so subsequent subtasks (architecture,
implementation, evals, docs, integrity review) can diff post-change
artefacts against a single contract.

This mirrors the pattern from `specs/20260517-meditate-agent-skill-decomposition/`
subtask 01 — it does not duplicate it. Where the 20260517 freeze line
already covers a contract item, this subtask cites the existing freeze
line by section anchor instead of restating. New material is only added
for surfaces not yet frozen.

## Deliverables Checklist

- [x] `meditate-richness-frozen-surface-20260523.md` written into the
      spec directory, recording each contract item this spec touches with
      back-traceable line ranges and section anchors in the **current**
      sources at git HEAD on 2026-05-23.
- [x] Cross-references to the 20260517 freeze line for any item already
      covered there (cite section number + page anchor; do not restate).
- [x] Explicit dual-target inventory: for each contract item, list
      where it lives **today** (pre-decomposition) AND where it would
      live **post-decomposition** (per the 20260517 patch matrix in its
      subtask 02 architecture design).
- [x] Inventory of every existing safeguard the spec must preserve verbatim
      (Anti-Homogenisation Rules, Universal Contrast, Subject-Matter Focus,
      citation discipline, Pattern A vs Pattern B boundaries, retrospective
      always-written rule, mandatory paired HTML+PDF, adversarial cycle).
- [x] Source-of-truth map (two-column concordance) following the same
      shape as the 20260517 freeze line Section 10.

## Definition of Done

- [x] Markdown-only artefact (no code edits).
- [x] Every contract item back-traceable to a current source line range
      or section anchor in the repo at the spec start commit.
- [x] Document referenced from spec index Execution Notes (Cross-references).
- [x] No linter errors introduced.

## Implementation Notes

### Scope — items to freeze

Only freeze what this spec will touch. Specifically:

1. **Calling-agent gate ordering** — the four pre-spawn gates today
   (Depth Selection → Cost Acknowledgment → Theme Preflight → Facet
   Confirmation Pattern-B). Capture exact ordering and the mid-flow
   timing of Facet Confirmation. The new spec **merges** richness
   selection into Cost Acknowledgment (renaming it
   `Q-Cost-and-Richness-Acknowledgment` — there is **no** standalone
   `Q-Comprehensiveness` gate) AND folds init-suggestion confirmation
   into the existing Facet Confirmation prompt, so the freeze must
   record the current `Q-Cost-Acknowledgment` prompt prose, options
   list, ensemble-mode prose variant, expansion variant, and
   non-interactive abort rule **verbatim** so subtask 03 can patch
   surgically.
2. **Existing facet-confirmation `needs_user_input` schema** —
   `facets-pending-{ts}.yml` shape, the `Q-Confirm-1` option set, the
   `Q-Confirm-2` option set. The new spec extends this with sections /
   visualisations / additional-focus-areas; the freeze must record the
   pre-extension shape.
3. **Report-generation contract minima** — current ≥4 charts, ≥3
   infographics, ≥1 calculator. Capture the exact lines / phrases that
   document these so subtask 05 (report contract) can replace them with
   the level-driven mapping.
4. **Per-branch / depth-3 / peer-review surfacing in the report** —
   today the report is rendered primarily off `consolidation.md` plus
   selective re-reading of branch files. Capture the current lines that
   say "all 39 branch files" / "input coverage verification" / etc., so
   the new spec's per-level "depth-3 leaf inclusion" and "peer-review
   surfacing" rules can layer on top.
5. **Anti-Homogenisation Rules** (lines 197–209 + 1174–1194 of the
   command file at HEAD, already covered in 20260517 freeze §6.2 — cite,
   don't restate).
6. **Universal Contrast block** (already covered in 20260517 freeze §6.3
   — cite, don't restate).
7. **Subject-Matter Focus rule** (already covered in 20260517 freeze §8
   — cite).
8. **Adversarial review 11-dimension list** (already covered in 20260517
   freeze §4.6 — cite). The new spec adds **two** new dimensions
   (comprehensiveness fidelity, init-suggestion honour); the freeze
   records the existing 11 verbatim.
9. **Citation discipline** (already covered in 20260517 freeze §5.5 — cite).
10. **Retrospective always-written rule** (already covered in 20260517
    freeze §5.7 — cite).
11. **Branch & Leaf Index template** (already covered in 20260517 freeze §5.8
    — cite). The new spec adds a new top-level artefact link
    (`init-suggestions-{ts}.yml`); the freeze records the existing
    "Top-level artifacts" section verbatim so the diff is auditable.
12. **Pattern A vs Pattern B boundaries** (already covered in 20260517
    freeze §3 — cite). The new spec must preserve every boundary;
    subagents still NEVER call `AskQuestion`.
13. **Cost-ack expansion variant** (`Q-Cost-Acknowledgment-Expansion`,
    20260517 freeze §2.3 — cite). The new spec replaces this with the
    read-only-richness variant of the merged
    `Q-Cost-and-Richness-Acknowledgment` gate (richness shown locked
    per K6 — set-once-per-invocation). The expansion variant does NOT
    offer a "keep richness setting?" follow-up; richness is implicitly
    locked. The existing "keep deep-confirm setting?" follow-up is
    preserved unchanged.
14. **Existing eval coverage** in `evals/test_q_meditate.py` and
    `evals/sdk/tests/q-meditate.test.ts` — list each existing test
    class and what it asserts so subtask 06 can extend without
    deleting.

### Dual-target listing rule

For each contract item, record a row of the form:

| Contract item | Pre-decomposition target (today) | Post-decomposition target (per 20260517) | Touch reason for this spec |
|---|---|---|---|

This becomes the input to subtask 02's patch matrix.

### Inputs

- `.cursor/commands/crux-meditate.md` (current file at spec start commit)
- `.cursor/agents/crux-cursor-memory-manager.md` (current file)
- `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260517.md`
  (sibling freeze line — cited, not duplicated)
- `specs/20260517-meditate-agent-skill-decomposition/subtask-02-meditate-decomp-architecture-design-20260517.md`
  (post-decomposition target paths)
- `evals/test_q_meditate.py`, `evals/sdk/tests/q-meditate.test.ts`
  (current test surface)

### Outputs

- `specs/20260523-meditate-richness/meditate-richness-frozen-surface-20260523.md`

## Testing Strategy

**IMPORTANT**: Do NOT trigger global test suites during parallel execution.

This is a documentation-only subtask. No tests to run. Verify the
freeze document by:

1. For every line range cited, opening the source file at that range
   and confirming the cited content is present.
2. For every cross-reference to 20260517, opening the section in
   `meditate-frozen-contract-20260517.md` and confirming the citation
   is correct.
3. Spot-check that the freeze covers every K1–K9 surface listed in
   `spec-meditate-richness-20260523.md`.

## Execution Notes

### Agent Session Info
- Agent: crux-platform-architect
- Started: 2026-05-23 (this turn)
- Completed: 2026-05-23 (this turn)

### Work Log

1. **Context loading** — read this subtask brief, the spec index
   `spec-meditate-richness-20260523.md` (sections through K10 +
   Definition of Done + Open Questions for context on what surfaces
   need to be frozen), and the sibling-spec freeze line
   `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260517.md`
   plus its subtask 02 architecture-design document
   `meditate-decomp-architecture-design-20260517.md` to identify
   the post-decomposition target paths.
2. **Verbatim source extraction** — read live sources for the
   items the 20260517 freeze does not cover with sufficient
   granularity:
   - `.cursor/commands/crux-meditate.md` — `Q-Cost-Acknowledgment`
     prompt + ensemble variant + options + behaviour rules + non-
     interactive abort rule (`:123-189`); `Q-Cost-Acknowledgment-
     Expansion` prompt + options (`:174-188`); `Q-Confirm-1`
     prompt body + options (`:311-330`); `Q-Confirm-2` prompt body
     + options (`:338-359`); report minima `≥4 charts / ≥3
     infographics / ≥1 calculator` (`:1068-1070, :1119-1121,
     :1137-1146, :1066, :1474`); per-branch / depth-3 / peer-review
     surfacing today (`:1000-1018`); Branch & Leaf Index `## Top-
     level artifacts` block (`:705-718`).
   - `.cursor/agents/crux-cursor-memory-manager.md` — consolidation
     step inputs (`:411-420` Research, `:457` Quick); working-dir
     framing (`:311`); 11-dim restatement reference (`:424-428,
     :833`); depth-0 step 12 report obligation (`:432-442`).
   - `evals/test_q_meditate.py` (entire file, 240 lines, 8 test
     classes, 25 tests).
   - `evals/sdk/tests/q-meditate.test.ts` (entire file, 357 lines,
     3 describe blocks Q1–Q3, 6 `it` tests).
3. **Cross-reference scaffolding** — built the table mapping
   subtask 01 scope items 5–13 to 20260517 freeze section anchors
   so the freeze cites rather than restates: §6.2 / §6.3 / §8 /
   §4.6 / §5.5 / §5.7 / §5.8 / §3 / §2.3.
4. **Dual-target inventory** — for each of the 14 in-scope
   contract items, recorded a row mapping
   `contract item | pre-decomposition target (file:lines today) |
   post-decomposition target (per 20260517 §3) | touch reason for
   this spec`. Used for the subtask 02 patch matrix.
5. **Decomposition notes** — surfaced six observations for
   subtask 02 (architecture-design): facets-pending YAML schema
   greenfield; combined askQuestion template greenfield; K10
   layered ensemble cadence integration point; dual literal-check
   tests (`test_spawns_memory_manager` + SDK
   `"spawns subagents for recursive exploration"`) require K3
   branching; greenfield test coverage; backwards-compat anchor
   ~45 agents at depth 3 Research.
6. **Output** — wrote
   `specs/20260523-meditate-richness/meditate-richness-frozen-surface-20260523.md`
   (~825 lines, 13 sections, markdown-only, no linter errors).
7. **Verification** — spot-checked the cited line ranges in the
   live sources (Q-Cost-Acknowledgment prompt at `:127-142`,
   Q-Confirm-1 at `:311-330`, Q-Confirm-2 at `:338-359`, report
   minima at `:1068-1070, :1119-1121, :1137-1146`, ensemble
   "in addition to standard minimums" heading at `:1474`,
   consolidation step inputs at agent `:411-420, :457`); all
   citations resolve correctly.

### Blockers Encountered

None. Every contract item in the 14-item scope was either captured
verbatim from the live sources or cited via an existing 20260517
freeze section anchor.

### Files Modified

- **Created**: `specs/20260523-meditate-richness/meditate-richness-frozen-surface-20260523.md`
- **Modified**: this file (Execution Notes + Deliverables/DoD ticks)
- **Modified**: `specs/20260523-meditate-richness/spec-meditate-richness-20260523.md` (Execution Notes / Cross-references — added pointer to the new freeze file)

### Adversarial Verification (zoto-spec-judge — 2026-05-23)

Verdict: **Verified**. Spot-checks confirmed:
- ~12 live-source citations in the freeze (Q-Cost-Acknowledgment
  prompt `:127-142`, ensemble variant `:144-154`, options
  `:158-166`, behaviour rules `:169-189`, Expansion prompt
  `:178-184` + options `:187-188`, Q-Confirm-1 `:311-330`,
  Q-Confirm-2 `:338-359`, write/delete semantics `:309`/`:361`,
  filename row `:446`, charts `:1068-1070`, infographics
  `:1119-1121`, calculator `:1137`, standard-minimums sentence
  `:1066`, ensemble visualisations heading `:1474`,
  Anti-Homogenisation `:1174-1194`, Universal Contrast
  `:1205-1231`, Subject-Matter Focus `:878-898`) all resolve to
  the cited content at HEAD on 2026-05-23.
- ~8 agent-file citations (User-Input Escalation `:17-46`,
  Meditate-mode reaffirmation `:302-307`, working-dir framing
  `:311`, Research consolidation step 8 `:411-420`, Quick step 8
  `:457`, depth-0 step 10 `:424-428`, step 12b `:444`, Citations
  protocol `:655-690`, design-principle `:833`/`:837`) all
  resolve correctly.
- 10 cross-references into the 20260517 freeze (§2.3, §3, §4.6,
  §5.5, §5.7, §5.8, §6.2, §6.3, §8, §10) — each exists at the
  cited section and covers the claimed material.
- Dual-target inventory rows present for all 14 contract items
  (§2 source-of-truth map at 21 rows + §11 dual-target table at
  14 rows; both pre- and post-decomp columns populated).
- Safeguard inventory (§10) names all eight required safeguards
  (Anti-Homogenisation, Universal Contrast, Subject-Matter
  Focus, citation discipline, Pattern A/B, retrospective,
  mandatory paired HTML+PDF, adversarial cycle) plus 8 bonus
  rows; every row carries a live-source citation + 20260517
  freeze anchor.
- Source-of-truth map (§2) follows the two-column concordance
  shape used in 20260517 §10.
- DoD #1 (Markdown-only): only files under
  `specs/20260523-meditate-richness/` were added; no edits to
  `.cursor/**`, `evals/**`, `scripts/**`, `install.py`,
  `.crux/**`, `.github/**`, `web/**`, `docs/**` were made by this
  subtask. (The non-spec changes in the git status snapshot
  predate this subtask.)
- DoD #3: spec index Execution Notes / Cross-references at
  `spec-meditate-richness-20260523.md:1423-1433` points to the
  new freeze file.
- DoD #4: `ReadLints` clean on freeze file + this subtask file
  + spec index.

K8 (no new files added to dist / install / version-bump) is a
negative constraint with no contract surface to freeze; its
absence from the freeze is acceptable. The freeze's "Is NOT
covered" section enumerates explicit out-of-scope items
including cross-repo touchpoints (§9 in 20260517).

All five Deliverables Checklist items and all four Definition of
Done items remain ticked (their original state) — verification
confirms each is genuinely satisfied.
