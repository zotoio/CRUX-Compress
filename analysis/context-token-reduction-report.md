# Context-Token Reduction Report — Skills, Commands, Agents

**Scope**: Token-cost analysis of `.cursor/agents/`, `.cursor/commands/`, `.cursor/skills/`, the always-applied rules in `.cursor/rules/`, and `AGENTS.md` / `CRUX.md`, with a focus on what these cost during **spec generation** (`/zoto-spec-create`) and **spec execution** (`/zoto-spec-execute`).

**Goal**: High accuracy + lower cost. Recommend changes that reduce tokens loaded into context per session and per subagent spawn, without losing actionable information.

---

## 1. Inventory and current cost

Token estimates use the project's own heuristic (prose ≈ 4 chars/token; we round to ≈ 4.0 chars/token for prose-heavy markdown). Numbers are intentionally rough — they are accurate enough to drive prioritisation decisions.

### 1.1 Always-loaded surface (every session)

| File | Bytes | Lines | Est. tokens | Loaded by |
|------|------:|------:|------:|-----------|
| `AGENTS.md` | 6,341 | 80 | ~1,585 | Cursor system prompt (always) |
| `.cursor/rules/_CRUX-RULE.mdc` | 1,687 | 33 | ~422 | `alwaysApply: true` |
| `.cursor/rules/crux-memories-integration.crux.mdc` | 1,330 | 42 | ~333 | `alwaysApply: true` |
| `.cursor/rules/crux-memories-mcp-context.mdc` | 1,610 | 35 | ~402 | `alwaysApply: true` |
| `.cursor/rules/docs-sync.crux.mdc` | 1,177 | 58 | ~294 | `alwaysApply: true` |
| `.cursor/rules/version-bump.crux.mdc` | 466 | 25 | ~117 | `alwaysApply: true` |
| `.cursor/rules/zip-contents-protection.crux.mdc` | 1,185 | 45 | ~296 | `alwaysApply: true` |
| `.cursor/rules/spec-agent-allocation.md` | 1,458 | 29 | ~365 | `alwaysApply: true` (uncompressed!) |
| Skill descriptions (7×) | ~1,400 | — | ~350 | `agent_skills` block in system prompt |
| **Always-on subtotal** | **~16,654** | **347** | **~4,164** | every turn |

Plus `CRUX.md` (28,190 B / 827 lines / **~7,048 tokens**) which `_CRUX-RULE.mdc` and `AGENTS.md` both **instruct** every agent to load on first turn — so it behaves as always-on for any non-trivial session.

**Effective always-on baseline ≈ 11,200 tokens** before the user message, and before any agent file or skill body is opened. `spec-agent-allocation.md`. `_CRUX-RULE.mdc`. `crux-memories-integration.crux.mdc`. `crux-memories-mcp-context.mdc`. `docs-sync.crux.mdc`. `version-bump.crux.mdc`. `zip-contents-protection.crux.mdc`. `AGENTS.md`. `CRUX.md`.

### 1.2 On-demand surface (loaded per command / per agent spawn)

| Category | File | Bytes | Lines | Est. tokens |
|----------|------|------:|------:|------:|
| Agent | `crux-cursor-memory-manager.md` | 37,434 | 493 | **~9,358** |
| Agent | `crux-cursor-rule-manager.md` | 20,525 | 360 | **~5,131** |
| Agent | `crux-platform-architect.md` | 6,385 | 104 | ~1,596 |
| Agent | `crux-software-engineer.md` | 5,770 | 101 | ~1,442 |
| Agent | `integrity-expert.md` | 6,337 | 213 | ~1,584 |
| Agent | `docs-sync-agent.md` | 3,385 | 89 | ~846 |
| Agent subtotal | — | **79,836** | 1,360 | **~19,957** |
| Command | `crux-compress.md` | 33,154 | 687 | **~8,288** |
| Command | `crux-test.md` | 11,902 | 318 | ~2,975 |
| Command | `crux-meditate.md` | 8,842 | 91 | ~2,210 |
| Command | `crux-dream.md` | 7,189 | 80 | ~1,797 |
| Command | `crux-recall.md` | 6,817 | 97 | ~1,704 |
| Command | `crux-forget.md` | 3,158 | 58 | ~789 |
| Command | `crux-remember.md` | 3,084 | 54 | ~771 |
| Command | `crux-amnesia.md` | 2,822 | 63 | ~705 |
| Command subtotal | — | **76,968** | 1,448 | **~19,239** |
| Skill | `crux-skill-memory-rebalance/SKILL.md` | 31,428 | 602 | **~7,857** |
| Skill | `crux-skill-memory-extract/SKILL.md` | 21,743 | 380 | **~5,435** |
| Skill | `crux-skill-memory-compress/SKILL.md` | 10,418 | 184 | ~2,604 |
| Skill | `crux-skill-memory-reference-tracker/SKILL.md` | 9,944 | 219 | ~2,486 |
| Skill | `crux-skill-memory-crud/SKILL.md` | 8,895 | 207 | ~2,223 |
| Skill | `crux-skill-memory-index/SKILL.md` | 5,179 | 126 | ~1,294 |
| Skill | `crux-utils/SKILL.md` | 3,209 | 111 | ~802 |
| Skill subtotal | — | **90,816** | 1,829 | **~22,701** |

**Total `.cursor/` content (excluding rules and hook scripts)** ≈ **~62K tokens**. None of it is loaded all at once — but specific workflows touch large slices (see §2).

### 1.3 Realistic per-workflow cost (worst case before optimisation)

Assumes: parent agent honours all "Read X if not already loaded" instructions in agent/skill prompts; subagents do not inherit `Read` results from the parent context.

| Workflow | Files pulled in | Est. tokens |
|----------|----------------|------:|
| Trivial Q&A (no spec, no compression, no memory) | always-on baseline | ~4.2K |
| Trivial Q&A (with `_CRUX-RULE.mdc` triggering `CRUX.md` load) | + `CRUX.md` | **~11.2K** |
| `/crux-compress @file.md` (single file) | baseline + `crux-compress.md` (8.3K) → spawns 2× `crux-cursor-rule-manager` (5.1K each + each re-loads `CRUX.md` 7K) | **~41K** |
| `/crux-dream <spec>` | baseline + `crux-dream.md` (1.8K) + `crux-cursor-memory-manager.md` (9.4K) + `crux-skill-memory-extract.md` (5.4K) + `crux-skill-memory-crud.md` (2.2K) + `crux-skill-memory-index.md` (1.3K) + each subagent re-reads `CRUX.md` (7K) and `AGENTS.md` (1.6K) and `crux-memories.json` (~0.8K) | **~40–55K** |
| `/crux-dream --rem` | baseline + dream chain + `crux-skill-memory-rebalance.md` (7.9K) + `crux-skill-memory-compress.md` (2.6K) + `crux-skill-memory-reference-tracker.md` (2.5K) | **~55–75K** |
| `/crux-meditate` (3 branches × 3 × 3 = 13 agents) | baseline + meditate command + `crux-cursor-memory-manager.md` × 13 (each ~12K including AGENTS+CRUX re-reads) | **~150–200K cumulative across the tree** |
| Spec execution (10-subtask spec, 4 parallel) | baseline + spec doc(s) + per subtask: agent file (1.5–9.4K) + `CRUX.md` re-read (7K) + `AGENTS.md` re-read (1.6K) + skill files invoked | **~80–120K total per pass**, dominated by repeated `CRUX.md` loads |

> **The single biggest cost is `CRUX.md` being instructed to load by every agent and several skills.** Even when an agent never produces or consumes CRUX-compressed content (e.g. `crux-software-engineer` writing a Python module), its system prompt says "Before doing ANY work, read `CRUX.md`". That is **7K tokens** per spawn that the work usually does not need.

---

## 2. Loading patterns — where the tokens actually go

### 2.1 Three load tiers

| Tier | What it contains | When it loads |
|------|------------------|---------------|
| **A. Always-on** | `AGENTS.md`, all 7 `alwaysApply: true` rules, `agent_skills` block | Every session start |
| **B. Self-pulled** | `CRUX.md`, `.crux/crux-memories.json`, agent body, SKILL files, related rules | Agent system prompt instructions explicitly tell the LLM to `Read X` on its first turn |
| **C. On-invocation** | Command `.md` files, subagent definitions, hook stdout | Loaded when the command runs or the subagent is spawned |

Tier B is the **hidden tier**: nothing in the Cursor config requires loading those files; the **agent prompts themselves** demand it. That makes Tier B optimisable purely with prose edits — no platform changes required.

### 2.2 Per-spec-execution build-up

For a typical spec executor running 10 subtasks across 4 parallel subagents:

```
Parent context:
  always-on (4.2K)
  + CRUX.md self-pulled (7.0K)
  + spec doc(s) (5–10K)
  + spec-agent-allocation rule already in always-on
  + crux-platform-architect (1.6K) loaded once for assessment
  ≈ 18–23K parent baseline

Per subagent spawn (×10):
  always-on inherited? NO — each subagent gets fresh system prompt
  agent file (1.4K – 9.4K)
  + AGENTS.md re-read (1.6K)
  + CRUX.md re-read (7.0K)               ← biggest waste, often unused
  + crux-memories.json (~0.8K) if memory work
  + 1–2 SKILL files (2–8K)
  + subtask doc (3–10K)
  ≈ 16–35K per subagent

Total spec pass: 18K + (10 × ~25K) ≈ 270K tokens of system+spec context
```

`CRUX.md` alone = **~70K of repeated loads** in that pass (10 × 7K). Removing the unconditional load for non-CRUX agents would recover the majority of this.

### 2.3 Spec generation (`/zoto-spec-create`) cost shape

Spec creation is dominated by the **architect** agent which then spawns one subagent per planned subtask to draft subtask files. Each draft pass currently re-instantiates AGENTS.md + CRUX.md + the architect file. A 10-subtask spec creation incurs roughly the same 10× repeat as execution.

---

## 3. Redundancy catalogue (where the bytes go)

These are the high-leverage redundancies discovered while reading every file end-to-end.

### R1. `Read AGENTS.md if not already loaded` and `Read CRUX.md` repeated in every agent
- Present in: `crux-cursor-memory-manager`, `crux-cursor-rule-manager`, `crux-platform-architect`, `crux-software-engineer`, `integrity-expert` (5 of 6 agents).
- Per-file cost: ~80 tokens of instruction. **Real cost: ~7K per spawn** because the LLM obeys it.
- For non-CRUX work (software engineer writing Python, integrity expert running shellcheck, docs-sync agent editing markdown), `CRUX.md` is rarely required.

### R2. User-Input Escalation / Pattern A / Pattern B explained five times
Full Pattern A/B description appears in:
- `AGENTS.md` (canonical)
- `crux-cursor-memory-manager.md` (full re-paste, ~700 tokens)
- `crux-dream.md`, `crux-recall.md`, `crux-forget.md`, `crux-remember.md`, `crux-meditate.md` (reduced re-paste each, ~150–250 tokens × 5)

Combined waste: **~1.6K tokens** of duplicated protocol description that every memory workflow re-teaches.

### R3. Config reference tables duplicated across skills
The same `.crux/crux-memories.json` keys (`maxMemorySize`, `compressionMinLines`, `compressionTarget`, `sizeUnit`, `typePriority`, `storage.*`, `referenceTracking.*`, `flags.enableMemory*`) are re-tabled in:
- `crux-skill-memory-rebalance/SKILL.md` (~50 lines of config table)
- `crux-skill-memory-compress/SKILL.md` (~12 lines)
- `crux-skill-memory-extract/SKILL.md` (~14 lines)
- `crux-skill-memory-crud/SKILL.md` (~10 lines)
- `crux-skill-memory-reference-tracker/SKILL.md` (~12 lines)

Combined waste: **~1.2K tokens** of duplicated schema documentation. The actual JSON is 80 lines and authoritative.

### R4. Compression metadata/contract duplicated between command and agent
`.cursor/commands/crux-compress.md` and `.cursor/agents/crux-cursor-rule-manager.md` both fully describe:
- Frontmatter fields (`generated`, `sourceChecksum`, `cruxLevel`, `beforeTokens`, `afterTokens`, `reducedBy`, `confidence`, `sourceUrl`, `alwaysApply`).
- Compression-level resolution algorithm.
- Plugin lifecycle hooks and registry shape.
- Validation flow + confidence thresholds + scoring weights.
- Source/output extension tables.

Combined waste: **~2.5K tokens** in the command alone that simply re-state what the agent will already do.

### R5. `crux-compress.md` repeats subagent prompts for each source type
Five near-identical "When invoked with…" sections (markdown / image / URL / code / ALL) each contain a ~25-line inline subagent prompt. ~80% of the prose differs by only a few keywords. **~1.5K tokens** of avoidable boilerplate.

### R6. `crux-cursor-memory-manager.md` carries an 80-line Canvas reference template inline
Lines 178–242 of the agent file are a `cursor/canvas` SDK template used **only** in `--total` mode of Recall. Cost: **~750 tokens** loaded for every memory-manager spawn even though Dream / REM / Forget / Remember never touch it.

### R7. `crux-skill-memory-rebalance/SKILL.md` has 12 step templates with output examples
Each of `Promote`, `Demote`, `Archive`, `Consolidate (single + multi)`, `Volume rebalance`, `Compress`, `Cleanup`, `Promote to rule` has a 5–15 line "Recommendation format" code block with example emojis. Cumulative: **~1.4K tokens** of formatting examples that the LLM does not need verbatim.

### R8. `Related` link block at the bottom of every command
Each of the 7 memory commands ends with a 6-line `## Related` listing the same set of commands and skills. ~120 tokens × 7 = **~840 tokens**.

### R9. `crux-test.md` is 3K tokens of test-case prose
Its instructions could be replaced with a single eval Python file (which is the project's stated convention) plus a one-paragraph command file. Most of the content describes test fixtures and assertion shapes that belong in code.

### R10. `spec-agent-allocation.md` is uncompressed
This is a CRUX-friendly rule (table → mapping) that is currently 365 tokens in always-on context. Compressed it could be ~100 tokens.

### R11. `_CRUX-RULE.mdc` and `crux-memories-integration.crux.mdc` overlap with `AGENTS.md`
The "8 foundational CRUX rules" appear in `AGENTS.md` and again in `_CRUX-RULE.mdc` (both always-on). Net duplication: **~250 tokens** loaded twice per session.

### R12. `crux-meditate.md` describes the recursion in both the command and the agent
Steps 1–7 in `crux-meditate.md` are paraphrased again in `crux-cursor-memory-manager.md` (Meditate Mode + Recursive exploration protocol). ~900 tokens of overlap.

---

## 4. Reduction options (with pros/cons, BC, rationale, benefits, risks)

The options are independently adoptable. They are ordered by leverage (largest expected savings first). Where a number is given, it is an estimated steady-state saving per spec execution; one-off costs (refactor, eval rewrites) are not amortised.

---

### Option 1 — Make `CRUX.md` lazy-load, scoped to CRUX-touching work

**What changes**
- Replace "Before doing ANY work, you MUST read `CRUX.md`" with a conditional: "Read `CRUX.md` only when the task involves writing, validating, or interpreting CRUX notation. Otherwise rely on the always-applied summary in `_CRUX-RULE.mdc` and `AGENTS.md`."
- Update `AGENTS.md` foundational rule #1 to say "interpret CRUX rules in context" rather than "load CRUX.md".
- Strip the unconditional load instruction from `crux-software-engineer`, `integrity-expert`, `docs-sync-agent`, `crux-platform-architect` (4 agents that almost never produce CRUX text).
- Keep the unconditional load only in `crux-cursor-rule-manager` and `crux-skill-memory-compress` where it is actually needed.

**Estimated savings per spec execution**: ~7K × N (subagents that don't need CRUX) ≈ **30–60K tokens / spec**.

**Pros**
- Largest single win. Hits the dominant cost line (§2.2) directly.
- Zero risk of behaviour change for compression workflows (those agents still load it).
- Aligns with foundational rule #2 ("DO NOT LOAD SOURCE FILES when CRUX exists") in spirit — `CRUX.md` is not actionable for non-compression code work.

**Cons**
- A subagent that *unexpectedly* needs CRUX symbol reference must add an explicit `Read CRUX.md` step. Failure mode is "asks once, then proceeds" — visible and recoverable.
- Slight risk of inconsistent CRUX block authoring if a non-rule-manager agent emits CRUX inadvertently.

**Backwards compatibility**: High. Edits are prompt-only; no file paths, schemas, or commands change. Existing CRUX outputs and the compression pipeline are untouched.

**Rationale**: The repository already has dedicated agents for CRUX work. Loading the spec into agents that delegate CRUX work to subagents is double-counting. The always-on `_CRUX-RULE.mdc` + `crux-memories-integration.crux.mdc` already carry the symbol-aware behavioural cues (interpret/honor/preserve paths/edit-source).

**Risks**: Low. Worst case: one extra "read CRUX.md" round-trip in an outlier subagent.

---

### Option 2 — CRUX-compress every long agent + skill + command

Targets (current → target ≤25%):

| File | Current tok | Target tok | Saving / spawn |
|------|-----------:|----------:|---------------:|
| `crux-cursor-memory-manager.md` | 9,358 | ~2,300 | ~7,000 |
| `crux-compress.md` | 8,288 | ~2,000 | ~6,300 |
| `crux-skill-memory-rebalance.md` | 7,857 | ~1,950 | ~5,900 |
| `crux-skill-memory-extract.md` | 5,435 | ~1,350 | ~4,100 |
| `crux-cursor-rule-manager.md` | 5,131 | ~1,300 | ~3,800 |
| `crux-test.md` | 2,975 | ~750 | ~2,200 |
| `crux-skill-memory-compress.md` | 2,604 | ~650 | ~1,950 |
| `crux-skill-memory-reference-tracker.md` | 2,486 | ~620 | ~1,870 |
| `crux-skill-memory-crud.md` | 2,223 | ~560 | ~1,660 |
| `crux-meditate.md` | 2,210 | ~550 | ~1,660 |
| `crux-dream.md` | 1,797 | ~450 | ~1,350 |
| `crux-recall.md` | 1,704 | ~430 | ~1,280 |
| `crux-platform-architect.md` | 1,596 | ~400 | ~1,200 |
| `crux-software-engineer.md` | 1,442 | ~360 | ~1,080 |
| `integrity-expert.md` | 1,584 | ~400 | ~1,180 |
| `crux-skill-memory-index.md` | 1,294 | ~325 | ~970 |

**Total potential**: ~42K tokens saved per agent/skill/command load, applied per spawn.

**Pros**
- Uses the project's flagship capability on its own surface — strongly on-brand.
- Mechanical: `crux-cursor-rule-manager` already runs on `.cursor/rules/` and can be pointed at `.cursor/agents/`, `.cursor/commands/`, `.cursor/skills/*/SKILL.md`.
- CRUX format keeps the source `.md` intact; agents/commands could be served by `.crux.md` via a small loader switch (or the `.cursor/` runtime can be updated to prefer `.crux.md` when present).

**Cons**
- The **agent** field in Cursor metadata expects `.md` with a YAML frontmatter; serving CRUX directly requires either (a) Cursor reading `.crux.md` natively, or (b) producing `.crux.mdc` adapters with the same frontmatter, or (c) keeping CRUX as the *body* but inside the original `.md` file.
- Validation overhead: every compressed agent/skill/command needs a confidence ≥ 90 % to be safe — these are behavioural prompts, not docs, so the bar is higher than rules.
- New maintainers must learn CRUX to edit these. Mitigation: edit source `.md`, regenerate `.crux.md`.
- Reviewers in PRs see CRUX diffs — slightly harder to read.

**Backwards compatibility**:
- Compatible if we adopt approach (c) — keep `.md` as canonical, replace its body with CRUX inside `⟦CRUX:source⟧` while preserving frontmatter. Cursor still loads the same path.
- Risk: any tool that greps these files for natural-language strings (e.g. eval matchers like "Pattern A", "Read AGENTS.md") would need re-tuning.

**Rationale**: This is the project's first-principles tool. Eating its own dogfood at scale would (i) yield the largest second-order saving, (ii) stress-test CRUX's semantic preservation on prompt-style content, (iii) feed evals.

**Risks**: Medium. Behaviour-prompt compression has tighter accuracy needs than rule compression. Mitigation: stage rollout — start with the largest, lowest-blast-radius targets (`crux-test.md`, `crux-skill-memory-rebalance` patterns). Run the full eval suite before/after on each.

---

### Option 3 — Single canonical "Memory Skills Reference" deduplicates §3 R3 + R2 + R8

**What changes**
- Move the config reference tables and the User-Input Escalation Pattern A/B description out of every skill/command and into one file: `.cursor/skills/_memory-shared.md` (or absorb into `.crux/crux-memories.json` schema doc).
- Each skill replaces the duplicated section with: "Config keys: see `.crux/crux-memories.json` and `.cursor/skills/_memory-shared.md`."
- `Related` link blocks → one shared registry pointed at by a single line in each command.

**Estimated savings**: ~3.5K tokens across the memory skill+command set (loaded only when those skills are pulled, but multiple are usually pulled together → ~7–10K saved per memory workflow).

**Pros**
- Eliminates drift (today the same key default appears with slightly different wording in 5 places).
- The shared file is loaded **only once** — sub-skills inherit it via the parent agent's context.

**Cons**
- One more file to navigate.
- Subagents must be taught to load `_memory-shared.md` once — same pattern as CRUX.md but cheaper.

**Backwards compatibility**: High. Skills still expose the same operations and signatures. Only their internal documentation changes.

**Rationale**: §3 R3 is pure copy/paste duplication. The JSON config is already authoritative; per-skill tables are documentation echoes.

**Risks**: Very low. If `_memory-shared.md` fails to load, each skill still references the JSON config explicitly.

---

### Option 4 — Split `crux-cursor-memory-manager` into mode-scoped agents

**What changes**
- Today's monolithic 9.4K-token agent supports 7 modes (Dream / REM / Recall / Remember / Forget / Meditate / Compress orchestration). Each command spawns it but uses one mode.
- Option: produce 4 thin agents — `crux-memory-dream`, `crux-memory-rem`, `crux-memory-recall`, `crux-memory-meditate` — each ~1.5K tokens, with `crux-cursor-memory-manager` retained as a thin dispatcher.
- The Canvas template (R6) lives only in `crux-memory-recall`.

**Estimated savings**: ~7K tokens per memory subagent spawn × ~3 spawns per Dream cycle = ~20K / dream. Meditate's ×13 spawn tree benefits the most: ~80K saved per `--total` run.

**Pros**
- Massive saving on Meditate (the fan-out workflow is the worst offender today).
- Clearer agent boundaries; easier to evaluate and version.
- Reduces accidental cross-mode contamination (e.g. an agent in Dream mode wandering into Recall behaviour).

**Cons**
- Requires updating each command file to point at the right thin agent.
- Increases the count of files in `.cursor/agents/` from 6 to ~9.
- Existing `/crux-dream`, `/crux-meditate`, `/crux-recall` test/eval fixtures may name `crux-cursor-memory-manager` — needs grep+replace.

**Backwards compatibility**: Medium. Anything (specs, evals, MCP) that hard-codes `crux-cursor-memory-manager` must add an alias or be updated. Recommend: keep the umbrella agent as a deprecation shim that delegates to the new thin agents, then remove in a future version bump.

**Rationale**: Single-responsibility yields exactly what the platform-architect agent itself recommends ("Each agent should have a single clear responsibility — delegate, don't accumulate"). Today's memory-manager violates this principle.

**Risks**: Medium. Test surface grows; cross-mode shared logic (e.g. config loading, feature-guard checks) must be DRY'd via §Option 3 to avoid regression.

---

### Option 5 — Subagent context inheritance: pass a "prelude bundle" instead of re-`Read`-ing

**What changes**
- Today, every subagent fresh-reads `AGENTS.md`, `CRUX.md`, `.crux/crux-memories.json`, sometimes the full memory index. Each load is paid in the subagent's context.
- Add a convention: the parent passes a compact JSON "context manifest" in the subagent's task prompt that lists what was already verified loaded ("`agents_md_loaded: true`, `crux_md_loaded: false`, `memory_config_summary: {...}`"). The subagent skips redundant loads when the manifest signals freshness.
- Update agent prompts: change "Before doing ANY work, you MUST read X" → "Before doing ANY work, ensure X is loaded. If your task prompt's `context_manifest` indicates X is already in context, do not re-read."

**Estimated savings**: 7–15K tokens per subagent spawn (mostly the avoided `CRUX.md` + `AGENTS.md` + config re-reads that the parent already paid for). For a 10-subtask spec: ~70–150K saved.

**Pros**
- No content changes. Works on top of any of Options 1–4.
- Mirrors the foundational CRUX rule "DO NOT LOAD SOURCE FILES when CRUX exists" — generalises it: do not load anything we know is already loaded.
- Encourages the parent to think about what context it actually transferred.

**Cons**
- Subagents currently get fresh model contexts in Cursor. The `context_manifest` approach is **promise-based** — the LLM trusts the parent's word that the file is loaded. If wrong, the subagent operates on stale assumptions.
- Mitigation: add a one-line probe ("If you cannot recall the contents of `X`, re-load it") with a couple of checksum-style hooks (e.g. ask the subagent to acknowledge a known phrase from `AGENTS.md`).

**Backwards compatibility**: High. Manifest is additive; a subagent that ignores it falls back to current behaviour.

**Rationale**: This is the cheapest cross-cutting improvement. It is also the most aligned with how the project already thinks about context (cf. `analysis/context-usage-hash-ids-and-hooks.md`).

**Risks**: Medium. Hallucination of "I already know AGENTS.md" without the parent actually passing content. Mitigation suggested above; also: keep the manifest path optional and apply Option 1 first to reduce the blast radius.

---

### Option 6 — Move the Canvas template (R6) and the per-source-type prompts (R5) into separate, lazily-loaded files

**What changes**
- Extract `cursor/canvas` reference template from `crux-cursor-memory-manager.md` into `.cursor/agents/templates/recall-canvas.tsx.md`. The agent prompt says "If invoked with `--total`, read the Canvas template at `…/recall-canvas.tsx.md`."
- Extract the five subagent task templates from `crux-compress.md` into `.cursor/commands/templates/compress-prompts.md`. The command says "Use the prompt template for the matched source type from `…/compress-prompts.md`."

**Estimated savings**:
- ~750 tokens from every memory-manager spawn (R6).
- ~1.5K tokens from every `/crux-compress` invocation (R5).

**Pros**
- Clean separation — operational text lives where the operator looks.
- The extracted files load only on the rare branches that need them.

**Cons**
- One extra file open on the cold paths.
- Slightly slower onboarding (documentation is one indirection deeper).

**Backwards compatibility**: High. No interface change.

**Rationale**: Minimal-change extraction with measurable wins.

**Risks**: Low.

---

### Option 7 — Compress the always-on rules and merge `_CRUX-RULE.mdc` overlap with `AGENTS.md`

**What changes**
- Compress `spec-agent-allocation.md` (R10) → CRUX. Saves ~265 tokens always-on.
- Reconcile `_CRUX-RULE.mdc` with the eight rules already in `AGENTS.md` (R11). Either delete the rule (CRUX rules already in AGENTS.md), or strip AGENTS.md's repeat. Saves ~250 tokens always-on.
- Audit the two memory rules (`crux-memories-integration.crux.mdc` and `crux-memories-mcp-context.mdc`) — they overlap on "when to search memories". Consolidate. Saves ~150 tokens.

**Estimated savings**: ~700 tokens shaved off **every session** (high impact because it is per-turn).

**Pros**
- Always-on context is the most expensive context in the project. Even small reductions compound.
- Forces the canonical source of CRUX foundational rules to be `AGENTS.md` only — single source of truth.

**Cons**
- Requires a careful diff: `_CRUX-RULE.mdc` is loaded as a Cursor `alwaysApply` rule whereas `AGENTS.md` is appended by Cursor's system message — both fire, but the latter is platform-dependent.

**Backwards compatibility**: Medium. Removing `_CRUX-RULE.mdc` means losing the rule for users on platforms that prefer rules over AGENTS. Recommend: keep `_CRUX-RULE.mdc` but slim it to a single CRUX-pointer line (~30 tokens).

**Rationale**: §1.1 + R11; small bytes, persistent gain.

**Risks**: Low.

---

### Option 8 — Replace `crux-test.md` with a Python eval entry point

**What changes**
- The 3K-token slash command `/crux-test` essentially scripts ten test cases. The codebase already has `evals/` for this purpose.
- Replace `crux-test.md` with a 200-token command file that runs `python3 -m evals.run_crux_test_suite` (or similar). All test descriptions move into pytest test docstrings.

**Estimated savings**: ~2.2K tokens per `/crux-test` invocation, plus removal of Pattern duplication.

**Pros**
- Aligns with the platform-architect's own guidance ("Eval-driven: no feature is complete without a corresponding eval").
- Tests become deterministic and CI-runnable (today they are LLM-orchestrated, which is slow and noisy).

**Cons**
- Some tests are inherently LLM-driven (semantic validation, decompression). Those still need an LLM agent — but the orchestration of "spawn fresh validator" can be a fixture in pytest.

**Backwards compatibility**: Medium. Anyone running `/crux-test` today gets a different invocation. Mitigation: `/crux-test` becomes a thin shim that calls the eval script and reports back.

**Rationale**: Code is cheaper than prompts for deterministic checks.

**Risks**: Medium — requires writing the pytest harness for the LLM-driven tests (already present in `evals/conftest.py`).

---

### Option 9 — `.crux/crux-memories.json` extended with a `context_loadout` map for command/agent inheritance

**What changes**
- Add a top-level config block listing, per command, the agents/skills it expects the parent to pre-load:

```json
"contextLoadout": {
  "/crux-dream": ["crux-cursor-memory-manager", "crux-skill-memory-extract", "crux-skill-memory-crud"],
  "/crux-recall": ["crux-cursor-memory-manager", "crux-skill-memory-compress"]
}
```

- Hooks read this on `sessionStart` (or on slash-command invocation if a future hook fires there) and inject only the relevant skill descriptions into context, suppressing the global `agent_skills` blanket.

**Estimated savings**: ~700–1,400 tokens always-on, more on command runs.

**Pros**
- Decouples command surface from always-on cost.
- Composable with Option 5 (the loadout becomes the parent-side manifest).

**Cons**
- Hardest option to implement — requires hook code and possibly Cursor cooperation for slash-command-triggered hooks (does not exist today).
- Adds a config layer to maintain.

**Backwards compatibility**: High if the new behaviour is opt-in (`flags.useContextLoadout: "true"`).

**Rationale**: The cheapest tokens are the ones never loaded; this builds the policy plumbing for that.

**Risks**: Medium-High due to platform dependency.

---

### Option 10 — Trim the on-disk file in addition to compressing — drop "What This Skill Does NOT Do" and other safety text

Many SKILL files end with a `## What This Skill Does NOT Do` section listing 5–7 lines of negative scope (e.g. "Does not create memories — that is `crux-skill-memory-crud`"). Useful for new contributors but redundant for the LLM, which already has the agent dispatch table in `AGENTS.md`.

- Move negative scope into a one-liner cross-reference: "Out of scope: see `AGENTS.md` agent table for delegation."
- Same treatment for the multiple "Integration" tables that re-list paths the agent already knows.

**Estimated savings**: 200–400 tokens per skill, ~2K across the skill set.

**Pros**: Minimal surgical edits. No semantic risk.
**Cons**: Slightly less self-contained skill docs for human readers. Mitigation: link to `AGENTS.md` for the registry.
**BC**: High. **Risks**: Very low.

---

## 5. Recommended sequencing

The options stack additively. Recommend the following order for fastest payoff with lowest risk:

| # | Option | Effort | Risk | Steady-state saving |
|---|--------|--------|------|--------------------:|
| 1 | Lazy `CRUX.md` (Opt 1) | Low (prose only) | Low | ~30–60K / spec |
| 2 | Compress and consolidate memory shared sections (Opt 3 + Opt 10) | Low | Low | ~5–8K / memory workflow |
| 3 | Extract Canvas + compress-prompts (Opt 6) | Low | Low | ~2K / spawn |
| 4 | Compress always-on rules and reconcile overlap (Opt 7) | Low | Low | ~700 / turn (huge cumulative) |
| 5 | CRUX-compress agents/skills/commands (Opt 2) — start with `crux-cursor-memory-manager`, `crux-compress`, `crux-skill-memory-rebalance` | Medium | Medium | ~10–15K / spawn |
| 6 | Replace `/crux-test` with pytest entry (Opt 8) | Medium | Medium | ~2K + better CI |
| 7 | Split memory manager into mode-scoped agents (Opt 4) | Medium | Medium | ~7K / memory spawn; ~80K / `--total` |
| 8 | Subagent context manifest inheritance (Opt 5) | Medium | Medium | ~10K / subagent |
| 9 | Slash-command context loadout (Opt 9) | High | High | persistent always-on saving |

Adopting the first four alone yields **~30–70 % reduction** in tokens loaded per realistic spec execution, with prose-only changes and no platform dependencies.

---

## 6. Backwards-compatibility summary

| Change | Affects… | Mitigation |
|--------|---------|-----------|
| Lazy `CRUX.md` | Subagents that incorrectly assume CRUX symbols are pre-known | Keep `_CRUX-RULE.mdc` always-on as a one-paragraph primer |
| Compress agents/skills/commands | Anything that grep'd those `.md` files for prose phrases (evals, docs scripts) | Re-tune evals; produce CRUX inside the same `.md` to keep paths stable |
| Memory skill consolidation file | Tooling that walked `.cursor/skills/*/SKILL.md` for self-contained docs | Add `_memory-shared.md` to that walker |
| Split memory manager | Specs / evals that hard-code agent name | Keep the umbrella agent as a delegation shim for one minor version |
| `/crux-test` → pytest | CI scripts and contributors that ran `/crux-test` | Keep `/crux-test` as a thin shim calling `pytest evals/test_crux_suite.py` |
| Context manifest | Subagents that ignore the manifest | Default falls through to current behaviour |
| Loadout config | Cursor hook availability | Behind `flags.useContextLoadout` opt-in |

No option requires breaking the public CLI of `install.py`, the `.crux/` schema (additive only), or any existing memory file format.

---

## 7. Appendix A — How the numbers were obtained

- Byte/line counts: `wc -l -c` on each file.
- Token estimates: prose ≈ 4 chars/token (project's own heuristic from `crux-utils`); rounded down conservatively (some prose contains tables and code which would shrink the per-token char count slightly, raising actual tokens by ~5 %). For `agent_skills` block size we counted only descriptions in `SKILL.md` frontmatter.
- Per-workflow estimates: walked each command file and tallied the agent + skill files that the command's text instructs the agent to read, plus per-spawn AGENTS.md / CRUX.md / config re-reads as documented in each agent file.

## 8. Appendix B — Files cited

- Agents: `.cursor/agents/crux-cursor-memory-manager.md`, `.cursor/agents/crux-cursor-rule-manager.md`, `.cursor/agents/crux-platform-architect.md`, `.cursor/agents/crux-software-engineer.md`, `.cursor/agents/integrity-expert.md`, `.cursor/agents/docs-sync-agent.md`.
- Commands: `.cursor/commands/crux-compress.md`, `.cursor/commands/crux-test.md`, `.cursor/commands/crux-meditate.md`, `.cursor/commands/crux-dream.md`, `.cursor/commands/crux-recall.md`, `.cursor/commands/crux-forget.md`, `.cursor/commands/crux-remember.md`, `.cursor/commands/crux-amnesia.md`.
- Skills: `.cursor/skills/crux-skill-memory-rebalance/SKILL.md`, `.cursor/skills/crux-skill-memory-extract/SKILL.md`, `.cursor/skills/crux-skill-memory-compress/SKILL.md`, `.cursor/skills/crux-skill-memory-reference-tracker/SKILL.md`, `.cursor/skills/crux-skill-memory-crud/SKILL.md`, `.cursor/skills/crux-skill-memory-index/SKILL.md`, `.cursor/skills/crux-utils/SKILL.md`.
- Rules: `.cursor/rules/_CRUX-RULE.mdc`, `.cursor/rules/spec-agent-allocation.md`, `.cursor/rules/crux-memories-integration.crux.mdc`, `.cursor/rules/crux-memories-mcp-context.mdc`, `.cursor/rules/docs-sync.crux.mdc`, `.cursor/rules/version-bump.crux.mdc`, `.cursor/rules/zip-contents-protection.crux.mdc`.
- Anchors: `AGENTS.md`, `CRUX.md`, `.crux/crux-memories.json`, `.cursor/hooks.json`.
- Adjacent design notes: `analysis/context-usage-hash-ids-and-hooks.md`.
