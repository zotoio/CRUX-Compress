# Subtask: Update Memory Manager Agent Definition

## Metadata
- **Subtask ID**: 02
- **Feature**: crux-remember
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260425

## Objective
Add a "Remember Mode" section to the `crux-cursor-memory-manager` agent definition and update the agent scoping rules to allow ad-hoc base-scope memory creation via `/crux-remember`.

## Deliverables Checklist
- [x] Remember Mode section added to `.cursor/agents/crux-cursor-memory-manager.md` under Operating Modes
- [x] Mode documents all invocation variants (no args, quoted text, `--type` flag) in a table
- [x] Full workflow documented: feature guard → input parsing → type selection via AskQuestion → metadata gathering → CRUD skill delegation → index rebuild → confirmation
- [x] Type options include descriptions for each: idea, learning, redflag, core, goal
- [x] Agent Scoping Rules section updated — rule 1 changed from "Only during dream extraction" to "Only during dream extraction or explicit remember"
- [x] Ad-hoc memories from `/crux-remember` default to base scope (`memories/{type}/`) unless user explicitly requests agent scoping
- [x] Agent's expertise list updated to include ad-hoc memory creation

## Definition of Done
- [x] Remember Mode section is positioned between Recall Mode and Meditate Mode in the Operating Modes hierarchy
- [x] Agent scoping rule explicitly mentions `/crux-remember` as a valid trigger for memory creation
- [x] No linter errors in modified file

## Implementation Notes
- Remember Mode is the simplest operating mode — it creates a single memory with user input, unlike Dream (which extracts from artifacts) or Recall (which queries)
- The scoping rule relaxation is critical: previously only dream extraction could create memories, but `/crux-remember` needs to write to base scope directly
- The workflow mirrors the command file but is authoritative — the command file defers to the agent definition for behavioral details
- AskQuestion type selection keeps the UX consistent with other interactive memory operations

## Testing Strategy
- Verify Remember Mode section exists in the agent definition
- Verify it is positioned correctly in the Operating Modes section
- Verify agent scoping rule mentions both dream extraction and explicit remember
- Grep for "adhoc" to confirm the source tag is documented

## Execution Notes

### Work Performed
1. Added Remember Mode section to `.cursor/agents/crux-cursor-memory-manager.md` after the Recall/Total Visualization section
2. Documented invocation variants table with three rows (no args, quoted text, `--type` flag)
3. Wrote seven-step workflow covering feature guard, input parsing, AskQuestion type selection with type descriptions, metadata gathering, CRUD delegation with `source: "adhoc"`, index rebuild, and confirmation
4. Updated Agent Scoping Rules — changed rule 1 from "Only during dream extraction" to "Only during dream extraction or explicit remember" with clarification that ad-hoc memories default to base scope

### Files Modified
- `.cursor/agents/crux-cursor-memory-manager.md`

### Blockers Encountered
None.
