---
id: "0a157b3"
title: "Meditate command decomposes into recursive phases"
description: "The /crux-meditate command implements a recursive exploration pattern: initial recall → gap analysis → targeted research → synthesis → optional memory creation. Each phase feeds the next, enabling deep understanding of topics the memory corpus only partially covers."
type: "learning"
strength: 2
created: 2026-04-27
modified: 2026-05-24

source: "spec:20260425-crux-meditate"
tags: [meditate, workflow, phases, recursion, exploration, design-pattern]
---

# Meditate command decomposes into recursive phases

## The phase pipeline

`/crux-meditate` is not a single monolithic exploration step — it is a pipeline of distinct phases, each with a single clear responsibility, where the output of each phase becomes the input to the next:

1. **Initial recall** — query the memory corpus for entries relevant to the seed (chat context, quoted topic, file/folder refs)
2. **Gap analysis** — compare what was recalled against what the topic actually demands; identify the unanswered subquestions
3. **Targeted research** — explore the codebase or external sources to fill specifically those gaps (not the whole topic)
4. **Synthesis** — merge recalled memory content with research findings into a cohesive picture
5. **Optional memory creation** — let the user decide whether any synthesised insights deserve to become new memories

Each phase is a separate cognitive operation with its own success criteria. Treating them as a single "explore the topic" step loses the structural benefits.

## Why phase decomposition matters

- **Each phase has a single responsibility** — recall does not research, research does not synthesise. This keeps each step focused and makes it possible to evaluate phase quality independently.
- **Output of one phase is the explicit input to the next** — gap analysis cannot start without recall results; targeted research cannot start without gap analysis output. The data flow is explicit, not implicit.
- **Phases compose with recursion** — at each recursion depth, the same phase pipeline runs against a narrower facet. The recursive structure does not blur phase boundaries; it nests them.
- **Failure modes are localised** — a weak recall phase produces obvious gap-analysis fallout; a hallucinating synthesis phase fails its own check independently of the research that fed it. Debugging is per-phase, not whole-pipeline.

## Concrete shape in the meditate workflow

The `crux-cursor-meditation-guide` agent (via the `crux-skill-memory-meditation-research` skill) embeds this pipeline at every depth:

| Depth | Phases performed | Output to parent |
|-------|-----------------|------------------|
| 0 (orchestrator) | derive facets → spawn 3 children → consolidate → present → optional save | full consolidation, presented to user |
| 1, 2 | recall → gap analysis → targeted research → spawn deeper child → aggregate | distilled summary back up |
| 3 (leaf) | recall → gap analysis → targeted research only (no recursion) | direct insights to parent |

The recursion is the same pipeline applied repeatedly, not a different structure at each level. That uniformity is what makes the agent self-recursive.

## Generalises to other exploratory commands

Any command that needs to "deeply understand X" benefits from this decomposition:

- **Recall + gap analysis + research + synthesis** is a generic shape for memory-informed exploration
- Investigative debugging commands could use the same pipeline (recall prior bugs → gap analysis vs current symptoms → targeted log/code search → synthesise hypothesis)
- Spec-drafting commands could use it (recall related specs → gap analysis vs new requirements → targeted code review → synthesise spec outline)

The pattern is portable: when a command must combine prior knowledge with fresh investigation, decompose into phases rather than doing it all at once.

## Source

`spec-crux-meditate-20260425.md` and the `crux-cursor-meditation-guide` agent (decomposed from `crux-cursor-memory-manager` by the 20260517-meditate-agent-skill-decomposition spec). The phase pipeline is owned by the `crux-skill-memory-meditation-research` skill's recursive exploration protocol (query → expand → craft queries → recurse → aggregate), where each step corresponds to one phase of the decomposition.
