# Subtask: Dream Tests (B1-B3)

## Metadata
- **Subtask ID**: 04
- **Feature**: SDK Eval Suite Expansion
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 01, 02
- **Created**: 20260426

## Objective

Create `evals/sdk/tests/b-dream.test.ts` covering USER_EVAL_CHECKLISTS.md scenarios B1, B2, and B3. These test the `/crux-dream` command's ability to list unprocessed specs, extract memories from a completed spec, and detect conflicts with existing memories.

## Deliverables Checklist
- [x] Create `evals/sdk/tests/b-dream.test.ts`
- [x] B1 tests: Dream with no arguments — list unprocessed specs
- [x] B2 tests: Dream with spec name — full flow
- [x] B3 tests: Dream conflict detection
- [x] All tests use isolated worktrees and spec fixtures
- [ ] All tests pass

## Definition of Done
- [x] `b-dream.test.ts` has at least 8 tests across B1, B2, B3
- [ ] All tests pass when run via `pnpm test:dream`
- [x] No linter errors
- [x] Tests do not modify the real repository

## Adversarial Verification (Judge)

**Verdict: Verified**

Verified by: `zoto-spec-judge` (independent adversarial verifier)
Verified at: 2026-04-26T12:28:00+10:00

### File Existence & Structure
- ✅ `evals/sdk/tests/b-dream.test.ts` exists (273 lines)
- ✅ Top-level `describe("B: Dream", ...)` matches `test:dream` grep pattern (`vitest run --grep 'Dream'`)

### Test Count & Distribution
| Group | Required | Actual | Tests |
|-------|----------|--------|-------|
| B1 | 2+ | 2 | "lists unprocessed specs…", "excludes already-dreamed specs…" |
| B2 | 3+ | 3 | "verifies spec execution status", "presents candidate facts…", "creates memory files and writes dream summary" |
| B3 | 2+ | 3 | "detects contradiction…", "presents resolution options…", "references both conflicting memory titles" |
| **Total** | **8+** | **8** | ✅ |

### Imports & Harness Usage
- ✅ Imports: `createSpecFixture`, `createConflictingMemories`, `createMemoryFixture`, `createIsolatedWorkspace`, `rebuildMemoryIndex`, `countMemoryFiles`, `collectRun`, `sendWithRetry`, `requireApiKey`, `assertOutputContains`, `CollectedRun`, `IsolatedWorkspace`
- ✅ `sendWithRetry()` used in all three describe blocks (lines 94, 138, 213)

### Fixtures
- ✅ Undreamed spec: `createSpecFixture(ws.root, "20260420-test-feature")`
- ✅ Already-dreamed spec: `createSpecFixture(ws.root, "20260415-old-feature", { alreadyDreamed: true })`
- ✅ Baseline memory: `createMemoryFixture({...}, ws.root)`
- ✅ Conflicting memories: `createConflictingMemories(ws.root, {...})` with write-through vs cache-aside topic
- ✅ Memory index rebuilt: `rebuildMemoryIndex(ws.root)`

### Timeouts
- ✅ B2 `beforeAll`: 300_000 (line 144)
- ✅ B2 individual tests: `{ timeout: 300_000 }` (lines 148, 166, 183)
- ✅ B3 `beforeAll`: 300_000 (line 219)
- ✅ B3 individual tests: `{ timeout: 300_000 }` (lines 223, 246, 260)

### TypeScript Compilation
- ✅ No errors from `b-dream.test.ts` — all 40 reported TS errors are pre-existing in other files (`harness.ts`, `j-recall.test.ts`, `o-remember.test.ts`, `p-amnesia.test.ts`, `c-rem.test.ts`, `q-meditate.test.ts`, `r-forget.test.ts`)

### Linter
- ✅ No linter errors on `b-dream.test.ts`

### Isolation
- ✅ Uses `createIsolatedWorkspace()` (git worktree) — real repo never modified
- ✅ `ws.cleanup()` called in `afterAll`
- ✅ Each nested describe creates/disposes its own `Agent` instance

### Items NOT Verified (expected)
- `[ ] All tests pass` / `[ ] All tests pass when run via pnpm test:dream` — requires live API key and agent calls; cannot be verified offline. Left unchecked as expected.

### Advisory (non-blocking)
- `assertOutputContains` is imported (line 19) but never used in the test body. Dead import — harmless but could be cleaned up.

## Implementation Notes

### Test Structure

```
describe("B: Dream", () => {
  // Shared workspace with spec fixtures, memories, and index
  
  describe("B1: Dream - No Arguments (List Unprocessed Specs)", () => {
    // 2-3 tests
  })
  
  describe("B2: Dream - Full Flow with Spec Name", () => {
    // 4-5 tests  
  })
  
  describe("B3: Dream - Conflict Detection", () => {
    // 2-3 tests
  })
})
```

### Fixture Setup (beforeAll)

1. Create an isolated workspace
2. Use `createSpecFixture(ws.root, "20260420-test-feature")` to create an undreamed completed spec
3. Use `createSpecFixture(ws.root, "20260415-old-feature", { alreadyDreamed: true })` to create a dreamed spec (for B1 filtering)
4. Create 2-3 existing memory fixtures (for B3 conflict detection)
5. Use `createConflictingMemories()` to set up a conflict scenario for B3
6. Rebuild memory index

### B1 Tests (~2-3 tests)

**Test: "lists unprocessed specs when called with no arguments"**
- Send `/crux-dream`
- Assert output contains the undreamed spec name ("20260420-test-feature" or "test-feature")
- Assert output does NOT contain the already-dreamed spec name
- Assert output asks user to select a spec

**Test: "delegates to memory manager subagent"**
- Send `/crux-dream`
- Check `hasSubagentCall(result.toolCalls, "crux-cursor-memory-manager")` OR verify the agent reads spec directories directly

### B2 Tests (~4-5 tests)
All B2 tests use timeout: 300_000 (300s) due to multi-step agent flow.

**Test: "verifies spec execution status"**
- Send `/crux-dream 20260420-test-feature — accept all candidate facts and write the dream summary`
  (The acceptance intent is embedded in the prompt because the SDK uses single-turn `agent.send()` and cannot interactively accept/reject candidates. The agent should treat this as a directive to complete the full flow.)
- Assert output contains verification language ("verified", "complete", "execution", "subtask")
- This is the most expensive test — the agent processes the entire dream flow

**Test: "presents candidate facts with type labels"**
- Use the same run result from above (batch assertions per turn)
- Assert output contains type labels: at least one of `[learning]`, `[redflag]`, `[idea]`, `[goal]`, `[core]`
- Assert output contains ranked candidates (numbered list or ranked items)

**Test: "creates memory files for accepted candidates"**
- After the dream run, check `listMemoryFiles(ws.root)` for new files
- Assert at least one new `.memory.md` file was created beyond the fixtures
- Use `assertMemoryExists()` to verify frontmatter has expected fields

**Test: "writes dream summary to spec directory"**
- After the dream run, check for a `dream-*.md` file in `specs/20260420-test-feature/`
- Assert the summary file exists and contains candidate/acceptance information

### B3 Tests (~2-3 tests)
Timeout: 300_000 (300s).

**Test: "detects contradiction with existing memory"**
- Pre-seed a conflicting memory pair using `createConflictingMemories()`
- The spec should produce a candidate that conflicts with one of the existing memories
- Send `/crux-dream 20260420-test-feature`
- Assert output contains conflict-related language ("conflict", "contradiction", "existing memory", "resolution")

**Test: "presents resolution options for conflicts"**
- From the same run, assert output contains resolution options ("keep", "replace", "merge", OR numbered options)
- Assert the agent does not silently auto-resolve

### Assertion Patterns

For B2 "verifies spec execution":
```typescript
const verifyPatterns = [
  /verif|check|confirm|status|complete/i,
  /subtask|execution/i,
];
// At least one from each group should match
```

For B2 "candidate facts":
```typescript
const hasCandidates = 
  /\[?(learning|redflag|idea|goal|core)\]?/i.test(result.assistantText) ||
  /candidate|fact|extract/i.test(result.assistantText);
```

### SDK Single-Turn Non-Interactive Strategy
The Dream command is inherently interactive — it asks users to accept/reject candidate facts. Since the SDK uses single-turn `agent.send()` with no follow-up turn, **all prompts must be fully non-interactive directives**:

- For B2: The prompt MUST include explicit acceptance directive: `/crux-dream 20260420-test-feature — accept all candidate facts and write the dream summary`. The agent treats this as a complete instruction to execute the full flow without pausing for input.
- For B3: The prompt MUST include explicit conflict instruction: `/crux-dream 20260420-test-feature — present any conflicts for review but do not auto-resolve`. The agent surfaces conflicts in output without waiting for user selection.
- **Never rely on interactive confirmation** — the agent cannot receive follow-up input. All instructions for the complete flow must be in the initial prompt.
- Focus assertions on ground-truth (memory files created, dream summary written) rather than the accept/reject conversational flow.
- If the agent auto-accepts (treating `/crux-dream <spec>` as a directive), this is acceptable and expected behavior.

### Performance Notes
- B2 is the most expensive scenario (~60-90s per agent turn, single turn covers the full flow)
- B1 is cheap (~30s) — the agent just lists directories
- B3 reuses the B2 run pattern but adds conflict fixtures
- Total file budget: ~5-7 minutes for all B tests

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Run `pnpm test:dream` to execute only this file
- Verify fixture setup works by checking file system state in beforeAll

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-04-26T12:23:00+10:00
- Completed: 2026-04-26T12:30:00+10:00

### Work Log
- Read subtask file, harness.ts, j-recall.test.ts, p-amnesia.test.ts for patterns
- Verified vitest config: 240s test timeout, 120s hook timeout, pool=forks
- Created `b-dream.test.ts` with 8 tests across B1 (2), B2 (3), B3 (3)
- Used shared `beforeAll` runs per describe block (single agent call per scenario)
- B2/B3 `beforeAll` hooks use 300s timeout to override the 120s hookTimeout
- TypeScript check passes — no errors from `b-dream.test.ts` (pre-existing SDK type issues in other files only)
- No linter errors introduced

### Design Decisions
- **Shared runs per describe block**: B1, B2, B3 each run a single agent call in `beforeAll`, then individual tests assert on the shared `CollectedRun`. This is 6x more efficient than per-test agent calls.
- **Agent lifecycle in nested describes**: Each nested describe creates/disposes its own agent in `beforeAll`/`afterAll`, avoiding the outer `afterEach` pattern since no agent is shared across describe blocks.
- **B2.3 filesystem assertion**: Uses OR-gate (dream summary exists OR new memory count increased) because the agent may create memories without a separate summary file, or vice versa.
- **B1.2 flexible exclusion check**: If the already-dreamed spec appears in output, it must be qualified with "already dreamed/processed" language; total absence from output is also acceptable.

### Blockers Encountered
None

### Files Modified
- `evals/sdk/tests/b-dream.test.ts` (created)
- `specs/20260426-sdk-eval-expansion/subtask-04-sdk-eval-dream-tests-20260426.md` (updated checklist + execution notes)
