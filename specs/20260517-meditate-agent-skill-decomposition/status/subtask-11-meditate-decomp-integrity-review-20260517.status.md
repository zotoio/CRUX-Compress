# Subtask 11 — meditate-agent-skill-decomposition — live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 11 |
| feature | meditate-agent-skill-decomposition |
| assigned_agent | integrity-expert |
| model | unassigned |
| token_budget | 200000 |
| state | pending |
| started_at |  |
| last_heartbeat |  |
| completed_at |  |
| git_sha |  |
| agent_session_id |  |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
## Checklist

- [ ] **D01** — Read the freeze document
- [ ] **D02** — For each contract item, locate it in the post-refactor
- [ ] **D03** — Flag every contract item whose destination cannot be located
- [ ] **D04** — Verify Pattern A vs Pattern B boundaries are intact (calling-
- [ ] **D05** — Run `pytest evals/test_q_meditate.py evals/test_p_amnesia.py -q`
- [ ] **D06** — Read the test file diffs against the test plan (subtask 03)
- [ ] **D07** — Spot-check the SDK eval `evals/sdk/tests/q-meditate.test.ts`
- [ ] **D08** — Confirm the new agent path appears in `scripts/create-crux-zip.py`
- [ ] **D09** — Confirm every new skill `SKILL.md` path appears in `DIST_FILES`.
- [ ] **D10** — Confirm `.crux/dist-manifest.json` matches the script output.
- [ ] **D11** — Confirm `install.py` `MEMORY_FILE_PREFIXES` and the fallback
- [ ] **D12** — Confirm `.github/workflows/version-bump.yml` `RELEASE_PATHS`
- [ ] **D13** — Run `python -m py_compile install.py scripts/create-crux-zip.py`
- [ ] **D14** — For every source file modified by subtasks 06 / 07 / 09, confirm
- [ ] **D15** — Confirm no `.crux.*` file was hand-edited (no diff outside
- [ ] **D16** — Run linter / type-checks on modified Python files
- [ ] **D17** — Run markdown lint on modified `.md` / `.mdc` files if a
- [ ] **D18** — Confirm no unrelated files were modified (compare against
- [ ] **D19** — Confirm the spec index status field flips from `Draft` to
- [ ] **D20** — Confirm the spec `status.md` aggregator output reflects all
- [ ] **D21** — Produce `integrity-review-meditate-decomp-20260517.md` inside
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
## Artifacts

_No artifacts yet._
<!-- status:artifacts:end -->

<!-- status:errors:start -->
## Errors

_No errors yet._
<!-- status:errors:end -->

<!-- status:notes:start -->
Pending — execution has not yet started.
<!-- status:notes:end -->
