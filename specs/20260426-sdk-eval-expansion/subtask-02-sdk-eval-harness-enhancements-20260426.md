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
- [ ] `createSpecFixture(workspaceRoot, specSlug, opts?)` — creates a mock completed spec directory:
  - `specs/<specSlug>/spec-<feature>-<date>.md` with overview and subtask manifest
  - `specs/<specSlug>/_execution-state.yml` with `status: complete`, `startedAt`, `completedAt`, subtask statuses
  - 2 subtask files (`subtask-01-*.md`, `subtask-02-*.md`) with execution notes, work logs, and files-modified sections
  - Optional `opts.alreadyDreamed: boolean` — if true, also creates a `dream-<slug>-<date>.md` summary file (to test B1 filtering)
  - Returns the spec directory path
- [ ] `seedAgedMemory(fixture, workspaceRoot, daysAgo)` — like `createMemoryFixture` but:
  - Sets `created` and `modified` to `daysAgo` days in the past
  - Returns the file path
- [ ] `createConflictingMemories(workspaceRoot, opts)` — creates two memories with contradictory content:
  - `opts.topic: string` — the topic they disagree on
  - `opts.memory1: { slug, type, title, body }` — first position
  - `opts.memory2: { slug, type, title, body }` — opposing position
  - Both memories get `strength: 3` and overlapping tags
  - Returns `[path1, path2]`
- [ ] `createTrackerFixture(workspaceRoot, memorySlug, opts?)` — creates a `.refs.yml` file in `.crux/reference-tracking/`:
  - `opts.referenceCount?: number` (default 1)
  - `opts.lastReferenced?: string` (ISO date string, default today)
  - Returns the tracker file path
- [ ] `createOrphanedTracker(workspaceRoot, slug)` — creates a `.refs.yml` tracker file with NO matching memory file. Returns the tracker path.

### New Assertion Helpers
- [ ] `assertMemoryExists(workspaceRoot, type, slugPattern)` — asserts at least one memory file in `memories/<type>/` matches the slug pattern (string or regex). Returns the file content.
- [ ] `assertMemoryDeleted(workspaceRoot, type, slugPattern)` — asserts NO memory file in `memories/<type>/` matches the slug pattern.
- [ ] `assertTrackerDeleted(workspaceRoot, slug)` — asserts the tracker file `<slug>.refs.yml` does not exist in `.crux/reference-tracking/`.
- [ ] `countMemoryFiles(workspaceRoot, type?)` — counts `.memory.md` and `.memory.crux.md` files, optionally filtered by type subdirectory.
- [ ] `listTrackerFiles(workspaceRoot)` — lists all `.refs.yml` files in `.crux/reference-tracking/`.

### Rate-Limit Retry Helpers (already implemented)
- [x] `withRetry(fn, label?, maxRetries?)` — retry any async operation with exponential backoff on rate-limit errors (base 2s, max 60s, 5 retries, jitter)
- [x] `sendWithRetry(agent, message)` — wraps `agent.send()` with automatic rate-limit retry

### Updated Exports
- [ ] All new helpers exported from `helpers/harness.ts`
- [ ] If `helpers/index.ts` exists, re-export new helpers from there

## Definition of Done
- [ ] All helpers implemented with JSDoc comments
- [ ] TypeScript compiles without errors
- [ ] No linter errors in modified files
- [ ] Helpers do not import any test framework — they are pure utility functions

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
