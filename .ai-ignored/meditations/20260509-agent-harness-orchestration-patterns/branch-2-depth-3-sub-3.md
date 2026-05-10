---
branch: 2
depth: 3
subfocus_index: 3
subfocus: "Pairing Reactive Retries with Proactive Concurrency Reduction"
parent_subfocus: "Retry Strategies and Transient Error Recovery"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

Reactive retries and proactive concurrency reduction are often designed independently, but their interaction determines whether the overall resilience model is redundant, synergistic, or counterproductive. Understanding how these two strategy families compose — and whether retries become vestigial when proactive measures succeed — is essential for deciding where to invest engineering effort in any multi-agent orchestration system.

## Discoveries

### 1. The CRUX harness implements a three-layer resilience stack

The codebase reveals three distinct resilience layers operating simultaneously:

| Layer | Strategy | Mechanism | Memory Source |
|-------|----------|-----------|---------------|
| **Proactive demand reduction** | Shared-agent-runs, skip-by-default gating | Reduce the number of API calls that occur at all | `6415c52`, `e05030c` |
| **Proactive concurrency limiting** | Conservative `maxForks: 2`, dependency-based phasing | Reduce how many calls happen *simultaneously* | `6265f8f`, `efc4c24` |
| **Reactive recovery** | Exponential backoff + jitter, per-attempt rate-limit detection | Recover when limits are hit despite proactive measures | `6265f8f` (harness.ts) |
| **Hard backstop** | Global wall-clock deadline (`SDK_EVAL_MAX_DURATION_MS`) | Kill everything if the reactive layer loops too long | `e05030c` |

These layers are not alternatives — they are a defense-in-depth stack where each layer catches what the previous one misses. [memory:Exponential backoff with jitter on rate-limit errors] [memory:Shared-agent-runs-per-describe-block reduce API cost] [memory:Gate expensive SDK evals behind SDK_EVAL_SKIP_EXPENSIVE]

### 2. Retries are NOT vestigial — they are insurance against irreducible variance

Even when proactive measures work perfectly, retries remain necessary because:

- **API rate limits are shared resources**: other clients hit the same endpoint, so your proactive measures only control your own contribution to the load, not the total load the server sees
- **Rate-limit windows are non-deterministic**: a burst of unrelated traffic can push you over the limit even at `maxForks: 1`
- **Proactive measures have configuration lag**: the guideline "scale to 3-4 only after a full validation run shows no rate-limit retries occurring" from `6265f8f` explicitly uses retry frequency as a *feedback signal* — if retries never fire, that's how you know the proactive settings are correct. Removing retries removes the signal.
- **Transient infrastructure events** (deploy rollouts, load balancer reconfigs, DNS hiccups) are outside proactive control

The retries are the canary, not just the recovery mechanism. A harness that only proactively limits concurrency without reactive retries would fail silently on transient spikes rather than recovering and logging the event.

### 3. Shared-agent-runs are demand reduction, not concurrency reduction — a critical distinction

Memory `6415c52` describes a pattern where N assertions share 1 agent call in `beforeAll`. This is **demand reduction** — it eliminates API calls entirely, reducing N calls to 1. This is fundamentally different from `maxForks` which is **concurrency reduction** — the same total work, spread over fewer simultaneous slots.

The distinction matters because:
- Demand reduction **multiplicatively** reduces both cost and rate-limit probability (3-6x fewer calls = 3-6x fewer chances to hit limits)
- Concurrency reduction **additively** reduces rate-limit probability per window (fewer simultaneous calls = lower peak request rate, but total calls unchanged)
- The two compose multiplicatively: 6x demand reduction × 2-fork concurrency limit = 12x reduction in rate-limit probability vs unbatched 4-fork execution

### 4. Skip-by-default creates a bimodal retry profile

Memory `e05030c` reveals that the skip-by-default gate for expensive tests (Meditate: up to 13 agents, Integration: 5+ turns) creates two distinct runtime profiles:

- **Default mode** (`pnpm test`): only cheap single-turn tests run. Rate limits are rare. The retry mechanism fires infrequently — it's almost entirely insurance.
- **Expensive mode** (`pnpm test:meditate`): recursive multi-agent tests run. Each test spawns up to 13 agent invocations. Rate limits are likely. The retry mechanism becomes load-bearing.

This means the retry mechanism's importance is *inversely proportional to the effectiveness of skip-by-default gating*. When the gate is working (default mode), retries are insurance. When the gate is bypassed (explicit expensive runs), retries are essential. The system correctly pairs "you're opting into expensive work" with "the safety net is proportionally more important."

### 5. The tension: fewer forks vs wall-clock deadlines

Proactive concurrency reduction (`maxForks: 2`) and wall-clock deadlines (`SDK_EVAL_MAX_DURATION_MS: 60min`) create a fundamental tension:

- Reducing forks increases total wall-clock time (serial execution of what could be parallel)
- Wall-clock deadlines cap total execution time
- At some fork count, the suite can't finish within the deadline

The CRUX harness resolves this by making the deadline generous (60 minutes) relative to suite size. But the tension generalises: in production multi-agent orchestration, reducing concurrency to avoid rate limits extends time-to-completion, which may violate SLAs or user expectations. The optimal fork count sits at the intersection of "low enough to avoid rate limits" and "high enough to finish within the deadline."

### 6. The "reduce forks rather than increase retries" guideline generalises as "reduce demand rather than increase tolerance"

The memory `6265f8f` states: *"If retries become frequent at any fork count, reduce parallelism rather than increasing retries."* This is a specific instance of a general principle:

**When a system hits resource limits, prefer reducing the demand on the resource over increasing the system's tolerance for resource exhaustion.**

This generalises beyond test harnesses:
- **Production API clients**: reduce request rate (batching, caching, debouncing) before increasing retry budgets
- **Multi-agent orchestration**: reduce agent count or consolidate agent workloads before extending timeout budgets
- **Database connection pools**: reduce query volume (caching, read replicas) before increasing pool size limits
- **CI/CD pipelines**: reduce parallel job count before extending queue timeout

The principle works because demand reduction attacks the *cause* (too many requests), while tolerance increase attacks the *symptom* (failed requests). Tolerance measures have diminishing returns (more retries = longer delays, higher cost, potential thundering herd), while demand reduction can have compounding returns (fewer calls = lower cost AND fewer failures AND shorter total time if the eliminated calls were redundant).

### 7. Session-scope flag propagation applies to concurrency limits

Memory `ba74013` describes how session flags must be inherited by subagents. This pattern extends to concurrency limits: if a parent agent determines that `maxForks: 2` is the safe operating point, but spawns subagents that each spawn their own parallel work at `maxForks: 4`, the total concurrency exceeds the parent's intent. Concurrency budgets, like session flags, need explicit inheritance contracts documented in alwaysApply rules. [memory:Session-scope command design: in-band handling and subagent inheritance]

## Connections

### Reactive-proactive synergy, not redundancy

The reactive and proactive layers are not redundant — they form a feedback loop:
1. **Proactive measures set the operating point** (how many forks, which tests to skip, how to batch)
2. **Reactive retries provide the feedback signal** (retry frequency tells you if the operating point is correct)
3. **The operating point adjusts based on feedback** ("scale to 3-4 only after a full validation run shows no rate-limit retries occurring")

Removing retries breaks the feedback loop. Removing proactive measures makes retries the primary load-bearing mechanism, which is fragile (retry storms, thundering herds, cascading timeouts).

### Advisory gates pattern mirrors skip-by-default

Memory `b0c02ea` describes advisory quality gates (`failClosed: false`) that warn but preserve output. The skip-by-default pattern for expensive tests is structurally identical: the default is safe (skip/warn), the user opts into risk explicitly. Both patterns follow the same principle: **progressive enhancement with explicit opt-in for expensive operations**. This creates a design vocabulary that spans plugins (advisory gates), test harness (skip-by-default), and potentially production orchestration (conservative defaults with explicit escalation). [memory:Plugin design patterns: advisory gates and progressive enhancement defaults]

### Concurrency as a propagating constraint

The combination of `maxForks` (vitest config), shared-agent-runs (test design), skip-by-default (test gating), and wall-clock deadlines (backstop) shows that concurrency management in agent harnesses is not a single knob but a *constraint that propagates through multiple system layers*. Each layer has its own mechanism, but they must be coherent — a generous `maxForks` undermines careful demand reduction, and an aggressive skip-gate makes the retry mechanism vestigial in normal operation but essential in explicit-run mode.

## Summary

The CRUX harness implements a four-layer resilience stack (demand reduction → concurrency limiting → reactive retry → hard deadline) where each layer handles what the previous misses. Retries are never vestigial — they serve as both recovery mechanism and feedback signal for tuning proactive measures. The key insight is that reactive and proactive strategies form a feedback loop: retry frequency tells you whether your proactive settings are correct, so removing retries breaks the tuning mechanism even if they rarely fire. The "reduce forks rather than increase retries" guideline generalises to "reduce demand rather than increase tolerance" — a principle that applies to production API clients, multi-agent orchestration, and connection pool management. The interaction between skip-by-default gating and retries creates a bimodal profile where the retry mechanism's importance is inversely proportional to how much proactive gating is in effect. Concurrency is not a single knob but a propagating constraint across test design (shared runs), test selection (skip gates), runtime config (maxForks), and hard limits (wall-clock deadline) — all four must be coherent.
