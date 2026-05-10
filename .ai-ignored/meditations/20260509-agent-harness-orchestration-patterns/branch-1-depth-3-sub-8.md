---
branch: 1
depth: 3
subfocus_index: 8
subfocus: "Provenance Tagging and Multi-Writer Disambiguation"
parent_subfocus: "Serialization Formats and Data Contracts"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

When multiple agents and commands write to a shared data store, the question "who wrote this, when, and why?" becomes a first-class design problem. This narrowing was chosen because the parent subfocus (serialization formats and data contracts) establishes the *shape* of inter-agent data, but shape alone doesn't prevent ambiguity — you also need provenance metadata woven into that shape. The sibling subfocuses cover schema design (sub-7) and human-vs-machine format tension (sub-9); this subfocus addresses the orthogonal concern of *attribution* within whatever format is chosen.

## Discoveries

### 1. The `source` Field Pattern (memory f8bd856)

The most direct provenance mechanism: every memory entry carries a `source` field that records its origin. Two forms exist:
- **Work-item slug** (e.g. `"20260425-crux-remember"`) — for entries extracted from structured artifacts via `/crux-dream`
- **Fixed literal `"adhoc"`** — for entries created via `/crux-remember` without an originating artifact

Key design decisions from the original spec (Decision 3 of `spec-crux-remember-20260425.md`):
- A constant string beats a missing/empty value — absence of provenance looks like data corruption, not legitimate ad-hoc creation
- Path-based inference was rejected: ad-hoc and extracted memories live in the same directories (`memories/{type}/`), so paths carry no signal
- A separate enum field was rejected: the existing `source` field already carries provenance; adding another field increases schema surface for no gain

**Downstream consumers**: REM sleep consolidation applies different rules to ad-hoc vs extracted memories (e.g. longer dormancy before consolidating ad-hoc entries). `/crux-recall spec-name` filters by source. Audit and debugging narrow triage by knowing whether a memory came from a structured artifact or freeform input.

### 2. `consolidated_from` — Merge Provenance Trail

When REM sleep consolidation merges N memories into one (or into multi-volume sets), the resulting memory's frontmatter carries `consolidated_from: [list of original id values]`. This is:
- **Set once, never modified** — the audit trail is append-only; no rewriting history
- **Shared across volumes** — when a consolidation topic splits into multiple parts (e.g. `plugin-architecture-pt1.memory.crux.md`, `plugin-architecture-pt2.memory.crux.md`), every volume carries the full list of all source IDs, not just its own subset
- **Paired with `consolidation_topic` and `consolidation_part`** — for multi-volume sets, these fields reconstruct the original grouping without requiring a separate manifest

The original member memories are also archived to `{compressionSourceArchive}/{yyyymmdd}/` before deletion, creating a physical fallback alongside the metadata trail.

### 3. `promoted_from` — Type-Transition Audit Trail

When a memory's type changes (e.g. `idea → learning` at strength 5, `learning → core` at strength 15), the skill writes `promoted_from: "{old_type}"` (or `demoted_from` for demotions) into the frontmatter. This preserves the memory's lifecycle history in-place:
- Downstream operations can distinguish a core memory that started as core (no `promoted_from`) from one that was earned through repeated validation (has `promoted_from: "learning"`)
- Reversibility: if a promoted memory later proves unreliable, the original type is recorded for potential reversion
- Set automatically by the crud skill's Update operation (step 3a) and the rebalance skill's transition logic (step 12)

### 4. Reference Tracker Provenance — Who Referenced, Not Just How Often

Reference tracker files (`.refs.yml`) record not just counts but *attribution*:

```yaml
recent_references:
  - spec: "20260401-dashboard-performance"
    count: 4
    last: 2026-04-01
  - conversation_id: "a3f7b2c"
    count: 3
    last: 2026-03-30
    context: "Discussed memoization strategy for data table components"
```

The source key is polymorphic: within a unit of work it uses `{unitOfWork}: "{id}"` (e.g. `spec: "20260403-crux-memories"`); in standalone conversations it uses `conversation_id: "{id}"`. This means:
- Strength calculations can be weighted by source diversity, not just raw count
- A memory referenced by 3 different specs is arguably more validated than one referenced 10 times in one conversation
- The `context` field provides human-readable rationale for why the reference occurred
- The `maxReferencesStored` cap (default 10) bounds storage while keeping the most recent references via FIFO eviction

### 5. CRUX Compression Provenance Chain

Compressed memory files carry a layered provenance chain:
- `compressed: true` — binary flag that the body is CRUX notation, not natural language
- `sourceArchive: ".ai-ignored/memories/sources/20260405/archive-source-before-compression.memory.md"` — physical path to the archived original
- `compressedDate`, `beforeTokens`, `afterTokens`, `reducedBy` — compression metadata that documents the transformation parameters
- Memory cd0c954 (core) explicitly mandates: archive first, then compress — never overwrite without preserving the original

For non-memory CRUX compression (rules, agents), the chain uses:
- `sourceChecksum: "{hash}"` — content hash of the source at compression time, enabling drift detection
- `generated: {timestamp}` — when the compressed output was produced
- The `> [!IMPORTANT] > Generated file - do not edit!` banner — a human-readable guard against accidental modification

### 6. Memory d944d7c — The Drift Warning

Memory d944d7c (redflag: "Spec index text can drift from subtask details") is relevant here not for its spec-system content but for its general principle: when the same truth is represented at multiple layers, the layers will drift. This is exactly the risk that explicit provenance mitigates — without `source`, `consolidated_from`, `promoted_from`, and `sourceArchive`, the only way to reconstruct a memory's lineage would be to infer it from timestamps, paths, and content similarity. Inference-based provenance degrades as the corpus evolves.

## Connections

### Provenance as a Layered DAG

The provenance fields form a directed acyclic graph:

```
source (origin command/spec)
  └→ consolidated_from (merge lineage)
       └→ promoted_from (type transition history)
            └→ sourceArchive (compression lineage)
                 └→ .refs.yml (usage attribution)
```

Each layer answers a different question: Where did this come from? What was it made of? What did it used to be? Where is its original form? Who has used it? Together they form a complete lifecycle record — any single layer can be consulted independently, but the full chain provides end-to-end traceability.

### Explicit vs Implicit Provenance

A consistent design principle emerges: **every provenance signal is stored as an explicit field, never inferred from path, position, or timestamp**. This was a deliberate choice:
- Paths change during type transitions (memory moves from `memories/idea/` to `memories/learning/`)
- Timestamps can collide or be ambiguous across timezones
- Content similarity is fuzzy and expensive to compute
- Explicit fields survive grep, survive file moves, survive compression, survive consolidation

### The Cost of Provenance

Each provenance field adds schema surface. The system manages this by:
- Making most provenance fields optional (only set when the event occurs)
- Using the existing `source` field rather than adding a parallel `origin` enum
- Keeping reference trackers in separate files rather than bloating memory frontmatter
- Capping stored references via `maxReferencesStored`

### Provenance Enables Downstream Intelligence

The separation of provenance from content enables REM sleep to make smarter decisions:
- Ad-hoc memories can have longer dormancy before consolidation (they lack peer review)
- Memories with diverse reference sources are more resistant to demotion
- Consolidated memories preserve their full ancestry for conflict resolution
- Compressed memories can be restored to their exact original form via `sourceArchive`

### Generalizability to Other Multi-Agent Systems

The `source` field pattern generalizes directly: any shared store written to by multiple agents benefits from a per-entry origin tag. The reference tracker pattern generalizes similarly: any data consumed by multiple agents benefits from recording *who* consumed it and *when*. Together, these create a bidirectional provenance graph — who wrote, who read — without requiring a centralized coordination service.

## Summary

The CRUX memory system implements a comprehensive, layered provenance model where every transformation — creation, consolidation, type transition, compression, consumption — is recorded as an explicit frontmatter field or tracker entry. Six distinct provenance mechanisms (`source`, `consolidated_from`, `promoted_from`, `sourceArchive`/`sourceChecksum`, `.refs.yml` attribution, `generated` banner) collectively ensure that no memory's lineage depends on inference from paths, timestamps, or content analysis. The core design principle is that explicit provenance survives every mutation the system can perform — file moves, compression, consolidation, promotion — while inference-based provenance degrades at each step. This pattern generalizes to any multi-agent architecture where shared data stores receive writes from multiple sources: tag origin at write time, record attribution at read time, and preserve transformation history at every intermediate step.
