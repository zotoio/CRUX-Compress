---
branch: 2
depth: 2
subfocus_index: 2
subfocus: "Timeout Detection, Hang Recovery, and Graceful Degradation"
parent_subfocus: "Failure Handling and Resilience in Multi-Agent Workflows"
timestamp: 2026-05-09T09:40:00Z
---

## Subfocus Rationale

Timeout and hang detection are the active defence layer in agent orchestration — they determine how quickly a harness recognises that something has gone wrong, and what it does next. This narrowing was chosen because the current CRUX harness has a rich but incomplete timeout hierarchy (per-test, per-hook, global deadline, plus one semantic detector) with critical gaps: no polling timeouts, no partial-result degradation, and no detection of phantom completions. Closing these gaps is prerequisite to reliable multi-agent workflows.

## Discoveries

### The Three-Tier Timeout Hierarchy (Existing)

The CRUX eval harness implements three time-based defence layers:

| Tier | Mechanism | Default | Purpose |
|------|-----------|---------|---------|
| Per-test | vitest `testTimeout` / per-test `{ timeout: N }` | 240s (up to 480s for meditate) | Kill individual hung agents |
| Per-hook | vitest `hookTimeout` | 120s | Kill stuck beforeAll/afterAll |
| Global deadline | `SDK_EVAL_MAX_DURATION_MS` + `process.exit(1)` | 60 minutes | Cap cumulative cost |

Plus one **semantic detector**: the AskQuestion abort pattern in `collectRun` that breaks the event stream loop when the agent requests user input that will never arrive.

### The Four Missing Detection Classes

1. **Tool-call loops**: Agent repeatedly calls the same tool with identical arguments. The event stream carries full structured data (`name`, `args`, `status`) to detect this mechanically.

2. **Thinking-without-acting**: Extended `thinking` events with no interleaved `tool_call` events — reasoning loops that burn tokens without producing observable progress.

3. **File-polling deadlocks**: Parent agent waits for child output files that will never appear (because the child has hung). The meditate protocol's polling loop has zero timeout — a single hung leaf blocks the entire tree.

4. **Phantom completions**: Agent reports success, exits cleanly, but produces no artifact on disk. Bypasses all time-based defences. Requires ground-truth verification (filesystem checks, not agent self-report).

### The All-or-Nothing Gap

The harness has no intermediate state between "one agent is struggling" and "kill everything." Specifically:
- Meditation polls forever for all 3 branch files — no partial-result path
- Spec execution phases block until all agents in the phase complete
- Shared test runs cascade-fail all N dependent tests when the shared agent crashes
- `withRetry` only retries rate-limit errors — all other failures throw immediately

### Key Metrics from the Codebase

- Per-test timeouts range from 120s to 480s (2–8 minutes) depending on test complexity
- The meditate protocol spawns up to 39 agents in a full tree (3^0 + 3^1 + 3^2 + 3^3 = 40 total)
- Adversarial verification catches issues at a 25% hit rate (6/24 subtasks across two specs)
- Rate-limit retry uses exponential backoff: 2s base, 60s cap, 5 max retries, ±15% jitter

## Connections

### Progress Tokens as Unifying Framework

All semantic hang patterns reduce to one question: "Is the agent making forward progress?" Observable progress signals include: new unique tool calls (name+args not seen before), new files written to disk, novel text in the output stream, completed subtask events. **Stagnation** = none of these signals fire within a configurable window. A `lastProgressTimestamp` tracker would subsume tool-call loops, thinking-without-acting, and file-polling deadlocks into a single detection mechanism.

### Phantom Completions ↔ Adversarial Verification ↔ Ground Truth Designation

Phantom completions connect to a deeper pattern visible across multiple memories: **when a system has multiple representations of truth (agent narrative, filesystem, spec index, tool-call log), they will silently diverge**. The remedy is always the same: designate one representation as ground truth (filesystem for outputs, subtask details for specs) and automate verification of all others against it.

The harness already has the primitives (`fileExists`, `assertMemoryExists`, `readFile`, `collectRun`'s tool-call capture) but doesn't yet wire them into a systematic "completion verifier" that cross-references tool-call streams against disk state in real time.

### Correlation-First Triage for Partial Results

The highest-leverage addition to the failure-handling layer is a **correlation check** as the first triage step:
- All branches fail → systemic issue (bad prompt, API down) → escalate immediately, don't retry
- One branch fails → isolated issue → retry the leaf or degrade gracefully

This single check prevents the most wasteful failure pattern: retrying a broken prompt N times before the global deadline finally kills everything.

### Exploratory vs. Transactional Operations

The decision to proceed with partial results depends on the operation's nature:
- **Exploratory** (meditation, recall, research): Partial results are almost always better than nothing. The parent can annotate the gap explicitly.
- **Transactional** (spec execution, memory creation): Partial results are dangerous — they may leave the system in an inconsistent state. Escalate to user.

### File-Based Coordination Enables Selective Retry

The meditation protocol's file-based coordination already supports a key resilience feature: child outputs persist independently of the parent. If a depth-2 parent hangs while aggregating, it can be re-run and will find existing child files. If a depth-3 leaf fails, only that leaf needs re-running — the siblings' outputs remain on disk. This makes **selective retry at the lowest possible level** feasible without reconstructing state.

## Child Subfocuses

### Sub-4: Semantic Hang Signals Beyond AskQuestion
**Rationale**: The single existing semantic detector (AskQuestion abort) covers one hang pattern. The event stream carries enough structured data to detect at least four more: tool-call loops, output stagnation, thinking-without-acting, and file-polling deadlocks. This child explores what detection patterns look like and how to avoid false-positives on legitimately slow agents.

### Sub-5: Phantom Completions and Silent Failures
**Rationale**: Phantom completions are uniquely insidious because they defeat all time-based defences. The agent exits cleanly — no timeout fires, no error thrown. This child explores the taxonomy of phantom subtypes and what a systematic verification layer looks like.

### Sub-6: Partial-Result Decision Logic in Fan-Out Failures
**Rationale**: The current harness is all-or-nothing. This child explores the decision framework for determining retry vs. degrade vs. escalate, including cost awareness, correlation detection, and the graceful consolidation pattern.

## Child Insights

### From Sub-4 (Semantic Hang Signals)

Five distinct semantic hang patterns were catalogued, each with detection mechanism and false-positive mitigation:

1. **Tool-call loop** — Hash `(name, args)` tuples; 3 consecutive identical = warning, 5 = abort. Discriminate on args identity (not just tool name) to avoid false-positive on legitimate multi-file reads.
2. **Output stagnation** — Sliding-window comparison of the last N characters; cosine similarity >0.9 over 3+ cycles after minimum output length (2000 chars).
3. **Thinking-without-acting** — Ratio of thinking events to tool calls; 10+ consecutive thinking events without a tool call after 60s of elapsed time.
4. **File-polling deadlock** — Track Shell tool calls matching file-existence patterns; same path checked >10 times without success = deadlock. The meditate protocol's unbounded polling is the concrete instance.
5. **Phantom completion** — Post-run cross-reference of Write tool calls against filesystem state. A Write with status "completed" where the target file doesn't exist = phantom.

The **most impactful first build** is the tool-call loop detector (mechanically simple, low false-positive risk, catches common failure mode). The **most urgent gap** is the meditate polling deadlock (zero timeout on file-based coordination means a single hung leaf blocks the entire tree indefinitely).

A unifying **progress token** framework: track `lastProgressTimestamp` based on novel tool calls, new files written, or novel output text. Stagnation = no progress tokens within a configurable window.

### From Sub-5 (Phantom Completions)

Four phantom completion subtypes were identified:
1. **Silent Write failure** — Tool returns success but no-ops
2. **Narrative hallucination** — Agent describes file creation without invoking Write
3. **UI-only emission** — Content rendered in chat UI only, never written to disk
4. **Partial Write** — File created but content is truncated/placeholder

A **four-layer verification pyramid** addresses all subtypes at appropriate cost:
- Layer 1 (free): Tool-call stream inspection — did a Write even occur?
- Layer 2 (cheap): Filesystem existence + content validation
- Layer 3 (moderate): Structural output schemas forcing falsifiable claims
- Layer 4 (expensive): Adversarial re-verification by independent agent

The deeper principle: **the filesystem is always ground truth; the agent's narrative is always a hypothesis**. This connects to spec index drift (memory d944d7c) and tooling defaults drift (memory 96a7410) — all instances of the same multiple-representations-of-truth problem.

The harness already has Layer 1-2 primitives (`fileExists`, `assertMemoryExists`, `collectRun` tool-call capture) but doesn't yet cross-reference them systematically.

### From Sub-6 (Partial-Result Decisions)

A decision matrix was developed: `failure_mode × branch_criticality × correlation → action`:
- Correlated failures (all N branches) = systemic → escalate immediately
- Isolated failure (1/N) + non-critical branch = proceed with partial results
- Isolated failure + critical branch = retry once at lowest possible level

**Selective retry cost** in the meditation tree: retrying a leaf costs 1 agent; retrying a depth-1 branch costs 13. The file-based coordination already supports this — child files persist, enabling parent re-aggregation without re-running successful children.

**The graceful consolidation pattern**: Parent writes partial synthesis with explicit acknowledgment of missing branches, impact assessment, and recommendation to re-run the gap. This is strictly better than all-or-nothing for exploratory operations.

**Extending `withRetry`**: The existing rate-limit-only retry could be generalized to a multi-signal decision: `shouldRetry(failure) = NOT correlated AND type IN [timeout, transient] AND idempotent AND retry_count < max AND cost < threshold`.

## Summary

The CRUX harness has a solid time-based defence (3-tier timeout hierarchy) but critical gaps in semantic detection and graceful degradation. Three key findings:

1. **Semantic hang detection needs expansion**: Beyond AskQuestion abort, the event stream supports detecting tool-call loops, thinking-without-acting, file-polling deadlocks, and phantom completions. A unifying "progress token" framework (track last novel action; flag stagnation) would subsume all patterns into a single configurable mechanism.

2. **Phantom completions require a verification layer**: Time-based defences cannot catch an agent that exits cleanly but produces nothing. A four-layer verification pyramid (tool-call stream → filesystem checks → structural schemas → adversarial re-verification) provides defence-in-depth at graduated cost. The filesystem is always ground truth.

3. **Partial-result degradation is missing and needed**: The harness is all-or-nothing at every level. For exploratory operations (meditation), a graceful consolidation pattern — poll with timeout, proceed with available results, annotate the gap — is immediately implementable and strictly better. For transactional operations, correlation-first triage (all fail = systemic, one fails = retry leaf) prevents the most wasteful failure pattern: retrying broken inputs.

The most urgent concrete fix: **add a polling timeout to the meditate protocol's file-based coordination** so a single hung leaf agent cannot block the entire meditation tree indefinitely.
