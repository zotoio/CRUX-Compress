# Subtask: Extract `/crux-compress` per-source-type subagent prompts into a lazy template file

## Metadata
- **Subtask ID**: 03
- **Feature**: context-token-reduction
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: None
- **Created**: 20260713

## Objective

Implement the `/crux-compress` half of **Option 6** from `analysis/context-token-reduction-report.md` (redundancy **R5** — five near-identical "When invoked with…" per-source-type subagent prompts inline in `crux-compress.md`, ~1.5K tokens of avoidable boilerplate). The Canvas-template half of Option 6 is folded into Subtask 05 (which owns the memory-manager split).

Move the five inline prompt templates (markdown / image / URL / code / ALL) out of `.cursor/commands/crux-compress.md` into a new template file that the command lazy-loads only when the corresponding source-type branch fires. Keep `crux-compress.md` at its current path (dist-manifest expects it).

## Deliverables Checklist

- [x] **D01** — Create `.cursor/commands/templates/compress-prompts.md` containing exactly the five per-source-type subagent prompt bodies extracted verbatim from `.cursor/commands/crux-compress.md`, each under a clearly-labeled `## <source-type>` heading (`markdown`, `image`, `url`, `code`, `all`). Keep any shared preamble at the top under `## Shared Preamble`.
- [x] **D02** — In `.cursor/commands/crux-compress.md`, replace each inline "When invoked with…" block with a two-to-three-line dispatcher that:
  - identifies the source type from `$ARGUMENTS`,
  - directs the LLM to load the corresponding section from `.cursor/commands/templates/compress-prompts.md`, and
  - re-states only the *invariant* frontmatter/parameter binding rules for that dispatch (e.g. which `$ARGUMENTS` slot is the file path, which flags apply).
- [x] **D03** — Preserve the top-level Usage table, flag documentation, plugin registry section, and every section of `crux-compress.md` that is **not** a per-source-type dispatch body. Only the five prompt bodies move.
- [x] **D04** — Record before/after token counts for `crux-compress.md` in the subtask's status `notes` (target: ~1.5K tokens saved on the command file itself; template file adds ~1.5K tokens but is loaded only on the cold path).
- [x] **D05** — Flag the dist-manifest addition needed for `.cursor/commands/templates/compress-prompts.md`:
  - `crux-compress.md` is in `.crux/dist-manifest.json`. If the command references the new template file, consumers need that template too.
  - Add a `notes` entry with the exact `SOURCE_DIST_FILES` addition (`.cursor/commands/templates/compress-prompts.md`) required, for Subtask 09 to aggregate under **Dist manifest additions — awaiting user approval**.
  - Do **not** edit `scripts/create-crux-zip.py`.

## Definition of Done

- [x] **DoD01** — `.cursor/commands/crux-compress.md` decreased in size by ≥ 1.2K tokens vs `analysis/context-token-reduction-report.md` §1.2 baseline of ~8.3K tokens.
- [x] **DoD02** — `.cursor/commands/templates/compress-prompts.md` exists and contains five clearly-labeled per-source-type sections plus a shared preamble.
- [x] **DoD03** — For each of markdown / image / URL / code / ALL, a manual walkthrough of `crux-compress.md` reads coherently — a fresh reader can dispatch to the correct template section without ambiguity.
- [x] **DoD04** — No path change to `.cursor/commands/crux-compress.md`; Cursor still resolves `/crux-compress` unchanged.
- [x] **DoD05** — No linter errors introduced.
- [x] **DoD06** — Subtask 09 has the dist-manifest addition captured in this subtask's notes.

## Implementation Notes

- **File-write disjoint from Phase-1 siblings**: S01 does not touch commands; S02 touches rules; S04 touches skills; S06 touches `crux-test.md` (a different command). Only `crux-compress.md` and the new template file are written here.
- The new `.cursor/commands/templates/` directory is a new subtree — nothing currently exists there. Create it, and do not assume Cursor will auto-load anything from it. The command file explicitly directs the LLM to read the template file.
- The extracted template file is **not** a Cursor command file. It has no frontmatter and is not registered with the IDE. It is a plain markdown data file the command loads on demand.
- Consumer impact (KD-5 in the spec index): this subtask creates a new file that consumers need to receive if they run `/crux-compress`. Do not modify `scripts/create-crux-zip.py`; flag the required addition for user approval.
- Coordinate on token estimates via `.cursor/skills/crux-utils/scripts/crux-utils.py`.
- Preserve every existing plugin hook, `--plugin` flag reference, and the plugin registry section verbatim. Do **not** compress `crux-compress.md` itself in this subtask — CRUX compression is Subtask 07's responsibility and works better on the leaner, post-extraction source.

## Testing Strategy

**Do NOT trigger global test suites during parallel execution.** Instead:

- Diff `crux-compress.md` before/after — verify that every removed block has a corresponding pointer to the template.
- Read `.cursor/commands/templates/compress-prompts.md` end-to-end to confirm all five bodies are complete, correctly labeled, and identical in intent to the originals.
- If evals exist that grep `crux-compress.md` for phrases from the moved bodies, note them for Subtask 08 to retune.
- Full eval sweep deferred to Subtask 08.

## Execution Notes

### Agent Session Info
- Agent: crux-platform-architect
- Started: 2026-07-13
- Completed: 2026-07-13

### Work Log

1. Baselined `crux-compress.md` at 8392 tokens via `crux-utils --token-count`.
2. Created `.cursor/commands/templates/` directory (previously did not exist).
3. Wrote `.cursor/commands/templates/compress-prompts.md` with a `## Shared Preamble` plus five clearly-labeled sections (`## markdown`, `## image`, `## url`, `## code`, `## all`) containing the extracted dispatch bodies. Template file measures 3394 tokens and is a plain markdown data file (no frontmatter, not IDE-registered).
4. Rewrote the five inline `### When invoked with …` blocks in `.cursor/commands/crux-compress.md` into short pointer dispatchers that name the template section to load, the `$ARGUMENTS` slot(s), and the invariant flag set with defaults. Added an intro `### Source-Type Dispatch` paragraph above the dispatchers that points at the template's shared preamble.
5. Preserved every non-dispatch section verbatim: Usage table, Flags table, Compression Level table, Output Formats, Plugin Parameter System (registry, standard hooks, default loading, explicit mode, common validation, execution contract), Parallelism Limits, Source Checksum Tracking, Force Flag Pre-processing, Eligibility Criteria, Adding New Files, Source vs Output Convention, Output Path Rules, Example Batch Execution, Semantic Validation, Related.
6. Re-measured `crux-compress.md` at 6038 tokens — a 2354-token reduction (~28%), well above the DoD01 ≥ 1.2K target.
7. Confirmed no linter errors on both files via `ReadLints`.
8. Wrote token counts, dist-manifest addition (for S09), manual-walkthrough evidence (DoD03), and evals grep-audit into the status.yml `notes` field; synced status.md from status.yml.

### Blockers Encountered

None.

### Files Modified

- `.cursor/commands/crux-compress.md` (modified — 8392 → 6038 tokens, −2354)
- `.cursor/commands/templates/compress-prompts.md` (created — 3394 tokens, cold-path only)

### Dist-manifest addition for Subtask 09

For S09 to aggregate under **Dist manifest additions — awaiting user approval** (do NOT edit `scripts/create-crux-zip.py` inside this spec):

```
SOURCE_DIST_FILES additions (exact):
  .cursor/commands/templates/compress-prompts.md
```

Rationale: `.cursor/commands/crux-compress.md` is already in `.crux/dist-manifest.json` and now references the template file on every dispatch, so consumers who invoke `/crux-compress` need the template file too.

