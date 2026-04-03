---
name: crux-skill-memory-compress
description: CRUX-compress memory files with adaptive sizing and source archival. Handles compress, decompress, migration of existing memories, and maxMemorySize enforcement. Use when compressing or decompressing memory files, or migrating uncompressed memories after enabling compression.
---

# CRUX Memory Compress

Applies CRUX compression to memory file bodies, enforces size caps, archives originals, and handles migration of pre-existing uncompressed memories.

## Prerequisites

Before any operation:

1. **Read config**: Load `.crux/crux-memories.json` and extract:
   - `flags.enableMemoryCompression` — must be `"true"` or abort with message
   - `cruxMemories.compressionTarget` — target percentage (default `33`)
   - `cruxMemories.maxMemorySize` — hard cap in bytes (default `2048`)
   - `cruxMemories.storage.compressionSourceArchive` — archive path (default `.ai-ignored/memories/sources`)
   - `cruxMemories.storage.memoriesDir` — where memories live (default `memories`)
2. **Load CRUX spec**: Read `CRUX.md` from project root for encoding symbols and compression rules
3. **Guard check**: If `flags.enableMemoryCompression` is not `"true"`, refuse all operations and inform the caller that memory compression is disabled

## Operations

### 1. Compress

Compress a single memory file's body using CRUX notation.

**Input**: Path to a `.memory.md` file

**Steps**:

1. Read the memory file and separate frontmatter from body
2. **Frontmatter is NEVER compressed** — preserve it exactly as-is (title, description, type, tags, strength, scope, etc.)
3. Estimate body token count using `crux-utils` skill (`--token-count`) if available, otherwise LLM estimation (prose: 4 chars/token, code: 3.5 chars/token, CRUX symbols: 1 token each)
4. Apply CRUX compression to the body only, targeting `compressionTarget`% of original body size
5. Measure compressed body size in bytes
6. **Adaptive sizing** — if compressed output exceeds `maxMemorySize` bytes:
   - Increase compression aggressiveness (reduce target by 10 percentage points)
   - Re-compress and re-measure
   - Repeat until under `maxMemorySize` or target reaches 5%
   - If still over `maxMemorySize` at maximum compression, flag for manual review and do NOT write the file
7. Archive the original (see [Source Archival](#3-source-archival))
8. Write compressed output as `{slug}.memory.crux.md` in the same directory
9. Delete the original `.memory.md` from the working directory (it has been archived in step 7)
10. Add compression metadata to frontmatter of the output file:
   ```yaml
   compressed: true
   compressionTarget: 33
   beforeTokens: <original body tokens>
   afterTokens: <compressed body tokens>
   reducedBy: <percentage>
   compressedDate: <YYYY-MM-DD>
   sourceArchive: <path to archived original>
   ```

**Output format** (`{slug}.memory.crux.md`):

```markdown
---
<original frontmatter fields preserved>
compressed: true
compressionTarget: 33
beforeTokens: 450
afterTokens: 140
reducedBy: 69%
compressedDate: 2026-04-04
sourceArchive: .ai-ignored/memories/sources/20260404/react-memo-list-rendering.memory.md
---

⟦CRUX:memory
<compressed body content>
⟧
```

**Key difference from rule compression**: Memory compression has a `maxMemorySize` hard cap that may require compressing beyond the `compressionTarget` ratio. Rule compression only targets a percentage — memory compression targets a percentage AND an absolute byte limit.

### 2. Decompress

Restore a compressed memory for editing.

**Input**: Path to a `.memory.crux.md` file

**Steps**:

1. Read the compressed file and separate frontmatter from CRUX body
2. Decompress the CRUX body back to natural language (terse, not verbose — preserve meaning without expanding to full prose)
3. Remove compression metadata fields from frontmatter (`compressed`, `compressionTarget`, `beforeTokens`, `afterTokens`, `reducedBy`, `compressedDate`, `sourceArchive`)
4. Write the result as `{slug}.memory.md` (rename from `.memory.crux.md` to `.memory.md`)
5. Delete the `.memory.crux.md` file

**Decompression style**: Expand CRUX notation to terse natural language. Do not inflate back to original verbosity — aim for compact, readable content that preserves all semantic meaning. This matches the MindReader display style.

**Source recovery**: If the original exists in the source archive (check `sourceArchive` frontmatter field), offer to restore the exact original instead of decompressing.

### 3. Source Archival

Before replacing a `.memory.md` with its compressed `.memory.crux.md`, archive the original.

**Archive path**: `{compressionSourceArchive}/{yyyymmdd}/{original-filename}`

Example: `.ai-ignored/memories/sources/20260404/react-memo-list-rendering.memory.md`

**Steps**:

1. Create the dated archive directory if it doesn't exist
2. Copy (not move) the original `.memory.md` to the archive path
3. Record the archive path in the compressed file's `sourceArchive` frontmatter field
4. Only after successful archival, proceed with writing the compressed file

The archive directory (`.ai-ignored/`) is excluded from AI context loading, keeping originals available for recovery without polluting agent context.

### 4. Migration

When compression is enabled on a repo with existing uncompressed memories, detect and offer to compress them.

**Trigger**: Called when `enableMemoryCompression` is `"true"` and uncompressed `.memory.md` files exist

**Steps**:

1. Scan `memoriesDir` recursively for `*.memory.md` files (exclude any already-compressed `*.memory.crux.md`)
2. For each uncompressed file, estimate current size and projected compressed size
3. Present a migration plan:
   ```
   Found N uncompressed memory files:

   | File | Current Size | Est. Compressed | Fits maxMemorySize |
   |------|-------------|-----------------|-------------------|
   | core/react-memo.memory.md | 3.2 KB | ~1.1 KB | Yes |
   | learning/stale-closure.memory.md | 1.8 KB | ~0.6 KB | Yes |
   | idea/visual-regression.memory.md | 4.5 KB | ~1.5 KB | Yes |

   Compress all? [all/select/skip]
   ```
4. On confirmation, compress each file using the [Compress](#1-compress) operation
5. Report results: how many compressed, any that exceeded `maxMemorySize` and were flagged

## CRUX Compression Patterns for Memories

When compressing memory bodies, follow these patterns adapted from the CRUX spec:

- Use standard CRUX blocks where applicable (`Ρ{}` for purpose, `Κ{}` for key definitions, `R{}` for rules, `Λ{}` for triggers, `P{}` for prohibitions)
- Use CRUX encoding symbols (`→`, `¬`, `⊤`, `⊥`, `∀`, `≻`, etc.) per `CRUX.md`
- For factual memories (learnings, core), compress to key-value assertions
- For procedural memories (goals, ideas), compress to action sequences
- For warning memories (redflags), compress to condition → consequence patterns
- Reference the `crux-cursor-rule-manager` agent definition for full compression methodology

## Integration

| Component | Location | Role |
|-----------|----------|------|
| CRUX spec | `CRUX.md` | Encoding symbols, compression rules, standard blocks |
| Rule compressor agent | `.cursor/agents/crux-cursor-rule-manager.md` | Compression patterns and methodology reference |
| Token estimator | `.cursor/skills/crux-utils/SKILL.md` | Token counting and ratio analysis |
| Config | `.crux/crux-memories.json` | `compressionTarget`, `maxMemorySize`, `flags.enableMemoryCompression`, `storage.compressionSourceArchive` |
| Memory CRUD | `.cursor/skills/crux-skill-memory-crud/SKILL.md` | Frontmatter management, file creation conventions |

## Config Reference

All config values come from `.crux/crux-memories.json`:

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `flags.enableMemoryCompression` | string | `"false"` | Feature gate — must be `"true"` to operate |
| `cruxMemories.compressionTarget` | number | `33` | Target compressed size as % of original |
| `cruxMemories.maxMemorySize` | number | `2048` | Hard cap on compressed output in bytes |
| `cruxMemories.storage.compressionSourceArchive` | string | `.ai-ignored/memories/sources` | Base path for archived originals |

## Error Handling

| Condition | Action |
|-----------|--------|
| `enableMemoryCompression` is not `"true"` | Abort, inform caller compression is disabled |
| File is not a `.memory.md` or `.memory.crux.md` | Reject with descriptive error |
| Compressed output exceeds `maxMemorySize` at max compression | Flag for manual review, do not write output |
| Source archive directory cannot be created | Abort compression, report filesystem error |
| Decompressed file would overwrite existing `.memory.md` | Prompt before overwriting |
| Config file missing or malformed | Report error with path and expected structure |
