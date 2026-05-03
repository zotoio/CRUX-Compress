---
id: "6415c52"
title: "Shared-agent-runs-per-describe-block reduce LLM eval cost from N agent calls to 1"
description: "Pattern: in vitest, run a single agent.send() in beforeAll, store the CollectedRun in a describe-scoped variable, and have N it() blocks each assert different aspects of that single run's output. This collapses what would otherwise be N x ~60-90s API calls into 1 x ~60-90s for the whole scenario — typical reduction is 3-6x cost and wall-clock time per describe block. Used successfully in b-dream (B1/B2/B3 each share one run) and q-meditate (Q1 shares 2-turn setup+meditate). Trade-off: if the shared run fails, all N tests fail together; descriptive error messages per assertion partially mitigate this. Use only when assertions are read-only (no side effects from one assertion to the next) or all check the same agent turn's output. Distinct from a single it() with multiple expects — separate it()s give per-assertion failure reporting."
type: "learning"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "20260426-sdk-eval-expansion"
tags: [evals, sdk, vitest, beforeAll, describe-scope, api-cost, performance, test-design, shared-state, batched-assertions]
---

# Shared-agent-runs-per-describe-block reduce LLM eval cost

## The pattern

When a single agent turn produces output that several independent assertions all need to inspect, run the agent **once** in `beforeAll` and store the collected run at describe scope. Each `it()` block reads its own slice of that shared result.

```typescript
describe("B2: Dream - Full Flow", () => {
  let result: CollectedRun;

  beforeAll(async () => {
    const agent = Agent.create({ apiKey: getApiKey(), local: { cwd: ws.root } });
    try {
      const run = await sendWithRetry(
        agent,
        "/crux-dream 20260420-test-feature — accept all candidate facts and write the dream summary"
      );
      result = await collectRun(run, "B2 dream full flow");
    } finally {
      agent[Symbol.asyncDispose]?.();
    }
  }, 300_000);

  it("verifies spec execution status", { timeout: 300_000 }, () => {
    expect(result.assistantText.toLowerCase()).toMatch(/verif|complete|execution/);
  });

  it("presents candidate facts with type labels", { timeout: 300_000 }, () => {
    expect(result.assistantText).toMatch(/\[(learning|redflag|idea|goal|core)\]/i);
  });

  it("creates memory files and writes dream summary", { timeout: 300_000 }, () => {
    expect(countMemoryFiles(ws.root)).toBeGreaterThan(initialMemoryCount);
  });
});
```

## The economics

| Approach | API calls per describe block | Wall-clock |
|----------|------------------------------|------------|
| One agent per `it()` | N | N × 60–120s |
| Single `it()` with multiple expects | 1 | 1 × 60–120s |
| **Shared `beforeAll` + N `it()`s (this pattern)** | **1** | **1 × 60–120s** |

For a describe block with 3-5 assertions (typical of B/Q tests), the shared-`beforeAll` pattern yields a 3-5x reduction over per-test agents while keeping the per-assertion failure-reporting granularity that a single `it()` would lose.

## When to use

The pattern works when **all** assertions in a describe block check the same agent turn's output:

- Multiple keyword/regex matches against one `assistantText`
- Multiple ground-truth file checks after the same side-effecting run
- Tool-call presence checks combined with output content checks
- Combinations of the above

It does **not** work when:

- Assertions need different prompts (each prompt is a separate agent call by definition)
- One assertion's side effect must be visible before the next runs (use sequential tests instead)
- The describe block tests an interactive multi-turn flow where each turn depends on the previous (use a shared agent across `it()`s with `describe.sequential` instead — see `tests/n-integration.test.ts`)

## Why not a single `it()` with multiple expects?

Both single-`it()` and shared-`beforeAll` approaches make exactly one API call. The difference is failure reporting:

- Single `it()`: first failing `expect()` throws, subsequent expects are skipped, one test fails
- Shared `beforeAll` + N `it()`s: each `expect()` runs in its own test; multiple can fail independently with their own descriptive names

For a flaky LLM output check, knowing which three of five assertions failed (and which two passed) is significantly more useful than seeing only the first failure. Per-test descriptions also make CI dashboards far more useful.

## The shared-failure trade-off

If the `beforeAll` itself fails (agent crashes, network drops, prompt rejected), every `it()` in the block fails. The failures are correlated — one root cause, N derivative failures.

Mitigation: **descriptive `beforeAll` setup**. When the agent call wraps in `try/catch` with logging, the `beforeAll` failure surfaces the underlying cause clearly. Per-test names should also describe what the test is checking so the cascade is interpretable in CI output.

For test categories where a `beforeAll` failure is unacceptable (e.g. quick-feedback regression tests), prefer per-`it()` agents at the cost of higher API spend.

## Distinct from sequential multi-turn

The integration test (`n-integration.test.ts`) uses a different pattern: a single `agent` instance shared across `it()`s with `describe.sequential()`, where each test sends its own `agent.send()` and references state created by previous tests. That pattern explicitly tests command wiring across turns. The shared-`beforeAll` pattern collapses what would have been multiple unnecessary agent calls into one — it does not replace inherently multi-turn testing.

## Files where this is used

- `evals/sdk/tests/b-dream.test.ts` — B1, B2, B3 each share one run (3 tests × 3 describe blocks = 9 tests via 3 agent calls)
- `evals/sdk/tests/q-meditate.test.ts` — Q1 (3 tests via 2-turn setup+meditate), Q2 (2 tests via 1 turn)

## Source

Subtask 04 (Dream Tests) Design Decisions section: "Shared runs per describe block: B1, B2, B3 each run a single agent call in `beforeAll`, then individual tests assert on the shared `CollectedRun`. This is 6x more efficient than per-test agent calls." Reinforced in subtask 09 (Validation & Profiling) Lessons Learned: "Shared agent runs via `beforeAll` (as used in b-dream and q-meditate) are significantly more cost-efficient than per-test agent creation, reducing API calls from N to 1 per describe block."
