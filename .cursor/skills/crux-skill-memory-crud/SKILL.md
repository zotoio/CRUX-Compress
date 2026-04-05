---
name: crux-skill-memory-crud
description: Create, read, update, delete, and validate memory files with proper frontmatter management. Use when creating new memories, modifying existing ones, removing memories, or validating memory file structure.
---

# CRUX Memory CRUD

Provides create, read, update, delete, and validate operations for CRUX memory files stored under `memories/`.

## When to Use

Use this skill whenever you need to:
- Create a new memory file from an extracted insight
- Read and parse an existing memory's frontmatter and body
- Update a memory's metadata or content (e.g. type promotion, strength change)
- Delete a memory and its reference tracker
- Validate a memory file against the required schema

## Configuration

All configuration lives in `.crux/crux-memories.json` under the `cruxMemories` key. Key settings:

| Setting | Default | Purpose |
|---------|---------|---------|
| `storage.memoriesDir` | `memories` | Root directory for base memories |
| `storage.agentMemoriesDir` | `memories/agents` | Root directory for agent-scoped memories |
| `sizeUnit` | `"lines"` | Unit for size thresholds — `"lines"` or `"bytes"` |
| `compressionMinLines` | 500 | Minimum file size in lines before compression is considered |
| `maxMemorySize` | 1000 | Maximum memory file size in lines (default) |
| `referenceTracking.trackingDir` | `.crux/reference-tracking` | Reference tracker location |
| `typePriority` | `[core, redflag, goal, learning, idea, archived]` | Valid memory types in priority order |

## Memory Frontmatter Schema

Every memory file must have YAML frontmatter with these fields:

### Required Fields

| Field | Type | Rules |
|-------|------|-------|
| `id` | string | 7-character hex hash, generated once at creation from `sha256(title)[:7]`. Immutable — never changes even if the title is edited. Used as the stable short identifier for display and selection. |
| `title` | string | Descriptive title conveying the key insight |
| `description` | string | Self-contained summary — enough to act on without reading the body |
| `type` | enum | One of: `core`, `redflag`, `goal`, `learning`, `idea`, `archived` |
| `strength` | integer | Starts at `1` for new memories; incremented on reinforcement |
| `created` | date | ISO date (`YYYY-MM-DD`); set once at creation, never modified |
| `modified` | date | ISO date (`YYYY-MM-DD`); updated on every write |
| `source` | string | Slug of the originating spec or session (e.g. `20260403-component-library`) |
| `tags` | list | Array of lowercase tag strings for categorization |

### Optional Fields

| Field | Type | Rules |
|-------|------|-------|
| `promoted_from` | string | Previous type before a type transition; set automatically on promotion/demotion |
| `consolidated_from` | list | List of original memory `id` values when this memory was created by merging multiple memories during REM sleep consolidation. Set once, never modified. |
| `consolidation_topic` | string | Shared slug identifying the topic across multi-volume consolidated memories (e.g. `plugin-architecture`). All volumes for the same topic share this value. Set during consolidation when splitting is needed. |
| `consolidation_part` | integer | Volume number within a multi-volume consolidated topic (1-indexed). Only present when `consolidation_topic` is set and the topic spans multiple files. |

### Example Frontmatter

```yaml
---
id: "a1b2c3d"
title: "Always validate CRUX checksums before overwriting"
description: "Source files can drift from their CRUX output. Always recompute and compare sourceChecksum before regenerating to avoid silent data loss."
type: "learning"
strength: 1
created: 2026-04-03
modified: 2026-04-03
source: "20260403-crux-memories"
tags: [crux, validation, checksums]
---
```

## File Naming and Placement

### File Names

- Uncompressed: `{slug}.memory.md`
- Compressed: `{slug}.memory.crux.md`

Slugs are lowercase, hyphen-separated, descriptive (e.g. `validate-checksums-before-overwrite`).

### Directory Placement

| Scope | Path |
|-------|------|
| Base memory | `memories/{type}/{slug}.memory.md` |
| Agent-scoped memory | `memories/agents/{agent-id}/{type}/{slug}.memory.md` |

Examples:
- `memories/learning/validate-checksums-before-overwrite.memory.md`
- `memories/agents/crux-cursor-rule-manager/core/compression-ratio-thresholds.memory.md`

## Operations

### Create

Create a new memory file.

**Inputs**: title, description, type, source, tags, body content, and optionally agent-id for scoping.

**Procedure**:

1. Load config from `.crux/crux-memories.json`
2. Validate `type` is one of the allowed types in `typePriority`
3. Generate slug from title (lowercase, replace spaces/special chars with hyphens, truncate to reasonable length)
4. Generate `id` by computing `sha256(title)` and taking the first 7 hex characters. If a collision exists with another memory, extend to 8 characters.
5. Build frontmatter with all required fields:
   - `id`: the generated hash
   - `strength`: `1`
   - `created`: today's date
   - `modified`: today's date
6. Compose the full file: frontmatter + body content
7. Check file size against `maxMemorySize` (default 1000 lines). If exceeded, warn the user and suggest trimming the body or compressing
8. Determine target directory:
   - If agent-id provided: `memories/agents/{agent-id}/{type}/`
   - Otherwise: `memories/{type}/`
9. Create parent directories if needed
10. Write `{slug}.memory.md` to the target directory
11. Return the file path and `id`

### Read

Load and parse an existing memory file.

**Inputs**: file path or slug (with optional type/scope hints for slug resolution).

**Procedure**:

1. If given a slug, resolve to a file path by searching `memories/` recursively for `{slug}.memory.md` or `{slug}.memory.crux.md`
2. Read the file
3. Split on the frontmatter delimiters (`---`)
4. Parse the YAML frontmatter into structured fields
5. Return frontmatter fields and body content separately

### Update

Modify a memory's frontmatter or body.

**Inputs**: file path or slug, fields to update, and optionally new body content.

**Procedure**:

1. Read the existing memory (use the Read operation)
2. Apply field updates to the frontmatter. Enforce these rules:
   - `id` — **never** modify this field; it is immutable after creation
   - `created` — **never** modify this field; reject any attempt to change it
   - `modified` — always set to today's date
   - `type` — if changed, handle type transition (see below)
   - `strength` — accept new value; no automatic changes here
3. If `type` has changed:
   a. Set `promoted_from` to the old type value
   b. Determine new target directory based on scope and new type
   c. Create new target directory if needed
   d. Move the file from old location to new location
4. If body content is provided, replace the body
5. Recompose and write the updated file
6. Check file size against `maxMemorySize`; warn if exceeded
7. Return the (possibly new) file path

### Delete

Remove a memory file and its reference tracker.

**Inputs**: file path or slug.

**Procedure**:

1. Resolve the file path (if given a slug, use the Read resolution logic)
2. Extract the slug from the filename (strip `.memory.md` or `.memory.crux.md`)
3. Delete the memory file
4. Check for a corresponding reference tracker at `{trackingDir}/{slug}.refs.yml` (where `trackingDir` comes from config, default `.crux/reference-tracking/`)
5. If the tracker file exists, delete it
6. Return confirmation of what was deleted

### Validate

Check a memory file against the required schema.

**Inputs**: file path or slug.

**Procedure**:

1. Read the memory file (use the Read operation)
2. Check all required frontmatter fields are present:
   - `id`, `title`, `description`, `type`, `strength`, `created`, `modified`, `source`, `tags`
3. Check field types:
   - `id` must be a 7-character (or 8 on collision) lowercase hex string
   - `type` must be one of: `core`, `redflag`, `goal`, `learning`, `idea`, `archived`
   - `strength` must be a positive integer
   - `created` and `modified` must be valid ISO dates
   - `tags` must be a list
   - `title` and `description` must be non-empty strings
4. Check file size against `maxMemorySize`
5. Check that the file is in the correct type subdirectory for its `type` field
6. Report all errors and warnings found. Return a pass/fail result with details

## What NOT to Do

- Do not modify `id` or `created` on updates — both are immutable after creation
- Do not set `strength` to anything other than `1` on new memories
- Do not write memory files outside the `memories/` directory tree
- Do not delete reference trackers without also deleting the memory
- Do not silently exceed `maxMemorySize` — always warn the user
- Do not create memories when the feature flag `enableMemories` is `false` in config without notifying the user
