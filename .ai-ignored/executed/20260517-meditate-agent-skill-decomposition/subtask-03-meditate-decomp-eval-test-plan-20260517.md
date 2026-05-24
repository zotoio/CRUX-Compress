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
- [x] Create `meditate-decomp-eval-test-plan-20260517.md` inside this
      spec directory.
- [x] **Current surface inventory**:
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
- [x] **Migration matrix**: one row per current assertion → new
      assertion (kept verbatim / re-targeted / replaced). Mark
      removed assertions explicitly and justify each.
- [x] **New assertion plan** for each new asset:
      - Guide agent: frontmatter shape, persona prologue substrings,
        mode router headings, Phases A–G headings, Quick 6-step
        headings, Ensemble Aggregation headings, Adversarial Review
        headings, `needs_user_input` mention.
      - Each new skill: `SKILL.md` exists, frontmatter `name` matches
        directory, `description` contains "meditation" + the verb,
        contract-specific substrings (e.g. report skill mentions
        "Universal Contrast", review skill mentions "13 dimensions"
        (corrected post-richness from the original "11 dimensions"
        per freeze §4.9), coordination skill mentions "facet registry").
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
- [x] **SDK eval plan** (TS): update agent invocation expectations
      from `crux-cursor-memory-manager` to
      `crux-cursor-meditation-guide`; keep gating; add new
      assertions for skill loading mentions in the assistant text
      where appropriate.
- [x] **Conftest changes** (if any): new fixtures needed for the
      new agent / skill files (paths, sample content).
- [x] **Manual eval scenarios**: list of `evals/USER_EVAL_CHECKLISTS.md`
      / `evals/sdk/README.md` updates needed so manual reviewers
      cover the new architecture.
- [x] **Regression guarantees**: explicit assertions that lock down
      the freeze line — modes present, gates present, mandatory
      report pair, adversarial loop, retrospective template.

## Definition of Done
- [x] Test plan document exists in spec directory
- [x] Every current assertion has a target row in the migration matrix
- [x] Every new asset has at least one substring assertion planned
- [x] Plan is actionable by subtask 08 without further design decisions
- [x] No linter errors introduced

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

### Agent Session Info
- Agent: `crux-platform-architect`
- Started: 2026-05-24
- Completed: 2026-05-24

### Work Log

1. Read the subtask brief, the new freeze contract
   `meditate-frozen-contract-20260524.md` (1557 lines — supersedes
   the 20260517 freeze), and the refreshed architecture-design doc
   §3 (section-mapping table — single-primary per row + 13 new
   richness rows) and §8 (discovery cues — positive + negative
   substrings).
2. Inventoried the current eval surface across `evals/test_q_meditate.py`
   (36 classes — 8 pre-richness + 28 richness-era; ≈177 test methods
   total), `evals/test_p_amnesia.py` (3 meditate touchpoints — all
   command-name-only, no subagent-identity literals), and
   `evals/sdk/tests/q-meditate.test.ts` (8 describe blocks — 3
   pre-richness Q1–Q3 + 5 richness-era structural; 28 `it` blocks
   total). Noted a minor freeze prose discrepancy: §10.3.2 prose says
   "4 NEW richness describe blocks" but the enumerated table inside
   the freeze itself lists 5; the eval plan adopts the actual file
   count (5).
3. Read `evals/conftest.py` (no fixtures consumed by meditate tests
   today) and inventoried `evals/USER_EVAL_CHECKLISTS.md` Q1–Q3 + the
   Integration § Meditate step + `evals/sdk/README.md` references.
4. Built the migration matrix: identified the single literal swap in
   `test_q_meditate.py::TestMeditateAgentSpawning::test_spawns_memory_manager`
   (`crux-cursor-memory-manager` → `crux-cursor-meditation-guide`),
   the single literal swap in
   `q-meditate.test.ts::Q1 — spawns subagents for recursive exploration`,
   6 resolver-widening cases for richness-era classes whose content
   moves into `skill:report` / `skill:review` / `skill:ensemble` /
   `skill:research`, and the K8 list narrowing in
   `TestMeditateNoNewDistFilesK8` (drop the 4 decomp-legitimate skill
   prefixes; keep runtime-only artefact prefixes). All 28 richness-era
   classes are structurally preserved (additive); ~80% of pytest
   classes kept verbatim by class count.
5. Drafted the new assertion plan grouped by destination: guide agent
   (24 new assertions in `TestMeditationGuideAgent`), six skills (69
   new assertions across six skill classes with the mandated
   three-presence + contract-specific substrings), refactored thin
   coordinator command (19 new assertions including the negative
   `crux-cursor-memory-manager` absence), trimmed memory-manager (12
   new assertions including 8 negative ones for forbidden Meditate
   executable headings), and dist-presence (4 new positive assertions
   across 17 substring checks). Total: **138 new positive + 28 new
   negative assertions** — both targets exceeded (≥50 / ≥10).
6. Drafted the SDK plan: 1 literal swap + 4 new unconditional
   structural describe blocks (26 new `it` tests) covering guide agent
   + six skills + thin coordinator + trimmed memory-manager.
7. Defined the conftest changes: new `_read_meditation_artifact(kind,
   name)` helper + 2 new fixtures (`sample_meditation_working_dir`,
   `sample_init_suggestions_yml`) — zero breaking changes.
8. Defined the manual-eval scenario updates: Q1 literal re-target + 3
   new expected-outcome rows; File Reference table additions for the
   new guide agent + six skill paths; SDK README Test Categories row
   update.
9. Defined the regression-guarantee block pinning every 2026-05-24
   freeze invariant (modes / 5 gates incl.
   `Q-Cost-and-Richness-Acknowledgment` and
   `Q-Finalisation-Enhancements` / mandatory paired HTML+PDF / 13-dim
   adversarial loop with Dim 12 + Dim 13 / retrospective always-written
   / K10 layered cadence / K10c rubric / Comprehensiveness Level
   Mapping / canonical `additional_focus_areas[]` + `treatment:` filter).
10. Defined the negative-assertion block (forbidden legacy field names
    `additional_focus_areas_skipped` / `additional_focus_areas_accepted`
    via 10 per-source granularity asserts; forbidden
    `crux-cursor-memory-manager` in `/crux-meditate` spawn context;
    forbidden Meditate executable headings in post-S07 memory-manager).
11. Verified the plan-doc-only deliverable is markdown-only with no
    linter errors via `ReadLints`. Plan-doc line count: **1095 lines**.
12. Updated this brief: ticked D01–D08 + DoD; recorded files modified
    below.

### Blockers Encountered
None. The freeze prose "4 NEW describe blocks" off-by-one was resolved
by anchoring on the actual file count (5) — noted in §1.3 of the plan
doc for the integrity-review subtask.

### Files Modified

- **created** `specs/20260517-meditate-agent-skill-decomposition/meditate-decomp-eval-test-plan-20260517.md`
  — 1095 lines; markdown-only; covers D01–D08 with §1 surface
  inventory (8 + 28 pytest classes, 3 + 5 SDK describes, 3 amnesia
  touchpoints, conftest fixtures, USER_EVAL_CHECKLISTS + SDK README
  references), §2 migration matrix (~80% verbatim by class count; 1
  pytest literal swap + 6 resolver widenings + 1 K8 list narrowing +
  1 SDK literal swap), §3 new assertion plan (138 positive across 10
  new pytest classes), §4 SDK plan (26 new it tests across 4 new
  structural describe blocks), §5 conftest changes (1 new helper + 2
  new fixtures), §6 manual scenario updates, §7 regression guarantees
  pinning all 2026-05-24 freeze invariants, §8 negative-assertion
  block (28 negative), §9 headline rollups, §10 recommended S08
  execution order.
- **modified** `specs/20260517-meditate-agent-skill-decomposition/subtask-03-meditate-decomp-eval-test-plan-20260517.md`
  — Ticked Deliverables Checklist D01–D08 and DoD items 1–5; filled
  Execution Notes (Work Log / Blockers / Files Modified / Agent Session
  Info). Corrected the original "11 dimensions" reference in the
  brief's review-skill cue to "13 dimensions" per freeze §4.9.
