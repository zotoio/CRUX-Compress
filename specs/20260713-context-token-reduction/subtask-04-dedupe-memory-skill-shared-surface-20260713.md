# Subtask: Consolidate memory-skill shared surface into `_memory-shared.md`

## Metadata
- **Subtask ID**: 04
- **Feature**: context-token-reduction
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: None
- **Created**: 20260713

## Objective

Implement **Option 3** and **Option 10** from `analysis/context-token-reduction-report.md`:
- **R3** — the same `.crux/crux-memories.json` config table (`maxMemorySize`, `compressionMinLines`, `compressionTarget`, `sizeUnit`, `typePriority`, `storage.*`, `referenceTracking.*`, `flags.enableMemory*`) is re-tabled in five memory-skill files (~1.2K tokens duplicated).
- **R2** — Pattern A/B User-Input Escalation is fully re-pasted in `crux-cursor-memory-manager.md` and reduced-re-pasted in five memory command files (~1.6K tokens duplicated).
- **R8** — every memory command ends with a 6-line `## Related` block listing the same set (~840 tokens duplicated).
- **Opt 10** — every memory skill ends with a `## What This Skill Does NOT Do` block plus one or more `## Integration` tables that re-list paths (~2K tokens duplicated).

Move all of these into a single `.cursor/skills/_memory-shared.md` and cross-reference from each skill / command with a single line. Consumer memory commands are all in `.crux/dist-manifest.json`; the new shared file becomes a dist candidate (KD-5).

## Deliverables Checklist

- [x] **D01** — Create `.cursor/skills/_memory-shared.md` containing:
  - `## Config Reference` — one authoritative table of `.crux/crux-memories.json` keys with defaults, cross-referenced against the JSON as source of truth.
  - `## User-Input Escalation` — canonical Pattern A / Pattern B write-up (may be a one-paragraph pointer to the AGENTS.md `<CRUX>` block plus the `needs_user_input` YAML example).
  - `## Related Commands & Skills` — one table listing all `/crux-*` memory commands and the `crux-skill-memory-*` skills with one-line purposes.
  - `## Cross-Skill Boundaries` — one list of "which skill owns what" derived from the AGENTS.md agent-allocation table.
- [x] **D02** — In each of the five memory-skill files below, remove the duplicated config table and replace with a one-line pointer:
  - `.cursor/skills/crux-skill-memory-rebalance/SKILL.md`
  - `.cursor/skills/crux-skill-memory-compress/SKILL.md`
  - `.cursor/skills/crux-skill-memory-extract/SKILL.md`
  - `.cursor/skills/crux-skill-memory-crud/SKILL.md`
  - `.cursor/skills/crux-skill-memory-reference-tracker/SKILL.md`

  Pointer form: `> Config keys and defaults: see \`.cursor/skills/_memory-shared.md#config-reference\` and \`.crux/crux-memories.json\` (authoritative).`
- [x] **D03** — In each of the **six** memory-command files below, remove the duplicated `## Related` block and the abbreviated Pattern A/B recap, replacing with a two-line pointer to `_memory-shared.md`:
  - `.cursor/commands/crux-dream.md`
  - `.cursor/commands/crux-recall.md`
  - `.cursor/commands/crux-forget.md`
  - `.cursor/commands/crux-remember.md`
  - `.cursor/commands/crux-meditate.md`
  - `.cursor/commands/crux-amnesia.md`
- [x] **D04** — In every memory-skill file (all six under `.cursor/skills/crux-skill-memory-*/`), remove the `## What This Skill Does NOT Do` block and any `## Integration` table that merely re-lists paths already documented in AGENTS.md or in another skill's ownership row. Replace with a one-line pointer:
  > Out-of-scope and cross-skill delegation: see `.cursor/skills/_memory-shared.md#cross-skill-boundaries` and the agent table in `AGENTS.md`.
- [x] **D05** — Do **not** remove any operational content (step lists, invocation examples, error handling protocols, or field-specific validation). Only remove reference material now covered by `_memory-shared.md`.
- [x] **D06** — Record before/after token counts per file in the subtask's status `notes`.
- [x] **D07** — Flag `.cursor/skills/_memory-shared.md` as a dist-manifest addition for Subtask 09 to aggregate under **Dist manifest additions — awaiting user approval**. This new file is required by every consumer memory skill / command that references it.

## Definition of Done

- [x] **DoD01** — `.cursor/skills/_memory-shared.md` exists with the four sections in D01.
- [ ] **DoD02** — Cumulative memory-skill + memory-command token count drops by ≥ 4K tokens vs `analysis/context-token-reduction-report.md` §1.2 baseline (target range 5–8K; measure actual). **Partial: -3,389 tokens achieved (611 short of 4K minimum). Further trimming would violate D05 — see status notes for evidence-based explanation and the §1.2 baseline drift caveat.**
- [x] **DoD03** — Every touched file still contains a working pointer to `_memory-shared.md` (no dangling section anchors — verify anchors exactly match the headings you wrote).
- [x] **DoD04** — No operational instruction removed: for each removed section, confirm the section was purely reference material (config table, protocol re-paste, "does not do" list, integration re-listing). Anything conditional or workflow-critical stays in the owning file.
- [x] **DoD05** — `rg -n "Pattern A" .cursor/commands/ .cursor/skills/` shows only pointers or brief per-command mode-note references — no full re-pasted protocol description remains outside `_memory-shared.md` and `AGENTS.md`.
- [x] **DoD06** — No linter errors introduced.
- [x] **DoD07** — Subtask 09 has the dist-manifest addition (`.cursor/skills/_memory-shared.md`) captured in this subtask's notes.

## Implementation Notes

- **File-write ownership vs Phase-1 / Phase-2 siblings**: S01 doesn't touch skills or memory commands. S02 touches rules; S03 touches `crux-compress.md`; S06 touches `crux-test.md`. This subtask edits five memory skills + **six** memory commands + creates `_memory-shared.md`.
- **Overlap with S05 (ordered, not parallel)**: S05 also edits the same memory **commands** (`crux-dream`, `crux-recall`, `crux-remember`, `crux-forget`, and incidental meditate callouts) to re-point spawn targets to thin agents. S05 depends on this subtask — S04 owns pointer/dedupe edits first; S05 re-reads those commands after S04 is verified and applies spawn re-points without undoing `_memory-shared.md` pointers. This subtask does **not** touch `crux-cursor-memory-manager.md` (S05 owns the split).
- The `_memory-shared.md` filename intentionally uses a leading underscore so tooling that walks `.cursor/skills/*/SKILL.md` (which expects a directory-per-skill layout) does not accidentally treat it as a skill.
- Do **not** create a `_memory-shared/SKILL.md` — it is not a Cursor skill, just a shared reference doc.
- Consumer impact (KD-5): `_memory-shared.md` becomes a new dist file. Flag for user approval; do not modify `scripts/create-crux-zip.py`.
- Preserve every skill's `description:` frontmatter verbatim so the IDE skill loader still discovers them correctly.
- Coordinate on cross-references with S01: if S01's AGENTS.md rewrite renames a section anchor, update your pointer accordingly. Use `AGENTS.md` heading text current at the time your work merges.
- Coordinate with S05: S05 will split `crux-cursor-memory-manager.md` into thin agents. Each thin agent should also use `_memory-shared.md` for the same pointers. S05 depends on this subtask so the shared file exists before the split.

## Testing Strategy

**Do NOT trigger global test suites during parallel execution.** Instead:

- After each per-file edit, `rg` for the removed section headings in that file — expect zero matches.
- Verify every pointer anchor (`#config-reference`, `#user-input-escalation`, etc.) matches a heading in `_memory-shared.md` exactly (character-for-character, lowercase with hyphens).
- Full eval sweep deferred to Subtask 08.

## Execution Notes

### Agent Session Info
- Agent: `crux-platform-architect`
- Started: 2026-07-13T07:12:00Z
- Completed: 2026-07-13T07:35:00Z

### Work Log

1. Read the subtask spec, the referenced analysis (`analysis/context-token-reduction-report.md` §3 R2/R3/R8 + §4 Option 10), and all 12 target files.
2. Captured before-token counts for each of the 12 touched files via `crux-utils --token-count`.
3. Created `.cursor/skills/_memory-shared.md` with the four required sections (`## Config Reference`, `## User-Input Escalation`, `## Related Commands & Skills`, `## Cross-Skill Boundaries`).
4. Removed the duplicated `## Config Reference` table (and the `### Type Transition Rules` subsection) from the five D02 skills and replaced with a one-line pointer to `_memory-shared.md#config-reference`.
5. Removed the `## Integration` and `## What This Skill Does NOT Do` blocks from all six D04 skills; replaced with the `#cross-skill-boundaries` pointer. Kept CRUD's `## What NOT to Do` (skill-specific behavioural rules, not cross-skill delegation).
6. Shortened the enumerated config-key list inside the `## Prerequisites` step of rebalance / compress / extract so it names the keys the skill needs but points at `#config-reference` for defaults and full descriptions (operational load-config instruction preserved).
7. Replaced the abbreviated Pattern A/B recap in all six memory commands with a one-line pointer to `#user-input-escalation`; replaced the 5–12 line `## Related` blocks with two-line pointers to `#related-commands--skills`.
8. Removed the duplicate `Do NOT call AskQuestion` sentence from `crux-skill-memory-extract` Response Format (kept the Pattern-B contract but replaced the long protocol restatement with a pointer).
9. Recaptured after-token counts and recorded per-file deltas + cumulative drop in the status YAML notes.
10. Verified DoD03 anchor validity for every pointer (`#config-reference`, `#user-input-escalation`, `#related-commands--skills`, `#cross-skill-boundaries` all exactly match headings in `_memory-shared.md`).
11. Ran `rg -n "Pattern A" .cursor/commands/ .cursor/skills/` and confirmed DoD05 (only pointers, brief mode notes, and per-gate operational references remain).
12. Recorded the dist-manifest addition (`_memory-shared.md`) under `extra.dist_manifest_additions` for Subtask 09 to consume.

### Blockers Encountered

None — DoD02 achieved 3,389 tokens vs the 4,000-token literal minimum (611 short). Further trimming would remove operational content (violating D05). The status notes explain the shortfall against the §1.2 baseline drift (meditate.md grew ~23K since the report was written) and the per-workflow amortisation of the shared file.

### Files Modified

Created:
- `.cursor/skills/_memory-shared.md` (3,619 tokens, new; flagged for dist manifest per KD-5)

Modified (all under `.cursor/skills/` and `.cursor/commands/`):
- `.cursor/skills/crux-skill-memory-rebalance/SKILL.md`
- `.cursor/skills/crux-skill-memory-compress/SKILL.md`
- `.cursor/skills/crux-skill-memory-extract/SKILL.md`
- `.cursor/skills/crux-skill-memory-crud/SKILL.md`
- `.cursor/skills/crux-skill-memory-reference-tracker/SKILL.md`
- `.cursor/skills/crux-skill-memory-index/SKILL.md`
- `.cursor/commands/crux-dream.md`
- `.cursor/commands/crux-recall.md`
- `.cursor/commands/crux-forget.md`
- `.cursor/commands/crux-remember.md`
- `.cursor/commands/crux-meditate.md`
- `.cursor/commands/crux-amnesia.md`

Untouched (as required):
- `.cursor/agents/crux-cursor-memory-manager.md` — owned by Subtask 05 (thin-agent split)
- `scripts/create-crux-zip.py` — KD-5 gate; addition flagged for Subtask 09 to aggregate

