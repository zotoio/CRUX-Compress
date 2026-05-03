---
id: "4d7fe72"
title: "Cursor canvas SDK restricts imports to `cursor/canvas` only — no external npm packages"
description: "The Cursor canvas build system only allows importing from `cursor/canvas`. External npm packages (like `3d-force-graph`), CDN scripts, and React hooks beyond `useCanvasState`/`useHostTheme`/`useCanvasAction` are unavailable. This forced a full redesign from 3D WebGL to 2D SVG with a custom force simulation."
type: "redflag"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "20260425-crux-recall"
tags: [canvas, cursor-sdk, import-restrictions, external-packages, visualization]
---

# Cursor canvas SDK restricts imports to `cursor/canvas` only — no external npm packages

## The constraint

A `.canvas.tsx` file authored for the Cursor canvas runtime can only import from the `cursor/canvas` package. The build system rejects every other import path:

- **No external npm packages** — `3d-force-graph`, `d3`, `three`, `framer-motion`, etc. are all unavailable
- **No CDN scripts** — there is no escape hatch via `<script src="…">` or dynamic `import()` of remote modules
- **No general React hooks** — only `useCanvasState`, `useHostTheme`, and `useCanvasAction` are exposed; standard hooks like `useEffect`, `useRef`, `useMemo`, `useCallback` are not available
- **No filesystem or network access at render time** — all data must be embedded as constants in the canvas module itself

## Concrete impact

The crux-recall `--total` visualization originally specified `3d-force-graph` ([vasturiano/3d-force-graph](https://github.com/vasturiano/3d-force-graph)) for a 3D WebGL force-directed graph. At implementation time the SDK constraint blocked the import. Replacing it required a full redesign:

- WebGL/ThreeJS renderer → native SVG `<circle>`, `<line>`, `<text>` elements
- 3D positioning → 2D coordinates with depth conveyed by node size/colour layering
- External force simulation library → custom Verlet integration loop run once at module load
- Library-provided interactions (camera controls, click handlers) → hand-rolled SVG event handlers

The redesign delivered equivalent analytical value (click-detail, hover-highlight, type filtering, tag search, zoom/pan), but the architectural shift cost the spec a full subtask redo.

## Plan around this from the start

For any future canvas work:

1. **Assume zero external dependencies.** Treat every visualization as buildable from raw SVG/CSS plus the three exposed hooks.
2. **Pre-compute everything.** Without `useEffect`/`useRef`, derived data (layouts, force simulations, deterministic randomness) must run at module scope before the component function executes.
3. **Embed all data as module constants.** No fetches, no async loading, no external state stores.
4. **Reach for SVG before WebGL.** SVG is the natural fit for the SDK's hook surface; WebGL/canvas2D requires lifecycle hooks the SDK does not expose.
5. **Validate the import surface before writing the spec.** A spec that names an external library has already failed if the canvas runtime is the target.

## Source

Subtask 06 of `spec-crux-recall-20260425.md`: the planned `3d-force-graph` integration was abandoned mid-implementation when the import was rejected. Recovery required redesigning the visualization to use only `cursor/canvas` primitives and hand-rolled SVG with a module-scope force simulation.
