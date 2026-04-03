# crux-mindreader

Decompress, query, and display CRUX memories in human-readable form.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-mindreader                                    - Show contextually relevant memories
/crux-mindreader "search query"                     - Search memories by keyword
/crux-mindreader 20260403-crux-memories              - Show memories from a specific plan
/crux-mindreader memories/core/some-memory.memory.md - Display a specific memory file
```

## Instructions

When this command is invoked, spawn a `crux-cursor-memory-manager` subagent in MindReader mode to query and display memories. MindReader is **read-only** — it never modifies memory files on disk.

### Argument Handling

- **No arguments**: The manager loads the memory index (`.crux/memory-index.yml`) and surfaces memories most likely to be relevant to the current conversation context. For each memory, it shows title, type, strength, reference count, and a brief rationale for why it was surfaced.
- **Quoted text** (e.g. `"performance optimization"`): The manager searches existing memories by title, description, tags, and body content. Results are ranked by relevance with decompressed body content shown for compressed memories. Pass `$ARGUMENTS` to the subagent as the search query.
- **Plan name(s)** (e.g. `20260403-crux-memories`): The manager finds all memories whose `source` field matches the given plan slug(s). Results are grouped by type. Pass `$ARGUMENTS` to the subagent as the plan name(s).
- **File path(s)** (e.g. `memories/learning/foo.memory.md`): The manager reads the specified memory file(s) directly. Compressed files (`.memory.crux.md`) are decompressed for display. Full frontmatter and body are shown. Pass `$ARGUMENTS` to the subagent as the file path(s).

### What Happens

1. The manager reads `.crux/crux-memories.json` to load configuration
2. Based on the invocation mode, it either:
   - Loads the memory index and selects relevant entries
   - Searches memory files for keyword matches
   - Filters memories by source plan slug
   - Reads specific memory files directly
3. For compressed memories (`.memory.crux.md`), decompresses the CRUX body to terse natural language for display — without modifying the file on disk
4. Presents results with frontmatter metadata and readable body content

### Display Format

Each displayed memory includes:

```
─── [{type}] {title} ───
Strength: {strength} | References: {references} | Source: {source}
Tags: {tags}
Created: {created} | Modified: {modified}

{body content — decompressed if needed}
```

## Related

- `crux-cursor-memory-manager` agent — The specialist that manages the memory lifecycle
- `crux-skill-memory-compress` skill — Decompression logic for compressed memories
- `crux-skill-memory-index` skill — Memory index used for discovery
- `/crux-dream` — Extract and create memories from completed work
