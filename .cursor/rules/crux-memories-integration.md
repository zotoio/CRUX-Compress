---
alwaysApply: true
description: "CRUX Memories integration rule"
crux: true
---

# CRUX Memories Integration Rule

This rule governs how agents interact with the CRUX Memories system. Behavior is controlled by the `enableMemories` flag in `.crux/crux-memories.json`.

## When Memories Are Enabled (`enableMemories: "true"`)

### Discovery

- Agents MUST discover memories by reading `.crux/memory-index.yml`
- Load full memory files only for likely matches (by title, description, or tags)
- If MCP is configured, agents may use semantic search instead of index scanning

### Output Annotation

- Agents annotate output with `[memory:{title}]` when influenced by a memory
- This enables reference tracking and memory strength scoring

### Reference Tracking

- Agents increment reference tracking via the CRUX memory reference-tracker skill
- Never manipulate reference tracking files directly

### Dream Nudge

- After spec execution completes, suggest running `/crux-dream` to extract learnings

## When Memories Are Disabled (`enableMemories: "false"`)

- Agents skip all memory operations silently
- No index loading, no annotation, no reference tracking

## General Rules

- Agents never directly read or write memory files — they use CRUX memory skills
- Agents only see base memories and their own agent-scoped memories
- Each repository owns its own memories; agents never touch memories from other repos
- Memory files live in the `memories/` directory (configurable via `cruxMemories.storage.memoriesDir`)

## MCP Server Configuration

To enable semantic search over memories, add the MCP server to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "crux-memories": {
      "command": "python",
      "args": ["-m", "crux_mcp_server", "-t", "stdio", "--config", ".crux/crux-memories.json"]
    }
  }
}
```

When MCP is available, agents prefer semantic search over linear index scanning for large memory sets.
