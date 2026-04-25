# Subtask: Add --total Flag to /crux-recall

## Metadata
- **Subtask ID**: 05
- **Feature**: crux-recall
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 01, 02
- **Created**: 20260425

## Objective
Add the `--total` parameter definition to the `/crux-recall` command file and the agent's Recall Mode section. This defines the interface — implementation is in subtask 06.

## Deliverables Checklist
- [x] `.cursor/commands/crux-recall.md`: Add `--total` parameter with description explaining it generates an interactive 3D force-directed visualization of the entire memory system using `/canvas` and `3d-force-graph`
- [x] `.cursor/agents/crux-cursor-memory-manager.md`: Update Recall Mode section to document `--total` behavior — gathering memory data, building graph, generating a visualization using `/canvas` and `3d-force-graph`
- [x] `.crux/crux-memories.json`: Update `commands.recall.description` to reflect the `--total` capability (e.g., "Decompress, view, and visualize memories")

## Definition of Done
- [x] `--total` parameter is documented in the command file
- [x] Agent definition describes the `--total` workflow (data gathering → graph construction → use `/canvas` to visualize)
- [x] No linter errors in modified files

## Implementation Notes
- The command file (`.cursor/commands/crux-recall.md`) should have a usage line and parameter section where `--total` is added
- The agent definition should describe the workflow:
  1. Read `.crux/memory-index.yml` for memory metadata
  2. Read all memory files from `memories/{type}/` directories
  3. Decompress CRUX-compressed memories (`.memory.crux.md`) for display
  4. Build graph edges from shared tags and source specs
  5. Use `/canvas` to generate a 3D force-directed visualization with `3d-force-graph` (https://github.com/vasturiano/3d-force-graph), with all data embedded
- Node visualization spec:
  - Size ∝ strength, color by memory type, label = title
- Edge spec:
  - Connect memories sharing tags or source specs
  - Thickness ∝ connection strength
- Interactions: click → detail panel, hover → highlight, search/filter, force simulation controls

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify the command file has the `--total` parameter
- Verify the agent definition describes the workflow
- Grep for consistency between command and agent description

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-04-25
- Completed: 2026-04-25

### Work Log
1. Read all three target files to understand current state
2. Added `--total` usage line and Parameters table to `.cursor/commands/crux-recall.md`
3. Added `--total` to Argument Handling and What Happens sections in command file
4. Added `--total` invocation variant and full "Total Visualization Workflow" to Recall Mode in `.cursor/agents/crux-cursor-memory-manager.md`
5. Updated `commands.recall.description` in `.crux/crux-memories.json`
6. Verified no linter errors in modified files

### Adversarial Verification (zoto-spec-judge)
- **Verdict: VERIFIED**
- Verifier: zoto-spec-judge (independent, fresh context)
- Verified: 2026-04-25

**Deliverables Checklist verification:**
- `.cursor/commands/crux-recall.md`: `--total` parameter present with usage line (line 14), detailed Parameters table entry (line 21), argument handling (line 33), and what-happens entry (line 43) — confirmed
- `.cursor/agents/crux-cursor-memory-manager.md`: `--total` invocation row in Recall Mode table (line 106) and full "Total Visualization Workflow" section (lines 110–123) covering data gathering, node/edge construction, canvas generation, and interaction specs — confirmed
- `.crux/crux-memories.json`: `commands.recall.description` updated to "Decompress, view, and visualize memories" (line 39) — confirmed

**Definition of Done verification:**
- `--total` parameter documented in command file — confirmed (5 occurrences across usage, parameters, argument handling, what-happens, and notes)
- Agent definition describes `--total` workflow (data gathering → graph construction → canvas visualization) — confirmed with 6-step workflow
- No linter errors in modified files — confirmed via ReadLints

### Blockers Encountered
None

### Files Modified
- `.cursor/commands/crux-recall.md` — Added `--total` parameter, usage line, Parameters table, argument handling, and what-happens entry
- `.cursor/agents/crux-cursor-memory-manager.md` — Added `--total` invocation variant and Total Visualization Workflow section
- `.crux/crux-memories.json` — Updated recall command description
