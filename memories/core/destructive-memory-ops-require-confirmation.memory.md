---
id: "c71c143"
title: "Destructive memory operations require explicit user confirmation"
description: "Any destructive memory lifecycle operation (forget, bulk archive, cascade delete) must always present matched memories and require explicit user confirmation before executing. There is intentionally no --yolo / auto-delete mode because these operations are irreversible. The manager confirms even when the user passes a fully qualified memory ID."
type: "core"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260406-crux-forget"
tags: [memory-system, safety, destructive-ops, confirmation, forget, irreversible]
---

# Destructive memory operations require explicit user confirmation

## Principle

Memory deletion and any other destructive memory lifecycle operation must never auto-execute. The manager always:

1. Resolves the input to one or more concrete memory files
2. Displays matched memories with `id`, title, type, strength, and source
3. Asks the user to confirm which entries to remove
4. Only then delegates to the destructive skill operation

This applies even when the input is unambiguous (e.g. a single 7-char hex `id`). Confirmation is mandatory because:

- Memory deletion removes both the memory file and its reference tracker — there is no built-in undo
- Aggregated knowledge represented by a memory is hard to reconstruct from scratch
- A user who is wrong about which memory to delete suffers silent knowledge loss

## Where this applies

- `/crux-forget` (memory deletion)
- Any future bulk operations: cascade delete, mass archive, forced demotion to `archived`, etc.
- Resolved-bug auto-forgetting in `/crux-dream`: even in `--yolo` mode, "possibly resolved" redflags still prompt the user; only "likely resolved" auto-forget

## Anti-patterns

- A `--yolo` / `--force` flag that bypasses confirmation for destructive memory ops
- Auto-deleting memories whose tracker shows zero references (use demotion / archival instead — those are reversible)
- Treating a single matched memory as "obviously what the user meant" and skipping confirmation

## Rationale source

Established as Decision 2 of `spec-crux-forget-20260406.md`: "Deletion always requires user confirmation — no `--yolo` auto-delete mode, since forgetting is destructive and irreversible."
