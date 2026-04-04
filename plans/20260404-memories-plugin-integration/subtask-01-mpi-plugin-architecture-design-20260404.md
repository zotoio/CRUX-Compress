# Subtask: Plugin Architecture Design — Default-Enabled Mechanism

## Metadata
- **Subtask ID**: 01
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: None
- **Created**: 20260404

## Objective

Design and document the `enabledByDefault` extension to the existing CRUX plugin architecture. This design becomes the foundation for subtask 06 (implementing the `compression-level` reference plugin) and subtask 07 (updating command/agent specs).

## Deliverables Checklist
- [ ] Design document (in this subtask's Execution Notes) covering:
  - Registry schema extension (`enabledByDefault` field)
  - Default plugin loading behavior when no `--plugin` flags are present
  - Interaction between explicit `--plugin` flags and defaults
  - Optional `--no-plugin <name>` mechanism for disabling defaults
  - Plugin context object extensions for compression-level data
- [ ] Updated `.crux/plugins/registry.json` with `enabledByDefault` field on existing plugins (all set to `false` for backward compat) and the new `compression-level` entry (set to `true`)
- [ ] `compression-level` plugin hook specification: what `beforeCompress` and `afterCompress` do

## Definition of Done
- [ ] Registry schema extension is documented and consistent
- [ ] Existing 3 plugins have `enabledByDefault: false` (no behavior change)
- [ ] `compression-level` plugin entry specifies hooks and `enabledByDefault: true`
- [ ] No changes to any agent/command spec files (those happen in subtask 07)
- [ ] No linter errors in modified files

## Implementation Notes

### Current State
- `.crux/plugins/registry.json` has 3 plugins: `frontmatter-tagger`, `quality-gate`, `release-notes`
- Each has `description`, `hooks[]`, `failClosed`
- No `enabledByDefault` field exists
- Plugins are only loaded when `--plugin <name>` is explicitly passed

### Design Constraints
- Zero breaking changes: existing `--plugin` usage must work identically
- When no `--plugin` flags: load `enabledByDefault: true` plugins silently
- When `--plugin` flags present: load ONLY those (explicit overrides defaults)
- `--no-plugin <name>`: disable a specific default (optional, design only)

### What the `compression-level` Plugin Does

**Hook: `beforeCompress`**
- Receive `compressionLevel` from orchestrator context
- Validate range (1-100), reject invalid
- Resolve `crux: true` → 25 (text/code/URL) or 80 (images) if not already resolved
- Set `targetRatio = compressionLevel / 100` in plugin context

**Hook: `afterCompress`**
- Run `crux-utils --token-count` on source and output (or use LLM estimate)
- Calculate `ratio = afterTokens / beforeTokens * 100`
- Calculate `reducedBy = 100 - ratio`
- Check `ratio <= compressionLevel`
- Inject/update frontmatter: `cruxLevel`, `beforeTokens`, `afterTokens`, `reducedBy`
- Report pass/fail for quality gate (advisory; `failClosed: false`)

### Registry Schema After This Subtask

```json
{
  "plugins": {
    "compression-level": {
      "description": "Enforce compression ratio targets and generate token metrics.",
      "hooks": ["beforeCompress", "afterCompress"],
      "failClosed": false,
      "enabledByDefault": true
    },
    "frontmatter-tagger": {
      "description": "Add standardized metadata after compression.",
      "hooks": ["afterCompress"],
      "failClosed": false,
      "enabledByDefault": false
    },
    "quality-gate": {
      "description": "Apply additional policy checks after validation.",
      "hooks": ["afterValidate"],
      "failClosed": false,
      "enabledByDefault": false
    },
    "release-notes": {
      "description": "Collect per-file reduction metrics for release summaries.",
      "hooks": ["afterCompress", "afterValidate"],
      "failClosed": false,
      "enabledByDefault": false
    }
  }
}
```

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Validate registry.json is well-formed JSON after edit
- Verify all existing plugins retain their original fields
- Defer full test suite execution to subtask 08

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
