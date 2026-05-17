# crux-meditate

Recursive memory-informed exploration of themes, topics, and intent through 3-level deep agent inception.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-meditate                          - Explore facets derived from current chat context
/crux-meditate "topic or question"      - Explore a specific theme
/crux-meditate @file.ts @folder/        - Explore facets around referenced code
/crux-meditate --quick "topic"          - Fast parallel-fanout exploration (legacy behaviour)
/crux-meditate --ensemble "topic"       - Run on multiple model families in parallel, then aggregate
/crux-meditate --ensemble --quick "topic" - Ensemble of Quick-mode trees
```

The `--quick` and `--ensemble` flags may appear anywhere in `$ARGUMENTS` and may be combined with any of the other forms.

## Modes

| Mode | Flag | Default? | Behaviour |
|------|------|----------|-----------|
| **Research** | _(none — default)_ | yes | Depth-first serial recursion. Each depth's findings drive the next depth's facet derivation. Globally unique facet allocation across all branches. Bottom-up incorporation. Branch peer review at the top. **Mandatory citations at every step.** |
| **Quick** | `--quick` | no | Fast parallel fan-out (legacy behaviour). All 3 facets per node derived upfront and explored in parallel. **Citations are still mandatory** (same `## Citations` requirement as Research mode), but the parent validates them best-effort and warns rather than re-spawning offending children. Use when you want speed over rigor. |
| **Ensemble** | `--ensemble` | no | Run the entire meditation process N times in parallel (one per model family from `cruxMemories.meditate.modelPool`), sharing the same user-confirmed facets, then aggregate findings into a cross-model synthesis report. Combinable with `--quick` (ensemble of Quick trees) or default Research mode. Each model tree runs independently; the aggregation highlights convergence, divergence, and unique insights. See the dedicated **Ensemble Protocol** section below. |

Both modes share every user-facing safeguard (cost ack, theme preflight, facet confirmation, the post-consolidation Branch & Leaf Index update in `facets.md`, and the mandatory adversarial review-and-fix cycle — see the dedicated sections below; mandatory report generation is fully documented by subtask 05). They differ only in the recursion model and coordination machinery described below. Ensemble mode wraps either Research or Quick mode and adds cross-model aggregation on top.

## Instructions

When this command is invoked, spawn a `crux-cursor-memory-manager` subagent in Meditate mode. The manager orchestrates a 3-level recursive exploration by spawning child instances of itself, each querying memories, expanding on discoveries, and writing consolidated insights to markdown files in a shared working directory.

**User input escalation — CRITICAL**: This command uses **Pattern B (work first, then escalate)** — the subagent tree must complete its recursive exploration before the user can decide on next steps. Subagents in the meditation tree NEVER call `AskQuestion` directly. ALL user-facing interactions (selecting expansion directions, saving as spec/report, ending meditation) are handled by the **parent agent** (you) using `AskQuestion` after the subagent tree completes.

**Critical**: All agents coordinate through markdown files in `meditations/{yyyymmdd}-{topic-slug}/`, not through in-context return values or JSONL transcript polling. The subagent performs **steps 1–8** (mode-specific — see **What Happens** below) and writes `consolidation.md` to the working directory. You then read that file and handle **steps 9–12** directly with the user. Four mandatory pre-spawn user gates — **Depth Selection**, **Cost & Scope Acknowledgment**, **Theme Preflight**, and (mid-flow) **Facet Confirmation** — fire before the subagent tree spawns; see the dedicated sections below.

### Argument Handling

**Mode selection (perform before topic-slug derivation)**: Inspect the raw `$ARGUMENTS` string for the `--quick` and `--ensemble` flags (case-sensitive, surrounded by whitespace or at the start/end of the string).

- If `--quick` is present → set `meditateMode: "quick"` and follow the **Quick mode protocol**. **Strip the flag from `$ARGUMENTS` before deriving the topic-slug** so the slug never contains `--quick`.
- If `--ensemble` is present → set `ensembleMode: true`. **Strip the flag from `$ARGUMENTS` before deriving the topic-slug** so the slug never contains `--ensemble`. Read `cruxMemories.meditate.modelPool` from `.crux/crux-memories.json` to determine which models to run. If the pool is empty or missing, abort with a clear error pointing the user at the config. `--ensemble` can combine with `--quick` (ensemble of Quick-mode trees) or run with default Research mode.
- If neither flag is present → set `meditateMode: "research"` (the default and recommended path for any work that will be cited, persisted, or used to drive downstream changes), `ensembleMode: false`.

Propagate the resolved `meditateMode` into the depth-0 subagent's task prompt; the subagent in turn forwards `meditateMode` to every child it spawns so the entire tree uses the same protocol. When `ensembleMode` is true, propagate `meditateMode` to each model-specific depth-0 subagent (they all share the same mode).

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

After Depth Selection, the calling agent runs a single `askQuestion` that surfaces the cost-and-scope tradeoff — using the accurate agent count for the selected depth — and lets the user proceed, swap modes, or cancel.

#### Approximate agent count and runtime per mode

| Mode | Agent count (at selected depth) | Runtime (typical) | Use when |
|------|---------------------------------|-------------------|----------|
| **Research** (default) | ~{researchCount} agents (see depth table above) | minutes to tens of minutes depending on depth | High-stakes strategic problems where citation rigor, peer review, and incorporation depth justify the cost |
| **Quick** (`--quick`) | ~{quickCount} agents (same tree minus peer reviewers) | substantially faster | Broad early-stage exploration where citations are still required but peer-review and citation re-spawn enforcement are not |
| **Ensemble + Research** (`--ensemble`) | ~{N×researchCount + 1} agents ({N} complete Research trees + 1 cross-model aggregation agent), where N = length of `cruxMemories.meditate.modelPool` | N× Research runtime (parallel) + aggregation | Maximum-confidence analysis where cross-model convergence/divergence is the deliverable |
| **Ensemble + Quick** (`--ensemble --quick`) | ~{N×quickCount + 1} agents ({N} complete Quick trees + 1 aggregation agent) | N× Quick runtime (parallel) + aggregation | Broad ensemble exploration when speed matters more than per-tree rigor |

Substitute `{researchCount}` and `{quickCount}` with the accurate per-tree agent counts from the **Agent count by depth and mode** table for the user's selected `maxDepth`. These counts exclude the calling agent itself and the per-iteration adversarial review subagents (which can run 1–3 times per model tree depending on findings).

#### Q-Cost-Acknowledgment (mandatory single-select)

Prompt:

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

When `ensembleMode` is true, replace the first paragraph with:

    /crux-meditate --ensemble will run {poolSize} complete depth-{maxDepth} meditation
    trees in parallel — one per model family ({modelLabels}) — spawning approximately
    {N} agents total, then aggregate findings into a cross-model synthesis report
    highlighting where models converge (high confidence), diverge (needs investigation),
    and surface unique insights.

    Each model tree produces its own full HTML + PDF report with infographics, and the
    ensemble aggregation produces a separate cross-model synthesis report. All trees
    share the same user-confirmed facets for apples-to-apples comparison.

Substitute `{poolSize}` with the model pool length, `{modelLabels}` with a comma-separated list of the `label` values from `cruxMemories.meditate.modelPool` (e.g. "GPT 5.5, Opus 4.7, Gemini Pro 3.1"), `{maxDepth}` with the user's depth selection, `{mode}` with the active mode name, and `{N}` with the accurate total agent count for the selected depth and mode.

Options (single-select):

- `proceed` — Yes, this is a high-value strategic problem; proceed in the currently-selected mode (`Research` or `Quick`, depth {maxDepth}, with or without Ensemble)
- `switch_to_quick` — Proceed but switch to Quick mode (~{quickCount} agents at depth {maxDepth}, faster, no peer review). **Only offered when current mode = Research.**
- `switch_to_research` — Proceed but switch to Research mode (~{researchCount} agents at depth {maxDepth}, peer-reviewed, slower). **Only offered when current mode = Quick.**
- `switch_to_ensemble` — Proceed but enable Ensemble mode (~{N×perModelCount + 1} agents across {N} model families + cross-model aggregation). **Only offered when `ensembleMode` is false.** Read `cruxMemories.meditate.modelPool` to compute the agent count.
- `switch_to_single` — Cancel Ensemble, run on a single model instead (~{perModelCount} agents). **Only offered when `ensembleMode` is true.**
- `cancel` — Cancel — I'll use a different approach

Substitute all `{...Count}` placeholders with the accurate agent counts from the depth table for the user's selected `maxDepth`.

#### Behaviour rules

- **Always run on the first invocation** in a session, regardless of arguments. Depth Selection runs first, then Cost Acknowledgment.
- **Mode swaps**: if the user picks `switch_to_quick` or `switch_to_research`, update the active `meditateMode` for the rest of this invocation and proceed to Theme Preflight; do not re-ask Q-Cost-Acknowledgment or Q-Depth-Selection. If the user picks `switch_to_ensemble`, set `ensembleMode: true` and proceed. If the user picks `switch_to_single`, set `ensembleMode: false` and proceed.
- **Cancel**: respond with a short note acknowledging the cancellation and stop. Do not spawn anything, do not run Theme Preflight, do not create the working directory.
- **Expansion-direction continuation** (calling agent step 12 — when the user picks an expansion option after a previous meditation): run a **shortened** version of this acknowledgment (`Q-Cost-Acknowledgment-Expansion`). The mode-swap and depth options are **not** re-offered (both persist across expansions); the user can `cancel` and re-invoke `/crux-meditate` if they want to change mode or depth.

  Q-Cost-Acknowledgment-Expansion prompt:

    Expanding this meditation will spawn a new depth-{maxDepth} research tree
    (~{N} additional agents) exploring the selected direction(s). This carries
    the same per-meditation cost as the original invocation — a full recursive
    tree, adversarial review cycle, and paired HTML + PDF report.

    The previous meditation's results are preserved; this expansion produces a separate
    report. If you only need a quick follow-up, consider a regular chat prompt instead.

  Options:
  - `proceed_expansion` — Yes, spawn the expansion tree
  - `cancel` — Cancel — I'll follow up in chat instead
- **Non-interactive sessions** (e.g. CI): if `askQuestion` cannot be answered, abort with a clear error explaining the cost-acknowledgment requirement. Never default to `proceed` silently — the safeguard exists precisely because the cost is non-trivial.

### Theme Preflight — MANDATORY (calling agent runs before spawning the subagent)

Every meditation must be themed deliberately. AI-generated reports tend to converge on a recognisable homogenised aesthetic — purple-blue gradient hero, Inter-700 headlines, three-card feature grids, doughnut chart with tinted-circle legend, indigo-500 accent, lucide-style icon-in-tinted-circle, Tailwind-default look. **This is forbidden as a default.** See the **Anti-Homogenization Rules** in the Report Generation section for the full block-list.

To make sure each meditation produces a visually distinct, intentional report, the calling agent **must** run an `askQuestion` sequence **before** spawning the depth-0 subagent. This is **Pattern A (pre-collected answers)**: gather every theming choice up front, then pass them to the subagent as a structured `theming` payload. The subagent never re-asks.

#### Anti-Homogenisation Rules (forbidden as defaults)

The following AI-generated defaults are **forbidden** as the starting point for any meditation report. They may only appear in a report if the user explicitly opts into them via the Theme Preflight sequence below:

- Purple-to-blue (or blue-to-purple) gradient hero banner
- Inter-700 or Inter-800 as the headline typeface
- Three-card feature grid as the dominant section layout
- Doughnut chart paired with a tinted-circle category legend
- Tailwind `indigo-500` (or any Tailwind default brand colour) as the accent
- `lucide`-style outline icon centred inside a tinted circle
- Tailwind-default "marketing landing page" look-and-feel

If the calling agent skips Theme Preflight, the report ends up looking like every other AI-generated report — this is a regression and a documentation defect. See the **Anti-Homogenization Rules** block in the Report Generation section for the canonical screenshot reference.

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

### Facet Confirmation — MANDATORY at depth 0, opt-in deeper

After the depth-0 subagent derives the **first 3 top-level facets** from the command contents (input args + chat context + referenced files), it **must** pause and let the user confirm or modify them before the meditation tree spawns. The first facet partitioning sets the entire shape of the exploration — every branch and every depth descends from it — so the user gets one mandatory checkpoint here.

Lower-level child subfocuses (depth-2 and depth-3) are **not** confirmed by default — they are derived autonomously from each parent's actual research findings. The user can opt in to deeper confirmation via a follow-up `askQuestion` immediately after the depth-0 confirm, with three granularities:

- `none` (default) — auto-derive at depth 2 and depth 3
- `depth_2_only` — pause to confirm depth-2 child subfocuses; auto-derive at depth 3
- `all_levels` — pause to confirm at depth 2 and depth 3

The choice becomes a `confirmDeepFacets` enum value passed to the depth-0 subagent and propagated unchanged to every child agent in the tree.

#### Depth-0 confirmation flow (Pattern B)

1. The depth-0 subagent derives 3 top-level facets per its normal logic, writes them to a draft file `facets-pending-{ts}.yml` in the working directory, and returns a `needs_user_input` block to the calling agent containing the proposed facets verbatim.

2. The calling agent displays the 3 proposed facets (verbatim from the subagent's `needs_user_input` block) and runs `askQuestion` **Q-Confirm-1** (single-select).

   Prompt (include the 3 facets inline, then):

     These 3 facets define the entire shape of the meditation — every branch and every
     depth descends from them. Good facets are complementary (covering different angles
     of the topic), independently explorable (each can go deep without needing the others),
     and concretely scoped (a specific question or angle, not a vague theme).

     If the facets look well-partitioned and you're happy with the exploration directions,
     confirm and proceed. If one feels too broad, overlapping with another, or missing a
     critical angle, modify it. If the overall partitioning feels wrong, regenerate for
     a fresh set (up to 3 attempts).

   Options:
   - `confirm_all` — proceed with all 3 facets unchanged
   - `modify_one` — change one facet (follow-up text input)
   - `modify_multiple` — change multiple facets (follow-up text input)
   - `regenerate` — discard these 3 and ask the subagent to derive a different set
   - `cancel` — abort the meditation entirely

3. If `regenerate` → calling agent resumes the subagent with `regenerate_facets: true` plus the previous `facets-pending-{ts}.yml` path; the subagent reads the rejected set, derives a different one, and re-escalates. Loop, **capped at 3 regeneration attempts**.

4. If `modify_one` or `modify_multiple` → calling agent collects the replacement text(s) via a free-text follow-up, then resumes the subagent with `facet_overrides: [{ index: N, new_subfocus: "...", new_slug: "..." (optional) }, ...]`. The subagent applies the overrides, re-derives slugs/citations for any modified facet, and proceeds to **Q-Confirm-2** below.

5. If `confirm_all` → calling agent proceeds directly to Q-Confirm-2.

6. **Q-Confirm-2** (single-select, asked once after depth-0 confirmation):

   Prompt:

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

   Options:
   - `none` (default — preselected) — auto-derive at depth 2 and depth 3
   - `depth_2_only` — pause for confirmation at depth 2; auto-derive at depth 3
   - `all_levels` — pause for confirmation at depth 2 and depth 3

7. Calling agent resumes the subagent with the confirmed facets plus the `confirmDeepFacets` enum value. Subagent appends the confirmed facets to `facet-registry.yml` (Research mode), promotes the draft to the final `facets.md`, deletes `facets-pending-{ts}.yml`, and proceeds to step 5 of the workflow (spawn explorers).

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

All branch / peer-review / report / review-iteration files written into the meditation working directory follow these patterns. This block mirrors the canonical reference in `.cursor/agents/crux-cursor-memory-manager.md` character-for-character (table, polling globs, and "Never hard-code these names" rule). Placeholder definitions (`{topic-slug}`, `{slug}`, `{ts}`, `{N}`, `{D}`, `{S}`) live exactly once in the agent file's **Coordination Conventions** subsection and are referenced unchanged here.

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

**Polling — prefix-glob, never equality.** Because the `{slug}` + `{ts}` suffix is not predictable until the writing agent commits the file, every polling agent must use **prefix-glob matching**:

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

Use `ls -1t <workingDir>/<glob> 2>/dev/null | head -n 1` to resolve the **latest** matching artefact when multiple regenerations have occurred (relevant for reports and review iterations).

**Never hard-code these names.** All references in this document, in the agent definition, and in the Branch & Leaf Index match these files via the prefix glob `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf`. Never hard-code `report.html` / `report.pdf`. This rule (mirrored verbatim in the **Report filenames** subsection of `### Report Generation — MANDATORY` below, and in the agent file's **Coordination Conventions** subsection) is the only place those deprecated literals may appear.

### What Happens

The depth-0 subagent runs a **mode-specific** workflow. Before the subagent tree spawns at all, the calling agent runs the four mandatory pre-spawn gates documented above — **Depth Selection**, **Cost & Scope Acknowledgment**, **Theme Preflight**, and (mid-flow, between subagent step 4 and step 5) **Facet Confirmation**. **Steps 1–8** are then performed by the subagent tree (file-based coordination, file outputs in the working directory); **steps 9–12** are performed by you (the calling agent) after the subagent returns.

The recursive exploration protocol that each depth-1/2 child agent runs is defined once in the agent file (`.cursor/agents/crux-cursor-memory-manager.md`) — see **Phases A–G** for Research mode and the **5-step protocol** for Quick mode. Depth-3 children terminate without further recursion in both modes.

#### Research mode (default)

**Steps 1–8: Subagent block (Research mode)**

1. **Feature Guard**: The manager reads `.crux/crux-memories.json` and verifies `flags.enableMemories` is `"true"`. If not, abort and inform the calling agent.
2. **Create Working Directory**: `meditations/{yyyymmdd}-{topic-slug}/` (using the flag-stripped `$ARGUMENTS` for the slug). This is the shared coordination space for all agents in the tree.
3. **Initialize coordination files** (Research mode only): seed an empty `facet-registry.yml` and an empty `citations-index.yml` in the working directory. Do NOT create `.facet-registry.lock/` yet — the lock is acquired on demand per the **Facet registry protocol** (see agent file).
4. **Derive top-level facets (cited) and confirm with the user (Pattern B)**: From the input (or chat context if no args), identify three distinct, non-overlapping exploration facets. Every facet description must be backed by at least one citation (memory, file, or chat reference). Write a **draft** to `facets-pending-{ts}.yml` (do NOT promote to `facets.md` yet), then escalate via the **Facet Confirmation** Pattern-B flow above (Q-Confirm-1 + Q-Confirm-2). Resume with the user's decision (`confirm_all` / `modify_one` / `modify_multiple` / `regenerate` / `cancel`) and the `confirmDeepFacets` enum value. Only after confirmation: append the confirmed 3 facets to `facet-registry.yml`, promote the draft to the final `facets.md` (three confirmed facets, their citations, the parent-context summary, and an explicit statement of how the three partition the topic), and delete `facets-pending-{ts}.yml`. Hold onto the `confirmDeepFacets` value — it is propagated to every child spawn in step 5.
5. **Spawn Explorers** (only after the depth-0 facet confirmation in step 4 has been resolved): Launch 3 background `crux-cursor-memory-manager` subagents in Meditate mode (one per **confirmed** facet) in parallel. Each receives `meditateMode: "research"`, `meditateDepth: 1`, `maxDepth` (the user's depth selection from Q-Depth-Selection — 1, 2, or 3), `branchNumber` (1|2|3), `branchSlug`, `subfocus` (the **confirmed** facet description = this branch's top-level subfocus), `parentSubfocus` (null at depth 1 — this is the top), `workingDir`, `parentContext`, `siblingFacets` (the other two branches' descriptions, so each branch avoids drifting into a sibling's territory), `theming` (passed through unchanged from the calling agent's Theme Preflight payload), and `confirmDeepFacets` (the enum value from Q-Confirm-2 — propagated unchanged to every deeper child).
6. **Poll for Branch Outputs** via prefix-glob: `branch-1-depth-1-sub-0-*.md`, `branch-2-depth-1-sub-0-*.md`, `branch-3-depth-1-sub-0-*.md`. Resolve the latest match per branch with `ls -1t <workingDir>/<glob> 2>/dev/null | head -n 1`. Use short intervals (10–30s); never read JSONL transcripts. All three branch files must exist before proceeding. (If any glob has been pending for more than 5 minutes AND `.facet-registry.lock/` exists, log a warning and `rmdir` the stale lock per the **Facet registry protocol** in the agent file.) **When `confirmDeepFacets ≠ none`, this same poll loop also globs for `pending-facets-*.yml`** and Pattern-B-escalates each (or batched together) to the calling agent per the **Deep confirmation flow** in the Facet Confirmation section above.
7. **Branch Peer Review** (Research mode only): spawn 3 `crux-cursor-memory-manager` peer-review agents in parallel. Each is assigned a different `peerReviewForBranch` (1, 2, or 3) and reads the other two branches' final depth-1 files plus its own branch's file, then writes `branch-{N}-peer-review-{branchSlug}-{ts}.md` per the **Peer review file** spec in the agent file. Poll for all three peer-review files via prefix-glob `branch-{N}-peer-review-*.md` before proceeding.
8. **Consolidate → index → adversarial review → re-index → report → return** — the comprehensive post-branch phase. Sub-steps 1–3 recap the work performed in steps 6 and 7; sub-steps 4–9 are step 8's new work and constitute the mandatory pre-report quality gate. Reports are **never** built over a failing adversarial review.

   1. *(Recap of step 6)* Wait for `branch-{1,2,3}-depth-1-sub-0-*.md` via prefix-glob; resolve the latest match per branch with `ls -1t <workingDir>/<glob> 2>/dev/null | head -n 1`. The deep-confirmation `pending-facets-*.yml` hook also runs here (see step 6 above).
   2. *(Recap of step 7, Research mode only)* Spawn 3 `crux-cursor-memory-manager` peer-review agents in parallel — one per branch.
   3. *(Recap of step 7, Research mode only)* Wait for `branch-{1,2,3}-peer-review-*.md` via prefix-glob (one per branch).
   4. **Consolidate**: read all 3 depth-1 branch files **plus** all 3 peer-review files **plus** `citations-index.yml`. Synthesize into `consolidation.md` following the **Subject-Matter Focus** rule (use facet titles and subfocus descriptions as section headings — never "Branch 1/2/3" or process terminology). Structure the consolidation as:
      - Key discoveries organized by facet theme (using the confirmed facet titles as section headings)
      - Cross-cutting connections and emergent themes (referencing topics by name, not by branch number)
      - Contradictions identified during quality review (presenting the substance, not "surfaced by peer review")
      - Gaps and open questions (framed as subject-matter gaps, not process gaps)
      - New evidence and supplementary findings from quality review
      - Potential directions for further exploration
      - A unified `## Citations` section that includes every distinct citation referenced anywhere in the meditation, with `[child: ...]` references translated to `[research: {subfocus-slug}]` format per the Subject-Matter Focus rule
   5. **Update `facets.md` with the Branch & Leaf Index**: per the **Branch & Leaf Index** section below, glob the working directory for actual filenames and append the index to `facets.md`. After this sub-step, `facets.md` is the single navigational entry point for every artefact the meditation produced.
   6. **Adversarial review and fix cycle**: per the **Adversarial Review and Fix Cycle** section below, spawn a fresh `crux-cursor-memory-manager` subagent in **Adversarial Review** function. Loop up to **3 iterations** until the verdict is `PASS` or `PASS_WITH_ADVISORIES`. If the reviewer escalates ambiguous `MUST_FIX` findings via `needs_user_input` (Pattern B), the calling agent runs `askQuestion`, then resumes the reviewer with the user's resolutions and continues iterating. If the cycle terminates with `ESCALATE` (cap exceeded or unresolved `MUST_FIX` remaining), **skip sub-steps 7 and 8 entirely** and surface the unresolved findings to the calling agent in sub-step 10 instead of report paths.
   7. **Re-run sub-step 5**: the adversarial reviewer may have rewritten branch / consolidation / peer-review files; re-glob the working directory and refresh the Branch & Leaf Index in `facets.md` so every link still resolves and missing-slot enumeration is accurate.
   8. **Generate the mandatory report artifacts** (HTML + PDF) per the **Report Generation — MANDATORY** section below — the canonical contract that documents filename pairing, theming, Anti-Homogenization Rules, light/dark mode, responsive nav, high-contrast PDF print theme, clickable PDF Table of Contents, headless-Chrome render command with `?print=1`, chromium-binary fallback chain, CDN allowlist, and final verification. Only run when the verdict from sub-step 6 was `PASS` or `PASS_WITH_ADVISORIES`; never run on `ESCALATE` — on `ESCALATE` skip this entire sub-step and surface unresolved findings in sub-step 10 instead of report paths.
   9. **Write process retrospective** (`retrospective-{ts}.md`): per the **Process Retrospective** section below, write a retrospective analysing the meditation process itself — what went well, what could be improved, and structural observations about the research tree's performance. This is the one output that **should** reference branches, depths, agent counts, timing, and other process details (the Subject-Matter Focus rule does not apply here). Always written, including on `ESCALATE` — process analysis is especially valuable when the review cycle failed.
   10. **Return paths** to the calling agent: working directory path, `facets.md` path, `consolidation.md` path, `retrospective-{ts}.md` path, the latest `report-{topic-slug}-{ts}.html` / `.pdf` pair (when reports were generated), and every `review-pre-report-*-iter-*.md` written by the review cycle (sorted ascending by iteration number). On `ESCALATE`, return the working directory, `facets.md`, `consolidation.md`, `retrospective-{ts}.md`, every review iteration, and a structured summary of unresolved `MUST_FIX` findings — explicitly **no** report paths.

#### Quick mode (`--quick`)

**Steps 1–8: Subagent block (Quick mode)** — same shape as Research, with these substitutions. **All four pre-spawn gates run identically in Quick mode** (Depth Selection, Cost & Scope Acknowledgment, Theme Preflight, and the Facet Confirmation Pattern-B flow including Q-Confirm-1 and Q-Confirm-2):

1. **Feature Guard** — identical.
2. **Create Working Directory** — identical.
3. **Skip entirely** in Quick mode — no `facet-registry.yml`, no `citations-index.yml`, no lock directory. Only `facets.md` is used for sibling-aware uniqueness.
4. **Derive top-level facets and confirm with the user (Pattern B)** — derive the three facets from the input as in Research (citations on each facet description are NOT required at this stage; the per-branch `## Citations` requirement still applies in step 5's child outputs), then **run the identical Facet Confirmation Pattern-B flow** (write `facets-pending-{ts}.yml`, escalate via `needs_user_input`, resume with the confirmed facets and the `confirmDeepFacets` enum value, promote draft to `facets.md`, delete the pending file). The Quick-mode subagent does NOT touch `facet-registry.yml` (it does not exist in Quick mode), but the user-confirmation flow itself is identical.
5. **Spawn Explorers** — identical to Research **except** each child receives `meditateMode: "quick"`. The `theming` and `confirmDeepFacets` payloads are threaded through unchanged just like in Research mode.
6. **Poll for Branch Outputs** — identical (same prefix-glob, same resolve rule). The same `pending-facets-*.yml` glob also runs here when `confirmDeepFacets ≠ none`.
7. **Skip entirely** in Quick mode — no peer review pass.
8. **Consolidate → index → adversarial review → re-index → report → return** — same shape as Research, with these substitutions:

   1. *(Recap of step 6)* Wait for `branch-{1,2,3}-depth-1-sub-0-*.md` via prefix-glob; resolve the latest match per branch. The `pending-facets-*.yml` deep-confirmation hook runs here whenever `confirmDeepFacets ≠ none`.
   2. **N/A in Quick mode** — no peer review pass.
   3. **N/A in Quick mode** — no peer review files to wait for.
   4. **Consolidate** — read only the 3 depth-1 branch files (no peer-review files to glob, no `citations-index.yml` to merge). Write `consolidation.md` following the **Subject-Matter Focus** rule (use facet titles as section headings, translate `[child: ...]` citations to `[research: {subfocus-slug}]` format, never reference branches/depths/agents). If any branch surfaced citation gaps (parents in Quick mode warn rather than respawn), include a "Citation gaps" callout listing every uncited finding.
   5. **Update `facets.md` with the Branch & Leaf Index** — identical to Research **except** omit per-branch "Peer review" lines and omit the Research-only `facet-registry.yml` / `citations-index.yml` entries under "Top-level artifacts". Everything else (per-branch sections, depth-2/3 leaves, top-level `consolidation.md` + report pair + review iterations + confirmed-facets entries, missing-slots enumeration, index metadata) is identical.
   6. **Adversarial review and fix cycle** — same reviewer agent, same iteration cap (3), same severity classification, same `ESCALATE` semantics, with two relaxations: (a) missing-citation findings are downgraded `MUST_FIX → SHOULD_FIX` (consistent with Quick mode's warn-only citation rule; unresolvable markers that *do* exist remain `MUST_FIX`); (b) the "peer review thoroughness" review dimension is N/A. Reports are still gated on `PASS` / `PASS_WITH_ADVISORIES`; `ESCALATE` still aborts sub-steps 7 and 8.
   7. **Re-run sub-step 5** — identical to Research.
   8. **Generate the mandatory report artifacts** — identical to Research per the **Report Generation — MANDATORY** section below. The same filename pairing, theming, anti-homogenisation rules, Universal Contrast requirements, light/dark mode, responsive nav, high-contrast PDF print theme, clickable PDF Table of Contents, and headless-Chrome render apply unchanged in Quick mode. Only run when the verdict from sub-step 6 was `PASS` or `PASS_WITH_ADVISORIES`; never run on `ESCALATE`.
   9. **Write process retrospective** — identical to Research per the **Process Retrospective** section below. Always written, including on `ESCALATE`.
   10. **Return paths** — identical to Research (working directory, `facets.md`, `consolidation.md`, `retrospective-{ts}.md`, report HTML+PDF pair when generated, every review iteration; on `ESCALATE` return everything except report paths plus a structured summary of unresolved `MUST_FIX` findings).

#### Ensemble mode (`--ensemble`)

**Steps 1–8 for Ensemble** are replaced by the **Ensemble Protocol** below. The calling agent owns the entire ensemble orchestration — it runs the pre-spawn gates once, spawns N independent meditation trees (one per model), waits for all to complete, then spawns the aggregation agent. Each model's depth-0 subagent runs the standard Research (or Quick, if combined with `--quick`) workflow in its own subdirectory, unaware that it is part of an ensemble.

**Ensemble Protocol — Calling-agent block**:

1. **Read model pool**: Load `cruxMemories.meditate.modelPool` from `.crux/crux-memories.json`. Let `N` = array length (default 3). If the pool is empty or missing, abort with a clear error: "Ensemble mode requires `cruxMemories.meditate.modelPool` in `.crux/crux-memories.json` — configure at least 2 model entries."

2. **Depth Selection**: Run `Q-Depth-Selection` (see above). Store the result as `maxDepth`. This is shared across all model trees.

3. **Cost & Scope Acknowledgment**: Run the ensemble-specific variant of `Q-Cost-Acknowledgment` (see above) with the total agent count `~{N × perModelCount + 1}` computed using the selected `maxDepth`, and the model labels from the pool.

4. **Theme Preflight**: Run once (identical to single-model mode). The resolved `theming` payload is shared across all model trees.

5. **Create ensemble working directory**: `meditations/{yyyymmdd}-{topic-slug}-ensemble/`. Write a shared `facets.md` stub here (promoted after facet confirmation).

6. **Derive and confirm facets (once, shared)**: Spawn a **single** `crux-cursor-memory-manager` subagent in Meditate mode using the **caller's own model** (not from the pool). This subagent runs only steps 1–4 of the standard workflow (feature guard, create working dir, initialize coordination files, derive + confirm facets via Pattern B). The `workingDir` for this temporary subagent is the ensemble root directory. After facet confirmation completes (Q-Confirm-1 + Q-Confirm-2), extract the confirmed facets and `confirmDeepFacets` value from the subagent's response. The per-model subdirectories are created in the next step.

7. **Spawn N model-specific meditation trees in parallel**: For each entry `{slug, label}` in `modelPool`:
   - Create subdirectory `{ensembleWorkingDir}/model-{label-slug}/` (where `label-slug` is the kebab-case version of the label, e.g. `model-gpt-5.5`, `model-opus-4.7`, `model-gemini-pro-3.1`).
   - Spawn a `crux-cursor-memory-manager` subagent in Meditate mode with **`model: slug`** on the Task tool invocation. Pass:
     - `meditateMode`: the active mode (`"research"` or `"quick"`)
     - `maxDepth`: the user's depth selection from Q-Depth-Selection (shared across all model trees)
     - `ensembleModel`: the model slug (so the subagent can propagate it to all children)
     - `ensembleModelLabel`: the human-readable label
     - `preConfirmedFacets`: the confirmed facets from step 6 (the subagent skips facet derivation and confirmation — uses these directly)
     - `confirmDeepFacets`: the Q-Confirm-2 value from step 6
     - `workingDir`: the model-specific subdirectory path
     - `theming`: the shared Theme Preflight payload
     - All other standard parameters (`parentContext`, stripped `$ARGUMENTS`, etc.)
   - All N subagents run in background simultaneously.

8. **Poll for N model tree completions**: Wait for each model-specific subagent to complete. Each writes its own `consolidation.md`, `facets.md` (with Branch & Leaf Index), `retrospective-{ts}.md`, and `report-{topic-slug}-{ts}.html` / `.pdf` pair in its model-specific subdirectory. Use the same prefix-glob verification as single-model step 9, but applied per subdirectory.

   **Deep-confirmation hook (when `confirmDeepFacets ≠ none`)**: Each model tree may produce `pending-facets-*.yml` files in its own subdirectory. The calling agent polls **all N subdirectories** for pending files and batches them into `askQuestion` prompts, noting which model produced each pending request so the user can make model-aware decisions. Write the corresponding `confirmed-facets-*.yml` to the correct model-specific subdirectory.

9. **Spawn cross-model aggregation agent**: Once all N trees have completed successfully, spawn a `crux-cursor-memory-manager` subagent in **Ensemble Aggregation** function (a new sub-mode of Meditate). If `cruxMemories.meditate.ensembleAggregatorModel` is set, pass it as `model:` on the Task tool; otherwise use the caller's own model. Pass:
   - `ensembleWorkingDir`: the ensemble root directory path
   - `modelSubdirs`: ordered list of `{label, subdirPath}` for each model
   - `confirmedFacets`: the shared facets
   - `theming`: the shared Theme Preflight payload
   - `meditateMode`: the active mode
   - `topicSlug`: the topic slug for report filenames

   The aggregation agent reads all N consolidations and branch files, produces `cross-model-synthesis.md` in the ensemble root, and generates the ensemble-level `ensemble-report-{topic-slug}-{ts}.html` / `.pdf` pair. See the **Ensemble Aggregation Report** section below for the full report contract.

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

   Options (multi-select):

   - Discovered tangent directions (derived from the exploration) — one option per discovered direction, each acting as an expansion trigger
   - `save_spec` — "Save meditation as draft spec" (write insights as a draft spec outline to the configured specs directory)
   - `end_meditation` — "End meditation" (complete the session)

   Do **not** offer "Save as interactive HTML report" or "Save as PDF report" — both artefacts are already produced as part of every meditation per the **Report Generation — MANDATORY** section above and were already surfaced in step 10.

12. **Handle the user's selection**:

    - **Expansion direction(s) selected** — **first run the shortened Cost & Scope re-acknowledgment** (`Q-Cost-Acknowledgment-Expansion`) per the rules in the **Cost & Scope Acknowledgment** section above. If the user cancels, stop without spawning anything. If they proceed, augment context with the new directions and user input, then repeat from step 2 (spawning a new subagent — which will produce its own mandatory Theme Preflight, depth-0 facet-confirmation Pattern-B escalation, adversarial review cycle, and paired `report-{topic-slug}-{ts}.html` + `report-{topic-slug}-{ts}.pdf` per the **Report Generation — MANDATORY** section). The new meditation **always** re-runs the depth-0 facet confirmation; the previous `confirmDeepFacets` value is reused by default but you may offer a one-line "keep deep-confirm setting?" follow-up. The mode-swap options from the initial `Q-Cost-Acknowledgment` are not re-offered (mode persists across expansions); the user must `cancel` and re-invoke `/crux-meditate` to change mode.
    - **`save_spec` selected** — write a draft spec outline file to the configured specs directory using the consolidation summary, the Branch & Leaf Index, and the confirmed top-level facets as the spec's input. Report the absolute path back to the user.
    - **`end_meditation` selected** — complete the session. Before the final response, remind the user that they can request further adjustments to content, theming, visual design, contrast, or report variants in a new agent session pointed at the meditation folder (`workingDir`).

    Note: the legacy `save_html` / `save_pdf` selections have been removed in subtask 05 because both artefacts are now produced automatically by every meditation.

### Branch & Leaf Index (appended to `facets.md`)

After consolidation completes, the depth-0 manager **must update `facets.md`** by appending a Branch & Leaf Index section that links to every file the meditation produced. This makes `facets.md` the single navigational entry point — open it once, jump from there to any branch, sub-focus, peer review, or top-level artifact.

**Construction rule**: glob the working directory for actual filenames (`branch-*-depth-*-sub-*-*.md`, `branch-*-peer-review-*.md`, `review-pre-report-*-iter-*.md`, `confirmed-facets-*.yml`, the latest `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf` pair) rather than reconstructing names from memory. Use **relative paths** (no `./` prefix needed) so links resolve when `facets.md` is opened from any tool that respects relative markdown links.

**Required structure** (appended below the existing `facets.md` frontmatter and content):

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

> When constructing the index, resolve `{topic-slug}` from the working-directory name and resolve `{ts}` placeholders by globbing for actual on-disk files: the **latest** matching `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf` pair, **every** `review-pre-report-*-iter-*.md` (sorted by iteration number ascending), and **every** `confirmed-facets-*.yml` (sorted by path-id then `{ts}`). List all of them as their actual on-disk filenames; never write literal `{topic-slug}-{ts}` placeholder text into `facets.md`. Pending facet files (`facets-pending-*.yml` and `pending-facets-*.yml`) are coordination artifacts — they are **not** linked from the index; only the corresponding confirmed counterparts are linked.

**Conventions**:

- Display label of each link is the file's `subfocus_slug` from frontmatter, prefixed with the local sub-index.
- Group depth-3 leaves under their depth-2 parent. Sibling indices 1–3 belong to D2-sub-1, 4–6 to D2-sub-2, 7–9 to D2-sub-3.
- If a slot didn't produce a file, omit the link AND list the slot under "Missing slots" so the gap is explicit.
- The "Top-level artifacts" subsection always lists `consolidation.md`, `retrospective-{ts}.md`, plus the latest report HTML/PDF pair (when generated), every review iteration discovered, and every confirmed-facets pair discovered. Registry / citations-index lines appear only in Research mode. The retrospective is always present (it is written even on `ESCALATE`).
- Quick mode produces the same index minus per-branch "Peer review" lines and the two Research-only registry / index lines.
- When the adversarial review verdict was `ESCALATE` the report HTML / PDF lines are omitted (no report was generated), but every `review-pre-report-*-iter-*.md` is still linked so the user can inspect why the cycle failed.

### Adversarial Review and Fix Cycle — MANDATORY

Before any report is generated, the depth-0 manager **must** run an adversarial review-and-fix cycle over every output file the meditation produced. This is a non-negotiable quality gate and runs in both Research and Quick mode.

#### Reviewer agent

Spawn a fresh `crux-cursor-memory-manager` subagent in **Adversarial Review** function (a sub-mode of Meditate). It runs in its own clean context — no inherited assumptions from the depth-0 manager or any branch agent. Pass it the following inputs in the spawn prompt:

- `meditateMode`: `"research"` or `"quick"` (the mode of the meditation under review)
- `reviewerIteration`: `1`, `2`, or `3` (1-indexed, capped at 3)
- `workingDir`: absolute path to the meditation working directory
- `theming`: the resolved Theme Preflight payload (so the reviewer can flag homogenisation drift)
- `priorReviewPath`: path to the previous iteration's review document, or `null` on the first iteration

The reviewer reads — but is the **only** agent permitted to **rewrite** during the cycle — the following files:

- Editable: `facets.md`, `consolidation.md`, every `branch-*-depth-*-sub-*-*.md`, every `branch-*-peer-review-*.md`
- Read-only: `facet-registry.yml`, `citations-index.yml` (Research mode only)
- Never touched by the reviewer: `report-*.html`, `report-*.pdf`, `.facet-registry.lock/`, `facets-pending-*.yml`, `pending-facets-*.yml`, `confirmed-facets-*.yml`

#### Review dimensions

The reviewer audits every editable file across all 11 dimensions on every iteration. Findings are classified per dimension and severity (see below).

1. **Citation integrity** — every claim in the body has at least one inline citation marker (`[memory: ...]`, `[file: ...]`, `[web: ...]`, `[chat: ...]`, `[child: ...]`); every marker resolves to an entry in the file's `## Citations` section; no unreferenced citation entries; `citations-index.yml` (Research mode) matches the union of per-file citations.
2. **Cross-file consistency** — no internal contradictions within a file; cross-file contradictions are surfaced in the file's `## Contradictions` section rather than hidden; `incorporated_children` in each parent's frontmatter matches the depth-1/2 children actually merged.
3. **Substance and sparseness** — no empty sections, no filler-only sections, no headings with one-line "(none discovered)" placeholders unless that genuinely reflects the research.
4. **Slop detection** — generic AI filler removed. Block-listed phrases include but are not limited to: "It's important to note that…", "In today's fast-paced world…", "Let's dive in", "stands as a testament to…", em-dash throat-clearing (e.g. " — let's explore…"), the "not just X but Y" tic, "delve into", "navigating the complexities of…".
5. **Calibration** — confidence in prose matches the strength of the evidence cited. Unqualified absolute claims ("always", "never", "the only way") must either be downgraded or supported by multi-source citations.
6. **Index integrity** — every link in `facets.md`'s Branch & Leaf Index resolves to an existing file; the "Missing slots" enumeration accurately reflects unproduced slots; the index metadata (timestamp, mode, count) matches reality.
7. **Frontmatter validity** — required YAML fields present on every branch / peer-review file; `subfocus_slug` and `timestamp_utc` match the on-disk filename; `incorporated_children` references resolve.
8. **Anti-homogenization drift in prose** — flag prose patterns that drift toward the homogenised AI default (purple-blue gradient metaphors, "synergy"-style buzzwords, marketing-deck cadence) regardless of which theming preset was chosen.
9. **Peer review thoroughness** (Research mode only) — every peer-review file makes concrete, cited cross-references to the branches under review; the `## Reinforcements`, `## Contradictions`, `## Gaps`, `## New Evidence` sections are substantively populated rather than placeholder lists. **N/A in Quick mode.**
10. **Ready-for-report** — downstream report generation will not have to invent content: every quantitative claim cited in `consolidation.md` resolves to a sourced data point in at least one branch file; every cross-branch theme is traceable to specific findings.
11. **Subject-matter focus** — `consolidation.md` must not contain process-oriented language per the **Subject-Matter Focus** rule: no "Branch 1/2/3" labels (use facet titles), no depth/leaf/agent references, no `[child: branch-N-depth-D-sub-S]` citations (must be `[research: {subfocus-slug}]`), no process-framing in the executive summary. Flag violations as `MUST_FIX` and rewrite the offending passages.

#### Severity classification

- **MUST_FIX** — blocks report generation. The reviewer applies the fix in the same iteration by rewriting the offending file, then continues sweeping the remaining files. If the fix is unambiguous (typo, missing citation marker that has an obvious target, a `## Citations` entry that needs to be added because the marker exists in body), the reviewer rewrites without asking. If the fix is ambiguous (e.g. multiple plausible citation targets for the same marker), the reviewer logs the finding with `fix_applied: false`, `reason: "ambiguous_fix"` and escalates via `needs_user_input` (Pattern B — see below).
- **SHOULD_FIX** — degrades quality but doesn't block report generation. Applied automatically when the fix is unambiguous; otherwise logged as `fix_applied: false`, `reason: "ambiguous_fix"` and surfaced in the review document for downstream attention.
- **ADVISORY** — observation only. Never auto-applied; never blocks; always logged.

Quick mode applies two relaxations: Citation integrity findings of "missing inline marker" downgrade `MUST_FIX → SHOULD_FIX`; the Peer review thoroughness dimension is skipped entirely.

#### Iteration loop (cap 3)

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

Cap is **3 iterations**. The depth-0 manager never spawns a 4th reviewer.

#### Reviewer escalation — Pattern B with mandatory decision-guidance

The reviewer **never calls `askQuestion` directly** (subagents are forbidden from doing so by `AGENTS.md`). When an ambiguous `MUST_FIX` finding cannot be auto-applied, the reviewer returns a `needs_user_input` block to the depth-0 manager, which surfaces it to the calling agent. **Every escalated `needs_user_input` entry MUST include `context` text that explains the trade-off the user is choosing between** — never present bare options. The calling agent uses that `context` when constructing the `askQuestion` prompt so the user understands the consequences of each choice.

Minimum escalation schema:

    ## needs_user_input

    ### question_id: <reviewer-iter-N-finding-M>
    - **prompt**: <the question, citing the offending file and line>
    - **options**: [<option-a>, <option-b>, ...]
    - **default**: <suggested option, or none>
    - **context**: <REQUIRED — explains what each option means for the meditation,
       which fix the reviewer would apply for each, and which downstream artefacts
       are affected. Without this, the calling agent cannot relay decision-guidance
       to the user.>

#### Review document format

Filename: `review-pre-report-{yyyymmddHHMMSS}-iter-{N}.md` (one per iteration, written by the reviewer).

    ---
    mode: "research" | "quick"
    iteration: 1
    reviewed_at: "2026-05-16T12:34:56Z"
    reviewer_agent: "adversarial-review-iter-1"
    files_reviewed:
      - facets.md
      - consolidation.md
      - branch-1-depth-1-sub-0-{slug}-{ts}.md
      # ... every editable file in the working directory
    prior_review: "review-pre-report-{prev-ts}-iter-{N-1}.md"   # null on first iteration
    ---

    ## Verdict
    PASS | PASS_WITH_ADVISORIES | ESCALATE

    ## Summary
    {X MUST_FIX, Y SHOULD_FIX, Z ADVISORY findings; A applied, B escalated, C deferred}

    ## MUST_FIX findings
    1. **File**: branch-1-depth-2-sub-1-{slug}-{ts}.md
       **Location**: line 47, claim "...always faster"
       **Dimension**: Calibration
       **Issue**: Unqualified "always faster" with only one citation; evidence is anecdotal
       **Fix applied**: yes
       **Fix**: Replaced with "faster in {cited-conditions}"
       **Diff**:
       ```diff
       - X is always faster [memory: caching-patterns]
       + X is faster under high-read low-write workloads [memory: caching-patterns]
       ```
    2. ...

    ## SHOULD_FIX findings
    {same structure as MUST_FIX}

    ## ADVISORY findings
    {same structure; fix_applied is always false}

    ## Iteration log
    - Iteration 1 — found 7 MUST_FIX, applied 5, escalated 2 (citation-ambiguity)
    - Iteration 2 — user resolved 2 escalations; reviewer found 1 new MUST_FIX (cascade), applied 1
    - Iteration 3 — clean sweep, verdict PASS

    ## Carry-forward to next iteration
    {any SHOULD_FIX or ADVISORY items the reviewer wants surfaced after the cycle ends}

#### Quick mode treatment

Quick mode runs the **same review cycle with the same iteration cap and severity classification**, with two relaxations:

- Citation integrity — "missing inline marker" findings are flagged as `SHOULD_FIX` rather than `MUST_FIX` (consistent with Quick mode's warn-only citation rule). Unresolvable markers that *do* exist in the body but cannot be traced to a citation entry remain `MUST_FIX`.
- Peer review thoroughness — N/A (no peer reviews exist in Quick mode).

All other dimensions, the iteration cap, the `ESCALATE` semantics, the Pattern-B escalation contract (including the mandatory `context` decision-guidance), and the review document format are enforced identically in both modes.

### Subject-Matter Focus — MANDATORY (all user-facing outputs)

The consolidation (`consolidation.md`) and the HTML/PDF reports are **subject-matter documents**, not process logs. They must read as authoritative analyses of the meditation topic — a reader should never need to know that the research was conducted by a tree of agents organized into branches and depths.

**Forbidden in consolidation and reports** (these are internal process concepts):

- References to "Branch 1", "Branch 2", "Branch 3" as organizational labels. Use the **facet title or subfocus description** instead (e.g. "Data Capture and Storage", not "Branch 1").
- References to "depth-1", "depth-2", "depth-3", "leaf agents", "leaf docs", "sub-agents", or agent counts (e.g. "39 branch files across 3 depths" or "27 depth-3 leaf agents").
- The `[child: branch-N-depth-D-sub-S]` citation format in its raw form. When citing findings from the research tree, translate the citation to a **subject-matter description** — e.g. `[research: token-bucket-budget-aware-provider-rotation]` using the subfocus slug, not `[child: branch-1-depth-3-sub-1]`. The `## Citations` section must map these to the underlying files for traceability, but the inline markers themselves must be meaningful to a reader who has never seen the meditation's internal structure.
- References to "peer-review agents" or "peer reviewers" as actors. Present peer-review findings as "cross-cutting analysis", "independent verification", or "quality review" — the findings matter, not the process that produced them.
- The phrase "this meditation explored X across three branches" or similar process-framing in executive summaries. Instead: "This analysis covers X" or "This research examines X".

**Required instead**:

- **Section headings** use the facet titles and subfocus descriptions (e.g. "## Data Capture and CRUX-Compressed Storage", "### Free API Source Composition and Failover").
- **Organizational framing** follows the subject matter's natural structure (theme → sub-theme → detail), not the tree's physical structure (branch → depth-2 → depth-3).
- **Cross-references** between sections reference topics by name ("as discussed in the Risk Engine section" or "consistent with the findings on WebSocket lifecycle management"), not by branch number.
- **Executive summaries** lead with the substantive conclusion, not a description of the research process.
- **The `## Citations` section** maps the subject-matter citation markers (e.g. `[research: token-bucket-budget-aware-provider-rotation]`) to source files so traceability is preserved, but the reader never needs to parse `branch-N-depth-D-sub-S` notation.

**Scope**: This rule applies to `consolidation.md` and the HTML/PDF reports only. Internal coordination files (`facets.md` Branch & Leaf Index, branch output files, peer-review files, `facet-registry.yml`, `citations-index.yml`) and the process retrospective (`retrospective-{ts}.md`) retain their process-oriented naming for coordination purposes.

### Process Retrospective — MANDATORY

After the report is generated (or after an `ESCALATE` verdict skips it), the depth-0 manager **must** write a process retrospective to `retrospective-{ts}.md` in the working directory. This is the designated place for process analysis — the **Subject-Matter Focus** rule does **not** apply here. The retrospective is always written, including on `ESCALATE` (process analysis is especially valuable when things went wrong).

**Filename**: `retrospective-{yyyymmddHHMMSS}.md` — use the same `{ts}` as the report pair when one was generated, or capture a fresh UTC timestamp if no report was produced (on `ESCALATE`).

#### Required sections

```markdown
---
mode: "research" | "quick"
topic_slug: "{topic-slug}"
generated_utc: "2026-05-17T12:34:56Z"
verdict: "PASS" | "PASS_WITH_ADVISORIES" | "ESCALATE"
---

## Process Retrospective — {topic title}

### Summary Statistics
- **Mode**: Research | Quick
- **Total agents spawned**: {count} (N depth-1 + N depth-2 + N depth-3 + N peer-review + N adversarial-review iterations)
- **Branch files produced**: {count} ({breakdown by depth})
- **Peer reviews**: {count} (Research mode) | N/A (Quick mode)
- **Adversarial review iterations**: {count}, final verdict: {verdict}
- **MUST_FIX findings**: {total found} → {applied} auto-fixed, {escalated} user-escalated, {unresolved} unresolved
- **SHOULD_FIX findings**: {total found} → {applied} auto-fixed
- **ADVISORY findings**: {total found}
- **Missing slots**: {list or "none"}
- **Facet regeneration attempts**: {count} (0 = confirmed on first try)
- **Deep-facet confirmations**: {count} (0 = confirmDeepFacets was "none")

### What Went Well
{Substantive observations about the process — not generic praise. Examples:}
- Which branches produced the richest findings and why
- Whether the facet partitioning created clean, non-overlapping exploration paths
- Effective cross-branch convergences discovered independently
- Citation coverage completeness
- Where peer review added genuine value (Research mode)
- How well the adversarial review caught real issues vs false positives

### What Could Be Improved
{Honest assessment of process weaknesses. Examples:}
- Branches or depth-2/3 nodes that produced thin or repetitive content
- Facet partitioning problems (overlap, gaps, one facet too broad)
- Citation gaps or weak sourcing patterns
- Adversarial review findings that should have been caught earlier
- Any ESCALATE causes and whether they were avoidable
- Coordination issues (stale locks, slow polling, missing files)
- Depth-3 leaves that added little incremental value over their depth-2 parent
- Whether Quick mode would have been sufficient (if Research was used) or vice versa

### Structural Observations
{Analysis of the research tree's shape and efficiency:}
- Branch balance — did all 3 branches produce comparable depth and quality?
- Depth utility — did depth-3 add meaningful detail beyond depth-2?
- Peer review impact — what fraction of peer-review findings changed the consolidation? (Research mode)
- Adversarial review efficiency — how many iterations were needed and could the first pass have been cleaner?
- Subject-matter focus compliance — were there process-language violations that needed fixing?

### Recommendations for Future Meditations
{Actionable suggestions for improving the next meditation on a similar topic:}
- Facet suggestions if the topic were re-explored
- Mode recommendation (Research vs Quick) for this topic's complexity level
- Areas where deeper exploration (4+ depths or more branches) would have helped
- Areas where the tree was over-provisioned
```

The depth-0 manager fills in every section with specifics from the actual meditation run. Generic or placeholder content is not acceptable — the retrospective must reflect concrete observations from this particular run.

### Report Generation — MANDATORY

Producing a detailed report HTML **and** PDF with rich infographics and visualizations is **mandatory** for every meditation, in both Research and Quick mode. Generate them automatically as part of step 8 of the workflow above — never as an opt-in. A meditation is not considered complete until both files exist in the working directory.

The depth-0 subagent owns this step end-to-end (its workflow step 12); the calling agent then runs a verification gate (calling-agent step 9 above) before presenting results. Reports are **never** built over a failing adversarial review (`ESCALATE` verdict from the review cycle aborts this section — see step 12 in the agent file).

#### Report filenames

Use the meditation's **topic slug** (the same `{topic-slug}` segment used in the working directory `{yyyymmdd}-{topic-slug}/`) plus a UTC timestamp captured at the moment of report generation:

    report-{topic-slug}-{yyyymmddHHMMSS}.html
    report-{topic-slug}-{yyyymmddHHMMSS}.pdf

- `{topic-slug}` MUST exactly match the slug component of the working-directory name (extract it as everything after the first `-` in the basename).
- `{yyyymmddHHMMSS}` is the UTC timestamp at write time (`date -u +%Y%m%d%H%M%S`).
- The HTML and PDF for a single generation share the same timestamp.
- All references in this document, in the agent definition, and in the Branch & Leaf Index match these files via the prefix glob `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf`. Never hard-code `report.html` / `report.pdf`.

#### Inputs

1. **Read all meditation files**: Load `consolidation.md`, `facets.md`, `facet-registry.yml` (Research mode), `citations-index.yml` (Research mode), all `branch-*-depth-*-sub-*-*.md` files, and all `branch-*-peer-review-*.md` files (Research mode) from the working directory. The trailing wildcards capture the slug-and-timestamp suffix on every file across depths 1–3 and the peer-review pass. Extract every data point, table, finding, comparison, citation, and insight — the report must reflect the **full** meditation, not just the consolidation summary.

#### HTML report requirements (`report-{topic-slug}-{ts}.html`)

Generate a self-contained single-file webpage in the working directory. **All** of the following are required:

##### Structural elements

- **Responsive top navigation bar** — see the **Responsive Navigation** subsection below
- **Table of Contents** immediately under the hero, with anchor links to every major section. Every section heading carries a stable `id` so the in-page TOC and the PDF bookmarks both resolve. This same TOC drives the PDF index (see PDF requirements below).
- **Hero / executive summary** — title, one-paragraph verdict, and a row of headline stat cards (key numbers extracted from the meditation). The visual identity here is set by the chosen `theming` payload — never use the homogenised default look (see Anti-Homogenization Rules). Per the **Subject-Matter Focus** rule, lead with the substantive conclusion — never describe the research process (no agent counts, tree depth, or branch structure).
- **Per-facet sections** — each confirmed facet becomes one or more report sections using its **facet title** as the heading (e.g. "Data Capture and CRUX-Compressed Storage", not "Branch 1"), with subheadings derived from subfocus descriptions for deeper findings. Organize content by the subject matter's natural structure, not by the tree's physical branch/depth layout.
- **Quality review section** (Research mode) — cross-cutting reinforcements, contradictions, gaps identified during independent review; one card per review file. Present findings as substantive analysis, not as "peer reviewer said X" — the content matters, not the process actor.
- **Cross-references** between sections where independent research streams converged on the same finding, referencing topics by name (not by branch number)
- **Citations section** at the bottom — mandatory in both modes. In Research mode, source it from `citations-index.yml` (the canonical aggregated index); in Quick mode, source it from inline citation markers extracted from every branch file. Either way, deduplicate and provide backlinks to every section that cited each source. If any finding in the report has no resolvable citation (possible only in Quick mode under the warn-only validation rule), include a "Citation gaps" callout in the executive summary that lists every uncited finding so the gap is visible to the user.
- **Footer** with meditation slug, timestamp, mode (`research` / `quick`), depth/branch counts, total citation count, and the resolved theming label (e.g. `theme: editorial / warm_palette / serif_headings_sans_body` or `theme: matched-repo (signals: …)`)

##### Report Comprehensiveness — No Information Loss (mandatory)

The report is the **final deliverable** of the meditation. Every important finding, data point, comparison, citation, and insight discovered across the entire research tree (all 39 branch files, peer reviews, and consolidation) must be faithfully represented in the HTML/PDF report. The report is NOT a summary of the consolidation — it is the fully-rendered, richly-visualized presentation of **all substantive research output**.

**Hard rules**:

- **Every quantitative data point** discovered in any branch file must appear in the report — either in a chart, table, infographic, or inline. No data should exist only in the branch files without representation in the report.
- **Every comparison or trade-off** surfaced during research must be visualized or tabulated, not merely mentioned in prose.
- **Every cited source** that contributed a material finding must appear in the report's Citations section with a backlink to where that finding is presented.
- **Every contradiction or tension** identified (including those from peer review) must be explicitly surfaced — either as a dedicated comparison section, a dual-column pro/con layout, or a decision matrix.
- **Input coverage verification**: Before declaring the report complete, enumerate the key findings from each branch file's `## Discoveries` and `## Summary` sections and verify each has a corresponding presentation element (chart, table, infographic, prose section, or calculator) in the report. Log any gap and fill it.

**Anti-sparseness escalation**: If the generated report contains fewer distinct data points or findings than the branch files collectively surfaced, the report fails its own completeness check. Re-read the branch files and add the missing content before the PDF render.

##### Option Comparison Research Reporting (mandatory when applicable)

When the meditation's goal involves **option comparison research** across products, tools, services, approaches, or strategies (e.g. technology evaluation, vendor selection, architectural decision, framework comparison), the report MUST include all of the following specialized elements in addition to the standard structural requirements. The depth-0 manager detects comparison intent from the confirmed facets and the topic-slug — if two or more facets correspond to distinct options being evaluated, or if the topic explicitly names a comparison/evaluation/selection activity, this section activates.

**Required elements for option-comparison reports**:

1. **Feature comparison matrix** — a comprehensive table (or set of tables) with:
   - Options as columns (or rows if many options)
   - Evaluation criteria as rows (or columns), derived from the research findings
   - Cell-level indicators: checkmarks (✓/✗), partial-support markers (◐), ratings (1–5 or A–F), or concise text values
   - Color-coded cells where appropriate (green = strong, yellow = partial, red = weak/absent)
   - Footnotes explaining nuanced cells that cannot be reduced to a single symbol
   - Sortable/filterable in the HTML version; default-sorted by overall score in the PDF

2. **Adoption and market presence** — at least one dedicated section or visualization showing:
   - Market share or adoption metrics (user counts, GitHub stars, download stats, enterprise penetration, or whatever quantitative adoption signals the research surfaced)
   - Trend direction (growing, stable, declining) with supporting evidence
   - Community health indicators (contributor counts, issue response times, release cadence) when available
   - Timeline of major releases or market events if the research surfaced temporal data

3. **Gartner Magic Quadrant-style visualization** — a 2×2 quadrant chart (implemented as D3.js or hand-rolled SVG) plotting each option on two key axes:
   - **X-axis**: Completeness of vision / breadth of capability / feature coverage (or the most natural "breadth" axis for the domain)
   - **Y-axis**: Ability to execute / maturity / production-readiness (or the most natural "depth/quality" axis for the domain)
   - Each option rendered as a labeled circle (radius optionally proportional to adoption or a third dimension)
   - Quadrant labels (e.g. "Leaders", "Challengers", "Visionaries", "Niche Players" — or domain-appropriate equivalents)
   - Axis labels, grid lines, and a legend explaining the placement methodology
   - In the PDF static fallback: permanent labels on each circle, axis values visible, quadrant regions clearly shaded
   - **Note**: This is a Gartner-*style* analytical placement, not a reproduction of any copyrighted Gartner report. The axes, methodology, and placement are derived solely from the meditation's own research findings.

4. **Key differentiators section** — a dedicated subsection (not buried in prose) that:
   - Lists 3–7 decisive differentiators that most strongly separate the options
   - For each differentiator: names which option(s) excel and which lag, with a one-sentence evidence summary and citation
   - Presented as a visual element (scorecards, bar chart per differentiator, or annotated comparison strips) — not just a bullet list
   - Highlights the "decision-driving" differentiators (the ones most likely to tip a choice) with visual emphasis

5. **Recommendation or decision framework** (when the research supports one) — either:
   - A clear recommendation with supporting rationale and caveats, OR
   - A decision tree / flowchart showing "if your priority is X → choose Y; if Z → choose W"
   - Rendered as an infographic (SVG decision tree, flowchart, or scorecard with weighted criteria)

**Activation heuristics** (depth-0 manager applies these after facet confirmation):

- Topic contains: "compare", "comparison", "versus", "vs", "evaluate", "evaluation", "alternatives", "options", "which", "best", "selection", "choose", "decision"
- Two or more facets correspond to distinct named products, tools, services, or approaches being assessed
- The user's original input explicitly frames the meditation as a choice between options

When option-comparison research activates, the standard content minimums (≥4 charts, ≥3 infographics, ≥1 calculator) still apply independently — the comparison-specific elements above are **additional** to those minimums, not replacements. The quadrant visualization counts toward the ≥4 chart minimum; the feature matrix and differentiators section count toward the ≥3 infographic minimum; a TCO/ROI calculator (if the comparison involves cost) counts toward the ≥1 calculator minimum.

##### Visualizations (Chart.js + D3.js, loaded from CDN)

Pick **at least 4 distinct chart types in total**, choosing those that fit the data the meditation actually surfaced AND the kind of facet being illustrated. The minimum can be met by any combination of **Chart.js** (standard chart types, fastest to author) and **D3.js** (advanced or facet-specific interactive visualizations). Do not fabricate data — if the meditation lacks the data a particular chart type needs, skip it and pick another.

**Hard rule**: Every D3 chart **must** gracefully degrade to a meaningful static equivalent in the PDF render. See the **D3 print degradation (mandatory)** subsection below — a D3 chart that cannot degrade is forbidden; pick a different visualization or implement the degradation paired view.

###### Chart.js types (standard, well-suited to numeric data the meditation surfaced)

- **Bar / stacked bar** — counts, comparisons across branches or options
- **Radar** — multi-dimensional scoring (criteria × option matrices)
- **Doughnut / pie** — categorical breakdowns (citation source mix, finding-type distribution)
- **Line / area** — temporal trends, projections, sensitivity sweeps
- **Scatter / bubble** — multi-axis trade-off plots (cost vs benefit, risk vs reward)
- **Polar area** — relative magnitude across categories
- **Mixed (bar + line)** — actual vs projected, baseline vs scenario

###### D3.js types (interactive, facet-specific — pick the one that fits each section)

| Facet kind | Suitable D3 chart types |
|------------|-------------------------|
| **Hierarchy / structural decomposition** (e.g. branch → depth-2 → depth-3 tree) | Tree (`d3-hierarchy` cluster/tree), dendrogram, sunburst, treemap, partition, icicle |
| **Networks / relationships** (e.g. cross-branch citation overlap, memory-to-finding linkage) | Force-directed graph, chord diagram, hierarchical edge bundling, arc diagram |
| **Flows / process volumes** (e.g. how findings cascade from depth-1 → depth-3) | Sankey, alluvial/parallel sets |
| **Time-series with interaction** (e.g. timeline with brushable zoom) | Brushable timeline, zoomable area chart, focus+context |
| **Geographic** (e.g. data tied to locations) | Choropleth, hex bin, projection-aware map |
| **Multi-dimensional comparison** (e.g. options × many criteria) | Parallel coordinates, brushed scatter matrix, radar with brush |
| **Calendar / temporal density** (e.g. activity over months) | Calendar heatmap |
| **Custom facet-specific** | Hand-coded D3 (e.g. a custom force-layout for a specific concept map) — always include the print degradation pair |

When using D3, load it from the official CDN: `<script src="https://d3js.org/d3.v7.min.js"></script>` (v7 is current at time of writing; pin to the latest stable major version available on the CDN). All data is still embedded inline as JavaScript constants — no runtime fetches.

###### D3 print degradation (mandatory)

In the PDF render, interactive features (hover tooltips, brushing, zooming, click-to-drill, animated transitions) do not work. Every D3 chart must therefore render a **meaningful static state** in print mode. The HTML must implement one of the following degradation strategies for every D3 chart, chosen per chart type:

| D3 pattern | Print degradation strategy |
|------------|---------------------------|
| **Hover tooltips** | In print mode, replace tooltips with permanent inline labels (data labels next to nodes, edges, or bars) OR a paired data table beneath the chart listing every value the tooltip would have shown. |
| **Brushable / zoomable** | In print mode, render the **most informative zoom level** (typically full-extent overview) with explicit axis labels and tick marks; if multiple zoom levels are essential, render a small-multiples grid showing each zoom level as its own static panel. |
| **Click-to-drill / expand-collapse** | In print mode, render the **fully expanded** state. If full expansion is too dense to be readable on one page, render a top-level overview followed by per-section detail panels on subsequent pages. |
| **Animated transitions** (e.g. force simulation settling) | In print mode, compute the final settled state at module scope (or pre-render via a one-shot tick loop) before paint; the PDF captures the final positions, not an in-progress animation. |
| **Interactive filtering** (e.g. parallel coordinates with brushes) | In print mode, render the unfiltered full view AND a paired summary table or small-multiples grid showing the same data faceted by the dimensions the user would normally brush on. |
| **Cannot degrade meaningfully** (e.g. an interactive simulation playground) | **Forbidden** — pick a different visualization, or pair the D3 chart with a co-located static SVG / Chart.js fallback that conveys the same insight; the print mode hides the interactive D3 chart and shows only the static pair. |

The HTML implementation pattern: every D3 chart sits inside a `<div class="d3-chart" data-degradation-strategy="..."></div>` container that includes:
1. A `<div class="d3-interactive">` for the on-screen interactive render.
2. A `<div class="d3-static-fallback" hidden>` for the print-state render — populated either at the same time as the interactive view (hidden via CSS in screen mode) OR populated lazily when `data-print-mode="true"` is set on `<html>`.
3. A `@media print { .d3-interactive { display: none } .d3-static-fallback { display: block } }` rule, AND an equivalent `[data-print-mode="true"] .d3-interactive { display: none } [data-print-mode="true"] .d3-static-fallback { display: block }` rule so the headless-Chrome PDF render with `?print=1` deterministically picks up the static fallback.

**Verification before declaring the report complete**: render the HTML twice in a headless browser sanity-check — once normal, once with `?print=1` — and confirm every D3 chart shows a non-empty static fallback in the print render. If any D3 chart degrades to an empty container, fix the fallback before the PDF is generated.

##### Infographics (HTML/CSS/SVG, no external library)

Pick **at least 3 distinct infographic types** from the list below — these convey structure visually rather than encoding numbers. Build them with hand-rolled HTML + CSS + inline SVG (no extra libraries):

- **Hierarchy / tree diagrams** — render the branch → depth-2 → depth-3 subfocus tree as a visual map (CSS grid or inline SVG with connector lines)
- **Comparison matrices** — option × criterion grids with cell-level color coding, badges, or icons
- **Decision trees / flow diagrams** — when the meditation surfaces a decision pathway, render it as a node-and-arrow SVG diagram
- **Scorecards** — per-option panels with weighted criterion bars and an overall score
- **Process / pipeline diagrams** — sequential stages with directional arrows
- **Quadrant / 2×2 matrices** — placement of options on two axes (e.g. effort × impact)
- **Heatmaps** — CSS grid where cell color encodes value
- **Risk meters / gauges** — segmented horizontal bars or radial dials with color-coded zones
- **Timeline ribbons** — horizontal chronological strips with milestone markers
- **Concept maps** — central-topic-with-spokes layouts using inline SVG
- **Venn diagrams** — overlap visualizations for branches that share findings (CSS or SVG)

##### Interactive elements

- **Interactive calculators** — at least one JavaScript-driven calculator if the meditation surfaces any quantifiable trade-off (input fields, recompute on change, formatted result panel). Infer what calculation would be useful from the meditation content.

  **Mandatory PDF graceful degradation**: every calculator must include a paired `.calculator-static-fallback` container that renders **3–5 pre-computed what-if scenarios** as a table or grid in the PDF. Interactive recompute does not work in print, so the fallback must let the reader see the answers for the most informative input combinations without typing anything. Pick the scenarios deliberately:
  - **Typical / baseline** — the most common or default input set (label it as such)
  - **Optimistic** — favourable assumptions (best-case inputs)
  - **Pessimistic** — unfavourable assumptions (worst-case inputs)
  - **Threshold / breakeven** — inputs that produce a notable boundary outcome (zero, sign-change, capacity limit, etc.) when one exists
  - **Recommended** — the meditation's preferred recommendation (only when the meditation surfaces one)

  Each scenario row lists every input value plus the computed output(s) with units, formatted exactly as the on-screen calculator would format them. A short caption above the table explains what each scenario represents and which finding from the meditation motivated picking it (with a citation). Forbidden: an empty static fallback, a single scenario, or a fallback that just lists input fields without computed results.

  **Implementation pattern** (mirrors the D3 print-degradation pattern):

      <div class="calculator" data-degradation-strategy="what-if-table">
        <div class="calculator-interactive">
          <!-- input fields, button, result panel -->
        </div>
        <div class="calculator-static-fallback" hidden>
          <!-- caption explaining scenarios + table of 3-5 pre-computed rows -->
        </div>
      </div>

  Plus the same `@media print` and `[data-print-mode="true"]` rules used for D3 charts:

      @media print {
        .calculator-interactive { display: none }
        .calculator-static-fallback { display: block }
      }
      [data-print-mode="true"] .calculator-interactive { display: none }
      [data-print-mode="true"] .calculator-static-fallback { display: block }

  **Verification before declaring the report complete** (folds into the existing adversarial-review "ready-for-report" dimension): render the HTML once with `?print=1` and confirm every calculator's static fallback is non-empty AND contains at least 3 fully-populated scenario rows. If any calculator degrades to an empty container, an inputs-only stub, or fewer than 3 scenarios, fix it before the PDF is generated.

- **Filterable tables** — comprehensive data tables with at least one filter or sort affordance for any tabular finding. In print mode, hide the filter / sort UI controls and render the **unfiltered, default-sorted** table; the data itself is preserved verbatim.

- **Tooltips** on inline citation markers showing the cited source on hover. In print mode, tooltips degrade to inline footnote markers (`[7]`) that resolve in the Citations section.

##### Anti-Homogenization Rules

AI-generated reports converge on a recognisable homogenised aesthetic. **All of the following defaults are forbidden** unless the user's `theming` payload explicitly invoked them by name. The goal is for every meditation to feel deliberately and visibly different from a "default AI report".

Forbidden defaults (see `assets/image-8bca59a2-5c28-4614-9fe8-98a395c28f57.png` for the canonical example to avoid):

- **Purple-blue gradient hero** (`linear-gradient(135deg, indigo, blue/violet)` and friends).
- **Inter as the headline font weight 700**. Default to a font dictated by the `theming.preset.typography` value or the matched repo signal.
- **Three-card feature grids** as the dominant layout. Vary layout per section (asymmetric grids, single hero panel, two-column with sidebar, full-bleed tables, masonry).
- **Doughnut chart with circular tinted-color legend chips** (the screenshot's signature). Either move the legend, change its shape, or pick a different chart for the same data.
- **Tailwind `indigo-500` (or its variants `#6366f1`, `#818cf8`) as the accent**. Pick a palette from the `theming` payload.
- **Lucide-style icon-in-tinted-circle motif** for stat cards and bullets. Use unboxed iconography, no icons at all, or hand-drawn SVG marks per the chosen direction.
- **Centred body paragraphs** and **gradient "Most popular" pricing pills** as filler. Do not add SaaS-marketing motifs.
- **Five-star testimonial rows** and **DiceBear avatar fallbacks**. There are no users to quote.
- **Smooth modern dark blue UI**, full stop, when no theming choice asked for it.

How to apply this:

1. Before writing any CSS, look at the `theming` payload and pick concrete values (font stack, primary/secondary/accent hex, layout grammar, divider style, link decoration, heading scale).
2. If the chosen direction would naturally produce one of the forbidden patterns, *deliberately substitute* — e.g. an editorial direction may want a serif drop-cap hero instead of a gradient banner; a brutalist direction wants flat blocks and no rounded corners; a terminal_dossier direction wants ASCII-art dividers, not gradient strips.
3. Include a one-line `theme:` annotation in the footer naming the resolved direction, palette, and typography.

##### Theming application (driven by the `theming` payload)

The depth-0 subagent receives a `theming` payload from the calling agent. Use it to drive every visual decision:

- `theming.source = match_repo` → load the listed `css_variables_file` / `tailwind_config`, extract the actual font stack, primary/secondary/accent colors, border-radius scale, spacing rhythm; render the report inline-styled to match (do **not** import the repo's CSS — extract the values and inline them).
- `theming.source = preset` → apply the `style_direction` × `color_scheme` × `typography` combination.
- `theming.source = custom` → follow the user's free-text description literally.
- `theming.source = surprise_me` → pick a `style_direction` deterministically seeded by the topic-slug, biased *away* from any direction recently used.

##### Universal Contrast (mandatory)

Every rendered element in the HTML and PDF reports must maintain high contrast against its actual background in **both** light and dark screen modes and in the print/PDF mode. This applies to text, lines, borders, chart strokes, chart labels, SVG connectors, quadrant axes, grid lines, table borders, heatmap labels, badges, callouts, code blocks, footnote markers, links, nav states, and any decorative marks that carry meaning.

**Minimum contrast requirements**:

- Body text, table text, captions, labels, legends, footnotes, citation markers, nav links, badge text, and chart labels: WCAG AA normal-text contrast (≥4.5:1) against the exact background behind the element.
- Large headings and large stat numerals: WCAG AA large-text contrast (≥3:1), with ≥4.5:1 preferred unless the design would be harmed.
- Non-text graphical elements that convey information (chart lines, SVG connectors, axes, grid lines, quadrant boundaries, heatmap cells, risk-meter segments, badges, table borders, focus rings): WCAG non-text contrast (≥3:1) against adjacent colours, with ≥4.5:1 preferred for thin lines (<2px) or small marks.
- Interactive focus outlines and active nav states: ≥3:1 against both the component background and the surrounding page background.

**Hard rules**:

- Never place text directly on a gradient, texture, image, translucent overlay, or saturated colour block unless the report also adds a solid or sufficiently opaque backing panel behind the text and verifies contrast against that panel.
- Do not rely on pastel text, low-opacity strokes, faint grid lines, transparent fills, glow-only emphasis, or colour-only distinctions. Pair colour with labels, patterns, symbols, or explicit text.
- Chart.js and D3 palettes must be generated separately for dark, light, and print modes; a colour that passes in dark mode is not assumed to pass in light or print mode.
- Every SVG/HTML infographic must define explicit stroke and text colours for each colour mode. Inherited theme colours are allowed only when they are known to pass contrast for the element's actual background.
- Heatmaps and quadrant backgrounds must keep labels readable in every cell/region; if necessary, switch label colour per cell (`light-on-dark` / `dark-on-light`) or add label pills.
- Thin lines (axes, connectors, borders) must be thickened, darkened, or backed by sufficient spacing if they would otherwise fall below contrast on coloured backgrounds.
- Disabled or secondary UI may be visually subdued, but still must remain readable and must not encode substantive findings with low-contrast styling.

**Verification before declaring the report complete**:

1. Inspect representative elements from every visual system used in the report: hero, nav, TOC, tables, stat cards, callouts, Chart.js charts, D3 charts and static fallbacks, SVG infographics, calculators and calculator fallbacks, citations, footer, and any option-comparison matrices/quadrants.
2. Verify contrast in all three render states: dark screen mode, light screen mode, and `?print=1` PDF mode.
3. If any text or meaningful line/border/mark is low contrast against its background, treat it as a report-generation defect and fix it before generating or returning the PDF.
4. Prefer deterministic CSS variables such as `--text-strong`, `--text-muted-readable`, `--line-strong`, `--line-subtle-readable`, `--chart-label`, and `--chart-axis` so contrast decisions are centralized rather than hand-tuned per component.

##### Light + Dark mode (mandatory)

- **Both modes are required.** Implement the report so every element renders legibly in both.
- **Default = dark mode** on first load, regardless of system preference.
- **Toggle in the nav** — a clearly visible button (sun/moon icon or text label like "☀ Light / ☾ Dark"). Switches modes immediately, no flicker.
- **Persistence** — store the user's choice in `localStorage` under `meditation-color-mode`; on subsequent loads, honour the stored value before any rendering occurs (set on `<html>` before paint to avoid FOUC).
- **System preference signal** — read `window.matchMedia('(prefers-color-scheme: dark)')` only as a fallback when no localStorage value exists.
- **Contrast** — both modes must satisfy the **Universal Contrast** subsection above for every rendered element, not just body text and headings.
- **Charts** — Chart.js color values must adapt to the active mode. Wire chart options to read CSS custom properties for stroke/fill so a single mode-toggle redraws all charts.

##### Responsive Navigation (mandatory)

- **Wide viewport (`≥768px`)** — horizontal nav across the top of the page. Group the section anchors into logical clusters using facet-derived names (e.g. *Overview*, *Data Capture*, *Decision Engine*, *Simulation*, *Cross-Cutting Analysis*, *Citations*) with a small visible separator (1px divider or extra spacing). Group labels are recommended for ≥6 anchors.
- **Narrow viewport (`<768px`)** — hide the horizontal nav and replace with a burger button (three horizontal lines, top-right). Tapping the burger opens a slide-in drawer or full-screen overlay containing the same grouped link list, vertically stacked.
- **Implementation** — pure CSS + minimal JS. No external nav library. Use `aria-expanded` / `aria-controls` for accessibility; trap focus inside the drawer while open.
- **Active section** — highlight the currently visible section's nav link as the user scrolls, in both viewport modes.

#### PDF report requirements (`report-{topic-slug}-{ts}.pdf`)

The PDF must be **legible and engaging** as a standalone printable artifact. It is not a screenshot of the dark-mode webpage — it is a deliberately-rendered print version with high-contrast text and elements, and a clickable table of contents.

##### Filename pairing

Capture the UTC timestamp **once** at the start of report generation and reuse it for both the HTML and PDF filenames so they pair up:

    TS=$(date -u +%Y%m%d%H%M%S)
    SLUG="{topic-slug}"
    HTML="{workingDir}/report-${SLUG}-${TS}.html"
    PDF="{workingDir}/report-${SLUG}-${TS}.pdf"

##### Print theme — high contrast (mandatory)

The HTML's `@media print` block (and an equivalent `body[data-print-mode="true"]` block toggled by a query parameter for the PDF render — see below) must apply a **high-contrast print theme** distinct from the on-screen dark mode and must satisfy the **Universal Contrast** requirements for every text, line, border, axis, SVG mark, and chart label:

- **Background**: pure white (`#fff`) or near-white (`#fafafa`).
- **Body text**: near-black (`#0a0a0a` / `#111`), minimum 11pt.
- **Headings**: `#000` with the chosen theme's display typeface preserved.
- **Links**: dark accent (`#0033aa` or theme-equivalent), underlined.
- **Tables**: black 1px borders, alternating row backgrounds at `#f5f5f5`.
- **All meaningful lines and marks**: axes, grid lines, quadrant boundaries, SVG connectors, table borders, legend swatches, footnote markers, and focus/fallback indicators must remain visibly distinct against the print background and adjacent fills; low-opacity decorative lines are forbidden when they carry information.
- **Charts**:
  - **Chart.js** — re-rendered with high-contrast palettes (opaque colours from a print-safe palette, no near-white fills, no light-on-light), thicker stroke widths (`borderWidth: 2`), labelled data points where space allows.
  - **D3.js** — every D3 chart's interactive container is hidden and its `.d3-static-fallback` print-state container is shown via the `@media print` and `[data-print-mode="true"]` rules described in the **D3 print degradation** section above. The static fallback uses high-contrast strokes (≥1.5px), solid fills, permanent inline labels (no hover-only tooltips), and computed-final-state positions (no in-progress animations). If any D3 chart's static fallback would be empty or unreadable in print, the chart fails the report-completion verification step and must be fixed before the PDF is generated.
- **Infographics**: foreground elements use solid black or theme-dark; backgrounds white. Drop shadows, glows, and partial-opacity tints stripped or strengthened.
- **Interactive calculators**: every calculator's `.calculator-interactive` container is hidden and its `.calculator-static-fallback` print-state container is shown via the `@media print` and `[data-print-mode="true"]` rules described in the **Interactive elements** section above. The static fallback renders 3–5 pre-computed what-if scenarios as a table with high-contrast borders and labelled scenario types (typical / optimistic / pessimistic / threshold / recommended). If any calculator's static fallback is empty, has fewer than 3 scenarios, or only shows input fields without computed results, the chart fails the report-completion verification step and must be fixed before the PDF is generated.
- **Hide**: the sticky nav, the colour-mode toggle, the burger button, any hover-only tooltip widget, and any filter / sort UI control on tables (the underlying data stays visible). Citation tooltips become inline footnote markers (`[7]` etc.) that resolve in the Citations section.
- **Page breaks**: every top-level section starts on a new page (`page-break-before: always`); no orphaned headings or split tables (`page-break-inside: avoid` on tables, charts, and infographic blocks).

By default `pdf_color_mode` in the `theming` payload is `light_high_contrast`. Honour any explicit user override (e.g. dark PDF for an editorial print) but warn that dark PDF is harder to read and consumes more ink.

##### Table of Contents (mandatory)

The PDF must open with a **clickable Table of Contents** as the first content page (after the title page if any). Build it once in the HTML; the same DOM serves both the on-page TOC and the PDF index:

- Place inside `<nav id="toc" aria-label="Table of contents">` immediately under the hero, before the per-facet content sections.
- Every section heading (`<h2>` / `<h3>`) carries a stable, kebab-case `id` (e.g. `id="data-capture-crux-storage"`, `id="quality-review"`, `id="citations"`).
- Headless Chrome preserves anchor links in the printed PDF natively, so the TOC entries become clickable bookmarks in the PDF reader.
- Two levels deep (top-level sections + branch subheadings); deeper depth-3 leaves are accessible via the in-section navigation.
- Right-aligned page numbers next to each entry are encouraged but optional.
- Add `<style>@media print { #toc { page-break-after: always; } }</style>` so the TOC sits on its own page in the PDF.

##### Render command

Render the PDF from the generated HTML using headless Chrome. Pass `?print=1` so the HTML can switch to its print theme (and TOC layout) deterministically:

    google-chrome --headless --disable-gpu --no-sandbox \
      --print-to-pdf="${PDF}" \
      --print-to-pdf-no-header \
      --no-pdf-header-footer \
      "file://${HTML}?print=1"

The HTML must read `URLSearchParams` on load and apply `data-print-mode="true"` to `<html>` when `print=1` is set, so the print theme and TOC styles are guaranteed to apply during the headless render even outside `@media print`.

Try `chromium` and `chromium-browser` as fallback binaries if `google-chrome` is not installed. If no headless Chromium is available, the meditation **fails** with a clear error: report the missing dependency, list the installation hint for the user's platform (e.g. `brew install --cask google-chrome` on macOS, `apt install chromium` on Debian/Ubuntu), and leave the HTML file in place so the user can manually print to PDF.

##### Final verification

Before returning control to the user, verify exactly one matching pair exists for this meditation and both files are non-empty. The newest matching pair is authoritative if multiple regenerations have occurred:

    HTML_LATEST=$(ls -1t "{workingDir}"/report-"{topic-slug}"-*.html 2>/dev/null | head -n 1)
    PDF_LATEST=$(ls -1t  "{workingDir}"/report-"{topic-slug}"-*.pdf  2>/dev/null | head -n 1)
    [ -s "${HTML_LATEST}" ] && [ -s "${PDF_LATEST}" ]

If either check fails, regenerate the missing artifact before presenting results.

##### Other styling rules

- All data embedded inline as JavaScript constants — **no external data fetches**, no `fetch()` calls.
- Allowed external resources (CDN script tags only — no runtime data fetches via these libraries):
  - **Chart.js** — `https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js`
  - **D3.js** — `https://d3js.org/d3.v7.min.js` (see the **Visualizations** subsection above for facet-specific usage and the **D3 print degradation (mandatory)** subsection for the `.d3-static-fallback` PDF-degradation contract)
  - **D3 plugins** as needed (`d3-sankey`, `d3-cloud`) loaded from the same official CDNs
  - **Custom fonts** from Google Fonts or `https://rsms.me/` *only if the chosen theme requires a non-system font*; never load a font just because Inter is "the default"
- No other external scripts, stylesheets, or assets — and never use the libraries above to fetch runtime data.

If the meditation is small (e.g. a quick `--quick` run on a narrow topic) and genuinely lacks the breadth for 4 chart types or 3 infographics, you must still produce **all** mandatory structural elements; substitute additional comparison matrices, scorecards, or hierarchy diagrams to compensate so the report is never sparse.

### Ensemble Aggregation Report — MANDATORY (when `ensembleMode` is true)

The ensemble aggregation report is the deliverable that justifies running N× the agents. It must surface where models converge (highest-confidence findings), where they diverge (areas needing investigation), and what unique insights each model brought that the others missed.

#### Ensemble working directory structure

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

Subdirectory names use the kebab-case version of each model's `label` from `cruxMemories.meditate.modelPool`, prefixed with `model-` (e.g. `model-gpt-5.5`, `model-opus-4.7`, `model-gemini-pro-3.1`).

#### Ensemble filename conventions

| Artefact | Filename pattern | Location |
|----------|------------------|----------|
| Shared facets | `facets.md` | Ensemble root |
| Per-model tree | `model-{label-slug}/` | Ensemble root |
| Cross-model synthesis | `cross-model-synthesis.md` | Ensemble root |
| Ensemble report HTML | `ensemble-report-{topic-slug}-{ts}.html` | Ensemble root |
| Ensemble report PDF | `ensemble-report-{topic-slug}-{ts}.pdf` | Ensemble root |

Per-model subdirectories follow the standard single-model **Coordination Conventions** for all internal files.

#### Cross-model synthesis (`cross-model-synthesis.md`)

The aggregation agent reads all N `consolidation.md` files plus (optionally for detail) branch files from each model's subdirectory. It produces `cross-model-synthesis.md` in the ensemble root with these mandatory sections:

```markdown
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

## Executive Summary
{One-paragraph verdict synthesizing the strongest findings across all models.
 Lead with the substantive conclusion, not a description of the ensemble process.}

## Convergence — High-Confidence Findings
{Findings that all N models independently arrived at. Each finding includes:
 - The shared conclusion
 - How each model framed or supported it (with [model: label] attribution)
 - Combined citation strength (union of citations from all models)
 These are the most trustworthy outputs of the meditation.}

## Divergence — Areas of Disagreement
{Findings where models reached different conclusions about the same facet.
 Each divergence includes:
 - The question or claim at issue
 - Each model's position with its reasoning and evidence ([model: label])
 - The aggregator's assessment of which position is better-supported and why
 - A confidence indicator (strong disagreement vs. nuanced difference)
 These are the most valuable outputs — they reveal where the topic is genuinely
 contested or where model-specific knowledge gaps exist.}

## Unique Insights — Single-Model Discoveries
{Findings surfaced by only one model that the others missed entirely.
 Each insight includes:
 - The finding and its evidence ([model: label])
 - Why the other models likely missed it (knowledge gap, different framing,
   different depth allocation)
 - The aggregator's assessment of whether the insight is credible and valuable
 These represent potential blind spots — valuable if real, risky if hallucinated.}

## Evidence Quality Comparison
{Per-facet assessment of citation strength across models:
 - Which model found the most/strongest citations for shared claims
 - Which model relied most on memory corpus vs. code analysis vs. web sources
 - Citation coverage gaps per model}

## Reasoning Style Comparison
{Meta-observation of how each model structured its analysis:
 - Depth vs. breadth trade-offs per model
 - Which model produced the most novel subfocus derivations at depth-2/3
 - Stylistic patterns (e.g. one model favours enumeration, another favours
   narrative synthesis)
 - Which model's consolidation was most/least aligned with the Subject-Matter
   Focus rule}

## Recommended Synthesis
{The aggregator's best-judgment unified analysis that:
 - Anchors on convergent findings as the foundation
 - Incorporates the best-supported position from each divergence
 - Integrates credible unique insights with appropriate hedging
 - Calls out remaining open questions where even the ensemble cannot resolve
   the disagreement}

## Per-Model Report Index
{Links to each model's individual report and consolidation for drill-down:
 - [GPT 5.5 Report (HTML)](model-gpt-5.5/report-{topic-slug}-{ts}.html)
 - [GPT 5.5 Report (PDF)](model-gpt-5.5/report-{topic-slug}-{ts}.pdf)
 - [GPT 5.5 Consolidation](model-gpt-5.5/consolidation.md)
 - ... (one group per model)}

## Citations
{Unified, deduplicated citation list across all models. Each entry includes
 [model: label] markers indicating which model(s) cited it. Backlinks to
 the sections that used each citation.}
```

#### Ensemble report (`ensemble-report-{topic-slug}-{ts}.html` / `.pdf`)

The ensemble report follows the same mandatory report contract as single-model reports (same theming, anti-homogenisation rules, Universal Contrast requirements, light/dark mode, responsive nav, PDF high-contrast print theme, clickable TOC, headless-Chrome render, CDN allowlist) with these ensemble-specific additions:

##### Ensemble-specific structural elements

- **Model comparison hero**: instead of a single stat-card row, show N model cards side-by-side, each with that model's headline finding and a convergence/divergence indicator
- **Per-facet comparison cards**: for each confirmed facet, show each model's key conclusion in parallel columns/cards with `[model: label]` attribution and a visual convergence indicator (green = all agree, amber = partial agreement, red = disagreement)
- **Agreement heatmap**: a facet × model matrix (Chart.js or D3) where cell color encodes the degree of agreement between each model pair for each facet. This is the ensemble report's signature visualization.
- **Divergence deep-dives**: each major divergence gets its own section with the competing positions presented side-by-side, evidence compared, and the aggregator's assessment
- **Per-model drill-down links**: every section includes links to the corresponding section in each model's individual HTML report

##### Ensemble-specific visualizations (in addition to the standard minimums)

- **Agreement heatmap** (required): facet × model matrix
- **Model attribution Sankey** (recommended): flow diagram showing how findings from each model fed into the convergence/divergence/unique categories
- **Citation Venn diagram** (recommended): overlap visualization showing which citations were shared vs. model-unique
- **Confidence radar**: per-facet confidence scores from each model, overlaid on a single radar chart

##### Model attribution citation format

All findings in the ensemble report carry `[model: {label}]` citation markers (e.g. `[model: GPT 5.5]`, `[model: Opus 4.7]`). These appear alongside standard citation markers (`[memory: ...]`, `[file: ...]`, etc.) and are listed in the `## Citations` section with backlinks. When a finding is convergent (all models agree), use `[models: all]` as a shorthand.

## Related

- `crux-cursor-memory-manager` agent — The specialist that orchestrates the recursive meditation
- `crux-skill-memory-index` skill — Memory index used for facet-relevant memory discovery
- `crux-skill-memory-crud` skill — Read operations for loading memory content during exploration
- `/crux-dream` — Extract and create memories from completed work
- `/crux-recall` — View and query memories
- `/crux-remember` — Create ad-hoc memories outside of spec workflows
- `/crux-forget` — Remove memories from the corpus
