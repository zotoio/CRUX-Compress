# Frozen Meditate Contract — 20260517

> [!IMPORTANT]
> **SUPERSEDED** by `meditate-frozen-contract-20260524.md` on 2026-05-24 to
> incorporate the completed 20260523 richness spec. This earlier freeze
> remains for audit trail only; do not consume it as the contract baseline.
> Downstream subtasks (S02–S12) must diff against
> `meditate-frozen-contract-20260524.md` instead.

> **Purpose**: This document is the authoritative freeze line for the
> `meditate-agent-skill-decomposition` spec (`20260517`). It captures
> every user-facing and executable behaviour of the current
> `/crux-meditate` workflow exactly as committed at git SHA
> `b4fc33b0c034866bb60b7fe7b03be9e0c7a18bbf` so that subsequent
> subtasks (architecture design, guide-agent extraction, skill
> extraction, command refactor, memory-manager trim, eval / test
> update, docs sync, install / dist enumeration, CRUX compression
> sync, integrity review) can diff post-refactor artefacts against
> a single contract. Every contract item is back-traceable to a line
> range or section heading in the **current** sources:
>
> - `.cursor/commands/crux-meditate.md` (1493 lines)
> - `.cursor/agents/crux-cursor-memory-manager.md` (946 lines)
>
> Where the two files mirror each other the command file is
> treated as the user-facing canonical text and the agent file as
> the executable canonical text. Differences are noted explicitly.
>
> **Source-of-truth map** (Section 10) is the single concordance
> the integrity-review subtask (12) consumes when verifying the
> post-refactor repo.

---

## 1. Modes Inventory

| Mode | Flag | Default? | Trigger | Calling-agent ownership | Subagent ownership | Per-tree agent count (at depth 3) | Source |
|------|------|----------|---------|--------------------------|--------------------|-----------------------------------|--------|
| **Research** | _(none)_ | Yes | `/crux-meditate [topic]` with no `--quick` and no `--ensemble` in `$ARGUMENTS` | All four pre-spawn gates + steps 9–12 continuation menu | Depth-0 manager runs subagent **steps 1–13** (Research) on `crux-cursor-memory-manager` | ~45 (1 depth-0 + 3 depth-1 + 9 depth-2 + 27 depth-3 + 3 peer reviewers + 1 adversarial) | Command lines 23–26, 60–67; Agent lines 360–448 |
| **Quick** | `--quick` | No | Flag present anywhere in `$ARGUMENTS` (case-sensitive, whitespace-bounded) | Identical 4 pre-spawn gates + steps 9–12 | Subagent **6-step protocol** at each non-leaf agent; no peer review; warn-only citations | ~42 (same minus peer reviewers) | Command lines 23–28, 517–540; Agent lines 450–471, 552–593 |
| **Ensemble + Research** | `--ensemble` | No | Flag present; reads `cruxMemories.meditate.modelPool` from `.crux/crux-memories.json` (default `N=3`) | Ensemble Protocol owns step 1–10 (model-pool read, depth selection, cost ack, theme preflight, ensemble working dir, shared facet derivation, N parallel trees, deep-confirm hook across all subdirs, aggregator spawn, ensemble verification) | Each model tree runs the standard Research depth-0 manager via `model: ensembleModel`; aggregator runs in **Ensemble Aggregation** function | `~{N × 45 + 1}` agents (`N` Research trees + 1 aggregation agent) | Command lines 26, 144–156, 541–613; Agent lines 872–907 |
| **Ensemble + Quick** | `--ensemble --quick` (any order) | No | Both flags present | Same Ensemble Protocol; `meditateMode: "quick"` threaded through | Each model tree runs the Quick 6-step protocol; aggregator runs in **Ensemble Aggregation** function | `~{N × 42 + 1}` agents | Command lines 16, 26, 41–46; Agent lines 290–294, 295–305 |

**Key config keys** (all consulted by the calling-agent / depth-0 manager):

| Key | Default | Purpose | Source |
|-----|---------|---------|--------|
| `flags.enableMemories` | `"true"` | Feature guard — abort if false | Agent line 362, 928 |
| `cruxMemories.meditate.modelPool` | `[{slug:"gpt-5.5-medium",label:"GPT 5.5"},{slug:"claude-opus-4-7-thinking-xhigh",label:"Opus 4.7"},{slug:"gemini-3.1-pro",label:"Gemini Pro 3.1"}]` | Models to spawn in Ensemble mode; empty → abort with config-pointer error | `.crux/crux-memories.json` lines 80–87; Command lines 43, 156, 547 |
| `cruxMemories.meditate.ensembleAggregatorModel` | `null` (uses caller's own model) | Override the model used for the cross-model aggregator agent | `.crux/crux-memories.json` line 86; Command lines 577–578 |
| `maxDepth` | `3` (default-preselected) | Recursion depth (1, 2, or 3); set by `Q-Depth-Selection`; propagated unchanged to every agent | Command lines 56–105; Agent lines 393, 823 |
| `meditateMode` | `"research"` | Mode flag propagated to every child | Command lines 41–46; Agent lines 296–301 |
| `confirmDeepFacets` | `"none"` (default-preselected) | Enum `none` / `depth_2_only` / `all_levels`; set by `Q-Confirm-2`; propagated to every child | Command lines 299–305, 338–360; Agent lines 307, 402 |
| `ensembleMode` | `false` | Set true when `--ensemble` is present | Command lines 41–46 |

**Mode-selection logic** (Command lines 38–46): inspect raw `$ARGUMENTS`; if `--quick` present strip flag and set `meditateMode:"quick"`; if `--ensemble` present strip flag and set `ensembleMode: true`; if neither set `meditateMode:"research", ensembleMode:false`. Flags may appear anywhere in `$ARGUMENTS` and must be stripped **before** topic-slug derivation.

**Internal/non-user-facing invocation forms** (Agent lines 292–294): child invocations with `meditateMode`, `meditateDepth`, `subfocus`, `subfocusIndex`; ensemble member invocations with `preConfirmedFacets`, `ensembleModel`, `confirmDeepFacets`; Ensemble Aggregation invocations with `ensembleAggregation` flag.

**Argument forms** (Command lines 9–16, 50–53): no args → derive from chat context; quoted text → seed topic; `@file @folder/` → file/folder references; mixed input synthesized.

---

## 2. Calling-Agent Gates (Verbatim or Near-Verbatim)

### 2.1 `Q-Depth-Selection` (mandatory, calling agent's very first action)

Source: Command lines 55–105.

**Prompt (verbatim)** — Command lines 73–89:

```
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
```

**Substitutions**: `{N1}`, `{N2}`, `{N3}` from per-mode agent table (Command lines 60–67); `{mode}` ∈ {Research, Quick}.

**Options (single-select)** — Command lines 95–97:

- `depth_1` — Depth 1: Broad survey (~{N1} agents)
- `depth_2` — Depth 2: Detailed analysis (~{N2} agents)
- `depth_3` — Depth 3: Deep research (~{N3} agents) **[default — preselected]**

**Behaviour rules** (Command lines 99–105):

- Always run on first invocation, regardless of arguments.
- Store result as `maxDepth` and propagate to every agent in the tree.
- Expansion continuation (step 12) reuses previous `maxDepth` by default; optional "keep depth setting?" follow-up only.
- Non-interactive sessions default to depth 3 without prompting.

### 2.2 `Q-Cost-Acknowledgment` (mandatory, calling agent's second action)

Source: Command lines 106–189.

**Prompt (verbatim, single-model)** — Command lines 127–143:

```
/crux-meditate is a deep research task that will spawn approximately {N} agents
(depth {maxDepth} in {mode} mode), produce a comprehensive HTML + PDF report with
infographics and clickable index, and run an adversarial review-and-fix cycle
before any output is finalised.

Compared with a single prompt or chat reply, this is significantly more expensive
in time and tokens. It's designed for well-considered problem statements tied to
high-value strategic activities (architecture decisions, strategic planning,
investment analyses, multi-week initiatives, deep technical research).

For lighter questions, prefer:
  - a regular chat
  - /crux-recall to query existing memories without spawning a tree
  - a single targeted prompt scoped to one file or function

How would you like to proceed?
```

**Ensemble-mode first-paragraph replacement (verbatim)** — Command lines 146–154:

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

**Substitutions** (Command line 156): `{poolSize}`, `{modelLabels}` (comma-separated `label` values from pool), `{maxDepth}`, `{mode}`, `{N}` (total agent count).

**Options (single-select)** — Command lines 160–166:

- `proceed` — proceed in currently-selected mode (Research or Quick, depth `{maxDepth}`, with or without Ensemble).
- `switch_to_quick` — proceed but switch to Quick mode (~{quickCount} agents at depth {maxDepth}, faster, no peer review). **Only offered when current mode = Research.**
- `switch_to_research` — proceed but switch to Research mode. **Only offered when current mode = Quick.**
- `switch_to_ensemble` — proceed but enable Ensemble mode. **Only offered when `ensembleMode` is false.** Reads `cruxMemories.meditate.modelPool` to compute count.
- `switch_to_single` — cancel Ensemble, run on a single model instead. **Only offered when `ensembleMode` is true.**
- `cancel` — cancel — I'll use a different approach.

**Behaviour rules** (Command lines 169–189):

- Always run on first invocation. Depth Selection runs first, then Cost Acknowledgment.
- Mode-swap updates active `meditateMode` (or `ensembleMode`) and proceeds to Theme Preflight without re-asking Q-Cost / Q-Depth.
- Cancel → short note, stop. Do NOT spawn anything, do NOT run Theme Preflight, do NOT create the working directory.
- Non-interactive sessions abort with a clear error explaining the cost-acknowledgment requirement; **never** silently default to `proceed`.

### 2.3 `Q-Cost-Acknowledgment-Expansion` (mandatory, calling-agent step 12 expansion path)

Source: Command lines 174–189.

**Prompt (verbatim)** — Command lines 178–185:

```
Expanding this meditation will spawn a new depth-{maxDepth} research tree
(~{N} additional agents) exploring the selected direction(s). This carries
the same per-meditation cost as the original invocation — a full recursive
tree, adversarial review cycle, and paired HTML + PDF report.

The previous meditation's results are preserved; this expansion produces a separate
report. If you only need a quick follow-up, consider a regular chat prompt instead.
```

**Options** (Command lines 187–188):

- `proceed_expansion` — Yes, spawn the expansion tree.
- `cancel` — Cancel — I'll follow up in chat instead.

**Behaviour rules**: mode-swap and depth options are **not** re-offered (both persist across expansions). User must `cancel` and re-invoke `/crux-meditate` to change mode/depth.

### 2.4 Theme Preflight Q1–Q5 (mandatory, Pattern A pre-collected before depth-0 spawn)

Source: Command lines 191–293.

**When**: always on first invocation; skip & reuse on expansion continuation (step 12) unless `$ARGUMENTS` contains `--retheme` or user asks to retheme (Command lines 211–215).

**Q1 — Theme source** (single-select, required) — Command lines 221–227:

- `match_repo` — Match the existing styling of files in this repo (scan `package.json`, `tailwind.config.*`, `*.css`, `*.scss`, `theme/`, `styles/`, design tokens, README screenshots)
- `preset` — Pick from a curated set of distinct preset directions
- `custom` — I'll describe a custom theme
- `surprise_me` — Pick something unexpected and deliberately different from the homogenised default

**Q1b — Repo scan confirmation** (only when Q1 = `match_repo`) — Command line 228: summarise found signals and ask `yes_use_them` / `yes_with_tweaks` / `no_pick_preset_instead`. If scan finds nothing useful, fall through to Q2.

**Q2 — Style direction** (single-select, required only if Q1 ≠ `match_repo` or Q1b = `no_pick_preset_instead`) — Command lines 230–240:

- `editorial` — magazine layout, serif headlines, asymmetric grids, drop caps, pull-quotes
- `scientific` — monospace + serif body, dense tables, IEEE-style figures, footnoted references
- `minimal_typographic` — system fonts, generous whitespace, no gradients, single accent color
- `bold_maximalist` — high-contrast colour blocks, oversized type, hand-drawn or marker accents
- `retro_print` — newspaper or vintage technical-manual styling, textured backgrounds, classical fonts
- `brutalist` — raw HTML aesthetics, intentional rough edges, monospace, minimal CSS, mono-color blocks
- `terminal_dossier` — green-on-black or amber-on-black CRT styling, ASCII-art dividers, monospace
- `architectural_blueprint` — blueprint-paper background, technical-drawing line weights, all-caps labels
- `surprise_me` — pick one of the above the user has not seen recently in this session

**Q3 — Colour scheme** (single-select, required) — Command lines 242–249:

- `cool_default` — the chosen direction's intended cool palette
- `warm_palette` — earth tones, terracotta, ochre, deep red
- `monochrome` — single-hue scale, no chromatic accents
- `high_contrast_minimal` — black/white plus one bold accent
- `repo_inferred` — derived from Q1 repo-scan results (only when source = `match_repo`)
- `custom_hex` — user supplies one or two hex codes (free text in a follow-up)

**Q4 — Typography** (single-select, required only when source ≠ `match_repo`) — Command lines 251–257:

- `serif_headings_sans_body`
- `sans_headings_sans_body`
- `mono_headings_mono_body`
- `serif_throughout`
- `mixed_distinctive` — pair two non-default fonts intentionally (e.g. Fraunces + JetBrains Mono); never just default-Inter

**Q5 — Confirmation** (single-select, always required) — Command line 261: one-line summary of chosen payload plus `confirm` / `restart_preflight` / `cancel_meditation`.

**Non-interactive `surprise_me` fallback** (hard rule) — Command lines 263–265:

> If the user does not engage with `askQuestion` (e.g. running non-interactively in CI), pick the `surprise_me` path for both Q1 and Q2 with a **deterministic-but-non-default** selection seeded by the topic-slug, then proceed without confirmation. **Never silently fall back to the homogenised default look.**

**Theming payload (verbatim YAML)** — Command lines 271–291:

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

The payload is included in the depth-0 subagent's spawn prompt as `theming:` and propagated **unchanged** to every child agent in the tree (Command line 293, Agent lines 305, 402, 831–832). Subagent must `abort with a clear error` if `theming` is missing from spawn prompt (Agent line 305).

### 2.5 Facet Confirmation `Q-Confirm-1` (mandatory, Pattern B at depth-0)

Source: Command lines 295–337.

**Prompt body (near-verbatim include + the 3 proposed facets)** — Command lines 313–323:

```
These 3 facets define the entire shape of the meditation — every branch and every
depth descends from them. Good facets are complementary (covering different angles
of the topic), independently explorable (each can go deep without needing the others),
and concretely scoped (a specific question or angle, not a vague theme).

If the facets look well-partitioned and you're happy with the exploration directions,
confirm and proceed. If one feels too broad, overlapping with another, or missing a
critical angle, modify it. If the overall partitioning feels wrong, regenerate for
a fresh set (up to 3 attempts).
```

**Options (single-select)** — Command lines 325–330:

- `confirm_all` — proceed with all 3 facets unchanged
- `modify_one` — change one facet (follow-up text input)
- `modify_multiple` — change multiple facets (follow-up text input)
- `regenerate` — discard these 3 and ask the subagent to derive a different set
- `cancel` — abort the meditation entirely

**Regeneration cap**: 3 attempts (Command line 332). Modify/regenerate handling resumes the subagent with `regenerate_facets: true` and the previous `facets-pending-{ts}.yml` path, or with `facet_overrides: [{ index, new_subfocus, new_slug? }, ...]`.

### 2.6 Facet Confirmation `Q-Confirm-2` (mandatory, asked once after `Q-Confirm-1`)

Source: Command lines 338–361.

**Prompt (verbatim)** — Command lines 342–353:

```
By default, deeper subfocuses (depth 2 and 3) are derived autonomously from each
parent's research findings — no further prompts. This is fastest and works well
when the top-level facets are well-scoped.

If you want more control, you can opt in to confirming subfocuses at deeper levels.
Be aware of the latency trade-off:
  - depth_2_only adds up to 9 confirmation prompts (3 per branch × 3 branches)
  - all_levels adds up to 36 additional prompts (9 at depth 2 + 27 at depth 3)
Each prompt pauses the exploration tree until you respond.

For most meditations, "none" is recommended. Use "depth_2_only" when you want to
steer the second level but trust the leaf-level derivation. Use "all_levels" only
for the highest-stakes explorations where you want full control over every subfocus.
```

**Options (single-select)** — Command lines 357–359:

- `none` (default — preselected) — auto-derive at depth 2 and depth 3
- `depth_2_only` — pause for confirmation at depth 2; auto-derive at depth 3
- `all_levels` — pause for confirmation at depth 2 and depth 3

### 2.7 `confirmDeepFacets` deep-YAML escalation (file-based, Pattern B via the poll loop)

Source: Command lines 363–431; Agent lines 491–509 (Research) and 563–571 (Quick).

**Pending file schema (verbatim)** — Command lines 376–397:

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

**Confirmation file schema (verbatim)** — Command lines 403–414:

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

**Per-child decision semantics** — Command lines 416–421:

- `confirmed` → use original child verbatim
- `modified` → replace with user-supplied subfocus/slug/rationale
- `regenerate` → re-derive that single child, write new pending file with same path-id but fresh `{ts}`, loop (**capped at 3 regenerations per child**)

**Depth-0 manager polling protocol** — Command lines 423–431; Agent line 407: depth-0 manager polls `pending-facets-*.yml` in working dir during the branch-output poll loop; batches multiple pending files into a single `needs_user_input` block; reuses same confirm/modify/regenerate option set as `Q-Confirm-1`; writes corresponding `confirmed-facets-{path-id}-{ts}.yml` for each; resumes branch-output poll.

**Re-spawn / continuation semantics** — Command lines 433–439: new meditation always re-runs depth-0 facet confirmation; reuses previous `confirmDeepFacets` value by default with an optional "keep deep-confirm setting?" follow-up.

---

## 3. Pattern A vs Pattern B Boundaries

Source-of-truth: Command lines 34–36 (Pattern B for the overall workflow); Agent lines 17–46 (subagent escalation protocol); Agent lines 302–307 (Meditate mode patterns).

### Pattern A (pre-collected before subagent spawn)

| Prompt | Why Pattern A | Source |
|--------|---------------|--------|
| `Q-Depth-Selection` | Sets `maxDepth` for the cost prompt; runs before anything else | Command lines 56–105 |
| `Q-Cost-Acknowledgment` | Single acknowledgment; mode-swap / cancel paths must not enter the tree | Command lines 106–189 |
| Theme Preflight Q1–Q5 (including Q1b repo-scan confirm) | Resolves `theming` payload; subagent must abort if payload is missing | Command lines 191–293 |
| Q1–Q5 `surprise_me` non-interactive fallback | Resolved by calling agent before spawn so subagent never re-asks | Command lines 263–265 |
| Ensemble model-pool read + per-model spawn parameters | Calling agent reads `.crux/crux-memories.json` and computes labels/counts before spawn | Command lines 545–570 |

### Pattern B (escalated from inside the subagent tree via `needs_user_input`)

| Escalation point | Origin | Schema | Source |
|------------------|--------|--------|--------|
| `Q-Confirm-1` (depth-0 facet confirmation) | Depth-0 subagent after step 4 derives facets; writes `facets-pending-{ts}.yml` | `needs_user_input` block referencing the pending file path + 3 proposed facets verbatim | Command lines 295–337; Agent lines 307, 374–385 |
| `Q-Confirm-2` (deep-facet enum) | Same flow, asked once after Q-Confirm-1 | `needs_user_input` (single-select) | Command lines 338–361; Agent line 307 |
| Deep-facet `pending-facets-*.yml` (depth_2_only / all_levels) | Any child agent at a depth requiring confirmation, batched by the depth-0 manager poll loop | File-based pending/confirmed pair; batched `needs_user_input` block | Command lines 363–431; Agent lines 407, 491–509, 563–571 |
| Adversarial review ambiguous `MUST_FIX` | Adversarial reviewer subagent (sub-mode of Meditate); never calls `AskQuestion` | `needs_user_input` block with **mandatory `context`** decision-guidance | Command lines 801–816; Agent lines 426 |
| Continuation menu after meditation completes (steps 10–12) | Calling agent runs `AskQuestion` after subagent returns | Multi-select with mandatory decision-guidance prose | Command lines 615–669; Agent lines 465–470 |

### Boundary rules

- **Subagents NEVER call `AskQuestion`** (Agent lines 17–20; Command line 34). The repo-wide rule from `AGENTS.md` is restated at every subagent escalation point.
- **Calling-agent (coordinator) owns every prompt** that requires interactive input — Command line 36 lists the four mandatory pre-spawn gates and the step 12 continuation menu.
- **`needs_user_input` schema** is the single mechanism for subagent → calling-agent escalation (Agent lines 31–44). When the parent resumes, answers arrive as `answers: { <question_id>: <selected_option(s)> }`.
- **`needs_user_input` for adversarial review MUST include a `context` field** with decision-guidance text — Command lines 801–816, restated Agent line 426.

---

## 4. Subagent Contracts (currently on `crux-cursor-memory-manager`)

All subagent contracts in this section currently live on the `crux-cursor-memory-manager` agent file and run when the agent is spawned in Meditate mode (or one of its sub-functions: Adversarial Review, Ensemble Aggregation). The decomposition spec moves these contracts to the new `crux-cursor-meditation-guide` agent and a family of `crux-skill-memory-meditation-*` skills — but the contracts themselves must remain semantically identical.

### 4.1 Research mode Phases A–G (per child agent at depth 1 through `maxDepth - 1`)

Source: Agent lines 472–550.

**Input parameters** (Agent lines 472–475): `meditateMode: "research"`, `workingDir`, `branchNumber`, `meditateDepth`, `maxDepth`, `subfocus`, `subfocusSlug`, `subfocusIndex`, `parentSubfocus`, `siblingFacets`, `theming` (propagated), `confirmDeepFacets` (propagated), `ensembleModel` (when set).

**Phase A** — Research own subfocus first (no children yet): query memory corpus via index (title, tag, description, body), examine code/files/web sources implied by subfocus, expand on subfocus, track every claim with at least one citation. (Agent lines 477–481)

**Phase B** — Write findings file first as working draft `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}-findings.md`. (Agent lines 483–484)

**Phase C** — Derive 3 child subfocuses from actual findings (Agent lines 486–515):

- Each narrower than agent's subfocus
- Each distinct from siblings
- Each globally unique against `facet-registry.yml`
- **Deep-confirmation hook** (when `confirmDeepFacets` requires it at this depth — `depth_2_only` at depth 1, OR `all_levels` at depth 1 or depth 2): write `pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml` **before** lock acquisition; poll matching `confirmed-facets-…-{ts}.yml`; apply per-child `confirmed`/`modified`/`regenerate` decisions (regen capped at 3 per child); only then proceed to registry-lock step.
- Acquire `mkdir`-based `.facet-registry.lock/`; read `facet-registry.yml`; check global slug + paraphrase uniqueness; refine collisions; append confirmed 3 subfocuses; release lock.

**Phase D** — Spawn 3 children at depth+1 in parallel (only when `meditateDepth < maxDepth`). Each child receives `meditateMode: "research"`, `workingDir`, `branchNumber`, `maxDepth`, `parentSubfocus`, `subfocus`, `subfocusSlug`, `subfocusIndex` (1, 2, or 3 — local to this parent's children), `siblingFacets`, `theming` (propagated unchanged), `confirmDeepFacets` (propagated unchanged), `ensembleModel` (if present — when set, pass `model: ensembleModel` on Task tool invocation). (Agent lines 517–524)

**Phase E** — Wait for child files via prefix-glob `branch-{N}-depth-{D+1}-sub-{S}-*.md`; resolve latest match per sibling-index with `ls -1t <workingDir>/<glob> 2>/dev/null | head -n 1`; **validate each child's citations strictly** — if any child's citations fail validation, delete that child's output file and respawn (**up to 2 retries** before recording a `## Citation failure` block and proceeding). (Agent lines 525–531)

**Phase F** — Incorporate child findings bottom-up by **REWRITING** this depth's own file (do NOT just append): weave children's findings into a coherent document, preserve every citation, deduplicate overlapping evidence, surface cross-child patterns, flag contradictions in `## Contradictions`, provenance via `[child: branch-N-depth-D-sub-S]` markers. (Agent lines 533–542)

**Phase G** — Promote findings file to final filename `branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md` (no `-findings` suffix); delete the `-findings` draft. (Agent lines 544–548)

**Leaf depth (`meditateDepth == maxDepth`)** — Phase A and Phase B only; promote `-findings` draft to final filename (Phase G shortcut); delete draft. With `maxDepth: 1`, depth-1 agents are leaves; with `maxDepth: 2`, depth-2 agents are leaves; default `maxDepth: 3`, depth-3 agents are leaves. (Agent line 550)

**Output body sections (mandatory, both modes)** — Agent lines 808–817:

- `## Subfocus Rationale`
- `## Discoveries`
- `## Connections`
- `## Child Subfocuses` (Phase C output, or Quick step 1)
- `## Child Insights` (Phase F or Quick step 6 aggregation)
- `## Contradictions`
- `## Summary`
- `## Citations` (mandatory in both modes)

**Frontmatter schema (verbatim)** — Agent lines 791–803:

```yaml
---
mode: "research"                          # or "quick"
branch: {N}
depth: {D}
subfocus_index: {S}                       # 0 at depth 1, 1–3 at depth 2, 1–3 at depth 3
subfocus_slug: "{kebab-case slug used in filename}"
subfocus: "{this agent's specific subfocus}"
parent_subfocus: "{parent agent's subfocus, or top-level facet if depth 1}"
parent_slug: "{parent's subfocus_slug, or null at depth 1}"
timestamp_utc: "{yyyymmddHHMMSS}"
timestamp_iso: "{ISO 8601}"
incorporated_children: ["branch-{N}-depth-{D+1}-sub-1-{slug}-{ts}.md", ...]   # empty at depth 3
---
```

### 4.2 Research mode depth-0 manager (steps 1–13)

Source: Agent lines 360–446.

| Step | Action | Source |
|------|--------|--------|
| 1 | Feature Guard — verify `flags.enableMemories == "true"` | Agent line 362 |
| 2 | Create working dir `meditations/{yyyymmdd}-{topic-slug}/` (numeric suffix if collision) | Agent line 364 |
| 3 | Seed empty `facet-registry.yml` and `citations-index.yml` (Research only) | Agent line 366 |
| 4 | Derive 3 top-level facets (cited) and run Q-Confirm-1 / Q-Confirm-2 via Pattern B; promote draft to `facets.md` after confirmation; **ensemble shortcut**: if `preConfirmedFacets` present, skip derivation/confirmation | Agent lines 368–388 |
| 5 | Spawn 3 background explorers with all parameters (`meditateMode`, `maxDepth`, `branchNumber`, `branchSlug`, `subfocus`, `siblingFacets`, `theming`, `confirmDeepFacets`, `ensembleModel`) | Agent lines 390–403 |
| 6 | Poll branch outputs via prefix-glob `branch-{N}-depth-1-sub-0-*.md`; deep-confirm hook globs `pending-facets-*.yml` and batches escalation | Agent lines 405–407 |
| 7 | Branch Peer Review (Research only) — spawn 3 peer reviewers in parallel | Agent lines 409 |
| 8 | Consolidate: read 3 depth-1 + 3 peer-review + `citations-index.yml`; write `consolidation.md` following Subject-Matter Focus rule | Agent lines 411–420 |
| 9 | Update `facets.md` with **Branch & Leaf Index** (glob actual filenames) | Agent line 422 |
| 10 | Adversarial review-and-fix cycle (cap 3 iterations); `MUST_FIX` escalations via `needs_user_input` with mandatory `context` | Agent lines 424–428 |
| 11 | Re-run step 9 only if verdict is `PASS` or `PASS_WITH_ADVISORIES` (reviewer may have rewritten files) | Agent line 430 |
| 12 | Generate mandatory paired HTML + PDF reports per `Report Generation — MANDATORY` (skip on `ESCALATE`) | Agent lines 432–442 |
| 12b | Write `retrospective-{ts}.md` (always written, including on `ESCALATE`) | Agent line 444 |
| 13 | Return to calling agent: workingDir, `facets.md`, `consolidation.md` (text + path), `retrospective-{ts}.md`, report pair (if generated), every `review-pre-report-*-iter-*.md`. On `ESCALATE` return everything except report paths plus structured summary of unresolved `MUST_FIX` findings | Agent line 446 |

### 4.3 Quick mode 6-step protocol (per child agent at depth < `maxDepth`)

Source: Agent lines 552–593.

**Input parameters**: `meditateMode: "quick"`, `workingDir`, `branchNumber`, `meditateDepth`, `maxDepth`, `subfocus`, `subfocusSlug`, `subfocusIndex`, `parentSubfocus`, `siblingFacets`, `theming` (propagated), `confirmDeepFacets` (propagated), `ensembleModel` (when set).

| Step | Action | Source |
|------|--------|--------|
| 1 | Pre-derive 3 child subfocuses upfront (no prior research). Each narrower than agent's subfocus, distinct from siblings, non-overlapping with `facets.md`. Sibling-aware only; no `facet-registry.yml` consultation. | Agent lines 557–562 |
| 2 | **Optional deep-confirmation hook** when `confirmDeepFacets` requires it: write `pending-facets-…-{ts}.yml`, poll for confirmed file, apply per-child decisions (cap 3 regens) | Agent lines 563–571 |
| 3 | Spawn 3 children at depth+1 in parallel with `meditateMode: "quick"`. Children receive all parameters including `theming`, `confirmDeepFacets`, `ensembleModel` (when set, pass `model: ensembleModel` on Task tool invocation) | Agent lines 573–578 |
| 4 | While children run, do this agent's own memory-query + expansion in parallel | Agent lines 580–581 |
| 5 | Wait for all 3 child files via prefix-glob `branch-{N}-depth-{D+1}-sub-{S}-*.md`. **Warn-only** on missing/unresolvable citations — do NOT respawn | Agent lines 583–585 |
| 6 | Aggregate children + own expansion into a single output file `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}.md` (no rewrite — straight aggregation under `## Child Insights` with `[child: ...]` provenance markers) | Agent lines 587–591 |

**Leaf (`meditateDepth == maxDepth`)**: query memories, expand, write leaf file. Citations still required in body + `## Citations`; warn-only on missing markers. (Agent line 593)

### 4.4 Quick vs Research differences table (verbatim)

Source: Agent lines 597–605.

| Aspect | Research (default) | Quick (`--quick`) |
|--------|--------------------|--------------------|
| Recursion order | Depth-first within each branch (parent finishes research before deriving children) | Pre-derived: parent derives all 3 child subfocuses upfront, no prior research required |
| Facet uniqueness | Global via `facet-registry.yml` + `mkdir`-based lock | Local sibling-aware only (read `facets.md` to avoid sibling overlap) |
| Citations | Mandatory; inline markers + `## Citations` section validated strictly by parent during Phase E (offending children re-spawned, up to 2 retries) | Mandatory; inline markers + `## Citations` section required, but parent validates best-effort and surfaces gaps as warnings rather than re-spawning |
| Bottom-up incorporation | Parent **rewrites** its own file (Phase F) to weave in children's findings | Parent appends `## Child Insights` section aggregating children |
| Peer review | Dedicated peer-review agents spawned post-branch-completion (depth-0 step 7) | None |
| Consolidation inputs | `branch-*` files + `branch-*-peer-review-*` files + `citations-index.yml` | `branch-*` files only |
| Coordination files | `facet-registry.yml`, `citations-index.yml`, `.facet-registry.lock/` (transient) | `facets.md` only |

### 4.5 Ensemble Aggregation function

Source: Agent lines 872–907.

**Spawn**: by calling agent's Ensemble Protocol step 9 with the `ensembleAggregation` flag. Spawn with `model: cruxMemories.meditate.ensembleAggregatorModel` if set, otherwise caller's own model. Parameters: `ensembleWorkingDir`, `modelSubdirs: [{slug,label,subdirPath}]`, `confirmedFacets`, `theming`, `meditateMode`, `topicSlug`. (Command lines 577–585; Agent lines 876–882)

**Workflow** (Agent lines 884–907):

1. Read all model consolidations + per-model `facets.md`; optionally branch files for detail.
2. Cross-model analysis: convergence detection (multi-model agreement scoring), divergence detection (per-model position + evidence + aggregator assessment), unique-insight detection (single-model finding credibility check), evidence-quality comparison, reasoning-style comparison.
3. Write `cross-model-synthesis.md` to ensemble root with `[model: {label}]` attribution; convergent uses `[models: all]`; unified deduplicated `## Citations` with per-citation model attribution.
4. Generate ensemble report `ensemble-report-{topic-slug}-{ts}.html` / `.pdf` per single-model report contract + ensemble-specific additions (model-comparison hero, per-facet comparison cards, agreement heatmap signature visualization, divergence deep-dives, per-model drill-down links, model-attribution Sankey, citation Venn, confidence radar). All standard content minimums (≥4 charts, ≥3 infographics, ≥1 calculator) still apply. Filenames share `{ts}`.
5. Return to calling agent: ensemble working directory path, `cross-model-synthesis.md` path, ensemble report HTML+PDF pair paths, ordered list of per-model subdirectory paths (each contains its own `consolidation.md`, `facets.md`, `report-{topic-slug}-{ts}.html` / `.pdf` pair). Include the follow-up adjustments reminder.

### 4.6 Adversarial Review function (sub-mode of Meditate)

Source: Command lines 737–876; Agent lines 424–428, 833.

**Reviewer agent** — Command lines 741–755: fresh `crux-cursor-memory-manager` subagent in **Adversarial Review** function, clean context, inputs `meditateMode`, `reviewerIteration` (1, 2, or 3), `workingDir`, `theming`, `priorReviewPath`.

**Editable files** (reviewer is the only agent permitted to rewrite during cycle): `facets.md`, `consolidation.md`, every `branch-*-depth-*-sub-*-*.md`, every `branch-*-peer-review-*.md`. (Command lines 753–754)

**Read-only**: `facet-registry.yml`, `citations-index.yml` (Research mode only). (Command line 754)

**Never touched**: `report-*.html`, `report-*.pdf`, `.facet-registry.lock/`, `facets-pending-*.yml`, `pending-facets-*.yml`, `confirmed-facets-*.yml`. (Command line 755)

**11 review dimensions** — Command lines 759–771 (also restated Agent line 833):

1. **Citation integrity** — every claim has inline marker; every marker resolves to `## Citations`; no unreferenced entries; `citations-index.yml` matches union (Research).
2. **Cross-file consistency** — no internal contradictions; cross-file contradictions surfaced in `## Contradictions`; `incorporated_children` frontmatter matches children actually merged.
3. **Substance and sparseness** — no empty / filler-only sections; no `(none discovered)` placeholders unless genuine.
4. **Slop detection** — block-listed phrases include `"It's important to note that…"`, `"In today's fast-paced world…"`, `"Let's dive in"`, `"stands as a testament to…"`, em-dash throat-clearing, `"not just X but Y"` tic, `"delve into"`, `"navigating the complexities of…"`.
5. **Calibration** — confidence matches evidence; absolute claims need multi-source citations or downgrade.
6. **Index integrity** — `facets.md` Branch & Leaf Index links resolve; missing-slots enumeration accurate; index metadata correct.
7. **Frontmatter validity** — required YAML fields present; `subfocus_slug` + `timestamp_utc` match filename; `incorporated_children` resolves.
8. **Anti-homogenization drift in prose** — flag homogenised-AI defaults regardless of theming preset (purple-blue gradient metaphors, synergy buzzwords, marketing-deck cadence).
9. **Peer review thoroughness** (Research mode only) — `## Reinforcements`, `## Contradictions`, `## Gaps`, `## New Evidence` substantively populated. **N/A in Quick mode.**
10. **Ready-for-report** — every quantitative claim in `consolidation.md` resolves to a sourced data point; every cross-branch theme traceable to specific findings.
11. **Subject-matter focus** — no "Branch 1/2/3" labels, no depth/leaf/agent references, no raw `[child: branch-N-depth-D-sub-S]` citations (must be `[research: {subfocus-slug}]`), no process-framing in executive summary. `MUST_FIX` and rewrite offending passages.

**Severity classification** (Command lines 773–779):

- `MUST_FIX` — blocks report generation. Reviewer applies unambiguous fixes; ambiguous → `fix_applied: false`, `reason: "ambiguous_fix"`, escalate via `needs_user_input` Pattern B with mandatory `context`.
- `SHOULD_FIX` — degrades quality but doesn't block. Applied automatically when unambiguous; otherwise logged with `reason: "ambiguous_fix"`.
- `ADVISORY` — observation only; never auto-applied; never blocks; always logged.

**Quick mode relaxations** (Command lines 779, 869–876):

- Citation integrity "missing inline marker" findings downgrade `MUST_FIX → SHOULD_FIX` (consistent with warn-only citation rule). Unresolvable markers that DO exist in body remain `MUST_FIX`.
- Peer review thoroughness dimension skipped entirely.

**Iteration loop (cap 3)** — Command lines 781–799 (verbatim):

```
iteration = 1
while iteration <= 3:
    spawn reviewer with reviewerIteration=iteration (fresh subagent each iteration)
    reviewer writes review-pre-report-{ts}-iter-{iteration}.md
    if verdict in {PASS, PASS_WITH_ADVISORIES}: break
    if reviewer escalated MUST_FIX via needs_user_input (Pattern B):
        calling agent runs askQuestion with reviewer-supplied decision-guidance,
        then resumes the reviewer with the user's resolutions; reviewer applies
        those resolutions, finalises the iteration document, and the loop continues.
    iteration += 1

if iteration > 3 and MUST_FIX still unresolved:
    verdict = ESCALATE
    abort report generation (sub-step 8.8 skipped)
    surface unresolved findings to the calling agent in sub-step 8.9 instead of report paths
```

**`MUST_FIX` `needs_user_input` schema (verbatim, with mandatory `context`)** — Command lines 803–816:

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

**Review document format** — Command lines 818–867: filename `review-pre-report-{yyyymmddHHMMSS}-iter-{N}.md`, frontmatter (`mode`, `iteration`, `reviewed_at`, `reviewer_agent`, `files_reviewed`, `prior_review`), sections `## Verdict` (`PASS` | `PASS_WITH_ADVISORIES` | `ESCALATE`), `## Summary` (counts X MUST_FIX, Y SHOULD_FIX, Z ADVISORY; A applied, B escalated, C deferred), `## MUST_FIX findings` (per-finding file, location, dimension, issue, fix_applied, fix, diff block), `## SHOULD_FIX findings`, `## ADVISORY findings`, `## Iteration log`, `## Carry-forward to next iteration`.

---

## 5. Coordination Conventions

Source-of-truth: the canonical reference lives in `.cursor/agents/crux-cursor-memory-manager.md` **Coordination Conventions** subsection (Agent lines 313–358) and is mirrored character-for-character in `.cursor/commands/crux-meditate.md` (Command lines 440–478). The command file explicitly states the agent file is the canonical reference; the command file mirrors it (Command line 442). Placeholders are defined exactly once in the agent file (Agent lines 331–336).

### 5.1 Artefact filename table (verbatim, from Agent lines 317–329 / Command lines 444–456)

| Artefact | Filename pattern | Notes |
|----------|------------------|-------|
| Top-level facets (initial, pre-confirmation) | `facets-pending-{ts}.yml` | Deleted after the user confirms via Q-Confirm-1 |
| Top-level facets (final, post-confirmation) | `facets.md` | Single navigational entry point; updated post-consolidation with the Branch & Leaf Index |
| Branch (depth 1, 2, 3) | `branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md` | `D` ∈ {1,2,3}; `S = 0` at depth 1, `S` ∈ {1,2,3} at depth 2, `S` ∈ {1,...,9} at depth 3 |
| Branch (intermediate, Phase B working draft) | `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}-findings.md` | Research mode only; deleted after Phase G promotion |
| Peer review (Research mode) | `branch-{N}-peer-review-{branchSlug}-{ts}.md` | One per branch |
| Pending deep-facet confirmation request | `pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml` | Only when `confirmDeepFacets ≠ none`; `D` is the **parent** agent's depth |
| Confirmed deep-facet response | `confirmed-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml` | Same path-id and `{ts}` as the pending file |
| Adversarial review iteration | `review-pre-report-{ts}-iter-{N}.md` | `N` ∈ {1, 2, 3}; iteration cap |
| Process retrospective | `retrospective-{ts}.md` | One per meditation; process analysis separate from subject-matter outputs |
| Report HTML | `report-{topic-slug}-{ts}.html` | Shares `{ts}` with PDF pair |
| Report PDF | `report-{topic-slug}-{ts}.pdf` | Shares `{ts}` with HTML pair |

### 5.2 Placeholders (defined once in Agent lines 331–336)

- `{topic-slug}` — slug component of working-directory name (extract everything after leading `yyyymmdd-`).
- `{slug}` (branch filenames) — kebab-case slug derived for that branch (depth 1) or subfocus (depth 2/3); max 40 chars; lowercase; alphanumerics + hyphens only; stop-words stripped; most meaningful 3–6 words.
- `{ts}` — UTC timestamp `yyyymmddHHMMSS` captured at write time: `date -u +%Y%m%d%H%M%S`.
- `{N}`, `{D}`, `{S}` — zero-padded numerals used as written above (`branch-1`, not `branch-01`).

### 5.3 Prefix-glob polling rule (verbatim, both files mirror)

Source: Agent lines 338–356; Command lines 458–478.

```
# Branch-output polls
branch-{N}-depth-1-sub-0-*.md            # depth-1 outputs
branch-{N}-depth-{D}-sub-{S}-*.md        # depth-D≥2 child outputs (one per child sibling-index)

# Peer review polls (Research mode)
branch-{N}-peer-review-*.md

# Report pair polls (verification gate)
report-{topic-slug}-*.html
report-{topic-slug}-*.pdf

# Pending deep-facet confirmation polls (depth-0 manager, when confirmDeepFacets ≠ none)
pending-facets-*.yml
```

**Resolve latest with**: `ls -1t <workingDir>/<glob> 2>/dev/null | head -n 1` for files where multiple regenerations have occurred (reports and review iterations).

**Never hard-code these names** (Agent line 358; Command line 478): all references in the agent definition, command file, and Branch & Leaf Index match these files via the prefix glob `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf`; **never** hard-code `report.html` / `report.pdf`. This rule is the single canonical statement; mirrored verbatim in the command file's Coordination Conventions and Report filenames subsections.

### 5.4 Facet registry lock semantics (Research mode only)

Source: Agent lines 607–653.

**Schema (append-only, verbatim)** — Agent lines 611–628:

```yaml
facets:
  - branch: 1
    depth: 0
    parent_slug: null              # null at depth 0; otherwise parent's subfocus_slug
    subfocus_slug: "auth-flow-trade-offs"
    subfocus: "Trade-offs in authentication flows for multi-tenant SaaS"
    timestamp_utc: "20260516103045"
    registered_by: "depth-0 manager"
  - branch: 1
    depth: 2
    parent_slug: "auth-flow-trade-offs"
    subfocus_slug: "session-vs-jwt"
    subfocus: "Session cookies vs JWT for cross-service auth"
    timestamp_utc: "20260516103217"
    registered_by: "branch-1 depth-1 agent"
  # ...
```

**Lock-and-append protocol (verbatim)** — Agent lines 630–651:

```bash
attempts=0
until mkdir "{workingDir}/.facet-registry.lock" 2>/dev/null; do
  attempts=$((attempts + 1))
  if [ $attempts -gt 60 ]; then
    echo "Failed to acquire facet-registry lock after 60s" >&2
    exit 1
  fi
  sleep 1
done

# inside lock:
# 1. Read facet-registry.yml
# 2. For each candidate subfocus, verify slug + paraphrase uniqueness
#    against ALL existing entries (every branch, every depth)
# 3. If collision, regenerate the colliding subfocus and re-check
# 4. Once all 3 candidates are globally unique, append them

rmdir "{workingDir}/.facet-registry.lock"
```

**Orphan recovery** (Agent line 653; Command line 495): if any branch's prefix-glob has been pending for more than 5 minutes AND `.facet-registry.lock/` exists, the depth-0 manager during step 6 (branch-output polling) logs a warning and `rmdir`s the stale lock.

### 5.5 Citations index format (Research mode only)

Source: Agent lines 655–690.

**Inline citation markers** (mandatory in the body, attached to the claim) — Agent lines 659–663:

- `[memory: title-or-id]`
- `[file: path/to/file.ts:start-end]`
- `[web: url]`
- `[chat: turn-N or quoted text]`
- `[child: branch-N-depth-D-sub-S]`

Every output file (depth-1/2/3, peer-review, consolidation) must include a `## Citations` section listing every source; use inline markers throughout the body; (Research) append every newly-introduced citation to `citations-index.yml`.

**`citations-index.yml` schema (verbatim)** — Agent lines 673–681:

```yaml
citations:
  - kind: "memory"            # one of: memory | file | web | chat | child
    ref: "agent-harness-orchestration-patterns"
    cited_by:
      - "branch-1-depth-1-sub-0-{slug}-{ts}.md"
      - "branch-2-depth-2-sub-1-{slug}-{ts}.md"
    note: "Patterns for parent-child handoff in async agent trees"
```

**Validation enforcement** (Agent lines 683–690):

- **Research mode**: parent reading a child file MUST verify the `## Citations` section is non-empty and every inline marker resolves. If validation fails, parent **deletes the child file and respawns** the child with instructions to add missing citations. After **2 failed retries**, parent records a `## Citation failure` block in its own file naming the offending child and proceeds.
- **Quick mode**: parents log warnings and proceed (no respawn). Report's executive summary must include a "Citation gaps" callout listing every uncited finding.

### 5.6 Peer review file spec (Research mode only)

Source: Agent lines 692–720.

**Filename pattern**: `branch-{N}-peer-review-{branchSlug}-{yyyymmddHHMMSS}.md` (one per branch — three files total; spawned in parallel by depth-0 step 7).

**Frontmatter (verbatim)** — Agent lines 698–703:

```yaml
---
peer_review_for_branch: {N}
reviewer_agent: "branch-{N} peer reviewer"
reviewed_branches: [1, 2, 3]
timestamp_utc: "{yyyymmddHHMMSS}"
---
```

**Required sections** (Agent lines 706–720):

- `## Reinforcements` — points where this branch's findings independently reinforce a sibling — cite both.
- `## Contradictions` — points where this branch contradicts a sibling — cite both, propose which is more strongly supported.
- `## Gaps` — aspects a sibling could have explored but didn't, given what this branch discovered — cite the discovery that revealed the gap.
- `## New Evidence` — new sources this peer reviewer surfaces while comparing branches.
- `## Citations` — full citation list — this branch's sources, siblings' sources, and any new sources.

### 5.7 Retrospective template (`retrospective-{ts}.md`)

Source: Command lines 900–965.

**Filename**: `retrospective-{yyyymmddHHMMSS}.md` — same `{ts}` as the report pair when one was generated, or a fresh UTC timestamp on `ESCALATE`.

**Required sections (verbatim YAML + headings)** — Command lines 908–965:

```yaml
---
mode: "research" | "quick"
topic_slug: "{topic-slug}"
generated_utc: "2026-05-17T12:34:56Z"
verdict: "PASS" | "PASS_WITH_ADVISORIES" | "ESCALATE"
---
```

**Section list (mandatory)**:

- `## Process Retrospective — {topic title}`
- `### Summary Statistics` — Mode; Total agents spawned (`{count}` with breakdown); Branch files produced (breakdown by depth); Peer reviews count (Research mode) or N/A (Quick); Adversarial review iterations + final verdict; MUST_FIX findings (total found → applied / escalated / unresolved); SHOULD_FIX findings (total → applied); ADVISORY findings count; Missing slots (list or "none"); Facet regeneration attempts (0 = confirmed on first try); Deep-facet confirmations (0 = `confirmDeepFacets` was `none`).
- `### What Went Well` — substantive observations (not generic praise): branches with richest findings, facet-partitioning quality, cross-branch convergences, citation coverage, peer-review value (Research), adversarial-review accuracy.
- `### What Could Be Improved` — honest weakness assessment: thin/repetitive branches, partitioning problems, citation gaps, adversarial findings that should've been caught earlier, ESCALATE causes, coordination issues, depth-3 marginal value, Quick-vs-Research mode-fit.
- `### Structural Observations` — branch balance, depth utility, peer-review impact ratio (Research), adversarial-review efficiency, subject-matter focus compliance.
- `### Recommendations for Future Meditations` — facet suggestions, mode recommendation, areas needing deeper exploration, over-provisioning observations.

**Always written**, including on `ESCALATE` (process analysis especially valuable when review cycle failed). The retrospective is **the one output where process-oriented language is expected** — the Subject-Matter Focus rule does **not** apply here. (Command line 902; Agent line 444)

### 5.8 Branch & Leaf Index template (appended to `facets.md`)

Source: Command lines 671–735; Agent line 422.

**Construction rule**: glob the working directory for actual filenames; use relative paths (no `./` prefix); never reconstruct names from memory.

**Required structure (verbatim)** — Command lines 677–724:

```
---
(existing facets.md frontmatter / content above this line is unchanged)
---

## Branch & Leaf Index

### Branch 1 — {branch-1 facet title}
**Subfocus**: {one-line facet description}

- **Depth 1 (root)**: [{branch-1-slug}](branch-1-depth-1-sub-0-{branch-1-slug}-{ts}.md)
- **Depth 2** (3 subfocuses):
  - [Sub 1 — {d2-sub-1-slug}](branch-1-depth-2-sub-1-{d2-sub-1-slug}-{ts}.md)
  - [Sub 2 — {d2-sub-2-slug}](branch-1-depth-2-sub-2-{d2-sub-2-slug}-{ts}.md)
  - [Sub 3 — {d2-sub-3-slug}](branch-1-depth-2-sub-3-{d2-sub-3-slug}-{ts}.md)
- **Depth 3** (up to 9 leaves):
  - Under D2-sub-1:
    - [Sub 1 — {slug}](branch-1-depth-3-sub-1-{slug}-{ts}.md)
    - [Sub 2 — {slug}](branch-1-depth-3-sub-2-{slug}-{ts}.md)
    - [Sub 3 — {slug}](branch-1-depth-3-sub-3-{slug}-{ts}.md)
  - Under D2-sub-2: ...
  - Under D2-sub-3: ...
- **Peer review** (Research mode only): [branch-1 peer review](branch-1-peer-review-{branch-1-slug}-{ts}.md)

### Branch 2 — ...
### Branch 3 — ...

### Top-level artifacts
- [Consolidation](consolidation.md)
- [Process Retrospective](retrospective-{ts}.md)
- [Report (HTML)](report-{topic-slug}-{ts}.html)
- [Report (PDF)](report-{topic-slug}-{ts}.pdf)
- Adversarial review iterations (one entry per `review-pre-report-*-iter-*.md` discovered):
  - [Review iter 1](review-pre-report-{ts}-iter-1.md)
  - [Review iter 2](review-pre-report-{ts}-iter-2.md) _(only if iteration 2 ran)_
  - [Review iter 3](review-pre-report-{ts}-iter-3.md) _(only if iteration 3 ran)_
- Facet confirmation trail (one entry per pending/confirmed pair discovered):
  - [Confirmed facets — branch 1 depth 1 sub 0](confirmed-facets-branch-1-depth-1-sub-0-{ts}.yml) _(only when `confirmDeepFacets ≠ none`)_
  - …
- [Facet registry](facet-registry.yml) _(Research mode only)_
- [Citations index](citations-index.yml) _(Research mode only)_

### Index metadata
- **Generated**: {ISO 8601 timestamp of index update}
- **Mode**: `research` | `quick`
- **Total files indexed**: {count}
- **Missing slots**: {list any branch/depth/sub combinations that did not produce a file, or "none"}
```

**Conventions** (Command lines 728–735):

- Display label of each link = file's `subfocus_slug` from frontmatter, prefixed with local sub-index.
- Group depth-3 leaves under their depth-2 parent. Sibling indices 1–3 → D2-sub-1; 4–6 → D2-sub-2; 7–9 → D2-sub-3.
- If a slot didn't produce a file, omit the link AND list the slot under "Missing slots".
- "Top-level artifacts" subsection always lists `consolidation.md` + `retrospective-{ts}.md` + report HTML/PDF pair (when generated) + every review iteration + every confirmed-facets pair. Registry / citations-index lines appear only in Research mode. Retrospective is always present (even on `ESCALATE`).
- Quick mode omits per-branch "Peer review" lines and the two Research-only registry/index lines.
- When `ESCALATE`, report HTML/PDF lines are omitted; every `review-pre-report-*-iter-*.md` is still linked.

**Pending coordination files** (`facets-pending-*.yml`, `pending-facets-*.yml`) are **never** linked from the index — only confirmed counterparts. (Command line 726)

---

## 6. Mandatory Report Contract

Source-of-truth: Command lines 969–1328 (`Report Generation — MANDATORY`) and Command lines 1330–1483 (`Ensemble Aggregation Report — MANDATORY`); cross-referenced from Agent lines 432–442 (depth-0 step 12 obligation) and Agent lines 835–840 (design principle).

### 6.1 Paired HTML + PDF rule

- **Both** files are MANDATORY in both Research and Quick mode. (Command line 971; Agent line 835)
- Produced automatically as part of step 8 (calling-agent block) / step 12 (subagent block) — never opt-in. (Command lines 971–973)
- Reports are **never** built over a failing adversarial review (`ESCALATE` aborts the section). (Command line 973; Agent line 428)
- Capture a single UTC `TS=$(date -u +%Y%m%d%H%M%S)` at the start of generation; reuse for both filenames. (Command lines 1256–1261)
- Filenames: `report-{topic-slug}-{yyyymmddHHMMSS}.html` and `report-{topic-slug}-{yyyymmddHHMMSS}.pdf`. (Command lines 977–985)
- `{topic-slug}` must exactly match the slug component of the working-directory name. (Command line 982)
- All references must use prefix glob `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf`. **Never hard-code `report.html` / `report.pdf`.** (Command lines 985, 478)

### 6.2 Anti-Homogenisation Rules (forbidden defaults)

Source: Command lines 197–209 (pre-flight context) and 1174–1194 (canonical block in Report Generation); referenced as a hard rule from Agent lines 437, 832.

**Forbidden as defaults** unless the user's `theming` payload explicitly invokes them (Command lines 1180–1188):

- Purple-blue (or blue-purple) gradient hero banner (`linear-gradient(135deg, indigo, blue/violet)` and friends).
- Inter-700 / Inter-800 as the headline typeface.
- Three-card feature grids as the dominant section layout.
- Doughnut chart paired with tinted-circle category legend chips.
- Tailwind `indigo-500` (or `#6366f1` / `#818cf8`) as the accent.
- `lucide`-style icon-in-tinted-circle motif for stat cards / bullets.
- Centred body paragraphs and "Most popular" pricing pills.
- Five-star testimonial rows and DiceBear avatar fallbacks.
- Smooth modern dark blue UI when no theming choice asked for it.

Canonical screenshot reference (avoidance target): `assets/image-8bca59a2-5c28-4614-9fe8-98a395c28f57.png`. (Command line 1178)

**How to apply** (Command lines 1190–1194):

1. Before any CSS, pick concrete values from `theming` payload (font stack, primary/secondary/accent hex, layout grammar, divider style, link decoration, heading scale).
2. If chosen direction would naturally produce a forbidden pattern, deliberately substitute (e.g. editorial direction → serif drop-cap hero; brutalist → flat blocks, no rounded corners; terminal_dossier → ASCII-art dividers).
3. Include a `theme:` annotation in the footer naming the resolved direction, palette, typography.

### 6.3 Universal Contrast (WCAG-style)

Source: Command lines 1205–1231; restated as design principle Agent line 836.

**Minimum contrast requirements** — Command lines 1209–1214:

- Body text / table text / captions / labels / legends / footnotes / citation markers / nav links / badge text / chart labels: WCAG AA normal-text (≥4.5:1) against actual background.
- Large headings + large stat numerals: WCAG AA large-text (≥3:1); ≥4.5:1 preferred.
- Non-text graphical elements (chart lines, SVG connectors, axes, grid lines, quadrant boundaries, heatmap cells, risk-meter segments, badges, table borders, focus rings): WCAG non-text (≥3:1); ≥4.5:1 preferred for thin lines (<2px).
- Interactive focus outlines + active nav states: ≥3:1 against component AND surrounding background.

**Hard rules** — Command lines 1216–1224:

- Never place text directly on gradient / texture / image / translucent overlay / saturated colour block without a sufficiently-opaque backing panel and verified contrast.
- Do NOT rely on pastel text, low-opacity strokes, faint grid lines, transparent fills, glow-only emphasis, colour-only distinctions. Pair colour with labels / patterns / symbols / explicit text.
- Chart.js + D3 palettes must be generated separately for dark, light, print modes — passing in dark does NOT imply passing in light or print.
- Every SVG/HTML infographic must define explicit stroke + text colours per colour mode.
- Heatmap + quadrant labels must remain readable in every cell/region (switch per-cell label colour `light-on-dark` / `dark-on-light` or add label pills).
- Thin lines (axes, connectors, borders) must be thickened / darkened / spaced if they'd otherwise fall below contrast.
- Disabled / secondary UI may be subdued, must still be readable, must not encode substantive findings.

**Recommended CSS variables**: `--text-strong`, `--text-muted-readable`, `--line-strong`, `--line-subtle-readable`, `--chart-label`, `--chart-axis`. (Command line 1231)

### 6.4 Light / Dark mode + Print TOC

Source: Command lines 1233–1248, 1283–1292.

**Light + Dark mode (mandatory)** — Command lines 1233–1241:

- Both modes required.
- Default = dark mode on first load, regardless of system preference.
- Toggle in nav — clearly visible button (sun/moon icon or "☀ Light / ☾ Dark" label); switches immediately with no flicker.
- Persistence via `localStorage` key `meditation-color-mode`; applied to `<html>` before paint to avoid FOUC.
- `window.matchMedia('(prefers-color-scheme: dark)')` only as fallback when no localStorage value exists.
- Both modes must satisfy Universal Contrast for every element.
- Chart.js colour values must adapt to active mode via CSS custom properties.

**Responsive Navigation (mandatory)** — Command lines 1243–1248:

- Wide viewport (`≥768px`) — horizontal nav across top, grouped into facet-derived clusters (e.g. *Overview*, *Data Capture*, *Decision Engine*, *Simulation*, *Cross-Cutting Analysis*, *Citations*) with 1px divider or extra spacing. Group labels recommended for ≥6 anchors.
- Narrow viewport (`<768px`) — hide horizontal nav; replace with burger button (three lines, top-right); tap opens slide-in drawer or full-screen overlay; same grouped link list vertically stacked.
- Pure CSS + minimal JS. No external nav library. `aria-expanded`/`aria-controls`; focus trap inside open drawer.
- Active-section highlighting as the user scrolls (both viewport modes).

**Table of Contents (mandatory in PDF)** — Command lines 1283–1292:

- `<nav id="toc" aria-label="Table of contents">` immediately under hero, before per-facet sections.
- Every `<h2>` / `<h3>` has a stable kebab-case `id` (e.g. `id="data-capture-crux-storage"`).
- Headless Chrome preserves anchor links → clickable PDF bookmarks.
- Two levels deep (top-level sections + branch subheadings).
- Right-aligned page numbers next to each entry encouraged but optional.
- `<style>@media print { #toc { page-break-after: always; } }</style>` — TOC on its own page.

**Print theme** — Command lines 1263–1281: high-contrast, distinct from on-screen dark mode:

- Background: pure white (`#fff`) or near-white (`#fafafa`).
- Body text: near-black (`#0a0a0a` / `#111`), minimum 11pt.
- Headings: `#000` with chosen theme's display typeface preserved.
- Links: dark accent (`#0033aa` or theme-equivalent), underlined.
- Tables: black 1px borders, alternating row backgrounds at `#f5f5f5`.
- Chart.js: re-rendered with high-contrast opaque palettes, no near-white fills, `borderWidth: 2`, labelled data points where space allows.
- D3.js: `.d3-interactive` hidden; `.d3-static-fallback` shown via `@media print` + `[data-print-mode="true"]` rules; ≥1.5px strokes, solid fills, permanent inline labels, computed-final-state positions.
- Calculators: `.calculator-interactive` hidden; `.calculator-static-fallback` shown.
- Infographics: solid black or theme-dark foreground; white backgrounds; drop shadows / glows / partial-opacity tints stripped or strengthened.
- Hide: sticky nav, color-mode toggle, burger button, hover-only tooltip widgets, filter/sort UI controls (data preserved). Citation tooltips → inline footnote markers (`[7]`) resolving in Citations.
- Page breaks: every top-level section starts on a new page (`page-break-before: always`); `page-break-inside: avoid` on tables / charts / infographic blocks.

**Default `pdf_color_mode`** = `light_high_contrast` (Command line 1281). Dark-PDF overrides allowed only if every element passes Universal Contrast.

### 6.5 Chart.js / D3 / calculator inclusion rules + static fallbacks

Source: Command lines 1068–1173.

**Minimum content** — Command lines 1068–1070, 1119–1121, 1137–1146, 1170–1172, 1328:

- **≥4 distinct chart types** from Chart.js + D3.js combined.
- **≥3 distinct infographic types** (hand-rolled HTML + CSS + inline SVG; no extra libraries).
- **≥1 interactive calculator** if the meditation surfaces a quantifiable trade-off.
- Filterable tables for any tabular finding (filter / sort UI hidden in print; default-sorted data preserved).
- Tooltips on inline citation markers (hover → inline footnote markers in print).
- Small `--quick` meditations that lack breadth must still meet all mandatory structural elements; substitute additional comparison matrices / scorecards / hierarchy diagrams to compensate so the report is never sparse.

**Chart.js types** — Command lines 1076–1082: bar / stacked bar; radar; doughnut / pie; line / area; scatter / bubble; polar area; mixed bar+line.

**D3.js types (facet-specific)** — Command lines 1086–1095, verbatim table:

| Facet kind | Suitable D3 chart types |
|------------|-------------------------|
| **Hierarchy / structural decomposition** (e.g. branch → depth-2 → depth-3 tree) | Tree (`d3-hierarchy` cluster/tree), dendrogram, sunburst, treemap, partition, icicle |
| **Networks / relationships** (e.g. cross-branch citation overlap, memory-to-finding linkage) | Force-directed graph, chord diagram, hierarchical edge bundling, arc diagram |
| **Flows / process volumes** (e.g. how findings cascade from depth-1 → depth-3) | Sankey, alluvial/parallel sets |
| **Time-series with interaction** | Brushable timeline, zoomable area chart, focus+context |
| **Geographic** | Choropleth, hex bin, projection-aware map |
| **Multi-dimensional comparison** | Parallel coordinates, brushed scatter matrix, radar with brush |
| **Calendar / temporal density** | Calendar heatmap |
| **Custom facet-specific** | Hand-coded D3 — always include the print degradation pair |

**CDN allowlist** — Command lines 1097, 1322–1326:

- Chart.js: `https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js`
- D3.js: `https://d3js.org/d3.v7.min.js` (pin to latest stable major on CDN)
- D3 plugins (`d3-sankey`, `d3-cloud`) from same official CDNs
- Custom fonts from Google Fonts or `https://rsms.me/` **only if** chosen theme requires a non-system font; never load a font just because Inter is "the default".
- No other external scripts / stylesheets / assets. **No runtime `fetch()` calls.** All data embedded inline as JavaScript constants.

**Infographics list (≥3 distinct from)** — Command lines 1121–1133: hierarchy / tree diagrams; comparison matrices (option × criterion); decision trees / flow diagrams; scorecards; process / pipeline diagrams; quadrant / 2×2 matrices; heatmaps; risk meters / gauges; timeline ribbons; concept maps; Venn diagrams.

**D3 print degradation table (verbatim, mandatory)** — Command lines 1103–1110:

| D3 pattern | Print degradation strategy |
|------------|---------------------------|
| **Hover tooltips** | Replace tooltips with permanent inline labels OR a paired data table beneath the chart listing every value the tooltip would have shown. |
| **Brushable / zoomable** | Render the **most informative zoom level** (typically full-extent overview) with explicit axis labels and tick marks; if multiple zoom levels are essential, render a small-multiples grid showing each zoom level as its own static panel. |
| **Click-to-drill / expand-collapse** | Render the **fully expanded** state. If too dense to be readable on one page, render top-level overview followed by per-section detail panels on subsequent pages. |
| **Animated transitions** (e.g. force simulation settling) | Compute the final settled state at module scope (or pre-render via one-shot tick loop) before paint; PDF captures final positions, not in-progress animation. |
| **Interactive filtering** (e.g. parallel coordinates with brushes) | Render the unfiltered full view AND a paired summary table or small-multiples grid showing data faceted by the dimensions the user would normally brush on. |
| **Cannot degrade meaningfully** | **Forbidden** — pick a different visualization, or pair the D3 chart with a co-located static SVG / Chart.js fallback; print mode hides the interactive D3 chart and shows only the static pair. |

**HTML implementation pattern (verbatim)** — Command lines 1112–1117:

```html
<div class="d3-chart" data-degradation-strategy="...">
  <div class="d3-interactive"><!-- on-screen interactive render --></div>
  <div class="d3-static-fallback" hidden><!-- print-state render --></div>
</div>
```

```css
@media print { .d3-interactive { display: none } .d3-static-fallback { display: block } }
[data-print-mode="true"] .d3-interactive { display: none } [data-print-mode="true"] .d3-static-fallback { display: block }
```

**Sanity-render verification gate** — Command line 1117: render HTML twice (normal + `?print=1`) and confirm every D3 chart shows non-empty static fallback in print render. Fix empty fallback before generating PDF.

**Interactive calculator static fallback (verbatim, mandatory)** — Command lines 1137–1168:

- Every calculator must include `.calculator-static-fallback` rendering **3–5 pre-computed what-if scenarios**.
- Scenario types (pick deliberately): **Typical / baseline**, **Optimistic**, **Pessimistic**, **Threshold / breakeven**, **Recommended** (when meditation surfaces one).
- Each scenario row lists every input value plus computed output(s) with units, formatted exactly as the on-screen calculator would format.
- Short caption above table explains scenario meaning and which finding motivated it (with citation).
- Forbidden: empty fallback, single scenario, fallback that just lists input fields without computed results.
- Implementation pattern mirrors D3 print-degradation pattern:

```html
<div class="calculator" data-degradation-strategy="what-if-table">
  <div class="calculator-interactive"><!-- inputs, button, result panel --></div>
  <div class="calculator-static-fallback" hidden>
    <!-- caption explaining scenarios + table of 3-5 pre-computed rows -->
  </div>
</div>
```

```css
@media print {
  .calculator-interactive { display: none }
  .calculator-static-fallback { display: block }
}
[data-print-mode="true"] .calculator-interactive { display: none }
[data-print-mode="true"] .calculator-static-fallback { display: block }
```

**Calculator verification gate** — Command line 1168: render HTML with `?print=1` and confirm every calculator's static fallback is non-empty AND contains ≥3 fully-populated scenario rows. Empty / inputs-only / under-populated fallbacks must be fixed before PDF generation.

**Report Comprehensiveness — No Information Loss** — Command lines 1006–1018:

- Every quantitative data point in any branch file must appear in the report (chart, table, infographic, or inline).
- Every comparison or trade-off must be visualized or tabulated, not just mentioned in prose.
- Every cited source contributing a material finding must appear in Citations with a backlink.
- Every contradiction or tension (including from peer review) must be explicitly surfaced.
- **Input coverage verification**: before declaring complete, enumerate key findings from each branch file's `## Discoveries` / `## Summary` and verify each has a corresponding presentation element; fill gaps.
- Anti-sparseness escalation: if report contains fewer distinct data points than branch files surfaced collectively, re-read branch files and add missing content before PDF render.

**Option Comparison Research Reporting** — Command lines 1020–1066 (mandatory when applicable):

- Activation: confirmed facets correspond to distinct named options, OR topic-slug contains "compare" / "comparison" / "versus" / "vs" / "evaluate" / "evaluation" / "alternatives" / "options" / "which" / "best" / "selection" / "choose" / "decision".
- Required elements: (1) feature comparison matrix (rows × columns with cell-level indicators ✓/✗/◐, ratings, color-coded; sortable in HTML, default-sorted by overall score in PDF; footnotes for nuanced cells); (2) adoption and market presence (market share, trend direction, community health, timeline); (3) **Gartner Magic Quadrant-style 2×2 visualization** (D3 or hand-rolled SVG; X = breadth, Y = depth/maturity; quadrant labels e.g. "Leaders / Challengers / Visionaries / Niche Players"; in PDF static fallback: permanent labels on each circle, axis values visible, quadrant regions clearly shaded; analytical placement only — not a reproduction of any copyrighted Gartner report); (4) key differentiators section (3–7 decisive differentiators, named option excels/lags + one-sentence evidence + citation; visual scorecards / bar charts / annotated comparison strips; decision-driving differentiators visually emphasised); (5) recommendation or decision framework (decision tree / flowchart / weighted scorecard).
- Standard content minimums (≥4 charts / ≥3 infographics / ≥1 calculator) still apply **additively**: the quadrant counts toward charts; the feature matrix + differentiators count toward infographics; a TCO/ROI calculator counts toward calculators.

### 6.6 Headless Chrome → Chromium degradation

Source: Command lines 1294–1316.

**Render command (verbatim)** — Command lines 1298–1302:

```
google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf="${PDF}" \
  --print-to-pdf-no-header \
  --no-pdf-header-footer \
  "file://${HTML}?print=1"
```

**HTML detection**: must read `URLSearchParams` on load and apply `data-print-mode="true"` to `<html>` when `print=1` is set so print theme + TOC styles apply during headless render even outside `@media print`. (Command line 1304)

**Fallback chain** — Command line 1306: try `chromium` and `chromium-browser` as fallback binaries if `google-chrome` is not installed.

**No-Chromium failure mode** — Command line 1306; Agent line 440: if no headless Chromium binary is available, the meditation **fails** with a clear error: report missing dependency, list platform-specific install hint (`brew install --cask google-chrome` on macOS, `apt install chromium` on Debian/Ubuntu, etc.), and **leave the HTML file in place** so user can manually print to PDF. **Never silently skip the PDF.**

**Final verification (verbatim)** — Command lines 1310–1316:

```
HTML_LATEST=$(ls -1t "{workingDir}"/report-"{topic-slug}"-*.html 2>/dev/null | head -n 1)
PDF_LATEST=$(ls -1t  "{workingDir}"/report-"{topic-slug}"-*.pdf  2>/dev/null | head -n 1)
[ -s "${HTML_LATEST}" ] && [ -s "${PDF_LATEST}" ]
```

Regenerate the missing artifact in place if check fails.

### 6.7 Ensemble Aggregation report extras

Source: Command lines 1330–1483.

**Ensemble working directory structure (verbatim)** — Command lines 1336–1357:

```
meditations/{yyyymmdd}-{topic-slug}-ensemble/
├── facets.md                                    # shared confirmed facets (bare — no Branch & Leaf Index)
├── model-gpt-5.5/                               # complete meditation tree for GPT 5.5
│   ├── facets.md                                # per-model copy with Branch & Leaf Index
│   ├── consolidation.md
│   ├── facet-registry.yml                       # Research mode only
│   ├── citations-index.yml                      # Research mode only
│   ├── branch-*-depth-*-sub-*-*.md
│   ├── branch-*-peer-review-*.md                # Research mode only
│   ├── review-pre-report-*-iter-*.md
│   ├── retrospective-{ts}.md
│   ├── report-{topic-slug}-{ts}.html
│   └── report-{topic-slug}-{ts}.pdf
├── model-opus-4.7/                              # complete meditation tree for Opus 4.7
│   └── ...same structure...
├── model-gemini-pro-3.1/                        # complete meditation tree for Gemini Pro 3.1
│   └── ...same structure...
├── cross-model-synthesis.md                     # aggregation output
├── ensemble-report-{topic-slug}-{ts}.html       # ensemble-level report
└── ensemble-report-{topic-slug}-{ts}.pdf        # ensemble-level PDF
```

Subdirectory names: kebab-case version of each model's `label` from `cruxMemories.meditate.modelPool`, prefixed `model-` (e.g. `model-gpt-5.5`). (Command line 1359)

**Ensemble filename conventions (verbatim table)** — Command lines 1365–1369:

| Artefact | Filename pattern | Location |
|----------|------------------|----------|
| Shared facets | `facets.md` | Ensemble root |
| Per-model tree | `model-{label-slug}/` | Ensemble root |
| Cross-model synthesis | `cross-model-synthesis.md` | Ensemble root |
| Ensemble report HTML | `ensemble-report-{topic-slug}-{ts}.html` | Ensemble root |
| Ensemble report PDF | `ensemble-report-{topic-slug}-{ts}.pdf` | Ensemble root |

**`cross-model-synthesis.md` frontmatter + sections (verbatim)** — Command lines 1378–1460:

Frontmatter:

```yaml
---
ensemble_mode: true
meditate_mode: "research" | "quick"
model_count: {N}
models:
  - slug: "gpt-5.5-medium"
    label: "GPT 5.5"
    subdir: "model-gpt-5.5"
  - slug: "claude-opus-4-7-thinking-xhigh"
    label: "Opus 4.7"
    subdir: "model-opus-4.7"
  - slug: "gemini-3.1-pro"
    label: "Gemini Pro 3.1"
    subdir: "model-gemini-pro-3.1"
aggregator_model: "{model slug or 'caller'}"
timestamp_utc: "{yyyymmddHHMMSS}"
---
```

Mandatory sections: `## Executive Summary` (one-paragraph cross-model verdict, leading with substantive conclusion); `## Convergence — High-Confidence Findings` ([models: all] attribution; combined citation strength); `## Divergence — Areas of Disagreement` (per-model position + reasoning + evidence + aggregator's better-supported assessment + confidence indicator); `## Unique Insights — Single-Model Discoveries` ([model: label] attribution; credibility assessment, hallucination flagging); `## Evidence Quality Comparison`; `## Reasoning Style Comparison`; `## Recommended Synthesis`; `## Per-Model Report Index` (links per model: HTML, PDF, consolidation); `## Citations` (unified deduplicated with [model: label] attribution).

**Ensemble report structural extras** — Command lines 1466–1483:

- **Model comparison hero**: instead of single stat-card row, show N model cards side-by-side, each with that model's headline finding + convergence/divergence indicator.
- **Per-facet comparison cards**: each confirmed facet shows each model's key conclusion in parallel columns/cards with `[model: label]` attribution and visual convergence indicator (green = agree, amber = partial, red = disagreement).
- **Agreement heatmap** (REQUIRED, signature visualisation): facet × model matrix (Chart.js or D3) where cell color encodes degree of pairwise agreement per facet.
- **Divergence deep-dives**: each major divergence gets its own section with competing positions side-by-side + aggregator's assessment.
- **Per-model drill-down links**: every section includes links to corresponding section in each model's individual HTML report.
- **Recommended additional visualisations**: Model attribution Sankey; Citation Venn diagram (shared vs model-unique); Confidence radar (per-facet confidence overlaid).
- **Model attribution citation format**: every finding carries `[model: {label}]` (e.g. `[model: GPT 5.5]`, `[model: Opus 4.7]`); convergent uses `[models: all]`. Listed in `## Citations` with backlinks.
- All standard content minimums (≥4 charts, ≥3 infographics, ≥1 calculator, filterable tables, light/dark mode, PDF degradation) still apply.

---

## 7. Continuation Menu — Calling-Agent Steps 9–12

Source: Command lines 615–669 (single-model); Command lines 594–613 (ensemble); Agent lines 465–470 (informational summary).

### 7.1 Single-model step 9 — Verify mandatory report artifacts

Command lines 617–623 (verbatim):

```
HTML_LATEST=$(ls -1t "{workingDir}"/report-"{topic-slug}"-*.html 2>/dev/null | head -n 1)
PDF_LATEST=$(ls -1t  "{workingDir}"/report-"{topic-slug}"-*.pdf  2>/dev/null | head -n 1)
[ -s "${HTML_LATEST}" ] && [ -s "${PDF_LATEST}" ]
```

If either resolves empty or size check fails, calling agent regenerates the missing artifact per Report Generation — MANDATORY before continuing. If PDF specifically missing because no headless Chromium binary is available, surface that error and the platform-specific install hint **prominently** in step 10. On `ESCALATE` verdict, step 9 is a no-op (no report pair generated; step 10 reports unresolved findings instead of report paths).

### 7.2 Single-model step 10 — Present to user

Source: Command line 625.

- Read `consolidation.md` (or use returned text).
- Display consolidated insights organised by facet theme (using facet titles, not branch numbers), highlighting cross-cutting connections, quality-review findings (Research), citation gaps (Quick), unresolved `MUST_FIX` findings (on `ESCALATE`).
- **Always include absolute paths** to: `workingDir`, `facets.md`, `retrospective-{ts}.md`, latest `report-{topic-slug}-{ts}.html`, latest `report-{topic-slug}-{ts}.pdf` (resolved via step 9 globs).
- On `ESCALATE`: list `workingDir`, every `review-pre-report-*-iter-*.md`, and unresolved findings summary instead of report paths (retrospective path always included).
- End with reminder: further content edits / visual refinements / theme adjustments / contrast tweaks / regenerated report variants → request in a new agent session pointed at `workingDir`.

### 7.3 Single-model step 11 — Interactive continuation

Source: Command lines 627–661.

**Prompt body (sample, multi-select, with mandatory decision-guidance prose)** — Command lines 629–653:

```
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
```

**Options (multi-select)** — Command lines 655–659:

- Discovered tangent directions (derived from the exploration) — one option per discovered direction; each acts as an expansion trigger.
- `save_spec` — "Save meditation as draft spec" (write insights as draft spec outline to the configured specs directory).
- `end_meditation` — "End meditation" (complete the session).

**Forbidden options (removed in subtask 05)** — Command line 661, Agent line 469: do NOT offer "Save as interactive HTML report" or "Save as PDF report" — both artefacts are now produced automatically.

### 7.4 Single-model step 12 — Handle the user's selection

Source: Command lines 663–669.

- **Expansion direction(s)**: first run `Q-Cost-Acknowledgment-Expansion`. If user cancels, stop without spawning. If proceeds, augment context with new directions + user input, repeat from step 2 (new subagent → new mandatory Theme Preflight, new Pattern-B depth-0 facet-confirmation escalation, new adversarial review cycle, new paired report). New meditation always re-runs depth-0 facet confirmation; previous `confirmDeepFacets` reused by default with optional "keep deep-confirm setting?" follow-up. Mode-swap options from initial Q-Cost-Acknowledgment are NOT re-offered (mode persists across expansions); user must `cancel` and re-invoke `/crux-meditate` to change mode.
- **`save_spec`**: write a draft spec outline file to the configured specs directory using the consolidation summary, the Branch & Leaf Index, and the confirmed top-level facets as input. Report absolute path back to user.
- **`end_meditation`**: complete the session. Remind user that further adjustments (content / theming / visual design / contrast / report variants) can be made in a new agent session pointed at `workingDir`.

### 7.5 Ensemble mode steps 10–13 — Calling-agent block

Source: Command lines 594–613.

- **Step 10 (verify artifacts)** — verify all N per-model report pairs + ensemble-level synthesis and report pair:

  ```
  SYNTH="${ensembleWorkingDir}/cross-model-synthesis.md"
  ENS_HTML=$(ls -1t "${ensembleWorkingDir}"/ensemble-report-"${topic-slug}"-*.html 2>/dev/null | head -n 1)
  ENS_PDF=$(ls -1t  "${ensembleWorkingDir}"/ensemble-report-"${topic-slug}"-*.pdf  2>/dev/null | head -n 1)
  [ -s "${SYNTH}" ] && [ -s "${ENS_HTML}" ] && [ -s "${ENS_PDF}" ]
  ```

  Regenerate any missing artifact.

- **Step 11 (present)** — read `cross-model-synthesis.md` from ensemble root; display cross-model analysis organised by synthesis dimensions (convergence / divergence / unique insights). Include absolute paths to: ensemble synthesis, ensemble report pair, each per-model report pair, each per-model `facets.md`. End with same follow-up reminder.

- **Step 12 (interactive continuation)** — same `AskQuestion` multi-select as single-model with additions: per-model expansion options ("Explore {direction} deeper using {model-label}" — spawns a single-model expansion tree on chosen model); `save_spec` (writes ensemble synthesis as draft spec with cross-model evidence); `end_meditation`.

- **Step 13 (handle selection)** — same as single-model. Expansion trees from an ensemble meditation run as single-model meditations (NOT re-ensembled) unless user explicitly passes `--ensemble` again.

---

## 8. Subject-Matter Focus Rule (applies to `consolidation.md` + HTML/PDF reports)

Source: Command lines 878–898; restated as design principle Agent line 837.

**Forbidden in consolidation and reports** (internal process concepts):

- References to "Branch 1", "Branch 2", "Branch 3" as organisational labels → use **facet title or subfocus description** instead (e.g. "Data Capture and Storage", not "Branch 1").
- References to "depth-1", "depth-2", "depth-3", "leaf agents", "leaf docs", "sub-agents", or agent counts.
- Raw `[child: branch-N-depth-D-sub-S]` citation format → translate to `[research: {subfocus-slug}]` using the subfocus slug.
- References to "peer-review agents" or "peer reviewers" as actors → use "cross-cutting analysis", "independent verification", "quality review".
- "this meditation explored X across three branches" or similar process-framing in executive summaries → use "This analysis covers X" / "This research examines X".

**Required**:

- Section headings use facet titles + subfocus descriptions.
- Organisational framing follows subject matter's natural structure (theme → sub-theme → detail).
- Cross-references reference topics by name.
- Executive summaries lead with substantive conclusion.
- `## Citations` section maps subject-matter citation markers to source files for traceability; reader never needs to parse `branch-N-depth-D-sub-S` notation.

**Scope**: applies to `consolidation.md` and HTML/PDF reports only. Internal coordination files (`facets.md` Branch & Leaf Index, branch outputs, peer-review files, `facet-registry.yml`, `citations-index.yml`, `retrospective-{ts}.md`) retain their process-oriented naming.

---

## 9. Cross-Repo Touchpoints

| File | Path | Reference / Line | Role | Source |
|------|------|------------------|------|--------|
| `/crux-amnesia` explicit-command list (rule restating that explicit memory commands override amnesia mode) | `.cursor/commands/crux-amnesia.md` | Line 40 | Lists `/crux-meditate` as a memory command that should be treated as direct user intent | grep `/crux-amnesia` |
| `/crux-amnesia` explicit-command list (Available memory commands section) | `.cursor/commands/crux-amnesia.md` | Line 63 | Lists `/crux-meditate — Recursive memory-informed exploration` | grep `/crux-amnesia` |
| `commands.meditate` config entry | `.crux/crux-memories.json` | Lines 46–50 | `{ "file": ".cursor/commands/crux-meditate.md", "default": "/crux-meditate", "description": "Recursive memory-informed exploration and insight synthesis" }` | `.crux/crux-memories.json` |
| `cruxMemories.meditate.modelPool` + `ensembleAggregatorModel` | `.crux/crux-memories.json` | Lines 80–87 | Ensemble model pool (3 entries) + aggregator override (null) | `.crux/crux-memories.json` |
| AGENTS.md memory-manager agent row | `AGENTS.md` | Line 27 | `crux-cursor-memory-manager` row that lists "Meditate" among its purposes | `AGENTS.md` |
| AGENTS.md subagent-protocol example | `AGENTS.md` | Line 59 | Lists `/crux-meditate` among commands invoking subagents | `AGENTS.md` |
| AGENTS.md "Memory lifecycle operations" allocation row | `AGENTS.md` | Line 75 | Routes memory lifecycle (dream, REM, recall) work to `crux-cursor-memory-manager` (no explicit meditate row — meditate is currently bundled under memory manager) | `AGENTS.md` |
| README.md meditation command rows (Memory Commands table) | `README.md` | Lines 682–683 | `/crux-meditate` (no args) + `/crux-meditate "topic"` rows | `README.md` |
| README.md amnesia override paragraph | `README.md` | Line 689 | Lists `/crux-meditate` among explicit memory commands that override amnesia | `README.md` |
| README.md File Reference table | `README.md` | Line 799 | `.cursor/commands/crux-meditate.md — Recursive exploration command` | `README.md` |
| README.md Memory System summary row | `README.md` | Line 947 | `Meditate Command — .cursor/commands/crux-meditate.md — Recursive memory exploration` | `README.md` |
| `docs/crux-memories.md` Memory Commands table | `docs/crux-memories.md` | Line 23 | `/crux-meditate ["topic"]` row with description | `docs/crux-memories.md` |
| `docs/crux-memories.md` agent narrative | `docs/crux-memories.md` | Lines 46, 252–253, 692, 718, 720, 775, 777, 818, 836–837, 855, 1112–1114 | Multiple references: agent invocation, cross-platform command mapping, amnesia carve-out, config wiring (cursor / claude-code / generic platforms), QA checklist | `docs/crux-memories.md` |
| `docs/crux-memories.md` config example | `docs/crux-memories.md` | Lines 316–319 | `commands.meditate.file` config block (same as `.crux/crux-memories.json`) | `docs/crux-memories.md` |
| `docs/crux-memories.md` QA checklist Q. Meditate Command | `docs/crux-memories.md` | Lines 1138–1153 | User-acceptance checks for `/crux-meditate` invocations, facet derivation, working-dir contents | `docs/crux-memories.md` |
| `web/compress.md/memories.html` landing SVG label | `web/compress.md/memories.html` | Line 52 | `/crux-meditate` SVG text label in command list | `web/compress.md/memories.html` |
| `web/compress.md/memories.html` command card | `web/compress.md/memories.html` | Lines 807–816 | `/crux-meditate` command card with three usage forms | `web/compress.md/memories.html` |
| `web/compress.md/memories.html` Meditate section | `web/compress.md/memories.html` | Lines 868–908 | "Meditate: Recursive Exploration" landing section + diagram | `web/compress.md/memories.html` |
| `install.py` `MEMORY_FILE_PREFIXES` enumeration | `install.py` | Line 61 | `.cursor/commands/crux-meditate.md` listed in memory-file prefixes installed by `install.py` | `install.py` |
| `install.py` fallback file list | `install.py` | Line 502 | `.cursor/commands/crux-meditate.md` listed in the fallback / dist-zip command set | `install.py` |
| `install.py` config-write defaults | `install.py` | Lines 800–803 | `commands.meditate` block written when generating `.crux/crux-memories.json` | `install.py` |
| `scripts/create-crux-zip.py` DIST_FILES | `scripts/create-crux-zip.py` | Line 38 | `.cursor/commands/crux-meditate.md` enumerated as a release asset | `scripts/create-crux-zip.py` |
| `.cursor/agents/crux-cursor-memory-manager.md` Meditate Mode section (THE BULK OF EXECUTABLE CONTRACTS LIVES HERE) | `.cursor/agents/crux-cursor-memory-manager.md` | Lines 279–841 (Meditate Mode) + Lines 872–907 (Ensemble Aggregation Mode) | All Phases A–G, Quick 6-step, Adversarial Review, Ensemble Aggregation, design principles | Source file |
| `.cursor/commands/crux-meditate.md` (calling-agent surface) | `.cursor/commands/crux-meditate.md` | Entire file 1–1494 | All calling-agent gates, continuation menu, mandatory-report contract | Source file |

**Touchpoints introduced by the decomposition spec** (not yet present — listed for subtask 10 to track):

- New agent file `.cursor/agents/crux-cursor-meditation-guide.md` — must be added to install.py, create-crux-zip.py, AGENTS.md table, README rows, CONTRIBUTORS.md table, version-bump RELEASE_PATHS (if needed), `.crux/dist-manifest.json`.
- Six new skill directories `.cursor/skills/crux-skill-memory-meditation-{research,quick,ensemble,review,report,coordination}/SKILL.md` — same enumeration surfaces.

**CRUX-compressed mirror surfaces** (subtask 11 scope; only regenerate existing maintained mirrors — never create new ones, never edit generated files):

- `.cursor/rules/crux-memories-integration.crux.mdc` ← `.cursor/rules/crux-memories-integration.md`
- `.cursor/rules/docs-sync.crux.mdc` ← `.cursor/rules/docs-sync.md`
- `.cursor/rules/version-bump.crux.mdc` ← `.cursor/rules/version-bump.md`
- `.cursor/rules/zip-contents-protection.crux.mdc` ← `.cursor/rules/zip-contents-protection.md`
- `AGENTS.md` is a source file in this repo; `AGENTS.crux.md` is **not** maintained — do **not** require or create it (per spec K8).

---

## 10. Source-of-Truth Map

Two-column concordance: every contract item back-traceable to a current source location. Subtask 02 plans moves against this map; subtask 12 verifies that the post-refactor repo preserves every row.

### 10.1 Command file `.cursor/commands/crux-meditate.md`

| Contract item | Line range | Section heading |
|--------------|-----------|-----------------|
| Header / repository link | 1–5 | `# crux-meditate` |
| Usage CLI examples (5 forms) | 7–18 | `## Usage` |
| Modes summary table (Research / Quick / Ensemble) | 20–28 | `## Modes` |
| Spawn instructions + Pattern B + 4 pre-spawn gates intro | 30–36 | `## Instructions` |
| Argument handling (flag detection, slug stripping, remaining args) | 38–53 | `### Argument Handling` |
| Depth Selection (gate 1) — overview + agent count table + Q-Depth-Selection prompt + options + behaviour rules | 55–105 | `### Depth Selection — MANDATORY (calling agent's very first action)` |
| Cost & Scope Acknowledgment (gate 2) — overview + runtime table + Q-Cost-Acknowledgment + ensemble variant + options + behaviour rules + Q-Cost-Acknowledgment-Expansion | 106–189 | `### Cost & Scope Acknowledgment — MANDATORY (calling agent's second action)` |
| Theme Preflight (gate 3) — Anti-Homogenisation context + when to run + Q1–Q5 sequence + Q1b repo-scan + surprise_me fallback + theming YAML payload | 191–293 | `### Theme Preflight — MANDATORY (calling agent runs before spawning the subagent)` |
| Facet Confirmation (gate 4, Pattern B) — depth-0 confirm flow + Q-Confirm-1 + Q-Confirm-2 + deep-confirm flow + pending/confirmed schemas + re-spawn semantics | 295–439 | `### Facet Confirmation — MANDATORY at depth 0, opt-in deeper` |
| Coordination Conventions (artefact filename table + prefix-glob polling rules + never-hard-code rule) | 440–478 | `### Coordination Conventions` |
| What Happens — workflow chooser (steps 1–8 subagent block + steps 9–12 calling-agent block) | 480–485 | `### What Happens` |
| Research mode steps 1–8 (sub-step expansion 1–10 inside step 8) | 486–515 | `#### Research mode (default)` |
| Quick mode steps 1–8 substitutions | 517–540 | `#### Quick mode (`--quick`)` |
| Ensemble mode protocol (steps 1–10 calling-agent + steps 9–12 ensemble-specific) | 541–613 | `#### Ensemble mode (`--ensemble`)` |
| Steps 9–12 single-model calling-agent block (verify report pair / present / interactive continuation / handle selection) | 615–669 | `**Steps 9–12: Calling-agent block (both modes, single-model)**` |
| Branch & Leaf Index template + conventions | 671–735 | `### Branch & Leaf Index (appended to `facets.md`)` |
| Adversarial Review and Fix Cycle — reviewer agent + 11 dimensions + severity classification + iteration loop + Pattern-B escalation schema + review document format + Quick-mode treatment | 737–876 | `### Adversarial Review and Fix Cycle — MANDATORY` |
| Subject-Matter Focus rule | 878–898 | `### Subject-Matter Focus — MANDATORY (all user-facing outputs)` |
| Process Retrospective template (frontmatter + required sections) | 900–967 | `### Process Retrospective — MANDATORY` |
| Report Generation — MANDATORY (filenames + inputs + HTML structural elements + comprehensiveness + option comparison + visualisations + infographics + interactive elements + anti-homogenisation rules + theming application + Universal Contrast + light/dark mode + responsive nav + PDF requirements + filename pairing + print theme + TOC + render command + final verification + other styling rules) | 969–1328 | `### Report Generation — MANDATORY` |
| Ensemble Aggregation Report (ensemble working dir + filename conventions + cross-model synthesis schema + ensemble report extras + model-attribution citations) | 1330–1483 | `### Ensemble Aggregation Report — MANDATORY (when `ensembleMode` is true)` |
| Related links (agent, skills, sibling commands) | 1485–1493 | `## Related` |

### 10.2 Agent file `.cursor/agents/crux-cursor-memory-manager.md`

| Contract item | Line range | Section heading |
|--------------|-----------|-----------------|
| Critical context loading rules | 9–16 | `## CRITICAL: Load Context First` |
| User Input Escalation — Pattern A / Pattern B / `needs_user_input` schema | 17–46 | `## User Input Escalation — CRITICAL` |
| Expertise list (Meditate listed, Ensemble Aggregation listed) | 48–58 | `## Your Expertise` |
| Skills used (memory-extract, memory-crud, memory-rebalance, memory-compress, memory-reference-tracker, memory-index) | 60–71 | `## Skills You Use` |
| Operating Modes header | 73 | `## Operating Modes` |
| **Meditate Mode** — invocation variants table + mode selection + cost ack pattern + theme pattern + facet confirmation pattern + file-based coordination intro + working dir + Coordination Conventions canonical table + placeholders + prefix-glob polling + never-hard-code rule | 279–358 | `### Meditate Mode — `/crux-meditate`` |
| Research mode depth-0 workflow steps 1–13 (incl. pre-confirmed facets shortcut for ensemble) | 360–446 | (within Meditate Mode) |
| Step-numbering provenance note | 448 | (within Meditate Mode) |
| Quick mode top-level workflow (steps 1–13 substitutions) | 450–463 | (within Meditate Mode) |
| Post-subagent flow (calling-agent steps 9–12 informational summary) | 465–470 | (within Meditate Mode) |
| Recursive exploration protocol — Research mode (Phases A–G + deep-confirmation hook) | 472–550 | (within Meditate Mode) |
| Recursive exploration protocol — Quick mode (6-step + step 2 deep-confirmation hook) | 552–593 | (within Meditate Mode) |
| Quick vs Research differences table | 595–605 | (within Meditate Mode) |
| Facet registry protocol (schema + mkdir lock + orphan recovery) | 607–653 | (within Meditate Mode) |
| Citations protocol (inline markers + per-file requirements + index schema + validation rules) | 655–690 | (within Meditate Mode) |
| Peer review file spec (filename + frontmatter + required sections) | 692–720 | (within Meditate Mode) |
| Subfocus narrowing example | 722–745 | (within Meditate Mode) |
| Working directory structure (canonical tree) | 747–784 | (within Meditate Mode) |
| Output file format (frontmatter + body sections) | 786–819 | (within Meditate Mode) |
| Design principles list (file-based coord / 3-way fan-out / predictable paths / mandatory citations / mode-specific traits / open-mindedness / concise outputs / pre-spawn gates / facet confirmation / theming / adversarial review / Branch & Leaf Index / mandatory reports / Universal Contrast / Subject-Matter Focus / Report Comprehensiveness / Option Comparison / Visualizations & PDF degradation / Ensemble model propagation) | 821–841 | (within Meditate Mode) |
| Forget Mode (separate mode; included for cross-reference completeness) | 843–870 | `### Forget Mode — `/crux-forget`` |
| Ensemble Aggregation Mode (internal sub-mode of Meditate) — invocation + workflow steps 1–5 | 872–907 | `### Ensemble Aggregation Mode — (internal, spawned by calling agent's Ensemble Protocol)` |
| Agent scoping rules | 909–923 | `## Agent Scoping Rules` |
| Critical rules (feature guards / data integrity / workflow discipline / skill delegation) | 925–946 | `## Critical Rules` |

### 10.3 Mapping summary by contract section

| Freeze section | Command source | Agent source |
|----------------|----------------|--------------|
| §1 Modes inventory | 20–28, 38–46, 60–67 | 279–305 |
| §2 Calling-agent gates | 55–439 | 303–307 |
| §3 Pattern A/B boundaries | 34–36, 195–196 | 17–46, 302–307 |
| §4 Subagent contracts — Research Phases A–G | (mirror) 486–515 | 472–550 |
| §4 Subagent contracts — depth-0 manager steps 1–13 | 486–615 | 360–446 |
| §4 Subagent contracts — Quick 6-step | 517–540 | 552–593 |
| §4 Subagent contracts — Ensemble Aggregation | 541–613, 1330–1483 | 872–907 |
| §4 Subagent contracts — Adversarial Review (11 dims, severities, ≤3 iters, MUST_FIX schema) | 737–876 | 424–428, 833 |
| §5 Coordination conventions (filenames / globs / locks / citations / peer review / retro / B&L index) | 440–478, 671–735, 900–967 | 313–358, 472–550, 607–720, 747–784 |
| §6 Mandatory report contract | 969–1483 | 432–442, 832, 834–840 |
| §7 Continuation menu (steps 9–12) | 594–613, 615–669 | 465–470 |
| §8 Subject-Matter Focus rule | 878–898 | 837 |
| §9 Cross-repo touchpoints | (n/a — external) | (n/a — external) |

---

## Definition of Done — Subtask 01

- [x] Freeze document exists in spec directory: `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260517.md`.
- [x] Every contract item back-traced to current source line range or section heading (Section 10).
- [x] Document referenced from spec index Execution Notes (Section 11 of spec — see `spec-meditate-agent-skill-decomposition-20260517.md` Execution Notes).
- [x] Markdown-only artefact; no linter errors introduced.

---

_Captured by `crux-platform-architect` against repo `/home/andrewv/git/cursor/CRUX-Compress` at git SHA `b4fc33b0c034866bb60b7fe7b03be9e0c7a18bbf` on 2026-05-17. Subsequent subtasks must treat this document as the **freeze line** — any deviation requires an explicit `needs_user_input` escalation surfaced through the calling agent._
