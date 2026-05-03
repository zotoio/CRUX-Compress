---
id: "039b05f"
title: "Reverse-engineer specs to restore traceability for work completed without planning"
description: "When meaningful work has been completed in a prior session without a formal spec, write a reverse-engineered spec after the fact — same structure as forward-planned specs (overview, decisions, subtasks, Definition of Done) but with an Execution Notes paragraph stating the spec is reverse-engineered. Restores traceability, makes the work auditable, and enables future memory extraction via /crux-dream. Could be formalised as a workflow command."
type: "idea"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260425-crux-remember"
tags: [spec-system, retrospective-documentation, traceability, dream-pipeline, workflow-idea, audit-trail]
---

# Reverse-engineer specs to restore traceability for work completed without planning

## The observation

The CRUX dream pipeline (`/crux-dream <spec-name>`) extracts memories from completed specs. It only works when a spec exists. Work that was done ad-hoc, in a prior chat, or "just because" is invisible to the dream pipeline — its insights cannot be captured as memories because there is no work-item directory to point at.

The `spec-crux-remember-20260425` spec is itself a working example of the fix: it documents work that was already completed, structured as if planned forward. Its Execution Notes section says: *"Reverse-engineered spec: This spec documents work already completed in a prior chat session. All subtasks were implemented and verified."*

This dream extraction itself only succeeded because that spec exists.

## The proposed workflow

Reverse-engineering a spec is currently informal — done by hand when someone notices the gap. Formalising it would look like:

### Manual recipe (today)

1. Identify the change set — usually a commit or commit range that captures the completed work
2. Read the diff and identify logical groupings (subtask-sized chunks)
3. Draft a forward-style spec: Overview, Key Decisions, Requirements, Subtask Manifest, Definition of Done
4. Add an Execution Notes section that says the spec is reverse-engineered, names the originating chat or commit, and confirms each subtask was already executed
5. Commit the spec to `specs/{date}-{slug}/` so it can be picked up by `/crux-dream`

### Formalised command (idea)

A `/crux-spec --reverse <commit-range>` (or equivalent) could:

1. Read the diff for the commit range
2. Cluster changed files into likely-subtask groups (by directory, by feature area, by file type)
3. Generate a draft spec skeleton with `# TODO` markers where the LLM cannot infer intent
4. Open the draft for human review and refinement
5. Save to `specs/{date}-{slug}/` once approved

The benefit: ad-hoc work becomes auditable and dreamable without each user re-discovering the technique.

## Why this is worth tracking as an idea

- **Demonstrated value**: the crux-remember spec's reverse-engineering produced extractable memories (this very dream cycle is the proof)
- **Clear gap**: the dream pipeline has no fallback for spec-less work; the only options today are "no memories" or "reverse-engineer by hand"
- **Composable**: a reverse-spec command would chain with `/crux-dream` to give a complete recovery path: commit → reverse-spec → dream → memories

## Open questions

- How aggressively should the LLM cluster changes into subtasks? Per-file? Per-directory? Per-decision?
- Should reverse-engineered specs participate in REM sleep on the same schedule as forward-planned ones, or be flagged for closer scrutiny since they were not adversarially verified during execution?
- What execution-state placeholder is appropriate? Mark all subtasks `Done` with a `reverse-engineered: true` flag?
- Should the reverse-spec command also create the `_execution-state.yml` so the dream pipeline's verification step does not need a manual override?

## Adjacent ideas

- A "diff archaeology" command that summarises a commit range without spec-shaping it — a lighter weight alternative when the work is too small to justify a spec
- A "spec-or-it-didn't-happen" lint that flags PRs touching feature surfaces without a corresponding `specs/` entry, encouraging spec-first workflow without blocking ad-hoc fixes

## Source

Spec `20260425-crux-remember`'s Execution Notes section: *"Reverse-engineered spec: This spec documents work already completed in a prior chat session."*
