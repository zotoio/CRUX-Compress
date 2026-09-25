# Subtask: Stage CRUX-compress the largest agents / commands / skills

## Metadata
- **Subtask ID**: 07
- **Feature**: context-token-reduction
- **Assigned Subagent**: crux-cursor-rule-manager
- **Dependencies**: 01, 02, 03, 04, 05
- **Created**: 20260713

## Objective

Implement **Option 2** from `analysis/context-token-reduction-report.md`: use CRUX compression on the largest agents, commands, and skills, achieving ≤ 25% of source tokens per file with confidence ≥ 90%. Follow **KD-2** (approach (c)): keep the original `.md` path and frontmatter, replace only the **body** with `⟦CRUX:source⟧…⟧` notation so Cursor still resolves each primitive at its current path — no consumer-visible path change.

This subtask runs **after** all prose/extraction/split subtasks (S01–S06) have landed and been verified, so we compress the leanest possible source once.

## Compression Wave Order (priority top-down)

Wave 1 — largest primitives, highest per-spawn savings:
1. `.cursor/commands/crux-meditate.md` (~25K tokens today → target ~6K)
2. `.cursor/agents/crux-cursor-meditation-guide.md` (~10.8K → target ~2.7K)
3. `.cursor/commands/crux-compress.md` (post-S03 shape → target ≤ 25%)

Wave 2 — memory surface (post-S05 shape):
4. `.cursor/agents/crux-memory-dream.md`
5. `.cursor/agents/crux-memory-rem.md`
6. `.cursor/agents/crux-memory-recall.md`
7. `.cursor/agents/crux-memory-remember.md`
8. `.cursor/agents/crux-memory-forget.md`
9. `.cursor/agents/crux-cursor-memory-manager.md` (dispatcher shim — skip if ≤ 60 lines already; per S05 target it will be)

Wave 3 — meditation skills (largest first):
10. `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md` (~13K → target ~3.3K)
11. `.cursor/skills/crux-skill-memory-meditation-report/SKILL.md`
12. `.cursor/skills/crux-skill-memory-meditation-ensemble/SKILL.md`
13. `.cursor/skills/crux-skill-memory-meditation-coordination/SKILL.md`
14. `.cursor/skills/crux-skill-memory-meditation-review/SKILL.md`
15. `.cursor/skills/crux-skill-memory-meditation-quick/SKILL.md`

Wave 4 — remaining memory skills (post-S04 shape):
16. `.cursor/skills/crux-skill-memory-rebalance/SKILL.md`
17. `.cursor/skills/crux-skill-memory-extract/SKILL.md`
18. `.cursor/skills/crux-skill-memory-compress/SKILL.md`
19. `.cursor/skills/crux-skill-memory-reference-tracker/SKILL.md`
20. `.cursor/skills/crux-skill-memory-crud/SKILL.md`
21. `.cursor/skills/crux-skill-memory-index/SKILL.md`

Wave 5 — remaining agents / commands / skills:
22. `.cursor/agents/crux-cursor-rule-manager.md`
23. `.cursor/agents/integrity-expert.md`
24. `.cursor/agents/crux-platform-architect.md`
25. `.cursor/agents/crux-software-engineer.md`
26. `.cursor/agents/docs-sync-agent.md`
27. `.cursor/skills/crux-utils/SKILL.md`
28. `.cursor/commands/crux-dream.md`
29. `.cursor/commands/crux-recall.md`
30. `.cursor/commands/crux-forget.md`
31. `.cursor/commands/crux-remember.md`
32. `.cursor/commands/crux-amnesia.md`

**Explicitly skip**: `.cursor/commands/crux-test.md` (Subtask 06 rewrote it as a shim; do not compress).

## Deliverables Checklist

- [ ] **D01** — For each file in the wave order, apply the standard CRUX compression protocol owned by `crux-cursor-rule-manager` (see `CRUX.md`). Approach:
  1. Read source `.md`. Compute baseline token count.
  2. Draft CRUX body inside `⟦CRUX:source-filename …⟧` block.
  3. Preserve YAML frontmatter (`name`, `model`, `description`, `alwaysApply`, etc.) verbatim above the body. Per **KD-11**, if the owning agent no longer unconditionally loads `CRUX.md`, keep a short **plaintext bootstrap** line between frontmatter and the CRUX fence: "If this body is CRUX-notated and you cannot decompress it from always-on rules alone, read `CRUX.md` before interpreting the body."
  4. Compute post-compression token count and semantic-equivalence confidence.
  5. **Accept only if** confidence ≥ 90% AND compressed body ≤ 25% of source tokens (allowing 30% for prompt-heavy agent files if 25% cannot be reached safely — record deviation in notes).
  6. **Reject and revert** the file if either bar is missed; log the file in the subtask notes under `## Deferred Compressions` with the reason. Do not merge partial or low-confidence compressions.
- [ ] **D02** — After each file compression, run a quick self-verification pass:
  - Spot-check three semantic properties from the source (e.g. for an agent: mode names, delegation targets, key workflow steps) survive in the compressed form.
  - If any survives with reduced fidelity, revert and defer.
- [ ] **D03** — Retune any grep-style eval that matches natural-language phrases in a now-compressed file:
  - Enumerate matches with `rg -l "<phrase>" evals/` before compression.
  - After compression, update the eval's expected phrase to the compressed-form equivalent (or replace the phrase-grep with a semantic-property assertion delegated to Subtask 08).
- [ ] **D04** — Record per-file token savings and confidence in the subtask's status `notes`. Include a summary table (before / after / % saved / confidence).
- [ ] **D05** — Emit an aggregate "compression impact" section in the subtask notes covering:
  - Total tokens saved per single spec-execution pass (approximated using §1.2 workflow model from the analysis report).
  - Any file that was **deferred** (not compressed) with reason.
- [ ] **D06** — Flag any file whose compression required an update to `.crux/dist-manifest.json` (should be zero — approach (c) keeps paths stable — but confirm) for Subtask 09.

## Definition of Done

- [ ] **DoD01** — At minimum Wave 1 (crux-meditate, meditation-guide, crux-compress) is compressed and verified. Waves 2–5 are attempted in order; each accepted compression is verified; each deferred compression is documented.
- [ ] **DoD02** — Every accepted compression has confidence ≥ 90% and body ≤ 25% of source (or ≤ 30% with documented rationale).
- [ ] **DoD03** — Every file path in `.crux/dist-manifest.json` still exists and still resolves through Cursor's normal path (`.cursor/agents/<name>.md`, `.cursor/commands/<name>.md`, `.cursor/skills/<name>/SKILL.md`). No `.md` path renamed or deleted.
- [ ] **DoD04** — YAML frontmatter (`name`, `model`, `description`, `alwaysApply`, etc.) is byte-identical to the source frontmatter for every touched file (verify by diffing frontmatter only).
- [ ] **DoD05** — `python3 scripts/create-crux-zip.py /tmp/crux-dryrun-s07` succeeds and produces a zip with the same file list as pre-compression. Delete `/tmp/crux-dryrun-s07/*.zip` after.
- [ ] **DoD06** — Any eval that grep'd a now-compressed phrase either succeeds against the new form or has been noted for Subtask 08 to replace with a semantic-property assertion.
- [ ] **DoD07** — Subtask notes contain an explicit `## Deferred Compressions` list; empty is acceptable if all waves compressed cleanly.
- [ ] **DoD08** — `python3 scripts/test.py` passes after Wave 1, after Wave 2, and after the final wave (aligned with Testing Strategy — not after every individual file). If any accepted compression breaks tests, roll back that wave's broken file(s) and defer.
- [ ] **DoD09** — No linter errors introduced.
- [ ] **DoD10** — Every accepted approach-(c) compression that targets a lazy-CRUX agent includes the KD-11 plaintext bootstrap (or the agent still unconditionally loads `CRUX.md`).

## Implementation Notes

- **Dependencies**: This subtask depends on S01, S02, S03, S04, and S05 being verified. Do not start compression until each of those `.status.yml` files shows `state: completed` **and** `extra.judge.verdict: verified`. S06 is **not** a hard dependency — `.cursor/commands/crux-test.md` is Explicitly skip regardless of whether the pytest shim has landed.
- **Wave sequencing**: Each wave must complete + verify before the next starts. Within a wave, files may be compressed sequentially (this is a single-agent subtask; parallelism is not applicable here).
- **Roll-back policy**: prefer to defer than to force. A skipped compression is fine; a low-quality compression costs more than the tokens it saves.
- **Approach (c) reminder**: keep the file at its current `.md` path, keep frontmatter, replace body with `⟦CRUX:…⟧`. This is the same pattern already used by `.cursor/rules/docs-sync.crux.mdc` and other CRUX-compressed rules — but applied inside agent/command/skill `.md` files.
- **KD-11**: before accepting a compression, confirm `_CRUX-RULE.mdc` still carries the Decompression — CRITICAL primer (S02). If S02 stripped it, stop and escalate — do not ship unreadable CRUX bodies.
- **Consumer safety**: because approach (c) preserves paths, the dist manifest is unaffected. Consumer AGENTS.md, memory index, and command surface all continue to resolve. Consumer-side upgrade for this subtask is simply "receive the new file body when the next dist zip ships" — no explicit action.
- **Interaction with S05 shim**: `crux-cursor-memory-manager.md` after S05 is a small dispatcher (~60 lines). Do not compress a file already ≤ 60 lines — cost of compression outweighs savings and the CRUX layer would obscure the dispatcher's readability. Skip it in Wave 2 (item 9 above) and note the skip.

## Testing Strategy

**Do NOT run the full test suite after every individual file.** Instead:

- After Wave 1 completes, run `python3 scripts/test.py` once.
- After Wave 2 completes, run `python3 scripts/test.py` once.
- After the final wave, run `python3 scripts/test.py` end-to-end plus the pytest suite from Subtask 06 if present (`python3 scripts/run_crux_command_suite.py`); if S06 has not landed yet, skip that suite and note it for Subtask 08.
- Any failure after a wave: roll back the last wave's broken compression(s) and re-run tests to isolate.

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

