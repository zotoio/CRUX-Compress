# CRUX Memories

CRUX provides a generalised, repo-agnostic memory system as a first-class tool — including slash commands, hooks, skills, compression, strength tracking, type transitions, dreaming, and REM sleep. Consuming frameworks do not implement any of this machinery. Instead, they configure the CRUX memory tool to work within their spec workflow, agent system, and repo conventions via a declarative integration contract.

---

## 1. CRUX Memory Tool Contract (What CRUX Provides)

The CRUX memory tool exposes the following interface. Consumers treat this as an opaque capability.

### Commands (provided by CRUX, configurable)

Each command points to a definition file. Defaults ship with CRUX; consumers can override by pointing to their own files.

| Command | Default | Purpose |
|---|---|---|
| dream [spec...] | `/crux-dream` | Post-execution analysis for given spec(s). If omitted, lists unprocessed specs to choose from |
| dream --rem | `/crux-dream --rem` | REM sleep: verify, consolidate, rebalance existing memories |
| dream --rem --yolo | `/crux-dream --rem --yolo` | Unattended REM sleep |
| mindreader [spec... \| memory... \| query] | `/crux-mindreader` | Decompress and display memories in chat. Pass spec(s) to show memories from those specs, memory file(s) to view specific ones, or a question about the current chat. If omitted, shows all memories referenced in the current session with rationale for why each was included |

### Hooks (provided by CRUX, configurable triggers)

| Hook | Trigger | Purpose |
|---|---|---|
| `session-start-memory-check` | Session start | Counts items in configurable directory; nudges user to dream if threshold exceeded |
| `post-dream-actions` | After Dream completes | Rebuilds memory index and notifies MCP server (if configured) to re-sync |

### Skills (provided by CRUX, available to agents)

| Skill | Purpose |
|---|---|
| `crux-skill-memory-extract` | Analyse execution artifacts, compare with existing memories, propose candidate facts |
| `crux-skill-memory-crud` | Create, read, update, delete memories with frontmatter management |
| `crux-skill-memory-rebalance` | Consolidate, promote, demote, archive memories based on strength and usage |
| `crux-skill-memory-compress` | CRUX-compress memory files, manage source archive for originals |
| `crux-skill-memory-reference-tracker` | Track which memories are referenced in agent output, increment strength counters |
| `crux-skill-memory-index` | Python script that builds a prioritised index from all memory frontmatter |

### Agent: `crux-cursor-memory-manager`

Commands (`/crux-dream`, `/crux-mindreader`) spawn a `crux-cursor-memory-manager` subagent to perform the actual work. This agent definition is provided by CRUX and lives at `.cursor/agents/crux-cursor-memory-manager.md` (Cursor) or equivalent per platform.

**Agent definition frontmatter:**

```yaml
---
name: crux-cursor-memory-manager
description: Memory lifecycle manager for CRUX. Handles dream extraction, REM sleep rebalancing, conflict detection, compression, and MindReader decompression.
model: claude-4.5-opus-high-thinking
repository: https://github.com/zotoio/CRUX-Compress
---
```

**Responsibilities:**

- Read `.crux/crux-memories.json` config on startup
- Orchestrate all memory skills (`crux-skill-memory-extract`, `crux-skill-memory-crud`, `crux-skill-memory-rebalance`, `crux-skill-memory-compress`, `crux-skill-memory-reference-tracker`, `crux-skill-memory-index`)
- Execute dream workflow steps (verify execution, diff changes, detect conflicts, present candidates, CRUD, write summary, offer archival)
- Execute REM sleep workflow steps (load memories, scan trackers, detect conflicts, recommend changes, apply, write summary)
- Execute MindReader operations (decompress memories, provide rationale for referenced memories, answer queries about memory influence)
- Respect agent scoping rules (only write agent memories during dream, only when spec artifacts identify the agent, never access other agents' directories)
- Respect `scopeRanking` and `typePriority` when presenting memories

**Key files the agent references:**

| File | Purpose |
|---|---|
| `.crux/crux-memories.json` | All config (storage, commands, hooks, transitions, scopes) |
| `.crux/memory-index.yml` | Prioritised memory index for discovery |
| `.crux/reference-tracking/*.refs.yml` | Per-memory reference tracking data |
| `CRUX.md` | CRUX compression specification (for compress/decompress operations) |

**Platform equivalents:**

| Platform | Agent definition location |
|---|---|
| Cursor | `.cursor/agents/crux-cursor-memory-manager.md` |
| Claude Code | Inline in command definitions (`.claude/commands/crux-dream.md` etc.) — Claude Code does not have a separate agent concept |
| Generic | Embedded in the `crux-memory-server` or shell script preamble |

### Memory File Format (managed by CRUX)

Each memory is **self-contained** — its frontmatter and body together provide full context without needing to read other files.

### Directory Structure

Memories are stored in subdirectories named by type. The index skill scans recursively.

```
memories/
├── core/
│   └── react-memo-list-rendering.memory.crux.md
├── redflag/
│   └── cache-invalidation-race-condition.memory.md
├── goal/
├── learning/
│   └── usecallback-stale-closures.memory.md
├── idea/
│   └── k8s-pod-resource-limits.memory.md
├── archived/
├── agents/
│   ├── code-reviewer/
│   │   ├── core/
│   │   ├── redflag/
│   │   │   └── missed-null-checks-in-api-handlers.memory.md
│   │   ├── learning/
│   │   │   └── prefer-exhaustive-switch-over-if-chains.memory.md
│   │   └── idea/
│   └── test-generator/
│       ├── core/
│       ├── learning/
│       │   └── mock-external-deps-not-internals.memory.md
│       └── idea/
└── shared/ -> ../other-repo/memories  (symlink, read-only)
```

When a memory's type changes (e.g. promoted from `learning` to `core`), the skill moves the file to the new type directory. Prioritisation order is defined by config (see `typePriority`), not by directory naming.

### Agent-Scoped Memories

Agent memories are **only written during the dream workflow**, never directly by agents during normal work. During dream, the CRUX engine examines spec execution artifacts to determine which agent was involved in producing each candidate memory:

- If the spec artifacts indicate a specific agent persona (e.g. `code-reviewer`, `test-generator`) **and** the memory is specific to that agent's concerns (e.g. review patterns, test strategies), it is saved to `memories/agents/{agent-id}/`
- All other memories go to the base `memories/` directories, even if an agent was involved — general-purpose learnings belong in base

Agent directories use the same type subdirectory structure and are named after the agent's ID or name.

**Boost rules:** When an agent discovers memories, its own agent-scoped memories are **boosted** in priority — ranked higher than base memories of the same type. However, agent memories never override base memories of a **higher-priority type**. For example:

| Agent memory | Base memory | Winner |
|---|---|---|
| `agents/code-reviewer/learning/...` | `learning/...` | Agent memory (same type, agent boosted) |
| `agents/code-reviewer/learning/...` | `redflag/...` | Base memory (higher-priority type wins) |
| `agents/code-reviewer/core/...` | `learning/...` | Agent memory (higher-priority type) |

Agents only read from their own agent directory and the base `memories/` directories — they never access other agents' memory directories. This means agents develop their own expertise over time without polluting the base memory corpus, their learnings naturally defer to project-wide core knowledge and red flags, and agent knowledge is isolated from other agents.

### File Naming

- Uncompressed: `{slug}.memory.md`
- Compressed: `{slug}.memory.crux.md`

```yaml
---
title: "React.memo on list item components prevents full re-render on data changes"
description: "Wrapping list item components in React.memo with a custom comparator reduced re-render time from 480ms to 12ms on a 500-item list. Key: comparator should check item ID and version, not deep-equal the entire props object."
type: "core" | "redflag" | "goal" | "learning" | "idea" | "archived"
strength: 3             # numeric, auto-incremented on reference
created: 2026-04-03
modified: 2026-04-03
source: "20260403-component-library"
tags: [react, performance, rendering]
promoted_from: "learning"   # if type transition occurred
---
```

| Field | Required | Description |
|---|---|---|
| `title` | Yes | Instructive, descriptive title — should convey the key insight at a glance |
| `description` | Yes | Self-contained summary of the memory's content — enough to act on without reading the body |
| `type` | Yes | Memory category — matches directory name. Default types: `core`, `redflag`, `goal`, `learning`, `idea`, `archived` |
| `strength` | Yes | Numeric strength, auto-incremented on reference |
| `created` | Yes | Date memory was created |
| `modified` | Yes | Date memory was last modified |
| `source` | Yes | The unit of work that originated this memory (e.g. spec, prp, task — matches `unitOfWork` config) |
| `tags` | No | Searchable tags |
| `promoted_from` | No | Previous type if a type transition occurred |

A configurable `maxMemorySize` (default: 2048 bytes) limits individual memory file size. When compression is enabled, the compression level is adjusted to fit within this limit — the skill will increase compression aggressiveness until the output fits, or flag the memory as too large if it cannot.

Reference counts and timestamps are **not** stored in memory frontmatter — they live in per-memory tracker files (see [Reference Tracking Data](#reference-tracking-data-cruxreference-tracking)).

### Strength → Type Transition Rules (configurable per-repo)

```json
{
  "typeTransitions": {
    "idea":     { "promoteAt": 5,  "promoteTo": "learning" },
    "learning": { "promoteAt": 15, "promoteTo": "core" },
    "redflag":  { "promoteAt": 10, "promoteTo": "core" },
    "core":     { "promoteAt": null },
    "goal":     { "promoteAt": null },
    "archived": { "promoteAt": null }
  },
  "demoteAfterDaysUnreferenced": 90,
  "archiveAfterDaysUnreferenced": 180
}
```

### Dream Workflow (executed by CRUX engine)

The term "spec" below is the default `unitOfWork` — frameworks can configure this to match their own terminology (e.g. "prp", "task", "story").

1. Verify spec execution success (check `_execution-state.yml` status)
2. Diff repo changes since spec start (if too many unrelated changes, warn/abort with configurable threshold)
3. Analyse spec + execution output + existing memories
4. **Detect conflicts:** Compare candidate facts against existing memories for contradictions (e.g. a new learning that directly conflicts with an existing core memory). Present conflicts to the user with both sides and ask how to handle: keep existing, replace, merge, or keep both with a note
5. Present top N candidate facts (configurable, default 5) — or auto-accept in `--yolo` mode
6. CRUD against memory corpus (user confirms each, or yolo)
7. Write dream summary to `dream-{slug}-{yyyymmdd}.md` in the specific spec subdirectory under `workDir` (e.g. `specs/current/20260401-component-library/dream-component-library-20260403.md`)
8. Offer spec archival: move to configured archive dir, leave in place, or delete

### REM Sleep Workflow (executed by CRUX engine)

1. Load all memories and scan `*.refs.yml` tracker files from `trackingDir`
2. Verify consistency (orphaned references, stale sources, broken strength chains, tracker files with no matching memory)
3. **Detect conflicts:** Identify memories that contradict each other (e.g. two learnings giving opposing advice, or an idea that conflicts with a core memory). Present each conflict with both sides and ask the user how to resolve: keep one, merge, or keep both with disambiguation notes
4. Analyse tracker data and recommend changes to the user:
   - **Conflicts:** contradicting memories that need resolution (from step 3)
   - **Promote:** memories whose strength exceeds the `promoteAt` threshold for their current type
   - **Demote:** memories unreferenced for longer than `demoteAfterDaysUnreferenced`
   - **Archive:** memories unreferenced for longer than `archiveAfterDaysUnreferenced`
   - **Consolidate:** duplicate or near-duplicate memories that should be merged
   - **Rebalance:** strength scores that are out of sync with actual reference counts
   - **Promote to rule:** memories exceeding `promotionToRuleThreshold` references — suggest converting to a permanent rule or context
   - **Cleanup:** orphaned tracker files with no matching memory file
5. Present all recommendations to the user for confirmation (or auto-apply in `--yolo`, except conflicts which always require user input)
6. Execute confirmed changes (move files between type directories, update frontmatter, delete/merge tracker files)
7. Write REM sleep summary to `rem-{yyyymmdd}.md` in `archiveDir` (not spec-specific — covers all memories reviewed)
8. Report what changed

---

## 2. Consumer Integration Configuration

A consumer's entire integration is a configuration block in their project config (e.g. `.crux/crux-memories.json`) plus a few platform-specific wiring files. No engine code.

### Platform Capability Mapping

The core memory engine is identical across platforms. Only the wiring layer differs:

| Capability | Cursor | Claude Code | Generic / Other |
|---|---|---|---|
| Agent rules | `.cursor/rules/*.mdc` | `CLAUDE.md` / `.claude/settings.json` | `memories/MEMORIES_AGENT_RULE.md` |
| Commands | `/crux-dream` → `.cursor/commands/crux-dream.md` | `/crux-dream` → `.claude/commands/crux-dream.md` | `crux-dream` → shell script or MCP call |
| Session hooks | `.cursor/hooks/*.sh` | `.claude/hooks/session-start.sh` | Git hook or manual |
| Skills/tools | `.cursor/skills/*/SKILL.md` | Tool use via MCP or inline prompts | MCP tools or scripts |
| Memory discovery (default) | Read `.crux/memory-index.yml`, load matching `*.memory.md` files | Read `.crux/memory-index.yml`, load matching `*.memory.md` files | Read `.crux/memory-index.yml`, load matching `*.memory.md` files |
| MCP integration (optional) | Cursor MCP config in `.cursor/` | `.mcp.json` or `claude mcp add` | MCP server config |
| Command trigger | `/crux-dream` in chat | `/crux-dream` or `claude -p "run crux-dream"` | `./crux-dream.sh` or MCP call |

### Configuration Schema

```json
{
  "platform": "cursor | claude-code | generic",

  "flags": [
    { "enableMemories": "false" },
    { "enableMemoryCompression": "false" }
  ],

  "cruxMemories": {
    "enabled": "${flags.enableMemories}",
    "compression": "${flags.enableMemoryCompression}",

    "storage": {
      "memoriesDir": "memories",
      "agentMemoriesDir": "memories/agents",
      "archiveDir": ".ai-ignored/executed",
      "compressionSourceArchive": ".ai-ignored/memories/sources",
      "indexFile": ".crux/memory-index.yml"
    },

    "maxMemorySize": 2048,
    "compressionTarget": 33,
    "unitOfWork": "spec",

    "commands": {
      "dream": {
        "file": ".cursor/commands/crux-dream.md",
        "default": "/crux-dream",
        "description": "Post-execution memory extraction and consolidation"
      },
      "mindReader": {
        "file": ".cursor/commands/crux-mindreader.md",
        "default": "/crux-mindreader",
        "description": "Decompress and view memories in chat"
      }
    },

    "hooks": {
      "sessionStartNudge": {
        "trigger": "sessionStart",
        "watchDir": "specs/current",
        "threshold": 20,
        "message": "Agent: 🥱 I need a nap to process what we've been working on. Run /crux-dream in a fresh thinking agent. I'll wake up fresh and ready for our next ${unitOfWork} after that!"
      }
    },

    "dream": {
      "maxCandidateFacts": 5,
      "maxUnrelatedChanges": 50,
      "stateFile": "_execution-state.yml",
      "workDir": "specs/current",
      "summaryPattern": "dream-{slug}-{yyyymmdd}.md"
    },

    "typePriority": ["core", "redflag", "goal", "learning", "idea", "archived"],

    "typeTransitions": {
      "idea":     { "promoteAt": 5,  "promoteTo": "learning" },
      "learning": { "promoteAt": 15, "promoteTo": "core" },
      "redflag":  { "promoteAt": 10, "promoteTo": "core" },
      "core":     { "promoteAt": null },
      "goal":     { "promoteAt": null }
    },

    "demoteAfterDaysUnreferenced": 90,
    "archiveAfterDaysUnreferenced": 180,

    "referenceTracking": {
      "enabled": true,
      "trackingDir": ".crux/reference-tracking",
      "indicateInOutput": true,
      "indicatorFormat": "[memory:{title}]",
      "promotionToRuleThreshold": 30,
      "maxReferencesStored": 10
    },

    "scopeRanking": ["base", "agents", "shared"],

    "scopes": {
      "base": {
        "memoriesDir": "memories",
        "readonly": false
      },
      "agents": {
        "memoriesDir": "memories/agents/{agent-id}",
        "readonly": false,
        "writeOnlyDuringDream": true,
        "boostSameType": true
      },
      "shared": [
        {
          "memoriesDir": "memories/shared/upstream-framework",
          "symlink": true
        }
      ]
    }
  }
}
```

### Reference Tracking Data (`.crux/reference-tracking/`)

Reference counts are **externalised** from memory files into per-memory tracker files. A tracker file is created in `trackingDir` (default: `.crux/reference-tracking/`) the first time a memory is referenced. Each memory gets its own file, named `{slug}.refs.yml`.

```
.crux/reference-tracking/
├── react-memo-list-rendering.refs.yml
├── cache-invalidation-race-condition.refs.yml
└── k8s-pod-resource-limits.refs.yml
```

Example — `.crux/reference-tracking/react-memo-list-rendering.refs.yml`:

```yaml
# Managed by crux-skill-memory-reference-tracker — do not edit manually
slug: react-memo-list-rendering
references: 12
last_referenced: 2026-04-03
strength: 3
recent_references:
  - spec: "20260403-component-library"
    count: 5
    last: 2026-04-03
  - spec: "20260401-dashboard-performance"
    count: 4
    last: 2026-04-01
  - conversation_id: "a3f7b2c"
    count: 3
    last: 2026-03-30
    context: "Discussed memoization strategy for data table components"
```

Example — `.crux/reference-tracking/cache-invalidation-race-condition.refs.yml`:

```yaml
# Managed by crux-skill-memory-reference-tracker — do not edit manually
slug: cache-invalidation-race-condition
references: 7
last_referenced: 2026-04-01
strength: 2
recent_references:
  - spec: "20260401-caching-layer"
    count: 5
    last: 2026-04-01
  - conversation_id: "e9c1d4a8"
    count: 2
    last: 2026-03-28
    context: "Reviewed TTL strategy for user profile cache"
```

| Field | Description |
|---|---|
| `slug` | Memory slug (matches filename, stable identifier) |
| `references` | Total times this memory was referenced across all sessions |
| `last_referenced` | Date of most recent reference |
| `strength` | Current strength score (kept in sync with memory frontmatter by the skill) |
| `recent_references` | Top N referrers (configurable via `maxReferencesStored`, default 10), ranked by `count` descending. Each entry records the source (`spec` or `conversation_id`), `count` of references from that source, `last` reference date, and optional `context` |

**Why per-memory files:**
- Zero contention — concurrent sessions referencing different memories write to different files
- Memory files stay clean — frontmatter describes *what* a memory is, not *how often* it's used
- Tracker created lazily on first reference — unreferenced memories have no tracker overhead
- Each tracker is small, easy to diff, and independently deletable
- Dream and REM sleep workflows scan the directory to drive promotion/demotion decisions

### Memory Index (`.crux/memory-index.yml`)

The `crux-skill-memory-index` skill runs a Python script that **recursively** scans all `*.memory.md` and `*.memory.crux.md` files across the type subdirectories, reads their frontmatter, joins with matching `*.refs.yml` tracker files from the `trackingDir`, and produces a prioritised index. This index is the **default memory discovery mechanism** — no MCP server is required. Agents read the index at session start, match titles/descriptions/tags against the current task, and load full memory files only for likely matches.

```yaml
# .crux/memory-index.yml
# Generated by crux-skill-memory-index — do not edit manually
# Last rebuilt: 2026-04-03T14:22:00Z

memories:
  - slug: react-memo-list-rendering
    title: "React.memo on list item components prevents full re-render on data changes"
    description: "Wrapping list item components in React.memo with a custom comparator..."
    type: "core"
    strength: 3
    references: 12
    tags: [react, performance, rendering]
    file: memories/core/react-memo-list-rendering.memory.crux.md

  - slug: cache-invalidation-race-condition
    title: "Cache invalidation race condition causes stale reads after writes"
    description: "Write-through cache with 200ms delay window causes stale..."
    type: "redflag"
    strength: 2
    references: 7
    tags: [caching, concurrency, consistency]
    file: memories/redflag/cache-invalidation-race-condition.memory.md

  - slug: k8s-pod-resource-limits
    title: "K8s pods without resource limits cause noisy-neighbour OOM kills"
    description: "Setting explicit CPU/memory requests and limits on all pods..."
    type: "idea"
    strength: 1
    references: 2
    tags: [kubernetes, reliability, resources]
    file: memories/idea/k8s-pod-resource-limits.memory.md
```

**Prioritisation order:** `core` > `redflag` > `goal` > `learning` > `idea` > `archived` (configurable via `typePriority`), then by strength descending, then by reference count descending.

The index is rebuilt by the Python script whenever memories change (during dream, REM sleep, or on-demand). Agents read this file first to find relevant memories by title, description, tags, or type — then load individual memory files only for likely matches. This keeps context window usage minimal: the index is small enough to scan fully, while full memory files are only loaded when the agent decides they're relevant.

When an MCP memory server is configured, agents may use it for semantic search instead of (or in addition to) the index file. MCP is optional — the index-based approach works on every platform with zero infrastructure.

### MCP Memory Server Specification (optional)

An MCP server providing memory search must implement the following tools. This is the contract that agents expect when MCP is configured.

#### Required Tools

**`memory-search`** — Semantic search across memories.

```json
{
  "name": "memory-search",
  "description": "Search memories by semantic similarity to a query. Returns ranked results with frontmatter and file paths.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Natural language search query"
      },
      "limit": {
        "type": "integer",
        "default": 10,
        "description": "Maximum number of results to return"
      },
      "types": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Filter by memory types (e.g. [\"core\", \"redflag\"]). Omit for all types"
      },
      "tags": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Filter by tags. Results must match at least one tag"
      },
      "agentId": {
        "type": "string",
        "description": "If provided, include agent-scoped memories for this agent. Base memories are always included"
      },
      "minStrength": {
        "type": "integer",
        "description": "Minimum strength score to include"
      },
      "includeContent": {
        "type": "boolean",
        "default": false,
        "description": "If true, return full memory file contents in a 'content' field for each result. Default returns only frontmatter references for the agent to filter and selectively load"
      }
    },
    "required": ["query"]
  }
}
```

Response format (default — `includeContent: false`):

```json
{
  "results": [
    {
      "slug": "react-memo-list-rendering",
      "title": "React.memo on list item components prevents full re-render on data changes",
      "description": "Wrapping list item components in React.memo...",
      "type": "core",
      "strength": 3,
      "tags": ["react", "performance", "rendering"],
      "file": "memories/core/react-memo-list-rendering.memory.crux.md",
      "score": 0.92
    }
  ]
}
```

With `includeContent: true`, each result includes the full file contents:

```json
{
  "results": [
    {
      "slug": "react-memo-list-rendering",
      "title": "...",
      "description": "...",
      "type": "core",
      "strength": 3,
      "tags": ["react", "performance", "rendering"],
      "file": "memories/core/react-memo-list-rendering.memory.crux.md",
      "score": 0.92,
      "content": "---\ntitle: \"React.memo on list item components...\"\n...\n---\n\nFull memory body here..."
    }
  ]
}
```

**`memory-read`** — Read the full content of a memory file.

```json
{
  "name": "memory-read",
  "description": "Read the full content of one or more memory files by slug or file path.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "slugs": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Memory slugs to read"
      },
      "files": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Memory file paths to read (relative to repo root)"
      }
    }
  }
}
```

#### Optional Tools

**`memory-stats`** — Return summary statistics about the memory corpus.

```json
{
  "name": "memory-stats",
  "description": "Return counts by type, total memories, and index freshness.",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

#### Indexing Workflow

The MCP server is responsible for maintaining its own search index. The recommended workflow:

1. On startup, read `.crux/memory-index.yml` and all `*.memory.md` / `*.memory.crux.md` files to build the initial index
2. Watch the `memoriesDir` for filesystem changes (file create/modify/delete/move) and update the index incrementally
3. When a dream or REM sleep completes, the `crux-skill-memory-index` Python script rebuilds `.crux/memory-index.yml` — the MCP server should detect this and re-sync
4. For compressed memories (`*.memory.crux.md`), index the frontmatter fields (title, description, tags) directly — these are never compressed. Optionally decompress the body for richer semantic indexing

The MCP server does **not** write memory files or tracker files — it is read-only. All writes go through the CRUX skills.

#### Reference Local stdio Server

A reference implementation is provided as a local stdio server that can be used with any MCP-compatible platform:

The server script uses a Python shebang for portability:

```python
#!/usr/bin/env python3
"""crux-memory-server — MCP stdio server for CRUX memory search."""
```

MCP configuration:

```json
{
  "mcpServers": {
    "crux-memories": {
      "command": "crux-memory-server",
      "args": ["--config", ".crux/crux-memories.json"]
    }
  }
}
```

The reference server:
- Runs as a local stdio process (no network, no external dependencies)
- Python script with `#!/usr/bin/env python3` — uses `sentence-transformers` for semantic search when available, falls back to TF-IDF over title, description, and tags
- Reads config from the specified `--config` path
- Watches the filesystem for changes and re-indexes incrementally
- Respects agent scoping — `agentId` parameter controls which agent directories are visible
- Decompresses `*.memory.crux.md` bodies on read via the CRUX decompression library

---

## 3. Platform Wiring (Minimal Changes per Platform)

Each platform needs three wiring points: an **agent rule** (teaches the agent about memories), a **session hook** (nudges the user to dream), and a **post-execution hook** (suggests dreaming after spec completion). The core behaviour is identical — only the file format and location differ.

### Agent Rule Content (shared across all platforms)

Regardless of platform, the agent rule must convey:

- When `enableMemories` flag is `"true"`, agents MUST:
  - **Discover memories:** Read `.crux/memory-index.yml` (generated by `crux-skill-memory-index`) to scan frontmatter (title, description, tags, type). If MCP is configured, agents may use semantic search instead for richer matching.
  - **Load on match:** When the index suggests a memory is relevant to the current task, load the full `*.memory.md` / `*.memory.crux.md` file referenced in the index entry
  - Clearly indicate when output is influenced by a memory: `[memory:{title}]`
  - Increment reference tracking (delegated to CRUX skill)
  - After spec execution completes, suggest running `/crux-dream`
- When `enableMemories` is `"false"`, agents skip all memory operations silently
- Agents never directly read/write memory files — they use CRUX memory skills
- Agents only see base memories and their own agent-scoped memories — never other agents' memories
- Each repo owns its own memories; agents never touch memories from other repos

---

### 3a. Cursor Wiring

**A. Rule:** `.cursor/rules/crux-memories-integration.mdc`

Standard Cursor rule file (`.mdc`) containing the agent rule content above. Automatically loaded by Cursor when the repo is opened.

**B. Session hook:** `.cursor/hooks/session-startup.sh`

Add a clause that:

1. Reads `cruxMemories.hooks.sessionStartNudge` from config
2. Counts directories in `watchDir`
3. If count > threshold and `enableMemories` is `"true"`, adds the nudge message to `additional_context`

**C. Post-execution hook:** In the execution-orchestration skill's finalization phase:

- If `enableMemories` is `"true"` and spec execution status is `complete`, suggest running the configured dream command (default: `/crux-dream`)

**D. Commands:** Pointed to by `commands.dream.file` and `commands.mindReader.file` in config.

Defaults to `.cursor/commands/crux-dream.md` and `.cursor/commands/crux-mindreader.md`. These are standard Cursor slash command definitions that invoke the CRUX dream and mindreader skills. Consumers can override by pointing `file` at their own command definitions (e.g. `.cursor/commands/my-dream.md`) to wrap additional project-specific logic.

**E. MCP (optional):** If configured, add CRUX memory MCP server in `.cursor/mcp.json` for semantic memory search. Without MCP, agents use the index file (`.crux/memory-index.yml`) for discovery — no additional setup required.

---

### 3b. Claude Code Wiring

**A. Rule:** `CLAUDE.md` (append) or `.claude/memories-rule.md`

Add the agent rule content to the project's `CLAUDE.md` file (which Claude Code reads automatically at session start), or place it in a `.claude/` subdirectory if the project supports modular instructions.

Example `CLAUDE.md` addition:

```markdown
## CRUX Memories

This project uses CRUX memories. When `enableMemories` is true in
`.crux/crux-memories.json`:

- Before starting work, read `.crux/memory-index.yml` and scan for
  memories relevant to the current task (by title, description, tags).
  Load the full memory file only for likely matches. If an MCP memory
  server is configured, you may use semantic search instead.
- When output is influenced by a memory, annotate with `[memory:{title}]`
- After spec execution completes, suggest: "Run `/crux-dream` to extract
  memories from this execution"
- Never read/write memory files directly — use CRUX memory skills
- Each repo owns its own memories; never touch other repos' memories

When `enableMemories` is false, skip all memory operations silently.
```

**B. Session hook:** `.claude/hooks/session-start.sh`

Claude Code supports project-level hooks. The session-start hook reads the CRUX config, counts spec directories, and prints the nudge message if threshold is exceeded:

```bash
#!/usr/bin/env bash
CONFIG=".crux/crux-memories.json"
if [ ! -f "$CONFIG" ]; then exit 0; fi

ENABLED=$(jq -r '.cruxMemories.enabled' "$CONFIG")
if [ "$ENABLED" != "true" ]; then exit 0; fi

WATCH_DIR=$(jq -r '.cruxMemories.hooks.sessionStartNudge.watchDir' "$CONFIG")
THRESHOLD=$(jq -r '.cruxMemories.hooks.sessionStartNudge.threshold' "$CONFIG")
COUNT=$(find "$WATCH_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)

if [ "$COUNT" -gt "$THRESHOLD" ]; then
  MSG=$(jq -r '.cruxMemories.hooks.sessionStartNudge.message' "$CONFIG")
  echo "$MSG"
fi
```

**C. Commands:** `.claude/commands/crux-dream.md` and `.claude/commands/crux-mindreader.md`

The config `commands.dream.file` points at the command definition. For Claude Code, the default is `.claude/commands/crux-dream.md`. Example:

```markdown
Analyse unprocessed spec directories and extract memories using the CRUX
memory system. Read config from `.crux/crux-memories.json`. Follow the
dream workflow: verify execution, diff changes, present candidate facts,
CRUD memories, offer archival. Use CRUX memory MCP tools for all operations.
Pass $ARGUMENTS as the spec directory to process (or list available if empty).
```

**D. MCP (optional):** If semantic search is desired, configure via `.mcp.json` (project root) or `claude mcp add`. Without this, agents use the index file for discovery.

```json
{
  "mcpServers": {
    "crux-memories": {
      "command": "crux-memory-server",
      "args": ["--config", ".crux/crux-memories.json"]
    }
  }
}
```

---

### 3c. Generic / Other Platforms

For platforms without native slash commands or hook systems, CRUX provides shell-level equivalents:

**A. Rule:** `memories/MEMORIES_AGENT_RULE.md`

A plain markdown file placed in the memories directory. Agents on any platform can be instructed to read this file at session start (via their platform's instruction mechanism).

**B. Session hook:** Manual or git-hook based

```bash
# Add to .git/hooks/post-checkout or run manually
crux-memories check-session --config .crux/crux-memories.json
```

**C. Commands:** The config `commands.dream.file` and `commands.mindReader.file` point at shell scripts by default on generic platforms:

```bash
# Dream (interactive) — default: ./crux-dream
crux-dream --config .crux/crux-memories.json

# Dream (unattended)
crux-dream --rem --yolo --config .crux/crux-memories.json

# MindReader — default: ./crux-mindreader
crux-mindreader --config .crux/crux-memories.json
```

**D. MCP (optional):** Standard MCP server configuration per the platform's method. Not required — the index file works without any MCP infrastructure.

---

### Platform Selection

The `"platform"` key in config controls which wiring conventions CRUX expects when it validates setup or scaffolds initial files:

| Value | Effect |
|---|---|
| `"cursor"` | Commands default to `.cursor/commands/crux-dream.md` etc. Expects `.cursor/rules/`, `.cursor/hooks/`, `.cursor/mcp.json` |
| `"claude-code"` | Commands default to `.claude/commands/crux-dream.md` etc. Expects `CLAUDE.md` or `.claude/`, `.mcp.json` |
| `"generic"` | Commands default to shell scripts (`crux-dream`, `crux-mindreader`). Expects `memories/MEMORIES_AGENT_RULE.md`, manual MCP config |

A `crux-memories init --platform <name>` command scaffolds the correct wiring files for the chosen platform.

---

## 4. Compression

Memory files should be compacted with CRUX. A separate `memoryCompression` feature flag (disabled by default) controls this.

### File Naming

| State | Pattern | Example |
|---|---|---|
| Uncompressed | `{slug}.memory.md` | `core/react-memo-list-rendering.memory.md` |
| Compressed | `{slug}.memory.crux.md` | `core/react-memo-list-rendering.memory.crux.md` |

### Adaptive Compression

When compression is enabled, the `crux-skill-memory-compress` skill targets `compressionTarget` (default `33` — aim for 33% of original size) and adjusts compression level to also fit within `maxMemorySize` (default 2048 bytes). The process:

1. Attempt CRUX compression targeting `compressionTarget` percentage (e.g. 33 = reduce to 33% of original)
2. If output exceeds `maxMemorySize`, increase compression aggressiveness beyond the target ratio
3. If still too large after maximum compression, flag the memory for manual review
4. Frontmatter (`title`, `description`, `type`, etc.) is never compressed — only the body

### Migration

When a memory has not been compressed and the compression flag is later enabled, offer to compress existing `*.memory.md` files detected as uncompressed. The original is moved to `.ai-ignored/memories/sources/[yyyymmdd]/*`.

### Viewing

As memories should not be manually modified and are not user-managed, CRUX concepts are all we care about. The `/crux-mindreader` command decompresses memories just in the chat window for users to view, only decompressing CRUX to terse content so that output is as similar as possible over multiple runs.

**Invocation modes:**

- **No arguments:** Show all memories that were referenced in the current session. For each, explain *why* it was included — what matched (title, tags, description) and how it influenced output. If no memories were referenced yet, show the top memories from the index by priority.
- **Query / question:** If the argument looks like a question about the current chat (e.g. "why did you suggest X?"), identify which memory or memories influenced that part of the conversation and explain the rationale.
- **Spec name(s):** Show all memories that originated from the given spec(s).
- **Memory file(s):** Decompress and display the specified memory file(s).

---

## 5. Example Interaction

```
User: "/crux-dream"

CRUX: "Found 3 unprocessed spec directories:
       1. 20260401-component-library
       2. 20260402-caching-layer
       3. 20260403-k8s-hardening

       Which would you like to process?"

User: "1"

CRUX: "Analysing 20260401-component-library...
       ✅ Execution verified: 6/6 sub-specs complete
       📊 9 repo changes since spec start (within threshold)

       Comparing with 39 existing memories...

       Top 5 candidate facts from this execution:

       1. [learning] React.memo on list items reduced re-render time
          from 480ms to 12ms on 500-item lists
       2. [redflag] Uncontrolled re-renders on context changes cause UI
          freezes with large component trees
       3. [idea] Storybook visual regression tests could catch theme
          breakages before PR merge
       4. [learning] useCallback dependencies must include dispatch
          functions to avoid stale closures in event handlers
       5. [goal] Target <16ms render cycle for all interactive components
          — achieved 12ms

       Accept all? Or review individually? [all/individual/skip]"

User: "all"

CRUX: "✅ 5 memories saved.
       - 2 new learnings (strength: 1)
       - 1 new redflag (strength: 1)
       - 1 new idea (strength: 1)
       - 1 updated goal (strength: 4 → 5, promoted to 'core')

       What would you like to do with the spec directory?
       1. Move to .ai-ignored/executed/ (recommended)
       2. Leave in place
       3. Delete"

User: "1"

CRUX: "✅ Moved to .ai-ignored/executed/20260401-component-library/
       📝 Dream summary saved: specs/current/dream-component-library-20260403.md

       Sweet dreams. 🌙"
```

---

## 6. What Consumers Do NOT Implement

All of the following are provided entirely by CRUX:

- Memory storage engine
- Strength tracking logic
- Type transition rules engine
- Dream analysis algorithm
- REM sleep rebalancing
- Memory compression
- MindReader decompression
- Reference tracking counters
- Usage analytics for memories

Consumers only provide: configuration, spec-specific context (state files, execution artifacts, directory conventions), and agent rules that make the system visible to agents.

---

## 7. Extension and Consumer Support

The CRUX memory tool is repo-agnostic. Any framework can integrate:

- **Base:** Full read/write to `memories/` type directories — shared across all agents in the repo
- **Agent-scoped:** Written only during dream when spec artifacts identify an agent-specific memory. Boosted for that agent but defers to higher-priority base types
- **Shared:** Read-only access to another repo's memories via symlink at `memories/shared/`. Configured with `symlink: true` in the shared scope
- **Standalone:** Can use CRUX memories with its own config — no external dependencies

---

## 8. Evaluations

Two categories of evals cover the system: **developer evals** (automated, scriptable, CI-ready) that verify engine correctness, file formats, config, and skills; and **user evals** (interactive scenario checklists) that verify agent behaviour, memory influence on output, and UX flows.

Dev evals should be implementable as shell scripts (bats) or Python tests that set up fixture directories, run skills/commands, and assert file system state. User evals are scenario checklists for manual or agent-driven testing. Each eval should be independently runnable with a clean fixture directory and not affect the repo it is running in.

### A. Memory CRUD and File Format

- **Dev:** Create a memory via skill, verify frontmatter schema (all required fields present, valid type, strength starts at 1)
- **Dev:** Update a memory, verify `modified` date changes but `created` does not
- **Dev:** Verify `.memory.md` and `.memory.crux.md` naming conventions enforced
- **Dev:** Verify memories are placed in correct type subdirectory

### B. Dream Workflow

- **Dev:** Given a completed spec with execution artifacts, run dream and verify N candidate facts are extracted
- **Dev:** Verify dream summary is written to the correct spec subdirectory under `workDir`
- **Dev:** Verify spec archival moves to `archiveDir` correctly
- **User:** Run `/crux-dream` with no args, verify it lists unprocessed specs
- **User:** Run `/crux-dream <spec>`, walk through the full flow, verify memories saved match expectations
- **User:** Verify conflict detection presents contradictions and asks for resolution

### C. REM Sleep

- **Dev:** Seed memories with known strength/reference data, run REM, verify promote/demote/archive recommendations match thresholds
- **Dev:** Create orphaned tracker files (no matching memory), verify cleanup is recommended
- **Dev:** Create two contradicting memories, verify conflict detection fires
- **Dev:** Verify REM summary written to `archiveDir`
- **User:** Run `/crux-dream --rem`, verify recommendations are presented clearly
- **User:** Verify `--yolo` auto-applies everything except conflicts

### D. Reference Tracking

- **Dev:** Reference a memory in agent output, verify `{slug}.refs.yml` is created in `trackingDir`
- **Dev:** Reference same memory from two specs, verify `recent_references` has both entries with correct counts
- **Dev:** Verify `maxReferencesStored` cap is enforced (oldest evicted)
- **Dev:** Verify `[memory:{title}]` indicator appears in output when `indicateInOutput` is true
- **Dev:** Verify no indicator when `indicateInOutput` is false

### E. Memory Index

- **Dev:** Create memories across multiple type directories, run index skill, verify `.crux/memory-index.yml` contains all entries
- **Dev:** Verify prioritisation order matches `typePriority` config, then strength desc, then references desc
- **Dev:** Verify index includes agent-scoped memories with correct file paths
- **Dev:** Delete a memory file, rebuild index, verify it is removed

### F. Type Transitions and Strength

- **Dev:** Set a memory's strength to `promoteAt` threshold, run REM, verify promotion recommended
- **Dev:** After promotion, verify file moved to new type directory and frontmatter updated (`type`, `promoted_from`)
- **Dev:** Verify `demoteAfterDaysUnreferenced` triggers demotion for stale memories
- **Dev:** Verify `archiveAfterDaysUnreferenced` triggers archival

### G. Compression

- **Dev:** Enable compression, create a memory exceeding `maxMemorySize`, verify adaptive compression produces `*.memory.crux.md` within size limit
- **Dev:** Verify frontmatter is never compressed (title, description readable in compressed file)
- **Dev:** Verify `compressionTarget` percentage is respected (output size ~33% of original)
- **Dev:** Enable compression on repo with existing uncompressed memories, verify migration offer and source archival to `.ai-ignored/memories/sources/`

### H. Agent Scoping

- **Dev:** Run dream with spec artifacts identifying agent `code-reviewer`, verify agent-specific memory goes to `agents/code-reviewer/{type}/`
- **Dev:** Verify general-purpose memory from same spec goes to base `memories/{type}/`
- **Dev:** Verify agent cannot read other agent directories (only own + base)
- **Dev:** Verify agent memories are only written during dream, not during normal agent work
- **User:** As `code-reviewer` agent, verify own memories are boosted over base memories of same type
- **User:** Verify base `redflag` still outranks agent `learning`

### I. Scope Ranking and Shared

- **Dev:** Configure shared symlink scope, verify shared memories appear in index as read-only
- **Dev:** Verify `scopeRanking` order is respected when memories of same type/strength exist across scopes
- **Dev:** Attempt to write to shared scope, verify it is rejected

### J. MindReader

- **User:** Run `/crux-mindreader` with no args, verify it shows memories referenced in current session with rationale
- **User:** Run `/crux-mindreader "why did you suggest X?"`, verify it identifies influencing memory
- **User:** Run `/crux-mindreader <spec>`, verify it shows memories from that spec
- **User:** Run `/crux-mindreader <memory-file>`, verify decompressed content displayed

### K. Session Hook

- **Dev:** Set threshold to 2, create 3 spec directories in `watchDir`, start session, verify nudge message appears
- **Dev:** Set `enableMemories` to false, verify no nudge regardless of count

### L. MCP Server (when configured)

- **Dev:** Start `crux-memory-server`, call `memory-search` with a query, verify results match expected memories
- **Dev:** Call `memory-search` with `includeContent: true`, verify `content` field present in results
- **Dev:** Call `memory-search` with `includeContent: false` (default), verify no `content` field
- **Dev:** Call `memory-search` with `agentId`, verify agent-scoped memories included and other agents excluded
- **Dev:** Call `memory-read` by slug, verify full content returned
- **Dev:** Call `memory-stats`, verify counts by type are accurate

### M. Config Validation

- **Dev:** Load config with missing required fields, verify clear error messages
- **Dev:** Verify `unitOfWork` interpolation works in nudge message
- **Dev:** Verify platform-specific command file paths resolve correctly for each platform value
- **Dev:** Verify `typePriority` order is used (not alphabetical) when ranking

### N. Cross-Platform

- **User:** Run full dream/REM/mindreader flow on Cursor, verify wiring works
- **User:** Run full dream/REM/mindreader flow on Claude Code, verify wiring works
- **User:** Run full dream/REM/mindreader flow on generic platform via shell scripts

---

## Design Philosophy

This integration model is **configuration over implementation** — consumers declare what they want through `cruxMemories` config, and CRUX's generalised memory tool does the heavy lifting. The total consumer change surface is: one config block, one rule file, two hook clauses, and agent behaviour governed by the rule.

The platform adapter pattern means the same memory engine works identically whether an agent runs in Cursor, Claude Code, or a bare terminal. The `"platform"` key selects the wiring convention; everything above the wiring layer — memory storage, strength tracking, type transitions, dream analysis, REM sleep, compression — is completely shared.

Agents will find all of this second nature. The implementation should be clear to them so that it becomes a key capability in CRUX for core, extensions, and consumers — with each repo owning its own memories and not touching others.
