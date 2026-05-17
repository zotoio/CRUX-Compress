# Subtask: Implement `crux-skill-memory-meditation-*` Skill Family

## Metadata
- **Subtask ID**: 05
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 02
- **Created**: 20260517

## Objective
Create the new meditation skill family under `.cursor/skills/`, following
the existing `crux-skill-memory-*` directory and `SKILL.md` conventions.
Each skill is a standalone, agent-loadable unit owned by a subset of the
Meditate contract per the architecture-design doc (subtask 02).

## Deliverables Checklist
For each skill in the **finalised list from subtask 02** (default proposal:
six skills below), create a directory and a `SKILL.md` with valid
frontmatter and contract-faithful body content.

- [ ] **`crux-skill-memory-meditation-research`** —
      Phases A–G research tree, facet registry + lock, citations index,
      peer review file spec, citation respawn rule (≤2 retries),
      depth-3 default and recursive expansion semantics.
- [ ] **`crux-skill-memory-meditation-quick`** —
      6-step quick protocol, warn-only citations, upfront child
      derivation, depth-1 default override.
- [ ] **`crux-skill-memory-meditation-ensemble`** —
      N-parallel-trees model-pool protocol, batched pending-facet
      cross-tree confirmation, aggregator spawn contract,
      `cross-model-synthesis.md` template, ensemble HTML / PDF
      report extras.
- [ ] **`crux-skill-memory-meditation-review`** —
      11-dimension adversarial review, severities, ≤3 iterations,
      `MUST_FIX` `needs_user_input` schema (with mandatory
      `context`), reviewer review-doc template, decision-guidance
      requirement on every parent `askQuestion`.
- [ ] **`crux-skill-memory-meditation-report`** —
      Mandatory paired HTML + PDF, anti-homogenisation theming,
      Universal Contrast, light/dark + print TOC, Chart.js / D3
      inclusion + static SVG / PNG fallback, calculator inclusion +
      static fallback, headless Chrome → Chromium degradation,
      report verification step ("verify both files exist before
      returning paths").
- [ ] **`crux-skill-memory-meditation-coordination`** —
      Artefact filename table (`meditations/{yyyymmdd}-{topic-slug}/`),
      prefix-glob polling rule ("never hard-code report names"),
      facet registry lock semantics, retrospective template
      (`retrospective-{ts}.md`), Branch & Leaf Index template
      appended to `facets.md`.

For each skill:

- [ ] Frontmatter contains `name: <skill-dir-name>` and a
      `description` that mentions "meditation" plus the verb
      (e.g. "research", "review").
- [ ] Body opens with a "When to use" section that states which
      agent / mode / sub-mode loads the skill.
- [ ] Body includes the contract items assigned to that skill in
      subtask 02's mapping table, with no items orphaned.
- [ ] Body references the new guide agent by exact name
      (`crux-cursor-meditation-guide`) when describing the caller.
- [ ] `SKILL.md` lints cleanly (frontmatter parses, no broken
      markdown links).

## Definition of Done
- [ ] All skill directories created under `.cursor/skills/`
- [ ] All `SKILL.md` files exist and validate
- [ ] No skill orphans an architecture-design contract item
- [ ] No two skills duplicate the same primary contract item
- [ ] No linter errors introduced

## Implementation Notes
- Use `.cursor/skills/crux-skill-memory-extract/SKILL.md` and
  `.cursor/skills/crux-skill-memory-rebalance/SKILL.md` as the
  template for SKILL.md frontmatter and body shape.
- Honour the project rule
  `crux-skill-memory-meditation-*` is **not** a generated `.crux.md`
  output — these are first-class hand-authored skill files.
- Do **not** wire skills into the coordinator command or the
  guide agent in this subtask — the wiring lives in subtasks 04
  (agent load directives) and 06 (command Related links).
- Do **not** add any of the new skill paths to install / dist /
  manifests in this subtask — that is owned by subtask 09.
- Final skill count and naming may be adjusted from the default
  list in K3 if subtask 02's design changed it; follow subtask 02's
  finalised list verbatim.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Markdown-only artefacts. Targeted verification: load each
  `SKILL.md` and confirm frontmatter parses (e.g. via `python -c
  "import yaml,frontmatter"` if used elsewhere; otherwise visual
  check).
- Subtask 08 adds substring-presence assertions for each skill.

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
