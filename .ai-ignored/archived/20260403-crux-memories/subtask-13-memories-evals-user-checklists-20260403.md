# Subtask: User Eval Checklists

## Metadata
- **Subtask ID**: 13
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 09, 10
- **Created**: 20260403

## Objective

Create the user evaluation checklists documenting manual/agent-driven testing scenarios for categories J (MindReader) and N (Cross-Platform), plus interactive scenarios for B (Dream) and C (REM Sleep).

## Deliverables Checklist

- [ ] `evals/USER_EVAL_CHECKLISTS.md` documenting manual/agent-driven scenarios for:
  - **B. Dream interactive flow**: Run `/crux-dream` with no args (verify it lists unprocessed plans), run with a plan name (walk through full flow, verify memories saved match expectations), verify conflict detection presents contradictions and asks for resolution
  - **C. REM interactive flow**: Run `/crux-dream --rem` (verify recommendations presented clearly), verify `--yolo` auto-applies everything except conflicts
  - **J. MindReader all invocation modes**: No args (shows referenced memories with rationale), query ("why did you suggest X?"), plan name(s) (shows memories from plans), memory file(s) (decompressed content)
  - **N. Cross-platform flows**: Cursor (full dream/REM/mindreader flow), Claude Code (wiring verification), Generic platform (shell script verification)

## Definition of Done
- [ ] `USER_EVAL_CHECKLISTS.md` contains clear, step-by-step scenarios for each category
- [ ] Each scenario has expected outcomes documented
- [ ] Scenarios reference the correct commands and file paths
- [ ] No ambiguity — a tester can follow each checklist without prior knowledge

## Implementation Notes

Reference `docs/crux-memories.md`:
- Section 5 "Example Interaction" for the expected dream UX
- Section 4 "Viewing" for MindReader invocation modes
- Section 3 "Platform Wiring" for cross-platform differences

User eval checklists are scenario-based and reference the spec directly. They do not require automated test infrastructure.

## Testing Strategy
Not applicable — this subtask produces documentation only.

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
