---
branch: 3
depth: 3
subfocus_index: 1
subfocus: "Cost tier taxonomy dimensions and optimal tier count"
parent_subfocus: "How should agent harnesses classify operations into cost tiers and gate execution accordingly?"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

Cost tier classification only works if the axes that distinguish tiers are well-defined and the tier count matches real-world clustering. Without examining the dimensionality first, any gating scheme risks either collapsing distinct cost profiles into one bucket (too few tiers) or fragmenting operations into unmaintainable micro-categories (too many).

## Discoveries

### Empirical Cost Categories from the CRUX Eval Suite

The CRUX Memories SDK eval suite provides concrete data on four naturally emergent cost categories [memory:Gate expensive SDK evals behind SDK_EVAL_SKIP_EXPENSIVE]:

| Category | Invocations | Wall-clock | Examples |
|----------|-------------|------------|----------|
| Single-turn | 1 agent call | 30–90s | Recall, Remember, Forget |
| Multi-step single-turn | 1 agent call (longer thinking) | 60–120s | Dream, REM Sleep |
| Recursive | up to 13 agent calls | minutes | Meditate (3 facets × 3 levels) |
| Integration | 5+ sequential turns | minutes | Dream → Recall → Remember → Forget → Amnesia chain |

These categories emerged organically from the test suite — they were not designed top-down. The fact that the suite ships with a binary gate (cheap vs expensive) despite having four observed categories is itself a data point about practical tier granularity.

### Four Dimensions of Cost

Analysis across the memory corpus and eval harness reveals four primary axes that distinguish cost levels:

**1. Invocation count** — The most predictive single axis. Single-call operations (Recall, Remember) are fundamentally different from recursive fan-outs (Meditate at 13 calls) or sequential multi-turn chains (Integration at 5+). This axis has the highest variance: a 13× range between cheapest and most expensive.

**2. Wall-clock time** — Partially correlated with invocation count but not identical. A single Dream invocation takes 60–120s (complex thinking), while a single Recall takes 30–60s (simpler retrieval). The global backstop (SDK_EVAL_MAX_DURATION_MS at 60 minutes) exists as an orthogonal safety net, suggesting wall-clock is a second-order concern behind invocation count.

**3. Token consumption** — Correlated with but distinct from wall-clock. The shared-agent-runs pattern [memory:Shared-agent-runs-per-describe-block reduce LLM eval cost] demonstrates that token cost and invocation count can be decoupled: batching N assertions behind one agent.send() collapses invocation cost while keeping token consumption similar. Specialized agents [memory:Specialized agents outperform generalPurpose] use fewer tokens per invocation, making per-invocation token cost variable.

**4. Agent spawn depth** — A structural dimension that invocation count alone misses. Meditate's 3-level recursion (depth 0 → 1 → 2 → 3) has qualitatively different failure modes than Integration's flat 5-turn sequence, even when invocation counts are similar. Deeper spawn trees have cascading failure risk and harder-to-bound cost ceilings.

### The Dimensionality Reduction Question

These four axes are not independent — they cluster. Invocation count and spawn depth are highly correlated (deep recursion implies many invocations). Wall-clock and token consumption are moderately correlated (more tokens → more processing time). This suggests that in practice, a 2-axis model — *invocation count* (primary) × *structural complexity* (flat vs recursive) — captures most of the variance.

### Binary vs N-Tier: What the Evidence Shows

The CRUX eval suite's actual implementation uses a **binary** gate despite observing four categories:

```
if (process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false") { ... }
```

This collapses the taxonomy to: cheap (runs by default) vs expensive (opt-in). The four observed categories map to two tiers:

| Tier | Categories | Gate |
|------|-----------|------|
| Cheap (default-on) | Single-turn, Multi-step single-turn | Always run |
| Expensive (default-off) | Recursive, Integration | SDK_EVAL_SKIP_EXPENSIVE=false |

The 5× median cost threshold rule from the memory further confirms the binary model: "Per-test cost is 5x+ the median" triggers skip-by-default. There is no intermediate "moderate" tier.

### Why Binary Beats 3-Tier in Practice

The adaptive escalation pattern [memory:maxMemorySize hard cap may force compression beyond target ratio] and the advisory gates pattern [memory:Plugin design patterns: advisory gates and progressive enhancement defaults] both converge on a key insight: **tier boundaries should correspond to distinct user decisions, not to continuous cost gradients**.

A 3-tier model (cheap/moderate/expensive) implies three distinct gating decisions:
1. Always run (cheap)
2. Sometimes run — but when? (moderate)
3. Opt-in only (expensive)

The "sometimes" tier creates ambiguity. The advisory gates pattern shows that gates work best when they map to clear user intents: "run everything fast" vs "run everything including expensive stuff". There is no natural user intent for "run medium-cost things but not expensive things" — users either want fast feedback or comprehensive coverage.

### When N-Tier Does Make Sense

The 4-category empirical taxonomy matters for **observability and cost reporting**, even if gating stays binary. Knowing that a Meditate run cost 13 invocations vs an Integration run at 5 is valuable for:
- Post-hoc cost attribution (billing, budgets)
- Performance regression detection (a test that used to take 1 invocation now takes 5)
- Capacity planning (how many Meditate runs can we afford per day?)

This suggests a **2-layer model**: binary gating for execution control, N-category labeling for cost observability.

## Connections

**Adaptive escalation transfers to tier boundaries.** The compression memory's pattern — try target ratio → check against hard cap → escalate if needed → flag for human review if still over — maps directly to how tier boundaries should respond to cost overruns. A test that unexpectedly crosses from "cheap" to "expensive" territory should escalate (warn) rather than silently run or silently fail.

**Session-scope inheritance affects cost propagation.** The session-scope subagent pattern [memory:Session-scope command design] reveals that cost tier classification must account for inheritance. A "cheap" parent spawning an "expensive" child creates a cost escalation that the parent's tier classification didn't predict. Tier classification should be applied to the full operation tree, not just the root invocation.

**Specialization reduces per-invocation cost but not invocation count.** The specialized-vs-generalPurpose memory shows that agent choice affects token cost per call but not the structural cost (number of calls, spawn depth). This reinforces that invocation count and spawn depth are the primary tier axes, while token consumption is a tunable secondary axis within a tier.

**The batching pattern creates a cost optimization orthogonal to tiers.** Shared-agent-runs-per-describe-block collapses N invocations to 1 — but this is a test harness optimization, not a change to the operation's inherent cost tier. The operation (e.g. Dream) is still "multi-step single-turn" regardless of whether the harness batches assertions. Tiers classify the operation's inherent cost, not the harness's efficiency at testing it.

## Summary

Four dimensions define agent operation cost: invocation count, wall-clock time, token consumption, and spawn depth. In practice, these reduce to two effective axes (invocation count × structural complexity) because the dimensions are correlated. The CRUX eval suite's empirical data reveals four natural categories but implements a binary gate — and this is correct. Binary gating (cheap/expensive) maps cleanly to user intent (fast feedback vs comprehensive), while finer categories serve observability and cost reporting. A 3-tier model introduces an ambiguous "moderate" tier that lacks a natural user decision point. The optimal architecture is therefore a 2-layer model: binary gating for execution control with N-category labeling for cost attribution. Tier boundaries should be defined by the 5× median cost heuristic and should use advisory escalation (warn on unexpected cost jumps) rather than hard enforcement.
