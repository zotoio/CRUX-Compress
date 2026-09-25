# Subtask: Evals + CI coverage for the new context surface

## Metadata
- **Subtask ID**: 08
- **Feature**: context-token-reduction
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 05, 06, 07
- **Created**: 20260713

## Objective

Add evals and CI coverage that lock in the reductions made by Subtasks 01–07 so future edits cannot silently regress them. The evals validate **behavioural invariants** (not surface text) so they survive further CRUX compression.

## Deliverables Checklist

- [ ] **D01** — Lazy-CRUX enforcement eval:
  - New eval file (or extension of the Subtask-06 eval file) that scans `.cursor/agents/*.md` and asserts:
    - `crux-cursor-rule-manager.md` **contains** an unconditional `Read CRUX.md` (or equivalent) instruction.
    - `.cursor/agents/crux-platform-architect.md`, `crux-software-engineer.md`, `integrity-expert.md`, `docs-sync-agent.md`, `crux-cursor-meditation-guide.md`, and all `crux-memory-*.md` files **contain** the conditional wording ("only when the task involves … CRUX notation") OR the `context_manifest` honor block.
    - No non-CRUX agent contains the phrase "Before doing ANY work, you MUST read CRUX.md" (post-compression, the eval must still catch equivalent CRUX-encoded instructions — coordinate with `crux-cursor-rule-manager` on a stable marker).
- [ ] **D02** — `context_manifest` honor eval:
  - Assert every long agent (all files > 3K tokens in the pre-compression baseline, or every agent named in Subtask 01 D03/D04/D06) either declares or references the `context_manifest` prelude.
  - Add a smoke test that spawns a stub subagent with a `context_manifest` stanza in its task prompt and asserts (via the LLM helper harness) that the subagent's first turn does not re-read a file marked `loaded`.
- [ ] **D03** — Template lazy-load eval:
  - Assert `.cursor/commands/templates/compress-prompts.md` exists and is only referenced from `crux-compress.md`.
  - Assert `.cursor/agents/templates/recall-canvas.tsx.md` exists and is only referenced from `crux-memory-recall.md`.
- [ ] **D04** — Memory-manager split eval:
  - Assert the five thin agent files exist and each has valid frontmatter.
  - Assert the umbrella `crux-cursor-memory-manager.md` is ≤ 60 lines (allowing for the deprecation notice + dispatcher table) and contains the deprecation banner.
  - Assert `rg -c "crux-cursor-memory-manager" .cursor/commands/` returns zero non-deprecation matches.
- [ ] **D05** — Compressed-primitive semantic parity eval:
  - For each file compressed in Subtask 07, run an LLM-driven parity check (existing pattern from `evals/`) that reads source (from git history via `git show HEAD~1:<path>`) if available OR the pre-compression fixture staged in `evals/fixtures/`, decompresses the current file, and asserts semantic equivalence with a confidence gate.
  - Recommended: store per-file "must-preserve properties" (like a checklist of workflow steps or delegation targets) as JSON fixtures under `evals/fixtures/crux-compressed/` so the parity check has an objective anchor.
- [ ] **D06** — `/crux-test` shim eval:
  - Assert `.cursor/commands/crux-test.md` is ≤ 60 lines and dispatches to `python3 scripts/run_crux_command_suite.py` (or equivalent per Subtask 06 D02).
  - Assert `python3 scripts/run_crux_command_suite.py` exits 0 (suite file: `evals/test_r_crux_command_suite.py`).
- [ ] **D07** — CI wiring:
  - Ensure `python3 scripts/test.py` runs all of the above evals in one invocation.
  - If CI (`.github/workflows/*.yml`) needs updates to invoke a new script or entry point, update the workflow(s) minimally and document the change.
- [ ] **D08** — Baseline vs post-spec token-cost measurement:
  - Produce a short markdown fragment (`evals/reports/context-token-reduction-baseline.md` or similar) that walks the three canonical workflows in the DoD ((a) trivial Q&A, (b) `/crux-dream <spec>`, (c) 10-subtask `/z-spec-execute` dry-run) and records baseline vs post-spec estimated tokens using `crux-utils`.
  - This fragment is what Subtask 09 pulls into the execution report.

## Definition of Done

- [ ] **DoD01** — Every eval above passes on the current tree.
- [ ] **DoD02** — `python3 scripts/test.py` passes end-to-end.
- [ ] **DoD03** — CI workflow(s) either need no update, or the update is minimal and documented.
- [ ] **DoD04** — Baseline vs post-spec token-cost report exists and records measurable reductions across all three canonical workflows. Aspirational target: ≥ 30% cumulative reduction across the three (matching the report's Phase-1-to-Phase-5 stack projection). The ≥ 30% figure is **aspirational**, not a hard gate — if measured savings are lower, document methodology and actual percentages; do not fail the subtask solely on missing 30%.
- [ ] **DoD05** — No linter errors introduced (Python + YAML for any workflow file).
- [ ] **DoD06** — Any deferred compression from Subtask 07 has a corresponding "not yet compressed" eval that will flip to green when the compression eventually lands (informational, not gating).

## Implementation Notes

- **Dependencies**: This subtask depends on Subtasks 05, 06, and 07 all being verified before it runs. Subtask 07's compression waves define which files the semantic-parity eval must cover — do not enumerate a compression eval for a file that Subtask 07 deferred.
- **Robustness to future compression**: use behavioural / structural assertions (frontmatter fields, file existence, agent-name resolution) rather than natural-language phrase matching wherever possible. Where a phrase check is unavoidable, coordinate with `crux-cursor-rule-manager` (Subtask 07's owner) on a stable CRUX marker that will survive future recompression.
- **Fixtures**: pre-compression fixtures under `evals/fixtures/crux-compressed/` should be small structured JSON files, not full markdown copies. Something like `{ "file": ".cursor/agents/crux-memory-recall.md", "must_preserve": ["Recall mode", "--total canvas branch", "invocation variants table", "Pattern B"] }`.
- **CI cost**: prefer deterministic assertions in CI; keep LLM-driven parity checks in a slower `test:full` or `test:llm` invocation that runs on a schedule or manually.
- **No shim-forever**: any eval you write to guard against silent regression should also fail if the deprecated umbrella `crux-cursor-memory-manager.md` grows beyond the shim shape — the deprecation notice is enforceable.

## Testing Strategy

- Run each eval individually as it is written: `python3 -m pytest evals/<file>::<test> -q`.
- Then run the full pytest suite: `python3 -m pytest evals/ -q`.
- Then run `python3 scripts/test.py` end-to-end.
- Include the LLM-driven parity checks in the "full" run; keep them out of the fast smoke run.

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

