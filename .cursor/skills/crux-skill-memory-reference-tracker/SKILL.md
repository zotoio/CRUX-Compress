---
name: crux-skill-memory-reference-tracker
description: Track which memories are referenced in agent output, manage .refs.yml tracker files, and keep strength counters in sync with memory frontmatter. Use when recording a memory reference, cleaning up orphaned trackers during REM sleep, or checking whether a memory should be promoted to a permanent rule.
---

# CRUX Skill: Memory Reference Tracker

Manages per-memory reference tracking files (`.refs.yml`) in the configured `trackingDir`. Tracker files are the single source of truth for how often, how recently, and by whom a memory was referenced. Memory frontmatter stays clean — it stores *what* a memory is, not *how often* it is used.

## Config

All settings live in `.crux/crux-memories.json` under `cruxMemories.referenceTracking`:

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `enabled` | boolean | `true` | Master switch for reference tracking |
| `trackingDir` | string | `.crux/reference-tracking` | Directory for `.refs.yml` files |
| `indicateInOutput` | boolean | `true` | Whether agents annotate output when influenced by a memory |
| `indicatorFormat` | string | `[memory:{title}]` | Format string for output annotations (`{title}` is replaced with the memory title) |
| `promotionToRuleThreshold` | integer | `30` | Total reference count that flags a memory for promotion to a permanent rule |
| `maxReferencesStored` | integer | `10` | Maximum entries in `recent_references` (oldest evicted when cap exceeded) |

Additionally, `cruxMemories.unitOfWork` (e.g. `spec`) determines the key name used in `recent_references` source entries.

## Operations

### 1. Record Reference

**When**: An agent's output is influenced by a memory.

**Steps**:

1. Read config from `.crux/crux-memories.json`. If `referenceTracking.enabled` is `false`, skip all tracking.
2. Determine the memory slug from the memory filename (strip `.memory.md` or `.memory.crux.md` suffix and any path prefix).
3. Look for `{trackingDir}/{slug}.refs.yml`.
   - **If it does not exist** — create it (see [Lazy Creation](#3-lazy-creation)).
   - **If it exists** — read and update it.
4. Increment the `references` counter by 1.
5. Set `last_referenced` to today's date (`YYYY-MM-DD`).
6. Update `recent_references` (see [Manage Recent References](#4-manage-recent-references)).
7. Sync `strength` from the memory file's frontmatter into the tracker (see [Sync Strength](#5-sync-strength)).
8. Write the updated tracker file.
9. Check whether `references` now exceeds `promotionToRuleThreshold` (see [Promotion Flag](#7-promotion-to-rule-flag)).

### 2. Indicate in Output

**When**: `referenceTracking.indicateInOutput` is `true` and an agent's output is influenced by a memory.

**Instruction to agents**: When your response is influenced by a loaded memory, include the configured indicator in your output. The default format is `[memory:{title}]`, where `{title}` is replaced with the memory's `title` frontmatter field.

Example with default format:

```
The list component should use React.memo with a custom comparator
that checks item ID and version rather than deep-equaling props.
[memory:React.memo on list item components prevents full re-render on data changes]
```

When `indicateInOutput` is `false`, do not add any annotation — still record the reference via the tracker, but omit the visible indicator.

### 3. Lazy Creation

Tracker files are created on first reference. Unreferenced memories have no tracker file and incur zero overhead.

**When creating a new tracker file**:

1. Read the memory file's frontmatter to get the current `strength` value.
2. Determine the source identifier:
   - If operating within a unit of work (e.g. a spec), use `{unitOfWork}: "{id}"` (e.g. `spec: "20260403-crux-memories"`).
   - If in a standalone conversation, use `conversation_id: "{id}"`.
3. Write the new `.refs.yml` file:

```yaml
# Managed by crux-skill-memory-reference-tracker — do not edit manually
slug: {slug}
references: 1
last_referenced: {YYYY-MM-DD}
strength: {strength from memory frontmatter}
recent_references:
  - {unitOfWork}: "{source-id}"
    count: 1
    last: {YYYY-MM-DD}
```

If the agent has context about how the memory was used, add `context: "brief description"` to the entry.

### 4. Manage Recent References

The `recent_references` list is a **capped, sorted** list of the top referrers for this memory.

**Update logic**:

1. Determine the current source:
   - Within a unit of work → key is the configured `unitOfWork` value (e.g. `spec`), value is the work ID.
   - Standalone conversation → key is `conversation_id`, value is the conversation ID.
2. Search `recent_references` for an existing entry matching the source.
   - **If found**: increment its `count`, update its `last` date. If context is available and the entry lacks one, add it.
   - **If not found**: append a new entry with `count: 1`, `last: {today}`, and optional `context`.
3. Sort the list by `count` descending (highest referrer first).
4. If the list exceeds `maxReferencesStored`, remove entries from the tail (lowest count).

**Entry format**:

```yaml
- spec: "20260403-component-library"    # key matches unitOfWork config
  count: 5
  last: 2026-04-03
  context: "Applied memoization pattern to data grid component"
```

Or for standalone conversations:

```yaml
- conversation_id: "a3f7b2c"
  count: 3
  last: 2026-03-30
  context: "Discussed memoization strategy for data table components"
```

### 5. Sync Strength

The tracker file's `strength` field must stay in sync with the memory frontmatter's `strength` field. The memory frontmatter is the authoritative source.

**When recording a reference**:

1. Read the memory file's frontmatter `strength` value.
2. Write that value into the tracker file's `strength` field.

This ensures the tracker always reflects the current strength, even if another skill (e.g. `crux-skill-memory-rebalance`) has modified the memory's strength since the last reference.

### 6. Cleanup (REM Sleep)

**When**: Called during REM sleep (`/crux-dream --rem`).

**Steps**:

1. List all `*.refs.yml` files in `trackingDir`.
2. For each tracker file, extract the `slug`.
3. Search the memory directories (configured `memoriesDir` and `agentMemoriesDir`, recursively) for a matching `{slug}.memory.md` or `{slug}.memory.crux.md` file.
4. If no matching memory file exists, the tracker is **orphaned** — recommend it for deletion.
5. Present orphaned trackers to the user (or auto-delete in `--yolo` mode).
6. Delete confirmed orphaned tracker files.

### 7. Promotion to Rule Flag

**When**: After updating a tracker, `references` exceeds `promotionToRuleThreshold`.

**Action**: Flag the memory for potential promotion to a permanent Cursor rule (`.cursor/rules/*.mdc`).

Report to the user:

```
⚡ Memory "{title}" has been referenced {references} times
   (threshold: {promotionToRuleThreshold}).
   Consider promoting it to a permanent rule in .cursor/rules/
```

This flag is advisory — the user decides whether to promote. The skill does not automatically create rules.

## `.refs.yml` File Format

Every tracker file follows this exact structure:

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

| Field | Type | Description |
|-------|------|-------------|
| `slug` | string | Memory slug — matches the filename stem, stable identifier |
| `references` | integer | Total reference count across all sessions and sources |
| `last_referenced` | date | Date of most recent reference (`YYYY-MM-DD`) |
| `strength` | integer | Current strength score, synced from memory frontmatter |
| `recent_references` | list | Top N referrers sorted by `count` descending (capped by `maxReferencesStored`) |

**`recent_references` entry fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `{unitOfWork}` or `conversation_id` | string | Yes | Source identifier — key name matches config `unitOfWork` (e.g. `spec`) or `conversation_id` for standalone sessions |
| `count` | integer | Yes | Number of references from this source |
| `last` | date | Yes | Date of most recent reference from this source |
| `context` | string | No | Brief description of how the memory was used |

## Design Rationale

- **Per-memory files**: Zero contention — concurrent sessions referencing different memories write to different files.
- **Externalised from memory frontmatter**: Memory files describe *what* a memory is, not *how often* it's used. Keeps memory files clean and diffable.
- **Lazy creation**: Unreferenced memories have no tracker file and no overhead.
- **Capped recent_references**: Prevents unbounded growth while preserving the most significant referrers.
- **Sorted by count**: The most frequent referrer is always first, making it easy to identify primary use patterns.

## Prerequisites

- `.crux/crux-memories.json` must exist with a valid `referenceTracking` config block.
- The `trackingDir` directory must exist (created by config scaffolding, subtask 01).
- Memory files must follow the naming convention `{slug}.memory.md` or `{slug}.memory.crux.md`.

## What This Skill Does NOT Do

- Does not create or modify memory files (that is `crux-skill-memory-crud`).
- Does not promote or demote memories between types (that is `crux-skill-memory-rebalance`).
- Does not build the memory index (that is `crux-skill-memory-index`).
- Does not automatically create rules from promoted memories — it only flags them.
