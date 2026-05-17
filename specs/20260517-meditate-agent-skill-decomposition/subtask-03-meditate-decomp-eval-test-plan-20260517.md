# Subtask: Eval & Test Plan

## Metadata
- **Subtask ID**: 03
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 01, 02
- **Created**: 20260517

## Objective
Capture the current Meditate-related eval / test surface, then produce a
detailed, file-by-file test plan that subtask 08 will execute. The plan
must (a) preserve all existing assertion intent, (b) re-target assertions
that move from `crux-cursor-memory-manager` to
`crux-cursor-meditation-guide`, and (c) add new regression coverage for
the new skills, modes (Research / Quick / Ensemble), gates (depth, cost,
theme, facet, deep-YAML), mandatory reports, and adversarial review.

## Deliverables Checklist
- [ ] Create `meditate-decomp-eval-test-plan-20260517.md` inside this
      spec directory.
- [ ] **Current surface inventory**:
      - `evals/test_q_meditate.py` — list every test class and what it
        currently asserts (substrings, file existence, frontmatter
        keys), and which contract item from subtask 01 it covers.
      - `evals/test_p_amnesia.py` — `EXPLICIT_MEMORY_COMMANDS`
        membership and `test_meditate_still_works` assertions.
      - `evals/sdk/tests/q-meditate.test.ts` — gating
        (`SDK_EVAL_SKIP_EXPENSIVE`), each test's regex/string
        assertions, fixtures used.
      - `evals/conftest.py` — fixtures consumed by meditate tests
        (today none directly).
      - Any other discovered assertions (e.g. README user-eval
        checklists, USER_EVAL_CHECKLISTS.md scenarios).
- [ ] **Migration matrix**: one row per current assertion → new
      assertion (kept verbatim / re-targeted / replaced). Mark
      removed assertions explicitly and justify each.
- [ ] **New assertion plan** for each new asset:
      - Guide agent: frontmatter shape, persona prologue substrings,
        mode router headings, Phases A–G headings, Quick 6-step
        headings, Ensemble Aggregation headings, Adversarial Review
        headings, `needs_user_input` mention.
      - Each new skill: `SKILL.md` exists, frontmatter `name` matches
        directory, `description` contains "meditation" + the verb,
        contract-specific substrings (e.g. report skill mentions
        "Universal Contrast", review skill mentions "11 dimensions",
        coordination skill mentions "facet registry").
      - Coordinator command: still has `## Usage`, mode descriptions,
        depth selection, cost ack, theme preflight, ensemble
        orchestration, continuation menu, **and now references
        `crux-cursor-meditation-guide`** (not memory-manager) for
        tree spawn.
      - Memory-manager: NO longer contains Meditate-only sections
        (negative assertions: absence of "Phases A–G research",
        absence of "Quick 6-step", absence of "Adversarial Review"
        as a memory-manager mode), but still contains Dream / REM /
        Recall / Remember / Forget contracts.
- [ ] **SDK eval plan** (TS): update agent invocation expectations
      from `crux-cursor-memory-manager` to
      `crux-cursor-meditation-guide`; keep gating; add new
      assertions for skill loading mentions in the assistant text
      where appropriate.
- [ ] **Conftest changes** (if any): new fixtures needed for the
      new agent / skill files (paths, sample content).
- [ ] **Manual eval scenarios**: list of `evals/USER_EVAL_CHECKLISTS.md`
      / `evals/sdk/README.md` updates needed so manual reviewers
      cover the new architecture.
- [ ] **Regression guarantees**: explicit assertions that lock down
      the freeze line — modes present, gates present, mandatory
      report pair, adversarial loop, retrospective template.

## Definition of Done
- [ ] Test plan document exists in spec directory
- [ ] Every current assertion has a target row in the migration matrix
- [ ] Every new asset has at least one substring assertion planned
- [ ] Plan is actionable by subtask 08 without further design decisions
- [ ] No linter errors introduced

## Implementation Notes
- This is a **read-only** subtask — produce a markdown plan only.
- Use the architecture-design doc from subtask 02 to know which
  contract items live in which destination, so assertions land in
  the right test class.
- Honour the project pattern of using **substring presence**
  assertions over content hashes — they are robust to incidental
  edits.
- Where an SDK eval relies on
  `hasSubagentCall(..., "crux-cursor-memory-manager")`, propose
  the new `crux-cursor-meditation-guide` value but keep a fallback
  consideration for tests that genuinely still spawn the memory
  manager (Dream / REM / Recall etc.) to avoid over-rewriting.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Markdown-only artefact; no automated tests apply.

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
