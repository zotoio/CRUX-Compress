# Subtask: REM Sleep Tests (C1-C3)

## Metadata
- **Subtask ID**: 05
- **Feature**: SDK Eval Suite Expansion
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 01, 02
- **Created**: 20260426

## Objective

Create `evals/sdk/tests/c-rem.test.ts` covering USER_EVAL_CHECKLISTS.md scenarios C1, C2, and C3. These test the `/crux-dream --rem` command's ability to analyze memories, present promotion/demotion/cleanup recommendations, auto-apply in `--yolo` mode, and handle conflicts requiring user input.

## Deliverables Checklist
- [ ] Create `evals/sdk/tests/c-rem.test.ts`
- [ ] C1 tests: REM Sleep interactive recommendations
- [ ] C2 tests: REM Sleep `--yolo` mode auto-apply
- [ ] C3 tests: REM Sleep conflict resolution
- [ ] All tests use isolated worktrees with seeded memory fixtures
- [ ] All tests pass

## Definition of Done
- [ ] `c-rem.test.ts` has at least 8 tests across C1, C2, C3
- [ ] All tests pass when run via `pnpm test:rem`
- [ ] No linter errors
- [ ] Tests do not modify the real repository

## Implementation Notes

### Test Structure

```
describe("C: REM Sleep", () => {
  // Shared workspace with diverse aged memories, orphaned trackers, conflicts
  
  describe("C1: REM Sleep - Interactive Recommendations", () => {
    // 3-4 tests
  })
  
  describe("C2: REM Sleep - Yolo Mode Auto-Apply", () => {
    // 3-4 tests
  })
  
  describe("C3: REM Sleep - Conflict Resolution", () => {
    // 2-3 tests
  })
})
```

### Fixture Setup (beforeAll)

1. Create an isolated workspace
2. **Promotion candidate**: Use `createMemoryFixture()` with `type: "idea"` and `strength: 6` (exceeds idea's `promoteAt` threshold of 5)
3. **Demotion candidate**: Use `seedAgedMemory()` with `daysAgo: 100` (exceeds `demoteAfterDaysUnreferenced` of 90 days). Also create a tracker with `lastReferenced` set 100 days ago.
4. **Archival candidate**: Use `seedAgedMemory()` with `daysAgo: 200` (exceeds `archiveAfterDaysUnreferenced` of 180 days)
5. **Orphaned tracker**: Use `createOrphanedTracker(ws.root, "nonexistent-memory")` — tracker exists but memory does not
6. **Conflicting memories**: Use `createConflictingMemories()` with opposing views on a topic
7. **Normal memories**: Create 2-3 healthy memories that should not trigger any REM actions
8. Rebuild memory index

### C1 Tests (~3-4 tests)
Timeout: 300_000 (300s).

**Test: "presents structured REM sleep report"**
- Send `/crux-dream --rem`
- Assert output contains section-like structure: at least 2 of ["promotion", "demotion", "archival", "cleanup", "conflict", "consolidation"]

**Test: "identifies promotion candidates"**
- From the same run, assert output mentions the idea memory with strength ≥ 5 and suggests promotion
- Look for patterns like "promote", "idea → learning", or the memory title

**Test: "identifies demotion and archival candidates"**
- Assert output mentions the aged memory (100+ days unreferenced) for demotion
- Assert output mentions the very aged memory (200+ days) for archival
- Look for patterns like "unreferenced", "days", "demote", "archive"

**Test: "asks for confirmation before applying changes"**
- Assert output contains confirmation language: "confirm", "approve", "apply", "proceed", "select"
- Assert the agent does NOT auto-apply changes (no file modifications to fixture memories yet)

### C2 Tests (~3-4 tests)
Timeout: 300_000 (300s).

**Test: "auto-applies non-conflict changes in yolo mode"**
- Send `/crux-dream --rem --yolo`
- Assert output contains auto-apply language: "applied", "auto", "✅", "promoted", "cleaned"
- Assert output does NOT ask for confirmation for non-conflict items

**Test: "cleans up orphaned trackers automatically"**
- After the yolo run, use `assertTrackerDeleted(ws.root, "nonexistent-memory")` to verify the orphan was cleaned
- OR check output confirms orphan cleanup

**Test: "rebuilds memory index after changes"**
- After the yolo run, check that `.crux/memory-index.yml` exists and has been updated
- Use `readMemoryIndex(ws.root)` and verify it reflects the current state

**Test: "conflicts still require user input in yolo mode"**
- From the same yolo run, assert output separates conflicts from auto-applied changes
- Assert output contains conflict-related language and resolution options

### C3 Tests (~2-3 tests)
Timeout: 300_000 (300s).

**Test: "presents both sides of a conflict"**
- Send `/crux-dream --rem --yolo` (or `/crux-dream --rem`)
- Assert output shows both conflicting memory titles
- Assert output provides resolution options

**Test: "does not auto-resolve conflicts"**
- Assert neither conflicting memory is deleted or modified without user input
- Check file system: both conflicting memory files still exist after the run

### Assertion Patterns

For REM report sections:
```typescript
const sectionKeywords = [
  "promot", "demot", "archiv", "cleanup", "orphan",
  "conflict", "consolidat", "rebalanc", "recommend"
];
const matchCount = sectionKeywords.filter(kw => 
  result.assistantText.toLowerCase().includes(kw)
).length;
expect(matchCount).toBeGreaterThanOrEqual(2);
```

For confirmation vs auto-apply:
```typescript
const asksConfirmation = /confirm|approve|select|proceed|apply.*\?/i.test(result.assistantText);
const autoApplied = /auto.*appl|✅.*promot|✅.*clean/i.test(result.assistantText);
```

### SDK Single-Turn Non-Interactive Strategy
REM Sleep in non-yolo mode (C1) normally asks for user confirmation. Since the SDK uses single-turn `agent.send()` with no follow-up, **all prompts must be fully non-interactive directives**:

- C1 tests focus on the **report structure** (sections present, candidates identified, actionable recommendations) rather than confirmation-gating behavior. The prompt should be a directive: `/crux-dream --rem — analyze and present recommendations without waiting for confirmation`.
- The agent may auto-apply changes in a single turn — if so, verify ground-truth state (files moved, trackers cleaned) rather than asserting it "waited".
- C2 (`--yolo`) explicitly controls auto-apply, making it the cleanest test for verifying automated application.
- C3 (conflict resolution): Prompt must include explicit conflict instruction: `/crux-dream --rem --yolo — present any conflicts for review but do not auto-resolve`. The agent surfaces conflicts but does not auto-resolve them even in `--yolo` mode.
- **Never rely on interactive confirmation** — the agent cannot receive follow-up input. All instructions for the complete flow must be in the initial prompt.

### Performance Notes
- C1 and C2 each require a single agent turn (~60-90s)
- C3 can share the C2 run if the assertions are compatible
- Consider batching C2 + C3 into a single test that sends `--rem --yolo` and checks both auto-apply and conflict handling
- Total file budget: ~5-7 minutes for all C tests

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Run `pnpm test:rem` to execute only this file
- Verify fixture setup produces the expected file structure before running agent tests

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
