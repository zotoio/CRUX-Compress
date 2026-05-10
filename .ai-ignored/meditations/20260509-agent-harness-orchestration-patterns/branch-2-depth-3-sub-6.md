---
branch: 2
depth: 3
subfocus_index: 6
subfocus: "Partial-Result Decision Logic in Fan-Out Failures"
parent_subfocus: "Timeout Detection, Hang Recovery, and Graceful Degradation"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

The parent facet identifies that the current harness is all-or-nothing — wait for all branches or abort everything. The gap between "one branch failed" and "kill the whole operation" is where the most impactful design decisions live: what criteria determine whether to retry, degrade, or escalate? This subfocus addresses that decision framework directly.

## Discoveries

### Memory-Corpus Findings

**`6265f8f` — Exponential backoff with jitter**: The `withRetry` function in `evals/sdk/helpers/harness.ts` retries only rate-limit errors (HTTP 429, "too many requests", "throttl"). Non-rate-limit errors — including agent crashes, context window exhaustion, phantom completions, and all non-API failures — are thrown immediately with no retry. This is a hard boundary: the retry infrastructure exists but is scoped exclusively to a single failure class. The decision to throw non-rate-limit errors immediately is deliberate (memory says "Throw non-rate-limit errors immediately so real bugs aren't masked") — but this means there's zero retry path for transient agent-level failures that aren't rate limits.

**`efc4c24` — Per-phase parallel execution**: The spec execution system runs subagents in parallel within a phase, with no inter-agent dependencies. If one agent hangs, the entire phase blocks. There is no "proceed with N-1 results" logic. The phase boundary is a hard synchronization point: all must complete.

**`6415c52` — Shared agent runs**: When a shared `beforeAll` run fails in vitest, all N tests in the describe block fail together. This is cascading failure by design — there's no graceful degradation to partial test results. The trade-off is accepted: "descriptive error messages per assertion partially mitigate this."

**`e05030c` — Expensive eval gating**: A global wall-clock deadline (SDK_EVAL_MAX_DURATION_MS, default 60min) serves as a backstop. Per-test timeouts protect individual agents. But the gap between "individual timeout fires" and "global kill" is undefined — there's no intermediate decision point.

**`ba74013` — Session-scope subagent patterns**: Subagent inheritance means session state flows from parent to child. For retry, this is critical: retrying a failed branch means either reconstructing the session state from scratch or preserving it across the retry boundary. The current inheritance model doesn't address state reconstruction for retries.

**`49303e0` — Write tool can silently fail**: Agent-reported file creation must be verified on disk. This is a "phantom completion" failure mode — the agent reports success, but the output never materialised. This is the hardest failure class to detect because it looks like success from the agent's perspective.

### Codebase Patterns

The meditation protocol (from the memory manager agent definition) specifies:
> "Poll for Branch Outputs: Wait for branch-1.md, branch-2.md, and branch-3.md to appear. Poll by checking file existence with ls — use short intervals (10-30s). All three files must exist before proceeding."

No timeout on polling. No partial-result path. The parent polls forever. This is the canonical example of the problem this subfocus addresses.

The `collectRun` function in `harness.ts` has one escape hatch: it detects `AskQuestion` tool calls and aborts the stream early (sets status to `requires_input`). This is a form of "escalate to user" — but it's specific to interactive prompts, not generalizable to arbitrary failure modes.

## Connections

### Decision Matrix: failure_mode × criticality × correlation → action

| Failure Mode | Branch Critical? | Correlated? | Recommended Action |
|---|---|---|---|
| **Timeout** (agent still running) | Yes | No (1/N) | Retry once with extended timeout, then escalate |
| **Timeout** | Yes | Yes (all N) | Escalate immediately — systemic issue (API down, bad prompt) |
| **Timeout** | No | No | Proceed with partial results + explicit annotation |
| **Crash** (error thrown) | Yes | No | Retry once (idempotent ops only), then escalate |
| **Crash** | Yes | Yes | Escalate — the shared input is likely malformed |
| **Crash** | No | No | Proceed with partial results |
| **Phantom completion** (agent says done, no output) | Any | Any | Escalate — this is a platform bug, retry won't help |
| **Rate limit** | Any | Yes (expected) | Retry with backoff (existing `withRetry` pattern) |

**Key insight**: correlation detection is the first triage step. If all branches fail, it's almost certainly systemic — retrying wastes resources. If 1/N fails, isolated retry is reasonable. The harness needs a `failureCorrelation()` check before deciding retry vs. escalate.

### The Meaningfulness Threshold

When is a partial result (e.g. 2/3 meditation branches) still valuable vs. misleading?

**Valuable**: When branches are independently meaningful and the parent can acknowledge the gap. Meditation is a good candidate — each branch explores a different facet, and a consolidation from 2/3 branches still provides insight. The synthesis just needs to explicitly state: "Branch 2 timed out — this synthesis is based on branches 1 and 3 only. The missing branch was exploring [subfocus]. Consider re-running to fill this gap."

**Misleading**: When branches have interdependencies that make the aggregate semantically incomplete. Example: if branch 1 discovers a pattern, branch 2 validates it, and branch 3 explores alternatives — losing branch 2 means the pattern is unvalidated but might be presented as established. For meditation this is low-risk (branches are designed to be independent); for spec execution where subtasks may have implicit semantic dependencies despite being phased as independent, the risk is higher.

**The heuristic**: If the operation is exploratory (meditation, research, gap analysis), partial results are almost always better than nothing. If the operation is transactional (spec execution, memory creation, index rebuild), partial results are dangerous and should escalate.

### Cost of Retry in the Meditation Tree

In a full 3-level meditation, retrying at each level has vastly different costs:

| Retry Level | Agents Re-Run | Approximate Cost |
|---|---|---|
| Depth-3 leaf | 1 | Low — single agent, fast |
| Depth-2 node | 1 + 3 children = 4 | Moderate |
| Depth-1 branch | 1 + 3 + 9 = 13 | High — full subtree re-execution |
| Depth-0 (full) | 1 + 3 + 9 + 27 = 40 | Prohibitive — defeats the purpose |

**Selective retry is feasible and necessary**: If a depth-3 leaf fails, retry just the leaf. If a depth-2 node fails, check whether any of its children succeeded — if yes, retry only the depth-2 aggregation step with cached child outputs. This requires the file-based coordination pattern to be designed for incremental progress: children's outputs should persist even if the parent fails.

The current design already supports this — child output files are written independently of the parent's aggregation. A failed parent can be re-run and it will find existing child files on disk.

### The "Graceful Consolidation" Pattern

Rather than blocking or aborting, the parent acknowledges the missing branch explicitly:

```
## Consolidation Note
Branch 2 (subfocus: "Timeout Detection and Hang Recovery") did not
produce output within the polling deadline. This synthesis incorporates
findings from branches 1 and 3 only.

**Impact assessment**: The missing branch was exploring [description].
Key areas that may be under-explored as a result: [list].

**Recommendation**: Re-run `/crux-meditate` with the missing subfocus
as the primary topic for targeted exploration.
```

This pattern preserves value, maintains transparency, and gives the user actionable next steps. It's strictly better than the current all-or-nothing approach for exploratory operations.

### Idempotency and Retry Safety

The meditation workflow is naturally idempotent: re-running a depth-3 agent that writes `branch-2-depth-3-sub-6.md` simply overwrites the file. There are no append operations, no database mutations, no external side effects. This makes retry safe at any level.

Spec execution is NOT naturally idempotent: a subtask that creates files, modifies code, or writes memories may have side effects that are dangerous to repeat. Retry in spec execution requires either:
1. Idempotency guards (check-before-write, git stash/restore)
2. Isolated workspaces per attempt (the `createIsolatedWorkspace` pattern from the eval harness)
3. User confirmation before retry

### Connection to `withRetry` — Extending the Pattern

The existing `withRetry` function discriminates on error type (rate-limit vs. other). A generalised version for agent-level failures would discriminate on a richer set of signals:

```
shouldRetry(failure) =
  NOT correlated_with_siblings(failure)
  AND failure.type IN [timeout, transient_crash]
  AND operation.is_idempotent
  AND retry_count < max_retries
  AND estimated_retry_cost < cost_threshold
```

This extends `withRetry`'s "is this a rate-limit?" check into a multi-dimensional decision: is this isolated? Is it transient? Is it safe to repeat? Is it worth the cost?

## Summary

The current CRUX harness has no partial-result decision logic — it's all-or-nothing at every level (meditation polls forever; spec phases block on all agents; shared test runs cascade-fail). Three patterns emerge from the analysis:

1. **Correlation-first triage**: Check whether failures are correlated (all branches failing = systemic, abort) vs. isolated (one branch = retry or degrade). This is the highest-leverage addition.

2. **Exploratory vs. transactional split**: Exploratory operations (meditation, recall, research) should degrade gracefully with explicit gap annotations. Transactional operations (spec execution, memory writes) should escalate to the user rather than proceeding with partial results.

3. **Selective retry with cost awareness**: Retry at the lowest possible level (leaf, not subtree). The file-based coordination pattern already supports this — child outputs persist independently. Extend `withRetry` from rate-limit-only to a multi-signal decision function considering correlation, idempotency, cost, and failure mode.

The graceful consolidation pattern — where the parent explicitly acknowledges missing branches and provides impact assessment — is the most immediately implementable improvement, requiring only a polling timeout and a template for partial synthesis.
