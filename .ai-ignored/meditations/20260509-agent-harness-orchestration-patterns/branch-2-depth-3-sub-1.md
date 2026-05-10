---
branch: 2
depth: 3
subfocus_index: 1
subfocus: "Error Classification Heuristics for Transient vs Permanent Failures"
parent_subfocus: "Retry Strategies and Transient Error Recovery"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

Error classification is the decision gate that determines every downstream retry behaviour — backoff timing, retry budget, and whether to retry at all. Getting this gate wrong in either direction (false positive: retrying a permanent error; false negative: throwing on a recoverable one) has outsized consequences, so it deserves dedicated depth-3 analysis separate from the retry mechanics themselves.

## Discoveries

### Memory corpus findings

**Memory `6265f8f`** (Exponential backoff with jitter) is the primary source. It documents the current `isRateLimitError()` implementation in `evals/sdk/helpers/harness.ts` (lines 128-139) and explicitly notes:
- The SDK "doesn't always surface HTTP status codes cleanly — sometimes the error is a generic `Error` with the upstream message embedded"
- Five substring patterns are matched case-insensitively: `"rate limit"`, `"rate_limit"`, `"429"`, `"too many requests"`, `"throttl"`
- "Adding more patterns is cheap; missing one means a transient error gets thrown as if it were a real bug"

**Memory `e05030c`** (Gate expensive evals) provides the global timeout backstop (`SDK_EVAL_MAX_DURATION_MS`, default 60 min) — a second line of defence if false-positive classification causes unbounded retries.

**Codebase sample** (`web/compress.md/assets/rules/sample-rule.source.md`, lines 272-285) demonstrates the alternative approach: a structured `IntegrationError` class with an explicit `retryable: boolean` property baked into the error type at construction time, rather than inspected after the fact.

### Current implementation analysis

The `isRateLimitError()` function makes three design choices worth examining:

1. **`instanceof Error` guard** — returns `false` for non-Error objects. This is safe within a single JS realm but breaks when errors cross serialisation boundaries (e.g., errors thrown in a child process, deserialised from JSON, or proxied through structured clone). Serialised errors become plain objects and silently bypass the classifier.

2. **Substring matching on `.message`** — practical but fragile. Five literal substrings cover the currently-known phrasings. The approach is O(1) to add a new pattern but requires someone to notice the new phrasing first.

3. **Binary classification (rate-limit → retry, everything else → throw)** — there is no intermediate category. Server errors (500, 502, 503), network timeouts, and DNS failures are all classified as permanent and thrown immediately, even though many are transient.

## Connections

### False-positive risk: "429" as a substring

The string `"429"` can appear in non-rate-limit error messages. Examples:
- Error messages containing memory addresses, trace IDs, or correlation IDs that happen to contain "429" as a substring (e.g., `"Request failed at offset 4290"`)
- Stack traces embedded in error messages where a line number is 429
- Errors mentioning a port number or configuration value containing "429"

The risk is low in practice because `.toLowerCase()` + `.includes("429")` matches any occurrence, but rate-limit errors almost always include "429" alongside other distinctive text. A tighter match like `"429 "` or `" 429"` (with adjacent space/punctuation) would reduce false-positive surface at negligible cost. A regex like `/\b429\b/` would be more precise while remaining readable.

### False-negative risk: evolving API phrasings

The five patterns are a snapshot of known phrasings. Silent false negatives arise when:
- An API introduces `"quota exceeded"` or `"request limit"` or `"capacity"` — none of which match
- The SDK wraps errors in a custom type where the original message is in a `.cause` property or nested `.data` field, not in `.message`
- The error uses a non-English locale for the status text
- Future SDK versions emit structured error objects with a `.code` or `.status` field instead of embedding it in the message string

Each missed phrasing causes a transient error to be thrown as permanent, failing the test. The only feedback mechanism is a developer noticing a spike in flaky test failures and manually adding a new pattern.

### The `instanceof Error` cross-realm problem

In Node.js, `instanceof Error` fails across:
- **Worker threads** — errors thrown in a `worker_threads` worker and posted to the parent via `parentPort.postMessage()` are serialised and deserialised, losing their prototype chain
- **Child processes** — `execSync` and `spawn` errors are often wrapped in new `Error` objects, but if the SDK communicates via JSON-RPC or similar, errors may arrive as plain objects
- **Structured clone** — `structuredClone(new Error("x"))` preserves the Error prototype, but custom subclasses lose their custom properties
- **JSON.parse round-trip** — any error serialised to JSON and back becomes a plain object

The current harness uses `agent.send()` which likely throws proper Error instances, so this is not an active bug — but it is a latent fragility if the SDK's error transport changes.

### The missing middle: errors that are transient but not rate limits

The current binary classifier (rate-limit → retry, else → throw) has no category for:
- **Server errors** (500, 502, 503, 504) — often transient, recoverable after a brief wait
- **Network errors** (`ECONNRESET`, `ECONNREFUSED`, `ETIMEDOUT`, `EPIPE`) — commonly transient under load
- **DNS resolution failures** — transient in environments with flaky resolvers

These are currently thrown immediately. For the eval harness, this is a defensible choice (fail fast, let the developer investigate). But for a production agent harness, a three-tier classification would be more robust:
1. **Definitely transient** (rate limits) → retry with backoff
2. **Probably transient** (server errors, network errors) → retry with shorter budget (1-2 attempts)
3. **Definitely permanent** (auth errors, validation errors, 404s) → throw immediately

### Extensibility model: hardcoded list vs pattern registry

The current approach hardcodes patterns directly in the function body. This is fine for a small, stable set but creates maintenance friction as APIs evolve. Alternative extensibility models:

| Model | Pros | Cons |
|-------|------|------|
| **Hardcoded list** (current) | Simple, zero overhead, easy to audit | Requires code change + deploy for each new pattern |
| **Configurable pattern array** | New patterns via config/env, no redeploy | Config drift risk; harder to test exhaustively |
| **Error code enum** | Structured, type-safe, composable | Requires upstream to emit codes — not always possible |
| **Classifier chain** (chain of responsibility) | Extensible, testable, supports multiple error categories | Over-engineered for 5 patterns |
| **Allowlist + denylist** | Explicit transient list AND explicit permanent list; unknown → configurable default | Most robust against unknown errors; two lists to maintain |

For the current harness, the hardcoded list is appropriate. If the pattern set grows beyond ~10 entries or if multiple consumers need different classification policies, a configurable pattern array (loaded from a constants file or config) would be the natural next step. The key insight is that the extensibility model should match the rate of change of the error surface.

### Connection to `IntegrationError.retryable`

The sample-rule codebase demonstrates the ideal: the error itself carries `retryable: boolean` as a typed property, set at throw-time by the code that knows whether the failure is transient. This pushes classification to the error producer rather than the error consumer. The consumer just reads `err.retryable` — no message inspection needed.

This is the direction the harness should evolve toward if/when the Cursor SDK introduces structured error types. Until then, message inspection is the only viable approach for third-party consumers of opaque Error objects.

### The global timeout as a safety net

Memory `e05030c` documents `SDK_EVAL_MAX_DURATION_MS` (default 60 min). This is architecturally important as a backstop against false-positive classification: even if `isRateLimitError()` incorrectly returns `true` for a permanent error, the global deadline eventually kills the process. Without this backstop, a misclassified permanent error would retry 5 times × 60s max delay = 5 minutes of wasted time per test, potentially cascading across all tests in a suite. The two mechanisms (classifier + deadline) form a defence-in-depth pair.

## Summary

The current `isRateLimitError()` implementation in `harness.ts` makes a pragmatic, well-documented choice: substring matching on `err.message` with a hardcoded list of 5 phrasings, `instanceof Error` guard, and binary classification (rate-limit → retry, else → throw). This is correct for the current SDK error surface but has three latent fragilities: (1) `"429"` as a bare substring can false-positive on non-rate-limit messages containing that number, (2) `instanceof Error` breaks across serialisation boundaries, and (3) the binary classification discards the "probably transient" category (server errors, network errors) that a production harness would want to retry with a shorter budget. The strongest extensibility direction is toward structured error types with explicit `retryable` properties (as demonstrated by the `IntegrationError` pattern in the sample codebase), with the configurable pattern array as the practical intermediate step. The global timeout (`SDK_EVAL_MAX_DURATION_MS`) provides a critical safety net against classification false positives, forming a defence-in-depth pair with the classifier itself.
