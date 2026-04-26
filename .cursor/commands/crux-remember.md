# crux-remember

Store ad-hoc memories outside of spec workflows. These memories participate in standard consolidation during REM sleep.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-remember                              - Interactively create a new memory
/crux-remember "insight text"               - Create a memory from the provided text
/crux-remember "insight" --type learning    - Create with pre-specified type
```

## Instructions

When this command is invoked, spawn a `crux-cursor-memory-manager` subagent in Remember mode. The manager uses `crux-skill-memory-crud` to create the memory and `crux-skill-memory-index` to rebuild the index afterwards.

### Argument Handling

- **No arguments**: Prompt the user for the memory content/insight they want to save.
- **Quoted text** (e.g. `"always validate checksums before overwrite"`): Use as the memory title/body. Pass `$ARGUMENTS` to the subagent.
- **`--type <type>`**: If provided, skip the type selection prompt and use the specified type directly.

### What Happens

1. The manager reads `.crux/crux-memories.json` to load configuration (check `enableMemories` flag)
2. Parses the input — if no text provided, asks the user what they want to remember
3. Uses the `AskQuestion` tool to ask the user to select the memory type. Present options from the `typeTransitions` keys in config: `idea`, `learning`, `redflag`, `core`, `goal`. If `--type` was provided, skip this step.
4. Asks the user for optional tags (comma-separated) and a brief description. Suggest relevant tags based on the memory content and current context.
5. Delegates to `crux-skill-memory-crud` Create operation with:
   - `title`: the user's insight text (concise)
   - `description`: brief summary of the memory
   - `type`: selected type
   - `tags`: user-provided tags
   - `source`: `"adhoc"` to distinguish from spec-extracted memories
   - `strength`: 1 (default for new memories)
   - Body: the full memory content
6. Rebuilds the memory index via `crux-skill-memory-index`
7. Confirms to the user with the memory's short hash ID, title, type, and file path

## Related

- `crux-cursor-memory-manager` agent — The specialist that manages the memory lifecycle
- `crux-skill-memory-crud` skill — Create operation that handles memory file creation
- `crux-skill-memory-index` skill — Rebuilds the prioritised memory index
- `/crux-dream` — Extract and create memories from completed work
- `/crux-recall` — View and query memories
- `/crux-forget` — Remove memories from the corpus
- `/crux-meditate` — Recursive memory-informed exploration
