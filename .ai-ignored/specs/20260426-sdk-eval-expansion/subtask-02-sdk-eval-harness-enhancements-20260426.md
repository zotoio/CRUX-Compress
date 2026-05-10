# Subtask: Harness Enhancements — New Fixture & Assertion Helpers

## Metadata
- **Subtask ID**: 02
- **Feature**: SDK Eval Suite Expansion
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260426

## Objective

Add new fixture creators and assertion utilities to `evals/sdk/helpers/harness.ts` (and re-export from `helpers/index.ts` if it exists) to support Dream, REM Sleep, Forget, Meditate, and Integration test files.

## Deliverables Checklist

### New Fixture Helpers
- [x] `createSpecFixture(workspaceRoot, specSlug, opts?)` — creates a mock completed spec directory:
  - `specs/<specSlug>/spec-<feature>-<date>.md` with overview and subtask manifest
  - `specs/<specSlug>/_execution-state.yml` with `status: complete`, `startedAt`, `completedAt`, subtask statuses
  - 2 subtask files (`subtask-01-*.md`, `subtask-02-*.md`) with execution notes, work logs, and files-modified sections
  - Optional `opts.alreadyDreamed: boolean` — if true, also creates a `dream-<slug>-<date>.md` summary file (to test B1 filtering)
  - Returns the spec directory path
- [x] `seedAgedMemory(fixture, workspaceRoot, daysAgo)` — like `createMemoryFixture` but:
  - Sets `created` and `modified` to `daysAgo` days in the past
  - Returns the file path
- [x] `createConflictingMemories(workspaceRoot, opts)` — creates two memories with contradictory content:
  - `opts.topic: string` — the topic they disagree on
  - `opts.memory1: { slug, type, title, body }` — first position
  - `opts.memory2: { slug, type, title, body }` — opposing position
  - Both memories get `strength: 3` and overlapping tags
  - Returns `[path1, path2]`
- [x] `createTrackerFixture(workspaceRoot, memorySlug, opts?)` — creates a `.refs.yml` file in `.crux/reference-tracking/`:
  - `opts.referenceCount?: number` (default 1)
  - `opts.lastReferenced?: string` (ISO date string, default today)
  - Returns the tracker file path
- [x] `createOrphanedTracker(workspaceRoot, slug)` — creates a `.refs.yml` tracker file with NO matching memory file. Returns the tracker path.

### New Assertion Helpers
- [x] `assertMemoryExists(workspaceRoot, type, slugPattern)` — asserts at least one memory file in `memories/<type>/` matches the slug pattern (string or regex). Returns the file content.
- [x] `assertMemoryDeleted(workspaceRoot, type, slugPattern)` — asserts NO memory file in `memories/<type>/` matches the slug pattern.
- [x] `assertTrackerDeleted(workspaceRoot, slug)` — asserts the tracker file `<slug>.refs.yml` does not exist in `.crux/reference-tracking/`.
- [x] `countMemoryFiles(workspaceRoot, type?)` — counts `.memory.md` and `.memory.crux.md` files, optionally filtered by type subdirectory.
- [x] `listTrackerFiles(workspaceRoot)` — lists all `.refs.yml` files in `.crux/reference-tracking/`.

### Rate-Limit Retry Helpers (already implemented)
- [x] `withRetry(fn, label?, maxRetries?)` — retry any async operation with exponential backoff on rate-limit errors (base 2s, max 60s, 5 retries, jitter)
- [x] `sendWithRetry(agent, message)` — wraps `agent.send()` with automatic rate-limit retry

### Updated Exports
- [x] All new helpers exported from `helpers/harness.ts`
- [x] If `helpers/index.ts` exists, re-export new helpers from there (auto-exported via `export * from "./harness.js"`)

## Definition of Done
- [x] All helpers implemented with JSDoc comments
- [x] TypeScript compiles without errors (pre-existing Agent type errors in test files are unrelated)
- [x] No linter errors in modified files
- [x] Helpers do not import any test framework — they are pure utility functions

## Implementation Notes

### Existing Patterns to Follow
Study the existing `createMemoryFixture()` and `createIsolatedWorkspace()` in `helpers/harness.ts` for style conventions:
- Functions accept `workspaceRoot: string` as the target directory
- Functions return the path(s) of created files
- Memory frontmatter uses the standard YAML format with `---` delimiters
- File operations use `node:fs` and `node:path`

### Spec Fixture Format
The `_execution-state.yml` file should follow this structure:
```yaml
status: complete
startedAt: "2026-04-20T10:00:00Z"
completedAt: "2026-04-21T14:30:00Z"
subtasks:
  - id: "01"
    status: complete
    agent: crux-software-engineer
  - id: "02"
    status: complete
    agent: crux-software-engineer
```

### Realistic Spec Fixture Content
The Dream command's agent parses subtask execution notes to extract candidate facts. Mock content must be realistic enough for the LLM to extract meaningful learnings, redflags, or ideas. Use content like this for subtask execution notes:

```markdown
### Work Log
- Implemented retry logic with exponential backoff for the API client
- Discovered that the existing error handling silently swallowed connection timeouts
- Refactored the connection pool to use a singleton pattern to avoid resource leaks
- Added circuit breaker pattern after observing cascading failures in staging

### Blockers Encountered
- Connection pool exhaustion under load — resolved by adding max-connection limits
- Silent timeout failures were masking real errors — added explicit timeout logging

### Files Modified
- src/api/client.ts (retry logic, circuit breaker)
- src/api/connection-pool.ts (singleton, max connections)
- tests/api/client.test.ts (new retry tests)
```

This content naturally produces extractable facts like:
- **Learning**: "Exponential backoff is essential for API retry logic"
- **Redflag**: "Silent error swallowing masks real failures — always log timeouts explicitly"
- **Idea**: "Circuit breaker pattern prevents cascading failures"

### Tracker Fixture Format
The `.refs.yml` file should follow this structure:
```yaml
memory: "<slug>"
reference_count: 1
last_referenced: "2026-04-26"
references:
  - agent: "test-agent"
    date: "2026-04-26"
    context: "SDK eval fixture"
```

### Aged Memory Date Calculation
```typescript
const date = new Date();
date.setDate(date.getDate() - daysAgo);
return date.toISOString().split("T")[0]; // "2026-01-26" for 90 days ago
```

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify TypeScript compilation with `pnpm exec tsc --noEmit` in `evals/sdk/`
- Manually test one fixture helper by adding a temporary test or inspecting output

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-04-26T12:18:00+10:00
- Completed: 2026-04-26T12:20:00+10:00

### Work Log
- Implemented all 5 fixture helpers and 5 assertion/listing helpers in `harness.ts`
- `createSpecFixture` generates realistic spec directory with subtask execution notes containing work logs, blockers, and files-modified sections suitable for LLM Dream extraction
- `seedAgedMemory` reuses the `MemoryFixture` interface and adjusts `created`/`modified` dates
- `createConflictingMemories` delegates to existing `createMemoryFixture` with shared tags and `strength: 3`
- `createTrackerFixture` generates `.refs.yml` with configurable reference count and date
- `createOrphanedTracker` is a thin wrapper around `createTrackerFixture` (no memory file created)
- All assertion helpers produce informative error messages listing found files on failure
- Verified TypeScript compilation — no new errors introduced (pre-existing `Agent.send` type errors in test files are unrelated to this subtask)
- Verified no linter errors in `harness.ts`
- `helpers/index.ts` already uses `export * from "./harness.js"` so all new exports are automatically re-exported

### Blockers Encountered
- None

### Files Modified
- `evals/sdk/helpers/harness.ts` — added 10 new helpers (5 fixture creators, 5 assertion/listing utilities)
- `specs/20260426-sdk-eval-expansion/subtask-02-sdk-eval-harness-enhancements-20260426.md` — ticked checklist items, filled execution notes

---

## Adversarial Verification

### Verifier
- Agent: zoto-spec-judge
- Verified: 2026-04-26T12:22:00+10:00

### Deliverables — Fixture Helpers
| # | Helper | Sig ✓ | JSDoc ✓ | Behaviour ✓ | Notes |
|---|--------|-------|---------|-------------|-------|
| 1 | `createSpecFixture` | ✅ | ✅ | ✅ | Creates overview, `_execution-state.yml`, 2 subtasks, optional dream summary. Returns spec dir path. |
| 2 | `seedAgedMemory` | ✅ | ✅ | ✅ | Backdates `created`/`modified` via `daysAgo` arithmetic. Returns file path. |
| 3 | `createConflictingMemories` | ✅ | ✅ | ✅ | Delegates to `createMemoryFixture` twice with shared tags and `strength: 3`. Returns `[path1, path2]`. |
| 4 | `createTrackerFixture` | ✅ | ✅ | ✅ | Creates `.refs.yml` with configurable `referenceCount` and `lastReferenced`. Returns tracker path. |
| 5 | `createOrphanedTracker` | ✅ | ✅ | ✅ | Thin wrapper around `createTrackerFixture` — no memory file created. Returns tracker path. |

### Deliverables — Assertion/Listing Helpers
| # | Helper | Sig ✓ | JSDoc ✓ | Behaviour ✓ | Notes |
|---|--------|-------|---------|-------------|-------|
| 6 | `assertMemoryExists` | ✅ | ✅ | ✅ | Supports string (substring) and RegExp. Returns file content. Informative error on failure. |
| 7 | `assertMemoryDeleted` | ✅ | ✅ | ✅ | Returns void if dir missing (correct). Throws with match details on failure. |
| 8 | `assertTrackerDeleted` | ✅ | ✅ | ✅ | Checks exact `<slug>.refs.yml` path. Throws on existence. |
| 9 | `countMemoryFiles` | ✅ | ✅ | ✅ | Recursive walk, counts `.memory.md` + `.memory.crux.md`. Optional `type` filter. |
| 10 | `listTrackerFiles` | ✅ | ✅ | ✅ | Filters `.refs.yml` in `.crux/reference-tracking/`. Returns absolute paths. |

### Pre-existing Helpers
| # | Helper | Present ✓ |
|---|--------|-----------|
| 11 | `withRetry` / `sendWithRetry` | ✅ (lines 150–181) |

### Export Verification
- All 10 new functions use `export function` — ✅
- `helpers/index.ts` contains `export * from "./harness.js"` — auto-reexport confirmed ✅

### Definition of Done
| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | All helpers have JSDoc comments | ✅ | Every new function has a `/** ... */` block |
| 2 | TypeScript compiles without new errors | ✅ | 3 errors in `harness.ts` are pre-existing (`Agent.send` type); 0 errors in new code (lines 395–865) |
| 3 | No linter errors in modified files | ✅ | `ReadLints` returned clean |
| 4 | Helpers do not import any test framework | ✅ | Imports: `@cursor/february/agent` (type-only), `node:*`, `./config.js` — no vitest/jest/mocha |

### Verdict: **Verified**
All Deliverables Checklist items and Definition of Done items independently confirmed. No issues found.
