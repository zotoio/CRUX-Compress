# Dream Summary: `20260425-crux-amnesia`

**Dream date**: 2026-04-26
**Spec status at dream time**: Completed (5/5 subtasks Done)
**Dream agent**: `crux-cursor-memory-manager`

## Verification

| Check | Result |
|-------|--------|
| Spec status field | Completed |
| Subtask manifest | All 5 subtasks marked Done |
| `_execution-state.yml` | Not present (reverse-engineered spec); verification fell back to spec status fields and Definition of Done checkmarks |
| Definition of Done | All 8 items checked |

## Diff scope analysis

| Metric | Value |
|--------|-------|
| Files changed in repo since 2026-04-25 | 94 |
| `maxUnrelatedChanges` threshold | 50 |
| Threshold exceeded? | Yes (proceeded with user acknowledgment) |

The diff exceeded threshold because the spec is reverse-engineered, capturing work built incrementally across multiple sessions. Concurrent unrelated work (`/crux-recall` rename, `/crux-remember`, `/crux-meditate`, eval expansion, version bumps) inflated the count. Candidate extraction was scoped to amnesia-specific artifacts only.

## Existing memory comparison

Compared candidates against 16 existing memories. Two close-related memories identified:

- `bdcc9ad` — `update-sibling-related-sections-on-command-family-expansion` (related to candidate 3, kept distinct as new memory)
- `7144866` — `install-py-release-files-vs-standard-files` (related to candidate 1, kept distinct — different surface)

No conflicts detected.

## Candidates extracted

5 candidates extracted, all accepted by user.

| # | Type | Title | ID | Status |
|---|------|-------|-----|--------|
| 1 | redflag | Distribution zip can silently omit incrementally-built feature files | `aba710d` | Created |
| 2 | learning | Session-scoped pure-toggle commands should be handled in-band, not via subagent delegation | `b6985f5` | Created |
| 3 | learning | Override exception lists are a backlink site easy to miss when expanding a command family | `8006029` | Created |
| 4 | learning | Session-scoped flags must define explicit subagent inheritance semantics | `4d0d83f` | Created |
| 5 | learning | CRUX rule phase-block ordering reflects evaluation precedence | `d5e503c` | Created |

## Memories created

### `memories/redflag/dist-zip-can-silently-omit-feature-files.memory.md`
- **ID**: `aba710d`
- **Type**: redflag
- **Strength**: 1 (initial)
- **Tags**: distribution, dist-files, release, completeness, installer, command-files, packaging
- **Captures**: The risk that new user-facing files (commands, rules, hooks, skills) can be checked in, configured, installed, and documented yet absent from `scripts/create-crux-zip.py DIST_FILES`. Survives multiple sessions because repo-cloned developers don't exercise the distribution path. The amnesia command was the concrete instance.

### `memories/learning/session-toggles-handled-in-band-no-subagent.memory.md`
- **ID**: `b6985f5`
- **Type**: learning
- **Strength**: 1 (initial)
- **Tags**: architecture, commands, session-scope, subagents, performance, design-pattern, agent-orchestration
- **Captures**: Architectural pattern — session-scope, write-nothing toggles should be handled in the parent agent rather than delegated to a subagent. Discriminator: does the command write anything? If no, handle in-band. Concrete instance: `/crux-amnesia` does NOT spawn the memory manager.

### `memories/learning/override-exception-lists-need-backlinks.memory.md`
- **ID**: `8006029`
- **Type**: learning
- **Strength**: 1 (initial)
- **Tags**: commands, command-families, override-rules, exception-lists, behavioural-spec, backlinks, completeness, spec-design
- **Captures**: Override exception lists are a second backlink site that needs updates when new commands join a family. Distinct from sibling Related sections (memory `bdcc9ad`) because override lists have behavioral implications — missing entries cause real suppression, not just navigational gaps. Concrete instance: amnesia exception list updated mid-session for `/crux-remember` and `/crux-meditate`.

### `memories/learning/session-flags-define-subagent-inheritance.memory.md`
- **ID**: `4d0d83f`
- **Type**: learning
- **Strength**: 1 (initial)
- **Tags**: subagents, session-scope, inheritance, flags, agent-orchestration, design-pattern, alwaysapply-rules
- **Captures**: Pattern for session-scope flags — must define explicit subagent inheritance to prevent subagents from silently violating session intent. Three-question contract: what propagates, what breaks inheritance, where is it documented (must be `alwaysApply: true` rule).

### `memories/learning/crux-phase-block-ordering-reflects-precedence.memory.md`
- **ID**: `d5e503c`
- **Type**: learning
- **Strength**: 1 (initial)
- **Tags**: crux, rules, ordering, precedence, phase-blocks, authoring-convention, alwaysapply-rules
- **Captures**: Authoring convention — when a CRUX-compressed rule contains multiple `Φ.*` phase blocks representing modes/overrides, order them highest-precedence first so the LLM evaluates overrides before defaults. Concrete instance: `Φ.amnesia` → `Φ.enabled` → `Φ.disabled`.

## Conflicts resolved

None.

## Resolved bug review

Scanned all 6 existing redflag memories against the amnesia work item. None resolved by this work:

| Redflag memory | Status |
|----------------|--------|
| `dbfd3ed` — `file-paths-in-docs-must-reference-actual-files` | Still active |
| `d944d7c` — `spec-index-can-drift-from-subtask-details` | Still active |
| `826c280` — `agents-crux-md-is-transient-install-artifact` | Still active |
| `96a7410` — `tooling-defaults-must-align-with-spec` | Still active |
| `9b9a4ac` — `tests-must-use-tmp-path-fixtures` | Still active |
| `da3d798` — `max-memory-size-adaptive-compression` | Still active |

No `/crux-forget` operations performed.

## Index rebuild

`.crux/memory-index.yml` rebuilt to include the 5 new memories.

## Spec archival

User to be prompted whether to move `specs/20260425-crux-amnesia/` to `.ai-ignored/executed/`.
