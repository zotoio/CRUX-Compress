---
branch: 1
depth: 3
subfocus_index: 3
subfocus: "Path Convention Design and the Coordination Namespace"
parent_subfocus: "File-Based Coordination Protocols"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

The parent subfocus (File-Based Coordination Protocols) examines the filesystem as a communication channel. This narrowing focuses on the *naming layer* — the conventions that map agent intent to file paths. Path conventions are the "addressing scheme" of file-based coordination; if two agents disagree on how to construct a path, coordination silently breaks without any error signal. This is a distinct concern from polling strategies (how often to check) or write verification (how to confirm integrity).

## Discoveries

### Memory corpus findings

**Memory d944d7c** (spec index drift): Warns that a spec's top-level index can contain text contradicting its subtask details, with subtask details being authoritative. This is structurally identical to path convention drift — two representations of the "same" information (the expected path) can diverge, and only the ground truth (what the child actually wrote to disk) is authoritative. The reader's expectation is the "spec index"; the writer's output is the "subtask detail."

**Memory 96a7410** (tooling defaults drift): The crux-utils.py default compression target was 20% while CRUX.md specified 25%. This went unnoticed until a dedicated refactor. Applied to path conventions: when a path template is defined in one place (agent definition) and reconstructed in another (spawning logic), the two can silently diverge — same class of problem, same invisibility.

**Memory dbfd3ed** (file paths in docs must reference actual files): Documentation listed `.sh` hook files when the actual files were `.py`. Path conventions exist in documentation, code, and agent minds simultaneously — any of these can drift from reality.

**Memory 49303e0** (agent-reported file creation must be verified on disk): The Write tool can silently fail, meaning an agent believes it wrote to a path but the file doesn't exist. For coordination, this means a parent polling for a child's output file may wait indefinitely — the path convention was followed correctly but the write never materialised.

**Memory f8bd856** (tag entry origin with source field): The `source` field on memories distinguishes "adhoc" from spec-derived entries. This is a metadata convention layered on top of the path convention (`memories/{type}/` for base scope) — provenance encoded in data rather than path, showing that not all coordination information belongs in the filename.

### Codebase pattern analysis

**Five distinct path convention families** coexist in this codebase:

1. **Meditation positional encoding**: `branch-{N}-depth-{D}-sub-{S}.md` with fixed bookend files `facets.md` and `consolidation.md`. Every dimension of the tree position is encoded in the filename.

2. **Dream summary templates**: `dream-{slug}-{yyyymmdd}.md` — configured via `summaryPattern` in `crux-memories.json`. The template is a *single source of truth* that all consumers reference.

3. **Memory slug-based naming**: `{slug}.memory.md` / `{slug}.memory.crux.md`. The extension encodes compression state — consumers strip suffixes longest-first (`.memory.crux.md` before `.memory.md`) to extract the slug.

4. **Sentinel files**: `.crux/pending-compression.json` and `.crux/pending-index-rebuild.json`. Existence = boolean signal, but content = structured data (file lists, timestamps). Written by hooks, consumed by session-start.

5. **Spec state files**: `_execution-state.yml` — underscore prefix convention for "internal" files. Located *inside* the work item directory, making scope implicit from position rather than from filename.

### A live path convention inconsistency

The agent definition's working directory tree diagram (lines 312-332) shows depth-3 files with a **globally sequential** sub-index: `branch-1-depth-3-sub-1.md` through `branch-1-depth-3-sub-9.md`, where sub-4 through sub-6 belong to depth-2-sub-2 and sub-7 through sub-9 belong to depth-2-sub-3. But the textual protocol description says each parent passes `subfocusIndex` as 1, 2, or 3 — implying a **per-parent-relative** index. If a depth-2 agent spawns children with subfocusIndex 1, 2, 3 regardless of its own position, all three depth-2 agents would write `branch-1-depth-3-sub-{1,2,3}.md` — colliding on the same filenames. The tree diagram implicitly assumes a global mapping; the protocol spec implies relative indexing. This is exactly the kind of drift that memory 96a7410 warns about.

## Connections

### Determinism as the prerequisite for decoupled coordination

Every path convention in this codebase is deterministic — given the same inputs (branch number, depth, subfocus index), any agent can independently compute the same path without communicating with the writer. This is what makes file-based coordination work without a central broker. The path *is* the address. The meditation convention packs `(branch, depth, subfocus)` into the filename; the memory convention packs `(slug, compressed?)` into the filename; sentinel files use a fixed path that every participant knows. Determinism enables the consumer to construct the expected path *before* the producer writes it, which is what makes polling possible.

### The sentinel/output architectural distinction is blurry in practice

Pure sentinel files (presence = boolean) would be empty or minimal. But both `.crux/pending-compression.json` and `.crux/pending-index-rebuild.json` carry structured payloads — file lists, timestamps, `needsRebuild` flags. They're hybrids: the *existence* check gates whether to act, but the *content* determines what to act on. This works because the consumer (session-start hook) first checks `is_file()` (sentinel behaviour) then reads the content (output behaviour). The hybrid pattern is more capable but also more fragile — a corrupt sentinel file (e.g. invalid JSON) can break the content read while still passing the existence check. The detect-memory-changes hook already handles this with a try/except fallback.

### Extension-based type discrimination is a compact encoding but creates parsing fragility

Memory files use `.memory.crux.md` vs `.memory.md` to encode compression state. The slug extraction code (`_extract_slug` in scanner.py, `slug_from_filename` in memory-index.py) strips suffixes longest-first — critical because `.memory.crux.md` ends with `.md` too, so naive suffix stripping would produce wrong slugs. This is a good design (longest-match-first is deterministic), but it means every new consumer must implement the same stripping logic in the same order. The MEMORY_EXTENSIONS tuple in detect-memory-changes.py lists `(".memory.md", ".memory.crux.md")` — used for matching, not stripping, but if a third variant emerged (e.g. `.memory.archive.md`), every consumer site would need updating.

### Human readability and machine parseability are complementary, not competing

The meditation filenames (`branch-1-depth-2-sub-3.md`) are simultaneously human-scannable (you can tell the tree position at a glance) and machine-parseable (a regex trivially extracts N, D, S). Memory slugs (`archive-source-before-compression.memory.crux.md`) are human-readable descriptions that also serve as deterministic identifiers. The dream summary pattern (`dream-{slug}-{yyyymmdd}.md`) embeds both provenance and temporal information. All three families achieve dual readability by encoding structured data into hyphen-separated segments — a lightweight, filesystem-safe serialisation.

### Config-sourced templates vs hardcoded path patterns

The dream summary pattern lives in `crux-memories.json` as `summaryPattern`, making it a configurable single source of truth. The meditation path convention, by contrast, is hardcoded in prose across the agent definition and the command file — no config key, no shared constant. The memory file extension convention is partially codified (the MEMORY_EXTENSIONS tuple) but duplicated across at least four files. The degree of centralisation correlates with change frequency: dream patterns are user-configurable (one config key), memory extensions are stable (duplicated but rarely changed), and meditation paths are session-specific (hardcoded in prose, changed by editing the agent definition). This suggests a design heuristic: centralise conventions that users might configure; duplicate conventions that are architectural invariants.

### The `_execution-state.yml` underscore prefix is a distinct convention from sentinel files

Both signal "something about this directory's state," but `_execution-state.yml` is positional (it lives *inside* the directory it describes) while sentinel files are global (they live in `.crux/`). The underscore prefix also signals "don't list this alongside user content" — a soft convention from build tools and web servers. This positional-vs-global distinction matters for coordination: positional state files scale naturally (each spec gets its own), while global sentinel files need explicit file-list management to avoid the "one file tracking all pending work" bottleneck.

## Summary

Path conventions are the addressing layer of file-based agent coordination — they make decoupled coordination possible by enabling consumers to independently compute expected file locations. This codebase uses five distinct convention families, each optimised for its domain: positional encoding for tree structures, slug-based naming for content identity, config-sourced templates for user-customisable patterns, extension-based type discrimination for variant encoding, and sentinel files for cross-session state signals. Good conventions share four properties: determinism (same inputs → same path), collision avoidance (no two writers target the same path), human readability (tree position visible at a glance), and machine parseability (regex-extractable structured data). The primary risk is convention drift — when a path template is defined in one place and reconstructed in another, silent divergence can cause agents to write and read at different locations. The codebase already exhibits one live instance of this: the meditation depth-3 file tree diagram implies globally sequential sub-indices while the protocol description implies per-parent-relative indices. Centralising path templates (as the dream system does via `summaryPattern` in config) mitigates drift; hardcoding in prose (as the meditation system does) invites it.
