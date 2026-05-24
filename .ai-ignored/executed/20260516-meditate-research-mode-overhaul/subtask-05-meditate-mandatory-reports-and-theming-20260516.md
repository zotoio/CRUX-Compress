# Subtask: Mandatory HTML + PDF Reports, Theming, Light/Dark, Responsive Nav, PDF TOC, Report Filenames

## Metadata
- **Subtask ID**: 05
- **Feature**: Meditate Research-Mode Overhaul
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 04
- **Created**: 20260516

## Objective

Make HTML + PDF report generation a **non-negotiable mandatory artefact** of every meditation, named per the `report-{topic-slug}-{ts}.{html,pdf}` convention. Add the structural reportgeneration spec covering:

- Filename pairing (HTML and PDF share the same UTC `{ts}`)
- Theming application driven by the Theme Preflight payload
- Anti-Homogenisation Rules (forbidden defaults referencing the canonical screenshot)
- Light + Dark mode (default dark, persistent toggle)
- Responsive Navigation (horizontal grouped at ≥768px, burger drawer at <768px)
- PDF requirements: high-contrast print theme + clickable Table of Contents
- Headless-Chrome render command with `?print=1` and chromium-binary fallback

The actual content requirements (charts, infographics, calculators, citations) live in subtask 06; the graceful PDF degradation contracts live in subtask 07.

## Files Modified

- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`

## Deliverables Checklist

- [x] **Report Generation — MANDATORY** section in the command file with intro, filename convention, inputs subsection, structural-elements subsection
- [x] **Anti-Homogenisation Rules** subsection with forbidden defaults (purple-blue gradient hero, Inter-700, three-card grids, doughnut + tinted-circle legend, Tailwind indigo-500 accent, lucide icon-in-tinted-circle, etc.) referencing the canonical screenshot path
- [x] **Theming application** subsection mapping `theming.source` enum values to render rules
- [x] **Light + Dark mode (mandatory)** subsection with default-dark, persistent toggle, system-preference fallback rules, contrast requirements, chart-color binding to CSS custom properties
- [x] **Responsive Navigation (mandatory)** subsection with breakpoint, grouping, burger drawer, accessibility, active-section highlighting
- [x] **PDF report requirements** subsection with filename pairing snippet, high-contrast print theme rules, mandatory Table of Contents, render command with `?print=1`, chromium-binary fallback chain, abort-on-missing-Chromium error
- [x] **Other styling rules** subsection with CDN allowlist (Chart.js + D3.js + plugins + optional fonts) and no-runtime-fetch rule
- [x] Subagent **step 12** (generate report) in the agent file references the command's Report Generation section as source of truth and lists the obligations summary
- [x] **Calling agent step 9** (verify report artifacts) added: glob the working directory for the latest matching pair, regenerate if missing, surface PDF-render failure prominently
- [x] **Calling agent step 10** (present to user) updated to always include the absolute paths to `facets.md`, the latest report HTML/PDF pair
- [x] **Calling agent step 11** (interactive continuation) reduced to: expansion options + save-spec + end (NO save-as-HTML/PDF — already mandatory)
- [x] One new design principle in the agent file: mandatory report artifacts (both modes); existing light/dark + responsive-nav design principle added

## Definition of Done

- [x] Every meditation produces a paired `report-{topic-slug}-{ts}.html` AND `.pdf` (sharing UTC `{ts}`)
- [x] HTML implements light + dark mode with default dark and a persistent toggle
- [x] HTML nav is horizontal-grouped at ≥768px and a burger drawer at <768px
- [x] PDF opens with a clickable TOC linking every section
- [x] PDF uses a high-contrast print theme distinct from the on-screen dark mode
- [x] Headless Chromium binary missing → clear error + install hint, never silent skip
- [x] No "Save as interactive HTML" / "Save as PDF" options remain in the interactive-continuation askQuestion
- [x] Linter passes on both files

## Implementation Notes

### Report Generation section header (command file, place after Adversarial Review)

```markdown
### Report Generation — MANDATORY

Producing a detailed report HTML **and** PDF with rich infographics and visualizations is **mandatory** for every meditation, in both Research and Quick mode. Generate them automatically as part of step 8 of the workflow above — never as an opt-in. A meditation is not considered complete until both files exist in the working directory.
```

### Report filenames subsection (command file)

```markdown
#### Report filenames

Use the meditation's **topic slug** (the same `{topic-slug}` segment used in the working directory `{yyyymmdd}-{topic-slug}/`) plus a UTC timestamp captured at the moment of report generation:

    report-{topic-slug}-{yyyymmddHHMMSS}.html
    report-{topic-slug}-{yyyymmddHHMMSS}.pdf

- `{topic-slug}` MUST exactly match the slug component of the working-directory name (extract it as everything after the first `-` in the basename).
- `{yyyymmddHHMMSS}` is the UTC timestamp at write time (`date -u +%Y%m%d%H%M%S`).
- The HTML and PDF for a single generation share the same timestamp.
- All references in this document, in the agent definition, and in the Branch & Leaf Index match these files via the prefix glob `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf`. Never hard-code `report.html` / `report.pdf`.
```

### Inputs subsection (command file)

```markdown
#### Inputs

1. **Read all meditation files**: Load `consolidation.md`, `facets.md`, `facet-registry.yml` (Research mode), `citations-index.yml` (Research mode), all `branch-*-depth-*-sub-*-*.md` files, and all `branch-*-peer-review-*.md` files (Research mode) from the working directory. The trailing wildcards capture the slug-and-timestamp suffix on every file across depths 1–3 and the peer-review pass. Extract every data point, table, finding, comparison, citation, and insight — the report must reflect the **full** meditation, not just the consolidation summary.
```

### HTML report structural elements (command file)

```markdown
#### HTML report requirements (`report-{topic-slug}-{ts}.html`)

Generate a self-contained single-file webpage in the working directory. **All** of the following are required:

##### Structural elements

- **Responsive top navigation bar** — see the **Responsive Navigation** subsection below
- **Table of Contents** immediately under the hero, with anchor links to every major section. Every section heading carries a stable `id` so the in-page TOC and the PDF bookmarks both resolve. This same TOC drives the PDF index (see PDF requirements below).
- **Hero / executive summary** — title, one-paragraph verdict, and a row of headline stat cards (key numbers extracted from the meditation). The visual identity here is set by the chosen `theming` payload — never use the homogenised default look (see Anti-Homogenization Rules).
- **Per-branch sections** — each branch becomes one or more report sections, in order, with subheadings for depth-2 and depth-3 findings
- **Peer-review section** (Research mode) — cross-branch reinforcements, contradictions, gaps; one card per peer-review file
- **Cross-references** between sections where branches independently converged on the same finding
- **Citations section** at the bottom (mandatory in both modes — sourced from `citations-index.yml` in Research, extracted from inline markers in Quick); see subtask 06 for the full content spec
- **Footer** with meditation slug, timestamp, mode (`research` / `quick`), depth/branch counts, total citation count, and the resolved theming label (e.g. `theme: editorial / warm_palette / serif_headings_sans_body` or `theme: matched-repo (signals: …)`)

(Visualization, infographic, calculator, and other content requirements live in subtasks 06 and 07.)
```

### Anti-Homogenization Rules subsection (command file)

```markdown
##### Anti-Homogenization Rules

AI-generated reports converge on a recognisable homogenised aesthetic. **All of the following defaults are forbidden** unless the user's `theming` payload explicitly invoked them by name. The goal is for every meditation to feel deliberately and visibly different from a "default AI report".

Forbidden defaults (see `assets/image-8bca59a2-5c28-4614-9fe8-98a395c28f57.png` for the canonical example to avoid):

- **Purple-blue gradient hero** (`linear-gradient(135deg, indigo, blue/violet)` and friends).
- **Inter as the headline font weight 700**. Default to a font dictated by the `theming.preset.typography` value or the matched repo signal.
- **Three-card feature grids** as the dominant layout. Vary layout per section (asymmetric grids, single hero panel, two-column with sidebar, full-bleed tables, masonry).
- **Doughnut chart with circular tinted-color legend chips** (the screenshot's signature). Either move the legend, change its shape, or pick a different chart for the same data.
- **Tailwind `indigo-500` (or its variants `#6366f1`, `#818cf8`) as the accent**. Pick a palette from the `theming` payload.
- **Lucide-style icon-in-tinted-circle motif** for stat cards and bullets. Use unboxed iconography, no icons at all, or hand-drawn SVG marks per the chosen direction.
- **Centred body paragraphs** and **gradient "Most popular" pricing pills** as filler. Do not add SaaS-marketing motifs.
- **Five-star testimonial rows** and **DiceBear avatar fallbacks**. There are no users to quote.
- **Smooth modern dark blue UI**, full stop, when no theming choice asked for it.

How to apply this:

1. Before writing any CSS, look at the `theming` payload and pick concrete values (font stack, primary/secondary/accent hex, layout grammar, divider style, link decoration, heading scale).
2. If the chosen direction would naturally produce one of the forbidden patterns, *deliberately substitute* — e.g. an editorial direction may want a serif drop-cap hero instead of a gradient banner; a brutalist direction wants flat blocks and no rounded corners; a terminal_dossier direction wants ASCII-art dividers, not gradient strips.
3. Include a one-line `theme:` annotation in the footer naming the resolved direction, palette, and typography.
```

### Theming application subsection (command file)

```markdown
##### Theming application (driven by the `theming` payload)

The depth-0 subagent receives a `theming` payload from the calling agent. Use it to drive every visual decision:

- `theming.source = match_repo` → load the listed `css_variables_file` / `tailwind_config`, extract the actual font stack, primary/secondary/accent colors, border-radius scale, spacing rhythm; render the report inline-styled to match (do **not** import the repo's CSS — extract the values and inline them).
- `theming.source = preset` → apply the `style_direction` × `color_scheme` × `typography` combination.
- `theming.source = custom` → follow the user's free-text description literally.
- `theming.source = surprise_me` → pick a `style_direction` deterministically seeded by the topic-slug, biased *away* from any direction recently used.
```

### Light + Dark mode subsection (command file)

```markdown
##### Light + Dark mode (mandatory)

- **Both modes are required.** Implement the report so every element renders legibly in both.
- **Default = dark mode** on first load, regardless of system preference.
- **Toggle in the nav** — a clearly visible button (sun/moon icon or text label like "☀ Light / ☾ Dark"). Switches modes immediately, no flicker.
- **Persistence** — store the user's choice in `localStorage` under `meditation-color-mode`; on subsequent loads, honour the stored value before any rendering occurs (set on `<html>` before paint to avoid FOUC).
- **System preference signal** — read `window.matchMedia('(prefers-color-scheme: dark)')` only as a fallback when no localStorage value exists.
- **Contrast** — both modes must achieve WCAG AA on body, AA-Large on headings.
- **Charts** — Chart.js color values must adapt to the active mode. Wire chart options to read CSS custom properties for stroke/fill so a single mode-toggle redraws all charts.
```

### Responsive Navigation subsection (command file)

```markdown
##### Responsive Navigation (mandatory)

- **Wide viewport (`≥768px`)** — horizontal nav across the top of the page. Group the section anchors into logical clusters (e.g. *Overview*, *Branches*, *Peer Review*, *Citations*) with a small visible separator (1px divider or extra spacing). Group labels are recommended for ≥6 anchors.
- **Narrow viewport (`<768px`)** — hide the horizontal nav and replace with a burger button (three horizontal lines, top-right). Tapping the burger opens a slide-in drawer or full-screen overlay containing the same grouped link list, vertically stacked.
- **Implementation** — pure CSS + minimal JS. No external nav library. Use `aria-expanded` / `aria-controls` for accessibility; trap focus inside the drawer while open.
- **Active section** — highlight the currently visible section's nav link as the user scrolls, in both viewport modes.
```

### PDF report requirements subsection (command file)

```markdown
#### PDF report requirements (`report-{topic-slug}-{ts}.pdf`)

The PDF must be **legible and engaging** as a standalone printable artifact. It is not a screenshot of the dark-mode webpage — it is a deliberately-rendered print version with high-contrast text and elements, and a clickable table of contents.

##### Filename pairing

Capture the UTC timestamp **once** at the start of report generation and reuse it for both the HTML and PDF filenames so they pair up:

    TS=$(date -u +%Y%m%d%H%M%S)
    SLUG="{topic-slug}"
    HTML="{workingDir}/report-${SLUG}-${TS}.html"
    PDF="{workingDir}/report-${SLUG}-${TS}.pdf"

##### Print theme — high contrast (mandatory)

The HTML's `@media print` block (and an equivalent `body[data-print-mode="true"]` block toggled by a query parameter for the PDF render — see below) must apply a **high-contrast print theme** distinct from the on-screen dark mode:

- **Background**: pure white (`#fff`) or near-white (`#fafafa`).
- **Body text**: near-black (`#0a0a0a` / `#111`), minimum 11pt.
- **Headings**: `#000` with the chosen theme's display typeface preserved.
- **Links**: dark accent (`#0033aa` or theme-equivalent), underlined.
- **Tables**: black 1px borders, alternating row backgrounds at `#f5f5f5`.
- **Charts**:
  - **Chart.js** — re-rendered with high-contrast palettes, thicker stroke widths (`borderWidth: 2`), labelled data points where space allows.
  - **D3.js** — see subtask 07 for the per-chart `.d3-static-fallback` contract.
- **Infographics**: foreground elements use solid black or theme-dark; backgrounds white. Drop shadows, glows, and partial-opacity tints stripped or strengthened.
- **Interactive calculators**: see subtask 07 for the `.calculator-static-fallback` contract.
- **Hide**: the sticky nav, the colour-mode toggle, the burger button, any hover-only tooltip widget, and any filter / sort UI control on tables (the underlying data stays visible). Citation tooltips become inline footnote markers (`[7]` etc.).
- **Page breaks**: every top-level section starts on a new page (`page-break-before: always`); no orphaned headings or split tables (`page-break-inside: avoid` on tables, charts, and infographic blocks).

By default `pdf_color_mode` in the `theming` payload is `light_high_contrast`. Honour any explicit user override (e.g. dark PDF for an editorial print) but warn that dark PDF is harder to read and consumes more ink.

##### Table of Contents (mandatory)

The PDF must open with a **clickable Table of Contents** as the first content page (after the title page if any). Build it once in the HTML; the same DOM serves both the on-page TOC and the PDF index:

- Place inside `<nav id="toc" aria-label="Table of contents">` immediately under the hero, before the per-branch sections.
- Every section heading (`<h2>` / `<h3>`) carries a stable, kebab-case `id` (e.g. `id="branch-1-{slug}"`, `id="peer-review"`, `id="citations"`).
- Headless Chrome preserves anchor links in the printed PDF natively, so the TOC entries become clickable bookmarks in the PDF reader.
- Two levels deep (top-level sections + branch subheadings); deeper depth-3 leaves are accessible via the in-section navigation.
- Right-aligned page numbers next to each entry are encouraged but optional.
- Add `<style>@media print { #toc { page-break-after: always; } }</style>` so the TOC sits on its own page in the PDF.

##### Render command

Render the PDF from the generated HTML using headless Chrome. Pass `?print=1` so the HTML can switch to its print theme (and TOC layout) deterministically:

    google-chrome --headless --disable-gpu --no-sandbox \
      --print-to-pdf="${PDF}" \
      --print-to-pdf-no-header \
      --no-pdf-header-footer \
      "file://${HTML}?print=1"

The HTML must read `URLSearchParams` on load and apply `data-print-mode="true"` to `<html>` when `print=1` is set, so the print theme and TOC styles are guaranteed to apply during the headless render even outside `@media print`.

Try `chromium` and `chromium-browser` as fallback binaries if `google-chrome` is not installed. If no headless Chromium is available, the meditation **fails** with a clear error: report the missing dependency, list the installation hint for the user's platform (e.g. `brew install --cask google-chrome` on macOS, `apt install chromium` on Debian/Ubuntu), and leave the HTML file in place so the user can manually print to PDF.

##### Final verification

Before returning control to the user, verify exactly one matching pair exists for this meditation and both files are non-empty. The newest matching pair is authoritative if multiple regenerations have occurred:

    HTML_LATEST=$(ls -1t "{workingDir}"/report-"{topic-slug}"-*.html 2>/dev/null | head -n 1)
    PDF_LATEST=$(ls -1t  "{workingDir}"/report-"{topic-slug}"-*.pdf  2>/dev/null | head -n 1)
    [ -s "${HTML_LATEST}" ] && [ -s "${PDF_LATEST}" ]

If either check fails, regenerate the missing artifact before presenting results.
```

### Other styling rules subsection (command file)

```markdown
##### Other styling rules

- All data embedded inline as JavaScript constants — **no external data fetches**, no `fetch()` calls.
- Allowed external resources (CDN script tags only — no runtime data fetches via these libraries):
  - **Chart.js** — `https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js`
  - **D3.js** — `https://d3js.org/d3.v7.min.js` (see subtask 06 for usage and subtask 07 for PDF degradation)
  - **D3 plugins** as needed (`d3-sankey`, `d3-cloud`) loaded from the same official CDNs
  - **Custom fonts** from Google Fonts or `https://rsms.me/` *only if the chosen theme requires a non-system font*; never load a font just because Inter is "the default"
- No other external scripts, stylesheets, or assets — and never use the libraries above to fetch runtime data.

If the meditation is small (e.g. a quick `--quick` run on a narrow topic) and genuinely lacks the breadth for the content minimums (subtask 06), you must still produce **all** mandatory structural elements; substitute additional comparison matrices, scorecards, or hierarchy diagrams to compensate so the report is never sparse.
```

### Subagent step 12 (agent file — generate report)

```markdown
12. **Generate the mandatory report (HTML + PDF)**: Producing the report HTML and PDF is **non-negotiable**. Only run this step after step 10 returns a passing verdict; if the review escalated to `ESCALATE`, **skip this step**, surface the unresolved findings to the calling agent. Follow the **Report Generation — MANDATORY** section in `.cursor/commands/crux-meditate.md` to the letter; that document is the source of truth. Summary of obligations:
   - Read all meditation files (consolidation, facets, registry, citations-index, all branch files, all peer-review files).
   - Capture a single UTC timestamp at the start of report generation (`TS=$(date -u +%Y%m%d%H%M%S)`) and use it for both filenames.
   - Apply the `theming` payload to drive every visual decision. Never default to the homogenised AI look.
   - Write a self-contained `report-{topic-slug}-{ts}.html` with: responsive nav, in-page TOC, hero/exec summary, per-branch sections, peer-review section, cross-references, citations section, footer with `theme:` annotation, **light AND dark mode** with default dark and persistent toggle, high-contrast `@media print` and `data-print-mode="true"` styles for PDF rendering, all data inline. (Chart counts, infographic counts, calculator requirements, and graceful-degradation contracts are documented in subtasks 06 and 07.)
   - Render the PDF from the HTML via headless Chrome with `?print=1`. Fall back to chromium/chromium-browser. Abort on missing binary with install hint.
   - Verify the latest matching pair exists and both files are non-empty using globs.
   - **Re-run step 9** to refresh the Branch & Leaf Index links so the `report-*` filenames in `facets.md` match the latest on-disk pair.
```

### Calling agent steps 9–12 (command file)

```markdown
**Steps 9–12: Performed by you (the calling agent)**

9. **Verify the mandatory report artifacts**: The depth-0 subagent is required to produce a paired `report-{topic-slug}-{ts}.html` AND `report-{topic-slug}-{ts}.pdf` in the working directory before returning. Verify the latest matching pair exists and both files are non-empty using `ls -1t ... | head -n 1` plus `[ -s ... ]`. If either is missing or empty, generate it yourself per the Report Generation section. If the PDF specifically is missing because no headless Chromium is available, surface the error and the platform-specific install hint prominently in step 10.

10. **Present to user**: Display the consolidated insights organized by branch, highlighting cross-branch connections, peer-review findings, and emergent themes. **Always include the absolute paths to `facets.md`, the latest `report-{topic-slug}-{ts}.html`, and the latest `report-{topic-slug}-{ts}.pdf`** so the user can open them immediately.

11. **Interactive continuation**: Use `askQuestion` with multi-select options:
    - Discovered tangent directions (derived from the exploration) as expansion options
    - "Save meditation as draft spec" — write insights as a draft spec outline to `specs/`
    - "End meditation" — complete the session

    Do **not** offer "Save as HTML" or "Save as PDF" — both are already produced as part of every meditation.

12. If the user selects expansion directions, **first run the shortened Cost & Scope re-acknowledgment** per subtask 03's rules. If they proceed, augment context and repeat from step 2 (spawning a new subagent — which will produce its own mandatory facet-confirmation, adversarial review cycle, and report pair). The new meditation **always** re-runs the depth-0 facet confirmation; the previous `confirmDeepFacets` value is reused by default. If "Save spec", write a draft spec file. If "End", finish.
```

### One new design principle (agent file)

```markdown
- **Mandatory report artifacts (both modes)**: Every meditation must end with a non-empty paired `report-{topic-slug}-{ts}.html` AND `report-{topic-slug}-{ts}.pdf` in the working directory (sharing the same UTC `{ts}`). The depth-0 manager owns this step; it is not optional, not user-selectable, and not deferred to the calling agent. If the headless Chromium binary required for the PDF render is missing, the meditation aborts with a clear, actionable error rather than silently skipping the PDF.
- **Light + dark mode in HTML, high-contrast in PDF (both modes)**: The HTML implements both color modes with a persistent toggle, defaulting to dark; the PDF renders with a high-contrast print theme (near-black on near-white) and a clickable Table of Contents at the start linking every section.
```

(Subtask 06 will add another design principle; subtask 07 will add yet another.)

## Testing Strategy

- After applying, simulate a full meditation that completes successfully: confirm the HTML opens in dark mode by default, the toggle persists via localStorage, the nav is horizontal at ≥768px and burgered at <768px, the PDF opens with a clickable TOC and uses light high-contrast theme.
- Confirm the calling agent's interactive-continuation askQuestion no longer offers "Save HTML" / "Save PDF".
- Confirm a deliberate Chromium-missing scenario produces a clear error with install hint.
- Run the linter on both files.

## Execution Notes

### Agent Session Info
- Agent: crux-platform-architect
- Started: 20260516
- Completed: 20260516

### Work Log
- Replaced the legacy `### Report Generation` section in `.cursor/commands/crux-meditate.md` (formerly a 4-step opt-in flow gated on user selection of "Save as HTML" / "Save as PDF") with the new `### Report Generation — MANDATORY` section containing: intro + non-negotiable framing, **Report filenames** subsection (UTC timestamp pairing + Never hard-code rule), **Inputs**, **HTML report requirements → Structural elements**, **Anti-Homogenization Rules** (9 forbidden defaults with canonical screenshot reference and how-to-apply guidance), **Theming application** (driven by `theming.source` enum), **Light + Dark mode** (default dark, localStorage persistence, WCAG AA contrast, chart-color binding), **Responsive Navigation** (≥768px horizontal grouped / <768px burger drawer with `aria-expanded` / `aria-controls` and focus trap), **PDF report requirements → Filename pairing**, **Print theme — high contrast**, **Table of Contents** (clickable, page-break-after on TOC), **Render command** (headless Chrome with `?print=1` + chromium-binary fallback chain + abort-on-missing-Chromium error with platform install hints), **Final verification**, and **Other styling rules** (CDN allowlist).
- Updated the calling-agent block in `.cursor/commands/crux-meditate.md` from the previous 4 steps (Present → Interactive continuation [with Save HTML/PDF options] → Handle save/end selection → Handle expansion selection) to a new 4-step shape: **step 9 Verify report artifacts** (new), **step 10 Present** (always includes the absolute paths to `facets.md` + latest HTML/PDF pair), **step 11 Interactive continuation** (multi-select reduced to expansion directions + `save_spec` + `end_meditation`, with mandatory decision-guidance context in the prompt body), **step 12 Handle the user's selection** (combines former 11+12: expansion + save-spec + end, with the shortened Cost & Scope re-acknowledgment for expansion).
- Updated subagent **step 12** in `.cursor/agents/crux-cursor-memory-manager.md` from the subtask-04 placeholder into the fully-documented non-negotiable mandatory-report obligation: references the command file's Report Generation section as source of truth, lists the obligations summary (read all files / capture single UTC TS / apply theming / write HTML with all required structural+behaviour elements / render PDF via headless Chrome with `?print=1` + chromium fallback + abort-on-missing-binary / final pair verification / re-run step 9 to refresh Branch & Leaf Index links). Updated Quick-mode step 12 note (line 448) and the post-subagent informational flow (lines 451-456) to reflect the new four-step calling-agent shape. Updated the Step-numbering note to record subtask 05's completion.
- Updated the sub-step 8 references in both Research-mode and Quick-mode workflow blocks of `.cursor/commands/crux-meditate.md` so they point to the newly-canonical Report Generation section instead of describing the placeholder.
- Added two new design principles at the end of the **Design principles** list in the agent file: **Mandatory report artifacts (both modes)** (non-negotiable per-meditation paired HTML+PDF, abort-on-missing-Chromium with install hints, legacy opt-in options removed, full contract in command file) and **Light + dark mode in HTML, high-contrast in PDF (both modes)** (default dark with persistent toggle, FOUC-safe, WCAG AA, print theme distinct from on-screen dark, clickable TOC as first PDF content page, responsive nav with accessibility attributes hidden in PDF).
- Updated both Coordination Conventions "Never hard-code these names" self-references (command file line 403; agent file line 353) so the self-reference correctly acknowledges the new mirror in the Report filenames subsection — the `report.html` / `report.pdf` deprecated literals now appear in three carefully-scoped places (two in the command file, one in the agent file), each of which is the canonical "Never hard-code" rule itself.

### Blockers Encountered
None. The cross-cutting decision-guidance requirement was satisfied by adding rich `context` text inside the calling-agent step 11 `AskQuestion` prompt body so the user understands the cost/trade-off of each option (expansion direction vs save-spec vs end).

### Files Modified
- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`
