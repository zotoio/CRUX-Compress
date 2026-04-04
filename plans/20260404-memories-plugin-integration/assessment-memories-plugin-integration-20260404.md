# Plan Assessment: Memories & Plugin Integration

**Target**: `plans/20260404-memories-plugin-integration/plan-memories-plugin-integration-20260404.md`
**Assessed**: 2026-04-04
**Verdict**: Conditional

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 3/5 | Gap analysis partially stale; website `install.sh` gap unaddressed; no rollback plan |
| Feasibility | 4/5 | Subtasks are achievable; subtask 03 overlaps with existing uncommitted changes |
| Structure | 4/5 | Dependencies and phases correct; subtask 01+06 split adds unnecessary handoff |
| Specificity | 4/5 | Strong code examples in 06; subtask 04 vague on placement |
| Risk Awareness | 2/5 | No rollback plan; uncommitted change overlap unidentified; no branch divergence risk |
| Convention Compliance | 4/5 | Follows plan template precisely; appropriate agent assignments |
| **Overall** | **3.55/5** | **Conditional — address stale analysis and risk gaps before execution** |

## Findings

### Strengths

- **Thorough gap analysis tables** for both workstreams with clear current-state/gap columns
- **Well-specified plugin architecture** in subtask 01, with exact JSON schema and hook specifications
- **Concrete code examples** in subtask 06 showing exact before/after for `crux-utils.py` changes
- **Proper deferred testing strategy** — global test suite deferred to subtask 08, preventing parallel execution conflicts
- **Correct agent assignments** — `docs-sync-agent` for docs (09), `integrity-expert` for audit (10), `generalPurpose` for implementation
- **Key Decision 5** correctly protects `CRUX.md` from modification per foundational rules
- **Key Decision 8** correctly avoids registering `crux-post-dream.py` in `hooks.json`
- **Zero-breaking-change invariant** stated clearly and traced through the data flow in subtask 07
- **Definition of Done** is comprehensive (11 items covering backward compat, CI, installer, website)

### Issues

| # | Severity | Subtask | Finding | Recommendation |
|---|----------|---------|---------|----------------|
| 1 | **High** | 03 | **Gap analysis is stale for CI/CD.** The plan states `test.yml` references `install.sh` and `bats tests/*.bats`, but the committed `test.yml` at HEAD has no `bats` reference. Furthermore, the working tree already has uncommitted diffs removing `install.sh` steps from `test.yml` and `version-bump.yml`, and updating `release.yml` to use `install.py`. Subtask 03's deliverables partially overlap with these existing changes. | Re-verify `test.yml` committed state vs working tree before execution. Update subtask 03 deliverables to reconcile with the existing uncommitted changes. If changes are already made, subtask 03 should validate rather than re-implement. |
| 2 | **High** | — | **No rollback plan.** The previous memories plan (`20260403`) explicitly included a rollback section. This plan has no rollback guidance. If the plugin architecture design proves flawed during implementation, there's no documented path to undo. | Add a Rollback section to the plan index. At minimum: "All changes on `feat/memories` branch. To revert, reset to pre-execution commit." |
| 3 | **Medium** | 04 | **Website `install.sh` reference not addressed.** `web/compress.md/index.html` lines 406 and 414 reference `curl ... install.sh \| bash` in the quickstart section. Subtask 04 explicitly says "Do not modify the install command on the website (that's a separate concern)" — but no other subtask addresses it either. This is a stale reference gap. | Either expand subtask 04 to also fix the install command, or add a new deliverable to subtask 03 or 09 to update the website install reference. |
| 4 | **Medium** | 05 | **`crux-post-dream.py` already has correct documentation.** The file's docstring already states: "Invoked by the crux-dream command/skill after memory extraction completes." Subtask 05's first deliverable to "update header comment" may be a no-op. | Rephrase deliverable to "Verify `crux-post-dream.py` header comment correctly documents programmatic invocation model" (verify rather than update). |
| 5 | **Medium** | 01, 06 | **Design/implementation split adds unnecessary handoff.** Subtask 01 produces a "design document in this subtask's Execution Notes." Subtask 06 then reads those notes. Since the plan index already contains the full design (registry schema, hook specs, key decisions), the design subtask adds a handoff step without significant value. The executing agent for subtask 06 already has all needed context in the subtask file itself. | Consider merging subtask 01 into subtask 06, or reframe subtask 01 as "registry schema update only" (the concrete JSON edit) and move the design narrative into the plan index where it already partially lives. |
| 6 | **Low** | 03 | **`bats` reference in gap analysis is incorrect.** The plan states `test.yml` references `bats tests/*.bats`, but no such reference exists in either the committed or working tree versions of `test.yml`. The `bats` reference exists only in `scripts/test.py` (which conditionally runs bats if `.bats` files exist). | Correct the gap analysis table to reference `scripts/test.py` instead of `test.yml` for the bats issue, or remove this gap if it's already resolved. |
| 7 | **Low** | 04 | **Vague placement guidance.** Subtask 04 says the memories section should go "After the existing compression type cards OR as a new section before the quickstart." The executing agent must make a design decision that could require revision. | Pick one placement and commit to it in the subtask. Recommend: after the URL compression section and before the Notation section, since memories is a capability, not a compression type. |
| 8 | **Low** | 08 | **Test file naming convention gap.** The existing memory eval tests skip `test_j_*.py` (letters go a, b, c, d, e, f, g, h, i, k, l, m). The plan doesn't mention this gap or whether new test files should follow the same convention. | Note the naming convention gap; ensure `test_plugin_registry.py` naming is consistent with the project's eval test naming pattern (consider `test_n_plugin_registry.py` to follow the lettered sequence). |

### Dependency Graph

The mermaid graph matches the Subtask Manifest exactly. All edges are verified correct:

- `01 → 06 → 07 → 08`: Plugin design → implementation → spec updates → tests (correct sequential chain)
- `02, 03, 04, 05 → 08`: All Phase 1 memory subtasks feed into testing (correct)
- `08 → 09 → 10`: Tests → docs → audit (correct)
- No missing edges detected
- No unnecessary sequential constraints — Phase 1 subtasks are correctly parallelized
- Subtask IDs are numbered in dependency order (lower never depends on higher)

**One structural observation**: Subtask 06 depends only on 01 (Phase 2), but subtask 07 depends only on 06 (Phase 3). The `01 → 06 → 07` chain introduces 3 sequential phases for the plugin workstream while the memory workstream (02-05) completes in 1 phase. If 01 and 06 were merged, the plugin chain would be `06 → 07` (2 phases), better aligning the two workstreams and reducing total execution time.

### Risk Summary

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Subtask 03 conflicts with uncommitted changes | High | Medium | Re-verify working tree state before execution; reconcile or commit existing changes first |
| Website `install.sh` reference remains stale after plan completion | High | Low | Add website install command fix to an existing subtask |
| Plugin design proves unworkable at implementation | Low | High | **Not mitigated** — add rollback plan and a checkpoint after subtask 01 |
| `feat/memories` branch diverges from `main` during execution | Medium | Medium | **Not mitigated** — consider a rebase checkpoint before Phase 4 |
| Parallel Phase 1 subtasks create merge conflicts | Low | Low | Subtasks modify disjoint files; minimal risk |
| Backward compatibility regression undetected until subtask 10 | Low | High | Subtask 07 traces data flow; subtask 08 runs full tests; mitigated |

## Recommendation

**Conditional Approval.** The plan is well-structured with strong specificity and appropriate agent assignments, but should not be executed until three issues are resolved: (1) reconcile the CI/CD gap analysis with the actual working tree state and existing uncommitted changes, (2) add a rollback plan, and (3) address the website `install.sh` reference gap. Merging subtasks 01 and 06 is recommended but not required.
