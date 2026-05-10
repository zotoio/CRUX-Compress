---
id: "2592516"
title: "Cursor Automation ideas: dependency upgrades, org-wide REM, and ADR enforcement"
description: "Three novel Cursor Automation use-cases that leverage agentic prose understanding + code editing: (1) semantic dependency upgrades that rewrite call sites alongside version bumps, (2) org-wide nightly REM sleep extracting learnings from merged PRs into memory/rules, and (3) living ADR enforcement that detects drift between prose constraints and code on every merge."
type: "idea"
strength: 3
created: 2026-05-03
modified: 2026-05-10
source: "adhoc"
tags: [cursor-automations, dependencies, upgrades, migration, breaking-changes, agentic, codemods, rem-sleep, memory, consolidation, org-wide, rules-promotion, architecture, adr, drift, enforcement, two-way-sync]
consolidated_from: ["1386fcc", "515c010", "e3bed1f"]
---

# Cursor Automation Ideas

Three novel use-cases for Cursor Automations (https://cursor.com/automate) that require the intersection of prose understanding, code edits, and scheduled/event-driven cadence — not achievable with linters, Dependabot, or vanilla cron+LLM approaches.

## 1. Semantic Dependency Upgrades

A Cursor Automation that watches upstream releases via MCP, reads CHANGELOGs and migration guides, and opens a single PR that bumps the version AND migrates breaking call sites.

**Why novel**: Dependabot/Renovate bump a string in `package.json` but cannot read a migration guide and rewrite renamed methods or restructured options. Hand-written codemods migrate but don't coordinate the version bump. Doing both autonomously requires agentic code editing with semantic understanding of the upstream change.

**Trigger**: Release event from npm/PyPI/Maven MCP, or weekly schedule for critical deps.
**Output**: A single "bump + migrate" PR per dependency, with the migration guide linked.

## 2. Org-Wide REM Sleep

A nightly Cursor Automation that walks every repo in the org, extracts durable learnings from merged PRs and review threads, dedupes against the existing memory corpus, and opens per-repo PRs promoting high-strength learnings into permanent `.cursor/rules/`.

**Why novel**: Linters cannot read review prose semantically. A vanilla LLM cron can summarise but cannot reconcile findings against an evolving knowledge base or apply surgical diffs to rules files.

**Trigger**: Nightly schedule, scoped per repo.
**Output**: A "memory consolidation" PR per repo, plus an org-wide Slack digest of newly promoted rules.

**Relationship to this repo**: The `crux-cursor-memory-manager` REM-sleep + Remember loop, lifted out of an interactive session and run unattended.

## 3. Living ADR Enforcement

A Cursor Automation that diffs merged PRs against prose constraints in `docs/adr/*.md` and either fixes the drift in code or amends the ADR with a "superseded by…" note, plus a quarterly architectural health report.

**Why novel**: AST-based linters cannot interpret prose ADRs. A static cron+LLM can flag drift but only an agent with repo write access can close the loop by correcting code or updating the doc. The two-way feedback (code → doc, doc → code) is unique to a tool that owns the whole IDE/PR surface.

**Trigger**: `pull_request_merged` event for code-and-ADR loop; quarterly schedule for health report.
**Output**: Drift-fix PR or ADR-amendment PR per violation; quarterly health report.

## Common Thread

All three follow a closed-loop pattern: observe → reason against prose → mutate code or docs → report back via MCP-connected channels. Single-purpose tools cover one or two legs but never the full circuit.

## Source

All three generated as adhoc memories (2026-05-03) exploring novel Cursor Automation use-cases.
