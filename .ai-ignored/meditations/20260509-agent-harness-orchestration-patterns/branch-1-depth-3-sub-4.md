---
branch: 1
depth: 3
subfocus_index: 4
subfocus: "The alwaysApply Rule as an Inheritance Vehicle"
parent_subfocus: "Session-Scope State Propagation"
timestamp: 2026-05-09T19:35:00+10:00
---

## Subfocus Rationale

Among the mechanisms by which session-scope state propagates, `alwaysApply: true` is architecturally singular: it is the only Cursor rule-loading mode that guarantees a child subagent receives the same behavioral contract as its parent without the parent explicitly passing it. This narrowing isolates why alternatives fail, why the mechanism works, and where it remains fragile.

## Discoveries

### 1. The Cursor Rule-Loading Taxonomy (from codebase observation)

Cursor loads rules into an agent's context via three distinct mechanisms, each with different propagation semantics:

| Loading Mode | Trigger | Subagent Visibility | Example in repo |
|---|---|---|---|
| `alwaysApply: true` | Rule file exists in `.cursor/rules/` with this frontmatter | **All contexts** — parent, any subagent type, any mode | `_CRUX-RULE.mdc`, `crux-memories-integration.crux.mdc`, `spec-agent-allocation.md` |
| Agent-requestable (no `alwaysApply`, or `alwaysApply: false`) | IDE determines relevance based on file context or agent type | **Not guaranteed** — only loaded when the IDE judges it relevant | `coding-standards-demo.crux.mdc`, `ignore-example-rules.crux.mdc` |
| Command file (`.cursor/commands/*.md`) | User invokes the slash-command | **Never propagates** — only the invoked agent sees it | `crux-dream.md`, `crux-amnesia.md` |
| Agent file (`.cursor/agents/*.md`) | IDE spawns that specific agent type | **Only that agent type** — a `generalPurpose` subagent never loads `crux-cursor-memory-manager.md` | All agents in `.cursor/agents/` |

**Key insight from memory ba74013**: "Placing the contract in a command file (only loaded on invocation), an agent file (only loaded for that agent type), or a non-applied rule would cause inheritance to fail for arbitrary subagent types."

### 2. Why Commands and Agent Files Fail as Inheritance Carriers

**Command files** are loaded only when the user types the slash-command. They define *how to execute the command*, not ambient behavioral contracts. When a parent agent spawns a `crux-software-engineer` to write code, that child never loads `/crux-amnesia`'s command file — it has no reason to. The amnesia suppression rules living in the command file would be invisible to it.

**Agent files** are loaded only for the matching agent type. The CRUX system has 6 specialized agents. If the amnesia contract lived in `crux-cursor-memory-manager.md`, a `crux-software-engineer` subagent would never see it. The inheritance would work for memory-manager subagents and fail silently for every other type.

**Non-applied rules** (`alwaysApply: false`) rely on IDE heuristics to judge relevance. The IDE might decide a coding-standards rule is relevant when editing a `.ts` file, but there is no guaranteed mechanism to force loading. A session-scope contract that depends on heuristic loading is non-deterministic — it might propagate, or might not.

### 3. The Broadcast Channel Metaphor

`alwaysApply: true` functions as an **implicit broadcast channel**: every agent context in the workspace, regardless of type or invocation path, receives the rule. This is analogous to:

- A Unix environment variable exported to all child processes vs. one passed as a command argument
- A CSS global style vs. a component-scoped style
- A kernel-level syscall filter vs. an application-level check

The amnesia integration rule (`crux-memories-integration.md`) demonstrates the pattern concretely. Its CRUX-compressed form encodes: `subagents→inherit; explicit /crux-dream|recall|remember|meditate|forget→user intent OK`. Every context — parent, `crux-software-engineer`, `generalPurpose`, `integrity-expert` — loads this rule and knows the inheritance contract without any explicit parameter-passing by the parent.

### 4. The Bootstrapping Problem

A child subagent must load the `alwaysApply` rule **before it can know the rule exists**. This is solved by the IDE infrastructure, not by the agent itself:

1. Cursor assembles the context for a new agent (parent or child)
2. It scans `.cursor/rules/` for files with `alwaysApply: true` frontmatter
3. It injects them into the `<always_applied_workspace_rules>` section of the system prompt
4. The agent then "knows" the rule from its first token

This sidesteps the chicken-and-egg problem because the loading mechanism is **external to the agent**. The agent does not decide to load the rule; the IDE forces it. The bootstrapping problem would re-emerge if `alwaysApply` behavior were agent-driven (e.g., "at session start, read all rules and apply them") — but it isn't.

However, the bootstrapping problem *does* apply to **rule content that references other rules**. The `_CRUX-RULE.mdc` rule says "If not already loaded in context, load `CRUX.md`" — this is a secondary bootstrap step that relies on the agent's initiative. If the agent ignores this instruction, it can't decompress CRUX notation in other alwaysApply rules. The system partially mitigates this by making `_CRUX-RULE.mdc` itself always-applied, creating a two-stage bootstrap: IDE injects → agent reads CRUX.md → agent can now interpret everything else.

### 5. The Fragility Surface

The fragility of `alwaysApply` as an inheritance vehicle manifests in several failure modes:

**Silent omission**: If a rule author forgets `alwaysApply: true` in frontmatter, the rule falls into "agent-requestable" mode. No error is raised. Subagents simply don't inherit the contract. The parent agent might still work correctly (it loaded the rule via heuristic relevance), but children won't — creating an inconsistency that's invisible to the parent.

**Exception list staleness** (memory 00a6d09): When new commands join a family, override exception lists in alwaysApply rules must be updated. `/crux-remember` and `/crux-meditate` joining the memory family required updating three separate files. A missed update means the new command gets suppressed — a behavioral bug, not a documentation gap.

**Phase-block ordering sensitivity** (memory d5e503c): Even when the rule is correctly always-applied, the *internal ordering* of its phase blocks affects LLM interpretation. Placing `Φ.amnesia` after `Φ.enabled` risks the LLM applying default memory behavior before recognizing the override. The rule is loaded but potentially misinterpreted.

**No verification mechanism**: There is no eval or CI check that confirms "all rules intended as behavioral contracts have `alwaysApply: true`". A regression (accidentally removing the flag during a rule edit) is undetectable without explicit verification steps in the eval suite (P3 in `USER_EVAL_CHECKLISTS.md` tests the observable behavior but not the mechanism).

**Workspace boundary**: `alwaysApply` only broadcasts within a single workspace. Multi-repo or shared-scope configurations require duplicating rules or relying on the `shared` scope mechanism (currently empty `[]` in config). Cross-workspace inheritance has no broadcast channel.

## Connections

### The alwaysApply ↔ Environment Variable Isomorphism

The pattern mirrors Unix process inheritance precisely:
- `alwaysApply: true` = `export VAR=value` (all children inherit)
- Agent file = binary-specific config (only that executable reads it)
- Command file = command-line argument (only the invoked process sees it)
- Non-applied rule = file on disk (accessible but not automatically read)

This isomorphism suggests that well-understood patterns from process management apply: inheritance should be explicit, overrides should be enumerated, and "what gets inherited" should be auditable.

### Tension: Broadcast Power vs. Context Budget

Every `alwaysApply: true` rule consumes tokens in *every* agent context. The repository currently has 6-7 always-applied rules. Each one taxes every subagent's context window. There's an implicit pressure against adding more — but the inheritance requirement demands it. This creates a design tension: rules must be alwaysApply to propagate, but each additional rule degrades every agent's available context for actual work.

CRUX compression partially resolves this — compressed `.crux.mdc` files achieve 55-84% token reduction while preserving semantic content. The `crux-memories-integration.crux.mdc` achieves 55% reduction. This is the system's answer to the broadcast-cost problem: compress the broadcast payload.

### The "Knows vs. Acts" Boundary

Loading a rule is not the same as obeying it. `alwaysApply` ensures the agent *knows* the contract. Whether it *acts* on it depends on:
1. Rule clarity (phase-block ordering, precedence markers like `≻`)
2. Rule salience (position in the context window, compression quality)
3. Competing instructions (the parent's prompt might contradict the rule)

The eval checklist P3 tests observable behavior ("subagents do NOT use ambient memories") rather than rule-loading verification. This is pragmatically correct but means the test can't distinguish "rule not loaded" from "rule loaded but ignored" — a gap in diagnostic capability.

### Connection to Hook-Based Context Injection

The `sessionStart` hook (`crux-session-start.py`) provides a complementary injection channel: it emits `additional_context` that appears in the session. But hooks fire at session start for the *parent* only — subagents don't trigger a new `sessionStart`. This reinforces why hooks cannot replace `alwaysApply` for inheritance: they have no propagation mechanism to children.

## Summary

`alwaysApply: true` is the sole reliable inheritance vehicle for behavioral contracts across arbitrary subagent types because it is the only rule-loading mode where the IDE — not the agent — guarantees universal injection. Command files fail (invocation-scoped), agent files fail (type-scoped), and non-applied rules fail (heuristic-scoped). The mechanism solves the bootstrapping problem by operating at the infrastructure layer, outside agent control. Its fragility lies in silent degradation: a missing flag, a stale exception list, or a misordered phase block all break inheritance without any error signal. The compressed broadcast channel (CRUX `.crux.mdc`) partially resolves the context-budget tension that broadcast universality creates. The pattern is isomorphic to Unix environment variable inheritance, suggesting that established process-management principles (explicit export, auditable inheritance, enumerated overrides) are directly applicable to agent orchestration.
