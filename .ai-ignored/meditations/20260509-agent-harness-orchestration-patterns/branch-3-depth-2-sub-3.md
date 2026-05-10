---
branch: 3
depth: 2
subfocus_index: 3
subfocus: "Hard resource caps composing with adaptive escalation strategies"
parent_subfocus: "Resource Governance and Bounded Execution"
timestamp: 2026-05-09T19:40:00+10:00
---

## Subfocus Rationale

The parent subfocus asks broadly how agent harnesses manage resources and prevent unbounded growth. This narrowing focuses specifically on the composition problem: when multiple resource caps (size, depth, time) are simultaneously active and each has its own escalation or enforcement strategy, how do they interact without losing data? This is the structural question that underpins whether a multi-cap governance system is coherent or merely a collection of independent limits.

## Discoveries

### The Escalation Ladder as Universal Pattern

The memory corpus and codebase reveal that resource governance in CRUX-Compress follows a common five-parameter pattern — the **escalation ladder**: initial level, step function, ceiling, invariant, and terminal action. Three concrete instances exist:

- **Compression sizing**: 33% target → reduce by 10pp per iteration → 5% floor → flag manual review
- **Rate-limit backoff**: 0ms → exponential × 2 with jitter → 5 retries / 60s max → throw
- **Memory type demotion**: current type → demotion chain → goal (immune) → flag for review

Each ladder has three structural decision points: a **pre-gate** (should we enter the ladder at all?), an **invariant check** (did this attempt succeed?), and a **ceiling check** (have we exhausted autonomous options?). The ceiling is always a static configuration value, never dynamically computed — this is what makes the maximum cost predictable at design time.

### Two Categories of Caps with Distinct Failure Semantics

Resource caps fall into a taxonomy determined by **reversibility of violation**:

| Category | Examples | Failure Mode | Data Risk |
|----------|----------|--------------|-----------|
| **Hard-stop (structural)** | Read-only exploration, no write tools | Impossible to violate | None |
| **Hard-stop (gate)** | Destructive op confirmation, recursion depth | Graceful halt or termination | None — agent writes what it has |
| **Hard-stop (kill)** | Wall-clock deadline (`process.exit(1)`) | Abrupt termination | In-flight work lost |
| **Negotiable (iterative)** | Compression target, retry count | Degrade quality, retry at new level | None if terminal is halt-and-report |
| **Negotiable (advisory)** | Plugin quality gates | Warn and preserve output | None |

The determining rule: a cap is hard when violation produces irreversible harm; negotiable when degradation is bounded, detectable, and retryable.

### The maxMemorySize Hybrid — Gold Standard for Composition

The most instructive composition pattern is `maxMemorySize`: the cap itself is **hard** (a file cannot exceed 1000 lines), but the path to compliance is **negotiable** (adaptive escalation from 33% → 5%). When the negotiable strategy exhausts itself, the system escalates to a hard gate (flag for manual review, refuse to write). The original file is preserved in archive.

This hybrid pattern — negotiable strategy wrapped in a hard boundary with human escalation at the terminal — is the template for how caps should compose: try progressively harder within the negotiable range, then defer to the user rather than losing data.

### Multi-Cap Conflict Resolution

Three resolution strategies emerge when caps conflict simultaneously:

1. **Refuse and flag** (compression at floor still exceeds size cap): No write, original preserved, user decides. Strongest data preservation.
2. **Write partial and stop** (recursion depth limit): Agent writes its current state and terminates cleanly. Data is incomplete but available.
3. **Hard kill with no drain** (wall-clock deadline): In-flight work lost, only disk-committed work survives. Weakest data preservation.

The archive-before-write ordering in compression provides accidental resilience against hard kills: because the original is archived before any compressed file is written, a process kill at any point leaves the original recoverable.

## Child Subfocuses

### Sub-7: Formal Structure of the Escalation Ladder
**Rationale**: Before caps can compose, the escalation pattern itself needs a precise structural definition — the loop anatomy, decision points, and terminal conditions that make it embeddable and chainable.

### Sub-8: Hard-Stop vs Negotiable Cap Taxonomy
**Rationale**: The failure semantics that follow from classifying a cap as hard vs negotiable determine whether the system can self-recover and what the user experiences — this taxonomy is the prerequisite for any composition strategy.

### Sub-9: Data Preservation Invariant Under Multi-Cap Conflicts
**Rationale**: When multiple caps are active simultaneously and their prescriptions conflict, the "never lose data silently" invariant is most at risk — this subfocus targets the intersection points where caps compete.

## Child Insights

### From Sub-7 (Escalation Ladder Structure)
The escalation ladder is a **five-parameter bounded loop** with a clean interface (parameterised config in, success-or-terminal-state out). The three decision points — pre-gate, invariant check, ceiling check — are the structural skeleton that all instances share. Key insight: the ceiling is **always static and configuration-driven**, never derived from the current attempt. This prevents the ladder from negotiating with itself about how hard to try, making maximum cost predictable at design time. The pattern is composable: ladders can be **nested** (one per memory file inside a REM sleep loop), **chained** (demotion ladder feeds archival ladder), or **parallelised** (independent ladders share no mutable state). Advisory gates represent the **degenerate case** — zero-rung ladders that immediately surface to the user.

### From Sub-8 (Hard vs Negotiable Taxonomy)
The determining factor for cap classification is **reversibility of violation**. Hard-stop caps protect against irreversible harms through mechanisms ranging from structural impossibility (cheapest — the system literally can't violate the cap) to process termination (most expensive — in-flight work is lost). Within the hard category, there's a "gate hardness spectrum": structural impossibility > graceful termination > halt-and-wait > abort. Good harness design moves caps upward on this spectrum. The classification should be made at **definition time** and the failure semantics should be explicit in the interface contract, not emergent from implementation. The `maxMemorySize` hybrid — hard boundary with negotiable compliance path — represents the ideal composition.

### From Sub-9 (Data Preservation Under Conflicts)
The "never lose data silently" invariant is well-preserved when cap conflicts have a clear resolution hierarchy, and fails when hard-stop mechanisms can interrupt without a drain window. The **archive-before-write ordering** provides accidental resilience against deadline kills — an emergent property of operation ordering, not explicit design. **File-based coordination** in the meditation system acts as a crash-consistent protocol: agent crashes produce a well-defined partial state (some files exist, others don't), and any parent can resume from whatever arrived. The deepest gap is between **soft stops** (agent notices the limit and flushes state) and **hard stops** (agent is killed externally with no notice). A **signal protocol** — "you have N seconds to flush" before the hard kill — is the missing piece. The Write tool silent failure (memory `49303e0`) represents an orthogonal, infrastructure-level violation that no application-level cap resolution can address.

## Summary

Hard resource caps compose with adaptive escalation through a layered architecture: **negotiable strategies** (escalation ladders with iterative aggressiveness increase) operate inside **hard boundaries** (absolute caps that the system cannot exceed), with **human escalation** as the terminal when automated strategies exhaust. The key design principles are:

1. **Static ceilings**: Maximum autonomous cost is always configuration-driven and predictable at design time
2. **Reversibility determines classification**: Caps protecting against irreversible harm must be hard; caps governing quality targets can be negotiable
3. **Archive-before-write ordering**: Preserves data integrity even under hard kills by ensuring the original is safe before any speculative output is attempted
4. **File-based coordination as crash consistency**: Inter-agent communication via the filesystem produces well-defined partial states that survive agent crashes
5. **Human escalation as the universal terminal**: When automated resolution would require data loss, the system refuses to pick a winner and defers to human judgment

The identified gap is the absence of a **graceful shutdown signal** for hard-stop mechanisms — wall-clock deadlines kill processes without giving agents a drain window. Moving from "abort" to "graceful termination" on the gate hardness spectrum would close the last data-preservation gap in multi-cap scenarios.
