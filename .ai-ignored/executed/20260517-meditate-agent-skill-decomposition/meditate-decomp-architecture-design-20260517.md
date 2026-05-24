# Meditate Decomposition — Architecture Design (20260517)

> **Purpose**: Translate the frozen contract in
> `meditate-frozen-contract-20260524.md` (the **post-richness refresh**
> freeze line; supersedes the original `meditate-frozen-contract-20260517.md`)
> into a concrete section-by-section assignment that places every
> contract item in exactly one of (a) the thin coordinator command
> `/crux-meditate`, (b) the new guide agent
> `crux-cursor-meditation-guide`, or (c) one of the six approved
> `crux-skill-memory-meditation-*` skills.
>
> **Refresh history**:
>
> - **Original capture (2026-05-17)** — drafted against
>   `meditate-frozen-contract-20260517.md` and the
>   pre-richness sources (`.cursor/commands/crux-meditate.md` 1493 lines,
>   `.cursor/agents/crux-cursor-memory-manager.md` 946 lines). Judge
>   blocker D04 was raised because the §3 section-mapping table carried
>   split or alternative primary destinations on four+ rows.
> - **Refresh 2026-05-24** — re-anchored against the new freeze line
>   `meditate-frozen-contract-20260524.md` (1557 lines) which captures
>   the 13 new contract surfaces introduced by the completed sibling
>   spec `specs/20260523-meditate-richness/` (executor sign-off
>   2026-05-24). The §3 mapping, §4.1 line numbers, §4.2 budget, §5
>   trim ranges, §7 risks, §8 discovery cues, and §9 per-subtask table
>   are all re-projected against the **current** sources:
>   `.cursor/commands/crux-meditate.md` (**2142 lines** — was 1493) and
>   `.cursor/agents/crux-cursor-memory-manager.md` (**1388 lines** —
>   was 946). The judge blocker D04 is resolved: every row is
>   normalised to a single primary destination plus zero-or-more
>   mirrors.
>
> **Authoritative reference**: every row in this document back-traces
> to a section heading in
> `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260524.md`.
> Where this document quotes line numbers, they refer to the **current**
> working-tree sources at git SHA
> `b4fc33b0c034866bb60b7fe7b03be9e0c7a18bbf` + unstaged 20260523
> richness changes (the same baseline the new freeze captured).
>
> **Secondary authoritative input**: the richness spec's
> `specs/20260523-meditate-richness/meditate-richness-architecture-design-20260523.md`
> §11 (init-suggestions schema) and §13 (patch matrix, 21 rows) are
> consulted by S04 + S05 implementers when richness rows touch their
> destination skills. The patch matrix is **secondary** — this design's
> §3 remains the authoritative concordance.
>
> Subtask 02 is **read-only against source code**: this document is the
> design contract that subtasks 04, 05, 06, 07 implement. Subtasks 03
> (eval/test plan), 08 (eval/test update), 09 (docs sync), 10
> (install/dist/release), 11 (CRUX compression) and 12 (integrity
> review) consume the table in §3 as the concordance for verifying
> functional preservation.

---

## 1. Final Guide-Agent Specification — `crux-cursor-meditation-guide`

### 1.1 Frontmatter

```yaml
---
repository: https://github.com/zotoio/CRUX-Compress
name: crux-cursor-meditation-guide
model: claude-opus-4-6
color: indigo
description: Recursive memory-informed meditation guide. Owns the Meditate persona, Research Phases A–G, Quick 6-step protocol, Adversarial Review function (13 dimensions, Report-Skill Respawn Protocol), and Ensemble Aggregation function (with K10 layered cadence). Spawned by `/crux-meditate` for the entire subagent tree; never user-invoked directly.
tools: ["*"]
---
```

**Field rationale**:

| Field | Value | Rationale |
|-------|-------|-----------|
| `name` | `crux-cursor-meditation-guide` | Matches `.cursor/agents/<name>.md`; suffix `-guide` distinguishes from `-memory-manager` and signals the persona role |
| `model` | `claude-opus-4-6` | Identical to current `crux-cursor-memory-manager.md` line 4; preserves model behaviour exactly. In ensemble mode, `model: ensembleModel` is passed per-Task and overrides this default (see §1.3 step 6). |
| `color` | `indigo` | Distinct from existing agents (memory-manager is unset, rule-manager defaults). Indigo is **not** in the Anti-Homogenisation block-list when used as agent-UI accent (it is forbidden only as the report hero gradient); the colour is a UI hint, never a report-theming source |
| `tools` | `["*"]` | Same surface as `crux-cursor-memory-manager.md` (no current tool restrictions in any meditate-mode invocation); future restriction can land in subtask 04 via integrity-expert review |
| `description` | as above | Substring `meditation` present (eval discoverability), substring `Recursive memory-informed` matches existing README copy, substring `crux-cursor-meditation-guide` not needed in description because `name` is authoritative. The 2026-05-24 refresh adds explicit mention of the 13-dimension reviewer, Report-Skill Respawn Protocol, and K10 layered cadence so eval discovery can pick them up |

### 1.2 Persona prologue

The agent's prologue (first ~30 lines after frontmatter) mirrors the
`crux-cursor-memory-manager.md` shape and contains:

1. **One-paragraph persona**: "You are the CRUX Meditation Guide, responsible for orchestrating recursive memory-informed exploration trees in the CRUX-Compress project — Research-mode Phases A–G recursion, Quick-mode 6-step parallel fan-out, K10 in-pass reflection (per-tree single-model + cross-model ensemble), Ensemble Aggregation cross-model synthesis with layered K10 cadence, and the 13-dimension adversarial review-and-fix cycle (with Report-Skill Respawn Protocol) that gates every report."
2. **CRITICAL: Load Context First** — identical pattern to memory-manager lines 9–16:
   - Read `AGENTS.md` if not loaded.
   - Read `CRUX.md` from project root.
   - Read `.crux/crux-memories.json` for `flags.enableMemories`, `cruxMemories.meditate.modelPool`, `cruxMemories.meditate.ensembleAggregatorModel`, `cruxMemories.meditate.finalisationEnhancements.{minimumImpactThreshold,weights}` (the K10 rubric config — proposed defaults documented in agent file even though not yet wired into `.crux/crux-memories.json` shipping defaults).
3. **User Input Escalation — CRITICAL** — verbatim copy of the Pattern A / Pattern B / `needs_user_input` schema block currently in
   `crux-cursor-memory-manager.md` lines 17–46. This block is **mirrored**
   between the two agents because each is independently spawnable; it is
   not coordination-state and never drifts.
4. **Your Expertise** — bulleted list:
   - Recursive Meditation (Research Phases A–G with comprehensiveness-aware leaf inclusion)
   - Quick parallel fan-out (6-step protocol)
   - Adversarial Review (13-dimension, ≤3 iterations, MUST_FIX `needs_user_input` with mandatory `context`, Dim 13 Report-Skill Respawn Protocol)
   - Ensemble Aggregation (cross-model synthesis with K10 layered cadence — per-tree + root reflection, single combined root gate, per-tree vs cross-model respawn targeting)
   - K10 in-pass reflection (impact × insight-value rubric inside the depth-0 manager turn, no extra spawn)
   - Report generation orchestration (HTML + PDF, Universal Contrast, anti-homogenisation, headless-Chrome → Chromium degradation, comprehensiveness-driven minima, init-suggestions + finalisation-enhancements honour, K10b Per-Cheap-Type Rendering Contract)
   - File-based coordination (artefact filename grammar — 18 rows including `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`, `follow-up-{type}-{ts}.yml`; prefix-glob polling; registry locks; citations index)

### 1.3 Mode router (executable section list)

The agent file body is organised as a thin **mode router** that loads
each skill on demand and provides only the orchestration glue. The
verbatim contracts (phase definitions, dimension lists, schemas) live
exclusively in the skills.

| Section | Heading | Loads | Owns directly (glue) |
|---------|---------|-------|----------------------|
| 1 | `## Skills You Use` | — | Skill discovery table (one row per skill, mirrors §2) |
| 2 | `### Meditate Mode — `/crux-meditate`` | `meditation-coordination` (filenames, placeholders, polling glob, retrospective template, Branch & Leaf Index template — including the `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`, and `follow-up-{type}-{ts}.yml` rows added by 2026-05-24) | Invocation variants table (mirrors current memory-manager Meditate Mode preamble), mode-selection logic, `theming` payload abort rule, **`comprehensiveness:` payload abort rule (canonical error string)**, file-based coordination preamble, working directory invariant `meditations/{yyyymmdd}-{topic-slug}/` |
| 3 | `#### Research mode depth-0 workflow (steps 1–13, incl. step 4b + step 8b)` | `meditation-research` + `meditation-coordination` | Step list with one paragraph per step; verbatim Phases A–G live in the skill. The router preamble mentions scouting init-suggestions production (step 4 derives sections + visualisations + 4-mode focus areas) and step 4b's `init-suggestions-{ts}.yml` write + 4-mode reconciliation |
| 4 | `#### Quick mode top-level workflow (substitutions; incl. step 4b + step 8b)` | `meditation-quick` + `meditation-coordination` | Step-list deltas vs. Research; verbatim 6-step protocol lives in the skill. The router preamble mentions scouting init-suggestions production (same combined Pattern-B gate; Quick warn-only citation regime) and step 4b's `init-suggestions-{ts}.yml` write |
| 5 | `#### K10 In-Pass Reflection function` (**NEW per 2026-05-24 refresh**) | `meditation-research` / `meditation-quick` (single-model per-tree reflection) + `meditation-ensemble` (cross-model reflection) | One-paragraph reminder that the K10 reflection runs **inside the depth-0 manager's existing LLM turn** — no new agent spawn — using inputs already in context (branch files + peer reviews + consolidation prose + citations index). Per-tree in single-model writes `finalisation-enhancements.yml`; cross-model in ensemble runs step 3c–3d after `cross-model-synthesis.md` and writes the root combined YAML. The router's role is to remind the agent that K10 fires before returning control to the calling agent for `Q-Finalisation-Enhancements`. |
| 6 | `#### Adversarial Review function` (**13+ dimensions; Report-Skill Respawn Protocol**) | `meditation-review` | One-paragraph spawn contract + which files are editable / read-only / never-touched. The verbatim 13 dimensions (incl. Dim 9 level-conditional expansion, Dim 12 Comprehensiveness fidelity, Dim 13 Init-suggestion AND finalisation-enhancement honour) + severities + MUST_FIX `needs_user_input` schema with mandatory `context` + Dim 13 `respawn_required: true` payload schema (K9 + K10b — `respawn_reasons` list-typed) all live in the skill |
| 7 | `#### Ensemble Aggregation function` (**with K10 layered cadence**) | `meditation-ensemble` + `meditation-report` | One-paragraph spawn contract (parameters `ensembleWorkingDir`, `modelSubdirs`, `confirmedFacets`, `theming`, **`comprehensiveness`**, `meditateMode`, `topicSlug`). The cross-model synthesis schema + ensemble report extras + K10 layered cadence (steps 3b–3f: read per-tree YAMLs → cross-model reflection → root combined YAML write → combined `needs_user_input` → resume handler) + K10 Ensemble Respawn Targeting all live in the skills |
| 8 | `#### Report generation obligation` | `meditation-report` + `meditation-coordination` | One-paragraph "step 12 produces a paired report-{topic-slug}-{ts}.html + .pdf per `meditation-report` consuming `comprehensiveness`, `init-suggestions-{ts}.yml` (mandatory honour), and accepted cheap items from `finalisation-enhancements.yml` (K10b Per-Cheap-Type Rendering Contract)"; full HTML/PDF contract lives in the skill |
| 9 | `## Design Principles` | — | The ≈20 design-principle bullets currently in memory-manager Meditate Mode (now spanning lines 1137–1158 post-richness) including the new bullets `mandatory user confirmation of facets + init-time suggestions`, `set-once-per-invocation richness`, `K10 reflection bounded`. Kept on the agent because they describe the persona's invariants, not executable steps |
| 10 | `## Agent Scoping Rules` | — | Brief carve-out: this agent never creates memories (it produces meditation artefacts in `workingDir`, not memory files). Mirrors memory-manager `## Agent Scoping Rules` conceptually but the Writing-Agent-Memories rule is N/A here — call out explicitly to avoid drift |
| 11 | `## Critical Rules` | — | Feature guard (`flags.enableMemories`), Pattern B integrity, never-call-AskQuestion, skill delegation (always read skill before invocation), **abort-if-comprehensiveness-missing rule (canonical error string)** |

**Spawn signature when the agent calls a skill** (subagent never spawns
subagents itself in research/quick mode — children are direct `Task`
calls to **another instance of the same** `crux-cursor-meditation-guide`
agent; skills are read in-context, not spawned):

```text
Read .cursor/skills/crux-skill-memory-meditation-{name}/SKILL.md
Follow its operations contract verbatim.
```

The only sub-spawns the guide agent issues are:
- Branch explorers in Research step 5 / Quick step 5: child `crux-cursor-meditation-guide` instances in Meditate mode (with `meditateMode`, `meditateDepth`, `workingDir`, `theming`, **`comprehensiveness`**, `confirmDeepFacets`, `ensembleModel?`)
- Peer reviewers in Research step 7: `crux-cursor-meditation-guide` in **Peer Review** sub-mode (one per branch)
- Adversarial reviewer in step 10: `crux-cursor-meditation-guide` in **Adversarial Review** function (with `reviewerIteration: 1|2|3`, `priorReviewPath?`)
- (Ensemble only, owned by coordinator command) Cross-model aggregation in coordinator step 9: `crux-cursor-meditation-guide` with `ensembleAggregation: true`
- (Single-model only, K10b expensive `spawn_now`) post-adversarial-cycle expensive agents per `pending_spawn_now: [...]` returned in step 13 — these spawns are **calling-agent-owned**, the guide agent only returns the queue.

All these spawns are documented in the agent body but the verbatim
parameter lists, regenerate caps, respawn-payload schemas, and
citation-validation respawn rules live in
`meditation-research` / `meditation-quick` / `meditation-review` /
`meditation-ensemble`.

### 1.4 Agent body length budget

| Metric | Source span (post-richness) | Target (in `crux-cursor-meditation-guide.md`) |
|--------|------------------------------|-----------------------------------------------|
| Lines 279–1159 (Meditate Mode) + 1189–1349 (Ensemble Aggregation) | ~1041 lines | **≤ 500 lines** total agent body |
| Reduction | — | ~52 % — verbatim Phases / dimensions / schemas / templates / K10c rubric / Report-Skill Respawn Protocol migrate to skills |

The original 2026-05-17 design targeted ≤ 350 lines against a ~600-line
source. The 2026-05-24 refresh **raises the budget to ≤ 500 lines**
because the source has grown to ~1041 lines (the richness spec added
the K10c rubric + K10b Per-Cheap-Type catalogue + 4-mode focus-area
reconciliation + comprehensiveness honouring at leaf depth + K10
layered cadence to the agent body). Integrity-expert flags **>550
lines** in S12 as "agent has not delegated enough to skills". The
target stays an order-of-magnitude under the source, but is
proportionally relaxed.

---

## 2. Final Skill List

The skill family is **fixed at exactly six skills** per spec K3 / spec
§K3 / subtask 02 brief. The 2026-05-24 refresh **confirms** the
six-skill cap holds — all 13 new contract surfaces map into the
existing six skills via mirrors. Executors must escalate via
`needs_user_input` before adding, removing, merging, or renaming any
of these. Naming follows the existing `crux-skill-memory-{verb}`
convention.

| # | Directory | `SKILL.md` `name` | `description` (one sentence) | Scope | Contract items owned (freeze §) | Callers | Cross-skill deps |
|---|-----------|-------------------|------------------------------|-------|---------------------------------|---------|------------------|
| 1 | `.cursor/skills/crux-skill-memory-meditation-research/` | `crux-skill-memory-meditation-research` | Research-mode meditation protocol: Phases A–G depth-first recursion, depth-0 manager steps 1–13 (incl. step 4b 4-mode focus-area reconciliation + `init-suggestions-{ts}.yml` write; step 8 K10c reflection writing `finalisation-enhancements.yml`; step 8b respawn-payload prep), facet registry lock, citations index, peer review file spec, comprehensiveness honouring at leaf depth (`verbatim_quotes` at `detailed`+). Use when the meditation guide agent runs the depth-0 manager or any Research-mode child agent. | Research-only executable contract | §1 (Research mode row), §2.6 combined Pattern-B (Research depth-0 subagent side), §2.7 `comprehensiveness:` propagation (Research path), §2.8 `Q-Finalisation-Enhancements` (K10c in-pass reflection — Research), §4.1 depth-0 steps 1–13, §4.2 Phases A–G + leaf comprehensiveness honouring, §4.4 (Research column of differences table), §4.6 4-mode focus-area reconciliation (Research write side, step 4b), §4.7 `init-suggestions-{ts}.yml` schema (Research write side), §4.8 K10c reflection rubric + 11-type catalogue (Research single-model `finalisation-enhancements.yml` schema), §5.4 facet registry lock, §5.5 citations index, §5.6 peer review file spec | `crux-cursor-meditation-guide` (Research workflows) | `meditation-coordination` (filename grammar incl. new richness rows, polling), `meditation-review` (handoff at step 10; bundles cheap accepted enhancements into iter 1 respawn payload), `meditation-report` (handoff at step 12; consumes `comprehensiveness`, `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`) |
| 2 | `.cursor/skills/crux-skill-memory-meditation-quick/` | `crux-skill-memory-meditation-quick` | Quick-mode meditation protocol: 6-step parallel fan-out with optional deep-confirm hook, warn-only citation validation, upfront child derivation, no peer review. Quick-mode K10c reflection (same rubric, same gate, warn-only at every richness level per K7). Use when the meditation guide agent runs the Quick depth-0 manager or any Quick-mode child agent. | Quick-only executable contract | §1 (Quick mode row), §2.6 combined Pattern-B (Quick depth-0 subagent side), §2.7 `comprehensiveness:` propagation (Quick path), §2.8 `Q-Finalisation-Enhancements` (K10c in-pass reflection — Quick; K10 fires in Quick at all 4 richness levels per K7 + OQ #5), §4.3 Quick 6-step protocol + leaf comprehensiveness honouring, §4.4 (Quick column of differences table), §4.6 4-mode focus-area reconciliation (Quick write side, step 4b), §4.7 `init-suggestions-{ts}.yml` schema (Quick write side), §4.8 K10c reflection rubric (Quick variant — same rubric, warn-only citation regime carried through), Quick relaxations referenced in §4.9 review and §6 report | `crux-cursor-meditation-guide` (Quick workflows) | `meditation-coordination`, `meditation-review`, `meditation-report` |
| 3 | `.cursor/skills/crux-skill-memory-meditation-ensemble/` | `crux-skill-memory-meditation-ensemble` | Ensemble Aggregation function: read N model consolidations, write `cross-model-synthesis.md`, perform K10 root cross-model reflection (step 3c), read per-tree `finalisation-enhancements.yml` files (step 3b) and write root combined YAML with `cross_model_candidates` + `union_candidates` (step 3d) with `surfaced_to_root` write-back, return single combined `needs_user_input` (step 3e), resume-handler dispatch by `source` provenance (step 3f) including K10 Ensemble Respawn Targeting (per-tree vs cross-model report targeting), hand off to the report skill for ensemble report HTML+PDF generation. Use when the meditation guide agent is spawned with `ensembleAggregation: true`. | Cross-model synthesis + K10 layered cadence | §4.5 Ensemble Aggregation function (steps 1, 2, 3 unchanged + new 3b/3c/3d/3e/3f K10 steps + step 5 with `pending_spawn_now`), §6.12 ensemble report extras + K10 Ensemble Respawn Targeting, §6.13 Ensemble layered cadence summary (per-tree write-only + single combined root gate; model-label fallback) | `crux-cursor-meditation-guide` (Ensemble Aggregation function); **never** loaded by per-model tree agents — the coordinator command owns model-pool enumeration and the per-tree spawn loop | `meditation-report` (for the ensemble HTML+PDF and per-tree respawns), `meditation-coordination` (ensemble working-dir layout + per-tree `finalisation-enhancements.yml` filename row + root `finalisation-enhancements.yml` filename row) |
| 4 | `.cursor/skills/crux-skill-memory-meditation-review/` | `crux-skill-memory-meditation-review` | Adversarial Review function: **13-dimension** audit (incl. citation integrity, slop detection, anti-homogenisation drift, level-conditional Dim 9 peer-review thoroughness, Dim 12 Comprehensiveness fidelity, Dim 13 Init-suggestion AND finalisation-enhancement honour), severity classification (MUST_FIX / SHOULD_FIX / ADVISORY), ≤3-iteration loop (shared between standard review and respawn cycles; max useful respawns = 2), MUST_FIX `needs_user_input` schema with mandatory `context` decision-guidance, Dim 13 `respawn_required: true` Report-Skill Respawn Protocol payload schema (K9 + K10b — `respawn_reasons` list-typed). Use when the meditation guide agent is spawned in Adversarial Review function (step 10). | Quality-gate only (+ Report-Skill Respawn Protocol authoring) | §4.9 Adversarial Review (reviewer agent / editable / read-only / never-touched files, 13 dimensions verbatim, severity classification, Quick relaxations, iteration loop with Dim 13 respawn branch, MUST_FIX `needs_user_input` schema with mandatory `context`, review document format), §6.10 Report-Skill Respawn Protocol (respawn payload schema with `respawn_reasons` list, per-reason processing order, iteration accounting, Pattern-B integrity for Dim 13 bypass), §6.11 Reviewer escalation Pattern-B with mandatory decision-guidance | `crux-cursor-meditation-guide` (Adversarial Review function spawned by research/quick step 10) | `meditation-coordination` (review document filename + Branch & Leaf Index link); **schema mirror only into `meditation-report`** for the respawn-handler resume-handler protocol (skill:review authors the payload; skill:report consumes and renders) — no circular dep because review must finish constructing the payload before report skill runs |
| 5 | `.cursor/skills/crux-skill-memory-meditation-report/` | `crux-skill-memory-meditation-report` | Mandatory paired HTML+PDF report generation: anti-homogenisation rules, Universal Contrast, light/dark mode + print TOC, **Comprehensiveness Level Mapping (12 dimensions × 4 levels)**, **Per-Branch Section Rule + Depth-3 Leaf Inclusion Rule + Peer-Review Surfacing Rule (level-conditional)**, **Init-Suggestions Honour rules** (read `init-suggestions-{ts}.yml`; mandatory floor-not-ceiling), **K10b Per-Cheap-Type Rendering Contract (7 cheap types)**, **Report-Skill Respawn Protocol resume-handler** (per-reason processing order; fuzzy-match auto-resolve), Chart.js / D3 / calculator content minimums driven by `comprehensiveness.minima.*` with static-fallback contracts, headless Chrome → Chromium degradation chain, Subject-Matter Focus rule for `consolidation.md` and reports, footer annotation extension (`level:` always written; `finalisation-enhancements:` segment when ≥1 accepted; ensemble split rule). Use when the meditation guide agent runs report generation (step 12), when the ensemble aggregator generates the ensemble-level report, or when the report skill is respawned via Dim 13. | Report-only (+ respawn handler) | §6.1 Comprehensiveness Level Mapping (12×4 table + `compact` backwards-compat anchor + subagent-abort rule), §6.2 paired rule, §6.3 anti-homogenisation, §6.4 Universal Contrast, §6.5 light/dark + print TOC + Chromium chain, §6.6 Chart.js / D3 / calculator + static fallback (level-driven minima) + accepted-cheap-counts-toward-minima rule, §6.7 Per-Branch / Depth-3 / Peer-Review Surfacing rules, §6.8 Init-Suggestions Honour (with backwards-compat fallback when YAML absent), §6.9 K10b Per-Cheap-Type Rendering Contract (7 types: `executive_summary`, `action_plan`, `risks_section`, `glossary`, `decision_tree_infographic`, `reader_persona_tldrs`, `cross_branch_synthesis_section` — payload shapes + landing locations + static degradation), §6.10 Report-Skill Respawn Protocol resume-handler (per-reason processing order; ensemble Per-Branch vs cross-model targeting via `source: "tree:{model-subdir}"` vs `"cross_model"`), §6.12 ensemble report extras (footer extension), §8 Subject-Matter Focus rule (applies to `consolidation.md` + reports) | `crux-cursor-meditation-guide` (research / quick step 12), `meditation-ensemble` (ensemble report generation; per-tree + cross-model targeting) | `meditation-coordination` (report filename grammar — never hard-code; respawn fresh-timestamp rule); consumes Dim 13 respawn payload authored by `meditation-review` |
| 6 | `.cursor/skills/crux-skill-memory-meditation-coordination/` | `crux-skill-memory-meditation-coordination` | File-based coordination primitives: artefact filename grammar (**18 rows** post-richness including `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`, `{model-subdir}/finalisation-enhancements.yml`, `follow-up-meditation-{ts}.yml`, `follow-up-spec-{ts}.yml`, `follow-up-memories-{ts}.yml`, `follow-up-expansion-{ts}.yml`), placeholders (`{topic-slug}`, `{slug}`, `{ts}`, `{N}/{D}/{S}`), prefix-glob polling rule (incl. `ls -1t \| head -n 1`), never-hard-code-`report.{html,pdf}` invariant, retrospective template, Branch & Leaf Index template (single-model + ensemble; **extended `## Top-level artifacts` block with init-suggestions / finalisation-enhancements / follow-up rows**). Use whenever the meditation guide agent reads, writes, or links a working-directory artefact. | Coordination grammar, polling, retro, B&L index | §5.1 artefact filename table (18 rows), §5.2 placeholders, §5.3 prefix-glob polling rule, §5.7 retrospective template, §5.8 Branch & Leaf Index template (incl. new top-level artefact rows); ensemble working-directory layout from §5.9 (the directory tree only — report extras stay in `meditation-report`) | All five other meditation skills + `crux-cursor-meditation-guide` directly | None — this is the leaf utility skill |

**Approved name set (no substitutions without `needs_user_input`)**:

```text
crux-skill-memory-meditation-research
crux-skill-memory-meditation-quick
crux-skill-memory-meditation-ensemble
crux-skill-memory-meditation-review
crux-skill-memory-meditation-report
crux-skill-memory-meditation-coordination
```

**Six-skill cap verdict (2026-05-24 refresh)**: **KEPT AT 6.** All 13
new richness surfaces map into the existing six skills via mirrors —
no seventh skill is required. The richness spec's own architecture
design §13 row #17 explicitly chose to extend `meditation-coordination`
rather than introduce `crux-skill-memory-meditation-finalisation`,
matching this design's cap. See §7 R9 for the full rationale.

**Eval discoverability anchors** (subtask 03 will plug these into the
substring-presence assertions):

- Each `SKILL.md` `description` field contains the literal substring `meditation`.
- Each directory name contains the literal substring `crux-skill-memory-meditation-`.
- Each `SKILL.md` `name` frontmatter equals the directory name (existing convention enforced by `evals/conftest.py`).
- The new agent file's frontmatter contains the literal substring `crux-cursor-meditation-guide`.
- The skill descriptions collectively contain (across the six files) the substrings: `Phases A–G`, `Quick`, `Ensemble`, `13-dimension`, `Comprehensiveness Level Mapping`, `Per-Cheap-Type`, `Report-Skill Respawn Protocol`, `init-suggestions`, `finalisation-enhancements`, `additional_focus_areas` (canonical, with `treatment:`).

---

## 3. Section-Mapping Table — Freeze Contract → Destination

The table below has **one row per contract item** in
`meditate-frozen-contract-20260524.md` Sections 1–8 (the new freeze
line). Every row has **exactly one primary** destination. Items that
must appear in both the agent and a skill (e.g. the agent body cites a
schema owned by a skill) are marked with the primary destination and
one-or-more mirror destinations.

Legend:
- `command` = `.cursor/commands/crux-meditate.md`
- `agent` = `.cursor/agents/crux-cursor-meditation-guide.md`
- `skill:<name>` = `.cursor/skills/crux-skill-memory-meditation-<name>/SKILL.md`
- "mirror" rows are non-canonical pointers that reference the primary by path. Mirrors are listed for cross-reference convenience only; only the primary destination owns the verbatim contract text. Where a contract is intrinsically mode-split (e.g. Research vs Quick output schema), it is presented as **two separate rows**, each with its own single primary.

### 3.1 Section 1 — Modes Inventory

| Contract item | Primary | Mirror(s) |
|---------------|---------|-----------|
| Research mode row + per-tree agent counts (~45 / ~72 at depth 3 by richness) | `command` (modes table + depth-richness table) | `agent` (invocation variants pointer) |
| Quick mode row + Quick per-tree count (~42 at depth 3 across all 4 levels) | `command` (modes table + depth-richness table) | `agent` (invocation variants pointer) |
| Ensemble + Research row (N×per-tree + 1 aggregator) | `command` (modes table + Ensemble Protocol) | — |
| Ensemble + Quick row (N×Quick per-tree + 1 aggregator) | `command` (modes table + Ensemble Protocol) | — |
| **Richness × depth × mode cost table** (§1.1 of new freeze — `compact` / `default` / `detailed` / `exhaustive` rows; `compact` reproduces pre-richness behaviour byte-for-byte) | `command` (verbatim, embedded in `Q-Cost-and-Richness-Acknowledgment` prompt body) | — |
| **`compact` backwards-compat anchor** (legacy behaviour available as opt-in) | `command` (verbatim Cost gate body + Comprehensiveness Level Mapping table) | `skill:report` (Comprehensiveness Level Mapping `compact` row reproduces pre-richness output) |
| Mode-selection logic (flag detection, slug stripping) | `command` (`### Argument Handling`) | — |
| Internal/non-user-facing invocation forms (child / ensemble member / aggregation) | `agent` (invocation variants table) | `skill:research` and `skill:quick` reference these in input-parameter sections |
| Argument forms (no-args / quoted / @-refs / mixed) | `command` (`### Argument Handling`) | — |
| `flags.enableMemories` feature guard | `agent` (Critical Rules — Feature Guards) | `skill:research` step 1 and `skill:quick` step 1 mirror as a precondition check |
| `cruxMemories.meditate.modelPool` config | `command` (Ensemble Protocol step 1) | `agent` (Ensemble Aggregation function loads `model` for self when `ensembleAggregatorModel` is set) |
| `cruxMemories.meditate.ensembleAggregatorModel` config | `command` (Ensemble Protocol step 9) | `skill:ensemble` documents the override semantics |
| **`cruxMemories.meditate.finalisationEnhancements.{minimumImpactThreshold,weights,formula}` config** (NEW per K10 OQ #11/#12 — proposed defaults documented in agent file even though not wired into shipping `.crux/crux-memories.json`) | `agent` (K10 reflection function preamble — defaults documented) | `skill:research` + `skill:quick` (K10c rubric consumers); `skill:ensemble` (K10 root reflection); subtask 10 owns the eventual shipping-defaults wiring |
| `maxDepth` propagation rule | `command` (`### Depth Selection`) | `agent` (mode router preamble — propagation is invariant for every child spawn) |
| `meditateMode` propagation rule | `command` (`### Argument Handling`) | `agent` (mode router preamble) |
| `confirmDeepFacets` propagation rule | `command` (`### Facet Confirmation`, now Sub-Q5 of combined Pattern-B) | `skill:research` (Phase C deep-confirm hook) + `skill:quick` (step 2) |
| `ensembleMode` flag semantics | `command` (`### Argument Handling`) | — |
| `selectedRichness` calling-agent-local state (tracks Sub-Q1; preserved across Sub-Q2 mode swaps; locked across expansion continuations) | `command` (verbatim Cost-and-Richness gate behaviour rules) | — |

### 3.2 Section 2 — Calling-Agent Gates

| Contract item | Primary | Mirror(s) |
|---------------|---------|-----------|
| `Q-Depth-Selection` prompt + options + behaviour rules | `command` (verbatim) | — |
| **`Q-Cost-and-Richness-Acknowledgment` merged depth × richness × mode gate (replaces legacy `Q-Cost-Acknowledgment`)** — Sub-Q1 (4-level richness, preselected = `default`), Sub-Q2 (proceed/swap/cancel; mode-swap preserves richness; set-once-per-invocation rule) | `command` (verbatim, including the 4-row cost table embedded in the prompt prose) | — |
| `Q-Cost-and-Richness-Acknowledgment` ensemble first-paragraph replacement | `command` (verbatim, ensemble branch) | — |
| **`Q-Cost-Acknowledgment-Expansion` read-only-richness variant** (replaces legacy expansion variant; richness displayed locked; "keep deep-confirm setting?" follow-up preserved) | `command` (verbatim, expansion branch in §2.3 + generalised read-only-richness rules in §2.4) | — |
| Read-only-richness variant — 3 trigger preambles (expansion / additional-facet acceptance / `spawn_now` acceptance) | `command` (verbatim §2.4 table) | — |
| Theme Preflight Q1 (theme source) + Q1b (repo-scan confirm) | `command` (verbatim) | — |
| Theme Preflight Q2 (style direction, 8 presets) | `command` (verbatim) | — |
| Theme Preflight Q3 (colour scheme) | `command` (verbatim) | — |
| Theme Preflight Q4 (typography) | `command` (verbatim) | — |
| Theme Preflight Q5 (confirmation + `restart_preflight` + `cancel_meditation`) | `command` (verbatim) | — |
| `surprise_me` non-interactive fallback (Q1+Q2 deterministic seeding by topic-slug) | `command` (verbatim) | — |
| Theming payload (verbatim YAML schema) | `command` (verbatim) | `agent` (abort-with-error rule when payload missing); `skill:report` (consumed in every visual decision) |
| **`comprehensiveness:` payload propagation** (Pattern A — passed alongside `theming:`; schema includes `level`, `minima.*`, 6 dimension fields; subagent abort with canonical error string `"comprehensiveness: payload required; missing from spawn prompt — caller misconfigured"` if missing at any depth in any mode) | `agent` (mode router preamble — same shape and abort rule as `theming:`; **canonical error string lives here**) | `command` (verbatim payload YAML in `### Theme Preflight — MANDATORY` propagation subsection); `skill:research` step 4 / step 5 input contract (receive + propagate); `skill:quick` step 3 / step 5 input contract (receive + propagate); `skill:report` (consumed at every visual decision); `skill:ensemble` (per-tree propagation) |
| **Combined Pattern-B Facet / Sections / Visualisations / Focus-Areas / Deep-Confirm** (replaces legacy sequential Q-Confirm-1 + Q-Confirm-2): single `needs_user_input` with 5 sub-questions; subagent-side schema with `prompt_inputs.{facets,sections,visualisations,additional_focus_areas,deep_confirm}` and `resume_handler_contract.expected_input.additional_focus_areas_decisions[].treatment` (canonical name — see row #6 below) | `command` (verbatim Pattern-B trigger + 5-sub-Q askQuestion schema + resume handler + cost-change check) | `skill:research` (step 4 — Research depth-0 derives 4 blocks; writes `facets-pending-{ts}.yml`); `skill:quick` (step 4 — Quick depth-0 mirrors derivation contract) |
| Deep-facet `pending-facets-*.yml` schema | `command` (verbatim, deep-confirm flow) | `skill:coordination` (filename row only); `skill:research` Phase C and `skill:quick` step 2 cite it |
| Deep-facet `confirmed-facets-*.yml` schema | `command` (verbatim) | Same mirror pattern |
| Per-child decision semantics (`confirmed` / `modified` / `regenerate` with 3-regen cap) | `command` (verbatim) | `skill:research` + `skill:quick` (poll-loop owners) |
| Depth-0 polling protocol (batch `pending-facets-*.yml` into a single `needs_user_input` block) | `command` (verbatim) | `skill:research` step 6 + `skill:quick` step 5 own the poll loop |
| Re-spawn / continuation semantics (new meditation always re-runs depth-0 facet confirm) | `command` (verbatim) | — |
| **`Q-Finalisation-Enhancements` gate (K10a)** — Pattern-B post-consolidation pre-adversarial; multi-select 0–5; per-item treatment sub-Q for expensive items (`queue` default vs `spawn_now` opt-in); `spawn_now` cost-ack re-presentation; `finalisation-enhancements.yml` update flow; **K10b mixed-cost taxonomy (7 cheap types + 4 expensive types)**; **K10c `finalisation-enhancements.yml` update flow**; **K10 ensemble Respawn Targeting orchestration**; **ensemble layered cadence askQuestion is calling-agent-side per K4**; layered cadence root-gate semantics (single combined askQuestion at root) | `command` (verbatim — Pattern-B askQuestion, per-item treatment sub-Q, cost-ack re-presentation, file update flow) | `skill:research` + `skill:quick` (in-pass K10c reflection writing `finalisation-enhancements.yml` — see also §3.4 step 8 / 8b rows); `skill:ensemble` (layered cadence steps 3b–3f + Per-Cheap-Type per-target dispatch); `skill:report` (K10b Per-Cheap-Type Rendering Contract for the 7 cheap types + Report-Skill Respawn Protocol resume-handler payload consumer); `skill:coordination` (`finalisation-enhancements.yml` filename row + ensemble per-tree filename row + 4 `follow-up-{type}-{ts}.yml` filename rows) |

**Rationale**: every gate that requires `AskQuestion` is forbidden inside
subagent trees by the project-wide rule (`AGENTS.md`). All five Theme
Preflight questions, both Cost-and-Richness Sub-Qs (including all three
read-only-richness triggers), the combined Pattern-B 5-sub-Q askQuestion,
the depth-selection question, the `Q-Finalisation-Enhancements` multi-select
+ per-item treatment sub-Qs, and the continuation menu therefore stay on
the **command** as the single source of truth. Skills only reference these
schemas — they never duplicate the verbatim prompt text, which prevents
drift.

### 3.3 Section 3 — Pattern A vs Pattern B Boundaries

| Contract item | Primary | Mirror(s) |
|---------------|---------|-----------|
| Pattern A list (depth, cost-and-richness, theme preflight, surprise_me fallback, ensemble pool read, `comprehensiveness:` payload) | `command` (Pattern boundary section) | `agent` (User Input Escalation block restates Pattern A / Pattern B / `needs_user_input` schema) |
| Pattern B list (combined Facet/Sections/Viz/Focus-Areas/Deep-Confirm, cost re-presentation on additional-facet acceptance, MUST_FIX, `Q-Finalisation-Enhancements`, ensemble layered combined gate, continuation menu) | `command` | `agent` (User Input Escalation block) |
| "Subagents NEVER call AskQuestion" rule | `agent` (Critical Rules — restated verbatim) | `skill:review` (MUST_FIX escalation cannot call `askQuestion`; Dim 13 respawn bypass does not call `askQuestion` either); `skill:research` and `skill:quick` (deep-confirm escalation + combined Pattern-B escalation + K10c `needs_user_input` from step 8); `skill:ensemble` (single combined root gate `needs_user_input` from step 3e) |
| `needs_user_input` schema (generic) | `agent` (User Input Escalation block — verbatim mirror of `AGENTS.md`) | All five executable skills cite the schema by reference, never duplicate it |
| `needs_user_input` mandatory `context` field for MUST_FIX (Dim 1–12) | `skill:review` (verbatim schema with required `context`) | `command` (Adversarial Review subsection points at the skill) |
| **Dim 13 `respawn_required: true` BYPASSES standard ambiguous `MUST_FIX` `needs_user_input`** — reviewer constructs structured deterministic respawn payload (no user input) | `skill:review` (verbatim Report-Skill Respawn Protocol payload schema + bypass rule) | `command` (one-paragraph mention in Adversarial Review pointer; `skill:report` is the consumer) |
| **K10b cheap-enhancement bundling** — multiple cheap items bundle into single respawn payload's `accepted_finalisation_enhancements:` list (one respawn, one iteration consumed); the `accepted_finalisation_enhancements` cause fires at most once per meditation | `skill:review` (respawn payload schema bundle rule) | `command` (`Q-Finalisation-Enhancements` resume documents the bundle); `skill:report` (consumes bundled payload, processes in §6.10 per-reason order) |

### 3.4 Section 4 — Subagent Contracts

| Contract item | Primary | Mirror(s) |
|---------------|---------|-----------|
| §4.1 Research input parameters (`meditateMode`, `workingDir`, `branchNumber`, `meditateDepth`, `maxDepth`, `subfocus`, `subfocusSlug`, `subfocusIndex`, `parentSubfocus`, `siblingFacets`, `theming`, **`comprehensiveness`** [REQUIRED — abort if missing], `confirmDeepFacets`, `ensembleModel?`) | `skill:research` (input contract) | `agent` (mode router preamble — high-level only; canonical error string for missing `comprehensiveness`) |
| §4.1 Phase A (research own subfocus, query memory index, cite every claim) | `skill:research` (verbatim) | — |
| §4.1 Phase B (write findings file; **leaf-depth `verbatim_quotes` at `detailed`+ honouring**) | `skill:research` (verbatim) | `skill:coordination` (filename row referenced) |
| §4.1 Phase C (derive 3 children + deep-confirm hook + registry lock + collision refinement) | `skill:research` (verbatim) | `skill:coordination` (registry lock semantics); `skill:research` references `skill:coordination`'s `pending-facets-*.yml` filename grammar |
| §4.1 Phase D (spawn 3 children + propagate `theming`, **`comprehensiveness`**, `confirmDeepFacets`, `ensembleModel?`) | `skill:research` (verbatim) | — |
| §4.1 Phase E (prefix-glob, citation validation, 2-retry respawn) | `skill:research` (verbatim) | `skill:coordination` (prefix-glob rule); Research-mode strict citation validation lives in `skill:research` |
| §4.1 Phase F (rewrite incorporation, `[child: …]` markers, contradictions section, **`comprehensiveness.minima.section_length_budget_tokens` ceiling honouring**) | `skill:research` (verbatim) | — |
| §4.1 Phase G (promote `-findings` draft → final filename) | `skill:research` (verbatim) | `skill:coordination` (filename row) |
| §4.1 Leaf-depth Phase A+B only (with comprehensiveness honouring) | `skill:research` (verbatim) | — |
| **§4.1 Output body sections list (8 mandatory `##` sections) — Research output schema** | `skill:research` (verbatim) | `agent` (high-level reminder only); `skill:quick` cross-references for the shared section list |
| **§4.1 Output body sections list (8 mandatory `##` sections) — Quick output schema** | `skill:quick` (verbatim — same 8 sections; mode-specific differences are in the differences-table rows below) | `agent` (high-level reminder only); `skill:research` cross-references |
| §4.1 Frontmatter schema (verbatim 10-field YAML) | `skill:research` (verbatim — single source of truth) | `skill:quick` cites it with `mode: "quick"` override |
| **§4.1 depth-0 manager steps 1–13 — Research workflow** (incl. step 4b 4-mode focus-area reconciliation + `init-suggestions-{ts}.yml` write; step 8 K10c reflection writing `finalisation-enhancements.yml`; step 8b respawn-payload prep + `pending_spawn_now` accumulation; step 13 returns `pending_spawn_now`) | `skill:research` (verbatim) | `agent` (mode router lists step numbers + one-paragraph summary per step) |
| §4.1 `preConfirmedFacets` ensemble shortcut at step 4 + shared init-suggestions payload propagation | `skill:research` (verbatim) | `skill:ensemble` (one-paragraph confirmation that per-model trees receive `preConfirmedFacets` + shared init-suggestions) |
| **§4.3 Quick 6-step protocol (input parameters incl. mandatory `comprehensiveness`; all 6 steps; leaf path with comprehensiveness honouring)** | `skill:quick` (verbatim) | `agent` (mode router lists steps + one-paragraph summary each) |
| **§4.4 Quick vs Research differences — Research column** (Research-side cells of the differences table: peer review at depth 1, mandatory citations, registry lock used) | `skill:research` (verbatim — Research column) | `agent` (one-paragraph pointer only); `skill:quick` cross-references for the Quick column |
| **§4.4 Quick vs Research differences — Quick column** (Quick-side cells of the differences table: no peer review, warn-only citations, no registry lock, upfront child derivation) | `skill:quick` (verbatim — Quick column) | `agent` (one-paragraph pointer only); `skill:research` cross-references for the Research column |
| **§4.5 Ensemble Aggregation function (spawn parameters, 5-step workflow, K10 layered cadence steps 3b–3f, step 5 with `pending_spawn_now`)** | `skill:ensemble` (verbatim) | `agent` (mode router §1.3 row 7 lists the parameters + step numbers + K10 cadence reminder) |
| **§4.5 K10 layered cadence — per-tree YAML write semantics (`source_tree:`, `surfaced_to_root: null` placeholder; per-tree YAMLs are write-only at the per-tree level — NO per-tree askQuestion fires)** | `skill:ensemble` (verbatim — step 3b + per-tree YAML schema) | `skill:research` + `skill:quick` (per-tree depth-0 manager writes `{model-subdir}/finalisation-enhancements.yml` before returning to aggregator); `skill:coordination` (filename row) |
| **§4.5 K10 root cross-model reflection (step 3c — runs in SAME LLM pass as `cross-model-synthesis.md`; cross-tree convergence calibration; `cross_model_candidates` ranked ≤5)** | `skill:ensemble` (verbatim) | — |
| **§4.5 K10 root combined YAML write (step 3d — `cross_model_candidates` + `union_candidates` with `source: "tree:{model-subdir}" | "cross_model"`; `surfaced_to_root` write-back to per-tree YAMLs)** | `skill:ensemble` (verbatim) | — |
| **§4.5 K10 single combined root gate (step 3e — single `needs_user_input` at ensemble root; option labels include provenance; model-label fallback to `"Unknown model ({model-subdir})"`)** | `skill:ensemble` (verbatim — schema + recommended-posture rationale) | `command` (calling-agent-owned orchestration of the askQuestion stays calling-agent-side per K4) |
| **§4.5 K10 ensemble resume-handler (step 3f — dispatch by `source` provenance to per-tree vs ensemble-root targets; cheap respawn payload routing; expensive `queue` follow-up file location; expensive `spawn_now` `pending_spawn_now` accumulation per target)** | `skill:ensemble` (verbatim) | `command` (ensemble respawn loop fires after step 5 return) |
| **§4.5 Non-infinite-loop guarantee (per-tree reflections bounded by `modelPool` size; root reflection once; single root gate once; per-tree adversarial reviews each ≤3; cross-model adversarial review ≤3; O(N) total)** | `skill:ensemble` (verbatim) | — |
| **§4.6 4-mode `additional_focus_areas[]` reconciliation (canonical post-W1b schema: array + per-item `treatment:` filter — `skip` / `additional_facet` / `report_section_only` / `additional_facet_AND_section`) — Research write side (step 4b)** | `skill:research` (verbatim — Research path of step 4b) | — |
| **§4.6 4-mode `additional_focus_areas[]` reconciliation — Quick write side (step 4b — same canonical schema; same 4 treatments)** | `skill:quick` (verbatim — Quick path of step 4b) | — |
| **§4.6 Cost-ack re-presentation rule on `additional_facet` / `additional_facet_AND_section` acceptance (calling-agent-owned)** | `command` (verbatim — combined Pattern-B `cost_change_check` + read-only-richness re-presentation) | `skill:research` + `skill:quick` (step 4b proceeds only after `cost_reack_confirmed: true` resume payload) |
| **§4.7 `init-suggestions-{ts}.yml` production — write side (depth-0 manager step 4b after combined Pattern-B resolves; schema with `confirmed_sections` + `confirmed_visualisations` + `additional_focus_areas` with canonical `treatment:` field + audit metadata)** | `skill:research` (verbatim — Research scouting writes the file) | `skill:quick` (Quick scouting writes the file with same schema); `skill:coordination` (filename row); `skill:report` (read side — see §3.6 Init-Suggestions Honour) |
| **§4.7 `init-suggestions-{ts}.yml` schema invariants (`resulting_section_id` iff `treatment ∈ {report_section_only, additional_facet_AND_section}`; `resulting_branch_index` iff `treatment ∈ {additional_facet, additional_facet_AND_section}`; `custom_report_section_title` iff `treatment == additional_facet_AND_section`; `compact`/`default` `additional_facet`-only → branch but NO section per K4 carve-out)** | `skill:research` (verbatim — single source of truth for the schema invariants) | `skill:quick` cross-references the invariants; `skill:report` honours them at render time |
| **§4.8 K10c reflection rubric (impact × insight-value 1–10 each; composite multiplicative or weighted-sum; `minimum_impact_threshold` default 6; top-5 selection with tie-break preferring `cheap`; graceful degradation)** | `skill:research` (verbatim — single-model rubric authority) | `skill:quick` cross-references (same rubric); `skill:ensemble` cross-references for per-tree + root cross-model reflection; `agent` mode router K10 row gives a one-paragraph reminder |
| **§4.8 K10c candidate type catalogue (7 cheap + 4 expensive = 11 total)** — payload shapes per type | `skill:research` (verbatim — single source of truth for the catalogue) | `skill:quick` cross-references; `skill:ensemble` cross-references; `skill:report` consumes the 7 cheap payload shapes via the K10b Per-Cheap-Type Rendering Contract (see §3.6 row) |
| **§4.8 `finalisation-enhancements.yml` schema (single-model variant) — frontmatter (rubric metadata + `degradation_reason`) + `candidates[]` (`id`, `type`, `cost_class`, `title`, `description`, `impact_score`, `insight_value_score`, `composite_score`, `source_signals`, `payload`, `accepted`, `treatment`, `decided_at_utc`)** | `skill:research` (verbatim — single-model write side) | `skill:quick` cross-references (same schema); `skill:coordination` (filename row only); `skill:ensemble` for the ensemble extension (per-tree + root combined variants — owned in `skill:ensemble`) |
| **§4.9 Adversarial Review reviewer agent contract** (fresh, clean context, inputs `meditateMode`, `reviewerIteration ∈ {1,2,3}`, `workingDir`, `theming`, **`comprehensiveness`**, `priorReviewPath?`) | `skill:review` (verbatim) | `agent` (mode router §1.3 row 6 — one-paragraph spawn summary) |
| §4.9 Editable / read-only / never-touched file lists | `skill:review` (verbatim) | — |
| **§4.9 Dimensions 1–11 (verbatim — unchanged from 20260517 freeze)** | `skill:review` (verbatim) | — |
| **§4.9 Dimension 9 level-conditional expansion (Research only; peer-review surfacing per `comprehensiveness.peer_review_surfacing`: `consolidation_only` / `named_section` / `per_branch_dedicated`)** | `skill:review` (verbatim) | `skill:report` (mirror — surfaces the named sections per Peer-Review Surfacing Rule) |
| **§4.9 Dimension 12 — Comprehensiveness fidelity** (chart / infographic / calculator counts ≥ minima; per-branch section depth matches; peer-review surfacing matches; `depth3_leaf_inclusion` honoured) — `MUST_FIX`, in-place rewrite, does NOT trigger respawn | `skill:review` (verbatim) | — |
| **§4.9 Dimension 13 — Init-suggestion AND finalisation-enhancement honour** (every `confirmed_sections[i].title` present with substantive body; every `confirmed_visualisations[i].type` rendered with non-empty data; every `finalisation-enhancements.yml.candidates[i]` with `accepted: true, treatment: respawn` rendered per K10b contract; ensemble layered audit — per-tree-sourced audited against per-tree report, cross-model-sourced audited against cross-model synthesis report) — `MUST_FIX` AND `respawn_required: true`, bypasses standard in-place fix flow | `skill:review` (verbatim) | `skill:report` (consumes the resulting respawn payload — see §3.6 Report-Skill Respawn Protocol row) |
| §4.9 Severity classification (MUST_FIX / SHOULD_FIX / ADVISORY — unchanged) | `skill:review` (verbatim) | — |
| §4.9 Quick-mode relaxations (citation-marker downgrade + peer-review N/A; Dim 12 still applies; Dim 13 still applies) | `skill:review` (verbatim, Quick branch) | `skill:quick` (one-paragraph pointer) |
| **§4.9 Iteration loop (cap 3 shared between standard review and respawn cycles; `respawn_required: true` handling branch; same-iteration Dim 1–11 fix THEN Dim 13 respawn ordering; maximum useful respawns per meditation = 2; `ESCALATE` semantics)** | `skill:review` (verbatim) | — |
| **§4.9 Reviewer Pattern-B respawn-with-decision-guidance MUST_FIX schema (mandatory `context` field) + Report-Skill Respawn Protocol (K9 + K10b)** — respawn payload schema with `respawn_reasons` LIST-typed (`missing_init_suggestion_sections`, `missing_init_suggestion_visualisations`, `accepted_finalisation_enhancements`), `missing_sections[]`, `missing_visualisations[]`, `accepted_finalisation_enhancements[]`, `preserve_other_content`, `comprehensiveness_payload`, `init_suggestions_payload`, `theming_payload`, `finalisation_enhancements_payload` | `skill:review` (verbatim — single source of truth for payload schema authoring) | `skill:report` (resume-handler protocol per-cheap-type processing order: enhancements → visualisations → sections, with fuzzy-match auto-resolve in either direction; iteration accounting; fresh-timestamp output filename rule) |
| §4.9 Review document format (filename + frontmatter + required sections) | `skill:review` (verbatim) | `skill:coordination` (review-iteration filename row); Branch & Leaf Index template lists review iterations |

### 3.5 Section 5 — Coordination Conventions

| Contract item | Primary | Mirror(s) |
|---------------|---------|-----------|
| §5.1 Artefact filename table (**18 rows** post-richness: facets-pending, facets, init-suggestions-{ts}, branch, branch-findings, peer-review, pending-facets, confirmed-facets, review iteration, finalisation-enhancements (single-model), finalisation-enhancements (ensemble per-tree), 4 × follow-up-{type}-{ts}, retrospective, report HTML, report PDF) | `skill:coordination` (verbatim) | `command` (Coordination Conventions subsection now becomes a single-paragraph pointer); `agent` (mode router preamble points at the skill) |
| §5.2 Placeholders (`{topic-slug}`, `{slug}`, `{ts}`, `{N}/{D}/{S}`) | `skill:coordination` (verbatim) | Same mirror pattern |
| §5.3 Prefix-glob polling rule + `ls -1t \| head -n 1` resolution + never-hard-code rule | `skill:coordination` (verbatim) | `command` and `agent` cite the skill |
| **§5.4 Facet registry schema** (verbatim YAML) — single primary, no "OR" | `skill:research` (verbatim — the registry exists **only** in Research mode; the operational protocol lives where it is used) | `skill:coordination` (filename row only — note "Research mode only") |
| §5.4 `mkdir`-based lock-and-append protocol (verbatim bash) | `skill:research` (verbatim) | `skill:coordination` only carries the lockfile-name row |
| §5.4 Orphan-recovery rule (5-min stale-lock `rmdir`) | `skill:research` (verbatim) | `skill:coordination` (poll-loop side note) |
| **§5.5 Inline citation markers — Research strict variant** (`[memory:…]` / `[file:…]` / `[web:…]` / `[chat:…]` / `[child:…]` mandatory; respawn 2-retry on validation failure) | `skill:research` (verbatim — Research strict regime) | — |
| **§5.5 Inline citation markers — Quick warn-only variant** (same marker vocabulary; warn-only validation; "Citation gaps" callout in consolidation) | `skill:quick` (verbatim — Quick warn-only regime) | — |
| §5.5 `citations-index.yml` schema | `skill:research` (verbatim — Research mode only artefact) | `skill:coordination` (filename row only — note "Research mode only") |
| **§5.5 Validation enforcement — Research path** (strict respawn 2-retry on missing/invalid citations; parent Phase E respawns the failing child) | `skill:research` (verbatim — Research path) | — |
| **§5.5 Validation enforcement — Quick path** (warn-only; "Citation gaps" callout in consolidation; parent does NOT respawn — invariant across all 4 richness levels per K7) | `skill:quick` (verbatim — Quick path) | — |
| §5.6 Peer review file spec (filename, frontmatter, 5 required `##` sections: `## Reinforcements` / `## Contradictions` / `## Gaps` / `## New Evidence` / `## Citations`) | `skill:research` (verbatim — Research mode only) | `skill:coordination` (filename row only) |
| **Peer-review explicit report sections at `detailed`+ (rendering side: `named_section` at `detailed`; `per_branch_dedicated` at `exhaustive` — adds Cross-Branch Reinforcements / Contradictions / Gaps named sections; `per_branch_dedicated` adds one per branch)** | `skill:report` (verbatim — Peer-Review Surfacing Rule rendering side) | `skill:research` (peer-review file spec — the data source; mirror only — `skill:research` does NOT own the rendering rule) |
| §5.7 Retrospective template (frontmatter + 6 mandatory `###` sections; always written including on `ESCALATE`) | `skill:coordination` (verbatim) | `agent` (mode router references it from step 12b) |
| §5.8 Branch & Leaf Index template (single-model variant + ensemble variant; extended `## Top-level artifacts` block with rows for `[Init suggestions](init-suggestions-{ts}.yml)`, `[Finalisation enhancements](finalisation-enhancements.yml)`, 4 × `[Follow-up: …](follow-up-{type}-{ts}.yml)`) | `skill:coordination` (verbatim) | `command` (existing block now becomes a pointer); `agent` (step 9 / step 11 references the template) |
| §5.8 Conventions (label = subfocus_slug, depth-3 grouping, missing-slots enumeration, Quick / `ESCALATE` omissions) | `skill:coordination` (verbatim) | — |
| §5.8 Pending coordination files never linked | `skill:coordination` (verbatim) | — |
| §5.9 Ensemble working directory structure (verbatim tree — extended with per-tree `finalisation-enhancements.yml` and root `finalisation-enhancements.yml`) | `skill:coordination` (verbatim — extension of §5 filename grammar) | `skill:ensemble` (one-paragraph pointer); `command` (Ensemble Protocol points at the skill) |

### 3.6 Section 6 — Mandatory Report Contract

| Contract item | Primary | Mirror(s) |
|---------------|---------|-----------|
| **§6.1 Comprehensiveness Level Mapping (12 dimensions × 4 levels — `minima.charts.count/types_required`, `minima.infographics.count/types_required`, `minima.calculators.count/scenarios_per`, `depth3_leaf_inclusion`, `per_branch_section_depth`, `citation_density`, `peer_review_surfacing`, `section_length_budget_tokens`, `ensemble_cross_model_depth`); `compact` reproduces pre-richness behaviour byte-for-byte; subagent-abort rule (canonical error string) when payload missing** | `skill:report` (verbatim — single source of truth for the 12×4 mapping at render time) | `skill:research` + `skill:quick` (per-level leaf honouring at depth-3 — `verbatim_quotes` at `detailed`+; `section_length_budget_tokens.per_facet` ceiling); `agent` (canonical error string also restated in Critical Rules) |
| §6.2 Paired HTML+PDF rule (`{ts}` capture, filename grammar, never hard-code; respawn writes fresh-timestamp pairs via prefix-glob latest-wins) | `skill:report` (verbatim) | `command` (Report Generation pointer); `skill:coordination` (filename rows) |
| §6.3 Anti-Homogenisation Rules (forbidden defaults list, canonical screenshot reference, application rules — applies verbatim at every comprehensiveness level per K7) | `skill:report` (verbatim) | `command` (Theme Preflight subsection retains a one-paragraph context citing the skill) |
| §6.4 Universal Contrast (min contrast requirements, hard rules, CSS variables — applies verbatim at every level per K7) | `skill:report` (verbatim) | — |
| §6.5 Light + Dark mode + responsive nav | `skill:report` (verbatim) | — |
| §6.5 Print TOC + print theme (verbatim CSS rules) | `skill:report` (verbatim) | — |
| §6.6 Chart.js types + D3 types facet table + CDN allowlist + infographics list + **level-driven minima** (`comprehensiveness.minima.*` placeholders resolve at runtime; accepted cheap enhancements count toward minima) | `skill:report` (verbatim) | — |
| §6.6 D3 print degradation table (6 patterns) + HTML/CSS implementation pattern | `skill:report` (verbatim) | — |
| §6.6 Calculator static-fallback (level-driven scenarios floor; forbidden states; verification gate) | `skill:report` (verbatim) | — |
| §6.6 Report Comprehensiveness — No Information Loss | `skill:report` (verbatim) | — |
| §6.6 Option Comparison Research Reporting (activation, 5 required elements) | `skill:report` (verbatim) | — |
| **§6.7 Per-Branch Section Rule** (`consolidation_only` / `branch_summary` / `per_leaf_detail`; `additional_facet` and `additional_facet_AND_section` branches honour the rule; `additional_facet_AND_section` honours `custom_report_section_title` at `detailed`+) | `skill:report` (verbatim) | — |
| **§6.7 Depth-3 Leaf Inclusion Rule** (`summary` / `verbatim_quotes`) | `skill:report` (verbatim) | `skill:research` (depth-3 leaf agents write per the rule at Phase B) |
| **§6.7 Peer-Review Surfacing Rule** (`consolidation_only` / `named_section` / `per_branch_dedicated`; Quick mode no-op with "Peer review not applicable in Quick mode" placeholder at higher levels) | `skill:report` (verbatim) | `skill:research` (peer-review file spec is the data source) |
| **§6.8 Init-Suggestions Honour rules** (mandatory floor; confirmed sections appear with substantive body; confirmed visualisations rendered with non-empty data; `treatment: report_section_only` entries become report sections with rationale prose at section top; floor-not-ceiling rule; backwards-compat fallback when YAML absent; audit cross-link to Dim 13) | `skill:report` (verbatim) | `skill:research` + `skill:quick` (write side of `init-suggestions-{ts}.yml`); `skill:coordination` (filename row); `skill:review` Dim 13 (audit side) |
| **§6.9 K10b Per-Cheap-Type Rendering Contract (7 types: `executive_summary`, `action_plan`, `risks_section`, `glossary`, `decision_tree_infographic`, `reader_persona_tldrs`, `cross_branch_synthesis_section` — landing locations + payload shapes consumed + static degradation rules; risks_section/decision_tree count toward `comprehensiveness.minima.infographics.count`)** | `skill:report` (verbatim) | `skill:review` Dim 13 (audit each accepted cheap enhancement against its contractual rendering); `command` (`Q-Finalisation-Enhancements` resume documents which types are cheap) |
| §6.6 Headless Chrome render command + URLSearchParams detection + fallback chain (`chromium`, `chromium-browser`) | `skill:report` (verbatim) | — |
| §6.6 No-Chromium failure mode (clear error + platform install hint + leave HTML in place) | `skill:report` (verbatim) | `command` (step 9 verification gate restates the surface-install-hint rule for the calling agent's display) |
| §6.6 Final verification (`ls -1t … head -n 1` + `[ -s "${LATEST}" ]`) | `skill:report` (verbatim) | `command` (step 9 verification gate) |
| **§6.10 Report-Skill Respawn Protocol resume-handler — per-reason processing order (1. `accepted_finalisation_enhancements` → 2. `missing_init_suggestion_visualisations` → 3. `missing_init_suggestion_sections` with fuzzy-match auto-resolve when step 1 covers a step-3 entry); fresh-timestamp output filename; iteration accounting (≤3 shared cap, max useful respawns = 2; `accepted_finalisation_enhancements` cause fires at most once per meditation); same-iteration Dim 1–11 fix THEN respawn ordering** | `skill:report` (verbatim — resume-handler protocol) | `skill:review` (authors the payload — see §3.4 row); `skill:coordination` (fresh-timestamp filename rule); `command` (Adversarial Review pointer mentions respawn handoff) |
| §5.9 Ensemble working-directory structure | `skill:coordination` (verbatim — see §3.5 row) | `skill:ensemble` (one-paragraph pointer); `command` (Ensemble Protocol points at the skill) |
| §6.12 Ensemble filename conventions table | `skill:coordination` (verbatim) | — |
| §6.12 `cross-model-synthesis.md` frontmatter + 8 mandatory `##` sections | `skill:ensemble` (verbatim) | — |
| §6.12 Ensemble report structural extras (model comparison hero, per-facet cards, agreement heatmap, divergence deep-dives, per-model drill-down links, model attribution Sankey + citation Venn + confidence radar, model-attribution citation format `[model: label]` / `[models: all]`) | `skill:ensemble` (verbatim) | `skill:report` (one-paragraph mention that ensemble extras layer **on top of** standard mandatory minimums) |
| **§6.12 Footer annotation extension** (`level:` always written from this spec forward; `finalisation-enhancements: N (type1, type2, …)` segment when ≥1 accepted; skip-all path OMITS the segment entirely — must NOT write `finalisation-enhancements: 0`; ensemble split: per-tree reports enumerate only per-tree-sourced accepts; cross-model report enumerates only cross-model-sourced accepts) | `skill:report` (verbatim — footer extension is a report-rendering concern) | `skill:ensemble` (cross-references the split rule for ensemble report rendering) |
| **§6.12 K10 Ensemble Respawn Targeting (per-tree-sourced accept targets per-tree report respawn; cross-model accept targets cross-model synthesis report respawn; per-tree reports NOT respawned for cross-model accepts; cross-model report NOT respawned for per-tree accepts; cost-ack re-presentation prose names which subsystems gain agents at which level for `spawn_now`)** | `skill:ensemble` (verbatim — the routing/targeting rule is an ensemble concern) | `command` (ensemble respawn loop) |
| **§6.12 Dim 13 layered audit at ensemble** (per-tree-sourced enhancement audited against per-tree report only; cross-model enhancement audited against cross-model synthesis report only; mismatched-report missing is NOT a finding) | `skill:review` (verbatim — audit rule) | `skill:ensemble` (cross-references the rule); `skill:report` (rendering target side) |
| **§6.13 Ensemble layered K10 cadence (per-tree write-only `{model-subdir}/finalisation-enhancements.yml`; root cross-model reflection writes combined YAML with `cross_model_candidates` + `union_candidates`; single combined root `askQuestion` at ensemble root; capped 0–5 multi-select; provenance labels in option prose; model-label fallback; skip-all reproduces today's behaviour byte-for-byte at every richness level)** | `skill:ensemble` (verbatim — single source of truth for the cadence) | `command` (orchestration of the layered-cadence root `askQuestion` stays calling-agent-side per K4); `skill:research` + `skill:quick` (per-tree manager writes per-tree YAML before returning to aggregator) |

### 3.7 Section 7 — Continuation Menu

| Contract item | Primary | Mirror(s) |
|---------------|---------|-----------|
| §7.1 Single-model step 9 verification gate (verbatim bash) | `command` (verbatim) | `skill:report` (final verification) |
| §7.2 Single-model step 10 (present, absolute paths, ESCALATE branch, follow-up reminder) | `command` (verbatim) | — |
| §7.3 Single-model step 11 (sample prompt, multi-select options, forbidden `save_html` / `save_pdf` options) — **extended K10c groups**: "Expansion directions" / "Apply un-chosen enhancements" (one option per `unchosen_persisted` item) / "Spawn queued follow-ups" (one option per queued expensive item) / "Other" (save_spec, end_meditation) | `command` (verbatim) | — |
| §7.4 Single-model step 12 (expansion / save_spec / end_meditation handlers + **K10c new handlers**: `reapply_enhancement_{id}` re-runs Q-Finalisation-Enhancements with single item pre-checked; `spawn_queued_{id}` triggers read-only-richness cost-ack re-presentation `spawn_now` variant then spawns) | `command` (verbatim) | — |
| §7.5 Ensemble step 10 verification (synth + ensemble HTML/PDF + per-tree + root `finalisation-enhancements.yml`) | `command` (verbatim, Ensemble Protocol) | — |
| §7.5 Ensemble step 11 (present cross-model synthesis + surface root-YAML unchosen + per-tree-only unchosen with provenance labels) | `command` (verbatim) | — |
| §7.5 Ensemble step 12 (per-model expansion options + save_spec + end_meditation + K10c per-tree-only item targets per-tree report respawn) | `command` (verbatim) | — |
| §7.5 Ensemble step 13 (expansions run single-model unless `--ensemble` re-passed) | `command` (verbatim) | — |

### 3.8 Section 8 — Subject-Matter Focus Rule

| Contract item | Primary | Mirror(s) |
|---------------|---------|-----------|
| Forbidden list (no Branch N labels, no depth/leaf/agent refs, no raw `[child:…]` in consolidation+reports, no peer-review-actor framing, no process-framing in executive summaries) | `skill:report` (verbatim — applies to `consolidation.md` and HTML/PDF reports) | `skill:research` step 8 (consolidation construction must translate `[child: …]` → `[research: {subfocus-slug}]`); `skill:quick` step 6 (Quick consolidation also follows the rule); `skill:review` dimension 11 (audits the rule) |
| Required substitutions (facet titles, subfocus descriptions, by-name cross-references, lead-with-substance executive summary) | `skill:report` (verbatim) | Same mirror pattern |
| Scope carve-out (rule applies to `consolidation.md` + HTML/PDF only; internal coordination files retain process-oriented naming) | `skill:report` (verbatim) | `skill:coordination` (carve-out cited in the retrospective and Branch & Leaf Index templates) |

### 3.9 Section 9 — Cross-Repo Touchpoints

Section 9 of the freeze contract is informational (current cross-repo
references that subtask 09 / subtask 10 must update). No row in §9 is
**owned** by the new agent/skills/command — they describe **existing**
external touchpoints. Subtask 09 (docs sync) and subtask 10 (install /
dist / release) own the updates listed in §9. The design doc does not
re-table §9 here; it only flags that the new
`crux-cursor-meditation-guide.md` file and the six new skill
directories must be **added** to:

1. `install.py` `MEMORY_FILE_PREFIXES` and the fallback file list (subtask 10)
2. `scripts/create-crux-zip.py` `DIST_FILES` (subtask 10)
3. `.crux/dist-manifest.json` (subtask 10, regenerated)
4. `.github/workflows/version-bump.yml` `RELEASE_PATHS` (subtask 10, if needed)
5. `CONTRIBUTORS.md` agent + skill tables (subtask 09)
6. `README.md` agent / skill listings (subtask 09)
7. `AGENTS.md` Available Agents table + Spec Execution Agent Allocation table (subtask 09) — add a new row for the guide agent and a "Recursive meditation (Research / Quick / Ensemble / Adversarial Review)" allocation row
8. `docs/crux-memories.md` agent narrative (subtask 09)
9. `web/compress.md/memories.html` agent + skill labels (subtask 09)

The `zip-contents-protection` rule's "explicit user authorisation"
requirement is **satisfied** by spec K7 (this spec carries the
authorisation). Subtask 10 may proceed.

The 2026-05-24 refresh notes that the richness spec
`specs/20260523-meditate-richness/` S07 has already extended
`README.md`, `docs/crux-memories.md`, and `web/compress.md/memories.html`
with richness coverage (the `## Refresh` row of the patch matrix
documents this). Subtask 09 must **integrate** with those existing
extensions rather than duplicate — the agent + skill listings are
additive on top of the richness-extended docs. See §6.5 of this
design.

CRUX-compressed mirror regeneration (subtask 11) is unchanged from
freeze §9: `.cursor/rules/crux-memories-integration.crux.mdc`,
`.cursor/rules/docs-sync.crux.mdc`, `.cursor/rules/version-bump.crux.mdc`,
`.cursor/rules/zip-contents-protection.crux.mdc`. **No new mirror
coverage** is created (spec K8). `AGENTS.crux.md` is not maintained and
must not be created (spec K8 restated).

---

## 4. Coordinator Command Shape — Post-Decomposition `/crux-meditate`

### 4.1 Sections retained on `.cursor/commands/crux-meditate.md`

The table below uses section-heading anchors as the stable key, with
current line ranges (post-richness, 2142-line command) in parentheses.
Each row is marked `unchanged` / `shrunk` / `modified` relative to the
pre-decomposition state.

| # | Section heading (anchor) | Current lines | Planned action | Notes |
|---|--------------------------|--------------:|----------------|-------|
| 1 | `# crux-meditate` header + repo link | 1–5 | unchanged | — |
| 2 | `## Usage` CLI examples (5 forms) | 7–18 | unchanged | — |
| 3 | `## Modes` summary table | 20–28 | unchanged | — |
| 4 | `## Instructions` (Pattern B intro + 5-gate intro [4 pre-spawn + Q-Finalisation-Enhancements] + new spawn target) | 30–36 | **modified** | One-line edit: spawn target text changes from `crux-cursor-memory-manager` to `crux-cursor-meditation-guide` |
| 5 | `### Argument Handling` (flag detection + slug stripping + remaining-args matrix) | 38–53 | unchanged | — |
| 6 | `### Depth Selection — MANDATORY` (`Q-Depth-Selection` + agent-count table + behaviour rules) | 55–105 | unchanged | — |
| 7 | `### Cost & Scope Acknowledgment — MANDATORY` (**`Q-Cost-and-Richness-Acknowledgment` merged gate, preamble, 4-row cost table, Sub-Q1 4-level richness, Sub-Q2 proceed/swap/cancel, behaviour rules incl. set-once-per-invocation, ensemble first-paragraph replacement, read-only-richness variant for expansion + cost-re-presentation + spawn_now triggers + 3 trigger preambles**) | 106–256 | unchanged | All five askQuestion-bearing prompts stay on the command |
| 8 | `### Theme Preflight — MANDATORY` (Anti-Homogenisation context, Q1–Q5, surprise_me fallback, theming YAML, **`comprehensiveness:` payload propagation YAML at lines 361–390**) | 257–390 | unchanged | The Anti-Homogenisation Rules canonical block in §6.3 moves to `skill:report`; the **context paragraph** introducing why Theme Preflight exists stays here. The `comprehensiveness:` payload propagation YAML block (lines 361–390) stays here because the calling agent serialises it pre-spawn (Pattern A) |
| 9 | `### Facet Confirmation — MANDATORY at depth 0, opt-in deeper` (**combined Pattern-B askQuestion with 5 sub-questions: facets / sections / visualisations / additional_focus_areas with `treatment:` filter / deep_confirm + cost-change check + read-only-richness re-presentation + resume-handler 1-4 sequence + deep-facet pending/confirmed schemas**) | 391–738 | unchanged | The combined askQuestion stays here in its entirety. Subagent-side `needs_user_input` schema is mirrored (not duplicated) by `skill:research` / `skill:quick` |
| 10 | `### Coordination Conventions` (filename table 18 rows + polling globs + never-hard-code rule) | 740–784 | **shrunk** to a one-paragraph pointer at `skill:coordination` | Reduces command by ~40 lines |
| 11 | `### What Happens` workflow chooser | 786–791 | unchanged | — |
| 12 | `#### Research mode (default)` (steps 1–8 substitutions) | 792–821 | **shrunk** to a one-paragraph pointer at `skill:research` | Reduces from ~30 lines to ~10 |
| 13 | `#### Quick mode (--quick)` (steps 1–8 substitutions) | 823–845 | **shrunk** to a one-paragraph pointer at `skill:quick` | Same pattern |
| 14 | `#### Ensemble mode (--ensemble)` (Ensemble Protocol steps 1–10 calling-agent block + per-tree aggregator spawn loop + ensemble-specific steps 9–13) | 847–919 | unchanged (orchestration is calling-agent-side per K4) | The aggregator-spawn parameters gain a one-paragraph pointer at `skill:ensemble` for the spawn-receiver contract; the calling-agent flow stays verbatim |
| 15 | `**Steps 9–12: Calling-agent block (both modes, single-model)**` (verify report pair + present + continuation menu with **K10c groups** + handle selection with **K10c handlers**) | 921–986 | unchanged | Pattern A / Pattern B integrity preserved; K10c groups + handlers stay calling-agent-side |
| 16 | `### Branch & Leaf Index` template (extended with init-suggestions + finalisation-enhancements + follow-up rows) | 988–1059 | **shrunk** to a one-paragraph pointer at `skill:coordination` | The template lives in the skill |
| 17 | **`### Finalisation Enhancements Gate — Q-Finalisation-Enhancements (K10a)`** (gate prompt + multi-select 0–5 + per-item treatment sub-Q + spawn_now cost-ack re-presentation + update flow + K10b Per-Cheap-Type Rendering Contract pointer + K10 Ensemble Respawn Targeting + Ensemble layered cadence summary) | 1062–1186 | **shrunk** to a one-paragraph pointer at `skill:research` / `skill:quick` for the in-pass K10c reflection contract + `skill:ensemble` for layered cadence + `skill:report` for K10b rendering | **NEW section post-richness.** The askQuestion + per-item treatment sub-Q + cost-ack re-presentation orchestration **STAYS on the command** (calling-agent-side per K4 — these require `AskQuestion`). The K10c reflection contract, K10b Per-Cheap-Type Rendering Contract, K10 Ensemble Respawn Targeting, and Ensemble layered cadence move to skills. The command retains a six-line summary pointing at each skill. |
| 18 | `### Adversarial Review and Fix Cycle — MANDATORY` (reviewer agent contract + **13 dimensions** + severity + iteration loop with Dim 13 respawn branch + Pattern-B MUST_FIX schema + review document format + Quick relaxations + **Report-Skill Respawn Protocol (K9 + K10b)**) | 1187–1447 | **shrunk** to a one-paragraph pointer at `skill:review` (+ `skill:report` for the respawn resume-handler) | The verbatim ~260-line block moves; the command retains a five-line summary stating the cycle is mandatory, owns 13 dimensions, has Report-Skill Respawn Protocol for Dim 13, uses MUST_FIX `needs_user_input` schema with mandatory `context` field |
| 19 | `### Subject-Matter Focus — MANDATORY (all user-facing outputs)` | 1448–1468 | **shrunk** to a one-paragraph pointer at `skill:report` | The verbatim rule moves into `skill:report` because that is where the rule is enforced (during report generation) |
| 20 | `### Process Retrospective — MANDATORY` | 1470–1537 | **shrunk** to a one-paragraph pointer at `skill:coordination` | The template moves |
| 21 | `### Report Generation — MANDATORY` (filenames + inputs + HTML structural elements + **Comprehensiveness Level Mapping table 12×4 at lines 1545–1571** + Report Comprehensiveness + Option Comparison + visualisations + infographics + interactive elements + **Per-Branch Section Rule** + **Depth-3 Leaf Inclusion Rule** + **Peer-Review Surfacing Rule** + **Init-Suggestions Honour at lines 1807–1821** + anti-homogenisation + theming application + Universal Contrast + light/dark + responsive nav + PDF requirements + filename pairing + print theme + TOC + render command + final verification + **footer annotation extension**) | 1539–1977 | **shrunk** to a one-paragraph pointer at `skill:report` | The verbatim ~440-line block moves wholesale to the skill |
| 22 | `### Ensemble Aggregation Report — MANDATORY (when ensembleMode is true)` (ensemble working dir + filename conventions + cross-model synthesis schema + ensemble report extras + model-attribution citations) | 1979–2132 | **shrunk** to a one-paragraph pointer at `skill:ensemble` (+ `skill:report` for shared report contracts) | The verbatim ~154-line block moves |
| 23 | `## Related` (links to agent + skills + sibling commands) | 2134–2142 | **modified** | Agent link points at new `crux-cursor-meditation-guide` and lists the six new meditation skills. The Memory Manager link can stay (it still owns Dream/REM/Recall/Remember/Forget) |

**Newly introduced sections post-richness** (already present in the
2142-line command; marked above as **modified** or stay verbatim):

| Anchor | Approximate lines | Disposition |
|--------|-------------------|-------------|
| `Q-Cost-and-Richness-Acknowledgment` preamble + cost table + Sub-Q1 + Sub-Q2 | 106–208 | unchanged on command (Pattern A askQuestion) |
| `Q-Cost-Acknowledgment-Expansion` read-only-richness variant | 210–256 | unchanged on command (Pattern A askQuestion) |
| `comprehensiveness:` payload YAML propagation block | 361–390 | unchanged on command (Pattern A pre-spawn serialisation) |
| Combined Pattern-B Facet/Sections/Viz/Focus-Areas/Deep-Confirm gate + resume handler | 391–738 | unchanged on command (Pattern B askQuestion) |
| `Q-Finalisation-Enhancements` gate + treatment sub-Q + update flow | 1062–1186 | shrunk via pointer; askQuestion stays on command per K4 |
| Adversarial Review extended to 13 dims + Report-Skill Respawn Protocol | 1187–1447 | shrunk to a pointer |
| Comprehensiveness Level Mapping table | 1545–1571 | included in the moved Report Generation block (→ `skill:report`) |
| Init-Suggestions Honour rules | 1807–1821 | included in the moved Report Generation block (→ `skill:report`) |

### 4.2 Command line-budget projection

| Source block | Current lines (in 2142-line command) | Planned lines | Δ |
|--------------|-------------------------------------:|--------------:|---:|
| Coordination Conventions (§10) | 45 | 5 | −40 |
| Research mode steps 1–8 (§12) | 30 | 10 | −20 |
| Quick mode steps 1–8 (§13) | 23 | 8 | −15 |
| Branch & Leaf Index template (§16) | 72 | 5 | −67 |
| Finalisation Enhancements Gate (§17 — internals moved; askQuestion stays) | 125 | 30 | −95 |
| Adversarial Review cycle (§18) | 261 | 12 | −249 |
| Subject-Matter Focus (§19) | 21 | 4 | −17 |
| Process Retrospective (§20) | 68 | 4 | −64 |
| Report Generation (§21) | 439 | 10 | −429 |
| Ensemble Aggregation Report (§22) | 154 | 6 | −148 |
| Comprehensiveness Level Mapping table (inside §21 — moves with Report Generation) | 27 | 0 | counted in §21 |
| Init-Suggestions Honour (inside §21 — moves with Report Generation) | 15 | 0 | counted in §21 |
| **Total command shrink** | **~1480** | **~104** | **≈ −1376 lines** |

The remaining ~660–680 command lines are exactly the Pattern A gates +
Pattern B coordinator menu + Q-Finalisation-Enhancements gate + the
combined Pattern-B 5-sub-Q askQuestion — the surface that
legitimately needs to live on the command file because it requires
`AskQuestion` and must never enter a subagent.

**Target post-refactor command size**: **~650 lines** (vs current 2142
lines, ~70 % shrink). The result is a **thin coordinator** per spec
K1, even with the K10a finalisation-enhancements askQuestion + per-item
treatment sub-Q + the combined Pattern-B 5-sub-Q askQuestion preserved
verbatim.

**Deletable surface from the command** (~1480 lines total):
Coordination Conventions, Branch & Leaf Index, the Adversarial Review
cycle, Subject-Matter Focus, Process Retrospective, Report Generation,
Ensemble Aggregation Report, the Comprehensiveness Level Mapping
table, and the Report-Skill Respawn Protocol contract. The orchestration
of askQuestion calls + per-item treatment sub-Qs + cost-ack
re-presentations + continuation menu **stay**.

### 4.3 New `Task` spawn signature for the guide agent

The coordinator command spawns the guide agent at `### Instructions`
(currently "spawn a `crux-cursor-memory-manager` subagent in Meditate
mode"). After decomposition:

#### 4.3.1 Single-model spawn (Research or Quick, depth-0 manager)

```text
Task(
  subagent_type: "crux-cursor-meditation-guide",
  description: "Meditate: {topic-slug-or-context-summary}",
  prompt: """
  You are the depth-0 manager for a /crux-meditate invocation.

  Pre-collected gate answers (Pattern A):
  - meditateMode: "research" | "quick"
  - maxDepth: 1 | 2 | 3
  - theming: { … full theming payload from Theme Preflight … }
  - comprehensiveness: { … full payload per §2.7 of the freeze … }   # REQUIRED
  - parentContext: { conversation summary, open files, recent activity }
  - stripped $ARGUMENTS: "{flag-stripped topic / refs}"

  Follow the Research-mode depth-0 workflow in
  `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md`
  (or `.cursor/skills/crux-skill-memory-meditation-quick/SKILL.md`
  when meditateMode == "quick").

  Coordination grammar:
  `.cursor/skills/crux-skill-memory-meditation-coordination/SKILL.md`

  Escalation: subagents NEVER call AskQuestion. Escalate via Pattern B
  `needs_user_input` when:
   - combined facet/sections/viz/focus-areas/deep-confirm at step 4
   - deep-facet pending files (when confirmDeepFacets != none)
   - K10c `Q-Finalisation-Enhancements` at step 8 (after consolidation)
   - MUST_FIX findings the adversarial reviewer cannot auto-apply

  Abort with the canonical error string if `comprehensiveness:` is
  missing from this prompt:
   `comprehensiveness: payload required; missing from spawn prompt — caller misconfigured`
  """,
  // No `model:` override on single-model spawn — guide agent uses its
  // default `model: claude-opus-4-6`.
)
```

#### 4.3.2 Ensemble member spawn (per-model tree, depth-0 manager)

```text
Task(
  subagent_type: "crux-cursor-meditation-guide",
  description: "Meditate (ensemble member {label}): {topic-slug}",
  prompt: """
  Same as 4.3.1, plus:
  - preConfirmedFacets: [ … 3 confirmed facets with citations … ]
  - sharedInitSuggestions: { … confirmed sections + visualisations + focus areas … }
  - confirmDeepFacets: "none" | "depth_2_only" | "all_levels"
  - ensembleModel: "{slug}"          // propagated to every child
  - ensembleModelLabel: "{label}"
  - workingDir: "{ensembleWorkingDir}/model-{label-slug}/"

  Skip step 4 derivation/confirmation — use preConfirmedFacets +
  sharedInitSuggestions verbatim per `skill:research` step 4 ensemble
  shortcut. Write `{model-subdir}/finalisation-enhancements.yml` after
  consolidation (no per-tree askQuestion — write-only). Return to the
  aggregator with `pending_spawn_now: []` (per-tree level does not yet
  spawn expensive items; aggregator coordinates across the tree set).
  """,
  model: "{slug}",   // e.g. "gpt-5.5-medium" — pinned per ensemble member
)
```

#### 4.3.3 Cross-model aggregation spawn (Ensemble Aggregation function)

```text
Task(
  subagent_type: "crux-cursor-meditation-guide",
  description: "Ensemble aggregation: {topic-slug}",
  prompt: """
  You are the cross-model synthesis agent. Function: ensembleAggregation.

  Inputs:
  - ensembleAggregation: true
  - ensembleWorkingDir: "{absolute path}"
  - modelSubdirs: [ { slug, label, subdirPath }, ... ]
  - confirmedFacets: [ … shared facets … ]
  - theming: { … shared payload … }
  - comprehensiveness: { … shared payload … }     # REQUIRED
  - meditateMode: "research" | "quick"
  - topicSlug: "{topic-slug}"

  Follow:
  `.cursor/skills/crux-skill-memory-meditation-ensemble/SKILL.md`

  K10 layered cadence: read per-tree `finalisation-enhancements.yml`
  files (step 3b), run K10 root cross-model reflection in the SAME LLM
  pass as `cross-model-synthesis.md` (step 3c), write root combined
  YAML with `cross_model_candidates` + `union_candidates` + write-back
  `surfaced_to_root` annotations (step 3d), return single combined
  `needs_user_input` (step 3e), apply resume handler with per-tree vs
  cross-model dispatch (step 3f).

  Report generation (ensemble HTML+PDF + per-tree report respawn
  targeting):
  `.cursor/skills/crux-skill-memory-meditation-report/SKILL.md`
  """,
  model: "{cruxMemories.meditate.ensembleAggregatorModel or caller's model}",
)
```

#### 4.3.4 Adversarial Review spawn (from inside the guide agent's step 10)

The adversarial reviewer is **spawned by the depth-0 guide agent**, not
by the coordinator command. The spawn signature is documented in
`skill:review`, but for completeness:

```text
Task(
  subagent_type: "crux-cursor-meditation-guide",
  description: "Adversarial review iter {N}: {topic-slug}",
  prompt: """
  You are the adversarial reviewer for a /crux-meditate cycle. Function:
  adversarialReview.

  Inputs:
  - meditateMode: "research" | "quick"
  - reviewerIteration: 1 | 2 | 3
  - workingDir: "{absolute path}"
  - theming: { … propagated payload … }
  - comprehensiveness: { … propagated payload … }     # REQUIRED for Dim 12
  - priorReviewPath: null | "{path to prior review-pre-report-*-iter-*.md}"
  - (ensemble only) model: ensembleModel propagated

  Follow:
  `.cursor/skills/crux-skill-memory-meditation-review/SKILL.md`

  When Dim 13 fires with `respawn_required: true`, construct the
  structured respawn payload per the Report-Skill Respawn Protocol;
  do NOT escalate via askQuestion for that finding. Standard ambiguous
  MUST_FIX (Dim 1–11 + Dim 12) findings still escalate via
  `needs_user_input` with mandatory `context`.
  """,
  // model override only when ensembleModel is set
)
```

### 4.4 Spawn-signature invariants

1. Every spawn carries `theming` unchanged (abort if missing per §2.5).
2. Every spawn except `ensembleAggregation` carries `meditateMode`, `maxDepth`, and `confirmDeepFacets`.
3. **Every spawn at every depth in every mode carries `comprehensiveness` unchanged** (abort with the canonical error string per §2.7 of the new freeze if missing). The set-once-per-invocation rule (K6) is enforced by the propagation invariant.
4. `model:` is set on `Task` **only** when ensemble member or ensemble aggregator (per spec K4 calling-agent surface).
5. `subagent_type` is always `crux-cursor-meditation-guide` after decomposition; the value `crux-cursor-memory-manager` no longer appears in any `/crux-meditate` spawn.
6. The skill path strings in each prompt are literal — preserve exactly as written (the project-wide `_CRUX-RULE.mdc` "Path Construction — CRITICAL" rule applies).

---

## 5. Memory-Manager Trim Plan — `.cursor/agents/crux-cursor-memory-manager.md`

### 5.1 Sections to DELETE (with replacement pointer paragraphs)

The 2026-05-24 refresh re-projects the deletion ranges against the
1388-line memory-manager file. The deletion ranges are **279–1159
(Meditate Mode)** and **1189–1349 (Ensemble Aggregation Mode)**,
totalling ~1041 lines. **Forget Mode now lives at lines 1160–1188**
(between the two deletion ranges) — see K4 risk in §7.3 for the
sharper callout.

| # | Heading | Line range | Replacement paragraph |
|---|---------|-----------:|------------------------|
| 1 | `### Meditate Mode — `/crux-meditate`` and **everything beneath it** through to the end of the section just before `### Forget Mode` | **279–1159** (Meditate Mode preamble, Coordination Conventions mirror, Research workflow steps 1–13 incl. step 4b + 8 + 8b, Quick top-level workflow, post-subagent flow, Recursive exploration protocol — Research Phases A–G with leaf comprehensiveness honouring, Recursive exploration protocol — Quick 6-step, Quick vs Research differences table, Facet registry protocol, Citations protocol, Peer review file spec, Subfocus narrowing example, Working directory structure, Output file format, Design principles list — ≈20 bullets incl. set-once-per-invocation richness + K10 reflection bounded) | **Replace with**:<br><br>`### Meditate Mode — moved`<br>`The `/crux-meditate` workflow now lives in the dedicated `crux-cursor-meditation-guide` agent (`.cursor/agents/crux-cursor-meditation-guide.md`) and the six `crux-skill-memory-meditation-*` skills (research, quick, ensemble, review, report, coordination). The coordinator command `.cursor/commands/crux-meditate.md` retains the five mandatory gates — Depth Selection, Cost-and-Richness Acknowledgment (merged depth × richness × mode per K2), Theme Preflight, combined Facet/Sections/Visualisations/Focus-Areas/Deep-Confirm Pattern-B gate, and the K10 Q-Finalisation-Enhancements gate (multi-select 0–5 post-consolidation pre-adversarial) — plus Ensemble Protocol orchestration, the post-tree continuation menu (with K10c groups), and the `comprehensiveness:` payload propagation. This agent's Memory Manager scope is **lifecycle only**: Dream, REM Sleep, Recall, Remember, and Forget. Meditate is no longer one of its responsibilities.` |
| 2 | `### Ensemble Aggregation Mode — (internal, spawned by calling agent's Ensemble Protocol)` and the **entire 5-step workflow + invocation parameter list + K10 layered cadence steps 3b–3f** | **1189–1349** | **Replace with**:<br><br>`### Ensemble Aggregation Mode — moved`<br>`Cross-model synthesis is now owned by `crux-cursor-meditation-guide` in its Ensemble Aggregation function. See `.cursor/skills/crux-skill-memory-meditation-ensemble/SKILL.md` for the verbatim 5-step workflow (with K10 layered cadence steps 3b–3f: per-tree `finalisation-enhancements.yml` read, K10 root cross-model reflection, root combined YAML write with `cross_model_candidates` + `union_candidates`, single combined `needs_user_input`, per-tree vs cross-model resume-handler dispatch), spawn parameters (including `comprehensiveness`), and report extras (including K10 Ensemble Respawn Targeting).` |
| 3 | `**Meditate**: Recursive memory-informed exploration and insight synthesis` bullet under `## Your Expertise` | (search by content; ≈line 57 in pre-richness; verify current line at S07 time) | **DELETE the line** (do not replace — Meditate is no longer in this agent's expertise). |
| 4 | `**Ensemble Aggregation**: Cross-model synthesis after parallel meditation trees complete` bullet under `## Your Expertise` | (search by content; ≈line 58 in pre-richness; verify current line at S07 time) | **DELETE the line** (same reason). |

**Total deletion**: ~1041 lines from the Meditate Mode + Ensemble
Aggregation Mode blocks (279–1159 + 1189–1349), plus the two expertise
bullets. Forget Mode (1160–1188) is **retained intact** between the
two deletion ranges.

### 5.2 Sections to RETAIN unchanged

| # | Heading | Line range | Why retained |
|---|---------|-----------:|--------------|
| 1 | Frontmatter | 1–6 | The agent's `name`, `model`, `description` remain valid for lifecycle work. The description currently lists "dream extraction, REM sleep rebalancing, conflict detection, compression, and Recall decompression" — Meditate is **not** in the description today. No edit needed. |
| 2 | Persona prologue | 7 | Generic — applies to lifecycle work |
| 3 | `## CRITICAL: Load Context First` | 9–16 | Generic — unchanged |
| 4 | `## User Input Escalation — CRITICAL` (Pattern A / Pattern B / `needs_user_input` schema) | 17–46 | **Generic and shared** — must remain on this agent because Dream / REM / Recall / Remember / Forget all use the same schema. Verbatim mirror exists on the new `crux-cursor-meditation-guide` per spec design (§1.2 step 3). No drift risk because both agents follow the schema in `AGENTS.md` lines 31–60. |
| 5 | `## Your Expertise` (minus the two deleted bullets) | 48–58 → 48–56 after deletions | Remaining bullets stay: Dream Extraction, REM Sleep, Recall, Conflict Detection, Memory Compression, Memory Removal, Reference Tracking |
| 6 | `## Skills You Use` | 60–71 | Lists only `crux-skill-memory-*` (extract, crud, rebalance, compress, reference-tracker, index) — none of these are meditation skills, so no edits needed |
| 7 | `## Operating Modes` header | 73 | unchanged |
| 8 | `### Dream Mode — `/crux-dream <spec-name>`` | 75–~120 | unchanged |
| 9 | `### REM Sleep Mode — `/crux-dream --rem`` | ~122–~155 | unchanged |
| 10 | `### Recall Mode — `/crux-recall`` | ~157–~244 | unchanged |
| 11 | `### Remember Mode — `/crux-remember`` | 245–277 | unchanged |
| 12 | **`### Forget Mode — `/crux-forget``** | **1160–1188** (post-richness location; was 843–870 pre-richness) | unchanged — retained even though physically appears between the two deleted sections; its content is unchanged. The deletion of §1 ends at line 1159, then `### Forget Mode` continues at line 1160 and ends at 1188, then deletion of §2 starts at line 1189. See K4 risk in §7.3 for the sharper callout. |
| 13 | `## Agent Scoping Rules` | 1351–1365 (post-richness) | Generic memory-scoping rules — unchanged. The `Writing Agent Memories` rule remains valid for the lifecycle scope; the new guide agent inherits the same self-exclusion (documented in its own `## Agent Scoping Rules` block — see §1.3 row 10 of this design). |
| 14 | `## Critical Rules` (Feature Guards, Data Integrity, Workflow Discipline, Skill Delegation) | 1367–1388 (post-richness) | Generic — unchanged |

### 5.3 Sections elsewhere on the file that REFERENCE Meditate

A grep of the trimmed file should leave **zero** references to the
literal string `Meditate`, `meditate`, `meditation`, or
`crux-meditate` after subtask 07 lands. The only acceptable residual
references are inside the **pointer paragraphs** added by §5.1
(items 1 and 2) — they explicitly direct readers to the new guide
agent and meditation skills.

Acceptance check for subtask 07:

```bash
rg -i "meditat|crux-meditate" .cursor/agents/crux-cursor-memory-manager.md
# Expected matches: exactly 2 paragraphs (the two pointer paragraphs)
```

### 5.4 Post-trim line budget

| Metric | Before (2026-05-24 working tree) | After |
|--------|---------------------------------:|------:|
| Total file lines | 1388 | ~360 |
| Meditate-related lines | ~1041 | ~10 (two pointer paragraphs incl. richness gate names) |
| Reduction | — | ~74 % |

---

## 6. Backwards-Compatibility Plan — Interim Window Between Subtasks 06 and 07

### 6.1 The window

The spec dependency graph places subtasks in this order:

```
S04 (guide agent file)
     → S06 (command refactor) → S07 (memory-manager trim)
S05 (skill files)
```

Between **the end of S06 and the start of S07**, the repository state
is:

- `.cursor/agents/crux-cursor-meditation-guide.md` exists (S04 created it).
- All six `.cursor/skills/crux-skill-memory-meditation-*/SKILL.md` exist (S05).
- `.cursor/commands/crux-meditate.md` has been refactored (S06) and spawns `crux-cursor-meditation-guide` — **not** `crux-cursor-memory-manager` — in its `### Instructions` section.
- `.cursor/agents/crux-cursor-memory-manager.md` **still contains** the full Meditate Mode + Ensemble Aggregation Mode sections (lines 279–1159 and 1189–1349) — they have not been removed yet.

### 6.2 Risk in the interim window

**No runtime risk**: the only consumer of `crux-cursor-memory-manager`'s
Meditate Mode sections is the `/crux-meditate` coordinator command. Once
S06 lands and the command spawns `crux-cursor-meditation-guide` instead,
the old Meditate sections on the memory manager are **dead code** —
still loaded into the memory manager's system prompt if the memory
manager is spawned for an unrelated reason (Dream / REM / Recall /
Remember / Forget), but no caller targets them.

**Potential drift risk**: a developer running an experimental
`Task(subagent_type: "crux-cursor-memory-manager", prompt: "do a meditation")` would still find a working contract. This is undesirable but
not catastrophic — it would behave as the pre-decomposition system.

### 6.3 Recommendation

**Option A (recommended)**: S06 adds a **one-paragraph pointer at the
top of the Meditate Mode section** on the memory manager file that
says:

> **DEPRECATED — moved to `crux-cursor-meditation-guide`.** This
> Meditate Mode section is preserved temporarily for backwards
> compatibility but is no longer the canonical contract.
> `/crux-meditate` now spawns `crux-cursor-meditation-guide` per
> `.cursor/commands/crux-meditate.md`. The verbatim contract lives in
> `.cursor/skills/crux-skill-memory-meditation-*/SKILL.md`.
> This section is removed by subtask 07.

That one-paragraph banner makes the deprecation explicit during the
short interim window. S07 then deletes the entire section per §5.

**Option B**: S06 and S07 are merged into one subtask. **Not
recommended** — it violates the spec's dependency graph (S07 depends
on S04 and S06) and would balloon the diff surface, making review
harder.

**Decision for subtask 02 (this design)**: **Option A is the chosen
path.** Subtask 06 will add the deprecation banner; subtask 07 will
remove the entire section. Both subtasks land within the same spec
execution, so the interim window is the duration between the two
status flips — typically minutes in autonomous execution.

### 6.4 Eval-suite interim compatibility

`evals/test_q_meditate.py` (now 1335 lines / 36 test classes), and
`evals/sdk/tests/q-meditate.test.ts` (now 576 lines / 7 describe
blocks) currently assert that `/crux-meditate` spawns
`crux-cursor-memory-manager`. **Subtask 03** (eval & test plan) and
**subtask 08** (eval & test update) own migrating those assertions to
expect `crux-cursor-meditation-guide`. The migration is single-atomic
per-test-file edit and lands in subtask 08 — after subtask 06 has
flipped the spawn target. There is **no window** where the command
spawns the guide agent but the evals still assert the old name,
because the dependency graph orders S03 → S08 after S06.

`evals/test_p_amnesia.py` is unchanged from the 20260517 freeze (the
richness spec did not touch it).

### 6.5 Coordination with the 20260523 richness patch matrix (NEW per 2026-05-24 refresh)

The completed sibling spec `specs/20260523-meditate-richness/` has
already shipped the 13 new contract surfaces into the source files.
Implementers MUST consult its design doc as a **secondary authoritative
input** when handling richness-touched rows in this design's §3:

| 20260523 reference | Reading required | Subtasks that need it |
|--------------------|------------------|-----------------------|
| `specs/20260523-meditate-richness/meditate-richness-architecture-design-20260523.md` §11 (init-suggestions schema) | Cross-reference the canonical `additional_focus_areas[]` schema with `treatment:` field (post-W1b — the legacy `_skipped` / `_accepted` field names are dead and must not return) when implementing the 4-mode reconciliation rows in S04 (agent body) and S05 (`skill:research` + `skill:quick`) | S04, S05 |
| `specs/20260523-meditate-richness/meditate-richness-architecture-design-20260523.md` §13 (patch matrix, 21 rows) | Cross-reference per-surface ownership decisions when implementing skill bodies. The patch matrix's row #17 architectural decision (extend `meditation-coordination` rather than create `meditation-finalisation`) is **affirmed** by this design's six-skill cap (§7 R9) | S04, S05 |

**Eval coverage preservation** (S08 acceptance criteria post-refresh):

- S08 MUST preserve the **30 new pytest classes** (28 net new + 2
  refactored counting modes) in `evals/test_q_meditate.py` introduced
  by richness S06 (lines 293–1308 of the 1335-line file).
- S08 MUST preserve the **4 new TS describe blocks** (22 new `it`
  tests) in `evals/sdk/tests/q-meditate.test.ts` introduced by
  richness S06 (lines 400–574 of the 576-line file).
- S08 may rename `TestMeditateAgentSpawning::test_*` assertions to
  expect `crux-cursor-meditation-guide` instead of
  `crux-cursor-memory-manager`, but otherwise must not delete any
  pre-existing richness assertions.

**Docs sync coordination** (S09 acceptance criteria post-refresh):

- S09 MUST integrate with the README / `docs/crux-memories.md` /
  `web/compress.md/memories.html` extensions already written by
  richness S07 (the new richness-level documentation, the new K10 gate
  documentation, the `finalisation-enhancements.yml` artefact
  mention). S09's job is **additive** — add the new
  `crux-cursor-meditation-guide` agent row and six new meditation
  skill rows on top of the richness-extended docs. **Do NOT duplicate**
  richness coverage.

---

## 7. Risks & Open Questions

### 7.1 Ambiguity resolutions made during design (no `needs_user_input` required)

| # | Ambiguity | Resolution | Rationale |
|---|-----------|-----------|-----------|
| R1 | Where does the **Subject-Matter Focus rule** primarily live? Skill `report`, or both `research` + `quick`? | Primary: `skill:report`. Mirror: `skill:research` step 8 and `skill:quick` step 6 cite the rule when constructing `consolidation.md`. | The rule applies to `consolidation.md` and HTML/PDF reports only (freeze §8 scope). Consolidation is the bridge artefact — placing the rule in the report skill keeps the single source of truth at the **enforcement point**. |
| R2 | Where does the **facet registry** schema live — `skill:coordination` (filename grammar) or `skill:research` (operational protocol)? | Schema + lock + orphan-recovery → `skill:research`. `skill:coordination` carries only the filename row + lockfile-name. **No "OR" — single primary.** | The registry exists **only in Research mode**. Placing it in the universal coordination skill would mislead Quick-mode readers. |
| R3 | Where does the **Quick vs Research differences table** primarily live? | Split into two rows: `skill:research` owns the **Research column**; `skill:quick` owns the **Quick column**. Each row has a single primary. | A single mirrored table would drift; split-by-column ensures each side stays accurate to its mode. |
| R4 | Where do the **ensemble structural extras** (model-comparison hero, agreement heatmap, etc.) live — `skill:ensemble` or `skill:report`? | Primary: `skill:ensemble`. Mirror paragraph in `skill:report` noting "ensemble extras layer additively on top of standard minimums". | Ensemble extras are conceptually a delta on top of the standard report contract; placing them with the ensemble workflow keeps the report skill focused on the single-tree contract. |
| R5 | Should the **`needs_user_input` schema** be duplicated on the new guide agent? Should the **Pattern-B respawn-with-decision-guidance** for Dim 13 mirror the same shape? | Yes for both. The generic schema is a verbatim mirror of `AGENTS.md` lines 31–60 on the new guide agent (same shape as the existing memory-manager mirror). The Dim 13 respawn payload schema (with `respawn_reasons` LIST-typed) lives in `skill:review` (authoring side) and `skill:report` (consuming side) — the calling agent never sees Dim 13 `respawn_required` findings via askQuestion. | Each independently-spawnable agent must carry the escalation schema in its own system prompt so subagents understand the protocol without loading `AGENTS.md` first. The Dim 13 bypass keeps the decision-guidance shape consistent with §6.10 of the new freeze: structured deterministic payloads, never user questions. |
| R6 | Should `skill:report` own the **paired-report verification gate** (`ls -1t … head -n 1` bash) or should it stay on the **command** (calling-agent step 9)? | Both — `skill:report` documents the gate as the subagent's pre-return invariant (step 12 finalisation); the command's step 9 re-runs the gate as a calling-agent-side defence-in-depth check. | Defence-in-depth: subagent ensures the artefacts exist before returning; calling agent re-verifies before presenting to the user. The two checks are identical bash but serve different actors. |
| R7 | The freeze contract §4.2 step 7 spawns "peer reviewers in parallel" — should this be a **separate skill** (`meditation-peer-review`) or stay inside `skill:research`? | Stay inside `skill:research` as the peer-review file spec (§5.6 of the contract). The seventh skill would exceed the spec K3 approved cap of six. | Peer review is Research-mode-only and tightly coupled to the depth-0 step-7 spawn pattern; bundling it into `skill:research` keeps the skill count at six and matches K3 exactly. The peer-review file spec is the only verbatim block; the spawn signature is inline in `skill:research` step 7. The 2026-05-24 refresh also keeps the **rendering side** of peer-review surfacing (named sections at `detailed`+) in `skill:report` (Peer-Review Surfacing Rule), so `skill:research` owns the data source and `skill:report` owns the renderer. |
| **R8** | **Where does the K10 in-pass reflection function live?** | The K10 reflection (per-tree in single-model + cross-model in ensemble) runs inside the depth-0 manager's **existing LLM turn** — no new agent spawn. The agent body documents it as a **mode router row** of its own (§1.3 row 5) so the agent persona knows the function exists; the verbatim rubric + catalogue + schema live in `skill:research` (single-model write side), `skill:quick` (Quick variant), and `skill:ensemble` (per-tree + root cross-model). No separate `skill:reflection` is needed. | The K10c reflection is not a spawned subagent; it is a sub-step of step 8 (single-model) and steps 3b–3f (ensemble). Treating it as a mode router row keeps the agent body's persona description honest (the persona must "know" this function exists) without bloating the skill count. |
| **R9** | **Six-skill cap verdict against the 13 new richness surfaces** | **KEPT AT 6.** All 13 surfaces map into the existing six skills via mirrors. The richness spec's own architecture design §13 row #17 explicitly chose to extend `meditation-coordination` for K10 finalisation gate ownership rather than create a seventh skill — this design **affirms** that choice. The verbatim distribution is captured by the §3 table above (each new surface has exactly one primary destination across the existing six skills + the agent + the command). | Adding a seventh skill (e.g. `meditation-finalisation` for K10) would split tightly-coupled contracts: the K10c rubric lives with single-model write-side responsibility (`skill:research` / `skill:quick`); the K10 layered cadence lives with cross-model write-side responsibility (`skill:ensemble`); the K10b rendering contract lives with the report (`skill:report`); the `Q-Finalisation-Enhancements` askQuestion stays on the command per K4. There is no natural single home for "K10" because K10 is a cross-skill orchestration. The six-skill cap holds; mirror references in `skill:coordination` (filename rows for the 4 follow-up artefact types + finalisation-enhancements YAML) cover any coordination-grammar drift. |

### 7.2 Open questions flagged for `needs_user_input` escalation by the executor (Pattern B)

**None at design time.** Every contract item in the new freeze
(`meditate-frozen-contract-20260524.md` Sections 1–10) maps to a
**single primary destination** (and optional mirror(s)) in §3 above.
Subtasks 04, 05, 06, 07, 09, 10 should proceed without re-escalation
**unless** they discover a conflict at implementation time, in which
case they must escalate per the spec's Pattern B protocol.

### 7.3 Risks for subsequent subtasks

| # | Risk | Likelihood | Mitigation |
|---|------|-----------|------------|
| K1 | Subtask 04 (guide agent file) accidentally **inlines verbatim Phases A–G / dimensions / K10c rubric / Per-Cheap-Type catalogue** in the agent body instead of delegating to skills. | Medium | The agent's line budget is documented in §1.4 (**≤ 500 lines** post-refresh, raised from ≤ 350 because the source has grown to ~1041 lines). Integrity-expert (S12) flags **>550 lines** as "agent has not delegated enough to skills". |
| K2 | Subtask 05 (skills extraction) produces a skill whose `description` field omits the substring `meditation`, breaking eval discoverability. | Low | The eval discoverability anchors in §2 are explicit; subtask 03 (eval plan) and subtask 08 (eval update) plus integrity-expert's S12 audit catch this. |
| K3 | Subtask 06 (command refactor) accidentally **deletes a Pattern A or Pattern B askQuestion** (e.g. Sub-Q5 deep_confirm, K10c per-item treatment sub-Q, or a read-only-richness trigger preamble) thinking it moved to a skill. | Low | The section-mapping table §3.2 is explicit: every prompt that requires `AskQuestion` stays on the command. S12 diffs against the new freeze line and flags any missing prompt. |
| K4 | **Subtask 07 (memory-manager trim) accidentally deletes Forget Mode (now at lines 1160–1188 — the ONLY thing between the two contiguous deletion ranges 279–1159 and 1189–1349).** Forget Mode sits **directly between** the two deletion ranges in the 1388-line file; an off-by-one error or a "delete-from-279-to-1349" shortcut would wipe it. | **Medium-high** | §5.2 row 12 explicitly lists Forget Mode as retained at 1160–1188; the deletion ranges in §5.1 are **279–1159** and **1189–1349** with Forget Mode at 1160–1188 left intact. The acceptance grep in §5.3 verifies. **S07 implementers MUST delete by section heading, NOT by line range, to avoid the contiguous-range trap.** |
| K5 | Subtask 09 (docs sync) misses the AGENTS.md Spec Execution Agent Allocation table, leaving meditation work unassigned. | Medium | §3.9 row 7 lists the AGENTS.md updates explicitly; integrity-expert's S12 audit reads AGENTS.md and verifies. |
| K6 | Subtask 10 (install/dist) adds the new agent + skills to `install.py` and `create-crux-zip.py` but forgets `.crux/dist-manifest.json` regeneration. | Medium | §3.9 enumerates all five surfaces (`install.py`, `create-crux-zip.py`, `.crux/dist-manifest.json`, `CONTRIBUTORS.md`, version-bump RELEASE_PATHS). The `zip-contents-protection` rule itself lists the four-step add procedure; S12 audit verifies. |
| K7 | Subtask 11 (CRUX compression sync) accidentally creates a new `AGENTS.crux.md` mirror when the spec explicitly forbids it (K8). | Low | K8 is restated in §3.9 and in the new freeze §9. The integrity-review subtask (12) audits for absence. |
| K8 | Drift between the agent's mirrored User Input Escalation block and the canonical block on `AGENTS.md`. | Low | Both blocks remain literally identical at the time of subtask 04. Any future change to the escalation protocol updates `AGENTS.md` first and propagates by hand to both agents (memory-manager and meditation-guide); the existing convention. |
| **K9** | **20260523 patch matrix coordination — S12 must diff against 20260524 freeze**. The richness spec landed before this decomposition; without the new freeze line, S12 might diff against the stale 20260517 freeze and miss richness regressions. | Medium | §6.5 of this design explicitly names `meditate-frozen-contract-20260524.md` as the freeze line. S12's integrity audit checklist MUST cite the new freeze line by name. The 20260517 freeze is preserved as an audit-trail artefact only and must not be consumed as the contract baseline (per the new freeze's footer). |
| **K10** | **`additional_focus_areas[]` canonical name (W1/W1b regression must not return)**. The richness spec's S03 originally shipped two divergent field names — `additional_focus_areas_skipped` / `additional_focus_areas_accepted` — and the W1 + W1b post-execution fixes normalised them to a single canonical array `additional_focus_areas[]` with a per-item `treatment:` filter. S04 (agent body), S05 (research + quick skills), S07 (memory-manager trim — affects pointer paragraphs), S08 (eval update — `TestMeditateInitSuggestions::test_four_opt_in_modes_documented` pins the canonical name) must NOT re-introduce the legacy field names. | Medium | Pin the canonical schema verbatim across S04/S05/S07/S08. §3.4 row "**§4.6 4-mode reconciliation**" explicitly names the canonical field (`additional_focus_areas[]` with `treatment:` filter) and explicitly excludes the legacy field names. §8 of this design includes **negative substring assertions** for `additional_focus_areas_skipped` and `additional_focus_areas_accepted` so S03 captures them. |

---

## 8. Cross-Reference — Discovery Cues for Subtask 03 (Eval & Test Plan)

To pre-empt eval coverage gaps that subtask 03 must capture as
substring-presence assertions (and negative-substring assertions where
indicated):

| Substring | Expected location | Polarity |
|-----------|-------------------|----------|
| `crux-cursor-meditation-guide` | `.cursor/agents/crux-cursor-meditation-guide.md` (frontmatter `name:`); `.cursor/commands/crux-meditate.md` `### Instructions` (spawn target); `AGENTS.md` Available Agents table | positive |
| `crux-skill-memory-meditation-research` | Directory + SKILL.md `name:` + every cross-skill cross-reference | positive |
| `crux-skill-memory-meditation-quick` | same | positive |
| `crux-skill-memory-meditation-ensemble` | same | positive |
| `crux-skill-memory-meditation-review` | same | positive |
| `crux-skill-memory-meditation-report` | same | positive |
| `crux-skill-memory-meditation-coordination` | same | positive |
| `meditation` (in each skill's `description`) | All six SKILL.md frontmatters | positive |
| `Pattern B` | Command coordination menu, agent User Input Escalation block, `skill:review` MUST_FIX schema, `skill:research` step 4 + step 6 + step 8, `skill:quick` step 4 + step 5 + step 8, `skill:ensemble` step 3e (combined root gate) | positive |
| `needs_user_input` | Same surfaces | positive |
| `mandatory context` (lower-case, in MUST_FIX context) | `command` Adversarial Review pointer + `skill:review` schema verbatim | positive |
| `Anti-Homogenization` / `anti-homogenisation` | `skill:report` (canonical block) + `command` Theme Preflight context paragraph | positive |
| `Universal Contrast` | `skill:report` (canonical) | positive |
| `ensemble-report-{topic-slug}-{ts}.html` literal | `skill:ensemble` + `skill:coordination` filename grammar | positive |
| `crux-cursor-memory-manager` (in `/crux-meditate` spawn context) | **Must not appear** in `.cursor/commands/crux-meditate.md` after subtask 06 lands | negative |
| **`Q-Cost-and-Richness-Acknowledgment`** | `command` Cost & Scope Acknowledgment section + `skill:review` Dim 12 references + `agent` mode router preamble pointer | positive |
| **`Q-Cost-Acknowledgment-Expansion`** read-only-richness variant naming | `command` (verbatim) | positive |
| **`Q-Finalisation-Enhancements`** | `command` Finalisation Enhancements Gate + `skill:research` step 8 K10c + `skill:quick` step 8 K10c + `skill:ensemble` step 3e + `agent` K10 reflection mode router row + Pattern B list | positive |
| **`comprehensiveness:`** payload literal | `command` Theme Preflight propagation block + `agent` mode router preamble + every skill receive contract | positive |
| **`Comprehensiveness Level Mapping`** | `skill:report` (12×4 table) + cross-references in `agent` + `command` pointer | positive |
| **`compact`** / **`default`** / **`detailed`** / **`exhaustive`** richness levels | `command` Cost gate + `skill:report` Level Mapping + `skill:research` + `skill:quick` propagation | positive |
| **`init-suggestions-{ts}.yml`** | `skill:coordination` filename row + `skill:research` step 4b write + `skill:quick` step 4b write + `skill:report` honour rules + `skill:review` Dim 13 audit + `command` pointer | positive |
| **`finalisation-enhancements.yml`** | Same surfaces as init-suggestions + `skill:ensemble` per-tree + root combined variants | positive |
| **`additional_focus_areas`** with `treatment:` filter (canonical post-W1b) | `command` combined Pattern-B Sub-Q4 + `skill:research` step 4b + `skill:quick` step 4b + `skill:report` Init-Suggestions Honour + `skill:review` Dim 13 | positive |
| **`additional_focus_areas_skipped`** (legacy W1 field name) | **Must not appear** anywhere in the post-decomp repo | negative |
| **`additional_focus_areas_accepted`** (legacy W1 field name) | **Must not appear** anywhere in the post-decomp repo | negative |
| **`Dimension 12`** / **`Comprehensiveness fidelity`** | `skill:review` (verbatim) | positive |
| **`Dimension 13`** / **`Init-suggestion AND finalisation-enhancement honour`** | `skill:review` (verbatim) | positive |
| **`Report-Skill Respawn Protocol`** | `skill:review` (payload authoring) + `skill:report` (resume handler) + `command` pointer | positive |
| **`respawn_reasons`** (list-typed) | `skill:review` (verbatim schema) + `skill:report` resume handler | positive |
| **`Per-Cheap-Type Rendering Contract`** | `skill:report` (verbatim — 7 types) + `command` pointer | positive |
| **`K10 Ensemble Respawn Targeting`** | `skill:ensemble` (verbatim) + `command` ensemble respawn loop | positive |
| **`source_tree`** (per-tree YAML field) | `skill:ensemble` + `skill:research` + `skill:quick` per-tree write | positive |
| **`surfaced_to_root`** (per-tree YAML field, written-back by aggregator) | `skill:ensemble` step 3d | positive |
| **`cross_model_candidates`** + **`union_candidates`** (root combined YAML) | `skill:ensemble` step 3d schema | positive |
| **`set-once-per-invocation`** (K6 richness rule) | `command` Cost-and-Richness gate behaviour rules + agent design principles | positive |
| **`compact reproduces pre-richness behaviour`** | `command` Cost gate + `skill:report` Comprehensiveness Level Mapping | positive |
| **`per_finding_table`** (`exhaustive` Research citation density) | `skill:report` Comprehensiveness Level Mapping row 9 | positive |
| **`Universal Contrast`** / **anti-homogenisation** at every richness level | `skill:report` (applies verbatim at every level per K7) | positive |

Subtask 03 will turn each of the above into a positive or negative
substring assertion; subtask 08 will refresh `evals/test_q_meditate.py`
+ `evals/test_p_amnesia.py` + `evals/sdk/tests/q-meditate.test.ts` +
`evals/conftest.py` accordingly, preserving all 30 new pytest classes +
4 new TS describe blocks already shipped by richness S06.

---

## 9. Implementation Summary for Downstream Subtasks

| Subtask | Reads | Produces |
|---------|-------|----------|
| **04** Guide Agent File | This design §1, §3, §6, §7 (esp. K1, K9, K10); new freeze §0 + §1.3 mode router rows + §2.7 `comprehensiveness:` payload + §2.8 K10c reflection + §4.5 Ensemble Aggregation extended | `.cursor/agents/crux-cursor-meditation-guide.md` (**≤ 500 lines** post-refresh; mode router row for K10 reflection function; canonical comprehensiveness-abort error string) |
| **05** Meditation Skills | This design §2, §3, §6.5, §7 (esp. K9, K10); new freeze §4 (subagent contracts incl. step 4b + step 8 K10c + step 8b respawn-prep + Ensemble layered cadence 3b–3f) + §5 (coordination conventions 18 rows) + §6 (mandatory report contract incl. Comprehensiveness Level Mapping + Per-Branch / Depth-3 / Peer-Review Surfacing Rules + Init-Suggestions Honour + K10b Per-Cheap-Type Rendering Contract + Report-Skill Respawn Protocol); secondary input: 20260523 design §11 + §13 | Six new `.cursor/skills/crux-skill-memory-meditation-*/SKILL.md` files containing verbatim contracts pulled from new freeze §4–§8. Canonical `additional_focus_areas[]` field name with `treatment:` filter — must NOT introduce legacy field names |
| **06** Command Refactor | This design §4, §6.5; new freeze §2 (calling-agent gates), §7 (continuation menu with K10c groups) | Refactored `.cursor/commands/crux-meditate.md` (**~650 lines**, ~70 % smaller from 2142); deprecation banner added to the top of memory-manager Meditate Mode |
| **07** Memory-Manager Trim | This design §5; new freeze §4 (deletion target lines 279–1159 + 1189–1349) | `.cursor/agents/crux-cursor-memory-manager.md` (**~360 lines**, ~74 % smaller from 1388); both deleted sections replaced by pointer paragraphs (richness gates named in the pointer); Forget Mode at 1160–1188 retained intact |
| **03** Eval & Test Plan | This design §2, §8; new freeze §10.3 (eval source-of-truth — 36 pytest classes / 7 TS describe blocks) | Eval matrix + new substring assertions (positive + negative); no implementation yet |
| **08** Eval & Test Update | Subtask 03's plan + this design §3, §6.5; new freeze §10.3 | Updated `evals/test_q_meditate.py` (preserves 30 new richness classes), `evals/test_p_amnesia.py`, `evals/sdk/tests/q-meditate.test.ts` (preserves 4 new richness describe blocks), `evals/conftest.py` |
| **09** Docs Sync | This design §3.9, §6.5; new freeze §9; 20260523 S07 outputs (richness-extended README / docs / web) | README, AGENTS.md, CONTRIBUTORS.md, docs/, web/ updates — **additive** on top of richness extensions, no duplication |
| **10** Install / Dist / Release | This design §3.9; new freeze §9 | `install.py`, `scripts/create-crux-zip.py`, `.crux/dist-manifest.json`, `.github/workflows/version-bump.yml` updates |
| **11** CRUX Compression Sync | New freeze §9 | Regenerated `.crux.mdc` mirrors for `crux-memories-integration`, `docs-sync`, `version-bump`, `zip-contents-protection`. **No new mirror coverage** per K8. |
| **12** Integrity Review | This design §1–§7 + new freeze §10 (Source-of-Truth Map); secondary input: 20260523 design §11 + §13 | Audit report; **diff against `meditate-frozen-contract-20260524.md`** (not the stale 20260517 freeze — see K9); zero unexplained deviations or flagged with `needs_user_input` for the calling agent |

---

## 10. Definition of Done — Subtask 02

- [x] Design document exists in spec directory at `specs/20260517-meditate-agent-skill-decomposition/meditate-decomp-architecture-design-20260517.md`
- [x] Every contract item from the new freeze document (§1–§8 of `meditate-frozen-contract-20260524.md`) has a **single primary destination** in §3 above (judge blocker D04 resolved — see "Refresh 2026-05-24" below)
- [x] Skill mapping covers **exactly** the six approved skill names from spec K3 (no additions, no merges, no renames) — see §2 + §7 R9
- [x] Coordinator command shape documented with new spawn signatures for single-model, ensemble member, ensemble aggregation, and adversarial review spawns — see §4.3
- [x] Memory-manager trim plan covers every Meditate section in the current 1388-line file (lines 279–1159 + 1189–1349 + two expertise bullets) — see §5; Forget Mode at 1160–1188 explicitly retained
- [x] Backwards-compat plan addresses the S06→S07 interim window with a deprecation banner — see §6.1–6.4; coordination with 20260523 patch matrix documented — see §6.5
- [x] Risks & open questions catalogued (R1–R9, K1–K10); no `needs_user_input` required at design time — see §7
- [x] Markdown-only artefact; no executable code introduced; no linter errors

### Refresh 2026-05-24

- [x] D04 resolved — every row in §3 normalised to a single primary destination plus zero-or-more mirrors. Five split-primary rows from the 2026-05-17 draft normalised: §3.4 Output body sections list (split into Research / Quick rows), §3.4 Quick vs Research differences (split into Research column / Quick column rows), §3.5 §5.4 Facet registry schema (single primary `skill:research`; mirror `skill:coordination` filename row only — "OR" removed), §3.5 §5.5 Inline citation markers (split into Research strict / Quick warn variants), §3.5 §5.5 Validation enforcement (split into Research / Quick paths).
- [x] §3 extended with 13 new richness-introduced rows covering: merged `Q-Cost-and-Richness-Acknowledgment` gate, read-only-richness `Q-Cost-Acknowledgment-Expansion` variant, `comprehensiveness:` payload propagation, `Q-Finalisation-Enhancements` gate (K10a/b/c with mirrors across all four supporting skills), Comprehensiveness Level Mapping (12×4), 4-mode `additional_focus_areas[]` reconciliation (write side mode-split + honour side), `init-suggestions-{ts}.yml` production, peer-review explicit report sections at `detailed`+, Adversarial Review Dim 12 + Dim 13, Reviewer Pattern-B respawn-with-decision-guidance + Report-Skill Respawn Protocol, Ensemble layered K10 cadence, K10 Ensemble Respawn Targeting.
- [x] §1.3 mode router refreshed: new row (5) for K10 In-Pass Reflection function; Research + Quick rows mention scouting init-suggestions production + step 4b; Adversarial Review row mentions 13 dimensions + Report-Skill Respawn Protocol.
- [x] §1.4 agent body budget raised to ≤500 lines against the post-richness ~1041-line source; S12 integrity-expert >550-line trigger documented.
- [x] §4.1 sections-retained table refreshed against the current 2142-line command with section-heading anchors as stable keys and current line-range parentheticals; new sections for richness-introduced surfaces enumerated; each row marked `unchanged` / `shrunk` / `modified`.
- [x] §4.2 budget projection recomputed: ~1376-line deletable surface; target post-refactor command ~650 lines.
- [x] §5 trim plan re-projected against the 1388-line memory-manager: deletion ranges 279–1159 + 1189–1349 (~1041 lines); Forget Mode at new location 1160–1188 (K4 risk sharpened); replacement pointer paragraphs name the new richness gates.
- [x] §6.5 NEW: coordination with 20260523 patch matrix; S08 preserves 30 new pytest classes + 4 new TS describe blocks; S09 integrates additively with richness-extended docs.
- [x] §7 risks refreshed: K1 budget threshold updated to ≤500 (was ≤350); R8 NEW (K10 reflection function placement); R9 NEW (six-skill cap verdict — kept at 6); K9 NEW (20260523 patch matrix coordination); K10 NEW (`additional_focus_areas[]` canonical name regression guard).
- [x] §8 discovery cues extended with new richness substrings and negative assertions for the legacy `_skipped` / `_accepted` field names.
- [x] §9 per-subtask read/produce table references the new freeze + new §3 row positions.

---

_Captured by `crux-platform-architect` against repo `/home/andrewv/git/cursor/CRUX-Compress`. Original 2026-05-17 draft refreshed in place on 2026-05-24 against the new freeze line `meditate-frozen-contract-20260524.md`. This design is the **contract** that subtasks 03, 04, 05, 06, 07, 08, 09, 10, 11, 12 must follow. Deviations require an explicit `needs_user_input` escalation surfaced through the calling agent._
