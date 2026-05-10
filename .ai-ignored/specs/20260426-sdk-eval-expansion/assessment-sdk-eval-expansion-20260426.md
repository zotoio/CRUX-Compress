# Assessment: SDK Eval Suite Expansion

**Spec**: `specs/20260426-sdk-eval-expansion/`
**Assessed**: 2026-04-26
**Verdict**: **Conditional** (3.7 / 5.0) — Address findings before execution

---

## Scoring Summary

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 4.0 | Good coverage; two checklist gaps noted |
| Feasibility | 3.5 | Most deliverables achievable; Dream/REM SDK testability is the primary risk |
| Structure | 4.5 | Clean phasing, correct dependencies, consistent formatting |
| Specificity | 4.0 | Implementation notes are detailed with code examples; a few areas underspecified |
| Risk Awareness | 3.0 | Key risk (interactive confirmation in single-turn SDK) identified but not fully mitigated; cost risk unaddressed |
| Convention Compliance | 3.5 | Follows existing patterns well; one config inconsistency and one naming convention gap |
| **Overall** | **3.7** | |

---

## 1. Spec Structure and Completeness

### Strengths

- **Authoritative source alignment**: The spec explicitly traces each test file back to `USER_EVAL_CHECKLISTS.md` categories (B, C, J, O, P, Q, R, N1). This is exemplary traceability.
- **Clear phasing**: 4 phases with a clean dependency graph — design first, implementation second, integration third, validation fourth.
- **Key decisions documented**: 9 decisions covering fixture strategy, simplification trade-offs, parallelization, and timeout budgets. These preempt common questions.
- **Mermaid dependency graph**: Visual dependency graph in the index is well-formed and matches the manifest table.

### Findings

**F1 — N2 and N3 checklist scenarios excluded without rationale (Medium)**
The spec index states it covers "N1" from cross-platform, but `USER_EVAL_CHECKLISTS.md` also defines N2 (Claude Code wiring verification) and N3 (Generic platform shell script verification). The spec overview says it covers features "that rely on LLM agent interaction," which is a reasonable exclusion criterion for N2/N3 (they are structural/file-verification checks, not agent-behavioral tests). However, this exclusion is not explicitly stated. The Definition of Done references "B, C, Q, R, N1" which is correct, but the Requirements section (item 1) says "categories B, C, J, O, P, Q, R, N1" — the inclusion of J, O, P here is slightly confusing since they already exist.

**Recommendation**: Add a one-line note in the Overview or Key Decisions explaining why N2 and N3 are excluded (they don't require LLM interaction). Clarify that J, O, P already have tests and are only referenced in the context of regression.

**F2 — Test count projections are vague (Low)**
The spec says "~60 tests" but the per-file estimates in subtasks sum to approximately: 10 (J, existing) + 7 (O, existing) + 8 (P, existing) + 8 (B) + 8 (C) + 6 (R) + 6 (Q) + 4 (N) = 57. The ~60 figure is reasonable but the existing J/O/P counts are taken from the current implementation rather than the subtask estimates. Subtask 01 is supposed to produce a "test count projection" deliverable — this creates a dependency that subtask 01 should confirm the final counts, but subtasks 04-07 already have hardcoded minimums.

**Recommendation**: Reconcile counts or note that the subtask minimums are floors and final counts come from subtask 01.

---

## 2. Subtask Granularity and Dependency Correctness

### Strengths

- **Dependency graph is acyclic and correct**: Phase 2 subtasks (04-07) depend on both 01 (architecture) and 02 (harness), which is correct — they need the design guide and the fixture helpers. Phase 3 (08) depends on 02 and all Phase 2 subtasks. Phase 4 (09) depends on everything. No circular dependencies.
- **Phase 1 is fully parallel**: Subtasks 01, 02, 03 have no interdependencies, enabling three parallel agents.
- **Phase 2 is fully parallel**: Subtasks 04-07 are independent of each other, enabling four parallel agents.
- **Agent assignments follow AGENTS.md**: Architecture goes to `crux-platform-architect`, all implementation to `crux-software-engineer`.

### Findings

**F3 — Subtask 01 is a design-only subtask that produces no artifacts beyond execution notes (Low)**
Subtask 01 outputs its design guidance as free-text in the "Execution Notes" section. Phase 2 subtasks depend on subtask 01, but the implementation notes in subtasks 04-07 already contain detailed assertion patterns, fixture setup, and test structure. In practice, the Phase 2 engineer agents will read their own subtask file, not subtask 01's execution notes.

**Impact**: Low. Subtask 01's value is in validating that the spec author's design decisions hold up under scrutiny. The hardcoded guidance in subtasks 04-07 reduces the risk of subtask 01 being a bottleneck, but it also means subtask 01's output may conflict with or duplicate the already-embedded guidance.

**Recommendation**: Either (a) make subtask 01 produce a separate `ARCHITECTURE.md` file in the spec directory that subtasks 04-07 explicitly reference, or (b) accept that subtask 01 is a review/validation step and adjust its description accordingly.

**F4 — Subtask 03 (vitest parallelization) has no downstream dependency from Phase 2 (Correct but notable)**
Subtask 03 only feeds into subtask 09 (validation). Phase 2 subtasks don't depend on 03 — this is correct because the new test files don't need parallel config to be written. However, this means 03 could be deferred to Phase 3 or even Phase 4 without affecting the dependency graph.

**Impact**: None — the current placement is valid and running it in Phase 1 is efficient.

**F5 — Subtask 08 (integration) dependency on 01 is missing (Low)**
Subtask 08's dependency list is `02, 04, 05, 06, 07`. It does not depend on 01 (architecture). Since 04-07 all depend on 01, subtask 01 is transitively required — but the explicit declaration is missing from the manifest table.

**Recommendation**: Add 01 to subtask 08's dependency list for completeness, or note that transitive dependencies are implicit.

---

## 3. Feasibility of Deliverables

### Subtask 01 — Test Architecture (Feasible)
Design-only subtask, no code changes. Low risk. The architect reviews existing code and documents patterns. The five deliverables (assertion guide, fixture strategy, timeout budget, parallelization confirmation, test count projection) are all achievable in a single agent session.

### Subtask 02 — Harness Enhancements (Feasible)
The 10 new helpers are well-specified with clear signatures, return types, and format examples. The existing `createMemoryFixture()` and `createIsolatedWorkspace()` provide strong patterns to follow.

**F6 — `createSpecFixture()` requires knowledge of realistic spec content (Medium)**
The subtask specifies creating mock subtask files with "execution notes, work logs, and files-modified sections." The Dream command's agent will parse these for candidate fact extraction. If the mock content is too synthetic (e.g., placeholder text), the LLM agent may not generate meaningful candidate facts during Dream tests, causing B2 tests to fail.

**Recommendation**: Provide example content in the subtask's implementation notes — realistic execution notes that would naturally produce extractable learnings, redflags, or ideas.

### Subtask 03 — Vitest Parallelization (Feasible)
Simple config change (`singleFork: true` → `maxForks: 4`) and adding npm scripts. Low risk.

**F7 — `maxForks: 4` may exhaust system resources with 4 concurrent agent SDK sessions (Medium)**
Each fork runs an isolated worktree AND a live SDK agent session that connects to the Cursor API. Four concurrent long-running agent sessions may hit API rate limits or exhaust local memory (each agent process includes the February SDK runtime). The spec acknowledges this is the plan but doesn't discuss rate-limit or resource mitigation.

**Recommendation**: Add a note that `maxForks` may need to be reduced to 2-3 if rate limiting or resource exhaustion is observed during subtask 09 validation. Consider documenting the `CURSOR_API_KEY` rate limit.

### Subtask 04 — Dream Tests (Feasible with caveats)

**F8 — Dream B2 "full flow" assumes the agent completes all steps in a single turn (High)**
The B2 checklist in `USER_EVAL_CHECKLISTS.md` describes a 9-step interactive flow: execution verification → diff analysis → candidate presentation → user acceptance → memory creation → dream summary → archival offer. The spec acknowledges this but recommends a single-turn approach with batched assertions.

The critical issue: the Dream command is inherently interactive — it asks the user to accept/reject candidate facts (step 6 in the checklist). With `agent.send()`, there's no follow-up turn to respond. The agent may:
1. Auto-accept all candidates (most likely with a direct command) — tests pass but don't verify the acceptance flow
2. Present candidates and stop, waiting for input — memory creation and summary writing don't happen
3. Treat the `/crux-dream <spec>` command as implicit acceptance — varies by agent behavior

This is the single biggest feasibility risk in the spec.

**Recommendation**: Add explicit guidance for handling the acceptance step. Options:
- Include acceptance intent in the prompt: `/crux-dream 20260420-test-feature — accept all candidates`
- Use a two-turn approach: first turn to get candidates, second turn to accept
- Accept that the agent may auto-accept and focus assertions on candidate extraction rather than the accept/reject flow

### Subtask 05 — REM Sleep Tests (Feasible with caveats)
Similar interactive-flow concerns as Dream. REM in non-yolo mode asks for user confirmation before applying changes.

**F9 — C1 "asks for confirmation" test may be unreliable (Medium)**
The test asserts the output contains confirmation language and that no file modifications occur. However, with a single-turn SDK send, the agent may present recommendations and auto-apply in one turn, or present and wait. The test's ground-truth check (no file modifications) may fail if the agent interprets the command as "analyze and apply."

**Recommendation**: C1 tests should focus on the report structure (sections present, candidates identified) rather than confirmation-gating behavior. Move confirmation-gating verification to C2 (where `--yolo` explicitly controls the behavior) as a contrast test.

### Subtask 06 — Forget Tests (Feasible)
The subtask already identifies the SDK single-turn limitation (see "Important: Agent Behavior with SDK" section) and recommends focusing on ground-truth assertions. This is well-handled.

### Subtask 07 — Meditate Tests (Feasible with cost concern)

**F10 — Meditate tests are extremely expensive and may be cost-prohibitive (High)**
Each Meditate test spawns 3 Level 1 agents, each spawning Level 2, each spawning Level 3 — up to 13 agents per test. With 6 tests at 480s timeout each, this is potentially 78 agent invocations across 48 minutes of wall-clock time. At SDK pricing, this could be the most expensive part of the entire suite.

The spec acknowledges Meditate is the "most expensive test file" and "wall-clock bottleneck," but doesn't quantify the API cost or suggest a cost-control mechanism (e.g., a `SKIP_EXPENSIVE` env variable, or reducing to 2-3 Meditate tests).

**Recommendation**: Add a `SKIP_MEDITATE` or `SDK_EVAL_SKIP_EXPENSIVE` environment variable that skips Meditate tests in routine CI. Reserve Meditate tests for explicit invocation via `pnpm test:meditate`.

### Subtask 08 — Integration Test (Feasible)
Well-designed sequential multi-turn test. The flow (Dream → Recall → Remember → Forget → Amnesia) is logical and each turn builds on prior state. 600s budget is reasonable for 5 turns.

**F11 — Integration test depends on Dream completing successfully, creating a cascading failure risk (Low)**
If Dream fails in turn 1 (the biggest risk per F8), subsequent turns that reference dreamed memories will also fail. The subtask handles this by tracking memory counts (`initialMemoryCount`, `afterRememberCount`) rather than referencing specific memories, which is a good mitigation.

### Subtask 09 — Validation & Profiling (Feasible)
Runs the full suite and documents results. Depends on all prior subtasks. The troubleshooting guide is a nice touch.

---

## 4. Risk Assessment

### High Risks

| Risk | Likelihood | Impact | Mitigation in Spec? |
|------|-----------|--------|---------------------|
| Dream/REM interactive flow doesn't complete in single SDK turn (F8, F9) | High | High — multiple tests fail | Partial — noted but not fully mitigated |
| Meditate test cost and duration blow budget (F10) | Medium | High — blocks validation, high API spend | Partial — acknowledged as bottleneck, no skip mechanism |
| API rate limiting with 4 concurrent agent sessions (F7) | Medium | Medium — tests timeout or fail intermittently | Not addressed |

### Medium Risks

| Risk | Likelihood | Impact | Mitigation in Spec? |
|------|-----------|--------|---------------------|
| Synthetic spec fixtures produce poor Dream candidates (F6) | Medium | Medium — B2 tests fail to extract facts | Not addressed |
| Non-deterministic agent output causes flaky assertions | Medium | Low — spec uses OR-patterns extensively | Well-mitigated |
| Worktree cleanup failures leave orphaned branches | Low | Low — spec uses `/tmp/` and force cleanup | Mitigated in existing harness |

### Low Risks

| Risk | Likelihood | Impact | Mitigation in Spec? |
|------|-----------|--------|---------------------|
| Existing J/O/P tests break under new fork config | Low | Medium | Subtask 03 includes regression check |
| Cross-file state leakage | Low | Medium | Each file creates isolated worktree |

---

## 5. Dimension Analysis

### Completeness (4.0)

The spec covers all five new checklist categories (B, C, Q, R, N1) with appropriate test counts per scenario. Every checklist scenario maps to at least one test. The only gap is the lack of explicit exclusion rationale for N2/N3 (F1), and the slight ambiguity around whether existing J/O/P tests are being modified or just validated for regression.

### Feasibility (3.5)

Most subtasks are straightforward extensions of the existing test infrastructure. The primary feasibility concerns are:
1. Interactive command flows (Dream, REM non-yolo) may not complete as expected in single-turn SDK sends (F8, F9)
2. Meditate's recursive subagent spawning makes tests expensive and slow (F10)
3. The harness helpers are well-specified and implementable

### Structure (4.5)

Excellent structure. The spec follows a clear template:
- Index with overview, decisions, requirements, manifest, dependency graph, execution order
- Each subtask has metadata, objective, deliverables checklist, definition of done, implementation notes, testing strategy, execution notes
- Phases are logically ordered with correct dependencies
- Consistent naming conventions (`subtask-XX-sdk-eval-<feature>-20260426.md`)

One minor issue: the dependency graph edges from B→H include a redundant B→H edge (02 already feeds into 08, and 02 is already shown), but this is cosmetically correct and doesn't cause issues.

### Specificity (4.0)

Implementation notes include TypeScript code examples for assertion patterns, fixture formats, and expected test structure. Each subtask specifies exact file names, function signatures, and timeout values. The level of detail is sufficient for a `crux-software-engineer` agent to implement without ambiguity in most cases.

Gaps:
- `createSpecFixture()` doesn't specify realistic execution note content (F6)
- No guidance on handling the acceptance step in Dream tests (F8)

### Risk Awareness (3.0)

The spec addresses some risks well (non-deterministic output via OR-patterns, worktree isolation for parallel safety, timeout budgets per test type). However, it under-addresses:
- The fundamental SDK-vs-interactive-flow tension for Dream and REM (F8, F9)
- API cost and rate limiting for expensive Meditate tests (F10, F7)
- No env-variable-based skip mechanism for expensive tests

### Convention Compliance (3.5)

The spec follows existing test file conventions closely — same import patterns, same harness usage, same `describe`/`it` nesting structure. Agent assignments follow `AGENTS.md`.

One issue: **the existing `package.json` uses `pnpm` as the package manager** (declared in `packageManager` field), but the user's rules state "always use yarn instead of npm." The spec and existing project both use `pnpm`, and the spec correctly references `pnpm test`, `pnpm test:dream`, etc. This is consistent with the codebase but contradicts the user rule. The spec should follow the existing project convention (pnpm) since changing package managers mid-project would be disruptive.

---

## 6. Recommendations

### Must-Fix Before Execution

1. **~~Address Dream/REM single-turn acceptance flow (F8, F9)~~** ✅ ADDRESSED: Subtasks 04 and 05 updated with "SDK Single-Turn Non-Interactive Strategy" sections. Decision 11 in spec index strengthened. All prompts must be fully non-interactive directives embedding acceptance intent.

2. **~~Add cost-control mechanism for Meditate tests (F10)~~** ✅ ADDRESSED: `SDK_EVAL_SKIP_EXPENSIVE` defaults to `true` (skip). Subtasks 07 and 08 updated with `process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false"` check. `.env.example` and README document the default. `pnpm test:meditate` and `pnpm test:integration` scripts explicitly set `SDK_EVAL_SKIP_EXPENSIVE=false`.

### Should-Fix

3. **~~Provide realistic spec fixture content (F6)~~** ✅ ADDRESSED: Already present in subtask 02's "Realistic Spec Fixture Content" section with work log, blockers, and files-modified examples.

4. **~~Document API concurrency considerations (F7)~~** ✅ ADDRESSED: `maxForks` changed from 4 to 2 (conservative start). Subtask 03 updated with guidance to increase after validation. Exponential backoff retry added to harness (Decision 13).

5. **~~Clarify N2/N3 exclusion (F1)~~** ✅ ADDRESSED: Decision 10 in spec index + explicit exclusion paragraph in Overview.

### Nice-to-Have

6. **~~Add subtask 01 → 08 explicit dependency (F5)~~** ✅ ADDRESSED: Added to manifest table, dependency graph, and subtask 08 metadata.

7. **~~Reconcile test count projections (F2)~~** ✅ ADDRESSED: Overview now includes per-category breakdown (57 total, ≈60 approximate) with note that minimums are floors.

---

## Appendix: Subtask-by-Subtask Checklist Mapping

| Checklist Scenario | Subtask | Tests Planned | Coverage |
|-------------------|---------|---------------|----------|
| B1: Dream no args | 04 | 2-3 | Full |
| B2: Dream full flow | 04 | 4-5 | Partial — acceptance flow at risk (F8) |
| B3: Dream conflict | 04 | 2-3 | Full |
| C1: REM interactive | 05 | 3-4 | Partial — confirmation gating at risk (F9) |
| C2: REM --yolo | 05 | 3-4 | Full |
| C3: REM conflict | 05 | 2-3 | Full |
| J1-J4: Recall | Existing | 10 | Already implemented |
| O1-O2: Remember | Existing | 7 | Already implemented |
| P1-P3: Amnesia | Existing | 8 | Already implemented |
| Q1: Meditate no args | 07 | 3 | Simplified — high-level flow only |
| Q2: Meditate topic | 07 | 2 | Simplified — no "Save as draft spec" |
| Q3: Meditate file ref | 07 | 1-2 | Minimal |
| R1: Forget by ID | 06 | 3-4 | Full |
| R2: Forget search | 06 | 2-3 | Full |
| N1: Cursor full flow | 08 | 3-4 | Partial — excludes Meditate and REM (by design) |
| N2: Claude Code wiring | — | 0 | Excluded (not LLM-interactive) |
| N3: Generic platform | — | 0 | Excluded (not LLM-interactive) |

---

*Assessment produced by zoto-spec-judge. This assessment is independent of the spec authors and executing agents.*
