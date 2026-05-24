# Subtask 10 - meditate-agent-skill-decomposition - live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 10 |
| feature | meditate-agent-skill-decomposition |
| assigned_agent | crux-software-engineer |
| model | claude-sonnet-4-6 |
| token_budget | 200000 |
| state | completed |
| started_at | 2026-05-24T06:07:00Z |
| last_heartbeat | 2026-05-24T06:09:26Z |
| completed_at | 2026-05-24T06:09:26Z |
| git_sha |  |
| agent_session_id |  |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
## Checklist

- [x] **D01** - install.py enumerates the new guide agent and six approved meditation skills
- [x] **D02** - scripts/create-crux-zip.py DIST_FILES includes the new guide agent and exactly six skill paths
- [x] **D03** - .crux/dist-manifest.json regenerated or updated to match dist file enumeration
- [x] **D04** - .github/workflows/version-bump.yml release paths cover the new shipped paths where applicable
- [x] **D05** - Source rule files updated only if they directly reference meditate agent architecture
- [x] **D06** - No generated .crux.md or .crux.mdc files are hand-edited
- [x] **D07** - Targeted parse checks for install.py and create-crux-zip.py recorded
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
## Artifacts

- `install.py` — Added `crux-cursor-meditation-guide.md` to `MEMORY_FILE_PREFIXES`; added agent + 6 skill paths to fallback list
- `scripts/create-crux-zip.py` — Added 7 new paths to `DIST_FILES` (agent + 6 meditation skills)
- `.crux/dist-manifest.json` — Updated with 7 new paths matching `DIST_FILES`
<!-- status:artifacts:end -->

<!-- status:errors:start -->
## Errors

_No errors._
<!-- status:errors:end -->

<!-- status:notes:start -->
version-bump.yml uses prefix matching derived from dist-manifest.json — no hand-edit required.
CONTRIBUTORS.md from S09 does NOT yet have the new entries (S09 state is still pending).
Coordination warning surfaced in subtask brief Execution Notes.
<!-- status:notes:end -->
