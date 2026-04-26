# Subtask: Vitest Config Parallelization & npm Scripts

## Metadata
- **Subtask ID**: 03
- **Feature**: SDK Eval Suite Expansion
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260426

## Objective

Update the Vitest configuration to support parallel test file execution via multiple forks, and add per-category npm scripts to `package.json` for targeted test runs.

## Deliverables Checklist

### Vitest Config (`evals/sdk/vitest.config.ts`)
- [ ] Change `singleFork: true` to `maxForks: 2` (conservative start; increase to 3-4 after validation if no rate limiting)
- [ ] Keep `pool: "forks"` — each fork gets its own process and worktree
- [ ] Keep default `testTimeout: 240_000` — individual tests override as needed
- [ ] Keep `hookTimeout: 120_000`
- [ ] Verify `setupFiles` and `reporters` are unchanged

### Package.json Scripts (`evals/sdk/package.json`)
- [ ] Add `"test:dream": "vitest run --grep 'Dream'"` for B category
- [ ] Add `"test:rem": "vitest run --grep 'REM'"` for C category
- [ ] Add `"test:forget": "vitest run --grep 'Forget'"` for R category
- [ ] Add `"test:meditate": "vitest run --grep 'Meditate'"` for Q category
- [ ] Add `"test:integration": "vitest run --grep 'Integration'"` for N category
- [ ] Keep existing scripts: `test`, `test:watch`, `test:recall`, `test:amnesia`, `test:remember`

## Definition of Done
- [ ] `vitest.config.ts` enables multi-fork execution
- [ ] All 8 test categories have a `test:<category>` npm script
- [ ] Existing tests still pass with the new config (verify with `pnpm test`)
- [ ] No linter errors in modified files

## Implementation Notes

### Why Multi-Fork Is Safe
Each test file creates its own isolated git worktree via `createIsolatedWorkspace()`. Worktrees are created in `/tmp/` with unique names (`sdk-eval-<timestamp>-<counter>`). There is no shared mutable state between test files, making parallel execution safe.

### Expected Performance Impact
With `maxForks: 2` and 8 test files, the Vitest scheduler will run 2 files concurrently:
- Batch 1: j-recall + o-remember → ~5 min
- Batch 2: p-amnesia + r-forget → ~5-7 min
- Batch 3: b-dream + c-rem → ~5-7 min
- Batch 4: q-meditate + n-integration → ~8-12 min
Wall-clock bottleneck is the slowest file (q-meditate at ~8-10 min). Total projected: ~25-30 minutes.

After validation, increasing to `maxForks: 3-4` can reduce this to ~15-20 minutes.

### Config Change
```typescript
poolOptions: {
  forks: {
    maxForks: 2,
  },
},
```

### API Concurrency Considerations
Each fork runs an isolated worktree AND a live SDK agent session connecting to the Cursor API. Concurrent long-running agent sessions may hit API rate limits or exhaust local memory (each agent process includes the February SDK runtime).

**Start conservatively with `maxForks: 2`** to avoid rate limiting. The harness includes exponential backoff retry on rate-limit errors (see Decision 13 in spec index), but fewer concurrent sessions reduces the likelihood of hitting limits in the first place.

During subtask 09 validation, if no rate limiting is observed:
1. Increase `maxForks` to 3, then 4
2. Document the observed rate-limit thresholds

If rate limiting persists even with `maxForks: 2`:
1. Consider splitting expensive files (meditate, integration) into a separate Vitest project that runs sequentially
2. Document the `CURSOR_API_KEY` rate limit

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Run `pnpm test` in `evals/sdk/` to verify existing tests pass with the new fork config
- Verify with `pnpm test:recall` that per-category scripts work

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
