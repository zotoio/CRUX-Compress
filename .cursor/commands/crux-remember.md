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

This command primarily uses **Pattern A (pre-collect then spawn)** — the user's choices (type, tags, description) are known upfront. The **parent agent** (you) collects all input via `AskQuestion` FIRST, then spawns a `crux-cursor-memory-manager` subagent with the pre-collected answers. The subagent never calls `AskQuestion` directly. If the subagent encounters an unexpected decision during creation (e.g. conflict, size limit), it falls back to **Pattern B** and returns `needs_user_input`.

### Argument Handling

- **No arguments**: Prompt the user for the memory content/insight they want to save.
- **Quoted text** (e.g. `"always validate checksums before overwrite"`): Use as the memory title/body. Pass `$ARGUMENTS` to the subagent.
- **`--type <type>`**: If provided, skip the type selection prompt and use the specified type directly.

### What Happens

**Phase 1 — Parent collects user input (before spawning subagent)**:

1. If no text was provided, ask the user what they want to remember
2. Use the `AskQuestion` tool to ask the user to select the memory type. Present options from the `typeTransitions` keys in config: `idea`, `learning`, `redflag`, `core`, `goal`. If `--type` was provided, skip this step.
3. Use the `AskQuestion` tool to ask the user for optional tags (comma-separated) and a brief description. Suggest relevant tags based on the memory content and current context.

**Phase 2 — Spawn subagent with all answers**:

4. Spawn a `crux-cursor-memory-manager` subagent in Remember mode, passing ALL collected answers in the task prompt:
   - The memory content/insight text
   - The selected type
   - The user's tags
   - The user's description
   - `source: "adhoc"`
5. The subagent creates the memory via `crux-skill-memory-crud` and rebuilds the index via `crux-skill-memory-index`
6. Display the subagent's confirmation to the user — the memory's short hash ID, title, type, and file path

**If the subagent returns `needs_user_input`**: Use `AskQuestion` to collect the requested information, then resume the subagent with the answers.

## Related

- `crux-cursor-memory-manager` agent — The specialist that manages the memory lifecycle
- `crux-skill-memory-crud` skill — Create operation that handles memory file creation
- `crux-skill-memory-index` skill — Rebuilds the prioritised memory index
- `/crux-dream` — Extract and create memories from completed work
- `/crux-recall` — View and query memories
- `/crux-forget` — Remove memories from the corpus
- `/crux-meditate` — Recursive memory-informed exploration
