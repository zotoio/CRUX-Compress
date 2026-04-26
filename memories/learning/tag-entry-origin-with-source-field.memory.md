---
id: "f8bd856"
title: "Tag entry origin with a source field when multiple commands write to one store"
description: "When multiple commands can create entries in a shared store (e.g. /crux-dream extracts from spec artifacts and /crux-remember creates ad-hoc entries), tag every entry with a `source` field — spec slug for extraction-derived entries, the fixed string \"adhoc\" for ad-hoc creations. This makes provenance explicit and lets downstream operations (REM sleep consolidation, filtering, audit, debug) differentiate without inspecting paths or content."
type: "learning"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260425-crux-remember"
tags: [memory-system, provenance, source-tags, multi-writer, design-pattern, audit-trail]
---

# Tag entry origin with a source field when multiple commands write to one store

## The pattern

A shared persistence layer can have multiple write paths. Without an explicit origin tag, downstream operations cannot tell where an entry came from once it has aged past its initial state (counters incremented, body edited, reference tracker diverged). Add a single `source` field that captures provenance in one of two forms:

- A **work-item slug** when the entry was extracted from a structured artifact (e.g. `20260425-crux-remember`)
- A **fixed string** like `"adhoc"` when the entry was created without a structured originating artifact

The string form is deliberately a constant, not a synthesised pseudo-slug, because the absence of an artifact is itself the signal.

## Concrete example: CRUX memories

The `/crux-remember` spec adds a second creation path to the memory store. Previously only `/crux-dream` wrote memories, and every memory carried its originating spec as `source`. Adding a second writer required a discrimination strategy:

- Memories from `/crux-dream` continue to use the spec slug (e.g. `source: "20260425-crux-remember"`)
- Memories from `/crux-remember` use the fixed literal `source: "adhoc"`

This was Decision 3 of the spec — chosen explicitly over alternatives like a separate `origin` enum, a path-based heuristic, or a missing-source convention.

## Why explicit beats implicit

Several alternatives were considered and rejected:

- **Inferring from path**: ad-hoc memories live in `memories/{type}/` and so do most extracted ones — paths alone are not a signal
- **Missing/empty source**: makes audit and search clumsy; legitimate ad-hoc creation now looks indistinguishable from data corruption
- **Separate enum field**: extra schema surface; the existing `source` field already carries provenance for one writer

A constant string for the no-artifact case keeps the existing schema, makes the discriminator queryable (`grep "adhoc"`), and survives memory edits.

## Downstream operations that benefit

- **REM sleep consolidation**: can apply different rules to ad-hoc vs extracted memories (e.g. require longer dormancy before consolidating ad-hoc entries that lack peer review)
- **Filtering**: `/crux-recall spec-name` lists memories by source; `/crux-recall adhoc` becomes a meaningful query for free
- **Audit**: a memory's lineage is visible in its frontmatter without needing to consult external logs
- **Debugging**: when a memory looks wrong, knowing whether it came from an artifact or a freeform user note narrows triage immediately

## Generalisation

Any persistence layer with multiple writers benefits from an explicit origin tag:

- Logs that aggregate from N services
- Queues that fan in from multiple producers
- Caches with both warm-up and lazy-fill paths
- Audit tables tracking both system and human actions

The cost is one schema field. The benefit is a perpetual, queryable record of provenance that survives downstream mutation.

## Source

Decision 3 of `spec-crux-remember-20260425.md`: "Ad-hoc memories always set `source: 'adhoc'` to distinguish them from spec-extracted memories (which carry their spec name as source)."
