---
id: "8006029"
title: "Override exception lists are a backlink site easy to miss when expanding a command family"
description: "When a command defines an override that suppresses ambient behavior except for an explicit list of exempt commands (e.g. /crux-amnesia exempts /crux-dream, /crux-recall, /crux-remember, /crux-meditate, /crux-forget), that exception list is a backlink site. When new commands join the family later, the exception list must be updated in every file where it appears — typically the command markdown AND the always-applied rule file (source AND CRUX-compressed). Distinct from sibling Related sections (memory bdcc9ad) because override lists have behavioral implications: missing entries cause real suppression of intended behavior, not just navigational gaps."
type: "learning"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260425-crux-amnesia"
tags: [commands, command-families, override-rules, exception-lists, behavioural-spec, backlinks, completeness, spec-design]
---

# Override exception lists need backlinks on family expansion

## The recurring gap

`memory bdcc9ad` (`update-sibling-related-sections-on-command-family-expansion`) captures one backlink site for command-family expansion: sibling `## Related` sections. The amnesia spec surfaced a second, semantically distinct backlink site:

**Override exception lists** — the explicit list of commands that bypass an override's suppression behavior.

Whereas Related sections are navigational (broken Related links degrade discovery), override exception lists are behavioral — missing entries mean the override actually suppresses the intended-to-be-exempt command.

## Concrete example

`/crux-amnesia` defines a session-scope override that suppresses ambient memory usage. The override has an explicit exception list: commands that work normally even when amnesia is active because they represent direct user intent to interact with the memory system.

The exception list lives in **two files**:

| File | Form |
|------|------|
| `.cursor/commands/crux-amnesia.md` | Natural-language list of exempt commands |
| `.cursor/rules/crux-memories-integration.md` | Same list under the amnesia override section |
| `.cursor/rules/crux-memories-integration.crux.mdc` | CRUX-compressed `Φ.amnesia{... explicit /crux-dream\|recall\|remember\|meditate\|forget→user intent OK}` |

Originally amnesia exempted only `/crux-dream`, `/crux-recall`, `/crux-forget`. When `/crux-remember` and `/crux-meditate` later joined the family, the exception list in both source files (and the regenerated CRUX block) had to be updated — a session-day fix captured in the amnesia spec's "Changes Made in This Session" section.

If the exception list had been missed, `/crux-remember` and `/crux-meditate` would have been suppressed under amnesia mode despite being explicit user invocations — a real behavioral bug, not just stale documentation.

## Required deliverable

When authoring a spec that adds a command to an existing family, include the following sites in deliverables:

1. **Sibling `## Related` sections** in every existing family member command — covered by memory `bdcc9ad`
2. **Override exception lists** in any rule or command that defines a suppression override over the family — this memory
3. **Compressed CRUX blocks** for any rule above (regenerate after source edit)

## Heuristic for finding override exception lists

For a new command in `.cursor/commands/{new}.md`:

1. Search for command-family override sections: `rg 'override|exception|exempt|suppress' .cursor/rules/ .cursor/commands/`
2. Check `alwaysApply: true` rules for any phase block (`Φ.*`) listing existing family members
3. Read the source `.md` file paired with any matching `.crux.mdc` to find the natural-language list (the CRUX block is generated)

## Why distinct from memory `bdcc9ad`

| Aspect | Related sections (`bdcc9ad`) | Override exception lists (this memory) |
|--------|------------------------------|----------------------------------------|
| Surface | Documentation cross-references | Behavioral specification |
| Failure mode | Discovery gap | Real suppression of intended-exempt commands |
| Detection | Navigation testing | Override-behavior testing |
| Files | Every sibling command file | Source rule + compressed rule + override-defining command |

Both backlink sites are easy to miss for the same root cause: the new command knows about its forward-references, but reverse-link surfaces are invisible from the new command's perspective. The fix in both cases is an explicit checklist deliverable.
