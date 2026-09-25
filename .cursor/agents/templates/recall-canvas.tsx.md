# Recall Canvas Reference Template

Structural guide for the `crux-memory-recall` agent's `--total` visualization branch. Loaded on the cold path only — never included when Recall runs without `--total`.

The Canvas SDK restricts imports to `cursor/canvas` only — no external npm packages, no CDN scripts, no standard React hooks beyond `useCanvasState`, `useHostTheme`, and `useCanvasAction`. All layout computation must run at module scope.

## Data & layout invariants

1. **Gather data**: Read `.crux/memory-index.yml` for the full list of memories with their metadata (title, type, strength, tags, source, references).
2. **Load memory files**: Read all memory files from `memories/{type}/` directories. Decompress CRUX-compressed memories (`.memory.crux.md`) so the body content is available for detail panels.
3. **Embed data**: Serialize all memory data as TypeScript constants at module scope in the canvas file. No `fetch()` or dynamic imports — all data is inline.
4. **Compute layout at module scope**: Run a Verlet force simulation (Coulomb repulsion, spring attraction along edges, centre gravity, progressive damping) for ~400 iterations at module scope before the component function. Freeze final `(x, y)` positions as constants. This is required because `useEffect`/`useRef` are unavailable.
5. **Build graph structures at module scope**:
   - **Nodes**: Each memory becomes a node. Radius is proportional to strength, colour is determined by memory type (use theme tokens from `useHostTheme()`), label is the title.
   - **Edges**: Connect memories sharing tags or source spec. Stroke width is proportional to connection strength (shared tag count + shared source).
6. **Generate canvas**: Write a `.canvas.tsx` file. Read the Canvas SKILL at `~/.cursor/skills-cursor/canvas/SKILL.md` for the canvas location path, design guidance, and pre-delivery self-check. Read `~/.cursor/skills-cursor/canvas/sdk/index.d.ts` and its sibling `.d.ts` files for exact component exports and prop shapes. Use the reference template below as a structural guide.
7. **Canvas layout** — the canvas should contain:
   - **Summary stats** (`Grid` + `Stat`): total memories, type count, connection count, average strength
   - **Filter bar** (`Row` + `Pill` toggles + `TextInput`): type filters and text search, wired to `useCanvasState`
   - **Graph area** (inline `<svg>`): circles for nodes, lines for edges, rendered from pre-computed positions. Clicking a node sets `useCanvasState("selectedId", ...)` to drive the detail panel
   - **Detail panel** (`Card` + `CardHeader` + `CardBody`): shows the selected memory's full metadata and decompressed body
   - **Type distribution** (`PieChart`): memory count by type
   - **Strength distribution** (`BarChart`): strength histogram
   - **Memory table** (`Table`): all memories with type, strength, tags, source — filtered by the active type/search filters
8. **Interactions** — all driven by `useCanvasState`:
   - **Click node**: selects a memory, populates the detail panel
   - **Type filter pills**: toggle visibility of memory types in the graph and table
   - **Text search**: filters nodes and table rows by title/tag match
   - **Hover** (SVG `onMouseEnter`/`onMouseLeave`): highlights a node and its connected edges

## Reference template (structural guide — adapt data and layout as needed)

```tsx
import {
  BarChart, Card, CardBody, CardHeader, Divider, Grid, H1, H2,
  PieChart, Pill, Row, Spacer, Stack, Stat, Table, Text, TextInput,
  useCanvasState, useHostTheme,
} from 'cursor/canvas';

// --- Module-scope data and layout computation ---
// Embed all memory data as constants here.
// Run force simulation here (400 iterations, Verlet integration).
// Compute edges, positions, type counts, strength histogram here.
// Everything the component reads must be a plain constant by this point.

const MEMORIES: Array<{
  id: string; title: string; type: string; strength: number;
  tags: string[]; source: string; body: string;
}> = [ /* ... agent embeds data here ... */ ];

// Force simulation, edge computation, position freezing ...
// const POSITIONS: Record<string, { x: number; y: number }> = ...
// const EDGES: Array<{ from: string; to: string; weight: number }> = ...

export default function TotalRecall() {
  const theme = useHostTheme();
  const [selectedId, setSelectedId] = useCanvasState<string | null>('selectedId', null);
  const [search, setSearch] = useCanvasState('search', '');
  const [activeTypes, setActiveTypes] = useCanvasState<Record<string, boolean>>('activeTypes', {});

  // Filter logic using the state values and module-scope constants.
  // Render: Stats grid, filter bar, SVG graph, detail panel, charts, table.

  return (
    <Stack gap={20}>
      <H1>Memory System — Total Recall</H1>
      {/* Stats, filters, SVG graph, detail panel, charts, table */}
    </Stack>
  );
}
```
