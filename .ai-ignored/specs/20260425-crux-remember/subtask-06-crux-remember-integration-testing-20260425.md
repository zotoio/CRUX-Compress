# Subtask: Integration Testing and Verification

## Metadata
- **Subtask ID**: 06
- **Feature**: crux-remember
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 04, 05
- **Created**: 20260425

## Objective
Verify the complete `/crux-remember` implementation is consistent across all modified files — command definition, agent definition, config, rules, documentation, installer, and distribution.

## Deliverables Checklist
- [x] `.cursor/commands/crux-remember.md` exists with correct content
- [x] `.cursor/agents/crux-cursor-memory-manager.md` has Remember Mode section
- [x] `.crux/crux-memories.json` has `commands.remember` entry
- [x] `.cursor/rules/crux-memories-integration.md` includes `/crux-remember` in amnesia override list
- [x] `.cursor/rules/crux-memories-integration.crux.mdc` regenerated with updated content
- [x] Agent scoping rule mentions both dream extraction and explicit remember
- [x] All documentation files reference `/crux-remember` (`README.md`, `CONTRIBUTORS.md`, `AGENTS.md`, `docs/crux-memories.md`, `web/compress.md/memories.html`)
- [x] Related sections in sibling commands (`crux-amnesia.md`, `crux-dream.md`, `crux-forget.md`, `crux-recall.md`) include `/crux-remember`
- [x] `evals/USER_EVAL_CHECKLISTS.md` has `/crux-remember` eval scenarios
- [x] `install.py` includes `crux-remember` in prefixes, defaults, and fallback
- [x] `install.crux.md` regenerated
- [x] `scripts/create-crux-zip.py` includes the command file in `DIST_FILES`
- [x] Project test suite passes
- [x] No linter errors in any modified files

## Definition of Done
- [x] All verification checks pass
- [x] Test suite passes with no regressions
- [x] Cross-file consistency verified — command, agent, config, rules, docs, install, and dist all reference `/crux-remember` correctly
- [x] Spec index updated with completion status

## Implementation Notes

### Verification Checklist
1. **Command file**: Verify `.cursor/commands/crux-remember.md` exists with AskQuestion type selection, `--type` flag, `source: "adhoc"`, and skill delegation
2. **Agent definition**: Verify Remember Mode between Recall and Meditate, scoping rule updated
3. **Config**: Verify `commands.remember` in `.crux/crux-memories.json` with correct file path and description
4. **Rules**: Verify amnesia override list includes `/crux-remember` in both source and CRUX-compressed files
5. **Documentation**: Grep for `crux-remember` across all doc files
6. **Install**: Verify `install.py` references in three locations
7. **Distribution**: Verify `scripts/create-crux-zip.py` includes the command file
8. **Test suite**: Run `python3 scripts/test.py`

### Files to Verify
- `.cursor/commands/crux-remember.md`
- `.cursor/agents/crux-cursor-memory-manager.md`
- `.crux/crux-memories.json`
- `.cursor/rules/crux-memories-integration.md`
- `.cursor/rules/crux-memories-integration.crux.mdc`
- `README.md`
- `CONTRIBUTORS.md`
- `AGENTS.md`
- `docs/crux-memories.md`
- `web/compress.md/memories.html`
- `.cursor/commands/crux-amnesia.md`
- `.cursor/commands/crux-dream.md`
- `.cursor/commands/crux-forget.md`
- `.cursor/commands/crux-recall.md`
- `evals/USER_EVAL_CHECKLISTS.md`
- `install.py`
- `install.crux.md`
- `scripts/create-crux-zip.py`

## Testing Strategy
This IS the testing subtask — run the full test suite and comprehensive verification:
- `python3 scripts/test.py` for the project test suite
- ReadLints on all modified files
- Grep for `crux-remember` across the project to verify completeness

## Execution Notes

### Work Performed
1. Verified `.cursor/commands/crux-remember.md` exists with all required content — AskQuestion type selection, `--type` flag, `source: "adhoc"`, CRUD and index skill delegation, Related section
2. Verified Remember Mode in agent definition — positioned between Recall and Meditate, invocation variants table, seven-step workflow, AskQuestion with type descriptions
3. Verified agent scoping rule updated — rule 1 says "Only during dream extraction or explicit remember"
4. Verified `commands.remember` in `.crux/crux-memories.json` with correct file path, default command, and description
5. Verified amnesia override list in `.cursor/rules/crux-memories-integration.md` includes `/crux-remember`
6. Verified CRUX-compressed rule regenerated with updated sourceChecksum
7. Verified all documentation files reference `/crux-remember`: README.md, CONTRIBUTORS.md, AGENTS.md, docs/crux-memories.md, web/compress.md/memories.html
8. Verified Related sections in all four sibling commands include `/crux-remember`
9. Verified eval scenarios added to `evals/USER_EVAL_CHECKLISTS.md`
10. Verified `install.py` includes `crux-remember` in MEMORY_FILE_PREFIXES, default commands, and fallback list
11. Verified `install.crux.md` regenerated
12. Verified `scripts/create-crux-zip.py` includes `.cursor/commands/crux-remember.md` in DIST_FILES
13. Ran project test suite — all tests passed, zero failures
14. Ran linter checks on all modified files — zero errors

### Blockers Encountered
None.
