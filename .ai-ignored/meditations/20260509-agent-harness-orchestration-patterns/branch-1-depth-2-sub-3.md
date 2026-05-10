---
branch: 1
depth: 2
subfocus_index: 3
subfocus: "Serialization Formats and Data Contracts"
parent_subfocus: "State Coordination and Handoff Mechanisms"
timestamp: 2026-05-09T19:42:00+10:00
---

## Subfocus Rationale

The parent subfocus examines how multi-agent systems pass state between parent and child agents. Siblings cover the coordination protocols (file paths, polling, verification) and session-scope propagation (flags, config inheritance). This subfocus addresses the orthogonal concern of *how the data itself is structured* — the serialization formats, metadata contracts, provenance mechanisms, and schema evolution strategies that make inter-agent data exchange reliable regardless of which coordination protocol delivers it.

## Discoveries

### 1. Prose-Defined Schema with Procedural Enforcement

The CRUX memory system defines its frontmatter schema entirely in prose — markdown tables in `crux-skill-memory-crud/SKILL.md` specifying 9 required fields and 4 optional fields with type constraints. There is no JSON Schema, Protobuf, or TypeScript interface. Instead, the Validate operation acts as a runtime schema checker: an LLM agent reads the prose rules and applies them. This is a deliberate design for a system where the primary consumer is an LLM, not a compiler.

Key constraints are enforced through triple-reinforcement — the same rule stated declaratively (schema table), procedurally (update steps), and proscriptively (anti-patterns). This redundancy compensates for the probabilistic nature of LLM parsing.

### 2. Additive-Only Schema Evolution Without Versioning

The frontmatter schema has undergone at least three waves of additive evolution:
- **Wave 1 — Type transitions**: `promoted_from` added for lifecycle tracking
- **Wave 2 — Consolidation**: `consolidated_from`, `consolidation_topic`, `consolidation_part` added as a cohesive sub-schema
- **Wave 3 — Compression**: 7 fields (`compressed`, `compressionTarget`, `beforeTokens`, `afterTokens`, `reducedBy`, `compressedDate`, `sourceArchive`) added by a different skill entirely

Each wave added optional fields. Existing consumers that don't know about new fields simply skip them — the YAML equivalent of Protobuf's unknown field preservation, achieved without version numbers, schema migration, or generated code. The required/optional partition maps to the Open-Closed Principle: closed for modification (required fields never change), open for extension.

### 3. Immutability as a Cross-File Coordination Primitive

Two fields are designated write-once: `id` (sha256(title)[:7]) and `created`. The `id` survives title edits, making it a stable foreign key that reference trackers, consolidation records, and the memory index all rely on. This serves the same function as immutable event IDs in event-sourced systems — stable reference points that multiple independent agents can use without coordination.

### 4. Six-Layer Provenance Model

The system implements comprehensive provenance through explicit fields rather than path/timestamp inference:

| Layer | Mechanism | Question Answered |
|-------|-----------|-------------------|
| Origin | `source` field ("spec-slug" or "adhoc") | Who created this? |
| Merge | `consolidated_from` (list of original IDs) | What was it made of? |
| Transition | `promoted_from` / `demoted_from` | What did it used to be? |
| Compression | `sourceArchive`, `sourceChecksum` | Where is the original? |
| Usage | `.refs.yml` with polymorphic source keys | Who consumed it? |
| Generation | `generated` timestamp + banner | When was this derived? |

These form a directed acyclic provenance graph that survives every mutation: file moves, compression, consolidation, promotion. Explicit provenance was deliberately chosen over inference — paths change during type transitions, timestamps collide across timezones, and content similarity is expensive to compute.

### 5. Three-Format Architecture Optimized for LLMs

The system uses a deliberate format hierarchy matching different consumers:

```
CRUX notation   → token-constrained LLM (5-10x compression)
Markdown body   → LLM + human (zero deserialization needed)
YAML frontmatter → human diff + machine indexing (readable, scannable)
JSON config      → CI/CD, install scripts (strict, no ambiguity)
```

The choice of markdown+YAML over pure JSON or protobuf reflects the primary consumer: LLMs interpret markdown tables and procedural instructions more reliably than formal schema definitions. The cost is real — no IDE autocomplete, no compile-time guarantees, YAML type coercion risks (memory 96a7410 documented drift between tooling defaults and spec) — but bounded by the fact that the primary "parser" is robust to ambiguities that would break traditional parsers.

### 6. Eventual Consistency Over Strict Enforcement

The system consistently chooses repair over prevention for data integrity:
- Orphaned trackers → cleaned up during REM sleep, not prevented by transactions
- Type placement mismatches → detected by Validate, not prevented by directory constraints
- Stale `consolidated_from` → points to archived (not deleted) memories
- Cross-file references → convention-based (slug matching), not foreign key enforced

This mirrors memory d944d7c's lesson: drift is inevitable in multi-agent environments, so build repair mechanisms rather than prevention mechanisms.

## Connections

### Data Contracts as Agent Communication Protocol

The frontmatter schema functions as an implicit communication protocol between agents. The CRUD skill is the "writer API," the index builder is the "reader API," and the Validate operation is the "protocol checker." No network protocol or message queue is needed — the shared file system with agreed-upon field contracts provides equivalent guarantees for an asynchronous, crash-prone multi-agent system.

### Config-Driven Enums Prevent a Class of Drift

Memory ba92c4e captures a key anti-drift pattern: when interactive options must mirror a domain concept (like memory types), source the options from config keys. Adding a new memory type to `typeTransitions` in config automatically propagates to the UI, Validate, and directory structure. This is schema evolution at the enum constraint level — the set of valid values for a typed field grows without touching the contract definition. Combined with memory 96a7410's warning about tooling-spec drift, the pattern that emerges is: **single-source-of-truth for constraint definitions, procedural enforcement at every consumption point**.

### The Provenance Graph Enables Intelligent Downstream Decisions

Provenance isn't just audit — it drives operational logic:
- REM sleep applies longer dormancy to `source: "adhoc"` memories (they lack peer review)
- Memories with diverse reference sources resist demotion
- Consolidated memories preserve full ancestry for conflict resolution
- `sourceArchive` enables exact restoration of compressed memories

### CRUX Notation as a Novel Fourth Format Layer

CRUX creates a format that is neither human-readable (requires the CRUX.md key) nor machine-parseable by conventional tools (no parser exists; the "parser" is an LLM). It is purpose-built for a consumer class that didn't exist when traditional serialization formats were designed: a token-counting LLM that reads sequentially and benefits from semantic density. Memory d5e503c shows that even ordering within CRUX blocks carries semantic weight — a property impossible in key-value formats where ordering is undefined.

### Git Trackability as an Architectural Constraint

All format layers share one hard constraint: they must be plain text that git can diff, merge, and track. This eliminates binary formats, database-backed stores, and deeply nested structures. The system trades parsing strictness for collaboration tooling compatibility. Memory 6c16dc6 (adversarial verification catches gaps at 25% hit rate) depends on this — verification runs on diffable text files.

## Child Subfocuses

Three narrower threads were explored at depth 3:

### Sub-7: YAML Frontmatter as a Metadata Contract
How the 9-required / N-optional field partitioning creates forward-compatible contracts without schema versioning. Examined immutability rules, additive evolution waves, eventual consistency for referential integrity, and the triple-reinforcement pattern for LLM-consumed constraints.

### Sub-8: Provenance Tagging and Multi-Writer Disambiguation
How `source`, `consolidated_from`, `promoted_from`, `sourceArchive`, and `.refs.yml` attribution create a six-layer provenance DAG where every transformation is recorded explicitly. Examined the design principle of explicit over implicit provenance and its survival across file moves, compression, and consolidation.

### Sub-9: The Tension Between Human-Readable and Machine-Parseable Formats
Why the system uses markdown+YAML over pure JSON or protobuf, and the three-format stack (JSON config, YAML frontmatter, markdown body) plus CRUX as a fourth layer. Examined the consumer-optimized format pyramid, the cost of prose-defined schemas, and git trackability as an architectural constraint.

## Child Insights

### From Sub-7 (YAML Frontmatter as Contract)

The prose-defined schema works because the primary "parser" is probabilistic — an LLM benefits from the same constraint stated in declarative, procedural, and proscriptive framings simultaneously. The required/optional partition is the key to forward compatibility: three waves of schema evolution (promotion, consolidation, compression) were each absorbed without breaking any existing consumer. Immutability of `id` and `created` provides referential stability analogous to immutable event IDs in event-sourced systems. Cross-file references use eventual consistency (REM sleep cleanup) rather than strict foreign key constraints — a pragmatic choice for a crash-prone multi-agent environment where an agent might fail between creating a memory and its tracker.

### From Sub-8 (Provenance Tagging)

Six distinct provenance mechanisms collectively ensure no memory's lineage depends on inference from paths, timestamps, or content. The provenance fields form a DAG: `source → consolidated_from → promoted_from → sourceArchive → .refs.yml`. Each layer answers a different lifecycle question. The core design principle is that explicit provenance survives every mutation the system performs (moves, compression, consolidation, promotion), while inference-based provenance degrades at each step. The `source` field pattern generalizes directly to any shared store with multiple writers. Reference trackers generalize similarly — recording both who wrote and who read creates a bidirectional provenance graph without centralized coordination.

### From Sub-9 (Human vs Machine Format Tension)

The format choices reflect an optimization hierarchy: LLM comprehension > human reviewability > git trackability > machine parsing strictness. JSON handles the narrow case where ambiguity is unacceptable (config). YAML frontmatter handles metadata that must be both indexable and diffable. Markdown handles the primary consumer — LLMs interpreting definitions without deserialization. CRUX handles the edge case where even markdown is too token-expensive. The "no formal schema" choice is deliberate: adding `consolidated_from` required updating only prose documentation; the LLM understood immediately without schema migration. The cost (type coercion, drift, no autocomplete) is bounded by the LLM's robustness to ambiguities that would break traditional parsers.

## Summary

Serialization formats and data contracts in this multi-agent system are built on four key architectural decisions: (1) **prose-defined schemas with procedural enforcement** — frontmatter contracts are documented in markdown and enforced by LLM-agents running Validate operations, optimizing for the primary consumer (LLMs) over traditional parsers; (2) **additive-only schema evolution** — a required/optional field partition enables three waves of capability addition without version numbers, migration scripts, or breaking changes; (3) **explicit six-layer provenance** — `source`, `consolidated_from`, `promoted_from`, `sourceArchive`, `.refs.yml` attribution, and `generated` banners create a complete lifecycle DAG where no lineage question requires inference from paths or timestamps; and (4) **a consumer-optimized format stack** — JSON for strict machine config, YAML frontmatter for diffable metadata, markdown for LLM-interpretable content, and CRUX notation for token-constrained contexts. The system consistently trades parsing strictness for LLM comprehension, repair (REM sleep) for prevention (foreign keys), and prose documentation for formal schemas — choices that reflect a world where the most important data consumer is not a compiler but a language model.
