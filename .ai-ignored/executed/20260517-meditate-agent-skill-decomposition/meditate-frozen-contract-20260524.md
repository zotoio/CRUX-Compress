# Frozen Meditate Contract — 20260524 (Refresh)

> **Supersedes** `meditate-frozen-contract-20260517.md` (which captured the
> pre-richness contract). Captured at working-tree state of git SHA
> `b4fc33b0c034866bb60b7fe7b03be9e0c7a18bbf` + unstaged 20260523 richness
> changes on 2026-05-24.
>
> **Purpose**: refresh the authoritative freeze line for the
> `meditate-agent-skill-decomposition` spec (`20260517`) to incorporate the
> completed sibling spec `specs/20260523-meditate-richness/` (executor
> sign-off 2026-05-24, all 9 subtasks judge-verified — see
> `specs/20260523-meditate-richness/execution-report-meditate-richness-20260523.md`).
> The 20260523 richness changes are present in the working tree
> (unstaged) but factually live at the file paths the 20260517
> decomposition spec operates on — subtasks 02 → 12 must trace their
> planned moves / new artefacts / diffs against **this** freeze line,
> not against `meditate-frozen-contract-20260517.md`.
>
> Every contract item is back-traceable to a line range or section
> heading in the **current** sources at the working-tree state:
>
> - `.cursor/commands/crux-meditate.md` (**2142 lines** — was 1493)
> - `.cursor/agents/crux-cursor-memory-manager.md` (**1388 lines** — was 946)
> - `evals/test_q_meditate.py` (**1335 lines** — was 240; 28 new richness test
>   classes added on top of the 8 pre-existing classes, ≈30 net new classes
>   counting refactors)
> - `evals/sdk/tests/q-meditate.test.ts` (**576 lines** — was 357; 4 new
>   describe blocks / 22 new tests on top of the existing Q1–Q3 blocks)
> - `evals/test_p_amnesia.py` (unchanged — `EXPLICIT_MEMORY_COMMANDS` row only)
>
> Where the two source files (command + memory-manager) mirror each
> other the command file is treated as the user-facing canonical text
> and the agent file as the executable canonical text. Differences are
> noted explicitly.
>
> **Source-of-truth map** (Section 10) is the single concordance the
> integrity-review subtask (12) consumes when verifying the post-refactor
> repo.

---

## 0. What changed since 2026-05-17

Thirteen new surfaces were added by the 20260523 richness spec. Each
must be preserved by the 20260517 decomposition without functionality
loss. The 13 surfaces:

| # | Surface | Where it lives today (post-richness) |
|---|---------|--------------------------------------|
| 1 | Merged depth × richness × mode gate `Q-Cost-and-Richness-Acknowledgment` (replaces `Q-Cost-Acknowledgment`) | Command lines 106–208 |
| 2 | Read-only-richness variant `Q-Cost-Acknowledgment-Expansion` | Command lines 210–256 |
| 3 | `comprehensiveness:` payload propagated alongside `theming:` | Command lines 361–390; Agent lines 307–337 |
| 4 | New Pattern-B `Q-Finalisation-Enhancements` gate (K10a) — multi-select 0–5, K10b mixed-cost taxonomy with per-cheap-type rendering contract for 7 types, K10c `finalisation-enhancements.yml` update flow, K10 ensemble respawn targeting, ensemble layered cadence | Command lines 1062–1186; Agent lines 596–722 (single-model step 8 + 8b) and 1189–1349 (Ensemble Aggregation 3b–3f + 5) |
| 5 | Adversarial review Dim 12 (Comprehensiveness fidelity) and Dim 13 (Init-suggestion AND finalisation-enhancement honour) with respawn protocol | Command lines 1207–1290 (Dimensions §), 1368–1447 (Report-Skill Respawn Protocol §) |
| 6 | Reviewer escalation Pattern B with mandatory `context` decision-guidance | Command line 1291 (restated; pre-existing rule preserved verbatim) |
| 7 | Report-Skill Respawn Protocol (K9 base + K10b extension) | Command lines 1368–1446 |
| 8 | Comprehensiveness Level Mapping contract — 12 dimensions × 4 levels (drives Per-Branch Section Rule, Depth-3 Leaf Inclusion Rule, Peer-Review Surfacing Rule, citation density, section length budgets, ensemble cross-model depth) | Command lines 1545–1571 |
| 9 | 4-mode `additional_focus_areas[]` reconciliation (write side — step 4b) with 4 treatments (`skip` / `additional_facet` / `report_section_only` / `additional_facet_AND_section`) | Agent lines 505–568 (post-W1b canonical) |
| 10 | `init-suggestions-{ts}.yml` schema + write semantics + report-side honour rules | Agent lines 517–566; Command lines 1807–1821 (Init-Suggestions Honour §) |
| 11 | Peer-review report-side surfacing (named sections / per-branch dedicated) at higher comprehensiveness levels | Command lines 1799–1805 (Peer-Review Surfacing Rule); agent peer-review file spec unchanged at agent lines 1008–1036 |
| 12 | Layered ensemble K10 cadence — per-tree `{model-subdir}/finalisation-enhancements.yml` + root combined `finalisation-enhancements.yml` after `cross-model-synthesis.md`; single combined multi-select at ensemble root | Agent lines 1215–1349 (Ensemble Aggregation Mode steps 3b–3f); Command lines 1153–1184 (K10 Ensemble Respawn Targeting + Ensemble layered cadence §) |
| 13 | New eval test classes (28 new on top of 8 pre-existing in `evals/test_q_meditate.py`) and 4 new TS describe blocks (22 tests) in `evals/sdk/tests/q-meditate.test.ts` | See §10 source-of-truth map |

**Functional preservation invariants (unchanged across all 4 richness levels per K7 + Requirement 10)**:

- Anti-Homogenisation Rules (§6.2 of 20260517 freeze)
- Universal Contrast / WCAG (§6.3)
- Subject-Matter Focus rule (§8)
- Pattern A vs Pattern B boundaries (§3) — subagents NEVER call `AskQuestion`
- Citation discipline (§5.5) — mode-driven (Research mandatory / Quick warn-only)
- Retrospective always-written rule (§5.7)
- Mandatory paired HTML + PDF rule (§6.1)
- Adversarial review-and-fix cycle iteration cap = 3 (§4.6)
- Headless Chrome → Chromium degradation chain (§6.6)
- Non-interactive abort on cost gate (§2.2)
- `confirmDeepFacets` deep-YAML escalation schema (§2.7)
- Facet registry lock — `mkdir`-based (§5.4)
- Peer-review file spec — Research mode only (§5.6)
- Theming payload propagation + subagent abort if missing (§2.4)
- Branch & Leaf Index template — entries listed below extended with `init-suggestions-{ts}.yml` and `finalisation-enhancements.yml` rows; existing template otherwise verbatim (§5.8)

The richness spec varied *richness*, not *rigor*. Every safeguard
above applies identically at `compact` / `default` / `detailed` /
`exhaustive`.

---

## 1. Modes Inventory

The 20260523 richness spec did **not** change the mode set or mode-selection
logic. Three new dimensions modulate cost: **depth × richness × mode**
(with ensemble multiplying per-tree counts by `N`).

| Mode | Flag | Default? | Trigger | Calling-agent ownership | Subagent ownership | Per-tree agent count (at depth 3, varies by richness — see Section 2.2 cost table) | Source |
|------|------|----------|---------|--------------------------|--------------------|-----------------------------------|--------|
| **Research** | _(none)_ | Yes | `/crux-meditate [topic]` with no `--quick` and no `--ensemble` in `$ARGUMENTS` | All five gates + steps 9–12 continuation menu | Depth-0 manager runs subagent **steps 1–13** (Research) on `crux-cursor-memory-manager` | ~45 at depth 3 for `compact` / `default` / `detailed`; ~72 at depth 3 for `exhaustive` (+27 per-leaf citation-builders) | Command lines 23–28, 61–67; Agent lines 279–294, 399–748 |
| **Quick** | `--quick` | No | Flag present anywhere in `$ARGUMENTS` (case-sensitive, whitespace-bounded) | Identical 5 gates + steps 9–12 | Subagent **6-step protocol** at each non-leaf agent; no peer review; warn-only citations at every level (K7 carve-out per OQ #5) | ~42 at depth 3 (same as before — `exhaustive` does NOT add per-leaf citation-builders in Quick) | Command lines 23–28, 823–845; Agent lines 752–767, 866–909 |
| **Ensemble + Research** | `--ensemble` | No | Flag present; reads `cruxMemories.meditate.modelPool` from `.crux/crux-memories.json` (default `N=3`) | Ensemble Protocol owns steps 1–10 (model-pool read, depth selection, **merged cost-and-richness ack**, theme preflight, ensemble working dir, **shared facet derivation + shared init-suggestions**, N parallel trees, deep-confirm hook across all subdirs, aggregator spawn, ensemble verification) | Each model tree runs the standard Research depth-0 manager via `model: ensembleModel`; aggregator runs in **Ensemble Aggregation** function (now extended with K10 layered cadence steps 3b–3f) | `~{N × per_tree_count + 1}` agents | Command lines 26, 165–175, 847–919; Agent lines 1189–1349 |
| **Ensemble + Quick** | `--ensemble --quick` (any order) | No | Both flags present | Same Ensemble Protocol; `meditateMode: "quick"` threaded through | Each model tree runs the Quick 6-step protocol; aggregator runs in **Ensemble Aggregation** function | `~{N × quick_tree_count + 1}` agents | Command lines 16, 26, 41–46; Agent lines 290–294, 295–305 |

**Key config keys** (all consulted by the calling-agent / depth-0 manager):

| Key | Default | Purpose | Source |
|-----|---------|---------|--------|
| `flags.enableMemories` | `"true"` | Feature guard — abort if false | Agent line 401, 1370 |
| `cruxMemories.meditate.modelPool` | `[{slug:"gpt-5.5-medium",label:"GPT 5.5"},{slug:"claude-opus-4-7-thinking-xhigh",label:"Opus 4.7"},{slug:"gemini-3.1-pro",label:"Gemini Pro 3.1"}]` | Models to spawn in Ensemble mode; empty → abort with config-pointer error | `.crux/crux-memories.json` lines 80–87; Command lines 43, 853 |
| `cruxMemories.meditate.ensembleAggregatorModel` | `null` (uses caller's own model) | Override the model used for the cross-model aggregator agent | `.crux/crux-memories.json` line 86; Command line 883 |
| `cruxMemories.meditate.finalisationEnhancements.minimumImpactThreshold` | `6` (composite_score floor on 1–10 × 1–10 rubric) | Filters K10c candidates below threshold; `degradation_reason` records when <5 candidates clear | Agent lines 622, 655; OQ #12 |
| `cruxMemories.meditate.finalisationEnhancements.weights` | `{ impact: 1.0, insight_value: 1.0 }` (default = multiplicative `product`; `formula: "weighted_sum"` flips to weighted-sum) | K10c rubric weighting | Agent lines 621, 656–657; OQ #11 |
| `maxDepth` | `3` (default-preselected) | Recursion depth (1, 2, or 3); set by `Q-Depth-Selection`; propagated unchanged to every agent | Command lines 56–105; Agent lines 577 |
| `meditateMode` | `"research"` | Mode flag propagated to every child | Command lines 41–46; Agent lines 296–301 |
| `confirmDeepFacets` | `"none"` (default-preselected) | Enum `none` / `depth_2_only` / `all_levels`; set by **Sub-Q5** of the combined Pattern-B askQuestion (was `Q-Confirm-2`); propagated to every child | Command lines 603–631; Agent lines 339, 587 |
| `comprehensiveness` (payload) | `level: "default"` (preselected at the merged gate) | **NEW** — structured payload (level + minima + 6 dimension fields); set-once-per-invocation per K6; propagated unchanged from depth-0 to every child and every ensemble tree | Command lines 361–390; Agent lines 307–337 |
| `ensembleMode` | `false` | Set true when `--ensemble` is present | Command lines 41–46 |
| `selectedRichness` | `"default"` (calling-agent local) | Tracks the Sub-Q1 richness selection; preserved across Sub-Q2 mode swaps per OQ #1; locked across expansion continuations per K6 | Command line 206 |

**Mode-selection logic** — unchanged from 20260517 freeze §1; richness spec did not alter mode selection. Command lines 38–46.

**Internal/non-user-facing invocation forms** (Agent lines 292–294): child invocations with `meditateMode`, `meditateDepth`, `subfocus`, `subfocusIndex`; ensemble member invocations with `preConfirmedFacets`, `ensembleModel`, `confirmDeepFacets`; Ensemble Aggregation invocations with `ensembleAggregation` flag. The richness spec adds: every child invocation now also carries `comprehensiveness` (propagated unchanged) and ensemble member invocations also carry the shared init-suggestions payload.

**Argument forms** (Command lines 9–18, 50–53): unchanged.

### 1.1 Richness × Depth × Mode cost table (worked example — verbatim from command lines 142–163)

The merged `Q-Cost-and-Richness-Acknowledgment` gate's prompt prose
embeds this table verbatim (substituting actual `{N_compact}` /
`{N_default}` / `{N_detailed}` / `{N_exhaustive}` numbers for the
selected depth + mode):

```
Cost summary at depth {maxDepth} in {mode} mode:

| Richness   | Agents per tree | Report tokens | Notes |
|------------|-----------------|---------------|-------|
| compact    | ~{N_compact}    | ~25k          | reproduces pre-richness behaviour |
| default    | ~{N_default}    | ~40k          | richer report; same agent count as compact |
| detailed   | ~{N_detailed}   | ~60k          | adds per-branch dedicated sections + per-leaf-detail |
| exhaustive | ~{N_exhaustive} | ~90k          | adds per-leaf citation-table pass (Research only — +27 builders at D=3); Quick is warn-only per OQ #5 |

(Ensemble adds ~{N_aggregator} aggregator + N×per-tree reflection cost ~6k tokens.)
```

**Canonical pinning (depth=3, Research, 3 facets, no ensemble, no additional facets)** — Command line 163:

| Level | Agent count (per tree) | Approx report-skill output |
|-------|------------------------|----------------------------|
| `compact` | ~45 (today's baseline: 1 depth-0 + 3 depth-1 + 9 depth-2 + 27 depth-3 + 3 peer reviewers + ≤3 adversarial review iters; rounding) | ~25k tokens |
| `default` | ~45 (no new agents; richer report only) | ~40k tokens |
| `detailed` | ~45 (no new agents; per-branch + peer-review dedicated sections inside the report skill) | ~60k tokens |
| `exhaustive` | ~72 (~45 + 27 per-leaf citation-table builders at depth 3 Research) | ~90k tokens |

**Quick mode rule**: subtract peer reviewers (3 at depth-3) from each row; `exhaustive` does NOT add per-leaf citation-builders in Quick (K7 + OQ #5 carve-out).

**Ensemble multiplier**: multiply per-tree counts by `poolSize` and add 1 aggregator.

**`compact` backwards-compat anchor** (K1 + Requirement 9 + DoD bullet): a `compact`-level invocation reproduces the pre-richness behaviour byte-for-byte — same chart/infographic/calculator minima (≥4/≥3/≥1), same depth-3 elision, same peer-review consolidation-only surfacing, same per-branch consolidation-only sections. The only "breaking" change vs pre-richness is the default-when-unspecified value (`default`, not `compact`); the legacy behaviour remains available as opt-in by selecting `compact`.

---

## 2. Calling-Agent Gates (Verbatim or Near-Verbatim)

There are **five logical gates** post-richness — four pre-spawn (Pattern A
for gates 1–3; Pattern B mid-flow for gate 4) plus one mid-workflow gate
(`Q-Finalisation-Enhancements`, K10a — Pattern B, fires post-consolidation
/ pre-adversarial-review).

The pre-spawn gate count stays at **4 logical slots** even after the K2
merge (Depth → merged Cost-and-Richness → Theme → combined
Facet/Sections/Visualisations/Focus-Areas). Per K2 + spec Requirement 1,
**no standalone `Q-Comprehensiveness` gate exists anywhere** —
richness is folded into Sub-Q1 of the cost-and-richness gate.

### 2.1 `Q-Depth-Selection` (mandatory, calling agent's very first action)

Source: Command lines 55–105.

Unchanged from 20260517 freeze §2.1 — prompt text, substitutions, options, and behaviour rules are byte-identical. The agent-count substitutions still resolve from the per-mode table at command lines 60–67 (which is also unchanged).

### 2.2 `Q-Cost-and-Richness-Acknowledgment` (mandatory, calling agent's second action — **MERGED per K2; replaces `Q-Cost-Acknowledgment`**)

Source: Command lines 106–208. **This entirely replaces the legacy `Q-Cost-Acknowledgment` from 20260517 freeze §2.2.** The legacy gate name is dead — `evals/test_q_meditate.py::TestMeditateMergedCostAndRichnessGate::test_no_standalone_q_comprehensiveness_gate` + `TestMeditateBackwardsCompatibility::test_no_standalone_q_comprehensiveness_gate` pin this negative invariant.

**Prompt preamble (verbatim)** — Command lines 127–161:

```
/crux-meditate is a deep research task that will spawn approximately {N} agents
(depth {maxDepth} in {mode} mode), produce a comprehensive HTML + PDF report with
infographics and clickable index, and run an adversarial review-and-fix cycle
before any output is finalised.

You're also choosing a comprehensiveness level — the level controls how much
research material reaches the report. Higher levels render more depth-3 detail,
more visualisations, more per-branch + peer-review sections, and longer prose,
without affecting research rigor (citation discipline, anti-homogenisation,
adversarial review are all preserved at every level per K7).

Cost summary at depth {maxDepth} in {mode} mode:

| Richness   | Agents per tree | Report tokens | Notes |
|------------|-----------------|---------------|-------|
| compact    | ~{N_compact}    | ~25k          | reproduces pre-richness behaviour |
| default    | ~{N_default}    | ~40k          | richer report; same agent count as compact |
| detailed   | ~{N_detailed}   | ~60k          | adds per-branch dedicated sections + per-leaf-detail |
| exhaustive | ~{N_exhaustive} | ~90k          | adds per-leaf citation-table pass (Research only — +27 builders at D=3); Quick is warn-only per OQ #5 |

(Ensemble adds ~{N_aggregator} aggregator + N×per-tree reflection cost ~6k tokens.)

Compared with a single prompt or chat reply, this is significantly more expensive
in time and tokens. It's designed for well-considered problem statements tied to
high-value strategic activities (architecture decisions, strategic planning,
investment analyses, multi-week initiatives, deep technical research).

For lighter questions, prefer:
  - a regular chat
  - /crux-recall to query existing memories without spawning a tree
  - a single targeted prompt scoped to one file or function

Pick a richness level, then choose how to proceed.
```

**Ensemble-mode first-paragraph replacement (verbatim)** — Command lines 167–175:

```
/crux-meditate --ensemble will run {poolSize} complete depth-{maxDepth} meditation
trees in parallel — one per model family ({modelLabels}) — spawning approximately
{N} agents total, then aggregate findings into a cross-model synthesis report
highlighting where models converge (high confidence), diverge (needs investigation),
and surface unique insights.

Each model tree produces its own full HTML + PDF report with infographics, and the
ensemble aggregation produces a separate cross-model synthesis report. All trees
share the same user-confirmed facets for apples-to-apples comparison.
```

**Sub-Q1 — Richness level (single-select; preselected = `default`; verbatim options)** — Command lines 177–187:

The `default` level is **both** the preselected option AND the enum value propagated through the `comprehensiveness:` payload — this dual meaning is intentional per K1's naming-reconciliation paragraph.

- `compact` — **Compact — pre-richness behaviour.** Reproduces the meditate report shipped before this spec (≥4 charts, ≥3 infographics, ≥1 calculator, depth-3 elided beyond summary, consolidation-only sections). Lowest token cost (~25k tokens). Pick when you want a backwards-compatible run or when token budget is tight. NOTE: this level reproduces pre-richness behaviour for users who want the legacy minima.
- `default` **[preselected]** — **Default — new default richness.** The new default-when-unspecified richness (5 charts / 4 infographics / 1 calculator, `branch_summary` per-branch sections, ~1.6× richer prose, ~40k tokens). Pick when you want the richer baseline without exhaustive cost. NOTE: the level *name* `default` matches the preselected option — these are not in conflict (per K1's naming-reconciliation paragraph; the level enum value `default` is what propagates through the `comprehensiveness:` payload).
- `detailed` — **Detailed — substantial bump.** 7 charts / 6 infographics / 2 calculators / `per_leaf_detail` per-branch sections / depth-3 `verbatim_quotes` / peer-review `named_section` (~60k tokens). Pick when stakeholders need every angle.
- `exhaustive` — **Exhaustive — maximum richness.** 10 charts / 8 infographics / 3 calculators / per-finding citation columns / `per_branch_dedicated` peer-review / `per_leaf_attribution` ensemble (~90k tokens). Spawns +27 per-leaf citation-builder agents at depth 3 in Research (Quick mode is warn-only per OQ #5).

**Sub-Q2 — Proceed / mode-swap / cancel (verbatim options; no preselection — proceed is NOT auto-selected)** — Command lines 188–196:

- `proceed` — Yes, this is a high-value strategic problem; proceed in the currently-selected mode (`Research` or `Quick`, depth {maxDepth}, with or without Ensemble)
- `switch_to_quick` — Proceed but switch to Quick mode (~{quickCount} agents at depth {maxDepth}, faster, no peer review). **Richness selection preserved across swap.** **Only offered when current mode = Research.**
- `switch_to_research` — Proceed but switch to Research mode (~{researchCount} agents at depth {maxDepth}, peer-reviewed, slower). **Richness selection preserved across swap.** **Only offered when current mode = Quick.**
- `switch_to_ensemble` — Proceed but enable Ensemble mode (~{N×perModelCount + 1} agents across {N} model families + cross-model aggregation). **Richness selection preserved across swap.** **Only offered when `ensembleMode` is false.** Read `cruxMemories.meditate.modelPool` to compute the agent count.
- `switch_to_single` — Cancel Ensemble, run on a single model instead (~{perModelCount} agents). **Richness selection preserved across swap.** **Only offered when `ensembleMode` is true.**
- `cancel` — Cancel — I'll use a different approach

**Mode-swap preserves richness (OQ #1 resolution — verbatim rule)** — Command line 199: the Sub-Q1 richness selection is preserved across any mode-swap decision. The prompt prose already displays all 4 richness rows for the current mode; a mode-swap recomputes the agent count but does not reset richness.

**Behaviour rules (verbatim)** — Command lines 201–208:

- **Always run on the first invocation** in a session, regardless of arguments. Depth Selection runs first, then `Q-Cost-and-Richness-Acknowledgment`.
- **Mode swaps**: update the active `meditateMode` (or `ensembleMode`) and proceed to Theme Preflight; do not re-ask `Q-Cost-and-Richness-Acknowledgment` or `Q-Depth-Selection`. **In all cases the richness selection from Sub-Q1 is preserved.**
- **Cancel**: respond with a short note acknowledging the cancellation and stop. Do not spawn anything, do not run Theme Preflight, do not create the working directory.
- **Richness set-once-per-invocation (K6)**: the richness level selected in Sub-Q1 is stored as `selectedRichness` and propagated to the depth-0 subagent as part of the `comprehensiveness:` payload. **It cannot be changed after this gate closes.** Expansion-direction continuations (calling agent step 12) use the **read-only-richness variant** (§2.3) — richness is shown locked; no "keep richness setting?" follow-up is offered. Users who want to change richness must `cancel` and re-invoke `/crux-meditate`.
- **Expansion-direction continuation** (calling-agent step 12): run a **shortened** version of this acknowledgment (`Q-Cost-Acknowledgment-Expansion` — uses the read-only-richness variant with locked richness). The mode-swap and depth options are **not** re-offered (both persist across expansions); the user can `cancel` and re-invoke `/crux-meditate` if they want to change mode or depth.
- **Non-interactive sessions** (e.g. CI): if `askQuestion` cannot be answered, abort with a clear error explaining the cost-acknowledgment requirement. Never default to `proceed` silently — the safeguard exists precisely because the cost is non-trivial. (Sub-Q1 receives the non-interactive default `default` per K2; Sub-Q2 aborts rather than defaulting to `proceed`.)

### 2.3 `Q-Cost-Acknowledgment-Expansion` — Read-only-richness variant (mandatory, calling-agent step 12 expansion path)

Source: Command lines 210–256. **This entirely replaces the legacy `Q-Cost-Acknowledgment-Expansion` from 20260517 freeze §2.3** — the legacy prompt is preserved verbatim in the body, but richness is now locked and shown as a non-interactive display row.

**Preamble (verbatim)** — Command lines 215–217:

```
You're continuing this meditation by expanding direction(s). Cost has been
recomputed for the expansion tree.
```

**Richness display row (locked — not interactive; verbatim)** — Command lines 219–222:

```
Richness: {selectedRichness} (locked — set at the start of this invocation;
cancel and re-invoke /crux-meditate to change)
```

**Prompt body (verbatim)** — Command lines 224–232 (mirrors the legacy `Q-Cost-Acknowledgment-Expansion` body byte-for-byte):

```
Expanding this meditation will spawn a new depth-{maxDepth} research tree
(~{N} additional agents) exploring the selected direction(s). This carries
the same per-meditation cost as the original invocation — a full recursive
tree, adversarial review cycle, and paired HTML + PDF report.

The previous meditation's results are preserved; this expansion produces a separate
report. If you only need a quick follow-up, consider a regular chat prompt instead.
```

**Options (Sub-Q2 only; verbatim)** — Command lines 236–237:

- `proceed_expansion` — Yes, spawn the expansion tree
- `cancel` — Cancel — I'll follow up in chat instead

**No "keep richness setting?" follow-up is offered** (K6 set-once rule) — richness is implicitly locked. **The existing "keep deep-confirm setting?" follow-up is preserved unchanged** (Command line 738; mirrors agent line — `confirmDeepFacets` persists across expansion by default with one-line opt-out).

### 2.4 Read-only-richness variant — generalised (Command lines 239–256)

The read-only-richness variant of `Q-Cost-and-Richness-Acknowledgment` is used whenever the gate re-fires after richness has been locked. **There are three triggers** — each fires at most once per cause within a single invocation; no re-presentation loops are possible.

- **Sub-Q1 (richness) is shown as a locked display row** (not interactive): `Richness: {locked_level} (locked — set at the start of this invocation; cancel and re-invoke /crux-meditate to change)`
- **Sub-Q2 (proceed/swap/cancel) remains fully interactive**
- **Prompt title** is **"Cost-and-Richness Acknowledgment (re-presented)"** per OQ #2

**Trigger preambles (verbatim)** — Command lines 250–254:

| Trigger | Preamble |
|---------|----------|
| Expansion path (calling agent step 12) | `You're continuing this meditation by expanding direction(s). Cost has been recomputed for the expansion tree.` |
| Additional-facet acceptance (from combined Pattern-B in §2.6) | `Cost has changed because you accepted {N} additional facets — please re-acknowledge or cancel.` |
| `spawn_now` acceptance (K10b) | `You've accepted spawning {N} follow-up agent(s) for finalisation enhancements ({enumerated_types}). The new total agent count is ~{N_total} (current depth {D}, richness {level}, mode {mode}, including {N_finalisation} spawn-now agents).` |

**Single-shot semantics** — Command line 1126: the cost-ack re-presentation for `spawn_now` is a single round trip. Treatment decisions are immutable for the remainder of the invocation after the cost-ack closes.

### 2.5 Theme Preflight Q1–Q5 (mandatory, Pattern A pre-collected before depth-0 spawn)

Source: Command lines 257–357.

**Unchanged from 20260517 freeze §2.4** — prompt text, Q1/Q1b/Q2/Q3/Q4/Q5 options, surprise_me non-interactive fallback, and `theming:` YAML payload (Command lines 337–357) are byte-identical. The only addition is the **Comprehensiveness payload propagation note** at command lines 361–390 (§2.7 below).

### 2.6 Combined Pattern-B Facet / Sections / Visualisations / Focus-Areas Confirmation (mandatory, Pattern B mid-flow at depth-0)

Source: Command lines 391–662. **This entirely replaces the legacy sequential `Q-Confirm-1` + `Q-Confirm-2` from 20260517 freeze §2.5 + §2.6.** The legacy `Q-Confirm-1` / `Q-Confirm-2` prompt prose is preserved verbatim inside Sub-Q1 (facets) and Sub-Q5 (deep_confirm) of the combined askQuestion, but they now fire as **one combined `askQuestion` with 5 sub-questions** in a single round trip per K4.

**Workflow rule (verbatim — Command lines 403–405)**:

> The depth-0 subagent derives 3 top-level facets PLUS 3–8 draft report sections, 5–10 candidate visualisations, and 0–5 additional focus areas. It writes all four blocks to `facets-pending-{ts}.yml` and returns a **combined `needs_user_input` block** to the calling agent. The calling agent then runs a **single `askQuestion` with 5 sub-questions** (facets + sections + visualisations + focus areas + deep_confirm) — one combined round trip replacing the legacy sequential Q-Confirm-1 + Q-Confirm-2 calls.

**Subagent-side `needs_user_input` schema (verbatim, abbreviated for length — see Command lines 407–474 for full block)**:

```yaml
needs_user_input:
  reason: "facets-and-init-suggestions-confirmation"
  pattern: "B"
  context: |
    The depth-0 seed exploration has produced:
    - 3 candidate facets for the meditation tree
    - {N_sections} candidate report sections derived from the topic
    - {N_visualisations} candidate visualisation types
    - {N_focus_areas} additional focus areas the topic touches outside the 3 facets
    Plus the deep-confirm question for depth-2/depth-3 facet derivation control.
    Confirm via the combined askQuestion below; the calling agent will resume
    me with the confirmed payload and I'll write init-suggestions-{ts}.yml
    and proceed to spawn the tree.
  decision_required: true
  prompt_inputs:
    facets:
      - index: 1
        title: "{facet-1-title}"
        subfocus: "{facet-1-subfocus}"
        slug: "{facet-1-slug}"
      # ... (3 items)
    sections:
      # 3-8 items per spec Risk #5 cap
      - id: "section-{slug-1}"
        title: "{section-1-title}"
        rationale: "{1-line why this section fits}"
        source_signals: ["[chat: turn-N]", "[memory: {memory-title}]", "[file: ...]"]
    visualisations:
      # 5-10 items per spec Risk #5 cap
      - id: "viz-{slug-1}"
        type: "{visualisation-type-enum}"
        rationale: "{1-line why this viz fits the topic}"
        what_it_would_show: "{1-2 sentences describing the rendering}"
        source_signals: [...]
    additional_focus_areas:
      # 0-5 items per spec Risk #5 cap
      - id: "focus-{slug-1}"
        title: "{focus-area-title}"
        rationale: "{1-line why this focus area is in scope-adjacent but not a primary facet}"
        source_signals: [...]
        recommended_treatment: "report_section_only"  # hint: skip/additional_facet/report_section_only/additional_facet_AND_section
    deep_confirm:
      default_option: "none"
      options: ["none", "depth_2_only", "all_levels"]
  files_written:
    - "facets-pending-{ts}.yml"
  resume_handler_contract:
    expected_input:
      facets_decision: "confirm_all | modify_one | modify_multiple | regenerate | cancel"
      facet_overrides: [{ index: 1|2|3, new_subfocus: "...", new_slug: "..." }]
      sections_kept: ["section-{slug-1}", ...]
      visualisations_kept: ["viz-{slug-1}", ...]
      additional_focus_areas_decisions:
        - id: "focus-{slug-1}"
          treatment: "skip | additional_facet | report_section_only | additional_facet_AND_section"
          custom_report_section_title: "..."
      deep_confirm_decision: "none | depth_2_only | all_levels"
```

**Calling-agent-side combined `askQuestion` (Pattern B integrity preserved; subagents NEVER call `AskQuestion`) — full schema at Command lines 478–646; per sub-question structure:**

| Sub-Q | ID | Kind | Required | Preselection | Verbatim prompt body source |
|-------|----|----|----------|--------------|----------------------------|
| 1 | `facets` | single_select | yes | none | Command lines 494–513 — verbatim mirror of legacy Q-Confirm-1 (5 options: `confirm_all` / `modify_one` / `modify_multiple` / `regenerate` / `cancel`) |
| 2 | `sections` | multi_select | no | all preselected | Command lines 535–543 — multi-select over `prompt_inputs.sections` |
| 3 | `visualisations` | multi_select | no | all preselected | Command lines 549–558 — multi-select over `prompt_inputs.visualisations` |
| 4 | `additional_focus_areas` | per_item_single_select | no | per item: `skip` (default) | Command lines 564–601 — **4-mode** decision per item: `skip` / `additional_facet` (cost_change_signal=true) / `report_section_only` / `additional_facet_AND_section` (cost_change_signal=true) |
| 5 | `deep_confirm` | single_select | yes | `none` | Command lines 607–631 — verbatim mirror of legacy Q-Confirm-2 (3 options: `none` / `depth_2_only` / `all_levels`) |

**Sub-Q4 verbatim 4-mode descriptions (Command lines 586–601)** — per-item options:

- `skip` — Skip — drop this focus area entirely. Decision guidance: "Pick when not relevant. Zero cost."
- `additional_facet` — Add as new facet (+~14 agents at D=3 Research; +~13 at D=3 Quick; cost-ack re-fires). Decision guidance: "Pick when the focus area warrants its own research branch. Bumps facet count → multiplies agent count." `cost_change_signal: true`
- `report_section_only` — Add as new report section (no agent cost). Decision guidance: "Pick when the topic warrants a dedicated section but no new exploration branch." `cost_change_signal: false`
- `additional_facet_AND_section` — Both — new facet + dedicated named section (cost-ack re-fires; follow-up text for custom section title). Decision guidance: "Pick when you want the new branch AND a named report section." `cost_change_signal: true`; `follow_up: "custom_report_section_title"`

**Resume handler sequence (verbatim — Command lines 633–646)**:

```
1: "Collect Sub-Q1 (facets) answer + any follow-up text inputs for modify_one/modify_multiple"
2: "Collect Sub-Q2 (sections) multi-select answer"
3: "Collect Sub-Q3 (visualisations) multi-select answer"
4: "Collect Sub-Q4 (additional_focus_areas) per-item answers + follow-up text for custom_report_section_title"
5: "Collect Sub-Q5 (deep_confirm) answer"
```

**Cost-change check + re-presentation (verbatim — Command lines 640–646)**:

```
condition: "any additional_focus_areas[i].treatment in {additional_facet, additional_facet_AND_section}"
on_true: "fire Q-Cost-and-Richness-Acknowledgment read-only-richness variant BEFORE resuming the depth-0 manager; on cancel abort and delete facets-pending-{ts}.yml; on re-acknowledge resume with full payload"
on_false: "resume depth-0 manager directly with confirmed payload"
on_cancel: "abort meditation; delete facets-pending-{ts}.yml; do NOT create init-suggestions-{ts}.yml"
on_regenerate: "resume depth-0 manager with regenerate_facets=true + previous facets-pending-{ts}.yml path; depth-0 manager re-emits needs_user_input with new prompt_inputs (cap 3 attempts per existing rule)"
```

**Resume-handler contract after re-presentation (verbatim — Command lines 657–662)**:

1. Calling agent resumes the depth-0 subagent with the confirmed facets (including any overrides), the `confirmDeepFacets` enum value, the confirmed `sections_kept` IDs, the confirmed `visualisations_kept` IDs, and the `additional_focus_areas_decisions` map.
2. Depth-0 subagent: appends the confirmed facets to `facet-registry.yml` (Research mode), promotes the draft to the final `facets.md`, deletes `facets-pending-{ts}.yml`, writes `init-suggestions-{ts}.yml` (confirmed sections + visualisations + per-item focus-area treatments), and proceeds to step 5 of the workflow (spawn explorers). The `confirmDeepFacets` value is propagated to every child spawn in step 5.
3. If `facets_decision` was `regenerate` → calling agent resumes the subagent with `regenerate_facets: true` plus the previous `facets-pending-{ts}.yml` path; the subagent reads the rejected set, derives a different one, and re-escalates. Loop, **capped at 3 regeneration attempts**.
4. If `facets_decision` was `modify_one` or `modify_multiple` → calling agent collects the replacement text(s) via a free-text follow-up, then resumes the subagent with `facet_overrides: [{ index: N, new_subfocus: "...", new_slug: "..." (optional) }, ...]`. The subagent applies the overrides and proceeds to resolve the full combined payload.

### 2.7 `comprehensiveness:` payload propagation (Pattern A — passed alongside `theming:`)

Source: Command lines 361–390; Agent lines 307–337.

**New surface introduced by 20260523 K5.** The calling agent serialises the Sub-Q1 richness selection into a `comprehensiveness:` payload and includes it in the depth-0 subagent's spawn prompt alongside the existing `theming:` payload. **Subagents MUST abort if `comprehensiveness:` is missing from the spawn prompt** with the exact error string `"comprehensiveness: payload required; missing from spawn prompt — caller misconfigured"`. The abort rule applies at every depth (depth-0, depth-1, depth-2, depth-3 children) and in every mode (Research, Quick, Ensemble).

**Payload shape (verbatim YAML, Command lines 365–387 / Agent lines 309–331)**:

```yaml
comprehensiveness:
  level: "compact" | "default" | "detailed" | "exhaustive"   # from Sub-Q1 of Q-Cost-and-Richness-Acknowledgment
  minima:
    charts:
      count: 4 | 5 | 7 | 10                                  # per level mapping table (§6.1)
      types_required: "..."                                   # per level
    infographics:
      count: 3 | 4 | 6 | 8
      types_required: "..."
    calculators:
      count: 1 | 1 | 2 | 3
      scenarios_per: 3 | 4 | 5 | 5
  depth3_leaf_inclusion: "summary" | "summary" | "verbatim_quotes" | "verbatim_quotes"
  per_branch_section_depth: "consolidation_only" | "branch_summary" | "per_leaf_detail" | "per_leaf_detail"
  citation_density: "mandatory_or_warn_only"                  # Research = mandatory; Quick = warn_only at all levels (K7)
  peer_review_surfacing: "consolidation_only" | "consolidation_only" | "named_section" | "per_branch_dedicated"
  section_length_budget_tokens:
    hero: 800 | 1200 | 1800 | 2400
    per_facet: 2500 | 4000 | 6500 | 9500
    citations: 1000 | 1500 | 2000 | 2500
  ensemble_cross_model_depth: "per_facet_cards" | "per_facet_cards" | "per_leaf_attribution" | "per_leaf_attribution"
```

**Propagation rules** (Agent lines 333–337):

- At `comprehensiveness.level ≥ detailed`: depth-3 leaf agents MUST include verbatim quotes from the sources they cite in `## Discoveries` (`depth3_leaf_inclusion = verbatim_quotes`). At `compact` or `default` the leaf agent writes a summary only.
- All agents at every depth: `## Discoveries` section length MUST stay within `comprehensiveness.minima.section_length_budget_tokens.per_facet` (number of tokens). The depth-0 manager's own synthesis sections honour `hero` and `citations` budgets.
- At `exhaustive` in Research mode: citation density escalates to `per_finding_table` — every finding table must include a citation column. At `exhaustive` in Quick mode: warn-only validation rule is preserved (citation tables still rendered with `(citation needed)` placeholder text where citations are absent per K7 + OQ #5 carve-out).
- Citation **validation** rule is mode-driven at every comprehensiveness level (K7): Research = `mandatory` (parent Phase E respawns on failure); Quick = `warn_only` (parent logs warning, does NOT respawn). This rule is invariant across all 4 levels.

### 2.8 `Q-Finalisation-Enhancements` (mandatory, calling agent's mid-workflow Pattern-B gate — **NEW per K10a**)

Source: Command lines 1062–1186; Agent lines 596–722 (single-model step 8) and 1189–1349 (Ensemble Aggregation steps 3b–3f).

**Timing**: fires **after consolidation completes** (after `consolidation.md` has been written and the Branch & Leaf Index has been refreshed in `facets.md`) but **before the adversarial review-and-fix cycle begins**. The gate runs in **both Research mode and Quick mode**, and at ensemble root (after all per-tree YAMLs are written and the aggregator produces the root combined YAML — see Ensemble layered cadence in §4.5).

**Skip-all backwards-compat path (verbatim — Command line 1066)**: if the user selects 0 items, resume the depth-0 manager with an empty accepted set; flow proceeds to adversarial review unchanged — this exactly reproduces today's pre-K10 behaviour. Pinned by `evals/test_q_meditate.py::TestMeditateK10SkipAllBackwardsCompat`.

**Graceful degradation (verbatim — Command line 1068)**: if `finalisation-enhancements.yml` contains fewer than 5 candidates (consolidation reflection found fewer high-quality ones), present whatever count surfaced (even 1–4). If `degradation_reason` indicates zero candidates met the threshold, surface a one-line "no high-quality enhancement candidates surfaced" message and proceed directly to adversarial review without firing `askQuestion`.

**Prompt preamble (verbatim — Command lines 1074–1085)**:

```
The meditation's consolidation reflection surfaced up to 5 candidate enhancements
that could increase the report's value to you. Each is scored by impact (1–10)
and insight-value (1–10); composite = impact × insight_value.

Select 0–5 to accept. Each has a cost class:
  - cheap: rendered by report respawn within the ≤3 adversarial iteration cap
    (no new agent spawns; bundled into the first review iteration)
  - expensive: spawns follow-up work (default = queue to continuation menu;
    opt-in spawn_now triggers cost-ack re-presentation before adversarial review)

Selecting 0 (skip all) proceeds to adversarial review unchanged — this exactly
reproduces pre-K10 behaviour.
```

**Options (multi-select, 0–5; one option per candidate; verbatim Command lines 1088–1090)**:

- `{candidate.id}` — **{candidate.title}** [{candidate.cost_class}] — {candidate.description} (impact={candidate.impact_score} × insight={candidate.insight_value_score} = composite={candidate.composite_score})
  - Decision guidance: **Cheap items** ("respawn" treatment default): selecting will bundle this enhancement into the first adversarial review iteration's report-respawn payload. Zero extra agent spawns within this invocation. **Expensive items** ("queue" treatment default): selecting will write a follow-up artefact (`follow-up-{type}-{ts}.yml`) surfaced in the continuation menu as "Spawn queued follow-ups"; selecting `spawn_now` instead triggers cost-ack re-presentation before adversarial review.

**Per-item treatment sub-question — `Q-Finalisation-Enhancement-Treatment-{id}`** (for each accepted expensive item, `cost_class: "expensive"`; verbatim Command lines 1094–1103):

After the multi-select resolves, the calling agent runs a follow-up single-select for each accepted expensive item:

- `queue` **[default — preselected]** — Write `follow-up-{type}-{ts}.yml` next to `consolidation.md`; surface in continuation menu as "Spawn queued follow-ups". Zero in-invocation cost. Decision guidance: "The expensive enhancement is queued as a follow-up artefact. You can trigger it from the continuation menu after reviewing the report. Zero additional agents in this invocation."
- `spawn_now` — Opt-in: triggers cost-ack re-presentation BEFORE the adversarial review begins. Expensive agents spawn after the adversarial cycle completes. Decision guidance: "The expensive enhancement spawns immediately after the report is finalised. Triggers cost-ack re-presentation with updated total agent count. See per-type contributions in the cost table below:
  - `additional_meditation`: 1 top-level `/crux-meditate` invocation (nested tree; nested gate handles its own cost)
  - `extracted_spec`: 1 spec-generator agent
  - `extracted_memories`: 1 memory-extraction agent
  - `expanded_branch`: ~14 agents at D=3 Research (1 + 3 + 9 + 1 peer); ~13 at D=3 Quick"

**Cost-ack re-presentation for `spawn_now`** (verbatim — Command lines 1107–1124): uses the read-only-richness variant of `Q-Cost-and-Richness-Acknowledgment` with the `spawn_now` trigger preamble (full preamble text reproduced in §2.4 above). On **cancel**: drop the `spawn_now` treatments, fall back to `queue` treatment for those items (no work lost), proceed. On **re-acknowledge**: proceed to adversarial review; expensive agents spawn in parallel after the adversarial cycle completes. **Single-shot semantics** — treatment decisions are immutable for the remainder of the invocation after the cost-ack closes (Command line 1126).

**`finalisation-enhancements.yml` update flow (verbatim — Command lines 1130–1137)**:

After `Q-Finalisation-Enhancements` + per-item treatment sub-questions + any `spawn_now` cost-ack re-presentation resolve, the calling agent:

1. Updates `finalisation-enhancements.yml` **in place**: for each candidate, set `accepted: true | false`, `treatment: "respawn" | "queue" | "spawn_now" | "unchosen_persisted"`, and `decided_at_utc: <ISO 8601>`.
2. Writes follow-up artefacts (`follow-up-{type}-{ts}.yml`) for each accepted expensive item with `treatment: queue` or `treatment: spawn_now`.
3. Resumes the depth-0 manager with the updated file path (`finalisation_enhancements_path: "meditations/{slug}/finalisation-enhancements.yml"`).
4. The depth-0 manager:
   - Bundles accepted cheap enhancements into the first adversarial review iteration's respawn payload (Dim 13 cause `accepted_finalisation_enhancements`)
   - After the adversarial cycle completes: spawns expensive `spawn_now` agents in parallel

---

## 3. Pattern A vs Pattern B Boundaries

Source-of-truth: Command lines 34–36 (Pattern B for the overall workflow); Agent lines 17–46 (subagent escalation protocol); Agent lines 302–339 (Meditate mode patterns — extended for K6 `comprehensiveness` + K10 finalisation gate).

### 3.1 Pattern A (pre-collected before subagent spawn)

| Prompt | Why Pattern A | Source |
|--------|---------------|--------|
| `Q-Depth-Selection` | Sets `maxDepth` for the cost prompt; runs before anything else | Command lines 56–105 |
| `Q-Cost-and-Richness-Acknowledgment` (Sub-Q1 + Sub-Q2) | Single acknowledgment; mode-swap / cancel paths must not enter the tree; richness preserved across mode swap | Command lines 106–208 |
| Read-only-richness variant — all 3 triggers (expansion / additional-facet acceptance / `spawn_now` acceptance) | Same gate, locked richness; calling-agent owned at every re-fire | Command lines 210–256 |
| Theme Preflight Q1–Q5 (including Q1b repo-scan confirm) | Resolves `theming` payload; subagent must abort if payload is missing | Command lines 257–357 |
| Q1–Q5 `surprise_me` non-interactive fallback | Resolved by calling agent before spawn so subagent never re-asks | Command lines 329–331 |
| Ensemble model-pool read + per-model spawn parameters | Calling agent reads `.crux/crux-memories.json` and computes labels/counts before spawn | Command lines 853–877 |
| `comprehensiveness:` payload (post-richness K5 addition) | Resolved at the merged gate (Sub-Q1) before any subagent spawn; propagated alongside `theming:` | Command lines 361–390 |

### 3.2 Pattern B (escalated from inside the subagent tree via `needs_user_input`)

| Escalation point | Origin | Schema | Source |
|------------------|--------|--------|--------|
| **Combined Facet / Sections / Visualisations / Focus-Areas / Deep-Confirm** (replaces legacy `Q-Confirm-1` + `Q-Confirm-2`) | Depth-0 subagent after step 4 derives facets + draft suggestions; writes `facets-pending-{ts}.yml` | Single `needs_user_input` block with `prompt_inputs: { facets, sections, visualisations, additional_focus_areas, deep_confirm }`; calling agent runs ONE combined `askQuestion` with 5 sub-questions | Command lines 391–646; Agent lines 425–501 |
| **Cost re-presentation when ANY additional-facet acceptance from Sub-Q4** | Calling-agent-owned re-presentation between Pattern-B resume and step-5 spawn | Read-only-richness variant of `Q-Cost-and-Richness-Acknowledgment` (§2.4 / §2.6 `cost_change_check`) | Command lines 640–646, 648–656 |
| Deep-facet `pending-facets-*.yml` (depth_2_only / all_levels) | Any child agent at a depth requiring confirmation, batched by the depth-0 manager poll loop | File-based pending/confirmed pair; batched `needs_user_input` block | Command lines 663–731; Agent lines 591–592, 877–885 |
| **`Q-Finalisation-Enhancements`** (post-consolidation, pre-adversarial-review) | Depth-0 subagent after step 8 K10c reflection writes `finalisation-enhancements.yml` | `needs_user_input` block referencing the yml file path; calling agent runs multi-select 0–5 + per-item treatment sub-Q for expensive items + cost-ack re-presentation if any `spawn_now` selected | Command lines 1062–1124; Agent lines 681–700 |
| **Ensemble layered combined `Q-Finalisation-Enhancements`** (single combined root gate over union of per-tree + cross-model candidates) | Ensemble Aggregation agent after step 3d writes root combined `finalisation-enhancements.yml` | `needs_user_input` at ensemble root with `prompt_inputs` listing union candidates with `source: "tree:{model-subdir}" | "cross_model"` provenance labels | Command lines 1153–1184; Agent lines 1306–1328 |
| Adversarial review ambiguous `MUST_FIX` (Dim 1–11 + Dim 12 + level-conditional Dim 9 expansion) | Adversarial reviewer subagent (sub-mode of Meditate); never calls `AskQuestion` | `needs_user_input` block with **mandatory `context`** decision-guidance | Command lines 1291–1306; Agent line 728 |
| Continuation menu after meditation completes (steps 10–12) | Calling agent runs `AskQuestion` after subagent returns | Multi-select with mandatory decision-guidance prose; **K10c new option groups**: `reapply_enhancement_{id}` + `spawn_queued_{id}` | Command lines 933–986; Agent lines 769–774 |

### 3.3 Boundary rules

- **Subagents NEVER call `AskQuestion`** (Agent lines 17–20; Command line 34). The repo-wide rule from `AGENTS.md` is restated at every subagent escalation point.
- **Calling-agent (coordinator) owns every prompt** that requires interactive input — Command line 36 lists the four mandatory pre-spawn gates and the step 12 continuation menu, **plus the K10 post-consolidation `Q-Finalisation-Enhancements` gate**.
- **`needs_user_input` schema** is the single mechanism for subagent → calling-agent escalation (Agent lines 31–44). When the parent resumes, answers arrive as `answers: { <question_id>: <selected_option(s)> }`.
- **`needs_user_input` for adversarial review (and Dim 13 respawn payloads) MUST include a `context` field** with decision-guidance text — Command lines 1293–1306, restated Agent line 728.
- **Dim 13 `respawn_required: true` findings BYPASS the standard ambiguous `MUST_FIX` `needs_user_input` path** — they trigger structured deterministic respawn payloads, never user questions. The reviewer constructs the respawn YAML and triggers the report-skill respawn directly (Command lines 1370–1444).
- **K10b cheap-enhancement bundling**: when multiple cheap items are accepted in one `Q-Finalisation-Enhancements` resolution, they bundle into a SINGLE respawn payload's `accepted_finalisation_enhancements:` list (one respawn, one iteration consumed). Command line 985, agent line 720 (non-infinite-loop guarantee).

---

## 4. Subagent Contracts (currently on `crux-cursor-memory-manager`)

All subagent contracts in this section currently live on the `crux-cursor-memory-manager` agent file and run when the agent is spawned in Meditate mode (or one of its sub-functions: Adversarial Review, Ensemble Aggregation). The 20260517 decomposition spec moves these contracts to the new `crux-cursor-meditation-guide` agent and a family of `crux-skill-memory-meditation-*` skills — but the contracts themselves must remain semantically identical. **The richness spec extended steps 4 → 4b, step 8 → 8+8b, and the Ensemble Aggregation function with steps 3b → 3f. All extensions must survive decomposition.**

### 4.1 Research mode depth-0 manager (steps 1–13, with new step 4b + step 8b)

Source: Agent lines 399–748.

| Step | Action | Source |
|------|--------|--------|
| 1 | Feature Guard — verify `flags.enableMemories == "true"` | Agent line 401 |
| 2 | Create working dir `meditations/{yyyymmdd}-{topic-slug}/` (numeric suffix if collision) | Agent line 403 |
| 3 | Seed empty `facet-registry.yml` and `citations-index.yml` (Research only) | Agent line 405 |
| **4** | **Derive Top-Level Facets + Draft Suggestions Payload (cited) and confirm with the user (Pattern B)** — **EXTENDED** from 20260517 freeze §4.2 step 4. Derive 3 facets PLUS draft suggestions in a single analysis pass: `proposed_sections` (3–8 items), `proposed_visualisations` (5–10 items), `additional_focus_areas` (0–5 items, each with `recommended_treatment` hint). Write all 4 blocks to `facets-pending-{ts}.yml`, escalate via combined `needs_user_input` (§2.6), resume with full confirmed payload. **Ensemble shortcut**: if `preConfirmedFacets` + shared init-suggestions present, skip derivation/confirmation. | Agent lines 407–501 |
| **4b** | **Resume-handler: apply confirmed payload, write `init-suggestions-{ts}.yml`, reconcile additional focus areas** — **NEW per K4 + K6**. See §4.6 below for the 4-mode reconciliation logic and §4.7 for the `init-suggestions-{ts}.yml` schema. | Agent lines 503–572 |
| 5 | Spawn Explorers (3 + any accepted `additional_facet` / `additional_facet_AND_section` opt-ins). Each child receives `meditateMode`, `meditateDepth: 1`, `maxDepth`, `branchNumber`, `branchSlug`, `subfocus`, `parentSubfocus: null`, `workingDir`, `parentContext`, `siblingFacets`, `theming`, **`comprehensiveness` (MUST be present; abort with the canonical error if missing)**, `confirmDeepFacets`, `ensembleModel` (if present). | Agent lines 574–588 |
| 6 | Poll branch outputs via prefix-glob `branch-{N}-depth-1-sub-0-*.md`; deep-confirm hook globs `pending-facets-*.yml` and batches escalation | Agent lines 590–592 |
| 7 | Branch Peer Review (Research only) — spawn 3 peer reviewers in parallel | Agent line 594 |
| **8** | **Consolidate + K10c Reflection** — **EXTENDED** from 20260517 freeze §4.2 step 8. Read all 3 depth-1 branch files + all 3 peer-review files + `citations-index.yml`. Synthesize into `consolidation.md` following Subject-Matter Focus. **K10c — In-pass reflection (runs in the SAME LLM pass — no extra file read)**: after writing `consolidation.md`, score candidate enhancements per impact × insight-value rubric (§4.8), select top 5 by composite_score, write `finalisation-enhancements.yml`, return K10 `needs_user_input` block. Do NOT return to calling agent for step 9+ yet — the K10 `needs_user_input` IS the mechanism for `Q-Finalisation-Enhancements` (§2.8). | Agent lines 596–700 |
| **8b** | **Resume-handler for accepted enhancements (K10b)** — **NEW**. Re-read updated `finalisation-enhancements.yml`. For each `accepted: true, treatment: "respawn"` (cheap): build entry for first adversarial-review iteration's respawn payload. For each `accepted: true, treatment: "queue"` (expensive): write `follow-up-{type}-{ts}.yml`. For each `accepted: true, treatment: "spawn_now"` (expensive): accumulate in `pending_spawn_now: [...]` for step 13 return. **Non-infinite-loop guarantee**: the `accepted_finalisation_enhancements` respawn cause fires AT MOST ONCE per meditation. | Agent lines 702–722 |
| 9 | Update `facets.md` with Branch & Leaf Index (glob actual filenames; appends new top-level artefact rows `[Init suggestions](init-suggestions-{ts}.yml)` AND `[Finalisation enhancements](finalisation-enhancements.yml)` AND any `follow-up-{type}-{ts}.yml` rows) | Agent line 724 |
| 10 | Adversarial review-and-fix cycle (cap 3 iterations); **13 dimensions now** (Dim 12 + Dim 13 added per K9); `MUST_FIX` escalations via `needs_user_input` with mandatory `context`; **Dim 13 `respawn_required: true` triggers Report-Skill Respawn Protocol** (see §6.10) | Agent lines 726–730 |
| 11 | Re-run step 9 only if verdict is `PASS` or `PASS_WITH_ADVISORIES` (reviewer may have rewritten files) | Agent line 732 |
| 12 | Generate mandatory paired HTML + PDF reports per `Report Generation — MANDATORY` — **report skill now reads `comprehensiveness:` payload + `init-suggestions-{ts}.yml` + `finalisation-enhancements.yml` for cheap accept-policy rendering** (skip on `ESCALATE`) | Agent lines 734–744 |
| 12b | Write `retrospective-{ts}.md` (always written, including on `ESCALATE`) — **unchanged** | Agent line 746 |
| 13 | Return to calling agent: workingDir, `facets.md`, `consolidation.md` (text + path), `retrospective-{ts}.md`, report pair (if generated), every `review-pre-report-*-iter-*.md`. **NEW (K10b)**: also return `pending_spawn_now: [...]` list so calling agent can spawn expensive `spawn_now` agents immediately after adversarial review completes. On `ESCALATE` return everything except report paths plus structured summary of unresolved `MUST_FIX` findings. | Agent line 748 |

### 4.2 Research mode Phases A–G (per child agent at depth 1 through `maxDepth - 1`)

Source: Agent lines 776–855.

**Phases A–G are unchanged structurally from 20260517 freeze §4.1**. The only additions (per K5 + K6):

- Every spawn must include `comprehensiveness:` in the spawn prompt; child aborts with the canonical error if missing (Agent lines 826–830).
- At leaf depth (Research mode), at `comprehensiveness.level ∈ {detailed, exhaustive}` (`depth3_leaf_inclusion = verbatim_quotes`), Phase B output for leaf agents MUST include verbatim quoted passages from cited sources in `## Discoveries`. At `compact` or `default` (`depth3_leaf_inclusion = summary`), leaf agents write a summary only (today's existing behaviour). (Agent line 861)
- The `## Discoveries` section length MUST stay within `comprehensiveness.minima.section_length_budget_tokens.per_facet`. (Agent line 862)
- At `exhaustive` in Research mode: citation density escalates to `per_finding_table` — every finding table must include a citation column. (Agent line 863)

All other Phase A/B/C/D/E/F/G semantics — including deep-confirmation hook, registry lock, child spawn parameters, prefix-glob polling, citation validation with respawn on failure, bottom-up rewrite, Phase G promotion — are byte-identical to 20260517 freeze §4.1.

### 4.3 Quick mode 6-step protocol (per child agent at depth < `maxDepth`)

Source: Agent lines 866–909.

**Unchanged structurally from 20260517 freeze §4.3.** Same additions as Research:

- Step 3 spawn must include `comprehensiveness:`; child aborts with canonical error if missing (Agent lines 890–894).
- Leaf-depth comprehensiveness honouring identical to Research (verbatim quotes at `detailed`+; section_length_budget cap applies) — Agent line 909.
- Citation validation remains `warn_only` at every level — parent does NOT respawn (K7 mode-driven rule).

### 4.4 Quick vs Research differences table

Source: Agent lines 911–921.

**Unchanged from 20260517 freeze §4.4.**

### 4.5 Ensemble Aggregation function (extended with K10 layered cadence steps 3b–3f)

Source: Agent lines 1189–1349.

**Existing 5-step workflow (steps 1, 2, 3, 4, 5) is preserved from 20260517 freeze §4.5.** Three K10 steps are inserted between step 3 (write `cross-model-synthesis.md`) and step 4 (generate ensemble report):

**Step 3b — Read per-tree `finalisation-enhancements.yml` files** (Agent lines 1215–1246):

Each tree's depth-0 manager wrote `{model-subdir}/finalisation-enhancements.yml` with `source_tree: "{model-subdir}"` and `surfaced_to_root: null` placeholder. Aggregator reads all per-tree YAMLs. Per-tree YAML schema includes `source_tree` (required for root-level provenance labelling) and `surfaced_to_root: null` placeholder. **NO per-tree askQuestion fires** — per-tree YAMLs are write-only at the per-tree level (OQ #10 resolved as "both layered" with single combined root gate).

**Step 3c — K10 root cross-model reflection (in the SAME LLM pass as `cross-model-synthesis.md` — no extra file read)** (Agent lines 1248–1254):

After writing `cross-model-synthesis.md`, run a SECOND reflection pass over: (a) all per-tree `consolidation.md` files (already in context from step 1); (b) all per-tree `finalisation-enhancements.yml` files (from step 3b); (c) `cross-model-synthesis.md` itself (just written). Produce up to **5 cross-model candidates** emergent from looking across all trees together. Rank high for:

1. **Cross-tree convergence**: ≥2 trees independently surfaced the same enhancement type (convergence signal). Apply `insight_value_score ≥ 7` calibration when convergence is explicit.
2. **Cross-model-only patterns**: visible only across models (e.g. a divergence between two trees suggests an `extracted_spec` one tree didn't see).
3. **Cross-model-synthesis-side opportunities**: `cross_branch_synthesis_section` is naturally cross-tree and often a high-value candidate.

Each cross-model candidate carries `source: "cross_model"`. Use the same impact × insight-value rubric (1–10 per axis) with `insight_value_score ≥ 7` calibration boost for convergent findings.

**Step 3d — Root combined YAML write** (Agent lines 1256–1304):

Write `{ensembleWorkingDir}/finalisation-enhancements.yml` (no `{model-subdir}` segment) containing both `cross_model_candidates: [...]` (5 ranked candidates from the aggregator's reflection) AND a denormalised `union_candidates: [...]` listing the top-N (capped at 5) by composite score drawn from `(per_tree × N) + (cross_model × 5)`. Each `union_candidates[]` entry carries `source: "tree:{model-subdir}" | "cross_model"` so the calling agent's askQuestion can label provenance and downstream report targeting can resolve to the correct report. After writing the root YAML, **write-back `surfaced_to_root` annotations to every per-tree YAML**: for each per-tree candidate, set `surfaced_to_root: true` if the candidate's `id` appears in `union_candidates`; set `surfaced_to_root: false` otherwise. **This is the ONLY mutation the aggregator makes to per-tree YAMLs.**

**Step 3e — Return K10 `needs_user_input` block (single combined root gate)** (Agent lines 1306–1328):

The aggregator returns a single combined `needs_user_input` block to the calling agent. Each option label includes provenance: `{title} [{cost_class}] ({source-label}) — composite={N}`. Source labels: `"cross-model"` or `"from tree: {model-label}"`. **Recommended posture** (per spec K10a / OQ #10 resolution): single combined root gate so the user is not interrupted N times; alternative (per-tree gates) is documented and rejected because it serialises trees, multiplies user prompts, and prevents cross-model insight from being visible at decision time.

**Model-label resolution fallback**: if `cruxMemories.meditate.modelPool` no longer contains the `{model-subdir}` slug at continuation time (model retired), label falls back to `"Unknown model ({model-subdir})"` (Command line 1182).

**Step 3f — K10 ensemble resume-handler for accepted enhancements** (Agent lines 1330–1337):

Re-read updated root `finalisation-enhancements.yml`. For each accepted `union_candidates` entry:

- `accepted: true, treatment: "respawn"` (cheap), `source: "cross_model"`: bundle into the **ensemble synthesis report**'s first adversarial-review iteration respawn payload.
- `accepted: true, treatment: "respawn"` (cheap), `source: "tree:{model-subdir}"`: bundle into the **per-tree `{model-subdir}` report**'s first adversarial-review iteration respawn payload.
- `accepted: true, treatment: "queue"` (expensive): write `follow-up-{type}-{ts}.yml` next to appropriate location: per-tree consolidation directory for tree-sourced; ensemble root for cross-model-sourced. Do NOT spawn agents.
- `accepted: true, treatment: "spawn_now"` (expensive): defer spawning until AFTER the corresponding adversarial-review cycle completes. Track in `pending_spawn_now: [...]` per target (per-tree vs ensemble).

**Non-infinite-loop guarantee (ensemble layered cadence)** — Agent line 1337: per-tree reflections happen exactly once per tree (bounded by `modelPool` size = constant); root cross-model reflection happens exactly once; single combined root gate fires once per invocation. Per-tree adversarial review cycles each have their own ≤3 cap (unchanged); cross-model adversarial review has its own ≤3 cap. Total: at most `N + 1` reflection writes + 1 user gate + `(N + 1) × 2 useful respawns × 1 report-skill run each` = `O(N)` total bounded work. Cannot infinite-loop.

**Step 5 — Return to calling agent** (Agent line 1349): unchanged from 20260517 freeze §4.5 except extended with `pending_spawn_now: [...]` list structured as `[{source: "cross_model"|"tree:{model-subdir}", type: "...", follow_up_file: "..."}]`.

### 4.6 4-mode `additional_focus_areas[]` reconciliation (step 4b write side — verbatim post-W1b canonical)

Source: Agent lines 505–514. **This is the canonical write-side spec post the 20260524 W1 + W1b post-execution fixes** — the canonical field name is `additional_focus_areas[]` (array) with a per-item `treatment:` filter; the divergent legacy field names (`additional_focus_areas_skipped`, `additional_focus_areas_accepted`) are dead and **must NOT** be re-introduced. Pinned by `evals/test_q_meditate.py::TestMeditateInitSuggestions::test_four_opt_in_modes_documented` and the post-execution verification grep at `execution-report-meditate-richness-20260523.md:177`.

For each focus area in `additional_focus_areas_decisions`:

- **`skip`** → record as an entry in `additional_focus_areas[]` in the YAML with `treatment: "skip"` (canonical array is a single per-decision array; `resulting_section_id` and `resulting_branch_index` stay `null`). No facet, no section.
- **`additional_facet`** → append a new entry to the confirmed facet set (becomes Branch 4 / 5 / 6 …, sequenced after Branch 3 in registration order; slug derived per existing facet-slug rules). Append to `facet-registry.yml` (Research mode) and `facets.md`. The new branch spawns alongside the original 3 in step 5. **No dedicated report section beyond what the new branch's natural output produces** (at `compact`/`default` richness, dim #8 = `consolidation_only`/`branch_summary` → contributions appear in consolidation prose only; at `detailed`/`exhaustive`, dim #8 = `per_leaf_detail` → a standard per-branch section appears under the auto-derived facet title). Set `new_branch_index` to the next branch number.
- **`report_section_only`** → record as an entry in `additional_focus_areas[]` with `treatment: "report_section_only"` and `custom_report_section_title` = the focus-area title (or user-supplied title); populate `resulting_section_id` per the schema invariant. **Do NOT add a facet.** The report skill reads `init-suggestions-{ts}.yml` and must include a section by that exact title; content is sourced from across-branch findings + the supplied rationale.
- **`additional_facet_AND_section`** → both effects: new facet (per `additional_facet` semantics above) AND record a confirmed report section title (per `report_section_only` semantics). Populate both `new_branch_index` and `custom_report_section_title` (from the calling agent's follow-up text input).

**Cost-ack re-presentation rule** (Agent line 515): if ANY focus-area decision is `additional_facet` OR `additional_facet_AND_section`, the calling agent (not this subagent) fires the read-only-richness variant of `Q-Cost-and-Richness-Acknowledgment` BEFORE this subagent resumes step 5. This subagent only proceeds to step 5 after the calling agent confirms re-acknowledgment (passed as `cost_reack_confirmed: true` in the resume payload). If the user cancels at re-presentation, abort: do NOT write `init-suggestions-{ts}.yml` and do NOT spawn children.

### 4.7 `init-suggestions-{ts}.yml` schema (write side, verbatim)

Source: Agent lines 517–566 (write-side schema with post-W1b canonical field name).

**Filename**: `meditations/{yyyymmdd}-{topic-slug}/init-suggestions-{ts}.yml`. Written by the depth-0 manager during step 4b resume (after the combined Pattern-B askQuestion resolves; after any cost-ack re-presentation is acknowledged).

**Schema (verbatim)**:

```yaml
---
generated_utc: "{utc-timestamp}"
topic_slug: "{topic-slug}"
seed_exploration_ts: "{ts}"
confirmed_at_utc: "{utc-timestamp}"
comprehensiveness_level: "{level}"      # echoed from comprehensiveness.level
audit:
  draft_count:
    sections: {N}
    visualisations: {N}
    additional_focus_areas: {N}
  confirmed_count:
    sections: {N}
    visualisations: {N}
    additional_focus_areas:
      skip: {N}
      additional_facet: {N}
      report_section_only: {N}
      additional_facet_AND_section: {N}
---
confirmed_sections:
  - id: "section-{slug}"
    title: "{title}"
    source: "depth_0_seed_exploration"   # or "additional_focus_area_report_section_only" or "additional_focus_area_AND_section"
    rationale: "{rationale}"
    source_signals:
      - "[chat: turn-N]"
      - "[memory: {memory-title}]"
    user_modified: false
confirmed_visualisations:
  - id: "viz-{slug}"
    type: "{visualisation-type-enum}"
    rationale: "{rationale}"
    what_it_would_show: "{1-2 sentences}"
    source_signals:
      - "[file: path/to/file.ts:N-N]"
additional_focus_areas:
  - id: "focus-{slug}"
    title: "{focus-area-title}"
    rationale: "{rationale}"
    source_signals: [...]
    treatment: "skip | additional_facet | report_section_only | additional_facet_AND_section"
    resulting_section_id: null | "section-{slug}"     # set when treatment ∈ {report_section_only, additional_facet_AND_section}
    resulting_branch_index: null | {N}                # set when treatment ∈ {additional_facet, additional_facet_AND_section}
    custom_report_section_title: null | "{title}"     # set when treatment == additional_facet_AND_section
    decided_at_utc: "{utc-timestamp}"
```

**Schema invariants (verbatim — Agent line 568)**:

- `resulting_section_id` is set iff `treatment ∈ {report_section_only, additional_facet_AND_section}`
- `resulting_branch_index` is set iff `treatment ∈ {additional_facet, additional_facet_AND_section}`
- `custom_report_section_title` is set iff `treatment == additional_facet_AND_section`
- At `compact` / `default` richness, `additional_facet`-only opt-ins produce `resulting_branch_index` but **NO** `resulting_section_id` (K4 carve-out per execution-report W1b)
- The `confirmed_sections` array includes entries from depth-0 seed exploration AND from accepted `report_section_only` / `additional_facet_AND_section` focus-area decisions

### 4.8 K10c reflection rubric + candidate type catalogue (impact × insight-value)

Source: Agent lines 609–642.

**Rubric (1–10 each axis)** — Agent lines 609–619:

- **`impact_score` (1–10)** — how much does this enhancement enable the reader to act or decide?
  - `9` = Enhancement directly enables a high-stakes decision. Example: an `executive_summary` for a vendor-comparison meditation that unblocks a board presentation; without it, the reader cannot make the decision the meditation was commissioned to inform.
  - `5` = Enhancement clarifies reading order but doesn't change recommended action. Example: a `glossary` that helps a non-domain reader skim the report faster, but every domain reader could already act on the existing content.
  - `2` = Cosmetic improvement only. Example: a `reader_persona_tldrs` for a 3-page meditation that the existing introduction already covers; the persona TL;DRs would be redundant phrasings.
- **`insight_value_score` (1–10)** — how much new substantive insight does this enhancement surface?
  - `9` = Surfaces a cross-branch synthesis no individual branch made visible. Example: a `cross_branch_synthesis_section` that connects an architectural choice surfaced in Branch 1 with a cost-of-ownership pattern surfaced in Branch 3 — neither branch made the connection but the synthesis is decision-relevant.
  - `5` = Re-organises content from one branch into a more readable form. Example: a `risks_section` that gathers risk findings already prominent in Branch 2 into a single section with a taxonomy axis. The reader gains organisational benefit but no new substantive insight.
  - `2` = Paraphrases content already prominent in existing sections. Example: an `action_plan` whose items each match one-to-one with the existing "Recommended Next Steps" section bullets, with no horizon-specific differentiation.

**Scoring rules** — Agent lines 620–625:

- Compute `composite_score = impact_score × insight_value_score` (multiplicative). If `cruxMemories.meditate.finalisationEnhancements.weights` configured (or `formula: "weighted_sum"`), use weighted-sum formula instead.
- Filter out any candidate whose `impact_score < minimum_impact_threshold` (default 6).
- Select top 5 by `composite_score` descending. Tie-break: prefer `cost_class: "cheap"` over `"expensive"`.
- Graceful degradation per §2.8.

**Candidate type catalogue — 11 types** (Agent lines 627–642):

**Cheap types (7) — rendered in the report via respawn (K10b Per-Cheap-Type Rendering Contract in §6.9 below)**:

| Type | Payload shape (subtask 02 / agent line 630–636) |
|------|-------------------------------------------------|
| `executive_summary` | `{ target_persona: "leadership"\|"engineer"\|"product"\|"researcher", max_paragraphs: int, anchor_findings: ["[research: slug]", ...] }` |
| `action_plan` | `{ horizons: ["7d", "30d", "quarter"], items_per_horizon: int, anchor_findings: [...] }` |
| `risks_section` | `{ risk_taxonomy_axes: ["likelihood", "impact", "detection_difficulty"], anchor_findings: [...] }` |
| `glossary` | `{ term_count_estimate: int, anchor_branches: ["branch-1", ...] }` |
| `decision_tree_infographic` | `{ root_decision: "...", depth: int, anchor_findings: [...] }` |
| `reader_persona_tldrs` | `{ personas: ["leadership", "engineer", "product"], paragraphs_per_persona: int }` |
| `cross_branch_synthesis_section` | `{ axes: ["convergent", "divergent"], anchor_findings_per_axis: { convergent: [...], divergent: [...] } }` |

**Expensive types (4) — spawn follow-up work (queue default; `spawn_now` opt-in)**:

| Type | Payload shape (Agent lines 638–642) |
|------|--------------------------------------|
| `additional_meditation` | `{ proposed_topic: "...", proposed_facet_seed: ["facet-1", "facet-2", "facet-3"], recommended_depth: 1\|2\|3, recommended_mode: "research"\|"quick" }` |
| `extracted_spec` | `{ proposed_slug: "{yyyymmdd}-{slug}", overview: "...", candidate_subtasks: [{title: "...", agent: "{subagent-id}"}], spec_template: "{relative-path}" }` |
| `extracted_memories` | `{ candidates: [{title: "...", type: "learning"\|"redflag"\|"core"\|"idea"\|"goal", body_summary: "...", source_signals: [...]}] }` |
| `expanded_branch` | `{ target_branch_index: int, recommended_new_depth: 1\|2\|3, facet_emphasis_override: "...", recommended_mode: "research"\|"quick" }` |

**`finalisation-enhancements.yml` schema (single-model variant; verbatim Agent lines 646–677)**:

```yaml
---
generated_utc: "{utc-timestamp}"
topic_slug: "{topic-slug}"
mode: "research"      # or "quick"
ensemble: false       # true → see ensemble layered cadence section
rubric:
  impact_score_max: 10
  insight_value_score_max: 10
  minimum_impact_threshold: 6
  weights: { impact: 1.0, insight_value: 1.0 }
  formula: "product"  # or "weighted_sum" if configured
degradation_reason: null   # null | "fewer than 5 candidates met threshold" | "no high-quality candidates surfaced"
---
candidates:
  - id: "{type}-{ts}"
    type: "{one-of-11-types}"
    cost_class: "cheap"    # or "expensive"
    title: "{title}"
    description: "{1-sentence description}"
    impact_score: {N}
    insight_value_score: {N}
    composite_score: {N}
    source_signals:
      - "[child: branch-N-depth-D-sub-S-{slug}-{ts}.md]"
      - "[memory: {memory-title}]"
    payload: { ... }        # type-specific shape per catalogue above
    accepted: null          # filled by calling agent: true | false
    treatment: null         # filled by calling agent: "respawn" | "queue" | "spawn_now" | "unchosen_persisted"
    decided_at_utc: null    # filled by calling agent
  # ... up to 5 candidates
```

**Ensemble per-tree YAML schema** (Agent lines 1217–1244) and **ensemble root combined YAML schema** with `cross_model_candidates` + `union_candidates` (Agent lines 1256–1304) reproduced in §5.2 below alongside the canonical filename table.

### 4.9 Adversarial Review function (sub-mode of Meditate) — extended to 13 dimensions

Source: Command lines 1187–1447; Agent lines 726–730, 1150 (design principle restatement).

**Reviewer agent**: Command lines 1191–1199 — unchanged from 20260517 freeze §4.6 (fresh `crux-cursor-memory-manager` subagent in **Adversarial Review** function, clean context, inputs `meditateMode`, `reviewerIteration` (1, 2, or 3), `workingDir`, `theming`, `priorReviewPath`).

**Editable files**: unchanged from 20260517 freeze §4.6 (Command lines 1201–1205).

**13 review dimensions** — Command lines 1207–1250 (dims 1–11 verbatim from 20260517 freeze §4.6 plus two new dims):

1. **Citation integrity** — unchanged from 20260517 freeze §4.6 dim 1.
2. **Cross-file consistency** — unchanged.
3. **Substance and sparseness** — unchanged.
4. **Slop detection** — unchanged.
5. **Calibration** — unchanged.
6. **Index integrity** — unchanged.
7. **Frontmatter validity** — unchanged.
8. **Anti-homogenization drift in prose** — unchanged.
9. **Peer-review thoroughness** (Research mode only) — **LEVEL-CONDITIONAL per K9** (Command lines 1219–1227):
   - At `peer_review_surfacing ∈ {consolidation_only}` (`compact` and `default`): peer-review files must exist for each branch and must each contain at least one identified reinforcement, contradiction, and gap. Verify peer-review reach into the consolidation prose.
   - At `peer_review_surfacing ∈ {named_section}` (`detailed`): in addition to the above, verify that the report contains a dedicated named section (e.g. "Quality Review" or "Cross-Cutting Reinforcements & Contradictions") surfacing the peer-review findings cross-cutting all branches.
   - At `peer_review_surfacing ∈ {per_branch_dedicated}` (`exhaustive`): in addition to the above, verify ONE named section per branch surfacing that branch's peer-review reinforcements / contradictions / gaps.
   - **Severity**: `MUST_FIX` (in-place rewrite at all levels — does NOT trigger respawn even at `per_branch_dedicated`, because adding a named section is a presentation-layer fix). **N/A in Quick mode** (no peer-review files exist).
10. **Ready-for-report** — unchanged from 20260517 freeze §4.6 dim 10.
11. **Subject-matter focus** — unchanged from 20260517 freeze §4.6 dim 11.
12. **Comprehensiveness fidelity** — **NEW per K9 + Requirement 8** (Command lines 1231–1239):
    - Chart count ≥ `comprehensiveness.minima.charts.count`.
    - Infographic count ≥ `comprehensiveness.minima.infographics.count`.
    - Calculator count ≥ `comprehensiveness.minima.calculators.count` (when topic surfaces a quantifiable trade-off).
    - Per-branch section depth matches `comprehensiveness.per_branch_section_depth` (e.g. at `detailed`+ verify each confirmed facet has a dedicated per-branch section; at `compact`/`default` verify per-branch content folds into consolidation prose only).
    - Peer-review surfacing matches `comprehensiveness.peer_review_surfacing` (e.g. at `detailed` verify a `named_section` exists for reinforcements/contradictions/gaps; at `per_branch_dedicated` verify one per branch).
    - `depth3_leaf_inclusion` mode honoured (e.g. at `verbatim_quotes` verify ≥1 depth-3 leaf quote with citation appears per branch).
    - **Severity**: `MUST_FIX` (in-place rewrite — does NOT trigger respawn). The reviewer can add missing charts / infographics / sections inline by rewriting the report HTML — these are presentation-layer fixes that don't require regenerating the full report.
13. **Init-suggestion AND finalisation-enhancement honour** — **NEW per K9 + K10b + Requirement 8** (Command lines 1241–1250):
    - For each `confirmed_sections[i]`: a section with that exact title must exist in the rendered HTML, AND its body must be non-empty (>1 paragraph or >100 words; a heading-only stub counts as missing). Auto-resolved=true means an accepted finalisation enhancement (cheap, respawned) has overlapping title — flag the section as auto-resolved AND verify the enhancement-driven section appears.
    - For each `confirmed_visualisations[i]`: a visualisation of that exact type must be rendered with non-empty data (a container with no data series counts as missing).
    - For each `finalisation-enhancements.yml.candidates[i]` with `accepted: true, treatment: respawn`: a section / chart / infographic / etc. matching the type's rendering contract (see the K10b Per-Cheap-Type Rendering Contract in §6.9) must appear in the report at its contractual location.
    - **Ensemble layered audit**: at ensemble, audit each accepted enhancement against the correct report — per-tree-sourced enhancements (from candidates with `source: "tree:{model-subdir}"`) are audited against the per-tree report; cross-model-sourced enhancements (from candidates with `source: "cross_model"`) are audited against the cross-model synthesis report. A missing accepted enhancement in the wrong report is NOT a finding; it is a finding only when the K10 Ensemble Respawn Targeting rule says it should be in that report.
    - **Severity**: `MUST_FIX` AND `respawn_required: true` — bypasses standard in-place fix flow per the Report-Skill Respawn Protocol (§6.10 / Command lines 1368–1446). The reviewer constructs the structured respawn payload and triggers a report-skill respawn rather than rewriting inline. Iteration budget shares the existing ≤3 cap.

**Severity classification** — Command lines 1254–1260: unchanged from 20260517 freeze §4.6 (`MUST_FIX` / `SHOULD_FIX` / `ADVISORY`).

**Quick mode relaxations** — Command line 1260: unchanged from 20260517 freeze §4.6 (citation integrity → `SHOULD_FIX`; peer-review thoroughness N/A).

**Iteration loop (cap 3) — UPDATED to handle Dim 13 respawn branch** (verbatim Command lines 1264–1287):

```
iteration = 1
while iteration <= 3:
    spawn reviewer with reviewerIteration=iteration (fresh subagent each iteration)
    reviewer writes review-pre-report-{ts}-iter-{iteration}.md
    if verdict in {PASS, PASS_WITH_ADVISORIES}: break
    if reviewer escalated MUST_FIX via needs_user_input (Pattern B):
        # Standard ambiguous-MUST_FIX path — Dim 13 respawn_required findings BYPASS this
        calling agent runs askQuestion with reviewer-supplied decision-guidance,
        then resumes the reviewer with the user's resolutions; reviewer applies
        those resolutions, finalises the iteration document, and the loop continues.
    if any finding has respawn_required: true (Dim 13 — init-suggestion / enhancement honour):
        # 1. Apply all Dim 1–11 in-place fixes first (reviewer already did these in same pass)
        # 2. Construct respawn payload (see Report-Skill Respawn Protocol below)
        # 3. Respawn the report-generation skill with fresh timestamp
        TS_new=$(date -u +%Y%m%d%H%M%S)
        # Prior HTML/PDF pair preserved on disk; respawn writes new pair at TS_new
        invoke report-generation skill with respawn_payload (iteration N consumed)
        # Next iteration (N+1) spawns a fresh reviewer to re-review the regenerated report
    iteration += 1

if iteration > 3 and MUST_FIX still unresolved:
    verdict = ESCALATE
    abort report generation (sub-step 8.8 skipped)
    surface unresolved findings to the calling agent in sub-step 8.9 instead of report paths
```

**Cap = 3 iterations** shared between standard review cycles and respawn cycles — no separate respawn budget. **Maximum useful respawns per meditation = 2** (Command line 1289).

**`MUST_FIX` `needs_user_input` schema (verbatim, with mandatory `context`)** — Command lines 1297–1306: unchanged from 20260517 freeze §4.6.

**Review document format** — Command lines 1308–1357: unchanged from 20260517 freeze §4.6 (filename `review-pre-report-{ts}-iter-{N}.md`; frontmatter + verdict + summary + MUST_FIX / SHOULD_FIX / ADVISORY findings + iteration log + carry-forward sections).

**Quick mode treatment** — Command lines 1359–1366: unchanged from 20260517 freeze §4.6.

---

## 5. Coordination Conventions

Source-of-truth: the canonical reference lives in `.cursor/agents/crux-cursor-memory-manager.md` **Coordination Conventions** subsection (Agent lines 345–397) and is mirrored character-for-character in `.cursor/commands/crux-meditate.md` (Command lines 740–784). Placeholders are defined exactly once in the agent file (Agent lines 370–375).

### 5.1 Artefact filename table (verbatim post-richness — 18 rows, Agent lines 349–368 / Command lines 744–762)

| Artefact | Filename pattern | Notes |
|----------|------------------|-------|
| Top-level facets (initial, pre-confirmation) | `facets-pending-{ts}.yml` | Deleted after the user confirms via **combined Pattern-B askQuestion**; schema extended to carry all 4 blocks (facets + sections + visualisations + additional_focus_areas) |
| Top-level facets (final, post-confirmation) | `facets.md` | Single navigational entry point; updated post-consolidation with the Branch & Leaf Index |
| **Init suggestions (confirmed payload)** — NEW per K6 | `init-suggestions-{ts}.yml` | Written by depth-0 manager during step 4b resume (after combined Pattern-B askQuestion resolves); schema: `confirmed_sections` + `confirmed_visualisations` + `additional_focus_areas` blocks; read by report-generation contract (Requirement 6) and adversarial reviewer Dim 13; linked from `facets.md` Branch & Leaf Index `## Top-level artifacts` |
| Branch (depth 1, 2, 3) | `branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md` | `D` ∈ {1,2,3}; `S = 0` at depth 1, `S` ∈ {1,2,3} at depth 2, `S` ∈ {1,...,9} at depth 3 |
| Branch (intermediate, Phase B working draft) | `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}-findings.md` | Research mode only; deleted after Phase G promotion |
| Peer review (Research mode) | `branch-{N}-peer-review-{branchSlug}-{ts}.md` | One per branch |
| Pending deep-facet confirmation request | `pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml` | Only when `confirmDeepFacets ≠ none`; `D` is the **parent** agent's depth |
| Confirmed deep-facet response | `confirmed-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml` | Same path-id and `{ts}` as the pending file |
| Adversarial review iteration | `review-pre-report-{ts}-iter-{N}.md` | `N` ∈ {1, 2, 3}; iteration cap |
| **Finalisation enhancements (single-model)** — NEW per K10c | `finalisation-enhancements.yml` | Written by depth-0 manager during step 8 consolidation reflection (in-pass, no extra read); top-5 ranked candidates; calling agent updates in place with `accepted` / `treatment` / `decided_at_utc` after `Q-Finalisation-Enhancements` resolves; linked from `facets.md` Branch & Leaf Index `## Top-level artifacts` |
| **Finalisation enhancements (ensemble per-tree)** — NEW per K10a layered cadence | `{model-subdir}/finalisation-enhancements.yml` | Written by per-tree depth-0 consolidation manager before returning to ensemble aggregator; carries `source_tree:` + `surfaced_to_root: null` placeholder (aggregator fills); **NO per-tree askQuestion fires** |
| **Follow-up artefact: additional meditation (queued/spawn-now expensive item)** — NEW per K10b | `follow-up-meditation-{ts}.yml` | Written by calling agent after `Q-Finalisation-Enhancements` resolves for `additional_meditation` items with `treatment ∈ {queue, spawn_now}`; `{ts}` is the calling-agent write timestamp |
| **Follow-up artefact: extracted spec** — NEW per K10b | `follow-up-spec-{ts}.yml` | Written by calling agent for `extracted_spec` items with `treatment ∈ {queue, spawn_now}` |
| **Follow-up artefact: extracted memories** — NEW per K10b | `follow-up-memories-{ts}.yml` | Written by calling agent for `extracted_memories` items with `treatment ∈ {queue, spawn_now}` |
| **Follow-up artefact: expanded branch** — NEW per K10b | `follow-up-expansion-{ts}.yml` | Written by calling agent for `expanded_branch` items with `treatment ∈ {queue, spawn_now}` |
| Process retrospective | `retrospective-{ts}.md` | One per meditation; process analysis separate from subject-matter outputs |
| Report HTML | `report-{topic-slug}-{ts}.html` | Shares `{ts}` with PDF pair |
| Report PDF | `report-{topic-slug}-{ts}.pdf` | Shares `{ts}` with HTML pair |

### 5.2 Placeholders (defined once in Agent lines 370–375)

Unchanged from 20260517 freeze §5.2:

- `{topic-slug}` — slug component of working-directory name (extract everything after leading `yyyymmdd-`).
- `{slug}` (branch filenames) — kebab-case slug derived for that branch (depth 1) or subfocus (depth 2/3); max 40 chars; lowercase; alphanumerics + hyphens only; stop-words stripped; most meaningful 3–6 words.
- `{ts}` — UTC timestamp `yyyymmddHHMMSS` captured at write time: `date -u +%Y%m%d%H%M%S`.
- `{N}`, `{D}`, `{S}` — zero-padded numerals used as written above (`branch-1`, not `branch-01`).

### 5.3 Prefix-glob polling rule (verbatim, both files mirror)

Source: Agent lines 377–395; Command lines 764–782.

**Unchanged from 20260517 freeze §5.3** — Branch-output polls, peer-review polls, report pair polls, pending deep-facet confirmation polls all preserved verbatim.

**Never hard-code these names** (Agent line 397; Command line 784): unchanged from 20260517 freeze §5.3.

### 5.4 Facet registry lock semantics (Research mode only)

Source: Agent lines 923–969.

**Unchanged from 20260517 freeze §5.4** — Schema, `mkdir`-based lock-and-append protocol (60s timeout), orphan recovery rule all byte-identical.

### 5.5 Citations index format (Research mode only)

Source: Agent lines 971–1006.

**Unchanged from 20260517 freeze §5.5** — Inline citation markers, `citations-index.yml` schema, Research-mode parent strict-validation + respawn (2 retries), Quick-mode warn-only all byte-identical.

### 5.6 Peer review file spec (Research mode only)

Source: Agent lines 1008–1036.

**Unchanged from 20260517 freeze §5.6** — Filename, frontmatter, required `## Reinforcements` / `## Contradictions` / `## Gaps` / `## New Evidence` / `## Citations` sections all byte-identical. The richness spec did not change the peer-review file itself; it changed how peer-review content surfaces in the **report** (via the new `peer_review_surfacing` dimension — see §6.7).

### 5.7 Retrospective template (`retrospective-{ts}.md`)

Source: Command lines 1470–1537.

**Unchanged from 20260517 freeze §5.7** — Filename, frontmatter, required sections (`## Process Retrospective`, `### Summary Statistics`, `### What Went Well`, `### What Could Be Improved`, `### Structural Observations`, `### Recommendations for Future Meditations`) all byte-identical. Always written, including on `ESCALATE`.

### 5.8 Branch & Leaf Index template (appended to `facets.md`)

Source: Command lines 988–1059; Agent line 724.

**Existing 20260517 freeze §5.8 template preserved verbatim; the richness spec ADDS 5 new top-level artefact link rows to the `## Top-level artifacts` block:**

- `[Init suggestions](init-suggestions-{ts}.yml)` — new per K6
- `[Finalisation enhancements](finalisation-enhancements.yml)` _(only when written by depth-0 consolidation reflection)_ — new per K10c
- `Follow-up artefacts (one entry per `follow-up-{type}-{ts}.yml` discovered):`
  - `[Follow-up: additional meditation — {title}](follow-up-meditation-{ts}.yml)` _(only if present; treatment: queue or spawn_now)_
  - `[Follow-up: extracted spec — {title}](follow-up-spec-{ts}.yml)` _(only if present)_
  - `[Follow-up: extracted memories — {title}](follow-up-memories-{ts}.yml)` _(only if present)_
  - `[Follow-up: expanded branch — {title}](follow-up-expansion-{ts}.yml)` _(only if present)_

**All other rows** (Consolidation / Process Retrospective / Report HTML+PDF / Adversarial review iterations / Facet confirmation trail / Facet registry / Citations index) preserved verbatim from 20260517 freeze §5.8.

**Conventions** (Command lines 1052–1059) — unchanged from 20260517 freeze §5.8 except:

- Quick mode produces the same index minus per-branch "Peer review" lines and the two Research-only registry/index lines (unchanged).
- When `ESCALATE`: report HTML/PDF lines omitted; every `review-pre-report-*-iter-*.md` still linked (unchanged).

### 5.9 Ensemble working directory structure (verbatim — Command lines 1985–2006)

**Unchanged structurally from 20260517 freeze §6.7** — per-model subdirectories `model-{label-slug}/` plus root `facets.md` + `cross-model-synthesis.md` + `ensemble-report-{topic-slug}-{ts}.html` / `.pdf`. **The richness spec adds**: each per-model subdirectory now also contains `finalisation-enhancements.yml` (per K10 layered cadence), and the ensemble root now also contains `finalisation-enhancements.yml` (root combined YAML with `cross_model_candidates` + `union_candidates`).

---

## 6. Mandatory Report Contract

Source-of-truth: Command lines 1539–1977 (`Report Generation — MANDATORY`) and Command lines 1979–2132 (`Ensemble Aggregation Report — MANDATORY`); cross-referenced from Agent lines 734–744 (depth-0 step 12 obligation) and Agent lines 1152 (design principle restatement).

### 6.1 Comprehensiveness Level Mapping (contract — NEW per K1 + K5 + Requirement 3 — verbatim Command lines 1545–1571)

The report-generation skill reads the `comprehensiveness:` payload from its spawn prompt. Every subsection below that cites a content minimum (charts, infographics, calculators, section depth, leaf inclusion) **MUST read from this payload rather than hard-coding fixed numerals**.

| # | Dimension (`comprehensiveness.minima.*`) | `compact` | `default` | `detailed` | `exhaustive` |
|---|------------------------------------------|-----------|-----------|------------|--------------|
| 1 | `minima.charts.count` | **4** | 5 | 7 | 10 |
| 2 | `minima.charts.types_required` | Any 4 distinct from Chart.js + D3 mix | ≥5 distinct, ≥1 D3-advanced (sunburst, sankey, force-directed, parallel-coordinates, choropleth) | ≥7 distinct, ≥2 D3-advanced, ≥1 per facet-kind: comparison, trend, distribution | ≥10 distinct, ≥3 D3-advanced, ≥1 per facet-kind: comparison, trend, distribution, composition, network/relationship, geo (when topic supports geo) |
| 3 | `minima.infographics.count` | **3** | 4 | 6 | 8 |
| 4 | `minima.infographics.types_required` | Any 3 distinct from the existing menu | ≥4 distinct, ≥1 hierarchy, ≥1 process/flow | ≥6 distinct, ≥1 hierarchy, ≥1 process/flow, ≥1 comparison (matrix/quadrant) | ≥8 distinct, ≥1 each of: hierarchy, process/flow, comparison, taxonomy, timeline, persona |
| 5 | `minima.calculators.count` | **1** | 1 | 2 | 3 |
| 6 | `minima.calculators.scenarios_per` | **3** | 4 | 5 | 5 |
| 7 | `depth3_leaf_inclusion` | `summary` | `summary` | `verbatim_quotes` | `verbatim_quotes` |
| 8 | `per_branch_section_depth` | `consolidation_only` | `branch_summary` | `per_leaf_detail` | `per_leaf_detail` |
| 9 | `citation_density` | Research=`mandatory`; Quick=`warn_only` | Research=`mandatory`; Quick=`warn_only` | Research=`mandatory`; Quick=`warn_only` | Research=`per_finding_table`; Quick=`warn_only` with per-finding-table column (placeholder text for missing citations) |
| 10 | `peer_review_surfacing` | `consolidation_only` | `consolidation_only` | `named_section` | `per_branch_dedicated` |
| 11 | `section_length_budget_tokens` | `{ hero: 800, per_facet: 2500, citations: 1000 }` | `{ hero: 1200, per_facet: 4000, citations: 1500 }` | `{ hero: 1800, per_facet: 6500, citations: 2000 }` | `{ hero: 2400, per_facet: 9500, citations: 2500 }` |
| 12 | `ensemble_cross_model_depth` | `per_facet_cards` | `per_facet_cards` | `per_leaf_attribution` | `per_leaf_attribution` |

**`compact` backwards-compatibility anchor** (verbatim Command line 1566): The `compact` row reproduces the pre-richness-feature behaviour byte-for-byte (4 charts, 3 infographics, 1 calculator, 3 scenarios per calculator, depth-3 leaf content elided beyond summary, all per-branch content folded into consolidation prose only, peer-review content folded into consolidation prose only). All subsections below must produce identical output for a `compact` run as the pre-richness codebase did. Pinned by `evals/test_q_meditate.py::TestMeditateBackwardsCompatibility` (8 dedicated tests).

**Subagent-abort rule** (verbatim Command line 1568): if the `comprehensiveness:` payload is missing from the spawn prompt, abort with: `"comprehensiveness: payload required; missing from spawn prompt — caller misconfigured"`.

### 6.2 Paired HTML + PDF rule

Source: Command lines 1539–1582; Agent line 1152.

**Unchanged from 20260517 freeze §6.1** — Both files MANDATORY in both modes; produced automatically as part of step 8 / step 12; never built over `ESCALATE`; capture single UTC `TS` at start; filenames `report-{topic-slug}-{yyyymmddHHMMSS}.html` / `.pdf` with shared `{ts}`; `{topic-slug}` matches working-dir slug; all references use prefix glob — never hard-code `report.html` / `report.pdf`. The respawn protocol (§6.10) writes fresh-timestamp pairs that supersede the prior pair via prefix-glob latest-wins.

### 6.3 Anti-Homogenisation Rules

Source: Command lines 1823–1843; pre-flight context Command lines 263–275.

**Unchanged from 20260517 freeze §6.2 — applies verbatim at every comprehensiveness level per K7 + Requirement 10.** No level relaxes this rule. `compact` does NOT downgrade.

### 6.4 Universal Contrast (WCAG-style)

Source: Command lines 1854–1880.

**Unchanged from 20260517 freeze §6.3 — applies verbatim at every comprehensiveness level per K7 + Requirement 10.** `compact` does NOT downgrade contrast.

### 6.5 Light / Dark mode + Print TOC + Print theme + Headless Chrome → Chromium degradation

Sources: Command lines 1882–1897 (light/dark + responsive nav), 1912–1930 (print theme), 1932–1941 (TOC), 1943–1955 (render command + chromium fallback), 1957–1965 (final verification).

**Unchanged from 20260517 freeze §6.4 + §6.6.** Render command, fallback chain, no-Chromium failure mode, `pdf_color_mode: light_high_contrast` default, page break rules all byte-identical.

### 6.6 Chart.js / D3 / calculator inclusion rules + static fallbacks — **level-driven minima**

Source: Command lines 1676–1777.

**Existing 20260517 freeze §6.5 contract preserved verbatim** for: D3 print degradation table (Command lines 1707–1725), HTML implementation pattern (Command lines 1717–1725), calculator static fallback contract (Command lines 1743–1776), sanity-render verification gate (Command line 1725), D3-cannot-degrade rule.

**The only differences post-richness** (driven by Comprehensiveness Level Mapping §6.1):

- Chart minimum is **`comprehensiveness.minima.charts.count`** (level-determined: `compact`=4, `default`=5, `detailed`=7, `exhaustive`=10) — was hard-coded `≥4`. (Command line 1678)
- Infographic minimum is **`comprehensiveness.minima.infographics.count`** (`compact`=3, `default`=4, `detailed`=6, `exhaustive`=8) — was hard-coded `≥3`. (Command line 1729)
- Calculator minimum is **`comprehensiveness.minima.calculators.count`** (`compact`=1, `default`=1, `detailed`=2, `exhaustive`=3) — was hard-coded `≥1`. (Command line 1745)
- Calculator scenarios floor is **`comprehensiveness.minima.calculators.scenarios_per`** (`compact`=3, `default`=4, `detailed`=5, `exhaustive`=5) — was hard-coded `3–5`. (Command line 1747)
- **Accepted cheap finalisation enhancements count toward the existing minima**: a `decision_tree_infographic` counts as an infographic; a `risks_section` with risk-meter counts as both an infographic AND a section. This makes minima more likely to be reached organically, especially at `compact`. (Command line 1141, 1678, 1729, 1745)

### 6.7 Per-Branch Section Rule + Depth-3 Leaf Inclusion Rule + Peer-Review Surfacing Rule (level-conditional — verbatim Command lines 1782–1805)

**NEW per K5 + K7.** The `comprehensiveness:` payload's dimension fields determine how the report renders confirmed facets, depth-3 leaf material, and peer-review findings.

**Per-Branch Section Rule** (Command lines 1782–1790):

- `consolidation_only` (`compact`): all per-branch content folds into consolidation prose. Each confirmed facet does NOT get its own standalone report section beyond what the consolidation already surfaced. Facet titles appear as section headings within the consolidated structure.
- `branch_summary` (`default`): each confirmed top-level facet gets its own report section presenting a branch-level summary of key findings beyond what the consolidation summarised. At this depth, depth-3 leaf content is represented as summary (per `depth3_leaf_inclusion = summary`).
- `per_leaf_detail` (`detailed` / `exhaustive`): every confirmed top-level facet gets its own dedicated report section with per-leaf subsections. Depth-3 leaf material is rendered at `verbatim_quotes` depth (quoted with full citations).
- **`additional_facet` and `additional_facet_AND_section` branches** at `detailed`+ (`per_leaf_detail`): each gets its own dedicated section just like the original 3 facets. `additional_facet_AND_section` branches additionally honour the user-supplied `custom_report_section_title` from `init-suggestions-{ts}.yml` as the section heading. Per-leaf detail applies at `per_leaf_detail` depth.

**Depth-3 Leaf Inclusion Rule** (Command lines 1794–1797):

- `summary` (`compact` / `default`): depth-3 leaf material is surfaced via its depth-2 parent's summary — key facts and conclusions extracted and represented in the per-branch section or the consolidation. Leaf-level verbatim content is elided beyond summary.
- `verbatim_quotes` (`detailed` / `exhaustive`): depth-3 leaf material is quoted verbatim (the most decision-relevant passages) with full citations (`[research: {subfocus-slug}]`). At least one verbatim quote per branch's depth-3 leaf set is required. Every depth-3 leaf's key finding must appear in the relevant per-branch section with direct citation.

**Peer-Review Surfacing Rule** (Command lines 1799–1805) — **Quick mode is a no-op at every level** (no peer-review files exist; report skill emits one-line "Peer review not applicable in Quick mode" placeholder when level demands a named or per-branch section):

- `consolidation_only` (`compact` / `default`): peer-review reinforcements, contradictions, and gaps reach the report only through the consolidation prose. No dedicated peer-review section beyond the existing "Quality review section" structural element.
- `named_section` (`detailed`): in addition to the existing quality-review content, the report adds three dedicated named cross-branch sections: **"Cross-Branch Reinforcements"** (findings independently confirmed across branches), **"Cross-Branch Contradictions"** (claims where branches disagreed), and **"Cross-Branch Gaps"** (areas identified as under-researched).
- `per_branch_dedicated` (`exhaustive`): one named peer-review section per branch (e.g. **"Branch 1 — {Facet Title}: Reinforcements / Contradictions / Gaps"**), PLUS the three cross-branch named sections from `named_section`.

### 6.8 Init-Suggestions Honour (mandatory when `init-suggestions-{ts}.yml` exists — verbatim Command lines 1807–1821)

**NEW per K4 + K6 + Requirement 6.** At the start of report generation, read `init-suggestions-{ts}.yml` from the working directory. This file was written by the depth-0 manager after the combined Pattern-B confirmation and governs which confirmed sections, visualisations, and additional focus areas MUST appear in the rendered report.

**Required honour rules (verbatim post-W1 canonical — Command line 1815)**:

1. **Confirmed sections** — every `confirmed_sections[i].title` MUST appear as a report section heading in the rendered HTML, with substantive non-empty content (>1 paragraph or >100 words). A heading-only stub counts as missing.
2. **Confirmed visualisations** — every `confirmed_visualisations[i].type` MUST be rendered with non-empty data (a container with no data series counts as missing). The report MAY render additional chart / infographic types beyond these confirmed ones.
3. **Additional focus areas** — every `additional_focus_areas[]` entry whose `treatment == "report_section_only"` MUST become a report section, with the entry's `rationale` prose included at the top of the section. Entries with other `treatment` values (`skip`, `additional_facet`, `additional_facet_AND_section`) are handled separately per the Branch & Leaf Index + per-branch section rules (see Per-Branch Section Rule subsection above for `additional_facet` / `additional_facet_AND_section` entries; `skip` entries are not honoured by the report).

**Floor-not-ceiling rule** (Command line 1817): the report MAY add more sections and more chart/infographic types beyond what `init-suggestions-{ts}.yml` confirmed — the file defines the **floor**, not the ceiling.

**Backwards-compat fallback** (Command line 1819): if `init-suggestions-{ts}.yml` does not exist (pre-richness run, or Quick mode before the file was introduced), skip these checks silently and fall back to the standard comprehensiveness minima.

**Audit cross-link** (Command line 1821): Adversarial Review Dimension 13 audits compliance with these honour rules after the report is generated — any confirmed section or visualisation that is absent or only present as an empty stub triggers a `MUST_FIX` + `respawn_required: true` finding. See the Report-Skill Respawn Protocol in §6.10 below.

### 6.9 K10b Per-Cheap-Type Rendering Contract (verbatim Command lines 1139–1151)

**NEW per K10b.** When a respawn payload carries `accepted_finalisation_enhancements`, the report skill renders each accepted cheap enhancement as follows. **Accepted cheap enhancements count toward the existing `comprehensiveness.minima` counts** — a `decision_tree_infographic` counts as an infographic; a `risks_section` with risk-meter counts as both an infographic (the risk meter) AND a section. This ensures accepting a cheap enhancement makes it more likely the minima are reached organically, especially at `compact` level.

| Type | Landing location in the report | Payload shape consumed | Static degradation rules |
|------|-------------------------------|------------------------|--------------------------|
| `executive_summary` | Before the hero stat-card row, immediately after the title | `{ target_persona, max_paragraphs, anchor_findings }` | Flowing prose, no homogenised marketing-pill cards; respect chosen `theming` payload; ≤`max_paragraphs` paragraphs; citations per `anchor_findings`. |
| `action_plan` | After the per-facet sections, before cross-cutting connections section | `{ horizons: ["7d", "30d", "quarter"], items_per_horizon, anchor_findings }` | Horizon-grouped list (7d / 30d / quarter) with citations per item; rendered as a Gantt-style timeline ribbon (D3 + static fallback) OR a labelled tabular form respecting the chosen direction. Print fallback: full table with all horizons. |
| `risks_section` | After the per-facet sections | `{ risk_taxonomy_axes: ["likelihood", "impact", "detection_difficulty"], anchor_findings }` | Risk-meter / gauge infographic (per the existing infographics catalogue) paired with a risk taxonomy table; risk-meter counts as 1 infographic toward `comprehensiveness.minima.infographics.count`. Print fallback: full table with all risk rows visible. |
| `glossary` | End-of-document appendix, before Citations section | `{ term_count_estimate, anchor_branches }` | 2-column term/definition list; respect chosen typography; print preserves all entries. |
| `decision_tree_infographic` | After the per-facet sections, before the cross-cutting connections section | `{ root_decision, depth, anchor_findings }` | SVG decision tree; print fallback shows fully-expanded state (no click-to-expand); respects `theming.preset.color_scheme`. Counts as 1 infographic toward `comprehensiveness.minima.infographics.count`. |
| `reader_persona_tldrs` | After the executive summary / hero, before the per-facet sections | `{ personas: ["leadership", "engineer", "product"], paragraphs_per_persona }` | Per-persona card grid (NOT the homogenised three-card feature grid — vary per chosen direction); print preserves all personas. |
| `cross_branch_synthesis_section` | After the per-facet sections and any `action_plan` / `decision_tree_infographic`, before Citations | `{ axes: ["convergent", "divergent"], anchor_findings_per_axis }` | Two-column or three-column "convergent / divergent / unique" layout (per chosen direction); citations attached per item. |

### 6.10 Report-Skill Respawn Protocol (K9 + K10b — verbatim Command lines 1368–1446)

**NEW per K9 + K10b.** When Dimension 13 fires with `respawn_required: true`, the standard in-place fix flow is bypassed. Instead:

**Respawn payload schema (verbatim — Command lines 1374–1411)**:

```yaml
respawn_reasons:           # list-typed — one respawn may carry multiple reasons
  - "missing_init_suggestion_sections"        # Dim 13 — confirmed_sections gap
  - "missing_init_suggestion_visualisations"  # Dim 13 — confirmed_visualisations gap
  - "accepted_finalisation_enhancements"      # K10b — cheap enhancements accepted
reviewer_iteration: 1 | 2 | 3
prior_report_paths:
  html: "report-{topic-slug}-{prior_ts}.html"
  pdf:  "report-{topic-slug}-{prior_ts}.pdf"
missing_sections:          # populated when respawn_reasons contains "missing_init_suggestion_sections"
  - title: "Adoption and Market Presence"
    rationale: "From init-suggestions; user confirmed this section"
    source_signals: ["[chat: turn-3]", "[memory: vendor-eval-patterns]"]
    branch_evidence_pointers:
      - "branch-1-depth-2-sub-1-{slug}-{ts}.md"
      - "branch-2-depth-3-sub-4-{slug}-{ts}.md"
missing_visualisations:    # populated when respawn_reasons contains "missing_init_suggestion_visualisations"
  - type: "magic_quadrant_2x2"
    rationale: "Topic explicitly compares 3 alternatives"
    source_signals: ["[file: src/router.ts:12-40]"]
accepted_finalisation_enhancements:    # populated when respawn_reasons contains "accepted_finalisation_enhancements"
  - id: "exec-summary-{ts}"            # one entry per accepted cheap enhancement
    type: "executive_summary"          # one of the 7 cheap K10a types
    title: "Executive Summary"
    description: "1-page exec summary aimed at C-level / time-poor readers"
    payload:                           # type-specific shape per K10b Per-Cheap-Type Rendering Contract
      target_persona: "leadership"
      max_paragraphs: 3
      anchor_findings:
        - "[research: auth-flow-trade-offs]"
    source_signals: ["[child: depth-3 leaf]", "[memory: ...]"]
preserve_other_content: true           # include prior report's confirmed sections verbatim in regenerated output
comprehensiveness_payload: { ... unchanged ... }
init_suggestions_payload: { ... unchanged, full ... }
theming_payload: { ... unchanged ... }
finalisation_enhancements_payload: { ... full file content if present, else null ... }
```

**Per-reason processing order in the respawn handler (verbatim — Command lines 1416–1422)**:

When a respawn payload carries multiple `respawn_reasons`, the report skill processes them in this order:

1. **`accepted_finalisation_enhancements`** — additive new sections / charts; render these first per the K10b Per-Cheap-Type Rendering Contract (§6.9).
2. **`missing_init_suggestion_visualisations`** — additive; render missing viz containers + data series.
3. **`missing_init_suggestion_sections`** — may be auto-resolved by step 1 if an accepted-enhancement title overlaps with a missing-section title via **fuzzy-match**: case-insensitive substring match in either direction (simpler rule — chosen over Jaccard ≥0.6 on tokenised titles per the architecture design's "subtask 05 picks" instruction). When step 1 auto-resolves a step-3 missing section, the report skill marks the missing section as `auto_resolved: true` in its respawn-output report metadata; the next iteration's reviewer verifies the enhancement-driven section meets the substantive-content bar (>1 paragraph / >100 words). If it doesn't, Dim 13 fires again with the same missing-section cause.

When step 1 and step 3 fire simultaneously and step 1 resolves a step-3 entry via fuzzy-match, **only 1 iteration is consumed** (the bundle counts as a single respawn per the OQ #9 bundling rule).

**Output filename rule (verbatim — Command line 1426)**: Respawned reports get a fresh timestamp: `TS=$(date -u +%Y%m%d%H%M%S)`. The prior HTML/PDF pair is **preserved on disk** for diff inspection. The Branch & Leaf Index resolves the latest pair via prefix-glob (`report-{topic-slug}-*.html` / `*.pdf`) — the newest file per glob is authoritative.

**Iteration accounting (verbatim — Command lines 1428–1433)**:

- Respawn shares the existing ≤3 adversarial review-and-fix iteration cap. A respawn is bundled into the iteration that flagged it — the iteration counter advances once per review-and-fix cycle regardless of whether a respawn fired.
- The **next** iteration's reviewer reviews the regenerated report (respawn-then-re-review).
- **Maximum useful respawns per meditation = 2**: iter 1 ends → respawn possible (reviewed at iter 2); iter 2 ends → respawn possible (reviewed at iter 3); iter 3 with Dim 13 still firing → `ESCALATE` (no iter 4 to review a respawn).
- The `accepted_finalisation_enhancements` cause can fire **at most once** per meditation (the `Q-Finalisation-Enhancements` gate fires once per meditation — accepted cheap enhancements bundle into iteration 1's respawn and cannot re-fire in later iterations).

**Same-iteration Dim 1–11 fix + Dim 13 respawn ordering (verbatim — Command lines 1437–1440 / OQ #7 resolution)**:

When iteration N's reviewer simultaneously fires Dim 1–11 findings AND Dim 13 with `respawn_required: true`:

1. **First**: apply Dim 1–11 in-place fixes (the reviewer rewrites branch / consolidation / peer-review files).
2. **Then**: respawn the report-generation skill; the respawn re-reads the now-fixed branch files and regenerates the report, cleanly incorporating the in-place fixes.

**Pattern B integrity (verbatim — Command line 1444)**: The reviewer **never calls `askQuestion`** for `respawn_required: true` findings — the respawn payload is structured and deterministic; no user input is needed to execute it. Standard ambiguous `MUST_FIX` findings (Dim 1–11) still follow the existing Pattern B escalation path with mandatory `context` field.

### 6.11 Reviewer escalation — Pattern B with mandatory decision-guidance (verbatim Command lines 1291–1306)

**Unchanged from 20260517 freeze §4.6 MUST_FIX schema, restated post-richness because Dim 12 also flows through this path.** Dim 13 `respawn_required: true` findings BYPASS this path per §6.10 above. **Every escalated `needs_user_input` entry MUST include `context` text that explains the trade-off the user is choosing between** — never present bare options. The calling agent uses that `context` when constructing the `askQuestion` prompt so the user understands the consequences of each choice.

Minimum escalation schema (verbatim — preserved from 20260517 freeze §4.6):

```
## needs_user_input

### question_id: <reviewer-iter-N-finding-M>
- **prompt**: <the question, citing the offending file and line>
- **options**: [<option-a>, <option-b>, ...]
- **default**: <suggested option, or none>
- **context**: <REQUIRED — explains what each option means for the meditation,
   which fix the reviewer would apply for each, and which downstream artefacts
   are affected. Without this, the calling agent cannot relay decision-guidance
   to the user.>
```

### 6.12 Ensemble Aggregation report extras + K10 Ensemble Respawn Targeting

Source: Command lines 1979–2132; K10 ensemble respawn targeting at Command lines 1153–1184.

**Existing 20260517 freeze §6.7 contract preserved verbatim** — ensemble working dir structure (extended with per-tree + root `finalisation-enhancements.yml`), filename conventions, `cross-model-synthesis.md` frontmatter + 8 mandatory sections, ensemble report structural extras (model comparison hero, per-facet comparison cards, agreement heatmap, divergence deep-dives, per-model drill-down links, model attribution Sankey, citation Venn, confidence radar), `[model: label]` / `[models: all]` citation format.

**Footer annotation extension** (Command lines 1601–1611) — **NEW per K10**:

The standard footer `theme:` annotation is extended with:

```
theme: editorial / warm_palette / serif_headings_sans_body | level: default
```

When ≥1 finalisation enhancement was accepted and rendered via the respawn path, append the enhancement segment:

```
theme: editorial / warm_palette / serif_headings_sans_body | level: default | finalisation-enhancements: 3 (executive_summary, risks_section, glossary)
```

**Skip-all path** (verbatim Command line 1609): when 0 finalisation enhancements were accepted (or when the K10a gate was skipped entirely), the `finalisation-enhancements:` segment MUST be omitted entirely — it must NOT be written as `finalisation-enhancements: 0`. The `level:` segment IS always written from this spec forward.

**Ensemble split** (verbatim Command line 1611): per-tree reports' footer annotations enumerate ONLY the per-tree-sourced accepted enhancements (from candidates with `source: "tree:{model-subdir}"`); the cross-model synthesis report's footer enumerates ONLY the cross-model-sourced accepted enhancements (from candidates with `source: "cross_model"`). This keeps each report's footer accurate with respect to what was actually integrated into that specific report.

**K10 Ensemble Respawn Targeting** (verbatim Command lines 1153–1171):

When an accepted enhancement was sourced from a per-tree candidate vs a cross-model candidate, the report-skill respawn targets a different report:

- **Per-tree-sourced accept** (`source: "tree:{model-subdir}"` in the root `union_candidates` list): the respawn payload for the **per-tree report** (`{model-subdir}/report-{topic-slug}-{ts}.html/.pdf` pair) gains the entry under `accepted_finalisation_enhancements`. The per-tree report skill respawns and the regenerated per-tree report incorporates the accepted enhancement. **The cross-model synthesis report is NOT respawned for per-tree-sourced accepts.**
- **Cross-model accept** (`source: "cross_model"`): the respawn payload for the **cross-model synthesis report** (`ensemble-report-{topic-slug}-ensemble-{ts}.html/.pdf`) gains the entry. The cross-model synthesis report skill respawns and the regenerated synthesis report incorporates the accepted enhancement. **Per-tree reports are NOT respawned for cross-model accepts.**

**Cost-ack re-presentation at ensemble for `spawn_now` (subsystem prose — verbatim Command lines 1160–1169)**: when the user opts an expensive item into `spawn_now` at the ensemble root gate, the cost-ack re-presentation prose names which subsystems gain agents at which level (per-tree-sourced expensive items spawn within the relevant per-tree model subdirectory; cross-model-sourced expensive items spawn at the ensemble root).

**Dim 13 layered audit at ensemble** (verbatim Command line 1171): the reviewer audits each accepted enhancement against the **correct** report — per-tree-sourced enhancements audited against the per-tree report; cross-model-sourced enhancements audited against the cross-model synthesis report. A missing accepted enhancement in the wrong report is NOT a Dim 13 finding; it is only a finding when the targeting rule above says it should be in that specific report.

### 6.13 Ensemble layered cadence summary (verbatim Command lines 1173–1184)

In Ensemble mode, the `Q-Finalisation-Enhancements` gate fires **once** at the ensemble root, after:

1. Each model tree's consolidation agent performs its own in-pass reflection and writes `{model-subdir}/finalisation-enhancements.yml` (**per-tree YAMLs are write-only at the per-tree level** — no per-tree `askQuestion` fires).
2. The aggregator runs a second reflection pass over all per-tree YAMLs + `cross-model-synthesis.md` and writes the root combined `finalisation-enhancements.yml` (with `cross_model_candidates` + `union_candidates`, capped at 5).

The calling agent's single combined `askQuestion` at ensemble root ranks across the union of `(per-tree × N) + (cross-model × 5)` candidates, capped at the standard 0–5 multi-select. Each option label includes provenance: `{title} [{cost_class}] ({source-label}) — composite={N}`.

**Model-label resolution fallback** (Command line 1182): if `cruxMemories.meditate.modelPool` no longer contains the `{model-subdir}` slug at continuation time (model retired), label falls back to `"Unknown model ({model-subdir})"`.

**Skip-all path reproduces today's behaviour byte-for-byte at every richness level** (Command line 1184).

---

## 7. Continuation Menu — Calling-Agent Steps 9–12

Source: Command lines 921–986 (single-model); Command lines 900–919 (ensemble); Agent lines 769–774 (informational summary).

### 7.1 Step 9 — Verify mandatory report artifacts

**Unchanged from 20260517 freeze §7.1.** Verification gate, `HTML_LATEST` / `PDF_LATEST` resolution via prefix-glob + size check, regeneration of missing artefact, `ESCALATE` no-op, no-Chromium error surfacing all preserved.

### 7.2 Step 10 — Present to user

**Unchanged from 20260517 freeze §7.2.** Always include absolute paths to `workingDir`, `facets.md`, `retrospective-{ts}.md`, latest report HTML + PDF; `ESCALATE` surfaces `review-pre-report-*-iter-*.md` paths instead.

### 7.3 Step 11 — Interactive continuation (UPDATED — verbatim Command lines 961–976)

**Existing 20260517 freeze §7.3 prompt body preserved verbatim** (Command lines 933–959). **New K10c options grouped under section headings** (Command lines 961–974):

**Expansion directions** (K10c group 1):

- Discovered tangent directions (derived from the exploration) — one option per discovered direction, each acting as an expansion trigger

**Apply un-chosen enhancements** (K10c group 2 — one option per `unchosen_persisted` item in `finalisation-enhancements.yml`; omit section if no unchosen items exist):

- `reapply_enhancement_{id}` — "Re-apply unchosen enhancement: {candidate.title}" — re-runs the post-consolidation phase with that single item pre-checked (other candidates greyed-out); fresh ≤3 iteration cap (new continuation invocation). Decision guidance: selecting re-triggers `Q-Finalisation-Enhancements` with this single item pre-checked; the existing report is not modified until the re-application respawn completes.

**Spawn queued follow-ups** (K10c group 3 — one option per queued expensive item with a `follow-up-{type}-{ts}.yml` on disk; omit section if no queued items exist):

- `spawn_queued_{id}` — "Spawn now: {type} — {follow_up_title}" — triggers cost-ack re-presentation (`spawn_now` variant) then spawns the agent. Decision guidance: triggers the read-only-richness cost-ack re-presentation showing the updated agent count; on proceed, the expensive agent spawns immediately.

**Other**:

- `save_spec` — "Save meditation as draft spec" (write insights as a draft spec outline to the configured specs directory)
- `end_meditation` — "End meditation" (complete the session)

**Forbidden options (removed in subtask 05 — unchanged from 20260517 freeze §7.3)** — Command line 976: do NOT offer "Save as interactive HTML report" or "Save as PDF report" — both artefacts are now produced automatically.

### 7.4 Step 12 — Handle the user's selection (UPDATED — verbatim Command lines 978–986)

**Existing expansion / `save_spec` / `end_meditation` semantics preserved** (Command line 980, 983, 984 — unchanged from 20260517 freeze §7.4). **New K10c handlers** (Command lines 981–982):

- **`reapply_enhancement_{id}` selected** (K10c — re-apply unchosen enhancement) — re-run `Q-Finalisation-Enhancements` with the selected item pre-checked (other candidates greyed-out). A fresh ≤3 iteration cap applies (this is a new continuation invocation). The respawn targets the same working directory's report pair.
- **`spawn_queued_{id}` selected** (K10c — spawn queued follow-up) — trigger the read-only-richness cost-ack re-presentation (`spawn_now` variant) with the selected expensive item enumerated. On proceed, spawn the expensive agent immediately. On cancel, return to the continuation menu without modifying the follow-up artefact.

**Expansion-direction cost-ack rule** (Command line 980): expansion runs the read-only-richness variant of `Q-Cost-Acknowledgment-Expansion` (richness locked); the existing "keep deep-confirm setting?" follow-up is preserved unchanged; mode-swap and depth options are NOT re-offered.

### 7.5 Ensemble mode steps 10–13 — Calling-agent block

Source: Command lines 894–919.

**Unchanged from 20260517 freeze §7.5** — verification of all per-model report pairs + ensemble synthesis + ensemble report pair; presentation reading `cross-model-synthesis.md`; per-model expansion options; `save_spec`; `end_meditation`. Expansion trees run as single-model unless `--ensemble` re-passed.

**Ensemble-specific K10 additions** (per §4.5 above):

- Step 9 ensemble verification also checks for `{model-subdir}/finalisation-enhancements.yml` per tree and root `finalisation-enhancements.yml`.
- Step 11 continuation menu surfaces unchosen items from the root YAML with provenance labels (`(cross-model)` or `(from tree: {model-label})`) AND per-tree-only unchosen items (`surfaced_to_root: false`) with `(from tree: {model-label}, not surfaced at root)` label per Agent lines 840–852 design.
- Selecting a per-tree-only unchosen item targets the per-tree report respawn (per subtask 05) rather than the cross-model synthesis report respawn.

---

## 8. Subject-Matter Focus Rule

Source: Command lines 1448–1468; restated as design principle Agent line 1154.

**Unchanged from 20260517 freeze §8 — applies verbatim at every comprehensiveness level per K7 + Requirement 10.** Applies to `consolidation.md` and HTML/PDF reports only; internal coordination files retain process-oriented naming. The retrospective is the one output where process-oriented language is expected.

---

## 9. Cross-Repo Touchpoints

| File | Path | Reference / Line | Role | Source |
|------|------|------------------|------|--------|
| `/crux-amnesia` explicit-command list (rule restating that explicit memory commands override amnesia mode) | `.cursor/commands/crux-amnesia.md` | Line 40 | Lists `/crux-meditate` as a memory command that should be treated as direct user intent | unchanged from 20260517 freeze §9 |
| `/crux-amnesia` explicit-command list (Available memory commands section) | `.cursor/commands/crux-amnesia.md` | Line 63 | Lists `/crux-meditate — Recursive memory-informed exploration` | unchanged |
| `commands.meditate` config entry | `.crux/crux-memories.json` | Lines 46–50 | `{ "file": ".cursor/commands/crux-meditate.md", "default": "/crux-meditate", "description": "Recursive memory-informed exploration and insight synthesis" }` | unchanged |
| `cruxMemories.meditate.modelPool` + `ensembleAggregatorModel` | `.crux/crux-memories.json` | Lines 80–87 | Ensemble model pool (3 entries) + aggregator override (null) | unchanged |
| **`cruxMemories.meditate.finalisationEnhancements`** (K10 config — proposed but not yet wired into `.crux/crux-memories.json` defaults; documented in spec + agent file only) | `.crux/crux-memories.json` | _Not yet present_ | Proposed keys: `minimumImpactThreshold: 6`, `weights: { impact: 1.0, insight_value: 1.0 }`, `formula: "product"`. Subtask 10 (install-dist-release) is the natural surface to add the default entries; the agent file references the keys regardless. | NEW per K10 OQ #11 + OQ #12 |
| AGENTS.md memory-manager agent row | `AGENTS.md` | Line 25 | `crux-cursor-memory-manager` row that lists "Meditate" among its purposes | unchanged |
| AGENTS.md subagent-protocol example | `AGENTS.md` | Line 55 | Lists `/crux-meditate` among commands invoking subagents | unchanged |
| AGENTS.md "Memory lifecycle operations" allocation row | `AGENTS.md` | Line 96 | Routes memory lifecycle (dream, REM, recall) work to `crux-cursor-memory-manager` | unchanged |
| README.md meditation command rows (Memory Commands table) | `README.md` | (post-S07 — extended +25 lines with richness coverage) | `/crux-meditate` rows + new richness-level documentation | UPDATED by 20260523 S07 (subtask 09 acceptance) |
| README.md amnesia override paragraph | `README.md` | Line 689 (legacy) | Lists `/crux-meditate` among explicit memory commands that override amnesia | unchanged |
| README.md File Reference table | `README.md` | Line 799 (legacy) | `.cursor/commands/crux-meditate.md — Recursive exploration command` | unchanged |
| README.md Memory System summary row | `README.md` | Line 947 (legacy) | `Meditate Command — .cursor/commands/crux-meditate.md — Recursive memory exploration` | unchanged |
| `docs/crux-memories.md` Memory Commands table | `docs/crux-memories.md` | Line 23 + extended (+108 lines post-S07) | `/crux-meditate ["topic"]` row with description + richness level documentation + K10 gate documentation + `finalisation-enhancements.yml` artefact mention | UPDATED by 20260523 S07 |
| `docs/crux-memories.md` agent narrative | `docs/crux-memories.md` | Multiple references (cross-platform mapping, amnesia carve-out, config wiring) | Unchanged structurally; references extended post-richness | unchanged anchors |
| `docs/crux-memories.md` config example | `docs/crux-memories.md` | Lines 316–319 (legacy) | `commands.meditate.file` config block | unchanged |
| `docs/crux-memories.md` QA checklist Q. Meditate Command | `docs/crux-memories.md` | Lines 1138–1153 (legacy) | User-acceptance checks for `/crux-meditate` invocations | UPDATED by 20260523 S07 to include richness coverage |
| `web/compress.md/memories.html` landing SVG label | `web/compress.md/memories.html` | Line 52 (legacy) | `/crux-meditate` SVG text label in command list | unchanged |
| `web/compress.md/memories.html` command card | `web/compress.md/memories.html` | Lines 807–816 + extended (+32 lines post-S07) | `/crux-meditate` command card with richness level documentation | UPDATED by 20260523 S07 |
| `web/compress.md/memories.html` Meditate section | `web/compress.md/memories.html` | Lines 868–908 (legacy) | "Meditate: Recursive Exploration" landing section + diagram | UPDATED by 20260523 S07 |
| `install.py` `MEMORY_FILE_PREFIXES` enumeration | `install.py` | Line 61 (legacy) | `.cursor/commands/crux-meditate.md` listed in memory-file prefixes installed by `install.py` | **NOT** modified by 20260523 (K8 — no new files added) |
| `install.py` fallback file list | `install.py` | Line 502 (legacy) | `.cursor/commands/crux-meditate.md` listed in the fallback / dist-zip command set | unchanged |
| `install.py` config-write defaults | `install.py` | Lines 800–803 (legacy) | `commands.meditate` block written when generating `.crux/crux-memories.json` | unchanged |
| `scripts/create-crux-zip.py` DIST_FILES | `scripts/create-crux-zip.py` | Line 38 (legacy) | `.cursor/commands/crux-meditate.md` enumerated as a release asset | **NOT** modified by 20260523 (K8) |
| `.cursor/agents/crux-cursor-memory-manager.md` (THE BULK OF EXECUTABLE CONTRACTS LIVES HERE) | `.cursor/agents/crux-cursor-memory-manager.md` | **Lines 279–1159 (Meditate Mode) + 1189–1349 (Ensemble Aggregation Mode w/ K10 layered cadence)** | All Phases A–G, Quick 6-step, Adversarial Review, Ensemble Aggregation, design principles + NEW K4 / K5 / K6 / K9 / K10 surfaces | UPDATED by 20260523 (line count 946 → 1388) |
| `.cursor/commands/crux-meditate.md` (calling-agent surface) | `.cursor/commands/crux-meditate.md` | Entire file 1–2142 | All calling-agent gates, continuation menu, mandatory-report contract + NEW K2 / K4 / K9 / K10 surfaces | UPDATED by 20260523 (line count 1493 → 2142) |
| `evals/test_q_meditate.py` | `evals/test_q_meditate.py` | Entire file 1–1335 | Test coverage: 8 pre-existing + 28 NEW richness test classes | UPDATED by 20260523 S06 (240 → 1335 lines) |
| `evals/sdk/tests/q-meditate.test.ts` | `evals/sdk/tests/q-meditate.test.ts` | Entire file 1–576 | SDK gated tests: 3 pre-existing + 4 NEW richness describe blocks | UPDATED by 20260523 S06 (357 → 576 lines) |
| `evals/test_p_amnesia.py` | `evals/test_p_amnesia.py` | `EXPLICIT_MEMORY_COMMANDS` row only | Lists `/crux-meditate` among amnesia-overriding commands | unchanged |

**Touchpoints introduced by the decomposition spec** (not yet present — listed for S10 to track):

- New agent file `.cursor/agents/crux-cursor-meditation-guide.md` — must be added to install.py, create-crux-zip.py, AGENTS.md table, README rows, CONTRIBUTORS.md table, version-bump RELEASE_PATHS (if needed), `.crux/dist-manifest.json`.
- Six new skill directories `.cursor/skills/crux-skill-memory-meditation-{research,quick,ensemble,review,report,coordination}/SKILL.md` — same enumeration surfaces.

**CRUX-compressed mirror surfaces** (S11 scope; only regenerate existing maintained mirrors — never create new ones, never edit generated files):

- `.cursor/rules/crux-memories-integration.crux.mdc` ← `.cursor/rules/crux-memories-integration.md`
- `.cursor/rules/docs-sync.crux.mdc` ← `.cursor/rules/docs-sync.md`
- `.cursor/rules/version-bump.crux.mdc` ← `.cursor/rules/version-bump.md`
- `.cursor/rules/zip-contents-protection.crux.mdc` ← `.cursor/rules/zip-contents-protection.md`
- `AGENTS.md` is a source file in this repo; `AGENTS.crux.md` is **not** maintained — do **not** require or create it (per spec K8).

---

## 10. Source-of-Truth Map

Two-column concordance: every contract item back-traceable to a current source location at the **working-tree state** captured on 2026-05-24. S02 plans moves against this map; S12 verifies that the post-refactor repo preserves every row.

### 10.1 Command file `.cursor/commands/crux-meditate.md` (2142 lines)

| Contract item | Line range | Section heading |
|--------------|-----------|-----------------|
| Header / repository link | 1–5 | `# crux-meditate` |
| Usage CLI examples (5 forms) | 7–18 | `## Usage` |
| Modes summary table (Research / Quick / Ensemble) + safeguards summary line (extended to include K10 gate) | 20–28 | `## Modes` |
| Spawn instructions + Pattern B + 5-gate intro (4 pre-spawn + Q-Finalisation-Enhancements) | 30–36 | `## Instructions` |
| Argument handling (flag detection, slug stripping, remaining args) | 38–53 | `### Argument Handling` |
| Depth Selection (gate 1) — overview + agent count table + Q-Depth-Selection + behaviour rules | 55–105 | `### Depth Selection — MANDATORY` |
| **Cost & Scope Acknowledgment (gate 2 — MERGED)** — `Q-Cost-and-Richness-Acknowledgment` preamble + cost table + Sub-Q1 + Sub-Q2 + behaviour rules + read-only-richness variant + 3 trigger preambles | 106–256 | `### Cost & Scope Acknowledgment — MANDATORY` |
| Theme Preflight (gate 3) — Anti-Homogenisation context + Q1–Q5 + Q1b repo-scan + surprise_me fallback + theming YAML + **`comprehensiveness:` payload propagation block** | 257–390 | `### Theme Preflight — MANDATORY` |
| **Facet Confirmation (gate 4 — combined Pattern B)** — depth-0 flow + combined `needs_user_input` schema + combined `askQuestion` 5 sub-questions + 4-mode focus-area decision set + resume handler + cost-change check + re-presentation + deep confirmation flow + re-spawn semantics | 391–738 | `### Facet Confirmation — MANDATORY at depth 0, opt-in deeper` |
| Coordination Conventions (artefact filename table 18 rows + prefix-glob polling + never-hard-code rule) | 740–784 | `### Coordination Conventions` |
| What Happens — workflow chooser | 786–791 | `### What Happens` |
| Research mode steps 1–8 (sub-step expansion 1–10 inside step 8) | 792–821 | `#### Research mode (default)` |
| Quick mode steps 1–8 substitutions | 823–845 | `#### Quick mode (`--quick`)` |
| Ensemble mode protocol (steps 1–10 calling-agent + steps 9–13 ensemble-specific) | 847–919 | `#### Ensemble mode (`--ensemble`)` |
| Steps 9–12 single-model calling-agent block (verify report pair / present / interactive continuation with K10c groups / handle selection with K10c handlers) | 921–986 | `**Steps 9–12: Calling-agent block (both modes, single-model)**` |
| Branch & Leaf Index template + conventions (extended with init-suggestions + finalisation-enhancements + follow-up rows) | 988–1059 | `### Branch & Leaf Index` |
| **Finalisation Enhancements Gate — Q-Finalisation-Enhancements (K10a/b/c)** — gate prompt + multi-select + per-item treatment sub-Q + spawn_now cost-ack + update flow + K10b Per-Cheap-Type Rendering Contract + K10 Ensemble Respawn Targeting + Ensemble layered cadence summary | 1062–1184 | `### Finalisation Enhancements Gate — Q-Finalisation-Enhancements (K10a)` |
| Adversarial Review and Fix Cycle — reviewer agent + **13 dimensions** (Dim 12 + Dim 13 + level-conditional Dim 9 expansion) + severity classification + iteration loop (with Dim 13 respawn branch) + Pattern-B escalation schema + review document format + Quick-mode treatment + **Report-Skill Respawn Protocol (K9 + K10b)** | 1187–1446 | `### Adversarial Review and Fix Cycle — MANDATORY` |
| Subject-Matter Focus rule | 1448–1468 | `### Subject-Matter Focus — MANDATORY` |
| Process Retrospective template (frontmatter + required sections) | 1470–1537 | `### Process Retrospective — MANDATORY` |
| Report Generation — MANDATORY (filenames + inputs + HTML structural elements + **Comprehensiveness Level Mapping table 12×4** + Report Comprehensiveness / No Information Loss / coverage rules per level + Option Comparison + visualisations + infographics + interactive elements + **Per-Branch Section Rule** + **Depth-3 Leaf Inclusion Rule** + **Peer-Review Surfacing Rule** + **Init-Suggestions Honour** + anti-homogenisation + theming application + Universal Contrast + light/dark + responsive nav + PDF requirements + filename pairing + print theme + TOC + render command + final verification + footer extension) | 1539–1977 | `### Report Generation — MANDATORY` |
| Ensemble Aggregation Report (ensemble working dir + filename conventions + cross-model synthesis schema + ensemble report extras + model-attribution citations) | 1979–2132 | `### Ensemble Aggregation Report — MANDATORY` |
| Related links (agent, skills, sibling commands) | 2134–2142 | `## Related` |

### 10.2 Agent file `.cursor/agents/crux-cursor-memory-manager.md` (1388 lines — Meditate-relevant + Forget Mode + Ensemble Aggregation Mode rows)

| Contract item | Line range | Section heading |
|--------------|-----------|-----------------|
| Critical context loading rules | 9–16 | `## CRITICAL: Load Context First` |
| User Input Escalation — Pattern A / Pattern B / `needs_user_input` schema | 17–46 | `## User Input Escalation — CRITICAL` |
| Expertise list (Meditate listed, Ensemble Aggregation listed) | 48–58 | `## Your Expertise` |
| Skills used | 60–71 | `## Skills You Use` |
| Operating Modes header | 73 | `## Operating Modes` |
| **Meditate Mode** — invocation variants table + mode selection + cost-and-richness ack pattern + theme pattern + **`comprehensiveness:` payload propagation block** + facet confirmation pattern (combined) + file-based coordination intro + working dir + Coordination Conventions canonical table (18 rows incl. init-suggestions, finalisation-enhancements, follow-ups) + placeholders + prefix-glob polling + never-hard-code rule | 279–397 | `### Meditate Mode — `/crux-meditate`` |
| **Research mode depth-0 workflow steps 1–13** — extended with step 4b (4-mode focus-area reconciliation + `init-suggestions-{ts}.yml` write) + step 8 K10c reflection + step 8b K10b resume handler | 399–748 | (within Meditate Mode) |
| Step-numbering provenance note | 750 | (within Meditate Mode) |
| **Quick mode top-level workflow** (steps 1–13 substitutions; Q-Finalisation-Enhancements fires identically) | 752–767 | (within Meditate Mode) |
| Post-subagent flow (calling-agent steps 9–12 informational summary) | 769–774 | (within Meditate Mode) |
| **Recursive exploration protocol — Research mode** (Phases A–G + deep-confirmation hook + **comprehensiveness honouring at leaf depth**) | 776–864 | (within Meditate Mode) |
| **Recursive exploration protocol — Quick mode** (6-step + step 2 deep-confirmation hook + comprehensiveness honouring at leaf depth) | 866–909 | (within Meditate Mode) |
| Quick vs Research differences table | 911–921 | (within Meditate Mode) |
| Facet registry protocol (schema + mkdir lock + orphan recovery) | 923–969 | (within Meditate Mode) |
| Citations protocol (inline markers + per-file requirements + index schema + validation rules) | 971–1006 | (within Meditate Mode) |
| **Peer review file spec** (filename + frontmatter + required sections — verbatim — unchanged from 20260517 freeze §5.6) | 1008–1036 | (within Meditate Mode) |
| Subfocus narrowing example | 1038–1061 | (within Meditate Mode) |
| Working directory structure (canonical tree) | 1063–1100 | (within Meditate Mode) |
| Output file format (frontmatter + body sections) | 1102–1135 | (within Meditate Mode) |
| **Design principles list** (file-based coord / 3-way fan-out / predictable paths / mandatory citations / mode-specific traits / open-mindedness / concise outputs / pre-spawn gates / **mandatory user confirmation of facets + init-time suggestions** / **set-once-per-invocation richness** / theming / adversarial review / Branch & Leaf Index / mandatory reports / Universal Contrast / Subject-Matter Focus / Report Comprehensiveness / Option Comparison / Visualizations & PDF degradation / Ensemble model propagation) | 1137–1158 | (within Meditate Mode) |
| **Forget Mode** (separate mode; line range UPDATED from 843–870 to **1160–1188** post-richness) | 1160–1188 | `### Forget Mode — `/crux-forget`` |
| **Ensemble Aggregation Mode** (internal sub-mode of Meditate) — invocation + workflow steps 1–5 with **K10 layered cadence steps 3b–3f inserted** | 1189–1349 | `### Ensemble Aggregation Mode — (internal)` |
| Agent scoping rules | 1351–1365 | `## Agent Scoping Rules` |
| Critical rules (feature guards / data integrity / workflow discipline / skill delegation) | 1367–1388 | `## Critical Rules` |

### 10.3 Eval files

#### 10.3.1 `evals/test_q_meditate.py` (1335 lines — 36 test classes total: 8 pre-existing + 28 NEW per richness S06)

**8 pre-existing classes (unchanged from 20260517 freeze § 10 / pre-richness baseline)**:

| Class | Line | Asserts (pre-richness contract) |
|-------|------|-------|
| `TestMeditateConfigPresence` | 58 | `commands.meditate` config presence + file path + default + file exists |
| `TestMeditateCommandDefinition` | 95 | Usage section + no-args / quoted-topic / file-references support |
| `TestMeditateFacetStructure` | 123 | 3 facets / distinct dimensions / facets become branches |
| `TestMeditateRecursiveDepth` | 150 | 3 depths / depth-1 spawns / depth-3 terminal / `Q-Depth-Selection` literal / default = 3 |
| `TestMeditateMemoryQuerying` | 192 | Memory queries / index usage / refines at each level |
| `TestMeditateConsolidation` | 216 | Documents consolidation / cross-branch connections / organised output |
| `TestMeditateContinuationMenu` | 240 | Expansion options / save-as-spec / end / AskQuestion |
| `TestMeditateAgentSpawning` | 268 | Spawns `crux-cursor-memory-manager` / mentions meditate mode |

**28 NEW richness test classes** (all introduced by S06 of `specs/20260523-meditate-richness/` — pinned to lines per `git grep '^class TestMeditate' evals/test_q_meditate.py`):

| Class | Line | Asserts |
|-------|------|---------|
| `TestMeditateMergedCostAndRichnessGate` | 293 | Merged gate exists; no standalone `Q-Comprehensiveness`; 4 richness enum values; `default` preselected; Sub-Q2 option set preserved; per-richness decision guidance; depth × richness cost estimates; mode-swap preserves richness; K1 dual-meaning callout |
| `TestMeditateReadOnlyRichnessVariant` | 358 | Read-only-richness variant exists; expansion variant exists; richness shown locked; 3 trigger preambles documented |
| `TestMeditateComprehensivenessLevelMapping` | 382 | Level mapping table exists; `compact` row chart minimum = 4 / infographic = 3 / calculator = 1 / scenarios = 3; all 4 levels have chart entry; every level row has all 12 dimensions |
| `TestMeditateInitSuggestions` | 430 | `init-suggestions-{ts}.yml` documented in command + agent + filename table + Branch & Leaf Index; 4 opt-in modes (`skip` / `additional_facet` / `report_section_only` / `additional_facet_AND_section`); schema fields enumerated |
| `TestMeditateCombinedFacetConfirmation` | 463 | Combined Pattern-B askQuestion documented; folds Q-Confirm-1 + Q-Confirm-2 + init-suggestions; 5 sub-questions enumerated; 4-mode focus-area sub-question; per-sub-Q decision guidance |
| `TestMeditateAdditionalFacetCostAck` | 499 | Cost-ack re-presentation documented; triggers on `additional_facet`; triggers on `additional_facet_AND_section`; does NOT trigger on `skip` or `report_section_only`; uses read-only-richness variant |
| `TestMeditateSetOncePersistence` | 536 | Set-once-per-invocation documented; expansion variant shows richness locked; no `--reset-richness` flag; users must `cancel` to change richness |
| `TestMeditateAdversarialReviewerExtension` | 560 | Reviewer has 13 dimensions; Dim 12 (Comprehensiveness fidelity); Dim 13 (Init-suggestion + finalisation-enhancement honour); Dim 9 level-conditional expansion |
| `TestMeditateRespawnProtocol` | 589 | Respawn protocol documented; `respawn_reasons` is list-typed; required payload keys (`missing_sections` / `missing_visualisations` / `accepted_finalisation_enhancements` / `preserve_other_content` / `comprehensiveness_payload` / `init_suggestions_payload` / `theming_payload` / `finalisation_enhancements_payload`); shares ≤3 iteration cap; `respawn_required: true` bypasses standard flow; respawn-then-re-review semantics |
| `TestMeditateRespawnFiniteIteration` | 637 | Iteration cap = 3; respawn counts as 1 iteration; `ESCALATE` verdict at iter 3 with Dim 13; max useful respawns = 2 |
| `TestMeditatePayloadPropagation` | 669 | `comprehensiveness` in depth-0 spawn prompt; propagated to children in Phase D; propagated in Quick mode; abort-if-missing documented |
| `TestMeditateNoNewDistFilesK8` | 699 | `scripts/create-crux-zip.py::DIST_FILES` contains no spec-introduced paths; `install.py::MEMORY_FILE_PREFIXES` likewise; `.crux/dist-manifest.json` likewise |
| `TestMeditateBackwardsCompatibility` | 783 | `compact` chart minimum unchanged (4); infographic unchanged (3); calculator unchanged (1); calculator scenarios unchanged (3); depth3_leaf_inclusion unchanged (`summary`); per_branch_section unchanged (`consolidation_only`); peer_review_surfacing unchanged (`consolidation_only`); no standalone `Q-Comprehensiveness` |
| `TestMeditateSafeguardRegressions` | 836 | Anti-homogenisation block / Universal Contrast / Subject-Matter Focus / Pattern B / paired HTML+PDF / mandatory citations / iteration cap / `MUST_FIX` `needs_user_input` mandatory `context` / retrospective always written |
| `TestMeditateFinalisationEnhancementGate` | 889 | Gate exists; gate is multi-select 0–5; fires after consolidation / before adversarial review; per-option labels include cost class; decision guidance on cost class consequences |
| `TestMeditateK10SkipAllBackwardsCompat` | 922 | Skip-all produces no accepted enhancements in respawn; `respawn_reasons` excludes accepted enhancements on skip-all; no follow-up files written on skip-all; footer omits `finalisation-enhancements:` segment on skip; `finalisation-enhancements.yml` written with `unchosen_persisted` treatment; no additional adversarial-review iteration consumed |
| `TestMeditateFinalisationCheapAcceptRespawn` | 964 | `accepted_finalisation_enhancements` list populated when cheap accepted; `respawn_reasons` includes the cause; cheap respawn shares iteration cap; multiple cheap items bundle into single respawn |
| `TestMeditateFinalisationExpensiveQueueDefault` | 990 | Expensive default = `queue`; follow-up file written for queued items; no agent spawned for queue treatment; queued item surfaces in continuation menu |
| `TestMeditateFinalisationExpensiveSpawnNow` | 1021 | `spawn_now` triggers cost-ack re-presentation; cancel falls back to `queue`; proceed defers spawning until after adversarial review |
| `TestMeditateFinalisationPersistence` | 1049 | `finalisation-enhancements.yml` schema has all fields; `decided_at_utc` filled by calling agent; linked from Branch & Leaf Index; unchosen items surface in continuation menu |
| `TestMeditateFinalisationContinuationMenu` | 1081 | Step 12 has section headings (K10c groups); unchosen enhancement options include title; queued expensive options trigger cost-ack |
| `TestMeditateFinalisationFiniteIteration` | 1104 | Gate fires at most once per meditation; cheap items contribute to iter-1 respawn; iteration cap remains 3; `ESCALATE` remains verdict at iter 3 |
| `TestMeditateFinalisationTripleReasonRespawn` | 1136 | Triple-reason ordering documented; accepted enhancements processed first; report skill processes in order (cheap → viz → sections) |
| `TestMeditateK10EnsembleLayeredCadence` | 1167 | Per-tree YAMLs documented; per-tree YAML has `source_tree` field; per-tree YAML has `surfaced_to_root` placeholder; root combined YAML documented; `surfaced_to_root` annotation documented; single root askQuestion documented; root ranking by composite score; single-model backwards-compat; per-tree vs cross-model report respawn targeting |
| `TestMeditateK10EnsembleContinuationMenuLayered` | 1222 | Per-tree-only items have provenance label; root unchosen items have provenance label; per-tree-only item targets per-tree report respawn |
| `TestMeditateK10QuickModeFires` | 1245 | Gate fires in Quick mode; Quick mode same 0–5 cap; Quick mode skip-all backwards-compat |
| `TestMeditateK10ReflectionRubric` | 1265 | Rubric documented in agent file; both axes use 1–10 scale; worked example impact_score 9; worked example impact_score 5; (also worked example insight_value_score 9 + minimum_impact_threshold defaults to 6) |
| `TestMeditateK10WeightsConfigurable` | 1308 | `weights` key documented; default weights are 1.0; formula defaults to multiplicative `product`; weights configurable via `cruxMemories.meditate.finalisationEnhancements.weights` |

**Net richness coverage**: 28 new test classes containing ≈147 new test methods (all additive — zero pre-existing assertions deleted per Requirement 12).

#### 10.3.2 `evals/sdk/tests/q-meditate.test.ts` (576 lines — 7 describe blocks total: 3 pre-existing Q1–Q3 + 4 NEW richness blocks)

**3 pre-existing describe blocks** — unchanged from 20260517 freeze §10 / pre-richness baseline:

| Describe block | Line | Tests | Asserts |
|----------------|------|-------|---------|
| `Q1: Meditate - No Arguments (Context-Derived Facets)` | 201 | 3 `it` blocks | Facet derivation language; spawns subagents (literal `crux-cursor-memory-manager`); references memories in consolidated output |
| `Q2: Meditate - Topic Argument` | 290 | 2 `it` blocks | Derives facets from topic; produces consolidated insights referencing memories |
| `Q3: Meditate - File/Folder References` | 357 | 1 `it` block | Derives facets from file/folder reference |

**4 NEW richness describe blocks** (introduced by S06):

| Describe block | Line | Tests | Asserts |
|----------------|------|-------|---------|
| `Q: Meditate — Structural: K2 Merged Cost+Richness Gate` | 400 | 6 `it` blocks | `Q-Cost-and-Richness-Acknowledgment` exists; no standalone `Q-Comprehensiveness`; all 4 richness enum values documented; `default` preselected; mode-swap preserves richness selection; K1 dual-meaning callout present |
| `Q: Meditate — Structural: K10 Finalisation Enhancement Gate` | 441 | 5 `it` blocks | `Q-Finalisation-Enhancements` documented; multi-select 0–5; fires after consolidation before adversarial review; skip-all reproduces today's behaviour; cheap items bundle into respawn / expensive default queue |
| `Q: Meditate — Structural: K10 Reflection Rubric` | 477 | 5 `it` blocks | Impact × insight-value rubric documented in agent; both axes 1–10; `minimum_impact_threshold` defaults to 6; worked examples for impact 9/5/2 present; weights configurable |
| `Q: Meditate — Structural: K9 Respawn Protocol` | 515 | 3 `it` blocks | Respawn protocol documented with all required payload keys; respawn shares ≤3 iteration cap + `ESCALATE` at iter 3; triple-reason ordering (accepted_enhancements first) |
| `Q: Meditate — Structural: K10 Ensemble Layered Cadence` | 558 | 3 `it` blocks | Per-tree YAML schema has `source_tree` and `surfaced_to_root` fields; root combined YAML has `cross_model_candidates` and `union_candidates`; single root askQuestion at ensemble root |

**Net SDK richness coverage**: 4 new describe blocks containing 22 new `it` tests (all additive — zero pre-existing tests deleted).

#### 10.3.3 `evals/test_p_amnesia.py` (unchanged)

The `EXPLICIT_MEMORY_COMMANDS` row listing `/crux-meditate` is unchanged. No richness-spec additions touch this file.

### 10.4 Mapping summary by contract section

| Freeze section | Command source | Agent source | Eval source |
|----------------|----------------|--------------|-------------|
| §1 Modes inventory (incl. richness × depth cost table) | 20–28, 38–46, 60–67, 142–163 | 279–305 | `TestMeditateMergedCostAndRichnessGate::test_cost_estimates_per_depth_richness_combination` |
| §2 Calling-agent gates (Q-Depth + Q-Cost-and-Richness merged + read-only-richness + Theme + comprehensiveness payload + Q-Finalisation-Enhancements) | 55–256, 257–390, 1062–1186 | 303–307, 307–337, 596–700 | `TestMeditateMergedCostAndRichnessGate`, `TestMeditateReadOnlyRichnessVariant`, `TestMeditateFinalisationEnhancementGate` |
| §3 Pattern A/B boundaries (incl. K10 + combined Pattern-B + Dim 13 respawn bypass) | 34–36, 391–662, 1062–1186, 1291–1306, 1368–1446 | 17–46, 302–339 | `TestMeditateCombinedFacetConfirmation`, `TestMeditateRespawnProtocol` |
| §4 Subagent contracts — depth-0 manager steps 1–13 (incl. step 4b + step 8 K10c + step 8b K10b) | (mirror) 792–845, 1062–1186 | 399–748 | `TestMeditateInitSuggestions`, `TestMeditatePayloadPropagation`, `TestMeditateK10ReflectionRubric` |
| §4 Subagent contracts — Phases A–G (incl. leaf comprehensiveness honouring) | (mirror) 792–821 | 776–864 | `TestMeditatePayloadPropagation::test_propagated_to_children_in_phase_d` |
| §4 Subagent contracts — Quick 6-step (incl. leaf comprehensiveness honouring) | 823–845 | 866–909 | `TestMeditatePayloadPropagation::test_propagated_in_quick_mode`, `TestMeditateK10QuickModeFires` |
| §4 Subagent contracts — Ensemble Aggregation (incl. K10 layered cadence 3b–3f) | 847–919, 1153–1184, 1979–2132 | 1189–1349 | `TestMeditateK10EnsembleLayeredCadence`, `TestMeditateK10EnsembleContinuationMenuLayered` |
| §4 Subagent contracts — Adversarial Review (**13 dims**, severities, ≤3 iters, MUST_FIX schema, **Dim 13 respawn**) | 1187–1446 | 726–730, 1150 | `TestMeditateAdversarialReviewerExtension`, `TestMeditateRespawnProtocol`, `TestMeditateRespawnFiniteIteration` |
| §4 4-mode focus-area reconciliation (step 4b) | 391–662 | 505–514 | `TestMeditateInitSuggestions::test_four_opt_in_modes_documented` |
| §4 `init-suggestions-{ts}.yml` schema | 740–784, 1807–1821 | 517–566 | `TestMeditateInitSuggestions::test_init_suggestions_schema_fields` |
| §4 K10c rubric + catalogue + `finalisation-enhancements.yml` schema | 1062–1186, 1368–1446 | 596–700 | `TestMeditateK10ReflectionRubric`, `TestMeditateFinalisationPersistence`, `TestMeditateK10WeightsConfigurable` |
| §5 Coordination conventions (filenames + globs + locks + citations + peer review + retro + B&L index — extended with init-suggestions + finalisation-enhancements + follow-ups) | 740–784, 988–1059 | 345–397, 923–1036, 1063–1100 | (multiple per row) |
| §6 Mandatory report contract — incl. Comprehensiveness Level Mapping + Per-Branch / Depth-3 / Peer-Review Surfacing + Init-Suggestions Honour + K10b Per-Cheap-Type + Report-Skill Respawn Protocol | 1539–1977 | 734–744, 1152–1157 | `TestMeditateComprehensivenessLevelMapping`, `TestMeditateBackwardsCompatibility`, `TestMeditateFinalisationCheapAcceptRespawn`, `TestMeditateFinalisationTripleReasonRespawn` |
| §7 Continuation menu — extended with K10c groups (unchosen + queued spawn-now) | 921–986 | 769–774 | `TestMeditateFinalisationContinuationMenu`, `TestMeditateFinalisationExpensiveSpawnNow` |
| §8 Subject-Matter Focus rule | 1448–1468 | 1154 | `TestMeditateSafeguardRegressions::test_subject_matter_focus_rule_present` |
| §9 Cross-repo touchpoints | (n/a — external) | (n/a — external) | `TestMeditateNoNewDistFilesK8`, `TestMeditateSafeguardRegressions` |

---

## Definition of Done — Refresh 2026-05-24

- [x] New freeze document exists at `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260524.md`.
- [x] Every richness-introduced contract item back-traced to a working-tree source line range or section heading (Section 10).
- [x] Document referenced from spec index Execution Notes (S02 dependency unblock — see `spec-meditate-agent-skill-decomposition-20260517.md` Execution Notes).
- [x] Predecessor freeze `meditate-frozen-contract-20260517.md` carries a 2026-05-24 supersession banner pointing at this file.
- [x] S01 brief (`subtask-01-meditate-decomp-contract-capture-20260517.md`) carries an appended `## Refresh 2026-05-24` section recording the new freeze artefact and the one-paragraph rationale.
- [x] Markdown-only artefact; no linter errors introduced.

---

_Captured by `crux-platform-architect` against repo `/home/andrewv/git/cursor/CRUX-Compress` at working-tree state of git SHA `b4fc33b0c034866bb60b7fe7b03be9e0c7a18bbf` + unstaged 20260523 richness changes on 2026-05-24. Subsequent subtasks (S02–S12) of `specs/20260517-meditate-agent-skill-decomposition/` must treat this document as the **freeze line** — any deviation requires an explicit `needs_user_input` escalation surfaced through the calling agent. The 20260517 freeze remains as an audit-trail artefact only; do not consume it as the contract baseline._
