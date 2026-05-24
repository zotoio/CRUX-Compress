# Frozen Surface — Meditate Richness + Init-Time Suggestions Spec (20260523)

> **Purpose**: This is the authoritative freeze line for **only the
> portion of the `/crux-meditate` contract surface that
> `spec-meditate-richness-20260523.md` will modify**. Subsequent
> subtasks (02 architecture-design, 03 coordinator-gates, 04 agent
> payload + scouting, 05 report contract, 06 evals, 07 docs-sync,
> 08 CRUX mirrors, 09 integrity review) diff post-change artefacts
> against this single contract.
>
> Each contract item is back-traceable to a current-source line range
> in the repo at git HEAD on 2026-05-23. Where the sibling spec
> `specs/20260517-meditate-agent-skill-decomposition/`'s freeze
> already covers a contract item, this document **cites** that freeze
> by section number rather than restating. New verbatim capture is
> only added for surfaces not covered there with sufficient
> granularity.
>
> **Pre-decomposition source files** (current truth at HEAD on 2026-05-23):
> - `.cursor/commands/crux-meditate.md` (1493 lines)
> - `.cursor/agents/crux-cursor-memory-manager.md` (946 lines)
> - `evals/test_q_meditate.py` (240 lines)
> - `evals/sdk/tests/q-meditate.test.ts` (357 lines)
>
> **Post-decomposition target files** (per
> `specs/20260517-meditate-agent-skill-decomposition/`'s subtask 02
> architecture design — these DO NOT EXIST on disk yet; the
> 20260517 spec is mid-flight):
> - `.cursor/agents/crux-cursor-meditation-guide.md`
> - `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md`
> - `.cursor/skills/crux-skill-memory-meditation-quick/SKILL.md`
> - `.cursor/skills/crux-skill-memory-meditation-ensemble/SKILL.md`
> - `.cursor/skills/crux-skill-memory-meditation-review/SKILL.md`
> - `.cursor/skills/crux-skill-memory-meditation-report/SKILL.md`
> - `.cursor/skills/crux-skill-memory-meditation-coordination/SKILL.md`
> - thinned `.cursor/commands/crux-meditate.md`
>
> **Sibling freeze cited throughout this document**:
> `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260517.md`
> (referred to below as *20260517 freeze §N*).

---

## 1. Scope of this freeze — what IS and what is NOT covered

### IS covered (the 14 items in subtask 01's "Scope — items to freeze")

1. Calling-agent gate ordering (4-gate pre-spawn sequence + mid-flow Facet Confirmation).
2. Existing facet-confirmation `needs_user_input` schema (`facets-pending-{ts}.yml` + `Q-Confirm-1` + `Q-Confirm-2`).
3. Report-generation contract minima (≥4 charts, ≥3 infographics, ≥1 calculator).
4. Per-branch / depth-3 / peer-review surfacing in the report today.
5. Anti-Homogenisation Rules → cite 20260517 freeze §6.2.
6. Universal Contrast block → cite 20260517 freeze §6.3.
7. Subject-Matter Focus rule → cite 20260517 freeze §8.
8. Adversarial review 11-dimension list → cite 20260517 freeze §4.6.
9. Citation discipline → cite 20260517 freeze §5.5.
10. Retrospective always-written rule → cite 20260517 freeze §5.7.
11. Branch & Leaf Index template → cite 20260517 freeze §5.8.
12. Pattern A vs Pattern B boundaries → cite 20260517 freeze §3.
13. Cost-ack expansion variant (`Q-Cost-Acknowledgment-Expansion`) → cite 20260517 freeze §2.3 + reproduce here verbatim because the spec replaces it.
14. Existing eval coverage in `evals/test_q_meditate.py` and `evals/sdk/tests/q-meditate.test.ts`.

### Is NOT covered (deliberately out of scope for this spec)

- The Modes Inventory (Research/Quick/Ensemble selection logic) — unchanged by this spec; 20260517 freeze §1 is sufficient.
- Theme Preflight Q1–Q5 prompt prose — unchanged by this spec; 20260517 freeze §2.4 covers it.
- `confirmDeepFacets` deep-YAML escalation schema (`pending-facets-*.yml` / `confirmed-facets-*.yml`) — unchanged by this spec; 20260517 freeze §2.7 covers it.
- Subagent Phases A–G and Quick 6-step protocol — unchanged by this spec apart from the new `comprehensiveness:` propagation field (K5) and the new `init-suggestions-{ts}.yml` write (K6); 20260517 freeze §4.1 / §4.3 covers the existing protocols.
- Coordination Conventions / artefact filename table / placeholders / prefix-glob polling — unchanged; 20260517 freeze §5.1 / §5.2 / §5.3 covers it.
- Ensemble Aggregation function (§4.5) and Ensemble Aggregation Report extras (§6.7) — unchanged apart from K10's layered finalisation-enhancement reflection step; 20260517 freeze §4.5 / §6.7 covers the existing contract.
- The Headless Chrome → Chromium degradation chain (§6.6) — unchanged.
- The Light/Dark + Print TOC + responsive nav rules (§6.4) — unchanged.
- The Process Retrospective template (§5.7) — unchanged.
- Continuation menu prompt prose (§7.1–§7.5) — extended (K10c surfaces unchosen-enhancement + queued-expensive options) but the existing menu structure is preserved.
- Subagent contracts on `crux-cursor-memory-manager.md` outside Meditate Mode (Dream / REM / Recall / Remember / Forget) — out of scope.
- Cross-repo touchpoints (§9) — install.py / dist-zip / version-bump / AGENTS.md / README.md / docs/crux-memories.md / web — out of scope at the source level; docs-sync touches are handled by subtask 07, not this freeze.

---

## 2. Source-of-truth map (Two-column concordance)

Following the shape of 20260517 freeze §10. Each row identifies the
current pre-decomposition location AND the post-decomposition
destination per
`meditate-decomp-architecture-design-20260517.md` §3.

| # | Contract item touched by this spec | Pre-decomp location (file:lines today) | Post-decomp destination (per 20260517 §3) |
|---|---|---|---|
| 1 | Calling-agent gate ordering — 4-gate pre-spawn + mid-flow Facet Confirmation | `.cursor/commands/crux-meditate.md:30-36` (Pattern-B preamble) + `:55-105` (Depth Selection) + `:106-189` (Cost Ack + Expansion) + `:191-293` (Theme Preflight) + `:295-439` (Facet Confirmation) | `command` (verbatim, all four gates) — per 20260517 §3.2 |
| 2 | `Q-Cost-Acknowledgment` prompt prose (single-model variant) | `.cursor/commands/crux-meditate.md:123-166` (prompt + ensemble variant + options) | `command` (verbatim) — per 20260517 §3.2 |
| 3 | `Q-Cost-Acknowledgment` ensemble first-paragraph replacement | `.cursor/commands/crux-meditate.md:144-154` | `command` (verbatim, ensemble branch) — per 20260517 §3.2 |
| 4 | `Q-Cost-Acknowledgment` behaviour rules + non-interactive abort | `.cursor/commands/crux-meditate.md:169-189` | `command` (verbatim) — per 20260517 §3.2 |
| 5 | `Q-Cost-Acknowledgment-Expansion` prompt + options + "keep deep-confirm setting?" follow-up | `.cursor/commands/crux-meditate.md:174-189` (prompt + options inside the expansion bullet) + `:433-439` (Re-spawn semantics with `confirmDeepFacets` reuse + follow-up) | `command` (verbatim, expansion branch) — per 20260517 §3.2 |
| 6 | `facets-pending-{ts}.yml` artefact (filename + write semantics) | `.cursor/commands/crux-meditate.md:446` (filename row) + `:309` (write-during-Q-Confirm-1) + `:361` (delete after confirmation) | `skill:coordination` (filename row) + `command` (Pattern-B trigger) — per 20260517 §5.1 / §3.2 |
| 7 | `Q-Confirm-1` prompt + 5-option decision set | `.cursor/commands/crux-meditate.md:311-330` (prompt body lines 315-323; options lines 325-330) | `command` (verbatim) + `skill:research`/`skill:quick` (reference the option set) — per 20260517 §3.2 |
| 8 | `Q-Confirm-2` prompt + 3-enum decision set + default | `.cursor/commands/crux-meditate.md:338-359` (prompt body lines 342-353; options lines 357-359) | `command` (verbatim) + `skill:research`/`skill:quick` (mirror) — per 20260517 §3.2 |
| 9 | Report-generation contract minima (≥4 charts, ≥3 infographics, ≥1 calculator) | `.cursor/commands/crux-meditate.md:1068-1070` (charts) + `:1119-1121` (infographics) + `:1137-1146` (calculator + "every calculator must include …") + `:1066` ("standard content minimums (≥4 charts, ≥3 infographics, ≥1 calculator)" in Option Comparison block) + `:1170-1172` (filterable tables + tooltips alongside the minima) | `skill:report` (verbatim) + `command` becomes a one-paragraph pointer — per 20260517 §3.6 |
| 10 | Per-branch / depth-3 / peer-review surfacing today (consolidation-driven + selective branch re-reading) | `.cursor/commands/crux-meditate.md:1000` ("Per-facet sections — each confirmed facet becomes one or more report sections") + `:1001` ("Quality review section (Research mode)") + `:1008` ("all 39 branch files, peer reviews, and consolidation") + `:1016` (input-coverage verification) + `.cursor/agents/crux-cursor-memory-manager.md:411-420` (consolidation step 8 reads 3 depth-1 + 3 peer-review + citations-index; Quick step 8 reads 3 depth-1 only at `:457`) | `skill:report` (verbatim) + `skill:research`/`skill:quick` (mirror) — per 20260517 §3.6 + §3.4 |
| 11 | Anti-Homogenisation Rules block | `.cursor/commands/crux-meditate.md:197-209` (pre-flight context) + `:1174-1194` (canonical block in Report Generation) | `skill:report` (verbatim) + `command` (one-paragraph pointer) — per 20260517 §3.6 |
| 12 | Universal Contrast (WCAG) block | `.cursor/commands/crux-meditate.md:1205-1231` | `skill:report` (verbatim) — per 20260517 §3.6 |
| 13 | Subject-Matter Focus rule | `.cursor/commands/crux-meditate.md:878-898` (canonical) + `.cursor/agents/crux-cursor-memory-manager.md:837` (design-principle restatement) | `skill:report` (verbatim) + `skill:research`/`skill:quick`/`skill:review` (mirror) — per 20260517 §3.8 |
| 14 | Adversarial review 11-dimension list | `.cursor/commands/crux-meditate.md:759-771` (dimensions) + `:773-779` (severity) + `:781-799` (iteration loop) + `:801-816` (MUST_FIX `needs_user_input` with mandatory `context`) + `.cursor/agents/crux-cursor-memory-manager.md:424-428` (depth-0 step 10) + `:833` (design-principle restatement) | `skill:review` (verbatim) + `agent` (mode-router pointer) — per 20260517 §3.4 |
| 15 | Citation discipline (inline markers, `## Citations` per-file, citations-index, validation) | `.cursor/agents/crux-cursor-memory-manager.md:655-690` (canonical) + `.cursor/commands/crux-meditate.md:1003` (Citations section requirement in report) | `skill:research` (Research strict variant) + `skill:quick` (warn-only variant) + `skill:coordination` (filename row only) — per 20260517 §3.5 |
| 16 | Retrospective always-written rule | `.cursor/commands/crux-meditate.md:900-967` (template + sections) + `.cursor/agents/crux-cursor-memory-manager.md:444` (depth-0 step 12b) | `skill:coordination` (verbatim) + `agent` (mode-router pointer at step 12b) — per 20260517 §3.5 |
| 17 | Branch & Leaf Index template (`## Top-level artifacts` section in particular) | `.cursor/commands/crux-meditate.md:671-735` (canonical) + `.cursor/agents/crux-cursor-memory-manager.md:422` (depth-0 step 9) + `:430` (post-review refresh, step 11) | `skill:coordination` (verbatim) + `command`/`agent` (pointer) — per 20260517 §3.5 |
| 18 | Pattern A vs Pattern B boundaries (subagents NEVER call `AskQuestion`; calling agent owns every prompt) | `.cursor/commands/crux-meditate.md:34-36` (preamble) + `.cursor/agents/crux-cursor-memory-manager.md:17-46` (User Input Escalation block) + `:302-307` (Meditate-mode reaffirmation) | `agent` (Critical Rules — verbatim) + `command` (Pattern-B preamble retained) + every skill cites by reference — per 20260517 §3.3 |
| 19 | `crux-cursor-memory-manager` Meditate-mode depth-0 manager steps 1–13 (Research) | `.cursor/agents/crux-cursor-memory-manager.md:360-446` (verbatim) | `skill:research` (verbatim) + `agent` (mode-router lists step numbers + 1-paragraph summary per step) — per 20260517 §3.4 |
| 20 | `evals/test_q_meditate.py` test classes | `evals/test_q_meditate.py:13-240` (full file; 8 test classes) | unchanged location — `evals/` is repo-stable across both pre- and post-decomp targets |
| 21 | `evals/sdk/tests/q-meditate.test.ts` test suites Q1–Q3 | `evals/sdk/tests/q-meditate.test.ts:31-357` (full file; 3 describe blocks Q1–Q3) | unchanged location — `evals/sdk/tests/` is repo-stable across both pre- and post-decomp targets |

---

## 3. Calling-agent gate ordering — verbatim freeze

### 3.1 Current 4-gate pre-spawn sequence

**Pre-spawn flow** (verbatim — `.cursor/commands/crux-meditate.md:36`):

> Four mandatory pre-spawn user gates — **Depth Selection**, **Cost &
> Scope Acknowledgment**, **Theme Preflight**, and (mid-flow) **Facet
> Confirmation** — fire before the subagent tree spawns; see the
> dedicated sections below.

The sequence in execution order is:

1. **Q-Depth-Selection** — Pattern A — `.cursor/commands/crux-meditate.md:55-105`.
2. **Q-Cost-Acknowledgment** — Pattern A — `.cursor/commands/crux-meditate.md:106-189` (incl. ensemble variant + Expansion variant + behaviour rules).
3. **Theme Preflight Q1–Q5** (with Q1b repo-scan confirm) — Pattern A — `.cursor/commands/crux-meditate.md:191-293`.
4. **Facet Confirmation `Q-Confirm-1` + `Q-Confirm-2`** — Pattern B (mid-flow; escalated from inside the depth-0 subagent after step 4 facet derivation) — `.cursor/commands/crux-meditate.md:295-361`.

This is the **target of K2's merge** — the new spec merges richness
selection into gate (2) (renaming it
`Q-Cost-and-Richness-Acknowledgment`) and folds the
init-suggestions confirmation into gate (4)'s combined Pattern-B
prompt. The new spec does **not** introduce a standalone
`Q-Comprehensiveness` gate; the gate ordering stays at 4 logical
slots even after the merge (Depth Selection → merged
Cost-and-Richness → Theme Preflight → combined
Facet/Sections/Visualisations/Focus-Areas confirmation).

### 3.2 `Q-Cost-Acknowledgment` — single-model prompt (verbatim)

Source: `.cursor/commands/crux-meditate.md:127-142`.

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

### 3.3 `Q-Cost-Acknowledgment` — ensemble variant first-paragraph replacement (verbatim)

Source: `.cursor/commands/crux-meditate.md:144-154`.

> When `ensembleMode` is true, replace the first paragraph with:

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

### 3.4 `Q-Cost-Acknowledgment` — options (verbatim)

Source: `.cursor/commands/crux-meditate.md:158-166`.

- `proceed` — Yes, this is a high-value strategic problem; proceed in the currently-selected mode (`Research` or `Quick`, depth {maxDepth}, with or without Ensemble)
- `switch_to_quick` — Proceed but switch to Quick mode (~{quickCount} agents at depth {maxDepth}, faster, no peer review). **Only offered when current mode = Research.**
- `switch_to_research` — Proceed but switch to Research mode (~{researchCount} agents at depth {maxDepth}, peer-reviewed, slower). **Only offered when current mode = Quick.**
- `switch_to_ensemble` — Proceed but enable Ensemble mode (~{N×perModelCount + 1} agents across {N} model families + cross-model aggregation). **Only offered when `ensembleMode` is false.** Read `cruxMemories.meditate.modelPool` to compute the agent count.
- `switch_to_single` — Cancel Ensemble, run on a single model instead (~{perModelCount} agents). **Only offered when `ensembleMode` is true.**
- `cancel` — Cancel — I'll use a different approach

### 3.5 `Q-Cost-Acknowledgment` — behaviour rules (verbatim)

Source: `.cursor/commands/crux-meditate.md:169-174` + `:189` (non-interactive).

- **Always run on the first invocation** in a session, regardless of arguments. Depth Selection runs first, then Cost Acknowledgment.
- **Mode swaps**: if the user picks `switch_to_quick` or `switch_to_research`, update the active `meditateMode` for the rest of this invocation and proceed to Theme Preflight; do not re-ask Q-Cost-Acknowledgment or Q-Depth-Selection. If the user picks `switch_to_ensemble`, set `ensembleMode: true` and proceed. If the user picks `switch_to_single`, set `ensembleMode: false` and proceed.
- **Cancel**: respond with a short note acknowledging the cancellation and stop. Do not spawn anything, do not run Theme Preflight, do not create the working directory.
- **Expansion-direction continuation** (calling agent step 12 — when the user picks an expansion option after a previous meditation): run a **shortened** version of this acknowledgment (`Q-Cost-Acknowledgment-Expansion`). The mode-swap and depth options are **not** re-offered (both persist across expansions); the user can `cancel` and re-invoke `/crux-meditate` if they want to change mode or depth.

**Non-interactive abort rule** (verbatim) — `.cursor/commands/crux-meditate.md:189`:

> - **Non-interactive sessions** (e.g. CI): if `askQuestion` cannot be answered, abort with a clear error explaining the cost-acknowledgment requirement. Never default to `proceed` silently — the safeguard exists precisely because the cost is non-trivial.

**Why this matters for the new spec** — K2 explicitly preserves the
non-interactive abort rule on the merged
`Q-Cost-and-Richness-Acknowledgment` gate; richness gets a
non-interactive default of `default`, but `proceed` is NOT
auto-selected. The cost-ack safeguard remains a hard abort in CI.

### 3.6 Cross-references to 20260517 freeze for the OTHER gates

| Gate | This spec's touch reason | Already covered in |
|------|---|---|
| `Q-Depth-Selection` (Pattern A — gate 1) | Unchanged; spec preserves verbatim because the merged gate-2 prompt continues to display the depth value (Sub-Q1 of the combined askQuestion shows depth row from Q-Depth-Selection's result). | 20260517 freeze §2.1 |
| Theme Preflight Q1–Q5 (Pattern A — gate 3) | Unchanged; spec preserves the existing `theming` payload propagation pattern that K5's new `comprehensiveness:` payload mirrors. | 20260517 freeze §2.4 |
| `confirmDeepFacets` deep-YAML escalation (Pattern B — file-based) | Unchanged; the new K6 set-once-per-invocation rule for richness mirrors the existing `confirmDeepFacets` propagation pattern. | 20260517 freeze §2.7 |

---

## 4. Existing facet-confirmation `needs_user_input` schema — verbatim freeze

### 4.1 `facets-pending-{ts}.yml` shape

This is the schema **as the depth-0 subagent writes it today** before
escalating via Pattern B. The new spec extends this with sections /
visualisations / additional-focus-areas (per K4) — the freeze
records the pre-extension shape so subtasks 03 + 04 can patch
surgically.

**Filename pattern** (`.cursor/commands/crux-meditate.md:446` + 20260517 freeze §5.1):

| Artefact | Filename pattern | Notes |
|----------|------------------|-------|
| Top-level facets (initial, pre-confirmation) | `facets-pending-{ts}.yml` | Deleted after the user confirms via Q-Confirm-1 |
| Top-level facets (final, post-confirmation) | `facets.md` | Single navigational entry point; updated post-consolidation with the Branch & Leaf Index |

**Write semantics** (verbatim) — `.cursor/commands/crux-meditate.md:309`:

> 1. The depth-0 subagent derives 3 top-level facets per its normal logic, writes them to a draft file `facets-pending-{ts}.yml` in the working directory, and returns a `needs_user_input` block to the calling agent containing the proposed facets verbatim.

**Delete semantics** (verbatim) — `.cursor/commands/crux-meditate.md:361`:

> 7. Calling agent resumes the subagent with the confirmed facets plus the `confirmDeepFacets` enum value. Subagent appends the confirmed facets to `facet-registry.yml` (Research mode), promotes the draft to the final `facets.md`, deletes `facets-pending-{ts}.yml`, and proceeds to step 5 of the workflow (spawn explorers).

**Per-spec observation**: the on-disk YAML schema for
`facets-pending-{ts}.yml` is **not** explicitly specified verbatim
in the command file (only the `pending-facets-*.yml` deep-facet
escalation schema is — at `.cursor/commands/crux-meditate.md:376-397`).
The `needs_user_input` block returned by the subagent contains
"the proposed facets verbatim" (`:309`). Subtask 02 of this spec
must explicitly define the extended schema (sections /
visualisations / additional-focus-areas blocks) so subtask 03's
patch is unambiguous.

### 4.2 `Q-Confirm-1` — prompt body + options (verbatim)

Source: `.cursor/commands/crux-meditate.md:311-330`.

**Prompt body** (`:313-323` — verbatim, included after the 3 facets):

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

**Options** (`:325-330` — verbatim, single-select):

- `confirm_all` — proceed with all 3 facets unchanged
- `modify_one` — change one facet (follow-up text input)
- `modify_multiple` — change multiple facets (follow-up text input)
- `regenerate` — discard these 3 and ask the subagent to derive a different set
- `cancel` — abort the meditation entirely

**Resume semantics** (verbatim) — `.cursor/commands/crux-meditate.md:332-336`:

- If `regenerate` → calling agent resumes the subagent with `regenerate_facets: true` plus the previous `facets-pending-{ts}.yml` path; the subagent reads the rejected set, derives a different one, and re-escalates. Loop, **capped at 3 regeneration attempts**.
- If `modify_one` or `modify_multiple` → calling agent collects the replacement text(s) via a free-text follow-up, then resumes the subagent with `facet_overrides: [{ index: N, new_subfocus: "...", new_slug: "..." (optional) }, ...]`. The subagent applies the overrides, re-derives slugs/citations for any modified facet, and proceeds to Q-Confirm-2 below.
- If `confirm_all` → calling agent proceeds directly to Q-Confirm-2.

### 4.3 `Q-Confirm-2` — prompt body + options (verbatim)

Source: `.cursor/commands/crux-meditate.md:338-359`.

**Prompt body** (`:342-353` — verbatim):

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

**Options** (`:357-359` — verbatim, single-select):

- `none` (default — preselected) — auto-derive at depth 2 and depth 3
- `depth_2_only` — pause for confirmation at depth 2; auto-derive at depth 3
- `all_levels` — pause for confirmation at depth 2 and depth 3

### 4.4 Combined askQuestion shape today

Today the calling agent runs `Q-Confirm-1` and `Q-Confirm-2` as
**two sequential `askQuestion` calls** (see calling-agent step
ordering in `.cursor/commands/crux-meditate.md:307-361`). They are
both Pattern B (escalated from inside the depth-0 subagent via the
single `needs_user_input` block emitted after step 4 facet
derivation — see 20260517 freeze §3 Pattern B table at `:386-388`).

**`needs_user_input` envelope** — the canonical schema lives in
`AGENTS.md` (the project-wide rule) and is restated in
`.cursor/agents/crux-cursor-memory-manager.md:17-46` (User Input
Escalation block). The freeze reference is 20260517 freeze §3.

**Why this matters for the new spec** — K4 + Requirement 5 fold
`Q-Confirm-1` + `Q-Confirm-2` + the new init-suggestion
confirmation (sections / visualisations / 4-mode focus-area opt-in)
into a **single combined askQuestion** to avoid a multi-round-trip
prompt sequence. Subtask 02 must produce the exact merged-prompt
template; subtask 03 implements; the freeze here records the
pre-merge shape so the diff is auditable.

---

## 5. Report-generation contract minima — verbatim freeze

The new spec (K1 + K5 + Requirement 3) replaces these fixed minima
with the level-driven `comprehensiveness.minima` payload mapping
table. The freeze records the **current** hard-coded values so
`compact` can reproduce them exactly per K1's backwards-compat
anchor.

### 5.1 Chart minima — `≥4 distinct chart types`

Source: `.cursor/commands/crux-meditate.md:1068-1070`.

> ##### Visualizations (Chart.js + D3.js, loaded from CDN)
>
> Pick **at least 4 distinct chart types in total**, choosing those that fit the data the meditation actually surfaced AND the kind of facet being illustrated. The minimum can be met by any combination of **Chart.js** (standard chart types, fastest to author) and **D3.js** (advanced or facet-specific interactive visualizations). Do not fabricate data — if the meditation lacks the data a particular chart type needs, skip it and pick another.

Also surfaced in `.cursor/agents/crux-cursor-memory-manager.md:439`:

> …**at least 4 distinct chart visualizations** (Chart.js + D3.js — pick the chart type per facet, e.g. tree/sunburst for hierarchy, sankey for flow, force-directed graph for relationships, choropleth for geo, parallel coordinates for multi-dimensional comparison)…

### 5.2 Infographic minima — `≥3 distinct infographic types`

Source: `.cursor/commands/crux-meditate.md:1119-1121`.

> ##### Infographics (HTML/CSS/SVG, no external library)
>
> Pick **at least 3 distinct infographic types** from the list below — these convey structure visually rather than encoding numbers. Build them with hand-rolled HTML + CSS + inline SVG (no extra libraries):

Also surfaced in `.cursor/agents/crux-cursor-memory-manager.md:439`:

> …**at least 3 distinct hand-rolled HTML/CSS/SVG infographics**…

### 5.3 Calculator minima — `≥1 interactive calculator if applicable`

Source: `.cursor/commands/crux-meditate.md:1137`:

> ##### Interactive elements
>
> - **Interactive calculators** — at least one JavaScript-driven calculator if the meditation surfaces any quantifiable trade-off (input fields, recompute on change, formatted result panel). Infer what calculation would be useful from the meditation content.

The full `≥3-5 pre-computed what-if scenarios` static-fallback
contract is at `:1139-1168`; the verbatim text is preserved in
20260517 freeze §6.5 (Calculator static fallback subsection).

Also surfaced in `.cursor/agents/crux-cursor-memory-manager.md:439`:

> …at least one **interactive calculator** if the meditation surfaces a quantifiable trade-off…

### 5.4 "Standard content minimums" canonical phrase (cross-referenced)

The exact phrase used in `Option Comparison Research Reporting`
that the new spec must update — `.cursor/commands/crux-meditate.md:1066`:

> When option-comparison research activates, the standard content minimums (≥4 charts, ≥3 infographics, ≥1 calculator) still apply independently — the comparison-specific elements above are **additional** to those minimums, not replacements. The quadrant visualization counts toward the ≥4 chart minimum; the feature matrix and differentiators section count toward the ≥3 infographic minimum; a TCO/ROI calculator (if the comparison involves cost) counts toward the ≥1 calculator minimum.

This is the line subtask 05 must replace with the level-driven
mapping (`comprehensiveness.minima.charts.count`,
`comprehensiveness.minima.infographics.count`,
`comprehensiveness.minima.calculators.count`) while preserving the
"additive on top of comparison-specific elements" semantics.

Also surfaced in the Ensemble Aggregation Report — 20260517
freeze §6.7 paraphrases as:

> All standard content minimums (≥4 charts, ≥3 infographics, ≥1 calculator, filterable tables, light/dark mode, PDF degradation) still apply.

Live source: `.cursor/commands/crux-meditate.md:1474` — the
heading "Ensemble-specific visualizations (in addition to the
standard minimums)" embeds the same invariant by explicitly
positioning ensemble visualisations as additive on top of the
per-tree standard minimums. The new spec must update this
Ensemble Aggregation surface too (because ensemble inherits the
per-tree `comprehensiveness.level` value per K5).

### 5.5 Where the minima live in the report-generation flow

The minima are enforced **inside the report-generation step** —
i.e. calling-agent steps 8 (subagent-block report generation) and
12 (depth-0 manager's mandatory report generation). The agent
file's depth-0 step 12 (`.cursor/agents/crux-cursor-memory-manager.md:432-442`)
delegates by reference to `.cursor/commands/crux-meditate.md` →
**Report Generation — MANDATORY**.

Today the enforcement is hard-coded into the report skill's prose
contract. The new spec injects the structured `comprehensiveness`
payload at depth-0 spawn time (per K5) and the report skill reads
the per-level numeric values from `comprehensiveness.minima.*`.

---

## 6. Per-branch / depth-3 / peer-review surfacing today — verbatim freeze

### 6.1 Today's report-rendering rule — primarily consolidation-driven

The report is rendered today primarily off `consolidation.md` plus
selective re-reading of branch files. The exact lines that govern
this:

**Per-facet section rule** — `.cursor/commands/crux-meditate.md:1000`:

> - **Per-facet sections** — each confirmed facet becomes one or more report sections using its **facet title** as the heading (e.g. "Data Capture and CRUX-Compressed Storage", not "Branch 1"), with subheadings derived from subfocus descriptions for deeper findings. Organize content by the subject matter's natural structure, not by the tree's physical branch/depth layout.

**Quality review section (Research mode)** —
`.cursor/commands/crux-meditate.md:1001`:

> - **Quality review section** (Research mode) — cross-cutting reinforcements, contradictions, gaps identified during independent review; one card per review file. Present findings as substantive analysis, not as "peer reviewer said X" — the content matters, not the process actor.

**"All 39 branch files" rule (today's input-coverage statement)** —
`.cursor/commands/crux-meditate.md:1008`:

> The report is the **final deliverable** of the meditation. Every important finding, data point, comparison, citation, and insight discovered across the entire research tree (all 39 branch files, peer reviews, and consolidation) must be faithfully represented in the HTML/PDF report. The report is NOT a summary of the consolidation — it is the fully-rendered, richly-visualized presentation of **all substantive research output**.

**Input coverage verification rule** —
`.cursor/commands/crux-meditate.md:1016`:

> - **Input coverage verification**: Before declaring the report complete, enumerate the key findings from each branch file's `## Discoveries` and `## Summary` sections and verify each has a corresponding presentation element (chart, table, infographic, prose section, or calculator) in the report. Log any gap and fill it.

**Anti-sparseness escalation** — `.cursor/commands/crux-meditate.md:1018`:

> **Anti-sparseness escalation**: If the generated report contains fewer distinct data points or findings than the branch files collectively surfaced, the report fails its own completeness check. Re-read the branch files and add the missing content before the PDF render.

**Working-directory framing** —
`.cursor/agents/crux-cursor-memory-manager.md:311`:

> **Working directory**: All artefacts live under `meditations/{yyyymmdd}-{topic-slug}/`. Each branch fans out into 3 subfocuses at depth 2, and each of those fans out into 3 at depth 3 — up to 39 branch output files plus `facets.md`, `consolidation.md`, peer reviews, adversarial review iterations, and the paired HTML + PDF reports. See **Coordination Conventions** below for the canonical filename + polling reference, and **Working directory structure** further down for the full tree.

### 6.2 Consolidation step inputs (today's per-branch / depth-3 / peer-review reach)

**Research-mode consolidation (step 8)** —
`.cursor/agents/crux-cursor-memory-manager.md:411-420`:

> 8. **Consolidate**: Read all 3 depth-1 branch files **plus** all 3 peer-review files **plus** `citations-index.yml`. Synthesize into `consolidation.md` following the **Subject-Matter Focus** rule in `.cursor/commands/crux-meditate.md` — use facet titles as section headings (never "Branch 1/2/3"), translate `[child: branch-N-depth-D-sub-S]` citations to `[research: {subfocus-slug}]` format, and never reference branches, depths, leaf agents, or other process concepts. Structure:
>    - Key discoveries organized by facet theme (using the confirmed facet titles as section headings)
>    - Cross-cutting connections and emergent themes (referencing topics by name, not by branch number)
>    - Contradictions identified during quality review (presenting the substance, not "surfaced by peer review")
>    - Gaps and open questions (framed as subject-matter gaps, not process gaps)
>    - New evidence and supplementary findings from quality review
>    - Potential directions for further exploration
>    - A unified `## Citations` section that includes every distinct citation referenced anywhere in the meditation, with `[child: ...]` references translated to `[research: {subfocus-slug}]` format
>
>    Write `consolidation.md` to the working directory. Do NOT return to the calling agent yet — steps 9–13 below must run first. Do NOT call `AskQuestion` at any point — the parent agent handles all post-meditation user interaction once you return in step 13.

**Quick-mode consolidation (step 8 substitution)** —
`.cursor/agents/crux-cursor-memory-manager.md:457`:

> - **Step 8** — consolidate from the 3 depth-1 branch files only. No peer-review files to glob, no `citations-index.yml` to merge. Follow the **Subject-Matter Focus** rule (use facet titles as section headings, translate `[child: ...]` citations to `[research: {subfocus-slug}]` format, never reference branches/depths/agents). If any branch surfaced citation gaps (parents in Quick mode warn rather than respawn), include a "Citation gaps" callout in `consolidation.md` listing every uncited finding. **Do NOT return to the calling agent yet** — steps 9–13 below must run first.

**Key observation for this spec** — today the consolidation step
reads ONLY the 3 depth-1 branch files (which themselves have
bottom-up incorporated depth-2 + depth-3 findings via Phase F
rewrite; see 20260517 freeze §4.1 Phase F at line 427). Depth-3
**leaf** material is therefore elided beyond what each depth-1
parent retained in its own rewrite — there is no second pass that
re-reads the depth-3 leaf files separately. Peer-review files reach
the consolidation but only flow to the report through the
"Quality review section" rule above (`:1001`).

This is the exact behaviour the new spec's
`comprehensiveness.depth3_leaf_inclusion` payload field will
control (per K5):
- `"elided"` (legacy / `compact` level) = today's behaviour.
- `"summary"` = each depth-3 leaf contributes a one-paragraph summary.
- `"verbatim_quotes"` = depth-3 leaf material reproduced with full citation.

And `comprehensiveness.peer_review_surfacing` will control whether
peer-review reinforcements / contradictions / gaps stay folded into
consolidation prose (`"consolidation_only"` — today / `compact`) or
get dedicated named report sections (`"named_section"` /
`"per_branch_dedicated"`).

### 6.3 Branch & Leaf Index `## Top-level artifacts` block (today)

This is the section the new spec extends with
`init-suggestions-{ts}.yml` (per K6 — the freeze records the
pre-extension shape).

Source: `.cursor/commands/crux-meditate.md:705-718` (verbatim,
covered also in 20260517 freeze §5.8).

```
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
```

**Where K6 extends this** — the new spec adds an
`[Init suggestions](init-suggestions-{ts}.yml)` line under
"Top-level artifacts" (also adds the new
`[Finalisation enhancements](finalisation-enhancements.yml)` line
under K10c). The 20260517 freeze §5.8 covers the existing template
verbatim; this spec only diffs the "Top-level artifacts" block.

---

## 7. Cross-references to the 20260517 freeze (items 5–13 from subtask 01 scope)

These items are already covered with sufficient granularity by the
20260517 freeze line. This spec **cites** them by section anchor
rather than restating. Subtask 02 (architecture-design) and the
implementation subtasks (03–05) must treat these references as
authoritative.

| # | Subtask 01 scope item | 20260517 freeze section anchor | This spec's touch reason |
|---|---|---|---|
| 5 | Anti-Homogenisation Rules | 20260517 freeze §6.2 (lines 873–895 of that document); live source lines `.cursor/commands/crux-meditate.md:197-209` (pre-flight context) + `:1174-1194` (canonical block) | **Preserve verbatim across every level** (K7 + Requirement 10). No level relaxes this. |
| 6 | Universal Contrast (WCAG-style) block | 20260517 freeze §6.3 (lines 897–918); live source `.cursor/commands/crux-meditate.md:1205-1231` | **Preserve verbatim across every level** (K7 + Requirement 10). `compact` does NOT downgrade contrast. |
| 7 | Subject-Matter Focus rule | 20260517 freeze §8 (lines 1284–1304); live source `.cursor/commands/crux-meditate.md:878-898` + design-principle restatement `.cursor/agents/crux-cursor-memory-manager.md:837` | **Preserve verbatim** (K7). Applies unchanged to `consolidation.md` + HTML/PDF reports at every level. |
| 8 | Adversarial review 11-dimension list | 20260517 freeze §4.6 (lines 528–600); live source `.cursor/commands/crux-meditate.md:737-876` + `.cursor/agents/crux-cursor-memory-manager.md:424-428, :833` | **Extend with 2 new dimensions** (K9 — Dim 12 Comprehensiveness Fidelity + Dim 13 Init-Suggestion Honour + level-conditional expansion of Dim 9). The existing 11 are frozen verbatim. **Dim 13 also triggers respawn protocol** (per K9 + K10b). |
| 9 | Citation discipline | 20260517 freeze §5.5 (lines 705–734); live source `.cursor/agents/crux-cursor-memory-manager.md:655-690` + report `## Citations` requirement at `.cursor/commands/crux-meditate.md:1003` | **Preserve verbatim** (K7 + Requirement 10). Citation density stays **mode-driven** (warn-only in Quick; mandatory in Research). The `comprehensiveness.citation_density` payload field is set by **mode** at every level, with `exhaustive` adding a per-finding-table citation column on top. |
| 10 | Retrospective always-written rule | 20260517 freeze §5.7 (lines 761–787); live source `.cursor/commands/crux-meditate.md:900-967` + `.cursor/agents/crux-cursor-memory-manager.md:444` (step 12b) | **Preserve verbatim** (K7 + Requirement 10). Always written, including on `ESCALATE` — unchanged. |
| 11 | Branch & Leaf Index template (`## Top-level artifacts` subsection in particular) | 20260517 freeze §5.8 (lines 789–855); live source `.cursor/commands/crux-meditate.md:671-735` | **Add 1–2 new top-level artefact links** (`init-suggestions-{ts}.yml` per K6 + `finalisation-enhancements.yml` per K10c). The existing "Top-level artifacts" subsection is reproduced verbatim in §6.3 above for diff clarity. |
| 12 | Pattern A vs Pattern B boundaries | 20260517 freeze §3 (lines 368–397); live source `.cursor/agents/crux-cursor-memory-manager.md:17-46` + `.cursor/commands/crux-meditate.md:34-36` | **Preserve every boundary** (K7 + Requirement 10). New gates (`Q-Cost-and-Richness-Acknowledgment`, combined Pattern-B facet+init-suggestions confirmation, `Q-Finalisation-Enhancements`) are all calling-agent-owned. Subagents NEVER call `AskQuestion`. |
| 13 | `Q-Cost-Acknowledgment-Expansion` prompt + options | 20260517 freeze §2.3 (lines 157–178); live source `.cursor/commands/crux-meditate.md:174-189` (incl. the embedded expansion bullet and prompt at `:176-188`) | **Replace** with the read-only-richness variant of the merged `Q-Cost-and-Richness-Acknowledgment` gate (richness locked per K6 set-once-per-invocation). The existing "keep deep-confirm setting?" follow-up at `:438` is **preserved unchanged**. The expansion variant does NOT offer a "keep richness setting?" follow-up. **See §8 below for the verbatim cost-ack expansion prose** — reproduced here because the spec replaces it. |

---

## 8. Cost-ack expansion variant — verbatim freeze

The new spec (K2 + K6) replaces this prompt with the
read-only-richness variant of the merged
`Q-Cost-and-Richness-Acknowledgment` gate. The existing "keep
deep-confirm setting?" follow-up at `.cursor/commands/crux-meditate.md:438`
is preserved unchanged. Richness is implicitly locked; no
"keep richness setting?" follow-up is offered.

### 8.1 `Q-Cost-Acknowledgment-Expansion` prompt prose (verbatim)

Source: `.cursor/commands/crux-meditate.md:176-188` (embedded inside
the Cost Ack behaviour rule at `:174`).

**Prompt** (verbatim, `:178-184`):

```
Expanding this meditation will spawn a new depth-{maxDepth} research tree
(~{N} additional agents) exploring the selected direction(s). This carries
the same per-meditation cost as the original invocation — a full recursive
tree, adversarial review cycle, and paired HTML + PDF report.

The previous meditation's results are preserved; this expansion produces a separate
report. If you only need a quick follow-up, consider a regular chat prompt instead.
```

**Options** (`:187-188` — verbatim):

- `proceed_expansion` — Yes, spawn the expansion tree
- `cancel` — Cancel — I'll follow up in chat instead

### 8.2 "Keep deep-confirm setting?" follow-up (verbatim)

Source: `.cursor/commands/crux-meditate.md:433-438` (Re-spawn semantics).

> When the user selects an "expansion direction" continuation (calling agent step 12), the new meditation:
>
> - **Always** re-runs the depth-0 facet confirmation.
> - **Reuses** the previous `confirmDeepFacets` enum value by default; the calling agent may offer a one-line "keep deep-confirm setting?" follow-up.

**This follow-up is preserved unchanged by the new spec.** K6
explicitly states: "The existing 'keep deep-confirm setting?'
follow-up is preserved unchanged."

### 8.3 "Mode-swap NOT re-offered on expansion" rule (verbatim)

Source: `.cursor/commands/crux-meditate.md:174` (last sentence of
the Expansion bullet under `#### Behaviour rules`).

> The mode-swap and depth options are **not** re-offered (both persist across expansions); the user can `cancel` and re-invoke `/crux-meditate` if they want to change mode or depth.

The new spec extends this rule transitively: **richness** is also
not re-offered on expansion (per K6 set-once-per-invocation). User
must `cancel` and re-invoke to change richness.

---

## 9. Existing eval coverage inventory

The new spec (K9 + Requirements 12 + 22) requires that **no
existing assertion is deleted**; new assertions are added on top.
The freeze records every existing test class / test function with a
one-line description of what it asserts so subtask 06 can extend
without regression.

### 9.1 `evals/test_q_meditate.py` (Python — 240 lines, 8 test classes, 25 tests)

| Class | Test function | Lines | Asserts |
|-------|---------------|-------|---------|
| `TestMeditateConfigPresence` | `test_meditate_command_in_config` | `:16-23` | `commands.meditate` key present in `.crux/crux-memories.json` |
| `TestMeditateConfigPresence` | `test_meditate_command_file_path` | `:25-32` | `commands.meditate.file == ".cursor/commands/crux-meditate.md"` |
| `TestMeditateConfigPresence` | `test_meditate_command_default` | `:34-41` | `commands.meditate.default == "/crux-meditate"` |
| `TestMeditateConfigPresence` | `test_meditate_command_file_exists` | `:43-47` | `.cursor/commands/crux-meditate.md` is a regular file |
| `TestMeditateCommandDefinition` | `test_has_usage_section` | `:61-63` | Command file contains `## Usage` |
| `TestMeditateCommandDefinition` | `test_supports_no_arguments` | `:65-67` | Contains `no argument` or `/crux-meditate` literal |
| `TestMeditateCommandDefinition` | `test_supports_quoted_topic` | `:69-71` | Contains `topic` or `question` token |
| `TestMeditateCommandDefinition` | `test_supports_file_references` | `:73-75` | Contains `@` or `file` token |
| `TestMeditateFacetStructure` | `test_documents_three_facets` | `:89-91` | Contains `three` or `3` |
| `TestMeditateFacetStructure` | `test_facets_are_distinct_dimensions` | `:93-98` | Contains ≥2 of `theme` / `topic` / `intent` / `facet` |
| `TestMeditateFacetStructure` | `test_facets_become_branches` | `:100-102` | Contains `branch` or `parallel` |
| `TestMeditateRecursiveDepth` | `test_documents_three_levels` | `:116-118` | Contains `3` or `three` |
| `TestMeditateRecursiveDepth` | `test_level_1_spawns_agents` | `:120-122` | Contains `level 1` or `spawn` |
| `TestMeditateRecursiveDepth` | `test_level_3_is_terminal` | `:124-127` | Contains `depth-3` / `depth 3` / `level 3` / `deepest` |
| `TestMeditateRecursiveDepth` | `test_recursive_structure` | `:129-131` | Contains `recursive` |
| `TestMeditateRecursiveDepth` | `test_depth_is_configurable` | `:133-136` | Contains `maxdepth` or `depth selection` |
| `TestMeditateRecursiveDepth` | `test_depth_selection_question_exists` | `:138-140` | Contains `Q-Depth-Selection` (literal) |
| `TestMeditateRecursiveDepth` | `test_depth_defaults_to_three` | `:142-144` | Contains `default` AND `3` |
| `TestMeditateMemoryQuerying` | `test_queries_memories` | `:158-160` | Contains `memor` |
| `TestMeditateMemoryQuerying` | `test_uses_memory_index` | `:162-164` | Contains `index` or `search` |
| `TestMeditateMemoryQuerying` | `test_refines_queries_at_each_level` | `:166-168` | Contains `refine` or `expand` |
| `TestMeditateConsolidation` | `test_documents_consolidation` | `:182-184` | Contains `consolidat` |
| `TestMeditateConsolidation` | `test_highlights_cross_branch_connections` | `:186-188` | Contains `cross` or `connection` |
| `TestMeditateConsolidation` | `test_presents_organized_output` | `:190-192` | Contains `branch` or `organized` |
| `TestMeditateContinuationMenu` | `test_offers_expansion_options` | `:206-208` | Contains `expansion` or `direction` |
| `TestMeditateContinuationMenu` | `test_offers_save_as_spec` | `:210-212` | Contains `spec` AND `save` |
| `TestMeditateContinuationMenu` | `test_offers_end_option` | `:214-216` | Contains `end` |
| `TestMeditateContinuationMenu` | `test_uses_ask_question` | `:218-220` | Contains `AskQuestion` (literal) |
| `TestMeditateAgentSpawning` | `test_spawns_memory_manager` | `:234-236` | Contains `crux-cursor-memory-manager` (literal) |
| `TestMeditateAgentSpawning` | `test_meditate_mode` | `:238-240` | Contains `meditate mode` or `Meditate mode` |

**Per-spec observation for subtask 06**:
- `test_spawns_memory_manager` (Class `TestMeditateAgentSpawning`) explicitly checks for `crux-cursor-memory-manager` — under K3 dual-target landing this assertion must remain valid against the **pre-decomposition** target. If 20260517 has shipped at execution time, subtask 06 must either branch this assertion on filesystem inspection or update it to check for `crux-cursor-meditation-guide` instead.
- The existing test list has **zero** assertions on `theming`, `comprehensiveness`, init-suggestions, finalisation-enhancements, or respawn protocol — these are all greenfield for subtask 06.

### 9.2 `evals/sdk/tests/q-meditate.test.ts` (TypeScript SDK — 357 lines, 3 describe blocks Q1–Q3)

These are **GATED** tests (gated behind `SDK_EVAL_SKIP_EXPENSIVE`,
default skip — see `:8-29`). They spin a real `@cursor/february/agent`
session in an isolated workspace with 8 pre-seeded memory fixtures
covering performance, security, architecture, and testing
categories (`:38-153`).

| `describe` | `it` test | Lines | Asserts |
|------------|-----------|-------|---------|
| `Q1: Meditate - No Arguments (Context-Derived Facets)` | `"derives exploration facets from context"` | `:194-208` | Agent's `assistantText` contains facet-derivation language (`facet`/`theme`/`dimension`/`branch`/`direction`/`aspect`/`exploration`) OR enumerates 1/2/3 |
| `Q1: Meditate - No Arguments (Context-Derived Facets)` | `"spawns subagents for recursive exploration"` | `:210-224` | At least one `Task` tool call OR a subagent call to `crux-cursor-memory-manager` |
| `Q1: Meditate - No Arguments (Context-Derived Facets)` | `"references memories in consolidated output"` | `:226-247` | Output text references at least one of `memory`/`memoiz`/`cache`/`lazy`/`singleton` AND contains consolidation language (`insight`/`finding`/`pattern`/`connection`/`theme`/`synthesis`/`consolidat`) |
| `Q2: Meditate - Topic Argument` | `"derives facets from provided topic"` | `:278-292` | Output text contains topic-relevant terms (`cache`/`caching`/`strategy`/`ttl`/`invalidation`) |
| `Q2: Meditate - Topic Argument` | `"produces consolidated insights referencing memories"` | `:294-314` | Output references memory content terms (`memory`/`stale-while-revalidate`/`ttl`/`cache invalidation`) AND contains insight language (`connection`/`pattern`/`across`/`relate`/`link`/`insight`/`consolidat`/`synthesis`) |
| `Q3: Meditate - File/Folder References` | `"derives facets from file/folder reference"` | `:322-356` | Run status = `"finished"` AND output contains facet-derivation language OR topic terms (`skill`/`pattern`/`memory`) |

**Per-spec observation for subtask 06**:
- All three describe blocks invoke `/crux-meditate` end-to-end with `model: { id: "composer-2" }` and a 480_000 ms timeout per `it`.
- The test `"spawns subagents for recursive exploration"` (`:210-224`) explicitly checks for `crux-cursor-memory-manager`. Same dual-target observation as the Python test above applies under K3.
- No existing SDK test covers cost-ack acknowledgement, theme preflight, richness selection, init-suggestions, finalisation-enhancements, or respawn protocol — all greenfield for subtask 06.
- The test setup uses `createMemoryFixture` × 8 (`:38-153`). Subtask 06 may want to add fixtures that surface a quantifiable trade-off (to exercise the calculator minima per level) and a comparison topic (to exercise the Option Comparison Research path × richness).

---

## 10. Existing safeguard inventory (must be preserved verbatim by this spec)

The new spec's non-negotiable preservation constraint (K7 +
Requirement 10) requires that every safeguard below is preserved
**unchanged at every comprehensiveness level**. The level varies
*richness*, not *rigor*.

| # | Safeguard | Live source (file:lines) | 20260517 freeze anchor | Preservation rule for this spec |
|---|-----------|--------------------------|-----------------------|-----------------|
| 1 | Anti-Homogenisation Rules | `.cursor/commands/crux-meditate.md:197-209` + `:1174-1194` | §6.2 | Identical at every level; `compact` does NOT relax. |
| 2 | Universal Contrast (WCAG) | `.cursor/commands/crux-meditate.md:1205-1231` | §6.3 | Identical at every level. |
| 3 | Subject-Matter Focus rule | `.cursor/commands/crux-meditate.md:878-898` | §8 | Identical at every level; applies to `consolidation.md` + HTML/PDF reports. |
| 4 | Citation discipline (mandatory `## Citations` section, validation rules) | `.cursor/agents/crux-cursor-memory-manager.md:655-690` + `.cursor/commands/crux-meditate.md:1003` | §5.5 | Density stays mode-driven (warn-only Quick / mandatory Research). `comprehensiveness.citation_density` payload field set by **mode**, not by level. `exhaustive` adds a per-finding-table column on top. |
| 5 | Pattern A vs Pattern B boundaries (subagents NEVER call `AskQuestion`) | `.cursor/agents/crux-cursor-memory-manager.md:17-46` + `.cursor/commands/crux-meditate.md:34-36` | §3 | Every new gate (`Q-Cost-and-Richness-Acknowledgment`, combined Pattern-B confirmation, `Q-Finalisation-Enhancements`) is calling-agent-owned. |
| 6 | Retrospective always-written rule | `.cursor/commands/crux-meditate.md:900-967` + `.cursor/agents/crux-cursor-memory-manager.md:444` | §5.7 | Unchanged. Always written including on `ESCALATE`. |
| 7 | Mandatory paired HTML + PDF output | `.cursor/commands/crux-meditate.md:969-985` (filename grammar + paired rule) + `.cursor/agents/crux-cursor-memory-manager.md:432` (depth-0 step 12) | §6.1 | Unchanged. Every level produces paired HTML + PDF; no level skips the PDF. |
| 8 | Adversarial review-and-fix cycle (≤3 iterations) | `.cursor/commands/crux-meditate.md:781-799` (iteration loop, verbatim) + `.cursor/agents/crux-cursor-memory-manager.md:424-428` | §4.6 | ≤3 iteration cap preserved. **New Dim 12 + Dim 13 + level-conditional Dim 9** added; **Dim 13 triggers respawn protocol** sharing the same iteration budget. **K10b** adds `accepted_finalisation_enhancements` as a respawn cause; respawn budget unchanged. |
| 9 | Headless Chrome → Chromium degradation chain | `.cursor/commands/crux-meditate.md:1294-1316` + `.cursor/agents/crux-cursor-memory-manager.md:440` | §6.6 | Unchanged. No-Chromium failure mode preserved (clear error + install hint + leave HTML in place). |
| 10 | Non-interactive abort on `Q-Cost-Acknowledgment` | `.cursor/commands/crux-meditate.md:189` | §2.2 (line 155 of that freeze) | Preserved. New merged gate inherits this rule; richness gets a non-interactive default of `default`, but `proceed` is NOT auto-selected. |
| 11 | `confirmDeepFacets` deep-YAML escalation schema | `.cursor/commands/crux-meditate.md:363-431` | §2.7 | Unchanged. The new K6 set-once-per-invocation pattern for richness mirrors the existing `confirmDeepFacets` propagation. |
| 12 | Citation index `citations-index.yml` (Research mode) | `.cursor/agents/crux-cursor-memory-manager.md:655-690` | §5.5 | Unchanged. Research mode strict citation validation with 2-retry respawn preserved. Quick mode warn-only preserved. |
| 13 | Facet registry lock (`mkdir`-based) | `.cursor/agents/crux-cursor-memory-manager.md:607-653` | §5.4 | Unchanged. Even with K4 `additional_facet` opt-ins increasing facet count, the registry lock-and-append protocol is unchanged. |
| 14 | Peer review file spec (Research mode) | `.cursor/agents/crux-cursor-memory-manager.md:692-720` | §5.6 | Unchanged. `comprehensiveness.peer_review_surfacing` controls REPORT surfacing of peer-review content; the peer-review file format itself is unchanged. |
| 15 | Theming payload propagation (subagent abort if missing) | `.cursor/commands/crux-meditate.md:267-293` + `.cursor/agents/crux-cursor-memory-manager.md:305` | §2.4 | Unchanged shape; the new `comprehensiveness:` payload mirrors this propagation pattern (same abort-if-missing rule per K5). |
| 16 | Branch & Leaf Index template (`## Top-level artifacts` block) | `.cursor/commands/crux-meditate.md:671-735` | §5.8 | Existing block preserved verbatim; spec ADDS new top-level artefact links (`init-suggestions-{ts}.yml` per K6 + `finalisation-enhancements.yml` per K10c) without modifying existing entries. |

---

## 11. Dual-target inventory — 14 contract items × (pre-decomp + post-decomp + touch reason)

This is the input table to subtask 02's patch matrix. For each of
the 14 contract items in subtask 01's "Scope — items to freeze",
this table lists the current pre-decomposition target (where it
lives at HEAD on 2026-05-23) AND the post-decomposition target
(per `meditate-decomp-architecture-design-20260517.md` §3) AND the
touch reason this spec applies.

| # | Contract item | Pre-decomposition target (today, file:lines) | Post-decomposition target (per 20260517 §3) | Touch reason for this spec |
|---|---------------|----------------------------------------------|---------------------------------------------|----------------------------|
| 1 | Calling-agent gate ordering — 4-gate pre-spawn + mid-flow Facet Confirmation | `.cursor/commands/crux-meditate.md:30-36` (Pattern-B preamble) + `:55-105` (Q-Depth) + `:106-189` (Q-Cost + Expansion) + `:191-293` (Theme Preflight) + `:295-439` (Facet Confirmation) | `command` (verbatim, all four gates) per 20260517 §3.2; no skill duplicates gate prompts | **K2** merges gate-2 with richness selection (renamed `Q-Cost-and-Richness-Acknowledgment`); **K4** folds init-suggestions into gate-4's combined Pattern-B prompt; gate count stays at 4 logical slots. |
| 2 | Existing facet-confirmation `needs_user_input` schema (`facets-pending-{ts}.yml` + `Q-Confirm-1` + `Q-Confirm-2`) | `.cursor/commands/crux-meditate.md:309` (write semantics) + `:311-330` (Q-Confirm-1 prompt+options) + `:338-359` (Q-Confirm-2 prompt+options) + `:361` (delete semantics) + filename row `:446` | `command` (verbatim) per 20260517 §3.2; `skill:coordination` (filename row only) per 20260517 §5.1; `skill:research`/`skill:quick` reference the option set | **K4** extends the schema with `sections` / `visualisations` / `additional_focus_areas` blocks AND folds `Q-Confirm-1` + `Q-Confirm-2` + new init-suggestions confirmation into a single combined `askQuestion`. |
| 3 | Report-generation contract minima (≥4 charts / ≥3 infographics / ≥1 calculator) | `.cursor/commands/crux-meditate.md:1068-1070` (charts) + `:1119-1121` (infographics) + `:1137-1146` (calculator) + `:1066` (Option Comparison "standard content minimums" sentence) + `:1474` (Ensemble "in addition to the standard minimums" heading) + `.cursor/agents/crux-cursor-memory-manager.md:439` (mirror) | `skill:report` (verbatim) per 20260517 §3.6; `command` and `agent` become one-paragraph pointers | **K1 + K5 + Requirement 3** — replace fixed minima with level-driven `comprehensiveness.minima.{charts,infographics,calculators}.count` payload mapping; `compact` reproduces the current numbers exactly. |
| 4 | Per-branch / depth-3 / peer-review surfacing today | `.cursor/commands/crux-meditate.md:1000` (per-facet sections) + `:1001` (quality review section, Research) + `:1008` (all 39 branch files rule) + `:1016` (input coverage verification) + `:1018` (anti-sparseness escalation) + `.cursor/agents/crux-cursor-memory-manager.md:311` (working-dir framing) + `:411-420` (Research consolidation step 8 reads 3 depth-1 + 3 peer-review + citations-index) + `:457` (Quick consolidation step 8 reads 3 depth-1 only) | `skill:report` (verbatim) per 20260517 §3.6 + `skill:research`/`skill:quick` (mirror for consolidation step 8) per 20260517 §3.4 | **K5** introduces `comprehensiveness.depth3_leaf_inclusion` (`elided` / `summary` / `verbatim_quotes`), `comprehensiveness.per_branch_section_depth` (`consolidation_only` / `branch_summary` / `per_leaf_detail`), and `comprehensiveness.peer_review_surfacing` (`consolidation_only` / `named_section` / `per_branch_dedicated`) payload fields. `compact` reproduces today's behaviour exactly. |
| 5 | Anti-Homogenisation Rules | `.cursor/commands/crux-meditate.md:197-209` + `:1174-1194` | `skill:report` (verbatim) per 20260517 §3.6 + `command` (one-paragraph pointer in Theme Preflight) | **K7 + Requirement 10** — preserve verbatim at every level. Cited via 20260517 freeze §6.2; not restated. |
| 6 | Universal Contrast (WCAG-style) block | `.cursor/commands/crux-meditate.md:1205-1231` | `skill:report` (verbatim) per 20260517 §3.6 | **K7 + Requirement 10** — preserve verbatim at every level. Cited via 20260517 freeze §6.3; not restated. |
| 7 | Subject-Matter Focus rule | `.cursor/commands/crux-meditate.md:878-898` + `.cursor/agents/crux-cursor-memory-manager.md:837` | `skill:report` (verbatim) per 20260517 §3.8 + `skill:research`/`skill:quick`/`skill:review` (mirror) | **K7 + Requirement 10** — preserve verbatim. Cited via 20260517 freeze §8; not restated. Applies to `consolidation.md` + HTML/PDF reports only (NOT to `retrospective-{ts}.md`). |
| 8 | Adversarial review 11-dimension list | `.cursor/commands/crux-meditate.md:759-771` (dimensions) + `:773-779` (severity) + `:781-799` (iteration loop) + `:801-816` (MUST_FIX escalation schema) + `:818-867` (review document format) + `:869-876` (Quick relaxations) + `.cursor/agents/crux-cursor-memory-manager.md:424-428` (depth-0 step 10) + `:833` (design-principle restatement) | `skill:review` (verbatim) per 20260517 §3.4 + `agent` (mode-router pointer) | **K9 + Requirement 8** — extend with 2 new dimensions (Dim 12 Comprehensiveness Fidelity + Dim 13 Init-Suggestion Honour) plus level-conditional expansion of Dim 9 (peer-review thoroughness). **Dim 13 triggers respawn protocol** (NOT in-place rewrite). The existing 11 dims + severity taxonomy + iteration loop + MUST_FIX `needs_user_input` schema are frozen verbatim. **K10b** extends respawn payload with `accepted_finalisation_enhancements` cause; iteration budget unchanged. |
| 9 | Citation discipline | `.cursor/agents/crux-cursor-memory-manager.md:655-690` (inline markers + per-file requirement + `citations-index.yml` schema + validation rules) + `.cursor/commands/crux-meditate.md:1003` (report Citations section requirement) | `skill:research` (Research strict variant) + `skill:quick` (warn-only variant) + `skill:coordination` (filename row only) per 20260517 §3.5 | **K7 + Requirement 10** — preserve verbatim. Cited via 20260517 freeze §5.5; not restated. `comprehensiveness.citation_density` payload field set by **mode** at every level. `exhaustive` ADDS a per-finding-table citation column on top; does NOT relax the underlying rule. |
| 10 | Retrospective always-written rule | `.cursor/commands/crux-meditate.md:900-967` + `.cursor/agents/crux-cursor-memory-manager.md:444` (step 12b) | `skill:coordination` (verbatim) per 20260517 §3.5 + `agent` (step 12b pointer) | **K7 + Requirement 10** — preserve verbatim. Cited via 20260517 freeze §5.7; not restated. |
| 11 | Branch & Leaf Index template (`## Top-level artifacts` subsection in particular) | `.cursor/commands/crux-meditate.md:671-735` + `.cursor/agents/crux-cursor-memory-manager.md:422` (depth-0 step 9) + `:430` (post-review refresh step 11) | `skill:coordination` (verbatim) per 20260517 §3.5 + `command`/`agent` (pointer) | **K6 + K10c** — add 1–2 new top-level artefact link rows: `[Init suggestions](init-suggestions-{ts}.yml)` AND `[Finalisation enhancements](finalisation-enhancements.yml)`. Existing template entries (`Consolidation`, `Process Retrospective`, `Report HTML/PDF`, `Adversarial review iterations`, `Facet confirmation trail`, `Facet registry`, `Citations index`) preserved verbatim. |
| 12 | Pattern A vs Pattern B boundaries | `.cursor/commands/crux-meditate.md:34-36` (preamble) + `.cursor/agents/crux-cursor-memory-manager.md:17-46` (User Input Escalation block) + `:302-307` (Meditate-mode reaffirmation) | `agent` (Critical Rules — verbatim restatement) per 20260517 §3.3 + `command` (preamble retained) + every skill cites by reference | **K7 + Requirement 10** — preserve verbatim. Cited via 20260517 freeze §3; not restated. Every new gate (`Q-Cost-and-Richness-Acknowledgment` per K2, combined Pattern-B confirmation per K4, `Q-Finalisation-Enhancements` per K10a, `spawn_now` re-presentation per K10b) is calling-agent-owned. Subagents NEVER call `AskQuestion`. |
| 13 | Cost-ack expansion variant (`Q-Cost-Acknowledgment-Expansion`) | `.cursor/commands/crux-meditate.md:174-189` (expansion bullet embedded in Cost Ack behaviour rule; prompt `:178-184`, options `:187-188`) + `:433-438` (Re-spawn semantics with `confirmDeepFacets` reuse + "keep deep-confirm setting?" follow-up) | `command` (verbatim, expansion branch in §2.3 mirror) per 20260517 §3.2 | **K2 + K6** — replace with the read-only-richness variant of the merged `Q-Cost-and-Richness-Acknowledgment` gate (richness shown LOCKED per K6 set-once-per-invocation). The expansion variant does NOT offer a "keep richness setting?" follow-up; richness is implicitly locked. The existing "keep deep-confirm setting?" follow-up at `:438` is **preserved unchanged**. Reproduced verbatim in §8 above. |
| 14 | Existing eval coverage in `evals/test_q_meditate.py` + `evals/sdk/tests/q-meditate.test.ts` | `evals/test_q_meditate.py:13-240` (8 test classes, 25 tests — see §9.1 above for table) + `evals/sdk/tests/q-meditate.test.ts:31-357` (3 describe blocks Q1–Q3, 6 `it` tests — see §9.2 above for table) | unchanged location (`evals/` is repo-stable across both pre- and post-decomp targets) | **K9 + Requirement 12 + K10 + Requirement 22** — extend without deleting any existing assertion. New tests assert: merged gate shape (sub-Q1 richness + sub-Q2 proceed/swap/cancel); `comprehensiveness` payload propagation; level → minima mapping (incl. `compact` regression test); combined Pattern-B askQuestion fold; `init-suggestions-{ts}.yml` schema + read by report; respawn protocol + finite-iteration; `Q-Finalisation-Enhancements` 0–5 multi-select; cheap-respawn + expensive-queue + expensive-spawn-now flows; `finalisation-enhancements.yml` schema; continuation menu surfaces unchosen + queued items. The existing `test_spawns_memory_manager` and SDK `"spawns subagents for recursive exploration"` (both literal-check `crux-cursor-memory-manager`) must remain valid against the pre-decomp target; under K3 dual-target landing, subtask 06 either branches on filesystem inspection or updates the literal to `crux-cursor-meditation-guide` when 20260517 has shipped. |

---

## 12. Decompositional notes for subtask 02

These observations surfaced while building this freeze and feed
directly into subtask 02 (architecture-design) decisions:

1. **`facets-pending-{ts}.yml` shape not specified verbatim today.**
   Only the deep-facet `pending-facets-*.yml` schema is verbatim
   (`.cursor/commands/crux-meditate.md:376-397`). The depth-0
   facet-pending YAML structure is described as "the proposed
   facets verbatim" (`:309`) but no YAML schema is given. Subtask
   02 must explicitly define the extended schema (with
   `sections` / `visualisations` / `additional_focus_areas`
   blocks) — there is no pre-existing schema to extend; this is
   greenfield contract specification.

2. **Combined `askQuestion` template doesn't exist today.** Today
   `Q-Confirm-1` and `Q-Confirm-2` are two sequential `askQuestion`
   calls. The new spec's combined Pattern-B prompt (folding 5
   things into one prompt) is a brand-new template — subtask 02
   must produce it from scratch and verify it meets the existing
   `MUST_FIX needs_user_input` decision-guidance schema rule
   (`.cursor/commands/crux-meditate.md:801-816`).

3. **K10 layered ensemble cadence reaches the existing `Ensemble
   Aggregation` function but does not duplicate it.** The K10a
   layered cadence (per-tree YAMLs + root cross-model YAML) adds
   a second reflection step on top of the existing 5-step
   ensemble aggregation workflow
   (`.cursor/agents/crux-cursor-memory-manager.md:872-907`).
   Subtask 02 must decide whether the layered cadence lives in
   `skill:ensemble` (which already owns Ensemble Aggregation) OR
   in a sibling `skill:research` / `skill:quick` extension. The
   freeze records the existing 5-step workflow as the integration
   point.

4. **Dual literal-check tests pose K3 risk.** Two existing test
   assertions (`test_spawns_memory_manager` Python and
   `"spawns subagents for recursive exploration"` SDK) literally
   check for `crux-cursor-memory-manager`. Under K3, the test
   must still pass against the pre-decomp target AND against the
   post-decomp target. Subtask 06 must decide on a branching
   strategy (filesystem inspection of which agent file exists, OR
   accept-either pattern). This is flagged for the subtask-02
   architect.

5. **No existing test asserts `theming`, `comprehensiveness`,
   init-suggestions, or finalisation-enhancements.** The entire
   K1–K10 surface is greenfield for test coverage. Subtask 06 is a
   sizeable scope; subtask 02's architecture-design deliverable
   should produce a test matrix anchored on each Requirement
   1–22 of the spec so subtask 06 has a deterministic checklist.

6. **Backwards-compat anchor cost numbers.** K1 requires `compact`
   to reproduce today's behaviour exactly. The per-tree agent
   count at depth 3 Research today is **~45**
   (`.cursor/commands/crux-meditate.md:65` + 20260517 freeze §1
   line 32). The spec's K2 worked-example table pegs `compact` at
   ~45 agents, which matches. Subtask 02's authoritative
   numerical table should use these existing counts as the
   `compact` row; subtask 06 may pin numerically via
   `TestMeditateCostFormulaNumericPinning` once subtask 02 lands.

---

## 13. Definition of Done — Subtask 01 (this freeze)

- [x] Markdown-only artefact (no code edits) — only this file is created.
- [x] Every contract item back-traceable to a current source line range or section anchor in the repo at the spec start commit (sections 2–11 above; each row carries `file:lines` citations or cross-references a 20260517 freeze section).
- [x] Document referenced from spec index Execution Notes (Cross-references) — see `spec-meditate-richness-20260523.md` Execution Notes section.
- [x] No linter errors introduced.

---

_Captured by `crux-platform-architect` against repo
`/home/andrewv/git/cursor/CRUX-Compress` at git HEAD on
2026-05-23. Subsequent subtasks of
`specs/20260523-meditate-richness/` must treat this document as
the **freeze line** for the touched surface — any deviation
requires an explicit `needs_user_input` escalation surfaced through
the calling agent._
