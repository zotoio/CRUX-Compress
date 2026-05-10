---
id: "b6985f5"
title: "Session-scoped pure-toggle commands should be handled in-band, not via subagent delegation"
description: "Among CRUX memory commands, /crux-amnesia is the only one that does NOT spawn the crux-cursor-memory-manager subagent. The others (dream, recall, remember, meditate, forget) all delegate because they read or write disk state. Amnesia is purely a session-scope toggle — it writes nothing, modifies no config, touches no files — so subagent spawn overhead would be pure waste. Pattern: when a command's only effect is to toggle a session-local flag with no persistent side effects, handle it in the parent agent directly. Future similar commands should follow this discriminator: does it write anything? If no, handle in-band."
type: "learning"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260425-crux-amnesia"
tags: [architecture, commands, session-scope, subagents, performance, design-pattern, agent-orchestration]
---

# Session-scoped pure-toggle commands should be handled in-band

## The pattern

CRUX memory commands fall into two categories:

| Category | Commands | Architecture |
|----------|----------|--------------|
| Stateful operations | `/crux-dream`, `/crux-recall`, `/crux-remember`, `/crux-meditate`, `/crux-forget` | Delegate to `crux-cursor-memory-manager` subagent |
| Session-scope toggle | `/crux-amnesia` | Handled in-band by the parent agent |

The discriminator is **persistent side effects**:

- Stateful commands read or write `.crux/crux-memories.json`, memory files, reference trackers, or the memory index
- Toggle commands flip a session-local flag and do nothing else

## Why amnesia bypasses the subagent

The amnesia spec (`spec-crux-amnesia-20260425.md`) under "Key Architectural Properties" explicitly documents this:

> 1. **No agent spawn** — unlike `/crux-dream`, `/crux-recall`, `/crux-remember`, `/crux-meditate`, and `/crux-forget`, amnesia does NOT delegate to the `crux-cursor-memory-manager` subagent
> 2. **No persistent state** — amnesia NEVER modifies `.crux/crux-memories.json`, memory files, trackers, or the memory index

Spawning a subagent for a write-nothing toggle would add cost (context loading, agent boot, return-trip serialization) for zero benefit — the parent agent already has everything needed to flip a session flag.

## Generalizable to future commands

When designing a new command, ask:

1. Does it read disk state outside the chat session? → Delegate
2. Does it write anything (config, files, trackers, index)? → Delegate
3. Is it purely a session-local flip with implicit reset on chat close? → Handle in-band

Examples that should follow the in-band pattern if introduced:

- A session-scope log-level toggle (e.g. `/crux-verbose`)
- A session-scope tool gate (e.g. `/crux-readonly`)
- A session-scope feature switch (e.g. `/crux-strict`)

Examples that should delegate:

- Anything that needs to enumerate memories, parse YAML files, run rebalancing logic, or write summaries

## Counter-pattern to avoid

Routing a session-scope toggle through a subagent "for consistency" with sibling commands. Consistency in command surface (markdown layout, related-section pattern, response format) is good. Consistency in execution model is wrong if the underlying needs differ — sibling-mimicry should not override architectural appropriateness.

## Detection heuristic

If a command's full behavior contract reads "set a flag, suppress N behaviors, restore on chat close, no side effects" — it should not spawn a subagent. If a reviewer flags such a command as "missing subagent delegation," cite the amnesia precedent and the no-side-effects discriminator.
