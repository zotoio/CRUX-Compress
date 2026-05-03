# Spec: CRUX-Compress Next Features — Meditation-Derived Roadmap

## Status
Draft

## Overview

This spec captures the consolidated output of a 3-level recursive `/crux-meditate` session exploring "the most useful features we could add next" to CRUX-Compress. Three parallel exploration branches — **technical capability gaps**, **UX friction**, and **ecosystem integration** — independently converged on a single architectural insight: **drift is the universal failure mode**, and the fix is a sequenced pivot that makes the MCP server the operational backbone, with Cursor commands as one of many adapters.

The proposed delivery is sequenced, not parallel — each phase unblocks the next.

## Key Insights

### The Three-Branch Convergence

All three branches independently diagnosed the same root problem from different angles:

1. **Branch 1 (Capability gaps)**: `CRUX.md` is parseable data, not just docs. Parsing it into canonical `{SYMBOL_MAP, BLOCK_LABELS}` lets the decompressor, search tokenizer, lint runner, and a `/crux-explain` command all consume one source — eliminating drift at the notation layer.

2. **Branch 2 (UX friction)**: The entire UX problem collapses to one pattern — drift between authoritative surfaces. `/crux-help` and `/crux-doctor` derived from `.crux/crux-memories.json` cannot structurally drift from reality.

3. **Branch 3 (Ecosystem)**: Federation, IDE-agnosticism, and CI/CD are one move — relocate the operational brain from Cursor agents into `crux_mcp_server`'s tool registry, then wrap with thin per-surface adapters.

### Memory Corpus Signals

- **`b0c02ea` (advisory + progressive-enhancement)** is the universal UX template cited by all three branches. Every proposed feature follows this pattern.
- **`6c16dc6` (adversarial verification, ~25% hit rate)** is the empirical motivator — mechanise via lints, embed via doctor, deploy via CI Actions.
- **`c71c143` + `cd0c954`** form a permission envelope permitting dry-run, staging, TTL'd soft-delete, and rollback without violating safety.
- **Four drift-related memories** (`bdcc9ad`, `96a7410`, `d944d7c`, `dbfd3ed`) encode the same pattern from four angles but have never been consolidated — a live REM-sleep opportunity.
- **Live adversarial-verification catch during this session**: a depth-3 grandchild fabricated five non-existent memory IDs; the depth-2 verifier caught and dropped them — proving `6c16dc6` in-process.

### Strength as Unifying Signal

The existing `strength` field already gates rule-promotion (30) and type-promotion (10). The same signal can: auto-tune lint strictness (advisory → strict), surface promotion forewarning to users, and set publish-quality thresholds for memory packs. One signal, three policy dials, none yet wired.

## Proposed Phases

### Phase 1 — Architectural Keystone: `CRUX.md` Spec Parser

**Rationale**: Every subsequent feature becomes downstream-cheap once the spec is parseable data.

| Deliverable | Description |
|---|---|
| `crux-spec-symbols` parser | Parse `CRUX.md` symbol and block tables into canonical `{SYMBOL_MAP, BLOCK_LABELS}` JSON |
| MCP tool: `crux-spec-symbols` | Expose parsed symbols via MCP for programmatic consumption |
| Fix `crux_decompress.py` | ~7 of 10 block labels mislabelled, ~17 spec symbols omitted — rebuild from parsed spec |
| CRUX-aware tokenizer | Update `search_engine.py` `_WORD_RE` to handle Unicode CRUX symbols — restore compressed-vs-uncompressed recall parity |
| `/crux-explain` command | Symbol introspection without loading the full spec; consumes the parser output |

### Phase 2 — MCP Write Tools + CLI

**Rationale**: The architectural pivot — Cursor commands become adapters; CI/federation/non-Cursor IDEs become incremental.

| Deliverable | Description |
|---|---|
| MCP write tools | `memory-write`, `memory-update`, `memory-forget`, `memory-trigger-dream`, `memory-trigger-rem` with two-step `*-extract`/`*-finalize` confirmation pattern |
| `crux` CLI | Thin CLI piping each tool to `crux-mcp-server` in stdio mode — enables headless, CI, and non-Cursor use |
| `memory-context-recall` | Context-aware recall with programmable query DSL (date/strength/source/regex filters) |
| `memory-validate` | Validation tool exposing invariant checks programmatically |

### Phase 3 — Advisory Layer: `/crux-doctor` + Invariant Runner

**Rationale**: Mechanises adversarial verification at machine cadence. Build once, expose as MCP tool (programmatic), Cursor command (interactive), and CI Action (automated).

| Deliverable | Description |
|---|---|
| `crux-invariant-runner` | Core engine consuming `lint:` frontmatter on redflag memories as positive invariant kinds, plus built-in negative kinds (bidirectional-reference, spec-drift, path-existence) |
| `/crux-doctor` command | Interactive advisory surface wrapping the invariant runner |
| `lint:` frontmatter contract | Schema for redflag memories to declare themselves as executable lint rules |
| `/crux-help` command | Auto-generated from `.crux/crux-memories.json` — structurally cannot drift |

### Phase 4 — UX Polish

**Rationale**: Snaps into the advisory layer from Phase 3.

| Deliverable | Description |
|---|---|
| Uniform `--dry-run` | On every state-changing command — primary learning vector for new users |
| `/crux-config get/set/list` | Replaces hand-editing JSON; eliminates stringly-typed flags |
| Session-start hook improvements | Memory-health surfacing, smarter nap signal (per-spec ack, snooze), amnesia indicator |
| `/crux-forget --staged` | TTL'd trash with rollback — restores symmetry with compression's archive pattern |
| First-run tour | Demo memory + `/crux-tour` via session-start hook — time-to-first-memory on-ramp |

### Phase 5 — CI Bundle

**Rationale**: Mechanises the 25% adversarial-verification hit rate at PR cadence using infrastructure already built.

| Deliverable | Description |
|---|---|
| `crux-drift-check` Action | Runs `/crux-doctor` invariants on every PR; advisory comments, optional fail-closed |
| `crux-pr-surface` Action | Posts relevant past learnings from `.crux/reference-tracking/*.refs.yml` as PR comments |
| `crux-citation-check` Action | Validates memory ID citations against `memory-index.yml` — would have caught this session's grandchild hallucination |
| `crux-dream-on-merge` Action | Triggers dream extraction on merge; continuous accumulation |
| `crux-rem-weekly` Action | Scheduled REM sleep; auto-rot prevention |

### Phase 6 — Eval Harness Expansion

**Rationale**: The compression-source archive (`cd0c954`) is a free eval corpus; `Ω.code`/`Ω.image` gates are speced but unmeasured.

| Deliverable | Description |
|---|---|
| Round-trip eval harness | Code and image compression ground-truth testing using the existing archive corpus |
| Compression-budget badge | CI-visible compression ratio tracking |

### Phase 7 — Ecosystem: Federation + Multi-IDE

**Rationale**: Every prior phase makes this incremental rather than architectural.

| Deliverable | Description |
|---|---|
| Memory-pack format | Publishable, installable memory bundles (analogous to ESLint configs) |
| `crux install`/`crux publish` | CLI commands populating `scopes.shared` — the designed-but-unused seam |
| Anonymisation pipeline | Snapshot → anonymise → validate → compress → sign → publish (pre-compression to avoid corrupting CRUX symbols) |
| `platforms` registry | `.crux/crux.json` extension + `install.py --platform <name>` adapters for IDE-agnostic distribution |
| Observability surface | Audit log + recall telemetry + `memory-stats` v2 with compression-ratio trends |

## Open Questions

1. **Phase sizing**: Each phase above could be its own spec. What granularity does the team prefer?
2. **MCP server maturity**: The current `crux_mcp_server/` is under active development — how stable is it as a pivot point?
3. **Consolidation first?**: Should we run `/crux-dream --rem` on the existing corpus before starting implementation, to consolidate the drift quartet and validate the system on itself?
4. **Strength wiring priority**: When should strength-as-policy (auto-tuning advisory→strict, publish thresholds) be threaded in — as a Phase 3 extension or its own phase?
5. **Breaking changes**: The MCP-as-backbone pivot (Phase 2) may shift the Cursor command interface. What's the deprecation/parity story?

## Potential Approaches

### Approach A: Full Sequential (recommended)
Execute phases 1→7 in order. Each unblocks the next. Slower overall but minimises rework.

### Approach B: Parallel Tracks
Run Phase 1 + Phase 4 (UX) in parallel since UX polish doesn't depend on the spec parser. Merge at Phase 3.

### Approach C: MCP-First
Start with Phase 2 (MCP write tools + CLI) to maximise ecosystem reach early. Back-fill the spec parser (Phase 1) once the MCP surface is stable. Riskier — the decompressor and tokenizer remain broken longer.

## Source

Generated from `/crux-meditate "on the most useful features we could add next"` on 2026-04-27. Three-branch, 3-level recursive exploration with ~13 subagents querying the full memory corpus.
