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
- [x] Assertion pattern guide: document the canonical patterns for resilient non-deterministic output checking (OR-keyword lists, regex alternatives, tool-call structural checks, file-system ground truth)
- [x] Fixture strategy: document which helpers each test file needs and the fixture data shapes (spec fixtures, aged memories, conflicting memories, orphaned trackers)
- [x] Timeout budget table: per-test-file timeout recommendations based on expected agent turns per test
- [x] Parallelization confirmation: verify that per-file worktree isolation is sufficient for safe multi-fork execution
- [x] Test count projection: estimated test count per file with rationale for consolidation choices (e.g., batching multiple assertions per agent turn to reduce wall-clock)

## Definition of Done
- [x] Architecture decisions documented in Execution Notes below
- [x] No code changes — this is a design-only subtask
- [x] Decisions are actionable enough for `crux-software-engineer` to implement without ambiguity

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

### Agent Session Info
- Agent: crux-platform-architect
- Started: 2026-04-26T12:17+10:00
- Completed: 2026-04-26T12:17+10:00

### Work Log
- Reviewed `j-recall.test.ts`, `p-amnesia.test.ts`, `o-remember.test.ts` for existing patterns
- Reviewed `harness.ts` for available helpers and fixture shapes
- Reviewed `vitest.config.ts` and `vitest.setup.ts` for pool/timeout/env config
- Reviewed `USER_EVAL_CHECKLISTS.md` for authoritative scenario definitions
- Wrote architecture decisions below

### Blockers Encountered
None.

### Files Modified
None — design-only subtask.

---

## Architecture Decisions

### 1. Assertion Pattern Guide

All new test files MUST follow these canonical assertion patterns, derived from `j-recall.test.ts` and `p-amnesia.test.ts`. The agent is non-deterministic — assertions must be resilient to phrasing variation.

#### 1a. OR-Keyword Lists (Preferred for Text Output)

Use when checking that the agent mentioned a concept, regardless of exact wording:

```typescript
const confirmsAction =
  result.assistantText.toLowerCase().includes("created") ||
  result.assistantText.toLowerCase().includes("saved") ||
  result.assistantText.toLowerCase().includes("stored") ||
  result.assistantText.toLowerCase().includes("recorded");
expect(confirmsAction).toBe(true);
```

Guidelines:
- Always call `.toLowerCase()` once into a `const text` variable for readability when doing multiple checks
- Include 3-5 synonyms per concept — enough for resilience, not so many that any output passes
- Name the boolean variable descriptively (`confirmsCreation`, `showsConflict`, `mentionsDeletion`)

#### 1b. `assertOutputContains()` for Mandatory Keywords

Use when specific domain terms MUST appear (not stylistic choices):

```typescript
assertOutputContains(
  result.assistantText,
  ["security", "log"],
  "J3: Filtered results show security memory"
);
```

This is stricter than OR-keyword lists. Use for fixture-seeded content that the agent must reference.

#### 1c. Regex for Structural Checks

Use when verifying format, not content:

```typescript
const hasStructuredFormat =
  /##\s*(core|learning|redflag|goal|idea)/i.test(result.assistantText) ||
  /\|.*\|.*\|/.test(result.assistantText) ||
  /`(core|learning|redflag)`/.test(result.assistantText);
```

Reserve regex for:
- Section headings (`## Promotions`, `## Conflicts`)
- Table formatting (`|...|...|`)
- Numbered lists (`/^\d+\.\s/m`)
- Type labels in brackets (`[learning]`, `[redflag]`)

#### 1d. Tool-Call Structural Checks

Use `hasSubagentCall()` to verify delegation occurred:

```typescript
const usedMemoryManager = hasSubagentCall(result.toolCalls, "crux-cursor-memory-manager");
expect(usedMemoryManager).toBe(true);
```

For `Task` tool calls (Meditate recursive spawning):

```typescript
const taskCalls = result.toolCalls.filter((tc) => tc.name === "Task");
expect(taskCalls.length).toBeGreaterThanOrEqual(1);
```

For file operations:

```typescript
const wroteFile = result.toolCalls.some(
  (tc) => tc.name === "write" || tc.name === "edit"
);
```

#### 1e. File-System Ground Truth Assertions

The strongest assertions — verify side effects on disk. Use `fs` directly (not agent output):

```typescript
// File created
expect(fs.existsSync(expectedPath)).toBe(true);

// File deleted
expect(fs.existsSync(memoryPath)).toBe(false);

// File moved (promotion)
expect(fs.existsSync(oldPath)).toBe(false);
expect(fs.existsSync(newPath)).toBe(true);

// Frontmatter field check
const content = fs.readFileSync(filePath, "utf-8");
expect(content).toContain('type: "learning"');

// File count delta
const afterFiles = listMemoryFiles(ws.root);
const newFiles = afterFiles.filter((f) => !beforeFiles.includes(f));
expect(newFiles.length).toBeGreaterThanOrEqual(1);

// Index rebuilt
const indexContent = readMemoryIndex(ws.root);
expect(indexContent).toContain(expectedSlug);
```

#### 1f. Assertion Layering Strategy

Each test SHOULD layer assertions from weakest to strongest:

1. `result.status === "finished"` — agent didn't crash
2. OR-keyword list OR `assertOutputContains()` — agent described what it did
3. Tool-call check — agent used expected tools/subagents
4. File-system ground truth — side effects are correct

Not every test needs all four layers. Use judgment:
- Output-only tests (Recall display): layers 1-2
- Side-effect tests (Remember creation, Forget deletion): layers 1-2-4
- Delegation tests (Dream, Meditate): layers 1-2-3
- Full-flow tests (Integration): all four layers

---

### 2. Fixture Strategy

#### 2a. Spec Fixtures for Dream (B)

`beforeAll` must create a mock completed spec directory:

```
specs/sdk-test-dream-spec/
  _execution-state.yml       # status: complete, subtasks: [{id: 01, status: complete}, ...]
  subtask-01-*.md             # Contains Execution Notes with learnings
  subtask-02-*.md             # Contains Execution Notes with a conflicting insight (for B3)
```

Helper needed (subtask-02 to build): `createSpecFixture(ws.root, specName, subtasks)` — writes the directory tree above. Each subtask should have realistic execution notes containing extractable facts.

For B3 (conflict detection), also create a memory that contradicts what the spec subtask notes would yield:

```typescript
createMemoryFixture({
  slug: "sdk-test-dream-conflict",
  type: "learning",
  title: "Always use write-through caching for user sessions",
  description: "Write-through ensures consistency",
  tags: ["caching", "sessions"],
  body: "Write-through is the only safe approach.",
  strength: 3,
}, ws.root);
```

The spec subtask notes should recommend the opposite (e.g., cache-aside).

#### 2b. Aged Memories for REM (C)

`beforeAll` must create memories with backdated timestamps:

| Fixture | Purpose | Key fields |
|---------|---------|------------|
| `sdk-test-rem-promote` | Triggers promotion | `type: "idea"`, `strength: 6` (above `promoteAt` for idea, default 5) |
| `sdk-test-rem-demote` | Triggers demotion | `modified: "2025-12-01"` (>90 days ago), no recent tracker |
| `sdk-test-rem-archive` | Triggers archival | `modified: "2025-08-01"` (>180 days ago) |
| `sdk-test-rem-normal` | Control — not flagged | `type: "core"`, `strength: 2`, recent `modified` |

Harness enhancement needed (subtask-02): extend `createMemoryFixture()` to accept `created` and `modified` date overrides instead of always using today.

#### 2c. Orphaned Trackers for REM Cleanup (C2)

Create a `.refs.yml` file with no matching memory:

```typescript
const orphanPath = path.join(ws.root, ".crux/reference-tracking/sdk-test-nonexistent.refs.yml");
fs.writeFileSync(orphanPath, `memory_slug: sdk-test-nonexistent\nlast_referenced: 2026-01-01\ncount: 3\n`);
```

After REM with `--yolo`, assert `fs.existsSync(orphanPath) === false`.

#### 2d. Conflicting Memories for REM Conflict (C3)

Create two memories with contradictory bodies:

```typescript
createMemoryFixture({
  slug: "sdk-test-rem-conflict-a",
  type: "learning",
  title: "Prefer SQL JOINs for related data",
  tags: ["sql", "performance"],
  body: "Always use SQL JOINs over multiple queries.",
}, ws.root);

createMemoryFixture({
  slug: "sdk-test-rem-conflict-b",
  type: "learning",
  title: "Avoid SQL JOINs for large tables",
  tags: ["sql", "performance"],
  body: "Use application-level joins for better cache utilization.",
}, ws.root);
```

#### 2e. Standard Memory Fixtures for Forget (R) and Meditate (Q)

Forget needs 3-5 memories with varied types and tags:

| Fixture | Type | Tags | Purpose |
|---------|------|------|---------|
| `sdk-test-forget-target` | `learning` | `[testing, validation]` | Will be deleted in R1 |
| `sdk-test-forget-keep` | `core` | `[architecture]` | Must survive deletion |
| `sdk-test-forget-search-a` | `learning` | `[performance, caching]` | Matches search in R2 |
| `sdk-test-forget-search-b` | `redflag` | `[performance, logging]` | Also matches search in R2 |

Forget tests must also create a matching tracker for the target memory at `.crux/reference-tracking/sdk-test-forget-target.refs.yml` to verify tracker cleanup.

Meditate needs 5-10 memories across varied domains and types (same set as Recall fixtures, plus a few more to provide enough density for recursive exploration).

---

### 3. Timeout Budget Table

Based on observed patterns: each `agent.send()` + `collectRun()` cycle takes 60-120s for simple commands, 120-180s for complex multi-tool flows.

| Test File | Default Timeout | Per-Test Override | Rationale |
|-----------|----------------|-------------------|-----------|
| `j-recall.test.ts` | 240s (vitest default) | — | Existing, single-turn commands |
| `o-remember.test.ts` | 240s (vitest default) | 300s for index rebuild test | Existing, some tests trigger writes + index |
| `p-amnesia.test.ts` | 240s (vitest default) | 300s for multi-turn tests | Existing, multi-turn on/off sequences |
| `b-dream.test.ts` | 240s (vitest default) | **300s per test** | Multi-step agent flow with spec reading, diff, candidate extraction |
| `c-rem.test.ts` | 240s (vitest default) | **300s per test** | Multi-step analysis, file moves, index rebuild |
| `r-forget.test.ts` | 240s (vitest default) | **300s per test** | Confirmation + deletion + tracker cleanup + index |
| `q-meditate.test.ts` | 240s (vitest default) | **480s per test** | 3-level recursive subagent spawning |
| `n-integration.test.ts` | 240s (vitest default) | **600s for the describe block** | 5-6 sequential agent turns |

Implementation: use vitest's per-test timeout option:

```typescript
it("extracts candidate facts from spec", { timeout: 300_000 }, async () => { ... });
```

For the integration describe block, use vitest's `describe.sequential()` and set the timeout at the describe level or on the final cumulative test.

Q and N tests are gated behind `SDK_EVAL_SKIP_EXPENSIVE`:

```typescript
const describeExpensive = process.env.SDK_EVAL_SKIP_EXPENSIVE === "false"
  ? describe
  : describe.skip;
```

This pattern is already established in `vitest.setup.ts` messaging.

---

### 4. Parallelization Confirmation

**Finding**: Per-file worktree isolation via `createIsolatedWorkspace()` IS sufficient for safe multi-fork execution.

Evidence:
- Each call creates a unique git worktree at `/tmp/sdk-eval-<timestamp>-<counter>` with a unique branch name `tmp/sdk-eval-<timestamp>-<counter>`
- The counter is process-scoped (`let worktreeCounter = 0` in `harness.ts`), BUT the `Date.now()` component ensures cross-process uniqueness
- Each worktree gets its own `memories/` directory tree and `.crux/` config — no shared mutable state between forks
- The vitest config uses `pool: "forks"` with `maxForks: 2` — each fork is a separate Node process

**Risk mitigation**:
- The `worktreeCounter` is per-process, so two forks starting simultaneously could get the same counter value. The `Date.now()` millisecond timestamp makes collision extremely unlikely, but for added safety, subtask-02 should add `process.pid` to the worktree name template: `/tmp/sdk-eval-<pid>-<timestamp>-<counter>`
- Git worktree operations (`git worktree add`, `git worktree remove`) acquire a repo-level lock file. If two forks try to create worktrees simultaneously, one will block briefly on the lock. This is safe — git handles the concurrency correctly.
- Cleanup in `afterAll` is best-effort (try/catch around remove). Orphaned worktrees in `/tmp/` will be cleaned by OS tmpdir policy.

**Recommendation**: Keep `maxForks: 2` for the current suite size (7-9 test files). Increasing to 3-4 would reduce wall-clock time but risks API rate limiting. Subtask-03 (vitest parallelization) should validate the optimal fork count empirically.

**N-file serialization**: `n-integration.test.ts` tests are inherently sequential (each turn depends on the previous). Use `describe.sequential()` — vitest will run them in order within a single fork. This file can still run in parallel with other test files.

---

### 5. Test Count Projection

#### B: Dream Tests (~8 tests)

**B1: Dream No Args — List Unprocessed Specs (2 tests)**
| Test | Assertions | Turns |
|------|-----------|-------|
| B1.1: Spawns memory manager, lists unprocessed specs | `hasSubagentCall()`, output contains numbered list | 1 |
| B1.2: Already-dreamed specs excluded from list | Create spec with existing `dream-*.md`, verify excluded | 1 |

**B2: Dream Full Flow (3 tests)**

*Correctness trade-off decision*: Use **single agent turn with batched assertions**. Rationale:
- Multi-turn isolation testing (one turn per step) costs 6x the wall-clock time (~600s vs ~100s)
- SDK `agent.send()` is single-turn — the agent will execute the full dream pipeline in one response
- Batched assertions identify which step's output was missing via descriptive error messages

| Test | Assertions | Turns |
|------|-----------|-------|
| B2.1: Execution verification + diff analysis in output | `assertOutputContains(["verified", "execution"])`, output mentions change count | 1 |
| B2.2: Candidate facts presented with type labels | Regex for `[learning]` or `[redflag]` etc., output contains ranked candidates | 1 |
| B2.3: Memory files created + dream summary written + index rebuilt | File-system ground truth: `memories/` has new files, `specs/*/dream-*.md` exists, index updated | 1 |

**B3: Dream Conflict Detection (2-3 tests)**
| Test | Assertions | Turns |
|------|-----------|-------|
| B3.1: Conflict detected and both sides presented | Output mentions "conflict", contains both memory titles | 1 |
| B3.2: Resolution options offered (keep/replace/merge) | OR-keyword check for resolution language | 1 |
| B3.3 (optional): Non-conflicting candidates presented normally alongside conflict | Output has both conflict section and normal candidates | Covered by B3.1-2 |

Consolidation rationale: B3.3 can be folded into B3.1's assertions to save one agent turn.

#### C: REM Sleep Tests (~8 tests)

**C1: REM Interactive Recommendations (3 tests)**
| Test | Assertions | Turns |
|------|-----------|-------|
| C1.1: Structured report with promotions section | Output contains promotion language, references `sdk-test-rem-promote` | 1 |
| C1.2: Demotions and archival sections present | Output mentions demotion/archival for aged memories | 1 |
| C1.3: Asks for confirmation before applying | OR-keyword: "confirm", "approve", "apply", "proceed" | Batched with C1.2 |

Consolidation: C1.2 and C1.3 share a single agent turn — both check different parts of the same REM output.

**C2: REM --yolo Auto-Apply (3 tests)**
| Test | Assertions | Turns |
|------|-----------|-------|
| C2.1: Non-conflict changes auto-applied (promotion file moved) | File-system: old path gone, new path exists, frontmatter updated | 1 |
| C2.2: Orphaned tracker cleaned up | File-system: orphan `.refs.yml` deleted | Batched with C2.1 |
| C2.3: Index rebuilt after changes | `readMemoryIndex()` reflects new state | Batched with C2.1 |

Consolidation: C2.1-C2.3 are all side effects of a single `--rem --yolo` agent turn. Use one `it()` test with multiple `expect()` calls, OR three tests sharing the same pre-computed `result` via a closure variable.

Recommendation: **Three separate `it()` blocks sharing a single `beforeAll` that runs the `--rem --yolo` agent turn.** This gives clear per-assertion failure reporting without re-running the agent.

**C3: REM Conflict Handling (2 tests)**
| Test | Assertions | Turns |
|------|-----------|-------|
| C3.1: Conflicts detected and presented separately | Output separates "auto-applied" from "conflicts" | 1 |
| C3.2: Conflicts not auto-resolved — agent asks for input | OR-keyword: "resolve", "choose", "keep", "which" | Batched with C3.1 |

#### R: Forget Tests (~6 tests)

**R1: Forget By ID (3-4 tests)**

*Forget confirmation decision*: With SDK single-turn, the agent will treat `/crux-forget` as user intent and complete the full flow. Assert BOTH that the output contains confirmation language AND that the file is deleted.

| Test | Assertions | Turns |
|------|-----------|-------|
| R1.1: Shows memory details in output before deletion | `assertOutputContains()` for memory title, type | 1 |
| R1.2: Memory file deleted from disk | `fs.existsSync(memoryPath) === false` | Batched with R1.1 |
| R1.3: Tracker file deleted | `fs.existsSync(trackerPath) === false` | Batched with R1.1 |
| R1.4: Index rebuilt without deleted memory | `readMemoryIndex()` does not contain slug | Batched with R1.1 |

Consolidation: R1.1-R1.4 can share a single agent turn. Use separate `it()` blocks with shared result, or one test with four assertion groups.

**R2: Forget Search and Select (2-3 tests)**
| Test | Assertions | Turns |
|------|-----------|-------|
| R2.1: Search returns matching memories | Output contains fixture titles matching query | 1 |
| R2.2: Only selected memories deleted, others survive | File-system: target gone, `sdk-test-forget-keep` still exists | 1 |

#### Q: Meditate Tests (~6 tests)

All gated behind `SDK_EVAL_SKIP_EXPENSIVE`.

**Q1: Meditate No Args (3 tests)**

*Meditate depth verification decision*: Check for `Task` tool calls (proving subagent spawning occurred) AND verify final output references memories. Do NOT trace the full 3-level recursion tree — it is fragile and the tool-call log may not surface nested subagent internals clearly.

| Test | Assertions | Turns |
|------|-----------|-------|
| Q1.1: Spawns memory manager, derives 3 facets | `hasSubagentCall()`, output mentions "facet" or lists 3 themes | 1 |
| Q1.2: Recursive exploration spawns `Task` calls | `taskCalls.length >= 1` (may not see all 9 nested agents, but should see L1 spawning) | Batched with Q1.1 |
| Q1.3: Consolidated insights reference memories | Output mentions at least one fixture memory title/slug | Batched with Q1.1 |

**Q2: Meditate Topic Argument (2 tests)**
| Test | Assertions | Turns |
|------|-----------|-------|
| Q2.1: Topic-driven facets relate to provided topic | Output facets mention the topic keywords | 1 |
| Q2.2: Completion without crash + insights produced | `result.status === "finished"`, output length > minimum threshold | Batched with Q2.1 |

**Q3: Meditate File/Folder Reference (1-2 tests)**
| Test | Assertions | Turns |
|------|-----------|-------|
| Q3.1: Code references produce relevant facets, session ends cleanly | `result.status === "finished"`, output references code domain | 1 |

#### N: Integration Tests (~4 tests)

All gated behind `SDK_EVAL_SKIP_EXPENSIVE`. Sequential turns within a single describe block.

*Turn budget decision*: Maximum 6 turns. 600s total. Each turn averages 60-90s.

| Test | Turn | Command | Key Assertions |
|------|------|---------|---------------|
| N1.1: Dream flow | 1 | `/crux-dream sdk-test-spec` | Memory files created, dream summary written |
| N1.2: Recall finds dreamed memories | 2 | `/crux-recall` | Output references memories from N1.1 |
| N1.3: Remember adds ad-hoc memory | 3 | `/crux-remember "integration test insight" --type idea` | New file in `memories/idea/` |
| N1.4: Forget removes a memory | 4 | `/crux-forget <slug>` | File deleted, index updated |

Optional turns 5-6 (Amnesia on/off) can be consolidated into N1.4 assertions or added if budget permits:

| N1.5: Amnesia on | 5 | `/crux-amnesia on` | Confirms enabled |
| N1.6: Amnesia off + verify | 6 | `/crux-amnesia off` then task | Memories surface again |

Implementation: use a **shared agent instance** across all N1 tests (do NOT dispose between turns). Use `describe.sequential()` to ensure order.

```typescript
describeExpensive("N: Integration", () => {
  let ws: IsolatedWorkspace;
  let agent: Agent;

  beforeAll(async () => { ws = createIsolatedWorkspace(); /* seed fixtures */ });
  afterAll(async () => { agent?.[Symbol.asyncDispose](); ws.cleanup(); });

  it("N1.1: Dream creates memories", { timeout: 180_000 }, async () => {
    agent = Agent.create({ ... });
    const run = await sendWithRetry(agent, "/crux-dream sdk-test-spec");
    // ...
  });

  it("N1.2: Recall finds dreamed memories", { timeout: 120_000 }, async () => {
    const run = await sendWithRetry(agent, "/crux-recall");
    // agent is reused from N1.1
  });
  // ...
});
```

---

### 6. Correctness Trade-Off Decisions (Summary)

| Question | Decision | Rationale |
|----------|----------|-----------|
| B2 single vs multi-turn | **Single turn, batched assertions** | 6x faster; SDK is single-turn by design; descriptive error messages identify which step failed |
| Meditate depth verification | **Check `Task` tool calls + output references memories** | Full recursion tracing is fragile; tool-call presence proves delegation occurred |
| REM C2 verification | **Sample-based: ≥1 promotion file moved + ≥1 orphan deleted** | Deterministic fixtures make sampling sufficient; exhaustive checking is brittle |
| Forget R1 confirmation | **Check output for confirm+deleted language + file-system ground truth** | SDK single-turn means agent completes full flow; both output and disk state must be correct |
| N1 turn budget | **Max 6 turns, 600s total, shared agent** | Each turn ~90s average; 6 turns covers Dream→Recall→Remember→Forget→Amnesia on→off |
| Q/N expensive gating | **`SDK_EVAL_SKIP_EXPENSIVE` env var (default: skip)** | Already established in `vitest.setup.ts`; prevents CI cost blowout |

---

### 7. Shared Patterns & Conventions

#### File naming
All test files follow the existing `<letter>-<name>.test.ts` convention:
- `b-dream.test.ts`
- `c-rem.test.ts`
- `r-forget.test.ts`
- `q-meditate.test.ts`
- `n-integration.test.ts`

#### Describe block structure
```
describe("<Letter>: <Name>", () => {
  // ws, agent declarations
  // beforeAll: workspace + fixtures
  // afterAll: cleanup
  // afterEach: agent dispose

  describe("<Letter><Number>: <Scenario Name>", () => {
    it("<description>", { timeout: N }, async () => { ... });
  });
});
```

#### Agent creation (copy-paste template)
```typescript
agent = Agent.create({
  apiKey: getApiKey(),
  model: { id: "composer-2" },
  local: { cwd: ws.root },
});
```

#### Rate limiting
Always use `sendWithRetry()` for agent turns in expensive tests (Q, N). For cheap tests (B, C, R), direct `agent.send()` is acceptable since `withRetry()` adds complexity. If rate limits become a problem in CI, retrofit.

#### Imports
Every test file imports from `../helpers/harness.js` and `../helpers/config.js`. No test file should import from `node:child_process` directly — all subprocess calls go through harness helpers.

---

## Adversarial Verification

**Verifier**: zoto-spec-judge
**Verified**: 2026-04-26T12:22+10:00

### Deliverables Checklist Verification

| Item | Verdict | Evidence |
|------|---------|----------|
| Assertion pattern guide | **Confirmed** | Sections 1a–1f cover all four required patterns (OR-keyword, regex, tool-call, file-system) plus layering strategy. Code examples are copy-paste ready. |
| Fixture strategy | **Confirmed** | Sections 2a–2e document fixture shapes for all 5 test files (Dream, REM, Forget, Meditate, Integration). Data shapes are specific with field-level detail. |
| Timeout budget table | **Confirmed** | Section 3 has per-file table with 8 rows. Default 240s matches `vitest.config.ts` (verified: `testTimeout: 240_000`). Per-test overrides include rationale. `SDK_EVAL_SKIP_EXPENSIVE` gating confirmed in `vitest.setup.ts` lines 59-64. |
| Parallelization confirmation | **Confirmed** | Section 4 confirms worktree isolation is sufficient. Claims verified: `Date.now()` + counter uniqueness in `harness.ts` line 61, `pool: "forks"` + `maxForks: 2` in `vitest.config.ts` lines 8-12. Risk mitigation (PID addition) is actionable. |
| Test count projection | **Confirmed** | Section 5 projects ~32 tests across 5 files (B:8, C:8, R:6, Q:6, N:4). Each test has ID, assertion types, turn count, and consolidation rationale. |

### Definition of Done Verification

| Item | Verdict | Evidence |
|------|---------|----------|
| Architecture decisions documented | **Confirmed** | 7 sections totalling ~470 lines of architecture content in Execution Notes. |
| No code changes | **Confirmed** | `git status` shows `harness.ts` modified, but this is attributable to subtask-02 (whose Files Modified section explicitly claims it). Subtask-01's "Files Modified: None" is accurate. |
| Decisions actionable | **Confirmed** | Provides copy-paste code templates, file naming conventions, describe block structure, agent creation template, specific test IDs with assertion types, import conventions, and rate limiting guidance. A software engineer can implement without ambiguity. |

### Verdict: **Verified**

All 5 Deliverables Checklist items and all 3 Definition of Done items independently confirmed. No items unticked or flagged.
