# Subtask: Report Content Requirements (Charts, Infographics, Calculators, Citations, Peer-Review section)

## Metadata
- **Subtask ID**: 06
- **Feature**: Meditate Research-Mode Overhaul
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 05
- **Created**: 20260516

## Objective

Add the substantive content requirements that the HTML report must satisfy. The structural shell, theming, light/dark mode, responsive nav, and PDF render path are already in place from subtask 05. This subtask defines:

- **Visualizations**: at least 4 distinct chart types in total, picked from Chart.js + D3.js. Per-facet selection guidance for D3 (hierarchy → tree/sunburst/treemap, networks → force-directed/chord, flows → sankey, geo → choropleth, multi-dim → parallel coordinates, etc.).
- **Infographics**: at least 3 distinct hand-rolled HTML/CSS/SVG infographic types from a curated list (hierarchy/tree, comparison matrix, decision tree, scorecard, quadrant, heatmap, risk meter, timeline, concept map, Venn).
- **Interactive elements**: at least one interactive calculator if the meditation surfaces a quantifiable trade-off; filterable tables; tooltips on inline citation markers.
- **Citations section**: complete, deduplicated, with backlinks to citing sections; a "Citation gaps" callout in the executive summary if any uncited findings made it through (Quick mode warn-only path).
- **Peer-review section** (Research mode): one card per peer-review file showing Reinforcements, Contradictions, Gaps.
- **Footer** with `theme:` annotation, mode label, depth/branch counts, total citation count.

The graceful-degradation contracts for D3 and calculators come in subtask 07.

## Files Modified

- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`

## Deliverables Checklist

- [x] **Visualizations subsection** in the command file with: minimum count rule (≥4 distinct chart types in total across Chart.js + D3.js), Chart.js types list (bar/stacked, radar, doughnut/pie, line/area, scatter/bubble, polar area, mixed bar+line), D3 types-per-facet table (hierarchy / networks / flows / time-series / geographic / multi-dim / calendar / custom)
- [x] **D3 hard rule** stated: every D3 chart must gracefully degrade to a meaningful static equivalent in PDF; subtask 07 documents the per-pattern rules
- [x] **Infographics subsection** in the command file with: minimum count rule (≥3 distinct types), curated list (hierarchy/tree, comparison matrix, decision tree/flow, scorecards, process/pipeline, quadrant 2×2, heatmaps, risk meters/gauges, timeline ribbons, concept maps, Venn)
- [x] **Interactive elements subsection** in the command file with: ≥1 calculator (with the print-degradation hook deferred to subtask 07), filterable tables (filter/sort affordance, hidden in print, data preserved), citation-marker tooltips (degrade to inline footnote markers in print)
- [x] **Citations section** spec in the report structural elements list updated: mandatory in both modes, sourced from `citations-index.yml` in Research / inline markers in Quick, deduplicated, backlinks; "Citation gaps" callout in the executive summary if any uncited findings (Quick mode warn-only)
- [x] **Peer-review section** spec in the report structural elements list: one card per peer-review file, listing Reinforcements / Contradictions / Gaps
- [x] **Footer** spec extended with the `theme:` annotation
- [x] Sparseness fallback rule: if the meditation lacks data for the minimums, substitute additional comparison matrices, scorecards, or hierarchy diagrams so the report is never sparse
- [x] Subagent **step 12** summary in the agent file mentions the chart counts, infographic counts, calculator requirement, citations section
- [x] One new design principle in the agent file: visualizations + interactive elements with mandatory PDF degradation (will be expanded by subtask 07)

## Definition of Done

- [x] HTML report contains ≥4 distinct chart visualizations and ≥3 distinct infographics
- [x] HTML report contains ≥1 interactive calculator if the meditation surfaces a quantifiable trade-off
- [x] Tables are filterable (filter/sort UI hidden in print)
- [x] Citations section is complete and deduplicated with backlinks
- [x] Peer-review section present in Research mode (one card per peer-review file)
- [x] Footer includes `theme:` annotation, mode label, depth/branch counts, total citation count
- [x] Linter passes on both files

## Implementation Notes

### Visualizations subsection (command file, place under HTML report requirements)

```markdown
##### Visualizations (Chart.js + D3.js, loaded from CDN)

Pick **at least 4 distinct chart types in total**, choosing those that fit the data the meditation actually surfaced AND the kind of facet being illustrated. The minimum can be met by any combination of **Chart.js** (standard chart types, fastest to author) and **D3.js** (advanced or facet-specific interactive visualizations). Do not fabricate data — if the meditation lacks the data a particular chart type needs, skip it and pick another.

**Hard rule**: Every D3 chart **must** gracefully degrade to a meaningful static equivalent in the PDF render. See subtask 07's **D3 print degradation** rules — a D3 chart that cannot degrade is forbidden; pick a different visualization or implement the degradation paired view.

###### Chart.js types (standard, well-suited to numeric data the meditation surfaced)

- **Bar / stacked bar** — counts, comparisons across branches or options
- **Radar** — multi-dimensional scoring (criteria × option matrices)
- **Doughnut / pie** — categorical breakdowns (citation source mix, finding-type distribution)
- **Line / area** — temporal trends, projections, sensitivity sweeps
- **Scatter / bubble** — multi-axis trade-off plots (cost vs benefit, risk vs reward)
- **Polar area** — relative magnitude across categories
- **Mixed (bar + line)** — actual vs projected, baseline vs scenario

###### D3.js types (interactive, facet-specific — pick the one that fits each section)

| Facet kind | Suitable D3 chart types |
|------------|-------------------------|
| **Hierarchy / structural decomposition** (e.g. branch → depth-2 → depth-3 tree) | Tree (`d3-hierarchy` cluster/tree), dendrogram, sunburst, treemap, partition, icicle |
| **Networks / relationships** (e.g. cross-branch citation overlap, memory-to-finding linkage) | Force-directed graph, chord diagram, hierarchical edge bundling, arc diagram |
| **Flows / process volumes** (e.g. how findings cascade from depth-1 → depth-3) | Sankey, alluvial/parallel sets |
| **Time-series with interaction** (e.g. timeline with brushable zoom) | Brushable timeline, zoomable area chart, focus+context |
| **Geographic** (e.g. data tied to locations) | Choropleth, hex bin, projection-aware map |
| **Multi-dimensional comparison** (e.g. options × many criteria) | Parallel coordinates, brushed scatter matrix, radar with brush |
| **Calendar / temporal density** (e.g. activity over months) | Calendar heatmap |
| **Custom facet-specific** | Hand-coded D3 (e.g. a custom force-layout for a specific concept map) — always include the print degradation pair |

When using D3, load it from the official CDN: `<script src="https://d3js.org/d3.v7.min.js"></script>` (v7 is current at time of writing; pin to the latest stable major version available on the CDN). All data is still embedded inline as JavaScript constants — no runtime fetches.
```

(The D3 print-degradation subsection is added by subtask 07.)

### Infographics subsection (command file)

```markdown
##### Infographics (HTML/CSS/SVG, no external library)

Pick **at least 3 distinct infographic types** from the list below — these convey structure visually rather than encoding numbers. Build them with hand-rolled HTML + CSS + inline SVG (no extra libraries):

- **Hierarchy / tree diagrams** — render the branch → depth-2 → depth-3 subfocus tree as a visual map (CSS grid or inline SVG with connector lines)
- **Comparison matrices** — option × criterion grids with cell-level color coding, badges, or icons
- **Decision trees / flow diagrams** — when the meditation surfaces a decision pathway, render it as a node-and-arrow SVG diagram
- **Scorecards** — per-option panels with weighted criterion bars and an overall score
- **Process / pipeline diagrams** — sequential stages with directional arrows
- **Quadrant / 2×2 matrices** — placement of options on two axes (e.g. effort × impact)
- **Heatmaps** — CSS grid where cell color encodes value
- **Risk meters / gauges** — segmented horizontal bars or radial dials with color-coded zones
- **Timeline ribbons** — horizontal chronological strips with milestone markers
- **Concept maps** — central-topic-with-spokes layouts using inline SVG
- **Venn diagrams** — overlap visualizations for branches that share findings (CSS or SVG)
```

### Interactive elements subsection (command file)

```markdown
##### Interactive elements

- **Interactive calculators** — at least one JavaScript-driven calculator if the meditation surfaces any quantifiable trade-off (input fields, recompute on change, formatted result panel). Infer what calculation would be useful from the meditation content. **Mandatory PDF graceful degradation**: see subtask 07 for the `.calculator-static-fallback` what-if-scenarios contract.

- **Filterable tables** — comprehensive data tables with at least one filter or sort affordance for any tabular finding. In print mode, hide the filter / sort UI controls and render the **unfiltered, default-sorted** table; the data itself is preserved verbatim.

- **Tooltips** on inline citation markers showing the cited source on hover. In print mode, tooltips degrade to inline footnote markers (`[7]`) that resolve in the Citations section.
```

### Citations section spec (command file — update the structural-elements bullet from subtask 05)

Replace the simple "Citations section at the bottom" bullet from subtask 05 with this expanded version:

```markdown
- **Citations section** at the bottom — mandatory in both modes. In Research mode, source it from `citations-index.yml` (the canonical aggregated index); in Quick mode, source it from inline citation markers extracted from every branch file. Either way, deduplicate and provide backlinks to every section that cited each source. If any finding in the report has no resolvable citation (possible only in Quick mode under the warn-only validation rule), include a "Citation gaps" callout in the executive summary that lists every uncited finding so the gap is visible to the user.
```

### Peer-review section spec (command file — update the structural-elements bullet from subtask 05)

Already included in subtask 05's structural elements list. Confirm it reads:

```markdown
- **Peer-review section** (Research mode) — cross-branch reinforcements, contradictions, gaps; one card per peer-review file
```

### Footer spec (command file — update the structural-elements bullet from subtask 05)

Already included in subtask 05's structural elements list. Confirm it reads:

```markdown
- **Footer** with meditation slug, timestamp, mode (`research` / `quick`), depth/branch counts, total citation count, and the resolved theming label (e.g. `theme: editorial / warm_palette / serif_headings_sans_body` or `theme: matched-repo (signals: …)`)
```

### Sparseness fallback rule (command file — already included in subtask 05's "Other styling rules")

Confirm it reads:

```markdown
If the meditation is small (e.g. a quick `--quick` run on a narrow topic) and genuinely lacks the breadth for 4 chart types or 3 infographics, you must still produce **all** mandatory structural elements; substitute additional comparison matrices, scorecards, or hierarchy diagrams to compensate so the report is never sparse.
```

### Subagent step 12 summary (agent file — update from subtask 05)

In the step 12 obligations summary, ensure the bullet that mentions chart counts reads:

```
- Write a self-contained `report-{topic-slug}-{ts}.html` with: a responsive nav, in-page TOC, hero/exec summary, per-branch sections, peer-review section, cross-references, citations section, footer with `theme:` annotation, **at least 4 distinct chart visualizations** (Chart.js + D3.js — pick the chart type per facet, e.g. tree/sunburst for hierarchy, sankey for flow, force-directed graph for relationships, choropleth for geo, parallel coordinates for multi-dimensional comparison), **at least 3 distinct hand-rolled HTML/CSS/SVG infographics**, at least one **interactive calculator**, filterable tables, light AND dark mode with default dark and persistent toggle, high-contrast print styles for PDF rendering, all data inline.
```

### One new design principle (agent file)

```markdown
- **Visualizations + interactive elements: mandatory PDF graceful degradation (both modes)**: Reports may use Chart.js for standard chart types, D3.js (loaded from `https://d3js.org/`) for advanced or facet-specific interactive visualizations (tree/sunburst/treemap for hierarchy, sankey for flow, force-directed graph or chord diagram for networks, choropleth for geo, parallel coordinates for multi-dimensional comparison, brushable timelines, etc.), and JavaScript-driven interactive calculators for any quantifiable trade-off the meditation surfaces. **Every D3 chart must implement a meaningful static print equivalent** and **every interactive calculator must implement a `.calculator-static-fallback` containing 3–5 pre-computed what-if scenarios** — see subtask 07 for the full degradation contracts. A D3 chart or calculator that cannot degrade is forbidden.
```

(Subtask 07 will replace this with the fully-detailed version including per-pattern degradation rules.)

## Testing Strategy

- After applying, sanity-check that the HTML report would have at least 4 chart types and at least 3 infographics for a meditation that surfaces typical strategic-planning data.
- Confirm the Citations section spec is unambiguous about deduplication and backlinks.
- Confirm the sparseness fallback gives the agent a way to satisfy the structural minimums even on small `--quick` runs.
- Run the linter on both files.

## Execution Notes

### Agent Session Info
- Agent: crux-platform-architect
- Started: 2026-05-17
- Completed: 2026-05-17

### Work Log

1. Read the subtask spec and located the subtask-05 anchors in `.cursor/commands/crux-meditate.md` (HTML report **Structural elements** subsection, the **Other styling rules** CDN allowlist, the sparseness fallback paragraph) and `.cursor/agents/crux-cursor-memory-manager.md` (subagent step 12, Quick-mode step 12 substitution bullet, step-numbering note, design-principles list).
2. In the command file, replaced the placeholder line `(Visualization, infographic, calculator, and other content requirements live in subtasks 06 and 07.)` with three new content subsections directly under **Structural elements**:
   - `##### Visualizations (Chart.js + D3.js, loaded from CDN)` — ≥4 distinct chart types rule, D3 hard-rule pointing at subtask 07, Chart.js types list, D3 types-per-facet table (8 facet kinds), CDN load-from-`d3js.org` note, inline-data reminder.
   - `##### Infographics (HTML/CSS/SVG, no external library)` — ≥3 distinct infographic types rule plus the 11-entry curated list (hierarchy/tree, comparison matrix, decision tree, scorecard, process/pipeline, quadrant, heatmap, risk meter, timeline ribbon, concept map, Venn).
   - `##### Interactive elements` — ≥1 calculator with the `.calculator-static-fallback` forward-reference to subtask 07, filterable tables (print-hide UI, preserve data), citation-marker tooltips degrading to inline footnote markers in print.
3. Rewrote the **Citations section** bullet in the structural-elements list to spell out: mandatory in both modes, sourced from `citations-index.yml` (Research) / inline markers (Quick), deduplicated, backlinks to every citing section, and the "Citation gaps" callout in the executive summary that lists every uncited finding from Quick mode's warn-only path.
4. Confirmed the **Peer-review section** bullet (`one card per peer-review file`) and the **Footer** bullet (`theme:` annotation + mode label + depth/branch counts + total citation count) already read correctly from subtask 05 — no changes required.
5. Updated the sparseness fallback paragraph in **Other styling rules** to use the canonical wording (`the breadth for 4 chart types or 3 infographics`) instead of the placeholder forward-reference to subtask 06, and tidied the CDN-allowlist D3 comment to point at the in-file **Visualizations** subsection rather than to subtask 06 itself.
6. In the agent file, replaced subagent **step 12**'s report-bullet with the canonical form: now lists `at least 4 distinct chart visualizations` (Chart.js + D3 with facet-type guidance), `at least 3 distinct hand-rolled HTML/CSS/SVG infographics`, `at least one interactive calculator` (when a quantifiable trade-off exists), filterable tables, and the deduplicated Citations section (with the "Citation gaps" callout for Quick mode). Preserved all the operational detail from subtask 05 (responsive nav, `localStorage` toggle key, `@media print` and `body[data-print-mode="true"]` print theme, headless-Chrome / chromium-fallback render, CDN allowlist rule, `?print=1` toggle). The graceful-degradation contracts forward-reference is now only to subtask 07.
7. Updated the Quick-mode **Step 12** substitution bullet so subtask 06's content minimums explicitly apply unchanged in Quick mode (including the "Citation gaps" callout for unresolved citations).
8. Updated the **Step-numbering note** to mark subtask 06 as applied (with the full inventory of what it added) and to leave only subtask 07 as a forward-reference.
9. Added one new **design principle** to the agent file's design-principles list, placed immediately after the **Light + dark mode in HTML, high-contrast in PDF** principle:
   - **Visualizations + interactive elements: mandatory PDF graceful degradation (both modes)** — names the libraries (Chart.js, D3 from `https://d3js.org/`), enumerates the D3 facet-kind → chart-type mapping inline, mandates the static print equivalent for every D3 chart and the `.calculator-static-fallback` (3–5 pre-computed what-if scenarios) for every calculator (with the full contract deferred to subtask 07), spells out the four content minimums (≥4 chart types, ≥3 infographics, ≥1 calculator when a trade-off exists, filterable tables, tooltip-to-footnote degradation, deduplicated Citations section), and locks in the sparseness-fallback rule.
10. Verified the IDE linter is clean on both files. No external markdownlint config exists in the repo, so the IDE linter is the authoritative gate.
11. Cross-cutting check: subtask 06 did not introduce any new `askQuestion` prompts or `needs_user_input` escalations; the mandatory `context` decision-guidance rule from subtask 04 (carried forward by subtask 05) remains intact on every existing escalation in both files (verified by inspection of the Adversarial Review reviewer-escalation block and the Facet Confirmation Pattern-B flow).

### Blockers Encountered

None. The subtask was self-contained and the canonical content excerpts in the spec mapped one-to-one onto the anchors left by subtask 05.

### Files Modified
- `.cursor/commands/crux-meditate.md` — three new HTML-report content subsections (Visualizations, Infographics, Interactive elements), rewritten Citations bullet, canonicalised sparseness paragraph, in-file CDN-allowlist cross-reference.
- `.cursor/agents/crux-cursor-memory-manager.md` — canonicalised subagent step 12 report bullet (chart counts, infographic counts, calculator, filterable tables, dedup Citations), Quick-mode step 12 substitution bullet (subtask 06 minimums apply in Quick), step-numbering note (subtask 06 marked applied), one new design principle (visualizations + interactive elements PDF degradation + content minimums + sparseness fallback).
