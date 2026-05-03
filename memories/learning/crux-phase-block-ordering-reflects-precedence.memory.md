---
id: "d5e503c"
title: "CRUX rule phase-block ordering reflects evaluation precedence"
description: "When a CRUX-compressed rule contains multiple phase blocks (Φ.*) representing modes or overrides, order them highest-precedence first so the LLM evaluates overrides before defaults. The amnesia rule in .cursor/rules/crux-memories-integration.crux.mdc demonstrates this: Φ.amnesia (override) → Φ.enabled (default) → Φ.disabled (off). The same ordering applies in the source markdown rule. Reversing the order risks the LLM applying the default behavior before checking the override."
type: "learning"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260425-crux-amnesia"
tags: [crux, rules, ordering, precedence, phase-blocks, authoring-convention, alwaysapply-rules]
---

# CRUX rule phase-block ordering reflects evaluation precedence

## The convention

When a `.cursor/rules/*.md` (and its compressed `.crux.mdc` counterpart) defines multiple modes or overrides as separate `Φ.*` phase blocks, order them highest-precedence first.

## Concrete example

`.cursor/rules/crux-memories-integration.crux.mdc` defines three phase blocks for memory behavior:

```
Φ.amnesia{ ... session override ≻ enableMemories ... }
Φ.enabled{ ... discover, load, annotate ... }
Φ.disabled{ ... skip all silently ... }
```

The order reflects evaluation precedence:

1. **`Φ.amnesia`** — session override, takes precedence over both
2. **`Φ.enabled`** — default when `enableMemories="true"` and amnesia is off
3. **`Φ.disabled`** — fallback when `enableMemories="false"`

Subtask 02 of the amnesia spec documents this is intentional: "ordering reflects override precedence: amnesia > enabled > disabled."

## Why ordering matters in LLM consumption

LLMs read rules sequentially. Although a competent LLM should evaluate all blocks before acting, top-down reading order influences which rule is most salient. Placing the override first ensures:

- The override semantics are loaded into working context first
- Ambiguous cases default to the override interpretation rather than the default behavior
- Reviewers reading the rule immediately see the precedence hierarchy

## Source markdown follows the same order

Subtask 02 also notes the natural-language source rule places the amnesia override section before the "When Memories Are Enabled" section. The compressed `.crux.mdc` mirrors the source order — generation does not reshuffle. So the ordering convention applies symmetrically: source author orders by precedence, compressed output preserves that order.

## Anti-pattern: defaults before overrides

Listing blocks in alphabetical or alphabetic-suffix order (e.g. `Φ.amnesia` last because "a < e < d" was applied incorrectly, or `Φ.disabled` first because it represents "the simplest case") leaves the precedence implicit and easy to miss. The reader has to re-derive precedence from the block contents rather than reading it from the order.

## Authoring checklist for multi-mode CRUX rules

When introducing a new mode/override into a rule with existing phase blocks:

1. Identify the precedence hierarchy: which mode wins when multiple apply?
2. Place the new block in the source markdown at its precedence position (not appended to the end)
3. Regenerate the compressed `.crux.mdc` to mirror the source order
4. Reviewer check: read the first phase block — it should be the highest-precedence override

This convention generalizes beyond memory rules to any always-applied rule with multiple modes (e.g. session vs persistent, override vs default, strict vs lenient).
