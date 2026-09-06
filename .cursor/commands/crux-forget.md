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

This command uses **Pattern B (work first, then escalate)**. The subagent NEVER calls `AskQuestion` directly — the parent agent resolves the input to matches, confirms deletion with the user via `AskQuestion`, then resumes the subagent with the confirmed list. For the full Pattern A / Pattern B contract and the `needs_user_input` YAML schema, see `.cursor/skills/_memory-shared.md#user-input-escalation` and `AGENTS.md`.

### Argument Handling

- **Memory ID(s)** (7-char hex hash, e.g. `a1b2c3d`): Pass `$ARGUMENTS` to the subagent to resolve.
- **Slug(s)** (e.g. `validate-checksums-before-overwrite`): Pass `$ARGUMENTS` to the subagent to resolve.
- **File path(s)** (e.g. `memories/learning/foo.memory.md`): Pass `$ARGUMENTS` to the subagent to resolve.
- **Quoted text** (e.g. `"performance optimization"`): Pass `$ARGUMENTS` to the subagent as a search query.
- **No arguments**: The subagent loads the memory index and returns all memories for selection.

### What Happens

**Phase 1 — Subagent resolves matches**:

1. Spawn a `crux-memory-forget` subagent, passing `$ARGUMENTS`
2. The subagent resolves the input to matching memory files and returns them with ID, title, type, strength, and file path
3. If the subagent returns `needs_user_input` with the resolved matches, proceed to Phase 2

**Phase 2 — Parent confirms deletion with user**:

4. Display matched memories to the user with their details
5. Use the `AskQuestion` tool to confirm which memories to delete — present each memory as a multi-select option. **Always confirm before deletion** — this operation is destructive and irreversible.

**Phase 3 — Resume subagent with confirmed list**:

6. Resume the subagent with the list of confirmed memory IDs/paths to delete
7. The subagent deletes each confirmed memory via `crux-skill-memory-crud` Delete operation:
   - Removes the memory file (`.memory.md` or `.memory.crux.md`)
   - Removes the corresponding reference tracker (`{trackingDir}/{slug}.refs.yml`) if it exists
8. The subagent rebuilds the memory index via `crux-skill-memory-index`
9. Display the subagent's report: count, types, and IDs of removed memories

## Related

See `.cursor/skills/_memory-shared.md#related-commands--skills` for the full
registry of memory commands and skills.
