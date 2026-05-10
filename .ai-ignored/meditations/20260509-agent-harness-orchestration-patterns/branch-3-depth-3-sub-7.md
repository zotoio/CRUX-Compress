---
branch: 3
depth: 3
subfocus_index: 7
subfocus: "Formal structure of the escalation ladder pattern"
parent_subfocus: "Hard resource caps composing with adaptive escalation strategies"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

The parent subfocus asks how hard caps compose with adaptive escalation. Before composability can be addressed, the escalation ladder itself needs a precise structural definition — its loop anatomy, decision points, terminal conditions, and the trigger that transitions from autonomous retry to user involvement. This subfocus provides that formalism by abstracting across the concrete instances in the codebase.

## Discoveries

### Concrete Escalation Ladders in the Codebase

Three distinct escalation ladder instances exist in CRUX-Compress, each with the same structural skeleton but different parameterisation:

**1. Adaptive compression sizing** (`.cursor/skills/crux-skill-memory-compress/SKILL.md`, step 6; memory `da3d798`):
- **Initial level**: compress at `compressionTarget` (33%)
- **Invariant check**: output ≤ `maxMemorySize` (1000 lines)?
- **Escalation function**: reduce target by 10 percentage points per iteration
- **Ceiling**: target reaches 5%
- **Terminal on failure**: flag for manual review; do NOT write the file
- **User surface**: the "flag" — system halts and presents the problem

**2. Exponential backoff with jitter** (`evals/sdk/helpers/harness.ts`; memory `6265f8f`):
- **Initial level**: attempt the operation immediately
- **Invariant check**: success, or non-rate-limit error? (non-rate-limit errors short-circuit out — only transient errors enter the ladder)
- **Escalation function**: `min(BASE * 2^attempt * jitter, MAX_DELAY)` — exponential with a multiplicative ceiling
- **Ceiling**: `attempt >= DEFAULT_MAX_RETRIES` (5)
- **Terminal on failure**: `throw err` — propagate to the caller
- **User surface**: error propagation to the test runner, which reports it

**3. Memory type demotion** (`.cursor/skills/crux-skill-memory-rebalance/SKILL.md`, steps 5-6):
- **Initial level**: memory at current type and strength
- **Invariant check**: has the memory been referenced within `demoteAfterDaysUnreferenced` (90 days)?
- **Escalation function**: type demotion chain: core → learning → idea → archived
- **Ceiling**: type-specific — `goal` types are never demoted
- **Terminal on failure**: goals flag for manual review; ideas skip demotion and go directly to archival
- **User surface**: all demotions require user confirmation in the REM sleep report

A fourth instance — **plugin advisory gates** (memory `b0c02ea`) — represents a degenerate ladder with only one rung: the system always warns and preserves output; the user opts into strictness. It is the zero-escalation baseline case where the system never autonomously increases aggressiveness.

### The Abstract Structure

Every escalation ladder is a bounded loop with five structural components and three decision points:

```
┌─────────────────────────────────────────────┐
│              ESCALATION LADDER               │
│                                              │
│  Parameters:                                 │
│    initial_level   — least aggressive setting │
│    step_function   — how to increase effort   │
│    ceiling         — max autonomous effort    │
│    invariant       — the constraint to satisfy│
│    terminal_action — what to do at ceiling    │
│                                              │
│  Loop:                                       │
│    level ← initial_level                     │
│                                              │
│    DP1: PRE-GATE                             │
│    │  Should we attempt at all?              │
│    │  (compressionMinLines, isRateLimitError)│
│    │  NO → exit with skip/throw             │
│                                              │
│    ┌──▶ ATTEMPT at current level             │
│    │    result ← execute(level)              │
│    │                                         │
│    │   DP2: INVARIANT CHECK                  │
│    │   │  Does result satisfy invariant?     │
│    │   │  YES → return result (success)      │
│    │   │  NO  → continue                     │
│    │                                         │
│    │   DP3: CEILING CHECK                    │
│    │   │  Has level reached ceiling?         │
│    │   │  NO  → level ← step_function(level) │
│    │   │        └──▶ loop back to ATTEMPT    │
│    │   │  YES → terminal_action(result)      │
│    │   │        (flag/throw/surface to user) │
│    └───┘                                     │
└─────────────────────────────────────────────┘
```

### Parameterisation Across Instances

| Parameter | Compression | Backoff | Demotion |
|-----------|------------|---------|----------|
| `initial_level` | 33% target | 0ms delay | current type |
| `step_function` | subtract 10pp | multiply by 2 + jitter | type chain lookup |
| `ceiling` | 5% target | 5 attempts / 60s max | `goal` (never demote) |
| `invariant` | output ≤ maxMemorySize | success or non-transient error | referenced within threshold |
| `terminal_action` | flag manual review | throw error | flag manual review |
| **step count** | 3 steps (33→23→13→3) | 5 steps | 3-4 steps (type-dependent) |
| **monotonicity** | decreasing (target %) | increasing (delay) | decreasing (type priority) |

### The Three Decision Points

**DP1 — Pre-gate**: Determines whether the ladder should be entered at all. This is a filter, not part of the loop. Examples: files below `compressionMinLines` skip the ladder entirely; non-rate-limit errors bypass the retry ladder and throw immediately. The pre-gate prevents the ladder from wasting effort on cases where escalation cannot help.

**DP2 — Invariant check**: The core test evaluated after every attempt. This is always a boolean predicate over the attempt's output. It must be cheap to evaluate relative to the attempt itself — the compression invariant is a line count, the backoff invariant is success/failure, the demotion invariant is a date comparison. Expensive invariants would make the ladder impractical.

**DP3 — Ceiling check**: Determines whether autonomous escalation should continue or the system should surface to the user. This is where the system's autonomy boundary lives. The ceiling is always a static, configuration-driven value — never dynamically computed from the attempt's result. This prevents the ladder from negotiating with itself about how hard to try.

### When the System Stops Escalating

The user-surfacing trigger is structurally simple: **ceiling reached AND invariant still violated**. But the codebase reveals two distinct terminal behaviours:

1. **Halt-and-report** (compression, demotion goals): The system stops, writes nothing destructive, and presents the situation to the user with options. The user decides the next action. This preserves the "never lose data silently" invariant because the system's autonomy ends before any irreversible action.

2. **Propagate-and-fail** (backoff): The system throws the error upward. The caller (test framework) handles reporting. This is appropriate when the escalation ladder is embedded inside a larger orchestration that has its own error handling — the ladder doesn't need to surface to the user directly because its caller will.

The choice between these two terminal modes correlates with data risk. When the ladder governs an operation that could lose data (compression writing a file, deleting a memory), the terminal is halt-and-report. When it governs a retriable, side-effect-free operation (an API call), the terminal is propagate-and-fail.

### Composability Properties

The ladder's composability comes from its interface: it takes a parameterised configuration and returns one of two outcomes — success (with the result) or failure (with the terminal state). This makes it embeddable:

- **Nesting**: A compression ladder can be nested inside a REM sleep loop that iterates over all memories. Each memory gets its own ladder instance. The outer loop's error handling consumes the inner ladder's terminal state.
- **Chaining**: A demotion ladder can feed into an archival ladder — if demotion doesn't satisfy the corpus-size invariant, archival is the next escalation tier.
- **Parallelism**: Independent ladders (one per memory file, one per API call) can run concurrently because they share no mutable state — each operates on its own `level` variable.

## Connections

**Escalation ladders are loop-with-bounded-exit patterns**. They are structurally identical to bounded retry loops in distributed systems, but the key insight from this codebase is that the "retry" can be *qualitative* (change the approach, not just wait longer). Compression escalation doesn't retry the same operation — it changes the compression parameters. Demotion escalation doesn't retry — it changes the memory's classification. Only backoff is a true "retry the same thing."

**The pre-gate is the ladder's type system**. It classifies inputs into "ladder-appropriate" (transient errors, large files) and "ladder-inappropriate" (programming errors, small files). Without the pre-gate, the ladder masks real problems by treating them as escalation opportunities.

**Static ceilings prevent negotiation loops**. A critical design choice: the ceiling is always a config constant (5%, 5 retries, `goal` type), never derived from the current attempt. If the ceiling were dynamic (e.g., "keep trying as long as each attempt shows improvement"), the ladder could theoretically run indefinitely on marginal improvements. The static ceiling is what makes the pattern *decidable* — the maximum cost is always known in advance.

**Advisory gates are degenerate ladders**. The plugin advisory pattern (memory `b0c02ea`) is an escalation ladder with `ceiling = initial_level` — zero autonomous escalation. The system immediately surfaces to the user (via warnings) and never tries harder. This is the conservative extreme of the spectrum, appropriate when the system cannot meaningfully improve the situation by trying different parameters.

**The wall-clock deadline (memory `e05030c`) is not a ladder — it's an orthogonal backstop**. Deadlines terminate the entire execution context, not just one ladder. They compose with ladders by providing an outer bound that kills runaway ladders whose individual steps are too slow. The ladder's ceiling bounds the number of steps; the deadline bounds total elapsed time. Together they prevent both infinite escalation (ladder's job) and slow convergence (deadline's job).

## Summary

The escalation ladder is a five-parameter bounded loop (initial level, step function, ceiling, invariant, terminal action) with three decision points (pre-gate, invariant check, ceiling check). The system decides to stop escalating and surface to the user when the ceiling is reached and the invariant is still violated — this is always a conjunction of a static bound and a predicate failure, never a dynamic judgment. The terminal action splits into halt-and-report (for data-risk operations) and propagate-and-fail (for side-effect-free operations). The pattern's composability comes from its clean interface: parameterised config in, success-or-terminal-state out — enabling nesting, chaining, and parallel execution. The key structural property that makes it safe is the static ceiling: the maximum autonomous cost is always known at configuration time, never negotiated at runtime.
