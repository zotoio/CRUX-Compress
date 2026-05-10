---
branch: 2
depth: 1
subfocus_index: 2
subfocus: "Failure Handling and Resilience in Multi-Agent Workflows"
parent_subfocus: "Agent harness orchestration patterns"
timestamp: 2026-05-09T19:50:00+10:00
---

## Subfocus Rationale

Failure handling is the critical dimension that separates toy agent orchestration from production-grade harnesses. While state coordination (sibling 1) addresses the happy path and resource governance (sibling 3) addresses prevention, this branch explores what happens when things go wrong despite those measures — how harnesses detect failures, distinguish transient from permanent, decide between automatic recovery and escalation, and maintain system integrity under partial failure conditions.

## Discoveries

### The Four-Layer Resilience Stack

[memory:Exponential backoff with jitter on rate-limit errors] [memory:Per-phase parallel subagent execution reduces wall-clock time] [memory:Gate expensive SDK evals behind SDK_EVAL_SKIP_EXPENSIVE]

The CRUX eval harness implements a mature four-layer defence-in-depth architecture:

| Layer | Mechanism | Examples | Role |
|-------|-----------|----------|------|
| **Demand reduction** | Shared-agent-runs, skip-by-default gating | N calls → 1; expensive tests opt-in only | Eliminate unnecessary API load |
| **Concurrency limiting** | maxForks: 2, dependency-based phasing | Phase-parallel execution, conservative fork counts | Reduce peak simultaneous pressure |
| **Reactive recovery** | Exponential backoff + jitter on rate-limit detection | `withRetry()`: BASE=2s, MAX=60s, 5 retries, ±15% jitter | Recover from limits hit despite proactive measures |
| **Hard backstop** | Global wall-clock deadline | `SDK_EVAL_MAX_DURATION_MS`: 60min → `process.exit(1)` | Kill suite if reactive layer loops too long |

### The Trust Inversion Principle

[memory:Agent-reported file creation must be verified on disk] The deepest epistemological finding: **an agent's narrative is a hypothesis, not evidence.** An executing agent reported a file as created with full contents and path, yet the file never existed on disk. This demands a fundamental trust inversion — treat all agent claims as falsifiable and verify against ground truth (filesystem state, not self-report).

### The 25% Hit Rate Signal

[memory:Adversarial verification catches real documentation gaps] Independent verification by a separate agent found 6 issues in 24 subtasks (25% overall), but with high variance: 7% in isolated implementations, 50% in cross-cutting integrations. The failure rate correlates with integration complexity, not task count.

### Semantic Hang Detection Gap

The existing harness has one semantic detector (AskQuestion abort) but four unaddressed patterns: tool-call loops, thinking-without-acting, file-polling deadlocks, and phantom completions. All share a common trait: time-based defences alone cannot distinguish them from legitimate slow work.

### The All-or-Nothing Problem

Current architecture has no intermediate state between "agent is struggling" and "kill everything":
- Meditation polls forever for child output files — zero timeout
- Spec execution phases block until all agents complete
- Shared test runs cascade-fail all N dependent tests on beforeAll failure
- `withRetry` only handles rate limits — all other errors throw immediately

## Connections

### Reactive Retries as Feedback Signal (not just recovery)

The "reduce forks rather than increase retries" guideline from memory `6265f8f` reveals that retry frequency functions as a **tuning signal** for proactive measures. If retries fire frequently, the proactive settings (fork count, batching) need adjustment. Removing retries would remove this feedback loop. This generalises to "reduce demand rather than increase tolerance" — a principle that applies beyond test harnesses to any agent orchestration system hitting resource limits.

### Cross-Reference Divergence as Structural Failure Pattern

All five categories where adversarial verification excels (silent persistence, documentation drift, cross-file consistency, default/spec alignment, distribution completeness) share a structural property: **truth distributed across multiple files** that a single sequential agent cannot hold in working memory simultaneously. The verifier's advantage is fresh context with no prior commitment to either source being correct.

### Progress Tokens as Unifying Hang Detection

All semantic hang patterns reduce to one question: "Is the agent making forward progress?" A `lastProgressTimestamp` tracker based on novel tool calls, new files written, or novel output text would subsume tool-call loops, thinking-without-acting, and file-polling deadlocks into a single configurable mechanism — far more robust than pattern-matching individual failure modes.

### The Exploratory/Transactional Divide

The decision to proceed with partial results depends on operation nature:
- **Exploratory** (meditation, recall, research): Partial results almost always beat nothing. Annotate the gap, proceed.
- **Transactional** (spec execution, memory creation): Partial results risk inconsistent state. Escalate to user.

This maps directly onto the meditation protocol's file-based coordination advantage: child outputs persist independently, enabling selective retry at the lowest possible level without reconstructing state.

### Concurrency as Propagating Constraint

Concurrency management propagates through the entire stack: test design (shared runs) → test selection (skip gates) → runtime config (maxForks) → retry parameters (jitter width) → hard limits (wall-clock deadline). All must be coherent — narrow ±15% jitter is adequate for maxForks: 2 but fails catastrophically at maxForks: 4 (56% collision probability). Session flags and concurrency limits need explicit inheritance contracts so child agents don't accidentally violate parent constraints.

## Child Subfocuses

### 1. Retry Strategies and Transient Error Recovery
**Rationale**: Retry logic is the most concrete, implementable dimension — it has a real implementation in the harness with quantifiable parameter tradeoffs and a clear path from current state to improvements.

### 2. Timeout Detection, Hang Recovery, and Graceful Degradation
**Rationale**: The gap between the existing three-tier timeout hierarchy and what's needed for robust multi-agent orchestration is the most urgent architectural concern — a single hung leaf can block an entire meditation tree indefinitely.

### 3. Adversarial Verification as Post-Hoc Failure Detection
**Rationale**: With 25% empirical hit rate and documented cases of catching completely invisible failures, adversarial verification is the most evidence-backed failure detection mechanism in the corpus and warrants dedicated cost-benefit analysis.

## Child Insights

### From Sub-1: Retry Strategies and Transient Error Recovery

The harness's actual retry budget is 62s nominal (not the documented 122s — off-by-one in the memory), consuming only ~21% of a 300s test timeout. Three concrete improvements emerged:

1. **Widen jitter** from ±15% to ±50% or decorrelated jitter to safely support higher parallelism
2. **Raise base delay** from 2s to 5s to reduce wasted retries against typical 10–60s rate-limit windows
3. **Evolve error classifier** from binary (rate-limit or throw) to three-tier (definitely transient → full budget, probably transient → short budget, definitely permanent → throw)

The deeper principle: reactive retries and proactive demand reduction form a feedback loop — retry frequency signals whether proactive settings are correct. Removing retries removes the diagnostic signal.

The four-layer stack (demand reduction → concurrency limiting → reactive retry → hard deadline) composes multiplicatively: 6x demand reduction × 2-fork limit = 12x reduction in rate-limit probability. Demand reduction has compounding returns (fewer calls = lower cost AND fewer failures), while concurrency reduction has diminishing returns (serial execution penalises wall-clock).

### From Sub-2: Timeout Detection, Hang Recovery, and Graceful Degradation

The harness has solid time-based defence (3-tier timeout hierarchy) but critical gaps:

**Five semantic hang patterns** were catalogued with detection mechanisms:
1. Tool-call loops (hash name+args; 3 identical = warning, 5 = abort)
2. Output stagnation (cosine similarity >0.9 over 3+ output cycles)
3. Thinking-without-acting (10+ consecutive thinking events without tool calls after 60s)
4. File-polling deadlocks (same path checked >10 times without success)
5. Phantom completions (Write tool "completed" but file doesn't exist)

A **unifying progress token framework** — track `lastProgressTimestamp` based on novel actions — subsumes all five into a single configurable mechanism.

**The most urgent fix**: Add a polling timeout to the meditate protocol's file-based coordination so a single hung leaf cannot block the entire meditation tree indefinitely.

**Partial-result decision matrix**: failure_mode × branch_criticality × correlation → action. Correlated failures (all N branches) = systemic → escalate immediately. Isolated failure + non-critical = degrade gracefully. The graceful consolidation pattern — proceed with available results, annotate the gap — is strictly better than all-or-nothing for exploratory operations.

### From Sub-3: Adversarial Verification as Post-Hoc Failure Detection

Adversarial verification excels at detecting **cross-reference divergence** — failures where truth is distributed across multiple files. Five categories are well-served; semantic correctness, performance, and security are not.

**Graduated verification model** optimizes cost-benefit:
- Tier 1 (near-zero cost): Automated filesystem checks on ALL subtasks (ls, git status, size checks)
- Tier 2 (moderate cost): Targeted adversarial review on HIGH-RISK subtasks (risk score ≥ 3)
- Tier 3 (expensive): Deep specialized audit on CRITICAL subtasks (risk score ≥ 5)

**Risk heuristic**: File creation (+3), cross-cutting registration (+3), documentation with paths (+2), first-time agent (+2), spec misalignment history (+2).

**Recovery vs escalation boundary** decomposes along three axes:
- Mechanistic failures (file not persisted) → auto-recover
- Judgmental failures (spec contradicts subtask) → escalate
- Expensive retries → always escalate regardless of confidence

**Advisory auto-recovery** pattern: fix the problem AND log it prominently, with a circuit breaker (per-category retry counter) that forces escalation on recurrence. This preserves both velocity and diagnostic visibility.

**Known exceptions manifest** (analogous to `.eslintignore`) suppresses false positives from pre-existing baseline noise, preventing verifier fatigue.

## Summary

Failure handling in multi-agent workflows operates through a defence-in-depth stack with four complementary layers: demand reduction, concurrency limiting, reactive recovery, and hard backstops. The CRUX harness implements all four but has three critical gaps:

1. **Semantic hang detection**: Beyond the single AskQuestion abort pattern, five more hang patterns are undetected. A "progress token" framework would unify detection into a single configurable mechanism. The most urgent concrete fix is adding a polling timeout to file-based coordination.

2. **Partial-result degradation**: The current all-or-nothing model wastes successful work. For exploratory operations, graceful consolidation (proceed with available results, annotate gaps) is strictly better. For transactional operations, correlation-first triage (all-fail = systemic → escalate, one-fail = isolated → retry leaf) prevents the most wasteful failure pattern.

3. **Systematic verification**: Adversarial verification's 25% hit rate justifies its cost, but uniform application is wasteful. A graduated model (automated checks on all, targeted adversarial on high-risk, deep audits on critical) with a risk scoring heuristic optimizes the cost-benefit curve.

The deepest cross-cutting insight: **an agent's narrative is a hypothesis, the filesystem is ground truth, and retry frequency is a diagnostic signal**. These three principles — trust inversion, ground-truth designation, and feedback loops — form the epistemological foundation for any resilient agent orchestration system.
