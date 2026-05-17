# Subtask: Refactor `/crux-meditate` into a Thin Coordinator

## Metadata
- **Subtask ID**: 06
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 04, 05
- **Created**: 20260517

## Objective
Rewrite `.cursor/commands/crux-meditate.md` so that it is a thin
coordinator: it owns argument parsing, calling-agent gates, ensemble
orchestration, and post-tree continuation, but delegates all
Meditate persona / executable contract work to the new
`crux-cursor-meditation-guide` agent (subtask 04) and its associated
`crux-skill-memory-meditation-*` skills (subtask 05). The user-facing
contract must be preserved exactly per the freeze document
(subtask 01).

## Deliverables Checklist
- [ ] Rewrite `.cursor/commands/crux-meditate.md` so that it contains
      only the calling-agent surface from the architecture-design
      doc (subtask 02). Specifically retain:
      - Title + repo link
      - Usage section (no-args, quoted topic, `@` refs, `--quick`,
        `--ensemble`, combined flags)
      - Modes overview table
      - Argument parsing rules (strip flags, derive `meditateMode`,
        `ensembleMode`, read `cruxMemories.meditate.modelPool`,
        `ensembleAggregatorModel`)
      - **`Q-Depth-Selection`** prompt body (calling-agent gate)
      - **`Q-Cost-Acknowledgment`** + **`Q-Cost-Acknowledgment-Expansion`**
        bodies (calling-agent gates)
      - **Theme preflight** Pattern A: Q1–Q5, anti-homogenisation
        block list, `theming:` YAML payload, `surprise_me`
        non-interactive fallback
      - **Facet confirmation resume**: `Q-Confirm-1`, `Q-Confirm-2`,
        `confirmDeepFacets` deep-YAML escalation handling
      - **Ensemble orchestration loop** (calling-agent owns: model
        pool enumeration, parallel tree spawn, batched pending-facet
        cross-tree confirmation, aggregator spawn)
      - **Post-tree steps 9–12**: verify report pair (with regenerator
        loop if PDF / HTML missing), present paths, continuation
        menu (`AskQuestion` allowed here on the calling agent),
        expansion / save-spec / end handling
      - **Coordination conventions pointer**: filename table
        + prefix-glob polling rule (either inline or pointing to
        `.cursor/skills/crux-skill-memory-meditation-coordination/SKILL.md`)
      - **Subagent spawn signature**: Task tool call with
        `subagent_type: crux-cursor-meditation-guide` and the full
        payload schema (mode, topic, depth, preconfirmed facets,
        theming, ensemble peer/aggregator parameters)
      - **`Related`** section listing the new agent + every new
        meditation skill (per subtask 02 design)
- [ ] Remove from the file any executable persona content that was
      moved to the agent or skill layer (Phases A–G prose, Quick 6-
      step prose, Ensemble Aggregation prose, Adversarial Review
      prose, mandatory report prose, retrospective prose) — replace
      with a one-line pointer to where it now lives.
- [ ] Update every reference to `crux-cursor-memory-manager` (in the
      Meditate context) to `crux-cursor-meditation-guide`.
- [ ] Preserve the workspace rule that **tree subagents NEVER call
      `AskQuestion`**; the coordinator (calling agent) is the only
      caller of `AskQuestion`.
- [ ] Verify line-count reduction is meaningful (target: >=50%
      reduction from the current ~1490-line file). If reduction is
      smaller, document the reason in Execution Notes (e.g. theming
      section too large to outsource).
- [ ] Run `python -m py_compile` is **not** applicable; instead
      use the project's markdown lint or local `mdformat --check`
      if available — at minimum, ensure the file renders correctly
      and has no broken anchor links.

## Definition of Done
- [ ] `.cursor/commands/crux-meditate.md` is a thin coordinator
- [ ] Subagent spawn signature targets `crux-cursor-meditation-guide`
- [ ] No executable persona content remains in the command file
- [ ] All calling-agent gates from the freeze contract remain
- [ ] User-facing contract (modes, prompts, gates, report contract,
      continuation menu) is preserved
- [ ] No linter errors introduced
- [ ] No broken internal markdown links in the modified file

## Implementation Notes
- Subtask 04 must be complete (guide agent file exists) before this
  subtask runs, because the spawn signature must match the agent's
  declared `name`.
- Subtask 05 must be complete (skill files exist) before this
  subtask runs, because the `Related` section must reference real
  paths.
- Do **not** modify `crux-cursor-memory-manager.md` here — the
  trim is owned by subtask 07. It is acceptable for the brief
  window during execution where the command no longer references
  the memory manager but the memory manager still contains
  meditate sections; subtask 07 closes that gap.
- Honour the foundational CRUX rule:
  `.cursor/commands/crux-meditate.md` is a source file; do not
  edit any `.crux.md` mirror.
- Update `.crux/crux-memories.json` ONLY if `commands.meditate`
  needs a new `agent` field — most likely no change required since
  the command file path is unchanged. If the JSON does need
  changing, do it here.
- Do not add new dependencies; markdown-only.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Run only file-targeted lint where available.
- Subtask 08 will assert the new spawn signature
  (`crux-cursor-meditation-guide`) and the absence of removed
  executable sections.

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
