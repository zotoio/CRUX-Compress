---
name: crux-skill-memory-meditation-quick
description: Quick-mode meditation protocol: 6-step parallel fan-out with optional deep-confirm hook, warn-only citation validation, upfront child derivation, no peer review, K10c reflection (same rubric, warn-only at every richness level per K7). Use when the `crux-cursor-meditation-guide` agent runs the Quick depth-0 manager or any Quick-mode child agent.
---

# CRUX Skill: Memory Meditation — Quick Protocol

Implements the full Quick-mode meditation contract: 6-step parallel fan-out, step 4b 4-mode `additional_focus_areas[]` reconciliation, `init-suggestions-{ts}.yml` write, K10c in-pass reflection (same rubric as Research — warn-only citation regime carried through), comprehensiveness honouring at Quick leaf depth, and the Quick-mode steps 9–13 (identical to Research with documented relaxations).

## When to Use

Load this skill when:
- The `crux-cursor-meditation-guide` agent is spawned in Quick mode (`--quick` flag, `meditateMode: "quick"`)
- You are executing the Quick-mode depth-0 manager workflow (steps 1–13 with Quick relaxations)
- You are executing as a Quick-mode child agent at depth 1, 2, or 3 (6-step protocol)

**Never load this skill** in Research mode, Ensemble Aggregation mode, or Adversarial Review function.

## Prerequisites

1. Verify `flags.enableMemories` is `"true"` (abort if not)
2. Confirm `comprehensiveness:` payload is present — abort with: "`comprehensiveness:` payload required; missing from spawn prompt — caller misconfigured" if missing
3. Confirm `theming:` payload is present — abort with a clear error pointing at Theme Preflight if missing
4. Confirm `modelStrategy:` payload is present — abort with: "`modelStrategy:` payload required; missing from spawn prompt — caller misconfigured" if missing

## Input Parameters (depth-0 manager, Quick mode)

Same shape as the Research depth-0 manager parameters (see the `crux-skill-memory-meditation-research` skill) with `meditateMode: "quick"`. The only parameter differences are:
- No `facet-registry.yml` operations (Quick mode skips global registry)
- No `citations-index.yml` initialization (Quick mode does not maintain this file)

## Input Parameters (Quick child agent, depth 1–3)

```yaml
meditateMode: "quick"
workingDir: "<path>"
branchNumber: {N}
meditateDepth: {D}
maxDepth: {D}                     # propagated unchanged
subfocus: "<subfocus>"
subfocusSlug: "<kebab-case slug>"
subfocusIndex: {S}
parentSubfocus: "<parent's subfocus or null at depth 1>"
siblingFacets: [ ... ]
theming: { ... }                  # propagated unchanged — REQUIRED
comprehensiveness: { ... }        # propagated unchanged — REQUIRED; abort if missing
modelStrategy: { ... }            # propagated unchanged — REQUIRED; abort if missing
confirmDeepFacets: "none" | "depth_2_only" | "all_levels"
ensembleModel: "<model-slug>"     # when present, propagated unchanged; per-spawn model: carrier for this branch's subtree
```

## Depth-0 Manager Workflow (Quick Mode)

All four pre-spawn user gates run identically in Quick mode — Depth Selection (calling agent), Cost & Scope Acknowledgment (calling agent), Theme Preflight (calling agent), and Facet Confirmation (subagent step 4 Pattern-B escalation). The post-consolidation steps 9–13 also run identically with the documented Quick-mode relaxations.

### Step 1 — Check Feature Guard

Verify `flags.enableMemories` is `"true"`. If not, return a message saying the feature is disabled and stop.

### Step 2 — Create Working Directory

Create `meditations/{yyyymmdd}-{topic-slug}/`. If the directory already exists, append a numeric suffix.

### Step 3 — SKIP

Quick mode does not use `facet-registry.yml`, `citations-index.yml`, or `.facet-registry.lock/`. Sibling-aware uniqueness uses `facets.md` only.

### Step 4 — Derive Top-Level Facets + Draft Suggestions Payload and Confirm (Pattern B)

Derive the three facets AND draft suggestions payload (proposed_sections 3–8 items, proposed_visualisations 5–10 items, additional_focus_areas 0–5 items) as in Research. Facet descriptions are NOT required to carry citation backing at this stage; per-branch `## Citations` requirements still apply to every child output. Run the **identical combined Pattern-B flow** (write extended `facets-pending-{ts}.yml` with all 4 blocks, escalate via combined `needs_user_input` block, resume with all 5 sub-question answers). Quick mode skips the `facet-registry.yml` append; the rest is identical including the `source_signals` discipline on every draft suggestion item.

The `needs_user_input` block schema is identical to the Research-mode block (see the `crux-skill-memory-meditation-research` skill, Step 4, for the full schema). Do NOT call `AskQuestion` — this is the calling agent's responsibility.

### Step 4b — Resume-handler: apply confirmed payload, write `init-suggestions-{ts}.yml`, reconcile additional focus areas

**Identical to Research** with these Quick-specific differences:
- `facet-registry.yml` operations are skipped (Quick mode only)
- `facets.md` append still happens (the confirmed facet descriptions, citations, parent-context summary, and explicit partitioning statement)
- `init-suggestions-{ts}.yml` is written with the same schema (see the `crux-skill-memory-meditation-research` skill for the full schema)

**4-mode additional-focus-area reconciliation**: same as Research — canonical `additional_focus_areas[]` array with per-item `treatment:` field:
- `skip` → record with `treatment: "skip"`, no facet, no section
- `additional_facet` → new branch spawned alongside the original 3; no dedicated report section beyond natural branch output (at `compact`/`default`); or per-branch section at `detailed`/`exhaustive`
- `report_section_only` → record with `treatment: "report_section_only"` and `custom_report_section_title`; populate `resulting_section_id`; report skill includes a section by that exact title
- `additional_facet_AND_section` → both effects; populate both `new_branch_index` and `custom_report_section_title`

**Cost-ack re-presentation**: same rule as Research — if ANY focus-area decision is `additional_facet` OR `additional_facet_AND_section`, the calling agent fires the read-only-richness variant before this subagent resumes step 5. Only proceeds after `cost_reack_confirmed: true`.

**Per-branch model assignment (`modelStrategy.mode == "per_branch"` only)**: identical to Research — after the final confirmed-branch count is known and any cost-ack re-presentation has resolved, resolve `modelStrategy.branch_assignments[]` per the policy in the `/crux-meditate` command's **Argument Handling** section (shuffle the pool with a topic+ts-derived seed; sample without replacement when `poolSize ≥ branchCount`, otherwise round-robin). The resolved assignments are surfaced in `facets.md` per the `crux-skill-memory-meditation-coordination` skill.

> **CRITICAL**: `additional_focus_areas_accepted` and `additional_focus_areas_skipped` are LEGACY field names. The canonical schema uses a SINGLE `additional_focus_areas[]` array with per-item `treatment:` field. Never emit the legacy field names.

Hold onto `confirmDeepFacets`, `comprehensiveness:`, and `modelStrategy:` — all propagated unchanged to every child spawn in step 5.

### Step 5 — Spawn Explorers

Identical to Research except each child receives `meditateMode: "quick"`. The `maxDepth`, `theming`, `comprehensiveness` (propagated unchanged — abort if missing), `modelStrategy` (propagated unchanged — abort if missing), `confirmDeepFacets`, and `ensembleModel` (when present) payloads are all threaded through unchanged. **Per-spawn `model:` dispatch is identical to Research** — see the Research skill's Step 5 for the four-case rule (none / random / per_branch / ensemble_max). For `per_branch`, the depth-0 manager looks up `modelStrategy.branch_assignments[branchNumber - 1].slug` and sets it as both the child's `model:` and its `ensembleModel` so descendants inherit.

### Step 6 — Poll for Branch Outputs

Identical poll loop (same prefix-glob, same resolve rule, same stale-lock guard is a no-op since no lock is ever created). The same **deep-confirmation `pending-facets-*.yml` polling hook** runs in Quick mode whenever `confirmDeepFacets ≠ none`.

### Step 7 — SKIP

No peer review in Quick mode.

### Step 8 — Consolidate + K10c Reflection

Consolidate from the branch files only at all depths that ran (per `maxDepth`). No peer-review files to glob, no `citations-index.yml` to merge. Follow the **Subject-Matter Focus** rule. If any branch surfaced citation gaps, include a "Citation gaps" callout in `consolidation.md`.

**K10c in-pass reflection runs identically in Quick mode** — same rubric, same scoring, same 5-candidate selection, same `finalisation-enhancements.yml` write. The only difference from Research is the set of inputs (no peer-review files, no `citations-index.yml`).

The `finalisation-enhancements.yml` schema is identical to Research except `mode: "quick"`. See the `crux-skill-memory-meditation-research` skill for the full schema and K10c rubric.

**Do NOT return to the calling agent yet** — step 8b (K10b resume-handler) fires after the calling agent resolves `Q-Finalisation-Enhancements`, then steps 9–13 follow.

### Step 8b — K10b Resume-handler for accepted enhancements

**Identical to Research**: re-read updated `finalisation-enhancements.yml`, process accepted cheap items into respawn payload, write follow-up artefacts for queued expensive items, accumulate `pending_spawn_now` list for spawn-now items.

### Step 9 — Update `facets.md` with the Branch & Leaf Index (NOT SKIPPED)

Append the Branch & Leaf Index per the same format used in Research mode, with these omissions:
- No per-branch "Peer review" lines
- No Research-only `facet-registry.yml` / `citations-index.yml` lines under "Top-level artifacts"
- Everything else (per-branch sections, depth-2/3 leaves, top-level `consolidation.md` + report pair + review iterations + confirmed-facets entries, missing-slots enumeration, index metadata) is identical

See the `crux-skill-memory-meditation-coordination` skill for the canonical Branch & Leaf Index template.

### Step 10 — Adversarial Review and Fix Cycle (NOT SKIPPED)

Same reviewer agent, same iteration cap (3), same severity classification, same Pattern-B `needs_user_input` contract (with the mandatory `context` decision-guidance), same `ESCALATE` semantics, with two relaxations:
- (a) "missing inline citation marker" findings are downgraded `MUST_FIX → SHOULD_FIX` (consistent with Quick mode's warn-only citation rule; unresolvable markers that *do* exist in the body remain `MUST_FIX`)
- (b) the "peer review thoroughness" review dimension is N/A

**Per-spawn `model:` dispatch for the reviewer is identical to Research** — see the Research skill's Step 10. For `modelStrategy.mode == "per_branch"`, omit `model:` so the reviewer runs on the caller's model (unified evaluator); for `random` pass the resolved slug; for `none` omit; for `ensemble_max` pass `ensembleModel`.

Reports are still gated on `PASS` / `PASS_WITH_ADVISORIES`; `ESCALATE` still aborts steps 11 and 12 exactly as in Research mode.

See the `crux-skill-memory-meditation-review` skill for the full review contract.

### Step 11 — Re-run Branch & Leaf Index (NOT SKIPPED)

Identical to Research: refresh `facets.md`'s Branch & Leaf Index after the reviewer's rewrites. Only runs when verdict from step 10 was `PASS` or `PASS_WITH_ADVISORIES`.

### Step 12 — Generate the Mandatory Report (HTML + PDF)

Identical to Research per the fully-documented contract in the `crux-skill-memory-meditation-report` skill. The same theming, anti-homogenisation, Universal Contrast, light/dark, responsive-nav, PDF high-contrast print theme, clickable TOC, headless-Chrome render, filename-pairing rules, content-minimum requirements (level-driven per `comprehensiveness`), graceful PDF-degradation contracts, Report Comprehensiveness — No Information Loss contract, and Option Comparison Research mode all apply unchanged in Quick mode. Only runs when verdict from step 10 was `PASS` or `PASS_WITH_ADVISORIES`; never runs on `ESCALATE`.

### Step 12b — Write Process Retrospective (NOT SKIPPED)

Identical to Research. Always written, including on `ESCALATE`.

### Step 13 — Return to Calling Agent

Identical to Research: working directory path, `facets.md`, `consolidation.md` text + path, `retrospective-{ts}.md` path, report HTML+PDF pair (when generated), every `review-pre-report-*-iter-*.md` written by the review cycle. On `ESCALATE` return everything except report paths, plus a structured summary of unresolved `MUST_FIX` findings.

## Quick Mode Child Protocol — 6-Step (Recursive, depth 1 through `maxDepth - 1`)

Each child agent at depth < `maxDepth` follows this simpler protocol.

```
1. Pre-derive 3 child subfocuses upfront (no prior research):
   Each must be narrower than this agent's subfocus, distinct from its siblings,
   and non-overlapping with the entries in facets.md. Sibling-aware only —
   Quick mode does NOT consult facet-registry.yml (the registry does not exist
   in Quick mode).

2. If confirmDeepFacets requires confirmation at this depth (depth_2_only at
   depth 1, OR all_levels at depth 1 or depth 2):
     - Write pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml with the
       proposed 3 children (same schema as Research-mode Phase C; see the
       canonical Deep confirmation flow in the /crux-meditate command).
     - Poll for the matching confirmed-facets-...-{ts}.yml.
     - Apply per-child decisions (confirmed / modified / regenerate;
       regenerations capped at 3 per child).
   Only after all 3 children are confirmed, proceed to step 3.

3. Spawn 3 children at depth+1 in parallel with meditateMode: "quick".
   Each child receives meditateMode, workingDir, branchNumber, maxDepth,
   parentSubfocus, subfocus, subfocusSlug, subfocusIndex, siblingFacets, theming,
   comprehensiveness (propagated unchanged — MUST be present; child aborts with
   "`comprehensiveness:` payload required; missing from spawn prompt — caller
   misconfigured" if missing), modelStrategy (propagated unchanged — MUST be
   present; child aborts with the canonical error if missing), confirmDeepFacets
   (propagated unchanged), and ensembleModel (if present — propagated unchanged
   from this agent's own ensembleModel; descendants of a `per_branch` branch all
   inherit the SAME ensembleModel that was assigned at the depth-0 → depth-1
   dispatch point). When ensembleModel is set, pass model: ensembleModel on the
   Task tool invocation.

4. While children run, do this agent's own memory-query and expansion in
   parallel (Quick mode trades depth-first rigor for elapsed-time speed).

5. Wait for all 3 child files via prefix-glob
   branch-{N}-depth-{D+1}-sub-{S}-*.md. If a child's citations are missing or
   unresolvable, log a warning and proceed — do NOT respawn.

6. Aggregate children + own expansion into a single output file:
   branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md
   (no rewrite — straight aggregation under ## Child Insights with
   `[child: branch-N-depth-D-sub-S]` provenance markers)
```

**Leaf depth (deepest = `maxDepth`, Quick mode)**: query memories, expand, write the leaf file `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}.md`. Citations are still required in the file body and `## Citations` section, but there is no parent respawn enforcement (warn-only). **Comprehensiveness honouring in Quick leaf depth**: at `comprehensiveness.level ∈ {detailed, exhaustive}` (`depth3_leaf_inclusion = verbatim_quotes`), leaf agents MUST include verbatim quoted passages from cited sources in their `## Discoveries` section (same as Research mode). The `section_length_budget_tokens.per_facet` cap applies. Citation validation remains `warn_only` at every level — the parent does NOT respawn on citation failure in Quick mode regardless of comprehensiveness level (K7 mode-driven rule).

## Output File Format (Quick branch files)

Identical frontmatter to Research branch files except `mode: "quick"`. See the `crux-skill-memory-meditation-research` skill for the full frontmatter schema.

Body sections (mandatory in Quick mode):
- `## Subfocus Rationale` — why this narrowing was chosen
- `## Discoveries` — key findings from memory queries and research
- `## Connections` — patterns, relationships, non-obvious links
- `## Child Subfocuses` — the 3 narrower subfocuses derived upfront in step 1
- `## Child Insights` — aggregated from child output files in step 6 (straight aggregation with `[child: branch-N-depth-D-sub-S]` provenance markers — NOT a rewrite)
- `## Contradictions` — contradictions surfaced between this depth's findings and the children's
- `## Summary` — concise distillation for parent consumption
- `## Citations` — every source backing every claim. **Mandatory in Quick mode**; parent validates best-effort and surfaces gaps as warnings rather than re-spawning.

## Citations Protocol (Quick Mode — Warn-Only)

Inline citation markers are the same vocabulary as Research (`[memory: ...]`, `[file: ...]`, `[web: ...]`, `[chat: ...]`, `[child: ...]`). Every output file requires a `## Citations` section.

**Validation rule — Quick mode**: parents log warnings for missing or unresolvable citations and proceed (no respawn). The eventual report's executive summary must include a "Citation gaps" callout listing every uncited finding when this happens.

Quick mode does NOT maintain `citations-index.yml` — citation tracking is per-file only.

## Quick vs Research Differences (Quick Column)

| Aspect | Quick (this skill) |
|--------|-------------------|
| Recursion order | Pre-derived: parent derives all 3 child subfocuses upfront, no prior research required |
| Facet uniqueness | Local sibling-aware only (read `facets.md` to avoid sibling overlap) |
| Citations | Mandatory; inline markers + `## Citations` section required, but parent validates best-effort and surfaces gaps as warnings rather than re-spawning |
| Bottom-up incorporation | Parent appends `## Child Insights` section aggregating children (no rewrite) |
| Peer review | None |
| Consolidation inputs | `branch-*` files only |
| Coordination files | `facets.md` only |

For the Research column, see the `crux-skill-memory-meditation-research` skill.

## Cross-Skill References

- `crux-skill-memory-meditation-coordination` — filename grammar, polling rules, Branch & Leaf Index template
- `crux-skill-memory-meditation-review` — adversarial review contract (step 10); Quick relaxations applied
- `crux-skill-memory-meditation-report` — report generation contract (step 12)
- `crux-skill-memory-meditation-research` — Research column of differences table + shared output schema reference + K10c rubric (same rubric; Quick uses warn-only citation regime)
