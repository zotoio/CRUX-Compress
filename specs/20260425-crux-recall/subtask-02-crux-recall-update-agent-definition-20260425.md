# Subtask: Update Agent Definition

## Metadata
- **Subtask ID**: 02
- **Feature**: crux-recall
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260425

## Objective
Update `.cursor/agents/crux-cursor-memory-manager.md` to rename "MindReader Mode" to "Recall Mode" and update all `/crux-mindreader` references to `/crux-recall`.

## Deliverables Checklist
- [x] "MindReader Mode" renamed to "Recall Mode" throughout the agent definition
- [x] `/crux-mindreader` references updated to `/crux-recall`
- [x] Any `mindreader`/`MindReader` variable names or references updated to `recall`/`Recall`
- [x] Agent behavior and logic preserved — only naming changes

## Definition of Done
- [x] No remaining `mindreader`/`MindReader` references in `.cursor/agents/crux-cursor-memory-manager.md`
- [x] Agent definition is internally consistent with new naming
- [x] No linter errors in modified files

## Implementation Notes
- Read the file first to understand the full scope of references
- The agent definition likely has a mode section header, command references, and possibly operational descriptions that reference MindReader
- Preserve all behavior — this is purely a rename
- Be thorough: check for `mindreader`, `MindReader`, `mindReader`, `mind-reader`, `mind_reader` variants

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Grep the modified file for any remaining `mindreader` references (case-insensitive)
- Verify the file parses correctly as markdown

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-04-25T21:45+10:00
- Completed: 2026-04-25T21:46+10:00

### Work Log
- Read `.cursor/agents/crux-cursor-memory-manager.md` — identified 9 occurrences of MindReader/mindreader
- Renamed frontmatter `description`: "MindReader decompression" → "Recall decompression"
- Renamed intro paragraph: "MindReader queries" → "Recall queries"
- Renamed expertise bullet: "**MindReader**" → "**Recall**"
- Renamed section header: "### MindReader Mode — `/crux-mindreader`" → "### Recall Mode — `/crux-recall`"
- Renamed all 4 invocation table entries: `/crux-mindreader` → `/crux-recall`
- Renamed decompression display note: "MindReader is read-only" → "Recall is read-only"
- Verified zero remaining mindreader/MindReader references via case-insensitive grep
- Confirmed no linter errors

### Blockers Encountered
None

### Files Modified
- `.cursor/agents/crux-cursor-memory-manager.md` — 9 MindReader/mindreader references renamed to Recall/recall

### Adversarial Verification (zoto-spec-judge)
- **Verified by**: zoto-spec-judge (independent)
- **Timestamp**: 2026-04-25T21:57+10:00
- **Verdict**: **Verified**
- Case-insensitive grep for `mindreader|mind.reader|MindReader` returned zero matches in `.cursor/agents/crux-cursor-memory-manager.md`
- "Recall Mode" section header confirmed at line 94: `### Recall Mode — /crux-recall`
- `/crux-recall` references confirmed at lines 94, 102, 103, 104, 105 (invocation table)
- Description field (line 5) confirmed: "Recall decompression" (no MindReader)
- Agent behavior and structure preserved — 174 lines, all operating modes intact
- No linter errors detected
