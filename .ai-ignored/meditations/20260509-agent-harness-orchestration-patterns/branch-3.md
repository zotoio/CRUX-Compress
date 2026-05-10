---
branch: 3
depth: 1
subfocus_index: 3
subfocus: "Resource Governance and Bounded Execution"
parent_subfocus: "Agent harness orchestration patterns"
timestamp: 2026-05-09T09:50:00Z
---

## Subfocus Rationale

Of the three orchestration facets (state coordination, failure handling, resource governance), resource governance addresses the economic and structural constraints that make multi-agent systems viable in practice. Without bounded execution, any sufficiently complex agent harness will eventually produce unbounded cost, unbounded runtime, or unbounded side effects — making the system unsafe to deploy. This facet is orthogonal to the sibling concerns: state coordination handles *what* flows between agents, failure handling addresses *what happens when things break*, and resource governance answers *how much can run, for how long, and at what cost*.

## Discoveries

### The Memory Corpus Encodes a Mature Governance Stack

Eight memories directly address resource governance, revealing a system that has evolved through empirical pain rather than top-down design:

1. **Cost-tier classification** (`e05030c`): Four natural cost categories emerged from the eval suite — single-turn (1 call), multi-step (1 long call), recursive (13 calls), integration (5+ turns). The 10x+ cost multiplier between cheap and expensive operations drove skip-by-default gating.

2. **Demand reduction over tolerance increase** (`6415c52`): Shared-agent-runs collapse N API calls to 1, achieving 3-6x savings. The system prefers eliminating unnecessary work over adding retry tolerance for excessive work.

3. **Conservative parallelism + reactive recovery** (`6265f8f`): maxForks: 2 as a starting point, exponential backoff with ±15% jitter for rate limits. Never compensate for too-high concurrency with more retries.

4. **Structural parallelism bounds** (`efc4c24`): Per-phase independence derived from dependency graphs eliminates coordination overhead. The bound is structural (problem shape), not environmental (runtime conditions).

5. **Specialization reduces per-task cost** (`e3c5837`): Domain-specific agents use fewer tokens than generalPurpose, compounding savings across large agent trees.

6. **Advisory gates preserve output** (`b0c02ea`): Non-destructive quality checks that warn but never block — progressive enhancement defaults.

7. **Adaptive escalation within hard caps** (`da3d798`): Compression target → escalate aggressiveness → if still exceeds cap → flag for human. Never silently truncate.

8. **Research caching eliminates redundant exploration** (`fc38ec6`): Repeated meditations on similar topics could skip re-exploration via intermediate result caching — an unrealized but well-defined optimization.

### Three Principles Unify the Governance Patterns

Across all eight memories, three design principles recur:

**Principle 1: Reduce demand before increasing tolerance.** The system first eliminates unnecessary work (batching, skip-by-default, specialization), then bounds what remains (caps, deadlines), then tolerates residual transients (retries, backoff). This ordering is critical — applying tolerance to unreduced demand creates a system that appears healthy while accumulating cost.

**Principle 2: Static ceilings, negotiable paths.** Maximum cost is always predictable at design time (hard caps, recursion depth limits, wall-clock deadlines). But the path to compliance is flexible (adaptive compression, retry with backoff, type demotion chains). The ceiling never negotiates.

**Principle 3: Human escalation as universal terminal.** When automated resolution would require data loss, the system refuses to decide. Conflicts require user input, manual review replaces truncation, destructive operations require confirmation. The agent's autonomy boundary is drawn at irreversibility.

## Connections

### The Three-Layer Control Architecture

The governance patterns compose into a layered architecture analogous to TCP congestion control:

| Layer | Function | Agent System Equivalent | TCP Analogue |
|-------|----------|------------------------|--------------|
| 1. Demand reduction | Eliminate unnecessary work before it starts | Batching, skip-by-default, specialization | Connection reuse, compression |
| 2. Admission control | Bound what can run concurrently and for how long | Static caps, phase-based parallelism, deadlines | Congestion window, slow start |
| 3. Reactive recovery | Handle transient failures at validated load | Exponential backoff, jitter, retry budgets | Fast retransmit, AIMD |

The codebase has strong implementations of layers 1 and 3 but layer 2 (admission control beyond static caps) is nearly absent — this represents the highest-value gap.

### Cost Tiers Map to User Intent, Not Continuous Gradients

Despite four natural cost categories existing, binary gating (cheap/expensive) is optimal because it maps to user decisions: "fast feedback" vs "comprehensive coverage." A 3-tier "moderate" category lacks a natural decision point. The optimal architecture is binary gating for execution control with N-category labeling for cost observability and attribution.

### Subagent Inheritance is Cost-Flag Propagation

Session-scope flags (`ba74013`) that fail to propagate to child agents cause silent governance violations. A parent in "amnesia" mode that spawns a cost-uncapped child defeats the parent's resource intent. The agent spawn boundary is the process fork boundary — governance flags must flow across it with the same guarantees as environment variables flow across process boundaries.

### The Escalation Ladder is a Composable Primitive

Adaptive escalation (try → measure → tighten → retry → flag) appears in compression, rate-limit recovery, and type demotion. It has a clean five-parameter interface: initial level, step function, ceiling, invariant predicate, and terminal action. Ladders can nest (per-file inside REM sleep), chain (demotion → archival), or run in parallel (independent ladders share no state).

### Read-Only Exploration Bounds Side-Effect Risk

The meditate system's read-only-with-opt-in-persistence (`31fec9d`) represents a governance pattern orthogonal to cost: bounding *blast radius* rather than *expenditure*. A 13-agent recursive exploration is expensive but safe because no agent writes persistent state until the user explicitly approves. This separates the "cost" dimension from the "damage" dimension of governance.

## Child Subfocuses

### 1. Cost-Tier Classification and Skip-by-Default Gating
**Rationale**: Before concurrency can be bounded or deadlines can be set, the system needs a taxonomy of what's cheap and what's expensive, plus a mechanism preventing expensive operations from running accidentally.

**Key findings**: Four cost dimensions (invocation count, wall-clock, tokens, spawn depth) reduce to two effective axes (invocations × structural complexity). Binary gating maps to user intent while N-category labeling serves observability. The `!== "false"` inversion pattern is maximally conservative — only one exact string enables execution. Five independent discoverability channels compensate for gate invisibility. The full override stack is: config → env → CLI → session → per-call. Blast radius should independently escalate tier classification beyond raw compute cost.

### 2. Concurrency Control Patterns for Bounded Parallel Execution
**Rationale**: Concurrency is the primary multiplier of both throughput and rate-limit pressure — the highest-leverage governance parameter.

**Key findings**: Five static concurrency caps coexist (maxForks, fan-out width, phase parallelism, mutual exclusion, wall-clock). No dynamic controllers exist — the gap between per-request retry and human config editing. Static caps are correct when constraints are structural; dynamic caps add value when constraints are environmental. A two-axis framework (constraint type × cost-of-error) determines the right choice. The scaling protocol is an empirical ratchet: start at 2, increment by 1, full validation, zero retries required, step back on failure. For decorrelation, ±15% jitter works at N=2 but collision probability scales O(N²), making it insufficient for larger fan-outs. Four proactive patterns are missing: staggered starts, admission queuing, correlated failure detection, and dynamic jitter windows.

### 3. Hard Resource Caps Composing with Adaptive Escalation
**Rationale**: When multiple caps are simultaneously active, their composition determines whether the system is coherent or merely a collection of independent limits.

**Key findings**: The escalation ladder is a five-parameter bounded loop (initial, step, ceiling, invariant, terminal). Caps classify by reversibility of violation: hard-stop (structural impossibility, graceful termination, abort) vs negotiable (iterative degradation, advisory). The ideal composition is the maxMemorySize hybrid: negotiable compliance path wrapped in a hard boundary with human escalation at the terminal. Three multi-cap conflict resolutions exist: refuse-and-flag (strongest preservation), write-partial-and-stop, hard-kill (weakest). Archive-before-write ordering provides accidental crash resilience. The identified gap: wall-clock deadlines kill without a drain window — a graceful shutdown signal protocol would close the last data-preservation gap.

## Child Insights

### From Sub-1 (Cost-Tier Classification)

The four cost dimensions reduce to two effective axes because invocation count and structural complexity capture most variance (wall-clock and tokens follow as correlated secondaries). Binary gating is optimal for execution control because users make binary decisions (fast feedback vs comprehensive), not continuous ones. The skip-by-default mechanism uses maximally conservative inversion logic with five independent discoverability channels. Tier placement uses both quantitative thresholds (5x median, >5min) and structural signals (recursion, multi-turn, external deps). Design-time classification suffices because agent operations have deterministic cost profiles. The missing frontier: blast radius as an independent tier escalation signal, and subagent inheritance as cost-flag propagation across spawn boundaries.

### From Sub-2 (Concurrency Control)

Concurrency governance decomposes into three complementary patterns operating at different levels: width selection (static for structural constraints, dynamic for environmental), starting point and scaling (maxForks: 2 → empirical ratchet), and failure decorrelation (jitter, staggered starts, admission control). The codebase philosophy is consistent: reduce demand before increasing tolerance. Shared runs, skip-by-default, and conservative maxForks are all demand reduction. Retries and backoff are residual tolerance for validated demand levels. The deepest gap is layer 2 (proactive admission control between demand reduction and reactive recovery). TCP congestion control provides the architectural template: slow start → conservative maxForks, AIMD → backoff with jitter, congestion window → admission semaphore, ECN → file-based rate-limit signals between agents.

### From Sub-3 (Hard Caps and Escalation)

Resource caps compose through a layered architecture: negotiable strategies (escalation ladders) inside hard boundaries (absolute caps) with human escalation as the universal terminal. Five design principles emerged: static ceilings make maximum cost predictable, reversibility determines cap classification, archive-before-write preserves data under crashes, file-based coordination provides crash-consistent partial states, and human escalation handles what automation cannot resolve without data loss. The escalation ladder is formally a five-parameter bounded loop with three decision points (pre-gate, invariant, ceiling) — composable via nesting, chaining, or parallelisation. The identified gap: hard-stop mechanisms lack a graceful shutdown signal, killing without drain windows.

## Summary

Resource governance in LLM-powered multi-agent systems converges on a **three-layer control architecture**: (1) demand reduction eliminates unnecessary work before it starts (batching, skip-by-default, agent specialization); (2) admission control bounds what can run simultaneously (static caps for structural constraints, dynamic caps for environmental ones, escalation ladders within hard ceilings); (3) reactive recovery handles residual transient failures at validated load (exponential backoff, jitter, retry budgets). Three design principles unify the stack: **reduce demand before increasing tolerance**, **static ceilings with negotiable compliance paths**, and **human escalation as the universal terminal for irreversible decisions**.

The governance system is already mature in layers 1 and 3 but has significant gaps in layer 2 — no dynamic concurrency controllers, no admission queuing, no staggered starts, and no graceful shutdown signals for hard deadlines. The deepest cross-cutting insight is that **cost classification and blast radius are orthogonal governance dimensions**: a 13-agent recursive exploration is expensive but safe (read-only), while a single-agent destructive operation is cheap but dangerous. Both dimensions must independently escalate governance tier classification. The TCP congestion control model provides a proven architectural template for the full three-layer system, including the missing layer-2 components.
