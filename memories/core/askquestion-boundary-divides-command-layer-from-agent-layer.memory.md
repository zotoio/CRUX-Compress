---
id: "998ff24"
title: "The AskQuestion boundary divides command layer from agent layer"
description: "In any command → agent → skill architecture, the AskQuestion boundary defines where the command layer ends and the agent layer begins. Everything requiring user interaction stays in the command/coordinator. Everything that runs autonomously goes to the agent. This boundary is the structural invariant that makes Pattern A / Pattern B work."
type: "core"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260517-meditate-agent-skill-decomposition"
tags: [architecture, askquestion, command-design, agent-design, pattern-a, pattern-b, user-interaction, subagent-model]
---

When decomposing a large command into command + agent + skill layers, the `AskQuestion` boundary is the architectural dividing line:

- **Command layer** (coordinator): everything that requires user interaction — gates, confirmations, menus, approvals, cost acknowledgments. This layer calls `AskQuestion`.
- **Agent layer**: everything that runs autonomously — persona, research, synthesis, review, report generation, ensemble aggregation. This layer NEVER calls `AskQuestion`; it returns `needs_user_input` when it hits a decision point.

This boundary is not a convention — it is a structural requirement of the Cursor subagent model. Tree subagents cannot reliably present interactive prompts to the user. The command/coordinator is the only layer that can call `AskQuestion`.

## Concrete division from the meditate decomposition

**Command layer** (calls `AskQuestion`):
- `Q-Depth-Selection` — user picks exploration depth
- `Q-Cost-and-Richness-Acknowledgment` — user acknowledges cost and scope
- Theme preflight Q1–Q5 — user chooses visual theming
- Facet confirmation `Q-Confirm-1` / `Q-Confirm-2` — user approves derived facets
- `Q-Finalisation-Enhancements` — user selects K10 enhancement types
- Ensemble orchestration — user sees model pool, approves parallel spawn
- Continuation menu — user picks expand / save-spec / end

**Agent layer** (never calls `AskQuestion`):
- Persona prologue and mode routing
- Phases A–G recursive research tree
- Quick 6-step protocol
- Adversarial review-and-fix cycle (≤3 iterations)
- Report generation (paired HTML+PDF)
- Ensemble aggregation cross-model synthesis

When the agent hits a decision point (e.g. adversarial review finds a MUST_FIX issue that requires user judgment), it returns `needs_user_input` with a structured response. The coordinator presents it via `AskQuestion` and resumes the agent with the answer (Pattern B).

## The test

For any section of a command or agent file, ask: **"Does this section need user input to proceed?"**

- **Yes** → command layer
- **No** → agent or skill layer

This test is mechanical and produces consistent results. It also makes the decomposition reversible — if you need to understand why something is in the command vs. the agent, check whether it calls `AskQuestion`.

## Relationship to Pattern A and Pattern B

- **Pattern A** (pre-collected answers): the command gathers all answers via `AskQuestion` before spawning the agent. The agent uses the pre-collected answers directly.
- **Pattern B** (work first, then escalate): the agent does analysis, then returns `needs_user_input`. The command collects the answer via `AskQuestion` and resumes the agent.

Both patterns enforce the same boundary: `AskQuestion` is always on the command side, never inside the agent tree.

## Generalisation

This principle applies to every command → agent decomposition in the project, not just meditate. Any future command that spawns a subagent should place all user-interaction logic in the command and all autonomous logic in the agent. The `AskQuestion` boundary makes this split unambiguous.
