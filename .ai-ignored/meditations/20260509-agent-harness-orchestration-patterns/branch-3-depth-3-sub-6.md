---
branch: 3
depth: 3
subfocus_index: 6
subfocus: "Thundering-herd avoidance in bounded-width agent pools"
parent_subfocus: "Concurrency control patterns for bounded parallel agent execution"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

The parent subfocus covers concurrency control broadly — fan-out width caps, conservative starting parallelism, throughput vs rate-limit trade-offs. This leaf zooms in specifically on the failure-synchronisation problem: when multiple agents in a bounded pool hit the same rate limit simultaneously, their retries can correlate and create a self-reinforcing cycle of failures. This is the thundering-herd problem applied to agent pools, and it requires distinct mitigation patterns beyond simply limiting fan-out width.

## Discoveries

### Existing Reactive Pattern: Exponential Backoff with Jitter

[memory:Exponential backoff with jitter on rate-limit errors] The codebase has a concrete implementation in `evals/sdk/helpers/harness.ts`. The `backoffDelay()` function applies ±15% jitter (multiplier in `[0.85, 1.15]`) to exponentially-growing delays (`BASE_DELAY_MS=2000`, `MAX_DELAY_MS=60000`). The memory `6265f8f` explicitly documents why this works: "at the cap, two simultaneously-throttled forks won't retry within the same 9-second window."

The jitter window was chosen deliberately. At attempt 5 (the cap), un-jittered delay would be `2000 × 2^5 = 64000ms`, clamped to 60000ms. With the ±15% jitter, actual waits span `[51000, 60000]` — a 9-second spread. For 2 concurrent forks, this gives roughly a 50% chance of non-collision. For wider fan-outs (3+ forks), the collision probability rises quadratically — this is the birthday-problem dynamic that makes jitter alone insufficient at scale.

### The Fixed-Delay Anti-Pattern

The memory explicitly rejects fixed-delay retry: "All forks retry simultaneously → thundering herd hits the limit again." This is the textbook thundering-herd scenario — N agents fail at time T, all sleep for D milliseconds, all retry at time T+D, all fail again. The exponential component ensures that even without jitter, successive retries diverge. Jitter then prevents the residual correlation from the shared exponential base.

### The Gap: No Proactive Patterns Exist

The codebase currently handles thundering-herd **only reactively** — after rate limits are hit. Four proactive patterns are absent:

**1. Staggered Initial Starts**

The Meditate command (documented in `.cursor/agents/crux-cursor-memory-manager.md`) launches all 3 branch agents simultaneously at each recursion depth. At depth 0 → 3 agents start concurrently. Each of those spawns 3 more (depth 1 → up to 9 concurrent). Each of those spawns 3 more (depth 2 → up to 27 concurrent in worst case). There is no inter-launch delay.

[memory:Gate expensive SDK evals] Memory `e05030c` notes that Meditate spawns up to 13 agents per test, implying the cascade creates significant rate-limit pressure. Staggered starts would spread initial API contact across a time window, reducing the probability that multiple agents hit the same rate-limit bucket simultaneously.

A stagger pattern for 3-agent fan-out might look like: launch agent 1 immediately, agent 2 after 500ms, agent 3 after 1000ms. The total launch window (1 second) is negligible relative to agent execution time (60-120 seconds) but spreads the initial API authentication and first-message bursts across different rate-limit windows.

**2. Admission Queuing (Semaphore with Spacing)**

The vitest config uses `maxForks: 2` as a static cap, but this is a process-level bound, not an application-level admission queue. A proper admission queue would:
- Maintain a semaphore of width W (the pool size)
- Add a minimum spacing between semaphore acquisitions (e.g. 200ms between consecutive starts)
- Optionally implement "slow start" — begin with W=1, increase to target only after the first agent succeeds without rate-limiting

This is analogous to TCP slow-start: don't assume the full window is available, probe capacity incrementally. [memory:Per-phase parallel subagent execution] Memory `efc4c24` shows the spec execution system already phases work (3 parallel agents per phase), but phases are separated by dependency barriers, not by explicit spacing. Adding intra-phase spacing would be a small refinement with outsized impact on rate-limit pressure.

**3. Correlated Failure Detection**

No code in the codebase detects correlated failures across agents. When 2 of 3 parallel agents hit rate limits within the same time window, this is strong evidence of systemic rate-limit pressure rather than isolated transient errors. A correlated-failure detector would:
- Track rate-limit errors across all agents in the pool (requires shared state or a coordination file)
- When `K` of `N` agents report rate-limit errors within a window `W`, trigger global backoff: pause new launches and increase base delay for all agents
- Gradually resume normal operation after a cooldown period

This is the "circuit breaker" pattern applied at the pool level rather than per-agent. The codebase mentions circuit breakers in the spec fixture (`n-integration.test.ts`) for external service calls, but doesn't apply the concept to the agent pool itself.

**4. Fan-out Width × Thundering-Herd Probability**

The relationship is super-linear. For a pool of N agents with independent jitter:
- Probability that any 2 agents retry within the same window scales as `O(N²)` (birthday problem)
- At N=2 (current `maxForks`), collision probability is modest
- At N=3 (Meditate's per-level fan-out), it roughly triples
- At N=9 (Meditate depth-1 total concurrent), the birthday-problem dynamic makes at least one collision near-certain

This means the jitter window that works for `maxForks: 2` is insufficient for Meditate's 9-agent concurrent case. Either the jitter window needs to scale with N, or the fan-out needs admission control.

### Shared-Run Pattern as Implicit Thundering-Herd Mitigation

[memory:Shared-agent-runs-per-describe-block reduce LLM eval cost] Memory `6415c52` documents the shared-`beforeAll` pattern where N assertions share 1 agent call. While designed for cost reduction, this pattern incidentally eliminates thundering-herd risk for the test suite — you can't have correlated retries if there's only 1 request. This is the ultimate thundering-herd avoidance: reduce N to 1.

### Session-Scope Inheritance as a Coordination Channel

[memory:Session-scope command design] Memory `ba74013` describes how session-scope flags propagate to subagents via `alwaysApply` rules. This inheritance mechanism could carry rate-limit state: if a parent agent detects rate-limit pressure, it could set a session flag that child agents read to add extra initial delay or reduce their own parallelism.

## Connections

**Jitter as a specific case of decorrelation**: The ±15% jitter in `backoffDelay()` is one instance of a general principle — when N independent actors might synchronise, inject per-actor randomness proportional to the population size. The current fixed 30% window works for N=2 but the window should widen as N grows. A formula like `jitter_range = 0.3 * sqrt(N)` would scale the decorrelation window with pool size.

**Meditate is the worst case for the current design**: The Meditate command creates a tree of agents (up to 13 total, with 9 potentially concurrent at depth-2) but uses zero proactive thundering-herd mitigation. It relies entirely on per-agent reactive retry. This works in practice because (a) most meditation agents are memory-search-heavy, not API-call-heavy, and (b) the `SDK_EVAL_SKIP_EXPENSIVE` gate means this path rarely runs. But for a production agent harness, this gap would be critical.

**File-based coordination enables pool-level circuit breaking**: The Meditate command already uses file-based coordination (agents write markdown files, parents poll for existence). This same mechanism could carry rate-limit signals: an agent that hits a rate limit writes a `rate-limit-{timestamp}.signal` file; sibling agents check for recent signal files before making API calls and add delay if any exist. No shared memory or IPC needed — the filesystem is the coordination bus.

**The cost-gate is an admission queue in disguise**: `SDK_EVAL_SKIP_EXPENSIVE` prevents the most agent-heavy tests from running by default. This is a binary admission decision (run or don't run) rather than a graduated queue, but it serves the same purpose — it limits the total concurrent agent population to what the rate limits can sustain under normal `pnpm test` runs.

**TCP congestion control as the meta-pattern**: The full set of desired patterns maps to TCP's congestion control evolution:
- Slow start → conservative `maxForks: 2`, increase empirically
- AIMD (additive increase, multiplicative decrease) → the exponential backoff with jitter
- Fast retransmit → correlated failure detection triggering pool-level backoff
- Congestion window → admission semaphore with dynamic width
- ECN (explicit congestion notification) → file-based rate-limit signals between agents

## Summary

The codebase has a solid reactive thundering-herd mitigation (exponential backoff + ±15% jitter in `harness.ts`) that works well for the current `maxForks: 2` case. The jitter window spreads retries across 9 seconds at the delay cap, making collision unlikely for 2 forks. However, four proactive patterns are absent: (1) staggered initial starts for fan-out launches, (2) admission queuing with inter-launch spacing and slow-start, (3) correlated failure detection triggering pool-level backoff, and (4) dynamic jitter windows that scale with pool size. These gaps are most acute in the Meditate command's 13-agent tree (up to 9 concurrent at peak), where the birthday-problem dynamic makes retry collisions near-certain with the current fixed jitter window. The existing file-based coordination mechanism provides a natural substrate for pool-level rate-limit signalling without requiring shared memory. The overall pattern space maps closely to TCP congestion control — slow start, AIMD, fast retransmit, and explicit congestion notification — suggesting that the networking community's decades of work on this problem offers directly applicable solutions.
