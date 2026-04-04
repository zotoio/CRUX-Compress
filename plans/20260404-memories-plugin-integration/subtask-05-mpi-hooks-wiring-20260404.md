# Subtask: Hooks & Wiring — Clarify Invocation Model and Close Plan DoD

## Metadata
- **Subtask ID**: 05
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: None
- **Created**: 20260404

## Objective

Clarify the hook invocation model for memory-related hooks, ensure MCP documentation is accurate, and close out the Definition of Done from the previous memories plan (`plans/20260403-crux-memories/`).

## Deliverables Checklist
- [ ] Verify `crux-post-dream.py` header comment correctly documents its programmatic invocation model (invoked by `/crux-dream` workflow, NOT a Cursor event hook); update only if documentation is missing or inaccurate
- [ ] Verify `.cursor/hooks.json` correctly lists only event-driven hooks (do NOT add `crux-post-dream.py`)
- [ ] Verify the integration rule (`.cursor/rules/crux-memories-integration.md`) MCP configuration example is accurate and matches the actual `crux_mcp_server/` package
- [ ] Update `plans/20260403-crux-memories/plan-crux-memories-20260403.md` — check the DoD items and tick those that are genuinely complete

## Definition of Done
- [ ] `crux-post-dream.py` has clear documentation about its invocation model
- [ ] `hooks.json` is unchanged (no new entries)
- [ ] MCP example in integration rule matches actual server command/args
- [ ] Previous memories plan DoD has accurate completion state
- [ ] No linter errors in modified files

## Implementation Notes

### Hook Invocation Model
There are two types of "hooks" in this project:
1. **Cursor event hooks** — registered in `.cursor/hooks.json`, triggered by IDE events (`sessionStart`, `afterFileEdit`)
2. **Workflow-invoked scripts** — called programmatically by agent workflows (e.g., the dream command calls `crux-post-dream.py` after extraction)

`crux-post-dream.py` is type 2. Its docstring should make this explicit to avoid confusion.

### MCP Documentation Check
The integration rule (`.cursor/rules/crux-memories-integration.md`) contains an example `.cursor/mcp.json` snippet. Verify:
- The `command` matches (`python` or `python3`)
- The `args` match the actual entry point (`-m crux_mcp_server` or similar)
- The `--config` path is correct (`.crux/crux-memories.json`)

### Previous Plan DoD
The memories plan at `plans/20260403-crux-memories/plan-crux-memories-20260403.md` has:
- All 14 subtasks marked "Done" in the manifest
- DoD checkboxes still unchecked
- Execution Notes still placeholder

Review each DoD item against actual repository state and tick those that are genuinely met. Add execution notes summarizing the plan's completion.

### Files to Read Before Editing
- `.cursor/hooks/crux-post-dream.py` — read header/docstring
- `.cursor/hooks.json` — verify current entries
- `.cursor/rules/crux-memories-integration.md` — MCP example
- `crux_mcp_server/__main__.py` or `crux_mcp_server/server.py` — actual entry point
- `plans/20260403-crux-memories/plan-crux-memories-20260403.md` — DoD section

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify `hooks.json` is valid JSON after any edits
- Defer integration testing to subtask 08

## Execution Notes
[To be filled by executing agent]

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
[Agent adds notes here during execution]

### Blockers Encountered
[Any blockers or issues]

### Files Modified
[List of files changed]
