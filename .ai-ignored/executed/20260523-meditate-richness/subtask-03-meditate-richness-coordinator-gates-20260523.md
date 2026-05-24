# Subtask: Coordinator Command — Gates + Combined Pattern-B Prompt

## Metadata
- **Subtask ID**: 03
- **Feature**: Meditate Comprehensiveness + Init-Time Suggestions
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 02
- **Created**: 20260523

## Objective

Implement the calling-agent surface changes in the coordinator command
file: **merge richness selection into the existing `Q-Cost-Acknowledgment`
gate** (renamed `Q-Cost-and-Richness-Acknowledgment`) — there is **no
standalone `Q-Comprehensiveness` gate**; replace `Q-Confirm-1` +
`Q-Confirm-2` with the combined Pattern-B askQuestion designed in
subtask 02 (with 4-mode additional-focus-area opt-in); add
`comprehensiveness:` payload propagation to the depth-0 spawn prompt;
extend `Q-Cost-Acknowledgment-Expansion` to use the read-only-richness
variant of the merged gate; implement the cost-ack re-presentation rule
(read-only-richness shape) when additional facets are accepted via
`additional_facet` or `additional_facet_AND_section`.

## Deliverables Checklist

- [x] Resolve target file at execution time per subtask 02 patch matrix:
  - **Pre-decomposition**: edit `.cursor/commands/crux-meditate.md`.
  - **Post-decomposition**: edit `.cursor/commands/crux-meditate.md`
    (thinned coordinator section) — confirm via repo state check
    whether `crux-cursor-meditation-guide.md` exists.
- [x] **`Q-Cost-Acknowledgment` renamed `Q-Cost-and-Richness-Acknowledgment`
      and extended** with a richness sub-question inserted as Sub-Q1
      (the existing proceed/swap/cancel options become Sub-Q2):
  - 4 single-select richness options: `compact` / `default` /
    `detailed` / `exhaustive`
  - Sub-Q1 preselected = the level literally named `default`
    (canonical phrasing — match this phrasing verbatim in every
    file this subtask touches so docs-sync and eval assertions
    have a single string to grep)
  - Decision-guidance prose per richness option (mandatory) —
    must concretely describe chart counts, depth-3 inclusion
    behaviour, length budgets per level
  - Sub-Q2 = today's `proceed` / `switch_to_quick` /
    `switch_to_research` / `switch_to_ensemble` /
    `switch_to_single` / `cancel`. Mode-swap PRESERVES the user's
    Sub-Q1 richness selection.
  - Prompt prose displays depth × richness × mode combinations
    with the resulting agent-count + runtime estimates from the
    cost-formula multiplier table (subtask 02 output).
  - Behaviour rules: always run on first invocation; non-interactive
    sessions abort with the existing cost-ack error message
    (preserved); expansion-mode uses the read-only-richness variant
    (set-once persistence).
- [x] **Read-only-richness variant** of
      `Q-Cost-and-Richness-Acknowledgment` implemented for:
  - `Q-Cost-Acknowledgment-Expansion` (calling-agent step 12).
  - Cost re-presentation when `additional_facet` or
    `additional_facet_AND_section` is accepted from init suggestions.
  - In this variant, Sub-Q1 (richness) is shown as a locked
    display row with the current level + clear "(locked)" notation;
    only Sub-Q2 is interactive. Prose preamble names the trigger
    (expansion vs additional-facet acceptance) so the user
    understands the re-presentation reason.
- [x] **Combined Pattern-B askQuestion** replaces today's
      `Q-Confirm-1` (lines 295–337) and `Q-Confirm-2` (lines 338–361):
  - Single `askQuestion` call with multiple sub-questions per the
    design in subtask 02.
  - **4-mode additional-focus-area opt-in**: per-item single-select
    over `skip` / `additional_facet` / `report_section_only` /
    `additional_facet_AND_section`. Per-mode decision-guidance
    prose explaining cost implication.
  - Resume-handler contract: parses combined answers and applies
    facet decisions, sections list, visualisations list,
    per-additional-focus-area mode decisions, and
    `confirmDeepFacets` enum in one resume.
  - Decision-guidance prose per sub-question.
- [x] **Cost-ack re-presentation logic** when one or more
      additional focus areas are accepted as `additional_facet` OR
      `additional_facet_AND_section`:
  - Recompute agent count using new facet count + richness
    multipliers from the cost-formula table.
  - Run the **read-only-richness variant** of
    `Q-Cost-and-Richness-Acknowledgment` with the updated count.
  - On cancel: abort meditation; delete `facets-pending-{ts}.yml`
    (the not-yet-promoted draft); ensure no `init-suggestions-{ts}.yml`
    is written.
  - On proceed: continue to depth-0 subagent spawn.
- [x] **`comprehensiveness:` payload added to depth-0 spawn prompt**
      adjacent to existing `theming:` payload (so propagation
      semantics are obvious from layout). Include the "subagent must
      abort if `comprehensiveness:` missing" rule mirroring the
      existing theming abort rule.
- [x] **`Q-Cost-Acknowledgment-Expansion` updated** to use the
      read-only-richness variant of the merged gate. The expansion
      variant does **NOT** offer a "keep richness setting?"
      follow-up — richness is locked per K6 (set-once-per-invocation).
      The existing "keep deep-confirm setting?" follow-up is
      preserved.
- [x] **Coordination Conventions table extended** to include
      `init-suggestions-{ts}.yml` artefact (filename pattern, notes
      column).
- [x] **Branch & Leaf Index "Top-level artifacts" entry** added for
      `init-suggestions-{ts}.yml`.
- [x] **K10a — `Q-Finalisation-Enhancements` askQuestion** inserted
      as a new gate AFTER consolidation completes (after `facets.md`
      Branch & Leaf Index refresh) and BEFORE the adversarial-review
      cycle begins. Gate shape:
  - Multi-select with **0–5** options, sourced from
    `finalisation-enhancements.yml` (which the depth-0 manager
    writes BEFORE returning control to the calling agent for this
    gate — see subtask 04).
  - Each option label includes: `{title}` + `[{cost_class}]` +
    one-line rationale + `impact_score × insight_value_score`
    composite score.
  - Decision-guidance prose per option mandatory (per the existing
    `MUST_FIX needs_user_input` schema rule). Per-option prose
    must explain the cost class consequences (cheap = report
    respawn within ≤3 cap; expensive default = queue, opt-in
    spawn-now triggers cost-ack re-presentation).
  - **Skip-all** path (0 selected) → resume depth-0 manager with
    empty accept set; flow proceeds to adversarial review
    unchanged. **Backwards-compatibility anchor**: skip-all
    reproduces today's behaviour byte-for-byte.
  - **Graceful degradation**: if `finalisation-enhancements.yml`
    contains fewer than 5 candidates (consolidation flagged
    fewer high-quality ones), present whatever count surfaced;
    if zero candidates surfaced, surface a one-line
    "no high-quality enhancement candidates surfaced" message
    and proceed directly to adversarial review without firing
    askQuestion (no user time wasted on an empty gate).
  - Mode coverage: gate fires in **both Research and Quick mode**
    (per K10 OQ #13 default). **In Ensemble mode (layered
    cadence per OQ #10 resolution 2026-05-23 "both layered")**:
    the user-facing askQuestion fires **once** at ensemble root
    after the aggregator writes the root combined
    `finalisation-enhancements.yml`. Per-tree consolidation
    agents perform their own reflection internally and write
    per-tree `{model-subdir}/finalisation-enhancements.yml`
    BEFORE the aggregator runs (NO per-tree askQuestion fires —
    per-tree YAMLs are write-only at the per-tree level). The
    root askQuestion ranks across the union of `(per-tree × N)
    + (cross-model × 5)` candidates, capped at the standard 0–5
    multi-select. See subtask 04 for per-tree + root reflection
    obligations and subtask 05 for per-tree vs cross-model
    report respawn targeting.
- [x] **K10b — Per-item treatment sub-questions for expensive
      items**: for each accepted enhancement with
      `cost_class: "expensive"`, run a follow-up single-select
      `Q-Finalisation-Enhancement-Treatment-{id}`:
  - Options: `queue` (default, preselected) — write
    `follow-up-{type}-{ts}.yml` next to `consolidation.md`,
    surface in continuation menu;
  - `spawn_now` — opt-in, triggers cost-ack re-presentation
    BEFORE the adversarial-review cycle starts.
  - Decision-guidance prose explaining the cost difference
    (queue = zero in-invocation cost; spawn_now =
    multiplicative agent count for the chosen type).
- [x] **K10b — Cost-ack re-presentation for `spawn_now`**: if any
      `spawn_now` selected, run the **read-only-richness variant**
      of `Q-Cost-and-Richness-Acknowledgment` with prose enumerating
      the spawn-now items + their estimated agent counts + total
      cost. Use the prompt template defined in subtask 02. On
      cancel: drop the `spawn_now` treatments, fall back to `queue`
      treatment for those items (no work lost), proceed.
- [x] **K10c — `finalisation-enhancements.yml` update flow**: after
      askQuestion + per-item treatment sub-questions + cost-ack
      re-presentation (if any), the calling agent updates the
      file in place: for each candidate set `accepted: true | false`
      and `treatment: "respawn" | "queue" | "spawn_now" | "unchosen_persisted"`
      and `decided_at_utc: <ISO 8601>`. The calling agent then
      resumes the depth-0 manager with the updated file path so
      the manager can:
      - Build the next adversarial-review iteration's respawn
        payload from the cheap-accepted entries (per K9 + K10b);
      - Write `follow-up-{type}-{ts}.yml` for each `queue`
        entry;
      - Spawn expensive agents for each `spawn_now` entry
        (after the adversarial-review cycle completes — so the
        respawned report incorporates accepted cheap
        enhancements before any expensive follow-up runs).
- [x] **K10c — Coordination Conventions filename table extended**
      with `finalisation-enhancements.yml` and the four
      `follow-up-{type}-{ts}.yml` artefact patterns.
- [x] **K10c — Branch & Leaf Index "Top-level artifacts" entry**
      extended with `finalisation-enhancements.yml` and any
      `follow-up-{type}-{ts}.yml` files (only if present;
      conditional listing matches existing `confirmed-facets-*.yml`
      pattern).
- [x] **K10c — Continuation menu (calling-agent step 12)
      extended** with two new option families:
  - **Re-apply unchosen enhancement: {title}** — one option per
    `unchosen_persisted` item in `finalisation-enhancements.yml`.
    Selecting one re-runs the post-consolidation phase with that
    single item pre-checked (other candidates greyed-out); fresh
    ≤3 iteration cap because this is a new continuation
    invocation.
  - **Spawn now: {type}** — one option per queued expensive
    item. Selecting one triggers the cost-ack re-presentation
    AND spawns the agent.
  - **Grouping**: per K10 OQ #14 default, the continuation menu
    groups options under section headings ("Expansion
    directions" / "Apply un-chosen enhancements" / "Spawn queued
    follow-ups"). Subtask 03 implements the grouped prompt
    template.

## Definition of Done

- [x] Code implemented (markdown content updated; no Python / shell
      changes).
- [x] No linter errors in modified files.
- [x] Existing safeguards preserved verbatim (Anti-Homogenisation
      Rules, Universal Contrast, Subject-Matter Focus, Pattern A vs
      Pattern B boundaries, retrospective always-written rule,
      mandatory paired HTML+PDF, adversarial cycle ≤3 iterations).
- [x] Pattern A vs Pattern B integrity preserved: subagents still NEVER
      call `AskQuestion`; the combined askQuestion is owned by the
      calling agent.
- [x] **Set-once-per-invocation richness rule honoured** (K6):
      `Q-Cost-Acknowledgment-Expansion` uses the read-only-richness
      variant of the merged gate; no `--reset-richness` flag exists
      anywhere in the modified file; the expansion variant does NOT
      offer a "keep richness setting?" follow-up.
- [x] **Cost re-presentation rule honoured** (K2 + K4): triggers on
      BOTH `additional_facet` AND `additional_facet_AND_section`
      acceptance; does NOT trigger on `skip` or `report_section_only`.
- [x] **No standalone `Q-Comprehensiveness` gate** present anywhere
      in the modified file (negative assertion).
- [x] **Mode-swap preserves richness selection** — `switch_to_*`
      decisions documented as preserving the user's Sub-Q1 selection
      (per spec OQ #1 default).
- [x] Targeted tests added in subtask 06 cover all the new prompts and
      behaviour rules.

## Implementation Notes

### Order of insertion / replacement

Edit in this order to minimise re-flow:

1. Update Coordination Conventions filename table FIRST (adds
   `init-suggestions-{ts}.yml` row); also extend the Branch & Leaf
   Index "Top-level artifacts" enumeration.
2. **Rename and extend** the existing `Q-Cost-Acknowledgment`
   section heading + body in place — it becomes
   `Q-Cost-and-Richness-Acknowledgment`. Add Sub-Q1 (richness
   level enum, default `default`); preserve Sub-Q2 (existing
   proceed/swap/cancel option set) verbatim except for one
   addition: mode-swap behaviour clarifies that richness selection
   is preserved across swap. Update the prompt prose to display
   depth × richness × mode combinations with cost estimates.
   **Do NOT insert any new gate between Q-Depth-Selection and
   Q-Cost-Acknowledgment.**
3. Add the **read-only-richness variant** as a sub-section of the
   renamed gate (used by both expansion and re-presentation paths).
4. Replace Q-Confirm-1 / Q-Confirm-2 sections with the combined
   Pattern-B askQuestion (single section heading with
   sub-question structure inside; 4-mode focus-area opt-in).
5. Update Q-Cost-Acknowledgment-Expansion subsection to describe
   the expansion variant of the merged gate (read-only-richness;
   no "keep richness setting?" follow-up; preserve "keep
   deep-confirm setting?" follow-up).
6. Add `comprehensiveness:` payload to the depth-0 spawn-prompt
   description (adjacent to `theming:`). Also add a "subagent must
   abort if `comprehensiveness:` is missing from spawn prompt" rule
   matching the existing theming abort rule.
7. Add cost-ack re-presentation logic to the
   facet-confirmation resume-handler section. Trigger conditions
   = any `additional_facet` OR `additional_facet_AND_section`
   acceptance.

### Specific line-range markers (current source at 2026-05-23)

These are anchor lines, not exact insertion points (executing agent
must search-and-confirm at execution time):

- Q-Depth-Selection: lines 55–105 (`### Depth Selection — MANDATORY`)
- Q-Cost-Acknowledgment: lines 106–189 (`### Cost & Scope Acknowledgment`)
- Theme Preflight: lines 191–293 (`### Theme Preflight — MANDATORY`)
- Facet Confirmation: lines 295–439
- Coordination Conventions filename table: lines 444–456
- Branch & Leaf Index template "Top-level artifacts": lines 824–838
  (in the `### Branch & Leaf Index` section starting around line 671)

### Decision-guidance text — minimum prose per option

Every sub-question in the merged gate AND in the combined Pattern-B
askQuestion MUST include decision-guidance text per the existing
`MUST_FIX needs_user_input` schema rule (lines 803–816). The user
must understand:

- For richness (Sub-Q1 of the merged gate): what each of `compact`
  / `default` / `detailed` / `exhaustive` means in concrete terms
  (chart counts, depth-3 inclusion, length budgets), so the user
  isn't picking blindly. The `default` level's prose must explicitly
  call out that it's both the level name AND the preselected option
  (per K1 reconciliation note).
- For proceed/swap/cancel (Sub-Q2 of the merged gate): same
  decision-guidance the existing `Q-Cost-Acknowledgment` provides,
  preserved.
- For sections: why each draft section was proposed (`source_signals`)
  so the user can quickly scan for misfits.
- For visualisations: why each draft visualisation type was proposed
  and what data it would chart.
- For additional focus areas: the cost difference between the **4
  modes** —
  - `skip` — discarded; zero cost; zero report effect.
  - `additional_facet` — bumps facet count → multiplies agent count
    (cost-ack re-presentation triggers); does NOT add a dedicated
    report section beyond the new branch's natural output.
  - `report_section_only` — adds a confirmed report section title
    to `init-suggestions-{ts}.yml`; does NOT bump facet count;
    zero agent cost.
  - `additional_facet_AND_section` — both: new branch (multiplies
    agent count, triggers cost-ack re-presentation) AND dedicated
    named report section using the user-supplied title.

### Backwards-compatibility check

Before declaring the subtask complete, verify by reading:

- The merged gate's richness Sub-Q1 default = `default` (so the
  user gets the new richer-than-today behaviour by accepting the
  preselection).
- `compact` decision-guidance text explicitly notes "reproduces
  pre-richness behaviour for users who want the legacy minima".
- Non-interactive sessions still abort on the merged gate (the
  cost-ack abort rule is preserved verbatim — only the prompt
  prose has changed, not the abort condition).

### Inputs

- `meditate-richness-architecture-design-20260523.md` (subtask 02 output)
- `meditate-richness-frozen-surface-20260523.md` (subtask 01 output)
- `.cursor/commands/crux-meditate.md` (target file)

### Outputs

- Modified `.cursor/commands/crux-meditate.md` (or thinned
  coordinator + new artefact, per repo state at execution time).

## Testing Strategy

**IMPORTANT**: Do NOT trigger global test suites during parallel
execution. Subtask 06 (evals/tests) is sequenced after this subtask
and runs the full eval coverage extension.

For local verification during this subtask:

- Run `pytest evals/test_q_meditate.py -k 'TestMeditateConfigPresence or TestMeditateCommandDefinition' -x`
  to verify the existing protocol-layer assertions still pass after
  edits. Do not run the full `evals/` suite.
- Manually grep the modified file for: `Q-Cost-and-Richness-Acknowledgment`,
  `comprehensiveness:`, `init-suggestions-{ts}`,
  `additional_focus_area`, `compact`, `default`, `detailed`,
  `exhaustive`, `additional_facet_AND_section`,
  `read-only-richness` — confirm every term appears where expected.
- Confirm `Q-Comprehensiveness` does **NOT** appear anywhere in the
  modified file (no standalone gate; the spec K2 explicitly
  forbids it).
- Confirm the file still contains every existing safeguard string:
  `Anti-Homogenization`, `Universal Contrast`, `Subject-Matter
  Focus`, `MUST_FIX`, `Pattern B`, `paired HTML + PDF`.

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer (Sonnet 4.6)
- Started: 2026-05-23T22:00:00+10:00
- Completed: 2026-05-23T22:30:00+10:00

### Work Log
- Read subtask file, architecture design doc (§6 merged gate, §9 combined Pattern-B, §16 K10 gate), frozen surface doc (§3, §4, §5, §6, §8)
- Edit 1: Coordination Conventions table — added `init-suggestions-{ts}.yml` row + updated `facets-pending` note + added `finalisation-enhancements.yml` row + 4 `follow-up-{type}-{ts}.yml` rows (K10c)
- Edit 2: Branch & Leaf Index Top-level artifacts — added `[Init suggestions]` + `[Finalisation enhancements]` + follow-up artefact conditional listing
- Edit 3: Renamed `Q-Cost-Acknowledgment` → `Q-Cost-and-Richness-Acknowledgment`; rewrote entire section with Sub-Q1 (richness, 4 options, preselected=`default`), Sub-Q2 (proceed/swap/cancel with richness-preservation note), cost table, and read-only-richness variant
- Edit 4: Added `Q-Cost-Acknowledgment-Expansion` as a named subsection using the read-only-richness variant; preserved "keep deep-confirm setting?" follow-up; no "keep richness setting?" follow-up
- Edit 5: Replaced `Q-Confirm-1` + `Q-Confirm-2` with combined Pattern-B `needs_user_input` schema + combined 5-sub-question `askQuestion` (facets, sections, visualisations, additional_focus_areas with 4-mode per-item, deep_confirm)
- Edit 6: Added cost-ack re-presentation logic block (triggers on `additional_facet` / `additional_facet_AND_section` ONLY; cancel deletes `facets-pending-{ts}.yml`)
- Edit 7: Added `comprehensiveness:` payload block adjacent to `theming:` payload in Theme Preflight section; abort rule mirroring theming abort
- Edit 8: Updated step 4 (Research + Quick) to reference combined Pattern-B flow + init-suggestions derivation
- Edit 9: Updated step 5 (Research + Quick) to include `comprehensiveness:` in child spawn payload + abort-if-missing rule
- Edit 10: Inserted `Q-Finalisation-Enhancements` gate section between Branch & Leaf Index and Adversarial Review — multi-select 0–5, per-item treatment sub-Qs, spawn_now cost-ack re-presentation, ensemble layered cadence, `finalisation-enhancements.yml` update flow
- Edit 11: Extended continuation menu (step 11) with K10c option groups ("Apply un-chosen enhancements" / "Spawn queued follow-ups" / "Other")
- Edit 12: Updated step 12 with K10c branches (reapply_enhancement, spawn_queued)
- All 26 grep checks pass; 8 pytest tests pass; no linter errors

### Blockers Encountered
None

### Files Modified
- `.cursor/commands/crux-meditate.md` — all deliverables implemented
- `specs/20260523-meditate-richness/subtask-03-meditate-richness-coordinator-gates-20260523.md` — this file (execution notes + checklist ticks)

### Adversarial Verification (judge — independent)

- **Judge**: `zoto-spec-judge` (fresh context, read-only)
- **Verified at**: 2026-05-23T22:59:00+10:00
- **Target file size**: `.cursor/commands/crux-meditate.md` = 1909 lines (matches executor's reported growth from ~1493 → ~1910)
- **Verdict**: **Verified** — every Deliverables Checklist item and every Definition of Done item is independently confirmed in the modified file.

**Per-item confirmation summary**:

| Item | Status | Evidence |
|------|--------|----------|
| Target file resolved (pre-decomposition) | ✓ | edits land in `.cursor/commands/crux-meditate.md`; `crux-cursor-meditation-guide.md` does not exist |
| `Q-Cost-and-Richness-Acknowledgment` renamed + extended (Sub-Q1 + Sub-Q2) | ✓ | lines 106–209; 4 richness options enumerated lines 183–186; preselected = `default` (canonical phrasing "preselected = the level literally named `default`" line 177); decision-guidance prose per option present; Sub-Q2 preserves proceed/swap/cancel with explicit "Richness selection preserved across swap" notes |
| Read-only-richness variant | ✓ | lines 239–256 define the general variant; lines 210–238 define the expansion-specific variant; trigger preambles table lines 250–254 covers expansion / additional-facet / spawn_now |
| Combined Pattern-B askQuestion replaces Q-Confirm-1 + Q-Confirm-2 | ✓ | lines 403–646; single askQuestion with 5 sub-questions; all 4 modes (`skip` / `additional_facet` / `report_section_only` / `additional_facet_AND_section`) present lines 586–601; resume-handler contract documented lines 633–646 |
| `comprehensiveness:` payload adjacent to `theming:` with abort rule | ✓ | theming block ends line 357; `comprehensiveness:` section starts line 361; abort rule mirrored verbatim line 363 |
| `Q-Cost-Acknowledgment-Expansion` uses read-only-richness; no "keep richness setting?" follow-up; "keep deep-confirm setting?" preserved | ✓ | line 234 explicitly states both rules; line 738 preserves deep-confirm follow-up |
| Cost-ack re-presentation triggers on `additional_facet` OR `additional_facet_AND_section` only | ✓ | lines 640–646 + lines 648–656; explicitly NOT triggered by `skip` or `report_section_only` |
| Coordination Conventions table extended (init-suggestions + finalisation-enhancements + 4 follow-up rows) | ✓ | lines 748, 758, 759–762 |
| Branch & Leaf Index "Top-level artifacts" extended | ✓ | lines 1036–1042 |
| K10a `Q-Finalisation-Enhancements` gate (multi-select 0–5, skip-all path, mode coverage, ensemble layered cadence) | ✓ | section at lines 1062–1126; skip-all backwards-compat path explicit line 1066; graceful degradation line 1068; ensemble layered cadence lines 1139–1150 |
| K10b per-item treatment sub-questions (queue default, spawn_now opt-in) | ✓ | lines 1092–1104 |
| K10b cost-ack re-presentation for `spawn_now` (read-only-richness) | ✓ | lines 1105–1126 |
| K10c `finalisation-enhancements.yml` update flow | ✓ | lines 1128–1137 |
| K10c continuation menu extended (Apply un-chosen / Spawn queued / grouped under section headings) | ✓ | lines 961–974 (menu); lines 980–986 (handler step 12) |
| **Negative**: no `Q-Comprehensiveness` anywhere | ✓ | grep returns 0 matches |
| **Negative**: no `--reset-richness` anywhere | ✓ | grep returns 0 matches |
| Backwards-compat strings preserved (Anti-Homogenization/isation, Universal Contrast, Subject-Matter Focus, MUST_FIX, Pattern B, paired HTML+PDF) | ✓ | grep returns 58 hits across the 6 anchor strings; line 229 confirms "paired HTML + PDF report" |
| Non-interactive abort rule preserved on merged gate | ✓ | line 208 (Sub-Q1 receives non-interactive default `default`; Sub-Q2 aborts rather than defaulting) |
| `compact` decision-guidance explicitly notes "reproduces pre-richness behaviour" | ✓ | line 183 (option text) and line 144 (cost table) both contain the anchor |
| Mode-swap preserves richness selection | ✓ | lines 191–194 each mode-swap option explicitly notes "Richness selection preserved across swap"; line 199 + line 204 reinforce |
| Ensemble K10 layered cadence (per-tree write-only + single combined root + union ranking) | ✓ | lines 1139–1150 |
| Lints clean | ✓ | `ReadLints` returned no errors on the modified file + this subtask file |
| Protocol-layer assertions pass | ✓ | `pytest evals/test_q_meditate.py -k 'TestMeditateConfigPresence or TestMeditateCommandDefinition' -x` → 8 passed, 22 deselected, 0 failed |
| Scope check | ✓ | `.cursor/commands/crux-meditate.md` is the only repo source-of-truth file plausibly attributable to subtask 03 — see scope notes below |

**Scope notes** (independent confirmation that subtask 03's executor did not cross scope):

- `.cursor/agents/crux-cursor-memory-manager.md` shows uncommitted changes in `git status`, but those are subtask 04's deliverables (mtime of `subtask-04-…md` = 22:58, after subtask 03's 22:56). The agent-file diff content is the `comprehensiveness:` payload propagation + combined-confirmation rewrite explicitly listed in subtask 04's Deliverables Checklist (which is now also ticked). Subtask 03's executor did NOT modify the agent file — they correctly limited their scope to the coordinator command.
- Other uncommitted files (`.gitignore`, `README.md`, `docs/crux-memories.md`, `web/compress.md/memories.html`, staged `AGENTS.md` + `install.py`) are pre-existing changes from prior 20260517 spec work unrelated to subtask 03 (e.g. `.gitignore` adds `.yarn/install-state.gz`; `README.md` documents the OLD `Q-Cost-Acknowledgment` name — content predates this spec).
- No edits to any `.crux.md` / `.crux.mdc` files, `scripts/create-crux-zip.py`, `.crux/dist-manifest.json`, or `.github/workflows/version-bump.yml` (subtask 08 / 10 scope).

**Minor observations** (not blocking, not unticking any item — flagged for subtask 09 integrity-review or a follow-up cleanup pass):

1. **Stale `Q-Confirm-1` / `Q-Confirm-2` references in Ensemble + deep-confirm prose**:
   - Line 729: deep-confirmation flow describes the option set as "the same … option set as Q-Confirm-1".
   - Line 863: Ensemble step 6 says "After facet confirmation completes (Q-Confirm-1 + Q-Confirm-2)".
   - Line 873: Ensemble step 6 says "the Q-Confirm-2 value from step 6".

   These are downstream references in workflow prose. The gate-definition replacement at lines 295–361 (now the combined Pattern-B askQuestion lines 403–646) IS done, and a deliberate historical reference at line 405 ("replacing the legacy sequential Q-Confirm-1 + Q-Confirm-2 calls") explicitly acknowledges the rename. The three remaining mentions in workflow prose should be updated to reference the combined askQuestion by name, but the underlying behaviour is correctly threaded through (the combined askQuestion's resume payload carries both the facet decision and the `confirmDeepFacets` enum together).

2. **Q-Finalisation-Enhancements not enumerated as a numbered sub-step of step 8**: the gate is defined as its own `###` section (lines 1062–1150) with explicit "fires BEFORE the adversarial review begins" prose, but step 8's sub-step list (lines 803–821 Research / lines 834–845 Quick) does not insert a new numbered sub-step between sub-step 5 (Branch & Leaf Index refresh) and sub-step 6 (Adversarial review). The placement is semantically clear from the dedicated section and from line 788 ("After consolidation completes and before adversarial review begins, the calling agent also runs `Q-Finalisation-Enhancements` (K10a)"), so the gate IS unambiguously sequenced — this is purely a presentation observation.

Neither observation rises to the bar of "deliverable not met" — both are doc-language polish opportunities that subtask 09 (integrity review) can address.
