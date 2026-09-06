# Subtask 03 — context-token-reduction — live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 03 |
| feature | context-token-reduction |
| assigned_agent | crux-platform-architect |
| model | composer-2-fast |
| token_budget | 200000 |
| state | completed |
| started_at | 2026-07-13 07:12:06.742000+00:00 |
| last_heartbeat | 2026-07-13 07:17:42.597000+00:00 |
| completed_at | 2026-07-13 07:17:42.597000+00:00 |
| git_sha |  |
| agent_session_id |  |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
- [x] **D01** — **D01** — Create `.cursor/commands/templates/compress-prompts.md` containing exactly the five per-source-type subagent prompt bodies extracted verbatim from `.cursor/commands/crux-compress.md`, each under a clearly-labeled `## <source-type>` heading (`markdown`, `image`, `url`, `code`, `all`). Keep any shared preamble at the top under `## Shared Preamble`.
- [x] **D02** — **D02** — In `.cursor/commands/crux-compress.md`, replace each inline "When invoked with…" block with a two-to-three-line dispatcher that:
- [x] **D03** — **D03** — Preserve the top-level Usage table, flag documentation, plugin registry section, and every section of `crux-compress.md` that is **not** a per-source-type dispatch body. Only the five prompt bodies move.
- [x] **D04** — **D04** — Record before/after token counts for `crux-compress.md` in the subtask's status `notes` (target: ~1.5K tokens saved on the command file itself; template file adds ~1.5K tokens but is loaded only on the cold path).
- [x] **D05** — **D05** — Flag the dist-manifest addition needed for `.cursor/commands/templates/compress-prompts.md`:
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
- **created** `.cursor/commands/templates/compress-prompts.md` — Extracted five per-source-type dispatch bodies + shared preamble
- **modified** `.cursor/commands/crux-compress.md` — Replaced five inline dispatch bodies with 1-2 line pointer dispatchers to templates/compress-prompts.md
<!-- status:artifacts:end -->

<!-- status:errors:start -->
_None._
<!-- status:errors:end -->

<!-- status:notes:start -->
## Token counts (crux-utils --token-count)

| File | Before | After | Delta |
|------|-------:|------:|------:|
| `.cursor/commands/crux-compress.md` | 8392 | 6038 | **−2354** |
| `.cursor/commands/templates/compress-prompts.md` (new, cold-path only) | — | 3394 | +3394 |

Baseline reference: `analysis/context-token-reduction-report.md` §1.2 (~8.3K tokens).
DoD01 target ≥ 1.2K token reduction on `crux-compress.md` — **met** with 2354 tokens saved (~28% of the command file).
Template file is loaded only when a dispatch actually fires (cold path); the hot path (help / usage / eligibility / examples / plugin resolution) no longer carries the per-source-type prompt bodies.

## Dist manifest addition — awaiting user approval (for Subtask 09)

`.cursor/commands/crux-compress.md` is already in `.crux/dist-manifest.json`. It now references `.cursor/commands/templates/compress-prompts.md` on every dispatch, so consumers who invoke `/crux-compress` need the template file too. Subtask 09 should aggregate this under **Dist manifest additions — awaiting user approval** with the following exact addition to `scripts/create-crux-zip.py`:

```
SOURCE_DIST_FILES additions (exact):
  .cursor/commands/templates/compress-prompts.md
```

Do **not** edit `scripts/create-crux-zip.py` inside this subtask (KD-5 + `zip-contents-protection.crux.mdc`). User approval is required at review time before that addition lands.

## Manual walkthrough (DoD03)

Each of the five dispatchers in `crux-compress.md` explicitly:
- identifies the source type from `$ARGUMENTS` (image extension / URL prefix / code extension / `@`-prefixed markdown / literal `ALL`),
- names the exact template section to load (`## image` / `## url` / `## code` / `## markdown` / `## all` in `.cursor/commands/templates/compress-prompts.md`),
- re-states the invariant flag set with defaults (`--force`, `--minified` where applicable, `--<n>` level, plugin flags), and
- calls out the dispatch-unique invariants (adapter file, output dir, checksum vs `sourceUrl`, ALL scan scope).

A fresh reader can dispatch to the correct template section without ambiguity, and the `### Source-Type Dispatch` preamble above the five dispatchers points at the template's `## Shared Preamble` for the cross-dispatch invariants (compression level resolution, plugin resolution, `--force` pre-processing, parallelism cap of 4, validation/checksum rules) that are already documented in the sections above the dispatchers.

## Evals grep-audit (for Subtask 08)

No evals under `evals/` grep `crux-compress.md` for phrases from the moved bodies. Subtask 08 should still add a lazy-load check (Requirement 9c) verifying that `templates/compress-prompts.md` is only read when the corresponding dispatch actually fires, but no existing eval needs retuning against the extracted bodies.

<!-- status:notes:end -->
