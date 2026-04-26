# Subtask: Full Suite Validation & Performance Profiling

## Metadata
- **Subtask ID**: 09
- **Feature**: SDK Eval Suite Expansion
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 03, 04, 05, 06, 07, 08
- **Created**: 20260426

## Objective

Run the complete SDK eval suite (all 8 test files, ~60 tests) with the parallel fork configuration, measure wall-clock times per file, verify no cross-file interference, and document the results. Fix any issues discovered during the full run.

## Deliverables Checklist
- [ ] Run `pnpm test` in `evals/sdk/` with `maxForks: 4` enabled
- [ ] Record per-file wall-clock times
- [ ] Verify all tests pass (both existing J/O/P and new B/C/Q/R/N)
- [ ] Verify no cross-file interference (parallel worktrees are fully isolated)
- [ ] Document total wall-clock time and compare against the 30-minute budget
- [ ] Fix any failing tests discovered during full run
- [ ] Record results in execution notes

## Definition of Done
- [ ] All ~60 tests pass in a single full-suite run
- [ ] Total wall-clock time is under 30 minutes
- [ ] Per-file times documented
- [ ] No flaky tests (or flaky tests identified with root cause)
- [ ] No linter errors in any test file

## Implementation Notes

### Run Commands

```bash
cd evals/sdk

# Full suite with verbose output and timing
pnpm test 2>&1 | tee test-results.log

# Individual file runs (for debugging failures)
pnpm test:recall
pnpm test:remember
pnpm test:amnesia
pnpm test:dream
pnpm test:rem
pnpm test:forget
pnpm test:meditate
pnpm test:integration
```

### Expected Timing Profile

| File | Tests | Expected Time | Notes |
|------|-------|---------------|-------|
| j-recall.test.ts | 10 | 3-5 min | Single-turn, fast |
| o-remember.test.ts | 7 | 3-5 min | Single-turn, file checks |
| p-amnesia.test.ts | 8 | 5-7 min | Multi-turn, most expensive existing |
| b-dream.test.ts | ~8 | 5-7 min | Multi-turn, spec fixtures |
| c-rem.test.ts | ~8 | 5-7 min | Single-turn but complex analysis |
| r-forget.test.ts | ~6 | 3-5 min | Single-turn, file checks |
| q-meditate.test.ts | ~6 | 8-12 min | Recursive subagents, slowest |
| n-integration.test.ts | ~4 | 5-8 min | Sequential multi-turn |

With `maxForks: 4`:
- Batch 1 (parallel): recall + remember + amnesia + forget → ~5-7 min
- Batch 2 (parallel): dream + rem + meditate + integration → ~8-12 min
- **Total projected: ~15-20 minutes** (limited by meditate file)

### Troubleshooting Guide

**Test timeouts**: Increase per-test timeout. Agent responses are non-deterministic in length.

**Flaky assertions**: If a pattern match fails intermittently, add more synonym alternatives to the OR-pattern array.

**Worktree conflicts**: If `git worktree add` fails, check for leftover worktrees from a previous failed run:
```bash
git worktree list
git worktree prune
```

**Cross-file interference**: If one test file's assertion depends on state created by another file, that's a bug — each file must be fully self-contained. Check that no test reads from `memories/` without first creating its own fixtures.

### What to Report in Execution Notes

1. Total wall-clock time
2. Per-file times (from Vitest verbose output)
3. Any tests that failed on first run (with root cause and fix applied)
4. Any tests that appear flaky (pass/fail non-deterministically)
5. Whether the 30-minute budget was met
6. Parallelization effectiveness (actual speedup vs sequential)

## Testing Strategy
- This subtask IS the full test run — execute everything
- If failures are found, fix them and re-run
- Run at least once with full suite to confirm parallel execution works

## Execution Notes
[To be filled by executing agent]

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
[Agent adds notes here during execution]

### Test Results
[Paste Vitest output summary here]

### Per-File Timing
| File | Time | Tests | Pass | Fail |
|------|------|-------|------|------|
| j-recall.test.ts | | | | |
| o-remember.test.ts | | | | |
| p-amnesia.test.ts | | | | |
| b-dream.test.ts | | | | |
| c-rem.test.ts | | | | |
| r-forget.test.ts | | | | |
| q-meditate.test.ts | | | | |
| n-integration.test.ts | | | | |

### Blockers Encountered
[Any blockers or issues]

### Files Modified
[List of files changed]
