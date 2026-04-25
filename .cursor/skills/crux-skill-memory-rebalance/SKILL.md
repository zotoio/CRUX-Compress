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
   - `flags.enableMemoryCompression` — whether compression is enabled (default `"false"`)
   - `flags.enableMemoryConsolidation` — whether consolidation is enabled (default `"false"`)
   - `cruxMemories.compressionTarget` — target compressed size as % of original (default `33`)
   - `cruxMemories.sizeUnit` — unit for size thresholds (default `"lines"`)
   - `cruxMemories.compressionMinLines` — minimum file size in lines before compression is considered (default `500`)
   - `cruxMemories.maxMemorySize` — hard cap on memory file size in lines (default `1000`)
   - `cruxMemories.maxConsolidatedSize` — hard cap on consolidated memory file size in lines (default `2000`)
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
| `flags.enableMemoryCompression` | string | `"false"` | Feature gate for compression during REM sleep |
| `flags.enableMemoryConsolidation` | string | `"false"` | Feature gate for consolidation during REM sleep |
| `cruxMemories.compressionTarget` | number | `33` | Target compressed size as % of original body |
| `cruxMemories.sizeUnit` | string | `"lines"` | Unit for size thresholds — `"lines"` or `"bytes"` |
| `cruxMemories.compressionMinLines` | number | `500` | Minimum file size in lines before CRUX compression is considered; files below this are left uncompressed |
| `cruxMemories.maxMemorySize` | number | `1000` | Hard cap on memory file size in lines (default); files exceeding this must be compressed |
| `cruxMemories.maxConsolidatedSize` | number | `2000` | Hard cap on consolidated memory file size in lines (default); exceeding triggers volume splitting |

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

If `flags.enableMemoryConsolidation` is not `"true"`, skip this step entirely.

Group related memories by subject matter and merge each group into a single compressed memory. This reduces corpus size while preserving all unique insights.

#### 7a. Identify Consolidation Groups

Cluster memories that cover the same domain or subject area:

1. **Tag overlap**: Memories sharing ≥50% of their tags are candidates for the same group
2. **Type affinity**: Memories of the same type are preferred grouping partners — group same-type memories first, only cross-type when the subject overlap is strong
3. **Title/description similarity**: Memories whose titles or descriptions reference the same concept, pattern, technique, or domain
4. **Source affinity**: Memories originating from the same `source` (spec/session) that cover facets of the same subject
5. **Body content**: Overlapping or complementary body content (e.g. two memories about plugin architecture with different specific lessons)

A memory may only belong to one consolidation group. Groups must contain at least 2 memories. Memories with no strong affinity to others remain standalone.

#### 7b. Build Consolidated Metadata

For each group, compose shared metadata from the member memories:

| Field | Rule |
|-------|------|
| `id` | New 7-character hex hash from `sha256(new_title)[:7]` |
| `title` | New title that captures the shared subject across all members — concise but covering the group's scope |
| `description` | New self-contained summary synthesising the key insights from all members — not a concatenation, but a coherent combined description |
| `type` | Highest-priority type in the group (per `typePriority`) |
| `strength` | Sum of all member strengths |
| `created` | Earliest `created` date from the group |
| `modified` | Today's date |
| `source` | Most frequently occurring source in the group; if tied, earliest |
| `tags` | Union of all member tag sets, deduplicated |
| `consolidated_from` | List of original memory `id` values (for audit trail) |

#### 7c. Calculate Combined Size and Split Volumes

1. Combine the body content from all members into a single merged body, preserving all unique insights and removing redundant content
2. Measure the combined body size in the configured `sizeUnit` (default: lines)
3. Determine whether the output fits within `maxConsolidatedSize` (default `1000` lines):
   - If `enableMemoryCompression` is `"true"`: estimate whether `compressionTarget`% of the combined body fits within `maxConsolidatedSize`
   - If compression is disabled: check whether the combined body fits within `maxConsolidatedSize` uncompressed
4. **If within limit**: the group produces a single consolidated file
5. **If exceeds limit**: split into multiple volumes (see [7e. Volume Splitting](#7e-volume-splitting))

#### 7d. Detect Existing Consolidated Topics

Before creating new consolidation groups, scan for existing multi-volume consolidated memories (files with `consolidation_topic` in frontmatter):

1. For each existing consolidated topic, check whether any new ungrouped memories belong to it (using the same affinity criteria from 7a)
2. If new memories match an existing topic:
   - Estimate whether adding them to an existing volume would keep that volume under `maxConsolidatedSize`
   - If yes: recommend adding to the existing volume (decompress, merge content, recompress)
   - If no: recommend creating a new volume for the topic and rebalancing content across all volumes (see [7f. Volume Rebalancing](#7f-volume-rebalancing))
3. Track the `consolidation_topic` slug and next available `consolidation_part` number

#### 7e. Volume Splitting

When a consolidation group's combined content exceeds `maxConsolidatedSize`:

1. Assign a `consolidation_topic` slug derived from the group's shared subject (e.g. `plugin-architecture`)
2. Partition the merged body into coherent sub-topics — each sub-topic becomes a volume. Split by semantic boundaries, not arbitrary byte offsets:
   - Group related insights, patterns, and examples together
   - Each volume should be independently understandable
   - Aim for roughly equal volume sizes, each within `maxConsolidatedSize`
3. Number volumes sequentially: `consolidation_part: 1`, `consolidation_part: 2`, etc.
4. Each volume gets its own `id` (hash from `"{topic} part {n}"`) but shares the same `consolidation_topic`, `type`, `tags`, and `consolidated_from` (full list of all source IDs across the topic)
5. Each volume gets its own `title` and `description` reflecting its specific sub-topic content
6. File naming: `{topic}-pt{n}.memory.crux.md` (e.g. `plugin-architecture-pt1.memory.crux.md`)

#### 7f. Volume Rebalancing

When existing multi-volume topics change (new memories added, members demoted/archived, or volumes become uneven):

1. Load all volumes for the topic (by `consolidation_topic` match)
2. Decompress all volumes to get the full combined content
3. Assess whether rebalancing is needed:
   - A volume exceeds `maxConsolidatedSize`
   - A volume is less than 25% of `maxConsolidatedSize` (under-filled)
   - Volumes could be reduced (total content now fits in fewer volumes)
4. If rebalancing is needed:
   - Re-partition all content across the optimal number of volumes, each within `maxConsolidatedSize`
   - Reassign `consolidation_part` numbers sequentially
   - Update each volume's `title` and `description` to reflect its new content
   - If volumes were reduced (e.g. 3 → 2), delete the surplus volume files and their trackers
5. Present rebalancing as a recommendation alongside new consolidations

**Recommendation format for rebalancing**:

```
🔀 Rebalance topic "{consolidation_topic}": {old_count} → {new_count} volumes
   Reason: {volume exceeds cap | under-filled volume | reducible}
   Volumes: {list of volume paths with current and projected sizes}
```

#### 7g. Present Recommendations

For each consolidation group, present the proposed merge:

**Single-volume group**:

```
🔀 Consolidate ({n} memories): "{new_title}"
   Members:
   - {path_a} "{title_a}" ({type_a}, strength {strength_a})
   - {path_b} "{title_b}" ({type_b}, strength {strength_b})
   - {path_c} "{title_c}" ({type_c}, strength {strength_c})
   Combined strength: {sum}
   Combined size: {total_lines} lines → est. {compressed_lines} lines compressed
   Tags: {union_of_tags}
   Output: {target_dir}/{new_slug}.memory.crux.md
```

**Multi-volume group** (exceeds `maxConsolidatedSize`):

```
🔀 Consolidate ({n} memories) into {v} volumes: topic "{consolidation_topic}"
   Members:
   - {path_a} "{title_a}" ({type_a}, strength {strength_a})
   - {path_b} "{title_b}" ({type_b}, strength {strength_b})
   - ...
   Combined strength: {sum}
   Tags: {union_of_tags}
   Volume 1: "{vol1_title}" — est. {vol1_lines} lines compressed
   Volume 2: "{vol2_title}" — est. {vol2_lines} lines compressed
   Output: {target_dir}/{topic}-pt1.memory.crux.md, ...
```

### Step 8: Compress Uncompressed Memories

When `flags.enableMemoryCompression` is `"true"`, detect remaining uncompressed `.memory.md` files that should be compressed individually:

1. From the corpus loaded in Step 1, identify all `.memory.md` files that do **not** have a corresponding `.memory.crux.md` companion
2. Exclude memories that are part of a consolidation group from Step 7 — those are already compressed as part of the merge
3. **Skip files below `compressionMinLines`** (default `500` lines) — these are too small to benefit from compression
4. For remaining files, estimate whether they exceed `maxMemorySize` (in the configured `sizeUnit`) or would benefit from compression to meet `compressionTarget`
5. Recommend compression only for files that meet the minimum size threshold

**Recommendation format**:

```
🗜️ Compress: "{title}"
   File: {path} ({size} lines)
   Target: {compressionTarget}% of body, max {maxMemorySize} lines
```

If `flags.enableMemoryCompression` is not `"true"`, skip this step entirely — do not recommend compression.

**Apply**: Delegate each confirmed compression to `crux-skill-memory-compress` Compress operation. The compress skill handles archival of the original, adaptive sizing, and writing the `.memory.crux.md` output.

### Step 9: Rebalance Strength

Sync strength scores between memory frontmatter and tracker files:

1. For each memory with a tracker, compare frontmatter `strength` with tracker `strength`
2. The memory frontmatter is authoritative — if they differ, update the tracker
3. Report any corrections made

### Step 10: Promote to Rule

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

### Step 11: Cleanup

Identify orphaned tracker files (from Step 2) and recommend deletion:

```
🧹 Cleanup: {slug}.refs.yml
   No matching memory file found — recommend deletion
```

### Step 12: Present Recommendations

Collect all recommendations from steps 2–11 and present them to the user in a structured report:

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

🔀 Consolidations: {count} groups ({total_merged} memories)
{list from Step 7g}

📚 Volume Rebalances: {count} topics
{list from Step 7f}

🗜️ Compressions: {count}
{list from Step 8}

🔄 Strength Rebalances: {count}
{list from Step 9}

⚡ Rule Promotion Candidates: {count}
{list from Step 10}

🧹 Cleanup: {count}
{list from Step 11}

Apply all recommendations? [all/select/skip]
```

**In `--yolo` mode**: Auto-apply everything EXCEPT conflicts (Step 3). Conflicts always require user input.

**In interactive mode**: Present the full report and wait for user confirmation. Options:
- **all**: Apply all non-conflict recommendations; then prompt for each conflict individually
- **select**: Walk through each recommendation individually for accept/reject
- **skip**: Abort without changes

### Step 13: Apply Changes

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

#### Merging (Consolidate) — Single Volume

For each confirmed consolidation group that fits within `maxConsolidatedSize`:

1. **Read all member memories** in the group (both `.memory.md` and `.memory.crux.md` — decompress any compressed members first)
2. **Compose merged body**: Synthesise a single body from all members. Preserve all unique insights, patterns, and examples. Remove redundant or overlapping content. Organise logically (not as a concatenation)
3. **Build consolidated frontmatter** per Step 7b rules — new `id`, shared `title`, synthesised `description`, union `tags`, summed `strength`, earliest `created`, `consolidated_from` listing all original `id` values
4. **Write the merged file** as `{new_slug}.memory.md` using `crux-skill-memory-crud` Create operation, placed in `{memoriesDir}/{type}/` (using the highest-priority type from the group)
5. **Compress the merged file**: If `enableMemoryCompression` is `"true"`, delegate to `crux-skill-memory-compress` Compress operation. The compress skill handles adaptive sizing against `maxConsolidatedSize`, source archival of the merged uncompressed file, and writing the final `.memory.crux.md` output
6. **Archive source memories**: Copy each original member memory file to `{compressionSourceArchive}/{yyyymmdd}/` before deletion
7. **Delete merged-away memories**: Remove all original member memory files from the working directory
8. **Merge reference trackers**: For all members that have tracker files, merge into a single tracker for the new memory slug:
   - Sum `references` across all member trackers
   - Keep the most recent `last_referenced`
   - Combine `recent_references` lists and re-cap to `maxReferencesStored`
   - Write the merged tracker as `{new_slug}.refs.yml`
9. **Delete merged-away trackers**: Remove all original member tracker files

#### Merging (Consolidate) — Multi-Volume

For each confirmed consolidation group that exceeds `maxConsolidatedSize`:

1. **Read all member memories** in the group (decompress any compressed members)
2. **Partition content** into volumes per Step 7e — split by semantic boundaries, each volume independently understandable, each within `maxConsolidatedSize`
3. **For each volume**, build frontmatter:
   - `id`: hash from `"{consolidation_topic} part {n}"`
   - `title` and `description`: specific to that volume's sub-topic content
   - `type`, `tags`, `strength`: shared across volumes (strength divided proportionally by content size, minimum 1 per volume)
   - `created`: earliest `created` from the full group
   - `consolidated_from`: full list of all source `id` values (shared across all volumes)
   - `consolidation_topic`: shared slug for the topic
   - `consolidation_part`: volume number (1-indexed)
4. **Write each volume** as `{topic}-pt{n}.memory.md` in `{memoriesDir}/{type}/`
5. **Compress each volume**: If `enableMemoryCompression` is `"true"`, delegate each to `crux-skill-memory-compress` (adaptive sizing against `maxConsolidatedSize`)
6. **Archive and delete source memories** (same as single-volume steps 6–7)
7. **Distribute reference trackers**: Create a tracker for each volume slug. Distribute reference counts proportionally by content size across volumes (minimum 1 reference per volume if source total > 0). Each tracker gets the same `last_referenced` date.
8. **Delete merged-away trackers**

#### Volume Rebalancing

For each confirmed volume rebalance recommendation (from Step 7f):

1. **Load all volumes** for the topic (by `consolidation_topic` frontmatter match)
2. **Decompress all volumes** to get full combined content
3. **If adding new memories**: merge new memory content into the combined body
4. **Re-partition** the combined content into the target number of volumes, each within `maxConsolidatedSize`, split at semantic boundaries
5. **Update existing volume files** in-place where possible; create new volumes or delete surplus volumes as needed
6. **Recompress** each updated volume via `crux-skill-memory-compress`
7. **Update trackers**: redistribute reference counts proportionally across the new volume set
8. **Archive and delete** any source memories that were merged in, and any surplus volume files

#### Compression

1. Delegate to `crux-skill-memory-compress` Compress operation, passing the `.memory.md` file path
2. The compress skill handles source archival, adaptive sizing against `maxMemorySize` (in the configured `sizeUnit`), and writing the `.memory.crux.md` output
3. If the compress skill flags a file for manual review (exceeds `maxMemorySize` even at maximum compression), report it in the REM summary as skipped

#### Strength Rebalance

1. Read the memory file's frontmatter `strength`
2. Write that value into the tracker file's `strength` field

#### Cleanup

1. Delete orphaned tracker files confirmed for removal

### Step 14: Write REM Summary

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

### Consolidated ({count} groups, {total_merged} memories merged)
- "{new_title}" ← {n} memories ({combined_size} → {compressed_size} lines)
  - {id_a} "{title_a}", {id_b} "{title_b}", ...

### Volume Rebalanced ({count} topics)
- topic "{consolidation_topic}": {old_volumes} → {new_volumes} volumes ({reason})

### Compressed ({count})
- "{title}": {original_size} → {compressed_size} lines ({reduced_by}% reduction)

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
- Total memories: {count} ({standalone_count} standalone, {consolidated_count} consolidated across {topic_count} topics)
- By type: core={n}, redflag={n}, goal={n}, learning={n}, idea={n}, archived={n}
- Compressed: {count} | Uncompressed: {count}
- Multi-volume topics: {count} (total volumes: {count})
- Tracked (with .refs.yml): {count}
- Untracked: {count}
```

### Step 15: Rebuild Index

After all changes are applied and the REM summary is written, rebuild the memory index to reflect the current state of the corpus:

```bash
python .cursor/skills/crux-skill-memory-index/scripts/memory-index.py
```

This is **mandatory** — skipping this step leaves the index stale, which causes downstream agents (Recall, Dream, session-start hooks) to reference moved, deleted, or renamed files. If the script fails, report the error but do not abort — the REM summary and applied changes are still valid.

### Step 16: Report

Present a concise summary of what changed to the user, including confirmation that the memory index was rebuilt (or an error if it failed).

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
| Memory Index | `.cursor/skills/crux-skill-memory-index/SKILL.md` | Index rebuild in Step 15 after all changes applied |

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
- Does not perform compression directly — delegates to `crux-skill-memory-compress` when compression is enabled and recommended during Step 8
- Does not record new references (that is `crux-skill-memory-reference-tracker`)
- Does not own the memory index script — it calls `crux-skill-memory-index` as a subprocess in Step 15
- Does not automatically create rules from promoted memories — it only flags candidates
- Does not modify `created` dates on any memory
