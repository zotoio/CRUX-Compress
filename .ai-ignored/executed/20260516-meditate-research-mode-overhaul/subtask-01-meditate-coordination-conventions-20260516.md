# Subtask: Coordination Conventions (filenames, slugs, timestamps, working directory tree)

## Metadata
- **Subtask ID**: 01
- **Feature**: Meditate Research-Mode Overhaul
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: None
- **Created**: 20260516

## Objective

Establish the file-naming, slug + timestamp, glob-based polling, and shared coordination-file conventions that every later subtask in this spec relies on. Without these conventions in place, the Research/Quick split, the adversarial review cycle, the facet registry, the pending/confirmed facet escalation, and the report filename pairing all collapse.

## Files Modified

- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`

## Deliverables Checklist

- [x] Every branch / peer-review / report / review-iteration filename in both files uses the unified pattern documented below
- [x] The working-directory tree in the agent file lists every coordination file produced by every later subtask (registry, lock, citations index, pending/confirmed facets, review iterations, reports)
- [x] Polling agents use prefix-glob matching, not literal filename equality
- [x] The `{topic-slug}` and `{ts}` placeholders are defined exactly once and referenced consistently from both files
- [x] No literal `branch-1.md` / `report.html` / `report.pdf` strings remain (other than the explicit "Never hard-code these names" rule documented in this subtask)

## Definition of Done

- [x] Filename + glob conventions documented in both files match each other character-for-character
- [x] Linter passes on both files
- [x] Manual grep for `branch-\d+\.md`, `report\.html`, `report\.pdf` returns only the explicit forbidden-defaults call-outs

## Implementation Notes

### Convention summary (the canonical reference)

All branch / peer-review / report / review-iteration files written into the meditation working directory follow these patterns:

| Artefact | Filename pattern | Notes |
|----------|------------------|-------|
| Top-level facets (initial, pre-confirmation) | `facets-pending-{ts}.yml` | Deleted after the user confirms via Q-Confirm-1 |
| Top-level facets (final, post-confirmation) | `facets.md` | Single navigational entry point; updated post-consolidation with the Branch & Leaf Index |
| Branch (depth 1, 2, 3) | `branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md` | `D` ∈ {1,2,3}; `S = 0` at depth 1, `S` ∈ {1,2,3} at depth 2, `S` ∈ {1,...,9} at depth 3 |
| Branch (intermediate, Phase B working draft) | `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}-findings.md` | Research mode only; deleted after Phase G promotion |
| Peer review (Research mode) | `branch-{N}-peer-review-{branchSlug}-{ts}.md` | One per branch |
| Pending deep-facet confirmation request | `pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml` | Only when `confirmDeepFacets ≠ none`; `D` is the **parent** agent's depth |
| Confirmed deep-facet response | `confirmed-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml` | Same path-id and `{ts}` as the pending file |
| Adversarial review iteration | `review-pre-report-{ts}-iter-{N}.md` | `N` ∈ {1, 2, 3}; iteration cap |
| Report HTML | `report-{topic-slug}-{ts}.html` | Shares `{ts}` with PDF pair |
| Report PDF | `report-{topic-slug}-{ts}.pdf` | Shares `{ts}` with HTML pair |

Where:

- `{topic-slug}` is the slug component of the working-directory name (`{yyyymmdd}-{topic-slug}/`) — extract as everything after the leading `yyyymmdd-`.
- `{slug}` (in branch filenames) is the kebab-case slug derived for that branch (depth 1) or that subfocus (depth 2/3); max 40 chars; lowercase; alphanumerics + hyphens only; stop-words stripped; the most meaningful 3–6 words.
- `{ts}` is the UTC timestamp `yyyymmddHHMMSS` captured at the moment the file is written: `date -u +%Y%m%d%H%M%S`.
- `{N}`, `{D}`, `{S}` are zero-padded numerals used as written above (`branch-1`, not `branch-01`).

### Polling — prefix-glob, never equality

Because the slug + timestamp suffix is not predictable until the writing agent commits the file, every polling agent must use **prefix-glob matching**:

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

Use `ls -1t .../glob-pattern 2>/dev/null | head -n 1` to resolve the **latest** matching artefact when multiple regenerations have occurred (relevant for reports and review iterations).

### Working directory structure (canonical tree, applies to both modes)

Document this tree in the **agent file's** Meditate Mode section, immediately under the recursive-exploration protocol:

```
meditations/{yyyymmdd}-{topic-slug}/
├── facets-pending-{ts}.yml                                   # depth-0 draft awaiting user confirmation (deleted after Q-Confirm-1 resumes)
├── facets.md                                                 # 3 user-confirmed top-level facets + slugs (depth-0); UPDATED post-consolidation with Branch & Leaf Index linking every file below
├── facet-registry.yml                                        # Research mode only — global facet allocation
├── citations-index.yml                                       # Research mode only — append-only citation index
├── .facet-registry.lock/                                     # Research mode only — transient mkdir-mutex
├── pending-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml      # deep-confirmation request from a child agent; only when confirmDeepFacets ≠ none
├── confirmed-facets-branch-{N}-depth-{D}-sub-{S}-{ts}.yml    # paired confirmation written by depth-0 manager; same path-id + {ts} as the pending file
├── branch-1-depth-1-sub-0-{branch-1-slug}-{ts}-findings.md   # Research mode only — Phase B working draft (deleted after Phase G)
├── branch-1-depth-1-sub-0-{branch-1-slug}-{ts}.md            # Branch 1 final aggregated output (depth-1)
├── branch-1-depth-2-sub-1-{d2-sub-1-slug}-{ts}.md            # Branch 1, depth-2 subfocus 1
├── branch-1-depth-2-sub-2-{d2-sub-2-slug}-{ts}.md
├── branch-1-depth-2-sub-3-{d2-sub-3-slug}-{ts}.md
├── branch-1-depth-3-sub-1-{d3-sub-1-slug}-{ts}.md            # Leaf: depth-3 under depth-2-sub-1 (×3 each)
├── branch-1-depth-3-sub-2-{d3-sub-2-slug}-{ts}.md
├── branch-1-depth-3-sub-3-{d3-sub-3-slug}-{ts}.md
├── ...                                                       # (up to 9 depth-3 files per branch)
├── branch-2-depth-1-sub-0-{branch-2-slug}-{ts}.md
├── branch-2-depth-2-sub-{1..3}-{slug}-{ts}.md
├── branch-2-depth-3-sub-{1..9}-{slug}-{ts}.md
├── branch-3-depth-1-sub-0-{branch-3-slug}-{ts}.md
├── branch-3-depth-2-sub-{1..3}-{slug}-{ts}.md
├── branch-3-depth-3-sub-{1..9}-{slug}-{ts}.md
├── branch-1-peer-review-{branch-1-slug}-{ts}.md              # Research mode only — peer review of branch 1
├── branch-2-peer-review-{branch-2-slug}-{ts}.md
├── branch-3-peer-review-{branch-3-slug}-{ts}.md
├── consolidation.md                                          # Final synthesis (depth-0)
├── review-pre-report-{ts}-iter-1.md                          # MANDATORY (both modes) — adversarial review iteration 1
├── review-pre-report-{ts}-iter-2.md                          # only present if iteration 2 was needed
├── review-pre-report-{ts}-iter-3.md                          # only present if iteration 3 was needed (cap = 3)
├── report-{topic-slug}-{ts}.html                             # MANDATORY (both modes); {topic-slug} matches the working-directory slug, {ts} is UTC yyyymmddHHMMSS at write time
└── report-{topic-slug}-{ts}.pdf                              # MANDATORY (both modes); shares the same {ts} as its HTML pair
```

(Some files in the tree above are produced by later subtasks; document them all here so the tree is the canonical reference.)

### Output file frontmatter (Research mode)

Every branch file (depths 1–3) carries this YAML frontmatter:

```yaml
---
mode: "research"
branch: {N}
depth: {D}
subfocus_index: {S}                       # 0 at depth 1, 1–3 at depth 2, 1–3 at depth 3 (local to parent's children)
subfocus_slug: "{kebab-case slug used in filename}"
subfocus: "{this agent's specific subfocus}"
parent_subfocus: "{parent agent's subfocus, or top-level facet if depth 1}"
parent_slug: "{parent's subfocus_slug, or null at depth 1}"
timestamp_utc: "{yyyymmddHHMMSS}"         # matches the {ts} segment of the filename
timestamp_iso: "{ISO 8601}"
incorporated_children: ["branch-{N}-depth-{D+1}-sub-1-{slug}-{ts}.md", ...]   # empty array at depth 3
---
```

Quick-mode files use identical frontmatter but with `mode: "quick"`.

Body sections (mandatory, both modes):

- `## Subfocus Rationale` — why this narrowing was chosen
- `## Discoveries` — key findings from memory queries and research
- `## Connections` — patterns, relationships, non-obvious links
- `## Child Subfocuses` — the 3 narrower subfocuses derived for children (if applicable)
- `## Child Insights` — aggregated from child output files (if applicable), with provenance markers `[child: branch-N-depth-D-sub-S]`
- `## Contradictions` — contradictions surfaced between this depth's findings and the children's, or between children
- `## Summary` — concise distillation for parent consumption
- `## Citations` — every source backing every claim (mandatory in both modes — see subtask 02 for the enforcement strength difference)

### What to enforce explicitly in the docs

Add a **Never hard-code these names** rule near the report-filename convention:

> All references in this document, in the agent definition, and in the Branch & Leaf Index match these files via the prefix glob `report-{topic-slug}-*.html` / `report-{topic-slug}-*.pdf`. Never hard-code `report.html` / `report.pdf`.

This rule is the only place the deprecated literals may appear.

### What to delete

Strip every legacy `branch-1.md` / `branch-2.md` / `branch-3.md` reference from both files; replace with the unified `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}.md` pattern. Strip every `report.html` / `report.pdf` reference except in the explicit "Never hard-code" rule above.

## Testing Strategy

**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:

- After applying the changes, grep both files for the deprecated literals and confirm only the forbidden-defaults call-out remains.
- Sanity-read the Working directory structure block in the agent file end-to-end and confirm every artefact named anywhere else in either file appears in the tree.
- Run the linter on both files (`cursor` lint or whatever the repo uses).

## Execution Notes

### Agent Session Info
- Agent: crux-platform-architect
- Started: 2026-05-16
- Completed: 2026-05-16

### Work Log

1. Loaded `AGENTS.md`, `CRUX.md`, the spec index, and both target files. Grepped both files for legacy literals (`branch-\d+\.md`, `branch-\{N\}.md`, `branch-\{N\}-depth-{2,3}-sub-{S}.md`, `report.html`, `report.pdf`) to build a complete change inventory before editing.
2. **Agent file** (`.cursor/agents/crux-cursor-memory-manager.md`):
   - Replaced the short "Working directory" pointer with a new **Coordination Conventions** subsection containing the canonical filename-pattern table, placeholder definitions (`{topic-slug}`, `{slug}`, `{ts}`, `{N}`, `{D}`, `{S}`), the polling prefix-glob list, and the "Never hard-code these names" rule. Positioned immediately under the invocation table so every later subsection inherits the conventions.
   - Updated workflow steps 5 (Poll for Branch Outputs) and 6 (Consolidate) to use the unified `branch-{N}-depth-1-sub-0-*.md` prefix-glob pattern with `ls -1t … | head -n 1` resolution.
   - Updated recursive-exploration steps 4 (Recurse) and 5 (Aggregate), plus the depth-3 termination rule, to write to and poll for files matching `branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}.md`.
   - Replaced the legacy 9-line working-directory tree with the canonical tree from the subtask, listing every coordination file that any later subtask will produce (`facets-pending-{ts}.yml`, `facet-registry.yml`, `citations-index.yml`, `.facet-registry.lock/`, `pending-facets-*.yml`, `confirmed-facets-*.yml`, `branch-{N}-depth-1-sub-0-{slug}-{ts}-findings.md`, peer reviews, `review-pre-report-{ts}-iter-{N}.md`, `report-{topic-slug}-{ts}.html`, `report-{topic-slug}-{ts}.pdf`).
   - Added the "Some files in the tree above are produced by later subtasks…" caveat after the tree so future readers know why workflow-less artefacts appear.
   - Replaced the legacy 6-field output frontmatter with the full Research/Quick schema (`mode`, `branch`, `depth`, `subfocus_index`, `subfocus_slug`, `subfocus`, `parent_subfocus`, `parent_slug`, `timestamp_utc`, `timestamp_iso`, `incorporated_children`), kept the body-section list, and added the new `## Contradictions` and `## Citations` mandatory sections.
3. **Command file** (`.cursor/commands/crux-meditate.md`):
   - Inserted a new `### Coordination Conventions` section between Argument Handling and What Happens. The table, polling-glob list, and "Never hard-code these names" rule mirror the agent file character-for-character; the section references the agent file for placeholder definitions (defined exactly once, per the deliverable).
   - Updated steps 5e (poll), 5f (write), 6 (Level 3), and 7 (Consolidation) to use the unified filename pattern and prefix-glob polling.
   - Updated Report Generation step 1 (read inputs), step 2 (HTML filename), and step 3 (PDF command) to use `report-{topic-slug}-{ts}.html` / `.pdf` with `{ts}` pair-sharing and `ls -1t … | head -n 1` resolution for the headless-Chrome render input.
4. **Verification**:
   - Re-grep of both files for `branch-\d+\.md`, `report\.html`, `report\.pdf` returns only the two explicit "Never hard-code these names" call-outs (one in each file) — exactly the forbidden-defaults rule, matching the spec requirement.
   - Re-grep for `branch-\{N\}.md`, `branch-\{N\}-depth-{2,3}-sub-\{S\}.md`, `branch-\*.md`, and `branch-\{N\}-depth-\{D\}-sub-\{1,2,3\}.md` returns zero matches — every legacy filename is gone.
   - `diff` of the shared shared blocks (filename-pattern table + polling block + Never-hard-code rule) between the two files returned `EXACT MATCH` (DoD01).
   - Sanity-read of the canonical working-directory tree confirmed every artefact named anywhere in either file appears in the tree.
   - `ReadLints` on both files returned no errors (DoD02). No project-level markdown linter (markdownlint / prettier) is configured at the repo root, so IDE diagnostics are the linter of record.

### Blockers Encountered
None.

### Files Modified
- `.cursor/commands/crux-meditate.md` — added `### Coordination Conventions` section (filename-pattern table, prefix-glob polling block, "Never hard-code these names" rule). Updated steps 5e, 5f, 6, 7 in `What Happens` and steps 1, 2, 3 in `Report Generation` to use the unified filename pattern + prefix-glob polling + `ls -1t` latest-match resolution.
- `.cursor/agents/crux-cursor-memory-manager.md` — added Coordination Conventions canonical reference (table, placeholders, polling globs, Never-hard-code rule) inside Meditate Mode. Updated top-level workflow steps 5–6 and recursive-exploration steps 4–5 plus the depth-3 termination rule to use the unified filename pattern + prefix-glob polling. Replaced the working-directory tree with the canonical tree from the subtask. Replaced the legacy output frontmatter and body-section list with the new Research/Quick schema (`mode`, `subfocus_slug`, `parent_slug`, `timestamp_utc`/`timestamp_iso`, `incorporated_children` + mandatory `## Contradictions` and `## Citations` sections).
