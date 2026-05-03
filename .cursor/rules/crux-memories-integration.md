---
alwaysApply: true
description: "CRUX Memories integration rule"
crux: true
---

# CRUX Memories Integration Rule

This rule governs how agents interact with the CRUX Memories system. Behavior is controlled by the `enableMemories` flag in `.crux/crux-memories.json`, unless the current chat session explicitly enables `/crux-amnesia`.

## Session Override: `/crux-amnesia`

- `/crux-amnesia` is a **chat-session-only** override
- When amnesia mode is on, it takes precedence over `enableMemories: "true"`
- Amnesia mode suppresses ambient memory discovery, loading, annotation, reference tracking, and automatic `/crux-dream` nudges during ordinary work
- This override must **never** modify `.crux/crux-memories.json`, memory files, trackers, or the memory index
- Subagents spawned for ordinary work inherit the same amnesia state and must suppress ambient memory usage too
- If the user explicitly invokes a memory-management command (`/crux-dream`, `/crux-recall`, `/crux-remember`, `/crux-meditate`, `/crux-forget`), treat that as direct user intent to interact with memories even while amnesia mode is on

## When Memories Are Enabled (`enableMemories: "true"`)

### Discovery

- Agents MUST discover memories by reading `.crux/memory-index.yml`
- Load full memory files only for likely matches (by title, description, or tags)
- If MCP is configured, agents may use semantic search instead of index scanning

### Output Annotation (CRITICAL)

- When a memory influences your response, you **MUST** include `[memory:{title}]` in your output, where `{title}` is the memory's exact title from its frontmatter
- Place the annotation inline near the relevant statement, or at the end of the paragraph it influenced
- This is how the system tracks which memories are valuable — an `afterAgentResponse` hook automatically scans for these annotations and updates reference trackers
- Example: "Components should use memoization with custom comparators. [memory:React.memo on list item components prevents full re-render on data changes]"
- You do NOT need to manually invoke the reference-tracker skill — the hook handles all `.refs.yml` bookkeeping automatically

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

The MCP server is installed at the user level and shared across all projects. Install it via:

```bash
pipx install ./crux_mcp_server
```

This configures `~/.cursor/mcp.json` with:

```json
{
  "mcpServers": {
    "crux-memories": {
      "command": "crux-mcp-server",
      "args": ["-t", "stdio", "--config", ".crux/crux-memories.json"]
    }
  }
}
```

When MCP is available, agents prefer semantic search over linear index scanning for large memory sets.
