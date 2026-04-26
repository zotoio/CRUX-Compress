---
id: "74f65d5"
title: "Relax restrictive rules surgically with phrase additions, not rewrites"
description: "When a new feature must bypass an existing restrictive rule, prefer surgical phrase addition over rewriting the rule. The crux-remember spec changed agent scoping rule 1 from \"Only during dream extraction\" to \"Only during dream extraction or explicit remember\" — a single-clause expansion. The rule's restrictive intent is preserved for all unaffected callers; only the new authorised path is added."
type: "learning"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260425-crux-remember"
tags: [rule-design, constraint-relaxation, surgical-edits, rule-evolution, diff-discipline, design-pattern]
---

# Relax restrictive rules surgically with phrase additions, not rewrites

## The pattern

When a new feature must bypass an existing restrictive rule, two approaches present themselves:

1. **Rewrite the rule** to express its new general shape ("Memory creation is permitted under any of these contexts: …")
2. **Append a phrase** to the existing rule that names exactly the new authorised path ("Only during dream extraction or explicit remember")

Prefer (2). The phrase addition preserves the original intent for every unaffected caller, produces a small reviewable diff, and leaves the rule's character intact. Rewrites tend to lose the restrictive tone — the very tone that prompted the rule's creation in the first place.

## Concrete example: agent scoping rule expansion

Before the `/crux-remember` spec, the memory manager's agent scoping rule 1 read:

> 1. **Only during dream extraction** — agent memories are created when processing a completed work item via `/crux-dream`.

`/crux-remember` introduced a second authorised creation path. The spec applied surgical relaxation:

> 1. **Only during dream extraction or explicit remember** — agent memories are created when processing a completed work item via `/crux-dream`, or when the user explicitly invokes `/crux-remember`. Ad-hoc memories from `/crux-remember` are always placed in base scope (`memories/{type}/`) unless the user explicitly requests agent scoping.

Three observations:

- The "Only" gate survives — the rule is still restrictive
- The new authorised path is named explicitly — not a vague "or with explicit user intent"
- A clarifying sentence captures the default behaviour for the new path, so the change is self-contained

Compare to a rewrite that might have produced: "Agent memories are created when the user has identified an agent owner via any supported workflow." — this loses the restrictive tone, omits the named entry points, and reads as if all paths are equivalent.

## Why surgical wins

- **Diff size**: a phrase addition is reviewable in seconds; a rewrite requires reading the whole rule plus its surrounding context to verify nothing was lost
- **Bisectability**: future debugging can pinpoint when the rule changed by searching for the new clause; rewrites blur the history
- **Intent preservation**: the original rule's tone (Only, Always, Never) survives; rewrites tend to soften because they aim for general applicability
- **Reversibility**: the phrase can be removed if the new feature is rolled back; a rewrite needs the original text reconstructed
- **Sibling rule consistency**: if other rules in the file follow the "Only X" pattern, the phrase addition keeps the family consistent; a rewrite makes one rule stylistically different from its peers

## When to choose rewrite

Rewriting is warranted when:

- The rule has accumulated three or more named exceptions and reads as a list of caveats
- The original rule's wording is now factually wrong (not just incomplete)
- The new feature changes the rule's intent, not just its scope

For the first one or two new authorised paths, prefer phrase addition.

## Heuristic

If the relaxation can fit in a sentence that names the new path, do that. If it requires three sentences, consider a rewrite. If it requires a paragraph, the underlying intent has likely shifted and a rewrite is the honest answer.

## Generalises to

- API documentation — "this endpoint is read-only" → "this endpoint is read-only except via the admin-write header"
- Validation rules — "values must be alphanumeric" → "values must be alphanumeric or one of the reserved tokens listed in §X"
- Lint configurations — narrow exception entries beat broad disabling
- Type annotations — narrow union additions beat replacing with `unknown`

The pattern is: name the new authorised case explicitly, don't dilute the restriction.

## Source

Subtask 02 of `spec-crux-remember-20260425.md` Implementation Notes: "The scoping rule relaxation is critical: previously only dream extraction could create memories, but `/crux-remember` needs to write to base scope directly". The change diff in `.cursor/agents/crux-cursor-memory-manager.md` is a single phrase addition.
