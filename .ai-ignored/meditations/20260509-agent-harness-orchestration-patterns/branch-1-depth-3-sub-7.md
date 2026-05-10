---
branch: 1
depth: 3
subfocus_index: 7
subfocus: "YAML Frontmatter as a Metadata Contract"
parent_subfocus: "Serialization Formats and Data Contracts"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

The parent subfocus identified YAML frontmatter as the central serialisation format for inter-agent data exchange in this system. This narrowing examines *why* YAML frontmatter works as a contract — the specific design choices around field partitioning, type constraints, immutability rules, and additive-only schema evolution that make it effective for multi-agent coordination without formal schema versioning infrastructure.

## Discoveries

### 1. Prose-Defined Schema with Runtime Validation

The CRUD skill (`crux-skill-memory-crud`) defines the frontmatter schema entirely in prose — a markdown table of 9 required fields and 4 optional fields with type constraints and mutation rules. There is no JSON Schema, no Protobuf definition, no TypeScript interface. Yet the Validate operation acts as a runtime schema checker, verifying:

- Field presence (all 9 required fields)
- Type constraints: `id` must be 7-char lowercase hex; `type` must be one of 6 enum values; `strength` must be a positive integer; `created`/`modified` must be valid ISO dates; `tags` must be a list; `title`/`description` must be non-empty strings
- Structural placement (file must live in the correct type subdirectory)
- Size limits (`maxMemorySize` from config)

This is a *prose schema with procedural enforcement* — the contract is human-readable and LLM-interpretable by design, not machine-parseable from a schema definition file. The validation logic is embedded in skill instructions that agents follow, not in a schema validator library.

### 2. Immutability as Referential Stability

Two fields are designated write-once: `id` and `created`. The CRUD skill enforces this at three levels:

- **Schema table**: "Immutable — never changes even if the title is edited"
- **Update procedure**: "id — never modify this field; it is immutable after creation" / "created — never modify this field; reject any attempt to change it"
- **What NOT to Do section**: "Do not modify id or created on updates — both are immutable after creation"

This triple-reinforcement is itself a design pattern for LLM-consumed contracts — the same constraint is stated declaratively (schema), procedurally (update steps), and proscriptively (anti-patterns). The redundancy compensates for the fact that the consumer is a probabilistic agent, not a deterministic parser.

The `id` field's immutability is particularly significant: it is derived from `sha256(title)[:7]` at creation time, but survives title edits. This makes it a stable foreign key that reference trackers (`.refs.yml` files), consolidation records (`consolidated_from` lists), and the memory index can all rely on without fear of invalidation. It is the anchor of the entire cross-file referencing system.

### 3. Additive-Only Schema Evolution — Three Documented Waves

The frontmatter schema has undergone at least three additive evolution events, each adding optional fields without touching the required field set:

**Wave 1 — Type transitions**: `promoted_from` (string) was added to track provenance when a memory changes type during REM sleep. Existing consumers that never trigger promotions simply never see this field.

**Wave 2 — Consolidation**: Three fields were added together: `consolidated_from` (list of IDs), `consolidation_topic` (string slug), and `consolidation_part` (integer). These form a cohesive sub-schema for multi-volume consolidated memories. Crucially, all three are optional — unconsolidated memories (the vast majority) carry none of them, and the CRUD skill's Validate operation does not require them.

**Wave 3 — Compression**: Seven fields were added: `compressed` (boolean), `compressionTarget` (integer), `beforeTokens` (integer), `afterTokens` (integer), `reducedBy` (string percentage), `compressedDate` (date), and `sourceArchive` (path). These are added by the compression skill, not the CRUD skill — a different agent entirely — yet they coexist peacefully in the same frontmatter block.

Each wave added fields that are meaningful to one specific operation (promotion, consolidation, compression) and invisible to all others. The Read operation parses all frontmatter into structured fields without discriminating between required and optional — unknown fields are simply carried along. This is the YAML equivalent of Protobuf's unknown field preservation, achieved without any schema versioning machinery.

### 4. The "Required vs Optional" Partition as a Compatibility Boundary

The 9 required fields form the *minimum viable contract* — every consumer can depend on these being present and correctly typed. The optional fields form the *extension surface* — new capabilities are expressed by adding optional fields, and existing consumers are unaffected because they never look for fields they don't know about.

This partition is the key to forward compatibility. A memory created today with `consolidated_from` can be read by code (or an agent prompt) written before consolidation existed — the reader simply sees extra YAML keys it ignores. Conversely, code written to process consolidation metadata can safely handle memories without it by checking for field presence.

Compare this with formal schema versioning:
- **JSON Schema**: Would require `additionalProperties: true` (or omission of the keyword) and careful `required` vs non-required field lists. Schema changes need version bumps and consumer migration.
- **Protobuf**: Unknown fields are preserved by default since proto3, but require `.proto` file updates, regeneration of language bindings, and version coordination across services.
- **YAML frontmatter with prose contracts**: New fields are documented in the skill that creates them. Other skills simply don't read them. No version numbers, no regeneration, no migration. The "schema" evolves by adding paragraphs to a markdown file.

### 5. Cross-File Schema Relationships Without Foreign Key Constraints

The system maintains cross-file relationships through conventions rather than enforced constraints:

- **Memory → Reference Tracker**: A memory's slug becomes the filename stem for its `.refs.yml` tracker. The CRUD Delete operation handles cascade deletion, but there is no foreign key constraint preventing orphaned trackers — REM sleep detects and cleans these up.
- **Memory → Memory**: `consolidated_from` contains `id` values of source memories that may no longer exist (they are archived after consolidation). The reference is historical, not live.
- **Memory → Config**: The `type` field's valid values are defined in `typePriority` in `crux-memories.json`. The Validate operation checks this at runtime, but there is no compile-time binding.

This is eventually-consistent referential integrity — breakages are detected and repaired during periodic maintenance (REM sleep) rather than prevented at write time. For a multi-agent system where agents operate asynchronously and may fail mid-operation, this is arguably more robust than strict foreign key constraints that could leave the system in an inconsistent state if an agent crashes between creating a memory and creating its tracker.

### 6. Config-Driven Enum Evolution (Memory ba92c4e)

Memory `ba92c4e` captures a key insight: when interactive options must mirror a domain concept (like memory types), source the options from config keys rather than hardcoding. The `type` field's valid values come from `typeTransitions` keys in config. Adding a new memory type to config automatically makes it available in the UI, the Validate operation, and the directory structure — without editing any skill or agent definition.

This is schema evolution at the *enum constraint level* — the set of valid values for a typed field can grow without touching the contract definition. The YAML frontmatter doesn't encode type constraints formally; the constraint lives in the config file and is enforced procedurally by the Validate operation.

## Connections

### Prose Contracts as LLM-Native Schema

The most striking pattern is that this entire schema system is designed for *LLM consumption*, not programmatic consumption. A JSON Schema or Protobuf definition would be more precise for a traditional service, but an LLM agent reads markdown tables and procedural instructions more reliably than formal schema definitions. The triple-reinforcement of immutability rules (declarative, procedural, proscriptive) is a recognition that the "parser" is probabilistic — it benefits from the same constraint being stated in multiple framings.

### Additive Evolution Mirrors Open-Closed Principle

The required/optional partition maps directly to the Open-Closed Principle: the schema is closed for modification (required fields never change) but open for extension (new optional fields can be added freely). This is the same design principle that makes REST APIs with optional response fields forward-compatible, and it works here for the same reason — consumers bind to a stable core and ignore what they don't understand.

### Eventual Consistency Over Strict Enforcement

The system consistently chooses eventual consistency over strict enforcement — orphaned trackers are cleaned up in REM sleep rather than prevented by transactions, type placement mismatches are detected by Validate rather than prevented by directory-level constraints, and stale `consolidated_from` references point to archived (not deleted) memories. This mirrors memory `d944d7c` (spec index can drift from subtask details) — the system acknowledges drift as inevitable in a multi-agent environment and builds repair mechanisms rather than prevention mechanisms.

### Immutability as Coordination Primitive

The `id` and `created` immutability rules serve the same function as immutable event IDs in event-sourced systems — they provide stable reference points that multiple independent agents can rely on without coordination. The `id` field enables cross-file references (reference trackers, consolidation records, index entries) that survive all mutations to the memory itself. Without this immutability guarantee, every agent that holds a reference would need to poll for ID changes — a coordination overhead that doesn't scale.

### The Provenance Memory (f8bd856) as Schema Design Evidence

Memory `f8bd856` documents the deliberate decision to overload the existing `source` field with a fixed string (`"adhoc"`) rather than adding a new `origin` enum field. This is additive evolution taken to its logical conclusion — even when a new concept (ad-hoc creation) needs representation, the preference is to reuse existing fields with new value conventions rather than adding schema surface. The decision explicitly rejected alternatives that would have expanded the schema (a new field) in favor of expanding the value space of an existing field.

## Summary

YAML frontmatter works as an inter-agent metadata contract because it implements five key design choices: (1) a fixed set of 9 required fields forming a minimum viable contract that every consumer can depend on; (2) an open-ended set of optional fields that enable additive-only schema evolution without version numbers or migration; (3) write-once immutability on `id` and `created` providing stable cross-file reference anchors; (4) prose-defined schema with procedural enforcement via the Validate operation, optimised for LLM consumption over formal machine parsing; and (5) eventual consistency for referential integrity, preferring periodic repair (REM sleep) over strict write-time constraints. The schema has already undergone three waves of additive evolution (promotion tracking, consolidation metadata, compression metadata) without breaking any existing consumers — the same forward-compatibility property that JSON Schema and Protobuf achieve through formal versioning, achieved here through the simpler mechanism of optional YAML keys that unknown consumers silently skip.
