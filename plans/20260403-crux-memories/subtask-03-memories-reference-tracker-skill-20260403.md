# Subtask: Reference Tracker Skill

## Metadata
- **Subtask ID**: 03
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 01
- **Created**: 20260403

## Objective

Create the `crux-skill-memory-reference-tracker` skill that tracks which memories are referenced in agent output, manages `.refs.yml` tracker files, and keeps strength counters in sync with memory frontmatter.

## Deliverables Checklist
- [ ] `.cursor/skills/crux-skill-memory-reference-tracker/SKILL.md` — skill definition with:
  - **Record reference**: When a memory is referenced in agent output, create or update the corresponding `{slug}.refs.yml` in `.crux/reference-tracking/`. Increment `references` count, update `last_referenced`, add entry to `recent_references`.
  - **Indicate in output**: When `referenceTracking.indicateInOutput` is true, instruct agents to annotate output with `[memory:{title}]` format (configurable via `indicatorFormat`).
  - **Sync strength**: Keep the `strength` field in the tracker file in sync with the memory frontmatter's `strength` field.
  - **Manage recent_references**: Maintain a capped list (configurable via `maxReferencesStored`, default 10) of top referrers sorted by count descending. Each entry records source (spec/plan ID or conversation_id), count, last date, and optional context.
  - **Lazy creation**: Tracker files are created on first reference — unreferenced memories have no tracker overhead.
  - **Cleanup**: Remove tracker files whose corresponding memory no longer exists (called during REM sleep).
- [ ] `.refs.yml` format per spec: `slug`, `references`, `last_referenced`, `strength`, `recent_references[]`
- [ ] Header comment in generated files: `# Managed by crux-skill-memory-reference-tracker — do not edit manually`

## Definition of Done
- [ ] SKILL.md clearly documents all tracker operations
- [ ] SKILL.md specifies the `.refs.yml` format with all fields
- [ ] SKILL.md handles lazy creation, updates, and cleanup
- [ ] SKILL.md references `referenceTracking` config from `.crux/crux-memories.json`
- [ ] No linter errors in modified files

## Implementation Notes

Reference `docs/crux-memories.md`:
- "Reference Tracking Data" section for `.refs.yml` format and examples
- "referenceTracking" config block for all settings
- Design rationale: per-memory files for zero contention, clean memory files, lazy creation

The `recent_references` list tracks the top N referrers. Each entry has:
- `spec` or `conversation_id` (source identifier)
- `count` (references from that source)
- `last` (date of most recent reference)
- `context` (optional, brief description of how the memory was used)

When `promotionToRuleThreshold` is exceeded, the skill should flag the memory for potential promotion to a permanent rule.

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
