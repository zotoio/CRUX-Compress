# Subtask 07 — meditate-agent-skill-decomposition — live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 07 |
| feature | meditate-agent-skill-decomposition |
| assigned_agent | crux-software-engineer |
| model | claude-sonnet-4-6 |
| token_budget | 200000 |
| state | completed |
| started_at | 2026-05-24T06:00:00Z |
| last_heartbeat | 2026-05-24T06:05:00Z |
| completed_at | 2026-05-24T06:05:00Z |
| git_sha |  |
| agent_session_id |  |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
## Checklist

- [x] **D01** — For each section listed in subtask 02's "memory-manager trim plan", delete the section content and replace it with a pointer paragraph
- [x] **D02** — **Phases A–G research** — removed; pointer added.
- [x] **D03** — **Quick 6-step protocol** — removed; pointer added.
- [x] **D04** — **Ensemble Aggregation sub-mode** — removed; pointer added.
- [x] **D05** — **Adversarial Review sub-mode** — removed; pointer added.
- [x] **D06** — **Meditate-only invocation rows** in the agent's invocation table — removed
- [x] **D07** — **Meditate-only sections of the `Skills You Use` table** — retained only non-Meditate rows
- [x] **D08** — **Examples and prompts** that are Meditate-only — removed
- [x] **D09** — **Front-matter, persona prologue, generic `needs_user_input` envelope schema, Dream / REM / Recall / Remember / Forget sections** — preserved untouched.
- [x] **D10** — Verify that the memory-manager file is still a complete, self-consistent agent definition for its remaining lifecycle modes (Dream / REM / Recall / Remember / Forget).
- [x] **D11** — Verify the file no longer contains substrings: `Phases A–G research`, `Quick 6-step`, `Ensemble Aggregation` as a memory-manager mode, `Adversarial Review` as a memory-manager mode
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
## Artifacts

- `.cursor/agents/crux-cursor-memory-manager.md` — Trimmed from 1392 to 352 lines. Meditate Mode and Ensemble Aggregation Mode sections replaced with pointer paragraphs. Two expertise bullets deleted. Forget Mode preserved verbatim at lines 281–308.
<!-- status:artifacts:end -->

<!-- status:errors:start -->
## Errors

_No errors._
<!-- status:errors:end -->

<!-- status:notes:start -->
Completed successfully. File trimmed from 1392 to 352 lines (1040 lines removed).
`rg "meditat|crux-meditate"` returns exactly 2 matches — both pointer paragraphs.
ReadLints clean. Forget Mode preserved verbatim.
<!-- status:notes:end -->
