# Spec 20260713-context-token-reduction — aggregate live status

<!-- status:overview:start -->
| Key | Value |
|-----|-------|
| spec_id | 20260713-context-token-reduction |
| phase | 0 |
| aggregate_state | completed |
| started_at | — |
| updated_at | 2026-07-13T09:58:28.239Z |

**config_reloaded**
_None._
<!-- status:overview:end -->

<!-- status:progress:start -->
| Metric | Count |
|--------|-------|
| Total | 9 |
| Completed | 9 |
| In progress | 0 |
| Blocked | 0 |
| Failed | 0 |
<!-- status:progress:end -->

<!-- status:subtasks:start -->
| Subtask | State | Status (yml) | Last heartbeat |
|---------|-------|--------------|----------------|
| 01 | completed | `specs/20260713-context-token-reduction/status/subtask-01-lazy-cruxmd-and-context-manifest-20260713.status.yml` | 2026-07-13T07:25:00.000Z |
| 02 | completed | `specs/20260713-context-token-reduction/status/subtask-02-compress-always-on-rules-20260713.status.yml` | 2026-07-13T07:38:46Z |
| 03 | completed | `specs/20260713-context-token-reduction/status/subtask-03-extract-crux-compress-templates-20260713.status.yml` | 2026-07-13 07:17:42.597000+00:00 |
| 04 | completed | `specs/20260713-context-token-reduction/status/subtask-04-dedupe-memory-skill-shared-surface-20260713.status.yml` | 2026-07-13T07:36:52Z |
| 05 | completed | `specs/20260713-context-token-reduction/status/subtask-05-split-memory-manager-and-canvas-template-20260713.status.yml` | 2026-07-13T08:06:25.860Z |
| 06 | completed | `specs/20260713-context-token-reduction/status/subtask-06-crux-test-pytest-shim-20260713.status.yml` | 2026-07-13T09:17:00Z |
| 07 | completed | `specs/20260713-context-token-reduction/status/subtask-07-crux-compress-large-primitives-20260713.status.yml` | 2026-07-13T19:16:08+10:00 |
| 08 | completed | `specs/20260713-context-token-reduction/status/subtask-08-evals-and-ci-coverage-20260713.status.yml` | 2026-07-13T19:38:40+10:00 |
| 09 | completed | `specs/20260713-context-token-reduction/status/subtask-09-docs-sync-and-upgrade-file-20260713.status.yml` | 2026-07-13T09:56:30Z |
<!-- status:subtasks:end -->

<!-- status:blockers:start -->
_None._
<!-- status:blockers:end -->

<!-- status:definition-of-done:start -->
- [x] **DOD01** — All nine subtasks marked completed with judge verdict `verified`
- [x] **DOD02** — `pnpm --filter zoto-spec-system-runtime run spec-onstop-check -- --human --repo-root .` (or `tsx plugins/zoto-spec-system/scripts/spec-onstop-check.ts --human --repo-root .` if invoked directly) returns exit `0`
- [x] **DOD03** — Full `python3 scripts/test.py` suite passes (BATS + pytest); evals under `evals/` pass
- [x] **DOD04** — `python3 -m evals.<crux_command_suite>` (from Subtask 06) passes and matches previous `/crux-test` semantic coverage
- [x] **DOD05** — No linter errors in files modified by any subtask
- [x] **DOD06** — `specs/20260713-context-token-reduction/upgrade-context-token-reduction.sh` is idempotent, `--yes`-gated, and passes `bash -n` (syntax) plus one dry-run against a scratch copy
- [x] **DOD07** — Any file the subtasks propose adding to the dist zip is listed in the execution report under a **Dist manifest additions — awaiting user approval** section, with the exact `SOURCE_DIST_FILES` diff. `scripts/create-crux-zip.py` is **not** modified as part of the spec.
- [x] **DOD08** — `AGENTS.md` `<CRUX agents="always">` block edits remain consumer-safe (no repo-internal-only agents leak into the block; no reference to non-dist files)
- [x] **DOD09** — Docs synchronized per `docs-sync.crux.mdc` (README, CONTRIBUTORS, `web/compress.md/` where relevant)
- [x] **DOD10** — Baseline vs post-spec token-cost measurement recorded in the execution report for at least three canonical workflows: (a) trivial Q&A, (b) `/crux-dream <spec>`, (c) a 10-subtask `/z-spec-execute` dry-run
- [x] **DOD11** — Version bump per `version-bump.crux.mdc` noted in the commit message body (minor bump — `feat`); actual `.crux/crux.json` bump left to the release commit at merge time, not performed inside the spec
<!-- status:definition-of-done:end -->

<!-- status:events:start -->
- **2026-07-13T09:57:51.737Z** `rebuild` — Aggregated 9 subtask source(s); digest 929cf202…
- **2026-07-13T09:58:14.550Z** `rebuild` — Aggregated 9 subtask source(s); digest 16841cae…
- **2026-07-13T09:58:28.239Z** `rebuild` — Aggregated 9 subtask source(s); digest 74e21bee…
<!-- status:events:end -->
