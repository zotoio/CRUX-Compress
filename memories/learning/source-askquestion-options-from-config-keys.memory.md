---
id: "ba92c4e"
title: "Source AskQuestion options from config keys to keep UI in sync with semantic model"
description: "When a command's interactive options must mirror a domain concept already defined in config (e.g. memory types defined as keys of `typeTransitions`), source the AskQuestion option list from the config keys directly rather than hardcoding the strings. Adding a new type to config then automatically appears in the UI; no separate UI update is needed. Eliminates a class of drift where the option list and the underlying semantic model fall out of sync."
type: "learning"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260425-crux-remember"
tags: [askquestion, ui, config-driven, drift-prevention, design-pattern, single-source-of-truth]
---

# Source AskQuestion options from config keys to keep UI in sync with semantic model

## The pattern

Every interactive prompt that asks the user to pick from a fixed set of domain values has two definitions: the option list shown in the prompt, and the underlying semantic model that uses those values. When these are maintained separately, they drift.

The fix: when the semantic model is already encoded as keys of a config map, pass those keys directly into the AskQuestion options. Treat the config as the single source of truth for both behaviour and UI.

## Concrete example: /crux-remember type selection

`/crux-remember` asks the user to pick a memory type. The five types — `idea`, `learning`, `redflag`, `core`, `goal` — are already defined as keys of `typeTransitions` in `.crux/crux-memories.json`:

```json
"typeTransitions": {
  "idea":     { "promoteAt": 5,  "promoteTo": "learning" },
  "learning": { "promoteAt": 15, "promoteTo": "core" },
  "redflag":  { "promoteAt": 10, "promoteTo": "core" },
  "core":     { "promoteAt": null },
  "goal":     { "promoteAt": null }
}
```

The Remember Mode workflow says: "Use the `AskQuestion` tool to present memory type options sourced from `typeTransitions` keys". Adding a sixth type (e.g. introducing a new `pattern` type) requires editing config in one place — the AskQuestion options follow automatically.

## What this prevents

- **Silent option-list drift**: a new type added to config but not the prompt is invisible to users; users keep picking from the old set even though the system supports more
- **Stale prompt entries**: a type removed from config but still in the prompt produces a runtime error when the user selects it
- **Documentation duplication**: type descriptions can live next to the config keys (or in a sibling description map), avoiding two places to update

This is a related drift class to `tooling-defaults-must-align-with-spec` (memory `96a7410`), where the surface was tool defaults vs spec defaults — same pattern, different artifact.

## Where it generalises

Any AskQuestion (or similar pickList / dropdown / radio) backed by a finite enum already defined elsewhere in the codebase:

- Status fields: read enum values from a status table or schema
- Routing destinations: read service names from a service registry
- Feature flags: read enabled features from the flag registry
- Sort orders: read the sort-key list from the data schema

If you find yourself typing strings into a prompt that exist verbatim somewhere else in the codebase, you have the drift hazard.

## Implementation note

When the option list comes from config keys, also consider sourcing per-option descriptions from the config (or a sibling `descriptions` map). Otherwise option text drifts the same way option keys would.

## Source

Decision 1 of `spec-crux-remember-20260425.md`: "Type selection uses `AskQuestion` with options sourced from `typeTransitions` keys (`idea`, `learning`, `redflag`, `core`, `goal`), keeping the UI consistent with the config-driven type system."
