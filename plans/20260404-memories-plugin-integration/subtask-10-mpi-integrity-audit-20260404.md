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
- [ ] CRUX sync: all modified source files have up-to-date `.crux.md`/`.crux.mdc` counterparts
- [ ] Test suite: `python3 scripts/test.py` passes cleanly
- [ ] Linter: no errors in any modified files (use ReadLints)
- [ ] Registry: `.crux/plugins/registry.json` is valid JSON with correct schema
- [ ] Backward compat: existing `/crux-compress` invocations produce identical behavior
- [ ] Documentation: README, CONTRIBUTORS, AGENTS accurately reflect current state
- [ ] Website: `web/compress.md/index.html` is well-formed HTML
- [ ] Installer: `install.py` syntax-checks and `--help` works
- [ ] CI/CD: workflow YAML files are syntactically valid
- [ ] Hooks: `hooks.json` is valid JSON with correct entries

## Definition of Done
- [ ] All audit checks pass
- [ ] No regressions identified
- [ ] Audit report written in Execution Notes below
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
