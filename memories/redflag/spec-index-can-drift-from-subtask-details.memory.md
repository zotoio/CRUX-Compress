---
id: "d944d7c"
title: "Spec index text can drift from subtask details; reviewers must verify both"
description: "A spec's top-level index (Decisions, Requirements, Definition of Done) can contain text that contradicts the subtask files' actual instructions. The subtask details are typically more accurate because they are written closer to execution. Reviewers and judges must read both layers; on conflict, the subtask details are authoritative. Reading only the spec index risks producing critical false-positive findings."
type: "redflag"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260406-crux-forget"
tags: [spec-system, review, judge, drift, verification, methodology, false-positive]
---

# Spec index text can drift from subtask details

## The pattern

Specs in this repository are split across multiple files:

- The spec index (`spec-{slug}-{date}.md`) — overview, Key Decisions, Requirements, Subtask Manifest, Definition of Done
- One subtask file per subtask (`subtask-NN-{slug}-{date}.md`) — concrete deliverables, implementation notes, work logs

These two layers can drift. The spec index is written first and may not be re-edited as the author refines individual subtasks. The result is that spec index text can describe behaviour that the subtasks deliberately do not perform.

## Concrete example (from `20260406-crux-forget`)

- **Spec index Decision 5 / Requirement 9** said the new command file would be added to `install.py`'s `standard_files` list
- **Subtask 06** (Implementation Notes section B, Deliverables Checklist line 17, Work Log step 4) explicitly said NOT to add it to `standard_files` — and the executor correctly followed the subtask
- The first judge read only the spec index and produced a CRITICAL finding accusing the spec of breaking installer conventions
- The second judge re-read the subtasks, discovered the contradiction, and corrected the assessment

## Authoritative layer

When the spec index and a subtask disagree:

- The **subtask** is treated as authoritative for what the executor actually does
- The spec index should be repaired to match the subtask, not the other way around
- Reviewers should mark the spec-index drift as a finding to fix, but should not flag the subtask's correct behaviour as wrong

## Required reviewer practice

When assessing a spec or auditing a completed execution:

1. Always read both the spec index AND every referenced subtask file
2. When the spec index makes a specific claim about a file or list, cross-check it against the subtask that owns that file
3. If the spec index disagrees with the subtask, treat the subtask as ground truth and recommend updating the spec index
4. Do not produce a CRITICAL or MEDIUM finding from spec-index text alone — verify against subtasks first

## Detection heuristic

Spec drift indicators to scan for:

- Spec index says "must include X" but subtask deliverables checklist explicitly checks "NOT modified"
- Spec index uses vague language ("update file Y") while subtasks contain explicit do-not-touch warnings
- Decision N references conventions that the subtask author corrected after consulting the codebase
