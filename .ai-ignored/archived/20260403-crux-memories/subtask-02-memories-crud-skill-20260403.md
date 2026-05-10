# Subtask: Memory CRUD Skill

## Metadata
- **Subtask ID**: 02
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 01
- **Created**: 20260403

## Objective

Create the `crux-skill-memory-crud` skill that provides create, read, update, and delete operations for memory files with proper frontmatter management.

## Deliverables Checklist
- [ ] `.cursor/skills/crux-skill-memory-crud/SKILL.md` — skill definition with:
  - **Create**: Generate a new memory file with valid frontmatter (title, description, type, strength=1, created, modified, source, tags) and body content. Place in correct type subdirectory. Enforce `maxMemorySize` from config.
  - **Read**: Load and parse a memory file by slug or path. Return frontmatter and body separately.
  - **Update**: Modify memory frontmatter or body. Update `modified` date. If type changes, move file to new type subdirectory and set `promoted_from`.
  - **Delete**: Remove a memory file. Also remove its corresponding `.refs.yml` tracker if one exists.
  - **Validate**: Check a memory file against the required frontmatter schema. Report missing/invalid fields.
- [ ] File naming enforcement: `{slug}.memory.md` (uncompressed) or `{slug}.memory.crux.md` (compressed)
- [ ] Directory placement logic: memory type → subdirectory mapping
- [ ] Agent-scoped memory placement: `memories/agents/{agent-id}/{type}/`
- [ ] Frontmatter schema validation against required fields from spec

## Definition of Done
- [ ] SKILL.md clearly documents all CRUD operations
- [ ] SKILL.md specifies the memory file format (frontmatter + body)
- [ ] SKILL.md handles agent-scoped vs base memory placement
- [ ] SKILL.md references `.crux/crux-memories.json` for config values
- [ ] No linter errors in modified files

## Implementation Notes

Reference `docs/crux-memories.md`:
- "Memory File Format" section for frontmatter schema
- "Directory Structure" section for placement rules
- "File Naming" section for naming conventions
- "Agent-Scoped Memories" section for agent memory rules

The skill is a SKILL.md file (agent instructions), not executable code. It tells agents how to perform CRUD operations on memory files. Follow the pattern of existing skills like `.cursor/skills/crux-utils/SKILL.md`.

Key constraints:
- `strength` starts at 1 for new memories
- `created` date never changes on update, only `modified`
- When type changes, move the file to the new type directory
- Agent memories go to `memories/agents/{agent-id}/{type}/`
- Base memories go to `memories/{type}/`
- Respect `maxMemorySize` (2048 bytes default) — flag if exceeded

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
