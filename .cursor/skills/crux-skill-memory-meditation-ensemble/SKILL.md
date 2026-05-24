---
name: crux-skill-memory-meditation-ensemble
description: Ensemble Aggregation function for meditation: reads N model consolidations, writes `cross-model-synthesis.md`, performs K10 root cross-model reflection (step 3c), manages K10 layered cadence steps 3b–3f (per-tree `finalisation-enhancements.yml` reads + root combined YAML write with `cross_model_candidates` + `union_candidates`), returns single combined `needs_user_input`, dispatches resume-handler by `source` provenance, and hands off to the report skill for ensemble HTML+PDF generation. Use when the `crux-cursor-meditation-guide` agent is spawned with `ensembleAggregation: true`.
---

# CRUX Skill: Memory Meditation — Ensemble Aggregation

Implements the Ensemble Aggregation function: cross-model synthesis after N independent meditation trees have completed, K10 layered cadence (steps 3b–3f), ensemble report extras, and K10 Ensemble Respawn Targeting. This skill is **never** loaded by per-model tree agents — only by the aggregator spawn.

## When to Use

Load this skill **only** when:
- The `crux-cursor-meditation-guide` agent is spawned with `ensembleAggregation: true`
- You are the cross-model aggregator spawned by the calling agent's Ensemble Protocol (step 8 of the `/crux-meditate` command)

This skill is **`modelStrategy.mode == "ensemble_max"` only**. The other two pool-using strategies — `random` and `per_branch` — are single-tree variants that do NOT spawn an aggregator and do NOT produce a `cross-model-synthesis.md` or ensemble report pair. They run the standard single-tree workflow with model dispatch driven by the `modelStrategy:` payload (see the `/crux-meditate` command's **Model Strategy payload** section).

**Never load this skill** in:
- Per-model tree Research or Quick mode workflows (per-model trees use the `crux-skill-memory-meditation-research` or `crux-skill-memory-meditation-quick` skill)
- Single-tree `random` runs (no aggregation needed — one model, one report)
- Single-tree `per_branch` runs (no aggregation needed — one tree with per-branch model attribution recorded in `facets.md` and the standard single-tree report)

## Prerequisites

1. All N per-model meditation trees have completed (calling agent confirms before spawning the aggregator)
2. `comprehensiveness:` payload is present in the spawn prompt — abort with: "`comprehensiveness:` payload required; missing from spawn prompt — caller misconfigured" if missing
3. `theming:` payload is present — abort with a clear error if missing

## Input Parameters (Ensemble Aggregation invocation)

```yaml
ensembleAggregation: true
ensembleWorkingDir: "<absolute path to the ensemble root directory>"
modelSubdirs: 
  - slug: "gpt-5.5-medium"
    label: "GPT 5.5"
    subdirPath: "<absolute path to model-gpt-5.5/>"
  # ... one entry per model
confirmedFacets: 
  - index: 1
    title: "{facet-1-title}"
    subfocus: "{facet-1-subfocus}"
    slug: "{facet-1-slug}"
  # ... 3 facets (shared, user-confirmed)
theming: { ... }                  # shared Theme Preflight payload — REQUIRED
comprehensiveness: { ... }        # shared comprehensiveness payload — REQUIRED; abort if missing
meditateMode: "research" | "quick"
topicSlug: "{topic-slug}"         # for report filenames
```

## Ensemble Aggregation Workflow

### Step 1 — Read All Model Consolidations

For each model subdirectory in `modelSubdirs`, read `consolidation.md`. Also read each model's `facets.md` (with Branch & Leaf Index) to understand the tree structure. Optionally read individual branch files (`branch-*-depth-*-sub-*-*.md`) for detail when consolidations alone are insufficient to assess convergence/divergence.

### Step 2 — Cross-Model Analysis

For each confirmed facet, compare each model's findings:
- **Convergence detection**: Identify conclusions that all N models independently reached. Score convergence strength by counting how many models agree and how closely their phrasing and evidence align.
- **Divergence detection**: Identify conclusions where models disagree. For each divergence, extract each model's position, reasoning, and supporting evidence. Assess which position is better-supported based on citation strength and internal consistency.
- **Unique insight detection**: Identify findings that only one model surfaced. Assess credibility by checking whether the finding is well-cited and internally consistent, or whether it might be a hallucination (single-source, weakly cited, inconsistent with convergent findings).
- **Evidence quality comparison**: For shared claims, compare citation breadth and depth across models. Note which model found the most/strongest citations, and which relied on different source types (memory corpus, code analysis, web sources).
- **Reasoning style comparison**: Analyse structural differences in how each model organized its exploration — subfocus derivation patterns, depth allocation, narrative vs. enumeration style, consolidation quality.

### Step 3 — Write `cross-model-synthesis.md`

Write the synthesis document to the ensemble root directory. Every finding carries `[model: {label}]` attribution markers. Convergent findings use `[models: all]`. The `## Citations` section is a unified, deduplicated list across all models with per-citation model attribution.

Required schema:
```markdown
---
ensemble_mode: true
meditate_mode: "research" | "quick"
model_count: {N}
models:
  - slug: "gpt-5.5-medium"
    label: "GPT 5.5"
    subdir: "model-gpt-5.5"
  - slug: "claude-opus-4-7-thinking-xhigh"
    label: "Opus 4.7"
    subdir: "model-opus-4.7"
  - slug: "gemini-3.1-pro"
    label: "Gemini Pro 3.1"
    subdir: "model-gemini-pro-3.1"
aggregator_model: "{model slug or 'caller'}"
timestamp_utc: "{yyyymmddHHMMSS}"
---

## Executive Summary
{One-paragraph verdict synthesizing the strongest findings across all models.
 Lead with the substantive conclusion, not a description of the ensemble process.}

## Convergence — High-Confidence Findings
{Findings that all N models independently arrived at. Each finding includes:
 - The shared conclusion
 - How each model framed or supported it (with [model: label] attribution)
 - Combined citation strength (union of citations from all models)
 These are the most trustworthy outputs of the meditation.}

## Divergence — Areas of Disagreement
{Findings where models reached different conclusions about the same facet.
 Each divergence includes:
 - The question or claim at issue
 - Each model's position with its reasoning and evidence ([model: label])
 - The aggregator's assessment of which position is better-supported and why
 - A confidence indicator (strong disagreement vs. nuanced difference)
 These are the most valuable outputs — they reveal where the topic is genuinely
 contested or where model-specific knowledge gaps exist.}

## Unique Insights — Single-Model Discoveries
{Findings surfaced by only one model that the others missed entirely.
 Each insight includes:
 - The finding and its evidence ([model: label])
 - Why the other models likely missed it (knowledge gap, different framing,
   different depth allocation)
 - The aggregator's assessment of whether the insight is credible and valuable
 These represent potential blind spots — valuable if real, risky if hallucinated.}

## Evidence Quality Comparison
{Per-facet assessment of citation strength across models:
 - Which model found the most/strongest citations for shared claims
 - Which model relied most on memory corpus vs. code analysis vs. web sources
 - Citation coverage gaps per model}

## Reasoning Style Comparison
{Meta-observation of how each model structured its analysis:
 - Depth vs. breadth trade-offs per model
 - Which model produced the most novel subfocus derivations at depth-2/3
 - Stylistic patterns (e.g. one model favours enumeration, another favours
   narrative synthesis)
 - Which model's consolidation was most/least aligned with the Subject-Matter
   Focus rule}

## Recommended Synthesis
{The aggregator's best-judgment unified analysis that:
 - Anchors on convergent findings as the foundation
 - Incorporates the best-supported position from each divergence
 - Integrates credible unique insights with appropriate hedging
 - Calls out remaining open questions where even the ensemble cannot resolve
   the disagreement}

## Per-Model Report Index
{Links to each model's individual report and consolidation for drill-down:
 - [GPT 5.5 Report (HTML)](model-gpt-5.5/report-{topic-slug}-{ts}.html)
 - [GPT 5.5 Report (PDF)](model-gpt-5.5/report-{topic-slug}-{ts}.pdf)
 - [GPT 5.5 Consolidation](model-gpt-5.5/consolidation.md)
 - ... (one group per model)}

## Citations
{Unified, deduplicated citation list across all models. Each entry includes
 [model: label] markers indicating which model(s) cited it. Backlinks to
 the sections that used each citation.}
```

### Step 3b — K10 Ensemble Layered Cadence: Read Per-Tree `finalisation-enhancements.yml` Files

Each per-tree depth-0 manager wrote `{model-subdir}/finalisation-enhancements.yml` with `source_tree: "{model-subdir}"` and `surfaced_to_root: null` placeholder fields. Read all per-tree YAMLs.

**K10 per-tree YAML schema** (each per-tree depth-0 manager writes this during step 8, before returning to the aggregator):
```yaml
---
generated_utc: "{utc-timestamp}"
topic_slug: "{topic-slug}"
mode: "research"      # or "quick"
ensemble: true
source_tree: "{model-subdir}"   # e.g. "gpt-5.5-medium", "claude-opus-4-6", etc.
rubric: { impact_score_max: 10, insight_value_score_max: 10, minimum_impact_threshold: 6, weights: { impact: 1.0, insight_value: 1.0 }, formula: "product" }
degradation_reason: null | "..."
---
candidates:
  - id: "{type}-{ts}"
    type: "{one-of-11-types}"
    cost_class: "cheap"   # or "expensive"
    title: "{title}"
    description: "{description}"
    impact_score: {N}
    insight_value_score: {N}
    composite_score: {N}
    source_tree: "{model-subdir}"   # required; enables root-level provenance labelling
    surfaced_to_root: null          # placeholder; aggregator fills true | false after union
    source_signals: [...]
    payload: { ... }
    accepted: null
    treatment: null
    decided_at_utc: null
```

**NOTE**: NO per-tree askQuestion fires — per-tree YAMLs are write-only at the per-tree level (OQ #10 resolved as "both layered" with single combined root gate).

### Step 3c — K10 Root Cross-Model Reflection (in the SAME LLM pass as `cross-model-synthesis.md`)

After writing `cross-model-synthesis.md`, run a SECOND reflection pass over: (a) all per-tree `consolidation.md` files (already in context from step 1); (b) all per-tree `finalisation-enhancements.yml` files (from step 3b); (c) `cross-model-synthesis.md` itself (just written). Produce up to **5 cross-model candidates** emergent from looking across all trees together. Rank high for:

1. **Cross-tree convergence**: ≥2 trees independently surfaced the same enhancement type (convergence signal). Apply `insight_value_score ≥ 7` calibration when convergence is explicit.
2. **Cross-model-only patterns**: visible only across models (e.g. a divergence between two trees suggests an `extracted_spec` one tree didn't see).
3. **Cross-model-synthesis-side opportunities**: `cross_branch_synthesis_section` is naturally cross-tree and often a high-value candidate.

Each cross-model candidate carries `source: "cross_model"`. Use the same impact × insight-value rubric (1–10 per axis) with the `insight_value_score ≥ 7` calibration boost for convergent findings.

### Step 3d — K10 Root Combined YAML Write

Write `{ensembleWorkingDir}/finalisation-enhancements.yml` (no `{model-subdir}` segment):
```yaml
---
generated_utc: "{utc-timestamp}"
topic_slug: "{topic-slug}"
mode: "research"      # or "quick"
ensemble: true
ensemble_pool_size: {N}   # modelPool size
rubric: { impact_score_max: 10, insight_value_score_max: 10, minimum_impact_threshold: 6, weights: { impact: 1.0, insight_value: 1.0 }, formula: "product" }
degradation_reason: null
---
cross_model_candidates:
  # up to 5 ranked candidates from the aggregator's cross-model reflection
  - id: "{type}-{ts}"
    type: "{one-of-11-types}"
    cost_class: "cheap"
    title: "{title}"
    description: "{description}"
    impact_score: {N}
    insight_value_score: {N}
    composite_score: {N}
    source: "cross_model"
    source_signals: ["[cross-model-synthesis: ...]"]
    convergence_signal: true | false   # true when ≥2 trees independently surfaced this
    payload: { ... }
    accepted: null
    treatment: null
    decided_at_utc: null
union_candidates:
  # denormalised top-N (capped at 5) by composite_score across (per_tree × N) + (cross_model × 5)
  # each entry is one of the per-tree or cross-model candidates; includes source provenance
  - id: "{id}"
    type: "{type}"
    cost_class: "cheap" | "expensive"
    title: "{title}"
    description: "{description}"
    impact_score: {N}
    insight_value_score: {N}
    composite_score: {N}
    source: "cross_model"   # or "tree:{model-subdir}" e.g. "tree:gpt-5.5-medium"
    source_signals: [...]
    payload: { ... }
    accepted: null
    treatment: null
    decided_at_utc: null
    surfaced_to_root: true   # always true for entries in union_candidates
```

After writing the root YAML, **write-back `surfaced_to_root` annotations to every per-tree YAML**: for each per-tree candidate, set `surfaced_to_root: true` if the candidate's `id` appears in `union_candidates`; set `surfaced_to_root: false` otherwise. This is the ONLY mutation the aggregator makes to per-tree YAMLs.

### Step 3e — Return K10 `needs_user_input` Block to the Calling Agent (single combined root gate)

This is the single combined root gate — recommended posture per architecture design (alternative per-tree gates are rejected because they serialise trees, multiply user prompts, and prevent cross-model insight from being visible at decision time). Do NOT call `AskQuestion` — this is the calling agent's responsibility.

```yaml
needs_user_input:
  reason: "finalisation-enhancements-gate"
  pattern: "B"
  context: |
    Post-consolidation reflection (per-tree + cross-model) surfaced {N} candidate
    finalisation enhancements across all {M} trees. Multi-select 0–5. Each option
    label includes provenance: {title} [{cost_class}] ({source-label}) — composite={N}.
    Source labels: "cross-model" or "from tree: {model-label}".
    Cross-model candidates tend to surface patterns no single model tree saw alone.
  decision_required: true
  files_written:
    - "finalisation-enhancements.yml"
    - "{model-subdir-1}/finalisation-enhancements.yml"
    - "{model-subdir-2}/finalisation-enhancements.yml"
    # ... one per tree
  resume_handler_contract:
    expected_input:
      finalisation_enhancements_path: "{ensembleWorkingDir}/finalisation-enhancements.yml"
      # calling agent has updated the root YAML in place with accepted/treatment/decided_at_utc
```

**Model-label resolution fallback**: if `cruxMemories.meditate.modelPool` no longer contains the `{model-subdir}` slug at continuation time (model retired), label falls back to `"Unknown model ({model-subdir})"`.

### Step 3f — K10 Ensemble Resume-Handler for Accepted Enhancements

Called after the calling agent resolves the gate and passes back `finalisation_enhancements_path`. Re-read the updated root `finalisation-enhancements.yml`. For each accepted `union_candidates` entry:

- **`accepted: true, treatment: "respawn"` (cheap), `source: "cross_model"`**: bundle into the **ensemble synthesis report**'s first adversarial-review iteration respawn payload (`accepted_finalisation_enhancements:` list in the cross-model adversarial reviewer invocation).
- **`accepted: true, treatment: "respawn"` (cheap), `source: "tree:{model-subdir}"`**: bundle into the **per-tree `{model-subdir}` report**'s first adversarial-review iteration respawn payload.
- **`accepted: true, treatment: "queue"` (expensive)**: write `follow-up-{type}-{ts}.yml` next to the appropriate location: per-tree consolidation directory for tree-sourced; ensemble root for cross-model-sourced. Do NOT spawn agents.
- **`accepted: true, treatment: "spawn_now"` (expensive)**: defer spawning until AFTER the corresponding adversarial-review cycle completes. Track in `pending_spawn_now: [...]` per target (per-tree vs ensemble).

**Non-infinite-loop guarantee (ensemble layered cadence)**: per-tree reflections happen exactly once per tree (bounded by `modelPool` size = constant); root cross-model reflection happens exactly once; single combined root gate fires once per invocation. Per-tree adversarial review cycles each have their own ≤3 cap (unchanged); cross-model adversarial review has its own ≤3 cap. Total: at most `N + 1` reflection writes + 1 user gate + `(N + 1) × 2 useful respawns × 1 report-skill run each` = `O(N)` total bounded work. Cannot infinite-loop.

### Step 4 — Generate the Ensemble Report (HTML + PDF)

Follow the same mandatory report contract as single-model reports (per the `crux-skill-memory-meditation-report` skill) with the ensemble-specific additions below. Key differences from single-model reports:
- The hero/executive summary leads with the cross-model verdict (what's convergent, what's contested)
- Per-facet sections show model comparisons side-by-side rather than a single narrative
- The agreement heatmap (facet × model matrix) is the signature visualization
- Per-model drill-down links connect to each model's individual HTML report
- The model attribution Sankey, citation Venn, and confidence radar are ensemble-specific recommended visualizations
- All standard content minimums (4+ chart types, 3+ infographics, interactive calculators, filterable tables, light/dark mode, PDF degradation) still apply; the minima are level-driven per `comprehensiveness.minima.*`

Filenames: `ensemble-report-{topic-slug}-{ts}.html` / `.pdf` in the ensemble root, with paired timestamps.

### Step 5 — Return to Calling Agent

Return the ensemble working directory path, the `cross-model-synthesis.md` path, the ensemble report HTML+PDF pair paths, the ordered list of per-model subdirectory paths (each containing its own `consolidation.md`, `facets.md`, `report-{topic-slug}-{ts}.html` / `.pdf` pair, and `{model-subdir}/finalisation-enhancements.yml`), and (when any expensive `spawn_now` items were accepted) a `pending_spawn_now: [...]` list structured as `[{source: "cross_model"|"tree:{model-subdir}", type: "...", follow_up_file: "..."}]` so the calling agent can spawn at the right moment. Include the same follow-up reminder: further content edits, visual refinements, theme adjustments, contrast tweaks, or regenerated report variants can be requested in a new agent session pointed at the ensemble meditation folder.

## Ensemble-Specific Structural Elements (Report Additions)

The ensemble report layers these elements **on top of** the standard mandatory minimums from the `crux-skill-memory-meditation-report` skill:

- **Model comparison hero**: instead of a single stat-card row, show N model cards side-by-side, each with that model's headline finding and a convergence/divergence indicator
- **Per-facet comparison cards**: for each confirmed facet, show each model's key conclusion in parallel columns/cards with `[model: label]` attribution and a visual convergence indicator (green = all agree, amber = partial agreement, red = disagreement)
- **Agreement heatmap** (required): a facet × model matrix (Chart.js or D3) where cell color encodes the degree of agreement between each model pair for each facet. This is the ensemble report's signature visualization.
- **Divergence deep-dives**: each major divergence gets its own section with the competing positions presented side-by-side, evidence compared, and the aggregator's assessment
- **Per-model drill-down links**: every section includes links to the corresponding section in each model's individual HTML report

**Ensemble-specific visualizations** (in addition to the standard minimums):
- **Agreement heatmap** (required): facet × model matrix
- **Model attribution Sankey** (recommended): flow diagram showing how findings from each model fed into the convergence/divergence/unique categories
- **Citation Venn diagram** (recommended): overlap visualization showing which citations were shared vs. model-unique
- **Confidence radar**: per-facet confidence scores from each model, overlaid on a single radar chart

**Model attribution citation format**: All findings in the ensemble report carry `[model: {label}]` citation markers (e.g. `[model: GPT 5.5]`, `[model: Opus 4.7]`). These appear alongside standard citation markers (`[memory: ...]`, `[file: ...]`, etc.) and are listed in the `## Citations` section with backlinks. When a finding is convergent (all models agree), use `[models: all]` as a shorthand.

## K10 Ensemble Respawn Targeting

When an accepted enhancement was sourced from a per-tree candidate vs a cross-model candidate, the report-skill respawn targets a different report:

- **Per-tree-sourced accept** (`source: "tree:{model-subdir}"` in the root `union_candidates` list): the respawn payload for the **per-tree report** (`{model-subdir}/report-{topic-slug}-{ts}.html/.pdf` pair) gains the entry under `accepted_finalisation_enhancements`. The per-tree report skill respawns and the regenerated per-tree report incorporates the accepted enhancement. The cross-model synthesis report is NOT respawned for per-tree-sourced accepts.
- **Cross-model accept** (`source: "cross_model"`): the respawn payload for the **cross-model synthesis report** (`ensemble-report-{topic-slug}-ensemble-{ts}.html/.pdf`) gains the entry. The cross-model synthesis report skill respawns and the regenerated synthesis report incorporates the accepted enhancement. Per-tree reports are NOT respawned for cross-model accepts.

**Cost-ack re-presentation at ensemble for `spawn_now`**: when the user opts an expensive item into `spawn_now` at the ensemble root gate, the cost-ack re-presentation prose names which subsystems gain agents at which level:

    Per-type subsystem agent contribution (ensemble):
      - Per-tree-sourced expensive items spawn within the relevant per-tree
        model subdirectory (depth-0 manager per tree re-spawns the relevant subtrees).
      - Cross-model-sourced expensive items spawn at the ensemble root (aggregator
        runs the expensive spawn after the adversarial cycle completes across all
        per-tree and root synthesis reports).
    [Locked: richness = {level}]
    [Locked: depth = {D}]

**Dim 13 layered audit at ensemble**: the reviewer audits each accepted enhancement against the **correct** report — per-tree-sourced enhancements audited against the per-tree report; cross-model-sourced enhancements audited against the cross-model synthesis report. A missing accepted enhancement in the wrong report is NOT a Dim 13 finding; it is only a finding when the targeting rule above says it should be in that specific report.

## Cross-Skill References

- `crux-skill-memory-meditation-report` — mandatory report contract for ensemble HTML+PDF generation and per-tree respawns
- `crux-skill-memory-meditation-coordination` — ensemble working-directory layout + per-tree `finalisation-enhancements.yml` filename row + root `finalisation-enhancements.yml` filename row
- `crux-skill-memory-meditation-research` — per-tree depth-0 manager writes `{model-subdir}/finalisation-enhancements.yml` before returning to aggregator; this skill reads those files in step 3b
- `crux-skill-memory-meditation-quick` — same per-tree write in Quick-mode ensemble trees
