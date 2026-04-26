---
id: "e9f54ac"
title: "Runtime-generated artifacts belong in agent workflow definitions, not as static repo files"
description: "The `/crux-recall --total` canvas visualization is generated dynamically when a user invokes the command, not pre-built as a static file. The command and agent definition contain sufficient instructions for the agent to produce the visualization at runtime. This is the correct architecture for agent-generated interactive artifacts."
type: "learning"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "20260425-crux-recall"
tags: [architecture, runtime-generation, canvas, agent-workflow, artifacts]
---

# Runtime-generated artifacts belong in agent workflow definitions, not as static repo files

## The architectural choice

Some agent outputs are **static artifacts** — code, configs, docs that live in the repo and are versioned. Others are **runtime-generated artifacts** — visualizations, reports, ephemeral views that an agent produces fresh on each invocation. These two classes have very different home locations:

| Class | Lives in | Lifecycle |
|-------|----------|-----------|
| Static artifact | Repo files (`.cursor/commands/`, `src/`, `.canvas.tsx` files, etc.) | Authored once, edited over time, versioned in git |
| Runtime-generated | Agent / command definitions only | Produced anew on every invocation; never persisted between runs |

Confusing the two leads to specs that prescribe the wrong deliverable.

## Concrete example: the `--total` canvas

The crux-recall spec initially framed subtask 06 as "create the canvas visualization file at `canvases/crux-recall-total.canvas.tsx`". When the file was missing during adversarial verification, the user clarified the actual architecture: the canvas is **runtime-generated** when a user runs `/crux-recall --total`. There is no static `.canvas.tsx` file in the repo.

What lives in the repo instead is the **generation recipe**:

- `.cursor/commands/crux-recall.md` — describes the `--total` flag and points to the workflow
- `.cursor/agents/crux-cursor-memory-manager.md` — contains a 6-step workflow:
  1. Read `.crux/memory-index.yml`
  2. Load all memory files (decompress CRUX-compressed ones)
  3. Build graph nodes (size = strength, colour = type)
  4. Build graph edges (shared tags + shared source)
  5. Generate canvas via `/canvas`
  6. Inform user of available interactions

The agent reads these instructions at invocation time and produces the canvas reflecting the **current** memory state. There is no need — and no benefit — to checking in a stale snapshot.

## How to tell which class an artifact belongs to

Apply this test:

1. **Does the artifact need to reflect live data at view time?**
   - Yes → runtime-generated. The data changes; a checked-in snapshot would be stale immediately.
   - No → static is fine.

2. **Is the artifact's content fully determined by the agent's input + repo state at invocation?**
   - Yes → runtime-generated. The agent can rebuild it on demand.
   - No → static, because the input is something the agent cannot reconstruct (e.g. handwritten code, design assets).

3. **Would versioning the artifact in git pay for itself?**
   - Yes → static. Git history and PR review are valuable.
   - No → runtime-generated. The artifact is ephemeral; git history adds noise.

The crux-recall canvas fails all three for static and passes all three for runtime-generated.

## Consequences for spec design

Specs that prescribe static files for runtime-generated artifacts:

- Cause subtasks to fail adversarial verification (the file isn't on disk)
- Pollute the repo with stale snapshots
- Hide the actual deliverable (the workflow definition) behind a misleading file path
- Create maintenance burden — each memory change requires regenerating the snapshot

Specs that correctly identify runtime-generated artifacts:

- Locate the deliverable in the command/agent definition
- Define acceptance via the workflow steps and observable runtime behaviour
- Avoid the trap of "where is the file?" verification

## Generalisation

This pattern applies to any agent-generated interactive artifact:

- Memory visualizations (the case here)
- Live dashboards, reports, summaries
- Interactive explorations of repo state (call graphs, dependency trees, test coverage views)
- One-shot UI tools the agent assembles for a specific user query

The deliverable is always the **generation recipe** in the agent/command definition. The artifact itself is a runtime side-effect.

## Source

Subtask 06 of `spec-crux-recall-20260425.md` and the user's mid-execution clarification: "canvas is runtime-generated via `/canvas`, not pre-built". Subtask 06 was rescoped accordingly; the durable deliverable became the 6-step Total Visualization Workflow added to the agent definition.
