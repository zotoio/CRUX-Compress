# Subtask: Update Memory Manager Agent with Forget Mode

## Metadata
- **Subtask ID**: 02
- **Feature**: crux-forget
- **Assigned Subagent**: generalPurpose
- **Dependencies**: None
- **Created**: 20260406

## Objective
Add a Forget mode to the memory manager agent definition (`.cursor/agents/crux-cursor-memory-manager.md`) so the agent knows how to handle `/crux-forget` invocations. This complements the existing Dream, REM Sleep, and MindReader modes.

## Deliverables Checklist
- [x] Forget mode section added to `.cursor/agents/crux-cursor-memory-manager.md` under "Operating Modes"
- [x] Forget mode workflow documented with clear steps
- [x] Forget mode listed in the agent's "Your Expertise" section
- [x] No existing content removed or broken

## Definition of Done
- [x] Agent file updated with Forget mode
- [x] No linter errors in modified file

## Implementation Notes

### File to Edit
`.cursor/agents/crux-cursor-memory-manager.md`

### Reference: Existing Operating Modes
The agent already has three modes:
1. **Dream Mode** — `/crux-dream <spec-name>` — Extract memories from completed work
2. **REM Sleep Mode** — `/crux-dream --rem` — Rebalance the entire memory corpus
3. **MindReader Mode** — `/crux-mindreader` — Query and display memories

### Changes Required

**1. Add to "Your Expertise" section:**
Add a bullet for Forget: `- **Memory Removal**: Resolving, confirming, and deleting memories and their associated reference trackers`

**2. Add Forget Mode under "Operating Modes":**

```markdown
### Forget Mode — `/crux-forget`

Remove one or more memories from the corpus.

**Workflow**:

1. **Parse Input**: Determine the input type from `$ARGUMENTS`:
   - Memory ID(s) (7-char hex hash): Scan the memory index for matches
   - Slug(s): Search `memoriesDir` recursively for matching files
   - File path(s): Read the specified files directly
   - Quoted text (search query): Search memories by title, description, tags
   - No arguments: Load the full memory index and present all memories

2. **Resolve Memories**: For each input, resolve to one or more memory files. If no matches found, report to the user and stop.

3. **Display for Confirmation**: Show matched memories with their ID, title, type, strength, and source. Use a table format for clarity.

4. **Confirm Deletion**: Ask the user to confirm which memories to delete. Never auto-delete — forgetting is destructive and irreversible.

5. **Delete Memories**: For each confirmed memory, delegate to `crux-skill-memory-crud` Delete operation. This handles:
   - Removing the memory file
   - Removing the corresponding reference tracker from `trackingDir`

6. **Rebuild Index**: Invoke `crux-skill-memory-index` to refresh `.crux/memory-index.yml`.

7. **Report**: Summarize what was deleted — count, types, and IDs of removed memories.
```

### Structural Guidelines
- Place the Forget Mode section after MindReader Mode in the "Operating Modes" section
- Follow the same documentation pattern (workflow steps, bold labels, code references)
- Keep the section concise — Forget is simpler than Dream or REM Sleep

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify the new section exists in the agent file
- Verify the section references `crux-skill-memory-crud` Delete
- Verify the section references `crux-skill-memory-index`
- Verify no existing content was accidentally removed

## Execution Notes

### Agent Session Info
- Agent: generalPurpose (subagent)
- Started: 20260407
- Completed: 20260407

### Work Log
- Read existing agent file to understand structure and operating modes
- Added "Memory Removal" bullet to "Your Expertise" section (line 24)
- Added "Forget Mode — `/crux-forget`" section after MindReader Mode (lines 109–134)
- Verified all existing content preserved — no lines removed or modified
- Ran linter — no errors

### Blockers Encountered
None

### Files Modified
- `.cursor/agents/crux-cursor-memory-manager.md` — added Forget expertise bullet + Forget Mode operating mode section

### Adversarial Verification (zoto-spec-judge)
- **Verified by**: zoto-spec-judge (independent verifier)
- **Date**: 2026-04-07
- **Verdict**: **Verified**
- Forget Mode section exists at line 109 under Operating Modes — confirmed via Grep and Read
- Placed correctly after MindReader Mode (MindReader ends line 107, Forget starts line 109)
- "Your Expertise" section includes "Memory Removal" bullet at line 24
- Workflow has 7 clear steps: Parse Input, Resolve Memories, Display for Confirmation, Confirm Deletion, Delete Memories, Rebuild Index, Report
- References `crux-skill-memory-crud` Delete operation (line 128)
- References `crux-skill-memory-index` (line 132)
- All existing modes verified intact: Dream (lines 42-71), REM Sleep (lines 72-92), MindReader (lines 94-107)
- Agent Scoping Rules, Critical Rules, and Skills table all preserved
- No linter errors confirmed via ReadLints
- **No issues found**
