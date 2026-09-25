# Spec Assessment: Context Token Reduction (Re-audit, 2026-09-06)

**Target**: `specs/20260713-context-token-reduction/spec-context-token-reduction-20260713.md`
**Assessed**: 2026-09-06 (fresh independent context)
**Assessor**: `zoto-spec-judge` (Mode 3 — spec quality / feasibility)
**Prior assessment**: [`assessment-context-token-reduction-20260713.md`](assessment-context-token-reduction-20260713.md) (Conditional → post-fix Approve ~4.2/5)
**Verdict**: **Approve — Ready for Review** (**4.35/5**)

## Framing

The invoking user described the spec as a **Draft** pending pre-execution judgement. On disk the spec is **post-execution**: the aggregator `status.yml` reports `aggregate_state: completed`, every subtask `.status.yml` carries `state: completed` with `extra.judge.verdict: verified`, the execution report is present, and the working tree holds substantial uncommitted WIP that materialises the spec's outputs (thin memory agents, `_memory-shared.md`, extracted templates, evals, upgrade script). This assessment therefore evaluates:

1. Spec quality and feasibility (the primary Mode 3 duty) — treating the spec markdown, subtask files, and dependency graph as the review subject.
2. Structural coherence of the spec directory itself (status pair drift, header consistency, execution-report accuracy).

It **does not** perform Mode 1 adversarial verification of deliverables. On-disk artifacts were spot-read only to confirm the six sanity anchors called out below.

## Six-anchor sanity read (spec-quality context, not execution verification)

| Anchor | Status |
|--------|--------|
| `_CRUX-RULE.mdc` retains `CRUX Decompression — CRITICAL`, `Path Construction`, `CRUX Compressed File Protection` primers (KD-11) | Present (L12, L15, L18) |
| `AGENTS.md` has `context_manifest` protocol content | Present (6 occurrences) |
| `.cursor/agents/crux-cursor-memory-manager.md` reduced to shim | 40 lines (≤60 target) |
| Thin memory agents exist under `.cursor/agents/crux-memory-*.md` | 5 files, 38–47 lines each |
| Canvas template at `.cursor/agents/templates/recall-canvas.tsx.md` | Present |
| `crux-memories-mcp-context.mdc` removed per S02 D03 | Deleted |

These confirm the spec's design intent survives to execution. They do not certify semantic parity — that's Mode 1's job.

## Scores (fresh independent read)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 4/5 | Options 1–8+10 covered; Opt 9 explicitly OOS; 9-subtask DAG; upgrade file, dist-gate protocol, evals, docs sync. KD-11 closes the earlier Opt1×Opt2 gap. Sole remaining gap: KD-2 was under-specified pre-execution (see Feasibility). |
| Feasibility | 3.5/5 | Delivered end-to-end (Wave 1+2 compressed, deferred waves documented). But KD-2 required **five** timeline revisions during execution (Approach c → `.crux.md` companions → `.mdx/.crux.md` → `.source.mdx/.md` skills + `.mdx/.crux.md` cmd/agent → authoritative `.source.mdx → .md`). Compression ratio for small thin agents ended at 48–55% (spec bar was ≤25%/≤30%). The initial spec did not model registration-frontmatter overhead. |
| Structure | 5/5 | DAG is coherent post-fix: Phase 1 (S01–S04, S06) parallel-disjoint, Phase 2 (S05), Phase 3 (S07), Phase 4 (S08), Phase 5 (S09). Mermaid classDef managed block present. No same-phase dependencies, no back-references. |
| Specificity | 4.5/5 | Concrete paths, token targets, DoDs, `SOURCE_DIST_FILES` diffs, dist-flag protocol. S07 wave ordering is explicit. Minor: S09 upgrade steps mix consumer `.cursor/agents/crux/` and repo `.cursor/agents/` paths (documented, but easy to trip on). |
| Risk Awareness | 4/5 | KD-1..KD-11 KD table covers BC, zip protection, shim scope, compress-last, decompression primer retention. Missing pre-execution: the KD-2 registration_model risk (the pre-execution spec pinned Approach c, but execution proved cursor registration mechanics forced a `.source.mdx → .md` split for cmd/agent primitives). |
| Convention Compliance | 5/5 | CRUX agents (not `generalPurpose`); zip-protection respected; upgrade file per hygiene Rule 3; deprecation notice without spec ids (post-fix); eval file named `test_r_crux_command_suite.py` (post-fix). |
| **Overall** | **4.35/5** | **Approve — Ready for Review** |

Weighted: `4·0.25 + 3.5·0.20 + 5·0.20 + 4.5·0.15 + 4·0.10 + 5·0.10 = 4.35`.

## Findings

### Strengths

- **Grounded audit-first design.** Every subtask ties back to a specific option or redundancy in `analysis/context-token-reduction-report.md`. OOS boundaries (Option 9) are explicit.
- **Compress-last ordering (KD-10)** correctly places prose/extraction/split subtasks before CRUX compression so the leanest source is compressed once.
- **KD-11 hard constraint** is load-bearing — `_CRUX-RULE.mdc` retains the CRUX Decompression primer, which makes CRUX-bodied agent files decompressable at runtime by non-CRUX agents.
- **Consumer-safe by construction.** `scripts/create-crux-zip.py` is untouched; every new dist file is aggregated for explicit user approval; the umbrella dispatcher shim (`crux-cursor-memory-manager.md` at 40 lines) protects pre-upgrade consumer installs.
- **Convention compliance is high.** CRUX agents throughout, no `generalPurpose`, no spec-id leaks in production code (per hygiene Rule 1), upgrade script per hygiene Rule 3, eval file follows `test_a_..test_r_` alphabetical convention.
- **Judge trail is exemplary.** Every `.status.yml` carries an `extra.judge` block with `verdict`, `at`, `notes`, and (importantly) an empty `fix_list` — the Mode 1 verification tour is durable.

### Issues (spec-quality only)

| # | Severity | Subtask / Path | Finding | Recommendation |
|---|----------|----------------|---------|----------------|
| 1 | HIGH | `subtask-05..09-*.md` bodies | **Subtask spec markdown drift.** For S05, S06, S07, S08, S09 the subtask spec files still show all deliverables as `- [ ]` unchecked and Execution Notes as `_To be filled by executing agent._` — yet the paired `.status.yml` files claim `state: completed` with all checklist items `done: true` and `extra.judge.verdict: verified`. A future reader loading only the subtask markdown would incorrectly conclude the work never started. `spec-onstop-check` does not catch this because it only reconciles the `.status.md` ↔ `.status.yml` pair inside `status/`. | Backfill each subtask markdown's Deliverables Checklist ticks and Execution Notes (Agent Session Info, Work Log, Files Modified) from the corresponding `.status.yml` `notes` and `artifacts`, so the two authoritative records agree. Either the executor or a small round-trip helper should keep them in lockstep at completion. |
| 2 | HIGH | Spec index `## Status` header | **Header/manifest inconsistency.** The `## Status` line reads `Ready for Review` while the Subtask Manifest reports every subtask as `Done` and the trailing Execution Notes states `Execution complete (pending user approval)`. The three signals disagree about lifecycle stage. | Pick one canonical convention (`Draft`, `Ready for Review`, `Executing`, `Complete`). Given the DoD box is fully ticked and the execution report exists, `Ready for Review` is the correct value **for user sign-off on dist-manifest additions**. Add a one-line note under `## Status` naming the specific outstanding gate (dist manifest additions, commit, version bump). |
| 3 | MEDIUM | Index KD-2 timeline | **KD-2 was under-specified pre-execution.** The spec locked in Approach (c) (in-place CRUX in `.md` bodies on registering paths) but execution required three user overrides plus an authoritative "registration_model" answer before landing on `<name>.source.mdx` (SoT) → `<name>.md` (loadable, CRUX body) for commands/agents and `SKILL.mdx` → `SKILL.md` for skills. The KD-2 body now carries a five-entry timeline that documents the pivots retrospectively rather than the original decision. | Not actionable for the shipped spec, but log the lesson: the next context-reduction (or CRUX-compression) spec must survey Cursor's actual registration semantics **before** committing to a single approach in KD-2, and must model the frontmatter/registration overhead that prevents small primitives from reaching ≤25%. |
| 4 | MEDIUM | S07 DoD02 | **Thin-agent ratio deviation is post-hoc.** DoD02 required body ≤25% of source (or ≤30% with documented rationale). Wave 2 thin agents landed at 48–55% and were accepted via the "documented rationale" escape hatch after the fact. This changes DoD semantics mid-execution. | Retrospectively edit S07 DoD02 to acknowledge that small primitives with heavy registration frontmatter have a natural floor around ~50% and carve that out as a first-class allowance, not as an emergency clause. Or, if leaving the shipped spec as-is is preferred, add a short paragraph in the execution report explaining why 48–55% is the correct target for thin agents. |
| 5 | MEDIUM | `execution-report-context-token-reduction-20260713.md` | **Execution report cites the pre-rename eval filename.** The report body under "What shipped" for S06 lists `evals/test_p_crux_test.py`, but the actual file on disk is `evals/test_r_crux_command_suite.py` (prior-assessment fix #5 renamed it for the `test_r_` alphabetical slot). | Update the execution report line to reference `evals/test_r_crux_command_suite.py`. Same file is correctly referenced in S06/S08 deliverables — only the exec-report summary drifted. |
| 6 | LOW | S06 subtask markdown | **S06 spec markdown does not name `evals/test_r_crux_command_suite.py`.** The body correctly names `test_r_crux_command_suite.py` (post-fix) but the checklist still shows `- [ ]`, so a reader can't confirm from the checklist whether the rename landed. This is the same drift as Issue 1 for S06 specifically. | Covered by Issue 1's fix. |
| 7 | LOW | S09 upgrade steps | **Consumer vs repo path phrasing.** S09 D01 correctly documents that the upgrade script must detect both `.cursor/agents/crux/` (consumer, post-install) and `.cursor/agents/` (repo/dist) layouts, but the surrounding prose in the Consumer Upgrade Steps (S05) uses only the consumer form. Not incorrect, but easy to miss when adapting for a repo-layout test. | Add one line to the S05 Consumer Upgrade Steps preamble: "In consumer installs `install.py` places primitives under `.cursor/agents/crux/`; in the source repo they live under `.cursor/agents/` — the script detects both." |
| 8 | LOW | Repository state | **All spec deliverables are uncommitted.** 40+ files (thin agents, source files, templates, evals, docs edits, upgrade script) sit as `M`/`??` in the working tree. Not a spec-quality issue per se, but a delivery-readiness concern the reviewing user should acknowledge before promoting Status to `Complete`. | Commit in logical groups (per subtask or per phase), attach the version-bump note per `version-bump.crux.mdc` on the merge commit, and only then flip Status. |

### Dependency Graph

Edges match the manifest. Phase assignments respect `phase > max(dep phases)`. No back-references. Aggregator has injected the `%% spec-system:classes:begin/end %%` block and coloured every node `specDone` (matches the completed state).

| Check | Result |
|-------|--------|
| Files exist for all manifest rows | Pass (01–09) |
| Metadata deps match manifest | Pass |
| No dependency on higher ID | Pass |
| Phase > all dependency phases | Pass |
| Parallelism claims sound | Pass — Phase 1 five-way is file-disjoint |
| Missing edges | None material |
| Unnecessary edges | None material after prior-assessment fix (S07→S06 removed) |
| Class-def block present | Pass (aggregator-managed) |

### Subtask Quality Snapshot

| ID | Objective | Deliverables | Agent | Notes |
|----|-----------|--------------|-------|-------|
| 01 | Strong | Strong | `crux-platform-architect` | Markdown filled; work log detailed |
| 02 | Strong | Strong | `crux-cursor-rule-manager` | Markdown filled; work log detailed |
| 03 | Strong | Strong | `crux-platform-architect` | Markdown filled; work log detailed |
| 04 | Strong | Strong | `crux-platform-architect` | Markdown filled; DoD02 explicitly `[ ]` with partial explanation — acceptable |
| 05 | Strong | Strong | `crux-platform-architect` | **Markdown checklist unchecked; work log placeholder** (Issue 1) |
| 06 | Strong | Strong | `crux-software-engineer` | **Markdown checklist unchecked; work log placeholder** (Issue 1) |
| 07 | Strong | Strong (large) | `crux-cursor-rule-manager` | **Markdown checklist unchecked; work log placeholder** (Issue 1). Thin-agent ratio deviation (Issue 4) |
| 08 | Strong | Strong | `crux-software-engineer` | **Markdown checklist unchecked; work log placeholder** (Issue 1) |
| 09 | Strong | Strong | `crux-software-engineer` | **Markdown checklist unchecked; work log placeholder** (Issue 1). Upgrade path phrasing (Issue 7) |

### Risk Summary

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Subtask markdown drift misleads future readers | Certain (already true) | Med | Issue 1 — backfill from `.status.yml` |
| Status header vs manifest disagreement confuses reviewer | High | Low | Issue 2 — canonicalise Status value |
| Next CRUX-compression spec repeats KD-2 pivots | Med | Med | Issue 3 — capture lesson in a memory or next spec's KD table |
| Post-hoc DoD relaxation normalises escape hatches | Med | Med | Issue 4 — either encode the small-primitive floor or add exec-report caveat |
| Dist zip missing thin agents / templates | High (by design) | Med | Already mitigated — umbrella shim + S09 approval section + upgrade script |
| Uncommitted WIP is lost or conflicts with `origin/main` merge | Med | High | Issue 8 — commit per subtask / phase before promoting Status |

## Comparison with Prior Assessment (2026-07-13)

The [prior assessment](assessment-context-token-reduction-20260713.md) applied nine HIGH/MEDIUM spec-content fixes (phase separation, S01/S05 ownership, KD-11, deprecation-notice hygiene, eval renaming, S09 agent assignment, `--repair` removal, S07 test cadence, S08 aspirational gate). Each was applied and each remains applied in the current spec. This re-assessment finds:

- All prior HIGH findings have been addressed in the spec markdown and reflected in execution.
- New HIGH findings surface at a different layer — **spec/status coherence** rather than spec content — because the executor ran ahead of the subtask-markdown reconciliation step. `.status.yml` is authoritative and correct; the subtask markdown was not backfilled.
- Two prior LOW items (mermaid classDef placeholder, skill path-pointer wording) are effectively resolved: the mermaid `classDef` block is now aggregator-managed and present; the `_memory-shared.md` path-pointer usage is scoped to shared reference doc pattern (borderline acceptable per `skill-and-agent-references.mdc` "path-as-subject" exception).

## Recommendation

**Verdict**: Approve — **Ready for Review** (~4.35/5).

**Next actions the user should take** (in order):

1. Decide whether to accept the two HIGH spec-quality fixes (Issue 1: backfill subtask markdown; Issue 2: canonicalise `## Status` value) — these are spec-file edits only, no application source. See the `needs_user_input` block in the host response.
2. Optionally accept the three MEDIUM fixes (Issue 3 lesson-capture; Issue 4 S07 DoD02 wording; Issue 5 exec-report eval filename).
3. LOW fixes (7, 8) are informational.
4. Commit the WIP in logical groups, then flip Status to `Complete` after dist-manifest additions have been reviewed and applied by the release engineer.

The spec **is** ready for user review as-is; the fixes above tighten the spec-directory record rather than blocking execution. The prior assessment's post-fix estimate of ~4.2/5 was accurate; this fresh audit lands at ~4.35/5 with the Structure and Convention Compliance scores promoted after independent re-check.
