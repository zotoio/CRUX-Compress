# Subtask: Rename Command File

## Metadata
- **Subtask ID**: 01
- **Feature**: crux-recall
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260425

## Objective
Rename the `.cursor/commands/crux-mindreader.md` command file to `.cursor/commands/crux-recall.md` and update all internal references within the file.

## Deliverables Checklist
- [x] `.cursor/commands/crux-mindreader.md` renamed to `.cursor/commands/crux-recall.md`
- [x] All internal references to `mindreader`/`MindReader` updated to `recall`/`Recall`
- [x] Command slug updated from `/crux-mindreader` to `/crux-recall`
- [x] File header/title updated

## Definition of Done
- [x] Old file `.cursor/commands/crux-mindreader.md` no longer exists
- [x] New file `.cursor/commands/crux-recall.md` exists with correct content
- [x] No remaining `mindreader` references within the new file
- [x] No linter errors in modified files

## Implementation Notes
- Use `git mv` to rename the file to preserve history
- Grep for case-insensitive `mindreader` and `MindReader` within the file
- The command slug in the frontmatter or title line should become `/crux-recall`
- Preserve all other command behavior — only naming changes

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify file exists at new path
- Verify old file no longer exists
- Grep the new file for any remaining `mindreader` references

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-04-25T21:45+10:00
- Completed: 2026-04-25T21:46+10:00

### Work Log
1. Read source file `.cursor/commands/crux-mindreader.md`
2. Used `git mv` to rename to `.cursor/commands/crux-recall.md` (preserves git history)
3. Updated file title from `# crux-mindreader` to `# crux-recall`
4. Updated all 4 usage examples from `/crux-mindreader` to `/crux-recall`
5. Updated "MindReader mode" to "Recall mode" and "MindReader is **read-only**" to "Recall is **read-only**"
6. Updated "MindReader results" to "Recall results"
7. Verified zero remaining case-insensitive `mindreader` references via grep
8. Verified old file no longer exists and new file exists

### Blockers Encountered
None.

### Files Modified
- `.cursor/commands/crux-mindreader.md` → `.cursor/commands/crux-recall.md` (renamed + content updated)

### Adversarial Verification (zoto-spec-judge)
- **Verified by**: zoto-spec-judge (independent)
- **Timestamp**: 2026-04-25T21:57+10:00
- **Verdict**: **Verified**
- Old file `.cursor/commands/crux-mindreader.md` confirmed absent (glob returned 0 results)
- New file `.cursor/commands/crux-recall.md` confirmed present with 84 lines of valid content
- Case-insensitive grep for `mindreader|mind.reader|MindReader` returned zero matches in new file
- Command slug `/crux-recall` confirmed on lines 10–13 of the new file
- File header confirmed as `# crux-recall` (line 1)
- No linter errors detected
