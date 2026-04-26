---
id: "826c280"
title: "AGENTS.crux.md is a transient install-time artifact, not a maintained CRUX file"
description: "AGENTS.md is a normal source file edited directly. AGENTS.crux.md does NOT exist as a persistent file in this repository — install.py generates it transiently during installation and deletes it after. The general 'always surgically update the corresponding .crux file when the source changes' rule does NOT apply to AGENTS.md. Reviewers and agents must not demand regeneration of AGENTS.crux.md after edits to AGENTS.md."
type: "redflag"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260406-crux-forget"
tags: [crux, agents-md, install.py, generated-files, transient, review, false-positive]
---

# AGENTS.crux.md is transient — do not demand regeneration

## The trap

The repository follows a strict rule: when a source file changes and a corresponding `.crux.md` / `.crux.mdc` file exists, the CRUX file must be updated with surgical diffs to stay in sync. This rule does **not** apply to `AGENTS.md`.

## Why

- `AGENTS.md` is a normal source file in this repository — edited directly, no generated frontmatter banner
- `AGENTS.crux.md` is **not** present as a checked-in file
- `install.py` generates `AGENTS.crux.md` on-the-fly during installation (around line 469-470) and deletes it again later (around line 341)
- Treating `AGENTS.crux.md` as a maintained CRUX-compressed artifact and demanding sync edits is a category error

## Observed false-positive

The first judge assessment of `spec-crux-forget-20260406` (`zoto-judge-assessment-crux-forget-20260406.md`) flagged "Missing `AGENTS.crux.md` regeneration" as a MEDIUM finding. The reassessment (`assessment-crux-forget-20260407.md`) correctly invalidated the finding after verifying no such file is checked in.

## Detection heuristic

Before demanding a `.crux` sync update for any file:

1. Run a glob for the alleged `.crux.md` / `.crux.mdc` artifact in the repository tree
2. If zero hits — the file is not a maintained CRUX artifact, and no sync is required
3. If hits — verify the frontmatter has `generated:` plus `sourceChecksum:` or `sourceUrl:` before applying the sync rule

## Implication for spec authors and reviewers

When introducing or modifying `AGENTS.md`, do **not** add a deliverable for `AGENTS.crux.md` regeneration. Note this exception in spec assessments to avoid generating false-positive findings.
