# Spec Assessment: /crux-forget Command

**Target**: `specs/20260406-crux-forget/spec-crux-forget-20260406.md`
**Assessed**: 2026-04-07
**Assessor**: zoto-spec-judge (independent, fresh context)
**Prior Assessment**: `zoto-judge-assessment-crux-forget-20260406.md` (reviewed and superseded)
**Verdict**: **Approve** — Score: **4.25 / 5.0**

---

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 4.0/5 | All 10 requirements covered; spec index Decision 5 / Requirement 9 contradiction with subtask 06 re `standard_files`; missing cross-references in existing commands' Related sections |
| Feasibility | 5.0/5 | All subtasks are realistic, well-scoped, and delegate to existing skills/patterns |
| Structure | 4.5/5 | Clean two-phase dependency graph; manifest and Mermaid are consistent; subtask 06's dependency on only 01 is defensible |
| Specificity | 4.0/5 | Line references verified accurate; concrete code snippets provided; SVG coordinates checked; Platform Capability Mapping guidance slightly vague |
| Risk Awareness | 3.5/5 | Zip-contents-protection handled well; no rollback plan; SVG downstream impact analysis incomplete |
| Convention Compliance | 4.0/5 | Follows existing command/agent patterns; correct subagent and skill delegation; spec index mentions `standard_files` incorrectly |
| **Overall** | **4.25/5** | **Approve** |

---

## Findings

### Strengths

1. **Comprehensive file coverage**: The spec identifies all 10 files/locations that need updating — command file, agent definition, 4 documentation files, website, config JSON, installer, and install.crux.md. Nothing is missing from file coverage.

2. **Zip-contents-protection compliance**: Decision 5 and subtask 06 correctly flag that `scripts/create-crux-zip.py` and `version-bump.yml RELEASE_PATHS` must NOT be auto-modified. The warning message in subtask 06 is well-worded and actionable.

3. **Clean dependency graph**: Phase 1 (command creation + agent update) and Phase 2 (docs/config/website) is a natural and correct decomposition. The Mermaid diagram is verified consistent with the manifest table.

4. **Accurate line references**: All line number references in subtasks were verified against the actual codebase:
   - Subtask 03: Commands table (lines 15-20) ✓, Config schema commands (lines 273-284) ✓, Platform Capability Mapping (lines 233-241) ✓, Section 5 (line 840) ✓, Section 8 (line 927) ✓
   - Subtask 04: README Memory Commands (lines 662-672) ✓, README overview (lines 622-631) ✓, CONTRIBUTORS distributed files (lines 250-267) ✓, Memory System Components (lines 271-287) ✓
   - Subtask 05: SVG COMMANDS box (lines 46-49) ✓, Commands grid (lines 749-772) ✓, Lifecycle diagram (lines 154-200) ✓

5. **Correct pattern following**: The spec identifies `crux-dream.md` and `crux-mindreader.md` as structural references. The command design (usage variants, argument handling, subagent spawning) is consistent with existing commands.

6. **Confirmation-first design**: Decision 2 (no `--yolo` auto-delete) is a sound safety decision. The workflow requiring explicit user confirmation before destructive operations is well-designed.

7. **Subtask 06 correctly handles `standard_files`**: Despite the spec index's incorrect mention of `standard_files`, subtask 06 explicitly and correctly states NOT to modify it (deliverable line 17, implementation notes section B, CRUX update notes, testing strategy). This demonstrates good codebase-aware subtask design.

---

### Issues

| # | Severity | Location | Finding | Recommendation |
|---|----------|---------|---------|----------------|
| 1 | MEDIUM | Spec index | Decision 5 and Requirement 9 mention adding to `standard_files`, but subtask 06 correctly says NOT to. Internal contradiction. | Remove `standard_files` from Decision 5 and Requirement 9 to match subtask 06 |
| 2 | MEDIUM | Spec index / Subtask 01 | Existing commands `crux-dream.md` (line 63) and `crux-mindreader.md` (line 83) have Related sections that don't mention `/crux-forget`. No subtask covers adding these cross-references. | Add deliverable to subtask 01: update Related sections of `crux-dream.md` and `crux-mindreader.md` to include `/crux-forget` |
| 3 | LOW | Subtask 05 | SVG modification guidance gives specific coordinates for the COMMANDS box resize and third text line, but does not instruct the agent to verify all downstream SVG element positions (arrows, AGENT box) after resizing | Add implementation note: "After resizing the COMMANDS box, verify all arrow endpoints and adjacent element positions still align correctly" |
| 4 | LOW | Spec index | No rollback plan documented. If execution partially fails, there is no guidance on reverting partial changes. | Add a brief rollback note to the spec index |
| 5 | LOW | Subtask 03 | Platform Capability Mapping table guidance says to "ensure the pattern `/crux-forget` is covered" but doesn't specify whether to add a new row or update the existing command row pattern | Clarify: the existing row `Commands` at line 236 uses `/crux-dream` as a representative example; update the pattern to show `/crux-{dream,mindreader,forget}` or add the new command |
| 6 | INFO | Spec index | MindReader's existing post-display delete action (line 66-73 of `crux-mindreader.md`) coexists with the new `/crux-forget`. No decision documents whether these remain parallel or one delegates to the other. | Consider adding Decision 6 noting the intentional coexistence |

### Previous Assessment Corrections

The prior assessment (`zoto-judge-assessment-crux-forget-20260406.md`) contained two factual errors that this reassessment corrects:

| Prior Finding | Prior Claim | Actual State | Verdict |
|---|---|---|---|
| Finding 1 (CRITICAL) | "Subtask 06 instructs the agent to add `crux-forget.md` to `standard_files`" | Subtask 06 explicitly says NOT to modify `standard_files` (deliverable line 17, section B, line 74, line 94). The issue is in the spec INDEX (Decision 5, Requirement 9), not the subtask. | Severity downgraded to MEDIUM — subtask is correct; only spec index text needs fixing |
| Finding 4 (MEDIUM) | "Missing `AGENTS.crux.md` regeneration" | `AGENTS.crux.md` does not exist as a persistent file (0 files found). It is only an intermediate artifact used during installation (`install.py` line 469-470, deleted at line 341). `AGENTS.md` is a source file edited directly. | Finding is invalid — no action needed |

---

### Dependency Graph

```
Phase 1:  [01] ──┐     [02] ──┐
                  │            │
Phase 2:  [03] ←─┤←───────────┤   ✓ correct
          [04] ←─┤←───────────┤   ✓ correct
          [05] ←─┤←───────────┤   ✓ correct
          [06] ←─┘                 ✓ only needs 01 (command file path)
```

The Mermaid graph matches the Subtask Manifest exactly. All edges verified:
- 01→03, 01→04, 01→05, 01→06 ✓
- 02→03, 02→04, 02→05 ✓
- No 02→06 edge — correct, since subtask 06 only references the command file path (created by 01), not the agent definition (created by 02)
- No circular dependencies ✓
- Lower IDs never depend on higher IDs ✓
- Phase assignments consistent with dependencies ✓

---

### Subtask Manifest Validation

| Check | Result |
|-------|--------|
| All listed files exist in spec directory | ✓ All 6 subtask files present |
| Subtask metadata matches manifest | ✓ IDs, dependencies, phases all consistent |
| Assigned subagent appropriate | ✓ `generalPurpose` suitable for all documentation/config tasks |
| No subtask depends on higher-numbered ID | ✓ |
| Phase assignments consistent with dependencies | ✓ |

### Subtask Quality

| ID | Single Responsibility | Concrete Deliverables | Correct Dependencies | Adequate Guidance | Testing Strategy |
|----|:---:|:---:|:---:|:---:|:---:|
| 01 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 02 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 03 | ✓ | ✓ (6 items) | ✓ | ✓ | ✓ |
| 04 | ✓ | ✓ (5 items) | ✓ | ✓ | ✓ |
| 05 | ✓ | ✓ (3 items) | ✓ | ✓ | ✓ |
| 06 | ✓ | ✓ (6 items) | ✓ | ✓ | ✓ |

---

### Risk Summary

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Zip-contents-protection violation | Low | High | ✅ Well-handled — Decision 5, subtask 06 explicit warning |
| SVG diagram breakage after resize | Medium | Low | ⚠ Basic coordinates given; downstream adjustment note missing |
| Spec index misleads agent on `standard_files` | Medium | Medium | ⚠ Subtask 06 is correct, but agent could read spec index first and get confused |
| Cross-reference staleness | Low | Low | ❌ Existing commands' Related sections not updated |
| MindReader delete overlap confusion | Low | Low | ⚠ Not documented; acceptable for initial version |
| `install.crux.md` pre-existing drift | Medium | Low | ⚠ The `M.standard_files(backup)` block in `install.crux.md` already includes memory commands not present in actual `install.py` — subtask 06 agent should be aware |

---

## Recommendation

The spec is well-structured, comprehensive, and ready for execution. The dependency graph is clean and verified, all file references check out against the actual codebase, and the subtask implementation notes are more accurate than the spec index text in the one area of contradiction (`standard_files`). The two MEDIUM issues (spec index text contradiction, missing cross-references) should ideally be fixed before execution but are not blocking — subtask 06 already has the correct behavior documented. After addressing the MEDIUM findings, the spec would score 4.5+.
