# Subtask: Cross-Platform N1 Integration Test

## Metadata
- **Subtask ID**: 08
- **Feature**: SDK Eval Suite Expansion
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 01, 02, 04, 05, 06, 07
- **Created**: 20260426

## Objective

Create `evals/sdk/tests/n-integration.test.ts` covering USER_EVAL_CHECKLISTS.md scenario N1 (Cursor full flow). This is a multi-turn integration test that exercises the complete CRUX Memories command chain in a single agent session: Dream → post-dream index rebuild → Recall → Remember → Forget → Amnesia toggle.

Meditate and REM are excluded from N1 to keep the test under 10 minutes. They are covered individually in their own test files (subtasks 05 and 07).

## Deliverables Checklist
- [ ] Create `evals/sdk/tests/n-integration.test.ts`
- [ ] N1 integration test: multi-turn Cursor full flow
- [ ] Uses a single agent session with sequential `agent.send()` calls
- [ ] Verifies end-to-end command wiring and state continuity across turns
- [ ] All tests pass

## Definition of Done
- [ ] `n-integration.test.ts` has 3-4 tests in a sequential flow
- [ ] All tests pass when run via `pnpm test:integration`
- [ ] No linter errors
- [ ] Test completes within 600s (10 minutes)
- [ ] Tests do not modify the real repository

## Implementation Notes

### Test Structure

The N1 test uses a sequential multi-turn conversation in a single agent session. Each turn builds on the previous one, verifying state continuity.

```
describe("N: Cross-Platform Integration", () => {
  // Single workspace, single agent, multiple turns
  
  describe("N1: Cursor Full Flow", () => {
    it("executes Dream → Recall → Remember → Forget → Amnesia in sequence")
    // OR split across multiple its that share the same agent
  })
})
```

### Design Decision: Single Test vs Multiple Tests

**Option A: Single large test** — One `it()` with 6 sequential `agent.send()` calls and assertions between each. Pro: shared agent state, faster (no agent re-creation). Con: if one step fails, all subsequent steps are skipped.

**Option B: Multiple tests sharing an agent** — Use `let agent` at describe scope, create in `beforeAll`, send sequentially across `it()` blocks using `test.sequential`. Pro: individual pass/fail per step. Con: Vitest `test.sequential` ensures order.

**Recommendation**: Option B with `test.sequential` (Vitest 3.x supports `describe.sequential`). This gives individual pass/fail while maintaining the multi-turn session.

### Fixture Setup (beforeAll)

1. Create an isolated workspace
2. Create a completed spec fixture for dream testing
3. Create 3-4 memory fixtures for recall testing
4. Rebuild memory index
5. Create the agent (shared across all sequential tests)

### Test Flow (~4 tests, sequential)
**All tests use timeout: 600_000 (600s total for the describe block).**

**Test 1: "Dream extracts memories from completed spec"**
- Send `/crux-dream 20260420-test-feature`
- Assert: output mentions candidates, memory creation
- Verify: at least one new memory file exists after this turn
- Verify: dream summary file exists in spec directory

**Test 2: "Recall retrieves memories including dreamed ones"**
- Send `/crux-recall`
- Assert: output displays at least one memory (fixture or newly dreamed)
- Assert: output contains structured format (type labels, metadata)

**Test 3: "Remember creates ad-hoc memory"**
- Send `/crux-remember "Integration test: always verify state continuity" --type learning`
- Assert: output confirms creation
- Verify: new learning memory file exists
- Record the memory slug for next test

**Test 4: "Forget deletes the just-created memory"**
- Send `/crux-forget "state continuity"` (search by content of the memory just created)
- Assert: output confirms deletion
- Verify: the memory file is deleted
- Verify: index no longer contains the deleted memory

**Optional Test 5: "Amnesia toggles correctly after full flow"**
- Send `/crux-amnesia on`
- Assert: output confirms amnesia mode is active
- Note: This verifies command wiring works even after dream/recall/remember/forget operations

### Assertion Patterns

Integration tests use relaxed assertions since the focus is on command wiring:
```typescript
// Dream worked
expect(listMemoryFiles(ws.root).length).toBeGreaterThan(initialMemoryCount);

// Recall worked
expect(result.assistantText.toLowerCase()).toContain("memory");

// Remember worked
const newFiles = listMemoryFiles(ws.root).filter(f => !previousFiles.includes(f));
expect(newFiles.length).toBeGreaterThanOrEqual(1);

// Forget worked
expect(listMemoryFiles(ws.root).length).toBeLessThan(afterRememberCount);
```

### Performance Notes
- 5 agent turns × ~60-90s average = ~5-8 minutes total
- This is the second most expensive test file after meditate
- Budget: 600s (10 minutes) for the full describe block
- The sequential nature means no parallelization within this file
- Per-test timeout: 180s for dream, 120s for others

### Cost Control — `SDK_EVAL_SKIP_EXPENSIVE` (default: skip)
The integration test involves 5+ agent turns and is the second most expensive file after Meditate. Gate it behind the same env variable, **which defaults to true (skip)**:

```typescript
const skipExpensive = process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false";

describe.skipIf(skipExpensive)("N: Cross-Platform Integration", () => {
  // ...
});
```

To explicitly run expensive tests:
```bash
SDK_EVAL_SKIP_EXPENSIVE=false pnpm test:integration
```

### State Continuity Considerations
- The same `agent` instance is reused across all turns, maintaining conversation context
- Each turn can reference previous actions ("the memory I just created")
- Fixture memory count must be tracked to distinguish new files from fixtures
- Use `beforeAll` to record the initial state (file count, index content)

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Run `pnpm test:integration` to execute only this file
- This file runs as a single sequential block — no internal parallelization

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
