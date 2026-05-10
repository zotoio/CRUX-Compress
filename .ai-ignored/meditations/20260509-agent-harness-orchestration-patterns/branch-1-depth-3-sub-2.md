---
branch: 1
depth: 3
subfocus_index: 2
subfocus: "Write Verification and Persistence Guarantees"
parent_subfocus: "File-Based Coordination Protocols"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

File-based coordination only works if files actually exist after being "written." Memory 49303e0 documents a real incident where the Write tool returned success but no file materialized on disk. This makes write verification not a nice-to-have but a structural prerequisite for any agent orchestration system that uses the filesystem as its communication bus. Without persistence guarantees, the entire coordination model collapses silently.

## Discoveries

### 1. The Trust Gap: Agent Narrative vs. Filesystem Ground Truth

Memory 49303e0 establishes the foundational insight: **an agent's work log is a hypothesis, not evidence**. The subtask 06 incident revealed three distinct failure modes for the Write tool:

- **Silent tool failure** — the Write call returns but the disk write is a no-op (transient error, permission issue, path resolution mismatch)
- **Canvas-only emission** — content rendered in chat UI but never persisted to disk
- **Self-deception** — the agent narrated the action without ever invoking Write

The agent has no independent filesystem view after writing. Its subsequent statements about the file's existence are based on the assumption that its tool call succeeded, not on verified state.

### 2. The Three-Layer Verification Protocol

Memory 49303e0 prescribes a specific protocol, ordered from cheapest to most authoritative:

1. **`ls` the claimed path** — confirms existence and non-zero size (catches total failures and empty files)
2. **`Read` the file** — confirms content matches expectations (catches truncation, wrong-path writes, and partial writes)
3. **`git status`** — confirms the file appears as new/modified in version control (catches writes to wrong worktrees, writes outside the repo, and ephemeral /tmp paths)

This protocol is asymmetric in cost: a five-second `ls` check prevents cascading failures that waste minutes or hours downstream.

### 3. Pre-Write Archival as a Data Integrity Pattern

Memory cd0c954 (core memory, strength 1) codifies archive-before-overwrite: before any destructive transform, move the original to a dated archive directory. The compression skill (`.cursor/skills/crux-skill-memory-compress/SKILL.md`) makes this explicit in step order:

- Step 7: Archive the original
- Step 8: Write the compressed output
- Step 9: Delete the original from the working directory

The critical sequencing rule from the skill: **"Only after successful archival, proceed with writing the compressed file."** This creates a transactional envelope — if the archive step fails, the write never happens, and the original remains intact.

The archive path (`{compressionSourceArchive}/{yyyymmdd}/{original-filename}`) uses dated subdirectories for easy cleanup while preserving rollback capability and audit trail. The `.ai-ignored/` prefix excludes archives from agent context loading, preventing stale originals from polluting future sessions.

### 4. Staging Directories as Atomic Write Proxies

The `install.py` script demonstrates a staging pattern that approximates atomic writes in agent tooling:

- **`download_and_stage()`**: Downloads to `tempfile.mkdtemp()`, extracts there, verifies checksums, then returns the staging directory for installation
- **`create_backup_zip()`**: Creates a full backup to `tempfile.gettempdir()` before any modifications
- **`install_from_staging()`**: Copies verified files from staging to their final destinations

This is the closest the codebase gets to the classical write-to-temp → verify → rename pipeline. The staging directory serves as a checkpoint — if verification fails, the original state is untouched.

### 5. Checksum Verification as Content Integrity Evidence

`install.py`'s `verify_checksums()` function implements post-write content verification using SHA256 hashes:

- Reads a release manifest (`crux-release-files.json`) containing expected checksums
- Computes actual checksums of staged files via `hashlib.sha256()`
- Reports mismatches with specific file names
- Degrades gracefully — missing manifest means skip, not abort

This pattern extends naturally to agent write verification: after writing, compute a checksum of the file on disk and compare against the checksum of the content the agent intended to write.

### 6. Idempotency as Retry Safety

The `crux-software-engineer` agent definition explicitly lists "Idempotency: Scripts and tools that are safe to re-run — critical for agent workflows that may retry" as a core competency. The CRUD skill's Create operation generates deterministic IDs via `sha256(title)[:7]`, meaning re-running the same creation with the same title produces the same ID (though collision detection extends to 8 chars).

For write operations, idempotency means: writing the same content to the same path twice produces the same end state. This is naturally true for file overwrites but breaks when the write includes side effects (moving files, updating trackers, incrementing counters). The compression skill's archive step is NOT idempotent — archiving the same file twice creates two archive copies in different dated directories. This is by design (audit trail), but it means retry logic must check whether the archive already exists before re-archiving.

### 7. Test Isolation as Write Containment

Memory 9b9a4ac establishes that tests must use `tmp_path` fixtures and never modify the actual repository. This is write containment — ensuring that write operations during testing cannot corrupt the real filesystem state. The pattern maps directly to agent safety: when an agent is exploring or testing, its writes should be contained to a scratch space, not directed at production paths.

## Connections

### The Verification Stack Mirrors the Failure Taxonomy

Each layer of the verification protocol targets a specific failure class:

| Verification Layer | Catches | Cost |
|---|---|---|
| `ls` (existence + size) | Total write failure, empty files | ~1 tool call |
| `Read` (content match) | Truncation, wrong content, partial writes | ~1 tool call + comparison |
| `git status` (VCS evidence) | Wrong worktree, out-of-repo writes, ephemeral paths | ~1 shell call |
| Checksum comparison | Bit-level corruption, encoding issues | ~1 computation |

No single layer catches all failure modes. The stack is ordered by cost-effectiveness, not by coverage.

### Archive-Before-Write + Verify-After-Write = Transactional Writes

Combining memory cd0c954 (archive before) with memory 49303e0 (verify after) creates a transactional write envelope:

1. **Archive original** → if this fails, abort (original preserved)
2. **Write new content** → may silently fail
3. **Verify new content** (ls + Read + git status) → if this fails, recover from archive
4. **Clean up original** → only after verified success

This is functionally equivalent to the database pattern of write-ahead logging: the archive is the WAL entry, and verification is the commit confirmation.

### Adversarial Verification as the Ultimate Write Check

Memory 6c16dc6 reports a 25% hit rate for adversarial verification catching real issues (6 in 24 subtasks). The 49303e0 incident was one of these catches. This suggests that even with the three-layer verification protocol, having an independent agent verify file existence provides a valuable fourth layer — because the writing agent may skip or misinterpret its own verification results due to context window pressure or reasoning errors.

### Documentation Path Verification Shares the Same Root Cause

Memory dbfd3ed (file paths in docs must reference actual files) is a different manifestation of the same trust gap: an agent writes a documentation reference to a path without verifying the path exists. The fix is the same — `ls` the path before or after referencing it. This unifies write verification and reference verification under a single principle: **every filesystem claim must be backed by filesystem evidence**.

### The Gap: No Formal Write Pipeline in Agent Definitions

The codebase has the *components* of a reliable write pipeline (archival in the compress skill, staging in install.py, checksums in crux-utils, verification protocol in memory 49303e0) but lacks a unified, codified write pipeline that agents invoke as a standard operation. Each skill implements its own ad-hoc verification. A formalized `write-and-verify` primitive — available as a skill or utility — would eliminate the inconsistency.

## Summary

Write verification is the weakest link in file-based agent coordination. A real incident (memory 49303e0) proved that the Write tool can silently fail, making post-write verification mandatory. The codebase contains the building blocks of a reliable write pipeline — pre-write archival (cd0c954), staging directories (install.py), checksum verification (crux-utils + install.py), and a three-layer verification protocol (ls → Read → git status) — but these exist as scattered patterns rather than a unified primitive. The key architectural insight is that archive-before-write + verify-after-write creates a transactional envelope that converts an unreliable write operation into a recoverable one. Idempotency enables safe retries, but side-effectful operations like archival need their own idempotency guards. The gap is the absence of a formal `write-and-verify` skill that all agents invoke consistently, rather than each skill reimplementing verification ad-hoc.
