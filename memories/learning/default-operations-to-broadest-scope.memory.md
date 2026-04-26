---
id: "c35a703"
title: "Default new operations to the broadest scope when calling context lacks specificity signals"
description: "Operations triggered without rich calling context (e.g. /crux-remember has no spec artifacts, no subtask agent assignments, no work logs) cannot reliably infer specialised scope. Default such operations to the broadest scope — base, root, default — and let the user opt into narrower scope explicitly. Document the default explicitly rather than as silent behaviour to prevent misclassification later."
type: "learning"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260425-crux-remember"
tags: [scope-selection, default-behavior, agent-scoping, ad-hoc-operations, principle-of-least-specificity, design-pattern]
---

# Default new operations to the broadest scope when calling context lacks specificity signals

## The pattern

Some operations on a scoped system have rich calling context — they run inside a workflow that produces signals about which scope an entry belongs to. Other operations have no such context — they are triggered ad-hoc by a user with no surrounding artifacts.

For ad-hoc operations, do not guess at narrow scope. Default to the broadest scope and document that default explicitly. Users with specific knowledge can override; users without that knowledge are safe by default.

## Concrete example: /crux-remember placement

The CRUX memory system supports two scopes: base (`memories/{type}/`) and agent-scoped (`memories/agents/{agent-id}/{type}/`). Two commands can write to either:

- `/crux-dream` runs after a spec completes. It has artifacts: subtask agent assignments, work logs, execution state. It can identify the owning agent for each candidate insight and place agent-specific memories in the right subdirectory.
- `/crux-remember` is invoked by the user with arbitrary text. There are no artifacts. The user's own context may or may not include hints about owning agents.

The spec made the deliberate design choice (Decision 4) to default `/crux-remember` to base scope. Agent scoping requires the user to opt in explicitly — it is never inferred. Rule 1 of the agent's scoping rules captures this: "Ad-hoc memories from `/crux-remember` are always placed in base scope (`memories/{type}/`) unless the user explicitly requests agent scoping."

## Why broadest by default

- **Reversible misclassification**: a memory placed in base scope can be moved to agent scope later if needed. The reverse is also reversible, but base-scope memories are visible to all agents — they cannot be lost from one agent's view.
- **No false specificity signal**: a memory placed in agent scope implies the system had a reason. If it was placed there without evidence, downstream consumers receive a misleading hint.
- **Lower cognitive load**: users do not need to understand the scope taxonomy to use the basic command. The default works for the common case.

## Why document the default explicitly

Implicit defaults rot. If "ad-hoc memories go to base" is treated as obvious or unspoken, a future change ("let's auto-classify by tags") can creep in without anyone noticing the regression. Stating the default in the agent definition and in the command file (rather than relying on it being inferred from behaviour) makes the contract reviewable.

The spec applied this discipline: the agent scoping rule was changed from "Only during dream extraction" to "Only during dream extraction or explicit remember", with a clarifying sentence that ad-hoc memories default to base unless explicitly scoped. Both halves are documented.

## Generalises to

Any operation that writes to a scoped store without rich calling context:

- A `quickPaste` operation into a permissions-scoped CMS — default to public root, require explicit folder selection
- A user-created tag without category context — default to "general" / uncategorised
- A bookmark added without folder context — default to top-level "Unfiled"
- A note created without project context — default to "Inbox"

The principle: when context is sparse, prefer broad placement. Users with specific knowledge can move; users without specific knowledge are not silently misled.

## Anti-pattern: heuristic-guessed narrow scope

Tempting alternatives that should be rejected:

- Inferring scope from tags (tags can be free-text and noisy)
- Inferring scope from the user's recent activity (their last task may be unrelated to the memory)
- Defaulting to "most recently used scope" (silently couples unrelated memories)

When the context is genuinely sparse, accept that and surface the broadest default.

## Source

Decision 4 of `spec-crux-remember-20260425.md` and the relaxed agent scoping rule 1 in `.cursor/agents/crux-cursor-memory-manager.md`.
