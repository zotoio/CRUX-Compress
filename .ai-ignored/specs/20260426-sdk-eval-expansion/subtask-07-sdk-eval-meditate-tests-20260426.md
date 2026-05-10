# Subtask: Meditate Tests (Q1-Q3)

## Metadata
- **Subtask ID**: 07
- **Feature**: SDK Eval Suite Expansion
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 01, 02
- **Created**: 20260426

## Objective

Create `evals/sdk/tests/q-meditate.test.ts` covering USER_EVAL_CHECKLISTS.md scenarios Q1, Q2, and Q3. These test the `/crux-meditate` command's ability to derive exploration facets, spawn recursive subagents, query memories at each level, and present consolidated insights.

Meditate is the most expensive command to test (3-level recursive subagent spawning). Tests are designed to verify the high-level flow — facet derivation, subagent spawning, memory references, and consolidated output — without tracing every recursion level.

## Deliverables Checklist
- [x] Create `evals/sdk/tests/q-meditate.test.ts`
- [x] Q1 tests: Meditate with no arguments — context-derived facets
- [x] Q2 tests: Meditate with topic argument — topic-driven facets
- [x] Q3 tests: Meditate with file/folder reference — code-derived facets (simplified)
- [x] All tests use isolated worktrees with diverse memory fixtures
- [ ] All tests pass (requires API key + expensive SDK runs; not verifiable offline)

## Definition of Done
- [x] `q-meditate.test.ts` has at least 6 tests across Q1, Q2, Q3
- [ ] All tests pass when run via `pnpm test:meditate` (requires API key + expensive SDK runs)
- [x] No linter errors (only pre-existing `Symbol.asyncDispose` type issue shared across all test files)
- [x] Tests do not modify the real repository

## Implementation Notes

### Test Structure

```
describe("Q: Meditate", () => {
  // Shared workspace with diverse memories across types and tags
  
  describe("Q1: Meditate - No Arguments (Context-Derived Facets)", () => {
    // 3 tests
  })
  
  describe("Q2: Meditate - Topic Argument", () => {
    // 2 tests
  })
  
  describe("Q3: Meditate - File/Folder References", () => {
    // 1-2 tests
  })
})
```

### Fixture Setup (beforeAll)

1. Create an isolated workspace
2. Create 6-8 diverse memory fixtures covering multiple domains:
   - Performance/optimization memories (2-3)
   - Security memories (1-2)
   - Architecture/design memories (1-2)
   - Testing/quality memories (1)
3. Rebuild memory index
4. Ensure the workspace has at least one source file for Q3 (the worktree already has the full repo)

### Q1 Tests (~3 tests)
**ALL Q1 tests use timeout: 480_000 (480s)** — meditate spawns multiple levels of subagents.

**Test: "derives exploration facets from context"**
- First send a setup message about performance optimization (to establish context)
- Then send `/crux-meditate`
- Assert output contains facet-related language: "facet", "theme", "dimension", "exploration", "branch"
- Assert output mentions at least 2 distinct exploration directions

**Test: "spawns subagents for recursive exploration"**
- From the same run, check `result.toolCalls` for `Task` subagent spawns
- The agent should spawn at least 1 subagent (memory manager or exploration agents)
- `hasSubagentCall(result.toolCalls, "crux-cursor-memory-manager")` should be true, OR multiple `Task` calls exist

**Test: "references memories in consolidated output"**
- From the same run, assert the consolidated output references at least one existing memory
- Check for memory titles, tags, or the word "memory" in the insight output
- Assert output contains consolidation language: "insight", "finding", "pattern", "connection", "theme"

### Q2 Tests (~2 tests)
Timeout: 480_000 (480s).

**Test: "derives facets from provided topic"**
- Send `/crux-meditate "how should we approach caching strategies"`
- Assert output contains facet derivation related to caching
- Look for patterns: "cache", "strategy", "ttl", "invalidation", or domain-specific terms

**Test: "produces consolidated insights referencing memories"**
- From the same run, assert the output references existing memory content
- Assert output contains at least one cross-reference or connection between facets
- Look for: "connection", "pattern", "across", "relate", "link"

### Q3 Tests (~1-2 tests)
Timeout: 480_000 (480s).

**Test: "derives facets from file/folder reference"**
- Send `/crux-meditate` with a reference to an existing directory in the worktree (e.g., "Explore the patterns in .cursor/skills/")
- Assert output contains facet derivation related to the referenced code
- Assert the session completes without errors (status: "finished")

### Assertion Patterns

For facet derivation:
```typescript
const hasFacets =
  /facet|theme|dimension|branch|direction|aspect/i.test(result.assistantText) ||
  /(1\.|2\.|3\.|\(1\)|\(2\)|\(3\)|first|second|third)/i.test(result.assistantText);
```

For memory references in output:
```typescript
const referencesMemory =
  result.assistantText.toLowerCase().includes("memory") ||
  result.assistantText.includes("memoize") ||  // from fixture
  result.assistantText.includes("cache") ||     // from fixture
  result.assistantText.includes("security");    // from fixture
```

For subagent spawning:
```typescript
const taskCalls = result.toolCalls.filter(tc => tc.name === "Task");
expect(taskCalls.length).toBeGreaterThanOrEqual(1);
```

### Performance Notes
- **Meditate is the most expensive test file** in the suite
- Each test involves recursive subagent spawning (3 levels × 3 facets = up to 13 agents)
- Expected time per test: 90-180 seconds
- Total file budget: 8-12 minutes
- This file will be the wall-clock bottleneck for the full suite
- Consider reducing Q3 to a single test to save ~2-3 minutes
- Q1 setup message + meditate = 2 agent turns per test
- Q2 and Q3 = 1 agent turn each (topic/reference provided directly)

### Simplification Decisions
- Do NOT verify every recursion level individually (would require 13 separate assertions)
- DO verify subagent spawning occurs (Task tool calls exist)
- DO verify the final consolidated output references memories
- DO verify the interactive continuation menu is presented (if it appears in output)
- Do NOT test "Save as draft spec" from the continuation menu — that's an interactive follow-up the SDK can't easily test

### Cost Control — `SDK_EVAL_SKIP_EXPENSIVE` (default: skip)
Meditate tests are the most expensive in the suite (~13 agent invocations per test). **By default, expensive tests are skipped** to prevent accidental API spend:

```typescript
const skipExpensive = process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false";

describe.skipIf(skipExpensive)("Q: Meditate", () => {
  // ...
});
```

The env var defaults to `true` (skip). To explicitly run expensive tests:
```bash
SDK_EVAL_SKIP_EXPENSIVE=false pnpm test:meditate
```

Document this in `evals/sdk/README.md` and the `.env.example` file.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Run `pnpm test:meditate` to execute only this file
- Set generous timeouts — meditate can take 3-5 minutes per test

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-04-26T12:24:00+10:00
- Completed: 2026-04-26T12:30:00+10:00

### Work Log
- Read harness.ts for exact function signatures and helpers
- Read j-recall.test.ts and p-amnesia.test.ts for established test patterns
- Created q-meditate.test.ts with 6 tests across Q1 (3), Q2 (2), Q3 (1)
- Used `describe.skipIf(skipExpensive)` gating with `SDK_EVAL_SKIP_EXPENSIVE` env var
- Used `sendWithRetry()` for all agent turns to handle rate limiting
- Q1 shares a single agent across 3 tests via `beforeAll` (2 agent turns: setup + meditate)
- Q2 shares a single agent across 2 tests via `beforeAll` (1 turn)
- Q3 uses a standalone agent with try/finally cleanup (1 turn)
- Fixed `beforeAll` timeout syntax: vitest takes a plain number, not `{ timeout }` object
- TypeScript compiles cleanly — only pre-existing `Symbol.asyncDispose` type issue shared with all other test files
- No linter errors introduced
- 8 diverse memory fixtures across performance (3), security (2), architecture (2), testing (1)

### Blockers Encountered
- None. "All tests pass" checklist items left unchecked — requires running with `SDK_EVAL_SKIP_EXPENSIVE=false` and a valid `CURSOR_API_KEY`, which is an expensive operation (~13 subagent invocations per test).

### Files Modified
- `evals/sdk/tests/q-meditate.test.ts` (created)
- `specs/20260426-sdk-eval-expansion/subtask-07-sdk-eval-meditate-tests-20260426.md` (updated)
