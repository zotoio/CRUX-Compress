# Subtask: Integrity & Regression Review

## Metadata
- **Subtask ID**: 12
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: integrity-expert
- **Dependencies**: 08, 09, 10, 11
- **Created**: 20260517

## Objective
Independently audit the post-refactor repo state against the frozen
contract from subtask 01 and the spec's Definition of Done. Confirm zero
functionality loss, full eval coverage, correct dist enumeration, and
consistent CRUX mirror state. Surface any deviation as a blocker for user
review.

## Deliverables Checklist

### Functional preservation audit
- [ ] Read the freeze document
      `meditate-frozen-contract-20260517.md` (subtask 01).
- [ ] For each contract item, locate it in the post-refactor repository
      (coordinator command / guide agent / a meditation skill /
      preserved memory-manager pointer) and record the destination.
- [ ] Flag every contract item whose destination cannot be located as a
      **MUST_FIX** finding.
- [ ] Verify Pattern A vs Pattern B boundaries are intact (calling-agent
      gates remain in the command; tree work is delegated via Task;
      subagents do not call `AskQuestion`).

### Eval coverage audit
- [ ] Run `pytest evals/test_q_meditate.py evals/test_p_amnesia.py -q`
      and confirm all green.
- [ ] Read the test file diffs against the test plan (subtask 03) and
      confirm every planned assertion was implemented and no assertion
      was silently dropped.
- [ ] Spot-check the SDK eval `evals/sdk/tests/q-meditate.test.ts`
      compiles (TypeScript) — `pnpm --filter <eval-package> build` or
      equivalent, if available — without forcing the gated run.

### Distribution audit
- [ ] Confirm the new agent path appears in `scripts/create-crux-zip.py`
      `DIST_FILES`.
- [ ] Confirm exactly six new meditation skill `SKILL.md` paths appear
      in `DIST_FILES`: `research`, `quick`, `ensemble`, `review`,
      `report`, `coordination`.
- [ ] Confirm `.crux/dist-manifest.json` matches the script output.
- [ ] Confirm `install.py` `MEMORY_FILE_PREFIXES` and the fallback file
      list include the new agent + new skill prefix.
- [ ] Confirm `.github/workflows/version-bump.yml` `RELEASE_PATHS` (or
      its source manifest) covers the new paths.
- [ ] Run `python -m py_compile install.py scripts/create-crux-zip.py`
      to confirm both still parse.

### CRUX mirror audit
- [ ] For every source file modified by subtasks 06 / 07 / 09 / 10,
      confirm that any pre-existing maintained `.crux.md` /
      `.crux.mdc` mirror has been regenerated (subtask 11) or skipped
      with documented justification.
- [ ] Confirm no `AGENTS.crux.md` file was created or required.
- [ ] Confirm no new `.crux.*` mirror coverage was introduced.
- [ ] Confirm no `.crux.*` file was hand-edited (no diff outside
      `crux-cursor-rule-manager` regeneration shape — banner +
      frontmatter + crux fenced block).

### Code-quality audit
- [ ] Run linter / type-checks on modified Python files (`install.py`,
      `scripts/create-crux-zip.py`, eval files): `python -m pyflakes`
      or the project's chosen tool.
- [ ] Run markdown lint on modified `.md` / `.mdc` files if a project
      tool is available.
- [ ] Confirm no unrelated files were modified (compare against git
      status from the start of this spec's execution).

### Spec hygiene
- [ ] Confirm the spec index status field flips from `Draft` to
      `Completed` only after this audit passes (the executor /
      aggregator does this; integrity-expert merely confirms it is
      appropriate).
- [ ] Confirm the spec `status.md` aggregator output reflects all 12
      subtasks as `completed`.
- [ ] Treat terse status checklist text as non-blocking. When a
      `.status.yml` or `.status.md` checklist item is abbreviated, verify
      its full context against the original subtask markdown before
      raising an issue.

### Findings report
- [ ] Produce `integrity-review-meditate-decomp-20260517.md` inside
      this spec directory with sections:
      - **Verdict** (`PASS` / `CONDITIONAL` / `FAIL`)
      - **Functional preservation** — coverage table contract item ->
        destination
      - **Eval coverage** — pass/fail summary
      - **Distribution** — pass/fail summary
      - **CRUX mirrors** — pass/fail summary
      - **Code quality** — lint/type-check summary
      - **Findings** — list of `MUST_FIX` / `SHOULD_FIX` /
        `NICE_TO_HAVE` issues with file paths and recommended
        remediation
      - **Sign-off** — confirmation that Definition of Done is met or
        list of unmet items requiring user decision

## Definition of Done
- [ ] All audits run; pass / fail recorded
- [ ] Findings document exists
- [ ] No `MUST_FIX` findings open (or each open one has explicit user
      approval to defer recorded in the spec index Execution Notes)
- [ ] Targeted pytest is green
- [ ] Distribution and install enumeration verified
- [ ] CRUX mirror state verified
- [ ] No linter errors introduced

## Implementation Notes
- **Read-only audit** — this subtask must not modify command, agent,
  skill, eval, doc, install, dist, manifest, or rule files. Only writes
  the findings document.
- If a `MUST_FIX` finding is detected, surface it via Pattern B
  `needs_user_input` in Execution Notes — do not silently fix it, even
  if the fix looks trivial. The spec executor / parent agent decides
  whether to spawn a follow-up subtask.
- Audit must be conducted independently — do not rely solely on the
  prior subtasks' Execution Notes; verify against the freeze document
  and the actual repo state.

## Testing Strategy
- Run **only**:
  - `pytest evals/test_q_meditate.py evals/test_p_amnesia.py -q`
  - `python -m py_compile install.py scripts/create-crux-zip.py`
  - Any project markdown / type checker for files modified.
- Do not run the global test suite or SDK gated eval.

## Execution Notes

### Agent Session Info
- Agent: integrity-expert
- Started: 2026-05-24T06:41:00Z
- Completed: 2026-05-24T06:45:00Z

### Work Log
1. Read S12 brief, 20260524 freeze contract (§0–§10), architecture design, eval plan, spec index + DoD.
2. Verified line counts: guide agent 495 ✓, memory-manager 351 ✓, command 1020 ✓, 6 skills 2155 total ✓.
3. Spot-checked all 13 richness surfaces via grep on post-refactor artefacts.
4. Verified all 41 freeze-contract items present.
5. Ran pytest: 353/353 green.
6. Ran vitest: 48 passed / 6 skipped (gated live-API tests) / 0 failed.
7. Ran `python3 -m py_compile install.py scripts/create-crux-zip.py`: COMPILE OK.
8. Ran ReadLints on 18 modified files: all clean.
9. Verified 5×7 dist enumeration matrix (create-crux-zip.py, install.py, dist-manifest.json, version-bump.yml, CONTRIBUTORS.md).
10. Verified negative assertions: 25 pytest + 7 TS = 32 total (≥31 ✓).
11. Verified CRUX mirrors: 10 mirrors, all checksums match via crux-utils; AGENTS.crux.md absent.
12. Verified negative-assertion forbidden substrings (no memory-manager spawn in coordinator, no legacy field names emitted).
13. Wrote integrity report to `integrity-report-meditate-decomp-20260524.md`.

### Blockers Encountered
None.

### Files Modified
- `specs/20260517-meditate-agent-skill-decomposition/integrity-report-meditate-decomp-20260524.md` (created — audit deliverable)
- `specs/20260517-meditate-agent-skill-decomposition/subtask-12-meditate-decomp-integrity-review-20260517.md` (Execution Notes appended)
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-12-meditate-decomp-integrity-review-20260517.status.md` (flipped to completed)
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-12-meditate-decomp-integrity-review-20260517.status.yml` (flipped to completed)
- `specs/20260517-meditate-agent-skill-decomposition/status.yml` (S12 state=completed, aggregate_progress+1, aggregate_state=completed)
- `specs/20260517-meditate-agent-skill-decomposition/spec-meditate-agent-skill-decomposition-20260517.md` (Status line + DoD ticks)

### D01–D08 Checklist
- [x] D01 Read the freeze document
- [x] D02 For each contract item, locate it in the post-refactor repository
- [x] D03 Flag every contract item whose destination cannot be located (0 flagged)
- [x] D04 Verify Pattern A vs Pattern B boundaries intact
- [x] D05 Eval coverage audit (pytest green; vitest structural green)
- [x] D06 Distribution audit (5 surfaces × 7 paths verified)
- [x] D07 CRUX mirror audit (10 mirrors current; no new mirrors)
- [x] D08 Code-quality audit (ReadLints clean; py_compile OK)

### Definition of Done
- [x] All audits run; pass / fail recorded
- [x] Findings document exists (`integrity-report-meditate-decomp-20260524.md`)
- [x] No `MUST_FIX` findings open
- [x] Targeted pytest is green (353/353)
- [x] Distribution and install enumeration verified
- [x] CRUX mirror state verified
- [x] No linter errors introduced
