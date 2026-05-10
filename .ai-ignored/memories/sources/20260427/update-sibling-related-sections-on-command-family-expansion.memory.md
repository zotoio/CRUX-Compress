---
id: "bdcc9ad"
title: "Adding a sibling command requires updating existing siblings' Related sections"
description: "When introducing a new command into an existing command family (e.g. /crux-forget joining /crux-dream and /crux-mindreader), the new command's own Related section is usually written, but the existing siblings' Related sections are typically forgotten. Both judges flagged this in the crux-forget spec. Spec deliverables for 'add a new command' should always include backlinks: every existing sibling's Related section must be updated to mention the new command."
type: "learning"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260406-crux-forget"
tags: [commands, cross-references, documentation, completeness, spec-design, command-families]
---

# Update sibling Related sections on command-family expansion

## The recurring gap

Every command file in `.cursor/commands/` ends with a `## Related` section that links to sibling commands and supporting agents/skills. When a new sibling is added to a family:

- The new command's own Related section is written from scratch and links to existing siblings — this part is rarely missed
- The existing siblings' Related sections do **not** automatically learn about the new sibling — they need surgical updates

The result: the new command knows about its family, but the family does not know about it. Discovery from older commands is broken.

## Concrete example

`spec-crux-forget-20260406` added `/crux-forget` to the memory command family alongside `/crux-dream` and `/crux-mindreader`. Both judges flagged that:

- `crux-dream.md`'s Related section (around line 63) listed `/crux-mindreader` but not `/crux-forget`
- `crux-mindreader.md`'s Related section (around line 83) listed `/crux-dream` but not `/crux-forget`

Neither was covered by any subtask. The spec was approved before this gap was fixed.

## Required deliverable

When authoring a spec that introduces a new command into a family, include this deliverable explicitly (or fold into the new-command-creation subtask):

> Update the Related section of every existing sibling command in the family (and every supporting agent/skill that links to the family) to include a link to the new command.

## Heuristic for finding siblings

For a new command at `.cursor/commands/{new}.md`, the siblings are typically:

1. All other `.cursor/commands/*.md` that share a prefix or theme (e.g. `crux-*`)
2. Any agent file that references the family (e.g. `crux-cursor-memory-manager.md` references all memory commands)
3. Any skill file that references the family

Search for the family prefix or one existing sibling's command name to locate every file that needs updating.

## Why this is recurring

Specs naturally focus on the new artifact and its forward-references. The reverse-link surface (existing files needing updates) is invisible from the new command's perspective. A checklist deliverable is the simplest fix.
