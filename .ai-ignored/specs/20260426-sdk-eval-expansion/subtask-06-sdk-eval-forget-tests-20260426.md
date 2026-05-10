# Subtask: Forget Tests (R1-R2)

## Metadata
- **Subtask ID**: 06
- **Feature**: SDK Eval Suite Expansion
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 01, 02
- **Created**: 20260426

## Objective

Create `evals/sdk/tests/r-forget.test.ts` covering USER_EVAL_CHECKLISTS.md scenarios R1 and R2. These test the `/crux-forget` command's ability to find, confirm, and delete memories by ID or search query.

## Deliverables Checklist
- [x] Create `evals/sdk/tests/r-forget.test.ts`
- [x] R1 tests: Forget by memory ID — confirmation, deletion, tracker cleanup, index rebuild
- [x] R2 tests: Forget by search query — search results, selective deletion
- [x] All tests use isolated worktrees with pre-seeded memories and trackers
- [ ] All tests pass

## Definition of Done
- [x] `r-forget.test.ts` has at least 6 tests across R1, R2
- [ ] All tests pass when run via `pnpm test:forget`
- [x] No linter errors
- [x] Tests do not modify the real repository

## Adversarial Verification (Judge)

**Verdict: Verified**

All deliverables independently confirmed. 6 tests (4 R1 + 2 R2), correct fixtures (5 memories, 2 trackers, index rebuild), 300s timeouts, ground-truth assertions (`assertMemoryDeleted`, `assertTrackerDeleted`, `assertMemoryExists`). Isolated worktree pattern confirmed. No new TS/lint errors (only pre-existing `TS7053` shared with all test files). Two unchecked items are runtime-dependent and correctly remain unchecked.

## Implementation Notes

### Test Structure

```
describe("R: Forget", () => {
  // Shared workspace with multiple memories and trackers
  
  describe("R1: Forget - By Memory ID", () => {
    // 3-4 tests
  })
  
  describe("R2: Forget - Search and Select", () => {
    // 2-3 tests
  })
})
```

### Fixture Setup (beforeAll)

1. Create an isolated workspace
2. Create 4-5 memory fixtures with distinct slugs, types, and tags:
   - `sdk-test-forget-perf` (type: learning, tags: [performance, optimization])
   - `sdk-test-forget-security` (type: redflag, tags: [security, auth])
   - `sdk-test-forget-cache` (type: idea, tags: [caching, performance])
   - `sdk-test-forget-testing` (type: learning, tags: [testing, quality])
   - `sdk-test-forget-keep` (type: core, tags: [architecture]) — this one should NOT be deleted
3. Create tracker fixtures for at least 2 of the memories using `createTrackerFixture()`
4. Rebuild memory index

### R1 Tests (~3-4 tests)
Timeout: 300_000 (300s) — the agent may need to recall, confirm, then delete.

**Test: "shows memory details and confirms deletion"**
- Send `/crux-forget sdk-test-forget-perf` (or the memory's slug/title)
- Assert output contains the memory's title ("performance" or related)
- Assert output contains confirmation language ("confirm", "delete", "forget", "remove")
- Note: The SDK sends a single message, so the agent will treat this as a confirmed deletion command

**Test: "deletes the memory file"**
- After the forget run, verify the memory file no longer exists
- Use `assertMemoryDeleted(ws.root, "learning", "sdk-test-forget-perf")`

**Test: "cleans up associated reference tracker"**
- After the forget run, verify the tracker file is also deleted
- Use `assertTrackerDeleted(ws.root, "sdk-test-forget-perf")`

**Test: "rebuilds index after deletion"**
- After the forget run, read the memory index
- Assert the deleted memory no longer appears in the index
- Assert other memories still appear

### R2 Tests (~2-3 tests)
Timeout: 300_000 (300s).

**Test: "searches memories by keyword and shows results"**
- Send `/crux-forget "performance"`
- Assert output contains search results mentioning "performance"-related memories
- Assert output shows at least 2 matching memories (perf and cache both have "performance" tag)

**Test: "only deletes selected memories, not all matches"**
- After a search-and-forget run, verify at least one non-performance memory still exists
- Use `assertMemoryExists(ws.root, "core", "sdk-test-forget-keep")`

**Test: "rebuilds index after search-based deletion"**
- Verify index is updated to reflect deletions

### Assertion Patterns

For deletion confirmation:
```typescript
const confirmsAction =
  result.assistantText.toLowerCase().includes("delet") ||
  result.assistantText.toLowerCase().includes("remov") ||
  result.assistantText.toLowerCase().includes("forgot") ||
  result.assistantText.toLowerCase().includes("forget");
```

For file-system ground truth:
```typescript
// Most reliable assertion — checks the actual file system
assertMemoryDeleted(ws.root, "learning", "sdk-test-forget-perf");
assertMemoryExists(ws.root, "core", "sdk-test-forget-keep");
```

### Important: Agent Behavior with SDK
The SDK sends a single message per `agent.send()` call. The agent cannot prompt the user for confirmation interactively. The agent will either:
1. Treat the `/crux-forget <id>` as a confirmed delete (most likely)
2. Ask for confirmation but then proceed since there's no follow-up

Design tests to handle both behaviors. Focus on ground-truth assertions (file deleted, index updated) rather than confirmation prompt verification.

### Performance Notes
- R1 deletion is a single agent turn (~30-60s)
- R2 search + delete may be a single or double turn
- Total file budget: ~3-5 minutes for all R tests

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Run `pnpm test:forget` to execute only this file
- Verify fixture setup creates all expected memory and tracker files

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-04-26T12:23:00+10:00
- Completed: 2026-04-26T12:24:00+10:00

### Work Log
- Read subtask spec, harness.ts, and j-recall.test.ts for patterns
- Created `evals/sdk/tests/r-forget.test.ts` with 6 tests across R1 (4) and R2 (2)
- R1 tests share a `forgetResult` at describe scope; first test populates it, subsequent tests assert filesystem ground truth
- R2 tests use a separate agent turn with search-by-keyword (`/crux-forget "performance"`)
- Verified TypeScript compiles — only pre-existing `Symbol.asyncDispose` TS7053 error (same as all other test files)
- No new linter errors introduced

### Blockers Encountered
- None

### Files Modified
- `evals/sdk/tests/r-forget.test.ts` (created)
- `specs/20260426-sdk-eval-expansion/subtask-06-sdk-eval-forget-tests-20260426.md` (updated checklist + execution notes)
