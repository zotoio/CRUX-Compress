---
branch: 3
depth: 3
subfocus_index: 4
subfocus: "Static vs dynamic fan-out width caps"
parent_subfocus: "Concurrency control patterns for bounded parallel agent execution"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

The parent identified two concrete concurrency approaches in this codebase — fixed-value caps (vitest `maxForks: 2`, meditate's fixed 3-way fan-out) and empirically-guided scaling hints (memory `6265f8f`'s "scale to 3-4 after validation"). This leaf examines the decision framework for choosing between them: when is a static cap sufficient, and what conditions make a dynamic controller worth its complexity cost?

## Discoveries

### Static caps found in the codebase

Five distinct static concurrency caps exist in this repository, each chosen for different reasons:

| Location | Cap | Rationale pattern |
|----------|-----|-------------------|
| `evals/sdk/vitest.config.ts` | `maxForks: 2` | Conservative safety floor — rate-limit avoidance for external API |
| Meditate agent definition | 3-way fan-out per recursion level | Structural design constraint — three facets partition the topic space |
| Spec executor | Phase-based parallelism (3 subagents per phase) | Dependency-graph bounded — all agents within a phase are independent |
| `deploy-pages.yml` | `concurrency: group: "pages"` (1 at a time) | Mutual exclusion — deployment must be serialized, no parallelism at all |
| `SDK_EVAL_MAX_DURATION_MS` (60min backstop) | Time-based cap, not concurrency cap | Resource budget ceiling — prevents runaway cost regardless of parallelism |

### Adaptive/dynamic patterns found

Two quasi-adaptive patterns exist, though neither implements a true dynamic controller:

1. **Empirical scaling advice** (memory `6265f8f`): "Scale `maxForks` to 3-4 only after a full validation run shows no rate-limit retries occurring." This is human-in-the-loop adaptive — the cap is still static in config, but the human adjusts it based on observed outcomes. The feedback loop is offline (run → observe → edit config → re-run).

2. **Adaptive compression escalation** (memory `da3d798`, `crux-skill-memory-compress`): When compressed output exceeds `maxMemorySize`, the compression logic escalates aggressiveness by 10 percentage points and re-compresses. This is a genuine runtime-adaptive loop — try at target, check result, escalate if needed, flag for manual review if maximum compression still fails. The pattern is: attempt → measure → adapt → attempt → cap.

### Patterns NOT found

No implementation of AIMD, token bucket, adaptive semaphore, or runtime concurrency controllers exists in this codebase. The closest thing to closed-loop concurrency control is the `withRetry()` exponential backoff — but that's reactive error recovery, not proactive concurrency adjustment.

## Connections

### The adaptive compression pattern is a concurrency controller in disguise

Memory `da3d798`'s adaptive compression escalation implements the same abstract pattern a dynamic concurrency controller would use:

1. Start with a default target (compression ratio 33% ≈ `maxForks: 2`)
2. Execute with that target
3. Measure the outcome against a hard constraint (`maxMemorySize` ≈ rate-limit budget)
4. If constraint violated, tighten the parameter (reduce target by 10pp ≈ reduce concurrency by 1)
5. Retry with the tighter parameter
6. If maximum tightening still violates the constraint, escalate to human review (≈ alert + manual override)

This is the AIMD "decrease" half — multiplicative decrease on constraint violation. The "increase" half (probing upward when conditions are good) exists only in the human-in-the-loop advice from memory `6265f8f`: "scale to 3-4 after a validation run shows no retries."

### Static caps work when the constraint is structural, not environmental

The three-way meditate fan-out is static because the constraint is *information-theoretic*, not resource-based. Three facets partition a topic's exploration space. Adding a fourth doesn't help (overlap increases, depth decreases); reducing to two loses coverage. The number is driven by the problem structure, not by system capacity.

Similarly, the spec executor's phase parallelism is static because it's *dependency-graph bounded*. The number of parallel agents equals the number of independent subtasks in the phase — determined at planning time, not runtime.

In contrast, `maxForks: 2` for the eval harness is static only because no one has built the dynamic version yet. The constraint is environmental (API rate limits), stochastic (depends on API server load), and variable (different times of day, different account tiers). This is exactly the regime where a dynamic controller would add value.

### A decision framework emerges

The choice framework has two axes:

**Axis 1: Is the constraint structural or environmental?**
- *Structural* (dependency graph, information partitioning, mutual exclusion): static cap is correct. The cap derives from the problem shape, not from runtime conditions. A dynamic controller would add complexity with no benefit.
- *Environmental* (rate limits, resource contention, variable latency): dynamic cap can add value. The optimal concurrency depends on conditions unknowable at config time.

**Axis 2: Is the cost of getting the cap wrong high or low?**
- *Low cost* (retries are cheap, wall-clock impact is small): static cap with conservative floor. The `maxForks: 2` pattern — pick a safe low number, accept suboptimal throughput, scale manually when proven safe.
- *High cost* (each wasted fork costs real money, or a too-low cap means 10x wall-clock): dynamic cap is worth the complexity. The adaptive compression pattern — try, measure, adjust, retry.

The quadrant:

| | Structural constraint | Environmental constraint |
|---|---|---|
| **Low cost of error** | Static, derived from problem shape (meditate 3-way) | Static conservative floor + manual tuning (maxForks: 2) |
| **High cost of error** | Static, derived from dependency graph (spec phases) | Dynamic controller (adaptive compression pattern → AIMD/token bucket) |

### Session-scope inheritance (memory `ba74013`) creates a hidden static cap

When subagents must inherit parent session state, the orchestrator implicitly caps concurrency at "however many subagents the harness can spawn while maintaining state coherence." This is a static cap imposed by architecture rather than explicit configuration. If session state is mutable (e.g., a flag that changes during execution), the cap effectively becomes 1 (serialize) unless the harness can snapshot state at spawn time.

### The exponential backoff in `withRetry()` is the wrong layer for concurrency control

Memory `6265f8f` pairs backoff with conservative parallelism, but the backoff operates *per-request* while the concurrency cap operates *per-suite*. These are different feedback loops with different time constants. The backoff reacts to individual failures in seconds; the concurrency cap should react to aggregate pressure over the duration of a suite run. A true dynamic concurrency controller would sit between these two layers — slower than per-request retry, faster than human config editing.

## Summary

This codebase uses exclusively static concurrency caps, but for fundamentally different reasons: structural caps (meditate's 3-way fan-out, spec executor's phase parallelism) are correct because the problem shape determines the number; conservative-floor caps (`maxForks: 2`) are pragmatic but suboptimal, compensating for the absence of dynamic control with retry-layer backoff. The adaptive compression pattern in `crux-skill-memory-compress` provides a template for what a dynamic concurrency controller would look like: attempt → measure → escalate → retry → flag-for-human. The key decision framework is: static caps are appropriate when the constraint is structural (problem-derived) or the cost of suboptimal throughput is low; dynamic caps are justified when the constraint is environmental (rate limits, variable load) AND the cost of getting the cap wrong is high enough to justify the implementation complexity.
