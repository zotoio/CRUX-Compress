---
id: "ba74013"
title: "Session-scope command design: in-band handling and subagent inheritance"
description: "Session-scoped commands that are pure toggles with no persistent side effects should be handled in-band by the parent agent, not delegated to a subagent. When session-scope flags do exist, every subagent spawn for ordinary work must inherit the parent's session state — documented in an alwaysApply rule — or subagents will silently violate the session intent. Explicit user invocation of exempt commands breaks inheritance because it represents direct user intent."
type: "learning"
strength: 2
created: 2026-04-26
modified: 2026-04-27
source: "20260425-crux-amnesia"
tags: [architecture, commands, session-scope, subagents, performance, design-pattern, agent-orchestration, inheritance, flags, alwaysapply-rules]
consolidated_from: ["b6985f5", "4d0d83f"]
---

# Session-scope command design: in-band handling and subagent inheritance

Two complementary patterns govern how session-scoped commands and flags interact with the agent architecture.

## Pattern 1: In-band handling for pure toggles

CRUX memory commands fall into two execution categories:

| Category | Commands | Architecture |
|----------|----------|--------------|
| Stateful operations | `/crux-dream`, `/crux-recall`, `/crux-remember`, `/crux-meditate`, `/crux-forget` | Delegate to `crux-cursor-memory-manager` subagent |
| Session-scope toggle | `/crux-amnesia` | Handled in-band by the parent agent |

### The discriminator: persistent side effects

- Stateful commands read or write `.crux/crux-memories.json`, memory files, reference trackers, or the memory index — these need the subagent's skill access and orchestration
- Toggle commands flip a session-local flag and do nothing else — subagent spawn adds cost (context loading, agent boot, return-trip serialization) for zero benefit

### Decision framework for new commands

1. Does it read disk state outside the chat session? → Delegate
2. Does it write anything (config, files, trackers, index)? → Delegate
3. Is it purely a session-local flip with implicit reset on chat close? → Handle in-band

### Anti-pattern

Routing a session-scope toggle through a subagent "for consistency" with sibling commands. Consistency in command surface (markdown layout, Related sections, response format) is good. Consistency in execution model is wrong when the underlying needs differ.

## Pattern 2: Explicit subagent inheritance for session flags

When a session-scope flag exists (e.g. amnesia ON), subagents get a fresh context and the flag does not propagate automatically. Without explicit inheritance semantics, subagents silently violate the session intent.

### The risk

- User runs `/crux-amnesia on` — parent is in amnesia mode
- Parent spawns a generalPurpose subagent for code review
- Subagent loads memory index, annotates output with `[memory:...]`, increments reference counters
- The parent's session intent (suppress ambient memory) is broken

### The amnesia inheritance contract

1. **Default**: subagents spawned for ordinary work inherit the amnesia state — they suppress discovery, loading, annotation, reference tracking, and dream nudges
2. **Exception**: explicit user invocation of an exempt memory command (`/crux-dream`, `/crux-recall`, `/crux-remember`, `/crux-meditate`, `/crux-forget`) breaks inheritance because the user explicitly invoked the memory system

### Three questions every session-flag spec must answer

1. **What do subagents inherit?** — Define the subset of behaviors that propagate. Default to "all" unless there is a specific reason to scope narrower.
2. **What breaks inheritance?** — Enumerate explicit user actions that override the inherited state. Direct user invocation should always be honored.
3. **Where is the contract documented?** — Place it in an `alwaysApply: true` rule so every parent agent and subagent loads the inheritance rules at session start.

### Why alwaysApply placement is critical

Subagent inheritance only works if the subagent loads the same rule. Placing the contract in a command file (only loaded on invocation), an agent file (only loaded for that agent type), or a non-applied rule would cause inheritance to fail for arbitrary subagent types. The amnesia rule in `.cursor/rules/crux-memories-integration.md` is `alwaysApply: true`, ensuring every context — parent or subagent — loads the same contract.

### Required deliverable for future session-flag specs

- Define inheritance behavior in an `alwaysApply: true` rule file
- Enumerate explicit-invocation exceptions
- Generate the corresponding CRUX-compressed rule with inheritance encoded
- Verify (in eval scenarios) that subagents respect the inherited state
