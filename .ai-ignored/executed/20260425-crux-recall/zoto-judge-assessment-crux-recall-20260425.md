# Spec Assessment: CRUX Recall — Rename & Memory Visualization

**Target**: `specs/20260425-crux-recall/spec-crux-recall-20260425.md`
**Assessed**: 2026-04-25
**Verdict**: Conditional

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 4/5 | Rename coverage thorough via grep DoD; missing explicit handling for generated CRUX files (`install.crux.md`) and `--total` feature documentation |
| Feasibility | 3/5 | Rename subtasks straightforward; canvas force simulation from scratch with no external deps is very ambitious for one subtask |
| Structure | 5/5 | Clean 4-phase dependency graph, correct ordering, good parallelism |
| Specificity | 4/5 | Subtasks 01–03, 05, 06 are well-specified; subtask 04 relies on catch-all grep; subtask 07 canvas verification is vague |
| Risk Awareness | 3/5 | No fallback for force simulation complexity; no rollback plan; canvas SDK limitations unaddressed |
| Convention Compliance | 4/5 | Respects CRUX rules, uses correct file structure; could explicitly note canvas skill dependency |
| **Overall** | **3.9/5** | **Conditional — address findings before executing** |

## Findings

### Strengths

- **Well-structured dependency graph**: 4 phases with correct dependency ordering. Phase 1 parallelism (3 concurrent rename subtasks) is smart. No circular dependencies, no over-serialization.
- **Thorough rename DoD**: The spec-level Definition of Done enforces a zero-hit case-insensitive grep, which catches any files the subtasks miss.
- **CRUX rule compliance**: Subtask 03 correctly identifies that `.crux.mdc` files must be regenerated from source, not edited directly. `AGENTS.md` correctly identified as a source file.
- **Subtask 06 data model**: TypeScript interfaces for `MemoryNode` and `MemoryEdge`, plus the edge construction algorithm, give the executing agent a concrete target.
- **Testing strategy avoids interference**: Each subtask explicitly avoids triggering global test suites during parallel phases, reserving full suite runs for the integration subtask.

### Issues

| # | Severity | Subtask | Finding | Recommendation |
|---|----------|---------|---------|----------------|
| 1 | HIGH | 04 | `install.crux.md` is a generated CRUX file (has `sourceChecksum` frontmatter). Subtask 04's implementation notes say "Check install.py and install.crux.md for any references" without distinguishing the generated file. A naive agent may edit `install.crux.md` directly, violating CRUX rules. `install.py` has 5 mindreader references; after updating it, `install.crux.md` must be regenerated via the `crux-cursor-rule-manager` subagent. | Add an explicit deliverable: "Update `install.py`, then regenerate `install.crux.md` via `crux-cursor-rule-manager` (do NOT edit the `.crux.md` directly)" |
| 2 | HIGH | 06 | The canvas SDK (`cursor/canvas`) provides no force simulation, no external npm packages, and no SVG graph component. The only graph layout available is `computeDAGLayout` (hierarchical DAG, not force-directed). Implementing a complete force simulation + SVG rendering + interactive features (click, hover, drag, search, filter, force controls, pan/zoom) from scratch in a single `.canvas.tsx` file is very ambitious. No fallback is defined if the force simulation proves too complex. | Add a risk note to subtask 06 acknowledging the SDK has no force simulation component. Define a fallback: if force-directed is infeasible, consider using `computeDAGLayout` from the SDK for a hierarchical graph instead, or a simplified spring layout. Also consider splitting the subtask if scope grows too large. |
| 3 | MEDIUM | 04 | Subtask 04's Deliverables Checklist only explicitly names `README.md` and `AGENTS.md`, with a catch-all "Any other files referencing mindreader discovered via project-wide grep." Codebase grep reveals 21 files with mindreader references. Several high-risk files are not mentioned: `CONTRIBUTORS.md` (2 refs), `docs/crux-memories.md`, `web/compress.md/memories.html`, `.crux/crux-release-files.json`, `.crux/dist-manifest.json`, `scripts/create-crux-zip.py`, `evals/USER_EVAL_CHECKLISTS.md`, `.cursor/commands/crux-amnesia.md`, `.cursor/commands/crux-dream.md`, `.cursor/commands/crux-forget.md`. | List additional high-priority files in subtask 04's deliverables or implementation notes. At minimum: `CONTRIBUTORS.md`, `docs/crux-memories.md`, `web/compress.md/memories.html`, `.cursor/commands/crux-{amnesia,dream,forget}.md`, and the `.crux/*.json` metadata files. |
| 4 | MEDIUM | — | No rollback plan in the spec index. The rename touches 21+ files across commands, agents, config, rules, documentation, scripts, and website. If something breaks mid-execution, there's no documented recovery path. | Add a rollback section to the spec index: "All changes are file renames and text replacements. Rollback via `git checkout` of the affected files." |
| 5 | MEDIUM | 06 | Subtask 06's objective says "Implement the interactive force-directed visualization" but the actual deliverable is agent workflow documentation + a canvas specification, not a persistent code artifact. Canvases are generated dynamically by the agent at runtime when the user runs `/crux-recall --total`. The subtask conflates two concerns: (a) defining the agent workflow and canvas specification, and (b) verifying the approach works. | Clarify in subtask 06 that the primary deliverable is the agent's `--total` workflow implementation in the memory manager definition (building on subtask 05's interface). Optionally include generating a test canvas to verify the approach. |
| 6 | LOW | 05 | Subtask 05 depends on 01 and 02 but not 03. This is correct (05 modifies the command file and agent definition, not config). However, the config JSON (`.crux/crux-memories.json`) has `commands.mindReader.description: "Decompress and view memories in chat"` — this description may need updating when `--total` is added. Subtask 03 renames the key but doesn't update the description for the new capability. | Consider adding a note in subtask 03 or 05 that the command description in `.crux/crux-memories.json` should be updated to reflect the `--total` capability (e.g., "Decompress, view, and visualize memories"). |
| 7 | LOW | — | No subtask explicitly documents the `--total` feature in user-facing documentation (README.md). Subtask 04 handles the rename across docs, and subtask 05 defines the `--total` interface, but neither adds `--total` usage examples to README.md or other docs. | Consider adding a note to subtask 04 or a follow-up subtask to document `--total` usage in README.md after the feature is complete. |

### Dependency Graph

The Mermaid graph accurately reflects the Subtask Manifest:
- **Edges match**: S01→S04, S02→S04, S03→S04, S01→S05, S02→S05, S05→S06, S04→S07, S06→S07
- **No missing edges**: Subtask 05 correctly excludes 03 (no config dependency). Subtask 06 correctly depends only on 05 (interface definition).
- **No unnecessary serialization**: Phase 1 (01, 02, 03) and Phase 2 (04, 05) correctly run in parallel where possible.
- **Phase assignments correct**: Each subtask's phase is strictly greater than all its dependencies' phases.

No graph issues found.

### Risk Summary

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Force simulation too complex for single canvas file | Medium | High | Define fallback to `computeDAGLayout` or simplified layout; consider subtask split |
| Agent edits `install.crux.md` directly | Medium | Medium | Explicit deliverable note about CRUX regeneration workflow |
| Missed mindreader references | Low | Medium | DoD grep catch-all covers this; explicit file list reduces risk |
| Canvas rendering issues at runtime | Medium | Low | Test canvas generation with actual memory data during subtask 07 |
| No docs for `--total` feature | Low | Low | Can be addressed post-execution or in a follow-up spec |

## Recommendation

The spec is well-structured with a clean dependency graph and thorough rename coverage. The two critical concerns are: (1) the `install.crux.md` generated-file handling needs to be explicit to prevent a CRUX rule violation during execution, and (2) the canvas force simulation complexity is the highest-risk element — adding a fallback strategy and acknowledging the SDK limitations will make subtask 06 more robust. Address the HIGH-severity findings before executing; the remaining issues are quality improvements that reduce execution risk.
