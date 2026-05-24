# Subtask: CRUX Compression Sync

## Metadata
- **Subtask ID**: 11
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-cursor-rule-manager
- **Dependencies**: 06, 07, 09, 10
- **Created**: 20260517

## Objective
For every source file modified by subtasks 06, 07, 09, and 10 that has
a corresponding existing maintained `.crux.md` or `.crux.mdc` generated
mirror checked into this repository, regenerate that mirror so the
compressed output stays in sync with the source. Honour the workspace
foundational rules: never hand-edit generated files; only the
`crux-cursor-rule-manager` workflow operates on `.crux.*` outputs; abort
regeneration if compression does not achieve ≤20% of the original token
count.

## Deliverables Checklist

### Audit
- [ ] List every source file modified by subtasks 06, 07, 09, and 10
      and check whether a checked-in maintained `[name].crux.md` or
      `[name].crux.mdc` mirror exists. Likely candidates:
      - `.cursor/rules/crux-memories-integration.md` ->
        `.cursor/rules/crux-memories-integration.crux.mdc`
      - `.cursor/rules/docs-sync.md` ->
        `.cursor/rules/docs-sync.crux.mdc`
      - Any other checked-in `.md` rule source with an existing
        maintained `.crux.*` mirror
- [ ] Explicitly record that `AGENTS.md` is a source file and
      `AGENTS.crux.md` is **not** a maintained checked-in mirror in this
      repository. Do not create, require, or regenerate `AGENTS.crux.md`.
- [ ] For each maintained mirror candidate, decide regenerate vs. skip:
      - **Regenerate** if the source changed in a way that affects the
        rule's encoded directives.
      - **Skip with note** if the source change is purely typographic /
        does not affect compressed semantics.

### Regenerate
- [ ] For each "regenerate" item, run the `crux-cursor-rule-manager`
      compression workflow on the source file. Confirm:
      - The compressed output keeps the generated banner
        `> [!IMPORTANT] > Generated file - do not edit!`
      - The frontmatter `sourceChecksum` (or `sourceUrl`) updates to the
        new source hash.
      - The compression ratio is ≤20% of the original token count (per
        CRUX rule 5 — abort otherwise).
      - The compressed output preserves every directive's intent.

### Verify
- [ ] Run the project's CRUX validator if one exists (e.g. a script
      under `scripts/` that checks every generated file's frontmatter
      against its source). If no such script exists, manually spot-check
      by reading the regenerated mirror.
- [ ] Confirm that no source file was hand-edited as a side effect.
- [ ] Confirm no new `.crux.md` / `.crux.mdc` mirror coverage was
      introduced.

## Definition of Done
- [ ] Every modified source with an existing maintained mirror is either
      regenerated or explicitly skipped with justification
- [ ] All regenerated mirrors carry the generated banner and updated
      `sourceChecksum`
- [ ] `AGENTS.crux.md` is neither created nor required
- [ ] No compression ratio violation
- [ ] No linter errors introduced
- [ ] No source file edited inside this subtask (only generated mirrors
      are written)

## Implementation Notes
- **Foundational CRUX rules** (from `_CRUX-RULE.mdc` and `AGENTS.md`):
  1. Never edit `CRUX.md`.
  2. Never edit generated `.crux.md` / `.crux.mdc` files by hand —
     only the `crux-cursor-rule-manager` workflow writes them.
  3. Abort compression if reduction is not ≤20% of original.
  4. Preserve literal paths in compressed output.
- This subtask is **mechanical regeneration**, not redesign. If a
  source file has changed in ways that require the compressed CRUX to
  alter directive intent, that is in scope. If the source file has not
  changed semantically, skip regeneration with a note in Execution Notes.
- Do not regenerate `.crux.*` mirrors for files that were not touched by
  upstream subtasks — that is out of scope.
- If a compressed mirror would be created **for the first time** for a
  file that previously did not have one, treat that as a blocker and
  do not proceed. This spec's approved scope is existing mirrors only.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Run only the project's CRUX-mirror validator (if any) on the affected
  files.
- No pytest / SDK eval runs needed here.

## Execution Notes

### Agent Session Info
- Agent: crux-cursor-rule-manager
- Started: 2026-05-24T06:32:00Z
- Completed: 2026-05-24T06:33:00Z

### Work Log

**Mirror Enumeration**: Globbed `**/*.crux.md` (29 files) and `**/*.crux.mdc` (7 files).

**Maintained rule mirrors identified** (source in `.cursor/rules/`):

| # | Mirror | Source | Stored Checksum | Current Checksum | Status |
|---|--------|--------|-----------------|------------------|--------|
| 1 | `.cursor/rules/docs-sync.crux.mdc` | `.cursor/rules/docs-sync.md` | 1356781034 | 1356781034 | up-to-date |
| 2 | `.cursor/rules/docs-sync.crux.md` | `.cursor/rules/docs-sync.md` | 1356781034 | 1356781034 | up-to-date |
| 3 | `.cursor/rules/zip-contents-protection.crux.mdc` | `.cursor/rules/zip-contents-protection.md` | 3371193391 | 3371193391 | up-to-date |
| 4 | `.cursor/rules/zip-contents-protection.crux.md` | `.cursor/rules/zip-contents-protection.md` | 3371193391 | 3371193391 | up-to-date |
| 5 | `.cursor/rules/crux-memories-integration.crux.mdc` | `.cursor/rules/crux-memories-integration.md` | 4002236386 | 4002236386 | up-to-date |
| 6 | `.cursor/rules/version-bump.crux.mdc` | `.cursor/rules/version-bump.md` | 1841243360 | 1841243360 | up-to-date |
| 7 | `.cursor/rules/version-bump.crux.md` | `.cursor/rules/version-bump.md` | 1841243360 | 1841243360 | up-to-date |
| 8 | `.cursor/rules/ignore-example-rules.crux.mdc` | `.cursor/rules/ignore-example-rules.md` | 3575892284 | 3575892284 | up-to-date |
| 9 | `.cursor/rules/ignore-example-rules.crux.md` | `.cursor/rules/ignore-example-rules.md` | 3575892284 | 3575892284 | up-to-date |
| 10 | `.cursor/rules/example/coding-standards-demo.crux.mdc` | `.cursor/rules/example/coding-standards-demo.md` | 264908382 | 264908382 | up-to-date |

**Non-rule `.crux.md` files** (not maintained mirrors of rule sources — out of scope):
- `memories/**/*.crux.md` (6 files) — memory compression output, managed by memory-manager
- `tests/fixtures/*.crux.md` (3 files) — test fixtures
- `web/compress.md/assets/**/*.crux.md` (8 files) — demo assets for landing page
- `install.crux.md` (1 file) — install script compression demo
- `web/compress-md-landing-page-prompt.crux.mdc` (1 file) — landing page prompt, not a rule mirror

**Negative-assertion check**: `AGENTS.crux.md` does NOT exist at repo root. Confirmed via `Glob`.

**Cross-reference with spec-modified surfaces**: None of the rule source files (docs-sync.md, zip-contents-protection.md, crux-memories-integration.md, version-bump.md, ignore-example-rules.md, coding-standards-demo.md) were modified by subtasks 04–10. The files changed by this spec execution (agents, skills, commands, docs, evals, install) are not rule sources and have no maintained `.crux.mdc` mirrors.

**Result**: Zero regenerations needed. All 10 maintained rule mirrors are up-to-date.

### Deliverables

- [x] D01: Modified sources audited — no rule sources changed by S04–S10
- [x] D02: `AGENTS.crux.md` confirmed non-existent, not generated
- [x] D03: Zero mirrors require regeneration (all checksums match)
- [x] D04: N/A — no regeneration performed (all fresh)
- [x] D05: No new mirror coverage introduced

### Definition of Done
- [x] Every modified source with an existing maintained mirror is either regenerated or explicitly skipped with justification (all skipped — sources unchanged)
- [x] All regenerated mirrors carry the generated banner and updated sourceChecksum (N/A — zero regens)
- [x] `AGENTS.crux.md` is neither created nor required
- [x] No compression ratio violation
- [x] No linter errors introduced
- [x] No source file edited inside this subtask

### Blockers Encountered
None.

### Files Modified
- `specs/20260517-meditate-agent-skill-decomposition/subtask-11-meditate-decomp-crux-compression-20260517.md` (this file — execution notes)
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-11-meditate-decomp-crux-compression-20260517.status.md` (status pair)
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-11-meditate-decomp-crux-compression-20260517.status.yml` (status pair)
- `specs/20260517-meditate-agent-skill-decomposition/status.yml` (spec aggregate)
