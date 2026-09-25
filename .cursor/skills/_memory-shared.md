# CRUX Memory — Shared Reference

Single source of truth for information that would otherwise be duplicated across
every memory skill (`crux-skill-memory-*`) and every memory-oriented command
(`/crux-dream`, `/crux-recall`, `/crux-forget`, `/crux-remember`, `/crux-meditate`,
`/crux-amnesia`). Skills and commands should link **into** this file with anchor
pointers (see the anchors listed under each heading below) rather than restating
the material.

This file is **not** a Cursor skill. It carries no `SKILL.md` name, is not
loaded by any agent by default, and is not registered by the IDE skill loader.
It is a shared reference doc that memory skills and commands cross-reference by
path. Do not create a `_memory-shared/SKILL.md` for it.

Authoritative sources referenced from here:

- `.crux/crux-memories.json` — canonical config (the "table" below is documentation).
- `AGENTS.md` (the `<CRUX agents="always">` block) — canonical User-Input
  Escalation protocol (Pattern A and Pattern B).
- Each skill's `SKILL.md` — canonical protocol for that skill's operation.

Sections:

- [Config Reference](#config-reference) — every `.crux/crux-memories.json` key
  used by a memory skill or command, with defaults.
- [User-Input Escalation](#user-input-escalation) — pointer to the canonical
  Pattern A / Pattern B write-up in `AGENTS.md` plus the `needs_user_input` YAML
  contract subagents must return when they need input.
- [Related Commands & Skills](#related-commands--skills) — one-table registry
  of every `/crux-*` memory command and every `crux-skill-memory-*` skill with
  a one-line purpose.
- [Cross-Skill Boundaries](#cross-skill-boundaries) — ownership map derived
  from the `AGENTS.md` agent-allocation table so no skill needs its own
  "Does NOT Do" or "Integration re-listing" block.

---

## Config Reference

All values live in `.crux/crux-memories.json` under `cruxMemories.*` and
`flags.*`. The JSON file itself is authoritative — this table documents the
keys memory skills and commands actually read. If a default here disagrees with
the JSON, trust the JSON.

### Feature flags

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `flags.enableMemories` | string | `"false"` | Master gate for every memory operation. Skills abort when this is not `"true"`. |
| `flags.enableMemoryCompression` | string | `"false"` | Feature gate for CRUX-compressing memories (Compress + REM sleep Step 8). |
| `flags.enableMemoryConsolidation` | string | `"false"` | Feature gate for REM sleep Step 7 (Consolidate). |

### Sizing

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `cruxMemories.sizeUnit` | string | `"lines"` | Unit for every size threshold — `"lines"` or `"bytes"`. |
| `cruxMemories.maxMemorySize` | number | `1000` | Hard cap on a single memory file (in `sizeUnit`); exceeding triggers adaptive compression. |
| `cruxMemories.maxConsolidatedSize` | number | `2000` | Hard cap on a consolidated (multi-source) memory file; exceeding triggers volume splitting. |
| `cruxMemories.compressionMinLines` | number | `500` | Minimum file size before CRUX compression is considered; files below this are left uncompressed. |
| `cruxMemories.compressionTarget` | number | `33` | Target compressed body size as % of original. |

### Type lifecycle

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `cruxMemories.typePriority` | array | `[core, redflag, goal, learning, idea, archived]` | Valid types in priority order. |
| `cruxMemories.typeTransitions` | object | see JSON | Per-type `promoteAt` / `promoteTo` used by REM sleep Step 4 (Promote). |
| `cruxMemories.demoteAfterDaysUnreferenced` | integer | `90` | Days without reference before REM sleep recommends demotion. |
| `cruxMemories.archiveAfterDaysUnreferenced` | integer | `180` | Days without reference before REM sleep recommends archival. |

### Storage

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `cruxMemories.storage.memoriesDir` | string | `memories` | Root directory for base memories. |
| `cruxMemories.storage.agentMemoriesDir` | string | `memories/agents` | Root for agent-scoped memories. |
| `cruxMemories.storage.archiveDir` | string | `.ai-ignored/executed` | Directory for REM sleep summaries. |
| `cruxMemories.storage.compressionSourceArchive` | string | `.ai-ignored/memories/sources` | Base path where uncompressed originals are archived before compression. |
| `cruxMemories.storage.indexFile` | string | `.crux/memory-index.yml` | Output path for the generated memory index. |

### Reference tracking

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `cruxMemories.referenceTracking.enabled` | boolean | `true` | Master switch for `.refs.yml` tracker writes. |
| `cruxMemories.referenceTracking.trackingDir` | string | `.crux/reference-tracking` | Directory containing `.refs.yml` tracker files. |
| `cruxMemories.referenceTracking.indicateInOutput` | boolean | `true` | Whether agents annotate influenced output with `[memory:{title}]`. |
| `cruxMemories.referenceTracking.indicatorFormat` | string | `[memory:{title}]` | Format string for output annotations (`{title}` interpolated from frontmatter). |
| `cruxMemories.referenceTracking.promotionToRuleThreshold` | integer | `30` | Reference count that flags a memory for potential promotion to a permanent rule. |
| `cruxMemories.referenceTracking.maxReferencesStored` | integer | `10` | Cap on `recent_references[]` per tracker (oldest evicted first). |

### Dream / extract

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `cruxMemories.unitOfWork` | string | `"spec"` | Type of work item consumed by `/crux-dream` (e.g. `spec`, `task`); also the key name for `recent_references[]` source entries. |
| `cruxMemories.dream.workDir` | string | `"specs"` | Directory containing units of work; `/crux-dream` only accepts subdirectories of this path. |
| `cruxMemories.dream.stateFile` | string | `"_execution-state.yml"` | Execution-state filename inside a unit-of-work directory. |
| `cruxMemories.dream.maxCandidateFacts` | integer | `5` | Maximum candidate facts to present per dream extraction. |
| `cruxMemories.dream.maxUnrelatedChanges` | integer | `50` | Changed-file threshold before dream warns that extraction may be noisy. |

### Meditate

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `cruxMemories.meditate.modelPool` | array | see JSON | Model pool used by `--random-model`, `--model-per-branch`, and `--ensemble`. |
| `cruxMemories.meditate.ensembleAggregatorModel` | string | unset | Optional model slug for the ensemble cross-model aggregation agent. |

Anchors used by skills and commands: `#config-reference`.

---

## User-Input Escalation

The canonical description of **Pattern A (pre-collect then spawn)** and
**Pattern B (work first, then escalate)** lives in `AGENTS.md`, inside the
`<CRUX agents="always">` block under **User Input Escalation — Subagent
Protocol**. Do not re-paste that description into skills or commands — link to
this section (`#user-input-escalation`) instead.

Two rules apply to every memory skill and every memory command:

1. **Subagents NEVER call `AskQuestion` directly.** All user-facing prompts are
   handled by the parent agent (the top-level agent the user interacts with).
2. When a subagent needs input mid-flight that was not pre-collected, it
   returns a `needs_user_input` block in its response. The parent runs
   `AskQuestion` and resumes the subagent with the answers.

### `needs_user_input` YAML contract

```yaml
needs_user_input:
  reason: "<one-line why this cannot proceed without the user>"
  questions:
    - id: <slug>
      prompt: "<question text>"
      options:
        - id: <slug>
          label: "<label>"
      allow_multiple: false   # optional; defaults to false
```

Free-form chat prompts from subagents for interactive choices are forbidden —
use `needs_user_input` so the parent can present structured options via
`AskQuestion`.

### Which pattern each memory command uses

| Command | Primary pattern | Notes |
|---------|-----------------|-------|
| `/crux-dream` | Pattern B | Subagent analyses artefacts and ranks candidates, then parent collects accept/skip decisions. |
| `/crux-recall` | Pattern B | Subagent queries and formats memories, then parent handles post-display next-steps menu. |
| `/crux-forget` | Pattern B | Subagent resolves matches, then parent confirms deletions before subagent applies them. |
| `/crux-remember` | Pattern A (with Pattern B fallback) | Parent pre-collects type/tags/description; subagent falls back to `needs_user_input` only on conflict or size limit. |
| `/crux-meditate` | Pattern B | Depth-0 subagent runs the recursive tree; parent owns every mandatory pre-spawn gate and every post-consolidation choice. |
| `/crux-amnesia` | n/a | Session-scoped toggle only; does not spawn a subagent and does not modify any memory file. |

Anchor: `#user-input-escalation`.

---

## Related Commands & Skills

Single registry for every memory command and skill. Commands and skills
should point here (`#related-commands--skills`) instead of maintaining their
own `## Related` block.

### Commands

| Command | Purpose |
|---------|---------|
| `/crux-dream` | Post-execution memory extraction from a completed unit of work, and REM-sleep rebalancing of the memory corpus (`--rem`). |
| `/crux-recall` | Decompress, query, and display CRUX memories in human-readable form (or as an interactive `--total` canvas). |
| `/crux-forget` | Remove one or more memories from the corpus by id / slug / path / search. |
| `/crux-remember` | Store an ad-hoc memory outside of a spec workflow. |
| `/crux-meditate` | Recursive memory-informed exploration of a topic through a depth-N agent tree with mandatory adversarial review and paired HTML+PDF report. |
| `/crux-amnesia` | Session-scoped toggle that suppresses ambient memory usage without editing config. |

### Skills

| Skill | Purpose |
|-------|---------|
| `crux-skill-memory-crud` | Create, read, update, delete, and validate memory files. Owns the frontmatter schema and file-move semantics. |
| `crux-skill-memory-extract` | Analyse a completed unit of work, compare candidates against existing memories, and produce a ranked candidate set for `/crux-dream`. |
| `crux-skill-memory-rebalance` | REM sleep workflow — consistency checks, conflict detection, promote/demote/archive/consolidate/compress/rebalance recommendations, and application. |
| `crux-skill-memory-compress` | CRUX-compress and decompress memory bodies with adaptive sizing and source archival. |
| `crux-skill-memory-reference-tracker` | Manage `.refs.yml` trackers — record references, sync strength, and detect promotion-to-rule candidates. |
| `crux-skill-memory-index` | Build and rebuild `.crux/memory-index.yml` — the prioritised discovery list. |
| `crux-utils` | Token estimation and checksum utility used by compression workflows. |

### Meditation-only skills (spawned by `/crux-meditate` via `crux-cursor-meditation-guide`)

| Skill | Purpose |
|-------|---------|
| `crux-skill-memory-meditation-research` | Research-mode depth-first recursion, facet registry, citations index, peer review, K10c reflection. |
| `crux-skill-memory-meditation-quick` | Quick-mode parallel fan-out protocol with warn-only citation validation. |
| `crux-skill-memory-meditation-ensemble` | Ensemble Aggregation function — cross-model synthesis and K10 layered cadence. |
| `crux-skill-memory-meditation-review` | Adversarial review contract (13 dimensions, Report-Skill Respawn Protocol). |
| `crux-skill-memory-meditation-report` | Mandatory paired HTML+PDF report generation with Comprehensiveness Level Mapping. |
| `crux-skill-memory-meditation-coordination` | File-based coordination primitives — artefact filename grammar, polling, retrospective template, Branch & Leaf Index template. |

Anchor: `#related-commands--skills`.

---

## Cross-Skill Boundaries

Ownership map derived from `AGENTS.md` — the agent-allocation table and the
per-skill descriptions. Use this section (`#cross-skill-boundaries`) instead of
per-skill "What This Skill Does NOT Do" and "Integration" re-listing blocks.

If you are a memory skill and you find yourself asked to perform an operation
below that is not in your row, delegate to the owning skill instead of
duplicating the behaviour.

| Concern | Owner |
|---------|-------|
| Memory frontmatter, file naming, and file placement | `crux-skill-memory-crud` |
| Type transitions, `promoted_from` / `demoted_from` bookkeeping, `id` and `created` immutability | `crux-skill-memory-crud` |
| Memory file creation from an accepted candidate | `crux-skill-memory-crud` (called by `crux-skill-memory-extract`) |
| Memory file deletion + tracker deletion | `crux-skill-memory-crud` (called by `crux-skill-memory-rebalance` and `/crux-forget`) |
| Extract candidate facts from a completed unit of work | `crux-skill-memory-extract` |
| Compare candidates against existing memories, detect conflicts, detect resolved bugs | `crux-skill-memory-extract` |
| REM sleep workflow (consistency, conflicts, promote / demote / archive / consolidate / compress / rebalance / cleanup) | `crux-skill-memory-rebalance` |
| Volume splitting and rebalancing across multi-volume consolidated topics | `crux-skill-memory-rebalance` |
| CRUX compression / decompression of a single memory body, adaptive sizing, source archival | `crux-skill-memory-compress` |
| Migration of pre-existing uncompressed memories when `enableMemoryCompression` is turned on | `crux-skill-memory-compress` |
| Recording a reference in `.refs.yml`, syncing `strength`, capping `recent_references[]` | `crux-skill-memory-reference-tracker` |
| Detecting orphaned trackers during REM sleep cleanup | `crux-skill-memory-reference-tracker` |
| Building and rebuilding `.crux/memory-index.yml` | `crux-skill-memory-index` |
| Promotion of a memory to a permanent `.cursor/rules/` rule | **User action** — skills only flag candidates via `promotionToRuleThreshold`. |
| Writing dream / REM summaries and archiving unit-of-work directories | The orchestrating thin agent (`crux-memory-dream` writes dream summaries; `crux-memory-rem` writes REM summaries), not any skill. |
| User-facing prompts (`AskQuestion`) | The **parent agent** only — see [User-Input Escalation](#user-input-escalation). |

Anchor: `#cross-skill-boundaries`.
