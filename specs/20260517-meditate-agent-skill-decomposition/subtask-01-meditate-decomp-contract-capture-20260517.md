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
that the integrity-review subtask (11) can mechanically diff post-refactor
artefacts against it.

## Deliverables Checklist
- [ ] Create `meditate-frozen-contract-20260517.md` inside this spec
      directory containing all sections below.
- [ ] **Modes inventory**: Research (default), `--quick`, `--ensemble`,
      combined `--quick --ensemble`. For each: trigger, calling-agent
      vs subagent ownership, key flags / config keys
      (`cruxMemories.meditate.modelPool`, `ensembleAggregatorModel`,
      depth defaults, ensemble facet batching).
- [ ] **Calling-agent gates** verbatim or near-verbatim text:
      `Q-Depth-Selection`, `Q-Cost-Acknowledgment`,
      `Q-Cost-Acknowledgment-Expansion`, theme preflight Q1–Q5 +
      `theming:` YAML payload + `surprise_me` non-interactive fallback,
      facet confirmation `Q-Confirm-1` / `Q-Confirm-2` and
      `confirmDeepFacets` deep-YAML escalation.
- [ ] **Pattern A vs Pattern B** boundaries: which prompts run before
      spawning the tree, which run as `needs_user_input` escalations
      from the tree.
- [ ] **Subagent contracts** (today on `crux-cursor-memory-manager`):
      Phases A–G research, Quick 6-step, Ensemble Aggregation,
      Adversarial Review (11 dimensions, severities, ≤3 iterations,
      `MUST_FIX` `needs_user_input` schema with mandatory `context`
      field).
- [ ] **Coordination conventions**: artefact filename table
      (`meditations/{yyyymmdd}-{topic-slug}/...`), prefix-glob polling
      rule ("never hard-code report names"), facet registry lock
      semantics, citations index format, peer-review file spec,
      retrospective template (`retrospective-{ts}.md`),
      Branch & Leaf Index template appended to `facets.md`.
- [ ] **Mandatory report contract**: paired HTML + PDF, anti-homogenisation
      rules, Universal Contrast / WCAG-style colour rules, light/dark
      theme + print TOC, Chart.js / D3 / calculator inclusion rules,
      static fallback rules for D3 / calculators, headless Chrome →
      Chromium degradation, ensemble aggregation report extras
      (`cross-model-synthesis.md`, ensemble HTML/PDF).
- [ ] **Continuation menu** (steps 9–12 calling-agent): verify report
      pair, present paths, expansion / save-spec / end handling.
- [ ] **Cross-repo touchpoints**: `/crux-amnesia` explicit-command
      list inclusion, `commands.meditate` config entry in
      `.crux/crux-memories.json`, AGENTS.md table row, README rows,
      `docs/crux-memories.md` description, `web/compress.md/memories.html`
      copy, `install.py` / `create-crux-zip.py` enumerations.
- [ ] **Source-of-truth map**: line ranges (or section headings) in the
      *current* `.cursor/commands/crux-meditate.md` and
      `.cursor/agents/crux-cursor-memory-manager.md` for each contract
      item, so subtask 02 can plan moves and subtask 11 can verify.

## Definition of Done
- [ ] Freeze document exists in spec directory
- [ ] Every contract item is traceable back to a current source line range or section heading
- [ ] Document is referenced from the spec index (Execution Notes) so later subtasks can find it
- [ ] No linter errors introduced (markdown-only artefact)

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
