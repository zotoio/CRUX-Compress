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

This command primarily uses **Pattern A (pre-collect then spawn)** — the parent agent collects the user's choices (type, tags, description) via `AskQuestion` FIRST, then spawns a `crux-memory-remember` subagent with the pre-collected answers. If creation surfaces an unexpected decision (e.g. conflict, size limit), the subagent falls back to **Pattern B** and returns `needs_user_input`. The subagent NEVER calls `AskQuestion` directly. For the full Pattern A / Pattern B contract and the `needs_user_input` YAML schema, see `.cursor/skills/_memory-shared.md#user-input-escalation` and `AGENTS.md`.

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

4. Spawn a `crux-memory-remember` subagent, passing ALL collected answers in the task prompt:
   - The memory content/insight text
   - The selected type
   - The user's tags
   - The user's description
   - `source: "adhoc"`
5. The subagent creates the memory via `crux-skill-memory-crud` and rebuilds the index via `crux-skill-memory-index`
6. Display the subagent's confirmation to the user — the memory's short hash ID, title, type, and file path

**If the subagent returns `needs_user_input`**: Use `AskQuestion` to collect the requested information, then resume the subagent with the answers.

## Related

See `.cursor/skills/_memory-shared.md#related-commands--skills` for the full
registry of memory commands and skills.
