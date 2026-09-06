<CRUX agents="always">

## CRITICAL: CRUX Notation

This repository uses CRUX notation for semantic compression. **Interpret CRUX rules already in your context** (this file, `_CRUX-RULE.mdc`, any `⟦CRUX:…⟧` block) as your working symbol primer. **Only load the full `CRUX.md` specification when your current task compresses, decompresses, authors, or validates CRUX notation** — routine work does not need it.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

### Foundational CRUX Rules (MUST FOLLOW)

1. **ALWAYS INTERPRET AND UNDERSTAND CRUX RULES ALREADY IN CONTEXT FIRST** - At the beginning of each agent session, interpret and understand all crux notation detected in rules already loaded, and when a new rule is added to context do the same immediately. Build a mental model the user can ask for at any point that includes a visualisation. **Load `CRUX.md` only when the current work touches CRUX notation** (compressing, decompressing, authoring, or validating); otherwise rely on the CRUX block in this file plus `_CRUX-RULE.mdc`.
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
| `crux-cursor-rule-manager` | `.cursor/agents/crux/crux-cursor-rule-manager.md` | CRUX compression, decompression, and validation |
| `crux-memory-dream` | `.cursor/agents/crux/crux-memory-dream.md` | Dream-mode memory extraction — ranks candidate facts from a completed unit of work, detects conflicts, flags resolved-bug redflags. Spawned by `/crux-dream <spec-name>`. |
| `crux-memory-rem` | `.cursor/agents/crux/crux-memory-rem.md` | REM Sleep memory rebalancer — corpus-wide consistency, conflicts, promote/demote/archive/consolidate/compress recommendations. Spawned by `/crux-dream --rem` (and by `/crux-recall` when the user selects "Consolidate"). |
| `crux-memory-recall` | `.cursor/agents/crux/crux-memory-recall.md` | Read-only memory query and display. Decompresses CRUX bodies on the fly and generates the interactive Canvas visualisation on `--total` using the template at `.cursor/agents/crux/templates/recall-canvas.tsx.md`. Spawned by `/crux-recall`. |
| `crux-memory-remember` | `.cursor/agents/crux/crux-memory-remember.md` | Ad-hoc memory creation with parent-collected type/tags/description. Spawned by `/crux-remember`. |
| `crux-memory-forget` | `.cursor/agents/crux/crux-memory-forget.md` | Memory deletion — resolves matches for parent-driven confirmation, then removes files and trackers. Spawned by `/crux-forget` (and by `/crux-recall` when the user selects "Delete"). |
| `crux-cursor-memory-manager` | `.cursor/agents/crux/crux-cursor-memory-manager.md` | (deprecated dispatcher — see `crux-memory-*`; remove after one minor release once thin agents ship in dist). |
| `crux-cursor-meditation-guide` | `.cursor/agents/crux/crux-cursor-meditation-guide.md` | Recursive memory-informed meditation guide. Owns the Meditate persona, Research Phases A–G, Quick 6-step protocol, Adversarial Review function, Ensemble Aggregation function, and the K10 finalisation-enhancements reflection function. Spawned by `/crux-meditate` for the entire subagent tree; never user-invoked directly. |

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

### `context_manifest` — Subagent Prelude

Parent agents may pass a `context_manifest` stanza in the spawn prompt to tell a subagent which foundational files are already resident in the parent's context. When present, the subagent MUST honor it and skip redundant re-reads. When absent, the subagent falls back to today's behavior (unconditional loads governed by its own agent definition).

**Schema** (JSON, embedded verbatim in the task prompt):

```json
{
  "context_manifest": {
    "agents_md": "loaded" | "not_loaded",
    "crux_md":   "loaded" | "not_loaded",
    "memory_config": {
      "path": ".crux/crux-memories.json",
      "loaded": true,
      "flags": {
        "enableMemories": "true" | "false",
        "enableMemoryCompression": "true" | "false"
      }
    },
    "extras": {
      "<well-known-key>": "loaded" | "not_loaded" | "<compact-value>"
    }
  }
}
```

**Field semantics**:

- `agents_md` — if `"loaded"`, do not re-read `AGENTS.md`. The parent has already surfaced it (either via the always-applied rule or a prior explicit read).
- `crux_md` — if `"loaded"`, do not re-read `CRUX.md`. Only meaningful for agents whose work touches CRUX notation; other agents ignore this field.
- `memory_config` — if `loaded: true`, do not re-read `.crux/crux-memories.json`. The `flags` object exposes the two consumer-visible booleans so memory-aware subagents can gate their behavior without a re-read. When the parent has NOT loaded the config, omit `loaded` / `flags` (or set `loaded: false`) and let the subagent read the file per its own contract.
- `extras` — well-known keys the parent can pre-hydrate (e.g. `memory_index`, a compact facet payload). Values may be `"loaded"`, `"not_loaded"`, or a compact literal value (string/number/short object) the subagent should treat as authoritative.

**Sentinel probe (mandatory)**: If a subagent's task prompt asserts `agents_md: "loaded"` but the subagent cannot recall a known load-bearing phrase from `AGENTS.md` (for example, the "Foundational CRUX Rules (MUST FOLLOW)" heading or Pattern A / Pattern B section titles), it MUST re-load `AGENTS.md` and proceed as if the manifest had said `"not_loaded"`. The same probe rule applies to `crux_md` for CRUX-authoring agents (they must recall a symbol table entry or the `⟦CRUX:…⟧` delimiter grammar before trusting `crux_md: "loaded"`).

**Fallback rule (absence)**: If the `context_manifest` stanza is missing from the task prompt entirely, the subagent behaves exactly as documented in its own agent file — including any unconditional loads. Absence of the stanza never triggers an error; it simply preserves today's behavior.

**Producer contract (parent agent)**: If you pass `context_manifest`, populate it accurately for every field you set. Omit fields you cannot vouch for. Never assert `"loaded"` for a file you have not actually read.

**Consumer contract (subagent)**: Check the stanza first. Skip loads marked `"loaded"`. Apply the sentinel probe. Fall back to your default load behavior when the stanza is missing or a field is unset. Do not error on missing fields — treat them as `"not_loaded"`.

**Note**: `context_manifest` is a **descriptive prompt protocol**, not a JSON schema file — enforcement lives in agent obedience to this contract.

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
| Dream extraction from a completed unit of work | `crux-memory-dream` |
| REM Sleep corpus rebalance | `crux-memory-rem` |
| Recall / query / display (read-only, incl. `--total` Canvas) | `crux-memory-recall` |
| Ad-hoc memory creation (`/crux-remember`) | `crux-memory-remember` |
| Memory deletion (`/crux-forget`) | `crux-memory-forget` |
| Meditate / Research / Quick / Ensemble work | `crux-cursor-meditation-guide` |
| Code quality audits, security reviews, CI/CD checks | `integrity-expert` |
| Documentation sync after source changes | `docs-sync-agent` |

**Do not default to `generalPurpose`** — every subtask in a spec should map to the most appropriate CRUX agent above.

