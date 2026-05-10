---
branch: 3
depth: 2
subfocus_index: 2
subfocus: "Concurrency control patterns for bounded parallel agent execution"
parent_subfocus: "Resource Governance and Bounded Execution"
timestamp: 2026-05-09T19:39:00+10:00
---

## Subfocus Rationale

The parent facet covers resource governance broadly — cost tiers, size limits, deadlines, adaptive escalation. This branch narrows to the specific question of how many agents should run simultaneously and what controls prevent that number from causing systemic failures. Concurrency is the primary multiplier of both throughput and rate-limit pressure in agent harnesses, making it the highest-leverage governance parameter to get right.

## Discoveries

### Five static concurrency caps coexist in this codebase

The repository uses five distinct static caps, each justified by a different constraint type:

| Location | Cap | Constraint Type |
|----------|-----|----------------|
| `evals/sdk/vitest.config.ts` | `maxForks: 2` | Environmental — API rate limits |
| Meditate agent definition | 3-way fan-out per recursion level | Structural — topic space partitioning |
| Spec executor | 2-3 agents per phase | Structural — dependency graph |
| `deploy-pages.yml` | 1 (mutual exclusion) | Structural — deployment serialisation |
| `SDK_EVAL_MAX_DURATION_MS` | 60-minute wall-clock cap | Budget — cost ceiling regardless of parallelism |

No dynamic concurrency controllers (AIMD, token bucket, adaptive semaphore) exist. The closest adaptive pattern is the human-in-the-loop scaling advice: "scale maxForks to 3-4 only after a full validation run shows zero rate-limit retries."

### The retry layer and the concurrency layer are distinct control loops

Memory `6265f8f` pairs per-request exponential backoff with a suite-level static `maxForks`. These operate at different timescales: backoff reacts to individual failures in seconds; concurrency caps should respond to aggregate pressure across minutes. The codebase currently has no controller between these two layers — the gap where a dynamic concurrency adjuster would sit.

### The memory corpus encodes a consistent design philosophy: reduce demand before increasing tolerance

- `6415c52`: Shared agent runs collapse N API calls to 1 (demand reduction)
- `e05030c`: Skip-by-default gates exclude expensive tests (demand reduction)
- `6265f8f`: Conservative `maxForks: 2` paired with retry as last resort (demand reduction + residual tolerance)
- `efc4c24`: Phase-based parallelism bounded by dependency graph (demand bounded by structure)

Tolerance mechanisms (retries, backoff, jitter) handle residual transient failures at a validated demand level. They never substitute for finding the right demand level.

## Connections

### The adaptive compression pattern is a concurrency controller template

Memory `da3d798` describes adaptive compression escalation: try at target → measure outcome → if constraint violated, tighten by 10pp → retry → flag for human if max tightening still fails. This is the AIMD "decrease" half applied to file size rather than concurrency. The same pattern transplants directly to agent pools: run at concurrency N → if rate-limit rate exceeds threshold, reduce to N-1 → if zero rate limits at N for a full validation run, try N+1.

### Static caps are correct when constraints are structural; dynamic caps add value when constraints are environmental

The three-way meditate fan-out is static because the constraint is information-theoretic (three facets partition the topic space). The spec executor's phase parallelism is static because it's dependency-graph bounded. Both derive from problem shape, not runtime conditions. A dynamic controller would add complexity with no benefit.

In contrast, `maxForks: 2` for the eval harness is static only because the dynamic version hasn't been built yet. The constraint (API rate limits) is stochastic, variable, and external. This is exactly the regime where dynamic control would help.

### The empirical ratchet protocol is well-defined but manual

The scaling protocol encoded in memory `6265f8f` is: start at 2 → run full validation → require zero retries → increment by 1 → repeat. Failure at any level means step back, never compensate with more retries. This is the correct logic for a dynamic controller, just executed by humans editing config files instead of by runtime code.

## Child Subfocuses

Three narrower threads were explored at depth 3:

1. **Static vs dynamic fan-out width caps** (sub-4): Decision framework for choosing between fixed and adaptive concurrency. Key finding: a two-axis framework (structural vs environmental constraint × cost of error) determines when static caps suffice and when dynamic control is worth its complexity.

2. **Conservative starting parallelism as a design pattern** (sub-5): Why `maxForks: 2` is the universal starting point and what the empirical scaling protocol looks like. Key finding: 2 is the minimum concurrency that exercises real concurrent behaviour while maintaining diagnostic clarity. The scaling protocol is an observation-gated ratchet: increment by 1, full validation pass, zero retries required, step back on failure.

3. **Thundering-herd avoidance in bounded-width agent pools** (sub-6): How jitter, staggered starts, and admission control prevent correlated failures. Key finding: the existing ±15% jitter works for N=2 forks but collision probability scales as O(N²) (birthday problem), making it insufficient for Meditate's 9-concurrent-agent case. Four proactive patterns are absent: staggered starts, admission queuing with slow-start, correlated failure detection, and dynamic jitter windows.

## Child Insights

### Sub-4: Static vs Dynamic Fan-Out Width Caps

A two-axis decision framework emerged:

| | Structural Constraint | Environmental Constraint |
|---|---|---|
| **Low cost of error** | Static, derived from problem shape (meditate 3-way) | Static conservative floor + manual tuning (maxForks: 2) |
| **High cost of error** | Static, derived from dependency graph (spec phases) | Dynamic controller (AIMD / token bucket) |

The adaptive compression escalation pattern (`da3d798`) provides the template for dynamic concurrency: attempt → measure → escalate → retry → flag-for-human. Session-scope inheritance (`ba74013`) creates a hidden static cap — mutable session state effectively serialises execution unless the harness snapshots state at spawn time. The exponential backoff in `withRetry()` operates at the wrong layer for concurrency control; a true dynamic controller would sit between per-request retry and human config editing.

### Sub-5: Conservative Starting Parallelism

`maxForks: 2` is correct because:
1. It's the minimum concurrency that exercises real concurrent behaviour (retry paths, jitter, races)
2. It provides diagnostic clarity — rate limits at 2 indicate an upstream quota problem, not a tuning problem
3. It gives a 2× speedup (sufficient for dev iteration) without entering risky territory
4. It establishes the observable baseline that gates all further scaling

The scaling protocol is a ratchet:
```
start at 2 → full validation → zero retries? → increment by 1 → repeat
failure at any level → step back, never compensate with more retries
```

This reflects the codebase-wide principle: reduce demand before increasing tolerance. Retries handle residual transient failures at a validated concurrency level, never substitute for finding the right level. The specific starting number (2) is provider-dependent, but the method (empirical ratchet with full-suite validation gates) is universal.

### Sub-6: Thundering-Herd Avoidance

The existing reactive mitigation (exponential backoff + ±15% jitter) works well for `maxForks: 2`, spreading retries across a 9-second window at the delay cap. But four proactive patterns are missing:

1. **Staggered initial starts**: Meditate launches all 3 branch agents simultaneously at each recursion depth. A 500ms inter-launch delay would spread initial API contact across different rate-limit windows at negligible cost to total execution time.

2. **Admission queuing with slow-start**: A semaphore with inter-acquisition spacing and TCP-style slow-start (begin at W=1, probe up to target). The spec executor's dependency-phased approach approximates this but lacks explicit inter-phase spacing.

3. **Correlated failure detection**: When K of N agents hit rate limits within the same window, trigger pool-level backoff. The existing file-based coordination mechanism (agents write markdown files, parents poll) could carry rate-limit signals via `rate-limit-{timestamp}.signal` files — no shared memory needed.

4. **Dynamic jitter windows**: The fixed ±15% works at N=2 but collision probability scales quadratically. A formula like `jitter_range = 0.3 × sqrt(N)` would scale decorrelation with pool size.

The overall pattern space maps to TCP congestion control: slow start → conservative maxForks, AIMD → exponential backoff with jitter, fast retransmit → correlated failure detection, congestion window → admission semaphore, ECN → file-based rate-limit signals.

## Summary

Concurrency control in agent harnesses decomposes into three complementary patterns, each operating at a different level:

**Pattern 1 — Width selection**: Choose between static caps (correct when constraints are structural: dependency graphs, topic partitioning, mutual exclusion) and dynamic caps (valuable when constraints are environmental: rate limits, variable load). The decision framework is a 2×2 matrix of constraint-type × cost-of-error. This codebase currently uses only static caps.

**Pattern 2 — Starting point and scaling**: Begin at `maxForks: 2` as the minimum concurrency that exercises real concurrent behaviour. Scale via an observation-gated ratchet: increment by 1, full suite validation, zero retries required, step back on any failure. Never compensate for excessive concurrency with more retries — reduce demand before increasing tolerance.

**Pattern 3 — Failure decorrelation**: Prevent correlated retries from creating self-reinforcing failure cycles. The existing per-request jitter works at N=2 but four proactive techniques are absent — staggered starts, admission queuing, correlated failure detection, and scaling jitter windows. The file-based coordination already used for agent output can serve as the substrate for pool-level rate-limit signalling, and TCP congestion control offers a well-proven template for the full control architecture.

The deepest insight: concurrency control is not a single parameter (`maxForks`) but a three-layer system — demand reduction (shared runs, skip-by-default gating), proactive admission control (width selection, staggered starts, slow-start), and reactive recovery (backoff, jitter, correlated-failure circuit breaking). The codebase has strong implementations of layers 1 and 3 but layer 2 is nearly absent, representing the highest-value gap for future investment.
