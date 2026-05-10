---
id: "e3bed1f"
title: "Living architecture-decision enforcement via PR-time drift detection"
description: "Cursor Automation that diffs merged PRs against prose constraints in docs/adr/*.md and either fixes the drift in code or amends the ADR with a superseded-by note, plus a quarterly architectural health report."
type: "idea"
strength: 1
created: 2026-05-03
modified: 2026-05-03
source: "adhoc"
tags: [cursor-automations, architecture, adr, drift, enforcement, agentic, two-way-sync]
---

# Living architecture-decision enforcement via PR-time drift detection

## Context

Generated as a novel use-case for Cursor Automations (https://cursor.com/automate) — closes the loop between ADRs and code, which usually drift apart within a quarter on most teams.

## Idea

A Cursor Automation that:

1. On every merged PR, diffs the changed code against prose constraints in `docs/adr/*.md` (e.g., "no direct DB access from controllers", "all external calls go through `lib/clients/`").
2. If a violation is detected, opens a follow-up PR that either:
   - **Fixes the drift** in code, or
   - **Amends the ADR** with a "superseded by …" note linking the originating PR.
3. Emits a quarterly "architectural health" report into a canvas/Slack channel showing which ADRs are decaying.

## Why it's novel

- AST-based linters can encode rules but cannot interpret prose ADRs, and rewriting an ADR is a documentation task no linter touches.
- A static cron + LLM can flag drift but only an agent with repo write access can close the loop by either correcting the code or updating the doc.
- The two-way feedback (code → doc, doc → code) is unique to a tool that owns the whole IDE/PR surface.

## Trigger and output

- **Trigger**: `pull_request_merged` event for code-and-ADR loop; quarterly schedule for the health report.
- **Output**: drift-fix PR or ADR-amendment PR per violation; quarterly health report.

## Common thread with sibling memories

Closed-loop pattern: observe → reason against prose → mutate code or docs → report back via MCP-connected channels. Single-purpose tools cover one or two legs but never the full circuit.
