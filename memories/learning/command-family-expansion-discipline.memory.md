---
id: "00a6d09"
title: "Command-family expansion requires updating all backlink sites"
description: "When adding a new command to an existing family, two distinct backlink sites must be updated: (1) sibling Related sections in every existing family member command file — navigational cross-references, and (2) override exception lists in any rule or command that defines a suppression override over the family — behavioral specifications. Missing Related sections degrade discovery; missing override exceptions cause real suppression of intended-exempt commands. Both are invisible from the new command's perspective and require explicit spec deliverables."
type: "learning"
strength: 2
created: 2026-04-26
modified: 2026-04-27
source: "20260406-crux-forget"
tags: [commands, command-families, cross-references, documentation, completeness, spec-design, override-rules, exception-lists, behavioural-spec, backlinks]
consolidated_from: ["bdcc9ad", "8006029"]
---

# Command-family expansion requires updating all backlink sites

## The recurring gap

When a new command joins an existing family (e.g. `/crux-forget` joining `/crux-dream` and `/crux-mindreader`), the new command's forward-references are always written. But existing files that should link back to the new command are routinely missed. There are two distinct backlink sites, each with different failure modes.

## Backlink site 1: Sibling Related sections

Every command file in `.cursor/commands/` ends with a `## Related` section. When a new sibling is added:

- The new command's own Related section links to existing siblings — rarely missed
- Existing siblings' Related sections do **not** automatically learn about the new command — they need surgical updates

**Failure mode**: Discovery gap. The new command knows about its family, but the family does not know about it. Navigation from older commands is broken.

**Concrete example**: `spec-crux-forget-20260406` added `/crux-forget` to the memory command family. Both judges flagged that `crux-dream.md` and `crux-mindreader.md` Related sections did not mention `/crux-forget`.

## Backlink site 2: Override exception lists

Some commands define overrides that suppress ambient behavior except for an explicit list of exempt commands. When a new command joins the family, it must be added to every exception list where it should be exempt.

**Failure mode**: Real behavioral suppression. Missing entries mean the override actually suppresses the intended-to-be-exempt command — not just a documentation gap.

**Concrete example**: `/crux-amnesia` defines a session-scope override suppressing ambient memory usage. The exception list lives in three files:

| File | Form |
|------|------|
| `.cursor/commands/crux-amnesia.md` | Natural-language list of exempt commands |
| `.cursor/rules/crux-memories-integration.md` | Same list under the amnesia override section |
| `.cursor/rules/crux-memories-integration.crux.mdc` | CRUX-compressed `Φ.amnesia{... explicit /crux-dream|recall|remember|meditate|forget→user intent OK}` |

When `/crux-remember` and `/crux-meditate` later joined the family, all three files had to be updated. If missed, those commands would have been suppressed under amnesia mode despite being explicit user invocations.

## Comparison

| Aspect | Related sections | Override exception lists |
|--------|-----------------|------------------------|
| Surface | Documentation cross-references | Behavioral specification |
| Failure mode | Discovery gap | Real suppression of intended-exempt commands |
| Detection | Navigation testing | Override-behavior testing |
| Files to update | Every sibling command file | Source rule + compressed rule + override-defining command |

## Required spec deliverables

When authoring a spec that adds a command to an existing family:

1. **Sibling Related sections** — update every existing family member's `## Related` section
2. **Override exception lists** — update any rule or command that defines a suppression override over the family
3. **Compressed CRUX blocks** — regenerate after source edits to rules

## Heuristic for finding backlink sites

For a new command at `.cursor/commands/{new}.md`:

1. All other `.cursor/commands/*.md` sharing a prefix or theme (Related sections)
2. Any agent/skill file referencing the family
3. Search for override sections: `rg 'override|exception|exempt|suppress' .cursor/rules/ .cursor/commands/`
4. Check `alwaysApply: true` rules for phase blocks listing existing family members

## Root cause

Specs naturally focus on the new artifact and its forward-references. Reverse-link surfaces (existing files needing updates) are invisible from the new command's perspective. An explicit checklist deliverable is the simplest fix for both backlink site types.
