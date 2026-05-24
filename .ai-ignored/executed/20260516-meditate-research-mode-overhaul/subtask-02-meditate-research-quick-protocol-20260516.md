# Subtask: Research/Quick Mode Protocol Split

## Metadata
- **Subtask ID**: 02
- **Feature**: Meditate Research-Mode Overhaul
- **Assigned Subagent**: crux-platform-architect
- **Dependencies**: 01
- **Created**: 20260516

## Objective

Replace the original "fast parallel-fanout" Meditate Mode protocol with a **two-mode** model:

- **Research mode (default)** — depth-first within each branch, globally unique facets via `facet-registry.yml` + `mkdir`-mutex, mandatory citations validated strictly by parents (delete + respawn offending children), bottom-up rewrite incorporation, dedicated peer-review pass after branches complete.
- **Quick mode (`--quick`)** — preserves the prior fast parallel-fanout behaviour. Mandatory citations validated best-effort (warn-only). No global registry. No peer review. No bottom-up rewrite.

Both modes share every user-facing safeguard (cost ack, theme preflight, facet confirmation, mandatory reports, adversarial review) — those are added in subsequent subtasks. This subtask establishes the recursion model itself.

## Files Modified

- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`

## Deliverables Checklist

- [x] **Modes table** in the command file lists Research (default) and Quick (`--quick`) with the citation enforcement difference made explicit
- [x] **Mode selection logic**: parsing `$ARGUMENTS` for `--quick`, stripping it before deriving the topic-slug, propagating `meditateMode` to every child agent
- [x] **Research mode workflow** documents: depth-first recursion, global facet registry + lock, mandatory citations (strict enforcement), bottom-up rewrite incorporation, dedicated peer-review pass, citation validation by parents
- [x] **Quick mode workflow** documents: parallel fan-out (3 child subfocuses derived upfront), sibling-aware uniqueness only, mandatory citations (warn-only enforcement), append-style aggregation, no peer review
- [x] **Recursive exploration protocol** (Phases A–G in Research, simpler 5-step in Quick) covers depth 1, depth 2, depth 3 termination
- [x] **Facet registry protocol** with `mkdir`-based lock snippet documented (Research mode only)
- [x] **Citations protocol** documented with inline marker formats (`[memory: ...]`, `[file: path:start-end]`, `[web: url]`, `[chat: ...]`, `[child: branch-N-depth-D-sub-S]`), validation rule (Research strict, Quick warn-only), and `citations-index.yml` schema (Research mode only)
- [x] **Peer review file** spec (Research mode only) with frontmatter and required sections (Reinforcements, Contradictions, Gaps, New Evidence, Citations)
- [x] **Output file format (Research mode)** updated per subtask 01's frontmatter spec
- [x] **Output file format (Quick mode)** documented with `mode: "quick"` and the same citation requirements (with the warn-only enforcement caveat)
- [x] **Subfocus narrowing example** (Research mode) showing how depth-2 facets emerge from depth-1 research findings
- [x] **Design principles** in the agent file include: file-based coordination, 3-way fan-out at every level, predictable paths + self-describing files, mandatory citations (both modes), Research-mode-only specifics, Quick-mode-only specifics

## Definition of Done

- [x] Both modes' workflows are end-to-end internally consistent
- [x] Step numbering between command file and agent file aligns (the agent file's depth-0 manager workflow is steps 1–8 in this subtask, expanded to 1–13 by later subtasks; the command file's "Steps 1–8 subagent block" sub-steps map correctly)
- [x] Linter passes on both files

## Implementation Notes

### Modes table (command file)

Place this directly under the Usage block:

```markdown
## Modes

| Mode | Flag | Default? | Behaviour |
|------|------|----------|-----------|
| **Research** | _(none — default)_ | yes | Depth-first serial recursion. Each depth's findings drive the next depth's facet derivation. Globally unique facet allocation across all branches. Bottom-up incorporation. Branch peer review at the top. **Mandatory citations at every step.** |
| **Quick** | `--quick` | no | Fast parallel fan-out (legacy behaviour). All 3 facets per node derived upfront and explored in parallel. **Citations are still mandatory** (same `## Citations` requirement as Research mode), but the parent validates them best-effort and warns rather than re-spawning offending children. Use when you want speed over rigor. |
```

### Mode selection (agent file Meditate Mode section)

```markdown
**Mode selection**: The top-level invocation receives the raw `$ARGUMENTS` from the slash command. Inspect it for the `--quick` flag:
- If `--quick` is present → set `meditateMode: quick` and follow the **Quick mode protocol** below. Strip the flag before deriving the topic-slug.
- Otherwise → set `meditateMode: research` and follow the **Research mode protocol** (this is the default and the recommended path for any work that will be cited, persisted, or used to drive downstream changes).

The `meditateMode` value is propagated to every child agent in the tree so the entire subagent population uses the same protocol.
```

### Research mode top-level workflow (agent file, depth-0 manager — steps 1–8 in this subtask; expanded to 1–13 by later subtasks)

```
1. Check Feature Guard (flags.enableMemories must be "true")
2. Create Working Directory (`meditations/{yyyymmdd}-{topic-slug}/`)
3. Initialize coordination files (facet-registry.yml seeded empty; citations-index.yml seeded empty; .facet-registry.lock/ does not yet exist)
4. Derive top-level facets (cited)  → write initial facets.md (subtask 03 will add the Pattern-B confirmation)
5. Spawn Explorers (3 background subagents in parallel; each receives meditateMode, meditateDepth=1, maxDepth=3, branchNumber, branchSlug, subfocus, parentSubfocus, workingDir, parentContext, siblingFacets)
6. Poll for Branch Outputs via prefix-glob (branch-{1,2,3}-depth-1-sub-0-*.md)
7. Branch Peer Review (spawn 3 peer-review agents in parallel; each writes branch-{N}-peer-review-{branchSlug}-{ts}.md)
8. Consolidate (read all 3 branch files plus all 3 peer-review files; write consolidation.md with key discoveries per branch, cross-branch connections, contradictions, gaps, unified citations section)
```

### Quick mode top-level workflow (agent file)

```
Same as Research steps 1–8 with these changes:
- Skip step 3 entirely (no facet-registry.yml, no citations-index.yml, no lock)
- Step 4: do not require citation backing for facet descriptions
- Step 5: spawn explorers with meditateMode: "quick"
- Skip step 7 (no peer review)
- Step 8: consolidate from branch-*-depth-1-sub-0-*.md files only; no citations index to read; no peer-review files to glob
```

### Recursive exploration protocol — Research mode (Phases A–G)

Each child agent at depths 1 and 2 follows this protocol. Receives `meditateMode: "research"`, `workingDir`, `branchNumber`, `meditateDepth`, `subfocus`, `subfocusSlug`, `subfocusIndex`, `parentSubfocus`, `siblingFacets`.

```
Phase A — Research own subfocus first (no children yet):
  - Query memory corpus via memory index (title, tag, description, body search)
  - Examine code/files/web sources implied by the subfocus
  - Expand on subfocus in light of evidence
  - Track every claim with at least one citation

Phase B — Write findings file first:
  branch-{N}-depth-{D}-sub-{S}-{slug}-{ts}-findings.md (working draft)

Phase C — Derive 3 child subfocuses from actual findings:
  - Each must be narrower, distinct, globally unique against facet-registry.yml
  - Acquire registry lock (mkdir-based)
  - Read registry, check global slug + paraphrase uniqueness
  - Refine any colliding subfocus until all 3 are globally unique
  - Append confirmed 3 subfocuses to facet-registry.yml
  - Release lock

Phase D — Spawn 3 children at depth+1 in parallel
  Each child receives: meditateMode, workingDir, branchNumber, parentSubfocus,
  subfocus, subfocusSlug, subfocusIndex (1, 2, or 3 — local to this parent's children)

Phase E — Wait for child files (prefix-glob branch-{N}-depth-{D+1}-sub-{S}-*.md)

Phase F — Incorporate child findings bottom-up:
  - Read all 3 child files
  - REWRITE this depth's own file (do NOT just append) to weave children's findings
  - Preserve every citation
  - Deduplicate overlapping evidence
  - Surface cross-child patterns
  - Flag contradictions in a ## Contradictions section
  - Provenance: every section indicates "this depth" or "child sub-{S}"

Phase G — Promote findings file to final filename:
  branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md (no -findings suffix)
  Then delete the -findings draft.
```

**Depth 3 (deepest)**: Phase A and Phase B only — no further recursion. Then promote the `-findings` draft to the final filename and delete the draft.

### Recursive exploration protocol — Quick mode

Each child agent at depth < `maxDepth`:

```
1. Pre-derive 3 child subfocuses upfront (no prior research)
   Each must be narrower, distinct from siblings, non-overlapping with facets.md entries
2. Spawn 3 children at depth+1 in parallel with meditateMode: "quick"
3. While children run, do this agent's own memory-query and expansion in parallel
4. Wait for all 3 child files via glob branch-{N}-depth-{D+1}-sub-{S}-*.md
5. Aggregate children + own expansion into a single output file
   branch-{N}-depth-{D}-sub-{S}-{slug}-{yyyymmddHHMMSS}.md
   (no rewrite — straight aggregation under ## Child Insights)
```

**Depth 3 (deepest, Quick mode)**: query memories, expand, write the leaf file. No citations validation respawn.

### Facet registry protocol (Research mode only)

`facet-registry.yml` schema:

```yaml
facets:
  - branch: 1
    depth: 0
    parent_slug: null              # null at depth 0; otherwise parent's subfocus_slug
    subfocus_slug: "auth-flow-trade-offs"
    subfocus: "Trade-offs in authentication flows for multi-tenant SaaS"
    timestamp_utc: "20260516103045"
    registered_by: "depth-0 manager"
  - branch: 1
    depth: 2
    parent_slug: "auth-flow-trade-offs"
    subfocus_slug: "session-vs-jwt"
    subfocus: "Session cookies vs JWT for cross-service auth"
    timestamp_utc: "20260516103217"
    registered_by: "branch-1 depth-1 agent"
  # ...
```

`mkdir`-based lock-and-append protocol (every registry update must use this):

```bash
attempts=0
until mkdir "{workingDir}/.facet-registry.lock" 2>/dev/null; do
  attempts=$((attempts + 1))
  if [ $attempts -gt 60 ]; then
    echo "Failed to acquire facet-registry lock after 60s" >&2
    exit 1
  fi
  sleep 1
done

# inside lock:
# 1. Read facet-registry.yml
# 2. For each candidate subfocus, verify slug + paraphrase uniqueness
#    against ALL existing entries (every branch, every depth)
# 3. If collision, regenerate the colliding subfocus and re-check
# 4. Once all 3 candidates are globally unique, append them

rmdir "{workingDir}/.facet-registry.lock"
```

If an agent crashes while holding the lock, the orphaned `.facet-registry.lock/` directory must be cleaned up by the depth-0 manager during branch-output polling — if any branch glob has been pending for more than 5 minutes AND the lock directory exists, log a warning and `rmdir` the lock so other agents can proceed.

### Citations protocol (both modes)

Inline citation markers (mandatory in body, attached directly to the claim they support):

- `[memory: title-or-id]`
- `[file: path/to/file.ts:start-end]`
- `[web: url]`
- `[chat: turn-N or quoted text]`
- `[child: branch-N-depth-D-sub-S]`

Every output file (depth-1, depth-2, depth-3, peer-review, consolidation) must:

1. Include a `## Citations` section at the bottom listing every source referenced.
2. Use inline citation markers throughout the body.
3. (Research mode only) Append every newly-introduced citation to `citations-index.yml`.

`citations-index.yml` schema (Research mode only):

```yaml
citations:
  - kind: "memory"            # one of: memory | file | web | chat | child
    ref: "agent-harness-orchestration-patterns"
    cited_by:
      - "branch-1-depth-1-sub-0-{slug}-{ts}.md"
      - "branch-2-depth-2-sub-1-{slug}-{ts}.md"
    note: "Patterns for parent-child handoff in async agent trees"
```

**Validation rule (Research mode, parent enforces during Phase F)**: When a parent reads a child file, it MUST verify:

- The child has a non-empty `## Citations` section
- Every numbered/bracketed inline citation marker resolves to an entry in the citations section

If the citation check fails, the parent **deletes the child file and respawns the child** with an explicit instruction to add citations. After 2 retries, the parent records a `## Citation failure` block in its own file naming the offending child and proceeds with the remaining citations intact.

**Validation rule (Quick mode)**: parents log warnings for missing or unresolvable citations and proceed (no respawn). The eventual report's executive summary must include a "Citation gaps" callout listing every uncited finding when this happens.

### Peer review file (Research mode only)

Filename pattern: `branch-{N}-peer-review-{branchSlug}-{yyyymmddHHMMSS}.md`

Frontmatter and required sections:

```markdown
---
peer_review_for_branch: {N}
reviewer_agent: "branch-{N} peer reviewer"
reviewed_branches: [1, 2, 3]
timestamp_utc: "{yyyymmddHHMMSS}"
---

## Reinforcements
{points where this branch's findings independently reinforce a sibling — cite both}

## Contradictions
{points where this branch contradicts a sibling — cite both, propose which is more strongly supported}

## Gaps
{aspects a sibling could have explored but didn't, given what this branch discovered — cite the discovery that revealed the gap}

## New Evidence
{any new sources this peer reviewer surfaces while comparing branches}

## Citations
{full citation list — sources from this branch, sources from siblings being reviewed, and any new sources}
```

### Quick vs Research differences (summary table for the agent file)

```markdown
| Aspect | Research (default) | Quick (`--quick`) |
|--------|--------------------|--------------------|
| Recursion order | Depth-first within each branch (parent finishes research before deriving children) | Pre-derived: parent derives all 3 child subfocuses upfront, no prior research required |
| Facet uniqueness | Global via `facet-registry.yml` + lock | Local sibling-aware only (read `facets.md` to avoid sibling overlap) |
| Citations | Mandatory; inline markers + `## Citations` section validated strictly by parent (offending children re-spawned, see retry rule) | Mandatory; inline markers + `## Citations` section required, but parent validates best-effort and surfaces gaps as warnings rather than re-spawning |
| Bottom-up incorporation | Parent **rewrites** its own file to weave in children | Parent appends `## Child Insights` section aggregating children |
| Peer review | Dedicated peer-review agents spawned post-branch-completion | None |
| Consolidation inputs | `branch-*` files + `branch-*-peer-review-*` files + `citations-index.yml` | `branch-*` files only |
| Coordination files | `facet-registry.yml`, `citations-index.yml`, `.facet-registry.lock/` | `facets.md` only |
```

### Subfocus narrowing example (Research mode, agent file)

```
Branch exploring "agent harness orchestration patterns":

- Depth 1 subfocus (registered by depth-0 manager):
  "Agent harness orchestration — how to coordinate multi-agent workflows with reliable state handoff"
- Depth 1 agent researches first, finds a memory [memory: file-coordination-vs-message-passing]
  saying file-based handoff outperforms message-passing for crash recovery — this finding
  motivates depth-2 subfocus 1.
  - Depth 2 subfocus 1 (registered by depth-1 agent after research):
    "What concrete file-based handoff schemas survive partial-failure restart in production agent systems?"
  - Depth 2 subfocus 2: "How should harnesses bound recursion depth and total agent count to prevent runaway fan-out?"
  - Depth 2 subfocus 3: "What observability surfaces let a parent detect a stuck child without polling JSONL transcripts?"
- Depth 2 subfocus 1 agent researches, finds two competing schema patterns — this motivates depth-3:
  - Depth 3 subfocus 1: "Idempotency requirements for the write-then-rename pattern under filesystem-level retries"
  - Depth 3 subfocus 2: "Frontmatter completeness checks the parent must run before treating a child file as final"
  - Depth 3 subfocus 3: "Trade-off between fsync cost and crash-window size for incremental status writes"

Each lower depth's subfocuses are derived FROM THE ACTUAL RESEARCH OUTPUT of the level above,
not pre-planned by the depth-0 manager.
```

### Design principles (agent file Meditate Mode section)

Add this list at the end of the Meditate Mode section:

```markdown
- **File-based coordination**: Never poll JSONL transcripts or rely on in-context returns. All inter-agent communication flows through files in the working directory.
- **3-way fan-out at every level**: Each agent eventually produces 3 child subfocuses (Research: after research; Quick: upfront). Depth 0 → 3 branches, each branch → 3 depth-2 agents, each → 3 depth-3 agents (up to 39 leaf files plus aggregations).
- **Predictable paths, self-describing files**: Every agent knows the exact `branch-{N}-depth-{D}-sub-{S}-` prefix it (and its children) will use, while the trailing `{slug}-{yyyymmddHHMMSS}.md` segment makes each file self-describing on disk and unique even on rapid re-runs.
- **Research-mode-only**: serial depth-first recursion, global facet uniqueness via registry+lock, mandatory citations validated strictly, bottom-up rewrite incorporation, dedicated peer-review pass, parent enforces citation validation on child files.
- **Quick-mode-only**: parallel fan-out per node, sibling-aware uniqueness, append-style aggregation, no peer review.
- **Open-minded**: Cast a wide net across memories, code, and (if applicable) web sources. Unexpected connections are the goal.
- **Concise outputs**: Each agent writes a focused summary, not a wall of text. The parent aggregates (Quick) or rewrites incorporating children (Research), never duplicates.
```

(Subsequent subtasks add more design principles to this list — preserve them when you apply this subtask.)

## Testing Strategy

- After applying, walk the entire Meditate Mode section of the agent file from top to bottom; confirm every Phase / Step / sub-protocol is reachable from the entry point and references existing later sections.
- Spot-check that every `branch-*` filename in either file uses the `subtask 01` convention.
- Run the linter on both files.

## Execution Notes

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
[Agent adds notes here during execution]

### Blockers Encountered
[Any blockers or issues]

### Files Modified
- `.cursor/commands/crux-meditate.md`
- `.cursor/agents/crux-cursor-memory-manager.md`
