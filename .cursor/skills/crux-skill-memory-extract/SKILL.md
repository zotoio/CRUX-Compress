---
name: crux-skill-memory-extract
description: Analyse execution artifacts from completed units of work, compare with existing memories, detect conflicts, and propose ranked candidate facts for memory creation. Use after a spec (or configured unitOfWork) completes to extract learnings, patterns, red flags, ideas, and goals.
---

# CRUX Skill: Memory Extract

Analyses execution artifacts from a completed unit of work, compares candidates against existing memories for novelty and conflicts, and presents ranked candidate facts for the user to accept, modify, or reject.

## When to Use

Use this skill when:
- A unit of work (e.g. spec) has completed execution and you want to extract memories from it
- The `/crux-dream` command is invoked for a specific completed work item
- The `crux-cursor-memory-manager` agent orchestrates a dream workflow

## Prerequisites

Before any operation:

1. **Read config**: Load `.crux/crux-memories.json` and extract:
   - `flags.enableMemories` — must be `"true"` or abort with message
   - `cruxMemories.unitOfWork` — the type of work item (e.g. `spec`, `task`)
   - `cruxMemories.dream.maxCandidateFacts` — max candidates to present (default `5`)
   - `cruxMemories.dream.maxUnrelatedChanges` — threshold for aborting on noisy diffs (default `50`)
   - `cruxMemories.dream.stateFile` — execution state filename (default `_execution-state.yml`)
   - `cruxMemories.dream.workDir` — directory containing units of work (default `specs`)
   - `cruxMemories.storage.memoriesDir` — base memory directory (default `memories`)
   - `cruxMemories.storage.agentMemoriesDir` — agent-scoped memory directory (default `memories/agents`)
   - `cruxMemories.typePriority` — valid types in priority order
2. **Guard check**: If `flags.enableMemories` is not `"true"`, refuse all operations and inform the caller that memories are disabled

## Operations

### 1. Verify Execution

Confirm the unit of work completed successfully before extracting memories.

**Input**: Path to the work item directory (e.g. `specs/20260403-crux-memories/`)

**Steps**:

1. Look for the configured `stateFile` (default `_execution-state.yml`) inside the work item directory
2. Parse the state file and check the `status` field
3. If status is not `complete` (or equivalent success state), report the current status and abort extraction — incomplete work items should not produce memories
4. If no state file exists, warn the user and ask whether to proceed anyway (the work item may have been executed outside the standard workflow)
5. Record the execution start date from the state file for use in diff analysis

### 2. Diff Analysis

Assess the scope of repository changes since the work item started to determine if extraction is meaningful.

**Steps**:

1. Determine the change boundary:
   - If the state file contains a start commit hash or timestamp, use it as the diff baseline
   - Otherwise, use the work item directory's creation date or earliest file modification as an approximation
2. Count the number of changed files in the repository since the baseline
3. Compare the count against `maxUnrelatedChanges` (default `50`)
4. If the count exceeds the threshold:
   - Warn the user: "Found {count} changed files since {unitOfWork} start (threshold: {maxUnrelatedChanges}). Many changes may be unrelated to this {unitOfWork}, which could reduce extraction quality."
   - Present options: proceed anyway, increase threshold, or abort
5. If within threshold, report the count and continue

The purpose of this check is to avoid extracting noise from unrelated work that happened concurrently.

### 3. Analyse Artifacts

Read all available execution artifacts and identify candidate facts.

**Artifacts to examine** (in the work item directory):

| Artifact | What to look for |
|----------|-----------------|
| Spec document | Goals, requirements, constraints, architectural decisions |
| Subtask files | Individual task outcomes, blockers encountered, workarounds applied |
| Execution state file | Completion status per subtask, timing, error counts |
| Dream summaries (prior) | Previously extracted memories from this or related work items — avoid duplicating |
| Agent work logs | Patterns agents discovered, red flags encountered, techniques that worked or failed |
| Code changes (diff) | New patterns introduced, anti-patterns fixed, performance improvements measured |

**What to extract**:

- Learnings: techniques, approaches, or insights that worked
- Red flags: bugs, anti-patterns, pitfalls, or mistakes discovered
- Goals: performance targets achieved or set, quality metrics established
- Ideas: speculative improvements, future work, or experiments suggested
- Core patterns: fundamental approaches that should always be followed

**Extraction heuristics**:

- Look for explicit statements of insight ("we learned that...", "this approach worked because...", "avoid doing X because...")
- Look for measurable outcomes (performance numbers, error rate changes, time savings)
- Look for recurring patterns across subtasks (if multiple subtasks hit the same issue, it is likely a strong candidate)
- Look for workarounds or non-obvious solutions (these often make the best memories)
- Look for agent-identified recommendations in work logs
- Ignore trivial or mechanical observations (e.g. "we created a file" or "we ran tests")

### 4. Compare with Existing Memories

Load existing memories and filter candidates for novelty.

**Steps**:

1. Scan configured `memoriesDir` and `agentMemoriesDir` recursively for all `*.memory.md` and `*.memory.crux.md` files
2. Read the frontmatter of each existing memory (title, description, type, tags)
3. For each candidate fact from step 3, compare against existing memories:
   - **Exact duplicate**: A memory with the same core insight already exists → discard the candidate
   - **Near duplicate**: A memory covers a very similar topic but with different details → flag for potential merge or update rather than creating a new memory
   - **Related but distinct**: Existing memories touch the same domain but this candidate adds genuinely new information → keep the candidate, note the related memories
   - **Novel**: No existing memory covers this territory → keep the candidate
4. Remove exact duplicates from the candidate list
5. Annotate near-duplicates with the existing memory they overlap and a suggested action (merge, update, or keep both)

### 5. Conflict Detection

Identify candidates that contradict existing memories.

**Steps**:

1. For each remaining candidate, check whether it directly contradicts an existing memory. Contradiction means the candidate and existing memory give opposing guidance on the same topic. Examples:
   - Candidate says "always use approach X" while existing memory says "avoid approach X"
   - Candidate reports a pattern works well while existing memory flags the same pattern as a red flag
   - Candidate sets a performance target that conflicts with an existing goal
2. For each detected conflict, prepare a conflict report:

```
⚠️ Conflict detected:

  Candidate: [candidate title]
  [candidate description]

  Conflicts with existing memory:
  File: [path to existing memory]
  Title: [existing memory title]
  [existing memory description]

  Resolution options:
  1. Keep existing — discard the candidate
  2. Replace — update the existing memory with the candidate's insight
  3. Merge — combine both perspectives into a single memory
  4. Keep both — retain both with disambiguation notes explaining when each applies
```

3. Conflicts always require user input — they are never auto-resolved, even in `--yolo` mode

### 6. Classify Type

Assign each candidate a memory type based on content analysis.

**Classification heuristics**:

| Type | Indicators |
|------|-----------|
| `core` | Fundamental patterns, architectural invariants, rules that should always be followed. Language: "always", "never", "must", "fundamental" |
| `redflag` | Bugs found, anti-patterns identified, pitfalls discovered, mistakes made. Language: "avoid", "don't", "causes", "breaks", "bug", "anti-pattern" |
| `goal` | Performance targets (achieved or set), quality metrics, SLAs, acceptance criteria with numbers. Language: "target", "achieved", "benchmark", "metric" |
| `learning` | Techniques, approaches, insights, best practices discovered through execution. Language: "works well", "effective", "technique", "approach", "discovered" |
| `idea` | Speculative improvements, future work, experiments to try, optimisations to explore. Language: "could", "might", "explore", "consider", "future", "experiment" |

When classification is ambiguous, prefer the lower-priority type (e.g. prefer `learning` over `core`). The memory can be promoted later through strength and reference tracking.

Validate the assigned type against `typePriority` from config. Do not assign `archived` — that type is only set through the rebalance workflow.

### 7. Agent Scoping

Determine whether each candidate should be a base memory or an agent-scoped memory.

**Steps**:

1. Examine the work item's execution artifacts for agent identification:
   - Subtask assignments that name specific agents (e.g. "Assigned Subagent: code-reviewer")
   - Work logs from specific agent personas
   - Changes made by specific agent types
2. For each candidate, determine if the insight is agent-specific:
   - **Agent-specific**: The insight relates to a specific agent's domain (e.g. review patterns for a code-reviewer, test strategies for a test-generator). Mark for placement in `memories/agents/{agent-id}/{type}/`
   - **General-purpose**: The insight applies broadly regardless of which agent is working. Place in the base `memories/{type}/` directory
3. When in doubt, place in base — general-purpose learnings benefit all agents. Only scope to an agent when the memory is clearly specific to that agent's concerns
4. Record the target scope in the candidate metadata

### 8. Rank Candidates

Order candidates by estimated value and present the top N.

**Ranking criteria** (in priority order):

1. **Type priority**: Higher-priority types rank first (per `typePriority` config: `core` > `redflag` > `goal` > `learning` > `idea`)
2. **Measurability**: Candidates with quantitative evidence (performance numbers, error rates, time savings) rank higher than qualitative observations
3. **Recurrence**: Patterns that appeared multiple times across subtasks rank higher
4. **Actionability**: Insights that give clear, specific guidance rank higher than vague observations
5. **Novelty**: Candidates that cover genuinely new territory (no near-duplicates) rank higher

**Steps**:

1. Score each candidate using the criteria above
2. Sort by score descending
3. Take the top `maxCandidateFacts` candidates (default `5`)
4. If more candidates remain beyond the limit, note how many were excluded and offer to show them

### 9. Resolved Bug Detection

Identify existing `redflag` memories whose bugs or anti-patterns appear to have been fixed by the completed work.

**Steps**:

1. From the existing memories loaded in step 4, filter to those with `type: redflag`
2. For each redflag memory, compare its described bug/anti-pattern against:
   - **Code changes**: Does the diff show changes that directly address the issue described in the redflag? (e.g. the anti-pattern was refactored away, the bug-causing code was rewritten)
   - **Subtask outcomes**: Did any subtask explicitly mention fixing, resolving, or addressing this specific issue?
   - **Pattern removal**: Was the problematic pattern described by the redflag removed or replaced with the recommended approach?
3. Classify each redflag into one of:
   - **Likely resolved**: Strong evidence — the diff contains changes that directly fix the described bug or remove the anti-pattern, or a subtask explicitly states the issue was resolved
   - **Possibly resolved**: Partial evidence — related code was changed but it is not conclusive whether the specific issue was fully addressed
   - **Still active**: No evidence of resolution — skip, do not present to the user
4. Only present redflags classified as "likely resolved" or "possibly resolved"
5. For each, prepare a resolution report (see Resolved Bug Format below)

**Heuristics for matching redflags to changes**:

- Compare the redflag's tags against changed file paths and content (e.g. a redflag tagged `[testing, fixtures]` matching changes in test files)
- Check if the redflag's "Solution" or "Prevention" section describes an approach that now appears in the codebase
- Check if the specific file, function, or pattern named in the redflag body was modified
- When in doubt, classify as "possibly resolved" rather than "likely resolved" — the user makes the final call

## Resolved Bug Format

Each potentially-resolved redflag is presented with these fields:

```yaml
memory_path: "memories/redflag/example-bug.memory.md"
title: "Example bug title from the memory"
confidence: "likely"          # or "possibly"
evidence: "The diff shows refactoring of X to use the recommended approach described in this memory's Solution section."
recommendation: "forget"      # always "forget" — user decides
```

**Field descriptions**:

| Field | Required | Description |
|-------|----------|-------------|
| `memory_path` | Yes | Path to the existing redflag memory file |
| `title` | Yes | Title from the redflag memory's frontmatter |
| `confidence` | Yes | `"likely"` or `"possibly"` — how strong the evidence is that the bug was fixed |
| `evidence` | Yes | Specific evidence from the diff, subtask outcomes, or code changes that suggests the bug was resolved |
| `recommendation` | Yes | Always `"forget"` — resolved bugs should be deleted, but the user confirms |

## Candidate Fact Format

Each candidate is presented with these fields:

```yaml
rank: 1
type: "learning"
title: "React.memo on list items reduced re-render time from 480ms to 12ms"
description: "Wrapping list item components in React.memo with a custom comparator that checks item ID and version (not deep-equal) reduced re-render time by 97% on a 500-item list."
tags: [react, performance, rendering, memoization]
scope: "base"                    # or "agents/{agent-id}"
rationale: "Quantitative performance improvement discovered during component library subtask. Recurred across 3 subtasks involving list rendering."
conflicts: []                    # or list of conflict reports
related_memories: []             # existing memories on similar topics
source: "20260401-component-library"  # work item identifier
```

**Field descriptions**:

| Field | Required | Description |
|-------|----------|-------------|
| `rank` | Yes | Position in the ranked list (1 = highest value) |
| `type` | Yes | Assigned memory type (`core`, `redflag`, `goal`, `learning`, `idea`) |
| `title` | Yes | Instructive title conveying the key insight — should be actionable at a glance |
| `description` | Yes | Self-contained summary with enough detail to act on without additional context |
| `tags` | Yes | Lowercase tags for categorization and search |
| `scope` | Yes | Target scope: `"base"` or `"agents/{agent-id}"` |
| `rationale` | Yes | Why this candidate was selected — what evidence supports it and why it is valuable |
| `conflicts` | No | List of conflict reports if the candidate contradicts existing memories |
| `related_memories` | No | Paths to existing memories on similar topics (for near-duplicates or related content) |
| `source` | Yes | Identifier of the originating work item (slug from the work directory name) |

## Presentation to User

After ranking, present candidates to the user for review. If resolved bugs were detected (step 9), present them in a separate section after the new candidates:

```
Analysing {unitOfWork} "{work-item-id}"...
✅ Execution verified: {subtask-count} subtasks complete
📊 {change-count} repo changes since start (within threshold)

Comparing with {existing-count} existing memories...

Top {N} candidate facts:

  1. [{type}] {title}
     {description}
     Tags: {tags}
     Scope: {scope}
     Rationale: {rationale}

  2. [{type}] {title}
     ...

  {conflict reports, if any}

Accept all? Or review individually? [all/individual/skip]
```

If resolved bugs were detected:

```
🐛 Resolved bugs detected — {count} redflag memories may no longer be needed:

  1. [{confidence}] {title}
     File: {memory_path}
     Evidence: {evidence}

  2. [{confidence}] {title}
     ...

Forget all resolved bugs? Or review individually? [all/individual/skip]
```

Each resolved bug the user confirms is deleted via `crux-skill-memory-crud` Delete operation (memory file and its reference tracker are both removed).

In `--yolo` mode:
- Auto-accept all new candidates except those with conflicts (conflicts always require user input)
- Auto-forget redflags classified as "likely" resolved
- Present "possibly" resolved redflags for user confirmation (insufficient confidence for auto-deletion)

## Integration

| Component | Location | Role |
|-----------|----------|------|
| Memory CRUD | `.cursor/skills/crux-skill-memory-crud/SKILL.md` | Actual memory file creation after user accepts candidates |
| Reference tracker | `.cursor/skills/crux-skill-memory-reference-tracker/SKILL.md` | Existing reference data used during comparison |
| Config | `.crux/crux-memories.json` | All dream config settings |
| Memory index | `.crux/memory-index.yml` | Quick lookup of existing memories for comparison |

After the user accepts candidates (all or individually), delegate to `crux-skill-memory-crud` for actual file creation. Pass the candidate's `type`, `title`, `description`, `tags`, `source`, and scope (agent-id if agent-scoped) directly to the CRUD skill's Create operation.

After the user confirms resolved bugs for deletion, delegate to `crux-skill-memory-crud` Delete operation. The memory file and its reference tracker are both removed.

## Config Reference

All config values come from `.crux/crux-memories.json`:

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `flags.enableMemories` | string | `"false"` | Feature gate — must be `"true"` to operate |
| `cruxMemories.unitOfWork` | string | `"spec"` | Type of work item to look for (e.g. `spec`, `task`) |
| `cruxMemories.dream.maxCandidateFacts` | integer | `5` | Maximum number of candidates to present |
| `cruxMemories.dream.maxUnrelatedChanges` | integer | `50` | Changed file count threshold before warning |
| `cruxMemories.dream.stateFile` | string | `"_execution-state.yml"` | Execution state filename within work item directory |
| `cruxMemories.dream.workDir` | string | `"specs"` | Directory containing units of work |
| `cruxMemories.storage.memoriesDir` | string | `"memories"` | Base memory directory |
| `cruxMemories.storage.agentMemoriesDir` | string | `"memories/agents"` | Agent-scoped memory directory |
| `cruxMemories.typePriority` | list | `[core, redflag, goal, learning, idea, archived]` | Valid types in priority order |

## Error Handling

| Condition | Action |
|-----------|--------|
| `enableMemories` is not `"true"` | Abort, inform caller memories are disabled |
| State file missing | Warn, ask user whether to proceed without execution verification |
| State file shows incomplete execution | Report status, abort extraction |
| Changed file count exceeds `maxUnrelatedChanges` | Warn, present options (proceed, adjust threshold, abort) |
| No artifacts found in work item directory | Report that no analyzable artifacts were found, abort |
| Zero candidates after comparison filtering | Report that all potential insights are already captured in existing memories |
| Conflict detected with existing memory | Present conflict report, require user resolution (never auto-resolve) |
| Config file missing or malformed | Report error with path and expected structure |

## What This Skill Does NOT Do

- Does not create memory files — delegates to `crux-skill-memory-crud` after user approval
- Does not delete memory files — proposes resolved bugs for user confirmation, delegates deletion to `crux-skill-memory-crud`
- Does not modify existing memories — only proposes new candidates, flags conflicts, or identifies resolved bugs for user resolution
- Does not handle REM sleep workflows (consolidation, promotion, demotion) — that is `crux-skill-memory-rebalance`
- Does not compress memories — that is `crux-skill-memory-compress`
- Does not build the memory index — that is `crux-skill-memory-index`
- Does not write dream summaries — that is the orchestrating agent's responsibility
- Does not archive work item directories — that is the orchestrating agent's responsibility
