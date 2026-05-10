---
branch: 1
depth: 1
subfocus_index: 1
subfocus: "State Coordination and Handoff Mechanisms"
parent_subfocus: "Agent harness orchestration patterns"
timestamp: 2026-05-09T19:44:00+10:00
---

## Subfocus Rationale

State coordination is the connective tissue of multi-agent orchestration. Without reliable mechanisms for passing context, results, and behavioral contracts between agents, every other orchestration concern — failure handling, resource governance, task decomposition — operates on unstable ground. This branch examines the "plumbing" that makes multi-agent systems coherent: how agents exchange data, propagate intent, and maintain contract fidelity across spawn boundaries.

## Discoveries

### From Memory Queries

Twelve memories were queried, spanning core principles, learned patterns, and documented failure modes:

- **ba74013** (learning, strength 2): Session-scope flags need explicit `alwaysApply` rules for subagent inheritance. Every session-flag spec must answer three questions: what inherits, what breaks inheritance, where is the contract documented.
- **49303e0** (redflag, strength 1): File writes can silently fail — the Write tool can return without persisting. Agent narratives are hypotheses; filesystem state is ground truth.
- **f8bd856** (learning, strength 1): When multiple writers contribute to a shared store, tag every entry with an explicit `source` field for provenance. Constants like `"adhoc"` are signals, not absence.
- **d944d7c** (redflag, strength 1): Multi-layer state (spec index + subtask files) drifts. The more local/specific layer is authoritative.
- **d5e503c** (learning, strength 1): Ordering of phase blocks in serialized rules encodes override precedence — exploiting LLM sequential attention.
- **31fec9d** (core, strength 1): Meditate enforces read-only exploration with a single persistence gate. Safety comes from separating exploration from side effects.
- **ba92c4e** (learning, strength 1): Sourcing interactive options from config keys (single-source-of-truth) prevents drift between the semantic model and its UI representations.
- **efc4c24** (learning, strength 1): Dependency-based phasing with parallel subagents eliminates coordination overhead for independent subtasks.
- **f8bdc0d** (core, strength 1): Agent files orchestrate; skill files contain detailed logic. This separation affects how state flows between architectural layers.
- **cd0c954** (core, strength 1): Archive original source files before overwriting — a write-safety primitive for data integrity.
- **96a7410** (redflag, strength 1): Tooling defaults must align with specification defaults — drift between implementations is silent until caught by dedicated audit.
- **3bf625d** (redflag, strength 1): Synthesis must not hallucinate connections — distinguish recalled vs discovered vs inferred provenance.

### Cross-Memory Patterns

Three meta-patterns emerged from the memory corpus:

1. **Explicit over implicit**: The system consistently favors explicit state declarations (source fields, alwaysApply rules, frontmatter contracts) over inference from paths, timestamps, or context. Every memory touching coordination encodes this preference.

2. **Repair over prevention**: Rather than enforcing referential integrity at write-time (foreign keys, transactions), the system uses eventual consistency with periodic repair cycles (REM sleep, index rebuilds, validation passes). This matches the reality of crash-prone LLM agents.

3. **Layered redundancy**: Critical constraints are stated in multiple forms (declarative schema, procedural steps, proscriptive anti-patterns) to compensate for the probabilistic nature of LLM compliance.

## Connections

### The Three Coordination Layers Form a Complete Protocol Stack

The three child subfocuses revealed that state coordination operates as a protocol stack:

```
Layer 3: Serialization (data contracts)  — WHAT is exchanged
Layer 2: Propagation (session scope)     — HOW intent flows
Layer 1: Transport (file-based protocols) — WHERE data moves
```

Each layer makes independent design decisions, but they compose: frontmatter contracts (Layer 3) define what fields a file must contain, propagation rules (Layer 2) determine which agents load which behavioral directives, and file-based protocols (Layer 1) define the naming, detection, and verification mechanisms for the physical files. A failure at any layer cascades: a silently failed file write (Layer 1) renders a perfect frontmatter contract (Layer 3) irrelevant.

### The Push-Pull Duality Spans All Three Layers

A unifying framework emerged: **pull** (each agent independently reads shared state from known locations) vs **push** (state is explicitly passed at spawn time).

| Layer | Pull Mechanism | Push Mechanism |
|-------|---------------|----------------|
| Transport | File polling (child writes, parent polls) | Direct parameter passing at spawn |
| Propagation | `alwaysApply` rules (IDE injects automatically) | Spawn-time arguments (ephemeral context) |
| Serialization | Config file read by all consumers | Override fields in spawn prompts |

Pull achieves zero-coordination consensus for persistent state. Push is required for ephemeral state. The mature pattern is hybrid: pull for defaults, push for overrides — mirroring the plugin system's advisory gates with opt-out overrides (b0c02ea).

### The Knows-vs-Acts Gap Is the Fundamental Challenge

The deepest insight across all three subfocuses: **delivering state to an agent is necessary but not sufficient for compliance**. This manifests differently at each layer:

- **Transport**: A file exists (detection) but may be invalid (verification gap)
- **Propagation**: A rule is loaded (knows) but may be ignored (acts gap) — competing MUST directives, attention dynamics, conditional parsing
- **Serialization**: A contract is defined (schema) but may be violated (enforcement gap) — eventual consistency rather than strict enforcement

The system's answer is a **compliance testing pyramid**: directive trust (weakest) → self-report → output-pattern analysis → side-effect observation → adversarial verification (strongest). Currently, most propagation checking operates at levels 1-3; advancing critical checks to levels 4-5 would close the gap.

### File-Based Coordination Is a Mature but Informally Specified Protocol

Five distinct coordination families coexist (meditation positional encoding, dream summaries, memory files, sentinel files, spec state files), each with different naming conventions, detection strategies, and verification expectations. The protocol works because of three properties:

1. **Path determinism**: Any agent independently computes the same file path given the same inputs — no central broker needed
2. **Existence as signal**: File presence/absence is the primary coordination primitive, augmented by structured content
3. **Verification as complement**: Post-write verification (ls → Read → git status) compensates for unreliable persistence

But the protocol is specified in prose, not code. A concrete drift instance was identified: meditation depth-3 file numbering shows global vs relative indexing ambiguity in the spec itself.

### Serialization Optimizes for the Primary Consumer

Format choices reflect an optimization hierarchy: **LLM comprehension > human reviewability > git trackability > machine parsing strictness**. This produces a four-format stack:

- **JSON**: Strict machine config (`.crux/crux-memories.json`)
- **YAML frontmatter**: Diffable metadata (memory files, meditation outputs)
- **Markdown body**: LLM-interpretable content (no deserialization needed)
- **CRUX notation**: Token-constrained LLM contexts (5-10x compression)

The "no formal schema" choice is deliberate: the primary parser (an LLM) is robust to ambiguities that would break traditional parsers, and schema evolution is additive-only, absorbed without version numbers or migration scripts.

### Provenance as a Six-Layer DAG

Explicit provenance tags create a complete lifecycle graph:

1. **Origin** (`source` field) — who created this
2. **Merge** (`consolidated_from`) — what was it made of
3. **Transition** (`promoted_from`) — what did it used to be
4. **Compression** (`sourceArchive`) — where is the original
5. **Usage** (`.refs.yml`) — who consumed it
6. **Generation** (`generated` timestamp) — when was this derived

This survives every mutation: file moves, compression, consolidation, promotion. Inference-based provenance degrades at each step; explicit provenance is durable.

## Child Subfocuses

### Sub-1: File-Based Coordination Protocols
How agents use the filesystem as a communication bus — naming conventions, detection strategies (polling vs events vs sentinel files), write verification, and path determinism as the foundation of decoupled coordination.

**Rationale**: File-based coordination is the dominant inter-agent pattern in this codebase, and understanding its mechanics is prerequisite to understanding the other two subfocuses.

### Sub-2: Session-Scope State Propagation
How flags, configuration, and behavioral contracts implicitly flow from parent to child agents — alwaysApply rules as inheritance vehicles, config-driven pull propagation, override precedence, and the knows-vs-acts gap.

**Rationale**: While file-based coordination handles explicit data exchange, much agent behavior is governed by implicit state that must propagate reliably across spawn boundaries.

### Sub-3: Serialization Formats and Data Contracts
How inter-agent data is structured — prose-defined schemas, additive evolution, provenance tagging, the four-format stack, and the tension between LLM comprehension and traditional parsing strictness.

**Rationale**: The reliability of both file-based coordination and session-scope propagation depends on the data contracts that define what well-formed inter-agent communication looks like.

## Child Insights

### From Sub-1 (File-Based Coordination Protocols)

File-based coordination operates across three sub-layers: **naming** (deterministic path conventions enabling decoupled address computation), **detection** (polling, events, or flag files matched to latency requirements), and **verification** (post-write checks ensuring persistence and integrity). The most important insight is that detection and verification are complementary halves currently treated as separate concerns. The meditate command detects (polls for file existence) but doesn't verify (no content validation, no timeout for missing children). Combining archive-before-write (cd0c954) with verify-after-write (49303e0) creates transactional semantics equivalent to write-ahead logging. Three actionable gaps: (1) meditate's polling loop needs a timeout, (2) scattered write-safety primitives should be unified into a reusable skill, (3) path conventions hardcoded in prose should be centralized.

### From Sub-2 (Session-Scope State Propagation)

Session-scope propagation uses a push-pull architecture: **pull** (shared config files read independently by all agents for persistent state) and **push** (alwaysApply rules for behavioral contracts, spawn-time arguments for ephemeral state). The `alwaysApply` mechanism is isomorphic to Unix environment variable export — the sole reliable broadcast channel because the IDE guarantees injection. Its fragility lies in silent degradation: missing flags, stale exception lists, and misordered phase blocks break inheritance without error signals. The deepest finding is the **knows-vs-acts gap**: propagation mechanisms ensure agents load directives, but compliance depends on LLM attention dynamics and conditional parsing. The only reliable bridge is a **compliance testing pyramid** from directive trust (weakest) through self-report, output-pattern analysis, and side-effect observation to adversarial verification (strongest).

### From Sub-3 (Serialization Formats and Data Contracts)

Serialization is built on four architectural decisions: (1) **prose-defined schemas with procedural enforcement** optimized for LLM consumption rather than compiler validation; (2) **additive-only schema evolution** via a required/optional field partition that has absorbed three capability waves without versioning; (3) **explicit six-layer provenance** where no lineage question requires inference; and (4) **a consumer-optimized format stack** trading parsing strictness for LLM comprehension. The system consistently chooses repair (REM sleep) over prevention (foreign keys), reflecting a world where the most important data consumer is probabilistic.

## Summary

State coordination in this multi-agent system operates as a three-layer protocol stack — transport (file-based protocols), propagation (session-scope inheritance), and serialization (data contracts) — unified by a push-pull duality where pull achieves zero-coordination consensus for persistent state and push handles ephemeral context.

**Five key architectural principles** emerge:

1. **Explicit over implicit**: Source fields, alwaysApply rules, and frontmatter contracts are preferred over inference from paths or context
2. **Repair over prevention**: Eventual consistency with periodic cleanup (REM sleep, index rebuilds) rather than strict referential integrity
3. **Consumer-optimized formats**: LLM comprehension is the primary design driver, producing a four-format stack from JSON to CRUX
4. **Path determinism enables decoupling**: Agents independently compute file locations without coordination, making the filesystem a viable message bus
5. **Layered redundancy**: Critical constraints are stated in multiple forms to compensate for probabilistic LLM compliance

**The central challenge** is the knows-vs-acts gap: delivering state to an agent is necessary but not sufficient for behavioral compliance. This manifests as detection-without-verification in file protocols, loaded-but-ignored rules in propagation, and defined-but-violated contracts in serialization. The system's compliance testing pyramid — from directive trust through side-effect observation to adversarial verification — provides the framework for systematically closing this gap. Currently operating at levels 1-3 for most coordination concerns, advancing critical checks to levels 4-5 represents the highest-value improvement opportunity.
