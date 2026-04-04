# Subtask: Tests — Plugin & Memory Integration Tests

## Metadata
- **Subtask ID**: 08
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 02, 03, 04, 05, 07
- **Created**: 20260404

## Objective

Add and update test coverage for both workstreams: (1) memory integration points in the installer and CI, and (2) the compression-level plugin and crux-utils configurable target. Run the full test suite to verify no regressions.

## Deliverables Checklist
- [ ] New or updated eval tests for `crux-utils.py` `--target` parameter:
  - Default target (25%) behavior
  - Explicit `--target 40` behavior
  - Invalid target values rejected
- [ ] New or updated eval test for plugin registry schema:
  - `enabledByDefault` field presence and type
  - `compression-level` plugin entry validity
  - Existing plugins unchanged
- [ ] Updated `evals/test_install.py` (if installer changes from subtask 02 need test coverage):
  - `--with-memories` flag parsing
  - Memory scaffolding file creation
- [ ] Verify existing memory eval tests still pass (`evals/test_a_*.py` through `evals/test_m_*.py`)
- [ ] Full test suite run: `python3 scripts/test.py`

## Definition of Done
- [ ] All new tests pass
- [ ] All existing tests pass (no regressions)
- [ ] `python3 scripts/test.py` exits cleanly
- [ ] Test files have no linter errors
- [ ] No flaky or environment-dependent tests

## Implementation Notes

### Test Files to Create or Update

1. **`evals/test_crux_utils.py`** — add tests for `--ratio --target`:
   - Test default target is 25% (not 20%)
   - Test explicit `--target 40` changes the target line
   - Test `--target 0` or `--target 101` is rejected
   - Test `--ratio` without `--target` works as before

2. **`evals/test_plugin_registry.py`** (new file) — plugin registry validation:
   - Registry is valid JSON
   - All plugins have required fields (`description`, `hooks`, `failClosed`)
   - `enabledByDefault` field is boolean when present
   - `compression-level` plugin has `enabledByDefault: true`
   - Existing plugins have `enabledByDefault: false`

3. **`evals/test_install.py`** — extend for `--with-memories`:
   - Test `--with-memories` is a valid argument
   - Test memory scaffolding creates expected directories
   - Test without `--with-memories` doesn't create memory files

### Full Test Suite
After all tests are written, run:
```bash
python3 scripts/test.py
```
This runs both bats (if any exist) and `pytest evals/ -v`.

### Files to Read Before Editing
- `evals/test_crux_utils.py` — existing crux-utils tests
- `evals/test_install.py` — existing installer tests
- `evals/conftest.py` — shared fixtures
- `evals/requirements.txt` — test dependencies

## Testing Strategy
This IS the testing subtask. Run the full test suite here:
- `python3 scripts/test.py` (orchestrates bats + pytest)
- Fix any failures introduced by earlier subtasks
- Report results in execution notes

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
