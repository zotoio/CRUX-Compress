---
id: "f71d9d9"
title: "Interactive content in agent-generated artifacts must include meaningful static fallbacks for non-interactive renderers"
description: "D3 charts, JavaScript calculators, and filterable tables that work on screen can render as blank spaces in PDFs. Every interactive element MUST include a meaningful static fallback verified by a sanity-render gate before publication."
type: "redflag"
strength: 2
created: 2026-05-24
modified: 2026-05-24
source: "20260516-meditate-research-mode-overhaul"
tags: [pdf-degradation, static-fallback, interactive-content, d3, calculators, print-mode, accessibility]
---

When agent-generated artifacts include interactive content (D3 charts, JavaScript calculators, filterable tables), every interactive element MUST include a meaningful static fallback that renders identically in non-interactive contexts (PDF, print, screenshot).

Failure mode this prevents: interactive visualizations work perfectly on screen but render as blank spaces in static output (PDFs, screenshots, print). The user receives a professional-looking HTML artifact but a broken PDF — the failure is silent because the HTML never triggers the code path that reveals the gap.

Mandatory fallback contracts:
- **D3 charts**: paired `.d3-static-fallback` container with per-pattern degradation (hover→permanent labels, zoom→full-extent overview, expand-collapse→fully expanded, animation→settled state)
- **Calculators**: paired `.calculator-static-fallback` container with 3–5 pre-computed what-if scenarios (typical / optimistic / pessimistic / threshold / recommended) rendered as a table
- **Filterable tables**: filter/sort UI hidden in print, but underlying data preserved verbatim in default sort order

The verification gate is critical: before generating any static output, sanity-render with the static trigger (e.g. `?print=1`) and confirm every fallback container is non-empty and meaningfully populated. Block publication on any empty / under-populated fallback. Interactive content that cannot degrade should be replaced with an alternative visualization that can.
