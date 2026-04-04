# Subtask: CI/CD — Fix Workflow References

## Metadata
- **Subtask ID**: 03
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: None
- **Created**: 20260404

## Objective

Review, validate, and commit existing uncommitted workflow fixes across `test.yml`, `release.yml`, and `version-bump.yml`. Most `install.sh` removal work is already done in the working tree — this subtask ensures the changes are correct and complete, then commits them.

## Deliverables Checklist
- [ ] Review uncommitted diff in `test.yml` (removes `install.sh` validation steps and summary line) — verify correctness, commit
- [ ] Review uncommitted diff in `release.yml` (changes `install.sh` → `install.py` in install commands) — verify correctness, commit
- [ ] Review uncommitted diff in `version-bump.yml` (removes `install.sh` from `RELEASE_PATHS`) — verify correctness, commit
- [ ] Verify `pytest evals/` step covers memory eval tests correctly
- [ ] Scan all workflow files for any remaining `install.sh` references and fix if found

## Definition of Done
- [ ] All uncommitted workflow diffs are reviewed and committed
- [ ] No workflow file references `install.sh`
- [ ] No CI steps will fail due to missing files
- [ ] Memory eval tests (`evals/test_a_*.py` through `evals/test_m_*.py`) are covered by `pytest evals/`
- [ ] No YAML syntax errors in workflow files
- [ ] No linter errors in modified files

## Implementation Notes

### Working Tree State (as of plan creation)
The following uncommitted diffs already exist and need review/commit:

1. **`test.yml`**: Removes `bash -n install.sh` and `bash install.sh --help` validation steps, removes summary line referencing install script check
2. **`release.yml`**: Changes two `install.sh` references to `install.py | python3 -` in the installation command output
3. **`version-bump.yml`**: Removes `install.sh` from `RELEASE_PATHS` list

The committed `test.yml` already uses `hashFiles` to conditionalize the plugin test step — no `bats` references exist in the committed version.

### Files to Read Before Committing
- `.github/workflows/test.yml` — review full diff
- `.github/workflows/release.yml` — review full diff
- `.github/workflows/version-bump.yml` — review full diff
- `.github/workflows/deploy-pages.yml` — scan for any `install.sh` references

### What NOT to Change
- Do not modify the `pytest evals/` step — it already covers memory tests
- Do not modify `deploy-pages.yml` unless it references `install.sh`

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Validate YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))"` (if pyyaml available) or visual inspection
- Defer CI pipeline validation to subtask 08

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
