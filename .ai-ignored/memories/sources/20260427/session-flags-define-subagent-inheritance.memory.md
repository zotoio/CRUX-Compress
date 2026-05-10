---
id: "4d0d83f"
title: "Session-scoped flags must define explicit subagent inheritance semantics"
description: "When a chat-session-only flag exists (e.g. amnesia ON), every subagent spawn for ordinary work must inherit the parent's session state — otherwise subagents could silently violate the session intent. The amnesia spec defines this contract explicitly: subagents inherit amnesia state for ordinary work, but explicit user invocation of an exempt command bypasses inheritance because that represents direct user intent. Pattern for any future session-scoped flag: (1) define what subagents inherit, (2) define what breaks inheritance, (3) document both in an alwaysApply rule so every agent context loads the inheritance rules consistently."
type: "learning"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260425-crux-amnesia"
tags: [subagents, session-scope, inheritance, flags, agent-orchestration, design-pattern, alwaysapply-rules]
---

# Session-scoped flags must define explicit subagent inheritance semantics

## The risk without explicit inheritance

A session-scope flag (like amnesia) exists in the parent agent's context. When the parent spawns a subagent, the subagent gets a fresh context — the flag does not propagate automatically. Without explicit inheritance semantics, a subagent could silently violate the session intent:

- User runs `/crux-amnesia on` — parent is in amnesia mode
- Parent spawns a generalPurpose subagent for code review
- Subagent loads `.crux/memory-index.yml`, annotates output with `[memory:...]`, increments reference counters

The parent's session intent (suppress ambient memory) is broken by the subagent. The user sees memory annotations they explicitly disabled.

## The amnesia inheritance contract

The amnesia spec under "What Amnesia Suppresses" #6 and "Key Architectural Properties" #3 jointly define:

1. **Default**: subagents spawned for ordinary work inherit the amnesia state — they too suppress discovery, loading, annotation, reference tracking, and dream nudges
2. **Exception**: explicit user invocation of an exempt memory command (`/crux-dream`, `/crux-recall`, `/crux-remember`, `/crux-meditate`, `/crux-forget`) breaks inheritance because the user explicitly invoked the memory system

The CRUX-compressed `Φ.amnesia` block encodes this concisely:

```
subagents→inherit; explicit /crux-dream|recall|remember|meditate|forget→user intent OK
```

## Generalizable pattern for future session flags

When introducing any new session-scoped flag, the spec must answer three questions:

1. **What do subagents inherit?** — Define the subset of behaviors that propagate. Default to "all" unless there is a specific reason to scope narrower.
2. **What breaks inheritance?** — Enumerate explicit user actions that override the inherited state. Direct user invocation should always be honored.
3. **Where is the contract documented?** — Place it in an `alwaysApply: true` rule so every parent agent and subagent loads the inheritance rules at session start.

## The alwaysApply rule placement is critical

Subagent inheritance only works if the subagent loads the same rule that defines the inheritance. Placing the contract in:

- A command file (`.cursor/commands/*.md`) — only loaded when the command is invoked
- An agent file (`.cursor/agents/*.md`) — only loaded when that specific agent is spawned
- A regular non-applied rule — not loaded by default

…would cause inheritance to fail for arbitrary subagent types. The amnesia rule lives in `.cursor/rules/crux-memories-integration.md` with `alwaysApply: true`, which means every agent context — parent or subagent — loads the same inheritance contract.

## Required deliverable for future session-flag specs

A session-flag spec must include a subtask or section that:

- Defines the inheritance behavior in an `alwaysApply: true` rule file
- Enumerates the explicit-invocation exceptions
- Generates the corresponding CRUX-compressed rule with the inheritance encoded
- Verifies (in eval scenarios) that subagents respect the inherited state for ordinary work

Without this explicit contract, the flag will leak under subagent fan-out, defeating its purpose.
