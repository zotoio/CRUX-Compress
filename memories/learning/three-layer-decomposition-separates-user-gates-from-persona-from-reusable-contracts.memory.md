---
id: "002dfa7"
title: "Three-layer decomposition separates user gates from persona from reusable contracts"
description: "When a command grows beyond ~300 lines with multiple modes and complex subagent contracts, decompose into three layers: a thin coordinator command (owns argument parsing, user gates, AskQuestion), a dedicated agent (owns persona, mode routing, executable contracts), and a family of loadable skills (own reusable mechanical protocols)."
type: "learning"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260517-meditate-agent-skill-decomposition"
tags: [architecture, decomposition, command-design, skills, agents, separation-of-concerns, meditate, askquestion-boundary]
---

When a command file grows beyond ~300 lines with multiple modes, complex subagent contracts, and user-facing gates, decompose into three layers:

1. **Thin coordinator command** — owns argument parsing, mode flag detection, every `AskQuestion` call (depth selection, cost acknowledgment, theme preflight, facet confirmation, continuation menu), ensemble orchestration loop, and post-tree steps. This is the only layer that interacts with the user.
2. **Dedicated agent** — owns the persona prologue, mode router, comprehensiveness invariants, and `needs_user_input` envelope schema. Spawned via `Task` by the coordinator. Never calls `AskQuestion` — returns `needs_user_input` when it hits a decision point (Pattern B).
3. **Skill family** — each skill owns a reusable mechanical protocol (research phases, quick protocol, adversarial review, report generation, coordination conventions, ensemble aggregation). Loaded by name on demand by the agent. The agent is the primary consumer, but other future agents could reuse individual skills.

The dividing line between command and agent layers is the `AskQuestion` boundary: everything that requires user interaction stays in the command; everything that runs autonomously moves to the agent. This boundary is structural, not arbitrary — it reflects the Cursor subagent model's constraint that tree subagents cannot reliably call `AskQuestion`.

## Quantified results from the meditate decomposition

The `/crux-meditate` command grew to 2,142 lines with the meditate contract duplicated between the command file and `crux-cursor-memory-manager.md` (1,388 lines). The duplication was a drift risk — when the richness spec (20260523) added 13 new surfaces, both files had to be updated in lockstep.

After decomposition:
- **Command file**: 2,142 → 1,020 lines (52% reduction)
- **Memory-manager agent**: 1,392 → 352 lines (75% reduction) — now cleanly focused on Dream / REM / Recall / Remember / Forget
- **New guide agent**: 495 lines (within ≤500 budget)
- **6 new skills**: 2,155 total lines (research: 678, quick: 238, ensemble: 346, review: 276, report: 344, coordination: 273)
- **Contract preservation**: 41/41 frozen-contract items verified PRESENT post-refactor
- **Eval coverage**: 353/353 pytest + 48 vitest passing, 12 new pytest classes + 4 new TS describe blocks

The memory manager (`crux-cursor-memory-manager`) became a focused lifecycle agent. The meditate workflow now lives in `crux-cursor-meditation-guide` and its 6 meditation skills.

## When to apply

- Any command file approaching or exceeding 300 lines with multiple modes
- Any agent file that hosts a large workflow alongside other unrelated lifecycle modes
- Any situation where the same contract is duplicated between a command and an agent (drift risk)
- The `skill-and-agent-references` workspace rule's 300-line threshold is validated by this decomposition

## Generalisation

The pattern is not meditate-specific. Any multi-mode command benefits from this split:
- The coordinator handles "what does the user want?" (mode selection, cost acknowledgment, confirmations)
- The agent handles "how do we do it?" (persona, orchestration, mode routing)
- The skills handle "what are the reusable mechanical steps?" (protocols, contracts, templates)
