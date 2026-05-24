# Subtask: Install, Distribution, and Release Path Sync

## Metadata
- **Subtask ID**: 10
- **Feature**: meditate-agent-skill-decomposition
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 04, 05, 06, 07
- **Created**: 20260517

## Objective
Update implementation-adjacent packaging and release surfaces so installs,
dist zips, and version-bump release path detection include the new
`crux-cursor-meditation-guide` agent and exactly six approved
`crux-skill-memory-meditation-{verb}` skills. This subtask also updates
source rule files only if they directly reference meditate's agent
architecture. Documentation-only surfaces are owned by subtask 09.

## Deliverables Checklist

### Install / distribution surfaces
- [ ] **`install.py`**:
      - `MEMORY_FILE_PREFIXES` adds `crux-cursor-meditation-guide.md`
        and `crux-skill-memory-meditation-` prefix.
      - Fallback CDN file list adds the new agent plus exactly six
        skill `SKILL.md` paths:
        `research`, `quick`, `ensemble`, `review`, `report`,
        `coordination`.
      - `DEFAULT_MEMORIES_CONFIG.commands.meditate` only changes if
        the command file path changed (it should not).

- [ ] **`scripts/create-crux-zip.py`**:
      - `DIST_FILES` adds the new agent file path.
      - `DIST_FILES` adds each of the six approved skill `SKILL.md`
        paths.
      - Do not add any seventh skill path or optional placeholder.

- [ ] **`.crux/dist-manifest.json`**:
      - Regenerate or update from the updated `create-crux-zip.py`
        so that version-bump's `RELEASE_PATHS` derivation is
        consistent.
      - If regeneration is automated by another script, run it and
        record the command.

- [ ] **`.github/workflows/version-bump.yml`**:
      - If `RELEASE_PATHS` is hand-maintained (not generated from the
        manifest), add the new agent path and a parent-dir entry for
        `.cursor/skills/crux-skill-memory-meditation-*`.
      - If `RELEASE_PATHS` is auto-generated from the manifest, no edit
        required — but verify by running the manifest regeneration
        step.

### Source rule surfaces
- [ ] **`.cursor/rules/crux-memories-integration.md`** (source), only
      if it directly references meditate's agent architecture:
      - Confirm `/crux-meditate` remains in the explicit-command list.
      - Update any agent-name reference for meditate to
        `crux-cursor-meditation-guide`.
      - Do not edit `crux-memories-integration.crux.mdc`; subtask 11
        regenerates maintained mirrors.

- [ ] **`.cursor/rules/docs-sync.md`** (source), only if the new docs
      / agent / skill paths change the rule's source patterns:
      - Update source-rule prose.
      - Do not edit `docs-sync.crux.mdc`; subtask 11 regenerates
        maintained mirrors.

- [ ] Other `.cursor/rules/*.md` source files only if they directly
      reference meditate persona or memory-manager-as-meditate-agent.

### Cross-repo implementation consistency
- [ ] Search non-documentation, non-historical files for any leftover
      string `crux-cursor-memory-manager` in a meditate context that
      should be `crux-cursor-meditation-guide` and update it.

- [ ] Search non-documentation, non-historical files for any leftover
      phrase like "Phases A–G" or "Adversarial Review" outside the new
      guide agent / new skills and confirm relocation.

## Definition of Done
- [ ] `install.py`, `create-crux-zip.py`, `.crux/dist-manifest.json`,
      and `version-bump.yml` enumerate the new agent + exactly six
      approved skills where applicable
- [ ] Source rule files are updated only where they directly reference
      the meditate architecture
- [ ] No documentation-only files owned by subtask 09 are modified here
      unless required to resolve a direct implementation consistency
      conflict
- [ ] No generated `.crux.md` / `.crux.mdc` files are hand-edited
- [ ] No linter errors introduced
- [ ] Spot-check: dist enumeration includes the new agent + six skills
      (subtask 12 verifies rigorously)

## Implementation Notes
- This subtask carries the **explicit user authorisation** required by
  `.cursor/rules/zip-contents-protection.crux.mdc` for adding new paths
  to `scripts/create-crux-zip.py` and related install / release
  surfaces — no further opt-in is needed.
- The skill list is fixed: `research`, `quick`, `ensemble`, `review`,
  `report`, `coordination`. If execution discovers a need for any
  additional skill path, stop and escalate via `needs_user_input`.
- Do **not** edit any `.crux.md` / `.crux.mdc` mirror directly. Edit
  source files only; subtask 11 handles existing maintained mirror
  regeneration.
- `AGENTS.crux.md` is not a maintained checked-in mirror and must not
  be generated or required.
- Honour the version-bump rule: this is a feature-level change (new
  agent + new skills + refactored command) -> minor bump (m). The rule
  auto-bumps via commit; do not bump manually here.

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution.
- Run only:
  - `python -c "import install"` to confirm `install.py` imports cleanly
    after edits.
  - `python -m py_compile scripts/create-crux-zip.py` to confirm the
    script still parses.
  - Spot-check dist enumeration using the project's existing script /
    command if available.

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Started: 2026-05-24T06:07:00Z
- Completed: 2026-05-24T06:09:26Z

### Work Log

**install.py — MEMORY_FILE_PREFIXES**
Added `.cursor/agents/crux-cursor-meditation-guide.md` as a new explicit entry. The existing `.cursor/skills/crux-skill-memory-` prefix already covers all six `crux-skill-memory-meditation-*` skills via prefix matching — no additional prefix entry was needed.

**install.py — fallback list**
Added the agent path and all six skill `SKILL.md` paths to the built-in fallback list returned when the dist manifest cannot be fetched from CDN. This mirrors the DIST_FILES list in `create-crux-zip.py`.

**scripts/create-crux-zip.py — DIST_FILES**
Appended the seven paths after the existing skill entries, maintaining the grouped ordering (agent block, then skills block).

**.crux/dist-manifest.json**
Edited directly (equivalent to running `python3 scripts/create-crux-zip.py` which regenerates it from DIST_FILES). The manifest now contains exactly 37 entries (30 prior + 7 new).

**.github/workflows/version-bump.yml — no change required**
The workflow reads `RELEASE_PATHS` from `.crux/dist-manifest.json` dynamically:
```yaml
RELEASE_PATHS=$(jq -r '.files[]' .crux/dist-manifest.json)
RELEASE_PATHS=$(echo "$RELEASE_PATHS" | sed 's|\(.cursor/skills/[^/]*/\).*|\1|' | sort -u)
```
The `sed` collapses skill paths to parent-directory form, so all six `.cursor/skills/crux-skill-memory-meditation-*/` directories are automatically covered once the manifest is updated. The agent path `.cursor/agents/crux-cursor-meditation-guide.md` is covered by exact path match. **No hand-edit of the workflow file was required.**

**Source rule files — no change required**
Scanned `.cursor/rules/crux-memories-integration.md` — `/crux-meditate` remains in the explicit-command list. The rule does not name a specific agent for meditate, so no update needed. `docs-sync.md` source patterns did not need updating. No other rule source files reference meditate agent architecture directly.

**Cross-repo consistency check**
`crux-cursor-memory-manager` in a meditate context: S07 already replaced all meditate sections with pointer paragraphs. No leftover references found outside historical/spec files.

**Parse/syntax checks**
- `python -c "import install"` → clean
- `python -m py_compile scripts/create-crux-zip.py` → clean
- `ReadLints` on all modified files → no errors

### Deliverable Checklist (D01–D07 + DoD)

- [x] D01 — `install.py` enumerates agent + 6 skills
- [x] D02 — `create-crux-zip.py` DIST_FILES: agent + exactly 6 skill paths
- [x] D03 — `.crux/dist-manifest.json` updated (37 entries)
- [x] D04 — `version-bump.yml`: manifest-derived prefix matching covers all 7 new paths (no edit needed)
- [x] D05 — Source rule files checked; no update required
- [x] D06 — No `.crux.md` / `.crux.mdc` files edited
- [x] D07 — Parse checks recorded above
- [x] DoD: 7 new paths enumerated across install + zip + manifest; lints clean; version-bump.yml confirmed

### Blockers Encountered

**COORDINATION WARNING — S09 (CONTRIBUTORS.md)**
`subtask-09-meditate-decomp-docs-sync-20260517.status.yml` is still `state: pending`. CONTRIBUTORS.md does NOT yet contain entries for the new agent or six skills. S09 (docs-sync-agent) must add these entries before the spec-level DoD for DOD08 can be ticked. S10 takes no action on CONTRIBUTORS.md per scope boundaries.

### Files Modified
- `install.py` — MEMORY_FILE_PREFIXES (+1 entry) + fallback list (+7 entries)
- `scripts/create-crux-zip.py` — DIST_FILES (+7 entries)
- `.crux/dist-manifest.json` — files array (+7 entries, 30→37)
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-10-meditate-decomp-install-dist-release-20260517.status.yml`
- `specs/20260517-meditate-agent-skill-decomposition/status/subtask-10-meditate-decomp-install-dist-release-20260517.status.md`
- `specs/20260517-meditate-agent-skill-decomposition/status.yml`
