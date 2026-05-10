---
branch: 2
depth: 2
subfocus_index: 1
subfocus: "Retry Strategies and Transient Error Recovery"
parent_subfocus: "Failure Handling and Resilience in Multi-Agent Workflows"
timestamp: 2026-05-09T19:39:00+10:00
---

## Subfocus Rationale

Retry logic is the most concrete, implementable dimension of failure resilience — it operates at the boundary between "detect" and "recover" and its parameters have quantifiable tradeoffs. Unlike timeout detection or graceful degradation (siblings in the parent facet), retry strategies have a real implementation in the CRUX harness (`evals/sdk/helpers/harness.ts`) with documented design decisions, making them ideal for grounded analysis rather than abstract pattern-cataloguing.

## Discoveries

### The CRUX harness as a concrete case study

[memory:Exponential backoff with jitter on rate-limit errors] The harness at `evals/sdk/helpers/harness.ts` exports `withRetry()` and `sendWithRetry()` — a clean separation between the generic retry wrapper and the agent-specific entry point. The implementation makes three core design choices:

1. **Error classification by message inspection**: `isRateLimitError()` checks `err.message.toLowerCase()` against five substring patterns (rate limit, rate_limit, 429, too many requests, throttl). Non-matching errors are thrown immediately — no retry.
2. **Exponential backoff with bounded jitter**: `BASE_DELAY_MS=2000`, exponential doubling, `MAX_DELAY_MS=60000` cap, ±15% jitter spread.
3. **Fixed retry budget**: `DEFAULT_MAX_RETRIES=5` — after 5 failed retries, the error propagates.

### Key quantitative finding: the budget is more conservative than documented

Memory `6265f8f` states worst-case delay is ~122s. The depth-3 analysis corrected this to **62s nominal (53–71s with jitter)** — the code throws at attempt 5 before computing a 6th delay. This means the retry budget consumes only ~21% of a 300s test timeout, leaving substantial headroom. The `MAX_DELAY_MS=60000` cap is effectively dead code under current parameters (never reached with only 5 retries).

### Three-tier classification gap

The current classifier is binary: rate-limit errors retry, everything else throws. Server errors (500, 502, 503), network errors (ECONNRESET, ETIMEDOUT), and DNS failures are all classified as permanent. For a test harness this is defensible (fail fast, investigate). For a production agent harness, a three-tier model would serve better: (1) definitely transient → full retry budget, (2) probably transient → short retry budget (1–2 attempts), (3) definitely permanent → throw immediately.

### Jitter width couples to parallelism

The ±15% jitter spread produces a 30% delay window at each attempt. At `maxForks: 2` the collision probability is ~10% — acceptable. At `maxForks: 4` it jumps to 56%, making thundering-herd retries likely. The `maxForks: 2` recommendation and the ±15% jitter form a tightly coupled pair — changing either requires re-evaluating the other. Wider alternatives (±50%, full jitter, decorrelated jitter) would decouple this constraint.

### Four-layer resilience stack

The harness implements not one but four complementary resilience layers:

| Layer | Mechanism | Role |
|-------|-----------|------|
| Demand reduction | Shared-agent-runs (N calls → 1), skip-by-default gating | Eliminate unnecessary API calls |
| Concurrency limiting | `maxForks: 2`, dependency-based phasing | Reduce peak simultaneous load |
| Reactive recovery | Exponential backoff + jitter on rate-limit detection | Recover from limits hit despite proactive measures |
| Hard backstop | Global `SDK_EVAL_MAX_DURATION_MS` (60min) | Kill suite if reactive layer loops too long |

## Connections

### Retries as feedback signal, not just recovery

The "reduce forks rather than increase retries" guideline from `6265f8f` reveals that retry frequency functions as a **tuning signal** for proactive measures. If retries fire frequently, the proactive settings (fork count, batching) need adjustment. If retries never fire, the proactive settings are correct. Removing retries would remove this feedback loop — making it impossible to know whether proactive measures are sufficient.

### Demand reduction vs concurrency reduction — multiplicative composition

Shared-agent-runs are demand reduction (eliminate calls entirely), while `maxForks` is concurrency reduction (same calls, fewer simultaneous). These compose multiplicatively: 6x demand reduction × 2-fork limit = 12x reduction in rate-limit probability vs unbatched 4-fork execution. This distinction matters because demand reduction has compounding returns (fewer calls = lower cost AND fewer failures), while concurrency reduction has diminishing returns (serial execution penalises wall-clock time).

### The "429" false-positive and `instanceof Error` cross-realm fragility

The substring `"429"` can false-positive on non-rate-limit messages containing that number (trace IDs, line numbers). The `instanceof Error` guard fails across serialisation boundaries (child processes, JSON round-trips, worker threads). Neither is an active bug, but both are latent fragilities that would surface if the SDK's error transport evolves. A word-boundary regex (`/\b429\b/`) and a duck-typing check (`typeof err === 'object' && 'message' in err`) would harden both.

### Structured error types as the ideal evolution

The sample codebase demonstrates `IntegrationError` with an explicit `retryable: boolean` property — pushing classification to the error producer who knows the failure's nature. This eliminates message inspection entirely. The current substring approach is a pragmatic workaround for consuming opaque third-party errors; the long-term direction is structured error types when the SDK provides them.

### Bimodal retry importance

Skip-by-default gating creates two runtime profiles: default mode (cheap tests, retries are insurance) and expensive mode (recursive multi-agent tests, retries are load-bearing). The retry mechanism's importance is inversely proportional to proactive gating effectiveness — exactly when you opt into expensive work, the safety net matters most.

### Base delay alignment with rate-limit windows

The 2s base delay likely wastes the first 1–2 retry attempts against typical 10–60s rate-limit reset windows (cumulative delay after 2 retries is only ~14s). A base of 5s with 4 retries would maintain the same total budget (~75s) while reducing wasted attempts. The optimal base delay is `ceil(reset_window / 2)` — long enough that first retry might clear the window, short enough not to dominate the budget.

### Concurrency as a propagating constraint

Concurrency management is not a single knob but a constraint that propagates through multiple system layers: test design (shared runs), test selection (skip gates), runtime config (maxForks), retry parameters (budget, jitter), and hard limits (wall-clock deadline). All must be coherent — a generous maxForks undermines demand reduction, narrow jitter fails at high parallelism, and aggressive skip-gating makes retries vestigial in default mode but essential in explicit-run mode.

## Child Subfocuses

### Sub-1: Error Classification Heuristics for Transient vs Permanent Failures
**Rationale**: Error classification is the decision gate that determines all downstream retry behaviour. Getting the gate wrong (false positive or false negative) has outsized consequences, warranting dedicated analysis of the substring-matching approach, cross-realm fragilities, and the missing three-tier classification model.

### Sub-2: Backoff Parameter Tuning and Retry Budget Optimisation
**Rationale**: The concrete parameters (BASE_DELAY, MAX_DELAY, retries, jitter) have quantifiable tradeoffs against test timeouts, rate-limit window alignment, and fork-count collision probabilities. Mathematical analysis reveals the budget is more conservative than documented and identifies specific parameter improvements.

### Sub-3: Pairing Reactive Retries with Proactive Concurrency Reduction
**Rationale**: Reactive and proactive strategies are often designed independently but their interaction determines whether the resilience model is synergistic or counterproductive. Understanding the four-layer stack and the feedback loop between retry frequency and proactive tuning is essential for generalising beyond test harnesses.

## Child Insights

### From Sub-1 (Error Classification)
- The `isRateLimitError()` binary classifier has three latent fragilities: bare `"429"` substring can false-positive, `instanceof Error` fails across serialisation boundaries, and the binary model discards "probably transient" server/network errors.
- The extensibility model (hardcoded substring list) is appropriate for <10 patterns but should evolve to a configurable array or structured error types as the error surface grows.
- The global timeout (`SDK_EVAL_MAX_DURATION_MS`) forms a defence-in-depth pair with the classifier — catching false positives that would otherwise retry indefinitely.
- The ideal long-term direction is pushing classification to the error producer via `retryable: boolean` properties on structured error types.

### From Sub-2 (Backoff Parameter Tuning)
- The actual worst-case delay budget is **62s nominal**, not the 122s documented in the memory — the code throws at attempt 5 before computing a 6th delay. This off-by-one means the parameters are more conservative than intended.
- The `MAX_DELAY_MS=60000` cap is never reached under current parameters (max un-jittered delay at attempt 4 is 32s).
- The ±15% jitter is adequate for `maxForks: 2` (10% collision probability) but fails at 4+ forks (56%). Widening to ±50% or switching to decorrelated jitter would allow safe parallelism increase.
- A base delay of 5s with 4 retries would maintain the same total budget while reducing wasted attempts against 10–60s rate-limit windows.
- The shared-agent-runs pattern is a structural prerequisite for the narrow jitter — without it, effective concurrency would exceed what ±15% jitter can safely desynchronise.

### From Sub-3 (Reactive + Proactive Pairing)
- The four-layer stack (demand reduction → concurrency limiting → reactive retry → hard deadline) operates as defence-in-depth where each layer catches what the previous misses.
- Retries are never vestigial — they function as both a recovery mechanism and a feedback signal for tuning proactive measures. Removing retries breaks the feedback loop.
- The "reduce forks rather than increase retries" guideline generalises to "reduce demand rather than increase tolerance" — a principle that applies to production API clients, multi-agent orchestration, and connection pool management.
- Skip-by-default creates a bimodal profile where retry importance is inversely proportional to proactive gating effectiveness.
- Concurrency limits, like session flags, need explicit inheritance contracts in multi-agent systems — a parent limiting to maxForks: 2 is undermined if child agents each spawn their own parallel work.

## Summary

The CRUX harness implements a mature four-layer resilience stack: demand reduction (shared runs, skip gating) → concurrency limiting (maxForks: 2, phased execution) → reactive retry (exponential backoff + jitter on rate-limit detection) → hard backstop (global wall-clock deadline). The actual retry budget is 62s nominal, not the documented 122s, leaving 75%+ of test timeout for real operations. Three improvement opportunities emerged: (1) widen jitter from ±15% to ±50% or decorrelated to enable safe fork-count increase, (2) raise base delay from 2s to 5s to reduce wasted retries against typical rate-limit windows, (3) evolve the binary error classifier toward a three-tier model (definitely transient / probably transient / definitely permanent) for broader error coverage. The deepest insight is that reactive retries and proactive measures form a feedback loop — retry frequency is the signal that tells you whether your proactive settings are correct — making retries essential even when proactive measures work perfectly. The "reduce demand rather than increase tolerance" principle generalises from test harnesses to any agent orchestration system hitting resource limits.
