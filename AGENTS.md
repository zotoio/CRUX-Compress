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
| `integrity-expert` | `.cursor/agents/integrity-expert.md` | Code quality audits, test coverage, security, CI/CD |
| `docs-sync-agent` | `.cursor/agents/docs-sync-agent.md` | Documentation synchronization on source changes |
| `crux-cursor-memory-manager` | `.cursor/agents/crux-cursor-memory-manager.md` | Memory lifecycle management (dream, REM sleep, Recall, Forget, Remember, Meditate) |
| `crux-platform-architect` | `.cursor/agents/crux-platform-architect.md` | Platform architecture, Cursor/LLM harness design, documentation, and eval strategy |
| `crux-software-engineer` | `.cursor/agents/crux-software-engineer.md` | Core implementation — Python, shell, MCP server, hooks, skills, and evals |

### Spec Execution — Agent Allocation

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
| Code quality audits, security reviews, CI/CD checks | `integrity-expert` |
| Documentation sync after source changes | `docs-sync-agent` |

**Do not default to `generalPurpose`** — every subtask in a spec should map to the most appropriate CRUX agent above.

### Spec System commands (`zoto-spec-system` plugin)

This repository wires up the [`zoto-spec-system`](https://github.com/zotoio/zoto-agents/tree/main/plugins/zoto-spec-system) Cursor plugin via `.zoto-spec-system/config.json`. When the plugin is installed, these commands are available:

- `/zoto-spec-create` — Create a structured spec under `specs/[yyyymmdd]-[feature-name]/`.
- `/zoto-spec-judge` — Independent assessment of a spec or the repo. Offers to apply fixes.
- `/zoto-spec-execute` — Run a spec with subagent coordination and adversarial verification.

Configuration:
- `unitOfWork=spec`, `specsDir=specs`, `workDir=specs/current`.
- `extensions.memory.enabled=true` with `plugin=crux-memories` — the CRUX memory commands (`/crux-dream`, `/crux-recall`, `/crux-forget`, `/crux-meditate`) integrate with the spec lifecycle.

See [`docs/zoto-spec-system.md`](docs/zoto-spec-system.md) for installation and daily-workflow details. Existing examples: `specs/20260406-crux-forget/`, `specs/20260425-crux-recall/`.

