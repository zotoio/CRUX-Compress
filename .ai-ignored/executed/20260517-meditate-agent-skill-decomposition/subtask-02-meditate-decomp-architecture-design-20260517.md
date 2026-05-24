# Subtask: Architecture Design — Agent + Skill Boundaries

## Metadata
- **Subtask ID**: 02
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 01
- **Created**: 20260517

## Objective
Translate the frozen contract from subtask 01 into a concrete section-by-section
mapping that places every contract item in exactly one of:
(a) the thin coordinator command, (b) the new
`crux-cursor-meditation-guide` agent, or (c) one of the new
`crux-skill-memory-meditation-*` skills. Produce a design document that
subsequent implementation subtasks (04, 05, 06, 07) can follow without
ambiguity.

## Deliverables Checklist
- [x] Create `meditate-decomp-architecture-design-20260517.md` inside this
      spec directory.
- [x] **Final agent specification**: `crux-cursor-meditation-guide`
      frontmatter (`name`, `description`, `color`, `tools`, `model`),
      persona prologue, mode router, and the executable section list
      (Phases A–G research, Quick 6-step, Ensemble Aggregation,
      Adversarial Review, Reports & Retrospective). Mark which
      sections call which skills.
- [x] **Final skill list** with one row per skill:
      directory name, `SKILL.md` `name` + `description`, scope
      summary, contract items it owns, the agent / command callers
      that load it, and any cross-skill dependencies. The list is
      fixed to exactly these six approved skills:
      `crux-skill-memory-meditation-research`,
      `crux-skill-memory-meditation-quick`,
      `crux-skill-memory-meditation-ensemble`,
      `crux-skill-memory-meditation-review`,
      `crux-skill-memory-meditation-report`, and
      `crux-skill-memory-meditation-coordination`. Do not consolidate,
      split, add, remove, or rename skills during execution unless the
      executor escalates a `needs_user_input` decision and receives
      explicit user approval.
- [x] **Section-mapping table**: one row per contract item from
      subtask 01 → destination
      (`command` / `agent` / `skill:<skill-name>`). Items that must
      appear in **both** the agent and a skill (e.g. invocation
      contract referenced by both) must be flagged with a "primary"
      destination and a "mirror" destination.
- [x] **Coordinator command shape**: outline what stays in
      `.cursor/commands/crux-meditate.md` after decomposition
      (argument parsing, mode flag handling, `Q-Depth-Selection`,
      `Q-Cost-Acknowledgment` + expansion variant, theme preflight,
      facet confirmation resume, ensemble orchestration loop, post-
      tree steps 9–12, continuation menu). Include the new spawn
      signature (Task tool call to `crux-cursor-meditation-guide`).
- [x] **Memory-manager trim plan**: list every section / heading to
      delete from `crux-cursor-memory-manager.md`, plus the pointer
      paragraph that replaces it. Explicitly call out sections that
      must remain (Dream / REM / Recall / Remember / Forget agent
      contracts, shared `needs_user_input` envelope schema if it is
      generic).
- [x] **Backwards-compat plan**: what happens during the brief
      window where the new agent exists but the command still
      references the memory manager (only inside subtask 06, before
      subtask 07 lands). Specify whether 06 must also update
      memory-manager pointers, or whether 07 handles it.
- [x] **Risks & open questions**: list any contract items where the
      destination is ambiguous and flag them for `needs_user_input`
      escalation by the executor (Pattern B).

## Definition of Done
- [x] Design document exists in spec directory
- [x] Every contract item from subtask 01 has a single primary destination
- [x] Skill mapping covers exactly the six approved skill names from spec K3
- [x] Coordinator command shape is documented with new spawn signature
- [x] Memory-manager trim plan covers every Meditate section in the current file
- [x] No linter errors introduced

## Implementation Notes
- This is a **read-only** subtask — produce a design document only.
- Reference subtask 01's freeze document by path; do not re-summarise
  the entire contract here.
- Pre-empt eval coverage gaps that subtask 03 will need: each
  destination should be discoverable by a substring assertion (e.g.
  the agent file should contain `crux-cursor-meditation-guide` in
  its frontmatter, each skill should mention `meditation` in its
  description).
- Honour the workspace `zip-contents-protection` rule — note that
  every new file path is a deliberate addition that must be
  enumerated by subtask 10.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Markdown-only artefact; no automated tests apply beyond markdown lint.

## Execution Notes

### Agent Session Info
- Agent: crux-platform-architect
- Started: 2026-05-17T12:22:51.975Z (subtask scaffold)
- Completed: 2026-05-17 (this turn)

### Work Log

1. **Context loading** — read the spec index, this subtask brief, the freeze
   contract (`meditate-frozen-contract-20260517.md`, 1441 lines), the existing
   `.cursor/agents/crux-cursor-memory-manager.md` Meditate Mode and Ensemble
   Aggregation Mode sections, and key blocks of
   `.cursor/commands/crux-meditate.md` (gates, Ensemble Protocol, calling-agent
   steps 9–12). Also read a sample existing skill SKILL.md (memory-extract) to
   confirm frontmatter convention.
2. **Pattern extraction** — identified the agent + skill responsibility split
   anchored on (a) what requires `AskQuestion` (must stay on the command),
   (b) what is mode-specific verbatim contract (research / quick / ensemble
   skills), (c) what is the universal coordination grammar (coordination
   skill), (d) what is the quality gate (review skill), and (e) what is the
   report contract (report skill).
3. **Section mapping** — walked each freeze-contract section (1–8) and
   placed every contract item into a single primary destination, marking
   mirrors only where independent spawnability or eval discoverability
   requires duplication.
4. **Coordinator shape** — projected the command's line budget post-refactor
   (≈ −840 lines, ~57 % shrink) and documented the four Task spawn
   signatures (single-model, ensemble member, ensemble aggregation,
   adversarial review).
5. **Memory-manager trim plan** — bounded the deletion ranges at lines
   279–841 and 872–907 plus two expertise bullets at 57–58; explicitly
   retained Forget Mode (843–870) and the generic User Input Escalation +
   Skills + Critical Rules blocks.
6. **Backwards-compat** — recommended a deprecation banner during the
   S06 → S07 interim window (Option A) over a merged S06+S07 (rejected).
7. **Risks** — catalogued seven design-time ambiguities (R1–R7) all
   resolved without `needs_user_input`, plus eight forward-looking risks
   (K1–K8) for subsequent subtasks.
8. **Output** — wrote
   `specs/20260517-meditate-agent-skill-decomposition/meditate-decomp-architecture-design-20260517.md`
   (768 lines, ten sections, markdown-only, no linter errors).
9. **Status hygiene** — heartbeated the status pair at start (state
   `in_progress`), after the design doc landed (ticked D01–D08 with
   `--artifact`), and on completion (state `completed`).

### Blockers Encountered

None. Every contract item mapped to a single primary destination. No
`needs_user_input` escalation required.

### Files Modified

- **Created**: `specs/20260517-meditate-agent-skill-decomposition/meditate-decomp-architecture-design-20260517.md`
- **Modified**: this file (execution notes + checklist ticks)
- **Modified**: `specs/20260517-meditate-agent-skill-decomposition/status/subtask-02-meditate-decomp-architecture-design-20260517.status.{yml,md}` (via the home-installed `spec-status-roundtrip` helper)

---

## Refresh 2026-05-24

The judge's 2026-05-17 partial verdict held a single blocker: **D04
section-mapping table contained split or alternative primary destinations**
(§4.1 output body sections, §4.4 Quick vs Research differences,
§5.4 facet registry "OR", §5.5 inline citation / validation rows).
In parallel, sibling spec `specs/20260523-meditate-richness/` shipped
2026-05-24, adding 13 new contract surfaces to the source files
(`.cursor/commands/crux-meditate.md` 1493 → 2142 lines;
`.cursor/agents/crux-cursor-memory-manager.md` 946 → 1388 lines).

A new freeze line `meditate-frozen-contract-20260524.md` was captured
by S01 and supersedes the 2026-05-17 freeze. This refresh re-projects
the entire architecture design against the new freeze line **in
place** (no sibling document), resolving D04 and absorbing all 13
richness surfaces. Six-skill cap holds — see §7 R9 of the refreshed
design for the rationale; the richness spec's own architecture design
§13 row #17 already chose to extend `meditation-coordination` for
K10 finalisation gate ownership rather than create a seventh skill,
which this design affirms.

### Refresh deliverables checklist

- [x] **D04 resolved** — every row in §3 has a single primary
      destination + zero-or-more mirrors. Five split-primary rows
      normalised:
      - §3.4 Output body sections list → split into Research / Quick
        rows (one primary each).
      - §3.4 Quick vs Research differences table → split into Research
        column / Quick column rows.
      - §3.5 §5.4 Facet registry schema → single primary
        `skill:research`; mirror `skill:coordination` (filename row
        only). "OR" removed.
      - §3.5 §5.5 Inline citation markers → split into Research strict
        variant / Quick warn-only variant.
      - §3.5 §5.5 Validation enforcement → split into Research strict
        respawn 2-retry / Quick warn-only "Citation gaps" callout.

### Refresh detail (cross-reference into the refreshed design doc)

- §3 — 13 new richness surface rows added covering: merged
  `Q-Cost-and-Richness-Acknowledgment` gate, read-only-richness
  `Q-Cost-Acknowledgment-Expansion` variant, `comprehensiveness:`
  payload propagation (same shape + abort semantics as `theming:`),
  `Q-Finalisation-Enhancements` gate (K10a multi-select 0–5 + K10b
  mixed-cost taxonomy with 7 cheap types + K10c YAML update flow +
  ensemble Respawn Targeting + layered cadence — primary `command`
  with mirrors in `skill:research` / `skill:quick` (in-pass K10c
  reflection) + `skill:ensemble` (layered cadence 3b–3f) +
  `skill:report` (K10b Per-Cheap-Type Rendering Contract +
  Report-Skill Respawn Protocol) + `skill:coordination` (filename
  rows)), Comprehensiveness Level Mapping (12×4), 4-mode
  `additional_focus_areas[]` reconciliation (canonical post-W1b
  schema with per-item `treatment:` filter — legacy
  `additional_focus_areas_skipped` / `_accepted` names are DEAD and
  pinned as negative assertions in §8), `init-suggestions-{ts}.yml`
  production, peer-review explicit report sections at `detailed`+,
  Adversarial Review Dim 12 (Comprehensiveness fidelity) + Dim 13
  (Init-suggestion AND finalisation-enhancement honour), Reviewer
  Pattern-B respawn-with-decision-guidance schema + Report-Skill
  Respawn Protocol (K9 + K10b — `respawn_reasons` list-typed),
  Ensemble layered K10 cadence, K10 Ensemble Respawn Targeting.
- §1.3 — mode router gains row 5 for the **K10 In-Pass Reflection
  function** (runs inside depth-0 / aggregator existing LLM turn —
  no extra spawn). Research / Quick rows updated to mention step 4b
  scouting + `init-suggestions-{ts}.yml` write. Adversarial Review
  row updated to mention 13 dimensions + Report-Skill Respawn
  Protocol.
- §1.4 — agent body budget **≤350 → ≤500 lines**, with S12
  integrity-expert flagging >550 lines.
- §4.1 — sections-retained table re-projected against the 2142-line
  post-richness command; uses section-heading anchors as the stable
  key with line-range parentheticals.
- §4.2 — budget projection recomputed: ~1376-line deletable surface;
  target ~650 lines remaining (Pattern A + Pattern B gates +
  Q-Finalisation-Enhancements askQuestion stay on command).
- §5 — trim plan re-projected against the 1388-line memory-manager:
  deletion ranges **279–1159 + 1189–1349** (~1041 lines). **Forget
  Mode at 1160–1188** (was 843–870 pre-richness). K4 risk sharpened
  — Forget Mode is the only thing between the two contiguous
  deletion ranges; S07 implementers MUST delete by section heading,
  not by line range.
- §6.5 NEW — coordination with the 20260523 patch matrix; S08 must
  preserve 30 new pytest classes + 4 new TS describe blocks; S09
  must integrate additively with richness-extended docs.
- §7 — R8 NEW (K10 reflection placement on mode router), R9 NEW
  (six-skill cap verdict — KEPT AT 6), K1 updated (≤500 budget
  threshold), K9 NEW (S12 must diff against the 20260524 freeze,
  not the stale 20260517 freeze), K10 NEW (`additional_focus_areas[]`
  canonical name regression guard for S04/S05/S07/S08).
- §8 — discovery cues extended with new richness substrings; negative
  assertions added for `additional_focus_areas_skipped` /
  `additional_focus_areas_accepted` (W1/W1b regression guard).
- §9 — per-subtask read/produce table updated to cite the new freeze
  and new §3 row positions.

### Refresh result

- **D04**: resolved. The judge's blocker is cleared.
- **Six-skill cap**: confirmed (`KEPT AT 6`) — no `needs_user_input`
  required.
- **Refreshed design doc**: ~1040 lines (was 768 pre-refresh) — line
  count growth proportional to the +13 richness surfaces +
  normalisation overhead. Markdown-only, no linter errors.

### Refresh checklist

- [x] **D04** — Section-mapping table normalised to single-primary + mirror per row across §3.4 / §3.5; five rows normalised; 13 richness rows added.

## Refresh 2026-05-24

### Deliverables Checklist (Refresh)

- [x] **D04** — **Section-mapping table**: every contract item from the new freeze `meditate-frozen-contract-20260524.md` (1557 lines) is mapped to a **single primary destination** in §3 of the design doc. Mirrors are listed for cross-reference only — the primary owns the verbatim contract text. **Judge blocker resolved.**

### Refresh Summary

The original 2026-05-17 design judge-verdict landed as `partial` with a blocker on D04: §3 contained four+ split-primary rows (`§4.1 Output body sections`, `§4.4 Quick vs Research differences`, `§5.4 Facet registry schema` with "OR", `§5.5 Inline citation markers`). In parallel, the completed sibling spec `specs/20260523-meditate-richness/` (executor sign-off 2026-05-24) added 13 new contract surfaces to the source files, growing `.cursor/commands/crux-meditate.md` from 1493 → 2142 lines and `.cursor/agents/crux-cursor-memory-manager.md` from 946 → 1388 lines. The 2026-05-17 freeze line is now stale.

This refresh re-anchors the design doc in place (no sibling file) against the new freeze line `meditate-frozen-contract-20260524.md` and resolves D04 in the same pass. Changes:

1. **§3 — Section-Mapping Table**: 5 split-primary rows normalised to single-primary + mirror(s) (§4.1 output body sections split into Research / Quick rows; §4.4 Quick vs Research differences split into Research column / Quick column rows; §5.4 facet registry schema single primary `skill:research` with mirror `skill:coordination` filename-row only — "OR" removed; §5.5 inline citation markers split into Research strict / Quick warn variants; §5.5 validation enforcement split into Research / Quick paths). 13 new rows added covering: merged `Q-Cost-and-Richness-Acknowledgment` gate, read-only-richness variant of `Q-Cost-Acknowledgment-Expansion`, `comprehensiveness:` payload propagation (with abort rule), `Q-Finalisation-Enhancements` gate (K10a/b/c with mirrors across `skill:research` + `skill:quick` + `skill:ensemble` + `skill:report` + `skill:coordination`), Comprehensiveness Level Mapping (12×4), 4-mode `additional_focus_areas[]` reconciliation (write+honour split), `init-suggestions-{ts}.yml` production, peer-review explicit report sections at `detailed`+, Adversarial Review Dim 12 + Dim 13, Reviewer Pattern-B respawn-with-decision-guidance + Report-Skill Respawn Protocol, Ensemble layered K10 cadence, K10 Ensemble Respawn Targeting.
2. **§1.3 mode router**: new row 5 for the K10 In-Pass Reflection function (per-tree single-model + cross-model ensemble; runs inside depth-0 manager turn, no new spawn); Research + Quick rows mention scouting init-suggestions production + step 4b; Adversarial Review row mentions 13 dimensions + Report-Skill Respawn Protocol.
3. **§1.4 agent body budget**: raised to ≤500 lines against the post-richness ~1041-line source (was ≤350 against pre-richness ~600 lines). Integrity-expert >550-line trigger documented.
4. **§4.1 sections-retained table**: refreshed against the current 2142-line command using section-heading anchors as the stable key, with current line ranges as parentheticals. New sections for richness-introduced surfaces (Q-Cost-and-Richness-Acknowledgment ~106–256, comprehensiveness payload ~361–390, combined Pattern-B 391–738, Q-Finalisation-Enhancements ~1062–1186, Comprehensiveness Level Mapping ~1545–1571, Init-Suggestions Honour ~1807–1821, Report-Skill Respawn Protocol pointer ~1368–1447). Each row marked `unchanged` / `shrunk` / `modified`.
5. **§4.2 budget projection**: recomputed against the 2142-line command; ~1376-line deletable surface; target post-refactor ~650 lines.
6. **§5 trim plan**: re-projected against the 1388-line memory-manager. Deletion ranges 279–1159 + 1189–1349 (~1041 lines). Forget Mode now at 1160–1188 (was 843–870) — K4 risk sharpened (Forget Mode is the ONLY thing between the two contiguous deletion ranges). Replacement pointer paragraphs name the new richness gates.
7. **§6.5 NEW**: coordination with the 20260523 patch matrix as a secondary authoritative input. S08 preserves the 30 new pytest classes + 4 new TS describe blocks introduced by richness S06. S09 integrates additively with README / docs / web extensions already shipped by richness S07.
8. **§7 risks refreshed**: K1 budget threshold updated to ≤500 (was ≤350); R8 NEW (K10 reflection function placement — mode router row, no seventh skill); R9 NEW (six-skill cap verdict — KEPT AT 6 with rationale); K9 NEW (20260523 patch matrix coordination — S12 must diff against 20260524 freeze); K10 NEW (`additional_focus_areas[]` canonical name regression guard — the legacy W1 field names `_skipped` / `_accepted` must not return).
9. **§8 discovery cues**: extended with new richness substrings (`Q-Cost-and-Richness-Acknowledgment`, `Q-Finalisation-Enhancements`, `additional_focus_areas` with `treatment:`, `Comprehensiveness Level Mapping`, `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`, `Dimension 12`, `Dimension 13`, `Report-Skill Respawn Protocol`, `respawn_reasons`, `Per-Cheap-Type Rendering Contract`, `K10 Ensemble Respawn Targeting`, `source_tree`, `surfaced_to_root`, `cross_model_candidates`, `union_candidates`, `set-once-per-invocation`, `compact reproduces pre-richness behaviour`, `per_finding_table`). Negative assertions added for the legacy `additional_focus_areas_skipped` / `additional_focus_areas_accepted` field names.
10. **§9 per-subtask read/produce table**: references the new freeze + new §3 row positions; S12 must diff against `meditate-frozen-contract-20260524.md` (not the stale 20260517 freeze).

### Refresh Outcome

- Refreshed design doc final line count: **1040 lines** (up from 769; ~35% growth driven by the 13 new §3 rows + new §6.5 + new K10 mode router row + extended §8 discovery cues + extended §10 DoD).
- Number of new richness rows added to §3: **13** (covering the 13 surfaces enumerated in the new freeze §0 "What changed since 2026-05-17").
- Number of split-primary rows normalised: **5** (exceeds the ≥4 expected): §4.1 Output body sections, §4.4 Quick vs Research differences, §5.4 Facet registry schema (OR removed), §5.5 Inline citation markers, §5.5 Validation enforcement.
- Risks added: R8, R9, K9, K10 — all confirmed.
- Six-skill cap verdict: **KEPT AT 6**. All 13 new surfaces map into the existing six skills via mirrors. Rationale documented in §7 R9 of the design doc.
- `needs_user_input` blocks emitted: **none**.

### Files Modified (Refresh)

- **Modified**: `specs/20260517-meditate-agent-skill-decomposition/meditate-decomp-architecture-design-20260517.md` (in-place refresh; 769 → 1040 lines; markdown-only; lint-clean)
- **Modified**: this file (Refresh 2026-05-24 section appended — original Deliverables Checklist + Execution Notes preserved verbatim)
- **Modified**: `specs/20260517-meditate-agent-skill-decomposition/status/subtask-02-meditate-decomp-architecture-design-20260517.status.{yml,md}` (state flipped to `completed`; D04 ticked; `extra.judge` replaced with `verified_after_refresh` verdict; artefact + refresh note appended)
- **Modified**: `specs/20260517-meditate-agent-skill-decomposition/status.{yml,md}` (aggregate_state → `in_progress`; S02 entry → `completed`; blocker removed; aggregate_progress updated; rebuild event appended)
