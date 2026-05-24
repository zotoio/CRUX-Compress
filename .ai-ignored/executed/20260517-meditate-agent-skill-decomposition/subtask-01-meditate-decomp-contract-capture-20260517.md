# Subtask: Frozen Meditate Contract Capture

## Metadata
- **Subtask ID**: 01
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: None
- **Created**: 20260517

## Objective
Produce a single, authoritative freeze document inside this spec directory
that captures every current `/crux-meditate` user-facing and executable
behaviour. This document is the contract baseline against which every later
subtask is verified ("lose no functionality"). It must be specific enough
that the integrity-review subtask (12) can mechanically diff post-refactor
artefacts against it.

## Deliverables Checklist
- [x] Create `meditate-frozen-contract-20260517.md` inside this spec
      directory containing all sections below.
- [x] **Modes inventory**: Research (default), `--quick`, `--ensemble`,
      combined `--quick --ensemble`. For each: trigger, calling-agent
      vs subagent ownership, key flags / config keys
      (`cruxMemories.meditate.modelPool`, `ensembleAggregatorModel`,
      depth defaults, ensemble facet batching).
- [x] **Calling-agent gates** verbatim or near-verbatim text:
      `Q-Depth-Selection`, `Q-Cost-Acknowledgment`,
      `Q-Cost-Acknowledgment-Expansion`, theme preflight Q1–Q5 +
      `theming:` YAML payload + `surprise_me` non-interactive fallback,
      facet confirmation `Q-Confirm-1` / `Q-Confirm-2` and
      `confirmDeepFacets` deep-YAML escalation.
- [x] **Pattern A vs Pattern B** boundaries: which prompts run before
      spawning the tree, which run as `needs_user_input` escalations
      from the tree.
- [x] **Subagent contracts** (today on `crux-cursor-memory-manager`):
      Phases A–G research, Quick 6-step, Ensemble Aggregation,
      Adversarial Review (11 dimensions, severities, ≤3 iterations,
      `MUST_FIX` `needs_user_input` schema with mandatory `context`
      field).
- [x] **Coordination conventions**: artefact filename table
      (`meditations/{yyyymmdd}-{topic-slug}/...`), prefix-glob polling
      rule ("never hard-code report names"), facet registry lock
      semantics, citations index format, peer-review file spec,
      retrospective template (`retrospective-{ts}.md`),
      Branch & Leaf Index template appended to `facets.md`.
- [x] **Mandatory report contract**: paired HTML + PDF, anti-homogenisation
      rules, Universal Contrast / WCAG-style colour rules, light/dark
      theme + print TOC, Chart.js / D3 / calculator inclusion rules,
      static fallback rules for D3 / calculators, headless Chrome →
      Chromium degradation, ensemble aggregation report extras
      (`cross-model-synthesis.md`, ensemble HTML/PDF).
- [x] **Continuation menu** (steps 9–12 calling-agent): verify report
      pair, present paths, expansion / save-spec / end handling.
- [x] **Cross-repo touchpoints**: `/crux-amnesia` explicit-command
      list inclusion, `commands.meditate` config entry in
      `.crux/crux-memories.json`, AGENTS.md table row, README rows,
      `docs/crux-memories.md` description, `web/compress.md/memories.html`
      copy, `install.py` / `create-crux-zip.py` enumerations.
- [x] **Source-of-truth map**: line ranges (or section headings) in the
      *current* `.cursor/commands/crux-meditate.md` and
      `.cursor/agents/crux-cursor-memory-manager.md` for each contract
      item, so subtask 02 can plan moves and subtask 12 can verify.

## Definition of Done
- [x] Freeze document exists in spec directory
- [x] Every contract item is traceable back to a current source line range or section heading
- [x] Document is referenced from the spec index (Execution Notes) so later subtasks can find it
- [x] No linter errors introduced (markdown-only artefact)

## Implementation Notes
- This is a **read-only** subtask — do not modify command, agent, skill,
  eval, doc, or install files. Only create the freeze document.
- Use the `explore` subagent if needed for cross-cutting line lookups
  but capture the final consolidated record yourself.
- Treat both
  `specs/20260516-meditate-research-mode-overhaul/spec-meditate-research-mode-overhaul-20260516.md`
  and the existing command + memory-manager files as inputs. If the
  20260516 execution report or subtask docs disagree with the
  *currently committed* command/agent text, the **command + agent
  files are authoritative**.
- Where the project rule says "no `AskQuestion` in subagents", record
  this as part of the contract — every escalation must remain a
  `needs_user_input` block.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- This subtask produces a markdown artefact; no automated tests apply
  beyond markdown lint. Run only file-scoped lint if any.

## Execution Notes

### Agent Session Info
- Agent: `crux-platform-architect`
- Started: 2026-05-17T11:58:35Z
- Completed: 2026-05-17T12:02:00Z (approx.)
- Repo SHA at start: `b4fc33b0c034866bb60b7fe7b03be9e0c7a18bbf`
- Token budget: 200000 (resolved)

### Work Log
- Read inputs: `.cursor/commands/crux-meditate.md` (1493 lines), `.cursor/agents/crux-cursor-memory-manager.md` (946 lines), and the parent spec `spec-meditate-agent-skill-decomposition-20260517.md`.
- Inspected cross-repo touchpoints across `.cursor/commands/crux-amnesia.md`, `.crux/crux-memories.json`, `AGENTS.md`, `README.md`, `docs/crux-memories.md`, `web/compress.md/memories.html`, `install.py`, `scripts/create-crux-zip.py`.
- Produced `meditate-frozen-contract-20260517.md` (1441 lines) covering: modes inventory (Research / Quick / Ensemble / combined with all per-mode config keys), every verbatim calling-agent gate prompt and option set, Pattern A vs Pattern B boundaries, subagent contracts (Phases A–G + Quick 6-step + Ensemble Aggregation + 11-dimension Adversarial Review with `MUST_FIX` `needs_user_input` schema), coordination conventions (filenames, prefix-glob polling, mkdir lock, citations index, peer-review file spec, retrospective template, Branch & Leaf Index template), mandatory report contract (paired HTML+PDF, anti-homogenisation, Universal Contrast / WCAG, light/dark, print TOC, Chart.js / D3 / calculator rules with static fallbacks, headless Chrome → Chromium degradation, ensemble extras), single-model + ensemble continuation menus (steps 9–12), cross-repo touchpoints, and a complete line-range source-of-truth map.
- Updated parent spec Execution Notes to point at the freeze document so subsequent subtasks can find it.

### Blockers Encountered
None.

### Files Modified
- `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260517.md` (created)
- `specs/20260517-meditate-agent-skill-decomposition/spec-meditate-agent-skill-decomposition-20260517.md` (Execution Notes updated)
- `specs/20260517-meditate-agent-skill-decomposition/subtask-01-meditate-decomp-contract-capture-20260517.md` (checklist + execution notes)
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-01-meditate-decomp-contract-capture-20260517.status.yml`
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-01-meditate-decomp-contract-capture-20260517.status.md`

## Refresh 2026-05-24

### Why

The sibling spec `specs/20260523-meditate-richness/` completed and
landed on 2026-05-24 (executor sign-off; all 9 subtasks judge-verified —
see `specs/20260523-meditate-richness/execution-report-meditate-richness-20260523.md`,
including the W1 + W1b post-execution canonicalisation of
`additional_focus_areas[]` with the `treatment:` filter). The richness
changes are present in the working tree (unstaged) but factually live at
the file paths the 20260517 decomposition spec operates on:

- `.cursor/commands/crux-meditate.md` grew from **1493 → 2142 lines** (+649 lines)
- `.cursor/agents/crux-cursor-memory-manager.md` grew from **946 → 1388 lines** (+442 lines)
- `evals/test_q_meditate.py` grew from **240 → 1335 lines** (28 new richness
  test classes containing ≈147 new test methods, all additive)
- `evals/sdk/tests/q-meditate.test.ts` grew from **357 → 576 lines** (4 new
  describe blocks with 22 new `it` tests, all additive)
- Forget Mode moved from agent lines 843–870 to **1160–1188**
- Ensemble Aggregation Mode moved from agent lines 872–907 to
  **1189–1349** and was extended with K10 layered cadence steps 3b–3f

Thirteen new contract surfaces were introduced by 20260523 (the merged
`Q-Cost-and-Richness-Acknowledgment` gate, the
`comprehensiveness:` payload, the post-consolidation
`Q-Finalisation-Enhancements` Pattern-B gate with K10a/b/c semantics,
adversarial Dim 12 + Dim 13 + level-conditional Dim 9, the Report-Skill
Respawn Protocol, the Comprehensiveness Level Mapping table, the 4-mode
`additional_focus_areas[]` reconciliation, the
`init-suggestions-{ts}.yml` schema with report-side honour rules, the
layered ensemble K10 cadence, and the new eval coverage). All thirteen
must be preserved by the 20260517 decomposition without functionality
loss.

The 2026-05-17 freeze document captured the pre-richness contract surface
at an earlier point in the decomposition spec's life. Since S02 was still
blocked at the moment of richness landing, refreshing the freeze line
before unblocking S02 keeps the decomposition spec auditable against the
**actually shipping** contract surface rather than an obsolete snapshot.

### New freeze artefact

A refreshed freeze document was produced at
`specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260524.md`
that:

- **Supersedes** `meditate-frozen-contract-20260517.md` (which now carries
  a `> [!IMPORTANT]` supersession banner pointing at the 2026-05-24 file).
- Preserves the original 10-section structure (Modes / Gates / Pattern
  A vs B / Subagent Contracts / Coordination Conventions / Report
  Contract / Continuation Menu / Subject-Matter Focus / Cross-Repo
  Touchpoints / Source-of-Truth Map).
- Inlines the **richness-modified or replaced** contract items verbatim
  (e.g. `Q-Cost-Acknowledgment` → `Q-Cost-and-Richness-Acknowledgment`,
  new Comprehensiveness Level Mapping table, new
  `Q-Finalisation-Enhancements` gate, extended adversarial review).
- **Cites** the 20260517 freeze for unchanged sections rather than
  duplicating them.
- Adds a refreshed source-of-truth map keyed to the **current 2142-line**
  command file and the **current 1388-line** memory-manager (with the
  Forget Mode + Ensemble Aggregation Mode line ranges updated).
- Refreshes the cross-repo touchpoints to reflect the 20260523 S07 docs
  sync (+25 lines to `README.md`, +108 lines to `docs/crux-memories.md`,
  +32 lines to `web/compress.md/memories.html`) and the K8 no-new-files
  constraint (install / dist / version-bump unchanged).

### What this refresh does NOT change

- The 2026-05-17 checklist above (`Deliverables Checklist`) is preserved
  as a historical record of the original contract-capture work.
- The 2026-05-17 work log (`Execution Notes` → `Work Log` above) is
  preserved.
- The 2026-05-17 freeze file is **not deleted** — it remains as an
  audit-trail artefact with a supersession banner pointing at the new file.
- The decomposition spec's K-decisions (K1–K8) are unchanged.
- The decomposition spec's subtask manifest, dependency graph, and DoD
  are unchanged.

### Files refreshed by this 2026-05-24 work

- `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260524.md`
  (created — refreshed freeze artefact)
- `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260517.md`
  (supersession banner added at top)
- `specs/20260517-meditate-agent-skill-decomposition/spec-meditate-agent-skill-decomposition-20260517.md`
  (Execution Notes → Frozen contract reference updated to point at the
  new freeze + refreshed SHA + line counts)
- `specs/20260517-meditate-agent-skill-decomposition/subtask-01-meditate-decomp-contract-capture-20260517.md`
  (this section appended — no checklist modifications)
