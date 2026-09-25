# Subtask: Compress always-on rules + reconcile `_CRUX-RULE.mdc` ↔ AGENTS.md overlap

## Metadata
- **Subtask ID**: 02
- **Feature**: context-token-reduction
- **Assigned Subagent**: crux-cursor-rule-manager
- **Dependencies**: None
- **Created**: 20260713

## Objective

Implement **Option 7** from `analysis/context-token-reduction-report.md`: compress `spec-agent-allocation.md`, slim `_CRUX-RULE.mdc` to a one-paragraph pointer (removing the eight-rule duplication with the `<CRUX>` block in `AGENTS.md`), and consolidate the overlap between `crux-memories-integration.crux.mdc` and `crux-memories-mcp-context.mdc`. Every byte saved here compounds — always-on rules are loaded on **every** session turn.

Target: **≥ 500 tokens shaved off the always-on baseline** (report projects ~700; measure and record actual).

## Deliverables Checklist

- [x] **D01** — CRUX-compress `.cursor/rules/spec-agent-allocation.md` following `CRUX.md`:
  - Produce `.cursor/rules/spec-agent-allocation.crux.md` (canonical CRUX source) and `.cursor/rules/spec-agent-allocation.crux.mdc` (Cursor `alwaysApply` variant).
  - Preserve frontmatter `alwaysApply: true` and the human `description`.
  - Delete `.cursor/rules/spec-agent-allocation.md` **only if** the CRUX version achieves ≤ 25% of source tokens AND semantic equivalence check passes; otherwise leave the source in place and drop `alwaysApply` to `false` on the source while the `.mdc` variant carries the always-on flag (mirroring existing pattern for other rules).
- [x] **D02** — Slim `.cursor/rules/_CRUX-RULE.mdc` to remove content already present in `AGENTS.md` `<CRUX>` block:
  - Retain: filename banner, one-paragraph pointer to `AGENTS.md` `<CRUX>` block, **`CRUX Decompression — CRITICAL`** (load-bearing for KD-11 / approach (c) compressed agent bodies), `CRUX Compressed File Protection` rule, `Path Construction` rule.
  - Remove: the eight-rule duplication and the `Foundational CRUX Rules (MUST FOLLOW)` header if now redundant — but **never** delete the decompression primer, path-construction, or compressed-file-protection rules.
  - Adjust the "load `CRUX.md` and `AGENTS.md`" opening line to the lazy wording aligned with Subtask 01 — this is a **coordination point**, verify against Subtask 01's final AGENTS.md phrasing so wording matches. If Subtask 01 has not yet landed, use the wording specified in S01/D01 (preamble + rule #1).
  - This file **is** in `.crux/dist-manifest.json` — consumers get this rule. Keep the rule concise but self-contained; do not reference repo-internal files.
- [x] **D03** — Reconcile `.cursor/rules/crux-memories-integration.md` (source) ↔ `.cursor/rules/crux-memories-mcp-context.mdc`:
  - `crux-memories-mcp-context.mdc` and `crux-memories-integration.md` both cover "when to search memories" and "how to use the MCP".
  - Consolidate: move the MCP-specific instructions into `crux-memories-integration.md`'s MCP section (already present) and reduce `crux-memories-mcp-context.mdc` to a one-paragraph pointer OR delete it if fully subsumed.
  - Regenerate `crux-memories-integration.crux.mdc` from the updated source using standard compression flow (`crux-cursor-rule-manager` compression, confidence ≥ 90%). Verify the regenerated `.crux.mdc` is still in `.crux/dist-manifest.json`.
- [x] **D04** — For each changed always-on rule, record before/after token counts in the subtask's status `notes` (use `.cursor/skills/crux-utils/scripts/crux-utils.py` for estimation).
- [x] **D05** — Update `.crux/dist-manifest.json` **only if** an always-on-rule file was **deleted** — the dist manifest edit is a **flag** to raise in the status notes, not applied here. Do **not** modify `scripts/create-crux-zip.py`.

## Definition of Done

- [x] **DoD01** — Cumulative always-on token count for `.cursor/rules/*.mdc` + `spec-agent-allocation.*` decreases by ≥ 500 tokens vs the values in `analysis/context-token-reduction-report.md` §1.1.
- [x] **DoD02** — CRUX output for every changed rule passes decompression by `crux-cursor-rule-manager` — the semantic-equivalence spot check must succeed.
- [x] **DoD03** — Frontmatter `alwaysApply: true` remains present on exactly the intended set of `.mdc` files after edits; no rule silently loses always-on status.
- [x] **DoD04** — `crux-memories-integration.crux.mdc` is still present in `.crux/dist-manifest.json` and still parses under the CRUX loader.
- [x] **DoD05** — If `spec-agent-allocation.md` is deleted, add a bullet to the subtask notes flagging the `.crux/dist-manifest.json` change and the `scripts/create-crux-zip.py` `SOURCE_DIST_FILES` addition needed (`.cursor/rules/spec-agent-allocation.crux.mdc`), for Subtask 09 to aggregate for user approval.
- [x] **DoD06** — `python3 scripts/create-crux-zip.py /tmp/crux-dryrun-s02` succeeds without WARNING/ERROR lines from the AGENTS.md extraction path.

## Implementation Notes

- **File-write disjoint from Phase-1 siblings**: S01 edits agent files + AGENTS.md; S03 edits `crux-compress.md`; S04 edits skill files; S06 edits `crux-test.md` + evals. Only rule-file touches are in this subtask. No merge conflict expected.
- **Coordination with S01**: Both S01 and this subtask talk about the wording of the "load `CRUX.md`" instruction inside always-on rules. S01 owns the master wording in AGENTS.md; S02 mirrors it in `_CRUX-RULE.mdc`. If S01 lands first, copy verbatim. If this subtask lands first, use the wording specified in S01/D01 and Subtask 01 will reconcile if it drifts.
- **KD-11 hard constraint**: after slimming, `_CRUX-RULE.mdc` must still enable agents to decompress in-body `⟦CRUX:…⟧` notation without re-reading the full `CRUX.md`. Spot-check by confirming the Decompression — CRITICAL sentence (or CRUX-equivalent) remains.
- Follow `CRUX.md` compression rules strictly — the always-on rules are already CRUX-friendly in shape.
- For `_CRUX-RULE.mdc`, keep the CRUX-compressed-file-protection rule intact — this is the only rule that instructs the LLM about `.crux.md` write protection.
- Zip protection: this subtask **may** propose a `.crux/dist-manifest.json` change if a rule file is renamed/deleted. Do **not** edit `scripts/create-crux-zip.py`. Flag the required `SOURCE_DIST_FILES` change in the notes for Subtask 09 to raise with the user.

## Testing Strategy

**Do NOT trigger global test suites during parallel execution.** Instead:

- After each CRUX compression, self-check by decompressing and comparing meaning against the source (`crux-cursor-rule-manager` protocol).
- `rg "alwaysApply: true" .cursor/rules/` — confirm each file that should be always-on still says so, and no file lost the flag silently.
- `python3 scripts/create-crux-zip.py /tmp/crux-dryrun-s02` — verify dist packaging works. Delete `/tmp/crux-dryrun-s02/*.zip` after.
- Full eval sweep deferred to Subtask 08.

## Execution Notes

_To be filled by executing agent._

### Agent Session Info
- Agent: crux-cursor-rule-manager
- Started: 2026-07-13T17:13Z
- Completed: 2026-07-13T17:26Z

### Work Log
- D01: Compressed `spec-agent-allocation.md` (366 tokens) to `.crux.mdc` (184 tokens, 50% ratio). Could not meet 25% target due to verbatim agent names dominating token count. Source kept with `alwaysApply: false`; compressed variant carries `alwaysApply: true`.
- D02: Slimmed `_CRUX-RULE.mdc` from 422 to 360 tokens. Removed "When you encounter CRUX notation" and "CRUX Compression - CRITICAL" sections (both in AGENTS.md `<CRUX>` block). Aligned opening line with S01 lazy-load wording.
- D03: Merged `crux-memories-mpc-context.mdc` (406 tokens) into `crux-memories-integration.md` source (Discovery section). Deleted `crux-memories-mpc-context.mdc`. Regenerated `crux-memories-integration.crux.mdc` (492→484 tokens). Net from two files: 898→484 = -414 tokens.
- D04: Token deltas recorded in status notes.
- D05: No dist-manifest or create-crux-zip.py changes needed. None of the deleted/renamed files were in dist.
- Net always-on savings: **658 tokens** (target was ≥500).

### Blockers Encountered
None.

### Files Modified
- `.cursor/rules/spec-agent-allocation.md` — set `alwaysApply: false`
- `.cursor/rules/spec-agent-allocation.crux.md` — NEW (canonical CRUX source)
- `.cursor/rules/spec-agent-allocation.crux.mdc` — NEW (always-on compressed variant)
- `.cursor/rules/_CRUX-RULE.mdc` — slimmed (removed duplicate content)
- `.cursor/rules/crux-memories-integration.md` — merged MPC search guidelines into Discovery section
- `.cursor/rules/crux-memories-integration.crux.mdc` — regenerated from updated source
- `.cursor/rules/crux-memories-mcp-context.mdc` — DELETED (content subsumed by integration rule)

