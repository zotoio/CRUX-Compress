# Subtask: Eval Infrastructure + Categories A-E

## Metadata
- **Subtask ID**: 11
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 09, 10
- **Created**: 20260403

## Objective

Create the Python eval test infrastructure (fixtures, conftest, directory structure, `requirements.txt`) and implement automated tests for categories A-E: Memory CRUD, Dream Workflow, REM Sleep, Reference Tracking, and Memory Index. Also update `scripts/test.sh` to include `pytest evals/`.

## Deliverables Checklist

### Directory Structure & Infrastructure
- [ ] `evals/` at repo root:
  ```
  evals/
  ├── requirements.txt                   # Python >=3.10 dependencies (pytest, pyyaml)
  ├── conftest.py                        # Shared fixtures (temp dirs, config, memory files)
  └── fixtures/                          # Test fixture data
      ├── sample-config.json             # Valid crux-memories config
      ├── sample-memories/               # Pre-built memory files for testing
      │   ├── core/
      │   ├── redflag/
      │   ├── learning/
      │   ├── idea/
      │   └── agents/code-reviewer/
      └── sample-trackers/               # Pre-built .refs.yml files
  ```
- [ ] `conftest.py` with reusable fixtures:
  - Temporary directory setup/teardown
  - Sample config generation
  - Sample memory file generation
  - Sample tracker file generation
- [ ] `requirements.txt` with `python_requires >= 3.10` comment, `pytest`, `pyyaml`
- [ ] Each test independently runnable with `pytest evals/test_X.py`
- [ ] Tests use temporary directories — never modify the actual repo

### Test Orchestration
- [ ] Update `scripts/test.sh` to run `pytest evals/` after existing BATS tests (guard with `command -v pytest` check so it skips gracefully if pytest not installed)

### Dev Eval Tests (pytest)

- [ ] **A. Memory CRUD** (`test_a_memory_crud.py`):
  - Create memory via frontmatter, verify schema (all required fields, valid type, strength=1)
  - Update memory, verify `modified` changes but `created` does not
  - Verify `.memory.md` and `.memory.crux.md` naming enforced
  - Verify memories placed in correct type subdirectory
  - Verify agent-scoped memories placed in `agents/{id}/{type}/`

- [ ] **B. Dream Workflow** (`test_b_dream_workflow.py`):
  - Given completed plan with execution artifacts, verify N candidate facts extracted
  - Verify dream summary written to correct subdirectory under `workDir`
  - Verify plan archival moves to `archiveDir` correctly

- [ ] **C. REM Sleep** (`test_c_rem_sleep.py`):
  - Seed memories with known strength/reference data, verify promote/demote/archive recommendations match thresholds
  - Create orphaned tracker files, verify cleanup recommended
  - Create two contradicting memories, verify conflict detection
  - Verify REM summary written to `archiveDir`

- [ ] **D. Reference Tracking** (`test_d_reference_tracking.py`):
  - Reference a memory, verify `.refs.yml` created in `trackingDir`
  - Reference same memory from two plans, verify both entries with correct counts
  - Verify `maxReferencesStored` cap enforced
  - Verify indicator format when `indicateInOutput` is true/false

- [ ] **E. Memory Index** (`test_e_memory_index.py`):
  - Create memories across type directories, run index script, verify YAML output
  - Verify prioritisation matches `typePriority`, then strength desc, then references desc
  - Verify agent-scoped memories included with correct paths
  - Delete a memory, rebuild, verify removal

## Definition of Done
- [ ] All A-E test files created with test functions covering spec requirements
- [ ] `conftest.py` provides reusable fixtures
- [ ] Tests pass: `pytest evals/test_a*.py evals/test_b*.py evals/test_c*.py evals/test_d*.py evals/test_e*.py`
- [ ] `scripts/test.sh` updated to include pytest
- [ ] No Python linter errors

## Implementation Notes

Reference `docs/crux-memories.md` Section 8 "Evaluations" for the complete list of eval requirements per category.

Key testing principles:
- Each test should be independently runnable with a clean fixture directory
- Tests should never modify the actual repo — use `tmp_path` fixtures
- Tests verify file system state (file existence, content, frontmatter, directory placement)

The index script tests should invoke `.cursor/skills/crux-skill-memory-index/scripts/memory-index.py` as a subprocess against fixture directories.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Run only the A-E test files for this subtask's tests
- Defer full test suite execution to the final verification phase

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
