# Spec Assessment: /crux-forget Command

**Date**: 2026-04-06
**Assessor**: zoto-spec-judge (independent)
**Spec**: `specs/20260406-crux-forget/spec-crux-forget-20260406.md`
**Verdict**: **Conditional Approve** — Score: **3.8 / 5.0**

---

## Scoring Summary

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 4.0 | Covers all files, but has inaccuracies in line references and a missing update target |
| Feasibility | 4.5 | All subtasks are realistic and well-scoped for generalPurpose agents |
| Structure | 4.0 | Clean phasing, good dependency graph, minor dependency gap in subtask 06 |
| Specificity | 3.5 | Some subtasks give exact code; others leave execution ambiguous or have wrong line refs |
| Risk Awareness | 4.0 | Zip-contents-protection rule handled well; some risks unaddressed |
| Convention Compliance | 3.0 | Several structural inaccuracies against the actual codebase |

**Weighted Average**: **3.8**

---

## Key Strengths

1. **Comprehensive scope**: The spec identifies all 10 files/locations that need updating — command file, agent definition, docs (crux-memories, README, CONTRIBUTORS, AGENTS), website, config JSON, installer, and install.crux.md. Nothing obvious is missing from the file coverage.

2. **Zip-contents-protection compliance**: Decision 5 and subtask 06 correctly flag that `scripts/create-crux-zip.py` and `version-bump.yml RELEASE_PATHS` must NOT be auto-modified. The warning message in subtask 06 is well-worded and actionable.

3. **Clean dependency graph**: Phase 1 (command creation + agent update) and Phase 2 (docs/config/website) is a natural and correct decomposition. The Mermaid diagram is consistent with the manifest table.

4. **Pattern consistency**: The spec correctly identifies `crux-dream.md` and `crux-mindreader.md` as structural references and instructs agents to follow their patterns. The command design (usage variants, argument handling, spawning subagent) is consistent with the existing commands.

5. **Confirmation-first design**: Decision 2 (no `--yolo` auto-delete) is a sound safety decision for a destructive operation. The workflow requiring explicit user confirmation is well-designed.

6. **Testability**: Each subtask has a "Testing Strategy" section with the important note about not triggering global test suites during parallel execution.

---

## Findings

### Finding 1 — CRITICAL: `standard_files` does not include memory commands

**Subtask 06** instructs the agent to add `crux-forget.md` to `standard_files` (the backup list in `install.py`). However, the existing `standard_files` list (line 228) does **not** include `crux-dream.md` or `crux-mindreader.md` — it only contains core CRUX files, not memory system files:

```python
standard_files = [
    "CRUX.md", "AGENTS.md", "install.crux.md",
    ".crux/crux.json", ".crux/crux-release-files.json",
    ".cursor/hooks.json", ".cursor/agents/crux-cursor-rule-manager.md",
    ".cursor/commands/crux-compress.md",
    ".cursor/hooks/crux-detect-changes.py", ".cursor/hooks/crux-session-start.py",
    ".cursor/rules/_CRUX-RULE.mdc",
    ".cursor/skills/crux-utils/SKILL.md", ".cursor/skills/crux-utils/scripts/crux-utils.py",
]
```

Adding `crux-forget.md` to `standard_files` without also adding the other memory commands would be inconsistent. The subtask should either:
- (a) Note that `standard_files` does not include memory command files and add `crux-forget.md` only to `RELEASE_FILES` and `DEFAULT_MEMORIES_CONFIG`, or
- (b) Also add `crux-dream.md` and `crux-mindreader.md` to `standard_files` for consistency (scope creep risk).

**Recommendation**: Update subtask 06 to remove the `standard_files` instruction, since the existing memory commands are not in that list. Only `RELEASE_FILES` and `DEFAULT_MEMORIES_CONFIG` need updating.

### Finding 2 — MEDIUM: Subtask 06 dependency should include 02

Subtask 06 depends only on subtask 01 (command file creation). However, its `DEFAULT_MEMORIES_CONFIG` update and the agent file reference in the config are conceptually dependent on subtask 02 (agent update) being defined. While the dependency is soft (the config only references the command file, not the agent), the Mermaid diagram does not show a 02→06 edge, creating an inconsistency with how subtasks 03, 04, and 05 all depend on both 01 and 02.

**Impact**: Low — subtask 06 could execute correctly without 02 since it only references the command file path. But for consistency with the other Phase 2 subtasks, adding 02 as a dependency would be cleaner.

### Finding 3 — MEDIUM: Inaccurate line references in subtask 03

Subtask 03 gives specific line numbers for locations in `docs/crux-memories.md`:
- "Commands table (around line 15-21)" — **Correct** (verified: lines 15-20)
- "Configuration Schema commands block (around line 273-284)" — **Correct** (verified: lines 273-284)
- "Platform Capability Mapping table (around line 233-241)" — **Correct** (verified: lines 233-241)

However, there is a structural inaccuracy in the section numbering: subtask 03 refers to "section 1", "section 2", etc. as though they map to `## 1.`, `## 2.` headings. This is correct — the doc uses numbered headings. But the subtask says:

> "Section 5 — Example Interaction"

The Example Interaction section is actually `## 5.` (line 840). Similarly, "Section 8 — Evaluations" maps to `## 8.` (line 927). These are correct.

One issue: the subtask's instruction for "Section 3 — Platform Wiring" asks to add `/crux-forget` to three subsections (3a Cursor, 3b Claude Code, 3c Generic). However, the Platform Capability Mapping table at line 233 shows commands as patterns like `/crux-dream → .cursor/commands/crux-dream.md`, not individual commands. The table is a capability mapping, not a command registry. Adding `/crux-forget` as a separate row would bloat the table — it should be represented as a pattern or the existing row should be updated to show multiple commands. The subtask should give clearer guidance here.

### Finding 4 — MEDIUM: Missing `AGENTS.crux.md` regeneration

The spec updates `AGENTS.md` (subtask 04) to change the memory manager's purpose column. However, `AGENTS.md` has a corresponding CRUX compressed file. Per the CRUX rules, when updating a source file that has a corresponding `.crux.*` file, the CRUX file must also be updated with surgical diff changes. The spec does not mention regenerating `AGENTS.crux.md`.

**Recommendation**: Add a deliverable to subtask 04: "Update `AGENTS.crux.md` with surgical diff to reflect the new purpose column, or delegate to `crux-cursor-rule-manager`."

### Finding 5 — LOW: Subtask 05 SVG coordinate guidance may be insufficient

Subtask 05 gives specific SVG modifications: increase COMMANDS rect height from 90 to 108 and adjust arrow origins. The actual SVG (line 46) has `height="90"` — this matches. However, the instruction to add a third text line at `y="106"` is correct but does not account for the potential need to shift all downstream elements (AGENT box, arrows, skills boxes) if the COMMANDS box grows. The existing architecture diagram has tight spacing and the COMMANDS box's bottom edge at y=110 (20+90) is close to the arrow starting points.

**Recommendation**: Add a note to subtask 05 that the agent should verify all arrow endpoints and element positions after resizing the COMMANDS box, not just the specific items mentioned.

### Finding 6 — LOW: Website section naming inconsistency

Subtask 05 says to add the command "in the MindReader section" of the commands grid, but the commands grid (lines 749-772) is under a section titled "MindReader" that actually contains **all** commands (both `/crux-dream` and `/crux-mindreader`). The section is arguably misnamed — it's really a "Commands" section nested under the MindReader heading. This doesn't affect execution but could confuse the agent. The subtask correctly identifies the right location.

### Finding 7 — LOW: No mention of `crux-dream.md` Related section update

The existing `crux-dream.md` has a "Related" section (line 58-63) that lists `/crux-mindreader` but does not mention `/crux-forget`. Similarly, `crux-mindreader.md`'s "Related" section (line 78-83) lists `/crux-dream`. For a complete integration, both existing commands should cross-reference `/crux-forget`.

**Recommendation**: Add a deliverable (could be in subtask 01 or a separate subtask) to update the "Related" sections of `crux-dream.md` and `crux-mindreader.md` to include `/crux-forget`.

### Finding 8 — LOW: MindReader delete overlap

The existing `/crux-mindreader` command already has a post-display "Delete memories" option in its Next Steps Menu (line 66-73 of `crux-mindreader.md`). The spec acknowledges this in the Overview ("Currently, memory deletion is only available as a secondary action within `/crux-mindreader`'s post-display menu"). However, the spec does not discuss whether `/crux-mindreader`'s delete option should be kept, removed, or modified to delegate to `/crux-forget`. This is a design question, not necessarily a spec defect, but worth noting.

**Recommendation**: Add a note in the spec's Key Decisions or a new Decision 6 stating that `/crux-mindreader`'s existing delete action remains as-is, and `/crux-forget` provides a first-class alternative.

### Finding 9 — INFO: Eval test coverage in subtask 03

Subtask 03 proposes evaluation tests for the forget command (section 8 of `docs/crux-memories.md`). These tests are well-structured but are manual dev/user verification steps, not automated tests. This is consistent with the existing evaluation approach in the docs, so no issue here.

---

## Dependency Graph Audit

```
Phase 1:  [01] ──┐     [02] ──┐
                  │            │
Phase 2:  [03] ←─┤←───────────┤   ✓ correct
          [04] ←─┤←───────────┤   ✓ correct
          [05] ←─┤←───────────┤   ✓ correct
          [06] ←─┘             │   ⚠ missing 02 dependency (minor)
```

The Mermaid graph in the spec is consistent with the manifest table for subtasks 01-05 but omits the 02→06 edge. This is also reflected in the manifest where subtask 06 lists only `01` in its Dependencies column.

**Verdict**: The dependency graph is functionally correct — subtask 06 genuinely only needs the command file (01) to exist. The missing 02 edge is a consistency nit, not a blocking issue.

---

## Risk Analysis

| Risk | Severity | Mitigation in Spec |
|------|----------|--------------------|
| Zip-contents-protection violation | High | ✅ Well-handled — explicit warning in subtask 06, Decision 5 |
| CRUX generated file edited directly | High | ⚠ Partially handled — `install.crux.md` regeneration covered, but `AGENTS.crux.md` not mentioned |
| SVG diagram breakage | Medium | ⚠ Basic guidance given but full impact analysis left to agent |
| `standard_files` inconsistency | Medium | ❌ Not detected — spec assumes memory commands belong in this list |
| Cross-reference staleness | Low | ❌ Existing commands' Related sections not updated |
| MindReader delete overlap | Low | ❌ Not addressed — acceptable for initial version |

---

## Recommended Changes

### Must Fix (before execution)
1. **Subtask 06**: Remove instruction to add `crux-forget.md` to `standard_files` — existing memory commands are not in that list
2. **Subtask 04**: Add deliverable for `AGENTS.crux.md` surgical diff update (or delegation to `crux-cursor-rule-manager`)

### Should Fix
3. **Subtask 05**: Add note to verify all SVG element positions after COMMANDS box resize
4. **Subtask 01 or new subtask**: Add cross-references to existing commands' Related sections
5. **Subtask 06**: Consider adding subtask 02 as a dependency for consistency

### Nice to Have
6. **Spec index**: Add Decision 6 regarding MindReader's existing delete action coexistence
7. **Subtask 03**: Clarify Platform Capability Mapping table update approach (pattern vs individual entry)

---

## Verdict

**Conditional Approve — 3.8 / 5.0**

The spec is well-structured, comprehensive in scope, and demonstrates strong awareness of the repository's conventions (especially the zip-contents-protection rule). The phased dependency graph is clean and the command design is consistent with existing patterns.

However, there are two issues that should be fixed before execution:
1. The `standard_files` instruction in subtask 06 is factually incorrect — it would introduce an inconsistency with how existing memory commands are handled in the installer
2. The missing `AGENTS.crux.md` regeneration in subtask 04 would violate the repository's CRUX surgical diff update rule

After addressing these two findings, the spec would score in the **Approve** range (4.0+).
