---
id: "1386fcc"
title: "Semantic dependency upgrades that rewrite call sites, not just bump versions"
description: "Cursor Automation that watches upstream releases via MCP, reads CHANGELOGs and migration guides, and opens a single PR that bumps the version AND migrates breaking call sites."
type: "idea"
strength: 1
created: 2026-05-03
modified: 2026-05-03
source: "adhoc"
tags: [cursor-automations, dependencies, upgrades, migration, breaking-changes, agentic, codemods]
---

# Semantic dependency upgrades that rewrite call sites, not just bump versions

## Context

Generated as a novel use-case for Cursor Automations (https://cursor.com/automate) — addresses the gap left by Dependabot/Renovate, which bump-without-fix, and bespoke codemods, which fix-without-bump.

## Idea

A Cursor Automation that:

1. Watches upstream releases via a GitHub or npm MCP.
2. For each major bump, fetches the CHANGELOG and migration guide.
3. Runs the codebase against the new API surface, detects breakages, and rewrites call sites (renamed methods, restructured options objects, removed types, etc.).
4. Opens a single PR that bumps the version AND migrates usage, with the migration guide cited in the PR body.

## Why it's novel

- Dependabot/Renovate change a string in `package.json`; they cannot read a library's CHANGELOG, locate breaking call sites, and rewrite them.
- Hand-written codemods migrate but do not coordinate the version bump or read prose migration guides.
- Doing both autonomously requires agentic code editing across the repo with semantic understanding of the upstream change.

## Trigger and output

- **Trigger**: release event from npm/PyPI/Maven MCP, or weekly schedule for selected critical deps.
- **Output**: a single "bump + migrate" PR per dependency, with the migration guide linked.
