---
name: crux-skill-memory-meditation-report
description: Mandatory paired HTML+PDF report generation for meditation: Comprehensiveness Level Mapping (12 dimensions × 4 levels), anti-homogenisation rules, Universal Contrast, light/dark mode + print TOC, Chart.js / D3 / calculator content minima with static fallbacks, Per-Branch Section Rule, Depth-3 Leaf Inclusion Rule, Peer-Review Surfacing Rule, Init-Suggestions Honour rules, K10b Per-Cheap-Type Rendering Contract (7 cheap types), and Report-Skill Respawn Protocol resume-handler. Use when the `crux-cursor-meditation-guide` agent runs report generation (step 12), when the ensemble aggregator generates the ensemble-level report, or when the report skill is respawned via Dim 13.
---

# CRUX Skill: Memory Meditation — Report Generation

Implements the mandatory paired HTML+PDF report generation contract: Comprehensiveness Level Mapping, Anti-Homogenisation Rules, Universal Contrast, light/dark mode + print TOC, Chart.js / D3 / calculator with static fallbacks, Subject-Matter Focus rule, Init-Suggestions Honour, K10b Per-Cheap-Type Rendering Contract, headless Chrome → Chromium degradation, and the Report-Skill Respawn Protocol resume-handler.

## When to Use

Load this skill when:
- The `crux-cursor-meditation-guide` agent runs report generation at step 12 of the depth-0 manager workflow
- The `crux-cursor-meditation-guide` ensemble aggregator generates the ensemble-level report (step 4 of Ensemble Aggregation)
- The report skill is respawned via Dim 13 of the adversarial review (Report-Skill Respawn Protocol)

## Prerequisites

1. Adversarial review verdict is `PASS` or `PASS_WITH_ADVISORIES` — **never run on `ESCALATE`**
2. `comprehensiveness:` payload is present — abort with: "`comprehensiveness:` payload required; missing from spawn prompt — caller misconfigured" if missing
3. `theming:` payload is present — abort with a clear error pointing at Theme Preflight if missing
4. All meditation files are available in the working directory

## Comprehensiveness Level Mapping (contract)

The report-generation skill reads the `comprehensiveness:` payload from its spawn prompt. Every subsection that cites a content minimum (charts, infographics, calculators, section depth, leaf inclusion) reads from this payload rather than hard-coding fixed numerals.

**`comprehensiveness:` payload fields consumed by report generation:**

| # | Dimension (`comprehensiveness.minima.*`) | `compact` | `default` | `detailed` | `exhaustive` |
|---|------------------------------------------|-----------|-----------|------------|--------------|
| 1 | `minima.charts.count` | **4** | 5 | 7 | 10 |
| 2 | `minima.charts.types_required` | Any 4 distinct from Chart.js + D3 mix | ≥5 distinct, ≥1 D3-advanced (sunburst, sankey, force-directed, parallel-coordinates, choropleth) | ≥7 distinct, ≥2 D3-advanced, ≥1 per facet-kind: comparison, trend, distribution | ≥10 distinct, ≥3 D3-advanced, ≥1 per facet-kind: comparison, trend, distribution, composition, network/relationship, geo (when topic supports geo) |
| 3 | `minima.infographics.count` | **3** | 4 | 6 | 8 |
| 4 | `minima.infographics.types_required` | Any 3 distinct from the existing menu | ≥4 distinct, ≥1 hierarchy, ≥1 process/flow | ≥6 distinct, ≥1 hierarchy, ≥1 process/flow, ≥1 comparison (matrix/quadrant) | ≥8 distinct, ≥1 each of: hierarchy, process/flow, comparison, taxonomy, timeline, persona |
| 5 | `minima.calculators.count` | **1** | 1 | 2 | 3 |
| 6 | `minima.calculators.scenarios_per` | **3** | 4 | 5 | 5 |
| 7 | `depth3_leaf_inclusion` | `summary` | `summary` | `verbatim_quotes` | `verbatim_quotes` |
| 8 | `per_branch_section_depth` | `consolidation_only` | `branch_summary` | `per_leaf_detail` | `per_leaf_detail` |
| 9 | `citation_density` | Research=`mandatory`; Quick=`warn_only` | Research=`mandatory`; Quick=`warn_only` | Research=`mandatory`; Quick=`warn_only` | Research=`per_finding_table`; Quick=`warn_only` with per-finding-table column (placeholder text for missing citations) |
| 10 | `peer_review_surfacing` | `consolidation_only` | `consolidation_only` | `named_section` | `per_branch_dedicated` |
| 11 | `section_length_budget_tokens` | `{ hero: 800, per_facet: 2500, citations: 1000 }` | `{ hero: 1200, per_facet: 4000, citations: 1500 }` | `{ hero: 1800, per_facet: 6500, citations: 2000 }` | `{ hero: 2400, per_facet: 9500, citations: 2500 }` |
| 12 | `ensemble_cross_model_depth` | `per_facet_cards` | `per_facet_cards` | `per_leaf_attribution` | `per_leaf_attribution` |

**`compact` backwards-compatibility anchor**: The `compact` row reproduces the pre-richness-feature behaviour byte-for-byte (4 charts, 3 infographics, 1 calculator, 3 scenarios per calculator, depth-3 leaf content elided beyond summary, all per-branch content folded into consolidation prose only, peer-review content folded into consolidation prose only). All subsections must produce identical output for a `compact` run as the pre-richness codebase did.

**Subagent-abort rule**: if the `comprehensiveness:` payload is missing from the spawn prompt, abort with: "`comprehensiveness:` payload required; missing from spawn prompt — caller misconfigured."

## Paired HTML+PDF Rule

Use the meditation's **topic slug** plus a UTC timestamp captured at the moment of report generation:

    TS=$(date -u +%Y%m%d%H%M%S)
    SLUG="{topic-slug}"
    HTML="{workingDir}/report-${SLUG}-${TS}.html"
    PDF="{workingDir}/report-${SLUG}-${TS}.pdf"

- `{topic-slug}` MUST exactly match the slug component of the working-directory name.
- The HTML and PDF for a single generation share the same timestamp.
- All references match these files via the prefix glob `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf`. **Never hard-code `report.html` / `report.pdf`.**
- Respawned reports get a fresh timestamp. The prior HTML/PDF pair is **preserved on disk** for diff inspection.

## Inputs

1. **Read all meditation files**: Load `consolidation.md`, `facets.md`, `facet-registry.yml` (Research mode), `citations-index.yml` (Research mode), all `branch-*-depth-*-sub-*-*.md` files, and all `branch-*-peer-review-*.md` files (Research mode) from the working directory.
2. **Read `init-suggestions-{ts}.yml`** if it exists (honour rules below).
3. **Read `finalisation-enhancements.yml`** if it exists and has accepted cheap entries (K10b rendering below).
4. **Read `model_strategy` from `facets.md` frontmatter** (per the `crux-skill-memory-meditation-coordination` skill's `facets.md` frontmatter spec). The model strategy drives per-branch attribution annotations (per the **Per-Branch Model Attribution** section below) and the footer annotation.

## Anti-Homogenisation Rules

AI-generated reports converge on a recognisable homogenised aesthetic. **All of the following defaults are forbidden** unless the user's `theming` payload explicitly invoked them by name:

- **Purple-blue gradient hero** (`linear-gradient(135deg, indigo, blue/violet)` and friends).
- **Inter as the headline font weight 700**. Default to a font dictated by the `theming.preset.typography` value or the matched repo signal.
- **Three-card feature grids** as the dominant layout. Vary layout per section (asymmetric grids, single hero panel, two-column with sidebar, full-bleed tables, masonry).
- **Doughnut chart with circular tinted-color legend chips**. Either move the legend, change its shape, or pick a different chart for the same data.
- **Tailwind `indigo-500` (or its variants `#6366f1`, `#818cf8`) as the accent**. Pick a palette from the `theming` payload.
- **Lucide-style icon-in-tinted-circle motif** for stat cards and bullets.
- **Centred body paragraphs** and **gradient "Most popular" pricing pills** as filler.
- **Five-star testimonial rows** and **DiceBear avatar fallbacks**.
- **Smooth modern dark blue UI**, full stop, when no theming choice asked for it.

How to apply this:
1. Before writing any CSS, look at the `theming` payload and pick concrete values (font stack, primary/secondary/accent hex, layout grammar, divider style, link decoration, heading scale).
2. If the chosen direction would naturally produce one of the forbidden patterns, *deliberately substitute*.
3. Include a one-line `theme:` annotation in the footer naming the resolved direction, palette, and typography.

## Universal Contrast (mandatory)

Every rendered element in the HTML and PDF reports must maintain high contrast against its actual background in **both** light and dark screen modes and in the print/PDF mode.

**Minimum contrast requirements**:
- Body text, table text, captions, labels, legends, footnotes, citation markers, nav links, badge text, and chart labels: WCAG AA normal-text contrast (≥4.5:1) against the exact background behind the element.
- Large headings and large stat numerals: WCAG AA large-text contrast (≥3:1), with ≥4.5:1 preferred unless the design would be harmed.
- Non-text graphical elements that convey information (chart lines, SVG connectors, axes, grid lines, quadrant boundaries, heatmap cells, risk-meter segments, badges, table borders, focus rings): WCAG non-text contrast (≥3:1) against adjacent colours, with ≥4.5:1 preferred for thin lines (<2px) or small marks.

**Hard rules**:
- Never place text directly on a gradient, texture, image, translucent overlay, or saturated colour block unless the report also adds a solid or sufficiently opaque backing panel behind the text.
- Do not rely on pastel text, low-opacity strokes, faint grid lines, transparent fills, glow-only emphasis, or colour-only distinctions.
- Chart.js and D3 palettes must be generated separately for dark, light, and print modes.
- Every SVG/HTML infographic must define explicit stroke and text colours for each colour mode.
- Heatmaps and quadrant backgrounds must keep labels readable in every cell/region.
- Thin lines (axes, connectors, borders) must be thickened, darkened, or backed by sufficient spacing if they would otherwise fall below contrast on coloured backgrounds.

## Light + Dark Mode (mandatory)

- **Both modes are required.** Default = dark mode on first load, regardless of system preference.
- **Toggle in the nav** — a clearly visible button. Switches modes immediately, no flicker.
- **Persistence** — store the user's choice in `localStorage` under `meditation-color-mode`; on subsequent loads, honour the stored value before any rendering occurs (set on `<html>` before paint to avoid FOUC).
- **System preference signal** — read `window.matchMedia('(prefers-color-scheme: dark)')` only as a fallback when no localStorage value exists.
- **Charts** — Chart.js color values must adapt to the active mode. Wire chart options to read CSS custom properties for stroke/fill.

## Print TOC + Print Theme (mandatory)

The PDF must open with a **clickable Table of Contents** as the first content page.

- Place inside `<nav id="toc" aria-label="Table of contents">` immediately under the hero.
- Every section heading (`<h2>` / `<h3>`) carries a stable, kebab-case `id`.
- Headless Chrome preserves anchor links in the printed PDF natively.
- Two levels deep; add `<style>@media print { #toc { page-break-after: always; } }</style>`.

**High-contrast print theme** (applied via `@media print` AND `body[data-print-mode="true"]`):
- **Background**: pure white (`#fff`) or near-white (`#fafafa`).
- **Body text**: near-black (`#0a0a0a` / `#111`), minimum 11pt.
- **Headings**: `#000` with the chosen theme's display typeface preserved.
- **Links**: dark accent (`#0033aa` or theme-equivalent), underlined.
- **Tables**: black 1px borders, alternating row backgrounds at `#f5f5f5`.
- Hide: the sticky nav, the colour-mode toggle, the burger button, any hover-only tooltip widget, and any filter / sort UI control on tables.
- Every top-level section starts on a new page (`page-break-before: always`).

## Chart.js + D3 + Calculator Rules with Static Fallbacks

Pick **at least `comprehensiveness.minima.charts.count` distinct chart types** from Chart.js + D3 combined. Accepted finalisation enhancements that include charts count toward this minimum.

**D3 print degradation (mandatory)** — every D3 chart must render a **meaningful static state** in print mode via a `<div class="d3-static-fallback" hidden>` container:

| D3 pattern | Print degradation strategy |
|------------|---------------------------|
| **Hover tooltips** | In print mode, replace tooltips with permanent inline labels OR a paired data table. |
| **Brushable / zoomable** | In print mode, render the **most informative zoom level** with explicit axis labels; use small-multiples if multiple zoom levels are essential. |
| **Click-to-drill / expand-collapse** | In print mode, render the **fully expanded** state. |
| **Animated transitions** | In print mode, compute the final settled state at module scope before paint. |
| **Interactive filtering** | In print mode, render the unfiltered full view AND a paired summary table. |
| **Cannot degrade meaningfully** | **Forbidden** — pick a different visualization or pair the D3 chart with a co-located static SVG / Chart.js fallback. |

The HTML implementation pattern:
```html
<div class="d3-chart" data-degradation-strategy="...">
  <div class="d3-interactive"><!-- on-screen interactive render --></div>
  <div class="d3-static-fallback" hidden><!-- print-state render --></div>
</div>
```
```css
@media print {
  .d3-interactive { display: none }
  .d3-static-fallback { display: block }
}
[data-print-mode="true"] .d3-interactive { display: none }
[data-print-mode="true"] .d3-static-fallback { display: block }
```

**Calculator static fallback (mandatory)** — every calculator must include a paired `.calculator-static-fallback` container with **`comprehensiveness.minima.calculators.scenarios_per`–5 pre-computed what-if scenarios** as a table:

```html
<div class="calculator" data-degradation-strategy="what-if-table">
  <div class="calculator-interactive"><!-- input fields, button, result panel --></div>
  <div class="calculator-static-fallback" hidden>
    <!-- caption explaining scenarios + table of pre-computed rows -->
  </div>
</div>
```

Scenarios: **Typical / baseline**, **Optimistic**, **Pessimistic**, **Threshold / breakeven**, **Recommended** (when the meditation surfaces one). Forbidden: an empty static fallback, a single scenario, or a fallback that just lists input fields without computed results.

**Report Comprehensiveness — No Information Loss (mandatory)**: The report is the **final deliverable**. Every important finding, data point, comparison, citation, and insight discovered across the entire research tree must be faithfully represented. Before declaring the report complete, enumerate the key findings from each branch file's `## Discoveries` and `## Summary` sections and verify each has a corresponding presentation element. Log any gap and fill it.

**Option Comparison Research Reporting (mandatory when applicable)**: When the meditation's goal involves option comparison research (detected from the confirmed facets and topic-slug), the report MUST include all of: (1) feature comparison matrix with color-coded cell-level indicators, (2) adoption and market presence data with trend direction, (3) Gartner Magic Quadrant-style 2×2 quadrant visualization, (4) key differentiators section with visual scorecards, (5) recommendation or decision framework infographic when the research supports one. These are **additional** to the standard content minimums.

## Per-Branch Section Rule (level-conditional)

The `comprehensiveness.per_branch_section_depth` value determines how confirmed top-level facets are rendered:

- **`consolidation_only`** (`compact`): all per-branch content folds into consolidation prose. Each confirmed facet does NOT get its own standalone report section beyond what the consolidation already surfaced. Facet titles appear as section headings within the consolidated structure.
- **`branch_summary`** (`default`): each confirmed top-level facet gets its own report section presenting a branch-level summary of key findings beyond what the consolidation summarised.
- **`per_leaf_detail`** (`detailed` / `exhaustive`): every confirmed top-level facet gets its own dedicated report section with per-leaf subsections. Depth-3 leaf material is rendered at `verbatim_quotes` depth (quoted with full citations).

**`additional_facet` and `additional_facet_AND_section` branches** at `detailed`+ (`per_leaf_detail`): each gets its own dedicated section just like the original 3 facets. `additional_facet_AND_section` branches additionally honour the user-supplied `custom_report_section_title` from `init-suggestions-{ts}.yml` as the section heading.

## Depth-3 Leaf Inclusion Rule (level-conditional)

The `comprehensiveness.depth3_leaf_inclusion` value determines how depth-3 leaf material appears:

- **`summary`** (`compact` / `default`): depth-3 leaf material is surfaced via its depth-2 parent's summary. Leaf-level verbatim content is elided beyond summary.
- **`verbatim_quotes`** (`detailed` / `exhaustive`): depth-3 leaf material is quoted verbatim (the most decision-relevant passages) with full citations (`[research: {subfocus-slug}]`). At least one verbatim quote per branch's depth-3 leaf set is required. Every depth-3 leaf's key finding must appear in the relevant per-branch section with direct citation.

## Peer-Review Surfacing Rule (level-conditional)

The `comprehensiveness.peer_review_surfacing` value determines how peer-review findings surface. **Quick mode is a no-op at every level** — the report skill emits a one-line "Peer review not applicable in Quick mode" placeholder when the level demands a named or per-branch section but no peer-review files exist.

- **`consolidation_only`** (`compact` / `default`): peer-review reinforcements, contradictions, and gaps reach the report only through the consolidation prose. No dedicated peer-review section beyond the existing "Quality review section" structural element.
- **`named_section`** (`detailed`): in addition to the existing quality-review content, the report adds three dedicated named cross-branch sections: "Cross-Branch Reinforcements", "Cross-Branch Contradictions", and "Cross-Branch Gaps".
- **`per_branch_dedicated`** (`exhaustive`): one named peer-review section per branch (e.g. "Branch 1 — {Facet Title}: Reinforcements / Contradictions / Gaps"), PLUS the three cross-branch named sections from `named_section`.

## Init-Suggestions Honour (mandatory when `init-suggestions-{ts}.yml` exists)

At the start of report generation, read `init-suggestions-{ts}.yml` from the working directory.

**Required honour rules**:

1. **Confirmed sections** — every `confirmed_sections[i].title` MUST appear as a report section heading in the rendered HTML, with substantive non-empty content (>1 paragraph or >100 words). A heading-only stub counts as missing.
2. **Confirmed visualisations** — every `confirmed_visualisations[i].type` MUST be rendered with non-empty data (a container with no data series counts as missing). The report MAY render additional chart / infographic types beyond these confirmed ones.
3. **Additional focus areas** — every `additional_focus_areas[]` entry whose `treatment == "report_section_only"` MUST become a report section, with the entry's `rationale` prose included at the top of the section. Entries with other `treatment` values (`skip`, `additional_facet`, `additional_facet_AND_section`) are handled separately per the Branch & Leaf Index + per-branch section rules; `skip` entries are not honoured by the report.

The report MAY add more sections and more chart/infographic types beyond what `init-suggestions-{ts}.yml` confirmed — the file defines the **floor**, not the ceiling.

If `init-suggestions-{ts}.yml` does not exist (pre-richness run, or Quick mode before the file was introduced), skip these checks silently and fall back to the standard comprehensiveness minima.

> **Audit**: Adversarial Review Dimension 13 audits compliance with these honour rules after the report is generated — any confirmed section or visualisation that is absent or only present as an empty stub triggers a `MUST_FIX` + `respawn_required: true` finding.

## K10b Per-Cheap-Type Rendering Contract (7 cheap types)

When a respawn payload carries `accepted_finalisation_enhancements`, the report skill renders each accepted cheap enhancement as follows. Accepted cheap enhancements count **toward the existing `comprehensiveness.minima` counts** — a `decision_tree_infographic` counts as an infographic; a `risks_section` with risk-meter counts as both an infographic (the risk meter) AND a section.

| Type | Landing location in the report | Payload shape consumed | Static degradation rules |
|------|-------------------------------|------------------------|--------------------------|
| `executive_summary` | Before the hero stat-card row, immediately after the title | `{ target_persona, max_paragraphs, anchor_findings }` | Flowing prose, no homogenised marketing-pill cards; respect chosen `theming` payload; ≤`max_paragraphs` paragraphs; citations per `anchor_findings`. |
| `action_plan` | After the per-facet sections, before cross-cutting connections section | `{ horizons: ["7d", "30d", "quarter"], items_per_horizon, anchor_findings }` | Horizon-grouped list (7d / 30d / quarter) with citations per item; rendered as a Gantt-style timeline ribbon (D3 + static fallback) OR a labelled tabular form respecting the chosen direction. Print fallback: full table with all horizons. |
| `risks_section` | After the per-facet sections | `{ risk_taxonomy_axes: ["likelihood", "impact", "detection_difficulty"], anchor_findings }` | Risk-meter / gauge infographic (per the existing infographics catalogue) paired with a risk taxonomy table; risk-meter counts as 1 infographic toward `comprehensiveness.minima.infographics.count`. Print fallback: full table with all risk rows visible. |
| `glossary` | End-of-document appendix, before Citations section | `{ term_count_estimate, anchor_branches }` | 2-column term/definition list; respect chosen typography; print preserves all entries. |
| `decision_tree_infographic` | After the per-facet sections, before the cross-cutting connections section | `{ root_decision, depth, anchor_findings }` | SVG decision tree; print fallback shows fully-expanded state (no click-to-expand); respects `theming.preset.color_scheme`. Counts as 1 infographic toward `comprehensiveness.minima.infographics.count`. |
| `reader_persona_tldrs` | After the executive summary / hero, before the per-facet sections | `{ personas: ["leadership", "engineer", "product"], paragraphs_per_persona }` | Per-persona card grid (NOT the homogenised three-card feature grid — vary per chosen direction); print preserves all personas. |
| `cross_branch_synthesis_section` | After the per-facet sections and any `action_plan` / `decision_tree_infographic`, before Citations | `{ axes: ["convergent", "divergent"], anchor_findings_per_axis }` | Two-column or three-column "convergent / divergent / unique" layout (per chosen direction); citations attached per item. |

## Report-Skill Respawn Protocol — Resume-Handler

When invoked with a `respawn_payload` (from Dim 13 of the adversarial review), process the reasons in this order:

### Per-Reason Processing Order

1. **`accepted_finalisation_enhancements`** — additive new sections / charts; render these first per the K10b Per-Cheap-Type Rendering Contract above.
2. **`missing_init_suggestion_visualisations`** — additive; render missing viz containers + data series.
3. **`missing_init_suggestion_sections`** — may be auto-resolved by step 1 if an accepted-enhancement title overlaps with a missing-section title via **fuzzy-match**: case-insensitive substring match in either direction. When step 1 auto-resolves a step-3 missing section, mark the missing section as `auto_resolved: true` in the respawn-output report metadata; the next iteration's reviewer verifies the enhancement-driven section meets the substantive-content bar (>1 paragraph / >100 words).

When step 1 and step 3 fire simultaneously and step 1 resolves a step-3 entry via fuzzy-match, only 1 iteration is consumed (the bundle counts as a single respawn).

### Output Filename Rule

Respawned reports get a fresh timestamp: `TS=$(date -u +%Y%m%d%H%M%S)`. The prior HTML/PDF pair is **preserved on disk** for diff inspection. The Branch & Leaf Index resolves the latest pair via prefix-glob — the newest file per glob is authoritative.

### Iteration Accounting

- Respawn shares the existing ≤3 adversarial review-and-fix iteration cap.
- **Maximum useful respawns per meditation = 2**.
- The `accepted_finalisation_enhancements` cause can fire **at most once** per meditation.

### Same-Iteration Dim 1–11 Fix + Dim 13 Respawn Ordering

When an iteration simultaneously fires Dim 1–11 findings AND Dim 13:
1. **First**: Dim 1–11 in-place fixes are applied by the reviewer to branch / consolidation / peer-review files.
2. **Then**: the report skill is respawned; it re-reads the now-fixed branch files and regenerates the report incorporating the in-place fixes.

### Ensemble Per-Branch vs Cross-Model Targeting

In ensemble mode, the `respawn_payload` carries `source` provenance on accepted enhancements:
- `source: "tree:{model-subdir}"` → respawn targets the per-tree report (`{model-subdir}/report-{topic-slug}-{ts}.html/.pdf`)
- `source: "cross_model"` → respawn targets the cross-model synthesis report (`ensemble-report-{topic-slug}-{ts}.html/.pdf`)

## Headless Chrome → Chromium Degradation

Render the PDF from the generated HTML. Pass `?print=1` so the HTML can switch to its print theme. The HTML must read `URLSearchParams` on load and apply `data-print-mode="true"` to `<html>` when `print=1` is set.

```bash
google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf="${PDF}" \
  --print-to-pdf-no-header \
  --no-pdf-header-footer \
  "file://${HTML}?print=1"
```

Try `chromium` and `chromium-browser` as fallback binaries if `google-chrome` is not installed. If no headless Chromium is available, **fail with a clear error**: report the missing dependency, list the installation hint for the user's platform (e.g. `brew install --cask google-chrome` on macOS, `apt install chromium` on Debian/Ubuntu), and leave the HTML file in place so the user can manually print to PDF.

## Subject-Matter Focus Rule (all user-facing outputs)

The HTML/PDF reports are **subject-matter documents**, not process logs. They must read as authoritative analyses of the meditation topic.

**Forbidden in reports**:
- References to "Branch 1", "Branch 2", "Branch 3" as organizational labels (use facet titles).
- References to "depth-1", "depth-2", "depth-3", "leaf agents", "sub-agents", or agent counts.
- The `[child: branch-N-depth-D-sub-S]` citation format — translate to `[research: {subfocus-slug}]`.
- References to "peer-review agents" or "peer reviewers" as actors (use "cross-cutting analysis", "independent verification", "quality review").
- Process-framing in executive summaries ("this meditation explored X across three branches" → "this analysis covers X").

**Required instead**:
- Section headings use the facet titles and subfocus descriptions.
- Organizational framing follows the subject matter's natural structure.
- Cross-references use topics by name.
- Executive summaries lead with the substantive conclusion.

## Per-Branch Model Attribution (level-conditional on `model_strategy.mode`)

The `model_strategy` block read from `facets.md` frontmatter drives how the report attributes findings by model:

- **`mode: "none"`** — no attribution annotations; report renders exactly as it did pre-modelStrategy.
- **`mode: "random"`** — the hero or executive-summary stat-card row includes one extra stat card or annotation: `Model: {resolved_model_label}` (one line, near the existing meta-row such as "Mode" / "Depth" / "Richness"). Per-branch sections do NOT carry per-finding model attribution because the entire tree ran on a single model.
- **`mode: "per_branch"`** — every per-branch section heading (when `per_branch_section_depth ∈ {branch_summary, per_leaf_detail}`) includes a `[branch model: {label}]` annotation next to the facet title. Findings in those sections inherit the annotation from their containing branch section (no per-finding repetition required). When `per_branch_section_depth == "consolidation_only"` (compact richness), inline `[branch model: {label}]` markers appear adjacent to each finding inside the consolidated prose to preserve attribution. The model legend MUST appear in the hero's meta-row (e.g. as a small chip row: `Branch 1: GPT 5.5 · Branch 2: Opus 4.7 · Branch 3: Gemini Pro 3.1`) so the reader can map labels to facets without scrolling.
- **`mode: "ensemble_max"`** — model attribution follows the ensemble report contract in the `crux-skill-memory-meditation-ensemble` skill (`[model: label]` / `[models: all]` markers, agreement heatmap, etc.). Per-tree reports under `model-{slug}/` use single-model attribution (effectively the `random` rendering pinned to that tree's model).

**Citation list integration**: when per-branch attribution markers are present, the `## Citations` section adds a brief "Model attribution" subsection listing each branch's model and the count of findings attributed to it.

## Footer Annotation

The footer annotation format:

    theme: editorial / warm_palette / serif_headings_sans_body | level: default

The `model_strategy` extension extends the footer:

- **`mode: "none"`** → no model-strategy segment appended.
- **`mode: "random"`** → append `| model_strategy: random ({resolved_model_label})`
- **`mode: "per_branch"`** → append `| model_strategy: per_branch ({comma-separated list of "b{index}: {label}"})`. Example: `| model_strategy: per_branch (b1: GPT 5.5, b2: Opus 4.7, b3: Gemini Pro 3.1)`.
- **`mode: "ensemble_max"`** → handled by the ensemble report contract (per-tree reports show the tree's pinned model; the cross-model synthesis report uses the ensemble footer extension in `skill:ensemble`).

When ≥1 finalisation enhancement was accepted and rendered via the respawn path, the existing `finalisation-enhancements:` segment is appended in the usual position. Order in the footer when all segments are present: `theme: … | level: … | model_strategy: … | finalisation-enhancements: …`.

Example combined footer:

    theme: editorial / warm_palette / serif_headings_sans_body | level: default | model_strategy: per_branch (b1: GPT 5.5, b2: Opus 4.7, b3: Gemini Pro 3.1) | finalisation-enhancements: 2 (executive_summary, risks_section)

**Skip-all path**: when 0 finalisation enhancements were accepted, the `finalisation-enhancements:` segment MUST be omitted entirely — it must NOT be written as `finalisation-enhancements: 0`. The `level:` segment IS always written from this spec forward. The `model_strategy:` segment is written if and only if `mode ≠ "none"`.

**Ensemble split**: per-tree reports' footer annotations enumerate ONLY the per-tree-sourced accepted enhancements; the cross-model synthesis report's footer enumerates ONLY the cross-model-sourced accepted enhancements.

## Final Verification

Before returning control to the user, verify exactly one matching pair exists and both files are non-empty:

    HTML_LATEST=$(ls -1t "{workingDir}"/report-"{topic-slug}"-*.html 2>/dev/null | head -n 1)
    PDF_LATEST=$(ls -1t  "{workingDir}"/report-"{topic-slug}"-*.pdf  2>/dev/null | head -n 1)
    [ -s "${HTML_LATEST}" ] && [ -s "${PDF_LATEST}" ]

If either check fails, regenerate the missing artifact before presenting results.

**Verification before declaring the report complete** (includes D3 + calculator degradation checks): render the HTML once with `?print=1` and confirm:
1. Every D3 chart shows a non-empty static fallback in the print render.
2. Every calculator's static fallback is non-empty AND contains at least `comprehensiveness.minima.calculators.scenarios_per` fully-populated scenario rows.
3. Every element passes Universal Contrast in dark screen mode, light screen mode, and `?print=1` PDF mode.

## Other Styling Rules

- All data embedded inline as JavaScript constants — **no external data fetches**, no `fetch()` calls.
- Allowed external resources (CDN script tags only):
  - **Chart.js** — `https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js`
  - **D3.js** — `https://d3js.org/d3.v7.min.js`
  - **D3 plugins** as needed (`d3-sankey`, `d3-cloud`) loaded from the same official CDNs
  - **Custom fonts** from Google Fonts or `https://rsms.me/` *only if the chosen theme requires a non-system font*
- No other external scripts, stylesheets, or assets.

## Cross-Skill References

- `crux-skill-memory-meditation-coordination` — report filename grammar (never hard-code); fresh-timestamp respawn rule; prefix-glob latest-wins
- `crux-skill-memory-meditation-review` — authors the Dim 13 respawn payload that this skill consumes as a resume-handler
- `crux-skill-memory-meditation-ensemble` — ensemble report extras (model comparison hero, agreement heatmap, etc.) layer on top of this skill's mandatory minimums; ensemble per-tree vs cross-model respawn targeting
- `crux-skill-memory-meditation-research` — source of `init-suggestions-{ts}.yml` (Research write side)
- `crux-skill-memory-meditation-quick` — source of `init-suggestions-{ts}.yml` (Quick write side)
