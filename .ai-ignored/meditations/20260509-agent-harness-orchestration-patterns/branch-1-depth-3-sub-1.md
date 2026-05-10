---
branch: 1
depth: 3
subfocus_index: 1
subfocus: "Polling-for-Existence vs Event-Driven Notification"
parent_subfocus: "File-Based Coordination Protocols"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

The parent's "File-Based Coordination Protocols" subfocus identifies the filesystem as the primary inter-agent communication channel. The most fundamental design decision within that protocol is *how* a waiting agent detects that a file has appeared. This codebase contains two contrasting implementations — naive ls-polling (meditate) and watchdog event-driven detection (MCP watcher) — making it an ideal case study for trade-off analysis.

## Discoveries

### Pattern 1: ls-Polling in Meditate (agent-to-agent coordination)

The meditate command specification (`crux-cursor-memory-manager.md` lines 261, 295; `crux-meditate.md` line 41) prescribes:
- Parent agents poll for child output files using `ls` at **10-30 second intervals**
- File existence is the **only** coordination signal
- Explicitly prohibits reading JSONL transcripts — the file's presence is sufficient

This is structurally a **busy-wait with a sleep interval**. The agent runtime has no native filesystem event API, so polling is the only available primitive.

### Pattern 2: Watchdog Event-Driven in MCP MemoryWatcher (process-to-process)

The `crux_mcp_server/indexer/watcher.py` implementation uses Python `watchdog` (≥4.0):
- `MemoryFileHandler` extends `FileSystemEventHandler`, receiving OS-level filesystem events
- Events are filtered to `*.memory.md` and `*.memory.crux.md` suffixes only
- A **1-second debounce timer** (`threading.Timer`) resets on every new event — only fires the callback after 1s of quiet
- The callback triggers a full index rebuild (`_rebuild_index` → `scan` + `SearchEngine.build`)
- The Observer is set to `daemon=True` and watches recursively across memory directories

### Pattern 3: Hook-Based Pending Flag (cross-session)

A third hybrid pattern exists in `crux-detect-memory-changes.py`:
- Triggered by the `afterFileEdit` hook — not polling, but editor-event-driven
- Writes a `pending-index-rebuild.json` flag file with affected paths
- The flag is consumed at **next session start** by `crux-session-start.py`
- This is effectively a **store-and-forward** pattern — latency is measured in sessions, not seconds

### Memory Corpus Findings

- **Memory 49303e0** ("Agent-reported file creation must be verified on disk"): The Write tool can silently fail — content exists in the agent's context but never reaches the filesystem. This directly undermines polling-for-existence: a parent polling for `branch-1.md` may wait indefinitely if the child agent *believes* it wrote the file but didn't. The file never appears, and the parent has no timeout/abort protocol.
- **Memory efc4c24** ("Per-phase parallel subagent execution"): Multiple agents writing to the same directory simultaneously creates burst-write scenarios where the debounce timer is critical — without it, the MCP watcher would fire N rebuilds for N near-simultaneous writes.
- **Memory ba74013** ("Session-scope subagent patterns"): Subagents get fresh contexts with no shared state — reinforcing why file-based coordination is necessary (no shared memory) and why polling is the only available detection mechanism for agent-to-agent coordination.

## Connections

### 1. Polling degrades to spin-waiting when intervals shrink below useful thresholds

The 10-30s polling interval in meditate is generous because child agents typically take 60-300 seconds to complete. But if the architecture were scaled to faster operations (sub-second file writes), polling intervals would need to shrink proportionally, converging on a spin-wait. The crossover point is roughly when `poll_interval < 2 × (ls_execution_time)` — at that point, the parent spends more time listing than sleeping.

In the agent harness context, this is unlikely to be a practical concern because the bottleneck is LLM inference time (tens of seconds per agent turn), not filesystem latency. The polling interval is well-matched to the operation timescale.

### 2. Debounce interval is a throughput-responsiveness trade-off with a sweet spot

The MCP watcher's 1-second debounce balances two forces:
- **Too short** (e.g. 50ms): Burst writes from parallel agents trigger multiple rebuilds. With 3 agents writing near-simultaneously (the meditate fan-out pattern), a 50ms debounce might fire 2-3 rebuilds instead of 1.
- **Too long** (e.g. 10s): Search results become stale for that duration — a user running `/crux-recall` 2 seconds after a dream extraction would see the old index.

The 1-second choice implicitly assumes that memory write operations take >1s each (they do — agent write operations involve LLM inference), so bursts naturally self-separate. This is workload-aware tuning, not arbitrary.

### 3. The three patterns form a latency spectrum mapped to use cases

| Pattern | Latency | Use Case | Constraint |
|---------|---------|----------|------------|
| Watchdog events + debounce | ~1-2s | MCP server index freshness | Long-running process with OS event access |
| ls-polling | 10-30s | Agent-to-agent coordination | No persistent process; agent runtime lacks event APIs |
| Pending-flag + session check | Minutes to hours | Cross-session state | No running process between sessions |

Each pattern is correctly matched to its latency requirements. The MCP server needs sub-second awareness because it serves live queries. Meditate parents can tolerate 30s because children take minutes. Cross-session flags can wait because the next session is the earliest possible consumer.

### 4. Silent Write tool failures create a detection-completeness gap

Memory 49303e0 reveals that file existence is necessary but not sufficient for coordination. A file might:
- **Never appear** (Write tool silent failure) — parent waits forever
- **Appear empty** (partial write) — parent reads garbage
- **Appear with incomplete content** (write interrupted mid-stream) — parent parses partial YAML frontmatter

Neither polling nor watchdog addresses this. The watchdog fires on `CREATE` events regardless of file completeness. Polling detects existence but not integrity. Both patterns need a **content validation layer** — checking that the file has non-zero size and valid frontmatter after detection.

The meditate spec has no timeout or abort mechanism for missing files. If a child agent crashes without writing its output, the parent blocks indefinitely. A robust implementation would need: `max_wait_time`, `fallback_on_timeout` (proceed with available branches), and `incomplete_file_detection` (validate content after existence check).

### 5. Platform-specific failure modes affect the watchdog pattern differently

- **inotify limits** (Linux `fs.inotify.max_user_watches`): The watcher recursively observes `memories/`, `memories/agents/`, and `.crux/`. With default limits (~65k watches), this is safe for the current scale (<50 memory files). But an org-wide REM sleep automation (memory idea 515c010) watching hundreds of repos would exhaust inotify handles.
- **NFS/network filesystem staleness**: `watchdog` on NFS falls back to polling internally (`PollingObserver`), collapsing the event-driven advantage. The codebase assumes local filesystem, which is correct for Cursor IDE workspaces.
- **Race condition between write-close and detect**: On Linux, watchdog receives `IN_CLOSE_WRITE` after the file descriptor is closed, which is safe. But `IN_CREATE` fires before content is written — if the handler acted on `CREATE` instead of waiting for `CLOSE_WRITE`, it could read an empty file. The current implementation uses `on_any_event` with debounce, which naturally waits past the write-close race because the debounce timer resets on subsequent events (CREATE → MODIFY → CLOSE_WRITE all reset the 1s timer).

### 6. The debounce pattern accidentally solves the write-completeness problem

Because the MemoryFileHandler debounces for 1s after the *last* event, and a typical write operation generates CREATE → MODIFY → CLOSE_WRITE in rapid succession (~ms), the debounce naturally waits until after the file is fully written and closed. This is an emergent correctness property, not an explicitly designed one — the debounce was intended to batch rapid changes, but it also provides a write-completion guarantee as a side effect.

## Summary

This codebase deploys three detection patterns across a latency spectrum — watchdog events (~1s) for live MCP queries, ls-polling (10-30s) for agent-to-agent meditation coordination, and pending-flag files (session-granularity) for cross-session state. Each is well-matched to its use case's latency tolerance.

The key insight is that **detection alone is insufficient**. Memory 49303e0 (silent Write tool failures) reveals that file existence doesn't guarantee file completeness. Neither pattern includes a content validation layer. The watchdog's 1-second debounce accidentally mitigates write-completeness races (by waiting past the CREATE→CLOSE_WRITE event sequence), but polling has no equivalent safeguard.

The most actionable gap is in meditate's polling loop: there is no timeout, no abort-on-missing-child, and no file-integrity check after detection. A child agent crash silently deadlocks the parent. Adding `max_wait_time` with graceful degradation (proceed with N-1 branches) would make the coordination protocol robust against the failure modes this codebase has already documented.
