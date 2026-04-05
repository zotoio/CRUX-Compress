---
title: "Per-phase parallel subagent execution reduces wall-clock time without coordination overhead"
description: "Phases 2, 3, and 6 each ran 3 parallel subagents simultaneously. The dependency-based phasing (no inter-agent dependencies within a phase) eliminated coordination overhead while achieving near-linear speedup on independent subtasks."
type: "learning"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [execution, parallelism, subagents, performance]
---

When subtasks have no dependencies on each other, they can run in parallel within a phase. The CRUX Memories plan demonstrated this across three phases:

- Phase 2: 3 parallel agents (CRUD, reference-tracker, compress skills)
- Phase 3: 3 parallel agents (index, extract, rebalance skills)
- Phase 6: 2 parallel agents (evals infrastructure, user checklists)

The dependency graph in the plan file explicitly shows which subtasks can run together. This phasing eliminates coordination overhead — agents don't wait on each other within a phase.

Future plans should structure subtasks to maximize parallelism by identifying independent work that can execute simultaneously.
