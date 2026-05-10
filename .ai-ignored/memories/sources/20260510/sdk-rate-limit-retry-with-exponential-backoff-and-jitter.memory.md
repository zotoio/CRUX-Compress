---
id: "6265f8f"
title: "Exponential backoff with jitter on rate-limit errors is the right concurrency mitigation for parallel SDK forks"
description: "When running concurrent agent.send() calls across vitest forks (pool: 'forks', maxForks: 2+), API rate limits are inevitable on long suites. Wrap agent.send() with sendWithRetry() that uses exponential backoff (BASE_DELAY_MS=2000, MAX_DELAY_MS=60000, DEFAULT_MAX_RETRIES=5) plus ±15% jitter to avoid thundering-herd retries. Detect rate-limit by checking the error message for 'rate limit', 'rate_limit', '429', 'too many requests', or 'throttl' (case-insensitive). Throw non-rate-limit errors immediately so real bugs aren't masked. Pair with conservative starting parallelism (maxForks: 2, scale empirically) — fewer concurrent sessions reduces retry pressure."
type: "learning"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "20260426-sdk-eval-expansion"
tags: [sdk, evals, rate-limiting, retry, exponential-backoff, jitter, concurrency, parallelism, vitest, harness]
---

# Exponential backoff + jitter for parallel SDK rate limits

## The problem

When vitest runs the SDK eval suite with `pool: "forks"` and `maxForks: 2+`, two or more agent SDK sessions hit the Cursor API concurrently. Long-running suites accumulate enough requests to occasionally trip rate limits. Without retry handling, transient `429`/throttle errors fail the test, even though the underlying agent behaviour was correct.

Naïve fixes have known failure modes:

| Approach | Failure mode |
|----------|--------------|
| Fixed delay retry | All forks retry simultaneously → thundering herd hits the limit again |
| Linear backoff | Slow to escape sustained rate-limit windows |
| Catching all errors | Real bugs (auth failures, programming errors) get retried into oblivion |
| Single-fork only | Wall-clock cost of full suite balloons to 50+ minutes |

## The pattern

Wrap `agent.send()` with a helper that:

1. Detects rate-limit errors by message inspection (substring match, case-insensitive)
2. Retries non-rate-limit errors **never** — throw immediately
3. Retries rate-limit errors with **exponential backoff** plus **jitter**
4. Caps retries at `DEFAULT_MAX_RETRIES = 5` and delays at `MAX_DELAY_MS = 60_000`

```typescript
const DEFAULT_MAX_RETRIES = 5;
const BASE_DELAY_MS = 2_000;
const MAX_DELAY_MS = 60_000;

function isRateLimitError(err: unknown): boolean {
  if (err instanceof Error) {
    const msg = err.message.toLowerCase();
    return (
      msg.includes("rate limit") ||
      msg.includes("rate_limit") ||
      msg.includes("429") ||
      msg.includes("too many requests") ||
      msg.includes("throttl")
    );
  }
  return false;
}

function backoffDelay(attempt: number): number {
  const jitter = Math.random() * 0.3 + 0.85; // 0.85-1.15x
  return Math.min(BASE_DELAY_MS * Math.pow(2, attempt) * jitter, MAX_DELAY_MS);
}

export async function withRetry<T>(
  fn: () => Promise<T>,
  label = "operation",
  maxRetries = DEFAULT_MAX_RETRIES
): Promise<T> {
  for (let attempt = 0; ; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (!isRateLimitError(err) || attempt >= maxRetries) {
        throw err;
      }
      const delay = backoffDelay(attempt);
      // log + sleep
      await new Promise((r) => setTimeout(r, delay));
    }
  }
}

export async function sendWithRetry(agent: Agent, message: string) {
  return withRetry(() => agent.send(message), `send("${message.slice(0, 60)}")`);
}
```

## The numbers matter

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `BASE_DELAY_MS` | 2000 | First retry waits 2-2.3s — long enough to clear most rate windows |
| `MAX_DELAY_MS` | 60000 | Caps the worst-case wait at 1 minute so vitest test timeouts stay meaningful |
| `DEFAULT_MAX_RETRIES` | 5 | Total worst-case: 2+4+8+16+32+60 ≈ 122s of waits — still under typical 300s test timeouts |
| Jitter `[0.85, 1.15]` | ±15% | Spreads retries across 30% of the wait window so concurrent forks don't re-collide |

The math: at attempt 5 (the cap) the un-jittered delay is `2000 × 2^5 = 64000ms`, which gets clamped to 60000. With jitter the actual wait is in `[51000, 60000]`. Even at the cap, two simultaneously-throttled forks won't retry within the same 9-second window.

## Detect by message, not by status code

The SDK doesn't always surface HTTP status codes cleanly — sometimes the error is a generic `Error` with the upstream message embedded. Match all five known phrasings:

- `"rate limit"` (most common)
- `"rate_limit"` (programmatic form)
- `"429"` (status code in message body)
- `"too many requests"` (HTTP status text)
- `"throttl"` (matches "throttle"/"throttled"/"throttling")

Adding more patterns is cheap; missing one means a transient error gets thrown as if it were a real bug.

## Critical: throw non-rate-limit errors immediately

The retry path is for **transient** errors only. Wrapping all errors in retries would mask real bugs:

- Auth failures would retry through the entire timeout budget before failing
- Programming errors (bad prompts, malformed JSON) would be repeated 5 times
- Test setup mistakes would look like rate limits

`isRateLimitError(err)` returning `false` short-circuits to `throw err` immediately. Be explicit.

## Pair with conservative parallelism

Retry alone is reactive. Reduce the *probability* of hitting limits by starting with low concurrency:

- `maxForks: 2` is a safe starting point for a 7-9 file suite
- Scale to 3-4 only after a full validation run shows no rate-limit retries occurring
- If retries become frequent at any fork count, reduce parallelism rather than increasing retries

## Where this lives

`evals/sdk/helpers/harness.ts` exports `withRetry()` and `sendWithRetry()`. Tests in expensive categories (Q, N) use `sendWithRetry()` consistently. Cheap tests (B, C, R) use direct `agent.send()` and can be retrofitted if rate limiting becomes an issue at higher fork counts.

## Source

Decision 13 of `spec-sdk-eval-expansion-20260426.md`. Originated as finding F7 in the spec assessment ("`maxForks: 4` may exhaust system resources with 4 concurrent agent SDK sessions"). Implementation in subtask 02 (Harness Enhancements).
