# Subtask: Update Command & Agent Specs for Default Plugins

## Metadata
- **Subtask ID**: 07
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 06
- **Created**: 20260404

## Objective

Update the `/crux-compress` command spec and the `crux-cursor-rule-manager` agent spec to support the new default-plugin loading mechanism and to delegate ratio enforcement/metrics to the `compression-level` plugin when active.

## Deliverables Checklist
- [ ] `.cursor/commands/crux-compress.md` updated:
  - Plugin Resolution section covers default-enabled plugins
  - When no `--plugin` flags: load `enabledByDefault: true` plugins from registry
  - When `--plugin` flags present: load only those (explicit overrides defaults)
  - Optional `--no-plugin <name>` to disable a specific default
  - Plugin context object includes `compressionLevel` for `compression-level` plugin
- [ ] `.cursor/agents/crux-cursor-rule-manager.md` updated:
  - When `compression-level` plugin is active: delegate ratio checking and metrics to plugin
  - When no plugin active: agent performs ratio checking and metrics itself (backward compat)
  - Clear delineation of what the agent does vs what the plugin does
- [ ] Both specs maintain full backward compatibility — existing commands work identically
- [ ] CRUX compressed versions updated if `.crux.md`/`.crux.mdc` files exist for these sources

## Definition of Done
- [ ] Command spec clearly documents default plugin loading
- [ ] Agent spec clearly documents plugin delegation
- [ ] A user running `/crux-compress @file.md --40` gets identical results as before
- [ ] A user running `/crux-compress @file.md` (no flags) gets identical results as before
- [ ] CRUX files for modified sources are regenerated
- [ ] No linter errors in modified files

## Implementation Notes

### Command Spec Changes (`crux-compress.md`)

**Plugin Resolution section** (currently lines ~140-162) needs an addition before step 3:

```
### Default Plugin Loading

Before source-type routing, resolve enabled plugins:

1. Parse all `--plugin` and `--no-plugin` flags.
2. If NO `--plugin` flags are present:
   a. Read `.crux/plugins/registry.json`
   b. Load all plugins with `enabledByDefault: true`
   c. Remove any plugins named in `--no-plugin` flags
3. If `--plugin` flags ARE present:
   a. Load only explicitly named plugins
   b. Ignore `enabledByDefault` settings
   c. `--no-plugin` has no effect (explicit list is authoritative)
4. Continue with existing validation (check registry, validate hooks, etc.)
```

### Agent Spec Changes (`crux-cursor-rule-manager.md`)

Add a section on plugin awareness:

```
### Plugin-Aware Behavior

When the `compression-level` plugin is active (indicated by orchestrator context):
- Do NOT perform ratio checking or generate token metrics yourself
- Compress toward the target `compressionLevel` as usual
- The plugin will handle: token counting, ratio validation, and frontmatter injection
  for `cruxLevel`, `beforeTokens`, `afterTokens`, `reducedBy`

When NO `compression-level` plugin is active:
- Perform all ratio checking and metrics generation as currently specified
- This ensures backward compatibility if the plugin is disabled
```

### CRUX File Updates
Check if these source files have corresponding `.crux.md`/`.crux.mdc`:
- `.cursor/commands/crux-compress.md` → likely `.cursor/commands/crux-compress.crux.md`?
- `.cursor/agents/crux-cursor-rule-manager.md` → check for `.crux.md`/`.crux.mdc`

If CRUX files exist, they must be regenerated after source edits (per foundational rule 4).

### Files to Read Before Editing
- `.cursor/commands/crux-compress.md` — full file
- `.cursor/agents/crux-cursor-rule-manager.md` — full file
- Subtask 01 output — design decisions for default-enabled mechanism
- Subtask 06 output — plugin behavior spec

### Backward Compatibility Verification
The key invariant: without any new flags, the compression output (file content and frontmatter) must be identical. The `compression-level` plugin produces the same metrics the agent previously produced itself. Verify by tracing the data flow:
1. Level resolved: same (CLI → frontmatter → default)
2. Compression: same (agent compresses to target)
3. Metrics: same values, now produced by plugin instead of agent
4. Output frontmatter: same fields and values

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Read modified specs for internal consistency
- Verify CRUX files are regenerated if they exist
- Defer full backward-compat testing to subtask 08

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
