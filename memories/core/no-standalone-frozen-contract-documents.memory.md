---
id: "3761d27"
title: "No standalone frozen-contract documents; spec body's Current Behaviour section is the contract"
description: "Engineering specs do NOT produce standalone frozen-contract / frozen-surface / freeze-line documents. The spec's own 'Current Behaviour' / 'Background' section, together with a git SHA pinned at spec start, IS the contract baseline that subsequent subtasks (architecture, implementation, evals, integrity review) diff against. Integrity-review subtasks read CURRENT source files at the pinned SHA; regression evals provide the 'lose no functionality' guarantee."
type: "core"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260524-spec-conventions-refactor"
tags: [specs, conventions, contract-capture, integrity-review, freeze-docs, spec-hygiene]
---

# No standalone frozen-contract documents; spec body's Current Behaviour section is the contract

## Convention

Engineering specs under `specs/<spec-id>/` MUST NOT produce standalone freeze artefacts. Concretely, do not create:

- `*-frozen-contract-<date>.md`
- `*-frozen-surface-<date>.md`
- "freeze line" / "contract baseline" companion files
- Separate per-subtask freeze artefacts that mirror or supersede an earlier freeze

Instead, the spec's own **"Current Behaviour"** (a.k.a. "Background") section in `spec-<slug>-<date>.md`, together with the git SHA pinned at spec start, IS the authoritative contract baseline.

## What the freeze artefact used to do — and what replaces it

| Old (separate freeze artefact) | New (inline + tooling) |
|---|---|
| Verbatim capture of current prompts, modes, flags, schemas | "Current Behaviour" section in the spec body, sized to actual planning need |
| Source-of-truth concordance (line ranges in current files) | Pinned git SHA at spec start; integrity-review reads CURRENT source files at that SHA |
| "Lose no functionality" guarantee for refactors | Regression evals + integrity-review subtask diffing post-change source against the pinned SHA |
| Cross-spec coordination (sibling specs cite a larger freeze) | Sibling specs cite the parent spec's "Current Behaviour" section by anchor |
| Audit trail | Git history of the spec file + source files; both already versioned |

## Why

- **No duplication.** A verbatim capture in a separate file drifts the moment the source moves. The spec body and git history together are already authoritative.
- **Smaller spec surface.** A 1000+ line freeze file per spec is a heavyweight artefact whose maintenance cost (refresh, supersession banners, sibling-cite chains) exceeds its value.
- **Tooling-friendly.** Integrity-review subtasks can mechanically compare two git refs of the same source file; they don't need a hand-written concordance to do so.
- **Sibling-spec drift avoided.** When two specs touch the same surface concurrently, both reference the same primary sources at their respective SHAs rather than maintaining separate scoped freeze docs that must then cite each other.

## What the spec's "Current Behaviour" section should contain

- A prose description of the surface being changed (modes, flags, key user-facing prompts, schema fields).
- The **git SHA pinned at spec start**.
- Pointers (path + line range or section heading) into the relevant source files at that SHA — the spec body cites the source, it does not republish it.
- For sibling specs touching overlapping surfaces, a one-line cross-reference: "see `specs/<other-spec-id>/spec-<slug>-<date>.md` § Current Behaviour".
- Verbatim quotation only for items that are genuinely load-bearing for downstream subtasks (e.g. the exact wording of a user-facing gate prompt). Everything else is summarised.

## Anti-patterns

- Creating `<feature>-frozen-contract-<date>.md` or `<feature>-frozen-surface-<date>.md` in a new spec.
- Republishing thousands of lines of verbatim prompts and tables in a freeze file.
- Adding a supersession banner to a freeze file because a sibling spec landed mid-flight — refresh the parent spec's "Current Behaviour" section instead.
- Citing a freeze artefact from another spec; cite the other spec's body section.
- Producing a separate "Source-of-Truth Map" appendix concordance document; record per-item source pointers inline next to each item in "Current Behaviour".

## Grandfathering existing freeze artefacts

As of 2026-05-24, three freeze artefacts exist on disk:

- `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260517.md` (superseded by the 20260524 refresh).
- `specs/20260517-meditate-agent-skill-decomposition/meditate-frozen-contract-20260524.md` (active baseline for that spec's S06–S12).
- `specs/20260523-meditate-richness/meditate-richness-frozen-surface-20260523.md` (referenced by that spec's completed subtasks and execution report).

These are **grandfathered**: they remain in their parent spec directories until those specs archive to `.ai-ignored/executed/` per the normal spec lifecycle. Do NOT migrate or rewrite them; the `20260517` spec's remaining subtasks still consume the 2026-05-24 freeze, and rewriting in-flight DoD references would be more disruptive than letting the artefacts retire naturally.

## Promotion path

If the next 1–2 specs adopt the inline "Current Behaviour" pattern without regressing the "lose no functionality" guarantee, this memory should be promoted to a permanent rule under `.cursor/rules/` (most likely as a section in `spec-implementation-hygiene.mdc`) so the spec-generator and spec-executor agents are bound by it at registration time. Until then, it lives here as guidance picked up via the memory index.
