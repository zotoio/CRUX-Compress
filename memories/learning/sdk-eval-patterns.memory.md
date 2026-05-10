---
id: "cc9291a"
title: "SDK eval patterns: rate limiting, cost control, single-turn testing, and shared runs"
description: "Four complementary patterns for running Cursor SDK eval suites efficiently: (1) exponential backoff with jitter for rate-limit retry, (2) skip-by-default gating for expensive recursive/multi-turn tests, (3) non-interactive directive prompts to collapse interactive commands into single-turn calls, and (4) shared-agent-runs-per-describe-block to reduce API calls from N to 1."
type: "learning"
strength: 4
created: 2026-04-27
modified: 2026-05-10
source: "20260426-sdk-eval-expansion"
tags: [sdk, evals, rate-limiting, retry, exponential-backoff, jitter, concurrency, parallelism, vitest, harness, cost-control, env-vars, expensive-tests, opt-in, ci, skip-by-default, single-turn, prompt-engineering, non-interactive, ground-truth-assertions, beforeAll, describe-scope, api-cost, performance, test-design, shared-state, batched-assertions]
consolidated_from: ["6265f8f", "e05030c", "fcd2f69", "6415c52"]
---

# SDK Eval Patterns

Four validated patterns for running Cursor SDK eval suites efficiently and reliably.

## 1. Exponential Backoff with Jitter for Rate Limits

When vitest runs with `pool: "forks"` and `maxForks: 2+`, concurrent agent sessions hit the API simultaneously. Transient 429/throttle errors must not fail tests.

**Pattern**: Wrap `agent.send()` with `sendWithRetry()` using exponential backoff (BASE_DELAY_MS=2000, MAX_DELAY_MS=60000, MAX_RETRIES=5) plus ±15% jitter.

**Detection**: Match error messages case-insensitively for `"rate limit"`, `"rate_limit"`, `"429"`, `"too many requests"`, or `"throttl"`. Throw non-rate-limit errors immediately — never mask real bugs.

**Parameters**: First retry ~2s, worst-case cumulative wait ~122s (under typical 300s test timeouts). Jitter spreads retries across a 30% window so concurrent forks don't re-collide.

**Pair with conservative parallelism**: Start at `maxForks: 2`, scale empirically. Fewer concurrent sessions reduces retry pressure.

**Location**: `evals/sdk/helpers/harness.ts` exports `withRetry()` and `sendWithRetry()`.

## 2. Skip-by-Default Gating for Expensive Tests

Recursive subagent commands (Meditate: up to 13 agents/test) and multi-turn integration flows (5+ turns) are 10x+ more expensive than single-turn tests.

**Pattern**: Gate expensive categories with `describe.skipIf(skipExpensive)` where:
```typescript
const skipExpensive = process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false";
```

Default (env unset) = skip. Explicit `SDK_EVAL_SKIP_EXPENSIVE=false` = run.

**Package.json scripts**: Dedicated scripts encode the opt-in:
```json
"test:meditate": "SDK_EVAL_SKIP_EXPENSIVE=false vitest run --grep Meditate"
```

**Defensive pair**: Global wall-clock deadline (`SDK_EVAL_MAX_DURATION_MS`, default 60min) kills runaway suites regardless of per-test timeouts.

**Apply when**: Per-test cost is 5x+ median, wall-clock >5 minutes, recursive spawning, or intended for explicit (nightly/pre-release) invocation only.

## 3. Non-Interactive Directive Prompts for Single-Turn Testing

The SDK's `agent.send()` is single-turn — no follow-up user input. Commands with interactive flows (Dream: accept/reject candidates, Forget: confirm deletions, REM: conflict resolution) need their acceptance intent embedded in the initial prompt.

**Pattern**: Append flow disposition after an em-dash:
```text
/crux-dream 20260420-feature — accept all candidate facts and write the dream summary
/crux-dream --rem --yolo — present any conflicts for review but do not auto-resolve
/crux-forget sdk-test-forget-perf
```

**Assertion strategy**: Replace conversational-flow assertions with ground-truth side-effect assertions:
- "Agent presented candidates" → memory files exist on disk after run
- "Agent confirmed before deleting" → target file absent on disk
- "Agent surfaced conflicts" → conflicting memory files still exist (unmodified)

**Exception**: Conflict detection directives must explicitly say "do not auto-resolve" — conflicts are always user decisions.

## 4. Shared-Agent-Runs-Per-Describe-Block

When multiple assertions all check the same agent turn's output, run the agent once in `beforeAll` and share the `CollectedRun` across N `it()` blocks.

**Economics**: 3-5x reduction in API calls and wall-clock time per describe block while preserving per-assertion failure reporting granularity.

**When to use**: All assertions check the same turn's output (keyword matches, file checks, tool-call presence). Does NOT work when assertions need different prompts or have sequential dependencies.

**Trade-off**: If `beforeAll` fails, all N tests fail together. Descriptive `beforeAll` setup and per-test names mitigate this in CI output.

**Distinct from multi-turn**: Integration tests use a shared `agent` instance with `describe.sequential()` where each test sends its own `agent.send()`. The shared-`beforeAll` pattern collapses unnecessary duplicate calls, not inherently multi-turn flows.

**Used in**: `b-dream.test.ts` (9 tests via 3 agent calls), `q-meditate.test.ts` (5 tests via 3 agent calls).

## Source

All four patterns from `spec-sdk-eval-expansion-20260426.md`, implemented across subtasks 02 (Harness), 04 (Dream), 05 (REM), 06 (Forget), 07 (Meditate), 08 (Integration), and 09 (Validation).
