# Subtask: Implement `crux-cursor-meditation-guide` Agent

## Metadata
- **Subtask ID**: 04
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 02
- **Created**: 20260517

## Objective
Create the new agent file
`.cursor/agents/crux-cursor-meditation-guide.md` that contains the
Meditate persona and every executable contract that the architecture-
design doc (subtask 02) assigned to the agent layer. The new file must
be a complete, working agent on its own — the coordinator command
(subtask 06) and the meditation skills (subtask 05) wire up to it,
not the other way round.

## Deliverables Checklist
- [ ] Create `.cursor/agents/crux-cursor-meditation-guide.md` with
      project-standard frontmatter (`name: crux-cursor-meditation-guide`,
      `description`, `color`, allowed `tools`, `model` matching the
      memory-manager's reasoning-class model — typically a
      thinking-class Opus default).
- [ ] **Persona prologue** ("You are the CRUX Meditation Guide…")
      that mirrors the tone of `crux-cursor-memory-manager.md` and
      states the read-only-with-optional-memory-creation contract
      from memory `meditate-uses-read-only-exploration-with-optional-memory-creation`.
- [ ] **Mode router**: dispatches inbound `Task` invocations to
      Research / Quick / Ensemble Aggregation / Adversarial Review
      / Reports & Retrospective sub-modes based on payload keys
      (`meditateMode`, `ensembleMode`, `meditateDepth`,
      `preConfirmedFacets`, `ensembleModel`, …). Mirror the current
      invocation table from `crux-cursor-memory-manager.md`'s
      Meditate section.
- [ ] **Phases A–G research workflow** (Research mode default,
      depth-3 default), including facet registry + lock semantics,
      citations index, peer review file spec, and citation respawn
      rule (≤2 retries) — sourced from the freeze contract in
      subtask 01.
- [ ] **Quick 6-step protocol** (`--quick`), warn-only citations,
      upfront child derivation.
- [ ] **Ensemble Aggregation sub-mode**: aggregator reads all
      `consolidation.md` outputs and writes `cross-model-synthesis.md`
      + `ensemble-report-{topic-slug}-{ts}.{html,pdf}`.
- [ ] **Adversarial Review sub-mode**: 11 dimensions, severities
      (`MUST_FIX` / `SHOULD_FIX` / `NICE_TO_HAVE`), ≤3 iterations,
      `needs_user_input` schema with `question_id`,
      `prompt`, `options`, mandatory `context`, and the reviewer
      review-doc template.
- [ ] **Skill load directives**: every sub-mode that maps to a new
      skill (per subtask 02 design) must explicitly say
      "read the relevant skill file at … before executing", citing
      the exact skill path (e.g.
      `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md`).
- [ ] **`needs_user_input` envelope schema** documented with the
      mandatory `context` field and the rule "tree subagents NEVER
      call `AskQuestion`". Include the adversarial-loop variant.
- [ ] **Subagent invocation contracts** that the agent itself
      spawns (branch / peer / reviewer children, ensemble peer
      trees) with payload schemas — copy from the current memory
      manager Meditate section, updated to reference the guide
      agent itself.
- [ ] **Coordination conventions pointer**: file-naming table,
      prefix-glob polling rule, registry lock, retro template, branch
      & leaf index template — either inline (if the design doc
      kept it on the agent) or as a load directive into the
      coordination skill.
- [ ] **Mandatory report contract pointer / inline**: paired HTML +
      PDF, anti-homogenisation, Universal Contrast, light/dark/print,
      Chart.js / D3 / calculator inclusion + static fallback rules,
      headless Chrome → Chromium degradation (per design doc, this
      is owned by the report skill but the agent must reference it).

## Definition of Done
- [ ] `.cursor/agents/crux-cursor-meditation-guide.md` exists and is
      well-formed
- [ ] Frontmatter validates against the project's agent file convention
- [ ] All sections from the architecture design's "agent layer"
      column are present
- [ ] No content from the freeze contract assigned to the agent layer
      is missing
- [ ] No linter errors in the new file
- [ ] File is added to `git status` (untracked, not staged unless
      project convention requires)

## Implementation Notes
- Read `.cursor/agents/crux-cursor-memory-manager.md` for the persona
  voice, invocation-table format, and `needs_user_input` schema —
  copy structures verbatim where appropriate, adjusted for the new
  agent name.
- Do **not** delete or touch
  `.cursor/agents/crux-cursor-memory-manager.md` in this subtask —
  trimming is owned by subtask 07.
- Do **not** modify `.cursor/commands/crux-meditate.md` here — the
  command refactor is owned by subtask 06.
- Follow the foundational CRUX rule: do not introduce a generated
  `.crux.md` mirror as part of this subtask. Subtask 11 handles
  CRUX compression of any source file that warrants it.
- The agent file is a **source** file (no generated frontmatter), so
  it is hand-edited.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Markdown-only artefact in this subtask. Targeted lint:
  `python -m pyflakes` is irrelevant; markdown lint may apply
  through repo hooks.
- A presence test in subtask 08 will assert the file exists with
  the expected frontmatter `name`.

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-05-24T05:20:00Z
- Completed: 2026-05-24T05:45:00Z

### Work Log

1. Read subtask-04 spec, frozen contract (meditate-frozen-contract-20260524.md), architecture
   design §1 (guide-agent spec, §1.3 mode router, §1.4 budget ≤500 lines), memory manager
   source (lines 279–1159 Meditate Mode + 1189–1349 Ensemble Aggregation Mode) for persona
   voice, invocation table, design principles, and step details.
2. Created `.cursor/agents/crux-cursor-meditation-guide.md` with exact frontmatter from user
   query constraint #2, persona prologue mirroring crux-cursor-memory-manager.md shape,
   User Input Escalation block verbatim from memory-manager, Your Expertise bullets per §1.2
   point 4, 6-row Skills You Use table, mode router with invocation variants table + preamble,
   Research steps 1–13 (incl. 4b, 8b, 12b) as one-paragraph-each summaries, Quick mode
   substitution table, K10 Reflection function section (new row per §1.3 row 5), Adversarial
   Review function, Ensemble Aggregation function, Report generation obligation, Design
   Principles (21 bullets derived from memory-manager 1137–1158 plus new richness-era bullets),
   Agent Scoping Rules, and Critical Rules.
3. First draft: 565 lines (over budget). Trimmed Research steps 4, 4b, 8, 8b, 12 and Design
   Principles bullets to reduce to 495 lines (within ≤500 budget).
4. Verified: 6 distinct skills referenced, comprehensiveness: invariant with canonical error
   string, K10 reflection has own mode-router section, legacy `additional_focus_areas_skipped`/
   `additional_focus_areas_accepted` absent (prohibition restated in Critical Rules), AskQuestion
   Critical Rule restated.
5. Updated S04 status pair (state: completed, all checklist items ticked) and spec status.yml
   (aggregate_progress: completed: 3, S04 state: completed, rebuild event appended).

### Blockers Encountered
None.

### Files Modified
- `.cursor/agents/crux-cursor-meditation-guide.md` — **CREATED** (495 lines)
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-04-meditate-decomp-guide-agent-20260517.status.md` — updated to completed
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-04-meditate-decomp-guide-agent-20260517.status.yml` — updated to completed
- `specs/20260517-meditate-agent-skill-decomposition/status.yml` — S04 → completed; aggregate_progress 3/12; rebuild event

## Deliverables Checklist
- [x] Create `.cursor/agents/crux-cursor-meditation-guide.md` with project-standard frontmatter
- [x] **Persona prologue** with Load Context First + User Input Escalation + Your Expertise
- [x] **Mode router** dispatching to Research / Quick / K10 Reflection / Adversarial Review / Ensemble Aggregation / Report generation
- [x] **Phases A–G research workflow** (pointer to skill:research; step summaries in router)
- [x] **Quick 6-step protocol** (pointer to skill:quick; substitution table in router)
- [x] **Ensemble Aggregation function** (K10 layered cadence pointer to skill:ensemble)
- [x] **Adversarial Review function** (13 dimensions pointer to skill:review)
- [x] **Skill load directives** for all 6 crux-skill-memory-meditation-* skills
- [x] **`needs_user_input` envelope schema** with mandatory `context`; AskQuestion Critical Rule
- [x] **Subagent invocation contracts** (invocation variants table + spawn parameter summaries)
- [x] **Coordination conventions pointer** to skill:coordination
- [x] **Mandatory report contract pointer** to skill:report

## Definition of Done
- [x] `.cursor/agents/crux-cursor-meditation-guide.md` exists and is well-formed
- [x] Frontmatter validates against project agent file convention (name, model, color, description, tools)
- [x] All sections from the architecture design's "agent layer" column present
- [x] No content from the freeze contract assigned to the agent layer is missing (all delegated to skills)
- [x] No linter errors in the new file (markdown-only artefact)
- [x] File is added to git status (untracked)
