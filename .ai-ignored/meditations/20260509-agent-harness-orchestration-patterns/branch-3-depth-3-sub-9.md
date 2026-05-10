---
branch: 3
depth: 3
subfocus_index: 9
subfocus: "Data preservation invariant under multi-cap conflicts"
parent_subfocus: "Hard resource caps composing with adaptive escalation strategies"
timestamp: 2026-05-09T19:37:00+10:00
---

## Subfocus Rationale

The sibling subfocuses cover escalation ladder structure (sub-7) and hard-vs-soft cap taxonomy (sub-8). This subfocus targets the gap between them: what happens at the intersection of two or more simultaneously active caps when their prescriptions conflict? The data preservation invariant ("never lose data silently") is the system's most critical safety property, and multi-cap conflicts are where it is most likely to break.

## Discoveries

### 1. Compression: Size Cap vs. Compression Floor — Fully Handled

[memory:maxMemorySize adaptive escalation] The compression skill (`crux-skill-memory-compress`) demonstrates the strongest multi-cap conflict resolution in the codebase. Two constraints are simultaneously active:

- **Compression target** (default 33% of original) — a ratio-based cap
- **maxMemorySize** (default 1000 lines) — an absolute size cap

When these conflict (a large file compressed to 33% still exceeds 1000 lines), the escalation ladder iterates: reduce target by 10pp per round, down to 5% floor. If even 5% exceeds the cap, the system **does not write the file** and flags for manual review. The original is preserved in the archive (moved there before any overwrite attempt).

The key invariant-preserving property: the archive-before-write ordering means the original is safe regardless of where the process fails. The compressed output is the "speculative" artifact — if it can't meet all constraints, it's simply never created. The user receives three options: split the memory, raise the limit, or accept the loss explicitly.

### 2. Wall-Clock Deadline vs. In-Flight Work — Gap Identified

[memory:Gate expensive SDK evals] The `SDK_EVAL_MAX_DURATION_MS` global timer fires `process.exit(1)` — a hard kill with no graceful drain. There is no pre-exit hook that:
- Flushes pending file writes
- Writes partial results for in-progress agents
- Signals child processes to save state

If the deadline fires while a compression escalation loop is mid-iteration, the outcome depends on which step was in progress:
- **Before archival**: The original `.memory.md` is intact (never touched yet). Safe — data preserved by accident of ordering.
- **After archival, before compressed write**: Archive exists in `.ai-ignored/memories/sources/`, but no `.memory.crux.md` was written. The original directory has neither file. Data is preserved in archive but the operation is incomplete. A human or subsequent REM sleep would need to detect and recover.
- **During write**: The file may be partially written or corrupted. The archive is the recovery path.

The meditation system partially mitigates this: file-based coordination means that any branch output file written before the deadline survives on disk. But the consolidation step (depth-0 aggregation) never runs, so the tree is headless — branches exist but no synthesis.

### 3. Recursion Depth vs. Exploration Completeness — Gracefully Degraded

The meditation system enforces `maxDepth=3` as a hard recursion cap. At the boundary, depth-3 agents simply write what they have — no further recursion, no error. The partial result is accepted as the full output for that leaf. This is "write partial result" rather than "discard and flag."

The data preservation invariant holds trivially: there is nothing to lose, because the depth cap prevents creation of data that would need preserving. The trade-off is exploration quality, not data integrity. Contrast with wall-clock deadlines, which can kill agents that *have* already produced data.

### 4. The Infrastructure-Level Violation — Write Tool Silent Failure

[memory:Write tool can silently fail] The most insidious multi-cap conflict is between the system's data preservation protocols and the infrastructure's reliability. Memory `49303e0` documents a case where:
- The agent followed all protocols correctly
- The Write tool reported success
- The file never materialized on disk

No amount of application-level cap conflict resolution can compensate for silent infrastructure failure. This is a category error: the "never lose data" invariant is defined at the application layer, but the violation occurs below it. The adversarial verification protocol (ls + read + git status) is the only current defense, and it's a post-hoc check, not a prevention mechanism.

### 5. Dual-Cap Conflict Resolution Taxonomy

Synthesizing across the codebase, three resolution strategies emerge for multi-cap conflicts:

| Strategy | When Used | Data Outcome |
|----------|-----------|--------------|
| **Refuse and flag** | Compression size cap at floor | No write, original preserved, user decides |
| **Write partial and stop** | Recursion depth limit | Incomplete but available partial output |
| **Hard kill with no drain** | Wall-clock deadline | In-flight work lost, disk-committed work survives |

The first two preserve the invariant. The third relies on the ordering of disk writes — data committed before the kill survives, data in-flight does not.

### 6. Advisory Gates as Universal Safety Net

[memory:Plugin design patterns] The advisory gate pattern (`failClosed=false` → warn but preserve output) provides a composable building block for multi-cap scenarios. When two caps conflict, an advisory gate says: "one cap says stop, the other says continue — preserve the work product, emit a warning, let the user decide." This pattern appears in:
- Plugin quality gates (warn but don't discard output)
- Compression manual review flags (don't write but don't destroy the original)
- Destructive op confirmation (don't auto-delete even when the input is unambiguous)

## Connections

**Archive-before-write is an accidental multi-cap safeguard.** The archive step in compression was designed for rollback capability, but it also provides resilience against wall-clock kills. Because the original is archived *before* the compressed file is written, a process kill at any point leaves the original recoverable. This is an emergent property of the ordering, not an explicit design for deadline resilience.

**File-based coordination is a crash-consistent protocol.** The meditation system's use of markdown files as the sole inter-agent communication channel means that agent crashes (including deadline kills) produce a well-defined partial state: some files exist, others don't. The parent can enumerate what arrived and aggregate whatever is available. This is structurally similar to write-ahead logging in databases — the file system state is the ground truth, and any agent can resume from it.

**The deepest gap is between soft stops and hard stops.** Recursion depth is a soft stop: the agent notices it has reached the limit and writes its partial result. Wall-clock deadline is a hard stop: the process is killed externally. The data preservation invariant is well-served by soft stops (the agent has agency to preserve its state) and poorly served by hard stops (the agent has no notice). The missing piece is a signal protocol: giving agents a "you have N seconds to flush" warning before the hard kill.

**Confirmation gates are the human-in-the-loop resolution for unresolvable cap conflicts.** When size cap says "too big" and compression floor says "can't compress further," the system doesn't pick a winner — it escalates to the user. This is the same pattern as conflict detection in dream extraction: contradictions between memories are always presented to the user. The system's implicit philosophy is: when automated resolution would require data loss, refuse to automate and defer to human judgment.

## Summary

The "never lose data silently" invariant is well-preserved when cap conflicts have a clear resolution hierarchy: the compression skill's escalation ladder with terminal manual-review flag is the gold standard. It fails gracefully when each cap allows the agent to notice and react (recursion depth). The invariant is most at risk when hard-stop mechanisms (wall-clock `process.exit(1)`) can interrupt mid-operation without a drain window. The archive-before-write ordering provides accidental resilience, but there is no systematic "flush before kill" signal protocol. The codebase's implicit resolution pattern for unresolvable multi-cap conflicts is human escalation: refuse to pick a winner that would lose data, and ask the user. The Write tool silent failure (memory `49303e0`) represents an orthogonal, infrastructure-level violation that no application-level cap resolution can address — only post-hoc verification catches it.
