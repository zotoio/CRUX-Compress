---
id: "f8bdc0d"
title: "Agent definitions should reference skills for operations, not duplicate spec content"
description: "Agent markdown files should be orchestration-focused — describing when to invoke which skill, decision points, and user interaction patterns. Detailed operation logic belongs in skill SKILL.md files. This separation keeps agents maintainable and avoids spec drift between agent and skill documentation."
type: "core"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [agents, skills, architecture, maintainability]
---

Agent definition files (`.cursor/agents/*.md`) should focus on:

- **Orchestration**: Which skills to invoke and in what order
- **Decision points**: When to branch, escalate, or ask the user
- **User interaction**: How to present information, ask for confirmation
- **Coordination**: How multiple skills work together in a workflow

Agent definitions should NOT contain:

- Detailed operation logic (belongs in skill SKILL.md)
- File format specifications (belongs in skill or spec docs)
- Implementation details that would need updating if the skill changes

This separation ensures that:
1. Skills are the single source of truth for operation details
2. Agents stay focused and readable
3. Updates to operation logic only need to change the skill file
4. No drift between what the agent says and what the skill does
