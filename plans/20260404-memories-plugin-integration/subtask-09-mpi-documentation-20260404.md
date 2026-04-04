# Subtask: Documentation — Update README, CONTRIBUTORS, AGENTS

## Metadata
- **Subtask ID**: 09
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: docs-sync-agent
- **Dependencies**: 08
- **Created**: 20260404

## Objective

Update project documentation to reflect both workstreams: memory integration improvements and the new default-enabled plugin mechanism with the `compression-level` reference plugin.

## Deliverables Checklist
- [ ] `README.md` updated:
  - Plugin section: document `enabledByDefault` mechanism, `--no-plugin` flag
  - Plugin section: add `compression-level` as a documented default plugin
  - Install section: mention `--with-memories` flag for optional memory setup
  - Testing section: note new test files (`test_plugin_registry.py`)
  - File Locations Summary: add `.crux/plugins/compression-level.md` if created
- [ ] `CONTRIBUTORS.md` updated:
  - Add "Plugin System" section covering: registry structure, hook lifecycle, `enabledByDefault`, how to add a new plugin
  - Test suite table: add new test files
  - Update any stale references (install.sh → install.py if not already done)
- [ ] `AGENTS.md` updated if any agent table entries changed (unlikely but verify)
- [ ] CRUX compressed versions regenerated for any modified source rules

## Definition of Done
- [ ] README accurately reflects current plugin behavior and memory integration
- [ ] CONTRIBUTORS has plugin contributor guidance
- [ ] No stale references to `install.sh` in documentation
- [ ] All documentation changes are surgical (update specific sections, don't rewrite)
- [ ] CRUX files regenerated for modified source rules
- [ ] No linter errors in modified files

## Implementation Notes

### README Changes

**Plugin Parameter System section** (currently covers `--plugin`, registry, hooks):
- Add: "Default plugins load automatically when no `--plugin` flags are specified"
- Add: `compression-level` to the registry example
- Add: `--no-plugin <name>` flag to the flags table
- Add: explanation that explicit `--plugin` overrides defaults

**Quick Install section**:
- Add `--with-memories` to the options table
- Brief note: "Optionally scaffold memory system components"

**Testing section**:
- Add `test_plugin_registry.py` to the test files table

### CONTRIBUTORS Changes

**New section: "Plugin System"**:
- Where plugins are defined (`.crux/plugins/registry.json`)
- Hook lifecycle (`beforeFetch` → `beforeCompress` → base compression → `afterCompress` → `afterValidate`)
- `enabledByDefault` mechanism
- How to add a new plugin (add to registry, implement behavior in agent/command spec)
- Reference: `compression-level` as the canonical example

### Files to Read Before Editing
- `README.md` — current plugin and install sections
- `CONTRIBUTORS.md` — current structure and sections
- `AGENTS.md` — agent table

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Verify documentation changes are accurate against actual code/config state
- Defer to subtask 10 for final integrity check

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
