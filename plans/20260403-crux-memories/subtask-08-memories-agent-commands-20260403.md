# Subtask: Agent Definition + Commands

## Metadata
- **Subtask ID**: 08
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 05, 06, 07
- **Created**: 20260403

## Objective

Create the `crux-cursor-memory-manager` agent definition and the `/crux-dream` and `/crux-mindreader` slash commands. Update `AGENTS.md` to register the new agent.

## Deliverables Checklist

### Agent Definition
- [ ] `.cursor/agents/crux-cursor-memory-manager.md` with:
  - Frontmatter: `name: crux-cursor-memory-manager`, `model: claude-4.5-opus-high-thinking`, `repository`, `description`
  - Instructions to read `.crux/crux-memories.json` config on startup
  - Orchestration of all 6 memory skills:
    - `crux-skill-memory-extract` — for dream extraction
    - `crux-skill-memory-crud` — for all memory file operations
    - `crux-skill-memory-rebalance` — for REM sleep
    - `crux-skill-memory-compress` — for compression
    - `crux-skill-memory-reference-tracker` — for reference tracking
    - `crux-skill-memory-index` — for index rebuilds
  - Dream workflow steps (1-8 from spec)
  - REM sleep workflow steps (1-8 from spec)
  - MindReader operations (decompress, rationale, query modes)
  - Agent scoping rules (only write agent memories during dream, only when artifacts identify the agent)
  - `scopeRanking` and `typePriority` awareness

### Commands
- [ ] `.cursor/commands/crux-dream.md` — slash command that:
  - Spawns `crux-cursor-memory-manager` subagent
  - Passes arguments (plan name, `--rem`, `--rem --yolo`)
  - Describes the dream workflow for the agent
- [ ] `.cursor/commands/crux-mindreader.md` — slash command that:
  - Spawns `crux-cursor-memory-manager` subagent
  - Supports invocation modes: no args, query, plan name(s), memory file(s)
  - Describes the MindReader workflow for the agent

### Registration
- [ ] Update `AGENTS.md` to add `crux-cursor-memory-manager` to the Available Agents table

## Definition of Done
- [ ] Agent definition follows the pattern of existing agents (e.g., `crux-planner.md`)
- [ ] Agent references all 6 skills by correct path
- [ ] Commands follow the pattern of existing commands (e.g., `crux-plan.md`)
- [ ] `AGENTS.md` updated with new agent row
- [ ] No linter errors in modified files

## Implementation Notes

Reference `docs/crux-memories.md`:
- Section 1 "Agent: crux-cursor-memory-manager" for agent definition details
- "Dream Workflow" for dream steps
- "REM Sleep Workflow" for REM steps
- Section 4 "Viewing" for MindReader operation modes

Study existing agents for conventions:
- `.cursor/agents/crux-planner.md` — similar orchestration pattern
- `.cursor/agents/crux-cursor-rule-manager.md` — for compression-related patterns

The agent should be comprehensive but not repeat the full spec. It should reference skills for detailed operations and focus on orchestration logic, decision points, and user interaction patterns.

Command files should follow the pattern of `.cursor/commands/crux-plan.md` — read it first to understand the format.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify agent file has valid frontmatter
- Verify commands reference correct agent
- Verify AGENTS.md update is syntactically correct
- Defer full test suite execution to the final verification phase

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
