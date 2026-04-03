# Plan Assessment: CRUX Memories System

**Target**: `plans/20260403-crux-memories/plan-crux-memories-20260403.md`
**Assessed**: 2026-04-03
**Verdict**: Approve

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 5/5 | All spec requirements covered; 14 subtasks with concrete deliverables |
| Feasibility | 4/5 | All subtasks achievable; MCP server is substantial but well-scoped |
| Structure | 5/5 | Clean direct-only deps, consistent graph/manifest, good parallelism |
| Specificity | 5/5 | Concrete deliverables, explicit config values, clear implementation notes |
| Risk Awareness | 4/5 | Rollback plan added; `.gitignore` addressed; TF-IDF fallback clarified |
| Convention Compliance | 4/5 | Follows existing patterns; per-directory deps; `.md` → `.crux.mdc` pipeline clarified |
| **Overall** | **4.5/5** | **Approve — ready for execution** |

## Findings

### Strengths

- **Comprehensive spec coverage**: All 12 requirements from the plan index map cleanly to deliverables. The 6 skills, 1 agent, 2 commands, platform wiring, MCP server, evals, and documentation are all covered across 14 subtasks.
- **Well-structured phasing**: The 7-phase execution order correctly respects dependencies. Phase 2 (skills 02-04), Phase 3 (skills 05-07), Phase 4 (agent + MCP), Phase 6 (evals + checklists), and Phase 7 (more evals + docs) all exploit parallelism effectively.
- **Clean dependency convention**: Manifest and graph use direct-only dependencies consistently — no transitive deps listed, graph matches manifest exactly.
- **Clear subtask format**: Every subtask has a consistent structure — Metadata, Objective, Deliverables Checklist, DoD, Implementation Notes, and Testing Strategy.
- **Spec-driven implementation notes**: Each subtask references specific sections of `docs/crux-memories.md`, reducing ambiguity.
- **Convention awareness**: The plan correctly identifies existing agent, skill, command, and hook patterns to follow.
- **Subtask manifest fully verified**: All 14 subtask files exist, all Metadata sections match the manifest, no subtask depends on a higher-numbered ID, and phase assignments are consistent with dependency ordering.
- **Eval split**: The eval suite is split into three focused subtasks (11: infra + A-E, 12: F-M, 13: user checklists) with good parallelism.
- **Test orchestration**: `scripts/test.sh` update is an explicit deliverable in subtask 11.
- **Rollback plan**: Branch-based rollback documented in the plan index.

### Issues (all resolved)

| # | Status | Subtask | Finding | Resolution |
|---|--------|---------|---------|------------|
| 1 | **RESOLVED** | 09 | Python module naming conflict | Renamed to `crux_mcp_server/` |
| 2 | **RESOLVED** | 09 | Server naming inconsistency | Plan aligned on `crux_mcp_server`; spec update during subtask 09 |
| 3 | **RESOLVED** | 11 | Eval subtask oversized | Split into subtasks 11 (infra + A-E), 12 (F-M), 13 (user checklists) |
| 4 | **RESOLVED** | 11 | Test orchestration gap | `scripts/test.sh` update added as deliverable to subtask 11 |
| 5 | **RESOLVED** | 01 | Vague `watchDir` config | Set to `"plans"` matching `unitOfWork` = `"plan"` |
| 6 | **RESOLVED** | 10 | CRUX compression pipeline | Clarified `.md` → `.crux.mdc` direct generation |
| 7 | **RESOLVED** | 01 | No `.gitignore` consideration | Added `.gitignore` deliverable for generated files |
| 8 | **RESOLVED** | 09 | Heavy optional dependency | TF-IDF fallback uses Python stdlib only; `sentence-transformers` marked optional |
| 9 | **RESOLVED** | — | Manifest listed transitive deps | Converted to direct-only deps; graph and manifest now consistent |
| 10 | **RESOLVED** | 09, 11 | No Python version constraint | Python `>=3.10` specified in subtask 09 and eval `requirements.txt` |
| 11 | **RESOLVED** | — | No rollback plan | Rollback section added to plan index |

### Dependency Graph

- **Manifest ↔ graph consistency**: Both use direct-only dependencies — every edge in the graph corresponds to a manifest dependency and vice versa.
- **Parallelism**: Phase 2 (3 skills), Phase 3 (3 skills), Phase 4 (agent + MCP server), Phase 6 (eval infra + user checklists), and Phase 7 (eval F-M + docs) all run subtasks in parallel.
- **No circular dependencies**: Confirmed — all dependencies flow from lower to higher subtask IDs.
- **Phase assignments verified**: Every subtask's phase is strictly higher than all its dependencies' phases.

### Risk Summary

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| MCP server is the most complex single subtask | Medium | Medium | Well-scoped deliverables, modular architecture, graceful TF-IDF fallback |
| Eval tests may need adjustment as skills are refined | Low | Low | Tests use fixtures and tmp_path; independent of live repo |
| `sentence-transformers` unavailable in some environments | Medium | Low | Stdlib TF-IDF fallback requires no extra deps |

## Recommendation

The plan is ready for execution. All previously identified issues have been resolved: module naming fixed, eval suite split into manageable pieces, dependency convention is clean and consistent, test orchestration gap addressed, config values are concrete, and rollback is documented. Proceed with `/crux-execute`.
