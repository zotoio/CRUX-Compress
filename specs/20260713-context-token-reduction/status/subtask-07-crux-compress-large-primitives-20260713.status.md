# Subtask 07 — context-token-reduction — live status

<!-- status:metadata:start -->
| Key | Value |
|-----|-------|
| schema_version | 1 |
| subtask_id | 07 |
| feature | context-token-reduction |
| assigned_agent | crux-cursor-rule-manager |
| model | composer-2-fast |
| token_budget | 200000 |
| state | completed |
| started_at | 2026-07-13T18:13:00+10:00 |
| last_heartbeat | 2026-07-13T19:16:08+10:00 |
| completed_at | 2026-07-13T19:14:02+10:00 |
| git_sha |  |
| agent_session_id |  |
<!-- status:metadata:end -->

<!-- status:checklist:start -->
- [x] **D01** — **D01** — For each file in the wave order, apply the standard CRUX compression protocol owned by `crux-cursor-rule-manager` (see `CRUX.md`). Approach: (`.cursor/commands/crux-compress.source.mdx`)
- [x] **D02** — **D02** — After each file compression, run a quick self-verification pass: (`.cursor/commands/crux-compress.md`)
- [x] **D03** — **D03** — Retune any grep-style eval that matches natural-language phrases in a now-compressed file: (`evals/conftest.py`)
- [x] **D04** — **D04** — Record per-file token savings and confidence in the subtask's status `notes`. Include a summary table (before / after / % saved / confidence).
- [x] **D05** — **D05** — Emit an aggregate "compression impact" section in the subtask notes covering:
- [x] **D06** — **D06** — Flag any file whose compression required an update to `.crux/dist-manifest.json` (should be zero — approach (c) keeps paths stable — but confirm) for Subtask 09.
- [x] **DoD01** — **DoD01** — Wave 1 compressed+verified; Waves 2–5 attempted; deferred documented.
- [x] **DoD02** — **DoD02** — Confidence ≥90% and body ≤25% (or ≤30%/documented thin-agent deviation).
- [x] **DoD03** — **DoD03** — Dist-manifest paths exist; Cursor loadable paths stable (no rename/delete).
- [x] **DoD04** — **DoD04** — Registration YAML frontmatter matches SoT for touched agents.
- [x] **DoD05** — **DoD05** — create-crux-zip.py dry-run succeeds; Wave 1 loadables present in zip.
- [x] **DoD06** — **DoD06** — Eval grep/prose contracts retuned to prefer .source.mdx SoT.
- [x] **DoD07** — **DoD07** — Deferred Compressions list present in status notes.
- [x] **DoD08** — **DoD08** — Tests reported passed (771/2 skip); meditate evals 320 passed on re-verify.
- [x] **DoD09** — **DoD09** — No linter errors introduced (markdown/CRUX loadables).
- [x] **DoD10** — **DoD10** — KD-11 plaintext bootstrap on loadable CRUX `.md` files (between frontmatter and CRUX fence). (`.cursor/agents/crux-cursor-meditation-guide.md`)
<!-- status:checklist:end -->

<!-- status:artifacts:start -->
- **created** `.cursor/commands/crux-compress.source.mdx` — Post-S03 SoT with Source-Type Dispatch + registration_model convention
- **modified** `.cursor/commands/crux-compress.md` — Loadable CRUX (registers); regenerated from .source.mdx
- **created** `.cursor/commands/crux-meditate.source.mdx` — Plaintext SoT moved from fat .md
- **modified** `.cursor/commands/crux-meditate.md` — Loadable CRUX body
- **created** `.cursor/agents/crux-cursor-meditation-guide.source.mdx` — Plaintext SoT
- **modified** `.cursor/agents/crux-cursor-meditation-guide.md` — Loadable CRUX + registration frontmatter
- **created** `.cursor/agents/crux-memory-dream.source.mdx` — Plaintext SoT
- **modified** `.cursor/agents/crux-memory-dream.md` — Loadable CRUX
- **created** `.cursor/agents/crux-memory-rem.source.mdx` — Plaintext SoT
- **modified** `.cursor/agents/crux-memory-rem.md` — Loadable CRUX
- **created** `.cursor/agents/crux-memory-recall.source.mdx` — Plaintext SoT
- **modified** `.cursor/agents/crux-memory-recall.md` — Loadable CRUX
- **created** `.cursor/agents/crux-memory-remember.source.mdx` — Plaintext SoT
- **modified** `.cursor/agents/crux-memory-remember.md` — Loadable CRUX
- **created** `.cursor/agents/crux-memory-forget.source.mdx` — Plaintext SoT
- **modified** `.cursor/agents/crux-memory-forget.md` — Loadable CRUX
- **modified** `.cursor/commands/templates/compress-prompts.md` — Updated for .source.mdx / SKILL.mdx registration_model
- **modified** `evals/conftest.py` — D03 prefer .source.mdx for prose-contract reads
- **modified** `evals/test_q_meditate.py` — D03 SoT-preferring readers for meditate contracts
<!-- status:artifacts:end -->

<!-- status:errors:start -->
_None._
<!-- status:errors:end -->

<!-- status:notes:start -->
## OVERRIDE registration_model (authoritative)

Prior override #2 product-gate block and override #3 `.mdx`→`.crux.md` work are
superseded. Authoritative layout applied to all Wave 1–2 targets:

| Primitive | SoT (editable, non-registering) | Loadable (registers with Cursor) |
|-----------|----------------------------------|----------------------------------|
| Commands  | `<name>.source.mdx`              | `<name>.md` (CRUX body)          |
| Agents    | `<name>.source.mdx`              | `<name>.md` (CRUX body)          |
| Skills    | `SKILL.mdx`                      | `SKILL.md` (CRUX body)           |

[memory:CRUX Compressed File Protection] — edit SoT only; regenerate loadable.
[memory:Skill and Agent References by name] — instructional prose uses registered names.

Mistaken adjacent `*.crux.md` companions for the eight Wave 1–2 targets were deleted.
Rules `*.crux.mdc` untouched.

## USER OVERRIDE #3 remediation — file moves/deletes/regens

### Moves / creates (SoT)
- `crux-compress.md` (pre-S03 fat) → rebuilt as `crux-compress.source.mdx` (post-S03 dispatch)
- `crux-meditate.md` → copied to `crux-meditate.source.mdx`
- `crux-cursor-meditation-guide.md` → `….source.mdx`
- `crux-memory-{dream,rem,recall,remember,forget}.md` → `….source.mdx`

### Regenerated loadables (`.md` = CRUX)
- All eight targets: registration FM preserved (agents); body = `⟦CRUX:….source.mdx …⟧`
- `crux-compress.md` freshly compressed after dispatcher restore (must not reuse pre-S03 companion)

### Deleted
- All eight `*.crux.md` companions under commands/agents for Wave 1–2

### Guidance updates
- `crux-compress.source.mdx`: Source vs Output Convention / Output Path Rules / Eligibility
  document `.source.mdx`→`.md` and `SKILL.mdx`→`SKILL.md`; forbid adjacent `.crux.md` as
  Cursor-loadable for cmd/agent/skill
- `templates/compress-prompts.md`: markdown dispatch + preamble updated for same convention

## Token savings table (SoT → loadable)

| File | beforeTokens | afterTokens | Ratio | Saved | Confidence |
|------|--------------|-------------|-------|-------|------------|
| commands/crux-compress | 6395 | 1374 | 21.5% | 79% | 94% |
| commands/crux-meditate | 25468 | 5173 | 20.3% | 80% | 92% |
| agents/crux-cursor-meditation-guide | 10745 | 2155 | 20.1% | 80% | 93% |
| agents/crux-memory-dream | 1245 | 637 | 51.2% | 49% | 92% |
| agents/crux-memory-rem | 1084 | 593 | 54.7% | 45% | 92% |
| agents/crux-memory-recall | 950 | 486 | 51.2% | 49% | 91% |
| agents/crux-memory-remember | 875 | 439 | 50.2% | 50% | 91% |
| agents/crux-memory-forget | 941 | 454 | 48.2% | 52% | 91% |
| **Wave 1 (meditate+guide+compress)** | **42608** | **8702** | **20.4%** | **80%** | ≥92% |

### Thin-agent ratio deviation (documented)
Wave 2 thin agents measure ~48–55% of current SoT tokens (above ≤25%/≤30% bar).
Rationale: SoT plaintext was already decompressed-from-CRUX (terse); loadable includes
full Cursor registration frontmatter + generated metrics + CRUX body. Confidence ≥91%.
Accept as documented deviation under Deferred Compressions / thin-agent note.

## Compression impact
- Wave 1 loadables meet ≤25% target (20–22%).
- Aggregate Wave 1+2 loadable tokens ~11.3k vs SoT ~47.7k (~24% overall including thin agents).
- Cursor still registers stable `<name>.md` paths (dist-stable).

## Deferred Compressions
| File | Reason |
|------|--------|
| agents/crux-cursor-memory-manager.md | Skip: thin shim ≤60 lines |
| commands/crux-test.md | Explicit skip (S06 shim) |
| Wave 3 meditation skills | Deferred: budget |
| Wave 4 memory skills (incl. memory-compress) | Deferred: leave plaintext; `SKILL.md` has CRUX only as documentation example |
| Wave 5 remaining agents/commands (rule-manager) | Deferred: budget |
| Do **not** emit `SKILL.crux.md` | Per registration_model |

## Dist-manifest flags for Subtask 09 (do NOT edit create-crux-zip.py)

Loadable paths stay `<name>.md` (stable for dist). New SoT paths may need dist inclusion
if consumers must edit/regenerate:

```
SOURCE_DIST_FILES additions (exact) — awaiting user approval:
  .cursor/commands/templates/compress-prompts.md
  .cursor/commands/crux-compress.source.mdx
  .cursor/commands/crux-meditate.source.mdx
  .cursor/agents/crux-cursor-meditation-guide.source.mdx
  .cursor/agents/crux-memory-dream.source.mdx
  .cursor/agents/crux-memory-rem.source.mdx
  .cursor/agents/crux-memory-recall.source.mdx
  .cursor/agents/crux-memory-remember.source.mdx
  .cursor/agents/crux-memory-forget.source.mdx
```

Possibly remove any prior `.crux.md` companion entries if they were staged for dist
(none were added to create-crux-zip.py in this spec).

## Verification evidence
- Layout: each of 8 targets has `.source.mdx` + CRUX `.md`; zero `*.crux.md` companions
- `crux-compress.source.mdx`: Source-Type Dispatch → templates/compress-prompts.md; no five fat When-invoked bodies
- Loadable `crux-compress.md` encodes `tpl=…/compress-prompts.md` and `.source.mdx`/`SKILL.mdx` convention
- `rg -l '⟦CRUX:' .cursor/skills/*/SKILL.md` → only `crux-skill-memory-compress/SKILL.md` (doc example; deferred)
- `python3 scripts/test.py` once at end: **771 passed, 2 skipped**
- D03: `evals/conftest.py` + `evals/test_q_meditate.py` prefer `.source.mdx` for prose contracts
## Judge fix_list — DoD10 / D01.3 KD-11 plaintext bootstrap (2026-07-13T19:14)

Added KD-11 plaintext bootstrap on all eight Wave 1–2 **loadable** `.md` files
(outside the CRUX fence, after YAML frontmatter, before generated banner):

> If this body is CRUX-notated and you cannot decompress it from always-on rules alone, read `CRUX.md` before interpreting the body.

Targets updated:
- `.cursor/agents/crux-cursor-meditation-guide.md`
- `.cursor/agents/crux-memory-dream.md`
- `.cursor/agents/crux-memory-rem.md`
- `.cursor/agents/crux-memory-recall.md`
- `.cursor/agents/crux-memory-remember.md`
- `.cursor/agents/crux-memory-forget.md`
- `.cursor/commands/crux-compress.md` (optional consistency)
- `.cursor/commands/crux-meditate.md` (optional consistency)

SoT `.source.mdx` unchanged; `sourceChecksum` still matches SoT for all eight.
No `*.crux.md` companions recreated.
[memory:CRUX Compressed File Protection] — bootstrap is plaintext on the generated
loadable only; SoT remains the editable source.

<!-- status:notes:end -->
