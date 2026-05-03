---
id: "a613386"
title: "Canvas components must pre-compute layout at module scope when SDK lacks hooks"
description: "The canvas SDK doesn't expose `useEffect` or `useRef`, so force simulation (400-iteration Verlet integration) must run once at module scope during import. Module-level edge computation keeps the component function pure. This pattern applies to any canvas that needs computed data."
type: "learning"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "20260425-crux-recall"
tags: [canvas, force-simulation, module-scope, pre-computation, hooks, cursor-sdk]
---

# Canvas components must pre-compute layout at module scope when SDK lacks hooks

## The problem

The Cursor canvas SDK exposes only three hooks: `useCanvasState`, `useHostTheme`, `useCanvasAction`. Standard React hooks for derived data — `useEffect`, `useRef`, `useMemo`, `useCallback` — are unavailable. Any expensive or stateful computation that React would normally place in `useEffect` has nowhere to live inside the component.

## The pattern

Run the computation at **module scope**, outside the component function, during module evaluation. The result becomes a plain constant (or set of constants) that the component reads on every render.

```typescript
const NODES = embeddedMemoryData.map(toNode);
const EDGES = computeEdges(NODES);
const POSITIONS = runForceSimulation(NODES, EDGES, { iterations: 400 });

export function MemoryGraph() {
  return (
    <svg>
      {EDGES.map(e => <line ... />)}
      {NODES.map(n => <circle cx={POSITIONS[n.id].x} ... />)}
    </svg>
  );
}
```

The component function becomes pure — it reads pre-computed data and renders. No lifecycle, no effects, no refs.

## Concrete example: memory graph layout

The crux-recall `--total` canvas needed force-directed layout for ~30 nodes. At module scope:

1. **Embed source data** — memory frontmatter and tags compiled into a `MEMORIES` constant
2. **Compute edges** — pairs of memories sharing tags or source spec, weighted by overlap count
3. **Run force simulation** — 400 iterations of Verlet integration with:
   - Coulomb repulsion between every pair of nodes
   - Spring attraction along each edge
   - Centre gravity to prevent drift
   - Progressive damping (energy decay) so positions converge
4. **Freeze positions** — final `(x, y)` per node stored in a positions constant

Render time then collapses to "draw circles and lines from constants" — fast, deterministic, no flicker.

## When to use this pattern

Any canvas with:

- Derived layouts (graphs, treemaps, timelines, heatmaps)
- Iterative computation (simulations, layout solvers, sorts that need the whole dataset)
- Deterministic randomness that must be stable across re-renders (seeded RNG run once)
- Heavy preprocessing of embedded data

Anything that React would naturally place in `useMemo` or a one-time `useEffect` should move to module scope.

## Trade-offs

**Pros:**
- Pure components, trivial to reason about
- Computation runs once per module load, not per render
- No hook ergonomics issues
- Output is deterministic and reproducible

**Cons:**
- Computation cannot depend on runtime canvas state (`useCanvasState` values are not available at module scope)
- Module load can become slow if the simulation is heavy
- Cannot react to changes in input data without re-loading the canvas

Because canvases are typically generated fresh per invocation by an agent, the "load once, render many times" model fits the actual lifecycle well.

## Source

Subtasks 06 and 07 of `spec-crux-recall-20260425.md`. The 400-iteration Verlet simulation was necessary because the canvas SDK had no `useEffect` to host the layout pass; running it at module scope produced stable, performant rendering.
