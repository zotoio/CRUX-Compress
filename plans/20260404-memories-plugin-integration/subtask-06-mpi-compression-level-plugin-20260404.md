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
- [x] `.crux/plugins/registry.json` finalized with the `compression-level` entry and `enabledByDefault` on all plugins (per subtask 01 design)
- [x] `crux-utils.py` updated: `--ratio` accepts optional `--target <n>` parameter (default 25)
- [x] `crux-utils.py` `--ratio` output shows target from `--target` instead of hardcoded 20%
- [x] `.cursor/skills/crux-utils/SKILL.md` updated to document `--target` parameter
- [x] Plugin behavior specification written (can be in a new file `.crux/plugins/compression-level.md` or inline in registry — decide based on subtask 01 design)

## Definition of Done
- [x] `crux-utils.py` syntax-checks cleanly
- [x] `crux-utils.py --ratio <source> <crux>` still works without `--target` (default 25)
- [x] `crux-utils.py --ratio <source> <crux> --target 40` uses 40% as target
- [x] Registry is valid JSON with all 4 plugins
- [x] Plugin behavior spec is clear enough for the agent to execute
- [x] No breaking changes to existing `crux-utils` usage
- [x] No linter errors in modified files

> **Adversarial verification completed 2026-04-04 — ALL items independently confirmed.**

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

### Agent Session Info
- Agent: generalPurpose (subtask executor)
- Started: 2026-04-04
- Completed: 2026-04-04

### Work Log

1. **Verified registry.json** — Confirmed subtask 01 already produced correct `compression-level` entry with `enabledByDefault: true`, `hooks: ["beforeCompress", "afterCompress"]`, `failClosed: false`. All 3 existing plugins have `enabledByDefault: false`. No changes needed.

2. **Updated `crux-utils.py`** — Added `--target <n>` parameter support:
   - `_calculate_ratio()` now accepts `target: int = 25` parameter (was hardcoded to 20)
   - CLI parsing extracts `--target` from ratio args, validates range 1-100 and integer type
   - Error handling for: missing value, non-integer, out-of-range
   - Updated docstring and `--help` output to document `--target`
   - Default changed from 20 to 25 to match CRUX spec

3. **Syntax-checked** — `python3 -c "import ast; ast.parse(...)"` passes cleanly

4. **Tested all scenarios**:
   - `--ratio` without `--target`: shows `Target (≤25%): NO` (default 25)
   - `--ratio --target 40`: shows `Target (≤40%): NO`
   - `--ratio --target 15`: shows `Target (≤15%): NO`
   - `--target 0`: error "must be 1-100"
   - `--target abc`: error "must be an integer"
   - `--target` (no value): error "requires a numeric argument"

5. **Updated SKILL.md** — Added `--target` to Quick Start, ratio mode section, and workflow steps. Updated example output from `≤20%` to `≤25%`.

6. **Wrote plugin behavior spec** — Created `.crux/plugins/compression-level.md` with full hook specifications (beforeCompress/afterCompress), context objects, failure modes, CLI integration, default targets table, and plugin interaction notes.

### Adversarial Verification (integrity-expert, 2026-04-04)

**Verdict: VERIFIED — all 12/12 items independently confirmed.**

#### Deliverables Verification

| # | Item | Result | Evidence |
|---|------|--------|----------|
| D1 | Registry finalized | PASS | Valid JSON, 4 plugins, `compression-level` has `enabledByDefault: true`, hooks `["beforeCompress","afterCompress"]`, `failClosed: false`. Other 3 plugins have `enabledByDefault: false`. |
| D2 | `--target` parameter | PASS | `_calculate_ratio(source_file, crux_file, target=25)` at line 93. CLI parsing at lines 188-201 validates integer, range 1-100, missing value. |
| D3 | Dynamic target output | PASS | Line 112: `f"Target (≤{target}%):    {target_met}"`. Tested: without `--target` shows `≤25%`, with `--target 40` shows `≤40%`. |
| D4 | SKILL.md updated | PASS | Quick Start, mode syntax, explanatory paragraph, and workflow steps all document `--target`. Example output updated from `≤20%` to `≤25%`. |
| D5 | Plugin behavior spec | PASS | `.crux/plugins/compression-level.md` (111 lines). Documents `beforeCompress` (input/output context, 5-step behavior, failure mode) and `afterCompress` (input/output context, 7-step behavior, failure mode). Includes CLI integration, default targets table, plugin interaction notes. |

#### Definition of Done Verification

| # | Item | Result | Evidence |
|---|------|--------|----------|
| DoD1 | Syntax-checks cleanly | PASS | `python3 -c "import ast; ast.parse(...)"` → `SYNTAX OK`, exit 0 |
| DoD2 | `--ratio` without `--target` | PASS | Output: `Target (≤25%): YES`, exit 0 (tested with CRUX.md → AGENTS.md) |
| DoD3 | `--ratio --target 40` | PASS | Output: `Target (≤40%): YES`, exit 0 |
| DoD4 | Registry valid JSON, 4 plugins | PASS | `python3 -m json.tool` validates; enumerated: compression-level, frontmatter-tagger, quality-gate, release-notes |
| DoD5 | Plugin spec clear | PASS | Detailed context tables, step-by-step behavior, failure modes, interaction notes — sufficient for agent execution |
| DoD6 | No breaking changes | PASS | `--token-count` (exit 0), `--cksum` (exit 0), `--ratio` (exit 0) all work unchanged. Default target changed 20→25 (intentional, more lenient, matches CRUX spec). |
| DoD7 | No linter errors | PASS | ReadLints on all 4 modified files: "No linter errors found" |

#### Error-handling edge cases independently tested

| Input | Expected | Actual | Status |
|-------|----------|--------|--------|
| `--target 0` | Error: must be 1-100 | `Error: --target must be 1-100, got 0` (exit 1) | PASS |
| `--target abc` | Error: must be integer | `Error: --target must be an integer, got 'abc'` (exit 1) | PASS |
| `--target` (no value) | Error: requires numeric arg | `Error: --target requires a numeric argument` (exit 1) | PASS |

#### Observation (non-blocking)

The default compression target changed from 20% to 25%. This is intentional per the subtask design ("to match CRUX spec") and is more lenient (no false negatives). Existing callers without `--target` will see `≤25%` instead of `≤20%` in output. This is acceptable and documented.

### Blockers Encountered
None.

### Files Modified
- `.cursor/skills/crux-utils/scripts/crux-utils.py` — added `--target` parameter, changed default from 20 to 25
- `.cursor/skills/crux-utils/SKILL.md` — documented `--target`, updated examples
- `.crux/plugins/compression-level.md` — **new file**, plugin behavior specification
