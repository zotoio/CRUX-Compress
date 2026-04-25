# crux-amnesia

Temporarily disable or restore ambient CRUX memory usage for the current chat session.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-amnesia           - Toggle amnesia mode for this chat session
/crux-amnesia on        - Disable ambient memory usage for this chat session
/crux-amnesia off       - Restore normal config-driven memory behavior
/crux-amnesia status    - Show the current session memory mode
```

## Instructions

This command manages a **session-scoped override** only. It must **never** edit `.crux/crux-memories.json`, memory files, trackers, or the memory index.

### Argument Handling

- **No arguments**: Toggle the current chat session between:
  - **Amnesia ON** — suppress ambient memory usage for normal work
  - **Amnesia OFF** — return to normal behavior governed by `.crux/crux-memories.json`
- **`on`**: Enable amnesia mode for the current chat session.
- **`off`**: Disable amnesia mode and return to config-driven behavior.
- **`status`**: Report whether the current chat session is in amnesia mode or following the repo config.

### What Amnesia ON Means

When amnesia mode is active for this chat session:

1. Do **not** discover memories from `.crux/memory-index.yml`
2. Do **not** load memory files automatically
3. Do **not** annotate output with `[memory:{title}]`
4. Do **not** increment memory reference tracking
5. Do **not** suggest `/crux-dream` automatically after ordinary work
6. When spawning subagents for ordinary work, explicitly tell them that CRUX memories are disabled for this chat session and they must not use them

This override applies only to **ambient memory usage during ordinary work**. If the user explicitly invokes a memory command such as `/crux-dream`, `/crux-recall`, `/crux-forget`, `/crux-remember`, or `/crux-meditate`, treat that as direct user intent to interact with the memory system.

### What Amnesia OFF Means

- Return to the repository's normal behavior
- Respect `.crux/crux-memories.json` again
- If `enableMemories` is `"false"` in config, memories remain disabled even after amnesia is turned off

### Response Format

Respond with a short status confirmation:

- **Session memory mode**: `amnesia-on` or `config-driven`
- **Scope**: current chat session only
- **Subagents**: inherit the same session memory mode unless the user explicitly invokes a memory-management command
- **Repo config**: unchanged (`.crux/crux-memories.json` was not modified)

## Related

- `/crux-dream` — Extract or rebalance memories intentionally
- `/crux-recall` — Inspect memories intentionally
- `/crux-forget` — Remove memories intentionally
- `/crux-remember` — Create ad-hoc memories intentionally
- `/crux-meditate` — Recursive memory-informed exploration
