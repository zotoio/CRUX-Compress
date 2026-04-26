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
- [ ] Create `evals/sdk/tests/r-forget.test.ts`
- [ ] R1 tests: Forget by memory ID — confirmation, deletion, tracker cleanup, index rebuild
- [ ] R2 tests: Forget by search query — search results, selective deletion
- [ ] All tests use isolated worktrees with pre-seeded memories and trackers
- [ ] All tests pass

## Definition of Done
- [ ] `r-forget.test.ts` has at least 6 tests across R1, R2
- [ ] All tests pass when run via `pnpm test:forget`
- [ ] No linter errors
- [ ] Tests do not modify the real repository

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
