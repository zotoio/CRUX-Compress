---
branch: 3
depth: 3
subfocus_index: 5
subfocus: "Conservative starting parallelism as a design pattern"
parent_subfocus: "Concurrency control patterns for bounded parallel agent execution"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

The codebase codifies `maxForks: 2` as the starting parallelism and prescribes a specific scaling protocol. This leaf examines *why* 2 is the safe default (not 1, not 3) and what constitutes a principled — rather than trial-and-error — protocol for increasing concurrency.

## Discoveries

### From memory corpus

- **`6265f8f`** (rate-limit retry): Explicitly states "maxForks: 2 is a safe starting point for a 7-9 file suite" and outlines a three-step scaling rule: (1) start at 2, (2) scale to 3-4 only after a full validation run shows zero rate-limit retries, (3) if retries become frequent at any fork count, reduce rather than add more retries.
- **`efc4c24`** (per-phase parallel execution): Validates that 3 parallel subagents per phase achieve near-linear speedup with no coordination overhead — but this is spec executor phases (independent subtasks), not API-bound eval forks.
- **`e05030c`** (expensive SDK evals): Documents that Meditate spawns up to 13 agents across the recursion tree. This is a fixed fan-out architecture (3×3+3+1), not a dynamically tunable concurrency level.
- **`6415c52`** (shared agent runs): Demonstrates that the primary cost-reduction lever is batching assertions per agent invocation (N→1), not increasing parallelism. This suggests the ecosystem defaults to *reducing* concurrent demand rather than scaling up.
- **`ba74013`** (session-scope subagent patterns): Shows that even non-API concerns (flag inheritance, context propagation) get harder with higher concurrency — each additional fork multiplies the surface area for silent behavioral violations.

### From codebase evidence

- `evals/sdk/vitest.config.ts`: `maxForks: 2` with no conditional or environment-driven override. The value is static — a deliberate architectural decision, not a temporary development constraint.
- The spec assessment (finding F7) explicitly flagged `maxForks: 4` as risky: "may exhaust system resources with 4 concurrent agent SDK sessions." The decision was to halve it preemptively.
- The retry helper has 5 retries with exponential backoff up to 60s — but the commentary emphasizes that retry is *reactive* and reducing concurrency is the *proactive* control. This hierarchy matters: prevention over mitigation.

### Analysis: why 2, not 1 or 3

**Why not 1** (serial):
- The memory explicitly notes: "Single-fork only → wall-clock cost of full suite balloons to 50+ minutes." Serial execution pays a prohibitive latency tax when suites contain 7-9 test files, each taking 30-120 seconds of API time.
- 1 fork provides zero information about rate-limit behaviour under concurrency. You can't validate your retry logic without at least 2 concurrent sessions.

**Why not 3** (or higher starting point):
- API rate limits are opaque: providers don't publish per-account concurrent session caps, and these caps may change without notice. Starting at N=3 means your *first* full suite run might hit limits, giving you no clean baseline.
- Diagnosing rate-limit errors at N=3 is ambiguous: was it the 3rd fork, or would 2 also have hit the limit on a different day? Starting at 2 and getting clean runs establishes a reliable floor.
- Each additional fork compounds: 2→3 is +50% concurrent API load, not +33%. The marginal rate-limit risk is non-linear because API quotas are typically window-based (requests per minute), not instantaneous.

**Why 2 works universally as a starting point:**
1. **Minimally concurrent**: 2 is the smallest number that exercises concurrency paths (race conditions, retry logic, jitter effectiveness) while keeping API pressure low.
2. **Diagnostic clarity**: If rate limits occur at 2 forks, the problem is the API quota, not your concurrency choice. You know immediately to fix upstream (get higher limits) rather than tune downstream.
3. **Fast enough**: For suites of 7-9 files at 60-120s each, 2 forks yield 3.5-4.5 minute wall-clock vs 7-9 minutes serial. The 2× speedup is sufficient for development iteration without entering risky territory.
4. **Observable baseline**: A clean run at 2 forks (zero retries) is the gate condition for scaling. Without this baseline, any scaling decision is guesswork.

## Connections

### The scaling protocol is observation-driven, not formula-driven

The codebase reveals a specific protocol structure:

```
1. Start at 2 (establish baseline)
2. Run a FULL validation pass (not a subset — all files, all scenarios)
3. Gate condition: ZERO rate-limit retries in the full pass
4. If gate passes: increment by 1 (to 3)
5. Repeat: full validation pass at new level
6. Gate condition: still zero retries
7. If gate fails at any level: decrement, don't add retries
```

This is a **ratchet protocol** — you can only move up one step at a time, each step requires a full clean validation, and the response to failure is always "step back" rather than "compensate with retries." It's conservative by design because:

- **Retries mask problems**: Adding retries at a higher fork count hides the signal that you've exceeded sustainable concurrency. The system appears to work (tests pass) but is burning extra time, API budget, and hiding fragility.
- **Full validation vs spot-checking**: The protocol demands a complete suite run because rate limits are window-based. A subset might pass at N=3 simply because fewer total requests fit within the rate window. Only a full run exercises the cumulative request pattern.

### Connection to the broader harness design

The conservative starting point reflects a deeper principle visible across the codebase: **prefer reducing demand over increasing tolerance**:

- `6415c52` reduces N API calls to 1 (demand reduction via shared runs)
- `e05030c` gates expensive tests behind skip-by-default (demand reduction via opt-in)
- `6265f8f` pairs retry (tolerance) with `maxForks: 2` (demand reduction)
- The spec executor uses 2-3 agents per phase (demand bounded by dependency graph)

The pattern: the system always reduces demand first, then adds tolerance mechanisms for the residual unavoidable transient failures. Tolerance (retry) is the last resort, never the primary strategy.

### Provider-dependence vs universality

The protocol is universal in *structure* (start low, validate, increment, never compensate with retries) but the *specific numbers* are provider-dependent:
- For Cursor's API with typical per-account rate limits: 2 is correct
- For a provider with higher rate limits or per-request (not per-session) throttling: 3-4 might be safe as a starting point
- For expensive models (opus-class): 2 may need to drop to 1 due to per-model caps

The universality is the *method* (empirical ratchet), not the *starting value* (2). But 2 is an excellent heuristic because it's the minimum value that exercises concurrency.

## Summary

`maxForks: 2` is the universal starting point because it's the minimum concurrency level that exercises real concurrent behavior (retry paths, jitter effectiveness, race conditions) while maintaining diagnostic clarity — if rate limits occur at 2, the problem is upstream quotas, not your architecture. The scaling protocol is an observation-gated ratchet: increment by 1, run a full validation pass demanding zero retries, step back on any failure. The philosophical commitment is "reduce demand before increasing tolerance" — retries compensate for residual transient failures at a validated concurrency level, never substitute for finding the right concurrency level. The number 2 is empirically optimal for typical LLM API rate-limit windows, but the *method* (empirical ratchet with full-suite validation gates) is the universal contribution.
