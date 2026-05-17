# Subtask: Update Evals & Tests

## Metadata
- **Subtask ID**: 08
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 03, 06, 07
- **Created**: 20260517

## Objective
Execute the test plan produced by subtask 03 against the post-refactor
repository state (subtasks 04–07): update existing evals to point at
the new agent, add new assertion classes for the guide agent and each
new meditation skill, lock down the freeze contract via regression
checks, and update SDK evals + manual checklists.

## Deliverables Checklist
- [ ] **`evals/test_q_meditate.py`** updated:
      - Migrate the `crux-cursor-memory-manager` substring assertion
        in `TestMeditateAgentSpawning` to assert
        `crux-cursor-meditation-guide` against the *coordinator
        command* file. Keep "meditate mode" or rename to whatever
        subtask 02 finalised.
      - Keep all existing classes
        (`TestMeditateConfigPresence`,
        `TestMeditateCommandDefinition`,
        `TestMeditateFacetStructure`,
        `TestMeditateRecursiveDepth`,
        `TestMeditateMemoryQuerying`,
        `TestMeditateConsolidation`,
        `TestMeditateContinuationMenu`).
      - Add **`TestMeditationGuideAgent`** asserting:
        `.cursor/agents/crux-cursor-meditation-guide.md` exists,
        frontmatter `name == crux-cursor-meditation-guide`,
        persona prologue substrings, mode router headings,
        Phases A–G headings, Quick 6-step heading,
        Ensemble Aggregation heading, Adversarial Review heading,
        `needs_user_input` envelope mention, mandatory
        `context` field mention.
      - Add **`TestMeditationSkills`** with one assertion block
        per skill from subtask 05 (presence of dir + `SKILL.md`,
        frontmatter `name`, key contract substrings).
      - Add **`TestMemoryManagerNoMeditate`** with **negative**
        assertions: the trimmed memory-manager file no longer
        contains Phases A–G prose, Quick 6-step prose, Ensemble
        Aggregation prose, or Adversarial Review prose outside
        of pointer paragraphs.
      - Add **`TestMeditateModesPresent`** asserting Research /
        `--quick` / `--ensemble` mode descriptions still appear in
        the coordinator command.
      - Add **`TestMeditateGatesPresent`** asserting `Q-Depth-Selection`,
        `Q-Cost-Acknowledgment`, theme preflight, facet
        confirmation, and continuation-menu substrings still appear
        in the coordinator command.
      - Add **`TestMeditateReportContract`** asserting paired
        HTML+PDF, Universal Contrast, anti-homogenisation,
        D3/calculator/Chrome fallback, and ensemble report
        substrings appear *somewhere* in
        guide agent + meditation-report skill (combined).

- [ ] **`evals/test_p_amnesia.py`** updated:
      - `EXPLICIT_MEMORY_COMMANDS` keeps `/crux-meditate`.
      - `test_meditate_still_works` updated if it asserts
        memory-manager mention; switch to assert
        `crux-cursor-meditation-guide` (or leave alone if it only
        checks the amnesia doc).

- [ ] **`evals/sdk/tests/q-meditate.test.ts`** updated:
      - All `hasSubagentCall(..., "crux-cursor-memory-manager")`
        assertions for the meditate scenarios switch to
        `crux-cursor-meditation-guide`.
      - Keep the `SDK_EVAL_SKIP_EXPENSIVE` gate.
      - Where appropriate, add a regex check for skill load mention
        (e.g. assistant text references at least one
        `crux-skill-memory-meditation-*` path).

- [ ] **`evals/conftest.py`** updated:
      - Add new fixtures only if subtask 03 specified them
        (e.g. paths to the new agent / skill files for parameterised
        tests).
      - Otherwise leave untouched.

- [ ] **`evals/USER_EVAL_CHECKLISTS.md`** and **`evals/sdk/README.md`**
      updated to mention the new agent + skills in the manual
      meditate scenario.

- [ ] Run the **specific** test suites locally to confirm green:
      `pytest evals/test_q_meditate.py -q` and
      `pytest evals/test_p_amnesia.py -q`. Record output excerpt in
      Execution Notes.

- [ ] If any pre-existing test failure is unrelated, capture it as
      a blocker; do not "fix" unrelated failing tests.

## Definition of Done
- [ ] All four eval files updated per the test plan
- [ ] New assertion classes / blocks added
- [ ] Negative assertions on the trimmed memory-manager pass
- [ ] Targeted pytest runs are green for the meditate / amnesia files
- [ ] No linter errors introduced
- [ ] No assertions silently dropped (every dropped assertion is
      justified in the Execution Notes against subtask 03's plan)

## Implementation Notes
- Follow subtask 03's test plan to the letter. If a deviation is
  needed (e.g. an assertion is impossible against the new
  architecture), record it as a blocker and escalate before
  rewriting.
- **Do not run the global test suite** (`pytest`/`pnpm test` with
  no arguments) during parallel execution; run only the targeted
  files.
- Pyproject's existing pytest config applies; do not add new
  dependencies.
- The SDK eval is **gated** behind `SDK_EVAL_SKIP_EXPENSIVE` —
  CI may skip it; nonetheless update it.
- When asserting frontmatter, use the project's existing
  `frontmatter` parser (see how `test_q_meditate.py` reads
  `.crux/crux-memories.json` for style).

## Testing Strategy
- Run **only**:
  - `pytest evals/test_q_meditate.py -q`
  - `pytest evals/test_p_amnesia.py -q`
- Skip global pytest, skip MCP / installer tests during parallel
  execution.

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
