---
id: "6947e29"
title: "Documentation-only decomposition specs need same rigor as code refactors"
description: "Restructuring agent definitions, skill files, and command files — even when no runtime code (Python, shell) changes — requires the same spec discipline as code refactors: frozen contracts, architecture design, eval test plans, phased execution, and integrity reviews."
type: "learning"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260517-meditate-agent-skill-decomposition"
tags: [spec-system, documentation, refactoring, planning-rigor, markdown, agents, skills, agent-definitions]
---

"Documentation-only" changes — restructuring markdown agent definitions, skill SKILL.md files, command files, and associated docs — are sometimes perceived as low-risk because no runtime code changes. This perception is dangerous in a project where agent definitions and skill files are executable specifications that drive agent behaviour at runtime.

## The evidence

The meditate decomposition spec was labelled "documentation-only at the meditate layer" — zero Python changes, zero shell changes, zero runtime code modifications. Despite that label, it required:

| Planning artefact | Scale |
|-------------------|-------|
| Subtasks | 12 across 8 dependency phases |
| Frozen contract | 1,558 lines, 41 verifiable items |
| Architecture design | 300 lines |
| Eval test plan | 1,095 lines |
| Pytest assertions | 353 tests (including 12 new classes) |
| Vitest assertions | 48 tests (including 4 new describe blocks) |
| Distribution audit | 5×7 verification matrix |
| Integrity review | Independent agent, mechanical diff |
| Files touched | ~110 files |
| Lines changed | ~30,000 |

The spec successfully preserved 41/41 contract items with zero functionality loss — but only because it was planned and verified with the same rigor as a code refactor.

## Why documentation refactors carry equivalent risk

In this project, agent definitions (`.cursor/agents/*.md`) and skill files (`.cursor/skills/*/SKILL.md`) are not passive documentation. They are:

- **Executable specifications**: agents read and follow them at runtime
- **Contract surfaces**: eval tests assert on their substring presence
- **Distribution artefacts**: `install.py`, `create-crux-zip.py`, and `dist-manifest.json` must enumerate them
- **Cross-referenced**: commands reference agents, agents reference skills, docs reference all three

Moving a section from an agent file to a skill file is functionally equivalent to moving a function from one module to another. The same risks apply: broken references, lost functionality, stale cross-references, incomplete distribution enumeration.

## The rule

When restructuring agent definitions, skill files, or command files:

1. **Plan it as a spec** with frozen contracts, architecture design, and phased execution
2. **Write eval assertions** for the new structure (not just the old one)
3. **Verify distribution surfaces** enumerate new files
4. **Run an independent integrity review** against the frozen contract
5. **Do not assume** that "no code changes" means "low risk"
