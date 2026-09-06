# Spec Assessment: Context Token Reduction

**Target**: `specs/20260713-context-token-reduction/spec-context-token-reduction-20260713.md`
**Assessed**: 2026-07-13
**Verdict**: Conditional → **post-fix estimate: Approve (~4.2/5)**
**Execution state note**: `status/` exists with all nine subtasks `state: pending` — no execution progress. This assessment is **spec quality only** (not adversarial execution verification).

## Fixes Applied (2026-07-13)

User approved `yes_all`. The following assessment recommendations were applied to **spec index + subtask markdown only** (no application source):

| # | Severity | Fix applied |
|---|----------|-------------|
| 1 | HIGH | S09 → Phase 5; Execution Order split Phase 4 (S08) / Phase 5 (S09); mermaid dropped `S06 → S07` |
| 2 | HIGH | S01: memory-manager removed from D04/D06; AGENTS preamble + rule #1 retargeted; D03 softened for integrity/docs-sync |
| 3 | HIGH | Index **KD-11** added; S02 retains Decompression — CRITICAL; S07 bootstrap + DoD10 |
| 4 | HIGH | S05 deprecation HTML comment rewritten without spec ids; KD-3 / AGENTS annotation aligned |
| 5 | MEDIUM | S06 eval renamed to `evals/test_r_crux_command_suite.py` throughout |
| 6 | MEDIUM | S04: six commands; overlap-with-S05 ownership notes clarified |
| 7 | MEDIUM | S09 assigned to `crux-software-engineer`; index path + no `--repair`; docs still per docs-sync protocol |
| 8 | MEDIUM | S07: drop S06 hard dep; DoD08 aligned with wave-level Testing Strategy |
| 9 | MEDIUM | S08 DoD04: ≥30% aspirational, not hard gate |

LOW items (mermaid classDef placeholders; skill path-pointer wording) were **not** in the approved HIGH/MEDIUM set and were left unchanged.

## Scores (pre-fix assessment)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 4/5 | Options 1–8 + 10 covered; Opt 9 explicitly OOS; upgrade + dist-gate + evals + docs present. Gaps on Opt1↔Opt2 interaction and a few ownership conflicts. |
| Feasibility | 3/5 | Mostly prose-feasible; S07 (32-file wave) is large but deferrable. Lazy-CRUX + in-body CRUX compression creates a real chicken-and-egg risk. |
| Structure | 3/5 | DAG is mostly sound; Phase 4 claims S08∥S09 despite S09→S08; S01 internal D04 vs notes conflict; mild over-serialization S06→S07. |
| Specificity | 4/5 | Concrete paths, schemas, token targets, DoDs, and dist-flag protocol. Minor naming/path inaccuracies. |
| Risk Awareness | 4/5 | Strong KD table (BC, zip protection, shim scope, compress-last). Under-specifies decompression-primer retention after S02 slimming. |
| Convention Compliance | 3/5 | Correct CRUX agents; zip-protection respected. Violates hygiene Rule 1 (spec-id in agent HTML comment); eval naming vs `test_a_`…`test_q_`; S09 agent vs shell-script work. |
| **Overall** | **3.5/5** | **Conditional** |

### Post-fix score estimate (not a re-audit)

| Dimension | Est. | Rationale |
|-----------|------|-----------|
| Completeness | 4/5 | Unchanged breadth; KD-11 closes the main completeness gap |
| Feasibility | 4/5 | Opt1×Opt2 risk now specified with bootstrap + primer retention |
| Structure | 5/5 | Phase/dep graph and S01 ownership fixed; S06→S07 over-serialization removed |
| Specificity | 5/5 | Naming, paths, agent assignment, DoDs tightened |
| Risk Awareness | 5/5 | KD-11 + S02/S07 hard constraints |
| Convention Compliance | 4/5 | Hygiene Rule 1 + eval naming + S09 agent assignment fixed |
| **Overall** | **~4.2/5** | **Approve** (re-run `/z-spec-judge` for an official re-score if desired) |

## Findings

### Strengths

- Grounded in a real audit (`analysis/context-token-reduction-report.md`) with clear OOS for Option 9.
- **KD-10 compress-last** is better than the analysis’s Opt-4-after-Opt-2 ordering for the split: thin agents are compressed after they exist.
- Hard boundaries respected: no auto-edit of `scripts/create-crux-zip.py`; dist additions flagged for user approval; upgrade file planned per `spec-implementation-hygiene.mdc` Rule 3.
- Subtasks use CRUX agents (`crux-platform-architect`, `crux-software-engineer`, `crux-cursor-rule-manager`, `docs-sync-agent`) — not `generalPurpose`.
- Deliverables and DoDs are unusually concrete (schemas, `rg` checks, token thresholds, dry-run zip checks).
- Codebase spot-checks largely confirm assumptions: memory-manager ~27 KB / 351 lines; five “When invoked with…” blocks in `crux-compress.md`; Canvas template present; `crux-test.md` non-dist; `spec-agent-allocation.md` always-on; eval alphabetical prefix convention exists through `test_q_`.

### Issues

| # | Severity | Subtask | Finding | Recommendation |
|---|----------|---------|---------|----------------|
| 1 | HIGH | Index / 09 | Manifest lists S08 and S09 both **Phase 4** and Execution Order says they run **in parallel**, but S09 **depends on S08**. Same-phase dependency forbids true parallelism; Spec System phase rule requires a subtask’s phase > all dependency phases. | Move S09 to **Phase 5**. Update Manifest, Execution Order heading, and mermaid (optional label). Keep edges `S05/S07/S08 → S09`. |
| 2 | HIGH | 01 / 05 | **Internal contradiction**: D04 edits `crux-cursor-memory-manager.md`, but Implementation Notes say this subtask does **not** touch that file because S05 owns the split. S05 will rewrite the umbrella to a ≤60-line shim, discarding S01 edits. | Remove `crux-cursor-memory-manager.md` from S01 D04/D06. Keep meditation-guide in S01. Require S05 thin agents to include lazy-CRUX + `context_manifest` honor blocks (already in S05 D01 — reinforce). |
| 3 | HIGH | 01 / 02 / 07 | **Opt 1 × Opt 2 chicken-and-egg**: S07 approach (c) puts `⟦CRUX:…⟧` in agent/command/skill **bodies**. S01 makes non-rule-manager agents skip `CRUX.md`. S02 slims `_CRUX-RULE.mdc` and may remove the always-on **CRUX Decompression — CRITICAL** primer that makes approach (c) safe. Analysis BC for Opt 1 explicitly relies on that primer. | Add an index KD (or S02/S07 notes): always-on surface **must retain** enough CRUX decompression guidance for in-body CRUX primitives; S02 must not delete decompression/path-construction essentials; any Wave that compresses an agent that no longer loads `CRUX.md` must either keep a plaintext “load CRUX.md before interpreting this body” line above the CRUX fence, or keep unconditional load for that agent. |
| 4 | HIGH | 05 | D03 HTML comment embeds `spec context-token-reduction` and “follow-up spec (id TBD)” inside a **production agent file**, violating `spec-implementation-hygiene.mdc` Rule 1 (no spec/subtask refs in code). | Replace with a deprecation notice that names **behavior** and **removal criteria** without a spec id (e.g. “DEPRECATED dispatcher — prefer `crux-memory-*`; remove after one minor release once thin agents ship in dist”). Keep upgrade/removal tracking in the spec/upgrade script only. |
| 5 | MEDIUM | 06 | Eval file named `evals/test_crux_command_suite.py` breaks the repo’s `test_a_`…`test_q_` sequencing convention documented in `crux-software-engineer.md`. | Rename to `evals/test_r_crux_command_suite.py` (or next free letter) and update shim / DoD references. |
| 6 | MEDIUM | 04 / 05 | S04 D03 edits the same memory **commands** S05 later re-points (`crux-dream` etc.). Ordering via S05→S04 dep is correct, but S04 notes claim “no overlap” with S05 — false for commands. D03 lists six commands (incl. amnesia) while notes say “five”. | Fix notes: S04 owns pointer/dedupe edits; S05 re-points spawn targets afterward. Align “five/six” wording. Optionally add soft note in S05: re-read commands after S04. |
| 7 | MEDIUM | 09 | Assigned entirely to `docs-sync-agent`, but D01 is a non-trivial **bash upgrade script** (and path mentions `install.py --repair`, which **does not exist** — notes hedge, but easy to miss). Upgrade path cites `.cursor/skills/crux/crux-skill-memory-index/...` — repo layout is `.cursor/skills/crux-skill-memory-index/` (consumer install may nest under `crux/`). | Split: `crux-software-engineer` owns `upgrade-*.sh`; `docs-sync-agent` owns README/CONTRIBUTORS/web/report prose — **or** keep one subtask but dual-assign / clarify primary = engineer with docs-sync for doc files. Fix index script path language to “repo path vs install path”. Drop or clearly mark `--repair` as non-existent. |
| 8 | MEDIUM | 07 | DoD08 says run `python3 scripts/test.py` **after every accepted wave**; Testing Strategy says only between wave groups / at end. Contradictory instructions to the executor. | Align: e.g. full suite after Wave 1, after Wave 2, and after final wave; not after every single file. |
| 9 | MEDIUM | 07 | Dependency on S06 is weakly justified (compression does not need the pytest shim). Over-serializes Phase 3. | Drop `06` from S07 deps **or** document why (e.g. avoid compressing pre-shim `crux-test.md` race — already Explicitly skip). Prefer drop. |
| 10 | MEDIUM | 01 | Objective text implies foundational rule #1 currently says “load `CRUX.md` unconditionally”. Actual AGENTS.md rule #1 is already “interpret CRUX rules in context”; the load cue is the **preamble** paragraph. D03 lists `integrity-expert` / `docs-sync-agent` as having unconditional Read blocks — integrity uses “if not already loaded”; docs-sync has no unconditional Read. | Retarget D01 to the preamble + rule #1 wording accurately; soften D03 to “any unconditional / early mandatory CRUX.md load”. |
| 11 | LOW | Index | Mermaid graph lacks `%% spec-system:classes:begin/end %%` classDef block (aggregator usually injects on first status rebuild). | Optional: leave for aggregator, or add empty managed block now. |
| 12 | LOW | 03 / 04 | Pointers use filesystem paths in instructional prose (`\.cursor/skills/_memory-shared.md`). `skill-and-agent-references.mdc` prefers names for skills/agents; path-as-subject is an allowed exception for data files — borderline. | Prefer “shared memory reference doc `_memory-shared.md` (under `.cursor/skills/`)” once, then section anchors; avoid teaching path-only references as the primary skill API. |
| 13 | LOW | 08 | DoD04 ≥30% cumulative reduction across three workflows is a hard gate that can fail due to measurement methodology even if work is correct. | Soften to “record measurable reduction; target ≥30% aspirational” or define exact measurement recipe in the subtask. |

### Dependency Graph

**Edges (manifest ↔ mermaid):** Match for declared deps.

| Check | Result |
|-------|--------|
| Files exist for all manifest rows | Pass (01–09) |
| Metadata deps match manifest | Pass |
| No dependency on higher ID | Pass |
| Phase > all dependency phases | **Fail** — S09 phase 4 depends on S08 phase 4 |
| Parallelism claims | **Fail** — Phase 4 “parallel” overstates S08∥S09 |
| Missing edges | None critical. Soft coordination S01↔S02 (wording) is documented, not a hard edge — acceptable. |
| Unnecessary edges | S07→S06 weakly justified (Issue 9) |
| Over-serialization | Mild (S06→S07); Phase 1 five-way parallel is correctly file-disjoint **except** the S01 memory-manager ownership bug |

Suggested phase layout after fix:

```text
Phase 1: 01, 02, 03, 04, 06
Phase 2: 05
Phase 3: 07
Phase 4: 08
Phase 5: 09
```

### Subtask Quality Snapshot

| ID | Objective clarity | Deliverables | Agent fit | Notes |
|----|-------------------|--------------|-----------|-------|
| 01 | Strong | Strong | `crux-platform-architect` ✓ | Fix D04/notes conflict; retarget AGENTS edit locus |
| 02 | Strong | Strong | `crux-cursor-rule-manager` ✓ | Must preserve decompression primer (Issue 3) |
| 03 | Strong | Strong | `crux-platform-architect` ✓ | Dist flag clear |
| 04 | Strong | Strong | `crux-platform-architect` ✓ | Fix five/six + overlap notes |
| 05 | Strong | Strong | `crux-platform-architect` ✓ | Hygiene Rule 1 on deprecation comment |
| 06 | Strong | Strong | `crux-software-engineer` ✓ | Eval naming convention |
| 07 | Strong | Strong but large | `crux-cursor-rule-manager` ✓ | Align DoD vs testing; consider drop S06 dep |
| 08 | Strong | Strong | `crux-software-engineer` ✓ | Soften ≥30% gate |
| 09 | Strong | Strong | `docs-sync-agent` partial | Shell upgrade better as engineer |

### Risk Summary

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Compressed agent bodies unreadable after lazy CRUX + slim `_CRUX-RULE` | Med | High | Issue 3 — retain always-on decompression primer; plaintext bootstrap above CRUX fence |
| Consumer dist zip missing thin agents / templates until user approves zip script | High (by design) | Med | Already mitigated by umbrella shim + Subtask 09 approval section — keep |
| S07 confidence bar causes many deferrals → savings miss ≥30% DoD | Med | Med | Defer list OK; soften S08 ≥30% hard gate |
| S01 edits to memory-manager wasted / merge conflict with S05 | High if unfixed | Med | Issue 2 |
| Phase mis-claim causes executor to spawn S09 before S08 finishes | Med | Med | Issue 1 |
| Spec-id comment leaks into shipped agent | Certain if D03 as written | Low–Med | Issue 4 |
| Grep evals break after approach (c) | Med | Med | Already planned in S07 D03 + S08 |
| Temporary umbrella shim becomes permanent | Med | Med | KD-3 + upgrade file; enforce ≤60 lines via S08 eval |

## Recommendation

**Pre-fix**: Conditional — address HIGH findings before `/z-spec-execute`.

**Post-fix (2026-07-13)**: All nine HIGH/MEDIUM recommendations from this assessment were applied to the spec index and subtask files. Estimated post-fix score **~4.2/5 (Approve)**. Spec is ready for `/z-spec-execute`. Optional: re-run `/z-spec-judge` on this path for an official fresh score; LOW items (mermaid classDef block; `_memory-shared` path-pointer wording) remain open and are non-blocking.

### Recommended fix set — APPLIED

1. ~~S09 → Phase 5; fix Execution Order parallelism wording.~~ **Done**
2. ~~S01: remove memory-manager from D04/D06; fix Implementation Notes; retarget AGENTS preamble wording.~~ **Done**
3. ~~Index KD + S02/S07 notes: retain always-on CRUX decompression primer; bootstrap rule for CRUX-bodied agents.~~ **Done (KD-11)**
4. ~~S05: rewrite deprecation comment without spec ids.~~ **Done**
5. ~~S06: rename planned eval to `test_r_crux_command_suite.py`.~~ **Done**
6. ~~S04: fix five/six + overlap notes with S05.~~ **Done**
7. ~~S09: assign upgrade script to `crux-software-engineer`; fix index path / `--repair` language.~~ **Done**
8. ~~S07: align DoD08 with Testing Strategy; drop S06 dependency.~~ **Done**
9. ~~S08: soften ≥30% hard DoD to measured + aspirational target.~~ **Done**

**Fixes applied**: all nine listed above (2026-07-13).
