# Subtask: Memory Compress Skill

## Metadata
- **Subtask ID**: 04
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 01
- **Created**: 20260403

## Objective

Create the `crux-skill-memory-compress` skill that CRUX-compresses memory files and manages the source archive for originals.

## Deliverables Checklist
- [ ] `.cursor/skills/crux-skill-memory-compress/SKILL.md` — skill definition with:
  - **Compress**: Apply CRUX compression to a memory file's body. Frontmatter (title, description, type, etc.) is NEVER compressed. Output as `{slug}.memory.crux.md`.
  - **Adaptive compression**: Target `compressionTarget` percentage (default 33 — aim for 33% of original). If output exceeds `maxMemorySize` (2048 bytes), increase compression aggressiveness. If still too large after maximum compression, flag for manual review.
  - **Source archival**: Move the original uncompressed file to `.ai-ignored/memories/sources/[yyyymmdd]/` before replacing with compressed version.
  - **Migration**: When compression is enabled on a repo with existing uncompressed `*.memory.md` files, offer to compress them. Detect uncompressed files and present migration plan.
  - **Decompress**: Restore a compressed memory for editing (decompress body, rename back to `.memory.md`).
  - **Guard**: Only operate when `flags.enableMemoryCompression` is `"true"` in config.
- [ ] File naming transition: `.memory.md` → `.memory.crux.md`
- [ ] Integration with existing CRUX compression tooling (reference `CRUX.md` spec)

## Definition of Done
- [ ] SKILL.md clearly documents compression/decompression operations
- [ ] SKILL.md specifies adaptive compression logic
- [ ] SKILL.md handles source archival and migration
- [ ] SKILL.md references compression config from `.crux/crux-memories.json`
- [ ] SKILL.md guards on `enableMemoryCompression` flag
- [ ] No linter errors in modified files

## Implementation Notes

Reference `docs/crux-memories.md`:
- Section 4 "Compression" for full compression specification
- "Adaptive Compression" subsection for the compression targeting logic
- "Migration" subsection for handling existing uncompressed files
- "Viewing" subsection for decompression via MindReader

The skill should leverage the existing CRUX compression capabilities described in `CRUX.md`. The `crux-cursor-rule-manager` agent already handles CRUX compression for rule files — this skill follows similar patterns but specialised for memory files.

Key difference from rule compression: memory compression has a `maxMemorySize` hard cap that may require going beyond the target compression ratio.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Review SKILL.md for completeness against spec
- Defer full test suite execution to the final verification phase

## Execution Notes
[To be filled by executing agent]

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
[Agent adds notes here during execution]

### Blockers Encountered
[Any blockers or issues]

### Files Modified
[List of files changed]
