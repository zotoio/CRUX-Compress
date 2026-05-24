# crux-meditate

Recursive memory-informed exploration of themes, topics, and intent through 3-level deep agent inception.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-meditate                          - Explore facets derived from current chat context
/crux-meditate "topic or question"      - Explore a specific theme
/crux-meditate @file.ts @folder/        - Explore facets around referenced code
/crux-meditate --quick "topic"          - Fast parallel-fanout exploration (legacy behaviour)
/crux-meditate --random-model "topic"   - One tree, model randomly picked from `cruxMemories.meditate.modelPool` (same agent count as default)
/crux-meditate --model-per-branch "topic" - One tree, each top-level facet branch assigned a model from the pool; descendants inherit (same agent count as default)
/crux-meditate --ensemble "topic"       - Ensemble max: run on every model in the pool in parallel, then aggregate
/crux-meditate --ensemble --quick "topic" - Ensemble max of Quick-mode trees
```

The `--quick`, `--random-model`, `--model-per-branch`, and `--ensemble` flags may appear anywhere in `$ARGUMENTS`. `--quick` may be combined with any of the model-strategy flags. **`--random-model`, `--model-per-branch`, and `--ensemble` are mutually exclusive** — passing more than one aborts with an error.

## Modes

Two orthogonal axes control a meditation: the **recursion mode** (Research vs Quick) and the **model strategy** (how `cruxMemories.meditate.modelPool` is used, if at all).

### Recursion mode

| Mode | Flag | Default? | Behaviour |
|------|------|----------|-----------|
| **Research** | _(none — default)_ | yes | Depth-first serial recursion. Each depth's findings drive the next depth's facet derivation. Globally unique facet allocation across all branches. Bottom-up incorporation. Branch peer review at the top. **Mandatory citations at every step.** |
| **Quick** | `--quick` | no | Fast parallel fan-out (legacy behaviour). All 3 facets per node derived upfront and explored in parallel. **Citations are still mandatory** (same `## Citations` requirement as Research mode), but the parent validates them best-effort and warns rather than re-spawning offending children. Use when you want speed over rigor. |

### Model strategy

The model strategy is an orthogonal axis that controls how `cruxMemories.meditate.modelPool` is used. All four values are combinable with either recursion mode.

| Strategy | Flag | Trees | Agent count | Cross-model synthesis report? |
|----------|------|-------|-------------|-------------------------------|
| **Single** (default) | _(none)_ | 1, on the caller's model | baseline (see depth table) | no |
| **Random model** | `--random-model` | 1, on a model randomly picked from `cruxMemories.meditate.modelPool` at the start of the meditation | same as baseline | no |
| **Model per branch** | `--model-per-branch` | 1, each top-level facet branch is assigned a distinct model from the pool (sampling without replacement when `poolSize ≥ branchCount`, otherwise round-robin); all descendants in that branch inherit the assigned model | same as baseline | no |
| **Ensemble (max)** | `--ensemble` | N parallel trees (one per pool entry), then 1 aggregator | `~N × baseline + 1` | yes (`cross-model-synthesis.md` + ensemble report pair) |

**Common ground & strategy selection**: every model strategy shares every user-facing safeguard (cost ack with richness selection, theme preflight, combined facet/sections/visualisations/focus-areas confirmation, post-consolidation `Q-Finalisation-Enhancements` gate, Branch & Leaf Index update, mandatory adversarial review-and-fix cycle, mandatory paired HTML+PDF report). Random and Model-per-branch produce single-tree artifacts (no `model-{slug}/` subdirs, no `cross-model-synthesis.md`, no `ensemble-report-*` pair) and only change which model executes which agent; Ensemble Max is the only strategy that runs the Ensemble Protocol with parallel trees and cross-model aggregation. The cost-and-richness gate offers in-place swaps whenever `cruxMemories.meditate.modelPool` has ≥1 entry (Random) or ≥2 entries (Per-Branch, Ensemble Max) — see **Sub-Q2** of `Q-Cost-and-Richness-Acknowledgment` below.

## Instructions

When this command is invoked, spawn a `crux-cursor-meditation-guide` subagent. The guide agent orchestrates the 3-level recursive exploration using the skills it loads (`crux-skill-memory-meditation-research` for Research mode, `crux-skill-memory-meditation-quick` for Quick mode), querying memories, expanding on discoveries, and writing consolidated insights to markdown files in a shared working directory.

**User input escalation — CRITICAL**: This command uses **Pattern B (work first, then escalate)** — the subagent tree must complete its recursive exploration before the user can decide on next steps. Subagents in the meditation tree NEVER call `AskQuestion` directly. ALL user-facing interactions (selecting expansion directions, saving as spec/report, ending meditation) are handled by the **parent agent** (you) using `AskQuestion` after the subagent tree completes.

**Critical**: All agents coordinate through markdown files in `meditations/{yyyymmdd}-{topic-slug}/`, not through in-context return values or JSONL transcript polling. The subagent performs **steps 1–8** (mode-specific — see **What Happens** below) and writes `consolidation.md` to the working directory. You then read that file and handle **steps 9–12** directly with the user. Four mandatory pre-spawn user gates — **Depth Selection**, **Cost & Scope Acknowledgment** (merged `Q-Cost-and-Richness-Acknowledgment` gate), **Theme Preflight**, and (mid-flow) **combined Facet / Sections / Visualisations / Focus-Areas Confirmation** — fire before the subagent tree spawns; see the dedicated sections below. A fifth calling-agent gate, **`Q-Finalisation-Enhancements`**, fires post-consolidation before adversarial review.

### Argument Handling

**Mode selection (perform before topic-slug derivation)**: Inspect the raw `$ARGUMENTS` string for the `--quick`, `--random-model`, `--model-per-branch`, and `--ensemble` flags (case-sensitive, surrounded by whitespace or at the start/end of the string).

Recursion mode:

- If `--quick` is present → set `meditateMode: "quick"` and follow the **Quick mode protocol**. **Strip the flag from `$ARGUMENTS` before deriving the topic-slug** so the slug never contains `--quick`.
- Otherwise → set `meditateMode: "research"` (the default and recommended path for any work that will be cited, persisted, or used to drive downstream changes).

Model strategy (the four flags are mutually exclusive — abort with `"--random-model, --model-per-branch, and --ensemble are mutually exclusive; pass at most one"` if more than one is present):

- If `--random-model` is present → set `modelStrategy.mode: "random"`. Read `cruxMemories.meditate.modelPool` from `.crux/crux-memories.json`. If the pool is empty or missing, abort with: `"--random-model requires cruxMemories.meditate.modelPool in .crux/crux-memories.json — configure at least 1 model entry"`. Pick a single model uniformly at random from the pool and record it as `modelStrategy.resolved_model_slug` / `resolved_model_label`. **Strip the flag** before deriving the topic-slug.
- If `--model-per-branch` is present → set `modelStrategy.mode: "per_branch"`. Read `cruxMemories.meditate.modelPool`. If the pool is empty or missing, abort with: `"--model-per-branch requires cruxMemories.meditate.modelPool in .crux/crux-memories.json — configure at least 1 model entry"`. The per-branch assignment is computed after facet confirmation (see step 4b of the depth-0 manager workflow) once the final branch count is known. **Strip the flag** before deriving the topic-slug.
- If `--ensemble` is present → set `modelStrategy.mode: "ensemble_max"` (also referred to as `ensembleMode: true` for backwards compatibility with the existing Ensemble Protocol section). Read `cruxMemories.meditate.modelPool`. If the pool is empty or has fewer than 2 entries, abort with a clear error pointing the user at the config. `--ensemble` can combine with `--quick` (ensemble of Quick-mode trees) or run with default Research mode. **Strip the flag** before deriving the topic-slug.
- If none of the model-strategy flags are present → set `modelStrategy.mode: "none"` (the caller's own model runs the whole tree).

**Per-branch assignment policy** (`modelStrategy.mode == "per_branch"`): the depth-0 manager resolves `modelStrategy.branch_assignments[]` in step 4b — after facet confirmation and any cost-ack re-presentation — using a deterministic shuffle of `cruxMemories.meditate.modelPool`. When `poolSize ≥ branchCount`, sample without replacement (each branch gets a distinct model); otherwise round-robin (some branches share a model) and set `assignment_policy_note` accordingly. The verbatim resolution algorithm (seed derivation, branch-count computation including `additional_facet` opt-ins, round-robin warning string) lives in step 4b of the `crux-skill-memory-meditation-research` and `crux-skill-memory-meditation-quick` skills; the resolved assignments are surfaced in `facets.md` per the `crux-skill-memory-meditation-coordination` skill.

Propagate the resolved `meditateMode` and `modelStrategy` into the depth-0 subagent's task prompt; the subagent in turn forwards both unchanged to every child it spawns (with `modelStrategy.resolved_model_slug` or `modelStrategy.branch_assignments[branch_index]` used to drive per-spawn `model:` selection — see the **Model Strategy Payload** section below). When `modelStrategy.mode == "ensemble_max"`, propagate `meditateMode` to each model-specific depth-0 subagent and the per-tree `modelStrategy` is effectively `mode: "random"` pinned to that tree's model (handled internally by the Ensemble Protocol).

**Remaining argument handling** (applied to the flag-stripped `$ARGUMENTS`):

- **No arguments**: The manager examines the current chat context — conversation history, open files, recent activity — to derive three exploration facets (theme, topic, intent). Pass the stripped `$ARGUMENTS` to the subagent.
- **Quoted text** (e.g. `"how should we handle caching"`): Use the provided text as the seed topic. The manager derives three facets from it. Pass the stripped `$ARGUMENTS` to the subagent.
- **File/folder references** (e.g. `@src/auth/ @config.ts`): The manager examines the referenced code to derive facets around its architecture, patterns, and purpose. Pass the stripped `$ARGUMENTS` to the subagent.
- **Mixed input**: Any combination of text, files, folders, images, or past chat references. The manager synthesizes all inputs to derive facets.

### Depth Selection — MANDATORY (calling agent's very first action)

The exploration depth controls how many levels of recursive subfocus derivation run. Deeper trees produce more thorough analysis but spawn more agents and take longer. The calling agent **must** ask the user to choose a depth before anything else — before Cost Acknowledgment, before Theme Preflight, before spawning anything — because the depth determines the agent count shown in the cost prompt.

#### Agent count by depth and mode

| Depth | Research agents (per tree) | Quick agents (per tree) | Tree shape |
|-------|---------------------------|------------------------|------------|
| **1** | ~8 (1 depth-0 + 3 depth-1 + 3 peer reviewers + 1 adversarial) | ~5 (1 depth-0 + 3 depth-1 + 1 adversarial) | 3 branches only — broad survey |
| **2** | ~17 (1 depth-0 + 3 depth-1 + 9 depth-2 + 3 peer reviewers + 1 adversarial) | ~14 (1 depth-0 + 3 depth-1 + 9 depth-2 + 1 adversarial) | 3 branches × 3 sub-branches — detailed analysis |
| **3** (default) | ~45 (1 depth-0 + 3 depth-1 + 9 depth-2 + 27 depth-3 + 3 peer reviewers + 1 adversarial) | ~42 (same minus peer reviewers) | 3 × 3 × 3 — deep research |

Adversarial review counts 1 agent at minimum; it may run up to 3 iterations. Ensemble mode multiplies the per-tree count by N (model pool size) and adds 1 aggregation agent.

#### Q-Depth-Selection (mandatory single-select)

Prompt:

    Choose the exploration depth for this meditation. Deeper levels produce
    more thorough analysis but spawn more agents and take longer.

      Depth 1 — Broad survey (~{N1} agents in {mode})
        3 top-level branches explore your facets directly. No sub-branches.
        Best for quick overviews, narrow topics, or when you want a fast
        first pass before deciding whether to go deeper.

      Depth 2 — Detailed analysis (~{N2} agents in {mode})
        Each branch spawns 3 sub-branches (9 sub-branches total), exploring
        narrower angles derived from the first level's findings. Good balance
        of depth and cost for most topics.

      Depth 3 — Deep research (~{N3} agents in {mode}, default)
        Each sub-branch spawns 3 more leaf agents (27 leaf agents total),
        producing the most thorough exploration. Best for complex strategic
        topics where you want every angle covered to maximum depth.

Substitute `{N1}`, `{N2}`, `{N3}` with the accurate agent counts from the table above for the currently-active `meditateMode`, and `{mode}` with "Research" or "Quick".

Options (single-select):

- `depth_1` — Depth 1: Broad survey (~{N1} agents)
- `depth_2` — Depth 2: Detailed analysis (~{N2} agents)
- `depth_3` — Depth 3: Deep research (~{N3} agents) **[default — preselected]**

#### Depth selection behaviour rules

- **Always run on the first invocation** in a session, regardless of arguments.
- **Store the result** as `maxDepth` (1, 2, or 3). This value is propagated to the depth-0 subagent and forwarded unchanged to every child agent in the tree.
- **Expansion-direction continuation** (calling agent step 12): reuse the previous `maxDepth` by default; the calling agent may offer a one-line "keep depth setting?" follow-up but does not re-run the full Q-Depth-Selection.
- **Non-interactive sessions** (e.g. CI): default to depth 3 without prompting.

### Cost & Scope Acknowledgment — MANDATORY (calling agent's second action)

`/crux-meditate` is **not** a quick chat replacement. Every invocation spawns a recursive research tree, generates infographic-rich HTML and PDF reports, and runs a multi-iteration adversarial review cycle. It is intentionally **more expensive** than a regular prompt or chat session and is intended for **well-considered problem statements tied to high-value strategic activities** — architecture decisions, multi-month initiatives, major investment analyses, organisational strategy, deep technical research, etc.

After Depth Selection, the calling agent runs a single `askQuestion` — `Q-Cost-and-Richness-Acknowledgment` — that surfaces the cost-and-scope tradeoff (using the accurate agent count for the selected depth) AND lets the user select a comprehensiveness (richness) level. The richness level is **set once per invocation** (per K6 — see set-once rule below) and controls how much research material reaches the final report.

#### Approximate agent count and runtime per mode

| Mode + Model Strategy | Agent count (at selected depth) | Runtime (typical) | Use when |
|------|---------------------------------|-------------------|----------|
| **Research** (default, single model) | ~{researchCount} agents (see depth table above) | minutes to tens of minutes depending on depth | High-stakes strategic problems where citation rigor, peer review, and incorporation depth justify the cost |
| **Quick** (`--quick`, single model) | ~{quickCount} agents (same tree minus peer reviewers) | substantially faster | Broad early-stage exploration where citations are still required but peer-review and citation re-spawn enforcement are not |
| **Research / Quick + Random Model** (`--random-model`) | identical to Research / Quick baseline (same tree, different model) | identical to baseline | Single-tree run on a non-default model perspective; useful for cheap diversity sampling across multiple invocations |
| **Research / Quick + Model per Branch** (`--model-per-branch`) | identical to Research / Quick baseline; each of the 3 top-level branches (plus any `additional_facet` opt-ins) runs on a different model from the pool | identical to baseline (parallel branches; longest branch dominates) | Single-tree run that compares how different models explore different facets — cheaper than Ensemble Max while still surfacing model-attribution differences |
| **Ensemble Max + Research** (`--ensemble`) | ~{N×researchCount + 1} agents ({N} complete Research trees + 1 cross-model aggregation agent), where N = length of `cruxMemories.meditate.modelPool` | N× Research runtime (parallel) + aggregation | Maximum-confidence analysis where cross-model convergence/divergence is the deliverable |
| **Ensemble Max + Quick** (`--ensemble --quick`) | ~{N×quickCount + 1} agents ({N} complete Quick trees + 1 aggregation agent) | N× Quick runtime (parallel) + aggregation | Broad ensemble exploration when speed matters more than per-tree rigor |

Substitute `{researchCount}` and `{quickCount}` with the accurate per-tree agent counts from the **Agent count by depth and mode** table for the user's selected `maxDepth`. These counts exclude the calling agent itself and the per-iteration adversarial review subagents (which can run 1–3 times per model tree depending on findings).

#### Q-Cost-and-Richness-Acknowledgment (mandatory single-select — two sub-questions)

This is the merged gate that simultaneously presents the cost tradeoff (Sub-Q2) and the richness level selection (Sub-Q1). It replaces the legacy `Q-Cost-Acknowledgment` gate. Richness selection is **folded into this gate as Sub-Q1** (per K2) — there is no separate standalone richness-selection gate.

**Prompt preamble** (displayed before the two sub-questions):

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

Substitute `{N_compact}`, `{N_default}`, `{N_detailed}`, `{N_exhaustive}` with the accurate per-tree agent counts from the worked-example cost tables for the selected `maxDepth`. For the standard case (depth=3, Research, 3 facets): compact~45, default~45, detailed~45, exhaustive~72. For Ensemble, multiply per-tree counts by `poolSize` and add 1 aggregator. For Quick mode, subtract peer reviewers (3 at depth-3) from each row. Substitute `{N_aggregator}` with the pool size.

When `modelStrategy.mode == "ensemble_max"` (`ensembleMode: true`), replace the first paragraph of the preamble with:

    /crux-meditate --ensemble will run {poolSize} complete depth-{maxDepth} meditation
    trees in parallel — one per model family ({modelLabels}) — spawning approximately
    {N} agents total, then aggregate findings into a cross-model synthesis report
    highlighting where models converge (high confidence), diverge (needs investigation),
    and surface unique insights.

    Each model tree produces its own full HTML + PDF report with infographics, and the
    ensemble aggregation produces a separate cross-model synthesis report. All trees
    share the same user-confirmed facets for apples-to-apples comparison.

When `modelStrategy.mode == "random"`, append before Sub-Q1:

    Model strategy: random — single tree, entire tree runs on a randomly-selected
    pool model. Picked: {resolved_model_label}. Agent count unchanged from baseline.

When `modelStrategy.mode == "per_branch"`, append before Sub-Q1:

    Model strategy: model-per-branch — single tree. Depth-0 manager runs on caller's
    model; each of {branchCount} top-level branches assigned a distinct pool model
    (sampling without replacement when poolSize >= branchCount, otherwise round-robin);
    descendants inherit. Agent count unchanged; report includes per-branch attribution.

**Sub-Q1 — Richness level** (single-select, **preselected = the level literally named `default`**):

The `default` level is both the name of the preselected option AND the enum value that propagates through the `comprehensiveness:` payload. This dual meaning is intentional per K1's naming-reconciliation paragraph — "default-when-unspecified" and "default richness level" are the same thing.

Options:

- `compact` — **Compact — pre-richness behaviour.** Reproduces the meditate report shipped before this spec (≥4 charts, ≥3 infographics, ≥1 calculator, depth-3 elided beyond summary, consolidation-only sections). Lowest token cost (~25k tokens). Pick when you want a backwards-compatible run or when token budget is tight. NOTE: this level reproduces pre-richness behaviour for users who want the legacy minima.
- `default` **[preselected]** — **Default — new default richness.** The new default-when-unspecified richness (5 charts / 4 infographics / 1 calculator, `branch_summary` per-branch sections, ~1.6× richer prose, ~40k tokens). Pick when you want the richer baseline without exhaustive cost. NOTE: the level *name* `default` matches the preselected option — these are not in conflict (per K1's naming-reconciliation paragraph; the level enum value `default` is what propagates through the `comprehensiveness:` payload).
- `detailed` — **Detailed — substantial bump.** 7 charts / 6 infographics / 2 calculators / `per_leaf_detail` per-branch sections / depth-3 `verbatim_quotes` / peer-review `named_section` (~60k tokens). Pick when stakeholders need every angle.
- `exhaustive` — **Exhaustive — maximum richness.** 10 charts / 8 infographics / 3 calculators / per-finding citation columns / `per_branch_dedicated` peer-review / `per_leaf_attribution` ensemble (~90k tokens). Spawns +27 per-leaf citation-builder agents at depth 3 in Research (Quick mode is warn-only per OQ #5).

**Sub-Q2 — Proceed / mode-swap / cancel** (no preselection — proceed is NOT auto-selected; non-interactive sessions abort):

Recursion-mode swap options (always offered):

- `proceed` — Yes, this is a high-value strategic problem; proceed in the currently-selected recursion mode and model strategy (`Research` or `Quick`, depth {maxDepth}, with the current model strategy)
- `switch_to_quick` — Proceed but switch to Quick mode (~{quickCount} agents at depth {maxDepth}, faster, no peer review). **Richness and model strategy preserved across swap.** **Only offered when current mode = Research.**
- `switch_to_research` — Proceed but switch to Research mode (~{researchCount} agents at depth {maxDepth}, peer-reviewed, slower). **Richness and model strategy preserved across swap.** **Only offered when current mode = Quick.**

Model-strategy swap options (offered conditionally — only those whose minimum pool size is satisfied appear, and the option matching the currently-active strategy is omitted):

- `switch_to_single` — Run on a single model (the caller's own model) (~{perModelCount} agents). **Only offered when `modelStrategy.mode ≠ "none"`.**
- `switch_to_random_model` — Random model from the pool (~{perModelCount} agents — same agent count as `single`; one model picked uniformly at random from `cruxMemories.meditate.modelPool` powers the whole tree). **Only offered when `modelStrategy.mode ≠ "random"` AND `poolSize ≥ 1`.**
- `switch_to_model_per_branch` — Model per branch (~{perModelCount} agents — same agent count as `single`; each top-level facet branch is assigned a distinct model from the pool, descendants inherit). **Only offered when `modelStrategy.mode ≠ "per_branch"` AND `poolSize ≥ 1`.**
- `switch_to_ensemble` — Ensemble max (~{N×perModelCount + 1} agents across {N} model families + cross-model aggregation). **Only offered when `modelStrategy.mode ≠ "ensemble_max"` AND `poolSize ≥ 2`.**

Cancel:

- `cancel` — Cancel — I'll use a different approach

Substitute all `{...Count}` placeholders with the accurate agent counts from the depth table for the user's selected `maxDepth`.

**Mode-swap preserves richness**: the Sub-Q1 richness selection is preserved across any mode-swap or model-strategy-swap decision. The prompt prose already displays all 4 richness rows for the current mode; a swap recomputes the agent count but does not reset richness. Model-strategy-swap semantics: `switch_to_random_model` immediately picks `resolved_model_slug` uniformly at random from the pool; `switch_to_model_per_branch` defers `branch_assignments` resolution to step 4b; `switch_to_ensemble` enters the Ensemble Protocol below; `switch_to_single` resets to the caller's model. All swaps continue to Theme Preflight without re-prompting.

#### Behaviour rules

- **Always run on the first invocation** in a session, regardless of arguments. Depth Selection runs first, then `Q-Cost-and-Richness-Acknowledgment`.
- **Mode swaps**: if the user picks `switch_to_quick` or `switch_to_research`, update the active `meditateMode` for the rest of this invocation and proceed to Theme Preflight; do not re-ask `Q-Cost-and-Richness-Acknowledgment` or `Q-Depth-Selection`. If the user picks any model-strategy swap (`switch_to_single` / `switch_to_random_model` / `switch_to_model_per_branch` / `switch_to_ensemble`), update `modelStrategy.mode` accordingly (and resolve `resolved_model_slug` immediately for `random`; defer `branch_assignments` resolution to step 4b for `per_branch`) and proceed. **In all cases the richness selection from Sub-Q1 is preserved.**
- **Cancel**: respond with a short note acknowledging the cancellation and stop. Do not spawn anything, do not run Theme Preflight, do not create the working directory.
- **Richness set-once-per-invocation** (K6): the richness level selected in Sub-Q1 is stored as `selectedRichness` and propagated to the depth-0 subagent as part of the `comprehensiveness:` payload. It cannot be changed after this gate closes. Expansion-direction continuations (calling agent step 12) use the **read-only-richness variant** (see below) — richness is shown locked; no "keep richness setting?" follow-up is offered. Users who want to change richness must `cancel` and re-invoke `/crux-meditate`.
- **Expansion-direction continuation** (calling agent step 12 — when the user picks an expansion option after a previous meditation): run a **shortened** version of this acknowledgment (`Q-Cost-Acknowledgment-Expansion` — uses the **read-only-richness variant** with locked richness). The mode-swap and depth options are **not** re-offered (both persist across expansions); the user can `cancel` and re-invoke `/crux-meditate` if they want to change mode or depth.
- **Non-interactive sessions** (e.g. CI): if `askQuestion` cannot be answered, abort with a clear error explaining the cost-acknowledgment requirement. Never default to `proceed` silently — the safeguard exists precisely because the cost is non-trivial. (Sub-Q1 receives the non-interactive default `default` per K2; Sub-Q2 aborts rather than defaulting to `proceed`.)

#### Q-Cost-Acknowledgment-Expansion (read-only-richness variant)

Used when the user selects an expansion direction from the continuation menu (calling agent step 12). The mode-swap and depth options are NOT re-offered; richness is locked at the value set during the original `Q-Cost-and-Richness-Acknowledgment` gate.

**Preamble** (one line naming the trigger):

    You're continuing this meditation by expanding direction(s). Cost has been
    recomputed for the expansion tree.

**Richness display row** (locked — not interactive):

    Richness: {selectedRichness} (locked — set at the start of this invocation;
    cancel and re-invoke /crux-meditate to change)

**Prompt body** (follows richness display row):

    Expanding this meditation will spawn a new depth-{maxDepth} research tree
    (~{N} additional agents) exploring the selected direction(s). This carries
    the same per-meditation cost as the original invocation — a full recursive
    tree, adversarial review cycle, and paired HTML + PDF report.

    The previous meditation's results are preserved; this expansion produces a separate
    report. If you only need a quick follow-up, consider a regular chat prompt instead.

**Options** (Sub-Q2 only — Sub-Q1 richness is locked; no "keep richness setting?" follow-up is offered; the existing "keep deep-confirm setting?" follow-up is preserved unchanged):

- `proceed_expansion` — Yes, spawn the expansion tree
- `cancel` — Cancel — I'll follow up in chat instead

#### Read-only-richness variant (general)

The read-only-richness variant of `Q-Cost-and-Richness-Acknowledgment` is used whenever the gate re-fires after richness has been locked. In this variant:

- **Sub-Q1 (richness) is shown as a locked display row** (not interactive): `Richness: {locked_level} (locked — set at the start of this invocation; cancel and re-invoke /crux-meditate to change)`
- **Sub-Q2 (proceed/swap/cancel) remains fully interactive**
- The prompt prose is prefixed with a **one-line preamble naming the trigger** (see table below)
- The prompt title is **"Cost-and-Richness Acknowledgment (re-presented)"** per OQ #2

**Trigger preambles**:

| Trigger | Preamble |
|---------|----------|
| Expansion path (calling agent step 12) | `You're continuing this meditation by expanding direction(s). Cost has been recomputed for the expansion tree.` |
| Additional-facet acceptance | `Cost has changed because you accepted {N} additional facets — please re-acknowledge or cancel.` |
| `spawn_now` acceptance (K10b) | `You've accepted spawning {N} follow-up agent(s) for finalisation enhancements ({enumerated_types}). The new total agent count is ~{N_total} (current depth {D}, richness {level}, mode {mode}, including {N_finalisation} spawn-now agents).` |

**No re-presentation loop**: each trigger fires at most once per cause within a single invocation. After the user re-acknowledges or cancels, the variant cannot re-fire within the same trigger context.

### Theme Preflight — MANDATORY (calling agent runs before spawning the subagent)

Every meditation must be themed deliberately. AI-generated reports tend to converge on a recognisable homogenised aesthetic — purple-blue gradient hero, Inter-700 headlines, three-card feature grids, doughnut chart with tinted-circle legend, indigo-500 accent, lucide-style icon-in-tinted-circle, Tailwind-default look. **This is forbidden as a default.** See the **Anti-Homogenization Rules** in the `crux-skill-memory-meditation-report` skill for the canonical block-list.

To make sure each meditation produces a visually distinct, intentional report, the calling agent **must** run an `askQuestion` sequence **before** spawning the depth-0 subagent. This is **Pattern A (pre-collected answers)**: gather every theming choice up front, then pass them to the subagent as a structured `theming` payload. The subagent never re-asks.

The canonical **Anti-Homogenisation Rules** (forbidden defaults block-list, screenshot reference, and application contract) live in the `crux-skill-memory-meditation-report` skill (§6.3 of the report skill). The calling agent must enforce the "forbid_homogenised_defaults: true" flag in the theming payload it passes to the depth-0 subagent; the report skill validates and rejects any report that violates the block-list.

If the calling agent skips Theme Preflight, the report ends up looking like every other AI-generated report — this is a regression and a documentation defect. See the **Anti-Homogenization Rules** block in the `crux-skill-memory-meditation-report` skill for the canonical screenshot reference.

#### When to run the preflight

- **Always** on the first invocation of a meditation in a session.
- **Skip and reuse the previous answers** when re-spawning under "expansion direction" continuation (step 12).
- **Always re-run** if the user explicitly asks to retheme, or if `$ARGUMENTS` contains `--retheme`.

#### The question sequence

Use one `askQuestion` call per logical question. Stop early as soon as the answers are sufficient.

**Q1 — Theme source** (single-select, required):

- `match_repo` — "Match the existing styling of files in this repo (scan `package.json`, `tailwind.config.*`, `*.css`, `*.scss`, `theme/`, `styles/`, design tokens, README screenshots)"
- `preset` — "Pick from a curated set of distinct preset directions"
- `custom` — "I'll describe a custom theme"
- `surprise_me` — "Pick something unexpected and deliberately different from the homogenised default"

If `match_repo`: scan the repo for theming signals (font-family declarations, CSS custom properties / design tokens, Tailwind theme config, accent color usage, brand colors in README/logos). Summarise what you found and ask **Q1b**: "Found these signals: …. Use them?" with options `yes_use_them` / `yes_with_tweaks` / `no_pick_preset_instead`. If the scan finds nothing useful, fall through to Q2 with a note explaining why.

**Q2 — Style direction** (single-select, required only if Q1 ≠ `match_repo` or Q1b = `no_pick_preset_instead`):

- `editorial` — magazine layout, serif headlines, asymmetric grids, drop caps, pull-quotes
- `scientific` — monospace + serif body, dense tables, IEEE-style figures, footnoted references
- `minimal_typographic` — system fonts, generous whitespace, no gradients, single accent color
- `bold_maximalist` — high-contrast colour blocks, oversized type, hand-drawn or marker accents
- `retro_print` — newspaper or vintage technical-manual styling, textured backgrounds, classical fonts
- `brutalist` — raw HTML aesthetics, intentional rough edges, monospace, minimal CSS, mono-color blocks
- `terminal_dossier` — green-on-black or amber-on-black CRT styling, ASCII-art dividers, monospace
- `architectural_blueprint` — blueprint-paper background, technical-drawing line weights, all-caps labels
- `surprise_me` — pick one of the above the user has not seen recently in this session

**Q3 — Colour scheme** (single-select, required):

- `cool_default` — the chosen direction's intended cool palette
- `warm_palette` — earth tones, terracotta, ochre, deep red
- `monochrome` — single-hue scale, no chromatic accents
- `high_contrast_minimal` — black/white plus one bold accent
- `repo_inferred` — derived from Q1 repo-scan results (only available when source = `match_repo`)
- `custom_hex` — user supplies one or two hex codes (free text in a follow-up)

**Q4 — Typography** (single-select, required only when source ≠ `match_repo`):

- `serif_headings_sans_body`
- `sans_headings_sans_body`
- `mono_headings_mono_body`
- `serif_throughout`
- `mixed_distinctive` — pair two non-default fonts intentionally (e.g. Fraunces + JetBrains Mono); never just default-Inter

**Q5 — Confirmation** (single-select, always required):

Show a one-line summary of the chosen theming payload and ask: `confirm` / `restart_preflight` / `cancel_meditation`.

#### Hard rule (non-interactive)

If the user does not engage with `askQuestion` (e.g. running non-interactively in CI), pick the `surprise_me` path for both Q1 and Q2 with a **deterministic-but-non-default** selection seeded by the topic-slug, then proceed without confirmation. **Never silently fall back to the homogenised default look.**

#### Theming payload (passed to the depth-0 subagent)

The calling agent serialises the answers into a YAML-shaped payload and includes it in the subagent's spawn prompt as `theming:`:

```yaml
theming:
  source: "match_repo" | "preset" | "custom" | "surprise_me"
  matched_repo_signals:
    fonts: ["..."]
    palette: ["#hex", "..."]
    css_variables_file: "path/to/main.css"
    tailwind_config: "tailwind.config.ts"
    notes: "one-line summary of what we matched"
  preset:
    style_direction: "editorial" | "scientific" | "minimal_typographic" | "bold_maximalist" | "retro_print" | "brutalist" | "terminal_dossier" | "architectural_blueprint"
    color_scheme: "cool_default" | "warm_palette" | "monochrome" | "high_contrast_minimal" | "repo_inferred" | "custom_hex"
    custom_hex_values: ["#hex", "..."]
    typography: "serif_headings_sans_body" | "sans_headings_sans_body" | "mono_headings_mono_body" | "serif_throughout" | "mixed_distinctive"
  custom:
    description: "free-text description from the user"
  default_color_mode: "dark"
  enable_color_toggle: true
  pdf_color_mode: "light_high_contrast"
  forbid_homogenised_defaults: true
```

The depth-0 subagent must use this payload to drive every visual choice in the report and propagate it unchanged to every child agent in the tree.

#### Comprehensiveness payload (passed to the depth-0 subagent alongside `theming:`)

The calling agent serialises the richness selection (from Sub-Q1 of `Q-Cost-and-Richness-Acknowledgment`) into a `comprehensiveness:` payload and includes it in the subagent's spawn prompt alongside `theming:`. The depth-0 subagent propagates it unchanged to every child agent in the tree (per K5 set-once-per-invocation rule). **Subagents MUST abort if `comprehensiveness:` is missing from spawn prompt** with error: "`comprehensiveness:` payload required; missing from spawn prompt — caller misconfigured".

```yaml
comprehensiveness:
  level: "compact" | "default" | "detailed" | "exhaustive"   # from Sub-Q1 of Q-Cost-and-Richness-Acknowledgment
  minima:
    charts:
      count: 4 | 5 | 7 | 10                                  # per level mapping table (§3 of architecture design)
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

Substitute the correct values per level from the richness level mapping table.

#### Model Strategy payload (passed to the depth-0 subagent alongside `theming:` and `comprehensiveness:`)

The calling agent serialises the resolved model strategy into a `modelStrategy:` payload and includes it in the subagent's spawn prompt. The depth-0 subagent propagates it unchanged to every child agent in the tree. **Subagents MUST abort if `modelStrategy:` is missing from the spawn prompt** with the canonical error: "`modelStrategy:` payload required; missing from spawn prompt — caller misconfigured".

```yaml
modelStrategy:
  mode: "none" | "random" | "per_branch" | "ensemble_max"
  pool: [{slug, label}, ...]            # full modelPool from .crux/crux-memories.json
  resolved_model_slug: null | "<slug>"   # set for mode: "random"
  resolved_model_label: null | "<label>"
  branch_assignments: []                 # set for mode: "per_branch" in step 4b
    # - { branch_index: N, slug: "<slug>", label: "<label>" }
  assignment_policy_note: null           # set when mode == "per_branch" and poolSize < branchCount
```

**Per-spawn `model:` selection rules** (four-case table — verbatim implementation lives in the `crux-cursor-meditation-guide` agent's step 5 / 7 / 10 and the research/quick skills):

- `mode: "none"` → omit `model:` from every Task invocation (use the caller's model).
- `mode: "random"` → pass `model: modelStrategy.resolved_model_slug` on every Task invocation in the entire tree (children, peer reviewers, adversarial reviewer).
- `mode: "per_branch"` → at the depth-0 → depth-1 spawn, look up `modelStrategy.branch_assignments[branch_index].slug` and pass as `model:`; that depth-1 agent records the slug as its own `ensembleModel` and propagates to descendants. **Peer reviewers and the adversarial reviewer run on the caller's model** (no `model:` parameter) so the cross-branch evaluator stays unified.
- `mode: "ensemble_max"` → handled by the Ensemble Protocol below; each per-tree depth-0 manager receives an internally-pinned model and the cross-model aggregator uses `cruxMemories.meditate.ensembleAggregatorModel` (or the caller's model when unset).

**Legacy `ensembleModel` field**: the existing `ensembleModel` field carried in child spawn prompts remains the spawn-time `model:` carrier inside each subtree; it is **derived** from `modelStrategy` at the depth-0 manager (and at the depth-0 → depth-1 dispatch point for `per_branch`). The skills continue to consume `ensembleModel` unchanged.

The verbatim branch-assignment resolution algorithm (deterministic shuffle, seed derivation, round-robin warning string) lives in step 4b of the `crux-skill-memory-meditation-research` and `crux-skill-memory-meditation-quick` skills.

### Facet Confirmation — MANDATORY at depth 0, opt-in deeper

After the depth-0 subagent derives the **first 3 top-level facets** from the command contents (input args + chat context + referenced files), it **must** pause and let the user confirm or modify them before the meditation tree spawns. The first facet partitioning sets the entire shape of the exploration — every branch and every depth descends from it — so the user gets one mandatory checkpoint here.

Lower-level child subfocuses (depth-2 and depth-3) are **not** confirmed by default — they are derived autonomously from each parent's actual research findings. The user can opt in to deeper confirmation via a follow-up `askQuestion` immediately after the depth-0 confirm, with three granularities:

- `none` (default) — auto-derive at depth 2 and depth 3
- `depth_2_only` — pause to confirm depth-2 child subfocuses; auto-derive at depth 3
- `all_levels` — pause to confirm at depth 2 and depth 3

The choice becomes a `confirmDeepFacets` enum value passed to the depth-0 subagent and propagated unchanged to every child agent in the tree.

#### Depth-0 confirmation flow (Pattern B) — combined askQuestion

The depth-0 subagent derives 3 top-level facets PLUS 3–8 draft report sections, 5–10 candidate visualisations, and 0–5 additional focus areas. It writes all four blocks to `facets-pending-{ts}.yml` and returns a **combined `needs_user_input` block** to the calling agent. The calling agent then runs a **single `askQuestion` with 5 sub-questions** (facets + sections + visualisations + focus areas + deep_confirm) — one combined round trip replacing the legacy sequential Q-Confirm-1 + Q-Confirm-2 calls.

**`needs_user_input` schema** (returned by the depth-0 subagent):

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
      - index: 2
        title: "{facet-2-title}"
        subfocus: "{facet-2-subfocus}"
        slug: "{facet-2-slug}"
      - index: 3
        title: "{facet-3-title}"
        subfocus: "{facet-3-subfocus}"
        slug: "{facet-3-slug}"
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

**Combined `askQuestion` schema** (calling-agent-owned — Pattern B integrity preserved; subagents NEVER call AskQuestion):

```yaml
askQuestion:
  title: "Confirm meditation shape — facets, sections, visualisations, and additional focus areas"
  preamble: |
    The depth-0 seed exploration has produced 3 candidate facets +
    draft report sections + draft visualisations + additional focus
    areas. Confirm the facets and review the rest — most defaults are
    checked already; uncheck what you don't want. Each section / viz /
    focus area shows a one-line rationale and source signals so you can
    quickly tell which ones are well-grounded.
  multi_sub_question: true
  sub_questions:

    - id: "facets"
      kind: "single_select"
      required: true
      prompt: |
        These 3 facets define the entire shape of the meditation — every
        branch and every depth descends from them. Good facets are
        complementary (covering different angles of the topic),
        independently explorable (each can go deep without needing the
        others), and concretely scoped (a specific question or angle,
        not a vague theme).

        Facet 1: {facets[0].title}
          Subfocus: {facets[0].subfocus}
        Facet 2: {facets[1].title}
          Subfocus: {facets[1].subfocus}
        Facet 3: {facets[2].title}
          Subfocus: {facets[2].subfocus}

        If the facets look well-partitioned and you're happy with the
        exploration directions, confirm and proceed. If one feels too
        broad, overlapping, or missing a critical angle, modify it. If
        the overall partitioning feels wrong, regenerate for a fresh set
        (up to 3 attempts).
      options:
        - value: "confirm_all"
          label: "Confirm all 3 facets unchanged"
          decision_guidance: "Pick when the facets look well-partitioned."
        - value: "modify_one"
          label: "Change one facet (follow-up text input)"
          decision_guidance: "Pick when ONE facet feels too broad / off-topic / overlapping."
        - value: "modify_multiple"
          label: "Change multiple facets (follow-up text input)"
          decision_guidance: "Pick when 2+ facets need work."
        - value: "regenerate"
          label: "Discard these 3 and re-derive a different set"
          decision_guidance: "Pick when the overall partitioning feels wrong (capped at 3 attempts; the subagent will re-derive on resume)."
        - value: "cancel"
          label: "Abort the meditation entirely"
          decision_guidance: "Pick to stop now — no agents spawn, no report generated."

    - id: "sections"
      kind: "multi_select"
      required: false
      preselected_indices: "all"
      prompt: |
        Confirm the draft report sections to include. Each is checked by
        default — uncheck any you don't want. Source signals show what
        flagged each section so you can quickly scan for misfits.
      options:  # one option per candidate from prompt_inputs.sections
        - value: "section-{slug-N}"
          label: "[checked] {sections[N].title} — {sections[N].rationale}"
          source_signals: "{sections[N].source_signals}"
          decision_guidance: "Uncheck if irrelevant; the report will still cover this content if the meditation surfaces it organically."

    - id: "visualisations"
      kind: "multi_select"
      required: false
      preselected_indices: "all"
      prompt: |
        Confirm the visualisation types the report should render. Each
        is checked by default — uncheck any that don't fit the topic.
        The adversarial reviewer's Dim 13 will flag missing confirmed
        visualisations for a respawn.
      options:
        - value: "viz-{slug-N}"
          label: "[checked] {visualisations[N].type} — {visualisations[N].what_it_would_show}"
          source_signals: "{visualisations[N].source_signals}"
          decision_guidance: "Uncheck if this visualisation type doesn't fit the topic's natural shape."

    - id: "additional_focus_areas"
      kind: "per_item_single_select"
      required: false
      default_per_item: "skip"
      prompt: |
        For each additional focus area, choose how to handle it. The 4
        modes differ in cost:
          - skip: discard (zero cost; zero report effect)
          - additional_facet: add as a NEW facet (multiplies agent count
            by ~13 per facet at depth 3 Research; cost-ack re-fires when
            ANY choice is additional_facet or additional_facet_AND_section)
          - report_section_only: add as a new report section (no agent
            cost; section content sourced from across-branch findings;
            does NOT trigger cost-ack re-presentation)
          - additional_facet_AND_section: BOTH (new facet AND dedicated
            report section under user-specified title; same agent cost
            as additional_facet; cost-ack re-fires)
        Cost change rule: ANY choice of additional_facet or
        additional_facet_AND_section triggers the read-only-richness
        cost-ack re-presentation BEFORE the tree spawns.
      items:  # one per candidate from prompt_inputs.additional_focus_areas
        - id: "focus-{slug-N}"
          title: "{additional_focus_areas[N].title}"
          rationale: "{additional_focus_areas[N].rationale}"
          source_signals: "{additional_focus_areas[N].source_signals}"
          options:
            - value: "skip"
              label: "Skip — drop this focus area entirely"
              decision_guidance: "Pick when not relevant. Zero cost."
            - value: "additional_facet"
              label: "Add as new facet (+~14 agents at D=3 Research; +~13 at D=3 Quick; cost-ack re-fires)"
              decision_guidance: "Pick when the focus area warrants its own research branch. Bumps facet count → multiplies agent count."
              cost_change_signal: true
            - value: "report_section_only"
              label: "Add as new report section (no agent cost)"
              decision_guidance: "Pick when the topic warrants a dedicated section but no new exploration branch."
              cost_change_signal: false
            - value: "additional_facet_AND_section"
              label: "Both — new facet + dedicated named section (cost-ack re-fires; follow-up text for custom section title)"
              decision_guidance: "Pick when you want the new branch AND a named report section."
              cost_change_signal: true
              follow_up: "custom_report_section_title"

    - id: "deep_confirm"
      kind: "single_select"
      required: true
      preselected_value: "none"
      prompt: |
        By default, deeper subfocuses (depth 2 and 3) are derived
        autonomously from each parent's research findings — no further
        prompts. This is fastest and works well when the top-level facets
        are well-scoped.

        If you want more control, you can opt in to confirming subfocuses
        at deeper levels. Be aware of the latency trade-off:
          - depth_2_only adds up to 9 confirmation prompts (3 per branch × 3 branches)
          - all_levels adds up to 36 additional prompts (9 at depth 2 + 27 at depth 3)
        Each prompt pauses the exploration tree until you respond.

        For most meditations, "none" is recommended. Use "depth_2_only" when you want to
        steer the second level but trust the leaf-level derivation. Use "all_levels" only
        for the highest-stakes explorations where you want full control over every subfocus.
      options:
        - value: "none"
          label: "[default] None — auto-derive at depth 2 and depth 3"
          decision_guidance: "Recommended for most meditations."
        - value: "depth_2_only"
          label: "Confirm at depth 2 only (adds up to 9 prompts)"
          decision_guidance: "Pick when you want to steer the second level but trust leaf-level derivation."
        - value: "all_levels"
          label: "Confirm at depth 2 and depth 3 (adds up to 36 prompts)"
          decision_guidance: "Pick for the highest-stakes explorations where you want full control over every subfocus."

  resume_handler:
    sequence:
      1: "Collect Sub-Q1 (facets) answer + any follow-up text inputs for modify_one/modify_multiple"
      2: "Collect Sub-Q2 (sections) multi-select answer"
      3: "Collect Sub-Q3 (visualisations) multi-select answer"
      4: "Collect Sub-Q4 (additional_focus_areas) per-item answers + follow-up text for custom_report_section_title"
      5: "Collect Sub-Q5 (deep_confirm) answer"
    cost_change_check:
      condition: "any additional_focus_areas[i].treatment in {additional_facet, additional_facet_AND_section}"
      on_true: "fire Q-Cost-and-Richness-Acknowledgment read-only-richness variant BEFORE resuming the depth-0 manager; on cancel abort and delete facets-pending-{ts}.yml; on re-acknowledge resume with full payload"
      on_false: "resume depth-0 manager directly with confirmed payload"
    on_cancel: "abort meditation; delete facets-pending-{ts}.yml; do NOT create init-suggestions-{ts}.yml"
    on_regenerate: "resume depth-0 manager with regenerate_facets=true + previous facets-pending-{ts}.yml path; depth-0 manager re-emits needs_user_input with new prompt_inputs (cap 3 attempts per existing rule)"
```

**Cost-ack re-presentation logic** (fires after combined askQuestion resolves, before subagent resumes):

If any `additional_focus_areas` decision is `additional_facet` OR `additional_facet_AND_section`:

1. Recompute agent count with new facet count (add 14 per `additional_facet` or `additional_facet_AND_section` at D=3 Research; 13 at D=3 Quick).
2. Run the **read-only-richness variant** of `Q-Cost-and-Richness-Acknowledgment` (title: "Cost-and-Richness Acknowledgment (re-presented)") with updated count and preamble: `Cost has changed because you accepted {N} additional facets — please re-acknowledge or cancel.`
3. On **cancel**: abort meditation; delete `facets-pending-{ts}.yml`; ensure no `init-suggestions-{ts}.yml` is written.
4. On **re-acknowledge** (`proceed` or `switch_to_*`): mode-swap is preserved (richness stays locked); resume depth-0 manager with full confirmed payload.

**Resume-handler contract** (after all sub-questions answered and any cost-ack re-presentation resolved):

1. Calling agent resumes the depth-0 subagent with the confirmed facets (including any overrides), the `confirmDeepFacets` enum value, the confirmed `sections_kept` IDs, the confirmed `visualisations_kept` IDs, and the `additional_focus_areas_decisions` map.
2. Depth-0 subagent: appends the confirmed facets to `facet-registry.yml` (Research mode), promotes the draft to the final `facets.md`, deletes `facets-pending-{ts}.yml`, writes `init-suggestions-{ts}.yml` (confirmed sections + visualisations + per-item focus-area treatments), and proceeds to step 5 of the workflow (spawn explorers). The `confirmDeepFacets` value is propagated to every child spawn in step 5.
3. If `facets_decision` was `regenerate` → calling agent resumes the subagent with `regenerate_facets: true` plus the previous `facets-pending-{ts}.yml` path; the subagent reads the rejected set, derives a different one, and re-escalates. Loop, **capped at 3 regeneration attempts**.
4. If `facets_decision` was `modify_one` or `modify_multiple` → calling agent collects the replacement text(s) via a free-text follow-up, then resumes the subagent with `facet_overrides: [{ index: N, new_subfocus: "...", new_slug: "..." (optional) }, ...]`. The subagent applies the overrides and proceeds to resolve the full combined payload.

#### Deep confirmation flow (when `confirmDeepFacets` ≠ `none`)

When deep confirmation is enabled, **file-based escalation** is used because the chain is too deep for direct return-up to be practical.

**Child agent side** (any agent at a depth where confirmation is required):

1. Derive 3 child subfocuses from actual research findings, per the existing Phase C logic.
2. **Before** acquiring the registry lock, write a pending-facets file:

       pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml

   Where `{N}/{D}/{S}/{ts}` identify the **parent agent** that derived these proposed children.

   ```yaml
   path:
     branch: 1
     parent_depth: 1
     parent_sub_index: 0
     parent_slug: "auth-flow-trade-offs"
   timestamp_utc: "20260516120000"
   proposed_children:
     - sub_index: 1
       slug: "session-vs-jwt"
       subfocus: "Session cookies vs JWT for cross-service auth"
       rationale: "Parent finding [memory: caching-patterns] surfaced this as the most contested choice"
     - sub_index: 2
       slug: "..."
       subfocus: "..."
       rationale: "..."
     - sub_index: 3
       slug: "..."
       subfocus: "..."
       rationale: "..."
   status: "pending"
   ```

3. **Poll** for the matching `confirmed-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml`. Use prefix-glob with the same `branch-{N}-depth-{D}-sub-{S}-` segment plus the `{ts}` from the pending file.

4. Once the confirmation file exists, read it. Schema mirrors the pending file but adds a `decision` per child:

   ```yaml
   decisions:
     - sub_index: 1
       decision: "confirmed" | "modified" | "regenerate"
       new_slug: "..."
       new_subfocus: "..."
       new_rationale: "..."
     - sub_index: 2
       decision: "..."
     - sub_index: 3
       decision: "..."
   ```

5. Apply the decisions:
   - `confirmed` → use the original child verbatim
   - `modified` → replace with the user-supplied subfocus/slug
   - `regenerate` → re-derive that single child from research findings, write a new pending file with the same path-id but a fresh `{ts}`, and loop (**capped at 3 regenerations per child**).

6. After all 3 are confirmed, acquire the registry lock and proceed with normal Phase C/D.

**Depth-0 manager side** (the root):

While polling for branch outputs, **also** poll for any new `pending-facets-*.yml` files. When one (or several) appears:

1. Read each pending file.
2. If multiple appeared in the same polling round, batch them into a single `needs_user_input` block.
3. Calling agent runs `askQuestion` (one entry per pending file, using the same confirm/modify/regenerate option set as Q-Confirm-1) and resumes with the user's decisions.
4. Depth-0 manager writes the corresponding `confirmed-facets-{path-id}-{ts}.yml` for each.
5. Resume the branch-output poll.

#### Re-spawn semantics

When the user selects an "expansion direction" continuation (calling agent step 12), the new meditation:

- **Always** re-runs the depth-0 facet confirmation.
- **Reuses** the previous `confirmDeepFacets` enum value by default; the calling agent may offer a one-line "keep deep-confirm setting?" follow-up.

### Coordination Conventions

The verbatim Coordination Conventions (artefact filename grammar — 18 rows post-richness including `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`, `follow-up-{type}-{ts}.yml` rows; placeholder definitions for `{topic-slug}`, `{slug}`, `{ts}`, `{N}`, `{D}`, `{S}`; prefix-glob polling rule; `ls -1t | head -n 1` resolution; never-hard-code-`report.{html,pdf}` invariant; retrospective template; Branch & Leaf Index template with extended top-level artefacts block) live in the `crux-skill-memory-meditation-coordination` skill. The calling agent never reads working-directory artefacts directly — the depth-0 guide agent owns coordination semantics. Calling-agent step 9 verifies the paired report pair by prefix-glob (`report-{topic-slug}-*.html` / `*.pdf`) before presenting in step 10; the coordination skill owns the "never hard-code `report.html`/`report.pdf`" invariant that governs these globs.

### What Happens

The depth-0 subagent runs a **mode-specific** workflow. Before the subagent tree spawns at all, the calling agent runs the four mandatory pre-spawn gates documented above — **Depth Selection**, **Cost & Scope Acknowledgment** (merged `Q-Cost-and-Richness-Acknowledgment`), **Theme Preflight**, and (mid-flow, between subagent step 4 and step 5) **combined Facet / Sections / Visualisations / Focus-Areas Confirmation**. After consolidation completes and before adversarial review begins, the calling agent also runs **`Q-Finalisation-Enhancements`** (K10a). **Steps 1–8** are then performed by the subagent tree (file-based coordination, file outputs in the working directory); **steps 9–12** are performed by you (the calling agent) after the subagent returns.

The recursive exploration protocol that each depth-1/2 child agent runs is defined in the `crux-cursor-meditation-guide` agent (loading the `crux-skill-memory-meditation-research` skill for Research Phases A–G and the `crux-skill-memory-meditation-quick` skill for the Quick 6-step protocol). Depth-3 children terminate without further recursion in both modes.

#### Research mode (default)

The depth-0 Research mode workflow (steps 1–8: feature guard, create working directory, initialize coordination files, derive + confirm facets via combined Pattern-B flow, spawn 3 branch explorers, poll for branch outputs with optional deep-confirm hook, run peer review, consolidate → Branch & Leaf Index → K10c reflection → return `needs_user_input`) is fully documented in the `crux-skill-memory-meditation-research` skill. The skill owns Phases A–G recursive depth-first recursion, the facet registry lock, citations index, peer review file spec, `init-suggestions-{ts}.yml` write (step 4b), K10c in-pass reflection writing `finalisation-enhancements.yml` (step 8), and respawn-payload prep (step 8b). The calling agent must pass `meditateMode`, `maxDepth`, `theming:`, `comprehensiveness:` (REQUIRED — guide agent aborts if missing), `parentContext`, and stripped `$ARGUMENTS` in the spawn prompt per §4.3.1 of the architecture design.

#### Quick mode (`--quick`)

The depth-0 Quick mode workflow (steps 1–8: feature guard, create working directory, skip registry/citations init, derive + confirm facets via identical combined Pattern-B flow, spawn 3 branch explorers with upfront child derivation, poll for branch outputs with optional deep-confirm hook, skip peer review, consolidate → Branch & Leaf Index → K10c reflection → return `needs_user_input`) is fully documented in the `crux-skill-memory-meditation-quick` skill. The skill owns the Quick 6-step parallel fan-out protocol, warn-only citation validation, `init-suggestions-{ts}.yml` write (step 4b), K10c in-pass reflection (same rubric as Research, warn-only citation regime), and Quick-mode steps 9–13 with documented relaxations. The calling agent spawn prompt carries identical required fields as Research mode.

#### Single-tree model strategies (`--random-model` and `--model-per-branch`)

When `modelStrategy.mode ∈ {"random", "per_branch"}`, the meditation runs as a **single tree** with the standard Research- or Quick-mode workflow above — one working directory, one `consolidation.md` / `facets.md` / report pair, no `cross-model-synthesis.md`, no `model-{slug}/` subdirectories, single-tree `finalisation-enhancements.yml` cadence. The model strategy only changes which model executes which agent — see the **Per-spawn `model:` selection rules** in the Model Strategy payload section above. `facets.md` frontmatter, the Branch & Leaf Index, and the report footer record the resolved strategy per the `crux-skill-memory-meditation-coordination` and `crux-skill-memory-meditation-report` skills; `--model-per-branch` additionally renders `[branch model: {label}]` attribution in per-facet report sections.

#### Ensemble Max mode (`--ensemble`, `modelStrategy.mode == "ensemble_max"`)

**Steps 1–8 for Ensemble Max** are replaced by the **Ensemble Protocol** below. The calling agent owns the entire ensemble orchestration — it runs the pre-spawn gates once, spawns N independent meditation trees (one per model), waits for all to complete, then spawns the aggregation agent. Each model's depth-0 subagent runs the standard Research (or Quick, if combined with `--quick`) workflow in its own subdirectory, unaware that it is part of an ensemble. Internally, each per-tree depth-0 manager receives `modelStrategy.mode: "random"` pinned to its assigned pool model (this keeps the per-spawn `model:` selection rules uniform across all strategies).

**Ensemble Protocol — Calling-agent block**:

1. **Read model pool**: Load `cruxMemories.meditate.modelPool` from `.crux/crux-memories.json`. Let `N` = array length (default 3). If the pool is empty or missing, abort with a clear error: "Ensemble mode requires `cruxMemories.meditate.modelPool` in `.crux/crux-memories.json` — configure at least 2 model entries."

2. **Depth Selection**: Run `Q-Depth-Selection` (see above). Store the result as `maxDepth`. This is shared across all model trees.

3. **Cost & Scope Acknowledgment**: Run the ensemble-specific variant of `Q-Cost-and-Richness-Acknowledgment` (see above) with the total agent count `~{N × perModelCount + 1}` computed using the selected `maxDepth`, and the model labels from the pool. The richness level selected in Sub-Q1 is shared across all model trees.

4. **Theme Preflight**: Run once (identical to single-model mode). The resolved `theming` payload is shared across all model trees.

5. **Create ensemble working directory**: `meditations/{yyyymmdd}-{topic-slug}-ensemble/`. Write a shared `facets.md` stub here (promoted after facet confirmation).

6. **Derive and confirm facets (once, shared)**: Spawn a **single** `crux-cursor-meditation-guide` subagent using the **caller's own model** (not from the pool). This subagent runs only steps 1–4 of the standard workflow (feature guard, create working dir, initialize coordination files, derive + confirm facets via Pattern B). The `workingDir` for this temporary subagent is the ensemble root directory. After facet confirmation completes (Q-Confirm-1 + Q-Confirm-2), extract the confirmed facets and `confirmDeepFacets` value from the subagent's response. The per-model subdirectories are created in the next step.

7. **Spawn N model-specific meditation trees in parallel**: For each entry `{slug, label}` in `modelPool`:
   - Create subdirectory `{ensembleWorkingDir}/model-{label-slug}/` (where `label-slug` is the kebab-case version of the label, e.g. `model-gpt-5.5`, `model-opus-4.7`, `model-gemini-pro-3.1`).
   - Spawn a `crux-cursor-meditation-guide` subagent with **`model: slug`** on the Task tool invocation. Pass:
     - `meditateMode`: the active mode (`"research"` or `"quick"`)
     - `maxDepth`: the user's depth selection from Q-Depth-Selection (shared across all model trees)
     - `ensembleModel`: the model slug (so the subagent can propagate it to all children)
     - `ensembleModelLabel`: the human-readable label
     - `preConfirmedFacets`: the confirmed facets from step 6 (the subagent skips facet derivation and confirmation — uses these directly)
     - `confirmDeepFacets`: the Q-Confirm-2 value from step 6
     - `workingDir`: the model-specific subdirectory path
     - `theming`: the shared Theme Preflight payload
     - `comprehensiveness`: the shared comprehensiveness payload (REQUIRED)
     - All other standard parameters (`parentContext`, stripped `$ARGUMENTS`, etc.)
   - All N subagents run in background simultaneously.

8. **Poll for N model tree completions**: Wait for each model-specific subagent to complete. Each writes its own `consolidation.md`, `facets.md` (with Branch & Leaf Index), `retrospective-{ts}.md`, and `report-{topic-slug}-{ts}.html` / `.pdf` pair in its model-specific subdirectory. Use the same prefix-glob verification as single-model step 9, but applied per subdirectory.

   **Deep-confirmation hook (when `confirmDeepFacets ≠ none`)**: Each model tree may produce `pending-facets-*.yml` files in its own subdirectory. The calling agent polls **all N subdirectories** for pending files and batches them into `askQuestion` prompts, noting which model produced each pending request so the user can make model-aware decisions. Write the corresponding `confirmed-facets-*.yml` to the correct model-specific subdirectory.

9. **Spawn cross-model aggregation agent**: Once all N trees have completed successfully, spawn a `crux-cursor-meditation-guide` subagent in **Ensemble Aggregation** function (a new sub-mode of Meditate). If `cruxMemories.meditate.ensembleAggregatorModel` is set, pass it as `model:` on the Task tool; otherwise use the caller's own model. Pass:
   - `ensembleAggregation: true`
   - `ensembleWorkingDir`: the ensemble root directory path
   - `modelSubdirs`: ordered list of `{label, subdirPath}` for each model
   - `confirmedFacets`: the shared facets
   - `theming`: the shared Theme Preflight payload
   - `comprehensiveness`: the shared comprehensiveness payload (REQUIRED)
   - `meditateMode`: the active mode
   - `topicSlug`: the topic slug for report filenames

   The aggregation agent reads all N consolidations and branch files, produces `cross-model-synthesis.md` in the ensemble root, and generates the ensemble-level `ensemble-report-{topic-slug}-{ts}.html` / `.pdf` pair. The spawn-receiver contract (K10 layered cadence steps 3b–3f, cross-model synthesis schema, ensemble report extras) lives in the `crux-skill-memory-meditation-ensemble` skill.

10. **Verify ensemble artifacts**: In addition to verifying each model's per-tree report pair (step 8), verify the ensemble-level artifacts:

       SYNTH="${ensembleWorkingDir}/cross-model-synthesis.md"
       ENS_HTML=$(ls -1t "${ensembleWorkingDir}"/ensemble-report-"${topic-slug}"-*.html 2>/dev/null | head -n 1)
       ENS_PDF=$(ls -1t  "${ensembleWorkingDir}"/ensemble-report-"${topic-slug}"-*.pdf  2>/dev/null | head -n 1)
       [ -s "${SYNTH}" ] && [ -s "${ENS_HTML}" ] && [ -s "${ENS_PDF}" ]

**Steps 9–12 for Ensemble — Calling-agent block**:

When `ensembleMode` is true, the calling-agent block (steps 9–12 of single-model mode) is replaced:

10. **Verify artifacts**: Run verification for all N per-model report pairs (one per subdirectory) plus the ensemble-level synthesis and report pair. Regenerate any missing artifact.

11. **Present to user**: Read `cross-model-synthesis.md` from the ensemble root. Display the cross-model analysis organized by the synthesis dimensions (convergence, divergence, unique insights — see **Ensemble Aggregation Report** below). Include absolute paths to:
    - The ensemble synthesis: `cross-model-synthesis.md`
    - The ensemble report pair: `ensemble-report-{topic-slug}-{ts}.html` / `.pdf`
    - Each per-model report pair: `model-{label-slug}/report-{topic-slug}-{ts}.html` / `.pdf`
    - Each per-model `facets.md` (for drill-down into individual model trees)

    End the presentation with a reminder: if the user wants further content edits, visual refinements, theme adjustments, contrast tweaks, or regenerated report variants, they can start a new agent session and point it at the ensemble meditation folder (`{ensembleWorkingDir}`) so the follow-up agent can work from the produced artifacts.

12. **Interactive continuation**: Same `AskQuestion` multi-select as single-model mode, with these additions:
    - Per-model expansion options: "Explore {direction} deeper using {model-label}" — spawns a single-model expansion tree on the chosen model
    - `save_spec` — writes the ensemble synthesis as a draft spec (includes cross-model evidence)
    - `end_meditation` — complete the session

13. **Handle selection**: Same as single-model mode. Expansion trees from an ensemble meditation run as single-model meditations (not re-ensembled) unless the user explicitly passes `--ensemble` again.

**Steps 9–12: Calling-agent block (both modes, single-model)**

9. **Verify the mandatory report artifacts**: The depth-0 subagent is required to produce a paired `report-{topic-slug}-{ts}.html` AND `report-{topic-slug}-{ts}.pdf` in the working directory before returning (its workflow step 12). Resolve the latest matching pair via prefix-glob and verify both files are non-empty:

       HTML_LATEST=$(ls -1t "{workingDir}"/report-"{topic-slug}"-*.html 2>/dev/null | head -n 1)
       PDF_LATEST=$(ls -1t  "{workingDir}"/report-"{topic-slug}"-*.pdf  2>/dev/null | head -n 1)
       [ -s "${HTML_LATEST}" ] && [ -s "${PDF_LATEST}" ]

   If either resolves empty or the size check fails, regenerate the missing artifact yourself per the **Report Generation — MANDATORY** section above before continuing. If the PDF specifically is missing because no headless Chromium binary is available on the host (the subagent will have aborted its PDF render with a missing-dependency error), surface that error and the platform-specific install hint (`brew install --cask google-chrome` on macOS, `apt install chromium` on Debian/Ubuntu, etc.) **prominently** in step 10 so the user can install Chromium and re-run — never silently skip the PDF. On an `ESCALATE` verdict from the adversarial review cycle, this step is a no-op: the subagent did not generate a report pair and step 10 reports unresolved findings instead of report paths.

10. **Present to user**: Read `consolidation.md` from the working directory (or use the returned text). Display the consolidated insights organized by facet theme (using facet titles, not branch numbers), highlighting cross-cutting connections, quality-review findings (Research mode), any citation gaps (Quick mode), and any unresolved `MUST_FIX` findings from the adversarial review (on `ESCALATE`). **Always include the absolute paths to `workingDir`, `facets.md`, `retrospective-{ts}.md`, the latest `report-{topic-slug}-{ts}.html`, and the latest `report-{topic-slug}-{ts}.pdf`** (resolved via the step 9 globs) so the user can open the meditation folder, the navigational entry point, the process retrospective, and both report artifacts immediately. On `ESCALATE`, list the `workingDir`, `review-pre-report-*-iter-*.md` paths, and the unresolved findings summary instead of the report paths (the retrospective path is always included). End the presentation with a reminder: if the user wants further content edits, visual refinements, theme adjustments, contrast tweaks, or regenerated report variants, they can start a new agent session and point it at `workingDir` so the follow-up agent can work from the produced artifacts.

11. **Interactive continuation**: Use `AskQuestion` with a multi-select prompt and **mandatory decision-guidance context** so the user understands the trade-off behind each option. Sample prompt body (adapt to the actual tangent directions discovered):

        The meditation produced `facets.md`, `consolidation.md`, and the paired
        `report-{topic-slug}-{ts}.html` / `.pdf` (shown above). Both report artefacts
        are produced automatically by every meditation now, so this prompt no longer
        offers "Save as HTML" / "Save as PDF" — those files already exist.

        Choose any combination of the following. Each has different cost and
        downstream implications:

          • Expansion direction(s) — opens a follow-up meditation tree that
            explores the tangent more deeply. Each expansion spawns a full new
            tree (agent count depends on the selected depth — see depth table)
            plus its own adversarial review cycle and paired report. Significant
            token cost; use when the consolidation surfaced a sub-question worth
            a dedicated deep dive. The original report pair is preserved for
            comparison.

          • Save meditation as draft spec — writes the consolidated insights and
            Branch & Leaf Index into a draft engineering-spec outline under the
            configured specs directory. Inexpensive; use when you intend to
            convert the meditation into actionable work.

          • End meditation — closes the session without further work. Use when
            the existing report pair is the deliverable. You can still request
            later content or theming adjustments in a new agent session pointed
            at the meditation folder shown above.

   Options (multi-select, grouped under section headings):

   **Expansion directions** (K10c group 1):
   - Discovered tangent directions (derived from the exploration) — one option per discovered direction, each acting as an expansion trigger

   **Apply un-chosen enhancements** (K10c group 2 — one option per `unchosen_persisted` item in `finalisation-enhancements.yml`; omit section if no unchosen items exist):
   - `reapply_enhancement_{id}` — "Re-apply unchosen enhancement: {candidate.title}" — re-runs the post-consolidation phase with that single item pre-checked (other candidates greyed-out); fresh ≤3 iteration cap (new continuation invocation). Decision guidance: selecting re-triggers `Q-Finalisation-Enhancements` with this single item pre-checked; the existing report is not modified until the re-application respawn completes.

   **Spawn queued follow-ups** (K10c group 3 — one option per queued expensive item with a `follow-up-{type}-{ts}.yml` on disk; omit section if no queued items exist):
   - `spawn_queued_{id}` — "Spawn now: {type} — {follow_up_title}" — triggers cost-ack re-presentation (`spawn_now` variant) then spawns the agent. Decision guidance: triggers the read-only-richness cost-ack re-presentation showing the updated agent count; on proceed, the expensive agent spawns immediately.

   **Other**:
   - `save_spec` — "Save meditation as draft spec" (write insights as a draft spec outline to the configured specs directory)
   - `end_meditation` — "End meditation" (complete the session)

   Do **not** offer "Save as interactive HTML report" or "Save as PDF report" — both artefacts are already produced as part of every meditation per the **Report Generation — MANDATORY** section above and were already surfaced in step 10.

12. **Handle the user's selection**:

    - **Expansion direction(s) selected** — **first run the read-only-richness variant of the Cost & Scope Acknowledgment** (`Q-Cost-Acknowledgment-Expansion` — richness locked at the level set during the original `Q-Cost-and-Richness-Acknowledgment` gate; no "keep richness setting?" follow-up) per the rules in the **Cost & Scope Acknowledgment** section above. If the user cancels, stop without spawning anything. If they proceed, augment context with the new directions and user input, then repeat from step 2 (spawning a new subagent — which will produce its own mandatory Theme Preflight, combined Facet/Sections/Visualisations/Focus-Areas Pattern-B escalation, adversarial review cycle, and paired `report-{topic-slug}-{ts}.html` + `report-{topic-slug}-{ts}.pdf` per the **Report Generation — MANDATORY** section). The new meditation **always** re-runs the depth-0 facet confirmation; the previous `confirmDeepFacets` value is reused by default but you may offer a one-line "keep deep-confirm setting?" follow-up. The mode-swap options from the original gate are not re-offered (mode persists across expansions); the user must `cancel` and re-invoke `/crux-meditate` to change mode.
    - **`reapply_enhancement_{id}` selected** (K10c — re-apply unchosen enhancement) — re-run `Q-Finalisation-Enhancements` with the selected item pre-checked (other candidates greyed-out). A fresh ≤3 iteration cap applies (this is a new continuation invocation). The respawn targets the same working directory's report pair.
    - **`spawn_queued_{id}` selected** (K10c — spawn queued follow-up) — trigger the read-only-richness cost-ack re-presentation (`spawn_now` variant) with the selected expensive item enumerated. On proceed, spawn the expensive agent immediately. On cancel, return to the continuation menu without modifying the follow-up artefact.
    - **`save_spec` selected** — write a draft spec outline file to the configured specs directory using the consolidation summary, the Branch & Leaf Index, and the confirmed top-level facets as the spec's input. Report the absolute path back to the user.
    - **`end_meditation` selected** — complete the session. Before the final response, remind the user that they can request further adjustments to content, theming, visual design, contrast, or report variants in a new agent session pointed at the meditation folder (`workingDir`).

    Note: the legacy `save_html` / `save_pdf` selections have been removed in subtask 05 because both artefacts are now produced automatically by every meditation.

### Branch & Leaf Index (appended to `facets.md`)

The verbatim Branch & Leaf Index template (construction rule, required structure with all section headings, depth-3 grouping conventions, missing-slots enumeration, Quick-mode and ESCALATE omission rules, extended top-level artefacts block including `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`, and four `follow-up-{type}-{ts}.yml` entries) lives in the `crux-skill-memory-meditation-coordination` skill. The depth-0 guide agent must read this skill and follow the template verbatim when appending the index to `facets.md` after consolidation completes. The calling agent verifies `facets.md` is present and non-empty (via `[ -s "${workingDir}/facets.md" ]`) as part of step 9 verification.

### Finalisation Enhancements Gate — Q-Finalisation-Enhancements (K10a)

After consolidation completes (and the Branch & Leaf Index is refreshed in step 9/sub-step 5), the depth-0 manager performs an **in-pass reflection** to score candidate enhancements. It writes `finalisation-enhancements.yml` to the working directory, then returns a `needs_user_input` block to the calling agent. **The calling agent then runs `Q-Finalisation-Enhancements`** (a new gate owned by the calling agent per Pattern B integrity). This gate fires **BEFORE** the adversarial review begins, in BOTH Research and Quick mode, and at ensemble root (after all per-tree YAMLs are written and the aggregator produces the root combined YAML — see Ensemble layered cadence below).

**Skip-all backwards-compat path**: if the user selects 0 items, resume the depth-0 manager with an empty accepted set; flow proceeds to adversarial review unchanged — this exactly reproduces today's pre-K10 behaviour.

**Graceful degradation**: if `finalisation-enhancements.yml` contains fewer than 5 candidates (consolidation reflection found fewer high-quality ones), present whatever count surfaced (even 1–4). If `degradation_reason` indicates zero candidates met the threshold, surface a one-line "no high-quality enhancement candidates surfaced" message and proceed directly to adversarial review without firing `askQuestion` (no user time wasted on an empty gate).

#### Q-Finalisation-Enhancements (multi-select 0–5)

**Prompt preamble**:

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

**Options** (multi-select, 0–5; one option per candidate in `finalisation-enhancements.yml`):

- `{candidate.id}` — **{candidate.title}** [{candidate.cost_class}] — {candidate.description} (impact={candidate.impact_score} × insight={candidate.insight_value_score} = composite={candidate.composite_score})
  - Decision guidance: **Cheap items** ("respawn" treatment default): selecting will bundle this enhancement into the first adversarial review iteration's report-respawn payload. Zero extra agent spawns within this invocation. **Expensive items** ("queue" treatment default): selecting will write a follow-up artefact (`follow-up-{type}-{ts}.yml`) surfaced in the continuation menu as "Spawn queued follow-ups"; selecting `spawn_now` instead triggers cost-ack re-presentation before adversarial review.

**Per-item treatment sub-question** (for each accepted expensive item, `cost_class: "expensive"`):

After the multi-select resolves, the calling agent runs a follow-up single-select `Q-Finalisation-Enhancement-Treatment-{id}` for each accepted expensive item:

- `queue` **[default — preselected]** — Write `follow-up-{type}-{ts}.yml` next to `consolidation.md`; surface in continuation menu as "Spawn queued follow-ups". Zero in-invocation cost.
  - Decision guidance: The expensive enhancement is queued as a follow-up artefact. You can trigger it from the continuation menu after reviewing the report. Zero additional agents in this invocation.
- `spawn_now` — Opt-in: triggers cost-ack re-presentation BEFORE the adversarial review begins. Expensive agents spawn after the adversarial cycle completes.
  - Decision guidance: The expensive enhancement spawns immediately after the report is finalised. Triggers cost-ack re-presentation with updated total agent count. See per-type contributions in the cost table below:
    - `additional_meditation`: 1 top-level `/crux-meditate` invocation (nested tree; nested gate handles its own cost)
    - `extracted_spec`: 1 spec-generator agent
    - `extracted_memories`: 1 memory-extraction agent
    - `expanded_branch`: ~14 agents at D=3 Research (1 + 3 + 9 + 1 peer); ~13 at D=3 Quick

**Cost-ack re-presentation for `spawn_now`** (fires once after per-item treatment sub-questions, if any `spawn_now` selected):

Uses the read-only-richness variant of `Q-Cost-and-Richness-Acknowledgment` with the `spawn_now` trigger preamble:

    You've accepted spawning {N} follow-up agent(s) for finalisation enhancements
    ({enumerated_types}). The new total agent count is ~{N_total} (current depth {D},
    richness {level}, mode {mode}, including {N_finalisation} spawn-now agents).

    Per-type subsystem agent contribution:
      - additional_meditation × M  → spawns M top-level /crux-meditate invocations
      - extracted_spec × M         → spawns M spec-generator agent(s)
      - extracted_memories × M     → spawns M memory-extraction agent(s)
      - expanded_branch × M        → spawns M branch-expansion subtrees (~14 agents each at D=3 Research)

    [Locked: richness = {level}]
    [Locked: depth = {D}]

    Re-acknowledge or cancel.

On **cancel**: drop the `spawn_now` treatments, fall back to `queue` treatment for those items (no work lost), proceed. On **re-acknowledge**: proceed to adversarial review; expensive agents spawn in parallel after the adversarial cycle completes.

**Single-shot semantics**: the cost-ack re-presentation for `spawn_now` is a single round trip. Treatment decisions are immutable for the remainder of the invocation after the cost-ack closes.

#### `finalisation-enhancements.yml` update flow (K10c)

After `Q-Finalisation-Enhancements` + per-item treatment sub-questions + any `spawn_now` cost-ack re-presentation resolve, the calling agent:

1. Updates `finalisation-enhancements.yml` **in place**: for each candidate, set `accepted: true | false`, `treatment: "respawn" | "queue" | "spawn_now" | "unchosen_persisted"`, and `decided_at_utc: <ISO 8601>`.
2. Writes follow-up artefacts (`follow-up-{type}-{ts}.yml`) for each accepted expensive item with `treatment: queue` or `treatment: spawn_now`.
3. Resumes the depth-0 manager with the updated file path (`finalisation_enhancements_path: "meditations/{slug}/finalisation-enhancements.yml"`).
4. The depth-0 manager:
   - Bundles accepted cheap enhancements into the first adversarial review iteration's respawn payload (Dim 13 cause `accepted_finalisation_enhancements`)
   - After the adversarial cycle completes: spawns expensive `spawn_now` agents in parallel

#### K10b Per-Cheap-Type Rendering Contract

The verbatim K10b Per-Cheap-Type Rendering Contract — 7 cheap enhancement types (`executive_summary`, `action_plan`, `risks_section`, `glossary`, `decision_tree_infographic`, `reader_persona_tldrs`, `cross_branch_synthesis_section`) with landing locations, payload shapes consumed, and static degradation rules — lives in the `crux-skill-memory-meditation-report` skill (§6.9). The calling agent verifies that each accepted cheap item's `type` matches a known type in the skill before resuming the depth-0 manager; the skill's resume-handler processes accepted cheap items in the per-reason processing order (enhancements → visualisations → sections).

#### K10 Ensemble Respawn Targeting and Ensemble Layered Cadence

The verbatim K10 Ensemble Respawn Targeting contract (per-tree-sourced vs cross-model-sourced accept dispatch; `source: "tree:{model-subdir}"` vs `source: "cross_model"` routing; per-tree vs ensemble-root report respawn targeting; Dim 13 ensemble layered audit) and the Ensemble layered cadence semantics (per-tree `finalisation-enhancements.yml` write-only at per-tree level with no per-tree `askQuestion`; aggregator step 3b–3f with `cross_model_candidates` + `union_candidates`; single combined root gate; model-label fallback) live in the `crux-skill-memory-meditation-ensemble` skill. The calling agent's single combined `askQuestion` at ensemble root ranks across the union list (each option label includes provenance: `{title} [{cost_class}] ({source-label}) — composite={N}`, capped at 0–5 multi-select). The skip-all path reproduces pre-K10 behaviour byte-for-byte at every richness level.

### Adversarial Review and Fix Cycle — MANDATORY

The adversarial review-and-fix cycle is **mandatory** at step 10 in both Research and Quick mode, running before any report is generated. The cycle audits all editable meditation files across **13 dimensions** (including Dim 9 level-conditional peer-review thoroughness, Dim 12 Comprehensiveness fidelity, and Dim 13 Init-suggestion AND finalisation-enhancement honour), with a ≤3-iteration cap shared between standard `MUST_FIX` in-place fixes and Dim 13 `respawn_required: true` Report-Skill Respawn Protocol triggers. Every escalated `MUST_FIX needs_user_input` entry **must** include a mandatory `context` field; Dim 13 bypasses user input entirely via the structured `respawn_reasons`-list payload (K9 + K10b) authored by the reviewer and consumed by the report skill.

The verbatim reviewer agent contract (13 dimensions, severity classification, iteration loop with Dim 13 respawn branch, MUST_FIX `needs_user_input` schema with mandatory `context`, review document format, Quick relaxations, and the full Report-Skill Respawn Protocol payload schema) lives in the `crux-skill-memory-meditation-review` skill. The Report-Skill Respawn Protocol resume-handler (per-reason processing order, fuzzy-match auto-resolve, iteration accounting) lives in the `crux-skill-memory-meditation-report` skill.

### Subject-Matter Focus — MANDATORY (all user-facing outputs)

The verbatim Subject-Matter Focus rule — governing what is forbidden (Branch 1/2/3 labels, depth/leaf/agent count references, raw `[child: branch-N-depth-D-sub-S]` citations, peer-reviewer-as-actor framing, process-framing executive summaries) and what is required (facet titles as headings, subject-matter organizational framing, topic-name cross-references, conclusion-first executive summaries, `[research: subfocus-slug]` citation translation) — lives in the `crux-skill-memory-meditation-report` skill. The rule applies to `consolidation.md` and the HTML/PDF reports only; internal coordination files and `retrospective-{ts}.md` retain process-oriented naming.

### Process Retrospective — MANDATORY

The verbatim Process Retrospective contract — always-written rule (including on `ESCALATE`), filename convention (`retrospective-{yyyymmddHHMMSS}.md`), and the required-sections template (frontmatter + Summary Statistics + What Went Well + What Could Be Improved + Structural Observations + Recommendations) — lives in the `crux-skill-memory-meditation-coordination` skill. The depth-0 guide agent writes the retrospective at step 12b of its workflow; the calling agent always includes the `retrospective-{ts}.md` path in step 10's presentation (it is always present, including on `ESCALATE`).

### Report Generation — MANDATORY

Producing a paired HTML **and** PDF report with rich infographics, visualisations, and a clickable index is **mandatory** for every meditation in both Research and Quick mode. Reports are never generated over a failing adversarial review (`ESCALATE` aborts step 12b of the depth-0 manager). The calling agent runs a verification gate (step 9 above) before presenting results.

The verbatim Report Generation contract — Comprehensiveness Level Mapping (12 dimensions × 4 levels including `compact` backwards-compat anchor and subagent-abort rule), paired filename rule, all HTML structural requirements (responsive nav, TOC, hero, per-facet sections, quality review section, visualisations, infographics, calculators, light/dark mode, anti-homogenisation enforcement, Universal Contrast, Per-Branch Section Rule, Depth-3 Leaf Inclusion Rule, Peer-Review Surfacing Rule, Init-Suggestions Honour rules, K10b Per-Cheap-Type Rendering Contract, Report-Skill Respawn Protocol resume-handler), PDF high-contrast print theme, clickable PDF TOC, headless-Chrome render command with `?print=1`, chromium-binary fallback chain, CDN allowlist, and final verification — lives in the `crux-skill-memory-meditation-report` skill. The calling agent must surface the platform-specific Chromium install hint prominently in step 10 if the PDF render fails due to a missing binary.

### Ensemble Aggregation Report — MANDATORY (when `modelStrategy.mode == "ensemble_max"`)

The verbatim Ensemble Aggregation Report contract — ensemble working-directory layout, `cross-model-synthesis.md` schema (frontmatter + 8 mandatory sections), ensemble-report structural extras (model comparison hero, per-facet comparison cards, agreement heatmap, divergence deep-dives, per-model drill-down links), ensemble-specific visualisations (agreement heatmap required; model attribution Sankey + citation Venn + confidence radar recommended), model-attribution citation format (`[model: label]` / `[models: all]`), and footer annotation extension — lives in the `crux-skill-memory-meditation-ensemble` skill (shared report contracts in the `crux-skill-memory-meditation-report` skill). The Ensemble Aggregation Report only fires for `ensemble_max`; `random` and `per_branch` produce a single-tree report via the standard contract (with model-attribution annotations as described in the **Single-tree model strategies** section above).

## Related

- `crux-cursor-meditation-guide` agent — The specialist that orchestrates the recursive meditation tree (Research Phases A–G, Quick 6-step protocol, Adversarial Review, Ensemble Aggregation)
- `crux-skill-memory-meditation-research` skill — Research-mode depth-first protocol (Phases A–G, facet registry, citations index, peer review, K10c reflection)
- `crux-skill-memory-meditation-quick` skill — Quick-mode parallel fan-out protocol (6-step, warn-only citations, K10c reflection)
- `crux-skill-memory-meditation-ensemble` skill — Ensemble Aggregation function (cross-model synthesis, K10 layered cadence, K10 Respawn Targeting)
- `crux-skill-memory-meditation-review` skill — Adversarial Review function (13 dimensions, Report-Skill Respawn Protocol)
- `crux-skill-memory-meditation-report` skill — Mandatory report generation (Comprehensiveness Level Mapping, K10b, Init-Suggestions Honour, Subject-Matter Focus)
- `crux-skill-memory-meditation-coordination` skill — File-based coordination primitives (artefact filename grammar, polling, retrospective template, Branch & Leaf Index template)
- `crux-cursor-memory-manager` agent — Memory lifecycle management (Dream, REM sleep, Recall, Remember, Forget) for non-Meditate workflows
- `/crux-dream` — Extract and create memories from completed work
- `/crux-recall` — View and query memories
- `/crux-remember` — Create ad-hoc memories outside of spec workflows
- `/crux-forget` — Remove memories from the corpus
