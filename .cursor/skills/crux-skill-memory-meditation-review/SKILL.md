---
name: crux-skill-memory-meditation-review
description: Adversarial Review function for meditation: 13-dimension audit (incl. citation integrity, slop detection, anti-homogenisation drift, level-conditional Dim 9 peer-review thoroughness, Dim 12 Comprehensiveness fidelity, Dim 13 Init-suggestion AND finalisation-enhancement honour), severity classification, ≤3-iteration loop, MUST_FIX `needs_user_input` schema with mandatory `context` decision-guidance, and Dim 13 `respawn_required: true` Report-Skill Respawn Protocol payload schema (K9 + K10b). Use when the `crux-cursor-meditation-guide` agent is spawned in Adversarial Review function (step 10).
---

# CRUX Skill: Memory Meditation — Adversarial Review

Implements the mandatory Adversarial Review function: quality gate over all editable meditation outputs across 13 dimensions, severity classification, ≤3-iteration loop with `ESCALATE` semantics, Pattern-B escalation with mandatory `context` field, and the Report-Skill Respawn Protocol (K9 + K10b) for Dim 13 findings.

## When to Use

Load this skill when:
- The `crux-cursor-meditation-guide` agent is spawned in **Adversarial Review function** (a sub-mode of Meditate) at step 10 of the depth-0 manager workflow
- You are a fresh reviewer agent (new, clean context — no inherited assumptions from the depth-0 manager or any branch agent)
- `reviewerIteration ∈ {1, 2, 3}` is set in the spawn prompt

**Never load this skill** in Research mode, Quick mode, Ensemble Aggregation mode, or Report generation — those are owned by their respective skill files.

## Input Parameters (Adversarial Review invocation)

```yaml
meditateMode: "research" | "quick"   # mode of the meditation under review
reviewerIteration: 1 | 2 | 3         # 1-indexed, capped at 3
workingDir: "<absolute path to the meditation working directory>"
theming: { ... }                      # so the reviewer can flag homogenisation drift — REQUIRED
comprehensiveness: { ... }            # so the reviewer can check level-conditional minima — REQUIRED
modelStrategy: { ... }                # propagated unchanged by every spawn — REQUIRED (consistent with the propagation rule in the meditation-guide agent). The reviewer does not itself spawn model-specific children, but the payload is recorded in the review document for audit (e.g. "reviewer ran on caller's model because modelStrategy.mode == per_branch")
priorReviewPath: null | "<path>"      # path to previous iteration's review document
```

## Editable, Read-Only, and Never-Touched File Lists

The reviewer reads — but is the **only** agent permitted to **rewrite** during the cycle — the following files:

- **Editable (can rewrite)**: `facets.md`, `consolidation.md`, every `branch-*-depth-*-sub-*-*.md`, every `branch-*-peer-review-*.md`
- **Read-only (no rewrite)**: `facet-registry.yml`, `citations-index.yml` (Research mode only), `init-suggestions-{ts}.yml`, `finalisation-enhancements.yml`
- **Never touched by the reviewer**: `report-*.html`, `report-*.pdf`, `.facet-registry.lock/`, `facets-pending-*.yml`, `pending-facets-*.yml`, `confirmed-facets-*.yml`

## Review Dimensions (13 Total)

Audit every editable file across all 13 dimensions on every iteration. Findings are classified per dimension and severity.

**Dimension 1 — Citation integrity**: every claim in the body has at least one inline citation marker (`[memory: ...]`, `[file: ...]`, `[web: ...]`, `[chat: ...]`, `[child: ...]`); every marker resolves to an entry in the file's `## Citations` section; no unreferenced citation entries; `citations-index.yml` (Research mode) matches the union of per-file citations.

**Dimension 2 — Cross-file consistency**: no internal contradictions within a file; cross-file contradictions are surfaced in the file's `## Contradictions` section rather than hidden; `incorporated_children` in each parent's frontmatter matches the depth-1/2 children actually merged.

**Dimension 3 — Substance and sparseness**: no empty sections, no filler-only sections, no headings with one-line "(none discovered)" placeholders unless that genuinely reflects the research.

**Dimension 4 — Slop detection**: generic AI filler removed. Block-listed phrases include but are not limited to: "It's important to note that…", "In today's fast-paced world…", "Let's dive in", "stands as a testament to…", em-dash throat-clearing (e.g. " — let's explore…"), the "not just X but Y" tic, "delve into", "navigating the complexities of…".

**Dimension 5 — Calibration**: confidence in prose matches the strength of the evidence cited. Unqualified absolute claims ("always", "never", "the only way") must either be downgraded or supported by multi-source citations.

**Dimension 6 — Index integrity**: every link in `facets.md`'s Branch & Leaf Index resolves to an existing file; the "Missing slots" enumeration accurately reflects unproduced slots; the index metadata (timestamp, mode, count) matches reality.

**Dimension 7 — Frontmatter validity**: required YAML fields present on every branch / peer-review file; `subfocus_slug` and `timestamp_utc` match the on-disk filename; `incorporated_children` references resolve.

**Dimension 8 — Anti-homogenization drift in prose**: flag prose patterns that drift toward the homogenised AI default (purple-blue gradient metaphors, "synergy"-style buzzwords, marketing-deck cadence) regardless of which theming preset was chosen.

**Dimension 9 — Peer-review thoroughness** (Research mode only):

At `comprehensiveness.peer_review_surfacing ∈ {consolidation_only}` (`compact` and `default`): peer-review files must exist for each branch and must each contain at least one identified reinforcement, contradiction, and gap. Verify peer-review reach into the consolidation prose.

At `comprehensiveness.peer_review_surfacing ∈ {named_section}` (`detailed`): in addition to the above, verify that the report contains a dedicated named section (e.g. "Quality Review" or "Cross-Cutting Reinforcements & Contradictions") surfacing the peer-review findings cross-cutting all branches.

At `comprehensiveness.peer_review_surfacing ∈ {per_branch_dedicated}` (`exhaustive`): in addition to the above, verify ONE named section per branch surfacing that branch's peer-review reinforcements / contradictions / gaps.

Severity: `MUST_FIX` (in-place rewrite at all levels — does NOT trigger respawn even at `per_branch_dedicated`, because adding a named section is a presentation-layer fix). **N/A in Quick mode** (no peer-review files exist; the `named_section` / `per_branch_dedicated` placeholder is verified to be present, not flagged as missing).

**Dimension 10 — Ready-for-report**: downstream report generation will not have to invent content: every quantitative claim cited in `consolidation.md` resolves to a sourced data point in at least one branch file; every cross-branch theme is traceable to specific findings.

**Dimension 11 — Subject-matter focus**: `consolidation.md` must not contain process-oriented language per the **Subject-Matter Focus** rule: no "Branch 1/2/3" labels (use facet titles), no depth/leaf/agent references, no `[child: branch-N-depth-D-sub-S]` citations (must be `[research: {subfocus-slug}]`), no process-framing in the executive summary. Flag violations as `MUST_FIX` and rewrite the offending passages.

**Dimension 12 — Comprehensiveness fidelity**: The rendered report's chart count, infographic count, calculator count, depth-3 leaf inclusion behaviour, per-branch section depth, citation density, peer-review surfacing, section length budget, and ensemble cross-model depth must match the deterministic minima for the `comprehensiveness.level` declared in the report footer. Specifically:
- Chart count ≥ `comprehensiveness.minima.charts.count`.
- Infographic count ≥ `comprehensiveness.minima.infographics.count`.
- Calculator count ≥ `comprehensiveness.minima.calculators.count` (when topic surfaces a quantifiable trade-off).
- Per-branch section depth matches `comprehensiveness.per_branch_section_depth` (e.g. at `detailed`+ verify each confirmed facet has a dedicated per-branch section; at `compact`/`default` verify per-branch content folds into consolidation prose only).
- Peer-review surfacing matches `comprehensiveness.peer_review_surfacing` (e.g. at `detailed` verify a `named_section` exists for reinforcements/contradictions/gaps; at `per_branch_dedicated` verify one per branch).
- `depth3_leaf_inclusion` mode honoured (e.g. at `verbatim_quotes` verify ≥1 depth-3 leaf quote with citation appears per branch).

Severity: `MUST_FIX` (in-place rewrite — does NOT trigger respawn). The reviewer can add missing charts / infographics / sections inline by rewriting the report HTML — these are presentation-layer fixes that don't require regenerating the full report.

**Dimension 13 — Init-suggestion AND finalisation-enhancement honour**: Confirmed sections from `init-suggestions-{ts}.yml` (`confirmed_sections` block) MUST appear as report sections with substantive content; confirmed visualisations from `init-suggestions-{ts}.yml` (`confirmed_visualisations` block) MUST be rendered. Accepted finalisation enhancements from `finalisation-enhancements.yml` (`accepted: true, treatment: respawn`) MUST appear in the report per the K10b cheap-respawn flow.

Specifically:
- For each `confirmed_sections[i]`: a section with that exact title must exist in the rendered HTML, AND its body must be non-empty (>1 paragraph or >100 words; a heading-only stub counts as missing). Auto-resolved=true means an accepted finalisation enhancement (cheap, respawned) has overlapping title — flag the section as auto-resolved AND verify the enhancement-driven section appears.
- For each `confirmed_visualisations[i]`: a visualisation of that exact type must be rendered with non-empty data (a container with no data series counts as missing).
- For each `finalisation-enhancements.yml.candidates[i]` with `accepted: true, treatment: respawn`: a section / chart / infographic / etc. matching the type's rendering contract (see the **K10b Per-Cheap-Type Rendering Contract** in the `crux-skill-memory-meditation-report` skill) must appear in the report at its contractual location.

**Ensemble layered audit**: at ensemble, audit each accepted enhancement against the correct report — per-tree-sourced enhancements (from candidates with `source: "tree:{model-subdir}"`) are audited against the per-tree report; cross-model-sourced enhancements (from candidates with `source: "cross_model"`) are audited against the cross-model synthesis report. A missing accepted enhancement in the wrong report is NOT a finding; it is a finding only when the **K10 Ensemble Respawn Targeting** rule says it should be in that report (see the `crux-skill-memory-meditation-ensemble` skill).

Severity: `MUST_FIX` AND `respawn_required: true` — bypasses standard in-place fix flow per the **Report-Skill Respawn Protocol** below.

## Severity Classification

- **MUST_FIX** — blocks report generation. The reviewer applies the fix in the same iteration by rewriting the offending file, then continues sweeping the remaining files. If the fix is unambiguous (typo, missing citation marker that has an obvious target, a `## Citations` entry that needs to be added because the marker exists in body), the reviewer rewrites without asking. If the fix is ambiguous (e.g. multiple plausible citation targets for the same marker), the reviewer logs the finding with `fix_applied: false`, `reason: "ambiguous_fix"` and escalates via `needs_user_input` (Pattern B — see below).
- **SHOULD_FIX** — degrades quality but doesn't block report generation. Applied automatically when the fix is unambiguous; otherwise logged as `fix_applied: false`, `reason: "ambiguous_fix"` and surfaced in the review document for downstream attention.
- **ADVISORY** — observation only. Never auto-applied; never blocks; always logged.

## Quick Mode Relaxations

Quick mode applies two relaxations:
- Citation integrity findings of "missing inline marker" downgrade `MUST_FIX → SHOULD_FIX` (consistent with Quick mode's warn-only citation rule). Unresolvable markers that *do* exist in the body but cannot be traced to a citation entry remain `MUST_FIX`.
- Peer review thoroughness dimension is skipped entirely (no peer reviews exist in Quick mode).

All other dimensions (1–8, 10–13), the iteration cap, the `ESCALATE` semantics, the Pattern-B escalation contract (including the mandatory `context` decision-guidance), and the review document format are enforced identically in both modes.

## Iteration Loop (cap 3)

```
iteration = 1
while iteration <= 3:
    spawn reviewer with reviewerIteration=iteration (fresh subagent each iteration)
    reviewer writes review-pre-report-{ts}-iter-{iteration}.md
    if verdict in {PASS, PASS_WITH_ADVISORIES}: break
    if reviewer escalated MUST_FIX via needs_user_input (Pattern B):
        # Standard ambiguous-MUST_FIX path — Dim 13 respawn_required findings BYPASS this
        calling agent runs askQuestion with reviewer-supplied decision-guidance,
        then resumes the reviewer with the user's resolutions; reviewer applies
        those resolutions, finalises the iteration document, and the loop continues.
    if any finding has respawn_required: true (Dim 13 — init-suggestion / enhancement honour):
        # 1. Apply all Dim 1–11 in-place fixes first (reviewer already did these in same pass)
        # 2. Construct respawn payload (see Report-Skill Respawn Protocol below)
        # 3. Respawn the report-generation skill with fresh timestamp
        TS_new=$(date -u +%Y%m%d%H%M%S)
        # Prior HTML/PDF pair preserved on disk; respawn writes new pair at TS_new
        invoke report-generation skill with respawn_payload (iteration N consumed)
        # Next iteration (N+1) spawns a fresh reviewer to re-review the regenerated report
    iteration += 1

if iteration > 3 and MUST_FIX still unresolved:
    verdict = ESCALATE
    abort report generation
    surface unresolved findings to the calling agent instead of report paths
```

Cap is **3 iterations** (shared between standard review cycles and respawn cycles — no separate respawn budget). The depth-0 manager never spawns a 4th reviewer. Maximum useful respawns per meditation = 2 (respawn at end of iter 1 → reviewed at iter 2; respawn at end of iter 2 → reviewed at iter 3; iter 3 with Dim 13 still firing → `ESCALATE`).

## Reviewer Escalation — Pattern B with Mandatory Decision-Guidance

The reviewer **never calls `AskQuestion` directly** (subagents are forbidden from doing so by `AGENTS.md`). When an ambiguous `MUST_FIX` finding cannot be auto-applied, the reviewer returns a `needs_user_input` block to the depth-0 manager, which surfaces it to the calling agent. **Every escalated `needs_user_input` entry MUST include `context` text that explains the trade-off the user is choosing between** — never present bare options.

Minimum escalation schema:

    ## needs_user_input

    ### question_id: <reviewer-iter-N-finding-M>
    - **prompt**: <the question, citing the offending file and line>
    - **options**: [<option-a>, <option-b>, ...]
    - **default**: <suggested option, or none>
    - **context**: <REQUIRED — explains what each option means for the meditation,
       which fix the reviewer would apply for each, and which downstream artefacts
       are affected. Without this, the calling agent cannot relay decision-guidance
       to the user.>

**For `respawn_required: true` findings (Dim 13)**: the reviewer **never calls `AskQuestion`** for `respawn_required: true` findings — the respawn payload is structured and deterministic; no user input is needed. Standard ambiguous `MUST_FIX` findings (Dim 1–11) still follow the Pattern B escalation path with mandatory `context` field.

## Report-Skill Respawn Protocol (K9 + K10b)

When Dimension 13 fires with `respawn_required: true`, the standard in-place fix flow is bypassed. Instead:

### Respawn Payload Schema

The reviewer constructs this YAML payload and passes it to the report-generation skill respawn:

```yaml
respawn_reasons:           # list-typed — one respawn may carry multiple reasons
  - "missing_init_suggestion_sections"        # Dim 13 — confirmed_sections gap
  - "missing_init_suggestion_visualisations"  # Dim 13 — confirmed_visualisations gap
  - "accepted_finalisation_enhancements"      # K10b — cheap enhancements accepted
reviewer_iteration: 1 | 2 | 3
prior_report_paths:
  html: "report-{topic-slug}-{prior_ts}.html"
  pdf:  "report-{topic-slug}-{prior_ts}.pdf"
missing_sections:          # populated when respawn_reasons contains "missing_init_suggestion_sections"
  - title: "Adoption and Market Presence"
    rationale: "From init-suggestions; user confirmed this section"
    source_signals: ["[chat: turn-3]", "[memory: vendor-eval-patterns]"]
    branch_evidence_pointers:
      - "branch-1-depth-2-sub-1-{slug}-{ts}.md"
      - "branch-2-depth-3-sub-4-{slug}-{ts}.md"
missing_visualisations:    # populated when respawn_reasons contains "missing_init_suggestion_visualisations"
  - type: "magic_quadrant_2x2"
    rationale: "Topic explicitly compares 3 alternatives"
    source_signals: ["[file: src/router.ts:12-40]"]
accepted_finalisation_enhancements:    # populated when respawn_reasons contains "accepted_finalisation_enhancements"
  - id: "exec-summary-{ts}"            # one entry per accepted cheap enhancement
    type: "executive_summary"          # one of the 7 cheap K10a types
    title: "Executive Summary"
    description: "1-page exec summary aimed at C-level / time-poor readers"
    payload:                           # type-specific shape per K10b Per-Cheap-Type Rendering Contract
      target_persona: "leadership"
      max_paragraphs: 3
      anchor_findings:
        - "[research: auth-flow-trade-offs]"
    source_signals: ["[child: depth-3 leaf]", "[memory: ...]"]
preserve_other_content: true           # include prior report's confirmed sections verbatim in regenerated output
comprehensiveness_payload: { ... unchanged ... }
init_suggestions_payload: { ... unchanged, full ... }
theming_payload: { ... unchanged ... }
finalisation_enhancements_payload: { ... full file content if present, else null ... }
```

**Pattern B integrity**: the respawn payload is structured and deterministic; no user input is needed to execute it.

**K10b cheap-enhancement bundling**: multiple cheap items bundle into single respawn payload's `accepted_finalisation_enhancements:` list (one respawn, one iteration consumed). The `accepted_finalisation_enhancements` cause fires at most once per meditation.

### Same-Iteration Dim 1–11 Fix + Dim 13 Respawn Ordering

When iteration N's reviewer simultaneously fires Dim 1–11 findings AND Dim 13 with `respawn_required: true`:

1. **First**: apply Dim 1–11 in-place fixes (the reviewer rewrites branch / consolidation / peer-review files).
2. **Then**: respawn the report-generation skill; the respawn re-reads the now-fixed branch files and regenerates the report, cleanly incorporating the in-place fixes.

### Iteration Accounting

- Respawn shares the existing ≤3 adversarial review-and-fix iteration cap. A respawn is bundled into the iteration that flagged it — the iteration counter advances once per review-and-fix cycle regardless of whether a respawn fired.
- The **next** iteration's reviewer reviews the regenerated report (respawn-then-re-review).
- **Maximum useful respawns per meditation = 2**: iter 1 ends → respawn possible (reviewed at iter 2); iter 2 ends → respawn possible (reviewed at iter 3); iter 3 with Dim 13 still firing → `ESCALATE`.
- The `accepted_finalisation_enhancements` cause can fire **at most once** per meditation.

## Review Document Format

Filename: `review-pre-report-{yyyymmddHHMMSS}-iter-{N}.md` (one per iteration, written by the reviewer).

    ---
    mode: "research" | "quick"
    iteration: 1
    reviewed_at: "2026-05-16T12:34:56Z"
    reviewer_agent: "adversarial-review-iter-1"
    files_reviewed:
      - facets.md
      - consolidation.md
      - branch-1-depth-1-sub-0-{slug}-{ts}.md
      # ... every editable file in the working directory
    prior_review: "review-pre-report-{prev-ts}-iter-{N-1}.md"   # null on first iteration
    ---

    ## Verdict
    PASS | PASS_WITH_ADVISORIES | ESCALATE

    ## Summary
    {X MUST_FIX, Y SHOULD_FIX, Z ADVISORY findings; A applied, B escalated, C deferred}

    ## MUST_FIX findings
    1. **File**: branch-1-depth-2-sub-1-{slug}-{ts}.md
       **Location**: line 47, claim "...always faster"
       **Dimension**: Calibration
       **Issue**: Unqualified "always faster" with only one citation; evidence is anecdotal
       **Fix applied**: yes
       **Fix**: Replaced with "faster in {cited-conditions}"
       **Diff**:
       ```diff
       - X is always faster [memory: caching-patterns]
       + X is faster under high-read low-write workloads [memory: caching-patterns]
       ```
    2. ...

    ## SHOULD_FIX findings
    {same structure as MUST_FIX}

    ## ADVISORY findings
    {same structure; fix_applied is always false}

    ## Iteration log
    - Iteration 1 — found 7 MUST_FIX, applied 5, escalated 2 (citation-ambiguity)
    - Iteration 2 — user resolved 2 escalations; reviewer found 1 new MUST_FIX (cascade), applied 1
    - Iteration 3 — clean sweep, verdict PASS

    ## Carry-forward to next iteration
    {any SHOULD_FIX or ADVISORY items the reviewer wants surfaced after the cycle ends}

## Cross-Skill References

- `crux-skill-memory-meditation-report` — consumer of the respawn payload constructed by this skill; the resume-handler protocol and per-cheap-type processing order live there
- `crux-skill-memory-meditation-coordination` — review-iteration filename row (`review-pre-report-{ts}-iter-{N}.md`); Branch & Leaf Index links review iterations
- `crux-skill-memory-meditation-ensemble` — K10 Ensemble Respawn Targeting rule (per-tree vs cross-model targeting) used by Dim 13 ensemble layered audit
