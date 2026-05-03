---
id: "31fec9d"
title: "Meditate uses read-only exploration with optional memory creation"
description: "The meditate command performs all exploration in read-only mode (no file modifications), with memory creation as an explicit opt-in step at the end. This separation ensures safety — the agent can deeply explore without risk of unintended changes, and the user controls what gets persisted."
type: "core"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "spec:20260425-crux-meditate"
tags: [meditate, safety, read-only, opt-in, separation-of-concerns, side-effects, design-pattern]
---

# Meditate uses read-only exploration with optional memory creation

## The principle

Exploration is read-only. Persistence is opt-in. The two are separated by an explicit user-confirmation gate.

`/crux-meditate` performs all of its work — recall, gap analysis, research, synthesis, recursion across three depths — without modifying any file on disk. Only after the user reviews the consolidated insights and chooses "Save meditation as draft spec" (or any other persisting action) does anything cross from agent context into the filesystem.

## Why this separation matters

### Safety during deep exploration

Recursive multi-agent exploration is exactly the kind of workflow where unintended writes are most dangerous. Each child agent has its own context, its own reasoning, and its own opportunities to misinterpret a finding as a directive to modify the codebase. Hard-gating the entire exploration phase as read-only removes that whole class of failure: a meditation that is mid-flight cannot leave artifacts behind.

### User control over what becomes durable

Synthesised insights vary widely in quality. Some are crisp; many are speculative; a few are wrong. Auto-persisting any of them pollutes the corpus. Forcing an explicit user decision after presentation ensures only insights the user judges worth keeping become durable artifacts.

### Reversibility for free

Anything that lives only in the agent's working context is reversible by design — closing the chat discards it. By keeping exploration entirely in-context until the explicit save step, every meditation is trivially abandonable. There is nothing to roll back if the meditation goes nowhere.

## How the boundary is enforced

| Phase | Side effects allowed |
|-------|---------------------|
| Recall | None — only reads `.crux/memory-index.yml` and memory files |
| Gap analysis | None — pure reasoning over recall output |
| Targeted research | None — read-only Grep/Read against the codebase |
| Synthesis | None — internal aggregation |
| Recursive child agents | Inherit read-only — they receive a read-only contract via `meditateFacet`/`meditateDepth` parameters |
| Presentation to user | None — message output only |
| Interactive continuation | The first state where writes can happen, and only via explicit user choice |
| If user picks "Save as draft spec" | A single, scoped write to `specs/YYYYMMDD-meditation-topic/spec-meditation-topic-YYYYMMDD.md` |

The write surface is minimal: one file, one location, only after explicit consent.

## Why "core" rather than "learning"

This is an architectural invariant, not a discovered technique. Any future change to meditate that introduces writes during exploration violates the contract that makes the command safe to invoke casually. The invariant is: **exploration is read-only; writes require explicit user approval at a single gate**.

## Generalises to other deep-exploration commands

Any command that performs heavyweight investigation and then offers to act on findings should use the same shape:

- **Code review commands** — read-only review, then explicit "apply suggestions" gate
- **Audit commands** — read-only audit, then explicit "apply fixes" gate
- **Spec drafting from prior work** — read-only synthesis, then explicit "save spec" gate

The shape is: a long read-only investigation phase, a presentation, and a single explicit gate that turns insights into persisted artifacts. Not "ask before each write" (too noisy), not "auto-save findings" (unsafe). One gate, after presentation.

## What this rules out

- Meditate creating memories silently (memory creation is not part of meditate's flow at all — it routes through `/crux-remember` or `/crux-dream`)
- Recursive children writing scratch files for inter-agent communication (state passes via parameters and return values only)
- Any "auto-save" feature that bypasses user confirmation
- Mid-exploration writes "for performance" (caching is allowed only via explicit, separately gated mechanisms)

## Source

`spec-crux-meditate-20260425.md` and the `crux-cursor-memory-manager` Meditate Mode workflow. The save-as-draft-spec step is the only write in the entire flow, and it is gated behind an `AskQuestion` multi-select after the user has seen the consolidated insights. The recursive children inherit the read-only contract because the agent definition gives them no skill that produces writes during exploration.
