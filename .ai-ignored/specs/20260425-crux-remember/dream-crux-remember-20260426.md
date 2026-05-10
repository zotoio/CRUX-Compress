# Dream Summary — `20260425-crux-remember`

**Generated**: 2026-04-26
**Spec**: `specs/20260425-crux-remember/`
**Spec status at extraction**: Completed (all 6 subtasks marked Done; no `_execution-state.yml` — spec is explicitly reverse-engineered)
**Mode**: Interactive — user accepted all candidates

## Spec Scope Recap

The spec added a `/crux-remember` command for ad-hoc memory creation outside spec workflows. Implementation spanned 6 subtasks across 3 phases:

- **Phase 1** (parallel): create command file, update memory manager agent, update config and rules
- **Phase 2** (parallel, after Phase 1): update documentation and cross-references, update install and distribution files
- **Phase 3**: integration testing and verification

Files touched (spec-attributable subset): `.cursor/commands/crux-remember.md` (new), Remember Mode section in `.cursor/agents/crux-cursor-memory-manager.md`, `commands.remember` entry in `.crux/crux-memories.json`, amnesia override list in `.cursor/rules/crux-memories-integration.{md,crux.mdc}`, doc updates across `README.md` / `AGENTS.md` / `CONTRIBUTORS.md` / `docs/crux-memories.md` / `web/compress.md/memories.html`, sibling Related sections in `crux-amnesia.md` / `crux-dream.md` / `crux-forget.md` / `crux-recall.md`, eval scenarios in `evals/USER_EVAL_CHECKLISTS.md`, `install.py` (3 locations), `install.crux.md`, `scripts/create-crux-zip.py` `DIST_FILES`.

## Diff Scope Note

Total repository changes since spec start were ~82 files — above the `maxUnrelatedChanges=50` threshold. The majority belong to subsequent unrelated specs (sdk-eval-expansion, integration tests). Spec-specific scope was small and well-bounded; extraction proceeded without dilution.

## Candidates Extracted, Compared, and Accepted

5 candidates extracted, ranked, and accepted in full by the user.

| Rank | ID | Type | Slug | Title |
|------|----|------|------|-------|
| 1 | `f8bd856` | learning | `tag-entry-origin-with-source-field` | Tag entry origin with a source field when multiple commands write to one store |
| 2 | `ba92c4e` | learning | `source-askquestion-options-from-config-keys` | Source AskQuestion options from config keys to keep UI in sync with semantic model |
| 3 | `c35a703` | learning | `default-operations-to-broadest-scope` | Default new operations to the broadest scope when calling context lacks specificity signals |
| 4 | `74f65d5` | learning | `relax-rules-surgically-with-phrase-additions` | Relax restrictive rules surgically with phrase additions, not rewrites |
| 5 | `039b05f` | idea | `reverse-engineer-specs-for-traceability` | Reverse-engineer specs to restore traceability for work completed without planning |

All accepted candidates use:
- `strength: 1` (per `crux-skill-memory-crud` schema — strength must be a positive integer; the user-requested `0.5` was adjusted to the canonical default)
- `created: 2026-04-26` and `modified: 2026-04-26`
- `source: "20260425-crux-remember"`
- Base scope (`memories/{type}/`) — no agent-specific scoping warranted

## Candidates Filtered Out as Duplicates

The following insights were observed in the spec but discarded because existing memories already cover them:

| Filtered candidate | Existing memory |
|--------------------|-----------------|
| Sibling Related sections need backlinks | `bdcc9ad` — `update-sibling-related-sections-on-command-family-expansion` |
| Amnesia override exception list needs expansion | `8006029` — `override-exception-lists-need-backlinks` |
| Feature commands belong in `RELEASE_FILES`, not `standard_files` | `7144866` — `install-py-release-files-vs-standard-files` |
| Dist zip can omit new feature files | `aba710d` — `dist-zip-can-silently-omit-feature-files` |
| Memory commands that touch disk delegate to subagent | `b6985f5` — `session-toggles-handled-in-band-no-subagent` (already names `/crux-remember`) |
| Agent docs reference skills, don't duplicate operation logic | `f8bdc0d` — `agent-definitions-reference-skills` |
| Phase-block ordering reflects evaluation precedence | `d5e503c` — `crux-phase-block-ordering-reflects-precedence` |

## Conflicts Detected and Resolved

**None.** The spec's behavioural choices are consistent with all 22 existing memories. Notably, `b6985f5` (session-toggles-handled-in-band-no-subagent) explicitly lists `/crux-remember` as one of the commands that *does* delegate to a subagent — the spec confirms this design.

## Resolved Bugs Forgotten

**None.** All 7 redflag memories were reviewed; none describe bugs that this spec fixes. The spec actually conforms to several existing redflags (e.g. `aba710d` — file was correctly added to `DIST_FILES`), but conformance is not resolution.

## Memories Created

5 of 5 candidates created at the user-specified paths:

- `memories/learning/tag-entry-origin-with-source-field.memory.md`
- `memories/learning/source-askquestion-options-from-config-keys.memory.md`
- `memories/learning/default-operations-to-broadest-scope.memory.md`
- `memories/learning/relax-rules-surgically-with-phrase-additions.memory.md`
- `memories/idea/reverse-engineer-specs-for-traceability.memory.md`

All files include full required frontmatter and a structured body covering principle, concrete example, generalisation, and source citation.

## Notes for Future Dream Cycles

- The 82-file diff size warning is real but was muted here because the spec's own attributable surface is narrow. When dream extracting future specs that landed atop other unrelated work, the scope-narrowing technique used here (restrict analysis to spec-named commits + spec-named subtasks rather than repo-wide diff) is reusable.
- The `/crux-remember` spec sits in a closely-related family with `/crux-dream`, `/crux-recall`, `/crux-meditate`, `/crux-forget`, and `/crux-amnesia`. Several of those have produced their own memories. Future dreams across this family should expect a high duplicate-filter rate — the patterns are well-trodden.
- The reverse-engineered-spec idea (`039b05f`) is itself a meta-observation about this dream cycle. If formalised into a `/crux-spec --reverse` command, future ad-hoc work would become dreamable without manual spec authoring.

## Post-Dream Actions

- Memory index rebuild: triggered after creation of all 5 memories
- Spec archival: spec directory moved to `.ai-ignored/specs/20260425-crux-remember/` per user instruction
