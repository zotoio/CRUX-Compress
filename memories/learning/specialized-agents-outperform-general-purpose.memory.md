---
title: "Specialized agents outperform generalPurpose for narrow domains like documentation sync"
description: "The docs-sync-agent (subtask 14) produced cleaner, more targeted documentation updates than generalPurpose agents on similar tasks in other plans. Specialized agents carry domain context without needing lengthy prompts, reducing token usage and improving output consistency."
type: "learning"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [agents, specialization, documentation, efficiency]
---

The docs-sync-agent was assigned to subtask 14 (documentation updates) and produced notably cleaner output than generalPurpose agents typically do for documentation tasks.

Benefits of specialized agents:
- Domain context is baked into the agent definition, not repeated in every prompt
- Consistent output style across invocations
- Lower token usage per task (no need to explain domain constraints each time)
- Better pattern adherence (e.g., docs-sync-agent follows surgical update rules automatically)

When a domain has clear boundaries and recurring tasks, creating a specialized agent is worth the upfront investment. Good candidates: documentation, code review, test generation, security audits.
