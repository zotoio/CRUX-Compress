# Subtask: Adversarial Review Cycle + Branch & Leaf Index in facets.md

## Metadata
- **Subtask ID**: 04
- **Feature**: Meditate Research-Mode Overhaul
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 03
- **Created**: 20260516

## Objective

Add two related quality gates that run after consolidation but before reports are generated:

1. **Branch & Leaf Index in `facets.md`** — post-consolidation, the depth-0 manager updates `facets.md` to append a comprehensive index linking every artefact the meditation produced via relative markdown links. `facets.md` becomes the single navigational entry point.
2. **Adversarial Review and Fix Cycle** — a fresh `crux-cursor-memory-manager` subagent in Adversarial Review function audits all output files across 10 dimensions, classifies findings as MUST_FIX/SHOULD_FIX/ADVISORY, applies unambiguous fixes by rewriting offending files, and iterates up to 3 times. Reports are never built over a failing review.

## Files Modified

- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`

## Deliverables Checklist

- [x] **Branch & Leaf Index** section in the command file with full format spec (per-branch sections with depth-1/2/3 sub-lists, per-branch peer-review line, top-level artifacts, missing-slots enumeration, index metadata)
- [x] **Adversarial Review and Fix Cycle** section in the command file with reviewer-agent spec, review dimensions (10), severity classification (MUST_FIX/SHOULD_FIX/ADVISORY), fix policy, iteration loop (cap 3), review document format, Quick mode treatment
- [x] Subagent **step 4** (write initial facets.md) updated to note that `facets.md` will be updated again post-consolidation with the Branch & Leaf Index
- [x] Subagent **step 8** (consolidation) extended with sub-step 5 (update facets.md with Branch & Leaf Index), sub-step 6 (adversarial review and fix cycle), sub-step 7 (re-run sub-step 5 to refresh links post-review), and the existing report-generation sub-step renumbered to 8
- [x] Quick mode workflow notes updated: step 9 (Branch & Leaf Index) and step 10 (adversarial review) are NOT skipped, with documented relaxations (no peer-review lines in index, missing-citation findings downgraded MUST_FIX → SHOULD_FIX in review)
- [x] Two new design principles in the agent file: mandatory adversarial review-and-fix cycle, `facets.md` as navigational entry point

## Definition of Done

- [x] `facets.md` ends every meditation containing a complete Branch & Leaf Index linking every artefact via relative paths
- [x] No report HTML / PDF is generated unless the adversarial review verdict is `PASS` or `PASS_WITH_ADVISORIES`
- [x] `ESCALATE` verdict aborts report generation and surfaces unresolved findings to the calling agent
- [x] Linter passes on both files

## Implementation Notes

### Branch & Leaf Index section (command file, place between Quick Mode and Report Generation)

```markdown
### Branch & Leaf Index (appended to `facets.md`)

After consolidation completes, the depth-0 manager **must update `facets.md`** by appending a Branch & Leaf Index section that links to every file the meditation produced. This makes `facets.md` the single navigational entry point — open it once, jump from there to any branch, sub-focus, peer review, or top-level artifact.

**Construction rule**: glob the working directory for actual filenames (`branch-*-depth-*-sub-*-*.md`, `branch-*-peer-review-*.md`) rather than reconstructing names from memory. Use **relative paths** (no `./` prefix needed) so links resolve when `facets.md` is opened from any tool that respects relative markdown links.

**Required structure**:

    ---
    (existing facets.md frontmatter / content above this line is unchanged)
    ---

    ## Branch & Leaf Index

    ### Branch 1 — {branch-1 facet title}
    **Subfocus**: {one-line facet description}

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

    ### Index metadata
    - **Generated**: {ISO 8601 timestamp of index update}
    - **Mode**: `research` | `quick`
    - **Total files indexed**: {count}
    - **Missing slots**: {list any branch/depth/sub combinations that did not produce a file, or "none"}

> When constructing the index, resolve `{topic-slug}` from the working-directory name and resolve `{ts}` placeholders by globbing for actual on-disk files: the **latest** matching `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf` pair, **every** `review-pre-report-*-iter-*.md` (sorted by iteration number ascending), and **every** `confirmed-facets-*.yml` (sorted by path-id then `{ts}`). List all of them as their actual on-disk filenames; never write literal `{topic-slug}-{ts}` placeholder text into `facets.md`. Pending facet files (`facets-pending-*.yml` and `pending-facets-*.yml`) are coordination artifacts — they are **not** linked from the index; only the corresponding confirmed counterparts are linked.

**Conventions**:
- Display label of each link is the file's `subfocus_slug` from frontmatter, prefixed with the local sub-index.
- Group depth-3 leaves under their depth-2 parent. Sibling indices 1–3 belong to D2-sub-1, 4–6 to D2-sub-2, 7–9 to D2-sub-3.
- If a slot didn't produce a file, omit the link AND list the slot under "Missing slots" so the gap is explicit.
- The "Top-level artifacts" subsection always lists `consolidation.md` plus the latest report HTML/PDF pair, every review iteration discovered, and every confirmed-facets pair discovered. Registry/citations-index lines appear only in Research mode.
- Quick mode produces the same index minus per-branch "Peer review" lines and the two Research-only registry/index lines.
```

### Adversarial Review and Fix Cycle section (command file, place between Branch & Leaf Index and Report Generation)

```markdown
### Adversarial Review and Fix Cycle — MANDATORY

Before any report is generated, the depth-0 manager **must** run an adversarial review-and-fix cycle over every output file the meditation produced. This is a non-negotiable quality gate.

#### Reviewer agent

Spawn a fresh `crux-cursor-memory-manager` subagent in **Adversarial Review** function (a sub-mode of Meditate). It runs in its own clean context. Pass it:

- `meditateMode`: `"research"` or `"quick"` (the mode of the meditation under review)
- `reviewerIteration`: `1`, `2`, or `3` (1-indexed, capped at 3)
- `workingDir`: absolute path to the meditation working directory
- `theming`: the resolved Theme Preflight payload
- `priorReviewPath`: path to the previous iteration's review document, if any

The reviewer reads — but is the only agent permitted to **rewrite** — the following files:
- `facets.md`, `consolidation.md`, every `branch-*-depth-*-sub-*-*.md`, every `branch-*-peer-review-*.md`
- Read-only: `facet-registry.yml`, `citations-index.yml`
- Never touches: `report-*.html`, `report-*.pdf`, `.facet-registry.lock/`

#### Review dimensions

1. **Citation integrity** — every claim has at least one inline citation marker; every marker resolves to an entry in the file's `## Citations` section; no unreferenced entries.
2. **Cross-file consistency** — no internal contradictions; cross-file contradictions surfaced in `## Contradictions`; `incorporated_children` matches reality.
3. **Substance and sparseness** — no empty / filler-only sections.
4. **Slop detection** — generic AI filler removed: "It's important to note that…", "In today's fast-paced world…", "Let's dive in", "stands as a testament to…", em-dash throat-clearing, the "not just X but Y" tic, etc.
5. **Calibration** — confidence matches evidence.
6. **Index integrity** — every link in `facets.md` resolves; "Missing slots" accurate.
7. **Frontmatter validity** — required fields present; slug/timestamp filename match.
8. **Anti-homogenization drift in prose** — generic AI patterns flagged.
9. **Peer review thoroughness** (Research only) — concrete cross-references.
10. **Ready-for-report** — downstream report won't have to invent content.

#### Severity classification

- **MUST_FIX** — blocks report generation. Reviewer applies the fix in the same iteration.
- **SHOULD_FIX** — degrades quality but doesn't block. Applied if unambiguous; otherwise logged with `reason: "ambiguous_fix"`.
- **ADVISORY** — observation only. Never auto-applied.
- **Ambiguous MUST_FIX** items are escalated via the reviewer's `needs_user_input` (Pattern B). The cycle pauses until the user resolves them, then resumes with iteration N+1.

#### Iteration loop

    iteration = 1
    while iteration <= 3:
        spawn reviewer with reviewerIteration=iteration
        reviewer writes review-pre-report-{ts}-iter-{iteration}.md
        if verdict in {PASS, PASS_WITH_ADVISORIES}: break
        if reviewer escalated MUST_FIX via needs_user_input:
            bubble up → user resolves → continue
        iteration += 1

    if iteration > 3 and MUST_FIX still unresolved:
        abort report generation, verdict = ESCALATE
        surface unresolved findings to calling agent

Cap is 3 iterations. Reports are never built over a failing review.

#### Review document format

Filename: `review-pre-report-{yyyymmddHHMMSS}-iter-{N}.md`

    ---
    mode: "research" | "quick"
    iteration: 1
    reviewed_at: "2026-05-16T12:34:56Z"
    reviewer_agent: "adversarial-review-iter-1"
    files_reviewed:
      - facets.md
      - consolidation.md
      - branch-1-depth-1-sub-0-{slug}-{ts}.md
      # ...
    prior_review: "review-pre-report-{prev-ts}-iter-0.md"   # null on first iteration
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
    {same structure}

    ## ADVISORY findings
    {same structure; fix_applied always false}

    ## Iteration log
    - Iteration 1 — found 7 MUST_FIX, applied 5, escalated 2 (citation-ambiguity)
    - Iteration 2 — user resolved 2 escalations; reviewer found 1 new MUST_FIX (cascade), applied 1
    - Iteration 3 — clean sweep, verdict PASS

    ## Carry-forward to next iteration
    {any SHOULD_FIX or ADVISORY items recommended for surfacing post-meditation}

#### Quick mode

Quick mode runs the **same review cycle with the same iteration cap and severity classification**, with two relaxations:
- Citation integrity — flagged as SHOULD_FIX rather than MUST_FIX when a citation marker is missing (consistent with Quick mode's warn-only citation rule). Unresolvable markers that *do* exist remain MUST_FIX.
- Peer review thoroughness — N/A (no peer reviews exist in Quick mode).

All other dimensions are enforced identically.
```

### Subagent step 4 update (agent file)

In step 4 of the depth-0 workflow, after writing the final `facets.md`, add a note:

```
Note: `facets.md` will be **updated again** in step 9 (post-consolidation) to append a Branch & Leaf Index linking to every file the meditation produces.
```

### Subagent steps 8 + 9 + 10 + 11 + 12 + 13 (agent file — extending step 8 from subtask 02 into multiple top-level steps)

In subtask 02 the agent file had steps 1–8. This subtask extends that to steps 1–13 by inserting four new steps after consolidation:

```
8. Consolidate → write consolidation.md (unchanged from subtask 02)

9. Update `facets.md` with the Branch & Leaf Index
   (glob working directory for actual filenames, append index per the command's spec)

10. Adversarial review and fix cycle
    (spawn fresh subagent in Adversarial Review function, loop up to 3 iterations,
     verdict must be PASS or PASS_WITH_ADVISORIES, ESCALATE aborts reports)

11. Re-run step 9
    (review may have rewritten files; refresh Branch & Leaf Index links)

12. Generate the mandatory report (HTML + PDF)
    (subtask 05 will fully document this — for now, just the placeholder step)

13. Return to calling agent
    (consolidation text + workingDir + facets.md path + report paths +
     review-pre-report-*-iter-*.md paths)
```

### Calling-agent steps 9–12 in command file (subagent block step 8 has sub-steps 1–9)

The command file's `Steps 1–8 subagent block` ends with step 8 having sub-steps:

```
8. Branch peer review, consolidation, index, review, and report (back at depth 0):
   1. Wait for branch-{1,2,3}-depth-1-sub-0-*.md via glob
   2. Spawn 3 peer-review agents in parallel
   3. Wait for branch-{1,2,3}-peer-review-*.md via glob
   4. Consolidate → write consolidation.md
   5. Update facets.md with the Branch & Leaf Index
   6. Adversarial review and fix cycle
   7. Re-run sub-step 5 (refresh index post-review)
   8. Generate the mandatory report artifacts
   9. Return paths (facets.md, consolidation.md, report HTML+PDF pair, review iterations)
```

Calling-agent block (steps 9–12) gains an explicit verification step for reports — see subtask 05.

### Quick mode workflow notes update (agent file)

Update Quick mode's "Step 9" and "Step 10" lines:

```
- **Step 9 (Branch & Leaf Index update) is NOT skipped** — append the index per the same format used in Research mode, with these omissions: no per-branch "Peer review" lines, no `facet-registry.yml` or `citations-index.yml` lines under "Top-level artifacts".
- **Step 10 (adversarial review and fix cycle) is NOT skipped** — Quick mode runs the same review cycle with the same iteration cap and severity classification, with two relaxations: (a) missing-citation findings downgraded MUST_FIX → SHOULD_FIX; (b) "peer review thoroughness" dimension is N/A. Reports are not built until verdict is PASS / PASS_WITH_ADVISORIES; ESCALATE aborts as in Research mode.
- **Step 11 (re-run Branch & Leaf Index) is NOT skipped** — refresh after review.
- Step 13: return paths including review iterations.
```

### Two new design principles (agent file)

Append to the design-principles list:

```markdown
- **Mandatory adversarial review-and-fix cycle before any report (both modes)**: After consolidation and after the Branch & Leaf Index update, the depth-0 manager spawns a fresh `crux-cursor-memory-manager` subagent in **Adversarial Review** function with a clean context. The reviewer audits every output file across 10 dimensions, classifies findings as `MUST_FIX` / `SHOULD_FIX` / `ADVISORY`, applies unambiguous fixes by rewriting offending files, and writes `review-pre-report-{ts}-iter-{N}.md`. Loops up to 3 iterations until verdict is `PASS` / `PASS_WITH_ADVISORIES`; an `ESCALATE` outcome aborts report generation. Reports are never built over a failing adversarial review.
- **`facets.md` is the navigational entry point (both modes)**: Post-consolidation, the depth-0 manager appends a Branch & Leaf Index to `facets.md` with relative markdown links to every branch, depth-2 sub, depth-3 leaf, peer-review (Research mode), and top-level artifact (`consolidation.md`, the latest `report-{topic-slug}-{ts}.html` / `.pdf` pair, every `review-pre-report-*-iter-*.md` discovered, every `confirmed-facets-*.yml` when `confirmDeepFacets ≠ none`, plus `facet-registry.yml` and `citations-index.yml` in Research mode). The index is built by globbing the working directory for actual filenames so missing slots are visible by absence.
```

## Testing Strategy

- After applying, simulate a meditation completion: confirm sub-step 5 writes the index, sub-step 6 spawns review, sub-step 7 re-writes index post-review, sub-step 8 generates reports, sub-step 9 returns.
- Confirm an `ESCALATE` verdict from review skips sub-step 8 and surfaces unresolved findings.
- Spot-check the Branch & Leaf Index format examples are well-formed markdown.
- Run the linter on both files.

## Execution Notes

### Agent Session Info
- Agent: crux-platform-architect
- Started: 20260516
- Completed: 20260516

### Work Log
- Added the **Branch & Leaf Index** section to `.cursor/commands/crux-meditate.md` between the calling-agent block (steps 9–12) and the Report Generation section, with the full per-branch / depth-2 / depth-3 / peer-review / top-level-artifact structure, the missing-slots enumeration rule, the index-metadata block, and the convention that pending coordination files are never linked (only their confirmed counterparts).
- Added the **Adversarial Review and Fix Cycle — MANDATORY** section immediately below the Branch & Leaf Index. Spec covers: reviewer-agent spawn (`crux-cursor-memory-manager` in Adversarial Review function, fresh context, 1-indexed `reviewerIteration` capped at 3); editable / read-only / never-touched file lists; all 10 review dimensions (citation integrity, cross-file consistency, substance, slop detection, calibration, index integrity, frontmatter validity, anti-homogenization drift, peer review thoroughness, ready-for-report); severity classification (`MUST_FIX` / `SHOULD_FIX` / `ADVISORY`) with the fix-application policy; iteration loop with the `ESCALATE` exit; Pattern-B `needs_user_input` contract with **mandatory `context` decision-guidance** so the calling agent can relay trade-offs to the user via `askQuestion`; review document format; Quick-mode relaxations (citation-marker downgrade, peer-review N/A).
- Restructured Research-mode subagent step 8 into sub-steps **8.1–8.9** (recap of polls/peer-review, consolidate, update facets.md with index, adversarial review, re-run index, mandatory report placeholder, return paths). Restructured Quick-mode step 8 identically with sub-steps 8.2/8.3 marked N/A and the documented relaxations.
- Updated the Modes table preamble in `.cursor/commands/crux-meditate.md` to reflect that the Branch & Leaf Index update and the adversarial review-and-fix cycle are now shared safeguards (subtask 04), while mandatory report generation remains owned by subtask 05.
- Updated agent file `.cursor/agents/crux-cursor-memory-manager.md` workflow step 4 with the explicit note that `facets.md` is updated again in step 9 (post-consolidation) with the Branch & Leaf Index.
- Extended the Research-mode workflow in the agent file from steps 1–8 to **steps 1–13**: step 8 still writes `consolidation.md` but no longer returns; step 9 appends the Branch & Leaf Index; step 10 runs the mandatory adversarial review-and-fix cycle with the `ESCALATE` semantics that abort steps 11 and 12; step 11 re-runs step 9 to refresh the index after reviewer rewrites; step 12 is the mandatory-report placeholder (full contract owned by subtask 05); step 13 returns paths (and on `ESCALATE` returns everything except report paths plus a structured summary of unresolved `MUST_FIX` findings).
- Updated the **Step-numbering note** in the agent file to record subtask 04's extension from steps 1–8 to steps 1–13 and clarified subtask 05's calling-agent verification-gate responsibility.
- Updated the **Quick mode top-level workflow** header from "Research steps 1–8" to "Research steps 1–13" and added new bullets for steps 9, 10, 11, 12, 13 that document the Quick-mode relaxations (omit peer-review lines + registry/index entries in the index; downgrade missing-citation findings to `SHOULD_FIX`; skip peer review thoroughness review dimension) while still gating reports on `PASS` / `PASS_WITH_ADVISORIES` and aborting on `ESCALATE`.
- Appended two new design principles to the agent file's design-principles list: **mandatory adversarial review-and-fix cycle before any report (both modes)** and **`facets.md` is the navigational entry point (both modes)**. Both principles explicitly reference subagent step numbers, both modes' behaviour, the 10 review dimensions, the `ESCALATE` consequences, the Pattern-B `context`-guidance contract, and the Quick-mode relaxations.

### Blockers Encountered
None. Subtasks 01–03 already provided the canonical Coordination Conventions, Pattern-A/B contracts, and Facet Confirmation flow, so the new sections reference rather than redefine those primitives.

### Files Modified
- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`
