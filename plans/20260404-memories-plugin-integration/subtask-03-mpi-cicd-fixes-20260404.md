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
- [x] Review diff in `test.yml` (removes `install.sh` validation steps and summary line) — **VERIFIER**: confirmed no `install.sh`, `bash -n install.sh`, or `bash install.sh --help` steps remain; summary references only pytest and zip validation
- [x] Review diff in `release.yml` (changes `install.sh` → `install.py` in install commands) — **VERIFIER**: confirmed lines 168 and 272 both use `install.py | python3 -`; zero `install.sh` references
- [x] Review diff in `version-bump.yml` (removes `install.sh` from `RELEASE_PATHS`) — **VERIFIER**: confirmed `RELEASE_PATHS` (lines 32-41) contains no `install.sh`; all listed paths verified to exist on disk
- [x] Verify `pytest evals/` step covers memory eval tests correctly — **VERIFIER**: confirmed 12 memory eval files (test_a through test_m, skipping j) exist in evals/; `pytest evals/ -v --tb=short` at line 30 runs them all
- [x] Scan all workflow files for any remaining `install.sh` references and fix if found — **VERIFIER**: ripgrep across all `.yml` files and entire `.github/` directory: zero matches

## Definition of Done
- [x] All workflow diffs are reviewed and committed (commit 903f3ef) — **VERIFIER**: commit exists in log, message: "fix: update CI/CD workflows to replace install.sh with install.py"
- [x] No workflow file references `install.sh` — **VERIFIER**: ripgrep confirms zero matches across all 4 workflow files and all `.yml` files in repo
- [x] No CI steps will fail due to missing files — **VERIFIER**: all referenced files verified to exist: `evals/requirements.txt`, `scripts/create-crux-zip.py`, `.crux/crux.json`, `.crux/crux-release-files.json`, `install.py`, all RELEASE_PATHS entries, `CRUX.md`; `install.sh` confirmed absent from repo
- [x] Memory eval tests (`evals/test_a_*.py` through `evals/test_m_*.py`) are covered by `pytest evals/` — **VERIFIER**: 12 files confirmed (a,b,c,d,e,f,g,h,i,k,l,m)
- [x] No YAML syntax errors in workflow files — **VERIFIER**: `yaml.safe_load()` passes for all 4 workflow files
- [x] No linter errors in modified files — **VERIFIER**: no workflow files were modified in working tree (changes already committed)

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

### Agent Session Info
- Agent: generalPurpose (subtask-03 executor)
- Started: 2026-04-04
- Completed: 2026-04-04

### Work Log
1. Read all four workflow files (`test.yml`, `release.yml`, `version-bump.yml`, `deploy-pages.yml`)
2. Discovered that the described "uncommitted diffs" had already been committed in `903f3ef` ("fix: update CI/CD workflows to replace install.sh with install.py")
3. Verified each committed change:
   - **test.yml**: Two steps removed (`bash -n install.sh` syntax check + `bash install.sh --help` help test) and one summary line removed. Current file has no `install.sh` references.
   - **release.yml**: Two install command references changed from `install.sh | bash` → `install.py | python3 -` (in release notes and step summary). Correct.
   - **version-bump.yml**: `install.sh` removed from `RELEASE_PATHS` env list. Correct.
4. Confirmed `deploy-pages.yml` has no `install.sh` references — no changes needed.
5. Verified `pytest evals/` covers all memory eval tests: `test_a_memory_crud.py` through `test_m_config_validation.py` (12 memory-related test files).
6. Scanned all `.yml` files across the repo — zero `install.sh` references remain.
7. Validated YAML syntax for all four workflow files — all pass.

### Blockers Encountered
None. The changes described as "uncommitted" were already committed prior to this subtask's execution.

### Files Modified
- `plans/20260404-memories-plugin-integration/subtask-03-mpi-cicd-fixes-20260404.md` (this file — status updates only)

No workflow files needed modification; all changes were already correct and committed.

---

### Adversarial Verification (integrity-expert)
- **Verifier**: integrity-expert subagent
- **Date**: 2026-04-04
- **Verdict**: **VERIFIED**

#### Verification Steps Performed
1. Read all 4 workflow files (`test.yml`, `release.yml`, `version-bump.yml`, `deploy-pages.yml`) independently
2. Ran ripgrep for `install.sh` across all `.yml` files — zero matches
3. Ran ripgrep for `install.sh` across entire `.github/` directory — zero matches
4. Verified commit `903f3ef` exists in git log with expected message
5. Confirmed `install.sh` does NOT exist in the repo (`install.py` exists as replacement)
6. Validated YAML syntax for all 4 workflow files via `yaml.safe_load()` — all pass
7. Verified all files referenced in workflow steps exist on disk:
   - `evals/requirements.txt`, `scripts/create-crux-zip.py`, `.crux/crux.json`, `.crux/crux-release-files.json` — all exist
   - All 9 entries in `RELEASE_PATHS` — all exist
8. Confirmed 12 memory eval test files (`test_a` through `test_m`, skipping `j`) are present in `evals/` and covered by `pytest evals/`
9. Verified `release.yml` installation commands (lines 168, 272) correctly use `install.py | python3 -`

#### Findings
- All deliverables confirmed complete
- All Definition of Done items independently verified
- No discrepancies found between executor's report and actual state
