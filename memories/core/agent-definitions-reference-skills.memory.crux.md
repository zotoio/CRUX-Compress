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
compressed: true
compressionTarget: 33
beforeTokens: 180
afterTokens: 55
reducedBy: 69%
compressedDate: 2026-04-05
sourceArchive: .ai-ignored/memories/sources/20260405/agent-definitions-reference-skills.memory.md
---

⟦CRUX:memory
E.agent{.cursor/agents/*.md}
R.focus{orchestration; skill invocation order; decision points; user interaction; coordination}
P.¬{detailed op logic→skill; file format specs→skill|spec; impl details that drift}
Ω{skill=source of truth; agents=focused+readable; Δlogic→skill only; ¬drift}
⟧
