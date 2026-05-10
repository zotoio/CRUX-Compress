# Subtask: Update Project Documentation (README, CONTRIBUTORS, AGENTS)

## Metadata
- **Subtask ID**: 04
- **Feature**: crux-forget
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 01, 02
- **Created**: 20260406

## Objective
Update the three project-level documentation files — `README.md`, `CONTRIBUTORS.md`, and `AGENTS.md` — to reference the new `/crux-forget` command and its command file.

## Deliverables Checklist
- [x] `README.md` — Memory Commands table updated with `/crux-forget` entries
- [x] `README.md` — Memories section overview updated to mention Forget capability
- [x] `CONTRIBUTORS.md` — Distributed files table updated with `.cursor/commands/crux-forget.md`
- [x] `CONTRIBUTORS.md` — Memory System Components table updated
- [x] `AGENTS.md` — Memory manager purpose column updated to include Forget

## Definition of Done
- [x] All three files updated with correct references
- [x] No linter errors in modified files
- [x] No existing content accidentally removed

## Implementation Notes

### File 1: `README.md`

**Memory Commands table (around line 663-672):**
Add these rows to the existing table:

```markdown
| `/crux-forget <memory-id>` | Forget a specific memory by ID |
| `/crux-forget "query"` | Search and select memories to forget |
```

**Memories section overview (around line 622-630):**
The overview currently mentions Dream, REM Sleep, and MindReader. Add a bullet for Forget:
```markdown
- **Forget** — Remove incorrect or unwanted memories from the corpus
```

**File inventory tables (around line 880-895):**
The component tables in README list commands. Add the forget command to the relevant table row if commands are listed individually. The table at line ~875 has:
```
| Compress Command    | `.cursor/commands/crux-compress.md`          | Compression interface          |
```
Add a similar row for:
```
| Forget Command      | `.cursor/commands/crux-forget.md`            | Memory removal interface       |
```

### File 2: `CONTRIBUTORS.md`

**Distributed files table (around line 257-267):**
Add a row for the new command file:
```markdown
| `.cursor/commands/crux-forget.md` | Memory forget command |
```
Place it after the existing `crux-mindreader.md` entry.

**Memory System Components table (around line 271-286):**
Add a row:
```markdown
| `.cursor/commands/crux-forget.md` | Yes | Memory forget command |
```
Place it after the existing `crux-mindreader.md` entry.

### File 3: `AGENTS.md`

**Memory manager agent row (line 27):**
Update the Purpose column from:
```
Memory lifecycle management (dream, REM sleep, MindReader)
```
to:
```
Memory lifecycle management (dream, REM sleep, MindReader, Forget)
```

**IMPORTANT**: `AGENTS.md` is a source file in this repository (not generated). Edit it directly.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify each file contains the new `/crux-forget` references
- Verify table formatting is consistent with existing entries
- Verify no content was accidentally removed (compare line counts before/after)

## Execution Notes

### Agent Session Info
- Agent: generalPurpose (subtask-04)
- Started: 2026-04-07
- Completed: 2026-04-07

### Work Log
1. Read all three target files to find exact edit locations
2. README.md: Added "Forget" bullet to memory lifecycle overview (updated "three phases" → "four phases"), added two `/crux-forget` rows to Memory Commands table, added Forget Command row to File Locations Summary table
3. CONTRIBUTORS.md: Added `.cursor/commands/crux-forget.md` row to Release-Relevant Files table and to Memory System Components table (both placed after `crux-mindreader.md`)
4. AGENTS.md: Updated `crux-cursor-memory-manager` Purpose column to include "Forget"
5. Verified all edits via spot-check reads; confirmed no linter errors

### Blockers Encountered
None

### Files Modified
- `README.md` — 3 additions (lifecycle overview bullet, 2 command table rows, 1 file inventory row) + phrase fix ("three phases" → "four phases")
- `CONTRIBUTORS.md` — 2 additions (1 row in distributed files table, 1 row in memory system components table)
- `AGENTS.md` — 1 edit (memory manager purpose column)

### Adversarial Verification (Judge)
- **Verifier**: zoto-spec-judge
- **Date**: 2026-04-07
- **Verdict**: **Verified**

**Deliverables Checklist — independently confirmed:**

README.md:
- [x] Memory Commands table has `/crux-forget <memory-id>` and `/crux-forget "query"` rows (lines 673-674)
- [x] Memories section overview mentions Forget as fourth phase (line 631), updated "three phases" → "four phases" (line 626)
- [x] File Locations Summary table includes Forget Command row (line 896)

CONTRIBUTORS.md:
- [x] Release-Relevant Files table includes `.cursor/commands/crux-forget.md` (line 262)
- [x] Memory System Components table includes `.cursor/commands/crux-forget.md` with `Yes` distributed flag (line 281)

AGENTS.md:
- [x] Memory manager purpose column includes "Forget": `Memory lifecycle management (dream, REM sleep, MindReader, Forget)` (line 27)
- [x] AGENTS.md is a source file — no generated frontmatter, no `sourceChecksum`, no "Generated file" banner

**Definition of Done — independently confirmed:**
- [x] All three files updated with correct references
- [x] No linter errors (verified via ReadLints)
- [x] No existing content accidentally removed (all sections intact)
