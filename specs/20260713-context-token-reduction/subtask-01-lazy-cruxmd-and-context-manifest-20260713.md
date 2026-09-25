# Subtask: Lazy `CRUX.md` load + `context_manifest` prelude protocol

## Metadata
- **Subtask ID**: 01
- **Feature**: context-token-reduction
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: None
- **Created**: 20260713

## Objective

Implement **Option 1** (lazy `CRUX.md` load) and **Option 5** (subagent `context_manifest` prelude) from `analysis/context-token-reduction-report.md`. Together these two changes remove the largest per-subagent context tax (a ~7K-token `CRUX.md` re-read plus AGENTS.md re-read on every spawn) by (a) restricting the unconditional load to agents that actually manipulate CRUX notation and (b) adding a promise-based manifest a parent can pass to skip redundant loads.

Both changes are **prose-only** and **additive**. Consumers see no path change; the fallback path (subagent loads per prompt when no manifest is provided) is preserved.

## Deliverables Checklist

- [x] **D01** — Update `AGENTS.md` `<CRUX agents="always">` block:
  - Retarget the **preamble** sentence that currently says load `CRUX.md` if not already loaded, plus foundational rule #1, so both say: interpret CRUX rules already in context; load `CRUX.md` only when the current work touches CRUX notation (compressing, decompressing, authoring, or validating). Preserve rule numbering. (Today rule #1 already emphasises interpreting in-context rules — do not invent a false "was unconditional" story; align preamble + rule #1.)
  - Add a new subsection titled **`context_manifest` — Subagent Prelude** documenting the JSON stanza schema (see D02), the parent's contract, and the subagent's fallback rule. Keep it inside the `<CRUX>` block (consumer-shipped).
- [x] **D02** — Document the `context_manifest` schema in AGENTS.md:
  ```json
  {
    "context_manifest": {
      "agents_md": "loaded" | "not_loaded",
      "crux_md":   "loaded" | "not_loaded",
      "memory_config": {
        "path": ".crux/crux-memories.json",
        "loaded": true|false,
        "flags": { "enableMemories": "true"|"false", "enableMemoryCompression": "true"|"false" }
      },
      "extras": { "<well-known-key>": "loaded"|"not_loaded"|<compact-value> }
    }
  }
  ```
  Include: (a) sentinel probe — subagents that cannot recall a known phrase from `AGENTS.md` MUST re-load it, and (b) fallback rule — absence of the stanza means today's behavior.
- [x] **D03** — Strip any unconditional / early-mandatory `Read CRUX.md` (or paraphrase) from agents that do not need it for every task:
  - `.cursor/agents/crux-platform-architect.md` (has unconditional Read today)
  - `.cursor/agents/crux-software-engineer.md` (has unconditional Read today)
  - `.cursor/agents/integrity-expert.md` (soft "Read AGENTS.md and CRUX.md if not already loaded" — replace with the same conditional two-liner)
  - `.cursor/agents/docs-sync-agent.md` (no unconditional Read today — add the conditional two-liner + `context_manifest` honor block only; do not invent a removal)

  Replace / standardise with:
  > If your task involves compressing, decompressing, authoring, or validating CRUX notation, read `CRUX.md`. Otherwise rely on `_CRUX-RULE.mdc` and the CRUX block in `AGENTS.md` for symbol-aware behavior.
- [x] **D04** — In `.cursor/agents/crux-cursor-meditation-guide.md` only, replace the unconditional `Read CRUX.md` block with:
  > Read `CRUX.md` only if you will read or write compressed memory bodies (`.memory.crux.md`), citation blocks, or any file whose contents are CRUX-notated. Otherwise `_CRUX-RULE.mdc` provides the symbol primer you need.

  **Do not edit** `.cursor/agents/crux-cursor-memory-manager.md` in this subtask — Subtask 05 owns that file (split + shim) and will apply the same lazy-CRUX + `context_manifest` blocks to each new thin agent.
- [x] **D05** — Keep the unconditional `Read CRUX.md` line in `.cursor/agents/crux-cursor-rule-manager.md` unchanged. Add one sentence noting the manifest contract: "If your task prompt includes `context_manifest.crux_md === "loaded"`, skip the re-read."
- [x] **D06** — In every agent file this subtask edits (D03 + D04 + D05), insert a short "Honor `context_manifest`" section immediately after the load-context block:
  > Before reading `AGENTS.md`, `CRUX.md`, or `.crux/crux-memories.json`, check your task prompt for a `context_manifest` stanza. If a file is marked `loaded`, do not re-read it. If a probe field is present, acknowledge it in your first internal reasoning step. If the stanza is missing entirely, fall back to unconditional loads as documented above.
- [x] **D07** — Update the `Available Agents` table in `AGENTS.md` **only if** wording touches CRUX-load behavior. Do not add new agents in this subtask (Subtask 05 owns that).
- [x] **D08** — Record the exact tokens saved per agent file (before/after `Read CRUX.md` block removed) in this subtask's status file `notes` — use `.cursor/skills/crux-utils/` for the estimation.

## Definition of Done

- [x] **DoD01** — `AGENTS.md` still passes the CRUX zip extraction check: `python3 scripts/create-crux-zip.py` (dry-run against `/tmp`) finds a well-formed `<CRUX>...</CRUX>` block and emits `AGENTS.crux.md` without warnings. Do **not** modify `scripts/create-crux-zip.py`.
- [x] **DoD02** — No agent file except `crux-cursor-rule-manager.md` contains the phrase "Before doing ANY work, you MUST read `CRUX.md`" (or paraphrase thereof) unconditionally. Verify with a `rg` sweep documented in the notes.
- [x] **DoD03** — Every agent file that was edited includes the `context_manifest` honor block and the conditional CRUX-load wording.
- [x] **DoD04** — Repo grep: `rg -n "context_manifest" .cursor/agents/ AGENTS.md` returns matches in every edited agent plus AGENTS.md.
- [x] **DoD05** — No lint errors introduced (`.cursor/agents/*.md` and `AGENTS.md`).
- [x] **DoD06** — No behavioral change is required of consumer projects — the AGENTS.md `<CRUX>` block edits remain semantically equivalent for anyone whose parent agent does not pass a manifest.

## Implementation Notes

- **File overlap with other Phase-1 subtasks**: This subtask edits `AGENTS.md` and agent files listed in D03–D05. It does **not** touch `crux-cursor-memory-manager.md` (Subtask 05 owns the split of that file — S05 is Phase 2 and depends on S01). Phase-1 sibling subtasks S02 (rules), S03 (`crux-compress.md`), S04 (skill + memory-command pointer edits), and S06 (`crux-test.md` + evals) touch disjoint files relative to this subtask's agent set. No merge conflicts expected.
- Per **KD-11**, do not weaken the always-on CRUX decompression primer when rewriting agent load prompts — agents may later receive CRUX bodies (Subtask 07) and must still decompress via `_CRUX-RULE.mdc` / AGENTS.md.
- The `context_manifest` stanza is **descriptive**, not schema-enforced — no JSON schema file yet. Follow-up spec may promote to a JSON schema under `.crux/schema/`. Do not create the schema file here.
- Do **not** write any code that reads the manifest. This is a prompt-protocol change. Enforcement lives in the LLM's obedience to the prompt.
- Preserve exact frontmatter (`name`, `model`, `description`) in every edited agent file — only the body prose changes.
- Consumer safety: the `<CRUX>` block in `AGENTS.md` is the only part shipped to consumers per `scripts/create-crux-zip.py` lines 227–242. Anything you write inside that block must make sense to a consumer whose agents inherit the CRUX block into their AGENTS.md but who does not have this repo's internal agents.
- Repo-internal agents (`crux-platform-architect`, `crux-software-engineer`, `integrity-expert`, `docs-sync-agent`) can be optimized aggressively — they are not shipped to consumers.

## Testing Strategy

**Do NOT trigger global test suites during parallel execution.** Instead:

- Manually spot-check by reading each edited agent file end-to-end after your edits.
- Run `python3 scripts/create-crux-zip.py /tmp/crux-dryrun` to verify the AGENTS.md `<CRUX>` extraction still succeeds. Delete `/tmp/crux-dryrun/*.zip` after.
- Run `rg -c "Before doing ANY work" .cursor/agents/` — expect the total match count to drop to 1 (only `crux-cursor-rule-manager.md`).
- Any comprehensive eval (`python3 scripts/test.py`, `evals/`) is deferred to Subtask 08.

## Execution Notes

### Agent Session Info
- Agent: `crux-platform-architect`
- Started: 2026-07-13 (heartbeat: started_at recorded in `.status.yml`)
- Completed: 2026-07-13 (completed_at recorded in `.status.yml`)

### Work Log

1. Read the subtask spec, the current `AGENTS.md`, and every agent file listed in D03–D05 to establish the baseline.
2. Measured baseline token counts for `AGENTS.md`, `CRUX.md`, and every edited agent file via `crux-utils --token-count`.
3. **D01 + D02** — Rewrote the `<CRUX agents="always">` preamble and foundational rule #1 in `AGENTS.md` to say "interpret CRUX rules already in context; load `CRUX.md` only when the current work touches CRUX notation." Added a new `### context_manifest — Subagent Prelude` subsection inside the `<CRUX>` block with the full JSON schema (agents_md, crux_md, memory_config w/ flags, extras), sentinel probe rule, fallback rule for absence, producer/consumer contracts, and a note that this is a descriptive prompt protocol (not a JSON schema file).
4. **D03** — Stripped the "Before doing ANY work, read `CRUX.md`" block from `crux-platform-architect.md`, `crux-software-engineer.md`, and `integrity-expert.md`. Replaced with the standardised conditional two-liner. In `crux-platform-architect.md` also updated the step-2 "Load relevant context" bullet in "When Invoked" so the workflow prose no longer instructs an unconditional CRUX.md read. Added the conditional two-liner + honor block to `docs-sync-agent.md` (which had no unconditional read to remove — spec explicitly said "add only, do not invent a removal").
5. **D04** — In `crux-cursor-meditation-guide.md` only, replaced the unconditional CRUX.md read with the verbatim spec-mandated conditional wording ("only if you will read or write compressed memory bodies … citation blocks, or any file whose contents are CRUX-notated"). Preserved the mandatory `.crux/crux-memories.json` read but made it manifest-honoring. Did NOT touch `crux-cursor-memory-manager.md` per spec (Subtask 05 owns that split).
6. **D05** — Kept the unconditional `Read CRUX.md` in `crux-cursor-rule-manager.md` intact. Added the required sentence: "If your task prompt includes `context_manifest.crux_md === "loaded"`, skip the re-read."
7. **D06** — Inserted a short `### Honor context_manifest` section immediately after the load-context block in every agent file this subtask edits (7 files: platform-architect, software-engineer, integrity-expert, docs-sync-agent, meditation-guide, rule-manager, plus the AGENTS.md-level protocol definition).
8. **D07** — Reviewed the `Available Agents` table in `AGENTS.md`. Row wording only describes agent purpose (compression, memory lifecycle, meditation) — none touches CRUX-load behavior. Per spec ("only if wording touches CRUX-load behavior"), no change required.
9. **D08** — Ran `crux-utils --token-count` on every edited file post-edit; computed deltas and per-spawn savings from lazy CRUX.md (7,341 tokens). Recorded in `.status.yml` notes.
10. **DoD01** — Ran `python3 scripts/create-crux-zip.py /tmp/crux-dryrun` — exit 0, `AGENTS.crux.md` produced (8,641 bytes) with no warnings; `<CRUX>` block extraction succeeded. Restored side-effect manifest writes (`.crux/crux-release-files.json`, `.crux/dist-manifest.json`) and cleaned `/tmp/crux-dryrun/*.zip`.
11. **DoD02** — `rg -c "Before doing ANY work" .cursor/agents/` → 2 matches: `crux-cursor-rule-manager.md` (kept per D05) and `crux-cursor-memory-manager.md` (owned by Subtask 05; explicitly excluded from this subtask). After S05 executes, the count drops to 1 as the Testing Strategy predicts.
12. **DoD03** — Verified via `rg -n "context_manifest"` sweep: every edited agent file has both a `### Honor context_manifest` heading and the conditional CRUX-load wording.
13. **DoD04** — `rg -n "context_manifest" .cursor/agents/ AGENTS.md` returns matches in AGENTS.md (7 lines) and each edited agent file. Verified.
14. **DoD05** — `ReadLints` on all 7 edited files → No linter errors found.
15. **DoD06** — Consumer safety: the fallback rule I added to AGENTS.md (`context_manifest` absent → today's behavior) preserves semantic equivalence for any consumer whose parent agent doesn't pass a manifest. The `<CRUX>` block edits are additive protocol documentation.

### Blockers Encountered
None. The stale checklist text in `.status.yml` (referencing `crux-cursor-memory-manager.md` under D04) was noted but did not block execution — I followed the authoritative subtask markdown text which explicitly excludes memory-manager and cites Subtask 05 as the owner.

### Files Modified
- `AGENTS.md` — Rewrote CRUX preamble + rule #1 for lazy loading; added `### context_manifest — Subagent Prelude` subsection with full schema, semantics, probe rule, fallback, and contracts (inside the shipped `<CRUX>` block).
- `.cursor/agents/crux-platform-architect.md` — Removed unconditional CRUX.md read; added conditional two-liner + `### Honor context_manifest` block; updated "When Invoked" step 2 to remove unconditional load prose.
- `.cursor/agents/crux-software-engineer.md` — Removed unconditional CRUX.md read; added conditional two-liner + `### Honor context_manifest` block.
- `.cursor/agents/integrity-expert.md` — Replaced soft "Read AGENTS.md and CRUX.md if not already loaded" with conditional two-liner + `### Honor context_manifest` block; updated "When Invoked" step 2 to point at the new Load Context section.
- `.cursor/agents/docs-sync-agent.md` — Added conditional two-liner + `### Honor context_manifest` block (no unconditional read existed to remove).
- `.cursor/agents/crux-cursor-meditation-guide.md` — Replaced unconditional CRUX.md read with the spec-mandated compressed-memory-conditional wording; wrapped `.crux/crux-memories.json` read with manifest-honoring caveat; added `### Honor context_manifest` block with `memory_config.flags` shortcut.
- `.cursor/agents/crux-cursor-rule-manager.md` — Kept unconditional CRUX.md load; appended one sentence noting manifest contract; added `### Honor context_manifest` block that documents the unconditional-in-absence-of-manifest exception for this agent.
- `specs/20260713-context-token-reduction/status/subtask-01-lazy-cruxmd-and-context-manifest-20260713.status.yml` — Ticked D01–D08; recorded token savings notes; set state=completed and completed_at.
- `specs/20260713-context-token-reduction/status/subtask-01-lazy-cruxmd-and-context-manifest-20260713.status.md` — Regenerated from yml via `spec-status-roundtrip md-from-yml`.
- `specs/20260713-context-token-reduction/subtask-01-lazy-cruxmd-and-context-manifest-20260713.md` — Ticked deliverables checklist and DoD; filled Execution Notes / Work Log / Files Modified.

Explicitly NOT modified (per spec):
- `.cursor/agents/crux-cursor-memory-manager.md` (Subtask 05 owns the split).
- `scripts/create-crux-zip.py` (explicit prohibition).
- `.crux/crux-release-files.json` / `.crux/dist-manifest.json` (side-effect writes from the DoD01 dry-run were reverted via `git checkout`).

