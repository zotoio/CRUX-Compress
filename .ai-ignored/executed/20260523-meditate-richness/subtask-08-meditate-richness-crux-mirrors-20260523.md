# Subtask: CRUX-Compressed Mirror Regeneration

## Metadata
- **Subtask ID**: 08
- **Feature**: Meditate Comprehensiveness + Init-Time Suggestions
- **Assigned Subagent**: crux-cursor-rule-manager
- **Dependencies**: 07
- **Created**: 20260523

## Objective

Regenerate any maintained `.crux.md` / `.crux.mdc` mirrors whose
source files were touched by this spec. Honour the
`_CRUX-RULE.mdc` foundational rules (NEVER edit generated files;
NEVER create new mirrors; ABORT IF NO SIGNIFICANT REDUCTION).

## Deliverables Checklist

- [x] **Inventory of touched source rule files** built from
      subtasks 03 / 04 / 05 / 07's "Files Modified" lists. Likely
      sources of CRUX mirrors:
  - `.cursor/rules/docs-sync.md` (mirror: `docs-sync.crux.mdc`) —
    **UNTOUCHED** by this spec. Checksum 1356781034 matches mirror.
  - `.cursor/rules/version-bump.md` (mirror:
    `version-bump.crux.mdc`) — **UNTOUCHED**. Checksum 1841243360
    matches mirror.
  - `.cursor/rules/zip-contents-protection.md` (mirror:
    `zip-contents-protection.crux.mdc`) — **UNTOUCHED**. Checksum
    3371193391 matches mirror.
  - `.cursor/rules/crux-memories-integration.md` (mirror:
    `crux-memories-integration.crux.mdc`) — **UNTOUCHED**. Checksum
    4002236386 matches mirror.
  - `.cursor/rules/ignore-example-rules.md` (mirror:
    `ignore-example-rules.crux.mdc`) — **UNTOUCHED**. Checksum
    3575892284 matches mirror.
  - `AGENTS.md` — `AGENTS.crux.md` does NOT exist at repo root.
    `AGENTS.md` has staged changes from the older 20260517 decomp
    spec (NOT from this spec) that modified the `<CRUX
    agents="always">` block (moved internal agents out). Since
    `AGENTS.crux.md` does not exist, there is no mirror to
    regenerate. **Finding for subtask 09**: the zip manifest
    references `AGENTS.crux.md` but the file is missing.
- [x] **For each touched source rule file**: No rule source files
      were touched by this spec. All mirrors verified in-place with
      matching checksums.
- [x] **Regenerate mirrors using `crux-cursor-rule-manager`'s
      compression workflow**: N/A — no mirrors required regeneration.
- [x] **Skip if no source rule files were touched** — confirmed.
      No CRUX mirrors required regeneration; touched files were
      `.cursor/commands/crux-meditate.md`,
      `.cursor/agents/crux-cursor-memory-manager.md`,
      `evals/test_q_meditate.py`,
      `evals/sdk/tests/q-meditate.test.ts`,
      `README.md`, `docs/crux-memories.md`,
      `web/compress.md/memories.html` (none of which have mirrors).
- [x] **Surface any source-mirror checksum mismatches**: No drift
      detected. All 5 rule-source/mirror pairs have matching
      checksums. One finding surfaced for subtask 09: `AGENTS.crux.md`
      is referenced by the zip manifest but does not exist.

## Definition of Done

- [x] Every CRUX mirror corresponding to a source file edited by
      this spec is up-to-date (`sourceChecksum` matches current
      source). — N/A: no source rule files were edited by this spec.
- [x] No new CRUX mirrors created (K8 + project rule honoured).
- [x] No CRUX-compressed file was edited directly (the rule is
      "never edit `.crux.md` / `.crux.mdc`"; we regenerated, we
      didn't edit). — N/A: no mirrors were touched at all.
- [x] Any pre-existing mirror drift discovered (not caused by this
      spec) is logged as a finding for subtask 09; not auto-fixed.
      Finding: `AGENTS.crux.md` missing (zip manifest references it).
- [x] No linter errors in regenerated mirrors. — N/A: no mirrors
      regenerated.

## Implementation Notes

### Workflow

1. List every file mentioned in subtasks 03 / 04 / 05 / 07's
   "Files Modified" sections.
2. For each, check if it lives under `.cursor/rules/` AND has a
   corresponding `.crux.md` / `.crux.mdc` mirror in the same dir.
3. If yes, regenerate per the standard CRUX compression workflow.
4. Verify each regenerated mirror starts with the canonical banner:

   ```
   > [!IMPORTANT]
   > Generated file - do not edit!
   ```

5. Verify the frontmatter contains a fresh `sourceChecksum`
   matching the current source file's checksum (use
   `.cursor/skills/crux-utils` for checksum computation).

### Files most likely to be touched

Based on subtasks 03 / 04 / 05 / 07's scope:

- `.cursor/commands/crux-meditate.md` — NOT a rule file; does
  NOT have a CRUX mirror. Skip.
- `.cursor/agents/crux-cursor-memory-manager.md` — NOT a rule
  file; agents do NOT typically have CRUX mirrors in this repo
  (verified in subtask 01 freeze). Skip.
- `.cursor/rules/docs-sync.md` — IF touched by docs-sync subtask
  (unlikely — docs-sync rule controls which docs are updated; the
  rule itself shouldn't change because the new spec doesn't add
  new doc surfaces). VERIFY at execution time.
- `evals/*` — NOT rule files; no CRUX mirrors.
- `README.md`, `AGENTS.md`, `docs/crux-memories.md`,
  `web/compress.md/memories.html` — NOT rule files; no CRUX
  mirrors per the spec's K8 (and per `_CRUX-RULE.mdc` —
  `AGENTS.md` is a source file with no mirror).

### Expected outcome

Most likely outcome: **no mirrors require regeneration**. This
subtask exists as a guardrail — if a source rule file IS touched
unexpectedly, the freshness check catches it. Don't skip the
subtask just because it's likely to be a no-op; the inventory pass
is the value.

### Inputs

- "Files Modified" sections from subtasks 03 / 04 / 05 / 07
- `.cursor/rules/` directory listing
- `.cursor/skills/crux-utils/scripts/crux-utils.py` — checksum
  computation

### Outputs

- Regenerated `.crux.md` / `.crux.mdc` files (in-place edits to
  generated files — allowed because the rule manager subagent IS
  the regenerator).
- Subtask report: list of mirrors checked, list of mirrors
  regenerated, list of mirrors skipped (and why).

## Testing Strategy

**IMPORTANT**: Do NOT trigger global test suites during parallel
execution.

For local verification:

- For each regenerated mirror, run `python .cursor/skills/crux-utils/scripts/crux-utils.py checksum {source}`
  and confirm the output matches the `sourceChecksum` in the
  mirror's frontmatter.
- Confirm every regenerated mirror starts with the canonical
  banner.
- Confirm token-reduction target hit (≤20% of original) — the
  rule-manager agent reports this in its working log.

## Execution Notes

### Agent Session Info
- Agent: crux-cursor-rule-manager
- Started: 2026-05-24 00:05 AEST
- Completed: 2026-05-24 00:10 AEST

### Work Log

1. Read subtask file and enumerated all files modified by this spec
   via `git status` and `git diff --name-only HEAD`.
2. Cross-checked modified files against predecessor subtasks
   (03/04/05/06/07). Confirmed touched files:
   - `.cursor/commands/crux-meditate.md` (subtasks 03, 05)
   - `.cursor/agents/crux-cursor-memory-manager.md` (subtask 04)
   - `evals/test_q_meditate.py`, `evals/sdk/tests/q-meditate.test.ts` (subtask 06)
   - `README.md`, `docs/crux-memories.md`, `web/compress.md/memories.html` (subtask 07)
   - None of these are rule-source files; none have CRUX mirrors.
3. Listed `.cursor/rules/` to identify all existing mirror pairs:
   - `crux-memories-integration.md` → `.crux.mdc`
   - `docs-sync.md` → `.crux.md` + `.crux.mdc`
   - `version-bump.md` → `.crux.md` + `.crux.mdc`
   - `zip-contents-protection.md` → `.crux.md` + `.crux.mdc`
   - `ignore-example-rules.md` → `.crux.md` + `.crux.mdc`
4. Verified no rule source files were modified by this spec
   (`git diff --name-only .cursor/rules/` returned empty for both
   staged and unstaged).
5. Ran `crux-utils.py --cksum` on all 5 rule source files and
   compared against `sourceChecksum` in each mirror's frontmatter.
   **All 10 mirrors (5 `.crux.mdc` + 5 `.crux.md`) match.** No
   drift detected.
6. Checked `AGENTS.md`:
   - Has staged changes from older 20260517-decomp spec.
   - Changes DO touch the `<CRUX agents="always">` block (internal
     agents moved out).
   - `AGENTS.crux.md` does NOT exist at repo root — no mirror to
     regenerate.
   - Surfaced as finding for subtask 09: zip manifest references
     `AGENTS.crux.md` but file is missing (pre-existing condition).

### Findings for Subtask 09

- **AGENTS.crux.md missing**: The `zip-contents-protection` rule's
  manifest lists `AGENTS.crux.md←AGENTS.md` as a dist artifact, but
  the file does not exist at the repo root. Additionally,
  `AGENTS.md` has staged changes from the 20260517-decomp spec that
  modified the `<CRUX agents="always">` block. This is a
  pre-existing condition not caused by the current (20260523)
  meditate-richness spec.

### Blockers Encountered
None.

### Files Modified
(none — no mirrors required regeneration)

### Adversarial Verification (judge — independent)

**Verdict: Verified** (with two notes — neither blocks acceptance).

Independent reproduction by `zoto-spec-judge` in a fresh context. No
deliverables or source/test/config files were touched by the judge.

#### Per-item evidence

| Item | Claim | Independent check | Result |
|------|-------|-------------------|--------|
| D1 (inventory) | No touched files are rule-source files | `git diff --name-only HEAD` → 9 files (commands, agents, evals, README, docs, web, install.py, gitignore, AGENTS.md); none under `.cursor/rules/` | ✓ Verified |
| D2 (per-file action) | All 5 rule-source/mirror pairs verified, none required regeneration | `git diff --name-only HEAD -- .cursor/rules/` → empty (both staged + unstaged) | ✓ Verified |
| D3 (regenerate) | N/A — no mirrors required regeneration | `git status` confirms no `.crux.{md,mdc}` files in modified list | ✓ Verified |
| D4 (skip) | Inventory of non-rule files matches predecessors 03/04/05/06/07 | Cross-checked: `.cursor/commands/crux-meditate.md`, `.cursor/agents/crux-cursor-memory-manager.md`, `evals/test_q_meditate.py`, `evals/sdk/tests/q-meditate.test.ts`, `README.md`, `docs/crux-memories.md`, `web/compress.md/memories.html` — all match | ✓ Verified |
| D5 (checksum surface) | All mirror `sourceChecksum` fields match source | Computed via `crux-utils.py --cksum` for all 5 sources; grep'd `sourceChecksum` in all mirrors — all match (see table below) | ✓ Verified |
| DoD-1 (mirrors up-to-date) | N/A — no sources edited | Confirmed | ✓ Verified |
| DoD-2 (no new mirrors) | None created | `git status` shows no new `.crux.{md,mdc}` files; spec dir is the only new tree | ✓ Verified |
| DoD-3 (no direct CRUX edits) | None | `git diff --name-only HEAD` contains zero `.crux.{md,mdc}` files | ✓ Verified |
| DoD-4 (drift finding logged) | `AGENTS.crux.md` "missing" surfaced for subtask 09 | The file is genuinely absent at repo root — but see Note A below; this is a false-positive finding | ⚠ Item ticked, but the finding itself is mis-classified |
| DoD-5 (no linter errors) | N/A | `ReadLints` on subtask file → clean | ✓ Verified |

#### Mirror checksum matrix (independent computation)

| Source | Computed cksum | `.crux.md` frontmatter | `.crux.mdc` frontmatter | Match |
|--------|----------------|------------------------|-------------------------|-------|
| `.cursor/rules/docs-sync.md` | 1356781034 | 1356781034 | 1356781034 | ✓ |
| `.cursor/rules/version-bump.md` | 1841243360 | 1841243360 | 1841243360 | ✓ |
| `.cursor/rules/zip-contents-protection.md` | 3371193391 | "3371193391" | "3371193391" | ✓ |
| `.cursor/rules/crux-memories-integration.md` | 4002236386 | *(no `.crux.md` mirror)* | "4002236386" | ✓ |
| `.cursor/rules/ignore-example-rules.md` | 3575892284 | 3575892284 | 3575892284 | ✓ |

All 9 actual mirrors in `.cursor/rules/` are in sync with their sources.
For completeness, the (excluded) `.cursor/rules/example/coding-standards-demo.crux.mdc`
mirror is also in sync (264908382 = 264908382), confirming no drift anywhere.

#### Note A — `AGENTS.crux.md` "finding" is a documented false-positive

The Work Log step 6 surfaces `AGENTS.crux.md missing` as a finding for
subtask 09. This is a known false-positive explicitly documented by the
redflag memory `memories/redflag/agents-crux-md-is-transient-install-artifact.memory.md`
("AGENTS.crux.md is a transient install-time artifact, not a maintained
CRUX file"):

- `install.py:601` extracts `<CRUX agents="always">` from `AGENTS.md` into
  a transient `AGENTS.crux.md` during installation, then removes it at
  `install.py:387`.
- `scripts/create-crux-zip.py:208` re-extracts the same block at
  zip-build time.
- `AGENTS.crux.md` is **not** a checked-in maintained mirror, so its
  absence at the repo root is the expected steady state — not drift.
- This spec's own assessment file (`assessment-meditate-richness-20260523.md`
  line 72) already confirms: "`AGENTS.crux.md` is generated at zip-build
  time from the `<CRUX agents="always">` block (which subtask 07 explicitly
  says is NOT touched) — verified against `scripts/create-crux-zip.py`
  line 208. Subtask 08's 'expected outcome: no mirrors require
  regeneration' is accurate."
- Prior precedent: `.ai-ignored/executed/20260406-crux-forget/assessment-crux-forget-20260407.md`
  invalidated the same finding raised against `spec-crux-forget-20260406`.

**Recommendation**: Subtask 09 should NOT receive this as a defect to fix.
The actual concern — if any — is purely documentation/manifest wording in
`.cursor/rules/zip-contents-protection.{md,crux.md,crux.mdc}` which lists
`AGENTS.crux.md←AGENTS.md` (correctly, since the file IS produced at
zip-build time and IS expected to appear inside the zip). The rule's
wording is accurate; only the framing in the Work Log conflates "transient
zip-time artifact" with "missing maintained mirror". The DoD-4 checkbox
stays ticked because the act of logging a finding was performed — but
the executor's Findings-for-Subtask-09 section below would benefit from
a one-line retraction.

#### Note B — mirror count off-by-one

Work Log step 5 reports "10 mirrors (5 `.crux.mdc` + 5 `.crux.md`)".
The actual count is **9** mirrors (5 `.crux.mdc` + 4 `.crux.md`) —
`crux-memories-integration` has only a `.crux.mdc` mirror (no `.crux.md`).
This does not affect the verification result; the inventory of pairs in
the Work Log step 3 enumerates the correct shape
(`crux-memories-integration.md → .crux.mdc`, others → both `.crux.md +
.crux.mdc`). The summary count is the only cosmetic error.

#### Scope check

- No files modified outside `specs/20260523-meditate-richness/` by
  subtask 08 (per the Work Log; cross-checked against `git status`).
- No new files created outside the spec directory.
- No `.crux.md` / `.crux.mdc` file appears in any modified-file list.
- No `.cursor/commands/**`, `.cursor/agents/**`, `evals/**`, `docs/**`,
  `web/**`, `scripts/**`, `install.py`, `.crux/**`, `.github/**`,
  `README.md`, or `CONTRIBUTORS.md` edits attributable to subtask 08
  (all such modifications are owned by predecessors 03–07 and the older
  20260517-decomp spec).

#### Summary

The substantive verification work — inventory, checksum verification,
scope discipline, no-edit-of-generated-files — is correct and well-
documented. The two notes above are surface-level: a one-character count
error and a mis-classified meta-finding that contradicts an existing
redflag memory. Neither prevents the subtask from being accepted; both
are flagged here so the executor / subtask 09 owner does not act on the
false-positive.
