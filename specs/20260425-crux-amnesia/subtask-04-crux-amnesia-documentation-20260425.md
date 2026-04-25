# Subtask: Documentation

## Metadata
- **Subtask ID**: 04
- **Feature**: crux-amnesia
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 01, 02
- **Created**: 20260425

## Objective
Ensure all documentation surfaces — README, detailed docs, web landing page, eval checklists, and sibling command cross-references — accurately describe the `/crux-amnesia` command, its session-scoped behavior, and its relationship to other memory commands.

## Deliverables Checklist
- [x] `README.md` includes `/crux-amnesia` in the commands table with description
- [x] `README.md` session override prose explains amnesia's precedence over `enableMemories`
- [x] `docs/crux-memories.md` includes amnesia in the contract table
- [x] `docs/crux-memories.md` includes amnesia in platform mapping sections
- [x] `web/compress.md/memories.html` includes amnesia in the command reference
- [x] `evals/USER_EVAL_CHECKLISTS.md` includes amnesia-related eval scenarios
- [x] Sibling commands (dream, recall, forget, remember, meditate) cross-reference amnesia in their Related sections
- [x] All documentation consistently describes amnesia as session-scoped and non-persistent
- [x] All five explicit memory commands listed as amnesia exceptions in relevant docs

## Definition of Done
- [x] `/crux-amnesia` appears in all five documentation files
- [x] Descriptions are consistent across all surfaces
- [x] Session-scoped behavior is clearly stated everywhere amnesia is mentioned
- [x] Cross-references between amnesia and sibling commands are bidirectional
- [x] No stale or contradictory amnesia documentation exists

## Implementation Notes
- Documentation updates are surgical — only sections relevant to amnesia are modified, not full rewrites
- The README commands table should have a row for amnesia showing the four invocation modes
- The `docs/crux-memories.md` contract table includes amnesia as a command with "Session override" behavior type, distinguishing it from the agent-delegated commands
- The eval checklists do not yet have a dedicated amnesia scenario section (no "A. Amnesia" section) but amnesia is referenced in cross-platform scenarios where the session override must be tested alongside other commands
- Sibling command Related sections should list amnesia with the description pattern: `/crux-amnesia` — Toggle session-scoped memory suppression

### Documentation Surfaces

| Surface | What to include |
|---------|----------------|
| `README.md` | Commands table row, session override paragraph in Memory System section |
| `docs/crux-memories.md` | Contract table entry, Cursor/Claude Code/generic platform wiring |
| `web/compress.md/memories.html` | Command reference card or list entry |
| `evals/USER_EVAL_CHECKLISTS.md` | Referenced in cross-platform flow (N1) and Quick Reference appendix |
| `.cursor/commands/crux-*.md` | Related section in dream, recall, forget, remember, meditate |

## Testing Strategy
- Grep each documentation file for `crux-amnesia` and verify at least one hit
- Verify README commands table includes amnesia row
- Verify eval checklist appendix includes amnesia in the commands quick reference
- Verify each sibling command's Related section includes amnesia
- Check for consistency: the description "Toggle session-scoped ambient memory usage" (or close variant) appears across all surfaces

## Execution Notes

### Reverse-Engineered From
- `README.md` (current state as of 20260425)
- `docs/crux-memories.md` (current state as of 20260425)
- `web/compress.md/memories.html` (current state as of 20260425)
- `evals/USER_EVAL_CHECKLISTS.md` (current state as of 20260425)
- `.cursor/commands/crux-dream.md`, `crux-recall.md`, `crux-forget.md`, `crux-remember.md`, `crux-meditate.md` (Related sections)

### Key Implementation Details
1. README includes amnesia in a dedicated commands table and mentions session override behavior in the Memory System description
2. `docs/crux-memories.md` is the most comprehensive documentation surface at ~1159 lines; amnesia appears in the contract table and platform-specific wiring sections
3. `web/compress.md/memories.html` is the public-facing landing page with a command reference section
4. Eval checklists reference amnesia in the Quick Reference appendix (commands table) and implicitly in cross-platform scenario N1
5. All five sibling commands now include amnesia in their Related sections with the word "intentionally" contrasting their behavior with amnesia's ambient suppression

### Cross-Reference Pattern
Each sibling command's Related section follows this pattern:
```markdown
## Related

- `/crux-amnesia` — Toggle session-scoped memory suppression
- `/crux-dream` — Extract or rebalance memories intentionally
- `/crux-recall` — Inspect memories intentionally
...
```

The amnesia command itself lists siblings with the same "intentionally" phrasing but from the opposite perspective.

### Files Covered
- `README.md`
- `docs/crux-memories.md`
- `web/compress.md/memories.html`
- `evals/USER_EVAL_CHECKLISTS.md`
- `.cursor/commands/crux-dream.md` (Related section)
- `.cursor/commands/crux-recall.md` (Related section)
- `.cursor/commands/crux-forget.md` (Related section)
- `.cursor/commands/crux-remember.md` (Related section)
- `.cursor/commands/crux-meditate.md` (Related section)
