# Subtask: Test Architecture & Correctness Strategy

## Metadata
- **Subtask ID**: 01
- **Feature**: SDK Eval Suite Expansion
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: None
- **Created**: 20260426

## Objective

Produce a concise architecture document (in this subtask's execution notes) that defines the test design patterns, assertion strategies, fixture conventions, and performance budget for all new SDK eval test files. This serves as the reference for subtasks 04-08.

## Deliverables Checklist
- [ ] Assertion pattern guide: document the canonical patterns for resilient non-deterministic output checking (OR-keyword lists, regex alternatives, tool-call structural checks, file-system ground truth)
- [ ] Fixture strategy: document which helpers each test file needs and the fixture data shapes (spec fixtures, aged memories, conflicting memories, orphaned trackers)
- [ ] Timeout budget table: per-test-file timeout recommendations based on expected agent turns per test
- [ ] Parallelization confirmation: verify that per-file worktree isolation is sufficient for safe multi-fork execution
- [ ] Test count projection: estimated test count per file with rationale for consolidation choices (e.g., batching multiple assertions per agent turn to reduce wall-clock)

## Definition of Done
- [ ] Architecture decisions documented in Execution Notes below
- [ ] No code changes — this is a design-only subtask
- [ ] Decisions are actionable enough for `crux-software-engineer` to implement without ambiguity

## Implementation Notes

### Files to Review
- `evals/sdk/helpers/harness.ts` — existing harness patterns
- `evals/sdk/tests/j-recall.test.ts` — best example of flexible assertion patterns
- `evals/sdk/tests/p-amnesia.test.ts` — best example of multi-turn conversation tests
- `evals/sdk/vitest.config.ts` — current pool/fork config
- `evals/USER_EVAL_CHECKLISTS.md` — authoritative scenarios for B, C, Q, R, N

### Key Questions to Address

1. **Correctness trade-offs**: For Dream (B2), the checklist expects ordered steps (execution verify → diff analysis → candidate presentation → memory creation → dream summary → archival offer). Should we test each step in isolation (more agent turns, slower) or verify them all from a single agent turn (faster but harder to diagnose failures)?
   - Recommendation: Single agent turn with batched assertions. Each assertion checks a different expected pattern in the output. If one fails, the error message identifies which step's output was missing.

2. **Meditate depth verification**: Q1 expects 3 levels of recursive subagent spawning. Should we count `Task` tool calls to verify 3 levels, or just check that the consolidated output references memories?
   - Recommendation: Check for `Task` tool calls (subagent spawning) AND verify the final output references memories. Don't try to trace the full recursion tree — just verify entry and exit.

3. **REM Sleep auto-apply verification (C2)**: Verifying that promotions/demotions are applied requires checking file moves across directories. Should we verify every file operation or sample one?
   - Recommendation: Verify at least one promotion (file moved from idea/ to learning/) and one cleanup (orphaned tracker deleted). Sample-based verification is sufficient given the deterministic fixture setup.

4. **Forget confirmation (R1)**: The checklist requires that deletion is NOT performed without confirmation. With the SDK (single-turn send), the agent will complete the full flow. Should we check that the output contains a confirmation message before the deletion report?
   - Recommendation: Check output contains both "confirm" language and "deleted" language. Also verify ground truth (file actually deleted). The agent will treat the /crux-forget command as user intent and complete the flow.

5. **N1 integration turn budget**: How many agent turns can we afford?
   - Recommendation: Maximum 6 turns (Dream → Recall → Remember → Forget → Amnesia on → Amnesia off). Budget 600s total. Each turn averages 60-90s.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- This subtask produces no code — no tests needed

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
[None — design-only subtask]
