---
branch: 3
depth: 2
subfocus_index: 1
subfocus: "Cost-tier classification and skip-by-default gating for agent operations"
parent_subfocus: "Resource Governance and Bounded Execution — How do agent harnesses manage computational resources, control costs, and prevent unbounded growth?"
timestamp: 2026-05-09T19:40:00+10:00
---

## Subfocus Rationale

Among the three resource governance subfocuses, this one addresses the upstream classification and gatekeeping question: before you can bound concurrency (sub-2) or enforce hard caps (sub-3), you need a taxonomy of what's cheap and what's expensive, and a mechanism that prevents expensive operations from running accidentally. This is the foundation that the other governance patterns build on.

## Discoveries

### The Empirical Cost Landscape

The CRUX Memories eval suite provides concrete data on four naturally emergent cost categories [memory:Gate expensive SDK evals behind SDK_EVAL_SKIP_EXPENSIVE]:

| Category | Invocations | Wall-clock | Examples |
|----------|-------------|------------|----------|
| Single-turn | 1 agent call | 30–90s | Recall, Remember, Forget |
| Multi-step single-turn | 1 agent call (longer thinking) | 60–120s | Dream, REM Sleep |
| Recursive | up to 13 agent calls | minutes | Meditate (3 facets × 3 levels) |
| Integration | 5+ sequential turns | minutes | Dream → Recall → Remember → Forget → Amnesia |

These categories emerged organically rather than being designed top-down — a strong signal that cost distributions in agent systems are naturally bimodal (cheap cluster vs expensive cluster) rather than continuous.

### Four Axes, Two That Matter

Analysis across the memory corpus identifies four dimensions of cost:

1. **Invocation count** — highest variance axis (1× to 13×), most predictive of total cost
2. **Spawn depth** — structural complexity (flat sequential vs recursive tree), determines failure mode severity
3. **Wall-clock time** — partially correlated with invocation count but also encodes a UX signal (developer patience, CI budget)
4. **Token consumption** — modifiable by agent specialization [memory:Specialized agents outperform generalPurpose] and batching [memory:Shared-agent-runs-per-describe-block reduce LLM eval cost], making it a tunable secondary axis

In practice, dimensions 1+2 (invocation count × structural complexity) capture most cost variance. Wall-clock and token consumption are correlated followers. This reduces the taxonomy design problem to a 2-axis classification.

### Binary Gating Is Optimal for Execution Control

The CRUX system implements a binary gate (`SDK_EVAL_SKIP_EXPENSIVE !== "false"`) despite observing four empirical categories. This is correct because:

- Tier boundaries should correspond to **user decisions**, not cost gradients — users want either "fast feedback" or "comprehensive coverage", not "medium"
- A 3-tier model introduces an ambiguous "moderate" tier lacking a natural decision point [memory:Plugin design patterns: advisory gates and progressive enhancement defaults]
- The 5x-median threshold lands cleanly in the bimodal gap between clusters
- Finer categories serve **observability** (cost reporting, regression detection, capacity planning) not **gating**

This yields a **2-layer architecture**: binary gating for execution control, N-category labeling for cost attribution.

### The Skip-by-Default Mechanism

The canonical pattern uses maximally conservative inversion logic:

```typescript
const skipExpensive = process.env.SDK_EVAL_SKIP_EXPENSIVE !== "false";
```

Only the exact string `"false"` enables execution. Every other state (unset, typo, empty, `"true"`, `"False"`) defaults to skip. The cognitive friction of the triple-negative (`SKIP` × `!==` × `"false"`) is a feature — it forces the developer to pause and acknowledge what they're opting into.

Discoverability is attacked through five independent channels: console output at setup, `.env.example`, README tables, `package.json` scripts, and test file header comments. Each compensates for the others being missed.

### Orthogonal Composition of Protection Layers

Per-category gates and global deadlines are independent:

| Layer | Type | Protects against |
|-------|------|------------------|
| `SDK_EVAL_SKIP_EXPENSIVE` | Binary gate | Known-expensive running by default |
| `SDK_EVAL_MAX_DURATION_MS` | Continuous deadline | Unexpected cost in any operation |

They compose multiplicatively — neither alone is sufficient. This pattern generalizes: gate what you know is expensive, deadline everything as a backstop.

### Multi-Layer Override Stack

The full override precedence across the codebase generalizes to:

**config default → env-var override → CLI flag override → session-scope override → per-invocation override**

Each layer has different persistence: permanent → process-scoped → shell-scoped → session-scoped → call-scoped. The critical failure mode is when overrides don't propagate across agent boundaries — session-scope flags that aren't inherited by subagents silently violate intent [memory:Session-scope command design].

### Tier Placement Criteria

**Quantitative thresholds (either triggers "expensive")**:
- Per-invocation cost ≥5x suite median
- Wall-clock >5 minutes

**Structural signals that predict quantitative thresholds**:
- Recursive subagent spawning (always expensive — multiplicative cost)
- Multi-turn interactive flows (≥5 turns)
- External service dependencies (unpredictable latency + cost)

**Design-time classification suffices** because agent operations have structurally determined cost profiles — recursion depth, fan-out width, and turn count are knowable from the code. Runtime measurement validates but doesn't override structural predictions.

## Connections

### Adaptive escalation as tier boundary response

The compression system's pattern — try target → check against cap → escalate → flag for human review [memory:maxMemorySize hard cap may force compression beyond target ratio] — maps to how tier boundaries should respond when an operation unexpectedly crosses from cheap to expensive. Advisory warning rather than silent execution or silent failure.

### Batching shifts effective tier but gating should use worst-case

Shared-agent-runs collapse N invocations to 1 (3-6x reduction), but this is a harness optimization, not a change to the operation's inherent cost. Tier gating must protect against the unoptimized path executing, while cost reporting can use the optimized actual.

### The wall-clock threshold is a UX signal, not a cost signal

">5 minutes" marks where developer feedback loops break, CI budgets strain, and accidental triggers become genuinely disruptive. This is why wall-clock and cost-multiplier are independent "expensive" criteria — they protect against different failure modes.

### Missing criterion: blast radius

No existing memory explicitly encodes blast radius as a tier signal, but it's implicit. A REM sleep touching every memory in the corpus has higher blast radius than a single Recall. Blast radius correlates with cost-of-failure and difficulty-of-rollback — it should escalate tier classification independently of raw compute cost.

### Subagent inheritance is the agent-world equivalent of env-var propagation

In production harnesses, cost-tier flags must propagate through the agent spawn tree the same way env vars must propagate through process trees. The amnesia inheritance pattern [memory:Session-scope command design] demonstrates both the mechanism (alwaysApply rules) and the failure mode (silent intent violation when inheritance breaks).

## Child Subfocuses

1. **Cost tier taxonomy dimensions and optimal tier count** — explores the four axes of cost (invocation count, wall-clock, tokens, spawn depth), their correlations, and why binary gating with N-category observability is optimal over 3-tier or N-tier gating.

2. **Skip-by-default env-var gating patterns and failure modes** — deep-dives into the `!== "false"` inversion logic, the five-channel discoverability strategy, naming conventions, orthogonal composition with deadlines, and generalization to production agent harnesses.

3. **Concrete criteria and heuristics for tier placement of new operations** — examines quantitative thresholds (5x median, 5min wall-clock), qualitative signals (recursion, interactivity, side-effects), design-time vs runtime classification, and how architectural patterns (batching, specialization) shift effective tiers.

## Child Insights

### Sub-1: Taxonomy Dimensions

The four cost dimensions reduce to two effective axes because they're correlated. Invocation count has the highest variance (1-13x). The CRUX suite's binary gate despite four observed categories confirms that binary gating maps to user intent (fast vs comprehensive) while finer categories serve cost observability. A 3-tier "moderate" tier lacks a natural user decision point. The optimal architecture is binary gating for control + N-category labeling for attribution. Session-scope inheritance affects cost propagation — a "cheap" parent spawning an "expensive" child creates cost escalation the parent's classification didn't predict, arguing for tree-level rather than root-level tier classification.

### Sub-2: Gating Mechanics

The `!== "false"` pattern is maximally conservative — only one string activates, every other state defaults safe. The SKIP naming is superior to RUN naming because it describes the default (observable) behavior. Five independent discoverability channels compensate for each other. Package.json scripts serve as the contract between gate mechanisms and CI workflows, encoding opt-in as named aliases. The full generalized override stack is: config → env → CLI → session → per-call. Advisory vs hard gates form a spectrum — catastrophically expensive operations get hard gates (skip entirely), moderately expensive ones might warrant advisory gates (warn but execute) in production harnesses. The pattern generalizes beyond test suites through the subagent inheritance mechanism.

### Sub-3: Placement Criteria

The 5x threshold generalizes to bimodal distributions (most agent harnesses) but fails for continuous distributions where percentile-based thresholds work better. Design-time structural classification (recursive? multi-turn? external dependency?) is sufficient because agent operation cost profiles are structurally determined — unlike database queries. Batching and specialization can shift effective tier, but gating should use worst-case unoptimized cost. Retry amplification can temporarily make cheap operations behave expensively, but tier classification should be based on steady-state cost with retry budgets as a separate concern. Blast radius (implicit in side-effect analysis) should independently escalate tier classification beyond raw compute cost.

## Summary

Agent harness cost-tier classification converges on a **2-layer architecture**: binary gating for execution control (cheap=default-on, expensive=opt-in-only) with N-category labeling for cost observability. Four dimensions define cost (invocation count, wall-clock, tokens, spawn depth) but reduce to two effective axes (invocations × structural complexity). The **skip-by-default env-var pattern** (`!== "false"`) is maximally conservative — only one exact string enables execution, every other state defaults safe — with five-channel discoverability compensating for the primary failure mode of gate invisibility. **Tier placement** uses both quantitative thresholds (5x median cost, >5min wall-clock) and structural signals (recursion, multi-turn, external dependencies), with design-time classification sufficient because agent operations have deterministic cost profiles. The gating mechanism composes orthogonally with global deadlines — gates prevent known-expensive defaults, deadlines catch unexpected expense. When generalized to production harnesses, the critical extension is **subagent inheritance**: cost-tier flags must propagate through the agent spawn tree or silently violate intent, just as env vars must propagate through process boundaries. The missing frontier is **blast radius** as an independent tier escalation signal beyond raw compute cost.
