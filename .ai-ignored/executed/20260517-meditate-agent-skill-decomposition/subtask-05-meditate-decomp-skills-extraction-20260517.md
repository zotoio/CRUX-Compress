# Subtask: Implement `crux-skill-memory-meditation-*` Skill Family

## Metadata
- **Subtask ID**: 05
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 02
- **Created**: 20260517

## Objective
Create the new meditation skill family under `.cursor/skills/`, following
the existing `crux-skill-memory-*` directory and `SKILL.md` conventions.
Each skill is a standalone, agent-loadable unit owned by a subset of the
Meditate contract per the architecture-design doc (subtask 02).

## Deliverables Checklist
Create exactly the six approved skills below. Do not add, remove,
merge, split, or rename skills unless the executor escalates a
`needs_user_input` decision and receives explicit user approval.
For each skill, create a directory and a `SKILL.md` with valid
frontmatter and contract-faithful body content.

- [ ] **`crux-skill-memory-meditation-research`** —
      Phases A–G research tree, facet registry + lock, citations index,
      peer review file spec, citation respawn rule (≤2 retries),
      depth-3 default and recursive expansion semantics.
- [ ] **`crux-skill-memory-meditation-quick`** —
      6-step quick protocol, warn-only citations, upfront child
      derivation, depth-1 default override.
- [ ] **`crux-skill-memory-meditation-ensemble`** —
      N-parallel-trees model-pool protocol, batched pending-facet
      cross-tree confirmation, aggregator spawn contract,
      `cross-model-synthesis.md` template, ensemble HTML / PDF
      report extras.
- [ ] **`crux-skill-memory-meditation-review`** —
      11-dimension adversarial review, severities, ≤3 iterations,
      `MUST_FIX` `needs_user_input` schema (with mandatory
      `context`), reviewer review-doc template, decision-guidance
      requirement on every parent `askQuestion`.
- [ ] **`crux-skill-memory-meditation-report`** —
      Mandatory paired HTML + PDF, anti-homogenisation theming,
      Universal Contrast, light/dark + print TOC, Chart.js / D3
      inclusion + static SVG / PNG fallback, calculator inclusion +
      static fallback, headless Chrome → Chromium degradation,
      report verification step ("verify both files exist before
      returning paths").
- [ ] **`crux-skill-memory-meditation-coordination`** —
      Artefact filename table (`meditations/{yyyymmdd}-{topic-slug}/`),
      prefix-glob polling rule ("never hard-code report names"),
      facet registry lock semantics, retrospective template
      (`retrospective-{ts}.md`), Branch & Leaf Index template
      appended to `facets.md`.

For each skill:

- [ ] Frontmatter contains `name: <skill-dir-name>` and a
      `description` that mentions "meditation" plus the verb
      (e.g. "research", "review").
- [ ] Body opens with a "When to use" section that states which
      agent / mode / sub-mode loads the skill.
- [ ] Body includes the contract items assigned to that skill in
      subtask 02's mapping table, with no items orphaned.
- [ ] Body references the new guide agent by exact name
      (`crux-cursor-meditation-guide`) when describing the caller.
- [ ] `SKILL.md` lints cleanly (frontmatter parses, no broken
      markdown links).

## Definition of Done
- [ ] All skill directories created under `.cursor/skills/`
- [ ] All `SKILL.md` files exist and validate
- [ ] No skill orphans an architecture-design contract item
- [ ] No two skills duplicate the same primary contract item
- [ ] No linter errors introduced

## Implementation Notes
- Use `.cursor/skills/crux-skill-memory-extract/SKILL.md` and
  `.cursor/skills/crux-skill-memory-rebalance/SKILL.md` as the
  template for SKILL.md frontmatter and body shape.
- Honour the project rule
  `crux-skill-memory-meditation-*` is **not** a generated `.crux.md`
  output — these are first-class hand-authored skill files.
- Do **not** wire skills into the coordinator command or the
  guide agent in this subtask — the wiring lives in subtasks 04
  (agent load directives) and 06 (command Related links).
- Do **not** add any of the new skill paths to install / dist /
  manifests in this subtask — that is owned by subtask 10.
- Skill count and naming are fixed to the six approved names in
  the Deliverables Checklist. If execution discovers a reason to
  change them, stop and escalate via `needs_user_input` instead
  of editing the skill plan.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Markdown-only artefacts. Targeted verification: load each
  `SKILL.md` and confirm frontmatter parses (e.g. via `python -c
  "import yaml,frontmatter"` if used elsewhere; otherwise visual
  check).
- Subtask 08 adds substring-presence assertions for each skill.

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer (claude-sonnet-4-6)
- Started: 2026-05-24T05:14:00Z
- Completed: 2026-05-24T05:50:00Z

### Work Log

1. **Read all source files** — `subtask-05-meditate-decomp-skills-extraction-20260517.md`, `meditate-frozen-contract-20260524.md` (1557 lines), `meditate-decomp-architecture-design-20260517.md` (846 lines), `.cursor/agents/crux-cursor-memory-manager.md` (1388 lines), `.cursor/commands/crux-meditate.md` (2142 lines), `.cursor/skills/crux-skill-memory-extract/SKILL.md` (format reference).

2. **Created skill directories** — all six under `.cursor/skills/`.

3. **Created `crux-skill-memory-meditation-research/SKILL.md`** (678 lines) — Phases A–G, steps 1–13, step 4b 4-mode additional_focus_areas[] reconciliation, init-suggestions-{ts}.yml schema, K10c reflection rubric + 11-type catalogue, finalisation-enhancements.yml schema, facet registry protocol, citations-index.yml schema, peer review file spec, comprehensiveness honouring at leaf depth. Canonical `additional_focus_areas[]` array with per-item `treatment:` field used throughout; legacy `_skipped`/`_accepted` field names absent.

4. **Created `crux-skill-memory-meditation-quick/SKILL.md`** (238 lines) — 6-step protocol, step 4b Quick variant, warn-only citation validation, Quick differences table (Quick column), K10c reflection (same rubric, warn-only), Quick leaf depth comprehensiveness honouring. Cross-references Research skill for shared schema.

5. **Created `crux-skill-memory-meditation-ensemble/SKILL.md`** (346 lines) — Ensemble Aggregation steps 1, 2, 3, 3b–3f, 4, 5; per-tree YAML schema; root combined YAML schema with cross_model_candidates + union_candidates; surfaced_to_root write-back; single combined root gate needs_user_input; resume-handler dispatch by source provenance; non-infinite-loop guarantee; ensemble report extras (9 mandatory sections, model attribution Sankey/citation Venn/confidence radar); K10 Ensemble Respawn Targeting.

6. **Created `crux-skill-memory-meditation-review/SKILL.md`** (276 lines) — Reviewer agent contract; editable/read-only/never-touched file lists; **13 review dimensions** (original 11 + Dim 12 Comprehensiveness fidelity + Dim 13 Init-suggestion AND finalisation-enhancement honour); severity classification; Quick relaxations; iteration loop pseudocode (cap 3, ESCALATE); MUST_FIX needs_user_input schema with mandatory context; Pattern-B respawn-with-decision-guidance schema (respawn_reasons list-typed enum including accepted_finalisation_enhancements, missing_sections, missing_visualisations); Report-Skill Respawn Protocol K9 + K10b (payload schema, per-reason processing order, iteration accounting); review document format.

7. **Created `crux-skill-memory-meditation-report/SKILL.md`** (344 lines) — Comprehensiveness Level Mapping (12 dimensions × 4 levels verbatim); paired rule; Anti-Homogenisation Rules; Universal Contrast; light/dark + print TOC; Chart.js / D3 / calculator rules with static fallbacks; Per-Branch Section Rule; Depth-3 Leaf Inclusion Rule; Peer-Review Surfacing Rule; Init-Suggestions Honour rules (with treatment == "report_section_only" filter); finalisation-enhancements honour; K10b Per-Cheap-Type Rendering Contract for all 7 cheap types; Report-Skill Respawn Protocol resume-handler (per-reason order, fuzzy-match auto-resolve, ensemble Per-Branch vs cross-model targeting); headless Chrome → Chromium degradation; Subject-Matter Focus rule; footer annotation format.

8. **Created `crux-skill-memory-meditation-coordination/SKILL.md`** (273 lines) — 18-row artefact filename table (including `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`, `{model-subdir}/finalisation-enhancements.yml`, all 4 follow-up artefact types); placeholders; prefix-glob polling rule + `ls -1t | head -n 1`; never-hard-code invariant; retrospective template (frontmatter + 6 mandatory ### sections); Branch & Leaf Index template (single-model + ensemble variants, with `## Top-level artifacts` block extended with init-suggestions / finalisation-enhancements / follow-up rows); ensemble working-directory structure (directory tree + ensemble filename conventions table).

9. **Updated status files** — S05 status pair (state=completed, all D01–D11 ticked, 6 artefact entries), spec status pair (S05 state=completed, aggregate_progress completed:4, rebuild event appended).

### Blockers Encountered

None.

### Files Modified

- `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md` (created, 678 lines)
- `.cursor/skills/crux-skill-memory-meditation-quick/SKILL.md` (created, 238 lines)
- `.cursor/skills/crux-skill-memory-meditation-ensemble/SKILL.md` (created, 346 lines)
- `.cursor/skills/crux-skill-memory-meditation-review/SKILL.md` (created, 276 lines)
- `.cursor/skills/crux-skill-memory-meditation-report/SKILL.md` (created, 344 lines)
- `.cursor/skills/crux-skill-memory-meditation-coordination/SKILL.md` (created, 273 lines)
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-05-meditate-decomp-skills-extraction-20260517.status.md` (updated)
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-05-meditate-decomp-skills-extraction-20260517.status.yml` (updated)
- `specs/20260517-meditate-agent-skill-decomposition/status.yml` (updated: S05 state=completed, aggregate_progress.completed=4, event appended)
- `specs/20260517-meditate-agent-skill-decomposition/status.md` (updated: progress count, S04+S05 state, events appended)
- `specs/20260517-meditate-agent-skill-decomposition/subtask-05-meditate-decomp-skills-extraction-20260517.md` (this file — Execution Notes appended)
