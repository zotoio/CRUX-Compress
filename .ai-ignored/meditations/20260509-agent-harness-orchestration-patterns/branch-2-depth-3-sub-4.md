---
branch: 2
depth: 3
subfocus_index: 4
subfocus: "Semantic Hang Signals Beyond AskQuestion — detecting alive-but-unproductive agents from the event stream"
parent_subfocus: "Timeout Detection, Hang Recovery, and Graceful Degradation"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

The harness currently has exactly one semantic hang detector (AskQuestion abort) and otherwise relies entirely on wall-clock timeouts. Timeouts are blunt — they can't distinguish "stuck for 200s" from "working hard for 200s." This subfocus catalogues the richer signal vocabulary available in the event stream and proposes detection patterns that avoid false-positiving on legitimate slow-but-progressing agents.

## Discoveries

### 1. The Event Stream Vocabulary

From `evals/sdk/helpers/harness.ts`, `collectRun` processes four event types from `run.stream()`:

| Event type | Fields available | Hang signal potential |
|-----------|-----------------|----------------------|
| `tool_call` | `name`, `status`, `args` | High — looping, phantom completion |
| `assistant` | `message.content[].text` | Medium — output stagnation, repetition |
| `thinking` | `text` | Medium — reasoning loops without action |
| `status` | `status` | Low — coarse state transitions |
| `task` | `status`, `text` | Low — subagent lifecycle only |

The `tool_call` events are the richest signal source because they carry structured data (tool name, arguments, status) that can be compared mechanically.

### 2. Five Semantic Hang Patterns

**Pattern A: Tool-Call Loop (same tool, same args, repeated N times)**

The `toolCalls` array in `CollectedRun` already stores `{ name, status, args }`. A sliding-window detector could hash `(name, JSON.stringify(args))` tuples and flag when the same hash appears K times within the last M tool calls.

*False-positive risk*: An agent legitimately reading multiple similar files (e.g., `Read` on `branch-1.md`, `branch-2.md`, `branch-3.md`) produces repeated tool names with different args — this is fine. The key discriminator is **args identity**, not just tool name. A Read tool called 5 times on the *same* file with the *same* line range is a loop; called on 5 different files is progress.

*Proposed threshold*: 3 consecutive identical `(name, args)` tuples → warning; 5 → abort. Exclude tool calls with `status: "completed"` vs `status: "started"` deduplication (the same call generates two events).

**Pattern B: Output Stagnation (streaming but repeating)**

If `assistant` chunks arrive but `assistantText` growth contains repeated substrings — the same paragraph generated twice, or a list item pattern cycling — the agent may be in a generation loop. Detection: compare the last 500 characters of `assistantText` against the penultimate 500 characters. Cosine similarity above 0.9 is suspicious.

*False-positive risk*: Agents producing tabular output or repetitive-but-correct lists (e.g., listing all 30 memory files with similar formatting) will produce high textual similarity. Mitigation: only trigger after a minimum output length (e.g., 2000 chars) and require the repetition to span at least 3 cycles.

**Pattern C: Thinking Without Acting (self-referential reasoning loop)**

Track the ratio of `thinking` events to `tool_call` events over a sliding window. An agent that produces 10+ consecutive `thinking` events without a single tool call may be caught in a reasoning loop — deliberating endlessly without committing to an action.

*False-positive risk*: Complex planning phases (e.g., the meditate facet-derivation step) can involve extended thinking before the first tool call. Mitigation: only flag after a minimum elapsed time (e.g., 60s of thinking-only events). Also, a single tool call resets the counter.

**Pattern D: File-Polling Deadlock (waiting for a file another hung agent should write)**

This is the meditate protocol's Achilles heel. The command spec says "poll by checking file existence with `ls` at short intervals" but imposes no timeout on the polling loop. If child agent B hangs and never writes `branch-2.md`, parent agent A polls `ls` indefinitely. Meanwhile, the parent is *alive* and *executing tool calls* (the `ls` commands), so it doesn't look hung from a tool-loop perspective — the args change each time (different timestamps in the shell session).

Detection requires **semantic awareness of the polling pattern**: if the same agent has issued N `Shell` tool calls whose command matches `ls.*branch-.*\.md` (or similar file-existence checks) without the expected file appearing, that's a polling deadlock.

*Proposed mechanism*: Track Shell tool calls that match a "file existence check" pattern. If the same file path is checked more than K times (e.g., 10) without the check succeeding (file still doesn't exist), flag the parent as polling-deadlocked. The harness could set a `maxPollAttempts` per expected file.

**Pattern E: Phantom Completion (alive, reporting success, no ground truth)**

[memory:Agent-reported file creation must be verified on disk] Memory `49303e0` documents this pattern precisely: the agent narrates "I created the file" but the filesystem is unchanged. The agent appears productive (tool calls flowing, assistant text accumulating, status: complete) but its claimed outputs don't exist.

This isn't detectable from the event stream alone — it requires **post-run verification** against ground truth. The harness already does this in assertion helpers (`assertMemoryExists`, `fileExists`), but only after the run completes. A streaming detector could intercept `Write` tool_call events and, on `status: "completed"`, immediately verify the file exists on disk. A Write that claims completion but produces no file is a phantom-completion signal.

### 3. Progress Token Framework

To distinguish slow-but-progressing from hung, the harness needs a concept of **forward progress**. Observable progress signals from the event stream:

| Signal | Indicates progress | How to measure |
|--------|-------------------|----------------|
| New unique tool call (name+args not seen before) | Agent exploring new territory | Set of seen `(name, argsHash)` tuples grows |
| `Write` tool call with new file path | Agent producing output | Set of written paths grows |
| `assistantText` grows with novel content | Agent synthesizing new information | Sliding-window novelty check |
| `task` event with `status: "completed"` | Subagent finished a subtask | Count of completed tasks increases |
| `thinking` followed by `tool_call` | Agent reasoning then acting | Healthy think→act cycle |

**Stagnation** = none of these signals fire within a configurable window (e.g., 60s). The harness could track a `lastProgressTimestamp` and flag stagnation when `now - lastProgressTimestamp > stagnationThresholdMs`.

### 4. The Meditate Polling Gap

The meditate protocol's file-based coordination (from `.cursor/commands/crux-meditate.md`) has no timeout on file polling. The spec says:

> "Poll for all 3 child output files by checking file existence with `ls` at short intervals"

But never specifies: what if the child never writes? The parent polls forever. This is a concrete instance of Pattern D. A fix would add a `maxPollDurationMs` parameter to the meditation protocol, after which the parent writes a partial consolidation from whatever branches did complete and reports the missing branch.

### 5. Relationship to the 3-Tier Timeout Hierarchy

[memory:Gate expensive SDK evals behind SDK_EVAL_SKIP_EXPENSIVE] The existing timeout tiers (per-test 240s, hook 120s, global 60min) are necessary but insufficient — they catch time-based hangs but not semantic ones. The semantic detectors proposed above operate **within** the timeout window:

- A tool-call loop that cycles every 2s would consume 120 iterations before a 240s per-test timeout kills it — that's 120 wasted API calls
- A polling deadlock burns real wall-clock time while appearing "active"
- A reasoning loop burns tokens (and money) without producing value

Semantic detectors catch these within the first few cycles, before the wall-clock timeout fires.

## Connections

**AskQuestion abort as template**: The existing AskQuestion detector in `harness.ts` is the archetype for all semantic hang detectors. It watches the event stream for a specific `(tool_name, status)` pattern and breaks the collection loop. Every detector proposed above follows the same structure: pattern match on event stream → flag → abort/warn.

**Phantom completion ↔ adversarial verification**: Memory `49303e0` shows that phantom completion was caught by an independent judge agent, not by the harness. This suggests a complementary strategy: lightweight in-stream detectors for the obvious patterns (loops, stagnation), plus post-run adversarial verification for the subtle ones (phantom completion, semantic correctness).

**Cascade failure amplification**: [memory:Shared-agent-runs-per-describe-block reduce API cost] Memory `6415c52` notes that shared-run failures cascade to all N dependent tests. A hung agent in a shared beforeAll doesn't just waste its own time — it fails the entire describe block. Semantic hang detection in the shared run is disproportionately valuable because early abort saves N × timeout_duration.

**File-polling deadlock ↔ parallel phase blocking**: [memory:Per-phase parallel subagent execution reduces wall-clock time] Memory `efc4c24` notes that parallel subagent phases achieve near-linear speedup — but a single hung child blocks the entire phase. The meditate protocol's 3×3 fan-out means a single depth-3 hang can block its depth-2 parent, which blocks its depth-1 parent, which blocks consolidation. The deadlock propagates up the tree.

**Session-scope inheritance blind spot**: Memory `ba74013` shows that subagent spawns can silently violate session intent. A semantic hang detector would itself need to be inherited — if the parent harness runs with loop detection enabled, spawned child agents' harnesses should inherit the same detector configuration.

## Summary

The harness's event stream carries five distinct semantic hang signal categories beyond AskQuestion: **tool-call loops** (same name+args repeated), **output stagnation** (repeated text chunks), **thinking-without-acting** (reasoning events with no tool calls), **file-polling deadlocks** (existence checks that never resolve), and **phantom completion** (claimed outputs that don't exist on disk). Each has a characteristic false-positive risk that requires specific mitigation — args identity for loops, minimum duration for thinking, cycle count for stagnation, and ground-truth verification for phantom completion.

The most impactful detector to build first is the **tool-call loop detector**, because it's mechanically simple (hash comparison on structured data), has low false-positive risk (args identity is a strong discriminator), and catches the most common failure mode. The most urgent gap to close is the **meditate polling deadlock**, because the protocol has zero timeout on file-based coordination — a single hung leaf agent can block the entire meditation tree indefinitely.

A unifying concept — **progress tokens** — would let the harness track a `lastProgressTimestamp` and flag any agent that hasn't demonstrated forward progress within a configurable window. This subsumes all five patterns into a single framework: an agent is hung when it's alive but producing no progress tokens.
