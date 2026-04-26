---
id: "ca54bd4"
title: "Gap analysis drives targeted research in meditate"
description: "The meditate workflow's gap analysis phase compares recalled memories against the user's topic to identify knowledge gaps. These gaps become focused research prompts, preventing unfocused codebase exploration and ensuring the agent researches only what the memory corpus lacks."
type: "learning"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "spec:20260425-crux-meditate"
tags: [meditate, gap-analysis, research, focus, design-pattern, exploration]
---

# Gap analysis drives targeted research in meditate

## The problem with unfocused exploration

When an agent is asked to "explore" a topic, the default failure mode is to wander the codebase reading whatever looks vaguely relevant. The result: high token cost, lots of context, and a synthesis that mostly restates what the agent already knew. The memory corpus's existing knowledge is never explicitly leveraged, and the research never narrows.

## Gap analysis as the focusing mechanism

Meditate inserts a deliberate gap-analysis phase between memory recall and research. The phase compares:

- **What the recall returned** — concrete memories (titles, descriptions, body content) that already address parts of the topic
- **What the topic actually demands** — the subquestions or aspects the user's seed implies

The output is a list of **specific gaps**: aspects of the topic that the memory corpus does not yet cover, expressed as focused research prompts.

Those gap-derived prompts then drive the targeted research phase. The agent does not search the whole codebase; it searches for exactly the missing pieces.

## What gap analysis prevents

- **Re-discovery of known facts** — research effort is not spent confirming things memories already say
- **Topic creep** — research is bounded by the gap list; tangentially interesting findings are out of scope unless a gap covers them
- **Empty synthesis** — a synthesis that combines "what we knew" with "what we found" only adds value when those two sets are actually different; gap analysis guarantees they are
- **Token waste** — without gap analysis, the agent often spends most of its budget reading code that confirms existing memories

## Concrete shape

For a meditate seed like *"how do we handle session-scoped flags?"*:

| Phase | Output |
|-------|--------|
| Recall | 2 memories: `session-scope-subagent-patterns`, `crux-phase-block-ordering-reflects-precedence` |
| Gap analysis | Recalled memories cover subagent inheritance and rule ordering, but lack: (a) how persistence interacts with flags, (b) how flags compose when multiple are active, (c) what testing strategy covers flag combinations |
| Targeted research | 3 focused prompts, one per gap, executed against the codebase |
| Synthesis | Combines the two recalled memories with three research findings into a cohesive picture |

Without the gap analysis step, the targeted-research phase would have no anchor and would default to reading whatever looked relevant.

## Why gap analysis must be its own phase

It is tempting to fold gap analysis into either recall ("recall and figure out what's missing") or research ("research with the recalls in mind"). Both are weaker:

- **Folded into recall**: recall is broad-and-shallow; gap analysis is narrow-and-deliberative. Mixing them produces neither.
- **Folded into research**: the agent ends up doing implicit gap analysis as it searches, which biases towards confirming recalled facts rather than finding what is missing.

Keeping gap analysis as a discrete step with its own output (an explicit gap list) prevents both failure modes.

## Generalises to other recall-then-research workflows

Any workflow that combines stored knowledge with fresh investigation benefits from an explicit gap-analysis step:

- Code review: prior review notes → gaps vs current diff → targeted re-review of new concerns
- Spec planning: prior specs → gaps vs new feature → targeted research on novel aspects
- Bug investigation: prior incident memories → gaps vs current symptoms → targeted log queries

The pattern: do not let prior knowledge silently shape research. Surface the gaps explicitly, then research only those.

## Source

`spec-crux-meditate-20260425.md` and the recursive exploration protocol in `crux-cursor-memory-manager` Meditate Mode (steps "Query memories" → "Expand" → "Craft queries"). The "craft queries" step is where gap analysis becomes explicit refined queries that drive deeper recursion.
