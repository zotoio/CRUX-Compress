# Subtask: Cursor Platform Wiring

## Metadata
- **Subtask ID**: 10
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 08
- **Created**: 20260403

## Objective

Create the Cursor-specific platform wiring: an agent rule that teaches all agents about the memory system, session-start hook modifications, and a post-dream hook.

## Deliverables Checklist

### Agent Rule
- [ ] `.cursor/rules/crux-memories-integration.md` — source rule file containing:
  - When `enableMemories` flag is `"true"` in `.crux/crux-memories.json`:
    - Agents MUST discover memories by reading `.crux/memory-index.yml`
    - Agents load full memory files only for likely matches (by title/description/tags)
    - If MCP is configured, agents may use semantic search instead
    - Agents annotate output with `[memory:{title}]` when influenced by a memory
    - Agents increment reference tracking (delegated to CRUX skill)
    - After plan execution completes, suggest running `/crux-dream`
  - When `enableMemories` is `"false"`, agents skip all memory operations silently
  - Agents never directly read/write memory files — they use CRUX memory skills
  - Agents only see base memories and their own agent-scoped memories
  - Each repo owns its own memories; agents never touch memories from other repos
- [ ] `.cursor/rules/crux-memories-integration.crux.mdc` — CRUX-compressed version generated directly from the `.md` source (delegate to `crux-cursor-rule-manager`; no intermediate `.crux.md` file needed)

### Session-Start Hook
- [ ] Modify `.cursor/hooks/crux-session-start.sh` to add a clause that:
  1. Reads `cruxMemories.hooks.sessionStartNudge` from `.crux/crux-memories.json`
  2. Checks if `enableMemories` is `"true"`
  3. Counts directories in `watchDir` (the plan working directory)
  4. If count > threshold, adds the nudge message to `additional_context`

### Post-Dream Hook
- [ ] Add post-dream action to `.cursor/hooks.json` or integrate into existing hook infrastructure:
  - Trigger: after dream completes
  - Actions: rebuild memory index (invoke `crux-skill-memory-index` Python script), notify MCP server if configured (touch `.crux/memory-index.yml` timestamp is sufficient — watcher picks it up)

### MCP Configuration (optional wiring)
- [ ] Document how to add MCP server to `.cursor/mcp.json`:
  ```json
  {
    "mcpServers": {
      "crux-memories": {
        "command": "python",
        "args": ["-m", "crux_mcp_server", "-t", "stdio", "--config", ".crux/crux-memories.json"]
      }
    }
  }
  ```

## Definition of Done
- [ ] Agent rule clearly communicates memory behavior to all agents
- [ ] Session-start hook correctly checks config and counts directories
- [ ] Post-dream actions are wired (index rebuild + MCP notify)
- [ ] CRUX-compressed rule generated from source
- [ ] No linter errors in modified files
- [ ] ShellCheck passes on modified shell scripts

## Implementation Notes

Reference `docs/crux-memories.md`:
- Section 3a "Cursor Wiring" for all Cursor-specific wiring points
- "Agent Rule Content" section for shared rule content across platforms

Study existing patterns:
- `.cursor/rules/docs-sync.md` and `.cursor/rules/docs-sync.crux.mdc` for the `.md` → `.crux.mdc` pair (the `crux-cursor-rule-manager` generates the `.crux.mdc` directly from the source `.md`)
- `.cursor/hooks/crux-session-start.sh` for existing session-start logic
- `.cursor/hooks.json` for hook registration format

The session-start hook modification should be additive — don't break existing pending-compression check logic. Add the memory nudge as a separate conditional block.

For the CRUX-compressed rule, delegate to `crux-cursor-rule-manager` subagent after the source `.md` is written.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify shell script syntax with `bash -n`
- Verify rule file has correct frontmatter format
- Defer ShellCheck and full test suite execution to the final verification phase

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
