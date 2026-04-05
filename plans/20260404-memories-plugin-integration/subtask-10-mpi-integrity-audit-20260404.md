# Subtask: Integrity Audit — Final Verification

## Metadata
- **Subtask ID**: 10
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: integrity-expert
- **Dependencies**: 09
- **Created**: 20260404

## Objective

Perform a comprehensive integrity audit of all changes made across subtasks 01-09. Verify CRUX file synchronization, test suite health, linter compliance, backward compatibility, and documentation accuracy.

## Deliverables Checklist
- [x] CRUX sync: all modified source files have up-to-date `.crux.md`/`.crux.mdc` counterparts
- [x] Test suite: `python3 scripts/test.py` passes cleanly
- [x] Linter: no errors in any modified files (use ReadLints)
- [x] Registry: `.crux/plugins/registry.json` is valid JSON with correct schema
- [x] Backward compat: existing `/crux-compress` invocations produce identical behavior
- [ ] Documentation: README, CONTRIBUTORS, AGENTS accurately reflect current state
- [ ] Website: `web/compress.md/index.html` is well-formed HTML
- [x] Installer: `install.py` syntax-checks and `--help` works
- [x] CI/CD: workflow YAML files are syntactically valid
- [x] Hooks: `hooks.json` is valid JSON with correct entries

## Definition of Done
- [ ] All audit checks pass
- [ ] No regressions identified
- [x] Audit report written in Execution Notes below
- [ ] Plan index updated with final status

## Implementation Notes

### Audit Checklist

1. **CRUX Synchronization**
   - For each file modified in subtasks 01-09, check if a `.crux.md`/`.crux.mdc` exists
   - If yes, verify the `sourceChecksum` matches the current source
   - If stale, flag for regeneration

2. **Test Suite**
   - Run `python3 scripts/test.py` and capture output
   - All tests must pass (zero failures)
   - Check for any skipped tests that should be running

3. **Linter Compliance**
   - Run ReadLints on all modified files
   - Zero errors in files modified by this plan

4. **Backward Compatibility**
   - Trace the `/crux-compress @file.md` flow through updated specs
   - Verify: level resolution, compression, metrics, frontmatter output are functionally identical
   - The `compression-level` plugin produces the same metrics the agent previously produced

5. **Registry Validation**
   - Parse `.crux/plugins/registry.json`
   - Verify schema: all plugins have `description`, `hooks`, `failClosed`, `enabledByDefault`
   - Verify `compression-level` is `enabledByDefault: true`
   - Verify existing 3 plugins are `enabledByDefault: false`

6. **Documentation Accuracy**
   - Spot-check README plugin section against actual registry
   - Spot-check CONTRIBUTORS plugin section against actual hook lifecycle
   - Verify no stale `install.sh` references remain

7. **Website**
   - Verify HTML is well-formed (no unclosed tags)
   - Verify memories section content matches README

8. **Installer**
   - Run `python3 install.py --help` — should show `--with-memories` option
   - Syntax check: `python3 -c "import ast; ast.parse(open('install.py').read())"`

9. **CI/CD**
   - Check `.github/workflows/test.yml` for valid YAML
   - Verify no references to non-existent files

10. **Hooks**
    - Parse `.cursor/hooks.json` — valid JSON
    - Verify entries match actual hook files

### Reporting
Write a summary in Execution Notes with:
- PASS/FAIL for each category
- Any issues found and whether they were fixed
- Overall verdict: Ready for merge / Needs fixes

## Testing Strategy
This IS the final verification phase. Run the full test suite:
```bash
python3 scripts/test.py
```

## Execution Notes

### Agent Session Info
- Agent: integrity-expert
- Started: 2026-04-05
- Completed: 2026-04-05

### Integrity Audit Report

**Scope:** Full — all changes from subtasks 01-09
**Date:** 2026-04-05

#### Summary

| Category | Status | Issues |
|----------|--------|--------|
| CRUX Sync | PASS | 0 (in-scope files current; `install.crux.md` stale is pre-existing) |
| Test Suite | PASS | 0 — 236/236 tests pass |
| Linter | PASS | 0 — no linter errors on any of the 19 modified files |
| Registry | PASS | 0 — valid JSON, 4 plugins, correct schema |
| Backward Compat | PASS | 0 — advisory quality gate is intentional and documented |
| Documentation | PASS | 0 — README, CONTRIBUTORS, AGENTS accurate; no stale `install.sh` refs |
| Website | PASS | 0 — HTML balanced (div 104/104, section 9/9, span 87/87), memories section present |
| Installer | PASS | 0 — syntax OK, `--help` shows `--with-memories` |
| CI/CD | PASS | 0 — all 4 workflow YAML files valid, no stale references |
| Hooks | PASS | 0 — `hooks.json` valid, referenced scripts exist |

**Overall Status:** PASS — Ready for merge

#### Detailed Findings

**1. CRUX Synchronization**

| CRUX File | Source | sourceChecksum | Status |
|-----------|--------|----------------|--------|
| `.cursor/rules/docs-sync.crux.md` | `docs-sync.md` | 1356781034 | CURRENT |
| `.cursor/rules/docs-sync.crux.mdc` | `docs-sync.crux.md` | 1356781034 | CURRENT |
| `install.crux.md` | `install.sh` (deleted) | 3344498055 | STALE (pre-existing, out of scope) |

Other modified files (`crux-compress.md`, `crux-cursor-rule-manager.md`, `crux-utils.py`, `SKILL.md`, `install.py`, `README.md`, `CONTRIBUTORS.md`, web files, test files) do not have CRUX counterparts — no sync needed.

**2. Test Suite**

```
236 passed in 2.89s — zero failures, zero skipped
```

Key new tests: `test_n_plugin_registry.py` (12 tests) validates registry schema, `enabledByDefault` semantics, and `compression-level` plugin entry. Updated tests: `test_crux_utils.py` (new `--target` tests), `test_install.py` (new `--with-memories` and `setup_memories` tests).

**3. Linter Compliance**

ReadLints on all 19 modified files: "No linter errors found."

**4. Backward Compatibility**

Traced `/crux-compress @file.md` flow:
- Level resolution: CLI flag → frontmatter `crux: <n>` → default 25/80 — **unchanged**
- Compression mechanics: identical
- Output format (frontmatter, .crux.md/.crux.mdc convention): **unchanged**
- Default plugin loading: `compression-level` loads automatically (no `--plugin` flags needed)
- Advisory quality gate change: with plugin active, CRUX file is written even if ratio target missed (`failClosed: false`). Without plugin, agent enforces hard gate. **Documented in agent spec line 91.**
- `--no-plugin compression-level` restores pre-plugin-era hard quality gate behavior

**5. Registry Validation**

| Plugin | description | hooks | failClosed | enabledByDefault |
|--------|-------------|-------|------------|-----------------|
| compression-level | string | [beforeCompress, afterCompress] | false | **true** |
| frontmatter-tagger | string | [afterCompress] | false | false |
| quality-gate | string | [afterValidate] | false | false |
| release-notes | string | [afterCompress, afterValidate] | false | false |

All fields present with correct types. Schema matches spec in `compression-level.md`.

**6. Documentation Accuracy**

- README plugin section (lines 474-513): JSON block matches actual `registry.json` verbatim
- README `--no-plugin` flag documented in flags table
- README `--with-memories` flag documented with install options
- README test coverage table includes `test_n_plugin_registry.py`
- CONTRIBUTORS Plugin System section (lines 276-328): hook lifecycle accurate, `enabledByDefault` documented, "Adding a New Plugin" guide present
- Zero `install.sh` references in README.md and CONTRIBUTORS.md (ripgrep confirmed)

**7. Website**

- HTML tag balance: div (104/104), section (9/9), span (87/87)
- Memories section: present (section id="memories"), with Dream/REM Sleep/MindReader modes, opt-in badge, and README link
- Install command: `curl -fsSL .../install.py | python3 -` (correct, not install.sh)

**8. Installer**

- `python3 install.py --help`: shows `--with-memories` option
- `python3 -c "import ast; ast.parse(...)"`: SYNTAX OK
- All functions defined (`check_dependencies`, `setup_memories`, etc.)

**9. CI/CD**

- `test.yml`, `release.yml`, `version-bump.yml`, `deploy-pages.yml`: all valid YAML
- Zero `install.sh` references across all 4 workflow files
- Referenced files all exist on disk

**10. Hooks**

- `.cursor/hooks.json`: valid JSON
- `sessionStart` → `crux-session-start.py` (exists)
- `afterFileEdit` → `crux-detect-changes.py` (exists)
- `crux-post-dream.py`: exists, correctly NOT in hooks.json (programmatic invocation only), header documents this

#### Pre-existing Issues (Out of Scope)

1. `install.crux.md` — references `⟦CRUX:install.sh` with stale sourceChecksum. The old install.sh was replaced by install.py; this CRUX file needs regeneration but is outside this plan's scope.
2. `.cursor/commands/crux-test.md` lines 108-110 — reference `install.sh` for validation steps. Pre-existing stale reference.
3. `CHANGELOG.md` — historical `install.sh` references (correct for historical records).

#### Verdict

**PASS — Ready for merge.** All 10 audit categories pass. No regressions identified. All 236 tests pass. No linter errors. Documentation, website, and configuration are consistent and accurate.

### Work Log

1. Ran full test suite: 236/236 pass
2. Ran `install.py --help` and syntax check: both pass
3. Validated CRUX sync for `docs-sync.crux.md` / `.crux.mdc` — sourceChecksum 1356781034 matches source
4. Validated all JSON configs: registry.json, hooks.json, pending-compression.json, crux.json
5. Validated all 4 CI/CD workflow YAML files
6. Checked all workflow files for stale install.sh references: none
7. Verified HTML tag balance on website
8. Verified memories section exists on website
9. Verified install command on website uses install.py
10. Spot-checked README plugin section vs actual registry.json — matches exactly
11. Spot-checked CONTRIBUTORS plugin section vs hook lifecycle — accurate
12. Verified no install.sh references in README.md or CONTRIBUTORS.md
13. Traced backward compatibility through command and agent specs
14. ReadLints on all 19 modified files: zero errors

### Blockers Encountered

None.

### Files Modified

- `plans/20260404-memories-plugin-integration/subtask-10-mpi-integrity-audit-20260404.md` — audit results written

---

### Adversarial Verification (Independent)

**Verifier:** integrity-expert (adversarial, did NOT execute the original work)
**Date:** 2026-04-05

#### Methodology

All checkboxes were reset to unchecked. Each deliverable was independently verified from scratch using fresh tool invocations — not by trusting the original audit's claims.

#### Independent Verification Results

| # | Check | Method | Result |
|---|-------|--------|--------|
| 1 | CRUX sync | `crux-utils.py --cksum .cursor/rules/docs-sync.md` → 1356781034; compared to `sourceChecksum` in both `.crux.md` and `.crux.mdc` frontmatter | **PASS** — checksums match |
| 2 | Test suite | `python3 scripts/test.py` — 236/236 passed in 2.44s, zero failures, zero skipped | **PASS** |
| 3 | Linter | `ReadLints` on install.py, crux-utils.py, registry.json, index.html, hook scripts | **PASS** — no errors |
| 4 | Registry | Parsed JSON; validated all 4 plugins have `description` (string), `hooks` (list), `failClosed` (bool), `enabledByDefault` (bool); confirmed `compression-level` is `enabledByDefault: true`, other 3 are `false` | **PASS** |
| 5 | Installer | `python3 -c "import ast; ast.parse(open('install.py').read())"` → SYNTAX OK; `python3 install.py --help` → shows `--with-memories` | **PASS** |
| 6 | Hooks | Parsed `.cursor/hooks.json` — valid JSON, version 1, `sessionStart` → `crux-session-start.py`, `afterFileEdit` → `crux-detect-changes.py`; all 3 hook scripts exist on disk | **PASS** |
| 7 | CI/CD | `yaml.safe_load()` on all 4 workflow files; no `install.sh` references | **PASS** |
| 8 | Backward compat | Traced `/crux-compress` flow through command spec; level resolution, output format, plugin loading semantics documented; `--no-plugin compression-level` restores pre-plugin behavior | **PASS** |
| 9 | Documentation | README plugin JSON matches `registry.json` verbatim; CONTRIBUTORS plugin section accurate; no `install.sh` in README/CONTRIBUTORS/website; AGENTS.md lists all 5 agents correctly | **PARTIAL** — see finding #1 below |
| 10 | Website | Memories section present (id="memories") with Dream/REM/MindReader; install command uses `install.py | python3 -`; no `install.sh` substring found | **FAIL** — see finding #2 below |

#### Findings the Original Audit Missed

**Finding #1: README TOC has broken anchor links (WARNING)**

Lines 26-27 of `README.md`:
- `[5. \`crux-session-start.py\` - The Hook](#5-crux-session-startsh---the-hook)` — anchor contains `sh` instead of `py`; furthermore, actual section 5 is `crux-compress.md` (the Command), not `crux-session-start.py` (the Hook)
- `[6. \`crux-detect-changes.py\` - The Hook](#6-crux-detect-changessh---the-hook)` — anchor contains `sh` instead of `py`

The TOC numbering for sections 3-5 is misaligned with actual `###` headers:
- TOC section 3 (`crux-cursor-rule-manager`) → actual section 3 is `_CRUX-RULE.mdc`
- TOC section 4 (`/crux-compress`) → actual section 4 is `crux-cursor-rule-manager.md`
- TOC section 5 (`crux-session-start.py`) → actual section 5 is `crux-compress.md`

The display text shows `.py` (correct filenames) but the links are broken. `README.md` is listed as modified by this plan.

**Finding #2: Website "What Gets Installed" section references `.sh` hook files (ERROR)**

Lines 467-468 of `web/compress.md/index.html`:
```html
<div class="file-tree-item"><code>.cursor/hooks/crux-detect-changes.sh</code>...</div>
<div class="file-tree-item"><code>.cursor/hooks/crux-session-start.sh</code>...</div>
```

These should be `.py`, not `.sh`. The actual hook files are `crux-detect-changes.py` and `crux-session-start.py`. The `install.py` RELEASE_FILES list correctly references `.py`. This file was modified by this plan (subtask-04) and the error should have been caught.

The original audit checked for `install.sh` string references and HTML tag balance but did not verify that file paths listed in the "What Gets Installed" section point to actual files.

#### Verdict

**PARTIAL — 2 issues require fixes before merge.**

8 of 10 deliverable checks independently confirmed. Website and Documentation items have legitimate issues that the original audit missed. Both are straightforward to fix:

1. Fix website hook file extensions: `.sh` → `.py` on lines 467-468 of `index.html`
2. Fix README TOC anchors and section numbering alignment (lines 22-28)
