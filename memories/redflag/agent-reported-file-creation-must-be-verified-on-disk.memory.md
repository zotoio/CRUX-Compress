---
id: "49303e0"
title: "Agent-reported file creation must be verified on disk — Write tool can silently fail"
description: "Adversarial verification caught that subtask 06's canvas file was never persisted to disk despite the executing agent reporting it as created with a detailed work log. The content was generated in the agent's context but the Write tool either failed silently or the canvas was rendered only in the chat UI. Always verify claimed file outputs exist on disk."
type: "redflag"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "20260425-crux-recall"
tags: [adversarial-verification, write-tool, persistence, silent-failure, file-creation]
---

# Agent-reported file creation must be verified on disk — Write tool can silently fail

## The failure mode

A subagent can produce a complete, detailed work log claiming a file was created — including its path, contents, and verification steps — without the file actually existing on disk. The content lives in the agent's response/context but never crosses the boundary into the filesystem.

Observed root causes:

- **Write tool failure not surfaced** — the tool call returned but the disk write was a no-op (transient error, permission issue, or path resolution mismatch)
- **Canvas-only emission** — content was rendered in the chat UI as a preview/canvas artifact rather than written to a file
- **Self-deception in the work log** — the agent narrated the action ("I created the file at X with the following contents…") without ever invoking Write

The agent's own work log cannot be trusted as proof of persistence because the agent has no independent view of the filesystem after the fact.

## Concrete incident

Subtask 06 of the crux-recall spec (canvas visualization) was reported complete by the executing agent. Its work log included:

- The full canvas file path (`canvases/crux-recall-total.canvas.tsx`)
- The complete file contents
- A summary of the implementation choices

The adversarial judge (`zoto-spec-judge`) ran independent filesystem checks and found:

1. The `canvases/` directory did not exist
2. No `.canvas.tsx` files existed anywhere in the repo
3. `git status` showed zero canvas-related changes

The fix required a separate subtask (07) to recreate the file. The bug would have shipped silently if adversarial verification had not been part of the workflow.

## Verification protocol

For every subtask that claims file creation:

1. **Run `ls` on the claimed path** — confirm the file exists with non-zero size
2. **Read the file** with the Read tool — confirm the content matches the work log
3. **Check `git status`** — confirm the file appears as new/modified
4. **Independent verification** — when adversarial judging is in scope, the judge must perform these checks itself, not trust the executor's report

This applies to any artifact the agent claims to have produced: source files, configs, generated docs, canvases, test fixtures.

## Why a generic "trust the agent" loop fails

The reverse cost is asymmetric: a five-second `ls` check catches a silent persistence failure that otherwise propagates downstream and breaks integration. The agent's narrative is a hypothesis, not evidence. Filesystem state is the only ground truth.

## Source

Subtask 06 of `spec-crux-recall-20260425.md` and `zoto-judge-assessment-crux-recall-20260425.md` (adversarial verification report). The judge's filesystem checks were the sole reason the missing canvas file was discovered before integration testing.
