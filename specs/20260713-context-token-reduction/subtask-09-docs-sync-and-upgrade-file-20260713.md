# Subtask: Docs sync + spec-local upgrade file + dist-manifest additions summary

## Metadata
- **Subtask ID**: 09
- **Feature**: context-token-reduction
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 05, 07, 08
- **Created**: 20260713

## Objective

Close out the spec (Phase 5 — after Subtask 08):
1. Aggregate every per-subtask upgrade step into one idempotent, `--yes`-gated `upgrade-context-token-reduction.sh` in this spec directory (primary engineering deliverable).
2. Synchronize documentation per `docs-sync.crux.mdc` (README, CONTRIBUTORS, `web/compress.md/` where applicable) — surgical edits following the docs-sync protocol.
3. Produce a **Dist manifest additions — awaiting user approval** section in the execution report enumerating every new file (from Subtasks 03, 04, 05) that consumers need but that this spec explicitly did **not** add to `scripts/create-crux-zip.py`.
4. Note the version-bump obligation per `version-bump.crux.mdc` (minor bump — `feat`) in the commit description for the release commit.

## Deliverables Checklist

- [ ] **D01** — Aggregate upgrade script `specs/20260713-context-token-reduction/upgrade-context-token-reduction.sh`:
  - Idempotent, safe to re-run.
  - `--yes` gate for any destructive step; without `--yes` the script prints planned actions and exits 0.
  - Reads per-subtask `Consumer Upgrade Steps` sections (Subtask 05 defined one; extend if S03/S04/S07 flag any) and combines them in dependency order.
  - Steps to include at minimum:
    - Detect pre-upgrade install (monolithic `crux-cursor-memory-manager.md` present, thin agents absent).
    - Point out required manual steps if `scripts/create-crux-zip.py` has not yet been updated (i.e. the user has not yet approved the dist additions).
    - Regenerate the memory index using the **repo-local** path `python3 .cursor/skills/crux-skill-memory-index/scripts/memory-index.py`, noting that consumer installs may nest primitives under `.cursor/skills/crux/` after `install.py` — detect both layouts.
    - Re-run plain `python3 install.py` (there is **no** `install.py --repair` mode today — do not invent one).
  - Passes `bash -n` (syntax check) and produces sensible output on a dry-run.
- [ ] **D02** — Update `README.md` (surgical, per `docs-sync.crux.mdc`):
  - Add or refresh a "Context Token Reduction" note in the changelog / recent-updates section.
  - Point at `analysis/context-token-reduction-report.md` as the source of the initiative.
  - Reflect the new memory-agent split (Subtask 05) in any docs enumerating available agents.
- [ ] **D03** — Update `CONTRIBUTORS.md` (surgical, per `docs-sync.crux.mdc`):
  - Reflect the pytest-driven `/crux-test` (Subtask 06) in the CI / testing section.
  - Reflect the `context_manifest` protocol (Subtask 01) in any agent-authoring guide.
  - Reflect the memory-agent split (Subtask 05) in the agent registry / how-to sections.
- [ ] **D04** — Update `web/compress.md/` (or its landing content) if it enumerates agents, commands, or the memory surface. Keep changes surgical.
- [ ] **D05** — Produce a `Dist manifest additions — awaiting user approval` section in the execution report:
  - Enumerate every new file each subtask flagged (S03: `.cursor/commands/templates/compress-prompts.md`; S04: `.cursor/skills/_memory-shared.md`; S05: five thin agent files + Canvas template).
  - Include the exact `SOURCE_DIST_FILES` diff the user would need to apply to `scripts/create-crux-zip.py` (in order matching the current file's grouping conventions).
  - State clearly: **`scripts/create-crux-zip.py` was NOT modified by this spec.** The user must review and apply the diff at their discretion; the accompanying dist-zip version bump (`.crux/crux.json`) is done in the release commit, not by this spec.
- [ ] **D06** — Version bump note:
  - Add a sentence to the execution report: "Per `version-bump.crux.mdc`, this spec introduces a `feat` and requires a **minor** version bump to `.crux/crux.json` at the release commit."
  - Do **not** bump `.crux/crux.json` inside the spec — that is the release engineer's job at merge time.
- [ ] **D07** — Final execution-report file `specs/20260713-context-token-reduction/execution-report-context-token-reduction-20260713.md`:
  - Executive summary (what shipped, tokens saved).
  - Per-subtask status references (linking to `status/*.status.md`).
  - Baseline vs post-spec token-cost table (pulled from Subtask 08 D08's report fragment).
  - Deferred compressions (from Subtask 07 notes).
  - Dist manifest additions — awaiting user approval (from D05).
  - Version bump note (from D06).
  - Consumer upgrade instructions (link to `upgrade-context-token-reduction.sh` and to Subtask 05's Consumer Upgrade Steps).

## Definition of Done

- [ ] **DoD01** — `specs/20260713-context-token-reduction/upgrade-context-token-reduction.sh` exists, passes `bash -n`, and a `--dry-run` invocation prints planned actions without side effects.
- [ ] **DoD02** — README, CONTRIBUTORS, and any web docs touched are consistent with the post-spec repository state (no orphan references to the pre-split memory-manager or the old prose `/crux-test`).
- [ ] **DoD03** — The execution report enumerates every deferred/pending dist-manifest addition and clearly attributes it to the originating subtask.
- [ ] **DoD04** — Version bump note is present in the execution report and does **not** trigger a `.crux/crux.json` edit inside this spec.
- [ ] **DoD05** — `scripts/create-crux-zip.py` is **not** modified by this spec (verify with `git diff --stat scripts/create-crux-zip.py` — expect no changes).
- [ ] **DoD06** — Docs edits pass any repository lint or link-check tooling that runs in CI. No broken links.
- [ ] **DoD07** — Docs edits follow `docs-sync.crux.mdc` (surgical edits, ¬rewrite; format consistent; upd ver+paths+examples; +workflow|test→+tables/lists).

## Implementation Notes

- **Dependencies**: This subtask depends on Subtask 05 (agent split final), Subtask 07 (compression waves final, deferred list known), and Subtask 08 (baseline/post-spec measurement written). It is **Phase 5** — do not start until S08 is verified.
- **Agent assignment**: `crux-software-engineer` owns this subtask because D01 is a non-trivial bash upgrade script. D02–D04 still follow the `docs-sync.crux.mdc` protocol surgically (same constraints as `docs-sync-agent`).
- **Docs edits are surgical**: `docs-sync.crux.mdc` Γ.README / Γ.CONTRIBUTORS / Γ.web sections define exactly what belongs in each. Follow that protocol.
- **Zip protection**: the hard rule from `zip-contents-protection.crux.mdc` — do NOT auto-modify `scripts/create-crux-zip.py`. Aggregate the required additions and present them for user approval instead.
- **Upgrade script scope**: cover only actions a pre-upgrade install needs. Anything a fresh install would get automatically (via `install.py`) does not need to appear.
- **Test the upgrade script**: at minimum, `bash -n` syntax check plus a dry-run against a scratch copy of the repo (`mkdir /tmp/upgrade-scratch && cp -r .cursor .crux AGENTS.md /tmp/upgrade-scratch/ && cd /tmp/upgrade-scratch && bash specs/20260713-context-token-reduction/upgrade-context-token-reduction.sh --dry-run` — adapt paths as needed).
- **This subtask never modifies application runtime code** outside docs, the upgrade shell script, and the execution report.

## Testing Strategy

- `bash -n specs/20260713-context-token-reduction/upgrade-context-token-reduction.sh`
- Dry-run the upgrade script per the Implementation Notes.
- If the repo has a docs link-checker in `scripts/` or `.github/workflows/`, run it locally.
- No global test-suite invocation needed — Subtask 08 already ran the full suite.

## Execution Notes

_To be filled by executing agent._

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
_Agent adds notes here during execution._

### Blockers Encountered
_Any blockers or issues._

### Files Modified
_List of files changed._
