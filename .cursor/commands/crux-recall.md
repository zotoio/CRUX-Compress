# crux-recall

Decompress, query, and display CRUX memories in human-readable form.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-recall                                    - Show contextually relevant memories
/crux-recall "search query"                     - Search memories by keyword
/crux-recall 20260403-crux-memories              - Show memories from a specific spec
/crux-recall memories/core/some-memory.memory.md - Display a specific memory file
/crux-recall --total                             - Visualize the entire memory system as an interactive canvas
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `--total` | Generate an interactive canvas visualization of the entire memory system using only `cursor/canvas` SDK primitives. The canvas includes: summary stats, type/search filters, an SVG force-directed graph (2D, pre-computed at module scope via Verlet simulation), a detail panel for selected memories, type/strength distribution charts (`PieChart`/`BarChart`), and a filterable memory table. Nodes represent memories (sized by strength, colored by type, labeled by title). Edges connect memories sharing tags or source specs. Supports click-to-detail, hover highlighting, type filter toggles, and text search. |

## Instructions

When this command is invoked, spawn a `crux-cursor-memory-manager` subagent in Recall mode to query and display memories. Recall is **read-only** — it never modifies memory files on disk.

### Argument Handling

- **No arguments**: The manager loads the memory index (`.crux/memory-index.yml`) and surfaces memories most likely to be relevant to the current conversation context. For each memory, it shows title, type, strength, reference count, and a brief rationale for why it was surfaced.
- **Quoted text** (e.g. `"performance optimization"`): The manager searches existing memories by title, description, tags, and body content. Results are ranked by relevance with decompressed body content shown for compressed memories. Pass `$ARGUMENTS` to the subagent as the search query.
- **Spec name(s)** (e.g. `20260403-crux-memories`): The manager finds all memories whose `source` field matches the given spec slug(s). Results are grouped by type. Pass `$ARGUMENTS` to the subagent as the spec name(s).
- **File path(s)** (e.g. `memories/learning/foo.memory.md`): The manager reads the specified memory file(s) directly. Compressed files (`.memory.crux.md`) are decompressed for display. Full frontmatter and body are shown. Pass `$ARGUMENTS` to the subagent as the file path(s).
- **`--total`**: The manager gathers the complete memory corpus — index metadata, all memory files, and their relationships — then uses `/canvas` to generate an interactive visualization of the entire memory system using only `cursor/canvas` SDK components and inline SVG. No table or text output is produced; the canvas is the deliverable.

### What Happens

1. The manager reads `.crux/crux-memories.json` to load configuration
2. Based on the invocation mode, it either:
   - Loads the memory index and selects relevant entries
   - Searches memory files for keyword matches
   - Filters memories by source spec slug
   - Reads specific memory files directly
   - (`--total`) Reads the full memory index and all memory files, builds a relationship graph, and generates a canvas visualization using `cursor/canvas` SDK primitives and inline SVG
3. For compressed memories (`.memory.crux.md`), decompresses the CRUX body to terse natural language for display — without modifying the file on disk
4. Presents results with frontmatter metadata and readable body content (or as an interactive canvas when `--total` is used)

### Display Format

Render memories as a markdown table grouped by type. Each row shows the memory's short hash `id` for easy reference.

**Table format** (one table per type group):

```markdown
### {Type} Memories

| ID | Title | Str | Refs | Source | Tags |
|----|-------|-----|------|--------|------|
| `{id}` | {title} | {strength} | {references} | {source} | {tags as comma-separated} |
```

After the table(s), show a **Details** section with each memory's body content (decompressed if needed), prefixed by its hash:

```markdown
#### `{id}` — {title}

{body content — decompressed if needed}
```

### Post-Display: Next Steps Menu

After displaying the Recall results, use the `AskQuestion` tool with a single multi-select question offering these actions:

| Option | Label | What it does |
|--------|-------|-------------|
| `delete` | Delete memories | Let the user pick which memories to remove from the corpus |
| `consolidate` | Consolidate memories | Automatically find optimal combinations, merge near-duplicates, and compress the result |
| `promote` | Promote (boost) memories | Increase strength of selected memories |
| `skip` | No thanks | Do nothing — end the interaction |

If the user selects one or more actions, execute them in order:

1. **Delete**: Present a follow-up `AskQuestion` listing each memory by its `id` and title as a multi-select. Delete selected memories using `crux-skill-memory-crud` Delete, then rebuild the index via `crux-skill-memory-index`.
2. **Consolidate**: Spawn a `crux-cursor-memory-manager` subagent in REM Sleep mode scoped to the displayed memories. The subagent identifies near-duplicates, merges them, and compresses if `enableMemoryCompression` is active. Present the consolidation report to the user.
3. **Promote**: Present a follow-up `AskQuestion` listing each memory by its `id` and title as a multi-select. For selected memories, increment strength by 1 via `crux-skill-memory-crud` Update, then rebuild the index.
4. **Skip**: End the interaction with no further action.

## Related

- `crux-cursor-memory-manager` agent — The specialist that manages the memory lifecycle
- `crux-skill-memory-compress` skill — Decompression logic for compressed memories
- `crux-skill-memory-index` skill — Memory index used for discovery
- `/crux-dream` — Extract and create memories from completed work
- `/crux-forget` — Remove memories from the corpus
- `/crux-remember` — Create ad-hoc memories outside of spec workflows
- `/crux-meditate` — Recursive memory-informed exploration
