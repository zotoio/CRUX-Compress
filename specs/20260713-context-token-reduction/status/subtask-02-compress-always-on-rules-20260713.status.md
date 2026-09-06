# Subtask 02 — context-token-reduction — live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 02 |
| feature | context-token-reduction |
| assigned_agent | crux-cursor-rule-manager |
| model | composer-2-fast |
| token_budget | 200000 |
| state | completed |
| started_at | 2026-07-13T07:13:58.641Z |
| last_heartbeat | 2026-07-13T07:38:46Z |
| completed_at | 2026-07-13T07:27:57.470Z |
| git_sha |  |
| agent_session_id |  |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
- [x] **D01** — **D01** — CRUX-compress `.cursor/rules/spec-agent-allocation.md` following `CRUX.md`: (`.cursor/rules/spec-agent-allocation.crux.mdc`)
- [x] **D02** — **D02** — Slim `.cursor/rules/_CRUX-RULE.mdc` to remove content already present in `AGENTS.md` `<CRUX>` block: (`.cursor/rules/_CRUX-RULE.mdc`)
- [x] **D03** — **D03** — Reconcile `.cursor/rules/crux-memories-integration.md` (source) ↔ `.cursor/rules/crux-memories-mcp-context.mdc`: (`.cursor/rules/crux-memories-integration.crux.mdc`)
- [x] **D04** — **D04** — For each changed always-on rule, record before/after token counts in the subtask's status `notes` (use `.cursor/skills/crux-utils/scripts/crux-utils.py` for estimation).
- [x] **D05** — **D05** — Update `.crux/dist-manifest.json` **only if** an always-on-rule file was **deleted** — the dist manifest edit is a **flag** to raise in the status notes, not applied here. Do **not** modify `scripts/create-crux-zip.py`.
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
- **created** `.cursor/rules/spec-agent-allocation.crux.mdc` — New always-on CRUX rule (185 tokens measured)
- **created** `.cursor/rules/spec-agent-allocation.crux.md` — Canonical CRUX source
- **modified** `.cursor/rules/_CRUX-RULE.mdc` — Slimmed from 422 to 360 tokens; KD-11 CRITICAL sections retained
- **modified** `.cursor/rules/crux-memories-integration.md` — Merged MCP search guidelines into Discovery section
- **modified** `.cursor/rules/crux-memories-integration.crux.mdc` — Regenerated from updated source (492→510 tokens); confidence 94%; includes MCP CallMcpTool example
- **deleted** `.cursor/rules/crux-memories-mcp-context.mdc` — Content subsumed by integration rule
- **modified** `.cursor/rules/spec-agent-allocation.md` — Set alwaysApply false
<!-- status:artifacts:end -->

<!-- status:errors:start -->
_None._
<!-- status:errors:end -->

<!-- status:notes:start -->
## Token Deltas (D04, updated after fix_list pass)
| File | Before | After | Delta |
|------|--------|-------|-------|
| spec-agent-allocation.md (alwaysApply→false) | 366 | 0 | -366 |
| spec-agent-allocation.crux.mdc (new, alwaysApply:true) | 0 | 184 | +184 |
| _CRUX-RULE.mdc (slimmed) | 422 | 360 | -62 |
| crux-memories-mcp-context.mdc (deleted) | 406 | 0 | -406 |
| crux-memories-integration.crux.mdc (regenerated+MCP example) | 492 | 510 | +18 |
| **NET ALWAYS-ON** | **1686** | **1054** | **-632** |

## Dist-Manifest Flags (D05)
- crux-memories-mcp-context.mdc was NOT in dist-manifest — no change needed
- spec-agent-allocation.md was NOT in dist-manifest — no change needed
- spec-agent-allocation.crux.mdc is NOT a dist target (repo-internal rule) — no change needed
- crux-memories-integration.crux.mdc remains in dist-manifest (confirmed)
- _CRUX-RULE.mdc remains in dist-manifest (confirmed, slimmed in-place)
- No dist-manifest or create-crux-zip.py edits required by this subtask

## fix_list remediation (re-spawn pass)
- D03 confidence gate: Performed semantic validation; set confidence to 94% (crux-memories-integration) and 95% (spec-agent-allocation) — both ≥90%
- D01 sourceChecksum drift: Updated spec-agent-allocation.crux.md and .crux.mdc sourceChecksum from 2395065204 to 1501558077 (matches current source after alwaysApply flip)
- D03 MCP example (nice_to_have): Added one-liner CallMcpTool memory-search example to crux-memories-integration.md source, regenerated .crux.mdc (+26 tokens; net savings still -632, above ≥500 target)

<!-- status:notes:end -->
