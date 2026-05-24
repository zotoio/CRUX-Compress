---
name: crux-skill-memory-meditation-research
description: Research-mode meditation protocol: Phases A–G depth-first recursion, depth-0 manager steps 1–13 (incl. step 4b 4-mode `additional_focus_areas[]` reconciliation + `init-suggestions-{ts}.yml` write; step 8 K10c reflection writing `finalisation-enhancements.yml`; step 8b respawn-payload prep), facet registry lock, citations index, peer review file spec, comprehensiveness honouring at leaf depth. Use when the `crux-cursor-meditation-guide` agent runs the depth-0 manager or any Research-mode child agent.
---

# CRUX Skill: Memory Meditation — Research Protocol

Implements the full Research-mode meditation contract: Phases A–G recursive depth-first exploration, depth-0 manager steps 1–13 (including step 4b 4-mode `additional_focus_areas[]` reconciliation, step 8 K10c in-pass reflection, and step 8b respawn-payload prep), facet registry lock, citations index, peer review file spec, and comprehensiveness honouring at leaf depth.

## When to Use

Load this skill when:
- The `crux-cursor-meditation-guide` agent is spawned in Research mode (no `--quick` flag, `meditateMode: "research"`)
- You are executing the depth-0 manager workflow (steps 1–13)
- You are executing as a child Research-mode agent at depth 1, 2, or 3 (Phases A–G)
- You are executing as a peer-review agent (`peerReviewForBranch` set)

**Never load this skill** in Quick mode, Ensemble Aggregation mode, or Adversarial Review function — those are owned by `meditation-quick`, `meditation-ensemble`, and `meditation-review` respectively.

## Prerequisites

1. Verify `flags.enableMemories` is `"true"` (abort if not)
2. Confirm `comprehensiveness:` payload is present in the spawn prompt — abort with: "`comprehensiveness:` payload required; missing from spawn prompt — caller misconfigured" if missing
3. Confirm `theming:` payload is present — abort with a clear error pointing at Theme Preflight if missing
4. Confirm `modelStrategy:` payload is present — abort with: "`modelStrategy:` payload required; missing from spawn prompt — caller misconfigured" if missing

## Input Parameters (depth-0 manager invocation)

The depth-0 manager receives these parameters from the calling agent:

```yaml
meditateMode: "research"
workingDir: "<absolute path to meditations/{yyyymmdd}-{topic-slug}/>"
theming: { ... }                  # Theme Preflight payload — REQUIRED
comprehensiveness: { ... }        # Richness payload — REQUIRED; abort if missing
modelStrategy: { ... }            # Model strategy payload — REQUIRED; abort if missing
confirmDeepFacets: "none" | "depth_2_only" | "all_levels"
maxDepth: 1 | 2 | 3               # default 3
ensembleModel: "<model-slug>"     # derived from modelStrategy at the depth-0 manager; carrier for per-spawn model: selection
preConfirmedFacets: [ ... ]       # only when in ensemble_max — skip step 4 derivation
```

`modelStrategy:` payload schema (verbatim in the `/crux-meditate` command's **Model Strategy payload** section):

```yaml
modelStrategy:
  mode: "none" | "random" | "per_branch" | "ensemble_max"
  pool: [{slug, label}, ...]
  resolved_model_slug: null | "<slug>"          # set when mode == "random"
  resolved_model_label: null | "<label>"
  branch_assignments: []                         # set in step 4b when mode == "per_branch"
  assignment_policy_note: null | "<note>"
```

## Input Parameters (child Research agent, depth 1–3)

```yaml
meditateMode: "research"
workingDir: "<path>"
branchNumber: {N}
meditateDepth: {D}                # 1, 2, or 3
maxDepth: {D}                     # propagated unchanged
subfocus: "<confirmed facet or derived subfocus>"
subfocusSlug: "<kebab-case slug>"
subfocusIndex: {S}                # 0 at depth 1; 1/2/3 at depth 2/3
parentSubfocus: "<parent's subfocus or null at depth 1>"
siblingFacets: [ ... ]
theming: { ... }                  # propagated unchanged — REQUIRED
comprehensiveness: { ... }        # propagated unchanged — REQUIRED; abort if missing
modelStrategy: { ... }            # propagated unchanged — REQUIRED; abort if missing
confirmDeepFacets: "none" | "depth_2_only" | "all_levels"
ensembleModel: "<model-slug>"     # when present, propagated unchanged; used as the per-spawn model: value for this branch's subtree
```

## Depth-0 Manager Workflow (steps 1–13)

### Step 1 — Check Feature Guard

Verify `flags.enableMemories` is `"true"`. If not, return a message saying the feature is disabled and stop. The calling agent will relay this to the user.

### Step 2 — Create Working Directory

Create `meditations/{yyyymmdd}-{topic-slug}/` where `{topic-slug}` is a kebab-case summary of the flag-stripped input (max 40 chars). If the directory already exists (re-run on same day/topic), append a numeric suffix.

### Step 3 — Initialize Coordination Files (Research mode only)

Seed an empty `facet-registry.yml` and an empty `citations-index.yml` in the working directory. Do NOT create `.facet-registry.lock/` yet — the lock is created on demand per the **Facet registry protocol** below.

### Step 4 — Derive Top-Level Facets + Draft Suggestions Payload and Confirm (Pattern B)

**Pre-confirmed facets shortcut (ensemble mode)**: If the spawn prompt includes a `preConfirmedFacets` parameter alongside a shared `init-suggestions-shared-{ts}.yml`, skip the entire derivation and confirmation flow. Use the provided facets directly — write them to `facets.md` (with their citations, parent-context summary, and partitioning statement), append them to `facet-registry.yml`, and extract the `confirmDeepFacets` enum value, the confirmed `comprehensiveness:` payload, and the confirmed sections/visualisations/additional-focus-areas from the spawn prompt. Proceed directly to step 4b.

**Standard path (non-ensemble)**: Analyse the input (or current chat context if no args) to identify three distinct exploration facets **and** a draft suggestions payload from the same seed exploration. Do this in a single analysis pass.

**Facet derivation** — each facet must be:
- **Complementary, not overlapping** — e.g. the technical theme, the user's underlying intent, and the broader topic area
- **Independently explorable** — each branch can go deep without needing the other branches' context
- **Concise** — one sentence each, framed as a specific angle or question
- **Cited** — every facet description must be backed by at least one citation (memory, file, or chat reference)

**Draft suggestions payload** — produce alongside the facets in the same analysis pass. Every item MUST carry `source_signals: [...]` listing the citations / memories / files / chat references that motivated the suggestion:

- `proposed_sections` (**3–8 items**): candidate report section titles with `id`, `title`, `rationale`, `source_signals`.
- `proposed_visualisations` (**5–10 items**): candidate visualisation types from the existing Chart.js / D3 / infographic catalogue with `id`, `type`, `rationale`, `what_it_would_show`, `source_signals`.
- `additional_focus_areas` (**0–5 items**; often 0): each with `id`, `title`, `rationale`, `source_signals`, `recommended_treatment` set as one of `skip` / `additional_facet` / `report_section_only` / `additional_facet_AND_section` (default recommendation = `report_section_only` unless evidence justifies promoting to a facet).

Then run the **Combined Pattern-B flow** (canonical in the `/crux-meditate` command):

1. Write a draft to `facets-pending-{ts}.yml`. Schema is **extended** to mirror all 4 blocks: `facets` (3 items), `sections` (3–8 items), `visualisations` (5–10 items), `additional_focus_areas` (0–5 items with `recommended_treatment`), plus `parent_context_summary`.
2. Escalate via Pattern B: return a combined `needs_user_input` block. **Do NOT call `AskQuestion` yourself — this is the calling agent's responsibility.**

Combined `needs_user_input` block schema:
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
      # 3–8 items
      - id: "section-{slug-1}"
        title: "{section-1-title}"
        rationale: "{1-line why this section fits}"
        source_signals: ["[chat: turn-N]", "[memory: {memory-title}]"]
      # ... up to 8
    visualisations:
      # 5–10 items
      - id: "viz-{slug-1}"
        type: "{visualisation-type-enum}"
        rationale: "{1-line why this viz fits}"
        what_it_would_show: "{1-2 sentences}"
        source_signals: [...]
      # ... up to 10
    additional_focus_areas:
      # 0–5 items
      - id: "focus-{slug-1}"
        title: "{focus-area-title}"
        rationale: "{1-line why this is scope-adjacent but not a primary facet}"
        source_signals: [...]
        recommended_treatment: "report_section_only"
      # ... up to 5
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
          custom_report_section_title: "..."   # only when treatment ∈ {report_section_only, additional_facet_AND_section}
      deep_confirm_decision: "none | depth_2_only | all_levels"
    on_regenerate: |
      Re-derive facets only; sections/visualisations/focus-areas MAY be
      re-derived alongside if the new facet shape implies a different
      recommendation set. Re-emit the combined needs_user_input with the
      new payload. Capped at 3 regeneration attempts per existing rule.
```

3. Resume with the user's combined decision (calling agent passes all 5 sub-question answers):
   - `cancel` → abort the meditation entirely; do NOT write `facets.md` or `init-suggestions-{ts}.yml`.
   - `regenerate` → re-derive a different set of facets; write a fresh `facets-pending-{ts}.yml`; re-escalate. Loop **capped at 3 regeneration attempts**.
   - `modify_one` / `modify_multiple` → apply the user's `facet_overrides`.
   - `confirm_all` (or after overrides applied) → proceed to step 4b below.

### Step 4b — Resume-handler: apply confirmed payload, write `init-suggestions-{ts}.yml`, reconcile additional focus areas

**Apply facet decisions**:
- Append the confirmed facets (3 ± any additional from focus-area reconciliation below) to `facet-registry.yml`.
- Promote the draft to the final `facets.md` (confirmed facet descriptions, citations, parent-context summary, and explicit partitioning statement), then delete `facets-pending-{ts}.yml`.

**4-mode additional-focus-area reconciliation**: for each focus area in `additional_focus_areas_decisions`:
- `skip` → record as an entry in `additional_focus_areas[]` in the YAML below with `treatment: "skip"` (the canonical array is a single per-decision array; `resulting_section_id` and `resulting_branch_index` stay `null`). No facet, no section.
- `additional_facet` → append a new entry to the confirmed facet set (becomes Branch 4 / 5 / 6 …, sequenced after Branch 3 in registration order; slug derived per existing facet-slug rules). Append to `facet-registry.yml` and `facets.md`. The new branch spawns alongside the original 3 in step 5. No dedicated report section beyond what the new branch's natural output produces (at `compact`/`default` richness → contributions appear in consolidation prose only; at `detailed`/`exhaustive` → a standard per-branch section appears under the auto-derived facet title). Set `new_branch_index` to the next branch number.
- `report_section_only` → record as an entry in `additional_focus_areas[]` with `treatment: "report_section_only"` and `custom_report_section_title` = the focus-area title (or user-supplied title); populate `resulting_section_id` per the schema invariant. Do NOT add a facet. The report skill reads `init-suggestions-{ts}.yml` and must include a section by that exact title.
- `additional_facet_AND_section` → both effects: new facet (per `additional_facet` semantics above) AND record a confirmed report section title (per `report_section_only` semantics). Populate both `new_branch_index` and `custom_report_section_title`.

**Cost-ack re-presentation**: if ANY focus-area decision is `additional_facet` OR `additional_facet_AND_section`, the calling agent (not this subagent) fires the read-only-richness variant of `Q-Cost-and-Richness-Acknowledgment` BEFORE this subagent resumes step 5. This subagent only proceeds to step 5 after the calling agent confirms re-acknowledgment (passed as `cost_reack_confirmed: true` in the resume payload). If the user cancels at re-presentation, abort: do NOT write `init-suggestions-{ts}.yml` and do NOT spawn children.

**Per-branch model assignment (`modelStrategy.mode == "per_branch"` only)**: after the final confirmed-branch count `B` is known (3 + any accepted `additional_facet` / `additional_facet_AND_section` opt-ins) AND after any cost-ack re-presentation has resolved, resolve `modelStrategy.branch_assignments[]` per the policy in the `/crux-meditate` command's **Argument Handling** section:

1. Compute `B = len(confirmed_facets)` (after `additional_facet` reconciliation).
2. Let `P = len(modelStrategy.pool)`.
3. Deterministically shuffle the pool with seed = SHA-256 of `"{topic_slug}-{first-pending-facets-ts}"` truncated to 32 bits (reproducible within a run; varies across runs).
4. If `P ≥ B`: `branch_assignments[i] = shuffled_pool[i]` for `i ∈ [0, B-1]` (each branch gets a distinct model).
5. If `P < B`: `branch_assignments[i] = shuffled_pool[i mod P]` for `i ∈ [0, B-1]` (round-robin; some models repeat); set `modelStrategy.assignment_policy_note = "per_branch model strategy: poolSize={P} < branchCount={B}; rounded-robin assignments may repeat"`.
6. Each entry: `{branch_index: i+1, slug: pool[k].slug, label: pool[k].label}`.

This update to `modelStrategy` is **in-memory only** for the depth-0 manager — it's a derived field used to drive per-spawn `model:` dispatch in step 5. The resolved assignments are also surfaced in `facets.md` per the `crux-skill-memory-meditation-coordination` skill so the report can attribute findings by branch.

For `modelStrategy.mode ∈ {"none", "random", "ensemble_max"}`, leave `branch_assignments` empty — those modes do not use per-branch dispatch.

**Write `init-suggestions-{ts}.yml`**: write to `meditations/{yyyymmdd}-{topic-slug}/init-suggestions-{ts}.yml`. Schema:

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

**Schema invariants**: `resulting_section_id` is set iff `treatment ∈ {report_section_only, additional_facet_AND_section}`; `resulting_branch_index` is set iff `treatment ∈ {additional_facet, additional_facet_AND_section}`; `custom_report_section_title` is set iff `treatment == additional_facet_AND_section`; at `compact`/`default` richness, `additional_facet`-only opt-ins produce `resulting_branch_index` but NO `resulting_section_id` (K4 carve-out). The `confirmed_sections` array includes entries from depth-0 seed exploration AND from accepted `report_section_only` / `additional_facet_AND_section` focus-area decisions.

> **CRITICAL**: `additional_focus_areas_accepted` and `additional_focus_areas_skipped` are LEGACY field names. The canonical schema uses a SINGLE `additional_focus_areas[]` array with per-item `treatment:` field. Never emit the legacy field names in any file this skill produces.

Hold onto the `confirmDeepFacets` enum value and the `comprehensiveness:` payload — both are propagated unchanged to every child spawn in step 5.

> **Note**: `facets.md` will be **updated again in step 9** (post-consolidation) to append a comprehensive **Branch & Leaf Index** linking to every file the meditation produces, including the `[Init suggestions](init-suggestions-{ts}.yml)` entry in `## Top-level artifacts`. From step 9 onward, `facets.md` is the single navigational entry point for the entire meditation.

### Step 5 — Spawn Explorers

Only after step 4b has completed (facets confirmed, `init-suggestions-{ts}.yml` written, `modelStrategy.branch_assignments` resolved for `mode: "per_branch"`, cost-reack resolved if any additional facets were accepted): Launch one background `crux-cursor-meditation-guide` subagent in Meditate mode per **confirmed** facet (3 + any accepted `additional_facet` / `additional_facet_AND_section` focus areas), all in parallel.

**Per-spawn `model:` dispatch** (driven by `modelStrategy.mode`):
- `mode: "none"` → omit `model:` from the Task invocation; do not set `ensembleModel` on the child.
- `mode: "random"` → pass `model: modelStrategy.resolved_model_slug`; set `ensembleModel: modelStrategy.resolved_model_slug` on the child so descendants inherit.
- `mode: "per_branch"` → pass `model: modelStrategy.branch_assignments[branchNumber - 1].slug`; set `ensembleModel: modelStrategy.branch_assignments[branchNumber - 1].slug` on the child so all descendants of THIS branch use the same model.
- `mode: "ensemble_max"` → this depth-0 manager is itself one of N per-tree managers spawned by the calling agent's Ensemble Protocol; its incoming `modelStrategy` is pinned to `mode: "random"` for the assigned pool model — handle as `random`.

Each child receives:
- `meditateMode`: `"research"`
- `meditateDepth`: 1
- `maxDepth`: the value from the calling agent's Depth Selection (1, 2, or 3; default 3)
- `branchNumber`: 1, 2, 3, … (one per confirmed facet including additional-facet opt-ins)
- `branchSlug`: the kebab-case slug derived for this branch's top-level **confirmed** facet
- `subfocus`: the **confirmed** facet description
- `parentSubfocus`: `null` at depth 1
- `workingDir`: the absolute path to the meditation working directory
- `parentContext`: summary of the chat context and any user-provided input
- `siblingFacets`: the other branches' **confirmed** facet descriptions
- `theming`: the Theme Preflight payload, passed through unchanged
- `comprehensiveness`: the comprehensiveness payload, passed through **unchanged** — **MUST be present; subagent aborts with "`comprehensiveness:` payload required; missing from spawn prompt — caller misconfigured" if missing**
- `modelStrategy`: the model strategy payload, passed through **unchanged** — **MUST be present; subagent aborts with the canonical error if missing**
- `confirmDeepFacets`: the enum value from the combined confirmation (`none` | `depth_2_only` | `all_levels`) — propagated unchanged to every deeper child
- `ensembleModel`: per the per-spawn `model:` dispatch rules above (propagated unchanged to every deeper child)

### Step 6 — Poll for Branch Outputs

Wait for one depth-1 file per branch using prefix-glob polling — `branch-1-depth-1-sub-0-*.md`, `branch-2-depth-1-sub-0-*.md`, `branch-3-depth-1-sub-0-*.md`. Resolve the latest match per branch with `ls -1t <workingDir>/<glob> 2>/dev/null | head -n 1`. Use short intervals (10–30s); do not read JSONL transcripts. All three branch files must exist before proceeding. If any branch glob has been pending for more than 5 minutes AND `.facet-registry.lock/` exists, log a warning and `rmdir` the stale lock so children can proceed (see **Facet registry protocol** for the orphan-recovery rule).

**Deep-confirmation hook (when `confirmDeepFacets ≠ none`)**: the same poll loop **also** globs `pending-facets-*.yml` in the working directory. When one (or several) appears, batch them into a single `needs_user_input` block (one entry per pending file, using the same confirm/modify/regenerate option set as Q-Confirm-1) and escalate to the calling agent via Pattern B. When resumed with the user's decisions, write the corresponding `confirmed-facets-{path-id}-{ts}.yml` for each (mirroring the pending file's path-id and `{ts}`), then resume the branch-output poll. See the **Deep confirmation flow** in the `/crux-meditate` command for the full pending/confirmed schema and the per-child `confirmed` / `modified` / `regenerate` decision semantics (regenerations capped at 3 per child).

### Step 7 — Branch Peer Review (Research mode only)

Spawn 3 `crux-cursor-meditation-guide` peer-review agents in parallel — one per branch. Per-spawn `model:` dispatch:

- `modelStrategy.mode == "none"` → omit `model:`.
- `modelStrategy.mode == "random"` → pass `model: modelStrategy.resolved_model_slug` (entire tree on one model, so peer reviewers also).
- `modelStrategy.mode == "per_branch"` → **omit `model:`** so the peer reviewer runs on the caller's model. Per-branch dispatch is intentionally NOT applied to peer reviewers because they compare branches against each other; using a single unified model keeps the cross-branch evaluation fair (the peer reviewer is a cross-branch evaluator, not a within-branch worker).
- `modelStrategy.mode == "ensemble_max"` → pass `model: ensembleModel` (this depth-0 manager's pinned per-tree model).

Each is assigned a different `peerReviewForBranch` (1, 2, or 3) and reads the other two branches' final depth-1 files plus its own branch's file, then writes `branch-{N}-peer-review-{branchSlug}-{ts}.md` per the **Peer review file spec** below. Poll for all three peer-review files via prefix-glob `branch-{N}-peer-review-*.md` (one per branch) before proceeding to consolidation.

### Step 8 — Consolidate + K10c Reflection

Read all branch files (all depths) **plus** all peer-review files **plus** `citations-index.yml`. Synthesize into `consolidation.md` following the **Subject-Matter Focus** rule in the `/crux-meditate` command — use facet titles as section headings (never "Branch 1/2/3"), translate `[child: branch-N-depth-D-sub-S]` citations to `[research: {subfocus-slug}]` format, and never reference branches, depths, leaf agents, or other process concepts. Structure:
- Key discoveries organized by facet theme (using the confirmed facet titles as section headings)
- Cross-cutting connections and emergent themes (referencing topics by name, not by branch number)
- Contradictions identified during quality review (presenting the substance, not "surfaced by peer review")
- Gaps and open questions (framed as subject-matter gaps, not process gaps)
- New evidence and supplementary findings from quality review
- Potential directions for further exploration
- A unified `## Citations` section that includes every distinct citation referenced anywhere in the meditation, with `[child: ...]` references translated to `[research: {subfocus-slug}]` format

Write `consolidation.md` to the working directory.

**K10c — In-pass consolidation reflection (runs in the SAME LLM pass as consolidation — no additional file read)**: After writing `consolidation.md`, reflect on what enhancements would most increase the report's value to the reader. The inputs for this reflection are the SAME inputs already in context for consolidation (branch files, peer-review files, `citations-index.yml`, the consolidation prose just written). This reflection adds ~1–2k tokens of LLM thinking overhead — no extra agent spawn.

**K10c reflection rubric**: score each candidate enhancement on two axes (1–10 each):

- **`impact_score` (1–10)** — how much does this enhancement enable the reader to act or decide?
  - `9` = Enhancement directly enables a high-stakes decision. Example: an `executive_summary` for a vendor-comparison meditation that unblocks a board presentation; without it, the reader cannot make the decision the meditation was commissioned to inform.
  - `5` = Enhancement clarifies reading order but doesn't change recommended action. Example: a `glossary` that helps a non-domain reader skim the report faster, but every domain reader could already act on the existing content.
  - `2` = Cosmetic improvement only. Example: a `reader_persona_tldrs` for a 3-page meditation that the existing introduction already covers; the persona TL;DRs would be redundant phrasings.
- **`insight_value_score` (1–10)** — how much new substantive insight does this enhancement surface?
  - `9` = Surfaces a cross-branch synthesis no individual branch made visible. Example: a `cross_branch_synthesis_section` that connects an architectural choice surfaced in Branch 1 with a cost-of-ownership pattern surfaced in Branch 3 — neither branch made the connection but the synthesis is decision-relevant.
  - `5` = Re-organises content from one branch into a more readable form. Example: a `risks_section` that gathers risk findings already prominent in Branch 2 into a single section with a taxonomy axis. The reader gains organisational benefit but no new substantive insight.
  - `2` = Paraphrases content already prominent in existing sections. Example: an `action_plan` whose items each match one-to-one with the existing "Recommended Next Steps" section bullets, with no horizon-specific differentiation.

**K10c scoring and selection**:
- Compute `composite_score = impact_score × insight_value_score` (multiplicative formula). If `cruxMemories.meditate.finalisationEnhancements.weights` is configured (or `formula: "weighted_sum"` is set), use the weighted-sum formula instead.
- Filter out any candidate whose `impact_score < minimum_impact_threshold` (default = 6; configurable via `cruxMemories.meditate.finalisationEnhancements.minimumImpactThreshold`).
- Select the **top 5 by `composite_score`** (descending). Tie-break: prefer `cost_class: "cheap"` over `cost_class: "expensive"`.
- Consider all enhancement types from the K10a menu but materialise only those the branches' findings + consolidation prose surface as genuinely relevant.
- **Graceful degradation**: if fewer than 5 candidates clear the threshold, set `degradation_reason: "fewer than 5 candidates met threshold"` and emit the subset. If zero candidates clear, set `degradation_reason: "no high-quality candidates surfaced"` and skip the `Q-Finalisation-Enhancements` gate entirely (workflow proceeds to adversarial review unchanged — do NOT return a `needs_user_input` block for K10).

**K10c candidate type catalogue** (11 types):

*Cheap types (7) — rendered in the report via respawn*:
- `executive_summary` → `payload: { target_persona: "leadership"|"engineer"|"product"|"researcher", max_paragraphs: int, anchor_findings: ["[research: slug]", ...] }`
- `action_plan` → `payload: { horizons: ["7d", "30d", "quarter"], items_per_horizon: int, anchor_findings: [...] }`
- `risks_section` → `payload: { risk_taxonomy_axes: ["likelihood", "impact", "detection_difficulty"], anchor_findings: [...] }`
- `glossary` → `payload: { term_count_estimate: int, anchor_branches: ["branch-1", ...] }`
- `decision_tree_infographic` → `payload: { root_decision: "...", depth: int, anchor_findings: [...] }`
- `reader_persona_tldrs` → `payload: { personas: ["leadership", "engineer", "product"], paragraphs_per_persona: int }`
- `cross_branch_synthesis_section` → `payload: { axes: ["convergent", "divergent"], anchor_findings_per_axis: { convergent: [...], divergent: [...] } }`

*Expensive types (4) — spawn follow-up work (queue by default; spawn_now opt-in)*:
- `additional_meditation` → `payload: { proposed_topic: "...", proposed_facet_seed: ["facet-1", "facet-2", "facet-3"], recommended_depth: 1|2|3, recommended_mode: "research"|"quick" }`
- `extracted_spec` → `payload: { proposed_slug: "{yyyymmdd}-{slug}", overview: "...", candidate_subtasks: [{title: "...", agent: "{subagent-id}"}], spec_template: "{relative-path}" }`
- `extracted_memories` → `payload: { candidates: [{title: "...", type: "learning"|"redflag"|"core"|"idea"|"goal", body_summary: "...", source_signals: [...]}] }`
- `expanded_branch` → `payload: { target_branch_index: int, recommended_new_depth: 1|2|3, facet_emphasis_override: "...", recommended_mode: "research"|"quick" }`

**K10c — Write `finalisation-enhancements.yml`** (BEFORE returning the `needs_user_input` block to the calling agent). Write to `meditations/{yyyymmdd}-{topic-slug}/finalisation-enhancements.yml`. Schema:

```yaml
---
generated_utc: "{utc-timestamp}"
topic_slug: "{topic-slug}"
mode: "research"
ensemble: false
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

If `degradation_reason: "no high-quality candidates surfaced"`, write the YAML with an empty `candidates: []` and skip returning a K10 `needs_user_input` block (proceeding directly to adversarial review).

Otherwise, return the K10 `needs_user_input` block to the calling agent:
```yaml
needs_user_input:
  reason: "finalisation-enhancements-gate"
  pattern: "B"
  context: |
    Post-consolidation reflection surfaced {N} candidate finalisation enhancements.
    Multi-select 0–5. Cheap items (respawn the report skill to add the enhancement)
    are zero agent-count cost. Expensive items default to queue (write a follow-up
    artefact for later); opt-in to spawn_now for immediate spawn after adversarial review.
  decision_required: true
  files_written:
    - "finalisation-enhancements.yml"
  resume_handler_contract:
    expected_input:
      finalisation_enhancements_path: "meditations/{slug}/finalisation-enhancements.yml"
      # calling agent has updated the YAML in place with accepted/treatment/decided_at_utc
```

**Do NOT return to the calling agent yet for the step 9+ flow** — the K10 `needs_user_input` above IS the mechanism for the `Q-Finalisation-Enhancements` gate. After the calling agent resolves the gate and resumes this subagent (passing `finalisation_enhancements_path`), execute step 8b.

### Step 8b — K10b Resume-handler for accepted enhancements

Re-read the updated `finalisation-enhancements.yml` (calling agent has filled in `accepted`, `treatment`, `decided_at_utc` for each candidate). Process each accepted item:

- **For each `accepted: true, treatment: "respawn"` entry (cheap types)**: build an entry for the first adversarial-review iteration's respawn payload's `accepted_finalisation_enhancements:` list. The respawn payload bundles:
  1. `accepted_finalisation_enhancements` (additive new sections/charts; rendered first)
  2. `missing_init_suggestion_visualisations` (if Dim 13 also fires; additive)
  3. `missing_init_suggestion_sections` (if Dim 13 also fires; may auto-resolve via step 1 overlap)
  Pass this respawn payload to the adversarial reviewer in step 10's first iteration.

- **For each `accepted: true, treatment: "queue"` entry (expensive types)**: write the appropriate follow-up artefact to the working directory. Do NOT spawn agents:
  - `additional_meditation` → write `follow-up-meditation-{ts}.yml`
  - `extracted_spec` → write `follow-up-spec-{ts}.yml`
  - `extracted_memories` → write `follow-up-memories-{ts}.yml`
  - `expanded_branch` → write `follow-up-expansion-{ts}.yml`

- **For each `accepted: true, treatment: "spawn_now"` entry (expensive types, opt-in)**: defer spawning until AFTER the adversarial-review cycle completes. Accumulate in a `pending_spawn_now: [...]` list — this list is returned to the calling agent in step 13's final return.

- **For each `accepted: false` or `treatment: "unchosen_persisted"` entry**: no action.

**Non-infinite-loop guarantee**: the `accepted_finalisation_enhancements` respawn cause can fire AT MOST ONCE per meditation. Total useful respawns remains ≤ 2.

After processing all accepted items, proceed to step 9.

### Step 9 — Update `facets.md` with the Branch & Leaf Index

Glob the working directory for actual filenames (`branch-*-depth-*-sub-*-*.md`, `branch-*-peer-review-*.md`, every `review-pre-report-*-iter-*.md` discovered, every `confirmed-facets-*.yml` discovered, the latest `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf` pair if any). Append a Branch & Leaf Index section to `facets.md` per the canonical format in the `crux-skill-memory-meditation-coordination` skill. Use relative paths. Enumerate missing slots explicitly.

### Step 10 — Adversarial Review and Fix Cycle

Spawn a **fresh** `crux-cursor-meditation-guide` subagent in **Adversarial Review** function per the canonical spec in the `crux-skill-memory-meditation-review` skill. Per-spawn `model:` dispatch (adversarial reviewer is the final unified evaluator across the entire tree):

- `modelStrategy.mode == "none"` → omit `model:`.
- `modelStrategy.mode == "random"` → pass `model: modelStrategy.resolved_model_slug`.
- `modelStrategy.mode == "per_branch"` → **omit `model:`** so the reviewer runs on the caller's model. The reviewer audits all branches together; a single unified model preserves consistent severity classification across branches that were explored by different models.
- `modelStrategy.mode == "ensemble_max"` → pass `model: ensembleModel` (this depth-0 manager's pinned per-tree model).

Pass `meditateMode`, `reviewerIteration` (1-indexed, capped at 3), `workingDir`, `theming`, `comprehensiveness`, `modelStrategy`, and `priorReviewPath` (null on first iteration). Iterate up to **3 times** until verdict is `PASS` or `PASS_WITH_ADVISORIES`. Bubble Pattern-B escalations up to the calling agent.

If the loop reaches iteration 3 with `MUST_FIX` findings still unresolved, the verdict is `ESCALATE`: **abort steps 11 and 12** and proceed to step 13 with unresolved findings.

### Step 11 — Re-run Step 9 (post-review refresh)

Only when the verdict from step 10 was `PASS` or `PASS_WITH_ADVISORIES`: re-glob the working directory and refresh the Branch & Leaf Index in `facets.md` so every link still resolves and the missing-slots enumeration is accurate.

### Step 12 — Generate the Mandatory Report (HTML + PDF)

Only when the verdict from step 10 was `PASS` or `PASS_WITH_ADVISORIES`; **skip entirely on `ESCALATE`**. Load the `crux-skill-memory-meditation-report` skill. Follow the full Report Generation contract verbatim. Key obligations:
- Read all meditation files: `consolidation.md`, `facets.md`, `facet-registry.yml`, `citations-index.yml`, every `branch-*-depth-*-sub-*-*.md`, every `branch-*-peer-review-*.md`.
- Honour the `comprehensiveness:` payload for all level-driven decisions.
- Apply `theming` payload to every visual decision; **never default to the homogenised AI look**.
- Enforce Universal Contrast in all three render states.
- Write `report-{topic-slug}-{ts}.html` and render PDF via headless Chrome.
- Verify both files exist and are non-empty before declaring complete.

### Step 12b — Write Process Retrospective

Write `retrospective-{ts}.md` **always**, including on `ESCALATE`. Follow the **Process Retrospective** section in the `/crux-meditate` command for the required sections. Use the same `{ts}` as the report pair when one was generated, or capture a fresh UTC timestamp on `ESCALATE`. Update `facets.md`'s Branch & Leaf Index to include the retrospective link under "Top-level artifacts".

### Step 13 — Return to Calling Agent

Return: working directory path, `facets.md` path, `consolidation.md` text and path, `retrospective-{ts}.md` path, report HTML+PDF pair (when generated), every `review-pre-report-*-iter-*.md` path (sorted ascending by iteration number), and (when any expensive `spawn_now` items were accepted in step 8b) a `pending_spawn_now: [...]` list. Include a `follow_up_adjustments_reminder` field. On `ESCALATE`, return the working directory, `facets.md`, `consolidation.md`, `retrospective-{ts}.md`, every review iteration path, and a structured summary of unresolved `MUST_FIX` findings — explicitly **no** report paths.

## Recursive Exploration Protocol — Research Mode (Phases A–G)

Each child agent at depths 1 through `maxDepth - 1` follows this protocol. The agent receives `meditateMode: "research"`, `workingDir`, `branchNumber`, `meditateDepth`, `maxDepth`, `subfocus`, `subfocusSlug`, `subfocusIndex`, `parentSubfocus`, and `siblingFacets`.

```
Phase A — Research own subfocus first (no children yet):
  - Query memory corpus via memory index (title, tag, description, body search)
  - Examine code/files/web sources implied by the subfocus
  - Expand on subfocus in light of evidence
  - Track every claim with at least one citation (see Citations protocol below)

Phase B — Write findings file first:
  branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}-findings.md (working draft)

  Comprehensiveness honouring at leaf depth (when meditateDepth == maxDepth):
  - At comprehensiveness.level ∈ {detailed, exhaustive} (depth3_leaf_inclusion = verbatim_quotes):
    Phase B output MUST include verbatim quoted passages from cited sources in the
    ## Discoveries section (one or more block-quotes per claim that has an identified
    source passage).
  - At compact or default (depth3_leaf_inclusion = summary): leaf agents write a summary
    without verbatim quotes.
  - All agents at every depth: the ## Discoveries section MUST stay within
    comprehensiveness.minima.section_length_budget_tokens.per_facet tokens.
    Estimate token count as (character_count / 4).
  - At exhaustive (citation_density = per_finding_table): every finding table in Phase B
    output MUST include a citation column.

Phase C — Derive 3 child subfocuses from actual findings:
  - Each must be narrower than this agent's own subfocus
  - Each must be distinct from its siblings
  - Each must be globally unique against facet-registry.yml (Research mode only)

  Deep-confirmation hook (when confirmDeepFacets requires confirmation at this
  depth: depth_2_only at depth 1, OR all_levels at depth 1 or depth 2):
    1. BEFORE acquiring the registry lock, write the proposed 3 children to
       pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml where {N}/{D}/{S}/{ts}
       identify THIS agent (the parent that derived the proposed children).
       Schema: path block (branch, parent_depth, parent_sub_index, parent_slug),
       timestamp_utc, proposed_children[{sub_index, slug, subfocus, rationale}],
       status: "pending". See the canonical Deep confirmation flow in the
       /crux-meditate command for the full schema.
    2. Poll for the matching confirmed-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml
       using prefix-glob with the same branch/depth/sub segment and the {ts} from
       the pending file.
    3. Once the confirmation file exists, read it and apply the per-child decision:
         - confirmed → use the original child verbatim
         - modified  → replace with the user-supplied subfocus/slug/rationale
         - regenerate → re-derive that single child from research findings, write
           a new pending file with the same path-id but a fresh {ts}, and loop
           (capped at 3 regenerations per child).
    4. Only after all 3 children are confirmed, proceed to the registry-lock step.

  Acquire registry lock (mkdir-based — see Facet registry protocol).
  Read facet-registry.yml; check global slug + paraphrase uniqueness.
  Refine any colliding subfocus until all 3 are globally unique.
  Append the confirmed 3 subfocuses to facet-registry.yml.
  Release the lock.

Phase D — Spawn 3 children at depth+1 in parallel (only when meditateDepth < maxDepth):
  Each child receives: meditateMode ("research"), workingDir, branchNumber,
  maxDepth, parentSubfocus, subfocus, subfocusSlug, subfocusIndex (1, 2,
  or 3 — local to this parent's children), siblingFacets (the other two
  child subfocuses registered by this parent), theming (propagated unchanged),
  comprehensiveness (propagated unchanged — MUST be present; child aborts
  with "`comprehensiveness:` payload required; missing from spawn prompt —
  caller misconfigured" if missing), modelStrategy (propagated unchanged —
  MUST be present; child aborts with the canonical error if missing),
  confirmDeepFacets (propagated unchanged), ensembleModel (if present —
  propagated unchanged from this agent's own ensembleModel; descendants
  of a `per_branch` branch all inherit the SAME ensembleModel that was
  assigned at the depth-0 → depth-1 dispatch point). When ensembleModel
  is set, pass model: ensembleModel on the Task tool invocation.

Phase E — Wait for child files via prefix-glob:
  branch-{N}-depth-{D+1}-sub-{S}-*.md (one per child sibling-index S ∈ {1,2,3})
  Resolve the latest match per sibling-index with `ls -1t <workingDir>/<glob>
  2>/dev/null | head -n 1`. Validate each child's citations per the Citations
  protocol below; if any child's citations fail validation, delete that child's
  output file and respawn that child (up to 2 retries before recording a
  `## Citation failure` block and proceeding).

Phase F — Incorporate child findings bottom-up:
  - Read all 3 child files
  - REWRITE this depth's own file (do NOT just append) to weave children's
    findings into a single coherent document
  - Preserve every citation from this depth and from the children
  - Deduplicate overlapping evidence
  - Surface cross-child patterns
  - Flag contradictions in a ## Contradictions section
  - Provenance: every section indicates "this depth" or "child sub-{S}" via
    inline `[child: branch-N-depth-D-sub-S]` markers

Phase G — Promote findings file to final filename:
  branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md (no -findings suffix)
  Then delete the -findings draft so the working directory only retains the
  final aggregated file at this path.
```

**Leaf depth (deepest = `maxDepth`, Research mode)**: Phase A and Phase B only — no further recursion. When `meditateDepth == maxDepth`, the agent does not run Phases C–F. After Phase B completes, immediately promote the `-findings` draft to the final filename and delete the draft.

## Output File Format (branch files at all depths)

```yaml
---
mode: "research"
branch: {N}
depth: {D}
subfocus_index: {S}
subfocus_slug: "{kebab-case slug used in filename}"
subfocus: "{this agent's specific subfocus}"
parent_subfocus: "{parent agent's subfocus, or top-level facet if depth 1}"
parent_slug: "{parent's subfocus_slug, or null at depth 1}"
timestamp_utc: "{yyyymmddHHMMSS}"
timestamp_iso: "{ISO 8601}"
incorporated_children: ["branch-{N}-depth-{D+1}-sub-1-{slug}-{ts}.md", ...]   # empty array at depth 3
---
```

Body sections (mandatory):
- `## Subfocus Rationale` — why this narrowing was chosen
- `## Discoveries` — key findings from memory queries and research
- `## Connections` — patterns, relationships, non-obvious links
- `## Child Subfocuses` — the 3 narrower subfocuses derived for children (Phase C, post-research)
- `## Child Insights` — aggregated from child output files (Phase F rewrite), with provenance markers `[child: branch-N-depth-D-sub-S]`
- `## Contradictions` — contradictions surfaced between this depth's findings and the children's, or between children
- `## Summary` — concise distillation for parent consumption
- `## Citations` — every source backing every claim, with inline markers in the body (`[memory: ...]`, `[file: ...]`, `[web: ...]`, `[chat: ...]`, `[child: ...]`). **Mandatory in Research mode** — parents validate child citations strictly at Phase E (delete + respawn offending children, up to 2 retries).

## Citations Protocol (Research Mode)

Inline citation markers (mandatory in the body, attached directly to the claim they support):
- `[memory: title-or-id]`
- `[file: path/to/file.ts:start-end]`
- `[web: url]`
- `[chat: turn-N or quoted text]`
- `[child: branch-N-depth-D-sub-S]`

Every output file (depth-1, depth-2, depth-3, peer-review, consolidation) must:
1. Include a `## Citations` section at the bottom listing every source referenced anywhere in the body.
2. Use the inline citation markers above throughout the body.
3. Append every newly-introduced citation to `citations-index.yml`.

`citations-index.yml` schema (Research mode only, append-only):
```yaml
citations:
  - kind: "memory"            # one of: memory | file | web | chat | child
    ref: "agent-harness-orchestration-patterns"
    cited_by:
      - "branch-1-depth-1-sub-0-{slug}-{ts}.md"
      - "branch-2-depth-2-sub-1-{slug}-{ts}.md"
    note: "Patterns for parent-child handoff in async agent trees"
```

**Validation rule — Research mode (parent enforces during Phase E)**: When a parent reads a child file, it MUST verify:
- The child has a non-empty `## Citations` section
- Every inline citation marker in the body resolves to an entry in the `## Citations` section

If the citation check fails, the parent **deletes the child file and respawns the child** with an explicit instruction to add the missing citations. After 2 failed retries, the parent records a `## Citation failure` block in its own file naming the offending child and proceeds.

## Facet Registry Protocol (Research Mode Only)

`facet-registry.yml` schema (append-only):
```yaml
facets:
  - branch: 1
    depth: 0
    parent_slug: null              # null at depth 0; otherwise parent's subfocus_slug
    subfocus_slug: "auth-flow-trade-offs"
    subfocus: "Trade-offs in authentication flows for multi-tenant SaaS"
    timestamp_utc: "20260516103045"
    registered_by: "depth-0 manager"
  # ...
```

`mkdir`-based lock-and-append protocol (every registry update at Phase C must use this):
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

**Orphan recovery**: if an agent crashes while holding the lock, the orphaned `.facet-registry.lock/` directory must be cleaned up by the depth-0 manager during step 6 (branch-output polling). If any branch's prefix-glob has been pending for more than 5 minutes AND `.facet-registry.lock/` exists, log a warning and `rmdir "{workingDir}/.facet-registry.lock"` so other agents can proceed.

## Peer Review File Spec (Research Mode Only)

Filename pattern: `branch-{N}-peer-review-{branchSlug}-{yyyymmddHHMMSS}.md` (one per branch).

```markdown
---
peer_review_for_branch: {N}
reviewer_agent: "branch-{N} peer reviewer"
reviewed_branches: [1, 2, 3]
timestamp_utc: "{yyyymmddHHMMSS}"
---

## Reinforcements
{points where this branch's findings independently reinforce a sibling — cite both}

## Contradictions
{points where this branch contradicts a sibling — cite both, propose which is more strongly supported}

## Gaps
{aspects a sibling could have explored but didn't, given what this branch discovered — cite the discovery that revealed the gap}

## New Evidence
{any new sources this peer reviewer surfaces while comparing branches}

## Citations
{full citation list — sources from this branch, sources from siblings being reviewed, and any new sources introduced by the peer reviewer}
```

## Research vs Quick Differences (Research Column)

| Aspect | Research (this skill) |
|--------|----------------------|
| Recursion order | Depth-first within each branch (parent finishes research before deriving children) |
| Facet uniqueness | Global via `facet-registry.yml` + `mkdir`-based lock |
| Citations | Mandatory; inline markers + `## Citations` section validated strictly by parent during Phase E (offending children re-spawned, up to 2 retries) |
| Bottom-up incorporation | Parent **rewrites** its own file (Phase F) to weave in children's findings |
| Peer review | Dedicated peer-review agents spawned post-branch-completion (depth-0 step 7) |
| Consolidation inputs | `branch-*` files + `branch-*-peer-review-*` files + `citations-index.yml` |
| Coordination files | `facet-registry.yml`, `citations-index.yml`, `.facet-registry.lock/` (transient) |

For the Quick column, see the `crux-skill-memory-meditation-quick` skill.

## Cross-Skill References

- `crux-skill-memory-meditation-coordination` — filename grammar (incl. `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml` rows), prefix-glob polling rule, Branch & Leaf Index template
- `crux-skill-memory-meditation-review` — adversarial review contract (step 10); bundles cheap accepted enhancements into iter 1 respawn payload
- `crux-skill-memory-meditation-report` — report generation contract (step 12); consumes `comprehensiveness`, `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`
- `crux-skill-memory-meditation-quick` — Quick column of differences table + shared output schema reference
