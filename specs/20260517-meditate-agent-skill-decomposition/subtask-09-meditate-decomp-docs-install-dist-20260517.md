# Subtask: Sync Docs, Rules, Install, Dist, Version-Bump

## Metadata
- **Subtask ID**: 09
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: docs-sync-agent
- **Dependencies**: 04, 05, 06, 07
- **Created**: 20260517

## Objective
Update every documentation, rule, install, distribution, and CI surface
that mentions the meditate workflow or that must enumerate shipped
files, so that they all reflect the new architecture: thin coordinator
command, `crux-cursor-meditation-guide` agent, and
`crux-skill-memory-meditation-*` skills. This subtask carries the
**explicit user authorisation** required by the workspace
`zip-contents-protection` rule for adding new paths.

## Deliverables Checklist

### Documentation surfaces
- [ ] **`README.md`**:
      - Command table — meditate description / agent column updated to
        `crux-cursor-meditation-guide`.
      - File table / agents table — add new agent + new skills.
      - Any "Available Agents" section — add the new agent.
      - Any "Skills" or "Skill catalogue" section — add the new
        skills with one-line descriptions.

- [ ] **`AGENTS.md`** (source file):
      - Add `crux-cursor-meditation-guide` to the "Available Agents"
        table with definition path and purpose.
      - Update "Spec Execution — Agent Allocation" if appropriate
        (e.g. add a row "Meditate / Research / Quick / Ensemble"
        → `crux-cursor-meditation-guide`).
      - Do NOT edit `AGENTS.crux.md` directly — subtask 10 regenerates
        it from this source.

- [ ] **`docs/crux-memories.md`**:
      - Update the meditate description to reflect the thin-coordinator
        + guide-agent + skills architecture.
      - Update the `commands.meditate` config example only if the path
        changed (it should not — the command file path is unchanged).
      - Update any walkthrough / checklist that references
        `crux-cursor-memory-manager` for meditate to
        `crux-cursor-meditation-guide`.

- [ ] **`web/compress.md/memories.html`**:
      - Update user-facing copy + diagram labels referring to
        meditate to mention the new agent.
      - Add the new skills to any relevant skill listing if present.

- [ ] **`CONTRIBUTORS.md`**:
      - Update any agent / skill table to include the new entries.

### Rule surfaces
- [ ] **`.cursor/rules/crux-memories-integration.md`** (source):
      - Confirm `/crux-meditate` remains in the explicit-command list.
      - Update any agent-name reference for meditate to
        `crux-cursor-meditation-guide`.
      - Subtask 10 regenerates `crux-memories-integration.crux.mdc`.

- [ ] **`.cursor/rules/docs-sync.md`** (source):
      - If documentation surfaces or skill paths change patterns,
        update the rule body. Subtask 10 regenerates
        `docs-sync.crux.mdc`.

- [ ] Other `.cursor/rules/*.md` only if they directly reference
      meditate persona or memory-manager-as-meditate-agent.

### Install / distribution surfaces
- [ ] **`install.py`**:
      - `MEMORY_FILE_PREFIXES` adds `crux-cursor-meditation-guide.md`
        and `crux-skill-memory-meditation-` prefix.
      - Fallback CDN file list adds the new agent + new skill
        `SKILL.md` paths.
      - `DEFAULT_MEMORIES_CONFIG.commands.meditate` only changes if
        the command file path changed (it should not).

- [ ] **`scripts/create-crux-zip.py`**:
      - `DIST_FILES` adds the new agent file path.
      - `DIST_FILES` adds each new skill `SKILL.md` path.
      - Run the script locally if convenient and capture the new
        manifest content for `.crux/dist-manifest.json` regeneration.

- [ ] **`.crux/dist-manifest.json`**:
      - Regenerate from the updated `create-crux-zip.py` so that
        version-bump's `RELEASE_PATHS` derivation is consistent.
      - If regeneration is automated by another script, run it.

- [ ] **`.github/workflows/version-bump.yml`**:
      - If `RELEASE_PATHS` is hand-maintained (not generated from
        the manifest), add the new agent path and a parent-dir entry
        for `.cursor/skills/crux-skill-memory-meditation-*`.
      - If `RELEASE_PATHS` is auto-generated from the manifest, no
        edit required — but verify by running the manifest
        regeneration step.

### Cross-doc consistency
- [ ] Search the repo for any leftover string `crux-cursor-memory-manager`
      in a meditate context that should be `crux-cursor-meditation-guide`
      and update it (excluding the trimmed agent file's own pointer
      paragraphs and historical spec / changelog entries).

- [ ] Search for any leftover phrase like "Phases A–G" or
      "Adversarial Review" outside the new guide agent / new skills /
      historical spec dirs / changelog and confirm relocation.

## Definition of Done
- [ ] All documentation surfaces reflect the new architecture
- [ ] All rule sources updated; CRUX mirrors flagged for subtask 10
- [ ] `install.py`, `create-crux-zip.py`, `.crux/dist-manifest.json`,
      and `version-bump.yml` enumerate the new agent + skills
- [ ] No linter errors introduced
- [ ] No broken links in updated docs
- [ ] Spot-check: cloning the dist zip after the change includes
      the new agent + skills (subtask 11 will verify rigorously)

## Implementation Notes
- This subtask carries the **explicit user authorisation** required
  by `.cursor/rules/zip-contents-protection.crux.mdc` for adding
  new paths to `create-crux-zip.py` — no further opt-in is needed.
- Do **not** edit any `.crux.md` / `.crux.mdc` mirror directly.
  Edit the source `.md` and let subtask 10 regenerate the mirror
  via `crux-cursor-rule-manager`.
- For `dist-manifest.json` regeneration, prefer the project's
  existing script if one exists; otherwise update by hand to match
  the new `DIST_FILES` content and document the procedure in
  Execution Notes.
- Honour the version-bump rule: this is a feature-level change
  (new agent + new skills + refactored command) → minor bump (m).
  The rule auto-bumps via commit; do not bump manually here.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Run only:
  - `python -c "import install"` to confirm install.py imports cleanly
    after edits.
  - `python -m py_compile scripts/create-crux-zip.py` to confirm the
    script still parses.
  - Spot-check: `python scripts/create-crux-zip.py --list` (if
    such a flag exists) to enumerate files.

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
