# Subtask: CRUX Compression Sync

## Metadata
- **Subtask ID**: 10
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-cursor-rule-manager
- **Dependencies**: 06, 07, 09
- **Created**: 20260517

## Objective
For every source file modified by subtasks 06, 07, and 09 that has a
corresponding `.crux.md` or `.crux.mdc` generated mirror, regenerate
that mirror so the compressed output stays in sync with the source.
Honour the workspace foundational rules: never hand-edit generated
files; only the `crux-cursor-rule-manager` agent operates on the
`.crux.*` outputs; abort regeneration if compression does not achieve
≤20% of the original token count.

## Deliverables Checklist

### Audit
- [ ] List every source file modified by subtasks 06, 07, 09 and
      check whether a `[name].crux.md` or `[name].crux.mdc` mirror
      exists. Likely candidates:
      - `AGENTS.md` → `AGENTS.crux.md`
      - `.cursor/rules/crux-memories-integration.md` →
        `.cursor/rules/crux-memories-integration.crux.mdc`
      - `.cursor/rules/docs-sync.md` →
        `.cursor/rules/docs-sync.crux.mdc`
      - Any other `.md` rule with a mirror pair
- [ ] For each candidate, decide regenerate vs. skip:
      - **Regenerate** if the source changed in a way that affects
        the rule's encoded directives.
      - **Skip with note** if the source change is purely typographic
        / does not affect compressed semantics.

### Regenerate
- [ ] For each "regenerate" item, run the `crux-cursor-rule-manager`
      compression workflow on the source file. Confirm:
      - The compressed output keeps the generated banner
        `> [!IMPORTANT] > Generated file - do not edit!`
      - The frontmatter `sourceChecksum` (or `sourceUrl`) updates
        to the new source hash.
      - The compression ratio is ≤20% of the original token count
        (per CRUX rule 5 — abort otherwise).
      - The compressed output preserves every directive's intent.

### Verify
- [ ] Run the project's CRUX validator if one exists (e.g. a script
      under `scripts/` that checks every generated file's
      frontmatter against its source). If no such script exists,
      manually spot-check by reading the regenerated mirror.
- [ ] Confirm that no source file was hand-edited as a side effect.

## Definition of Done
- [ ] Every modified source with a mirror is either regenerated or
      explicitly skipped with justification
- [ ] All regenerated mirrors carry the generated banner and updated
      `sourceChecksum`
- [ ] No compression ratio violation
- [ ] No linter errors introduced
- [ ] No source file edited inside this subtask (only generated
      mirrors are written)

## Implementation Notes
- **Foundational CRUX rules** (from `_CRUX-RULE.mdc` and
  `AGENTS.md`):
  1. Never edit `CRUX.md`.
  2. Never edit generated `.crux.md` / `.crux.mdc` files by hand
     — only the `crux-cursor-rule-manager` workflow writes them.
  3. Abort compression if reduction is not ≤20% of original.
  4. Preserve literal paths in compressed output.
- This subtask is **mechanical regeneration**, not redesign.
  If a source file has changed in ways that require the
  compressed CRUX to alter directive intent, that is in scope.
  If the source file has not changed semantically, skip
  regeneration with a note in Execution Notes.
- Do not regenerate `.crux.*` mirrors for files that were not
  touched by upstream subtasks — that is out of scope.
- If a compressed mirror is created **for the first time** for
  a file that previously did not have one, treat that as a
  separate decision and surface it as a blocker — do not
  introduce new mirror coverage in this subtask without explicit
  user opt-in.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Run only the project's CRUX-mirror validator (if any) on the
  affected files.
- No pytest / SDK eval runs needed here.

## Execution Notes
*(to be filled by executing agent)*

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
