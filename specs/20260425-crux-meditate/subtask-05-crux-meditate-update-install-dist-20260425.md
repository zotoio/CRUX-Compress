# Subtask: Update Install and Distribution Files

## Metadata
- **Subtask ID**: 05
- **Feature**: crux-meditate
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 01
- **Created**: 20260425

## Objective
Update `install.py` to register the new `/crux-meditate` command in MEMORY_FILE_PREFIXES, default command lists, and fallback lists. Regenerate `install.crux.md`. Update `scripts/create-crux-zip.py` DIST_FILES to include the new command file.

## Deliverables Checklist
- [x] `install.py`: `MEMORY_FILE_PREFIXES` updated to include `crux-meditate` prefix
- [x] `install.py`: Default commands list updated to include `crux-meditate.md`
- [x] `install.py`: Fallback list updated to include `/crux-meditate` command
- [x] `install.crux.md`: Regenerated from updated `install.py` via `crux-cursor-rule-manager`
- [x] `scripts/create-crux-zip.py`: `DIST_FILES` list updated to include `.cursor/commands/crux-meditate.md`

## Definition of Done
- [x] `crux-meditate` appears in all relevant lists in `install.py`
- [x] `install.crux.md` regenerated with updated sourceChecksum
- [x] `scripts/create-crux-zip.py` includes the command in its distribution file list
- [x] No linter errors in modified files

## Implementation Notes
- `install.py` has three locations that need updating:
  1. `MEMORY_FILE_PREFIXES` — tuple of command file prefixes used for memory-related file detection
  2. Default commands list — the list of `.cursor/commands/*.md` files installed by default
  3. Fallback list — backup list used when config file is missing
- `install.crux.md` is a **generated CRUX file** — NEVER edit directly. Update `install.py` first, then regenerate via `crux-cursor-rule-manager`
- `scripts/create-crux-zip.py` `DIST_FILES` determines what goes into the distribution zip. The command file must be added to ensure it ships with the release.
- Follow the zip-contents-protection rule: this change is explicitly requested by the spec, not an auto-add

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify `crux-meditate` appears in MEMORY_FILE_PREFIXES, default commands, and fallback list in `install.py`
- Verify `install.crux.md` was regenerated (check sourceChecksum differs from previous)
- Verify `scripts/create-crux-zip.py` DIST_FILES includes the meditate command path

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Completed: 2026-04-25

### Work Log
1. Read `install.py` to identify all locations requiring updates
2. Added `"crux-meditate"` to `MEMORY_FILE_PREFIXES` tuple
3. Added `"crux-meditate.md"` to the default commands list
4. Added `/crux-meditate` to the fallback command list
5. Delegated `install.crux.md` regeneration to `crux-cursor-rule-manager`
6. Read `scripts/create-crux-zip.py` to identify DIST_FILES location
7. Added `.cursor/commands/crux-meditate.md` to DIST_FILES list
8. Verified no linter errors across modified files

### Blockers Encountered
None.

### Files Modified
- `install.py` (MEMORY_FILE_PREFIXES, default commands, fallback list)
- `install.crux.md` (regenerated)
- `scripts/create-crux-zip.py` (DIST_FILES updated)
