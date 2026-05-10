# crux-meditate

Recursive memory-informed exploration of themes, topics, and intent through 3-level deep agent inception.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-meditate                          - Explore facets derived from current chat context
/crux-meditate "topic or question"      - Explore a specific theme
/crux-meditate @file.ts @folder/        - Explore facets around referenced code
```

## Instructions

When this command is invoked, spawn a `crux-cursor-memory-manager` subagent in Meditate mode. The manager orchestrates a 3-level recursive exploration by spawning child instances of itself, each querying memories, expanding on discoveries, and writing consolidated insights to markdown files in a shared working directory.

**Critical**: All agents coordinate through markdown files in `.ai-ignored/meditations/{yyyymmdd}-{topic-slug}/`, not through in-context return values or JSONL transcript polling. The subagent performs steps 1–6 and writes `consolidation.md` to the working directory. You then read that file and handle steps 7–9 directly with the user.

### Argument Handling

- **No arguments**: The manager examines the current chat context — conversation history, open files, recent activity — to derive three exploration facets (theme, topic, intent). Pass `$ARGUMENTS` to the subagent.
- **Quoted text** (e.g. `"how should we handle caching"`): Use the provided text as the seed topic. The manager derives three facets from it. Pass `$ARGUMENTS` to the subagent.
- **File/folder references** (e.g. `@src/auth/ @config.ts`): The manager examines the referenced code to derive facets around its architecture, patterns, and purpose. Pass `$ARGUMENTS` to the subagent.
- **Mixed input**: Any combination of text, files, folders, images, or past chat references. The manager synthesizes all inputs to derive facets.

### What Happens

**Steps 1–6: Performed by the subagent tree (file-based coordination)**

1. The manager reads `.crux/crux-memories.json` to load configuration (check `enableMemories` flag).
2. **Create working directory**: `.ai-ignored/meditations/{yyyymmdd}-{topic-slug}/`. This is the shared coordination space for all agents in the tree.
3. **Derive facets**: From the input (or chat context if no args), identify three distinct, non-overlapping exploration facets — e.g. theme, topic, and intent. Each facet must be independently explorable and complementary to the others. Write `facets.md` to the working directory with the facets and an explanation of how they partition the topic. Each facet becomes a branch's top-level subfocus.
4. **Spawn Level 1**: Launch 3 background `crux-cursor-memory-manager` subagents in Meditate mode, one per facet, each with `meditateDepth: 1`, `maxDepth: 3`, `branchNumber: 1|2|3`, `workingDir`, and `siblingFacets` (the other two branches' descriptions, so each branch avoids drifting into a sibling's territory). All three run in parallel.
5. **Recursive exploration** (each agent at depth 1 and 2) — each agent receives a distinct **subfocus** that is narrower than its parent's:
   a. Query memories relevant to its assigned subfocus using the memory index and search
   b. Expand on the subfocus in light of discovered memories — draw connections, identify patterns, surface non-obvious relationships
   c. Derive **3 distinct child subfocuses** — the three most promising narrower threads within this agent's subfocus (each must be strictly narrower, non-overlapping with each other and with sibling branches)
   d. Spawn **3 child** `crux-cursor-memory-manager` agents at `depth + 1`, one per child subfocus, with same `workingDir` and `branchNumber` plus a `subfocusIndex` (1, 2, 3). All 3 run in parallel.
   e. **Poll for all 3 child output files** (e.g. `branch-{N}-depth-{D}-sub-{1,2,3}.md`) by checking file existence with `ls` at short intervals — never read JSONL transcripts
   f. Read all child output files, aggregate with own expansion, write aggregated result to own output file (`branch-{N}.md` for depth-1, `branch-{N}-depth-2-sub-{S}.md` for depth-2)
6. **Level 3** (deepest): Performs steps a–b only — no further recursion. Writes insights to `branch-{N}-depth-3-sub-{S}.md`.
7. **Consolidation**: Level 0 polls for `branch-1.md`, `branch-2.md`, and `branch-3.md`. When all exist, reads them and synthesizes a cohesive summary. Writes `consolidation.md` to the working directory and returns the consolidation text to the calling agent.

**Steps 8–10: Performed by you (the calling agent)**

8. **Present to user**: Read `consolidation.md` from the working directory (or use the returned text). Display the consolidated insights organized by branch, highlighting cross-branch connections and emergent themes.
9. **Interactive continuation**: Use `AskQuestion` with multi-select options:
   - Discovered tangent directions (derived from the exploration) as expansion options
   - "Save meditation as draft spec" — write insights as a draft spec outline to `specs/`
   - "Save as interactive HTML report" — synthesize all meditation outputs into a comprehensive self-contained webpage (see Report Generation below)
   - "Save as PDF report" — generate the HTML report and also render it as a PDF
   - "End meditation" — complete the session
10. If the user selects expansion directions, augment context with the new directions and user input, then repeat from step 2 (spawning a new subagent with the expanded context and a new working directory). If "Save spec", write a draft spec file. If "Save HTML" or "Save PDF", generate the report (see below). If "End", finish.

### Report Generation

When the user selects "Save as interactive HTML report" or "Save as PDF report":

1. **Read all meditation files**: Load `consolidation.md`, `facets.md`, all `branch-*.md` files, and all `branch-*-depth-*-sub-*.md` files from the working directory. Extract every data point, table, finding, comparison, and insight.

2. **Generate `report.html`** in the working directory — a self-contained single-file webpage with:
   - **Sticky top navigation bar** with section anchor links
   - **Executive summary** with key stats, verdict, and cross-branch themes
   - **All data organized into logical sections** derived from the meditation branches (each branch becomes one or more report sections)
   - **Interactive Chart.js visualizations** (loaded from CDN) — bar charts, radar charts, doughnut charts, line charts for any quantitative data discovered (comparisons, timelines, distributions, risk profiles)
   - **Comprehensive data tables** for all tabular findings
   - **Interactive calculators** relevant to the topic (with JavaScript, input fields, and computed results) — infer what calculations would be useful from the meditation content
   - **Cross-references** between sections where branches independently converged on the same finding
   - **Risk/priority indicators** with color-coded badges and visual meters where appropriate
   - **Timeline visualization** for any chronological events or milestones discovered
   - **References section** listing all data sources mentioned across the meditation
   - **Dark theme** with modern styling, responsive grid layout, and print-friendly CSS media queries
   - All data embedded inline as JavaScript constants — no external data fetches

3. **If PDF requested**: Run `google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="{workingDir}/report.pdf" --print-to-pdf-no-header "file://{workingDir}/report.html"` to render the HTML as a PDF. If Chrome is unavailable, inform the user they can open the HTML in a browser and print to PDF.

4. **Report the file paths** to the user and note they can open the HTML in a browser for interactive features.

## Related

- `crux-cursor-memory-manager` agent — The specialist that orchestrates the recursive meditation
- `crux-skill-memory-index` skill — Memory index used for facet-relevant memory discovery
- `crux-skill-memory-crud` skill — Read operations for loading memory content during exploration
- `/crux-dream` — Extract and create memories from completed work
- `/crux-recall` — View and query memories
- `/crux-remember` — Create ad-hoc memories outside of spec workflows
- `/crux-forget` — Remove memories from the corpus
