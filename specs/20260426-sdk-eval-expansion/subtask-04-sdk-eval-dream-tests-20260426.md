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
- [ ] Create `evals/sdk/tests/b-dream.test.ts`
- [ ] B1 tests: Dream with no arguments — list unprocessed specs
- [ ] B2 tests: Dream with spec name — full flow
- [ ] B3 tests: Dream conflict detection
- [ ] All tests use isolated worktrees and spec fixtures
- [ ] All tests pass

## Definition of Done
- [ ] `b-dream.test.ts` has at least 8 tests across B1, B2, B3
- [ ] All tests pass when run via `pnpm test:dream`
- [ ] No linter errors
- [ ] Tests do not modify the real repository

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
