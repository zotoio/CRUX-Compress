# Subtask: Update Install and Distribution Files

## Metadata
- **Subtask ID**: 05
- **Feature**: crux-remember
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 01
- **Created**: 20260425

## Objective
Update the installer and distribution scripts to include the `/crux-remember` command file, ensuring it is distributed with CRUX installations and recognized by the install/upgrade process.

## Deliverables Checklist
- [x] `install.py` — `MEMORY_FILE_PREFIXES` updated to include `crux-remember`
- [x] `install.py` — Default commands list updated with `remember` entry
- [x] `install.py` — Fallback list updated to include `crux-remember.md`
- [x] `install.crux.md` — Regenerated from updated `install.py` source
- [x] `scripts/create-crux-zip.py` — `DIST_FILES` updated to include `.cursor/commands/crux-remember.md`

## Definition of Done
- [x] `install.py` references `crux-remember` in all relevant locations (prefixes, defaults, fallback)
- [x] `install.crux.md` regenerated with updated sourceChecksum
- [x] `scripts/create-crux-zip.py` includes the new command file in the distribution manifest
- [x] No linter errors in modified files

## Implementation Notes
- `MEMORY_FILE_PREFIXES` is used by the installer to identify memory-related command files during installation and upgrades
- The default commands list in `install.py` maps to `DEFAULT_MEMORIES_CONFIG` which populates `.crux/crux-memories.json` on fresh installs
- The fallback list ensures the file is installed even when the config doesn't explicitly list it
- `install.crux.md` is a generated CRUX file — never edit directly; update `install.py` then regenerate via `crux-cursor-rule-manager`
- Per zip-contents-protection rule, `scripts/create-crux-zip.py` was updated with explicit user permission

## Testing Strategy
- Verify `crux-remember` appears in `MEMORY_FILE_PREFIXES` in `install.py`
- Verify `remember` entry exists in the default commands configuration
- Verify `crux-remember.md` is in the fallback list
- Verify `install.crux.md` was regenerated (check sourceChecksum)
- Verify `.cursor/commands/crux-remember.md` appears in `DIST_FILES` in `scripts/create-crux-zip.py`

## Execution Notes

### Work Performed
1. Updated `install.py`:
   - Added `"crux-remember"` to `MEMORY_FILE_PREFIXES` list
   - Added `remember` entry to `DEFAULT_MEMORIES_CONFIG` commands with file path, default command, and description
   - Added `"crux-remember.md"` to the fallback command file list
2. Regenerated `install.crux.md` via `crux-cursor-rule-manager` with updated sourceChecksum
3. Updated `scripts/create-crux-zip.py` — added `.cursor/commands/crux-remember.md` to `DIST_FILES`

### Files Modified
- `install.py`
- `install.crux.md`
- `scripts/create-crux-zip.py`

### Blockers Encountered
None.
