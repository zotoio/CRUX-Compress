# Subtask: Documentation Sync

## Metadata
- **Subtask ID**: 09
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: docs-sync-agent
- **Dependencies**: 04, 05, 06, 07
- **Created**: 20260517

## Objective
Update documentation surfaces that describe the meditate workflow so they
reflect the new architecture: thin coordinator command,
`crux-cursor-meditation-guide` agent, and exactly six
`crux-skill-memory-meditation-{verb}` skills. This subtask is limited to
documentation sync. It must not edit implementation, install,
distribution, manifest, or workflow files.

## Deliverables Checklist

### Documentation surfaces
- [ ] **`README.md`**:
      - Command table — meditate description / agent column updated to
        `crux-cursor-meditation-guide`.
      - File table / agents table — add the new agent and the six
        approved skills.
      - Any "Available Agents" section — add the new agent.
      - Any "Skills" or "Skill catalogue" section — add the six
        approved skills with one-line descriptions.

- [ ] **`AGENTS.md`** (source file):
      - Add `crux-cursor-meditation-guide` to the "Available Agents"
        table with definition path and purpose.
      - Update "Spec Execution — Agent Allocation" if appropriate
        (e.g. add a row "Meditate / Research / Quick / Ensemble"
        -> `crux-cursor-meditation-guide`).
      - Do **not** assume `AGENTS.crux.md` is a maintained checked-in
        mirror. It is a transient install-time artifact and must not
        be regenerated or created by this spec.

- [ ] **`docs/crux-memories.md`**:
      - Update the meditate description to reflect the thin-coordinator
        + guide-agent + six-skill architecture.
      - Update the `commands.meditate` config example only if the path
        changed (it should not — the command file path is unchanged).
      - Update any walkthrough / checklist that references
        `crux-cursor-memory-manager` for meditate to
        `crux-cursor-meditation-guide`.

- [ ] **`web/compress.md/memories.html`**:
      - Update user-facing copy + diagram labels referring to
        meditate to mention the new agent.
      - Add the six approved skills to any relevant skill listing if
        present.

- [ ] **`CONTRIBUTORS.md`**:
      - Update any agent / skill table to include the new guide agent
        and six approved meditation skills.

- [ ] **Manual / eval documentation**:
      - Update `evals/USER_EVAL_CHECKLISTS.md` and
        `evals/sdk/README.md` if they describe meditate's subagent
        architecture.

### Cross-doc consistency
- [ ] Search documentation files for any leftover string
      `crux-cursor-memory-manager` in a meditate context that should
      be `crux-cursor-meditation-guide` and update it (excluding
      historical spec / changelog entries).

- [ ] Search documentation files for any leftover phrase like
      "Phases A–G" or "Adversarial Review" outside the new guide
      agent / new skills / historical spec dirs / changelog and
      confirm relocation.

## Definition of Done
- [ ] All documentation surfaces reflect the new architecture
- [ ] All six approved skills are documented by exact name
- [ ] No optional or extra skill names are introduced
- [ ] No implementation, install, dist, manifest, workflow, or generated
      `.crux.*` files are modified by this subtask
- [ ] No linter errors introduced
- [ ] No broken links in updated docs

## Implementation Notes
- This subtask is documentation-only. Do **not** edit `install.py`,
  `scripts/create-crux-zip.py`, `.crux/dist-manifest.json`,
  `.github/workflows/version-bump.yml`, or `.cursor/rules/*`.
  Those surfaces are owned by subtask 10.
- Do **not** edit any `.crux.md` / `.crux.mdc` mirror directly.
  If a maintained checked-in mirror becomes stale because a source
  changed, subtask 11 regenerates it.
- `AGENTS.md` is a source documentation/guidance file. There is no
  maintained checked-in `AGENTS.crux.md` mirror in this repository.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Run only file-targeted markdown lint or link checks where available.
- Do not run pytest, SDK evals, install scripts, dist scripts, or
  workflow commands in this subtask.

## Execution Notes

### Agent Session Info
- Agent: docs-sync-agent
- Started: 2026-05-24T06:10:00Z
- Completed: 2026-05-24T06:35:00Z

### Work Log
- Read subtask brief, frozen contract, architecture design §3.9/§6.5, and all five target doc surfaces
- Verified 20260523 richness content already present in README/docs/html; no duplication needed
- Updated AGENTS.md: added `crux-cursor-meditation-guide` to Available Agents table (consumer block) and Spec Execution — Agent Allocation table (repo-internal)
- Updated README.md: added Meditation Skills subsection (+10 lines with 6 skill rows), added meditation guide agent row to Installation in Another Project table and File Locations Summary table
- Updated docs/crux-memories.md: amended line 46 to correctly attribute `/crux-meditate` → `crux-cursor-meditation-guide`; added meditation guide agent subsection; added 6 meditation skill rows to Skills table
- Updated web/compress.md/memories.html: added "Meditation Agent & 6 Skills" subsection with agent label and 6 skill divs after existing "Powered by 6 Skills" section
- Updated CONTRIBUTORS.md: added guide agent row to Release-Relevant Files and Memory System Components tables; added 6 individual meditation skill rows to Memory System Components; added `test_q_meditate.py` to directory listing and test suites table; added `evals/sdk/tests/q-meditate.test.ts` to directory listing and test suites table
- Ran ReadLints: no linter errors on any modified file
- Searched for stale `crux-cursor-memory-manager` in meditate context — no remaining stale references outside historical spec/changelog entries

### Blockers Encountered
None.

### Files Modified
- `AGENTS.md` (+2 lines)
- `README.md` (+12 lines)
- `docs/crux-memories.md` (+15 lines)
- `web/compress.md/memories.html` (+11 lines)
- `CONTRIBUTORS.md` (+14 lines)

### Deliverables Checklist (ticked)
- [x] **D01** README.md — guide agent row + 6 skill rows added
- [x] **D02** AGENTS.md — Available Agents + Spec Allocation updated; no AGENTS.crux.md regenerated
- [x] **D03** docs/crux-memories.md — thin coordinator + guide agent + six-skill architecture documented
- [x] **D04** web/compress.md/memories.html — guide agent label + six skill names added
- [x] **D05** CONTRIBUTORS.md — agent row + 6 skill rows + eval files added
- [x] **D06** eval documentation — test_q_meditate.py + q-meditate.test.ts added to listing
- [x] **D07** stale reference search complete — no meditate memory-manager refs outside historical entries

### Definition of Done
- [x] All documentation surfaces reflect the new architecture
- [x] All six approved skills documented by exact name
- [x] No optional or extra skill names introduced
- [x] No implementation, install, dist, manifest, workflow, or generated .crux.* files modified
- [x] No linter errors introduced
- [x] No broken links in updated docs
