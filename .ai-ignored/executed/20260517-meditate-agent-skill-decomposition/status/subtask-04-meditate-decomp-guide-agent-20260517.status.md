# Subtask 04 — meditate-agent-skill-decomposition — live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 04 |
| feature | meditate-agent-skill-decomposition |
| assigned_agent | crux-software-engineer |
| model | claude-sonnet-4-6 |
| token_budget | 200000 |
| state | completed |
| started_at | 2026-05-24T05:20:00Z |
| last_heartbeat | 2026-05-24T05:45:00Z |
| completed_at | 2026-05-24T05:45:00Z |
| git_sha | unstaged |
| agent_session_id | crux-software-engineer-s04 |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
## Checklist

- [x] **D01** — Create `.cursor/agents/crux-cursor-meditation-guide.md` with project-standard frontmatter
- [x] **D02** — **Persona prologue** ("You are the CRUX Meditation Guide…") with Load Context First, User Input Escalation, Your Expertise
- [x] **D03** — **Mode router**: dispatches inbound `Task` invocations via 8-row invocation table + theming/comprehensiveness abort rules
- [x] **D04** — **Phases A–G research workflow** (Research mode depth-0, steps 1–13 incl. 4b + 8b; Phases A–G pointer to skill:research)
- [x] **D05** — **Quick 6-step protocol** (`--quick`), warn-only citations, Quick substitution table
- [x] **D06** — **Ensemble Aggregation function**: aggregator workflow pointer, K10 layered cadence (steps 3b–3f) pointer to skill:ensemble
- [x] **D07** — **Adversarial Review function**: 13 dimensions pointer, severities, ≤3 iterations, MUST_FIX needs_user_input with mandatory context, Dim 13 respawn_required pointer
- [x] **D08** — **Skill load directives**: every sub-mode explicitly says "Read .cursor/skills/crux-skill-memory-meditation-{name}/SKILL.md"
- [x] **D09** — **`needs_user_input` envelope schema** with mandatory `context` field; "tree subagents NEVER call `AskQuestion`" Critical Rule
- [x] **D10** — **Subagent invocation contracts**: invocation variants table + spawn parameter summaries per mode
- [x] **D11** — **Coordination conventions pointer**: 18-row filename grammar + prefix-glob polling + retrospective + Branch & Leaf Index all delegated to skill:coordination
- [x] **D12** — **Mandatory report contract pointer**: paired HTML + PDF, anti-homogenisation, Universal Contrast, K10b Per-Cheap-Type Rendering Contract all delegated to skill:report
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
## Artifacts

| Path | Type | Description |
|------|------|-------------|
| `.cursor/agents/crux-cursor-meditation-guide.md` | agent | New meditation guide agent, 495 lines (≤500 budget) |
<!-- status:artifacts:end -->

<!-- status:errors:start -->
## Errors

_No errors._
<!-- status:errors:end -->

<!-- status:notes:start -->
Completed 2026-05-24. Agent file created at 495 lines — within the ≤500 line budget and well under the integrity-expert 550-line flag threshold. All 6 skills referenced exactly. comprehensiveness: invariant documented with canonical error string. K10 reflection function has its own mode-router section. Legacy additional_focus_areas_skipped / additional_focus_areas_accepted names absent. AskQuestion prohibition restated as Critical Rule. No verbatim Phases A–G, dimension lists, or schemas inlined — all delegated to skill files.
<!-- status:notes:end -->
