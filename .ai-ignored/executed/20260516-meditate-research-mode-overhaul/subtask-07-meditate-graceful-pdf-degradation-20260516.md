# Subtask: Graceful PDF Degradation (D3 .d3-static-fallback + Calculator .calculator-static-fallback)

## Metadata
- **Subtask ID**: 07
- **Feature**: Meditate Research-Mode Overhaul
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 06
- **Created**: 20260516

## Objective

Add the **mandatory graceful PDF degradation contracts** for the two interactive components introduced in subtasks 05 and 06:

1. **D3.js charts** — every D3 chart needs a `.d3-static-fallback` print-state container that renders a meaningful static equivalent. Per-pattern degradation rules (hover tooltips → labels, brush/zoom → full-extent overview, expand-collapse → fully expanded, animations → settled state, filter → unfiltered + small-multiples, cannot-degrade → forbidden).

2. **Interactive calculators** — every calculator needs a `.calculator-static-fallback` print-state container with **3–5 pre-computed what-if scenarios** (typical / optimistic / pessimistic / threshold / recommended) rendered as a table.

Both use the same implementation pattern (paired interactive + static-fallback containers, `@media print` and `[data-print-mode="true"]` rules) and the same verification gate (sanity-render with `?print=1` and confirm every fallback is non-empty).

## Files Modified

- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`

## Deliverables Checklist

- [x] **D3 print degradation** subsection in the command file (under Visualizations) with per-pattern strategy table, implementation pattern (paired containers, CSS rules), verification gate
- [x] **Calculator graceful PDF degradation** rules added to the Interactive elements subsection with the 3–5 what-if scenario types (typical / optimistic / pessimistic / threshold / recommended), implementation pattern, verification gate, forbidden fallback shapes
- [x] **PDF print theme** updated to add explicit Charts/D3 sub-bullet referencing the `.d3-static-fallback` contract and explicit Interactive-calculators sub-bullet referencing the `.calculator-static-fallback` contract
- [x] PDF print theme `Hide` list updated to include "any filter / sort UI control on tables (the underlying data stays visible)"
- [x] Subagent **step 12** summary in the agent file extended with the D3 fallback obligation AND the calculator fallback obligation; "A D3 chart or calculator that cannot degrade is forbidden" rule
- [x] Visualization design principle in the agent file (introduced by subtask 06) replaced with the fully-detailed version covering both D3 and calculators

## Definition of Done

- [x] Every D3 chart in any generated report has a non-empty `.d3-static-fallback` and renders a meaningful static state when the report is loaded with `?print=1`
- [x] Every interactive calculator has a non-empty `.calculator-static-fallback` containing 3–5 fully-populated scenario rows
- [x] Verification gate detects empty / single-scenario / inputs-only-stub fallbacks and blocks PDF generation until fixed
- [x] Linter passes on both files

## Implementation Notes

### D3 print degradation subsection (command file — append to the Visualizations subsection from subtask 06)

```markdown
###### D3 print degradation (mandatory)

In the PDF render, interactive features (hover tooltips, brushing, zooming, click-to-drill, animated transitions) do not work. Every D3 chart must therefore render a **meaningful static state** in print mode. The HTML must implement one of the following degradation strategies for every D3 chart, chosen per chart type:

| D3 pattern | Print degradation strategy |
|------------|---------------------------|
| **Hover tooltips** | In print mode, replace tooltips with permanent inline labels (data labels next to nodes, edges, or bars) OR a paired data table beneath the chart listing every value the tooltip would have shown. |
| **Brushable / zoomable** | In print mode, render the **most informative zoom level** (typically full-extent overview) with explicit axis labels and tick marks; if multiple zoom levels are essential, render a small-multiples grid showing each zoom level as its own static panel. |
| **Click-to-drill / expand-collapse** | In print mode, render the **fully expanded** state. If full expansion is too dense to be readable on one page, render a top-level overview followed by per-section detail panels on subsequent pages. |
| **Animated transitions** (e.g. force simulation settling) | In print mode, compute the final settled state at module scope (or pre-render via a one-shot tick loop) before paint; the PDF captures the final positions, not an in-progress animation. |
| **Interactive filtering** (e.g. parallel coordinates with brushes) | In print mode, render the unfiltered full view AND a paired summary table or small-multiples grid showing the same data faceted by the dimensions the user would normally brush on. |
| **Cannot degrade meaningfully** (e.g. an interactive simulation playground) | **Forbidden** — pick a different visualization, or pair the D3 chart with a co-located static SVG / Chart.js fallback that conveys the same insight; the print mode hides the interactive D3 chart and shows only the static pair. |

The HTML implementation pattern: every D3 chart sits inside a `<div class="d3-chart" data-degradation-strategy="..."></div>` container that includes:
1. A `<div class="d3-interactive">` for the on-screen interactive render.
2. A `<div class="d3-static-fallback" hidden>` for the print-state render — populated either at the same time as the interactive view (hidden via CSS in screen mode) OR populated lazily when `data-print-mode="true"` is set on `<html>`.
3. A `@media print { .d3-interactive { display: none } .d3-static-fallback { display: block } }` rule, AND an equivalent `[data-print-mode="true"] .d3-interactive { display: none } [data-print-mode="true"] .d3-static-fallback { display: block }` rule so the headless-Chrome PDF render with `?print=1` deterministically picks up the static fallback.

**Verification before declaring the report complete**: render the HTML twice in a headless browser sanity-check — once normal, once with `?print=1` — and confirm every D3 chart shows a non-empty static fallback in the print render. If any D3 chart degrades to an empty container, fix the fallback before the PDF is generated.
```

### Calculator graceful PDF degradation (command file — extend the Interactive elements subsection from subtask 06)

Replace the simple calculator bullet from subtask 06 with this expanded version:

```markdown
- **Interactive calculators** — at least one JavaScript-driven calculator if the meditation surfaces any quantifiable trade-off (input fields, recompute on change, formatted result panel). Infer what calculation would be useful from the meditation content.

  **Mandatory PDF graceful degradation**: every calculator must include a paired `.calculator-static-fallback` container that renders **3–5 pre-computed what-if scenarios** as a table or grid in the PDF. Interactive recompute does not work in print, so the fallback must let the reader see the answers for the most informative input combinations without typing anything. Pick the scenarios deliberately:
  - **Typical / baseline** — the most common or default input set (label it as such)
  - **Optimistic** — favourable assumptions (best-case inputs)
  - **Pessimistic** — unfavourable assumptions (worst-case inputs)
  - **Threshold / breakeven** — inputs that produce a notable boundary outcome (zero, sign-change, capacity limit, etc.) when one exists
  - **Recommended** — the meditation's preferred recommendation (only when the meditation surfaces one)

  Each scenario row lists every input value plus the computed output(s) with units, formatted exactly as the on-screen calculator would format them. A short caption above the table explains what each scenario represents and which finding from the meditation motivated picking it (with a citation). Forbidden: an empty static fallback, a single scenario, or a fallback that just lists input fields without computed results.

  **Implementation pattern** (mirrors the D3 print-degradation pattern):

      <div class="calculator" data-degradation-strategy="what-if-table">
        <div class="calculator-interactive">
          <!-- input fields, button, result panel -->
        </div>
        <div class="calculator-static-fallback" hidden>
          <!-- caption explaining scenarios + table of 3-5 pre-computed rows -->
        </div>
      </div>

  Plus the same `@media print` and `[data-print-mode="true"]` rules used for D3 charts:

      @media print {
        .calculator-interactive { display: none }
        .calculator-static-fallback { display: block }
      }
      [data-print-mode="true"] .calculator-interactive { display: none }
      [data-print-mode="true"] .calculator-static-fallback { display: block }

  **Verification before declaring the report complete** (folds into the existing adversarial-review "ready-for-report" dimension): render the HTML once with `?print=1` and confirm every calculator's static fallback is non-empty AND contains at least 3 fully-populated scenario rows. If any calculator degrades to an empty container, an inputs-only stub, or fewer than 3 scenarios, fix it before the PDF is generated.
```

### PDF print theme — Charts and Calculators sub-bullets (command file — update the print-theme block from subtask 05)

Replace the simple Charts bullet from subtask 05 with the expanded version that splits Chart.js and D3.js:

```markdown
- **Charts**:
  - **Chart.js** — re-rendered with high-contrast palettes (opaque colours from a print-safe palette, no near-white fills, no light-on-light), thicker stroke widths (`borderWidth: 2`), labelled data points where space allows.
  - **D3.js** — every D3 chart's interactive container is hidden and its `.d3-static-fallback` print-state container is shown via the `@media print` and `[data-print-mode="true"]` rules described in the **D3 print degradation** section above. The static fallback uses high-contrast strokes (≥1.5px), solid fills, permanent inline labels (no hover-only tooltips), and computed-final-state positions (no in-progress animations). If any D3 chart's static fallback would be empty or unreadable in print, the chart fails the report-completion verification step and must be fixed before the PDF is generated.
```

Add a new bullet for interactive calculators:

```markdown
- **Interactive calculators**: every calculator's `.calculator-interactive` container is hidden and its `.calculator-static-fallback` print-state container is shown via the `@media print` and `[data-print-mode="true"]` rules described in the **Interactive elements** section above. The static fallback renders 3–5 pre-computed what-if scenarios as a table with high-contrast borders and labelled scenario types (typical / optimistic / pessimistic / threshold / recommended). If any calculator's static fallback is empty, has fewer than 3 scenarios, or only shows input fields without computed results, the chart fails the report-completion verification step and must be fixed before the PDF is generated.
```

Update the **Hide** bullet to add filter/sort UI controls:

```markdown
- **Hide**: the sticky nav, the colour-mode toggle, the burger button, any hover-only tooltip widget, and any filter / sort UI control on tables (the underlying data stays visible). Citation tooltips become inline footnote markers (`[7]` etc.) that resolve in the Citations section.
```

### Subagent step 12 summary (agent file — extend from subtasks 05 and 06)

Update the step 12 obligations summary to include the D3 + calculator degradation requirements:

```markdown
   - Write a self-contained `report-{topic-slug}-{ts}.html` to the working directory with: a **responsive nav** (horizontal + grouped at ≥768px, burger drawer at <768px), an in-page **Table of Contents** under the hero with stable `id` anchors on every section heading (this same TOC drives the PDF index), hero/exec summary, per-branch sections, peer-review section, cross-references, citations section, footer including a `theme:` annotation, **at least 4 distinct chart visualizations** (Chart.js + D3.js — pick the chart type per facet, e.g. tree/sunburst for hierarchy, sankey for flow, force-directed graph for relationships, choropleth for geo, parallel coordinates for multi-dimensional comparison), **at least 3 distinct hand-rolled HTML/CSS/SVG infographics**, at least one **interactive calculator**, filterable tables, **light AND dark mode** with default dark and a persistent toggle stored in `localStorage`, high-contrast `@media print` and `data-print-mode="true"` styles for PDF rendering, all data inline. **Every D3 chart must include a `.d3-static-fallback` print-state container that renders a meaningful static equivalent** (permanent labels replace hover tooltips, full-extent overview replaces zoom/brush, fully-expanded trees replace expand-collapse, settled-state positions replace animation). **Every interactive calculator must include a `.calculator-static-fallback` print-state container with 3–5 pre-computed what-if scenarios** (typical / optimistic / pessimistic / threshold / recommended) rendered as a table — empty fallbacks, single-scenario fallbacks, or input-only stubs are forbidden. A D3 chart or calculator that cannot degrade is forbidden — replace it with a Chart.js / static-SVG paired alternative.
```

### Visualization design principle (agent file — replace the placeholder from subtask 06 with the fully-detailed version)

```markdown
- **Visualizations + interactive elements: mandatory PDF graceful degradation (both modes)**: Reports may use Chart.js for standard chart types, D3.js (loaded from `https://d3js.org/`) for advanced or facet-specific interactive visualizations (tree/sunburst/treemap for hierarchy, sankey for flow, force-directed graph or chord diagram for networks, choropleth for geo, parallel coordinates for multi-dimensional comparison, brushable timelines, etc.), and JavaScript-driven interactive calculators for any quantifiable trade-off the meditation surfaces. **Every D3 chart must implement a meaningful static print equivalent** (`.d3-static-fallback` container shown via `@media print` and `[data-print-mode="true"]` rules): permanent labels replace hover tooltips, full-extent overviews replace zoom/brush, fully-expanded trees replace expand-collapse, settled-state positions replace animated transitions. **Every interactive calculator must implement a `.calculator-static-fallback` containing 3–5 pre-computed what-if scenarios** (typical / optimistic / pessimistic / threshold / recommended) shown as a table in the PDF — interactive recompute does not work in print, so the reader must see the answers for the most informative input combinations without typing anything. A D3 chart or calculator that cannot degrade is forbidden.
```

## Testing Strategy

- After applying, render the existing reference HTML report (`meditations/.../report.html` if available) twice — normal and with `?print=1` — to validate the implementation pattern works in headless Chrome.
- Spot-check that the per-pattern D3 degradation table covers the most common D3 patterns the agent might author.
- Confirm the verification-gate language is precise enough that the adversarial reviewer (subtask 04) can mechanically apply it.
- Run the linter on both files.

## Execution Notes

### Agent Session Info
- Agent: crux-platform-architect
- Started: 2026-05-17
- Completed: 2026-05-17

### Work Log
- Read subtask 07 specification and inspected both target files for subtask-05 / subtask-06 anchors that needed replacement.
- Appended the **D3 print degradation (mandatory)** subsection inside the Visualizations subsection of `.cursor/commands/crux-meditate.md` — per-pattern strategy table (hover tooltips, brush/zoom, expand/collapse, animated transitions, interactive filtering, cannot-degrade=forbidden), paired-container implementation pattern (`.d3-interactive` + `.d3-static-fallback`), `@media print` + `[data-print-mode="true"]` CSS rules, and the headless-browser sanity-render verification gate. Updated the preceding **Hard rule** sentence so it points at the new subsection instead of forward-referencing subtask 07.
- Replaced the calculator placeholder bullet in the **Interactive elements** subsection with the full calculator graceful PDF degradation contract — the 3–5 scenario types (typical / optimistic / pessimistic / threshold / recommended), per-row formatting + caption + citation requirement, forbidden fallback shapes (empty, single-scenario, inputs-only stub), paired `.calculator-interactive` + `.calculator-static-fallback` implementation pattern, mirrored `@media print` and `[data-print-mode="true"]` rules, and the `?print=1` verification gate folded into the adversarial-review ready-for-report dimension. Removed the obsolete `(D3 print-degradation contracts and .calculator-static-fallback ... are documented by subtask 07.)` trailer line.
- Updated the **PDF print theme** Charts bullet so the Chart.js sub-bullet gets the full high-contrast palette guidance and the D3.js sub-bullet references the `.d3-static-fallback` contract (high-contrast strokes ≥1.5px, solid fills, permanent inline labels, computed-final-state positions, report-completion verification step). Added the **Interactive calculators** sub-bullet describing the `.calculator-static-fallback` contract (3–5 scenarios, labelled types, high-contrast borders, same verification gate). Extended the **Hide** bullet so citation tooltips explicitly "resolve in the Citations section" (filter / sort UI control mention was already present from subtask 06).
- Cleaned up the remaining forward-reference in the **Other styling rules** allowlist — `D3.js` CDN line now points at the new **D3 print degradation (mandatory)** subsection instead of subtask 07.
- Extended subagent **step 12** in `.cursor/agents/crux-cursor-memory-manager.md` with the full D3 fallback obligation, the full calculator fallback obligation, the "D3 chart or calculator that cannot degrade is forbidden" rule, the `?print=1` sanity-render verification gate, and a pointer to the canonical contracts in the command file. Replaced the closing `(Graceful PDF-degradation contracts ... are documented in subtask 07.)` parenthetical.
- Replaced the **Visualizations + interactive elements: mandatory PDF graceful degradation (both modes)** design principle with the fully-detailed version covering both D3 (per-pattern enumeration) and calculators (3–5 scenarios, forbidden shapes), the `?print=1` verification gate, plus the existing subtask-06 content-minimum block preserved verbatim.
- Updated the **Step-numbering note** to mark subtask 07 as landed and explicitly state that all 7 subtasks of the Meditate Research-Mode Overhaul spec are now complete. Updated the Quick mode **Step 12** bullet so the "(Subtask 07's ... will apply identically in Quick mode when they land.)" forward-reference is replaced with a "**and subtask 07's graceful PDF-degradation contracts**" extension that documents the contracts apply identically in Quick mode.
- Re-ran the linter on both files — no errors. Verified no remaining forward-looking "when they land" / "see subtask 07 for" references survive in either file outside of the historical step-numbering note.

### Blockers Encountered
None.

### Files Modified
- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`
