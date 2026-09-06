# Subtask: Split `crux-cursor-memory-manager` into mode-scoped thin agents + extract Canvas template

## Metadata
- **Subtask ID**: 05
- **Feature**: context-token-reduction
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 01, 04
- **Created**: 20260713

## Objective

Implement **Option 4** (split the monolithic 27.5-KB `crux-cursor-memory-manager.md` into five thin mode-scoped agents) plus the memory-manager half of **Option 6** (extract the ~80-line Canvas reference template out of the file so only Recall pays for it) from `analysis/context-token-reduction-report.md`.

This is the highest-consumer-impact subtask in the spec. `crux-cursor-memory-manager.md` is in `.crux/dist-manifest.json` and is invoked by every memory command consumers rely on (`/crux-dream`, `/crux-recall`, `/crux-remember`, `/crux-forget`, `/crux-meditate`). Follow **KD-3**: retain the umbrella file as a documented **temporary dispatcher/shim** so consumers with pre-spec installs continue working while the upgrade script (Subtask 09) re-points their setup.

## Deliverables Checklist

- [ ] **D01** — Create five thin mode-scoped agent files under `.cursor/agents/`:
  - `.cursor/agents/crux-memory-dream.md` — owns the Dream mode workflow (Steps 1–12 currently in memory-manager)
  - `.cursor/agents/crux-memory-rem.md` — owns the REM Sleep mode workflow
  - `.cursor/agents/crux-memory-recall.md` — owns Recall including the `--total` Canvas branch (see D02)
  - `.cursor/agents/crux-memory-remember.md` — owns the Remember mode workflow
  - `.cursor/agents/crux-memory-forget.md` — owns the Forget mode workflow

  Each thin agent MUST:
  - Carry a valid YAML frontmatter (`name`, `model`, `description`) that mirrors the current memory-manager's model choice.
  - Include the Subtask-01 lazy-CRUX + `context_manifest` honor blocks.
  - Point at `.cursor/skills/_memory-shared.md` (from Subtask 04) for config / Pattern A/B / Related.
  - Contain only the mode-specific workflow — no cross-mode boilerplate.
  - Include a `## Ownership` line naming the parent orchestrator (the corresponding `/crux-<mode>` command) and the delegated skills.
- [ ] **D02** — Handle the Canvas reference template (~80 lines currently inline at memory-manager L178–L242):
  - Move it into `.cursor/agents/templates/recall-canvas.tsx.md` (a plain-markdown data file, no frontmatter).
  - `crux-memory-recall.md` references it with a one-liner: "If invoked with `--total`, read `.cursor/agents/templates/recall-canvas.tsx.md` for the structural Canvas template."
  - No other thin agent references the template.
- [ ] **D03** — Rewrite `.cursor/agents/crux-cursor-memory-manager.md` as a documented **temporary dispatcher/shim**:
  - Reduce body to ≤ 60 lines.
  - Content: a one-paragraph BC notice, a table mapping each mode to its thin-agent successor, and a routing rule: "If your task is `<mode>`, prefer spawning `<thin-agent>` directly. This umbrella is retained for pre-upgrade installs and will be removed after one minor release once thin agents ship in the dist zip."
  - Add a top-of-file HTML comment (no spec ids — hygiene Rule 1): `<!-- DEPRECATED dispatcher — prefer crux-memory-* thin agents. Do not add new behavior here; extend the appropriate thin agent. Remove after one minor release once thin agents ship in dist. -->`
  - Preserve YAML frontmatter so Cursor still resolves the name; note the deprecation in the `description` field text so IDE tooltips surface it.
- [ ] **D04** — Re-point every in-repo caller to the new thin agents (**same change set**, no dual-path):
  - `.cursor/commands/crux-dream.md` → spawns `crux-memory-dream`
  - `.cursor/commands/crux-recall.md` → spawns `crux-memory-recall`
  - `.cursor/commands/crux-remember.md` → spawns `crux-memory-remember`
  - `.cursor/commands/crux-forget.md` → spawns `crux-memory-forget`
  - `.cursor/commands/crux-meditate.md` → continues to spawn `crux-cursor-meditation-guide` (unchanged). Any incidental memory-lifecycle callouts inside the meditate command that reference memory-manager should point at the appropriate thin agent.
  - `.cursor/agents/crux-cursor-meditation-guide.md` — if it references memory-manager for a lifecycle op, re-point to the correct thin agent.
- [ ] **D05** — Update `AGENTS.md` `<CRUX agents="always">` block:
  - Add rows to the `Available Agents` table for each new thin agent.
  - Keep the `crux-cursor-memory-manager` row but annotate as "(deprecated dispatcher — see `crux-memory-*`; remove after one minor release once thin agents ship in dist)".
  - Both the annotation and the new rows must remain **consumer-safe** (no repo-internal-only agents leak inside the `<CRUX>` block).
- [ ] **D06** — Update `AGENTS.md` `## Repository-Internal Agents (CRUX-Compress repo only)` **spec-execution allocation table** (line ~87 area) — the memory-lifecycle row currently reads "Memory lifecycle operations (dream, REM, recall) → crux-cursor-memory-manager". Change to enumerate the thin agents. This edit lives **outside** the `<CRUX>` block so it is not shipped to consumers, but it steers this repo's spec executor.
- [ ] **D07** — Coordinate with Subtask 04 to ensure the split thin agents reference `_memory-shared.md` correctly. If S04 has not yet completed at the time this subtask runs, the executor MUST block until S04 is verified per the dependency graph.
- [ ] **D08** — Record the following in the subtask's status `notes`:
  - Before/after token count for `crux-cursor-memory-manager.md` (target: ≤ 60 lines, ~700 tokens).
  - Token count for each new thin agent (target: ≤ 1.5K tokens each).
  - The **exact** `SOURCE_DIST_FILES` diff required for `scripts/create-crux-zip.py`: five new agent file paths + one new template file path, ordered as they should appear. Do **not** apply this diff — Subtask 09 aggregates it for user approval.
  - The consumer-side upgrade actions the follow-up upgrade script (Subtask 09) must perform (documented under `## Consumer Upgrade Steps` below).

## Definition of Done

- [ ] **DoD01** — Each thin agent file resolves to a valid Cursor agent (`rg -n "^name: crux-memory-" .cursor/agents/` returns five distinct names matching directory basenames).
- [ ] **DoD02** — `.cursor/agents/crux-cursor-memory-manager.md` is ≤ 60 lines and contains the deprecation banner and the dispatcher table.
- [ ] **DoD03** — Every in-repo caller (`.cursor/commands/crux-{dream,recall,remember,forget}.md` and any meditate references) spawns the correct thin agent by exact name — verify with `rg -n "crux-cursor-memory-manager" .cursor/commands/ .cursor/agents/` returning **zero non-deprecation matches** (only the umbrella file itself + deprecation notices in AGENTS.md and the umbrella's own body may contain the name).
- [ ] **DoD04** — `.cursor/agents/templates/recall-canvas.tsx.md` exists and is referenced only by `crux-memory-recall.md`.
- [ ] **DoD05** — AGENTS.md `<CRUX>` block table shows the five new thin agents plus the deprecation-annotated umbrella row. Consumers reading only the `<CRUX>` block can still find every memory operation.
- [ ] **DoD06** — `python3 scripts/create-crux-zip.py /tmp/crux-dryrun-s05` succeeds. The dry run will fail to include the new agent + template files (because `SOURCE_DIST_FILES` was not edited) — this is **expected**; the failure/omission is documented in the subtask notes and forwarded to Subtask 09 for user approval.
- [ ] **DoD07** — No linter errors introduced.
- [ ] **DoD08** — The Consumer Upgrade Steps section below is filled out with idempotent commands ready for Subtask 09 to fold into the aggregate upgrade script.
- [ ] **DoD09** — No dual-path forever shim beyond the umbrella dispatcher. Per `spec-implementation-hygiene.mdc` Rule 2, the umbrella is a scoped temporary exception documented here.

## Consumer Upgrade Steps

Idempotent, `--yes`-gateable steps for the follow-up upgrade script (Subtask 09) to fold into the aggregate `upgrade-context-token-reduction.sh`. Every step is safe to re-run; each terminates cleanly when its guard is already satisfied.

### 0 — Precondition detection

```sh
# Only run when the consumer has the monolithic umbrella and no thin agents yet.
if test -f .cursor/agents/crux/crux-cursor-memory-manager.md \
   && ! test -f .cursor/agents/crux/crux-memory-dream.md; then
  needs_split=1
else
  needs_split=0
fi
```

If `needs_split=0`, the upgrade script skips steps 1–4 for this concern and only re-checks step 5.

### 1 — Copy the five thin agents + Canvas template into place

Guarded copy from the dist zip (or the on-disk dist mirror after `install.py` extracts it). Consumer paths use the `crux/` subdirectory prefix (`.cursor/agents/crux/`) whereas the source repo uses `.cursor/agents/`; the dist-to-consumer path translation is handled by `install.py` per `to_crux_primitive_path()`.

```sh
mkdir -p .cursor/agents/crux/templates
for f in crux-memory-dream crux-memory-rem crux-memory-recall crux-memory-remember crux-memory-forget; do
  test -f ".cursor/agents/crux/${f}.md" || cp "${DIST_ROOT}/.cursor/agents/crux/${f}.md" ".cursor/agents/crux/${f}.md"
done
test -f .cursor/agents/crux/templates/recall-canvas.tsx.md \
  || cp "${DIST_ROOT}/.cursor/agents/crux/templates/recall-canvas.tsx.md" .cursor/agents/crux/templates/recall-canvas.tsx.md
```

### 2 — Rewrite the umbrella to the shim body

The dist zip ships the ≤60-line shim body for `.cursor/agents/crux/crux-cursor-memory-manager.md`. `install.py`'s normal file-copy pass overwrites the consumer's umbrella with the shim when the checksum differs. No dedicated step is required beyond the standard `python3 install.py` re-run (step 4).

### 3 — Re-point consumer callers that still name the umbrella

The dist zip's re-pointed commands (`.cursor/commands/crux/crux-{dream,recall,remember,forget}.md`) already spawn the thin agents by name. `install.py` overwrites the consumer's copies unless they were modified locally.

For consumer-custom commands or agents that reference `crux-cursor-memory-manager` outside the shipped dist surface, warn but do not auto-modify:

```sh
custom_hits=$(grep -RIl --include='*.md' 'crux-cursor-memory-manager' .cursor/ 2>/dev/null \
  | grep -v '/crux/crux-cursor-memory-manager.md$' \
  | grep -v '/crux/crux-cursor-meditation-guide.md$' \
  || true)
if [ -n "${custom_hits}" ]; then
  echo "WARN: the following files still reference crux-cursor-memory-manager by name."
  echo "      The umbrella dispatcher will keep working for one minor release, but you should"
  echo "      re-point these to the appropriate crux-memory-* thin agent."
  printf '  %s\n' ${custom_hits}
fi
```

### 4 — Reconcile the installer index

```sh
python3 install.py --yes
```

The installer maintains the checksum-aware manifest (`.crux/crux-release-files.json`) and copies the new thin agents / template alongside every other dist file.

### 5 — Post-upgrade sanity check (always run)

```sh
python3 install.py --verify --yes || {
  echo "ERROR: install.py --verify failed; investigate before proceeding."
  exit 1
}
```

Verify that `.cursor/agents/crux/crux-memory-{dream,rem,recall,remember,forget}.md` and `.cursor/agents/crux/templates/recall-canvas.tsx.md` exist and have non-zero size. Warn (do not fail) if the consumer's `.cursor/agents/crux/crux-cursor-memory-manager.md` was locally modified — instruct the user to reconcile so the shim body is in place before the next release removes the file.

## Implementation Notes

- **Dependencies**: This subtask depends on S01 (agent load prompts + `context_manifest` protocol are in final form) and S04 (`_memory-shared.md` exists so the thin agents can point at it). Do not start until both are marked verified.
- **File-write coordination**: This subtask edits `AGENTS.md` after S01 has landed. Re-read AGENTS.md fresh before editing to avoid stale merges. Do not touch the `<CRUX>` block wording that S01 owns — only add table rows and annotate the memory-manager row. Re-read memory **commands** after S04 (pointer/dedupe) and re-point spawn targets without removing `_memory-shared.md` pointers. Each thin agent must include Subtask-01 lazy-CRUX + `context_manifest` honor blocks (S01 does not edit the umbrella).
- **Consumer safety**: The five new thin agents + Canvas template are net-new files. Until `scripts/create-crux-zip.py` is updated (needs explicit user approval, Subtask 09 flags it), the dist zip will **not** include them. The umbrella dispatcher shim is what protects pre-upgrade-install consumers from breakage until they can upgrade.
- **Cursor path stability**: `.md` filenames are what Cursor resolves. Do not rename `crux-cursor-memory-manager.md` — retain the exact filename with the shim body.
- **No shim-forever**: `spec-implementation-hygiene.mdc` Rule 2 forbids indefinite backwards-compat layers. The umbrella dispatcher is a scoped exception per the same rule's spec-local-upgrade guidance. Document removal criteria (one minor release after thin agents ship in dist) without embedding a spec id.
- **Canvas template file**: has no frontmatter and no `name:` field. It is a plain data file that the Recall agent reads on the `--total` cold path only.

## Testing Strategy

**Do NOT trigger global test suites during parallel execution.** Instead:

- Read each thin agent end-to-end after writing — confirm no mode's workflow was lost.
- Read the umbrella shim to confirm every mode has a valid table entry pointing at the right thin agent.
- Verify caller re-pointing with `rg -c "crux-cursor-memory-manager" .cursor/commands/`.
- Full eval sweep + agent-name-resolution eval deferred to Subtask 08.

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

