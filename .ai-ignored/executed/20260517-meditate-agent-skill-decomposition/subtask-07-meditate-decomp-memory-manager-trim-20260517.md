# Subtask: Trim Meditate Sections out of `crux-cursor-memory-manager.md`

## Metadata
- **Subtask ID**: 07
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 04, 06
- **Created**: 20260517

## Objective
Remove every Meditate-specific section from
`.cursor/agents/crux-cursor-memory-manager.md`. Replace each removed
section with a one-paragraph pointer to the new
`crux-cursor-meditation-guide` agent and, where relevant, the
appropriate `crux-skill-memory-meditation-*` skill. Preserve every
non-Meditate section (Dream / REM / Recall / Remember / Forget agent
contracts, shared `needs_user_input` envelope schema if it is generic
across modes, generic skill-load directives, persona prologue parts
that apply to all lifecycle modes).

## Deliverables Checklist
- [ ] For each section listed in subtask 02's "memory-manager trim
      plan", delete the section content and replace it with a
      pointer paragraph of the form:
      > **Meditate (and Research / Quick / Ensemble Aggregation /
      > Adversarial Review): see
      > `.cursor/agents/crux-cursor-meditation-guide.md`. Tree work
      > is owned by that agent; the memory manager no longer
      > contains the Meditate executable contract.**
- [ ] **Phases A–G research** — removed; pointer added.
- [ ] **Quick 6-step protocol** — removed; pointer added.
- [ ] **Ensemble Aggregation sub-mode** — removed; pointer added.
- [ ] **Adversarial Review sub-mode** — removed; pointer added.
- [ ] **Meditate-only invocation rows** in the agent's invocation
      table — removed (rows for `--quick`, `--ensemble`, internal
      child payloads with `meditateDepth` / `preConfirmedFacets` /
      `ensembleModel`).
- [ ] **Meditate-only sections of the `Skills You Use` table** —
      retained rows that apply to other lifecycle modes; remove
      Meditate-only rows; the new meditation skills are NOT listed
      here (they belong to the guide agent's table).
- [ ] **Examples and prompts** that are Meditate-only — removed; if
      they double as generic examples, retained with a
      "(non-Meditate use only)" qualifier.
- [ ] **Front-matter, persona prologue, generic `needs_user_input`
      envelope schema, Dream / REM / Recall / Remember / Forget
      sections** — preserved untouched.
- [ ] Verify that the memory-manager file is still a complete,
      self-consistent agent definition for its remaining lifecycle
      modes (Dream / REM / Recall / Remember / Forget).
- [ ] Verify the file no longer contains substrings:
      `Phases A–G research`, `Quick 6-step`,
      `Ensemble Aggregation`, `Adversarial Review` as a
      memory-manager mode (the strings may still appear inside
      pointer paragraphs, but only there).

## Definition of Done
- [ ] All Meditate sections removed from
      `.cursor/agents/crux-cursor-memory-manager.md`
- [ ] Each removed section has a pointer paragraph
- [ ] All non-Meditate sections preserved verbatim
- [ ] No linter errors introduced
- [ ] File still parses and renders cleanly
- [ ] No broken internal links

## Implementation Notes
- Use the trim plan from subtask 02 as the authoritative list of
  sections to remove — do not improvise.
- If subtask 02 marked any section "shared" (e.g. the
  `needs_user_input` envelope schema), keep it in
  `crux-cursor-memory-manager.md` (since it is a generic envelope)
  and ensure the guide agent (subtask 04) has its own copy or a
  pointer to memory-manager — whichever subtask 02 chose.
- Do **not** modify the new guide agent file or the new skill files
  in this subtask.
- This subtask **completes the source-of-truth migration**. After
  it lands, `crux-cursor-memory-manager.md` is the source of truth
  for all non-Meditate lifecycle modes, and
  `crux-cursor-meditation-guide.md` is the source of truth for
  Meditate / Research / Quick / Ensemble / Adversarial Review.
- Remember:
  `.cursor/agents/crux-cursor-memory-manager.md` is a source file —
  edit directly. If a `.crux.md` / `.crux.mdc` mirror exists for
  it (none today), subtask 11 regenerates it.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Run only file-targeted lint.
- Subtask 08 will assert the absence of removed substrings as a
  negative test, plus presence of pointer paragraphs as a positive
  test.

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-05-24T06:00:00Z
- Completed: 2026-05-24T06:05:00Z

### Work Log
1. Read `.cursor/agents/crux-cursor-memory-manager.md` (1392 lines pre-trim) to map exact section boundaries.
2. Confirmed Meditate Mode section: lines 279–1162 (header through blank line before Forget Mode).
3. Confirmed Forget Mode: lines 1163–1191 — preserved verbatim.
4. Confirmed Ensemble Aggregation Mode section: lines 1192–1353 (header through blank line before `## Agent Scoping Rules`).
5. Executed atomic Python script performing 3 replacements in-memory:
   - Deleted both expertise bullets (lines 57–58): `**Meditate**` and `**Ensemble Aggregation**`.
   - Replaced Meditate Mode section (lines 279–1162) with pointer paragraph `### Meditate Mode — moved`.
   - Replaced Ensemble Aggregation Mode section (lines 1192–1353) with pointer paragraph `### Ensemble Aggregation Mode — moved`.
6. File written: 352 lines (target ~360; 1040 lines removed).
7. Verified: `rg -n "meditat|crux-meditate"` returns exactly 2 matches (lines 279 and 312 — both pointer paragraphs).
8. Verified: No forbidden content survives (`Phases A–G`, `Quick 6-step`, `additional_focus_areas`, `Adversarial Review`, invocation table, etc.).
9. Verified: Forget Mode preserved verbatim at lines 281–308 of trimmed file.
10. `ReadLints` clean — no linter errors.

### Blockers Encountered
None.

### Files Modified
- `.cursor/agents/crux-cursor-memory-manager.md` — trimmed from 1392 to 352 lines; Meditate Mode and Ensemble Aggregation Mode sections replaced with pointer paragraphs; two expertise bullets deleted.
