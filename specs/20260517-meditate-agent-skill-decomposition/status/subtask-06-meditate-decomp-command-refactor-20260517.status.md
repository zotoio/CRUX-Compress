# Subtask 06 — meditate-agent-skill-decomposition — live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 06 |
| feature | meditate-agent-skill-decomposition |
| assigned_agent | crux-software-engineer |
| model | claude-sonnet-4-6 |
| token_budget | 200000 |
| state | completed |
| started_at | 2026-05-24T05:55:00.000Z |
| last_heartbeat | 2026-05-24T06:20:00.000Z |
| completed_at | 2026-05-24T06:20:00.000Z |
| git_sha |  |
| agent_session_id |  |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
## Checklist

- [x] **D01** — Rewrite `.cursor/commands/crux-meditate.md` so that it contains only the calling-agent surface from the architecture-design doc
- [x] **D02** — Remove from the file any executable persona content that was moved to the agent or skill layer (Phases A–G prose, Quick 6-step prose, Ensemble Aggregation prose, Adversarial Review prose, mandatory report prose, retrospective prose) — replaced with pointer paragraphs
- [x] **D03** — Update every reference to `crux-cursor-memory-manager` (in the Meditate context) to `crux-cursor-meditation-guide`
- [x] **D04** — Preserve the workspace rule that **tree subagents NEVER call `AskQuestion`**; the coordinator (calling agent) is the only caller of `AskQuestion`
- [x] **D05** — Verify line-count reduction is meaningful: 2142 → 1020 lines (52% reduction, exceeds >=50% target)
- [x] **D06** — Markdown renders correctly; no broken anchor links; all 6 skill paths are valid relative paths to existing SKILL.md files
- [x] **D07** — Add deprecation banner to top of Meditate Mode section in `crux-cursor-memory-manager.md` (line 279)
- [x] **D08** — Spec status files updated to completed
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
## Artifacts

- `.cursor/commands/crux-meditate.md` — Refactored thin-coordinator command (1020 lines, down from 2142 = 52% reduction)
- `.cursor/agents/crux-cursor-memory-manager.md` — Deprecation banner added at top of Meditate Mode section (line 279)
<!-- status:artifacts:end -->

<!-- status:errors:start -->
## Errors

_No errors yet._
<!-- status:errors:end -->

<!-- status:notes:start -->
Completed 2026-05-24. crux-meditate.md refactored from 2142 to 1020 lines (52% reduction). All verbatim gates retained. All 6 skill paths referenced. spawn target updated to crux-cursor-meditation-guide. Deprecation banner added to memory-manager Meditate Mode section.
<!-- status:notes:end -->
