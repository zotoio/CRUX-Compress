---
name: crux-skill-memory-meditation-coordination
description: File-based coordination primitives for meditation: artefact filename grammar (18 rows including `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`, per-tree ensemble variants, and 4 follow-up artefact types), placeholders, prefix-glob polling rule, never-hard-code invariant, retrospective template, Branch & Leaf Index template (single-model + ensemble variants). Use whenever the `crux-cursor-meditation-guide` agent reads, writes, or links a working-directory artefact.
---

# CRUX Skill: Memory Meditation — Coordination

Implements all file-based coordination primitives for the meditation system: artefact filename grammar (18 rows post-richness), placeholder definitions, prefix-glob polling rule, never-hard-code `report.{html,pdf}` invariant, process retrospective template, Branch & Leaf Index template (single-model and ensemble variants), and the ensemble working-directory structure.

## When to Use

Load this skill whenever the `crux-cursor-meditation-guide` agent:
- Reads, writes, or links any working-directory artefact
- Needs to poll for branch outputs or report files
- Needs to construct filenames from placeholders
- Needs to append the Branch & Leaf Index to `facets.md`
- Needs to write the process retrospective

This is the **leaf utility skill** — all five other meditation skills reference it for filename grammar and polling rules.

## Artefact Filename Table (18 rows post-richness)

All artefacts in the meditation working directory follow these filename patterns:

| Artefact | Filename pattern | Notes |
|----------|------------------|-------|
| Top-level facets (initial, pre-confirmation) | `facets-pending-{ts}.yml` | Deleted after the user confirms via combined Pattern-B askQuestion; schema extended to carry all 4 blocks (facets + sections + visualisations + additional_focus_areas) |
| Top-level facets (final, post-confirmation) | `facets.md` | Single navigational entry point; updated post-consolidation with the Branch & Leaf Index |
| Init suggestions (confirmed payload) | `init-suggestions-{ts}.yml` | Written by depth-0 manager during step 4b resume (after combined Pattern-B askQuestion resolves); schema: `confirmed_sections` + `confirmed_visualisations` + `additional_focus_areas` blocks; read by report-generation contract and adversarial reviewer Dim 13; linked from `facets.md` Branch & Leaf Index `## Top-level artifacts` |
| Branch (depth 1, 2, 3) | `branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md` | `D` ∈ {1,2,3}; `S = 0` at depth 1, `S` ∈ {1,2,3} at depth 2, `S` ∈ {1,...,9} at depth 3 |
| Branch (intermediate, Phase B working draft) | `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}-findings.md` | Research mode only; deleted after Phase G promotion |
| Peer review (Research mode) | `branch-{N}-peer-review-{branchSlug}-{ts}.md` | One per branch |
| Pending deep-facet confirmation request | `pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml` | Only when `confirmDeepFacets ≠ none`; `D` is the **parent** agent's depth |
| Confirmed deep-facet response | `confirmed-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml` | Same path-id and `{ts}` as the pending file |
| Adversarial review iteration | `review-pre-report-{ts}-iter-{N}.md` | `N` ∈ {1, 2, 3}; iteration cap |
| Finalisation enhancements (single-model) | `finalisation-enhancements.yml` | Written by depth-0 manager during step 8 consolidation reflection (in-pass, no extra read); top-5 ranked candidates; calling agent updates in place with `accepted` / `treatment` / `decided_at_utc` after `Q-Finalisation-Enhancements` resolves; linked from `facets.md` Branch & Leaf Index `## Top-level artifacts` |
| Finalisation enhancements (ensemble per-tree) | `{model-subdir}/finalisation-enhancements.yml` | Written by per-tree depth-0 consolidation manager before returning to ensemble aggregator; carries `source_tree:` + `surfaced_to_root: null` placeholder (aggregator fills); NO per-tree askQuestion fires |
| Follow-up artefact: additional meditation | `follow-up-meditation-{ts}.yml` | Written by calling agent after `Q-Finalisation-Enhancements` resolves for `additional_meditation` items with `treatment ∈ {queue, spawn_now}`; `{ts}` is the calling-agent write timestamp |
| Follow-up artefact: extracted spec | `follow-up-spec-{ts}.yml` | Written by calling agent for `extracted_spec` items with `treatment ∈ {queue, spawn_now}` |
| Follow-up artefact: extracted memories | `follow-up-memories-{ts}.yml` | Written by calling agent for `extracted_memories` items with `treatment ∈ {queue, spawn_now}` |
| Follow-up artefact: expanded branch | `follow-up-expansion-{ts}.yml` | Written by calling agent for `expanded_branch` items with `treatment ∈ {queue, spawn_now}` |
| Process retrospective | `retrospective-{ts}.md` | One per meditation; process analysis separate from subject-matter outputs |
| Report HTML | `report-{topic-slug}-{ts}.html` | Shares `{ts}` with PDF pair |
| Report PDF | `report-{topic-slug}-{ts}.pdf` | Shares `{ts}` with HTML pair |

**Research-mode-only files** (noted in table above): `branch-*-findings.md` (Phase B draft), peer-review files (`branch-{N}-peer-review-*.md`), `facet-registry.yml` (global facet allocation), `citations-index.yml` (append-only citation index), `.facet-registry.lock/` (transient mkdir-mutex).

## `facets.md` frontmatter — model strategy fields

When the depth-0 manager writes the final `facets.md` (step 4b promotion) and refreshes it post-consolidation (step 9 Branch & Leaf Index update), include the following fields in the frontmatter to record the resolved model strategy:

```yaml
---
# ... existing facets.md frontmatter fields (topic_slug, mode, confirmed_at_utc, etc.) ...
model_strategy:
  mode: "none" | "random" | "per_branch" | "ensemble_max"
  resolved_model_slug: null | "<slug>"             # set when mode == "random"
  resolved_model_label: null | "<label>"
  branch_assignments: []                           # set when mode == "per_branch"
    # - branch_index: 1
    #   slug: "<slug>"
    #   label: "<label>"
  assignment_policy_note: null | "<note>"          # set when mode == "per_branch" and poolSize < branchCount
---
```

The `model_strategy` block is read by the report skill to drive per-branch attribution annotations and footer rendering. It is also read by the calling agent's step-10 presentation to surface the model strategy alongside the rest of the meditation outputs.

## Placeholders

These placeholders are defined once here; all other meditation artefacts reference these definitions:

- `{topic-slug}` is the slug component of the working-directory name (`{yyyymmdd}-{topic-slug}/`) — extract as everything after the leading `yyyymmdd-`.
- `{slug}` (in branch filenames) is the kebab-case slug derived for that branch (depth 1) or that subfocus (depth 2/3); max 40 chars; lowercase; alphanumerics + hyphens only; stop-words stripped; the most meaningful 3–6 words.
- `{ts}` is the UTC timestamp `yyyymmddHHMMSS` captured at the moment the file is written: `date -u +%Y%m%d%H%M%S`.
- `{N}`, `{D}`, `{S}` are zero-padded numerals used as written above (`branch-1`, not `branch-01`).

## Prefix-Glob Polling Rule (never equality)

Because the `{slug}` + `{ts}` suffix is not predictable until the writing agent commits the file, every polling agent must use **prefix-glob matching**:

```
# Branch-output polls
branch-{N}-depth-1-sub-0-*.md            # depth-1 outputs
branch-{N}-depth-{D}-sub-{S}-*.md        # depth-D≥2 child outputs (one per child sibling-index)

# Peer review polls (Research mode)
branch-{N}-peer-review-*.md

# Report pair polls (verification gate)
report-{topic-slug}-*.html
report-{topic-slug}-*.pdf

# Pending deep-facet confirmation polls (depth-0 manager, when confirmDeepFacets ≠ none)
pending-facets-*.yml
```

Use `ls -1t <workingDir>/<glob> 2>/dev/null | head -n 1` to resolve the **latest** matching artefact when multiple regenerations have occurred (relevant for reports and review iterations).

**Never hard-code these names.** All references in this document, in the agent definition, and in the Branch & Leaf Index match these files via the prefix glob `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf`. Never hard-code `report.html` / `report.pdf`.

## Process Retrospective Template

Filename: `retrospective-{yyyymmddHHMMSS}.md` — use the same `{ts}` as the report pair when one was generated, or capture a fresh UTC timestamp if no report was produced (on `ESCALATE`).

**Always written**, including on `ESCALATE` (process analysis is especially valuable when the review cycle failed).

```markdown
---
mode: "research" | "quick"
topic_slug: "{topic-slug}"
generated_utc: "2026-05-17T12:34:56Z"
verdict: "PASS" | "PASS_WITH_ADVISORIES" | "ESCALATE"
---

## Process Retrospective — {topic title}

### Summary Statistics
- **Mode**: Research | Quick
- **Total agents spawned**: {count} (N depth-1 + N depth-2 + N depth-3 + N peer-review + N adversarial-review iterations)
- **Branch files produced**: {count} ({breakdown by depth})
- **Peer reviews**: {count} (Research mode) | N/A (Quick mode)
- **Adversarial review iterations**: {count}, final verdict: {verdict}
- **MUST_FIX findings**: {total found} → {applied} auto-fixed, {escalated} user-escalated, {unresolved} unresolved
- **SHOULD_FIX findings**: {total found} → {applied} auto-fixed
- **ADVISORY findings**: {total found}
- **Missing slots**: {list or "none"}
- **Facet regeneration attempts**: {count} (0 = confirmed on first try)
- **Deep-facet confirmations**: {count} (0 = confirmDeepFacets was "none")

### What Went Well
{Substantive observations about the process — not generic praise. Examples:}
- Which branches produced the richest findings and why
- Whether the facet partitioning created clean, non-overlapping exploration paths
- Effective cross-branch convergences discovered independently
- Citation coverage completeness
- Where peer review added genuine value (Research mode)
- How well the adversarial review caught real issues vs false positives

### What Could Be Improved
{Honest assessment of process weaknesses. Examples:}
- Branches or depth-2/3 nodes that produced thin or repetitive content
- Facet partitioning problems (overlap, gaps, one facet too broad)
- Citation gaps or weak sourcing patterns
- Adversarial review findings that should have been caught earlier
- Any ESCALATE causes and whether they were avoidable
- Coordination issues (stale locks, slow polling, missing files)
- Depth-3 leaves that added little incremental value over their depth-2 parent
- Whether Quick mode would have been sufficient (if Research was used) or vice versa

### Structural Observations
{Analysis of the research tree's shape and efficiency:}
- Branch balance — did all 3 branches produce comparable depth and quality?
- Depth utility — did depth-3 add meaningful detail beyond depth-2?
- Peer review impact — what fraction of peer-review findings changed the consolidation? (Research mode)
- Adversarial review efficiency — how many iterations were needed and could the first pass have been cleaner?
- Subject-matter focus compliance — were there process-language violations that needed fixing?

### Recommendations for Future Meditations
{Actionable suggestions for improving the next meditation on a similar topic:}
- Facet suggestions if the topic were re-explored
- Mode recommendation (Research vs Quick) for this topic's complexity level
- Areas where deeper exploration (4+ depths or more branches) would have helped
- Areas where the tree was over-provisioned
```

The depth-0 manager fills in every section with specifics from the actual meditation run. Generic or placeholder content is not acceptable.

## Branch & Leaf Index Template (Single-Model Variant)

After consolidation completes, the depth-0 manager **must update `facets.md`** by appending this Branch & Leaf Index section. Glob the working directory for actual filenames rather than reconstructing names from memory. Use relative paths (no `./` prefix needed).

**Construction rule**: glob the working directory for actual filenames (`branch-*-depth-*-sub-*-*.md`, `branch-*-peer-review-*.md`, `review-pre-report-*-iter-*.md`, `confirmed-facets-*.yml`, the latest `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf` pair). Resolve `{topic-slug}` from the working-directory name and resolve `{ts}` placeholders by globbing for actual on-disk files. **Never write literal `{topic-slug}-{ts}` placeholder text into `facets.md`.**

**Required structure** (appended below the existing `facets.md` frontmatter and content):

    ---
    (existing facets.md frontmatter / content above this line is unchanged)
    ---

    ## Branch & Leaf Index

    ### Branch 1 — {branch-1 facet title}
    **Subfocus**: {one-line facet description}
    **Model**: {branch-1 model label} _(only when `modelStrategy.mode == "per_branch"`; for `random` show `model_strategy:` line under `### Index metadata` instead)_

    - **Depth 1 (root)**: [{branch-1-slug}](branch-1-depth-1-sub-0-{branch-1-slug}-{ts}.md)
    - **Depth 2** (3 subfocuses):
      - [Sub 1 — {d2-sub-1-slug}](branch-1-depth-2-sub-1-{d2-sub-1-slug}-{ts}.md)
      - [Sub 2 — {d2-sub-2-slug}](branch-1-depth-2-sub-2-{d2-sub-2-slug}-{ts}.md)
      - [Sub 3 — {d2-sub-3-slug}](branch-1-depth-2-sub-3-{d2-sub-3-slug}-{ts}.md)
    - **Depth 3** (up to 9 leaves):
      - Under D2-sub-1:
        - [Sub 1 — {slug}](branch-1-depth-3-sub-1-{slug}-{ts}.md)
        - [Sub 2 — {slug}](branch-1-depth-3-sub-2-{slug}-{ts}.md)
        - [Sub 3 — {slug}](branch-1-depth-3-sub-3-{slug}-{ts}.md)
      - Under D2-sub-2: ...
      - Under D2-sub-3: ...
    - **Peer review** (Research mode only): [branch-1 peer review](branch-1-peer-review-{branch-1-slug}-{ts}.md)

    ### Branch 2 — ...
    ### Branch 3 — ...

    ### Top-level artifacts
    - [Consolidation](consolidation.md)
    - [Process Retrospective](retrospective-{ts}.md)
    - [Report (HTML)](report-{topic-slug}-{ts}.html)
    - [Report (PDF)](report-{topic-slug}-{ts}.pdf)
    - Adversarial review iterations (one entry per `review-pre-report-*-iter-*.md` discovered):
      - [Review iter 1](review-pre-report-{ts}-iter-1.md)
      - [Review iter 2](review-pre-report-{ts}-iter-2.md) _(only if iteration 2 ran)_
      - [Review iter 3](review-pre-report-{ts}-iter-3.md) _(only if iteration 3 ran)_
    - Facet confirmation trail (one entry per pending/confirmed pair discovered):
      - [Confirmed facets — branch 1 depth 1 sub 0](confirmed-facets-branch-1-depth-1-sub-0-{ts}.yml) _(only when `confirmDeepFacets ≠ none`)_
      - …
    - [Facet registry](facet-registry.yml) _(Research mode only)_
    - [Citations index](citations-index.yml) _(Research mode only)_
    - [Init suggestions](init-suggestions-{ts}.yml)
    - [Finalisation enhancements](finalisation-enhancements.yml) _(only when written by depth-0 consolidation reflection)_
    - Follow-up artefacts (one entry per `follow-up-{type}-{ts}.yml` discovered):
      - [Follow-up: additional meditation — {title}](follow-up-meditation-{ts}.yml) _(only if present; treatment: queue)_
      - [Follow-up: extracted spec — {title}](follow-up-spec-{ts}.yml) _(only if present)_
      - [Follow-up: extracted memories — {title}](follow-up-memories-{ts}.yml) _(only if present)_
      - [Follow-up: expanded branch — {title}](follow-up-expansion-{ts}.yml) _(only if present)_

    ### Index metadata
    - **Generated**: {ISO 8601 timestamp of index update}
    - **Mode**: `research` | `quick`
    - **Model strategy**: `none` | `random ({label})` | `per_branch (b1: {label}, b2: {label}, b3: {label}, …)` | `ensemble_max (member: {label})` _(line ALWAYS written; values reflect `modelStrategy.mode` and any resolved per-branch assignments / picked model from the depth-0 manager's in-memory `modelStrategy`)_
    - **Total files indexed**: {count}
    - **Missing slots**: {list any branch/depth/sub combinations that did not produce a file, or "none"}

**Conventions**:
- Display label of each link is the file's `subfocus_slug` from frontmatter, prefixed with the local sub-index.
- Group depth-3 leaves under their depth-2 parent. Sibling indices 1–3 belong to D2-sub-1, 4–6 to D2-sub-2, 7–9 to D2-sub-3.
- If a slot didn't produce a file, omit the link AND list the slot under "Missing slots".
- The "Top-level artifacts" subsection always lists `consolidation.md`, `retrospective-{ts}.md`, plus the latest report HTML/PDF pair (when generated), every review iteration discovered, and every confirmed-facets pair discovered. Registry / citations-index lines appear only in Research mode.
- Quick mode produces the same index minus per-branch "Peer review" lines and the two Research-only registry / index lines.
- When the adversarial review verdict was `ESCALATE` the report HTML / PDF lines are omitted (no report was generated), but every `review-pre-report-*-iter-*.md` is still linked.
- Pending coordination files (`facets-pending-*.yml` and `pending-facets-*.yml`) are **not** linked from the index; only the corresponding confirmed counterparts are linked.
- The per-branch `**Model**:` line appears only when `modelStrategy.mode == "per_branch"`. For `mode ∈ {"none", "random", "ensemble_max"}` the per-branch model line is omitted (a single tree-wide model — or no model override — is recorded in the **Model strategy** line of "Index metadata" instead).

## Branch & Leaf Index Template (Ensemble Variant)

For ensemble meditations, the ensemble root `facets.md` (shared, bare — no Branch & Leaf Index) is supplemented by per-model `facets.md` files (each with its own Branch & Leaf Index in the standard single-model format above). The ensemble report filenames are handled by the ensemble working-directory structure below.

## Ensemble Working-Directory Structure

```
meditations/{yyyymmdd}-{topic-slug}-ensemble/
├── facets.md                                    # shared confirmed facets (bare — no Branch & Leaf Index)
├── finalisation-enhancements.yml                # root combined YAML written by aggregator (step 3d)
├── cross-model-synthesis.md                     # aggregation output
├── ensemble-report-{topic-slug}-{ts}.html       # ensemble-level report
├── ensemble-report-{topic-slug}-{ts}.pdf        # ensemble-level PDF
├── model-gpt-5.5/                               # complete meditation tree for GPT 5.5
│   ├── facets.md                                # per-model copy with Branch & Leaf Index
│   ├── consolidation.md
│   ├── finalisation-enhancements.yml            # per-tree YAML written by per-tree depth-0 manager
│   ├── facet-registry.yml                       # Research mode only
│   ├── citations-index.yml                      # Research mode only
│   ├── branch-*-depth-*-sub-*-*.md
│   ├── branch-*-peer-review-*.md                # Research mode only
│   ├── review-pre-report-*-iter-*.md
│   ├── retrospective-{ts}.md
│   ├── report-{topic-slug}-{ts}.html
│   └── report-{topic-slug}-{ts}.pdf
├── model-opus-4.7/                              # complete meditation tree for Opus 4.7
│   └── ...same structure...
└── model-gemini-pro-3.1/                        # complete meditation tree for Gemini Pro 3.1
    └── ...same structure...
```

Subdirectory names use the kebab-case version of each model's `label` from `cruxMemories.meditate.modelPool`, prefixed with `model-` (e.g. `model-gpt-5.5`, `model-opus-4.7`, `model-gemini-pro-3.1`).

**Ensemble filename conventions**:

| Artefact | Filename pattern | Location |
|----------|------------------|----------|
| Shared facets | `facets.md` | Ensemble root |
| Root combined finalisation enhancements | `finalisation-enhancements.yml` | Ensemble root |
| Per-tree finalisation enhancements | `{model-subdir}/finalisation-enhancements.yml` | Per-model subdir |
| Per-model tree | `model-{label-slug}/` | Ensemble root |
| Cross-model synthesis | `cross-model-synthesis.md` | Ensemble root |
| Ensemble report HTML | `ensemble-report-{topic-slug}-{ts}.html` | Ensemble root |
| Ensemble report PDF | `ensemble-report-{topic-slug}-{ts}.pdf` | Ensemble root |

Per-model subdirectories follow the standard single-model **Coordination Conventions** for all internal files.

## Cross-Skill References

This skill is the **leaf utility** — all five other meditation skills reference it:
- `crux-skill-memory-meditation-research` — filename grammar for `init-suggestions-{ts}.yml`, Phase B draft files, `facet-registry.yml`, `citations-index.yml`, peer review files; polling loop; lock semantics
- `crux-skill-memory-meditation-quick` — filename grammar for branch outputs, polling loop
- `crux-skill-memory-meditation-ensemble` — ensemble working-directory layout; per-tree `finalisation-enhancements.yml` filename row; root `finalisation-enhancements.yml` filename row
- `crux-skill-memory-meditation-review` — review-iteration filename row; Branch & Leaf Index links review iterations
- `crux-skill-memory-meditation-report` — report filename grammar (never hard-code `report.html`/`report.pdf`); fresh-timestamp respawn rule; prefix-glob latest-wins
