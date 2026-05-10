---
branch: 1
depth: 2
subfocus_index: 2
subfocus: "Session-Scope State Propagation"
parent_subfocus: "State Coordination and Handoff Mechanisms"
timestamp: 2026-05-09T19:41:00+10:00
---

## Subfocus Rationale

State propagation is the invisible infrastructure of multi-agent orchestration. While file-based coordination (sibling subfocus 1) handles explicit data exchange and serialization formats (sibling subfocus 3) handle structure, this subfocus examines the implicit channels: how does a child agent come to share its parent's understanding of flags, configuration, and behavioral contracts? The parent context identified this as a rich area because the memory corpus contains several interconnected memories (ba74013, d5e503c, ba92c4e, d944d7c, b0c02ea) that together describe a layered propagation architecture unique to LLM agent systems.

## Discoveries

### The Three-Question Framework for Inheritance Contracts

Memory ba74013 provides the foundational framework that every session-flag spec must answer:

1. **What do subagents inherit?** — Define the subset of behaviors that propagate. Default to "all" unless scoped narrower.
2. **What breaks inheritance?** — Enumerate explicit user actions that override inherited state. Direct invocation should always be honored.
3. **Where is the contract documented?** — Place it in an `alwaysApply: true` rule so every parent and subagent loads the same contract.

This framework is deceptively simple but architecturally powerful. It forces spec authors to make inheritance explicit rather than hoping it happens implicitly.

### The Push-Pull Propagation Taxonomy

Analysis of the codebase reveals two fundamentally different propagation models operating simultaneously:

| Mechanism | Model | Suitable For | Failure Mode |
|-----------|-------|-------------|-------------|
| `.crux/crux-memories.json` | Pull | Persistent thresholds, types, paths, feature flags | Hard-coding breaks consensus |
| `alwaysApply: true` rules | Pull (broadcast) | Behavioral contracts that span all agent types | Missing flag → silent non-propagation |
| Spawn-time arguments | Push | Ephemeral state, session flags, calling context | Must be enumerated in every spawn |
| CLI flags / overrides | Push | User-initiated overrides of defaults | Only reaches the invoked command |
| Phase-block ordering | Implicit | Override precedence within a loaded rule | Misordering → LLM misinterpretation |

The key insight: pull propagation achieves zero-coordination consensus for persistent state, while push propagation is required for ephemeral and contextual state. The codebase uses pull for "what" (values) and push for "when/who" (session context, agent identity).

### Override Precedence as Serialized Position

Memory d5e503c reveals that within a single propagated rule, override precedence is encoded as block ordering — highest-precedence first. The amnesia rule demonstrates: `Φ.amnesia (override) → Φ.enabled (default) → Φ.disabled (off)`. This is not merely a convention; it exploits the sequential nature of LLM attention: top-down reading order influences which directive is most salient.

### Config as Coordination-Free Consensus

`.crux/crux-memories.json` is consumed by 48+ files across agents, skills, MCP server, hooks, evals, rules, commands, and the installer. None receive config values from a parent — each independently reads the file. This achieves consensus without coordination, with the file system as the shared data store. The pattern works because config changes are rare, consumers read at startup, and the schema is stable.

### Command-Family Expansion as Propagation Maintenance

Memory 00a6d09 identifies a propagation maintenance burden: when new commands join a family, override exception lists in alwaysApply rules must be updated. The amnesia rule's exception list exists in three files (command, source rule, compressed rule). A missed update causes real behavioral suppression of the new command — not a documentation gap, but a propagation failure.

## Connections

### The alwaysApply ↔ Environment Variable Isomorphism

The `alwaysApply` mechanism maps precisely onto Unix process inheritance:
- `alwaysApply: true` = `export VAR=value` (all children inherit automatically)
- Agent file = binary-specific config (only that executable reads it)
- Command file = command-line argument (only the invoked process sees it)
- Non-applied rule = file on disk (accessible but never automatically read)

This isomorphism suggests that well-understood patterns from process management — explicit export, auditable inheritance chains, enumerated overrides — translate directly to agent orchestration.

### The Bootstrapping Paradox (Resolved at Infrastructure Level)

A child must load the inheritance rule before it can know the rule exists. The Cursor IDE resolves this by operating at the infrastructure layer: it scans `.cursor/rules/` for `alwaysApply: true` frontmatter and injects matching rules into the system prompt before the agent processes its first token. The bootstrapping problem would resurface if rule loading were agent-driven, but the IDE pre-empts it.

A secondary bootstrap chain exists: `_CRUX-RULE.mdc` (always-applied) instructs the agent to load `CRUX.md` → agent can then interpret CRUX notation in other always-applied rules. This is a two-stage bootstrap where the IDE handles stage one and the agent handles stage two.

### Broadcast Cost vs. Inheritance Completeness

Every `alwaysApply` rule consumes tokens in every agent context. The repository has ~7 always-applied rules. Adding more ensures inheritance completeness but degrades every agent's available context budget. CRUX compression partially resolves this tension: the memories integration rule achieves 55% token reduction in its `.crux.mdc` form. The compressed broadcast channel is the system's answer to the inherent cost of universal propagation.

### The Knows-vs-Acts Gap as the Fundamental Challenge

The most profound discovery is that propagation mechanisms are necessary but not sufficient. Loading a rule (knowing) does not guarantee behavioral compliance (acting). Three forms of this gap were identified:

1. **Attention competition**: Multiple MUST directives in the same rule compete. The amnesia rule contains both "MUST suppress" and "MUST annotate" — the conditional logic determining which applies depends on the LLM correctly parsing natural-language precedence.
2. **Negative assertion weakness**: Testing that a child *didn't* use memories (amnesia compliance) requires negative assertions, which are inherently ambiguous — success could mean correct suppression or irrelevant memories.
3. **Self-report unreliability**: Agents can claim compliance without achieving it (the canvas-file incident, memory 49303e0).

The only reliable detection mechanism is observability of effects: filesystem state, tracker file updates, annotation presence/absence. A compliance testing pyramid emerges from weakest to strongest: directive → self-report → output-pattern → side-effect → adversarial verification.

## Child Subfocuses

Three depth-3 branches explored narrower threads:

1. **The alwaysApply Rule as an Inheritance Vehicle** (sub-4) — Why `alwaysApply: true` is the sole reliable inheritance mechanism: command files fail (invocation-scoped), agent files fail (type-scoped), non-applied rules fail (heuristic-scoped). Fragility surfaces include silent flag omission, stale exception lists, phase-block misordering, and no verification mechanism for "all contracts have alwaysApply."

2. **Config-Driven Behavior Propagation** (sub-5) — How `.crux/crux-memories.json` achieves zero-coordination consensus across 48+ consumers via pull propagation. Succeeds for persistent, slowly-changing state; fails for ephemeral, contextual, or high-frequency state. The primary failure mode is drift when consumers hard-code instead of reading config. Prevention requires testing that consumers actually pull (96a7410) and sourcing derivatives from config keys (ba92c4e).

3. **The Knows-vs-Acts Gap** (sub-6) — The fundamental disconnect between loading a directive and complying with it. Observability of effects (not intentions) is the only reliable bridge. Identified a compliance testing pyramid (directive < self-report < output-pattern < side-effect < adversarial verification) and the attention competition model where spawn-time prompts and alwaysApply rules compete for behavioral influence.

## Child Insights

### From sub-4 (alwaysApply as Inheritance Vehicle)

The rule-loading taxonomy is architecturally definitive: `alwaysApply` is the only mode where the IDE (not the agent) guarantees universal injection. This solves the bootstrapping problem at the infrastructure layer. The fragility surface is real but bounded — silent flag omission, exception list staleness, and phase-block misordering are all detectable by audits. The broadcast-cost tension (more rules = less context budget per agent) is partially resolved by CRUX compression but creates an implicit ceiling on how many behavioral contracts can be propagated.

### From sub-5 (Config-Driven Propagation)

The push-pull spectrum is the most clarifying framework. Pull propagation (config files) achieves coordination-free consensus but only works for persistent state. Push propagation (spawn arguments, CLI flags) is required for ephemeral state but scales poorly (every spawn must enumerate). The hybrid pattern — pull for defaults, push for overrides — seen in the plugin system (b0c02ea) represents the mature architecture. The eval fixture pattern (`conftest.py` creating synthetic config at the expected path) proves the pull contract is clean: the filesystem IS the injection point.

### From sub-6 (The Knows-vs-Acts Gap)

The dual-MUST conflict in the amnesia rule is a concrete instance of the gap: two MUST directives in the same loaded rule compete, and the conditional logic depends on LLM attention dynamics. The reference tracking hook provides partial observability (detecting annotation presence) but cannot detect annotation absence (agent influenced by memory but didn't annotate). The hallucination redflag (3bf625d) generalizes the gap beyond state propagation: any behavioral constraint is subject to the same knows-vs-acts failure mode.

## Summary

Session-scope state propagation in this codebase operates through a layered architecture with two primary models: **pull propagation** (shared config files read independently by all agents, achieving zero-coordination consensus for persistent state) and **push propagation** (alwaysApply rules for behavioral contracts, spawn-time arguments for ephemeral state). The three-question framework (what inherits, what breaks inheritance, where is the contract) from memory ba74013 provides the design discipline, while override precedence is encoded through phase-block ordering within rules (d5e503c).

The `alwaysApply: true` mechanism is isomorphic to Unix environment variable export — the sole reliable broadcast channel because the IDE (not the agent) guarantees injection. Its fragility lies in silent degradation: a missing flag, a stale exception list, or misordered phase blocks break inheritance without error signals. Config-driven pull propagation achieves remarkable coordination-free consensus across 48+ consumers but fails for ephemeral and contextual state.

The deepest finding is the **knows-vs-acts gap**: propagation mechanisms ensure agents *load* directives, but compliance depends on LLM attention dynamics, conditional parsing accuracy, and the competition between multiple MUST directives. The only reliable bridge is observability of effects — filesystem checks, tracker state, output-pattern analysis — structured as a compliance testing pyramid from weakest (directive trust) to strongest (adversarial verification). The current system operates at levels 1-3; advancing critical propagation checks to levels 4-5 would close the gap between "the parent knows X" and "the child acts on X."
