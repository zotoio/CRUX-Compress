---
repository: https://github.com/zotoio/CRUX-Compress
name: crux-cursor-memory-manager
model: claude-opus-4-6
description: DEPRECATED dispatcher — prefer the mode-scoped crux-memory-* thin agents. Retained temporarily so pre-upgrade consumer installs continue to resolve the name. Removed after one minor release once the thin agents ship in the dist zip.
---
<!-- DEPRECATED dispatcher — prefer crux-memory-* thin agents. Do not add new behavior here; extend the appropriate thin agent. Remove after one minor release once thin agents ship in dist. -->

This agent is a **deprecated dispatcher shim**. The Memory Manager has been split into five mode-scoped thin agents so each memory command only pays for the mode it uses. If your task maps to one of the modes below, spawn the thin agent directly.

## Dispatch table

| Mode | Thin agent to spawn | Parent orchestrator |
|------|---------------------|---------------------|
| Dream Mode | `crux-memory-dream` | `/crux-dream <spec-name>` |
| REM Sleep | `crux-memory-rem` | `/crux-dream --rem` (also `/crux-recall` → Consolidate) |
| Recall Mode | `crux-memory-recall` | `/crux-recall` (Canvas branch on `--total`) |
| Remember Mode | `crux-memory-remember` | `/crux-remember` |
| Forget Mode | `crux-memory-forget` | `/crux-forget` (also `/crux-recall` → Delete) |

**Routing rule**: If your task is `<mode>`, prefer spawning `<thin-agent>` directly. This umbrella is retained for pre-upgrade installs and will be removed after one minor release once thin agents ship in the dist zip. The five thin agents each carry their own `context_manifest` honor block and shared-reference pointer, so no capability is lost by bypassing this dispatcher.

**Meditate ownership**: Meditate / Research / Quick / Ensemble work is owned by `crux-cursor-meditation-guide` (spawned by `/crux-meditate`) — not by this dispatcher.

## Removal criteria

- The five thin agents (`crux-memory-dream`, `crux-memory-rem`, `crux-memory-recall`, `crux-memory-remember`, `crux-memory-forget`) plus `.cursor/agents/templates/recall-canvas.tsx.md` are shipped in the dist zip.
- The consumer upgrade script re-points existing installs at the thin agents.
- One minor release cycle has elapsed since the thin agents shipped so downstream projects have had a chance to upgrade.

Once all three criteria are met, delete this file.

## Shared reference

Shared config keys, User-Input Escalation contract, memory command/skill registry, and cross-skill boundaries live in `.cursor/skills/_memory-shared.md`. Do not re-paste that content — the thin agents link to it directly.

## Ownership

- **Parent orchestrator**: none — this dispatcher exists only to keep the registered name resolvable. Callers should spawn the thin agent from the dispatch table above.
- **Thin agents**: `crux-memory-dream`, `crux-memory-rem`, `crux-memory-recall`, `crux-memory-remember`, `crux-memory-forget`.
