# Subtask: CI/CD — Fix Workflow References

## Metadata
- **Subtask ID**: 03
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: None
- **Created**: 20260404

## Objective

Fix `.github/workflows/test.yml` to align with the actual repository state. The workflow currently references files and patterns that don't exist, causing broken or misleading CI steps.

## Deliverables Checklist
- [ ] `test.yml`: Replace `bash -n install.sh` and `bash install.sh --help` with `python3 -c "import ast; ast.parse(open('install.py').read())"` and `python3 install.py --help`
- [ ] `test.yml`: Remove or conditionalize `bats tests/*.bats` step (no `.bats` files exist)
- [ ] `test.yml`: Conditionalize `pytest plugins/zoto-spec-system/tests/` step (only run if directory exists)
- [ ] `version-bump.yml`: Update `RELEASE_PATHS` to reference `install.py` instead of `install.sh` (if applicable)
- [ ] Verify `pytest evals/` step covers memory eval tests correctly

## Definition of Done
- [ ] `test.yml` references only files that exist in the repository
- [ ] No CI steps will fail due to missing files
- [ ] Memory eval tests (`evals/test_a_*.py` through `evals/test_m_*.py`) are covered by `pytest evals/`
- [ ] No YAML syntax errors in workflow files
- [ ] No linter errors in modified files

## Implementation Notes

### Current Issues in `test.yml`
1. **`bash -n install.sh`** — `install.sh` does not exist; the installer is `install.py`
2. **`bash install.sh --help`** — same; should be `python3 install.py --help`
3. **`bats tests/*.bats`** — no `.bats` files exist in `tests/`; this step will error
4. **`pytest plugins/zoto-spec-system/tests/`** — `plugins/` directory may not exist on all branches

### Fixes
1. Replace bash syntax check with Python AST parse
2. Replace bash help with Python help
3. Either remove bats step entirely or gate it: `if ls tests/*.bats 1>/dev/null 2>&1; then bats tests/*.bats; fi`
4. Gate plugin tests: `if [ -d "plugins/zoto-spec-system/tests" ]; then pytest plugins/zoto-spec-system/tests/ -v; fi`

### Files to Read Before Editing
- `.github/workflows/test.yml` — full workflow
- `.github/workflows/version-bump.yml` — check RELEASE_PATHS for install.sh

### What NOT to Change
- Do not modify the `pytest evals/` step — it already covers memory tests
- Do not modify `release.yml` or `deploy-pages.yml` unless they reference `install.sh`

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
