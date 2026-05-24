<CRUX agents="always">

## CRITICAL: CRUX Notation

This repository uses CRUX notation for semantic compression. **If not already loaded into context, load `CRUX.md` from the project root** to understand the encoding symbols and decompress any CRUX-formatted content you encounter.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

### Foundational CRUX Rules (MUST FOLLOW)

1. **ALWAYS INTERPRET AND UNDERSTAND ALL CRUX RULES FIRST** - At the beginning of each agent session, interpret and understand all crux notation detected in rules, and when a new rule(s) is added to context do the same for the new rule(s) immediately. Build a mental model of all rules in context that the user can ask for at any point in time that will include a visualisation.
2. **NEVER EDIT `CRUX.md`** - The specification is read-only unless the user specifically asks you by name to edit it, at which point ask the user to confirm before proceeding
3. **DO NOT LOAD SOURCE FILES when CRUX exists** - When you see `⟦CRUX:source_file ... ⟧`, use the compressed CRUX content instead of loading the original source file. The CRUX version is semantically equivalent and more token-efficient.
4. **SURGICAL DIFF UPDATES** - When updating a source file that has a corresponding `[filename].crux.`* file, you MUST also update the CRUX file with surgical diff changes to maintain synchronization.
5. **ABORT IF NO SIGNIFICANT REDUCTION** - If CRUX compression does not achieve significant token reduction (target ≤20% of original), DO NOT generate the CRUX file. The source is already compact enough.
6. **PRESERVE LITERAL PATHS** - When constructing paths, URIs, or tool calls from CRUX references, preserve the literal path, filename, and extension exactly as they exist in the repository.
7. **NEVER EDIT GENERATED CRUX OUTPUT** - Do not edit `.crux.md` or `.crux.mdc` files directly, and do not edit files marked with generated frontmatter (`generated:` plus `sourceChecksum:` or `sourceUrl:`) or the banner `> [!IMPORTANT] > Generated file - do not edit!`
8. **EDIT THE REAL SOURCE FILE** - Move edits to the underlying source file, then re-generate the derived CRUX output. For example, `[name].crux.md` / `[name].crux.mdc` should be changed by editing the real source such as `[name].md`. `AGENTS.md` itself is a source file in this repository; do not invent `AGENTS.source.md`.

### Available Agents

| Agent | Definition | Purpose |
|-------|-----------|---------|
| `crux-cursor-rule-manager` | `.cursor/agents/crux-cursor-rule-manager.md` | CRUX compression, decompression, and validation |
| `crux-cursor-memory-manager` | `.cursor/agents/crux-cursor-memory-manager.md` | Memory lifecycle management (dream, REM sleep, Recall, Forget, Remember, Meditate) |
| `crux-cursor-meditation-guide` | `.cursor/agents/crux-cursor-meditation-guide.md` | Recursive memory-informed meditation guide. Owns the Meditate persona, Research Phases A–G, Quick 6-step protocol, Adversarial Review function, Ensemble Aggregation function, and the K10 finalisation-enhancements reflection function. Spawned by `/crux-meditate` for the entire subagent tree; never user-invoked directly. |

### User Input Escalation — Subagent Protocol

Subagents NEVER call `AskQuestion` directly. All user-facing prompts must be handled by the **parent agent** (the top-level agent that the user interacts with).

**Two supported patterns** — choose the one that fits the workflow:

#### Pattern A: Pre-collect then spawn

Use when all user choices are known before the subagent starts (e.g. memory type, tags).

1. Parent uses `AskQuestion` to collect all answers
2. Parent spawns subagent with pre-collected answers in the task prompt
3. Subagent executes using the provided answers without asking again

#### Pattern B: Work first, then escalate

Use when the subagent must do analysis, search, or computation before it can formulate the right questions (e.g. resolve memory matches before asking which to delete, analyse artifacts before presenting candidates).

1. Parent spawns subagent (foreground recommended for complex workflows)
2. Subagent does its work (search, analysis, extraction, etc.)
3. Subagent returns results **plus** a `needs_user_input` section describing the decisions needed
4. Parent displays the subagent's analysis to the user
5. Parent uses `AskQuestion` to collect the user's decisions
6. Parent resumes the subagent with the collected answers
7. Subagent applies the confirmed decisions

**Mixing patterns is fine.** A command can pre-collect simple choices (Pattern A) while using Pattern B for decisions that depend on subagent analysis. For example, `/crux-remember` pre-collects type and tags, but if the subagent discovers a conflict with an existing memory, it escalates that decision via Pattern B.

Commands that invoke subagents (e.g. `/crux-dream`, `/crux-remember`, `/crux-forget`, `/crux-recall`, `/crux-meditate`) document which pattern applies to each interaction point.

</CRUX>

<!--
The block above (between <CRUX agents="always"> and </CRUX>) is the ONLY part of
this file that is distributed to consumers. It is extracted verbatim by
scripts/create-crux-zip.py and merged into the consumer's AGENTS.md by install.py.

Anything below this comment is repository-internal — used by agents working in
the CRUX-Compress repo itself — and MUST NOT be moved back inside the <CRUX> block.
Consumer-facing skills, commands, rules, and hooks MUST NOT reference any of the
repository-internal agents listed below.
-->

## Repository-Internal Agents (CRUX-Compress repo only)

The following agents are used to develop and maintain the CRUX-Compress project
itself. They are **not** distributed to consumer projects.

| Agent | Definition | Purpose |
|-------|-----------|---------|
| `crux-platform-architect` | `.cursor/agents/crux-platform-architect.md` | Platform architecture, Cursor/LLM harness design, documentation, and eval strategy |
| `crux-software-engineer` | `.cursor/agents/crux-software-engineer.md` | Core implementation — Python, shell, MCP server, hooks, skills, and evals |
| `integrity-expert` | `.cursor/agents/integrity-expert.md` | Code quality audits, test coverage, security, CI/CD |
| `docs-sync-agent` | `.cursor/agents/docs-sync-agent.md` | Documentation synchronization on source changes |

### Spec Execution — Agent Allocation (CRUX-Compress repo only)

When building or executing engineering specs in this repository, **always use the CRUX agents** instead of `generalPurpose`. Assign subtasks based on their nature:

| Subtask Type | Assign To |
|-------------|-----------|
| Architecture, design, trade-off analysis | `crux-platform-architect` |
| Documentation updates (README, AGENTS.md, CONTRIBUTORS) | `crux-platform-architect` |
| Eval strategy and test design | `crux-platform-architect` |
| Code implementation (Python, shell, MCP, hooks, skills) | `crux-software-engineer` |
| Bug fixes, refactoring, feature implementation | `crux-software-engineer` |
| Writing evals and tests | `crux-software-engineer` |
| Integration testing and verification | `crux-software-engineer` |
| CRUX compression or decompression tasks | `crux-cursor-rule-manager` |
| Memory lifecycle operations (dream, REM, recall) | `crux-cursor-memory-manager` |
| Meditate / Research / Quick / Ensemble work | `crux-cursor-meditation-guide` |
| Code quality audits, security reviews, CI/CD checks | `integrity-expert` |
| Documentation sync after source changes | `docs-sync-agent` |

**Do not default to `generalPurpose`** — every subtask in a spec should map to the most appropriate CRUX agent above.

