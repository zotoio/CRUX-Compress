---
branch: 1
depth: 3
subfocus_index: 5
subfocus: "Config-Driven Behavior Propagation"
parent_subfocus: "Session-Scope State Propagation"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

Config files that multiple agents independently load constitute a "pull" propagation mechanism — an alternative to explicit parent-to-child parameter passing. This narrowing examines the architectural properties, failure modes, and boundaries of config-as-state-propagation, distinguishing it from direct push propagation and session-scope inheritance.

## Discoveries

### Memory ba92c4e — Single-source-of-truth via config keys

The `/crux-remember` command sources its interactive type options directly from `typeTransitions` keys in `.crux/crux-memories.json`. The parent agent definition, the CRUD skill, the extract skill, and the rebalance skill all independently read the same config file and derive the same type list. No agent ever passes `["idea", "learning", "redflag", "core", "goal"]` to another agent — they all pull it from disk.

**Key property**: Adding a sixth type to config propagates to all consumers without any inter-agent communication. The propagation is implicit, zero-coordination, and eventually consistent (all agents see the new state on their next config read).

### Memory 96a7410 — Drift as the primary failure mode

The tooling-defaults-vs-spec drift (20% vs 25% compression target) is the canonical failure of pull propagation. When one consumer hard-codes a value that should come from config, the propagation chain is broken. The drift is silent — no error, no warning, just subtly wrong behavior until someone notices.

**Structural cause**: Pull propagation assumes all consumers actually pull. The moment a consumer caches, hard-codes, or derives a value locally instead of reading the shared source, the single-source-of-truth guarantee breaks.

### Memory b0c02ea — Layered propagation (defaults + overrides)

The plugin system demonstrates a hybrid model: config provides `enabledByDefault` values (pull propagation), but CLI flags (`--plugin X`, `--no-plugin X`) override them (push propagation). This is not pure pull — it's pull-with-override, where explicit signals from the invocation context take precedence over disk-based defaults.

### Codebase evidence — The `.crux/crux-memories.json` consumption graph

From grep analysis, at least 48 files reference `crux-memories.json`. These span:
- **Agent definitions** (memory-manager reads config as its first action)
- **Skills** (CRUD, extract, rebalance, compress, index, reference-tracker — each independently loads and parses config)
- **MCP server** (Python config loader with upward directory walk)
- **Hooks** (session-start, detect-changes, track-references)
- **Evals** (conftest.py generates synthetic config for test isolation)
- **Rules** (crux-memories-integration rule references config path)
- **Commands** (dream, recall, remember, meditate, forget, amnesia)
- **Install script** (generates config during installation)

None of these consumers receive config values from a parent. Each independently reads the file. The MCP server even has a `_find_config()` function that walks up the directory tree — a discovery mechanism, not a handoff.

### Memory ba74013 — Where pull propagation fails

The session-scope subagent patterns memory identifies a critical boundary: session-scope flags (like amnesia mode) **cannot** use pull propagation because they are ephemeral (exist only for the chat session duration, never written to disk). The solution is an alwaysApply rule that encodes the inheritance contract — a form of push propagation where the rule system ensures every agent loads the same behavioral contract, but the actual flag state must be pushed via spawn arguments.

This reveals the fundamental limitation: **pull propagation only works for persistent state**. Anything ephemeral, contextual, or session-scoped cannot be config-driven.

### Memory c35a703 — Config cannot replace contextual awareness

"Default to broadest scope when calling context lacks specificity signals" — config can provide defaults and constraints, but cannot encode the calling context. Agent-scoping decisions require information about which agent is running, what work item is active, and what artifacts are available. This is inherently push-propagated (or self-discovered) state that config cannot pre-encode.

## Connections

### The Push-Pull Spectrum

State propagation in this codebase exists on a spectrum:

| Mechanism | Type | Persistence | Drift Risk | Coordination Cost |
|-----------|------|-------------|------------|-------------------|
| `.crux/crux-memories.json` | Pull | Persistent | Medium (hard-coding breaks it) | Zero |
| alwaysApply rules | Pull (contract) | Persistent | Low (rule is always loaded) | Zero |
| Spawn arguments | Push | Ephemeral | None (explicit handoff) | High (must enumerate) |
| CLI flags / overrides | Push | Ephemeral | None (explicit override) | Medium |
| Session-scope flags | Push via rule | Ephemeral | Medium (rule must be loaded) | Low |

**Insight**: The codebase uses pull propagation for *what* (types, thresholds, paths, feature flags) and push propagation for *when* and *who* (session state, calling context, agent identity). This is not accidental — it reflects a deeper architectural truth about what kinds of state are suitable for each mechanism.

### Config as Coordination-Free Consensus

Pull propagation via config achieves something remarkable: **consensus without coordination**. 48+ consumers agree on the same values without any message passing, event bus, or central coordinator. The file system acts as a shared-nothing data store with last-write-wins semantics. This works because:

1. Config changes are rare (human-initiated, deliberate)
2. All consumers read at startup (no stale caches during a session)
3. The schema is stable (consumers can hard-code their access patterns)

When any of these assumptions breaks, pull propagation degrades:
- Frequent config changes → stale reads between sessions
- Mid-session config edits → inconsistency between long-running agents
- Schema evolution → consumers reading fields that no longer exist

### The Eval Fixture Pattern as Proof of Design

The `conftest.py` `_make_config()` fixture is architecturally significant: tests create a synthetic config, place it at the expected path, and then the code-under-test pulls it normally. This proves the pull propagation contract is clean — any valid config file at the right path produces correct behavior. The test doesn't need to mock injection points or intercept constructor arguments. The file system IS the injection point.

### Prevention Patterns for Drift

From memory 96a7410's compressed CRUX notation:
```
R.prevention{
  1.impl spec→ref spec constant(comment|cfg)
  2.spec default=tool default
  3.test: tool.default==spec.documented
  4.Δspec default→grep hardcoded old val
}
```

These prevention patterns are specifically about maintaining pull propagation integrity:
1. Reference the config, don't duplicate it
2. Make config the canonical source
3. Test that consumers actually read from config
4. When config changes, find consumers that didn't follow the pattern

### Where Disk-Based Config Is NOT the Right Abstraction

Pull propagation via config files is wrong for:
- **Ephemeral state** (session flags, transaction IDs, temporary overrides) — no persistence needed
- **High-frequency state** (per-request context, streaming positions) — file I/O too slow
- **Contextual state** (which agent am I, what's my parent doing) — not knowable at config-write time
- **Security-sensitive state** (API keys, tokens) — config files are readable by all consumers
- **State requiring acknowledgment** (migrations, breaking changes) — pull gives no delivery guarantee

For these, push propagation (spawn arguments, environment variables, in-memory state) is the correct mechanism.

## Summary

Config-driven behavior propagation (pull model) achieves zero-coordination consensus across 48+ independent consumers in this codebase. Its power comes from treating the file system as a shared data store where all agents independently read the same truth. The pattern succeeds for persistent, slowly-changing, schema-stable state (feature flags, thresholds, type definitions, paths). It fails for ephemeral, contextual, or high-frequency state — which is why the codebase uses push propagation (spawn arguments, alwaysApply rules, CLI overrides) for session flags and calling context. The primary failure mode is drift: when a consumer hard-codes rather than reads, the consensus breaks silently. Prevention requires testing that consumers actually pull (memory 96a7410) and sourcing all derivative artifacts from config keys (memory ba92c4e). The hybrid pattern — pull for defaults, push for overrides — seen in the plugin system (memory b0c02ea) represents the mature architecture: config provides the baseline, explicit signals override it.
