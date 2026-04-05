---
id: "efc4c24"
title: "Per-phase parallel subagent execution reduces wall-clock time without coordination overhead"
description: "Phases 2, 3, and 6 each ran 3 parallel subagents simultaneously. The dependency-based phasing (no inter-agent dependencies within a phase) eliminated coordination overhead while achieving near-linear speedup on independent subtasks."
type: "learning"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [execution, parallelism, subagents, performance]
compressed: true
compressionTarget: 33
beforeTokens: 130
afterTokens: 42
reducedBy: 68%
compressedDate: 2026-04-05
sourceArchive: .ai-ignored/memories/sources/20260405/parallel-subagent-execution-per-phase.memory.md
---

⟦CRUX:memory
R{¬deps within phase→parallel; near-linear speedup}
E.CRUX-Memories{
 phase2: 3∥(CRUD,ref-tracker,compress)
 phase3: 3∥(index,extract,rebalance)
 phase6: 2∥(evals,checklists)
}
Ω{dep graph in plan→explicit parallel work; ¬wait within phase; future plans→maximize ∥}
⟧
