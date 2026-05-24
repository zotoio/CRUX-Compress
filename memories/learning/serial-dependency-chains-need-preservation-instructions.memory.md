---
id: "8fb7310"
title: "Serial dependency chains need explicit content-preservation instructions between subtasks"
description: "When multiple subtasks in a serial dependency chain all edit the same files, each executing agent's prompt must include an explicit 'preserve content from subtasks N–M' instruction to prevent accidental overwrites."
type: "learning"
strength: 2
created: 2026-05-24
modified: 2026-05-24
source: "20260516-meditate-research-mode-overhaul"
tags: [spec-execution, serial-dependencies, content-preservation, overwrite-prevention, multi-subtask, agent-coordination]
---

When multiple subtasks in a serial dependency chain all edit the same files, each executing agent's prompt must include an explicit "preserve content from subtasks N–M" instruction. Without this, later subtasks can accidentally overwrite content established by earlier ones — the agent sees the file's current state but may not recognise which sections were added by prior phases vs. which were pre-existing.

This was validated during the Meditate Research-Mode Overhaul: 7 subtasks editing the same 2 files (`.cursor/commands/crux-meditate.md`, `.cursor/agents/crux-cursor-memory-manager.md`) in strict serial order. The cross-cutting preservation rule was enforced after Phase 3's adversarial judge caught a decision-guidance gap that would have propagated through 4 remaining phases.

The pattern generalises to any spec where >3 subtasks touch overlapping file sets. Concrete mitigation: each subtask prompt should enumerate the specific sections it must not modify and reference the subtask IDs that own those sections.
