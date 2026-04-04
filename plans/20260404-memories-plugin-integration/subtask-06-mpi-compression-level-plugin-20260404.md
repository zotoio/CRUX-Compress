# Subtask: Implement compression-level Reference Plugin

## Metadata
- **Subtask ID**: 06
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 01
- **Created**: 20260404

## Objective

Implement the `compression-level` plugin as the reference default-enabled plugin. This includes updating the registry (already drafted in subtask 01), making `crux-utils.py` accept a configurable target, and documenting the plugin's behavior specification.

## Deliverables Checklist
- [ ] `.crux/plugins/registry.json` finalized with the `compression-level` entry and `enabledByDefault` on all plugins (per subtask 01 design)
- [ ] `crux-utils.py` updated: `--ratio` accepts optional `--target <n>` parameter (default 25)
- [ ] `crux-utils.py` `--ratio` output shows target from `--target` instead of hardcoded 20%
- [ ] `.cursor/skills/crux-utils/SKILL.md` updated to document `--target` parameter
- [ ] Plugin behavior specification written (can be in a new file `.crux/plugins/compression-level.md` or inline in registry — decide based on subtask 01 design)

## Definition of Done
- [ ] `crux-utils.py` syntax-checks cleanly
- [ ] `crux-utils.py --ratio <source> <crux>` still works without `--target` (default 25)
- [ ] `crux-utils.py --ratio <source> <crux> --target 40` uses 40% as target
- [ ] Registry is valid JSON with all 4 plugins
- [ ] Plugin behavior spec is clear enough for the agent to execute
- [ ] No breaking changes to existing `crux-utils` usage
- [ ] No linter errors in modified files

## Implementation Notes

### crux-utils.py Changes

Current `_calculate_ratio` function (lines ~90-109):
```python
def _calculate_ratio(source_file: str, crux_file: str) -> None:
    # ...
    target_met = "YES" if ratio <= 20 else "NO"
    print(f"Target (≤20%):     {target_met}")
```

Change to accept target parameter:
```python
def _calculate_ratio(source_file: str, crux_file: str, target: int = 25) -> None:
    # ...
    target_met = "YES" if ratio <= target else "NO"
    print(f"Target (≤{target}%):   {target_met}")
```

CLI changes in `main()`:
- When `--ratio` is used, check for `--target <n>` in remaining args
- Validate target is 1-100
- Pass to `_calculate_ratio`

### Plugin Behavior Specification

The `compression-level` plugin's behavior at each hook:

**`beforeCompress`**:
- Read `compressionLevel` from orchestrator context
- Validate range 1-100
- If `crux: true` in source and no explicit level: resolve to 25 (text) or 80 (image)
- Set `targetRatio = compressionLevel / 100` in context for the compressing agent
- This hook is advisory — it enriches context, not enforces

**`afterCompress`**:
- Read source and output file paths from context
- Run `crux-utils --token-count` on both (or estimate)
- Calculate: `ratio = (afterTokens * 100) / beforeTokens`
- Calculate: `reducedBy = 100 - ratio`
- Check: `ratio <= compressionLevel`
- Inject into output frontmatter: `cruxLevel`, `beforeTokens`, `afterTokens`, `reducedBy`
- Report: PASS if target met, WARN if not (since `failClosed: false`)

### Where the Plugin Spec Lives

Option A: Inline in registry.json (add `spec` field) — compact but less readable
Option B: Separate `.crux/plugins/compression-level.md` — more room for detail
Recommendation: Option B, consistent with how agent/command specs work

### Files to Read Before Editing
- `.crux/plugins/registry.json` — current state
- `.cursor/skills/crux-utils/scripts/crux-utils.py` — full file
- `.cursor/skills/crux-utils/SKILL.md` — current documentation
- Subtask 01 output — design decisions

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Run `python3 -c "import ast; ast.parse(open('.cursor/skills/crux-utils/scripts/crux-utils.py').read())"` to syntax-check
- Run `python3 .cursor/skills/crux-utils/scripts/crux-utils.py --help` to verify CLI
- Test `--ratio` with and without `--target` on a fixture file pair (e.g., from `tests/fixtures/`)
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
