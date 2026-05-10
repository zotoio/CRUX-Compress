# Subtask: Create /crux-remember Command File

## Metadata
- **Subtask ID**: 01
- **Feature**: crux-remember
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260425

## Objective
Create the `.cursor/commands/crux-remember.md` command definition file that enables users to store ad-hoc memories outside of spec workflows. The command supports interactive type selection via `AskQuestion`, an optional `--type` flag, and delegates to existing memory skills for creation and indexing.

## Deliverables Checklist
- [x] `.cursor/commands/crux-remember.md` created
- [x] Usage section documents all invocation variants: no args, quoted text, `--type` flag
- [x] Instructions section describes full workflow: config check → input parsing → type selection → metadata gathering → skill delegation → index rebuild → confirmation
- [x] Type selection uses `AskQuestion` with options from `typeTransitions` keys (`idea`, `learning`, `redflag`, `core`, `goal`)
- [x] `--type` flag documented to skip interactive type selection
- [x] Memory creation sets `source: "adhoc"` to distinguish from spec-extracted memories
- [x] Delegates to `crux-skill-memory-crud` for creation and `crux-skill-memory-index` for index rebuild
- [x] Related section links to memory manager agent, skills, and sibling commands

## Definition of Done
- [x] File exists at `.cursor/commands/crux-remember.md`
- [x] Command follows the established pattern of existing memory commands (`crux-dream.md`, `crux-forget.md`, `crux-recall.md`)
- [x] All invocation variants are documented with examples
- [x] No linter errors

## Implementation Notes
- The command file is a markdown instruction document (not executable code) — it tells the agent what to do when `/crux-remember` is invoked
- Type options are sourced from `typeTransitions` keys in `.crux/crux-memories.json`, keeping the command config-driven
- `AskQuestion` is used for type selection to provide a structured UI rather than free-text input
- The `--type` flag provides a programmatic escape hatch for users who know what type they want
- Memory `strength` defaults to 1 for newly created memories
- The `source: "adhoc"` tag is critical — it distinguishes remember-created memories from dream-extracted ones, which matters during REM sleep consolidation

## Testing Strategy
- Verify file exists at the expected path
- Verify file follows the structure of sibling command files
- Verify all documented invocation variants are internally consistent
- Check for references to correct skill names and config keys

## Execution Notes

### Work Performed
1. Created `.cursor/commands/crux-remember.md` following the established command file pattern
2. Documented three invocation variants: bare `/crux-remember`, with quoted text, and with `--type` flag
3. Wrote seven-step workflow covering config check, input parsing, type selection, metadata gathering, skill delegation, index rebuild, and user confirmation
4. Added Related section linking to the memory manager agent, CRUD skill, index skill, and all sibling commands (`/crux-dream`, `/crux-recall`, `/crux-forget`, `/crux-meditate`)

### Files Created
- `.cursor/commands/crux-remember.md`

### Blockers Encountered
None.
