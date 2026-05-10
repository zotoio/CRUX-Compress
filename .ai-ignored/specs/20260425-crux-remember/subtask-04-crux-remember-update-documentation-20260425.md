# Subtask: Update Documentation

## Metadata
- **Subtask ID**: 04
- **Feature**: crux-remember
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 01, 02, 03
- **Created**: 20260425

## Objective
Update all documentation files to include the `/crux-remember` command — user-facing docs, developer docs, the website, related command cross-references, agent description, and eval checklists.

## Deliverables Checklist
- [x] `README.md` — `/crux-remember` added to Memory Commands table with usage examples
- [x] `CONTRIBUTORS.md` — `.cursor/commands/crux-remember.md` added to distributed files table
- [x] `AGENTS.md` — `crux-cursor-memory-manager` description updated to mention Remember
- [x] `docs/crux-memories.md` — command table, wiring guide, and usage examples updated
- [x] `web/compress.md/memories.html` — command grid and feature descriptions updated
- [x] `.cursor/commands/crux-amnesia.md` — Related section updated to include `/crux-remember`
- [x] `.cursor/commands/crux-dream.md` — Related section updated to include `/crux-remember`
- [x] `.cursor/commands/crux-forget.md` — Related section updated to include `/crux-remember`
- [x] `.cursor/commands/crux-recall.md` — Related section updated to include `/crux-remember`
- [x] `evals/USER_EVAL_CHECKLISTS.md` — eval scenarios added for `/crux-remember` workflows

## Definition of Done
- [x] All documentation files accurately describe the `/crux-remember` command
- [x] Cross-references between related commands are consistent and bidirectional
- [x] Eval scenarios cover bare invocation, `--type` flag, adhoc source tag, and REM sleep integration
- [x] No linter errors in modified files

## Implementation Notes
- Follow the docs-sync pattern: surgical updates, not full rewrites
- `AGENTS.md` is a source file — edit directly (not via a `.source.md` intermediary)
- The memory manager description in `AGENTS.md` should mention the new Remember capability alongside Dream, REM, Recall, etc.
- Related sections in sibling command files should list `/crux-remember` with a concise description
- Eval scenarios should test the differentiation between adhoc and spec-extracted memories

## Testing Strategy
- Verify `/crux-remember` appears in all target documentation files
- Verify Related sections in sibling commands are bidirectionally consistent
- Verify eval checklist has `/crux-remember` scenarios
- Check that no documentation references the command incorrectly

## Execution Notes

### Work Performed
1. Updated `README.md` — added `/crux-remember` row to Memory Commands table with usage description and examples
2. Updated `CONTRIBUTORS.md` — added `.cursor/commands/crux-remember.md` to the distributed files listing
3. Updated `AGENTS.md` — added "Recall decompression" and Remember to `crux-cursor-memory-manager` description
4. Updated `docs/crux-memories.md` — added command entry in commands table, wiring section, and usage examples showing all three invocation variants
5. Updated `web/compress.md/memories.html` — added `/crux-remember` to the commands grid with description and icon
6. Updated Related sections in `.cursor/commands/crux-amnesia.md`, `crux-dream.md`, `crux-forget.md`, `crux-recall.md` — each now includes a `/crux-remember` entry
7. Added eval scenarios to `evals/USER_EVAL_CHECKLISTS.md` covering: bare invocation, `--type` flag, adhoc source tagging, base-scope placement, and REM sleep consolidation of adhoc memories

### Files Modified
- `README.md`
- `CONTRIBUTORS.md`
- `AGENTS.md`
- `docs/crux-memories.md`
- `web/compress.md/memories.html`
- `.cursor/commands/crux-amnesia.md`
- `.cursor/commands/crux-dream.md`
- `.cursor/commands/crux-forget.md`
- `.cursor/commands/crux-recall.md`
- `evals/USER_EVAL_CHECKLISTS.md`

### Blockers Encountered
None.
