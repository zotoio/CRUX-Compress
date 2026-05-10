# Subtask: Documentation Updates

## Metadata
- **Subtask ID**: 14
- **Feature**: CRUX Memories
- **Assigned Subagent**: docs-sync-agent
- **Dependencies**: 11, 13
- **Created**: 20260403

## Objective

Update all project documentation to reflect the new CRUX Memories system. This includes README.md, CONTRIBUTORS.md, and ensuring AGENTS.md is accurate after the agent addition in subtask 08.

## Deliverables Checklist

### README.md
- [ ] Add "Memories" section describing the memory system feature
- [ ] Add installation/setup instructions for the memory system:
  - Enabling memories in `.crux/crux-memories.json`
  - Running `/crux-dream` and `/crux-mindreader`
  - Optional MCP server setup
- [ ] Add Python dependency installation instructions (per-directory `requirements.txt` in `crux_mcp_server/` and `evals/`)
- [ ] Update feature list to include memories
- [ ] Add MCP server usage instructions

### CONTRIBUTORS.md
- [ ] Add memory system components to the project structure table
- [ ] Document the eval/test structure (`evals/` directory, `pytest`, integration with `scripts/test.sh`)
- [ ] Document the MCP server (`crux_mcp_server/` directory)
- [ ] Update CI/CD flow documentation if workflows changed
- [ ] Add Python development setup instructions

### AGENTS.md
- [ ] Verify `crux-cursor-memory-manager` row is correctly added (done in subtask 08, verify here)
- [ ] Verify all agent references are accurate

### Web Documentation (if applicable)
- [ ] Update `web/compress.md/` feature highlights if memory system should be featured on the landing page

## Definition of Done
- [ ] README.md accurately describes memory system setup and usage
- [ ] CONTRIBUTORS.md reflects new project structure
- [ ] AGENTS.md is accurate and up to date
- [ ] No broken links in documentation
- [ ] Documentation is clear enough for a new contributor to understand and use the memory system

## Implementation Notes

Follow the docs-sync rule (`.cursor/rules/docs-sync.md`):
- Surgical updates, not full rewrites
- Maintain consistent formatting
- Update versions, paths, and examples
- Add tables/lists for new workflows

The docs-sync-agent should read the actual implemented files to understand what was built, not just the plan files. Key files to reference:
- `.crux/crux-memories.json` — for config examples
- `.cursor/agents/crux-cursor-memory-manager.md` — for agent description
- `.cursor/commands/crux-dream.md` and `crux-mindreader.md` — for command usage
- `crux_mcp_server/README.md` — for MCP server details
- `evals/` — for test structure

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Review documentation for accuracy against implemented code
- Check for broken links
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
