---
branch: 1
depth: 2
subfocus_index: 1
subfocus: "File-Based Coordination Protocols"
parent_subfocus: "State Coordination and Handoff Mechanisms"
timestamp: 2026-05-09T19:40:00+10:00
---

## Subfocus Rationale

Among the three dimensions of state coordination (file-based protocols, session-scope propagation, serialization formats), file-based coordination is the dominant inter-agent communication pattern in this codebase. The meditation command, dream extraction, spec execution, memory system hooks, and MCP watcher all use the filesystem as their primary coordination bus. Understanding the protocols that make this work — naming conventions, detection strategies, and persistence guarantees — is foundational to understanding how the entire agent harness holds together.

## Discoveries

### The filesystem as a communication bus

This codebase treats the filesystem as a shared message bus where agents are producers and consumers. Five distinct coordination families coexist:

1. **Meditation tree coordination** — positional encoding (`branch-{N}-depth-{D}-sub-{S}.md`) with fixed bookend files (`facets.md`, `consolidation.md`). Up to 39 output files plus bookends in a single meditation.
2. **Dream summaries** — config-sourced templates (`dream-{slug}-{yyyymmdd}.md` via `summaryPattern` in `crux-memories.json`).
3. **Memory files** — slug-based naming with extension-encoded type discrimination (`.memory.md` vs `.memory.crux.md`).
4. **Sentinel/flag files** — presence-as-signal (`.crux/pending-index-rebuild.json`, `.crux/pending-compression.json`) carrying structured payloads.
5. **Spec state files** — positional within the work directory (`_execution-state.yml`).

### Three detection patterns across a latency spectrum

| Pattern | Latency | Use Case | Mechanism |
|---------|---------|----------|-----------|
| Watchdog + debounce | ~1-2s | MCP index freshness | OS filesystem events via Python `watchdog`, 1s debounce timer |
| ls-polling | 10-30s | Agent-to-agent coordination | Shell `ls` at intervals; file existence = only signal |
| Pending-flag + session check | Minutes-hours | Cross-session state | Hook writes flag; next session-start reads it |

Each is correctly matched to its use case's latency tolerance.

### The trust gap: agent narrative vs filesystem evidence

Memory 49303e0 [memory:Agent-reported file creation must be verified on disk] established that the Write tool can silently fail. An agent can produce a detailed work log claiming file creation — with path, contents, and verification narrative — without the file existing on disk. Three observed root causes: silent tool failure, canvas-only emission, and agent self-deception (narrating without invoking Write).

### Scattered but complete write-safety primitives

The codebase contains all the building blocks for transactional writes, but they exist as scattered patterns rather than a unified primitive:
- **Pre-write archival** (memory cd0c954): compression skill archives originals to dated directories before overwriting
- **Staging directories**: `install.py` downloads to `tempfile.mkdtemp()`, verifies checksums, then installs from staging
- **Three-layer verification**: ls → Read → git status (prescribed by memory 49303e0)
- **Checksum verification**: `install.py` SHA256 verification against release manifests
- **Idempotent writes**: CRUD skill generates deterministic IDs via `sha256(title)[:7]`

## Connections

### 1. Detection and verification are complementary halves of the coordination protocol

Detection (polling or events) answers "did a file appear?" Verification (ls + Read + git status) answers "is the file valid?" Neither alone is sufficient. The meditate command has detection (ls-polling) but no verification — a parent reads the file without checking integrity. The MCP watcher's debounce accidentally provides a weak verification proxy (waiting 1s past the last event naturally waits past CREATE→CLOSE_WRITE), but this is emergent, not designed. A complete coordination protocol needs both halves explicitly.

### 2. Archive-before-write + verify-after-write creates transactional semantics

Combining the archival pattern (cd0c954) with the verification protocol (49303e0) produces a transactional write envelope: (1) archive original → abort if fails, (2) write new content → may silently fail, (3) verify → if fails, recover from archive, (4) clean up original → only after verified success. This is functionally equivalent to write-ahead logging in databases.

### 3. Path determinism enables decoupled coordination without a broker

Every path convention is deterministic — given the same inputs, any agent independently computes the same path. This is what eliminates the need for a central coordinator. The consumer constructs the expected path *before* the producer writes, which is what makes polling possible. But determinism is fragile: if the path template is defined in prose (meditation) rather than config (dream), silent drift between producer and consumer goes undetected.

### 4. A live path convention inconsistency illustrates the drift risk

The meditation working directory tree diagram shows depth-3 files with globally sequential sub-indices (sub-1 through sub-9), but the protocol description passes `subfocusIndex` as 1-3 per parent — implying per-parent-relative indexing. If implemented literally, three depth-2 agents would all write `branch-1-depth-3-sub-{1,2,3}.md`, colliding on the same filenames. This is exactly the class of drift that memory 96a7410 (tooling defaults diverging from spec) and memory d944d7c (spec index text contradicting subtask details) warn about.

### 5. Sentinel files are architecturally distinct from output files but blur in practice

Pure sentinels would be empty (presence = boolean). But this codebase's sentinel files carry structured payloads — file lists, timestamps, `needsRebuild` flags. They're hybrids: existence gates whether to act, content determines what to act on. This works but creates a fragility: corrupt JSON passes the existence check but fails the content read. The `crux-detect-memory-changes.py` hook handles this with try/except, but the pattern needs explicit documentation.

### 6. The meditate polling loop has no timeout — a deadlock waiting to happen

If a child agent crashes without writing its output file, the parent blocks indefinitely. There is no `max_wait_time`, no fallback-on-timeout (proceed with N-1 branches), and no incomplete-file detection. Memory 49303e0 documents why this matters: the Write tool can silently fail, meaning a child that "completed" may never produce its output file.

## Child Subfocuses

### Sub-1: Polling-for-Existence vs Event-Driven Notification
How do parent agents detect when child output files appear? Trade-offs between naive ls-polling (meditate), watchdog event handlers with debouncing (MCP watcher), and pending-flag files (cross-session hooks). Focuses on latency, resource usage, race conditions, and failure modes of each detection strategy.

### Sub-2: Write Verification and Persistence Guarantees
Given that file writes can silently fail, what verification protocols ensure persistence? Covers the three-layer verification stack (ls → Read → git status), pre-write archival, staging directories, checksum verification, idempotent writes, and the gap between having these primitives scattered vs unified.

### Sub-3: Path Convention Design and the Coordination Namespace
How do predictable naming patterns enable decoupled coordination? Covers the five convention families, what makes a convention good (determinism, collision avoidance, dual readability), sentinel vs output files as coordination primitives, config-sourced vs prose-hardcoded templates, and the risks of convention drift.

## Child Insights

### From Sub-1 (Polling vs Event-Driven)

The three detection patterns form a latency spectrum correctly matched to use cases: watchdog events (~1s) for live MCP queries, ls-polling (10-30s) for agent coordination where children take minutes, pending-flags (session-granularity) for cross-session state. The key insight is that **detection alone is insufficient** — file existence doesn't guarantee file completeness. The watchdog's 1-second debounce *accidentally* mitigates the write-completeness race (by waiting past CREATE→MODIFY→CLOSE_WRITE sequences), but polling has no equivalent safeguard. The most actionable gap: meditate's polling loop has no timeout or abort-on-missing-child, so a child crash silently deadlocks the parent. Platform-specific failure modes (inotify limits, NFS staleness) are unlikely concerns at current scale but would become relevant for org-wide automation ideas like memory 515c010.

### From Sub-2 (Write Verification)

Write verification is the weakest link in file-based coordination. The codebase has scattered but complete building blocks: pre-write archival (cd0c954) creates rollback capability, staging directories (install.py) approximate atomic writes, the three-layer verification protocol (49303e0) catches different failure classes at different costs, and checksum verification provides bit-level integrity evidence. Combined, archive-before-write + verify-after-write creates transactional semantics equivalent to write-ahead logging. Adversarial verification (memory 6c16dc6, 25% hit rate) provides a fourth verification layer — because the writing agent may skip or misinterpret its own verification. The central gap: these primitives aren't unified into a formal `write-and-verify` skill that all agents invoke consistently. Each skill reimplements verification ad-hoc, inviting inconsistency.

### From Sub-3 (Path Conventions)

Path conventions are the addressing layer that makes decoupled coordination possible — consumers independently compute expected locations without communicating with producers. Good conventions share four properties: determinism, collision avoidance, human readability, and machine parseability. The five convention families each optimise for their domain. The primary risk is convention drift — when templates are defined in one place and reconstructed in another. The codebase already has a live instance: the meditation depth-3 file numbering shows global vs relative indexing ambiguity. Centralising templates (as `summaryPattern` in config does) mitigates drift; hardcoding in prose invites it. The sentinel/output distinction is architecturally meaningful but blurry in practice — sentinel files carry structured payloads, making them hybrids that need explicit error handling for corrupt content.

## Summary

File-based coordination in this codebase is a mature but informally specified protocol operating across three layers: **naming** (deterministic path conventions enabling decoupled address computation), **detection** (polling, events, or flag files matched to latency requirements), and **verification** (post-write checks ensuring persistence and integrity). The architecture works because these layers compose: agents compute where to write (naming), other agents detect when the write appears (detection), and either party can confirm the write is valid (verification).

The most important cross-cutting insight is that **detection and verification are complementary halves that are currently treated as separate concerns**. The meditate command detects but doesn't verify. The memory 49303e0 protocol verifies but is prescribed as a one-off practice rather than a composable primitive. Combining archive-before-write with verify-after-write creates transactional semantics, but this pattern isn't codified as a reusable skill.

Three actionable gaps emerge: (1) meditate's polling loop needs a timeout and graceful degradation for missing children, (2) the scattered write-safety primitives should be unified into a formal write-and-verify skill, and (3) path conventions hardcoded in prose (especially meditation's depth-3 numbering scheme) should be centralised to prevent the same class of drift that memories 96a7410 and d944d7c document in other domains.
