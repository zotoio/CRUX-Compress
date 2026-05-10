---
id: "515c010"
title: "Org-wide REM sleep automation for cross-repo memory consolidation"
description: "Nightly Cursor Automation that walks every repo in the org, extracts durable learnings from merged PRs and review threads, dedupes against the existing memory corpus, and opens per-repo PRs promoting high-strength learnings into permanent .cursor/rules/."
type: "idea"
strength: 1
created: 2026-05-03
modified: 2026-05-03
source: "adhoc"
tags: [cursor-automations, rem-sleep, memory, consolidation, org-wide, agentic, rules-promotion]
---

# Org-wide REM sleep automation for cross-repo memory consolidation

## Context

Generated as a novel use-case for Cursor Automations (https://cursor.com/automate) — specifically one not easily achievable with cron jobs, GitHub Actions, Dependabot, or rule-engine bots, because it requires combining prose understanding, code edits, and a stable scheduled cadence.

## Idea

A nightly Cursor Automation that:

1. Walks every repo in the org.
2. Reads merged PRs and their review threads.
3. Extracts durable learnings (red flags, patterns, gotchas).
4. De-duplicates them against an existing memory corpus.
5. Opens a PR per repo that promotes high-strength learnings into permanent `.cursor/rules/`.

## Why it's novel

- Linters and `release-please`-style bots cannot read review prose semantically.
- A vanilla LLM cron can summarise but cannot reconcile new findings against an evolving knowledge base nor apply a surgical diff to the rules file.
- Cursor Automations sit at the intersection where prose understanding, code edits, and a stable scheduled cadence all live.

## Trigger and output

- **Trigger**: nightly schedule, scoped per repo.
- **Output**: a "memory consolidation" PR per repo, plus an org-wide Slack digest of newly promoted rules.

## Relationship to this repo

Essentially the `crux-cursor-memory-manager` agent's REM-sleep + Remember loop, lifted out of an interactive session and run unattended. Related to the existing memory `memories/idea/reverse-engineer-specs-for-traceability.memory.md`.
