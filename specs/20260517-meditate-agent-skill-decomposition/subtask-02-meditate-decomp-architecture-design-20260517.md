# Subtask: Architecture Design — Agent + Skill Boundaries

## Metadata
- **Subtask ID**: 02
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 01
- **Created**: 20260517

## Objective
Translate the frozen contract from subtask 01 into a concrete section-by-section
mapping that places every contract item in exactly one of:
(a) the thin coordinator command, (b) the new
`crux-cursor-meditation-guide` agent, or (c) one of the new
`crux-skill-memory-meditation-*` skills. Produce a design document that
subsequent implementation subtasks (04, 05, 06, 07) can follow without
ambiguity.

## Deliverables Checklist
- [ ] Create `meditate-decomp-architecture-design-20260517.md` inside this
      spec directory.
- [ ] **Final agent specification**: `crux-cursor-meditation-guide`
      frontmatter (`name`, `description`, `color`, `tools`, `model`),
      persona prologue, mode router, and the executable section list
      (Phases A–G research, Quick 6-step, Ensemble Aggregation,
      Adversarial Review, Reports & Retrospective). Mark which
      sections call which skills.
- [ ] **Final skill list** with one row per skill:
      directory name, `SKILL.md` `name` + `description`, scope
      summary, contract items it owns, the agent / command callers
      that load it, and any cross-skill dependencies. Default
      proposal is the six skills listed in spec K3, but you may
      consolidate (e.g. fold ensemble into research) or split
      (e.g. extract `meditation-theming`) if the contract justifies
      it. Document the rationale.
- [ ] **Section-mapping table**: one row per contract item from
      subtask 01 → destination
      (`command` / `agent` / `skill:<skill-name>`). Items that must
      appear in **both** the agent and a skill (e.g. invocation
      contract referenced by both) must be flagged with a "primary"
      destination and a "mirror" destination.
- [ ] **Coordinator command shape**: outline what stays in
      `.cursor/commands/crux-meditate.md` after decomposition
      (argument parsing, mode flag handling, `Q-Depth-Selection`,
      `Q-Cost-Acknowledgment` + expansion variant, theme preflight,
      facet confirmation resume, ensemble orchestration loop, post-
      tree steps 9–12, continuation menu). Include the new spawn
      signature (Task tool call to `crux-cursor-meditation-guide`).
- [ ] **Memory-manager trim plan**: list every section / heading to
      delete from `crux-cursor-memory-manager.md`, plus the pointer
      paragraph that replaces it. Explicitly call out sections that
      must remain (Dream / REM / Recall / Remember / Forget agent
      contracts, shared `needs_user_input` envelope schema if it is
      generic).
- [ ] **Backwards-compat plan**: what happens during the brief
      window where the new agent exists but the command still
      references the memory manager (only inside subtask 06, before
      subtask 07 lands). Specify whether 06 must also update
      memory-manager pointers, or whether 07 handles it.
- [ ] **Risks & open questions**: list any contract items where the
      destination is ambiguous and flag them for `needs_user_input`
      escalation by the executor (Pattern B).

## Definition of Done
- [ ] Design document exists in spec directory
- [ ] Every contract item from subtask 01 has a single primary destination
- [ ] Skill list is finalised (count, names, scopes)
- [ ] Coordinator command shape is documented with new spawn signature
- [ ] Memory-manager trim plan covers every Meditate section in the current file
- [ ] No linter errors introduced

## Implementation Notes
- This is a **read-only** subtask — produce a design document only.
- Reference subtask 01's freeze document by path; do not re-summarise
  the entire contract here.
- Pre-empt eval coverage gaps that subtask 03 will need: each
  destination should be discoverable by a substring assertion (e.g.
  the agent file should contain `crux-cursor-meditation-guide` in
  its frontmatter, each skill should mention `meditation` in its
  description).
- Honour the workspace `zip-contents-protection` rule — note that
  every new file path is a deliberate addition that must be
  enumerated by subtask 09.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Markdown-only artefact; no automated tests apply beyond markdown lint.

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
