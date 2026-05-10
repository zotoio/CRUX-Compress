# Dream Summary: SDK Eval Suite Expansion

**Spec**: `specs/20260426-sdk-eval-expansion/`
**Source slug**: `20260426-sdk-eval-expansion`
**Dream date**: 2026-04-27
**Mode**: interactive (user accepted all 5 candidates)

## Inputs Analysed

- `spec-sdk-eval-expansion-20260426.md` — index, 14 decisions, 9 subtasks
- `execution-report-sdk-eval-expansion-20260426.md` — 17m 35s duration, 9/9 verified
- `assessment-sdk-eval-expansion-20260426.md` — pre-execution judge findings (3.7/5.0 conditional)
- `subtask-01-sdk-eval-test-architecture-20260426.md` — design-only, 7 sections of architecture decisions
- `subtask-02-sdk-eval-harness-enhancements-20260426.md` — 10 new harness helpers
- `subtask-03-sdk-eval-vitest-parallelization-20260426.md` — config + npm scripts (already implemented)
- `subtask-04-sdk-eval-dream-tests-20260426.md` — `b-dream.test.ts`, 8 tests
- `subtask-05-sdk-eval-rem-tests-20260426.md` — `c-rem.test.ts`, 8 tests
- `subtask-06-sdk-eval-forget-tests-20260426.md` — `r-forget.test.ts`, 6 tests
- `subtask-07-sdk-eval-meditate-tests-20260426.md` — `q-meditate.test.ts`, 6 tests
- `subtask-08-sdk-eval-integration-test-20260426.md` — `n-integration.test.ts`, 5 tests
- `subtask-09-sdk-eval-validation-profiling-20260426.md` — structural validation, 57 tests confirmed

## Verification

- Execution status: **complete** — all 9 subtasks adversarially verified
- Diff scope: within threshold (focused on `evals/sdk/` and spec artifacts; uncommitted memory file changes are unrelated)
- Existing memory corpus: 31 memories scanned (5 core, 10 redflag, 14 learning, 2 idea, 0 goal)

## Candidates Extracted

10 candidates were generated from the artifacts. The top 5 (by type priority, recurrence, actionability, and novelty) were presented to the user.

## Memories Created

| ID | Slug | Type | File |
|----|------|------|------|
| `fcd2f69` | `sdk-single-turn-requires-non-interactive-directives` | learning | `memories/learning/sdk-single-turn-requires-non-interactive-directives.memory.md` |
| `e05030c` | `expensive-sdk-evals-gated-skip-by-default` | learning | `memories/learning/expensive-sdk-evals-gated-skip-by-default.memory.md` |
| `62c0212` | `cursor-february-sdk-type-defs-have-preexisting-errors` | redflag | `memories/redflag/cursor-february-sdk-type-defs-have-preexisting-errors.memory.md` |
| `6265f8f` | `sdk-rate-limit-retry-with-exponential-backoff-and-jitter` | learning | `memories/learning/sdk-rate-limit-retry-with-exponential-backoff-and-jitter.memory.md` |
| `6415c52` | `shared-agent-runs-per-describe-block-reduce-api-cost` | learning | `memories/learning/shared-agent-runs-per-describe-block-reduce-api-cost.memory.md` |

All memories created with `strength: 1`, `source: 20260426-sdk-eval-expansion`, base scope (no agent scoping — insights apply broadly to anyone working on SDK-based evals or Cursor SDK consumers).

## Candidates Rejected (above the 5-fact cap)

These were ranked but excluded from the top 5; preserved here for future REM consideration:

- `global-walltime-deadline-as-test-suite-safety-net` (learning) — partially captured by `expensive-sdk-evals-gated-skip-by-default`'s "defensive pair" section
- `git-worktree-isolation-for-parallel-vitest-forks` (learning) — adjacent to existing `tests-must-use-tmp-path-fixtures` redflag; could merge or stand alone in a future REM cycle
- `conservative-parallelism-then-empirical-scaling` (learning) — captured by retry candidate's "pair with conservative parallelism" clause
- `multi-turn-integration-test-shared-agent-validates-command-wiring` (learning) — single occurrence; lower recurrence
- `already-implemented-subtask-detection-prevents-rework` (learning) — single occurrence (subtask 03); generalises existing engineering judgement

## Conflicts Resolved

**None.** All 5 created candidates are novel relative to the existing memory corpus. The redflag (`cursor-february-sdk-type-defs-have-preexisting-errors`) is structurally similar to the existing `agents-crux-md-is-transient-install-artifact` redflag (both are "false-positive prevention" patterns for reviewers) but addresses a different artefact, so they coexist as siblings without contradiction.

## Resolved Bugs Forgotten

**None.** All 10 existing redflag memories were cross-checked against the spec's code diffs and subtask outcomes. Two were reinforced rather than resolved:

- `tests-must-use-tmp-path-fixtures` — reinforced by the SDK suite's git worktree isolation pattern (the JavaScript analogue of pytest's `tmp_path`)
- `agent-reported-file-creation-must-be-verified-on-disk` — reinforced by the new `assertMemoryExists` / `assertMemoryDeleted` / `assertTrackerDeleted` harness helpers

The remaining redflags (`dist-zip-can-silently-omit-feature-files`, `cursor-canvas-sdk-restricts-imports`, `spec-index-can-drift-from-subtask-details`, `agents-crux-md-is-transient-install-artifact`, `meditate-synthesis-must-not-hallucinate-connections`, `max-memory-size-adaptive-compression`, `tooling-defaults-must-align-with-spec`, `file-paths-in-docs-must-reference-actual-files`) are unrelated to SDK eval work.

## Index Rebuild

`.crux/memory-index.yml` rebuilt after creation; the new memories are sorted by type priority and now appear in the index alongside the existing 31 entries (corpus total: 36).

## Archival

Spec directory moved from `specs/20260426-sdk-eval-expansion/` to `.ai-ignored/specs/20260426-sdk-eval-expansion/` per user request.
