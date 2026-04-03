---
name: crux-skill-memory-rebalance
description: Consolidate, promote, demote, and archive memories based on strength, usage patterns, and type transition rules. Use when running REM sleep, rebalancing memory strength, detecting conflicts, or cleaning up orphaned trackers.
---

# CRUX Skill: Memory Rebalance

The complete REM sleep workflow for the CRUX memory system. Analyses all memories and their reference trackers to verify consistency, detect conflicts, recommend promotions/demotions/archival/consolidation, and apply confirmed changes.

## When to Use

Use this skill when:
- Running REM sleep (`/crux-dream --rem` or `/crux-dream --rem --yolo`)
- Manually rebalancing memory strength scores
- Investigating potential conflicts between memories
- Cleaning up orphaned tracker files or stale memories

## Prerequisites

Before any operation:

1. **Read config**: Load `.crux/crux-memories.json` and extract:
   - `cruxMemories.typeTransitions` — promotion thresholds and targets per type
   - `cruxMemories.demoteAfterDaysUnreferenced` — days before demotion (default `90`)
   - `cruxMemories.archiveAfterDaysUnreferenced` — days before archival (default `180`)
   - `cruxMemories.referenceTracking.trackingDir` — tracker file location (default `.crux/reference-tracking`)
   - `cruxMemories.referenceTracking.promotionToRuleThreshold` — reference count triggering rule promotion flag (default `30`)
   - `cruxMemories.storage.memoriesDir` — base memory directory (default `memories`)
   - `cruxMemories.storage.agentMemoriesDir` — agent-scoped memory directory (default `memories/agents`)
   - `cruxMemories.storage.archiveDir` — archive directory for REM summaries (default `.ai-ignored/executed`)
   - `cruxMemories.typePriority` — valid types in priority order
2. **Guard check**: If `flags.enableMemories` is not `"true"`, abort and inform the caller that memories are disabled

## Config Reference

All config values come from `.crux/crux-memories.json`:

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `cruxMemories.typeTransitions` | object | See below | Promotion thresholds and targets per type |
| `cruxMemories.demoteAfterDaysUnreferenced` | integer | `90` | Days without reference before demotion recommended |
| `cruxMemories.archiveAfterDaysUnreferenced` | integer | `180` | Days without reference before archival recommended |
| `cruxMemories.referenceTracking.trackingDir` | string | `.crux/reference-tracking` | Directory containing `.refs.yml` files |
| `cruxMemories.referenceTracking.promotionToRuleThreshold` | integer | `30` | Reference count that flags a memory for rule promotion |
| `cruxMemories.storage.memoriesDir` | string | `memories` | Root directory for base memories |
| `cruxMemories.storage.agentMemoriesDir` | string | `memories/agents` | Root directory for agent-scoped memories |
| `cruxMemories.storage.archiveDir` | string | `.ai-ignored/executed` | Directory for REM sleep summaries |
| `cruxMemories.typePriority` | array | `[core, redflag, goal, learning, idea, archived]` | Valid types in priority order |

### Type Transition Rules

Read from `cruxMemories.typeTransitions` in config. These are configurable per-repo — do not hard-code thresholds.

| Type | `promoteAt` | `promoteTo` | Notes |
|------|-------------|-------------|-------|
| `idea` | 5 | `learning` | Low-confidence insights that gain traction |
| `learning` | 15 | `core` | Validated learnings graduating to core knowledge |
| `redflag` | 10 | `core` | Frequently-hit warnings becoming core doctrine |
| `core` | null | — | Terminal type, no further promotion |
| `goal` | null | — | Terminal type, no further promotion |

## REM Sleep Workflow

The full REM sleep workflow executes these steps in order. Each step produces recommendations that are collected and presented together before any changes are applied.

### Step 1: Load Corpus

1. Recursively scan `memoriesDir` and `agentMemoriesDir` for all `*.memory.md` and `*.memory.crux.md` files
2. Parse frontmatter from each memory file (title, description, type, strength, created, modified, source, tags)
3. List all `*.refs.yml` files in `trackingDir`
4. Parse each tracker file (slug, references, last_referenced, strength)
5. Build a joined dataset: each memory paired with its tracker (if one exists)

### Step 2: Consistency Verification

Check for data integrity issues:

1. **Orphaned trackers**: For each `.refs.yml` file, verify a matching memory file exists (by slug). If no memory matches, flag the tracker as orphaned
2. **Stale sources**: For each memory, check if its `source` field references a unit of work that still exists. Flag if the source directory no longer exists (advisory only — does not trigger deletion)
3. **Broken strength chains**: Compare each tracker's `strength` field against the corresponding memory's frontmatter `strength`. If they differ, flag for rebalancing
4. **Missing trackers for strong memories**: Memories with `strength > 1` but no tracker file may indicate a tracking gap. Flag as advisory

**Output**: List of consistency issues found, categorized by severity.

### Step 3: Conflict Detection

Identify memories that contradict each other:

1. Compare memory titles, descriptions, and bodies pairwise for semantic contradictions:
   - Opposing advice (e.g. "always use X" vs "never use X")
   - Conflicting patterns (e.g. two memories recommending incompatible approaches to the same problem)
   - An `idea` or `learning` that directly contradicts a `core` memory
2. For each detected conflict, record:
   - The two conflicting memories (paths, titles, types, strengths)
   - A brief description of the contradiction
   - Resolution options: **keep A**, **keep B**, **merge**, **keep both with disambiguation note**

**Conflicts always require user input** — even in `--yolo` mode, conflicts are never auto-resolved.

### Step 4: Promote

For each memory, check if its `strength` (from frontmatter) meets or exceeds the `promoteAt` threshold for its current type:

1. Look up the memory's current `type` in `typeTransitions`
2. If `promoteAt` is `null`, skip (terminal type)
3. If `strength >= promoteAt`, recommend promotion to `promoteTo`

**Recommendation format**:

```
⬆️ Promote: "{title}"
   {current_type} → {promoteTo} (strength {strength} ≥ threshold {promoteAt})
   File: {current_path} → {new_path}
```

### Step 5: Demote

For each memory that has a tracker file, check temporal staleness:

1. Calculate days since `last_referenced` (from tracker)
2. If days > `demoteAfterDaysUnreferenced` (default 90) and the memory is not already `archived`:
   - If memory type is `core`, recommend demotion to `learning`
   - If memory type is `learning`, recommend demotion to `idea`
   - If memory type is `redflag`, recommend demotion to `learning`
   - If memory type is `idea`, recommend archival instead (skip to Step 6)
   - `goal` types are never demoted — flag for manual review instead

For memories with no tracker file (never referenced):
1. Calculate days since `created` (from frontmatter)
2. If days > `demoteAfterDaysUnreferenced`, recommend demotion following the same type rules

**Recommendation format**:

```
⬇️ Demote: "{title}"
   {current_type} → {demoted_type} (unreferenced for {days} days, threshold: {demoteAfterDaysUnreferenced})
   File: {current_path} → {new_path}
```

### Step 6: Archive

For memories that are stale beyond the archival threshold:

1. Calculate days since `last_referenced` (from tracker), or days since `created` if no tracker exists
2. If days > `archiveAfterDaysUnreferenced` (default 180) and the memory is not already `archived`:
   - Recommend moving to the `archived/` type directory

**Recommendation format**:

```
📦 Archive: "{title}"
   {current_type} → archived (unreferenced for {days} days, threshold: {archiveAfterDaysUnreferenced})
   File: {current_path} → {new_path}
```

### Step 7: Consolidate

Detect duplicate or near-duplicate memories that should be merged:

1. Compare memory titles, descriptions, tags, and bodies for semantic similarity
2. Flag pairs that cover the same concept, technique, or pattern with substantially overlapping content
3. For each duplicate pair, recommend merging:
   - Combined body content (keep the more detailed version as base, incorporate unique points from the other)
   - Combined strength: sum of both strengths
   - Tags: union of both tag sets
   - Type: keep the higher-priority type (per `typePriority`)
   - Delete the merged-away memory and its tracker

**Recommendation format**:

```
🔀 Consolidate: "{title_a}" + "{title_b}"
   Keep: {path_a} ({type_a}, strength {strength_a})
   Merge into it: {path_b} ({type_b}, strength {strength_b})
   Combined strength: {sum}
```

### Step 8: Rebalance Strength

Sync strength scores between memory frontmatter and tracker files:

1. For each memory with a tracker, compare frontmatter `strength` with tracker `strength`
2. The memory frontmatter is authoritative — if they differ, update the tracker
3. Report any corrections made

### Step 9: Promote to Rule

Flag memories that exceed the `promotionToRuleThreshold` for potential conversion to a permanent rule:

1. For each tracker where `references >= promotionToRuleThreshold` (default 30):
   - Flag the corresponding memory for rule promotion

**Recommendation format**:

```
⚡ Promote to rule: "{title}"
   Referenced {references} times (threshold: {promotionToRuleThreshold})
   Consider creating a permanent rule in .cursor/rules/
```

This is advisory — the user decides whether to create the rule. This skill does not automatically create rules.

### Step 10: Cleanup

Identify orphaned tracker files (from Step 2) and recommend deletion:

```
🧹 Cleanup: {slug}.refs.yml
   No matching memory file found — recommend deletion
```

### Step 11: Present Recommendations

Collect all recommendations from steps 2–10 and present them to the user in a structured report:

```
=== REM Sleep Analysis ===

📋 Consistency Issues: {count}
{list of issues from Step 2}

⚠️ Conflicts: {count} (require manual resolution)
{list of conflicts from Step 3}

⬆️ Promotions: {count}
{list from Step 4}

⬇️ Demotions: {count}
{list from Step 5}

📦 Archival: {count}
{list from Step 6}

🔀 Consolidations: {count}
{list from Step 7}

🔄 Strength Rebalances: {count}
{list from Step 8}

⚡ Rule Promotion Candidates: {count}
{list from Step 9}

🧹 Cleanup: {count}
{list from Step 10}

Apply all recommendations? [all/select/skip]
```

**In `--yolo` mode**: Auto-apply everything EXCEPT conflicts (Step 3). Conflicts always require user input.

**In interactive mode**: Present the full report and wait for user confirmation. Options:
- **all**: Apply all non-conflict recommendations; then prompt for each conflict individually
- **select**: Walk through each recommendation individually for accept/reject
- **skip**: Abort without changes

### Step 12: Apply Changes

Execute confirmed changes. For each approved recommendation:

#### Moving Files (Promote, Demote, Archive)

1. Determine the new target directory based on scope and new type:
   - Base memory: `{memoriesDir}/{new_type}/`
   - Agent-scoped memory: `{agentMemoriesDir}/{agent-id}/{new_type}/`
2. Create target directory if needed
3. Move the memory file to the new directory
4. Update frontmatter:
   - Set `type` to the new type
   - Add `promoted_from` (for promotions) or `demoted_from` (for demotions) with the old type value
   - Set `modified` to today's date
5. If a compressed version exists (`.memory.crux.md` alongside `.memory.md`, or vice versa), move that too
6. The reference tracker file stays in `trackingDir` — trackers reference by slug, not path, so no tracker update is needed for file moves

#### Merging (Consolidate)

1. Read both memory files
2. Compose merged content:
   - Use the higher-priority memory as the base
   - Incorporate unique content from the other memory
   - Sum the strengths
   - Union the tag sets
   - Keep the earlier `created` date
   - Set `modified` to today
3. Write the merged file (using `crux-skill-memory-crud` Update operation)
4. Delete the merged-away memory file
5. If the merged-away memory has a tracker, merge its reference counts into the surviving tracker (sum `references`, keep the more recent `last_referenced`, combine `recent_references` and re-cap to `maxReferencesStored`)
6. Delete the merged-away tracker

#### Strength Rebalance

1. Read the memory file's frontmatter `strength`
2. Write that value into the tracker file's `strength` field

#### Cleanup

1. Delete orphaned tracker files confirmed for removal

### Step 13: Write REM Summary

After all changes are applied, write a summary to `{archiveDir}/rem-{yyyymmdd}.md`:

```markdown
# REM Sleep Summary — {YYYY-MM-DD}

## Changes Applied

### Promotions ({count})
- "{title}": {old_type} → {new_type}

### Demotions ({count})
- "{title}": {old_type} → {new_type}

### Archived ({count})
- "{title}": {old_type} → archived

### Consolidated ({count})
- "{title_a}" + "{title_b}" → "{surviving_title}"

### Strength Rebalanced ({count})
- "{title}": tracker strength {old} → {new}

### Conflicts Resolved ({count})
- "{title_a}" vs "{title_b}": {resolution}

### Cleaned Up ({count})
- {slug}.refs.yml (orphaned)

### Rule Promotion Candidates ({count})
- "{title}" ({references} references)

## Skipped
- {list of recommendations user declined}

## Corpus Summary
- Total memories: {count}
- By type: core={n}, redflag={n}, goal={n}, learning={n}, idea={n}, archived={n}
- Tracked (with .refs.yml): {count}
- Untracked: {count}
```

### Step 14: Report

Present a concise summary of what changed to the user.

## File Move Procedure (Detailed)

When a memory transitions between types, follow this exact procedure:

1. **Resolve scope**: Determine if the memory is base-scoped or agent-scoped by examining its current path
   - Path starts with `{agentMemoriesDir}` → agent-scoped; extract `{agent-id}` from path
   - Otherwise → base-scoped
2. **Build target path**:
   - Base: `{memoriesDir}/{new_type}/{slug}.memory.md` (or `.memory.crux.md`)
   - Agent: `{agentMemoriesDir}/{agent-id}/{new_type}/{slug}.memory.md` (or `.memory.crux.md`)
3. **Create target directory** if it does not exist
4. **Move the file** to the target path
5. **Update frontmatter** in-place after the move:
   - `type` → new type value
   - `promoted_from` or `demoted_from` → old type value
   - `modified` → today's date (`YYYY-MM-DD`)
6. **Handle compressed companion**: If a `.memory.crux.md` exists for a `.memory.md` being moved (or vice versa), move the companion file to the same target directory and update its frontmatter identically
7. **No tracker update needed**: Tracker files in `trackingDir` reference memories by `slug`, not by path. Moving a memory file does not break the tracker association

## Integration

| Component | Location | Role |
|-----------|----------|------|
| Config | `.crux/crux-memories.json` | `typeTransitions`, `demoteAfterDaysUnreferenced`, `archiveAfterDaysUnreferenced`, `referenceTracking`, `storage` |
| Memory CRUD | `.cursor/skills/crux-skill-memory-crud/SKILL.md` | Frontmatter updates, file moves, type transitions |
| Reference Tracker | `.cursor/skills/crux-skill-memory-reference-tracker/SKILL.md` | Tracker file format, strength sync, cleanup |
| Memory Compress | `.cursor/skills/crux-skill-memory-compress/SKILL.md` | Compressed file handling during moves |
| Memory Index | `.cursor/skills/crux-skill-memory-index/SKILL.md` | Index rebuild after rebalance (called post-REM) |

## Error Handling

| Condition | Action |
|-----------|--------|
| `enableMemories` is not `"true"` | Abort, inform caller memories are disabled |
| Config file missing or malformed | Report error with path and expected structure |
| Memory file cannot be read or parsed | Skip that memory, report in consistency issues |
| Target directory cannot be created | Abort the specific move, report filesystem error |
| Conflict between two memories | Always present to user, never auto-resolve |
| Strength exceeds `promoteAt` but `promoteTo` is not in `typePriority` | Skip promotion, report config issue |
| File move would overwrite an existing file | Prompt user before overwriting |

## What This Skill Does NOT Do

- Does not create new memories (that is `crux-skill-memory-crud`)
- Does not compress or decompress memory bodies (that is `crux-skill-memory-compress`)
- Does not record new references (that is `crux-skill-memory-reference-tracker`)
- Does not rebuild the memory index (that is `crux-skill-memory-index`, called after REM completes)
- Does not automatically create rules from promoted memories — it only flags candidates
- Does not modify `created` dates on any memory
