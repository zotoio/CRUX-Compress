# Subtask: Memory Rebalance Skill

## Metadata
- **Subtask ID**: 07
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 02, 03, 04
- **Created**: 20260403

## Objective

Create the `crux-skill-memory-rebalance` skill that consolidates, promotes, demotes, and archives memories based on strength, usage patterns, and type transition rules.

## Deliverables Checklist
- [ ] `.cursor/skills/crux-skill-memory-rebalance/SKILL.md` — skill definition with:
  - **Consistency verification**: Check for orphaned references (tracker with no memory), stale sources, broken strength chains, tracker files with no matching memory
  - **Conflict detection**: Identify memories that contradict each other (opposing advice, conflicting patterns). Present each conflict with both sides and resolution options
  - **Promote**: Recommend promotion when memory strength exceeds `promoteAt` threshold for its current type. Move file to new type directory, update frontmatter (`type`, `promoted_from`)
  - **Demote**: Recommend demotion when memory unreferenced for longer than `demoteAfterDaysUnreferenced` (default 90 days)
  - **Archive**: Recommend archival when unreferenced for longer than `archiveAfterDaysUnreferenced` (default 180 days). Move to `archived/` directory
  - **Consolidate**: Detect duplicate or near-duplicate memories. Recommend merging with combined content and strength
  - **Rebalance strength**: Sync strength scores with actual reference counts from tracker files
  - **Promote to rule**: Flag memories exceeding `promotionToRuleThreshold` references for potential conversion to a permanent rule
  - **Cleanup**: Identify orphaned tracker files and recommend deletion
  - **Apply changes**: Execute confirmed changes (move files, update frontmatter, delete/merge trackers)
- [ ] Type transition rules read from `typeTransitions` config
- [ ] Temporal thresholds read from `demoteAfterDaysUnreferenced` and `archiveAfterDaysUnreferenced`
- [ ] REM sleep summary written to `archiveDir` as `rem-{yyyymmdd}.md`

## Definition of Done
- [ ] SKILL.md clearly documents all rebalance operations
- [ ] SKILL.md handles the complete REM sleep workflow (steps 1-8 from spec)
- [ ] SKILL.md specifies conflict detection and resolution
- [ ] SKILL.md references type transition config from `.crux/crux-memories.json`
- [ ] No linter errors in modified files

## Implementation Notes

Reference `docs/crux-memories.md`:
- "REM Sleep Workflow" section (steps 1-8) for the full rebalance flow
- "Strength → Type Transition Rules" section for promotion/demotion thresholds
- Type transitions are configurable per-repo (read from config, don't hard-code)

The rebalance skill is invoked during REM sleep (`/crux-dream --rem`). It produces a comprehensive report of recommended changes, waits for user confirmation (or auto-applies in `--yolo` mode except for conflicts which always require user input), then executes.

When moving files between type directories:
1. Create target directory if needed
2. Move the memory file
3. Update frontmatter: change `type`, add `promoted_from` (or `demoted_from`), update `modified`
4. If the memory has a compressed version, move that too
5. The reference tracker file stays in `.crux/reference-tracking/` (it references by slug, not path)

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Review SKILL.md for completeness against spec
- Defer full test suite execution to the final verification phase

## Execution Notes
[To be filled by executing agent]

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
