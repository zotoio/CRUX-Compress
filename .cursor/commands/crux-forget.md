# crux-forget

Remove memories from the CRUX memory corpus.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-forget <memory-id>           - Forget a specific memory by its short hash ID
/crux-forget <slug>                - Forget a memory by slug
/crux-forget <file-path>           - Forget a memory by file path
/crux-forget "search query"        - Search memories and select which to forget
/crux-forget                       - List all memories for selection
```

## Instructions

When this command is invoked, spawn a `crux-cursor-memory-manager` subagent to handle the forget workflow. The manager uses `crux-skill-memory-crud` to perform the deletion and `crux-skill-memory-index` to rebuild the index afterwards.

### Argument Handling

- **Memory ID(s)** (7-char hex hash, e.g. `a1b2c3d`): Resolve to memory files by scanning the memory index or searching memory directories. Show matched memory details and confirm before deletion. Pass `$ARGUMENTS` to the subagent as the memory ID(s).
- **Slug(s)** (e.g. `validate-checksums-before-overwrite`): Resolve to memory file(s) by searching `memories/` recursively for `{slug}.memory.md` or `{slug}.memory.crux.md`. Show matched memory details and confirm. Pass `$ARGUMENTS` to the subagent as the slug(s).
- **File path(s)** (e.g. `memories/learning/foo.memory.md`): Read the specified file(s) directly. Show details and confirm. Pass `$ARGUMENTS` to the subagent as the file path(s).
- **Quoted text** (e.g. `"performance optimization"`): Search memories by title, description, tags, and body content. Present matches ranked by relevance and let the user select which to forget. Pass `$ARGUMENTS` to the subagent as the search query.
- **No arguments**: Load the memory index (`.crux/memory-index.yml`), display all memories in a selectable list, and let the user pick which to forget.

### What Happens

1. The manager reads `.crux/crux-memories.json` to load configuration
2. Based on the invocation mode, resolves the input to one or more memory files
3. Displays matched memories with their `id`, title, type, and strength for review
4. **Always confirms before deletion** — this operation is destructive and irreversible
5. For each confirmed memory, deletes via `crux-skill-memory-crud` Delete operation:
   - Removes the memory file (`.memory.md` or `.memory.crux.md`)
   - Removes the corresponding reference tracker (`{trackingDir}/{slug}.refs.yml`) if it exists
6. Rebuilds the memory index via `crux-skill-memory-index`
7. Reports what was deleted: count, types, and IDs of removed memories

## Related

- `crux-cursor-memory-manager` agent — The specialist that manages the memory lifecycle
- `crux-skill-memory-crud` skill — Delete operation that handles memory file and tracker removal
- `/crux-dream` — Extract and create memories from completed work
- `/crux-recall` — View and query memories
- `/crux-remember` — Create ad-hoc memories outside of spec workflows
- `/crux-meditate` — Recursive memory-informed exploration
