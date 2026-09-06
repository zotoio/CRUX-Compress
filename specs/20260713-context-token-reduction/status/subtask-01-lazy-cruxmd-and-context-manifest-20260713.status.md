# Subtask 01 — context-token-reduction — live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 01 |
| feature | context-token-reduction |
| assigned_agent | crux-platform-architect |
| model | composer-2-fast |
| token_budget | 200000 |
| state | completed |
| started_at | 2026-07-13T07:11:42.158Z |
| last_heartbeat | 2026-07-13T07:25:00.000Z |
| completed_at | 2026-07-13T07:18:37.880Z |
| git_sha |  |
| agent_session_id |  |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
- [x] **D01** — **D01** — Update `AGENTS.md` `<CRUX agents="always">` block:
- [x] **D02** — **D02** — Document the `context_manifest` schema in AGENTS.md:
- [x] **D03** — **D03** — Strip the unconditional `Read CRUX.md` block from:
- [x] **D04** — **D04** — In `.cursor/agents/crux-cursor-memory-manager.md` and `.cursor/agents/crux-cursor-meditation-guide.md`, replace the unconditional `Read CRUX.md` block with:
- [x] **D05** — **D05** — Keep the unconditional `Read CRUX.md` line in `.cursor/agents/crux-cursor-rule-manager.md` unchanged. Add one sentence noting the manifest contract: "If your task prompt includes `context_manifest.crux_md === "loaded"`, skip the re-read."
- [x] **D06** — **D06** — In every agent file above, insert a short "Honor `context_manifest`" section immediately after the load-context block:
- [x] **D07** — **D07** — Update the `Available Agents` table in `AGENTS.md` **only if** wording touches CRUX-load behavior. Do not add new agents in this subtask (Subtask 05 owns that).
- [x] **D08** — **D08** — Record the exact tokens saved per agent file (before/after `Read CRUX.md` block removed) in this subtask's status file `notes` — use `.cursor/skills/crux-utils/` for the estimation.
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
- **modified** `AGENTS.md` — Rewrote CRUX preamble + rule #1 for lazy loading; added context_manifest subagent-prelude section inside the shipped <CRUX> block.
- **modified** `.cursor/agents/crux-platform-architect.md` — Removed unconditional CRUX.md read; added conditional two-liner + Honor context_manifest block; updated 'When Invoked' step 2.
- **modified** `.cursor/agents/crux-software-engineer.md` — Removed unconditional CRUX.md read; added conditional two-liner + Honor context_manifest block.
- **modified** `.cursor/agents/integrity-expert.md` — Replaced soft AGENTS.md + CRUX.md read with conditional two-liner + Honor context_manifest block; updated 'When Invoked' step 2.
- **modified** `.cursor/agents/docs-sync-agent.md` — Added conditional two-liner + Honor context_manifest block (no unconditional read existed to remove).
- **modified** `.cursor/agents/crux-cursor-meditation-guide.md` — Replaced unconditional CRUX.md read with compressed-memory-conditional wording; wrapped .crux/crux-memories.json read with manifest-honoring caveat; added Honor context_manifest block.
- **modified** `.cursor/agents/crux-cursor-rule-manager.md` — Kept unconditional CRUX.md load; appended manifest-contract sentence; added Honor context_manifest block documenting unconditional-in-absence exception.
- **modified** `specs/20260713-context-token-reduction/subtask-01-lazy-cruxmd-and-context-manifest-20260713.md` — Ticked deliverables + DoD; filled Execution Notes / Work Log / Files Modified.
<!-- status:artifacts:end -->

<!-- status:errors:start -->
_None._
<!-- status:errors:end -->

<!-- status:notes:start -->
## D08 Token Estimation (crux-utils --token-count)

Baseline CRUX.md load cost (avoided per subagent spawn when the manifest marks it loaded or the
agent's task does not touch CRUX notation): **7,341 tokens**.

### Per-file token deltas (before edits → after edits)

| File | Before | After | Δ (agent-file growth) |
|------|-------:|------:|----------------------:|
| AGENTS.md                                          | 1,916  | 2,820  | +904  |
| .cursor/agents/crux-platform-architect.md          | 1,592  | 1,762  | +170  |
| .cursor/agents/crux-software-engineer.md           | 1,434  | 1,543  | +109  |
| .cursor/agents/integrity-expert.md                 | 1,612  | 1,799  | +187  |
| .cursor/agents/docs-sync-agent.md                  |   857  | 1,019  | +162  |
| .cursor/agents/crux-cursor-meditation-guide.md     | 10,745 | 10,922 | +177  |
| .cursor/agents/crux-cursor-rule-manager.md         | 5,175  | 5,342  | +167  |

Agent-file growth totals +1,876 tokens across 7 files (of which +904 lives in AGENTS.md and is
amortised across every subagent spawn because AGENTS.md is always-applied).

### Net per-spawn savings

The primary saving is CRUX.md load elimination for spawns whose task does not touch CRUX
notation (or whose parent asserts crux_md: "loaded" in the manifest). Per subagent:

| Agent | CRUX.md load skipped? | Prose growth | Net per-spawn Δ (tokens) |
|-------|-----------------------|-------------:|-------------------------:|
| crux-platform-architect  | Yes (conditional)     | +170 | -7,171 |
| crux-software-engineer   | Yes (conditional)     | +109 | -7,232 |
| integrity-expert         | Yes (conditional)     | +187 | -7,154 |
| docs-sync-agent          | Yes (already lazy)    | +162 | ~0 baseline; -7,179 when manifest sets crux_md: "loaded" |
| crux-cursor-meditation-guide | Yes (conditional) | +177 | -7,164 when meditation body isn't CRUX-notated |
| crux-cursor-rule-manager | No (unconditional)    | +167 | 0 baseline; -7,174 when manifest sets crux_md: "loaded" |

For a typical spec-execution scenario where the parent orchestrator spawns 4–8 subagents that
do NOT touch CRUX notation, expected savings per spec run: **~30,000–60,000 tokens**.
AGENTS.md growth (+904 tokens) is a one-time cost per session, not per-spawn.

## DoD Verification Evidence

- **DoD01** — `python3 scripts/create-crux-zip.py /tmp/crux-dryrun` → exit 0; AGENTS.crux.md
  produced (8,641 bytes); no warnings; <CRUX>...</CRUX> extraction succeeded. Side-effect writes
  to .crux/crux-release-files.json and .crux/dist-manifest.json reverted via git checkout.
- **DoD02** — `rg -c "Before doing ANY work" .cursor/agents/` returns 2 matches:
  crux-cursor-rule-manager.md (kept per D05) + crux-cursor-memory-manager.md (owned by S05;
  explicitly excluded from this subtask). Testing-Strategy prediction of "drop to 1" holds
  conditional on S05 executing later.
- **DoD03** — Every edited agent file contains both a `### Honor context_manifest` heading and
  the conditional CRUX-load wording (verified via `rg -n "context_manifest"` sweep).
- **DoD04** — `rg -n "context_manifest" .cursor/agents/ AGENTS.md` returns matches in AGENTS.md
  (7 lines) plus every edited agent file. Verified.
- **DoD05** — `ReadLints` on all 7 edited files → No linter errors found.
- **DoD06** — Fallback rule ("stanza absent → today's behavior") preserves semantic equivalence
  for consumers whose parent agent does not pass a manifest. <CRUX> block edits are additive
  protocol documentation; shipped AGENTS.crux.md extracts cleanly.

## Notes on D07
Available Agents table wording in AGENTS.md only describes agent purpose (compression, memory
lifecycle, meditation) — no row references CRUX-load behavior. Per spec ("only if wording
touches CRUX-load behavior"), no change required.

## Notes on stale checklist text
The D04 row in this .status.yml file was generated from an earlier draft that mentioned both
crux-cursor-memory-manager.md and crux-cursor-meditation-guide.md. The authoritative subtask
markdown explicitly forbids editing memory-manager (Subtask 05 owns that split + shim). This
execution followed the authoritative subtask markdown; memory-manager was NOT edited.

<!-- status:notes:end -->
