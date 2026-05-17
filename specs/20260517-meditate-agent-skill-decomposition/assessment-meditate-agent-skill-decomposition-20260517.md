# Spec Assessment: Meditate Agent + Skill Decomposition

**Target**: `specs/20260517-meditate-agent-skill-decomposition/spec-meditate-agent-skill-decomposition-20260517.md`  
**Assessed**: 2026-05-17  
**Verdict**: Conditional

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 4/5 | The spec covers the approved command -> guide agent -> six-skill split, evals, docs, install/dist, CRUX sync, and final integrity review. A few convention-sensitive details need tightening before execution. |
| Feasibility | 4/5 | The work is achievable and well phased. The only feasibility concern is that subtask 09 combines documentation sync with Python/script/workflow edits under an agent not meant for that whole surface. |
| Structure | 4/5 | The 8-phase dependency graph is coherent, acyclic, and matches the manifest. Phase sequencing is conservative but defensible for a functional-preservation refactor. |
| Specificity | 4/5 | Deliverables are concrete and mostly verifiable. Some language still leaves approved choices open, especially skill count and naming. |
| Risk Awareness | 4/5 | The freeze-line contract, mapping documents, test plan, targeted evals, and integrity review are strong controls. CRUX mirror and dist/install risks need sharper wording. |
| Convention Compliance | 3/5 | Most CRUX, zip-content, docs-sync, and status conventions are considered, but `AGENTS.crux.md` is treated as a maintained mirror and subtask 09's agent assignment conflicts with repository allocation rules. |
| **Overall** | **3.9/5** | **Conditional** |

## Findings

### Strengths

- The manifest and mermaid graph agree: every listed subtask file exists, metadata matches the manifest, dependencies only point backward, and each phase is greater than its dependencies' phases.
- The architecture follows the approved split: thin `/crux-meditate` coordinator, new `crux-cursor-meditation-guide` agent, and `crux-skill-memory-meditation-{verb}` skills.
- The freeze-document, architecture-mapping, eval-plan, implementation, CRUX-sync, and integrity-review chain gives later reviewers a concrete way to check "no functionality loss."
- Status scaffolding is present for all 11 subtasks with paired `.status.yml` / `.status.md` files, schema-shaped fields, pending states, and block markers compatible with Spec System round-trip conventions.

### Issues

| # | Severity | Subtask | Finding | Recommendation |
|---|----------|---------|---------|----------------|
| 1 | HIGH | 09, 10, index | The spec repeatedly treats `AGENTS.md` -> `AGENTS.crux.md` as a maintained CRUX mirror. `AGENTS.crux.md` is not checked into this repo and is a transient install artifact, so requiring regeneration would violate the approved "existing mirrors only" scope and repeat a known false-positive. [memory:AGENTS.crux.md is a transient install-time artifact, not a maintained CRUX file] | Remove `AGENTS.crux.md` from the index examples and subtasks 09/10. Say `AGENTS.md` is edited directly and only pre-existing checked-in mirrors with generated frontmatter, such as `.cursor/rules/crux-memories-integration.crux.mdc` or `docs-sync.crux.*`, may be regenerated. |
| 2 | HIGH | 09 | Subtask 09 is assigned to `docs-sync-agent`, but it also owns `install.py`, `scripts/create-crux-zip.py`, `.crux/dist-manifest.json`, and `.github/workflows/version-bump.yml`. Repository allocation rules reserve code/script/config implementation for `crux-software-engineer`; `docs-sync-agent` is appropriate for README/CONTRIBUTORS/web/docs sync, not the whole install/dist surface. | Split subtask 09 into docs-sync and install/dist subtasks, or reassign the install/dist portion to `crux-software-engineer` while preserving the 8-phase sequencing. |
| 3 | MEDIUM | 02, 05, index | The user-approved structure fixes the skill family to six skills, but subtask 02 still allows consolidation/splitting and the index says the final count may be adjusted at user review. | Lock the skill list to the six approved skills unless the executor escalates a `needs_user_input` decision and receives explicit approval to change it. |

### Dependency Graph

- The graph matches the Subtask Manifest exactly and preserves the requested 8 phases.
- Parallelism is reasonable: phase 3 separates eval planning, guide agent creation, and skill creation; phase 6 separates tests from docs/install/dist.
- If subtask 09 is split, keep both resulting subtasks in phase 6 and make subtask 10 depend on the install/dist half plus any docs/rule-source half that touches CRUX-mirrored sources.

### Risk Summary

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Non-existent `AGENTS.crux.md` gets created or demanded | Medium | High | Remove it from CRUX-sync deliverables; use a checked-in-mirror test before any regeneration. |
| Docs agent edits Python/workflow distribution code | Medium | Medium | Reassign or split subtask 09 by ownership. |
| Six-skill architecture drifts during execution | Medium | Medium | Make the six skill directories non-negotiable in subtasks 02 and 05. |
| Live status checklists are terse because multiline checklist text is truncated | Low | Low | Keep as non-blocking, but have executors and judges verify against the original subtask markdown for full item text. |

## Recommendation

Do not mark the spec Ready for Review until the three issues above are addressed. After those edits, the spec should be safe to execute: the dependency graph is sound, acceptance criteria are concrete, and the final integrity-review subtask is strong enough to catch functional-preservation regressions.
