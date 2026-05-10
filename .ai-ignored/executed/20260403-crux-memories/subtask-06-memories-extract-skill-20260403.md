# Subtask: Memory Extract Skill

## Metadata
- **Subtask ID**: 06
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 02, 03
- **Created**: 20260403

## Objective

Create the `crux-skill-memory-extract` skill that analyses execution artifacts from completed plans, compares with existing memories, and proposes candidate facts for memory creation.

## Deliverables Checklist
- [ ] `.cursor/skills/crux-skill-memory-extract/SKILL.md` — skill definition with:
  - **Verify execution**: Check `_execution-state.yml` (or configured `stateFile`) for plan completion status
  - **Diff analysis**: Diff repo changes since plan start. If changes exceed `maxUnrelatedChanges` threshold, warn and optionally abort
  - **Analyse artifacts**: Read plan execution output, agent work logs, and code changes to identify learnings, patterns, red flags, ideas, and goals
  - **Compare with existing**: Load existing memories and compare candidates against them for relevance and novelty
  - **Conflict detection**: Identify candidates that contradict existing memories. Present both sides to the user with options: keep existing, replace, merge, or keep both with disambiguation
  - **Rank candidates**: Present top N candidates (configurable via `maxCandidateFacts`, default 5) ordered by estimated value
  - **Classify type**: Assign each candidate a type (`core`, `redflag`, `goal`, `learning`, `idea`) based on content analysis
  - **Agent scoping**: When plan artifacts identify a specific agent persona and the memory is agent-specific, mark for placement in `memories/agents/{agent-id}/`
- [ ] Candidate fact format: type, title, description, tags, rationale for inclusion
- [ ] Integration with `crux-skill-memory-crud` for actual memory creation

## Definition of Done
- [ ] SKILL.md clearly documents the extraction workflow
- [ ] SKILL.md handles conflict detection and resolution flow
- [ ] SKILL.md handles agent-scoped vs base memory classification
- [ ] SKILL.md references dream config from `.crux/crux-memories.json`
- [ ] No linter errors in modified files

## Implementation Notes

Reference `docs/crux-memories.md`:
- "Dream Workflow" section (steps 1-8) for the full extraction flow
- "Agent-Scoped Memories" section for agent classification rules
- Section 5 "Example Interaction" for the expected UX

The `unitOfWork` is `plan` for this repo, so the skill looks for plan execution artifacts rather than "specs". The skill should read `unitOfWork` from config and use it generically.

Candidate classification heuristics:
- **core**: Fundamental patterns that should always be followed
- **redflag**: Bugs, anti-patterns, or pitfalls discovered during execution
- **goal**: Performance targets, quality metrics achieved or set
- **learning**: Techniques, approaches, or insights gained
- **idea**: Speculative improvements or future work suggested by the execution

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
