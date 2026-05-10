# Subtask: Update Core Memories Documentation

## Metadata
- **Subtask ID**: 03
- **Feature**: crux-forget
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 01, 02
- **Created**: 20260406

## Objective
Update `docs/crux-memories.md` — the canonical memories documentation — to include the `/crux-forget` command in all relevant sections: the commands table, the workflow description, and the example interactions.

## Deliverables Checklist
- [x] `/crux-forget` added to the Commands table in section 1
- [x] Forget workflow documented (new subsection under "Dream Workflow" / after "REM Sleep Workflow", or integrated appropriately)
- [x] Config schema's `commands` section updated to include `forget` entry
- [x] Platform Capability Mapping table updated if needed
- [x] Example interaction section includes a forget example
- [x] Evaluation section updated with forget-specific evals

## Definition of Done
- [x] `docs/crux-memories.md` updated with all forget command references
- [x] No linter errors in modified file

## Implementation Notes

### File to Edit
`docs/crux-memories.md`

### Changes Required

**1. Section 1 — Commands table (around line 15-21):**
Add a new row to the commands table:

```markdown
| forget [memory... | query] | `/crux-forget` | Remove incorrect or unwanted memories from the corpus. Pass memory ID(s), slug(s), file path(s), or a search query. If omitted, lists all memories for selection |
```

**2. Section 2 — Configuration Schema — `commands` block (around line 273-284):**
Add a `forget` entry to the commands JSON:

```json
"forget": {
  "file": ".cursor/commands/crux-forget.md",
  "default": "/crux-forget",
  "description": "Remove incorrect or unwanted memories"
}
```

**3. Section 3 — Platform Wiring:**
- In section 3a (Cursor Wiring), subsection D (Commands), add `/crux-forget` to the list of commands pointed to by config
- In section 3b (Claude Code Wiring), subsection C (Commands), add `.claude/commands/crux-forget.md`
- In section 3c (Generic), subsection C (Commands), add `crux-forget` shell script reference

**4. Platform Capability Mapping table:**
The mapping table (around line 233-241) references commands — ensure the pattern `/crux-forget` is covered under the Cursor/Claude Code/Generic columns.

**5. New subsection — Forget Workflow:**
Add a brief subsection (after REM Sleep Workflow or at an appropriate location) describing the forget workflow:
- Resolve input to memory files
- Display matched memories for confirmation
- Delete confirmed memories and their reference trackers
- Rebuild the memory index
- Report deletions

**6. Section 5 — Example Interaction:**
Add a short example showing `/crux-forget` usage, e.g.:

```
User: "/crux-forget a1b2c3d"

CRUX: "Found memory matching ID a1b2c3d:

       [learning] React.memo on list items reduced re-render time
       from 480ms to 12ms on 500-item lists
       Strength: 3 | Source: 20260403-component-library

       Are you sure you want to forget this memory? [yes/no]"

User: "yes"

CRUX: "✅ 1 memory forgotten:
       - [learning] a1b2c3d — React.memo on list items...
       - Reference tracker removed
       - Memory index rebuilt

       This knowledge has been removed from the corpus."
```

**7. Section 8 — Evaluations:**
Add a new subsection for forget-specific evals:

```markdown
### O. Forget Command

- **Dev:** Run `/crux-forget` with a valid memory ID, verify the memory file and its tracker are deleted
- **Dev:** Run `/crux-forget` with a valid slug, verify resolution and deletion
- **Dev:** Run `/crux-forget` with a search query, verify matching memories are presented for selection
- **Dev:** Run `/crux-forget` with no arguments, verify all memories are listed for selection
- **Dev:** Verify memory index is rebuilt after deletion
- **User:** Run `/crux-forget`, select memories to delete, verify they are no longer in the corpus
- **User:** Run `/crux-forget "nonexistent"`, verify graceful handling of no matches
```

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify the commands table has the new entry
- Verify the config schema has the forget command entry
- Verify no existing documentation was accidentally removed
- Check for consistent formatting with existing sections

## Execution Notes

### Agent Session Info
- Agent: generalPurpose
- Started: 2026-04-07
- Completed: 2026-04-07

### Work Log
All 7 change areas applied to `docs/crux-memories.md`:

1. **Commands table (section 1):** Added `/crux-forget` row with full description
2. **Config schema (section 2):** Added `forget` entry to `commands` JSON block
3. **Platform Wiring (section 3):**
   - 3a Cursor: Updated subsection D to list all three command files
   - 3b Claude Code: Updated subsection C to include `.claude/commands/crux-forget.md`
   - 3c Generic: Updated subsection C with `crux-forget` shell script example
4. **Platform Capability Mapping table:** Expanded Commands row to list all three commands across all platforms
5. **Platform Selection table:** Added `crux-forget` to generic shell scripts list
6. **Agent description:** Updated agent command list, added Forget operations to responsibilities, added Claude Code platform equivalent
7. **Forget Workflow subsection:** New subsection after REM Sleep Workflow describing the 5-step forget workflow
8. **Example interaction (section 5):** Added forget example showing ID-based deletion with confirmation
9. **What Consumers Do NOT Implement (section 6):** Added "Memory deletion (forget workflow)"
10. **Evaluations (section 8):** Added subsection O with 9 forget-specific evals (6 dev, 3 user), updated cross-platform evals in section N to include forget

### Blockers Encountered
None.

### Files Modified
- `docs/crux-memories.md` — all forget command references added across 10 change points

### Adversarial Verification (Judge)
- **Verifier**: zoto-spec-judge
- **Date**: 2026-04-07
- **Verdict**: **Verified**

**Deliverables Checklist — independently confirmed:**
- [x] `/crux-forget` row in Commands table (line 21)
- [x] `forget` command entry in Configuration Schema JSON (lines 298-302)
- [x] Cursor wiring (3a) mentions `/crux-forget` (line 694)
- [x] Claude Code wiring (3b) mentions `/crux-forget` (line 749)
- [x] Generic wiring (3c) mentions `crux-forget` (lines 791-805)
- [x] Platform Capability Mapping table includes `/crux-forget` across all 3 platforms (line 250)
- [x] Forget Workflow subsection exists with 5-step workflow (lines 225-236)
- [x] Example interaction includes forget example with confirmation flow (lines 918-937)
- [x] Evaluations section O has 9 forget-specific evals (lines 1080-1091)
- [x] Cross-platform evals (section N) updated to include forget (line 1076-1078)

**Definition of Done — independently confirmed:**
- [x] `docs/crux-memories.md` updated with all forget command references (1100 lines, all original sections intact)
- [x] No linter errors (verified via ReadLints)

**Additional observations:**
- Agent description and platform equivalents table also updated (lines 43, 81)
- "What Consumers Do NOT Implement" section includes "Memory deletion (forget workflow)" (line 952)
- No existing content was removed; all original sections verified intact
