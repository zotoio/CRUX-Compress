---
branch: 3
depth: 3
subfocus_index: 3
subfocus: "Concrete criteria and heuristics for tier placement of new operations"
parent_subfocus: "How should agent harnesses classify operations into cost tiers and gate execution accordingly?"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

The sibling branches address taxonomy structure and env-var gating mechanics respectively. This branch tackles the harder upstream question: given a new agent operation, what concrete signals determine which tier it belongs in — and can those signals be evaluated at design time or must they be measured at runtime?

## Discoveries

### The CRUX System's Empirical Thresholds

Memory `e05030c` documents the thresholds used in CRUX's own eval harness:

| Signal | Threshold | Classification |
|--------|-----------|---------------|
| Per-test cost relative to median | ≥5x | Expensive |
| Wall-clock duration | >5 minutes | Expensive |
| Recursive subagent spawning | Any | Expensive |
| Multi-turn flows | 5+ turns | Expensive |
| Expensive external services | Any dependency | Expensive |

These were derived empirically from the CRUX Memories eval suite cost distribution:
- Single-turn commands (Recall, Remember, Forget): 1 agent invocation, ~30-90s
- Multi-step single-turn (Dream, REM): 1 agent invocation, ~60-120s
- Recursive (Meditate): up to 13 agent invocations, unbounded wall-clock
- Integration (multi-turn): 5+ sequential invocations

The 5x multiplier is not arbitrary — it's the natural gap between the single-turn cluster (1 invocation) and the recursive/multi-turn cluster (5-13 invocations). The distribution is bimodal, so the threshold lands cleanly in the gap between modes.

### Qualitative Signals That Predict Tier

From cross-referencing memories, three qualitative axes emerge:

**1. Recursion depth vs linearity** (from `e05030c`, spec context)
- Linear operations have bounded, predictable cost — one invocation regardless of input
- Recursive operations (Meditate's 3-level fan-out) have cost that compounds: 1 + 3 + 9 = 13 agents for 3-level × 3-way branching
- Any recursion is a strong "expensive" signal because even shallow recursion (depth 2) multiplies base cost by 4x minimum

**2. Side-effecting vs read-only** (from `31fec9d`, `ba74013`)
- Read-only operations (Recall, Meditate exploration) are safer to run speculatively
- Side-effecting operations (Dream writes memories, REM rebalances corpus) need confirmation gates
- The session-scope pattern memory (`ba74013`) establishes a crisp discriminator: "Does it write anything? → Delegate [to heavier machinery]"
- However, side-effect presence alone doesn't determine cost tier — it determines *gating* requirements, which is orthogonal

**3. Interactive vs batch** (from `fcd2f69`)
- Interactive multi-turn flows (conflict resolution, candidate acceptance) cannot be batched or parallelized
- Batch/single-turn operations can share agent runs (`6415c52`), reducing effective tier
- The SDK's single-turn constraint forces non-interactive directives for testing — this means the test cost ≈ production cost for batch operations but potentially underestimates interactive ones

### Batching as Tier Reduction

Memory `6415c52` reveals a crucial insight: **an operation's tier is not fixed — architectural patterns can shift it**. Shared-agent-runs-per-describe-block collapse N invocations into 1, achieving 3-6x cost reduction. This means:

- The *nominal* tier (what the operation would cost naively) differs from the *effective* tier (what it costs after optimization)
- Tier placement should consider the *optimized* cost when the optimization is structurally guaranteed
- But tier *gating* should be based on *worst-case* cost to protect against the unoptimized path

### Retry Amplification

Memory `6265f8f` demonstrates that retries amplify effective cost:
- BASE_DELAY escalation: 2s → 4s → 8s → 16s → 32s → 60s (capped)
- Worst-case 5 retries add 122s of wall-clock plus the repeated API calls
- A nominally-cheap operation that triggers rate limits under concurrency can briefly behave like an expensive one
- This argues for tier classification based on *steady-state* cost, with retry budgets as a separate concern

### Adaptive Escalation and Input-Dependent Cost

Memory `da3d798` reveals that some operations have input-dependent cost profiles:
- A memory compression that hits the size cap must escalate aggressiveness iteratively
- An operation might be "cheap" for small inputs but "expensive" for large ones
- The system flags for manual review rather than silently crossing tier boundaries — suggesting that tier violations should be visible, not auto-absorbed

### Specialization as Cost Reduction

Memory `e3c5837` shows specialized agents reduce per-invocation cost vs generalPurpose:
- Shorter prompts (domain context baked in)
- Fewer tokens per task
- More consistent output (fewer retries)
- This suggests that the *agent type* assigned to an operation affects its effective tier — the same logical task costs less when routed to a specialist

## Connections

### Design-Time vs Runtime: A False Dichotomy

The CRUX system resolved this by using a **design-time structural classification** validated by **runtime empirical measurement**:

1. **Design-time**: structural signals (recursive? multi-turn? external dependency?) place the operation in a provisional tier
2. **First measurement**: the eval suite's initial run provides empirical cost data
3. **Threshold validation**: if measured cost matches the structural prediction (5x+ median, >5min), the tier is confirmed
4. **No runtime reclassification**: once classified, the tier is static per code version — operations don't dynamically shift tiers during execution

This works because agent operations have *structurally determined* cost profiles. A Meditate command will always spawn ~13 agents regardless of input content. Unlike database queries (where the same query can be fast or slow depending on data), agent orchestration patterns have deterministic multipliers.

### The 5x Threshold Generalizes When Distributions Are Bimodal

The 5x-median threshold works well when:
- The cost distribution has clear clusters (cheap vs expensive)
- The gap between clusters is wide enough for a threshold to land cleanly
- Operations don't frequently straddle the boundary

It generalizes poorly when:
- Cost distributions are continuous/normal (no natural gap)
- Many operations cluster near 3-4x median (where to draw the line?)
- Input variance causes the same operation to span both sides of the threshold

For systems with continuous distributions, a percentile-based threshold (e.g., P90 of historical cost) might be more robust than a multiplier of the median.

### The Wall-Clock Threshold Encodes a Human Patience Assumption

The ">5 minutes" threshold is not a cost signal per se — it's a UX signal. It marks the boundary where:
- A developer won't wait for the result in a tight feedback loop
- CI inclusion becomes contentious (PR check budgets are typically 10-15 min total)
- Accidental triggering becomes genuinely disruptive (lost context, wasted time)

This is why wall-clock and cost-multiplier are independent criteria (either triggers "expensive") — a cheap-but-slow operation and an expensive-but-fast operation both need gating, for different reasons.

### The Missing Criterion: Blast Radius

None of the existing memories explicitly encode *blast radius* as a tier signal, but it's implicit in the side-effect axis. Consider:
- A side-effecting operation that writes one file has low blast radius
- A REM sleep that touches every memory in the corpus has high blast radius
- Blast radius correlates with both cost-of-failure and difficulty-of-rollback
- High blast radius should escalate tier classification independently of raw compute cost

## Summary

The CRUX system's tier placement criteria are:

**Quantitative (either triggers "expensive")**:
- Per-invocation cost ≥5x suite median
- Wall-clock >5 minutes

**Qualitative (structural signals that predict quantitative thresholds)**:
- Recursive subagent spawning (always expensive — multiplicative cost)
- Multi-turn interactive flows (≥5 turns)
- External service dependencies (unpredictable latency + cost)

**The 5x threshold generalizes** to systems with bimodal cost distributions (most agent harnesses, since simple vs compound operations naturally cluster). It generalizes poorly to continuous distributions — use percentile thresholds instead.

**Design-time placement is sufficient** because agent operations have structurally-determined cost profiles (recursion depth, fan-out width, turn count are all knowable from the code). Runtime measurement validates but doesn't override structural classification. This is unlike database-style operations where identical code can have wildly different costs based on data.

**Architectural patterns can shift effective tier** (batching, specialization, caching), but tier *gating* should be based on worst-case unoptimized cost to protect against the unoptimized path executing.
