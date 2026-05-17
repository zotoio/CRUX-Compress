# Subtask: Integrity & Regression Review

## Metadata
- **Subtask ID**: 11
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: integrity-expert
- **Dependencies**: 08, 09, 10
- **Created**: 20260517

## Objective
Independently audit the post-refactor repo state against the frozen
contract from subtask 01 and the spec's Definition of Done. Confirm
zero functionality loss, full eval coverage, correct dist enumeration,
and consistent CRUX mirror state. Surface any deviation as a
blocker for user review.

## Deliverables Checklist

### Functional preservation audit
- [ ] Read the freeze document
      `meditate-frozen-contract-20260517.md` (subtask 01).
- [ ] For each contract item, locate it in the post-refactor
      repository (coordinator command / guide agent / a meditation
      skill / preserved memory-manager pointer) and record the
      destination.
- [ ] Flag every contract item whose destination cannot be located
      as a **MUST_FIX** finding.
- [ ] Verify Pattern A vs Pattern B boundaries are intact (calling-
      agent gates remain in the command; tree work is delegated
      via Task; subagents do not call `AskQuestion`).

### Eval coverage audit
- [ ] Run `pytest evals/test_q_meditate.py evals/test_p_amnesia.py -q`
      and confirm all green.
- [ ] Read the test file diffs against the test plan (subtask 03)
      and confirm every planned assertion was implemented and no
      assertion was silently dropped.
- [ ] Spot-check the SDK eval `evals/sdk/tests/q-meditate.test.ts`
      compiles (TypeScript) — `pnpm --filter <eval-package> build`
      or equivalent, if available — without forcing the gated run.

### Distribution audit
- [ ] Confirm the new agent path appears in `scripts/create-crux-zip.py`
      `DIST_FILES`.
- [ ] Confirm every new skill `SKILL.md` path appears in `DIST_FILES`.
- [ ] Confirm `.crux/dist-manifest.json` matches the script output.
- [ ] Confirm `install.py` `MEMORY_FILE_PREFIXES` and the fallback
      file list include the new agent + new skill prefix.
- [ ] Confirm `.github/workflows/version-bump.yml` `RELEASE_PATHS`
      (or its source manifest) covers the new paths.
- [ ] Run `python -m py_compile install.py scripts/create-crux-zip.py`
      to confirm both still parse.

### CRUX mirror audit
- [ ] For every source file modified by subtasks 06 / 07 / 09, confirm
      that any pre-existing `.crux.md` / `.crux.mdc` mirror has been
      regenerated (subtask 10) — verify by checking
      `sourceChecksum` matches the current source.
- [ ] Confirm no `.crux.*` file was hand-edited (no diff outside
      `crux-cursor-rule-manager` regeneration shape — banner +
      frontmatter + crux fenced block).

### Code-quality audit
- [ ] Run linter / type-checks on modified Python files
      (`install.py`, `scripts/create-crux-zip.py`, eval files):
      `python -m pyflakes` or the project's chosen tool.
- [ ] Run markdown lint on modified `.md` / `.mdc` files if a
      project tool is available.
- [ ] Confirm no unrelated files were modified (compare against
      git status from the start of this spec's execution).

### Spec hygiene
- [ ] Confirm the spec index status field flips from `Draft` to
      `Completed` only after this audit passes (the executor /
      aggregator does this; integrity-expert merely confirms it
      is appropriate).
- [ ] Confirm the spec `status.md` aggregator output reflects all
      11 subtasks as `completed`.

### Findings report
- [ ] Produce `integrity-review-meditate-decomp-20260517.md` inside
      this spec directory with sections:
      - **Verdict** (`PASS` / `CONDITIONAL` / `FAIL`)
      - **Functional preservation** — coverage table contract item →
        destination
      - **Eval coverage** — pass/fail summary
      - **Distribution** — pass/fail summary
      - **CRUX mirrors** — pass/fail summary
      - **Code quality** — lint/type-check summary
      - **Findings** — list of `MUST_FIX` / `SHOULD_FIX` /
        `NICE_TO_HAVE` issues with file paths and recommended
        remediation
      - **Sign-off** — confirmation that Definition of Done is met
        or list of unmet items requiring user decision

## Definition of Done
- [ ] All audits run; pass / fail recorded
- [ ] Findings document exists
- [ ] No `MUST_FIX` findings open (or each open one has explicit
      user approval to defer recorded in the spec index Execution
      Notes)
- [ ] Targeted pytest is green
- [ ] Distribution and install enumeration verified
- [ ] CRUX mirror state verified
- [ ] No linter errors introduced

## Implementation Notes
- **Read-only audit** — this subtask must not modify command,
  agent, skill, eval, doc, install, dist, manifest, or rule files.
  Only writes the findings document.
- If a `MUST_FIX` finding is detected, surface it via Pattern B
  `needs_user_input` in Execution Notes — do not silently fix it,
  even if the fix looks trivial. The spec executor / parent agent
  decides whether to spawn a follow-up subtask.
- Audit must be conducted independently — do not rely solely on
  the prior subtasks' Execution Notes; verify against the freeze
  document and the actual repo state.

## Testing Strategy
- Run **only**:
  - `pytest evals/test_q_meditate.py evals/test_p_amnesia.py -q`
  - `python -m py_compile install.py scripts/create-crux-zip.py`
  - Any project markdown / type checker for files modified.
- Do not run the global test suite or SDK gated eval.

## Execution Notes
*(to be filled by executing agent)*

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
[Agent adds notes here during execution]

### Blockers Encountered
[Any blockers or issues]

### Files Modified
[List of files changed]
