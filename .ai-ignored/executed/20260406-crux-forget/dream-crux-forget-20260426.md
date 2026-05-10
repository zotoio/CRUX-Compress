# Dream Summary: `20260406-crux-forget`

**Dreamt**: 2026-04-26
**Spec**: `spec-crux-forget-20260406.md`
**Spec status**: Completed (2026-04-06 22:59:05 → 23:09:37 UTC, 10m 32s)
**Dream agent**: `crux-cursor-memory-manager`

---

## Pre-extraction Verification

| Check | Result |
|-------|--------|
| Execution status | Completed (6/6 subtasks adversarially verified) |
| `_execution-state.yml` | Not present — proceeded based on execution report and judge assessments |
| Test suite | 247 passed, 0 failed |
| Linter | Clean across all 10 modified files |
| Repo changes since spec start | Within `maxUnrelatedChanges` threshold (50). Bundled commit `36e1317` included some unrelated improvements (recall hook, website pages, dist-manifest) but spec-scope changes were clearly attributable |

## Artifacts Analysed

- `spec-crux-forget-20260406.md`
- `execution-report-crux-forget-20260406.md`
- `subtask-01` through `subtask-06` (6 files)
- `assessment-crux-forget-20260407.md` (second/authoritative judge)
- `zoto-judge-assessment-crux-forget-20260406.md` (first judge, superseded)
- Code commit `36e1317` for diff context

## Existing Memories Compared

13 existing memories loaded (12 in index + 1 consolidated). Closest neighbours considered:

| Existing memory | Relationship | Action |
|-----------------|--------------|--------|
| `f8bdc0d` agent-definitions-reference-skills (core) | Same theme as "thin orchestration commands" candidate | Excluded — near-duplicate; existing memory already covers the principle for agents and generalises naturally |
| `96a7410` tooling-defaults-must-align-with-spec (redflag) | Related to install.crux.md drift theme | Kept as related; new candidates target distinct surfaces |
| `6c16dc6` adversarial-verification-catches-documentation-gaps (learning, strength 2) | Reinforced by 2-pass judge correction | Strength bump deferred to next REM sleep |

## Conflicts Detected

None. No candidate contradicted an existing memory.

## Resolved Bug Detection

None of the existing redflag memories were resolved by this spec:

- `tooling-defaults-must-align-with-spec` — pre-existing `install.crux.md` drift was *noted* but not fixed
- `file-paths-in-docs-must-reference-actual-files` — unrelated
- `tests-must-use-tmp-path-fixtures` — unrelated
- `max-memory-size-adaptive-compression` — unrelated

## Candidates Presented (5)

| Rank | Type | ID | Title |
|------|------|----|-------|
| 1 | core | `c71c143` | Destructive memory operations require explicit user confirmation |
| 2 | core | `7144866` | install.py: feature commands belong in RELEASE_FILES, not standard_files |
| 3 | redflag | `826c280` | AGENTS.crux.md is a transient install-time artifact, not a maintained CRUX file |
| 4 | redflag | `d944d7c` | Spec index text can drift from subtask details; reviewers must verify both |
| 5 | learning | `bdcc9ad` | Adding a sibling command requires updating existing siblings' Related sections |

## Candidates Rejected as Duplicates

| Candidate considered | Reason rejected |
|----------------------|-----------------|
| "New commands should be thin orchestration layers" | Near-duplicate of `f8bdc0d` agent-definitions-reference-skills — same principle, different surface |
| "Phased parallel subtask execution" | Already covered by `efc4c24` parallel-subagent-execution-per-phase; no new evidence |
| "install.crux.md `M.standard_files(backup)` pre-existing drift" | Pre-existing, not introduced by this spec; folded into Rank 2's evidence rather than a standalone memory |

## User Decision

User accepted **all 5 candidates** and approved spec archival.

## Memories Created (5)

All 5 candidates were created in base scope (no agent scoping warranted — these are general memory-system / installer / spec-process insights).

| Type | File | ID |
|------|------|----|
| core | `memories/core/destructive-memory-ops-require-confirmation.memory.md` | `c71c143` |
| core | `memories/core/install-py-release-files-vs-standard-files.memory.md` | `7144866` |
| redflag | `memories/redflag/agents-crux-md-is-transient-install-artifact.memory.md` | `826c280` |
| redflag | `memories/redflag/spec-index-can-drift-from-subtask-details.memory.md` | `d944d7c` |
| learning | `memories/learning/update-sibling-related-sections-on-command-family-expansion.memory.md` | `bdcc9ad` |

All memories created with `strength: 1`, `created: 2026-04-26`, `modified: 2026-04-26`, and `source: "20260406-crux-forget"`.

## Resolved Bugs Forgotten

None.

## Post-extraction Actions

- [x] 5 memory files written via `crux-skill-memory-crud` Create operation
- [x] Memory index rebuilt via `crux-skill-memory-index`
- [x] Dream summary written to this file
- [x] Spec directory archived to `.ai-ignored/executed/20260406-crux-forget/`

## Notes for Next REM Sleep

- Consider strength bump for `6c16dc6` adversarial-verification-catches-documentation-gaps — the two-pass judge correction (1st judge produced false-positive CRITICAL, 2nd judge corrected) is another data point reinforcing this learning
- Consider compression of all 5 newly created memories — they are uncompressed (`enableMemoryCompression: "true"` is set in config)
- Consider consolidation candidates: the two new `core` memories on installer/safety, and the two new `redflag` memories on review/spec-drift, may or may not warrant grouping — leave to REM sleep heuristics
