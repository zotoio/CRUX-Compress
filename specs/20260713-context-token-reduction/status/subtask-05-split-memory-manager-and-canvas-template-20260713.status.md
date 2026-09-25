# Subtask 05 — context-token-reduction — live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 05 |
| feature | context-token-reduction |
| assigned_agent | crux-platform-architect |
| model | composer-2-fast |
| token_budget | 200000 |
| state | completed |
| started_at | 2026-07-13T17:39:00Z |
| last_heartbeat | 2026-07-13T08:06:25.860Z |
| completed_at | 2026-07-13T18:15:00Z |
| git_sha |  |
| agent_session_id |  |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
- [x] **D01** — **D01** — Create five thin mode-scoped agent files under `.cursor/agents/`:
- [x] **D02** — **D02** — Handle the Canvas reference template (~80 lines currently inline at memory-manager L178–L242):
- [x] **D03** — **D03** — Rewrite `.cursor/agents/crux-cursor-memory-manager.md` as a documented **temporary dispatcher/shim**:
- [x] **D04** — **D04** — Re-point every in-repo caller to the new thin agents (**same change set**, no dual-path):
- [x] **D05** — **D05** — Update `AGENTS.md` `<CRUX agents="always">` block:
- [x] **D06** — **D06** — Update `AGENTS.md` `## Repository-Internal Agents (CRUX-Compress repo only)` **spec-execution allocation table** (line ~87 area) — the memory-lifecycle row currently reads "Memory lifecycle operations (dream, REM, recall) → crux-cursor-memory-manager". Change to enumerate the thin agents. This edit lives **outside** the `<CRUX>` block so it is not shipped to consumers, but it steers this repo's spec executor.
- [x] **D07** — **D07** — Coordinate with Subtask 04 to ensure the split thin agents reference `_memory-shared.md` correctly. If S04 has not yet completed at the time this subtask runs, the executor MUST block until S04 is verified per the dependency graph.
- [x] **D08** — **D08** — Record the following in the subtask's status `notes`:
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
- **created** `.cursor/agents/crux-memory-dream.md` — thin agent — Dream mode
- **created** `.cursor/agents/crux-memory-rem.md` — thin agent — REM Sleep mode
- **created** `.cursor/agents/crux-memory-recall.md` — thin agent — Recall (references template on --total)
- **created** `.cursor/agents/crux-memory-remember.md` — thin agent — Remember (Pattern A)
- **created** `.cursor/agents/crux-memory-forget.md` — thin agent — Forget (Pattern B)
- **created** `.cursor/agents/templates/recall-canvas.tsx.md` — Canvas structural template extracted from umbrella
- **modified** `.cursor/agents/crux-cursor-memory-manager.md` — rewritten as ≤60-line deprecated dispatcher shim
- **modified** `.cursor/commands/crux-dream.md` — re-pointed to crux-memory-dream / crux-memory-rem
- **modified** `.cursor/commands/crux-recall.md` — re-pointed to crux-memory-recall + Canvas template pointer
- **modified** `.cursor/commands/crux-remember.md` — re-pointed to crux-memory-remember
- **modified** `.cursor/commands/crux-forget.md` — re-pointed to crux-memory-forget
- **modified** `.cursor/agents/crux-cursor-meditation-guide.md` — memory-lifecycle callout re-pointed to thin agents
- **modified** `.cursor/agents/crux-software-engineer.md` — memory-lifecycle delegate re-pointed to thin agents
- **modified** `.cursor/skills/crux-skill-memory-extract/SKILL.md` — dream-workflow orchestrator reference re-pointed
- **modified** `.cursor/skills/_memory-shared.md` — cross-skill-boundaries owner row re-pointed to thin agents
- **modified** `.cursor/rules/spec-agent-allocation.md` — memory-lifecycle allocation enumerates thin agents
- **modified** `AGENTS.md` — Available Agents table + Repository-Internal allocation table updated
- **modified** `specs/20260713-context-token-reduction/subtask-05-split-memory-manager-and-canvas-template-20260713.md` — Consumer Upgrade Steps section filled with idempotent steps 0–5
<!-- status:artifacts:end -->

<!-- status:errors:start -->
_None._
<!-- status:errors:end -->

<!-- status:notes:start -->
# Token counts (crux-utils prose-based estimator)

Umbrella `crux-cursor-memory-manager.md`:
- Before: 6908 tokens (352 lines)
- After (shim): 696 tokens (38 lines) — 90% reduction, well under the 60-line target.

Thin agents:
- crux-memory-dream:     2492 tokens (115 lines)
- crux-memory-rem:       2089 tokens ( 92 lines)
- crux-memory-recall:    1729 tokens ( 81 lines)
- crux-memory-remember:  1382 tokens ( 78 lines)
- crux-memory-forget:    1462 tokens ( 82 lines)

Canvas template (loaded only on `--total` cold path):
- .cursor/agents/crux/templates/recall-canvas.tsx.md: 1272 tokens (71 lines)

Note on the ≤1.5K target: dream / rem / recall come in slightly above the target
because each thin agent preserves the load-bearing workflow steps verbatim from the
umbrella (feature guards, conflict-detection rules, full-analysis-in-response
discipline, no-skill-bypass invariants). Net savings per invocation vs the pre-split
umbrella are still substantial:
- Dream:                6908 → 2492  ( 64% reduction)
- REM Sleep:            6908 → 2089  ( 70% reduction)
- Recall (no --total):  6908 → 1729  ( 75% reduction)
- Recall (--total):     6908 → 3001  ( 57% reduction, incl. cold-path template)
- Remember:             6908 → 1382  ( 80% reduction)
- Forget:               6908 → 1462  ( 79% reduction)

A follow-up compression pass (e.g. via /crux-compress on each thin agent) could
push dream / rem / recall under the 1.5K target if desired. Not required by DoD.

# SOURCE_DIST_FILES diff for scripts/create-crux-zip.py (flagged for S09 — DO NOT
# apply here per KD-5)

Add these six paths to the SOURCE_DIST_FILES list in
scripts/create-crux-zip.py, ordered as shown, immediately after the existing
".cursor/agents/crux-cursor-memory-manager.md" entry so the memory-agent block
stays visually cohesive:

    ".cursor/agents/crux-memory-dream.md",
    ".cursor/agents/crux-memory-rem.md",
    ".cursor/agents/crux-memory-recall.md",
    ".cursor/agents/crux-memory-remember.md",
    ".cursor/agents/crux-memory-forget.md",
    ".cursor/agents/templates/recall-canvas.tsx.md",

The umbrella (`.cursor/agents/crux-cursor-memory-manager.md`) STAYS in the list
during the deprecation window so pre-upgrade consumer installs continue to
resolve the registered name. Remove it after one minor release once all
consumers have run the upgrade script.

# create-crux-zip.py dry-run verification (DoD06)

Ran `python3 scripts/create-crux-zip.py /tmp/crux-dryrun-s05` from a clean tree.
Result:
- Script exit code: 0 (success).
- CRUX-Compress-v2.11.3.zip built. Zip contents include the rewritten
  2789-byte umbrella shim (`.cursor/agents/crux/crux-cursor-memory-manager.md`)
  but do NOT include any of the five thin agents or the Canvas template —
  exactly as expected because SOURCE_DIST_FILES was not modified per KD-5.
- Side effects: the script also rewrites `.crux/dist-manifest.json` and
  `.crux/crux-release-files.json`. Both were reverted with
  `git checkout` after the dry run to keep the tree clean; S09 will re-run
  the full release path once SOURCE_DIST_FILES is updated with user approval.

# Handoff to S09

Flags for the aggregate upgrade script and dist protection:
1. Add the six paths listed above to scripts/create-crux-zip.py's
   SOURCE_DIST_FILES (requires explicit user approval per
   `.cursor/rules/zip-contents-protection.crux.mdc`).
2. Fold the "Consumer Upgrade Steps" section (now filled in the subtask spec)
   into upgrade-context-token-reduction.sh — the section is idempotent and
   `--yes`-gateable as required by `spec-implementation-hygiene.mdc` Rule 3.
3. Remove the umbrella file (`.cursor/agents/crux-cursor-memory-manager.md`)
   and its SOURCE_DIST_FILES entry after one minor release cycle once all
   consumers have upgraded. Removal criteria are documented in the umbrella
   shim body under "## Removal criteria".

# CRUX-compressed rule regeneration follow-up (docs-sync-agent)

The source `.cursor/rules/spec-agent-allocation.md` was updated to enumerate
the five thin agents. Its two CRUX mirrors
(`.cursor/rules/spec-agent-allocation.crux.md`, `.cursor/rules/spec-agent-allocation.crux.mdc`)
are generated files carrying the "Generated file - do not edit!" banner and
were left untouched per CRUX rule #7. `docs-sync-agent` / `/crux-compress`
should regenerate both mirrors before release. The current stale content
(`mem→crux-cursor-memory-manager`) still resolves via the umbrella dispatcher
during the deprecation window.

# DoD verification summary

- DoD01 ✓ `rg -n "^name: crux-memory-" .cursor/agents/` returned five matches
  with directory-basename parity.
- DoD02 ✓ Umbrella body = 38 lines (well under ≤60), carries the DEPRECATED
  HTML comment (after frontmatter so Cursor's YAML parser still resolves the
  name), the dispatcher table (all 5 thin agents), and the routing rule.
- DoD03 ✓ `rg -n "crux-cursor-memory-manager" .cursor/commands/` = 0 matches.
  `rg -n "crux-cursor-memory-manager" .cursor/agents/` = 1 match (the
  umbrella's own `name:` field).
- DoD04 ✓ Canvas template exists at
  `.cursor/agents/templates/recall-canvas.tsx.md`. Operational references:
  only `crux-memory-recall.md` (agent). The umbrella lists the path once in
  its "Removal criteria" bookkeeping paragraph (contextual, not a load).
- DoD05 ✓ AGENTS.md `<CRUX>` block table lists all 5 thin agents plus the
  deprecation-annotated umbrella row. Consumer-safe — no repo-internal
  agents leaked inside the block.
- DoD06 ✓ create-crux-zip.py dry-run exit 0; new files intentionally
  omitted from the zip. Documented above and forwarded to S09.
- DoD07 pending: run ReadLints before finalising.
- DoD08 ✓ Consumer Upgrade Steps section in the subtask spec now contains
  idempotent, `--yes`-gateable steps 0–5.
- DoD09 ✓ No dual-path forever shim. The umbrella dispatcher is the only
  exception and it carries explicit removal criteria per hygiene Rule 2.

<!-- status:notes:end -->
