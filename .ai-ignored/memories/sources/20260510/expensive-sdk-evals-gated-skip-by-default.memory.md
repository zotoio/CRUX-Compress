---
id: "e05030c"
title: "Gate expensive SDK evals behind SDK_EVAL_SKIP_EXPENSIVE with skip-by-default to prevent accidental API spend"
description: "Recursive subagent commands (Meditate spawns up to 13 agents per test) and multi-turn integration flows (5+ turns) are 10x+ more expensive than single-turn tests. Use describe.skipIf(skipExpensive) gated by an env var that defaults to true (skip): const skipExpensive = process.env.SDK_EVAL_SKIP_EXPENSIVE !== 'false'. Provide explicit package.json scripts that set the env var to 'false' (e.g. 'test:meditate': 'SDK_EVAL_SKIP_EXPENSIVE=false vitest run --grep Meditate'). Document the default in README and .env.example so engineers understand why pnpm test omits these tests. Pair with global wall-clock deadline (SDK_EVAL_MAX_DURATION_MS, default 60min) as a backstop."
type: "learning"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "20260426-sdk-eval-expansion"
tags: [sdk, evals, cost-control, env-vars, expensive-tests, opt-in, ci, vitest, skip-by-default]
---

# Gate expensive LLM evals behind a skip-by-default env var

## The cost asymmetry

Not all SDK eval tests cost the same. In the CRUX Memories suite the cost distribution is roughly:

| Category | Per-test cost | Notes |
|----------|---------------|-------|
| Single-turn (Recall, Remember, Forget) | 1 agent invocation | ~30-90s |
| Multi-step single-turn (Dream, REM) | 1 agent invocation, longer thinking | ~60-120s |
| Recursive (Meditate) | up to 13 agent invocations per test | 3 facets × 3 levels of subagent inception |
| Integration (multi-turn N1) | 5+ agent invocations | sequential turns sharing one agent |

The recursive and integration categories are 10x+ more expensive than the rest. Running them on every `pnpm test` invocation — including local re-runs, CI on every push, and accidental triggers — risks unbounded API spend.

## The pattern

Skip the expensive categories by default, opt in explicitly when they need to run.

```typescript
const skipExpensive = process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false";

describe.skipIf(skipExpensive)("Q: Meditate", () => {
  // ...
});

describe.skipIf(skipExpensive)("N: Cross-Platform Integration", () => {
  // ...
});
```

Note the comparison: `!== "false"`. The default (env var unset) is "skip". The user must explicitly set `SDK_EVAL_SKIP_EXPENSIVE=false` to run these tests.

In `package.json`, dedicated scripts encode the opt-in:

```json
{
  "test": "vitest run",
  "test:meditate": "SDK_EVAL_SKIP_EXPENSIVE=false vitest run --grep 'Meditate'",
  "test:integration": "SDK_EVAL_SKIP_EXPENSIVE=false vitest run --grep 'Integration'"
}
```

`pnpm test` runs everything that is not skip-gated. `pnpm test:meditate` and `pnpm test:integration` run the gated suites by toggling the env var inline. There is no third path.

## The defensive pair: global wall-clock deadline

Even with skip-by-default, a runaway agent or an unexpected loop can accumulate cost. Pair the per-suite gate with a global wall-clock deadline in the test setup file:

```typescript
const DEFAULT_MAX_DURATION_MS = 3_600_000; // 60 minutes
const maxDurationMs = parseInt(
  process.env.SDK_EVAL_MAX_DURATION_MS || String(DEFAULT_MAX_DURATION_MS),
  10
);

const globalTimer = setTimeout(() => {
  console.error(`GLOBAL TIMEOUT: Test suite exceeded ${maxDurationMs}ms.`);
  process.exit(1);
}, maxDurationMs);

globalTimer.unref();
```

Per-test timeouts protect against individual hangs; the global deadline protects against the cumulative case where every test runs successfully but the suite as a whole exceeds the budget.

## Discoverability

The setup file should announce the gating state on every run so engineers understand why some tests are missing:

```text
✓ Global max duration: 60 minutes (SDK_EVAL_MAX_DURATION_MS=3600000)
✓ Expensive tests (Meditate, Integration) will be SKIPPED (set SDK_EVAL_SKIP_EXPENSIVE=false to run them)
```

Document the env vars in `.env.example` and the eval suite README so the opt-in path is discoverable without reading source.

## When to apply this pattern

Apply skip-by-default gating whenever a test category meets any of:

- Per-test cost is 5x+ the median
- Per-test wall-clock is >5 minutes
- The test exercises recursive subagent spawning, long multi-turn flows, or expensive external services
- The test is intended for explicit invocation (e.g. nightly, pre-release) rather than every CI run

Cheap tests stay default-on. Expensive tests stay default-off. There is no in-between.

## Source

Decision 12 of `spec-sdk-eval-expansion-20260426.md`. Originated as finding F10 in the spec assessment ("Meditate tests are extremely expensive and may be cost-prohibitive"). Implemented in subtasks 07 (Meditate), 08 (Integration), and reflected in `evals/sdk/vitest.setup.ts`, `evals/sdk/package.json`, and the eval suite README.
