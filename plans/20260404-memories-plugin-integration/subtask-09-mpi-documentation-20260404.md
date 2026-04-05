# Subtask: Documentation — Update README, CONTRIBUTORS, AGENTS

## Metadata
- **Subtask ID**: 09
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: docs-sync-agent
- **Dependencies**: 08
- **Created**: 20260404

## Objective

Update project documentation to reflect both workstreams: memory integration improvements and the new default-enabled plugin mechanism with the `compression-level` reference plugin.

## Deliverables Checklist
- [x] `README.md` updated:
  - Plugin section: document `enabledByDefault` mechanism, `--no-plugin` flag
  - Plugin section: add `compression-level` as a documented default plugin
  - Install section: mention `--with-memories` flag for optional memory setup
  - Testing section: note new test files (`test_n_plugin_registry.py`)
  - File Locations Summary: add `.crux/plugins/compression-level.md`
- [x] `CONTRIBUTORS.md` updated:
  - Add "Plugin System" section covering: registry structure, hook lifecycle, `enabledByDefault`, how to add a new plugin
  - Test suite table: add new test files
  - Update any stale references (install.sh → install.py if not already done)
- [x] `AGENTS.md` verified — no changes needed (all 5 agents match definitions on disk)
- [ ] CRUX compressed versions updated surgically for modified source rules (`docs-sync.md` → `docs-sync.crux.md`, `docs-sync.crux.mdc`)

## Definition of Done
- [x] README accurately reflects current plugin behavior and memory integration
- [x] CONTRIBUTORS has plugin contributor guidance
- [x] No stale references to `install.sh` in documentation (README, CONTRIBUTORS, web/index.html all clean)
- [x] All documentation changes are surgical (update specific sections, don't rewrite)
- [ ] CRUX files updated surgically for modified source rules
- [x] No linter errors in modified files

## Implementation Notes

### README Changes

**Plugin Parameter System section** (currently covers `--plugin`, registry, hooks):
- Add: "Default plugins load automatically when no `--plugin` flags are specified"
- Add: `compression-level` to the registry example
- Add: `--no-plugin <name>` flag to the flags table
- Add: explanation that explicit `--plugin` overrides defaults

**Quick Install section**:
- Add `--with-memories` to the options table
- Brief note: "Optionally scaffold memory system components"

**Testing section**:
- Add `test_plugin_registry.py` to the test files table

### CONTRIBUTORS Changes

**New section: "Plugin System"**:
- Where plugins are defined (`.crux/plugins/registry.json`)
- Hook lifecycle (`beforeFetch` → `beforeCompress` → base compression → `afterCompress` → `afterValidate`)
- `enabledByDefault` mechanism
- How to add a new plugin (add to registry, implement behavior in agent/command spec)
- Reference: `compression-level` as the canonical example

### Files to Read Before Editing
- `README.md` — current plugin and install sections
- `CONTRIBUTORS.md` — current structure and sections
- `AGENTS.md` — agent table

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Verify documentation changes are accurate against actual code/config state
- Defer to subtask 10 for final integrity check

## Execution Notes

### Agent Session Info
- Agent: docs-sync-agent
- Started: 2026-04-05
- Completed: 2026-04-05

### Work Log
1. Read all target docs (README.md, CONTRIBUTORS.md, AGENTS.md) and source files (registry.json, install.py, compression-level.md, crux-compress.md command spec, crux-utils SKILL.md)
2. **README.md** — 5 surgical edits:
   - Added `--no-plugin` flag to Flags table
   - Replaced minimal plugin registry example with full 4-plugin registry showing `enabledByDefault`, `failClosed` fields
   - Added "Plugin Loading Modes" explanation and `compression-level` plugin description
   - Added `--with-memories` to Install Options
   - Added `--target <n>` mode to crux-utils Modes table
   - Added `test_n_plugin_registry.py` to Test Coverage table (updated coverage descriptions for existing entries)
   - Added Plugin Registry and Plugin Spec entries to File Locations Summary table
3. **CONTRIBUTORS.md** — 3 surgical edits:
   - Added "Plugin System" section (registry structure, hook lifecycle, `enabledByDefault` mechanism, how to add a new plugin) before Manual Version Bump
   - Added `test_n_plugin_registry.py` to Test Suites table
   - Added Plugin System to Table of Contents
4. **AGENTS.md** — Verified, no changes needed. All 5 agent definitions match files on disk.
5. **Stale references** — Confirmed README.md, CONTRIBUTORS.md, web/compress.md/index.html have zero `install.sh` references. Fixed 2 stale references in `.cursor/rules/docs-sync.md` source (`install.sh` → `install.py`, `tests/*.bats` → `evals/*.py`)
6. **CRUX sync** — Applied surgical diffs to `docs-sync.crux.md` and `docs-sync.crux.mdc` to match source changes (full regeneration deferred to integrity audit)

### Blockers Encountered
None.

### Files Modified
- `README.md` — plugin docs, install options, test table, file locations
- `CONTRIBUTORS.md` — plugin system section, test table, TOC
- `.cursor/rules/docs-sync.md` — fixed stale `install.sh` and `tests/*.bats` refs
- `.cursor/rules/docs-sync.crux.md` — surgical sync with source
- `.cursor/rules/docs-sync.crux.mdc` — surgical sync with source

### Adversarial Verification (integrity-expert)
- **Verifier**: integrity-expert
- **Date**: 2026-04-05
- **Verdict**: **PARTIAL** — 9/11 items confirmed, 2 items failed (both CRUX sync)

#### Confirmed Items (re-ticked)

**README.md** (all 5 sub-items confirmed):
- `enabledByDefault` mechanism documented at lines 472, 485, 509-513 ✅
- `--no-plugin` flag in Flags table (line 460) and Plugin Loading Modes (line 511) ✅
- `compression-level` as documented default plugin (lines 481, 511, 514) with `.crux/plugins/compression-level.md` reference ✅
- `--with-memories` in Install Options (line 257) ✅
- `test_n_plugin_registry.py` in Test Coverage table (line 949) ✅
- File Locations Summary includes Plugin Registry (line 829) and Plugin Spec (line 830) ✅

**CONTRIBUTORS.md** (all 3 sub-items confirmed):
- "Plugin System" section (lines 276-327) covers: registry structure, hook lifecycle (6-step), `enabledByDefault` mechanism, how to add a new plugin (5-step guide referencing `compression-level` as canonical example) ✅
- `test_n_plugin_registry.py` in Test Suites table (line 96) ✅
- Zero `install.sh` references (ripgrep confirmed) ✅

**AGENTS.md**: Verified — 5 agents in table match definitions on disk ✅

**Stale references**: Zero `install.sh` matches in README.md, CONTRIBUTORS.md, web/compress.md/index.html (ripgrep confirmed all three) ✅

**Linter errors**: None in any modified file ✅

**Surgical edits**: Changes are targeted section updates, not file rewrites ✅

#### Failed Items (left unchecked)

**CRUX sourceChecksum is STALE** (Deliverables item 4, DoD item 5):
- `docs-sync.crux.md` and `docs-sync.crux.mdc` both carry `sourceChecksum: 347482193`
- Actual checksum of `docs-sync.md` source is `1356781034` (verified via `crux-utils.py --cksum`)
- The CRUX **content** is correct (notation reflects `install.py` and `evals/*.py`), but the frontmatter checksum was not updated after the source was modified
- This means the next `/crux-compress ALL` run will flag these files as needing regeneration (false positive)
- **Fix required**: Update `sourceChecksum` in both `.crux.md` and `.crux.mdc` frontmatter to `1356781034`

#### Bonus Findings (out of scope but noted)

1. `docs-sync.md` line 30 references `tests/helpers.bash` — this file does not exist in the repo (0 matches from glob). This is a pre-existing stale reference not addressed by any subtask.
2. `install.crux.md` in project root still references `install.sh` in its CRUX notation (header: `⟦CRUX:install.sh`). This is a separate stale artifact unrelated to subtask 09.
3. `.cursor/commands/crux-test.md` lines 108-110 still reference `install.sh` for test validation steps — another pre-existing stale reference outside subtask 09 scope.
