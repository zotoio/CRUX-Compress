# Subtask: Replace `/crux-test` with a pytest shim

## Metadata
- **Subtask ID**: 06
- **Feature**: context-token-reduction
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260713

## Objective

Implement **Option 8** from `analysis/context-token-reduction-report.md`: replace the ~3K-token `.cursor/commands/crux-test.md` (a ten-case LLM-orchestrated test walkthrough written entirely in prose) with a thin shim that invokes a pytest-driven eval suite. The prose test cases move into `evals/` as deterministic pytest tests plus optional LLM-driven assertion helpers.

`crux-test.md` is **not** in `.crux/dist-manifest.json` — this subtask has no consumer impact and no dist-manifest change.

## Deliverables Checklist

- [ ] **D01** — Design the pytest suite structure under `evals/`:
  - New file: `evals/test_r_crux_command_suite.py` (next letter after existing `test_q_meditate.py`, matching the `test_a_`… alphabetical convention in `crux-software-engineer.md`).
  - One pytest test per current `/crux-test` case; use existing `evals/conftest.py` fixtures.
  - Deterministic assertions where possible; where an LLM step is unavoidable (semantic validation, decompression check), use a fixture that spawns a fresh model call and asserts on the structured result.
  - Cover at minimum: (a) baseline compression roundtrip, (b) frontmatter preservation, (c) confidence threshold enforcement, (d) minified/formatted output modes, (e) each `--<n>` level's target-ratio adherence, (f) semantic-equivalence spot check via LLM helper, (g) `--force` re-compression behavior.
- [ ] **D02** — Add a wrapper entry point that the shim invokes. Two acceptable shapes; pick one and document it in the file:
  - **Preferred**: a new `scripts/run_crux_command_suite.py` that calls `pytest evals/test_r_crux_command_suite.py -q` with well-defined exit codes and human-readable summary. Preserves single Python entry point convention already used elsewhere in `scripts/`.
  - **Alternative**: run pytest directly from the shim without a wrapper script.
- [ ] **D03** — Rewrite `.cursor/commands/crux-test.md` as a shim ≤ 60 lines containing:
  - Command purpose (one paragraph).
  - Usage table (single command line — `python3 scripts/run_crux_command_suite.py` or equivalent).
  - One-paragraph mapping from historical `/crux-test` scenarios to their new pytest test names, so anyone who bookmarks the old behavior finds the new location.
  - Zero embedded test prose (that is now inside the pytest file docstrings).
- [ ] **D04** — Add pytest markers or a `-k` group so a partial "smoke" run can be triggered (`pytest evals/test_r_crux_command_suite.py -m crux_command_smoke`).
- [ ] **D05** — Move every test-case description now living in prose in `crux-test.md` into the corresponding pytest test's docstring so the semantic coverage transfers verbatim.
- [ ] **D06** — Ensure `python3 scripts/test.py` (the repository's canonical test runner per `crux-software-engineer.md`) picks up the new tests without configuration changes; if it does not, add the minimum needed to `scripts/test.py`.
- [ ] **D07** — Record before/after `.cursor/commands/crux-test.md` token count in the subtask's status `notes` (target: from ~3K to ≤ 400 tokens).

## Definition of Done

- [ ] **DoD01** — `python3 scripts/run_crux_command_suite.py` (or the direct `pytest evals/test_r_crux_command_suite.py`) exits 0 on a clean tree.
- [ ] **DoD02** — `python3 scripts/test.py` passes (existing full suite), including the new file.
- [ ] **DoD03** — Every historical `/crux-test` scenario is represented by at least one pytest test whose docstring cites the historical case (grep-able mapping).
- [ ] **DoD04** — `.cursor/commands/crux-test.md` is ≤ 60 lines and contains only the shim body per D03.
- [ ] **DoD05** — No linter errors introduced (Python + markdown).
- [ ] **DoD06** — The pytest suite is deterministic enough that a re-run under CI produces the same result on a clean tree (flag any inherently LLM-driven case with an `@pytest.mark.flaky` allowance if needed; document any such marker in the notes).
- [ ] **DoD07** — Subtask 08 has the eval-file paths captured in the subtask notes so its coverage evals can assert them.

## Implementation Notes

- **File-write disjoint from Phase-1 siblings**: `crux-test.md` is edited by no other subtask. `evals/*.py` is new territory for this spec. No merge conflict.
- **No dist impact**: `crux-test.md` is not in `.crux/dist-manifest.json`. This is why Opt 8 is safe to run in Phase 1 alongside the other prose changes.
- **LLM-driven assertions**: some historical `/crux-test` scenarios (semantic equivalence, decompression) require the LLM. Model those as fixtures that spawn a subagent (see `evals/conftest.py` for existing patterns) and assert on the structured return value. Do not embed the LLM prompt inside `crux-test.md`; keep prompts in Python constants or template files under `evals/`.
- **Alphabetical eval file ordering**: use `evals/test_r_crux_command_suite.py` (after `test_q_meditate.py`). Do not use an unprefixed `test_crux_*.py` name.
- **Do not modify `scripts/create-crux-zip.py`**. `crux-test.md` staying (as a shim) means no dist-manifest impact.

## Testing Strategy

**Do NOT trigger the full global suite during parallel execution.** Instead:

- Run just the new pytest file: `python3 -m pytest evals/test_r_crux_command_suite.py -q`.
- Run `python3 scripts/run_crux_command_suite.py` (or equivalent) once end-to-end.
- Full `python3 scripts/test.py` sweep runs at the end of Subtask 08.

## Execution Notes

_To be filled by executing agent._

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
_Agent adds notes here during execution._

### Blockers Encountered
_Any blockers or issues._

### Files Modified
_List of files changed._

