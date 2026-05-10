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
- [x] Verify `crux-post-dream.py` header comment correctly documents its programmatic invocation model (invoked by `/crux-dream` workflow, NOT a Cursor event hook); update only if documentation is missing or inaccurate
- [x] Verify `.cursor/hooks.json` correctly lists only event-driven hooks (do NOT add `crux-post-dream.py`)
- [x] Verify the integration rule (`.cursor/rules/crux-memories-integration.md`) MCP configuration example is accurate and matches the actual `crux_mcp_server/` package
- [x] Update `plans/20260403-crux-memories/plan-crux-memories-20260403.md` — check the DoD items and tick those that are genuinely complete

## Definition of Done
- [x] `crux-post-dream.py` has clear documentation about its invocation model
- [x] `hooks.json` is unchanged (no new entries)
- [x] MCP example in integration rule matches actual server command/args
- [x] Previous memories plan DoD has accurate completion state
- [x] No linter errors in modified files

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

### Agent Session Info
- Agent: generalPurpose
- Started: 2026-04-04
- Completed: 2026-04-04

### Work Log
1. Read all relevant files: `crux-post-dream.py`, `hooks.json`, `crux-memories-integration.md`, `crux_mcp_server/__main__.py`, `crux_mcp_server/server.py`, and the previous plan file
2. **D1**: Updated `crux-post-dream.py` docstring to explicitly state it is NOT a Cursor event hook and NOT registered in `hooks.json` — invoked programmatically by `/crux-dream`
3. **D2**: Verified `hooks.json` lists only `crux-session-start.py` (sessionStart) and `crux-detect-changes.py` (afterFileEdit) — no changes needed
4. **D3**: Verified MCP config example in integration rule matches actual server entry point (`python -m crux_mcp_server -t stdio --config .crux/crux-memories.json`) — no changes needed
5. **D4**: Assessed all 12 DoD items in the previous memories plan against repository state; all verified complete. Ticked all checkboxes, set status to "Complete", and added execution notes summary
6. Verified no linter errors in modified files

### Blockers Encountered
None

### Files Modified
- `.cursor/hooks/crux-post-dream.py` — updated docstring to clarify invocation model
- `plans/20260403-crux-memories/plan-crux-memories-20260403.md` — ticked all DoD items, updated status to Complete, added execution notes

### Adversarial Verification (integrity-expert)
- **Verifier**: integrity-expert subagent
- **Date**: 2026-04-04
- **Verdict**: **VERIFIED** — all 4 deliverables and 5 DoD items independently confirmed

#### D1: `crux-post-dream.py` header
Docstring at lines 2-10 explicitly states: "INVOCATION MODEL: This script is called programmatically by the /crux-dream workflow [...] It is NOT a Cursor event hook and is NOT registered in .cursor/hooks.json." Clear and accurate.

#### D2: `hooks.json` unchanged
Contains exactly 2 event hooks: `crux-session-start.py` (sessionStart), `crux-detect-changes.py` (afterFileEdit). No `crux-post-dream.py` present. Correct.

#### D3: MCP config example
Integration rule shows `python -m crux_mcp_server -t stdio --config .crux/crux-memories.json`. Cross-referenced against `crux_mcp_server/__main__.py` argparse: module name, `-t`/`--transport` (stdio/http), `--config` path — all match exactly.

#### D4: Previous plan DoD
All 12 DoD items in `plan-crux-memories-20260403.md` independently spot-checked:
- 14 subtasks "Done" in manifest — confirmed
- 6 memory SKILL.md files exist — confirmed (glob: 6 matches)
- Agent `crux-cursor-memory-manager.md` exists — confirmed
- Commands `crux-dream.md`, `crux-mindreader.md` exist — confirmed
- `memories/` directory with subdirs (archived, goal, redflag) — confirmed
- `.crux/crux-memories.json` valid JSON, correct schema — confirmed
- 18 eval test files in `evals/` — confirmed
- MCP server supports HTTP+stdio (`__main__.py` argparse) — confirmed
- Status "Complete", execution notes present — confirmed

#### D5 (DoD): No linter errors
ReadLints on modified files returned zero errors.
