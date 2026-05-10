# Branch 1 Expansion Notes (Internal)

## Memories Queried

- `ba74013` — Session-scope command design: in-band handling and subagent inheritance (strength 2)
- `f8bdc0d` — Agent definitions should reference skills for operations, not duplicate spec content (strength 1)
- `0a157b3` — Meditate command decomposes into recursive phases (strength 1)
- `31fec9d` — Meditate uses read-only exploration with optional memory creation (strength 1)
- `efc4c24` — Per-phase parallel subagent execution reduces wall-clock time (strength 1)
- `f8bd856` — Tag entry origin with source field (strength 1)
- `49303e0` — Agent-reported file creation must be verified on disk (strength 1)
- `d944d7c` — Spec index can drift from subtask details (strength 1)
- `ba92c4e` — Source AskQuestion options from config keys (strength 1)
- `d5e503c` — CRUX rule phase-block ordering reflects evaluation precedence (strength 1)
- `cd0c954` — Archive original source files before overwriting (strength 1)
- `3bf625d` — Meditate synthesis must not hallucinate connections (strength 1)

## Key Patterns Identified

1. File-based coordination is the dominant inter-agent pattern in this codebase
2. Session-scope inheritance requires explicit contracts in alwaysApply rules
3. Provenance tagging via source fields is a serialization best practice
4. File writes can silently fail — verification is critical
5. Ordering of serialized blocks reflects precedence for LLM consumption
6. Multi-layer state drifts — the more local layer is authoritative
7. Config-driven options prevent drift between semantic model and consumers

## Derived Child Subfocuses

1. File-based coordination protocols — predictable paths, polling, frontmatter contracts, verification
2. Session-scope state propagation — flags, config, inheritance contracts, alwaysApply semantics
3. Serialization formats and data contracts — schemas, provenance, ordering, evolution
