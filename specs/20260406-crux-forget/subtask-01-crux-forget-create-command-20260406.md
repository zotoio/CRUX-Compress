# Subtask: Create /crux-forget Command File

## Metadata
- **Subtask ID**: 01
- **Feature**: crux-forget
- **Assigned Subagent**: generalPurpose
- **Dependencies**: None
- **Created**: 20260406

## Objective
Create the command definition file `.cursor/commands/crux-forget.md` that allows users to invoke `/crux-forget` to remove one or more memories from the corpus.

## Deliverables Checklist
- [x] `.cursor/commands/crux-forget.md` created
- [x] Command follows the structural pattern of `crux-dream.md` and `crux-mindreader.md`
- [x] Repository link included in header
- [x] Usage section with all invocation modes documented
- [x] Instructions section specifying subagent spawning behaviour
- [x] Argument handling section covering all input types
- [x] "What Happens" section describing the deletion workflow
- [x] Related section linking to memory manager agent, CRUD skill, and sibling commands

## Definition of Done
- [x] File created at `.cursor/commands/crux-forget.md`
- [x] No linter errors in the file

## Implementation Notes

### File Location
`.cursor/commands/crux-forget.md`

### Reference Files (read these for pattern consistency)
- `.cursor/commands/crux-dream.md` — Structure and tone reference
- `.cursor/commands/crux-mindreader.md` — Structure and tone reference
- `.cursor/skills/crux-skill-memory-crud/SKILL.md` — The Delete operation this command delegates to

### Command Design

**Usage:**
```
/crux-forget <memory-id>                    - Forget a specific memory by its short hash ID
/crux-forget <slug>                         - Forget a memory by slug
/crux-forget <file-path>                    - Forget a memory by file path
/crux-forget "search query"                 - Search memories and select which to forget
```

**Key behaviours:**
1. The command spawns a `crux-cursor-memory-manager` subagent to handle the forget workflow
2. Pass `$ARGUMENTS` to the subagent
3. **Always confirm before deletion** — display matched memories with their ID, title, type, and strength, then ask the user to confirm which ones to remove
4. Deletion uses `crux-skill-memory-crud` Delete, which handles both the memory file and its reference tracker
5. After deletion, rebuild the memory index via `crux-skill-memory-index`
6. Report what was deleted (count, types, IDs)

**Argument handling:**
- **Memory ID(s)** (7-char hex hash, e.g. `a1b2c3d`): Resolve to memory files by scanning the index or memory directories. Show matched memory details and confirm deletion.
- **Slug(s)** (e.g. `validate-checksums-before-overwrite`): Resolve to memory file(s) by searching `memories/` recursively. Show matched memory details and confirm.
- **File path(s)** (e.g. `memories/learning/foo.memory.md`): Read the specified file(s) directly. Show details and confirm.
- **Quoted text** (e.g. `"performance optimization"`): Search memories by title, description, and tags. Present matches and let the user select which to forget.
- **No arguments**: Load the memory index, display all memories in a selectable list, let the user pick which to forget.

### Header format
Follow this pattern:
```markdown
# crux-forget

[Brief one-line description]

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)
```

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify the file was created at the correct path
- Verify the file is valid markdown
- Verify it references the correct subagent (`crux-cursor-memory-manager`)
- Verify it references `crux-skill-memory-crud` Delete operation

## Execution Notes

### Agent Session Info
- Agent: generalPurpose (subtask executor)
- Started: 2026-04-07
- Completed: 2026-04-07

### Work Log
- Read reference files: `crux-dream.md`, `crux-mindreader.md`, and `crux-skill-memory-crud/SKILL.md`
- Created `.cursor/commands/crux-forget.md` following the structural pattern of sibling commands
- Structure includes: header with repo link, usage section (5 invocation modes), instructions with subagent spawning, argument handling for all input types, "What Happens" workflow (7 steps), and related section
- Confirmed no linter errors on the created file

### Blockers Encountered
None

### Files Modified
- `.cursor/commands/crux-forget.md` — Created (new file)
- `specs/20260406-crux-forget/subtask-01-crux-forget-create-command-20260406.md` — Updated checklist and execution notes

### Adversarial Verification (zoto-spec-judge)
- **Verified by**: zoto-spec-judge (independent verifier)
- **Date**: 2026-04-07
- **Verdict**: **Verified**
- File exists at `.cursor/commands/crux-forget.md` (47 lines) — confirmed via Read tool
- Structural pattern matches `crux-dream.md` and `crux-mindreader.md` (title, description, repo link, Usage, Instructions, Argument Handling, What Happens, Related)
- All 5 invocation modes present in Usage block (memory-id, slug, file-path, search query, no-args)
- Subagent spawning correctly specifies `crux-cursor-memory-manager`
- Argument handling covers all 5 input types with `$ARGUMENTS` passthrough
- "What Happens" section has 7-step workflow including config load, resolve, display, confirm, delete, rebuild index, report
- Related section links to agent, CRUD skill, and both sibling commands (`/crux-dream`, `/crux-mindreader`)
- References `crux-skill-memory-crud` Delete operation (line 35) and `crux-skill-memory-index` (line 38)
- No linter errors confirmed via ReadLints
- **No issues found**
