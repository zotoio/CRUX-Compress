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
  `.crux.md` mirror as part of this subtask. Subtask 10 handles
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
*(to be filled by executing agent)*

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
[Agent adds notes here during execution]

### Blockers Encountered
[Any blockers or issues]

### Files Modified
[List of files changed]
