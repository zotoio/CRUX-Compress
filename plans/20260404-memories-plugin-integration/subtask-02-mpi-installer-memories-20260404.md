# Subtask: Installer — Add Optional Memory Components

## Metadata
- **Subtask ID**: 02
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: None
- **Created**: 20260404

## Objective

Update `install.py` to optionally set up memory system components when a user wants to enable the memories feature. The core distribution remains lightweight; memory enablement is a discoverable post-install action.

## Deliverables Checklist
- [ ] `install.py` updated with a `--with-memories` flag (or equivalent mechanism)
- [ ] When `--with-memories` is used:
  - Creates `.crux/crux-memories.json` with `enableMemories: false` (user must explicitly enable)
  - Creates `memories/` directory structure per spec
  - Prints setup instructions for enabling memories (flip flag, optional MCP config)
- [ ] Completion report updated to mention memories availability
- [ ] Without `--with-memories`: behavior is identical to current (zero breaking changes)

## Definition of Done
- [ ] `install.py` syntax-checks cleanly (`python3 -c "import ast; ast.parse(open('install.py').read())"`)
- [ ] Existing install flow (without `--with-memories`) produces identical output
- [ ] `--with-memories` creates the expected files/directories
- [ ] No memory files added to `RELEASE_FILES` or distribution zip
- [ ] No linter errors in modified files

## Implementation Notes

### Current Installer Behavior
- `install.py` (649 lines) handles: CLI parsing, version check, download, backup, preview, install, hooks merge, AGENTS block upsert
- `RELEASE_FILES` list defines what's in the distribution zip
- Completion report shows next steps
- No mention of memories anywhere in installer

### What to Add
1. **Argument**: `--with-memories` in argparse
2. **Post-install step** (after main install completes):
   - Write `.crux/crux-memories.json` with the schema from `docs/crux-memories.md` but `enableMemories: "false"`, `enableMemoryCompression: "false"`
   - Create `memories/` and `memories/agents/` directories
   - Create `.crux/reference-tracking/` directory
   - Print: "Memory system scaffolding created. To enable: set enableMemories to 'true' in .crux/crux-memories.json"
3. **Completion report**: Add a "Memories" section noting availability and how to enable
4. **Do NOT** add memory skills, commands, agent, or MCP server to the installer — those are dev-time components

### Files to Read Before Editing
- `install.py` — full file to understand structure
- `.crux/crux-memories.json` — reference config schema
- `docs/crux-memories.md` — spec for config structure (if needed)

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Run `python3 -c "import ast; ast.parse(open('install.py').read())"` to syntax-check
- Verify `--with-memories` is accepted by argparse without error
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
