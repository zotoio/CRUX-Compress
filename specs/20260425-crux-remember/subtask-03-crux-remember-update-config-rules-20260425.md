# Subtask: Update Config and Rules

## Metadata
- **Subtask ID**: 03
- **Feature**: crux-remember
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260425

## Objective
Add the `/crux-remember` command to the memory system configuration and update the amnesia integration rule to recognize it as a memory-management command that should be allowed even during amnesia mode.

## Deliverables Checklist
- [x] `.crux/crux-memories.json` — `commands.remember` entry added with `file`, `default`, and `description` fields
- [x] `.cursor/rules/crux-memories-integration.md` — amnesia override list updated to include `/crux-remember`
- [x] `.cursor/rules/crux-memories-integration.crux.mdc` — regenerated from updated source with new sourceChecksum

## Definition of Done
- [x] `commands.remember` entry in `.crux/crux-memories.json` matches the pattern of existing command entries
- [x] Amnesia rule source file lists `/crux-remember` alongside `/crux-dream`, `/crux-recall`, `/crux-meditate`, and `/crux-forget`
- [x] CRUX-compressed rule file is regenerated (not manually edited)
- [x] No linter errors

## Implementation Notes
- The `commands.remember` config entry follows the exact schema of sibling commands: `file` (path to command definition), `default` (slash command), `description` (human-readable purpose)
- The amnesia override is critical for UX: users should be able to `/crux-remember` even when ambient memory loading is suppressed, because it represents explicit intent to interact with the memory system
- The CRUX rule regeneration must be done via `crux-cursor-rule-manager` — never edit `.crux.mdc` files directly
- The config entry positions `remember` between `recall` and `meditate` in the commands object for logical ordering

## Testing Strategy
- Verify `commands.remember` exists in `.crux/crux-memories.json` with correct field values
- Verify `/crux-remember` appears in the amnesia override list in `.cursor/rules/crux-memories-integration.md`
- Verify `.crux.mdc` file was regenerated (check for updated sourceChecksum)

## Execution Notes

### Work Performed
1. Added `commands.remember` entry to `.crux/crux-memories.json`:
   - `file`: `.cursor/commands/crux-remember.md`
   - `default`: `/crux-remember`
   - `description`: `"Create ad-hoc memories outside of spec workflows"`
2. Updated `.cursor/rules/crux-memories-integration.md` — added `/crux-remember` to the amnesia override list of memory-management commands (line 18)
3. Regenerated `.cursor/rules/crux-memories-integration.crux.mdc` via `crux-cursor-rule-manager` with updated sourceChecksum

### Files Modified
- `.crux/crux-memories.json`
- `.cursor/rules/crux-memories-integration.md`
- `.cursor/rules/crux-memories-integration.crux.mdc`

### Blockers Encountered
None.
