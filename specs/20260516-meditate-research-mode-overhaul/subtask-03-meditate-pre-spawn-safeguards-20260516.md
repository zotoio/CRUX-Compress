# Subtask: Pre-Spawn User Safeguards (Cost & Scope Acknowledgment + Theme Preflight + Facet Confirmation)

## Metadata
- **Subtask ID**: 03
- **Feature**: Meditate Research-Mode Overhaul
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 02
- **Created**: 20260516

## Objective

Add the three mandatory `askQuestion` user gates that fire **before** the meditation tree spawns. Each gate has a distinct purpose:

1. **Cost & Scope Acknowledgment** (very first action) — surface that this is a deep research task spawning ~45 agents and offer mode-swap or cancel.
2. **Theme Preflight** — collect a deliberate, non-homogenised visual identity for the eventual report via a 5-question sequence with a `match_repo` short-circuit and an Anti-Homogenisation Rules block.
3. **Facet Confirmation** — after the depth-0 subagent derives the first 3 facets, escalate them via Pattern B for confirm/modify/regenerate, plus an opt-in `confirmDeepFacets` enum for deeper levels.

## Files Modified

- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`

## Deliverables Checklist

- [x] **Cost & Scope Acknowledgment** section in the command file with per-mode agent counts, `Q-Cost-Acknowledgment` askQuestion spec, behaviour rules (always run on first invocation, mode swap, cancel, expansion-mode shortened version, non-interactive abort)
- [x] **Theme Preflight** section in the command file with the 5-question sequence (Q1 source / Q1b match-repo confirm / Q2 style direction / Q3 colour scheme / Q4 typography / Q5 confirmation), the `theming` payload schema, and an Anti-Homogenisation Rules forbid-list referencing the canonical screenshot
- [x] **Facet Confirmation** section in the command file with depth-0 Pattern-B flow (Q-Confirm-1 + Q-Confirm-2), deep confirmation file-based escalation protocol (pending/confirmed schema, depth-0 manager poll-loop hook, child agent polling)
- [x] Subagent **step 4** (derive facets) updated to escalate via Pattern B before writing final `facets.md`
- [x] Subagent **step 5** (spawn explorers) updated to spawn only after confirmation; thread `theming` and `confirmDeepFacets` payloads
- [x] Recursive exploration **Phase C** updated with the deep-confirmation hook (write pending file, poll for confirmed, apply per-child decisions, regeneration cap)
- [x] Calling-agent step 12 (expansion handling) updated to run shortened cost re-acknowledgment first
- [x] Quick mode workflow notes updated to confirm all three gates run identically (cost ack, theme preflight, facet confirmation Pattern B)
- [x] Mode-selection block in the agent file gains: Cost & Scope Acknowledgment Pattern-A note, Theming payload Pattern-A note, Facet confirmation Pattern-B note
- [x] Three new design principles in the agent file: mandatory cost & scope acknowledgment, deliberate non-homogenised theming, mandatory user confirmation of the first 3 facets

## Definition of Done

- [x] All three pre-spawn gates fire in order on first invocation (cost ack → theme preflight → facet confirmation)
- [x] No subagent spawns until the user has explicitly proceeded through every gate
- [x] `confirmDeepFacets` propagates unchanged to every child agent
- [x] The forbidden anti-homogenisation defaults are documented explicitly
- [x] Linter passes on both files

## Implementation Notes

### Cost & Scope Acknowledgment section (command file, place between Argument Handling and Theme Preflight)

```markdown
### Cost & Scope Acknowledgment — MANDATORY (calling agent's first action)

`/crux-meditate` is **not** a quick chat replacement. Every invocation spawns a deep recursive research tree of tens of agents, generates infographic-rich HTML and PDF reports, and runs a multi-iteration adversarial review cycle. It is intentionally **more expensive** than a regular prompt or chat session and is intended for **well-considered problem statements tied to high-value strategic activities** — architecture decisions, multi-month initiatives, major investment analyses, organisational strategy, deep technical research, etc.

To make sure the user has chosen the right tool, the calling agent's **very first action** — before Theme Preflight, before spawning anything — is a single `askQuestion` that surfaces the cost-and-scope tradeoff and lets the user proceed, swap modes, or cancel.

#### Approximate agent count and runtime per mode

| Mode | Agent count (typical) | Runtime (typical) | Use when |
|------|-----------------------|-------------------|----------|
| **Research** (default) | ~45 agents (1 depth-0 manager + 3 depth-1 branches + 9 depth-2 + 27 depth-3 + 3 peer reviewers + 1–3 adversarial review iterations) | tens of minutes | High-stakes strategic problems where citation rigor, peer review, and incorporation depth justify the cost |
| **Quick** (`--quick`) | ~42 agents (same tree minus peer reviewers) | substantially faster | Broad early-stage exploration where citations are still required but peer-review and citation re-spawn enforcement are not |

These counts exclude the calling agent itself and the per-iteration adversarial review subagents (which can run 1–3 times depending on findings).

#### Q-Cost-Acknowledgment (mandatory single-select)

Prompt:

  /crux-meditate is a deep research task that will spawn approximately {N} agents,
  produce a comprehensive HTML + PDF report with infographics and clickable index,
  and run an adversarial review-and-fix cycle before any output is finalised.

  Compared with a single prompt or chat reply, this is significantly more expensive
  in time and tokens. It's designed for well-considered problem statements tied to
  high-value strategic activities (architecture decisions, strategic planning,
  investment analyses, multi-week initiatives, deep technical research).

  For lighter questions, prefer:
    - a regular chat
    - /crux-recall to query existing memories without spawning a tree
    - a single targeted prompt scoped to one file or function

  How would you like to proceed?

Options (single-select):
  - proceed                 — Yes, this is a high-value strategic problem; proceed in the
                              currently-selected mode ({Research} or {Quick})
  - switch_to_quick         — Proceed but switch to Quick mode (~42 agents, faster, no
                              peer review). Only offered when current mode = Research.
  - switch_to_research      — Proceed but switch to Research mode (~45 agents, peer-
                              reviewed, slower). Only offered when current mode = Quick.
  - cancel                  — Cancel — I'll use a different approach

Substitute `{N}` with the accurate agent count for the currently-selected mode and `{Research}`/`{Quick}` with the active mode label so the user sees the concrete number and the current mode in the prompt.

#### Behaviour rules

- **Always run on the first invocation** in a session, regardless of arguments.
- **Mode swaps**: if the user picks `switch_to_quick` or `switch_to_research`, update the active mode for the rest of this invocation and proceed to Theme Preflight; do not re-ask Q-Cost-Acknowledgment.
- **Cancel**: respond with a short note acknowledging the cancellation and stop. Do not spawn anything, do not run Theme Preflight, do not create the working directory.
- **Expansion-direction continuation** (calling agent step 12 — when the user picks an expansion option after a previous meditation): run a **shortened** version of this acknowledgment that re-states the cost and asks `proceed_expansion` / `cancel`. The mode-swap options are not re-offered (mode persists across expansions); the user can `cancel` and re-invoke `/crux-meditate` if they want to change mode.
- **Non-interactive sessions** (e.g. CI): if `askQuestion` cannot be answered, abort with a clear error explaining the cost-acknowledgment requirement. Never default to "proceed" silently — the safeguard exists precisely because the cost is non-trivial.
```

### Theme Preflight section (command file, place after Cost & Scope Acknowledgment)

```markdown
### Theme Preflight — MANDATORY (calling agent runs before spawning the subagent)

Every meditation must be themed deliberately. AI-generated reports tend to converge on a recognisable homogenised aesthetic — purple-blue gradient hero, Inter-700 headlines, three-card feature grids, doughnut chart with tinted-circle legend, indigo-500 accent, lucide-style icon-in-tinted-circle, Tailwind-default look. **This is forbidden as a default.** See the **Anti-Homogenization Rules** in the Report Generation section for the full block-list.

To make sure each meditation produces a visually distinct, intentional report, the calling agent **must** run a `askQuestion` sequence **before** spawning the depth-0 subagent. This is **Pattern A (pre-collected answers)**: gather every theming choice up front, then pass them to the subagent as a structured `theming` payload. The subagent never re-asks.

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

#### Hard rule

If the user does not engage with `askQuestion` (e.g. running non-interactively in CI), pick the `surprise_me` path for both Q1 and Q2 with a deterministic-but-non-default selection seeded by the topic-slug, then proceed without confirmation. Never silently fall back to the homogenised default look.

#### Theming payload (passed to the depth-0 subagent)

The calling agent serialises the answers into a YAML-shaped payload and includes it in the subagent's spawn prompt as `theming:`:

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

The depth-0 subagent must use this payload to drive every visual choice in the report.
```

### Facet Confirmation section (command file, place after Theme Preflight)

```markdown
### Facet Confirmation — MANDATORY at depth 0, opt-in deeper

After the depth-0 subagent derives the **first 3 top-level facets** from the command contents (input args + chat context + referenced files), it **must** pause and let the user confirm or modify them before the meditation tree spawns. The first facet partitioning sets the entire shape of the exploration — every branch and every depth descends from it — so the user gets one mandatory checkpoint here.

Lower-level child subfocuses (depth-2 and depth-3) are **not** confirmed by default — they are derived autonomously from each parent's actual research findings. The user can opt in to deeper confirmation via a follow-up `askQuestion` immediately after the depth-0 confirm, with three granularities:

- `none` (default) — auto-derive at depth 2 and depth 3
- `depth_2_only` — pause to confirm depth-2 child subfocuses; auto-derive at depth 3
- `all_levels` — pause to confirm at depth 2 and depth 3

The choice becomes a `confirmDeepFacets` enum value passed to the depth-0 subagent and propagated unchanged to every child agent in the tree.

#### Depth-0 confirmation flow (Pattern B)

1. The depth-0 subagent derives 3 top-level facets per its normal logic, writes them to a draft file `facets-pending-{ts}.yml` in the working directory, and returns a `needs_user_input` block to the calling agent containing the proposed facets verbatim.

2. The calling agent runs `askQuestion` **Q-Confirm-1** (single-select):
   - `confirm_all` — proceed with all 3 facets unchanged
   - `modify_one` — change one facet (follow-up text input)
   - `modify_multiple` — change multiple facets (follow-up text input)
   - `regenerate` — discard these 3 and ask the subagent to derive a different set
   - `cancel` — abort the meditation entirely

3. If `regenerate` → calling agent resumes the subagent with `regenerate_facets: true` plus the previous facets-pending file path; the subagent reads the rejected set, derives a different one, and re-escalates. Loop, capped at 3 regeneration attempts.

4. If `modify_one` or `modify_multiple` → calling agent collects the replacement text(s) via a free-text follow-up, then resumes the subagent with `facet_overrides: [{ index: N, new_subfocus: "...", new_slug: "..." (optional) }, ...]`. The subagent applies the overrides, re-derives slugs/citations for any modified facet, and proceeds to **Q-Confirm-2** below.

5. If `confirm_all` → calling agent proceeds directly to Q-Confirm-2.

6. **Q-Confirm-2** (single-select, asked once after depth-0 confirmation):
   - `none` (default — preselected) — auto-derive at depth 2 and depth 3
   - `depth_2_only` — pause for confirmation at depth 2; auto-derive at depth 3
   - `all_levels` — pause for confirmation at depth 2 and depth 3

7. Calling agent resumes the subagent with the confirmed facets plus the `confirmDeepFacets` enum value. Subagent appends the confirmed facets to `facet-registry.yml` (Research mode), promotes the draft to the final `facets.md`, deletes `facets-pending-*.yml`, and proceeds to step 5 of the workflow (spawn explorers).

#### Deep confirmation flow (when `confirmDeepFacets` ≠ `none`)

When deep confirmation is enabled, **file-based escalation** is used because the chain is too deep for direct return-up to be practical.

**Child agent side** (any agent at a depth where confirmation is required):

1. Derive 3 child subfocuses from actual research findings, per the existing Phase C logic.
2. **Before** acquiring the registry lock, write a pending-facets file:

    pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml

   Where `{N}/{D}/{S}/{ts}` identify the **parent agent** that derived these proposed children.

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
         - ...
       status: "pending"

3. **Poll** for the matching `confirmed-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml`. Use prefix-glob with the same `branch-{N}-depth-{D}-sub-{S}-` segment plus the `{ts}` from the pending file.

4. Once the confirmation file exists, read it. Schema mirrors the pending file but adds a `decision` per child:

       decisions:
         - sub_index: 1
           decision: "confirmed" | "modified" | "regenerate"
           new_slug: "..."
           new_subfocus: "..."
           new_rationale: "..."
         - ...

5. Apply the decisions:
   - `confirmed` → use the original child verbatim
   - `modified` → replace with the user-supplied subfocus/slug
   - `regenerate` → re-derive that single child from research findings, write a new pending file with the same path-id but a fresh `{ts}`, and loop (capped at 3 regenerations per child).

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
```

### Subagent step 4 update (agent file)

```markdown
4. **Derive top-level facets (cited) and confirm with the user (Pattern B)**:
   ...
   1. Write a draft to `facets-pending-{ts}.yml` (do NOT write the final `facets.md` yet).
   2. Escalate via Pattern B: return `needs_user_input` with the proposed 3 facets.
   3. Resume with the user's decision (regenerate / modify / confirm / cancel).
   4. Append the confirmed 3 facets to `facet-registry.yml`, promote the draft to the final `facets.md`, delete `facets-pending-{ts}.yml`.
   5. Hold onto the `confirmDeepFacets` enum value — propagated to every child spawn.
```

### Subagent step 5 update (agent file)

Add to the spawn payload:

- `theming` — passed through unchanged from the calling agent
- `confirmDeepFacets` — propagated unchanged to every deeper child
- `subfocus` is the **confirmed** facet description

### Recursive exploration Phase C update (agent file)

Add the deep-confirmation hook:

```markdown
   - **If `confirmDeepFacets` requires confirmation at this depth** (`depth_2_only` and we are at depth 1, OR `all_levels` and we are at depth 1 or 2):
     1. Write `pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml` per the Deep confirmation flow.
     2. Poll for the matching `confirmed-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml`.
     3. Apply per-child decisions (regenerations capped at 3 per child).
   - Acquire registry lock and proceed with normal Phase C completion.
```

### Subagent step 6 (poll for branch outputs) update (agent file)

When `confirmDeepFacets ≠ none`, the same poll loop ALSO globs for `pending-facets-*.yml` and Pattern-B-escalates each (or batched) to the calling agent.

### Quick mode workflow notes update (agent file)

Confirm all three pre-spawn gates run identically in Quick mode (cost ack, theme preflight, facet confirmation Pattern B). Phase C of recursive exploration in Quick mode also implements the file-based deep-confirmation escalation when enabled (the `facet-registry.yml` collision check is skipped in Quick mode, but the user-confirmation flow itself still runs).

Quick mode (depth 1 and 2) workflow now has a step 2 inserted:

```
2. If confirmDeepFacets requires confirmation at this depth:
   write pending-facets-{path-id}-{ts}.yml, poll for confirmed-facets-..., apply decisions.
```

### Calling agent step 12 update (command file)

```markdown
12. If the user selects expansion directions, **first run the shortened Cost & Scope re-acknowledgment** (`Q-Cost-Acknowledgment-Expansion`) — re-state the per-mode agent count and ask `proceed_expansion` / `cancel`. If the user cancels, stop without spawning anything. If they proceed, augment context with the new directions and user input, then repeat from step 2 (spawning a new subagent — which will produce its own mandatory Theme Preflight, depth-0 facet-confirmation Pattern-B escalation, adversarial review cycle, and pair of `report-{topic-slug}-{ts}.html` and `report-{topic-slug}-{ts}.pdf`). The new meditation **always** re-runs the depth-0 facet confirmation; the previous `confirmDeepFacets` value is reused by default but you may offer a one-line "keep deep-confirm setting?" follow-up. If "Save spec", write a draft spec file. If "End", finish.
```

### Mode selection block additions (agent file)

Add three notes alongside the existing mode-selection text:

```markdown
**Cost & Scope Acknowledgment — Pattern A (pre-collected by the calling agent, before everything else)**: Before any work begins — before Theme Preflight, before this subagent is spawned — the calling agent runs a mandatory **Cost & Scope Acknowledgment** `askQuestion`. The user must explicitly proceed (or swap mode, or cancel) before anything else fires. If the user cancelled, this subagent is never spawned. Treat the existence of your spawn invocation as proof that the user has acknowledged the cost (~45 agents in Research, ~42 in Quick) and chosen the active `meditateMode` deliberately. Do not re-prompt the user about cost — that is the calling agent's responsibility.

**Theming payload — Pattern A (pre-collected by the calling agent)**: After cost acknowledgment but before spawning this subagent, the calling agent runs a mandatory **Theme Preflight** `askQuestion` sequence and passes the resolved `theming` payload in the spawn prompt. Use this payload to drive every visual decision in the report — never default to the homogenised AI look (purple-blue gradient hero, Inter-700, three-card grid, doughnut + tinted-circle legend, Tailwind indigo-500, etc.). Propagate the payload unchanged to every child agent. If the payload is missing from the spawn prompt, abort with a clear error pointing the calling agent at the Theme Preflight section.

**Facet confirmation — Pattern B (escalated mid-flow) for depth-0; file-based escalation for deeper levels**: After deriving the **first 3 top-level facets** (step 4 below), this subagent **must** pause and escalate them to the calling agent via Pattern B (`needs_user_input` block). The calling agent runs the mandatory `askQuestion` confirm/modify/regenerate flow, then asks a follow-up `askQuestion` to set `confirmDeepFacets ∈ {none, depth_2_only, all_levels}`. Both the confirmed facets and the `confirmDeepFacets` enum value come back in the resume payload; propagate the latter unchanged to every child agent in the tree.
```

### Three new design principles (agent file)

Append to the design-principles list:

```markdown
- **Mandatory upfront cost & scope acknowledgment (both modes)**: Before any subagent is spawned, before Theme Preflight, the calling agent runs a single `askQuestion` warning the user that this is a deep research task spawning ~45 agents in Research mode (~42 in Quick) and is intentionally more expensive than a regular chat. The user must explicitly proceed, swap mode, or cancel.
- **Mandatory user confirmation of the first 3 facets (both modes)**: After deriving the top-level facets, the depth-0 manager pauses via Pattern B and lets the calling agent run the mandatory `Q-Confirm-1` and `Q-Confirm-2` flow. No branches are spawned and `facets.md` is not finalised until the user confirms. Deeper levels are auto-derived by default; `confirmDeepFacets ∈ {none, depth_2_only, all_levels}` lets the user opt in to per-level confirmation, implemented via file-based `pending-facets-*.yml` / `confirmed-facets-*.yml` escalation through the depth-0 manager's poll loop.
- **Deliberate, non-homogenised theming (both modes)**: Every report's visual identity is set by the `theming` payload collected during the calling agent's Theme Preflight `askQuestion` sequence. Never default to the homogenised AI look (purple-blue gradient hero, Inter-700, three-card grid as dominant layout, doughnut + tinted-circle legend, Tailwind indigo-500 accent, lucide icon-in-tinted-circle motif). If the `theming` payload is missing from the spawn prompt, abort with a clear error.
```

## Testing Strategy

- After applying, simulate a fresh `/crux-meditate "test problem"` invocation in your head and confirm the order is: Cost ack → Theme preflight → Subagent spawn → Subagent derives 3 facets → Pattern-B escalation → Q-Confirm-1 → Q-Confirm-2 → Subagent resumes and spawns branches.
- Confirm cancellation at any of the three gates stops the flow without spawning anything or creating any working directory.
- Confirm `--quick` flag swap option only appears when current mode is Research, and vice versa.
- Run the linter on both files.

## Execution Notes

### Agent Session Info
- Agent: crux-platform-architect
- Started: 20260516
- Completed: 20260516

### Work Log

- Added **Cost & Scope Acknowledgment** section to `.cursor/commands/crux-meditate.md` between Argument Handling and Coordination Conventions, including per-mode agent counts (Research ~45, Quick ~42), the full `Q-Cost-Acknowledgment` prompt and option set, and behaviour rules covering first invocation, mode swap, cancel, expansion-mode shortened `Q-Cost-Acknowledgment-Expansion`, and non-interactive abort.
- Added **Theme Preflight** section with the canonical Anti-Homogenisation Rules forbid-list (7 explicitly named defaults), the 5-question askQuestion sequence (Q1 source / Q1b match-repo confirm / Q2 style direction / Q3 colour scheme / Q4 typography / Q5 confirmation), the non-interactive `surprise_me` fallback rule, and the YAML `theming` payload schema.
- Added **Facet Confirmation** section with the depth-0 Pattern-B flow (Q-Confirm-1 + Q-Confirm-2 with the 3-attempt regenerate cap), the file-based deep-confirmation escalation protocol (pending/confirmed YAML schemas, depth-0 manager poll-loop hook, child-agent polling, per-child confirmed/modified/regenerate decisions with 3-cap), and the re-spawn semantics for expansion continuations.
- Updated calling-agent step 11 → step 11 (save/end) + new step 12 (expansion with shortened cost re-ack) in the command file; renamed the calling-agent block header from "Steps 9–11" to "Steps 9–12" and updated all forward references.
- Updated command-file subagent step 4 (derive facets, Pattern-B escalation) and step 5 (spawn explorers only after confirmation, thread `theming` + `confirmDeepFacets`); updated step 6 to also glob `pending-facets-*.yml` when deep confirmation is enabled.
- Updated Quick-mode workflow notes to confirm all three gates run identically (cost ack, theme preflight, facet confirmation Pattern B); updated Quick-mode steps 4, 5, 6 to mirror Research-mode behaviour for the gates and the deep-confirmation poll.
- Added the three Pattern-A / Pattern-B notes to the mode-selection block in `.cursor/agents/crux-cursor-memory-manager.md` (Cost & Scope Acknowledgment Pattern A, Theming payload Pattern A, Facet confirmation Pattern B with file-based deep escalation).
- Updated agent-file Research-mode workflow step 4 (Pattern-B escalation with full flow), step 5 (only-after-confirmation + theming + confirmDeepFacets), step 6 (deep-confirmation poll-loop hook), and the step-numbering note (calling-agent block is now steps 9–12); updated the post-subagent flow to describe the shortened cost re-ack on expansion.
- Updated Research-mode Phase C with the deep-confirmation hook (write pending file, poll confirmed, apply per-child decisions, regen cap of 3) executed BEFORE the registry lock; added the equivalent step 2 hook to the Quick-mode recursive protocol (now 6 steps), updated downstream references to Quick-mode step numbers.
- Appended three new design principles to the agent file: mandatory upfront cost & scope acknowledgment, mandatory user confirmation of the first 3 facets (with `confirmDeepFacets` propagation), and deliberate non-homogenised theming (with explicit abort-on-missing-payload rule).
- Confirmed `ReadLints` clean on both modified files.

### Blockers Encountered

None. The canonical step 12 text in the spec was extended with an explicit "Save HTML/PDF" handling clause to preserve compatibility with subtasks 01–02 (since the mandatory-reports change is owned by subtask 05, which has not yet been applied) — save HTML/PDF handling lives in step 11 and expansion-with-cost-re-ack lives in step 12.

### Files Modified
- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`
