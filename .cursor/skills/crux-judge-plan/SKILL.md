---
name: crux-judge-plan
description: Independent assessment of the repository or engineering plans. Reviews quality, feasibility, completeness, risk, and structure. Use to audit the repo or to assess a plan before execution.
---

# CRUX Judge Plan

Independent assessment workflow for the repository or individual engineering plans. Provides a structured review with scores, findings, and actionable recommendations. The judge should ideally run in a **fresh agent context** to avoid bias from prior sessions.

## When to Use

- **No target specified**: Assess the entire repository — write report to `plans/assessment-repo-[yyyymmdd].md`
- **Plan path specified**: Assess a specific plan — write report to that plan's directory as `assessment-[feature-name]-[yyyymmdd].md`

## Assessment Dimensions

The judge evaluates plans across six dimensions, each scored 1-5:

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| **Completeness** | 25% | All requirements covered, no gaps in deliverables, DoD is thorough |
| **Feasibility** | 20% | Subtasks are achievable, scope is realistic, no impossible demands |
| **Structure** | 20% | Dependencies are correct, phases are logical, no circular deps |
| **Specificity** | 15% | Subtasks have clear objectives, deliverables are concrete and verifiable |
| **Risk Awareness** | 10% | Edge cases considered, potential blockers identified, rollback possible |
| **Convention Compliance** | 10% | Follows repo patterns (agent/skill/command/test conventions) |

### Scoring

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | Excellent | No issues found |
| 4 | Good | Minor improvements possible |
| 3 | Adequate | Some gaps but executable |
| 2 | Needs Work | Significant issues — revise before executing |
| 1 | Deficient | Major problems — plan should be reworked |

**Overall verdict** is the weighted average:
- **4.0+**: Approve — ready for execution
- **3.0–3.9**: Conditional — address findings before executing
- **< 3.0**: Reject — plan needs rework via `/crux-plan`

## Workflow: Repository Assessment (no target)

### Step 1: Explore Codebase

Spawn an `explore` subagent for a thorough survey:
- Full directory structure (agents, skills, commands, hooks, tests, scripts, config)
- All wiring files (`.cursor/hooks.json`, config JSON files, `AGENTS.md`)
- Test coverage — which components have tests, which do not
- Documentation state (README.md, CONTRIBUTORS.md, AGENTS.md)

### Step 2: Run Integrity Checks

Spawn `integrity-expert` to perform automated checks:
- Shell script quality (shellcheck, error handling)
- CRUX synchronization (sourceChecksum freshness)
- CI/CD workflow validity
- Configuration consistency

### Step 3: Evaluate Dimensions (repo-adapted)

Apply the six dimensions to the repository as a whole:
- **Completeness**: Are all agents, skills, commands properly wired? Orphaned or missing files?
- **Feasibility**: Is the architecture sustainable? Scaling concerns?
- **Structure**: Are directory conventions consistent? Are component dependencies clear?
- **Specificity**: Are agent/skill/command definitions concrete with clear responsibilities?
- **Risk Awareness**: Security concerns, untested code paths, missing error handling?
- **Convention Compliance**: Do all files follow established patterns (frontmatter, naming, testing)?

### Step 4: Generate Report

Write `plans/assessment-repo-[yyyymmdd].md` with scores, findings, and recommendations.

---

## Workflow: Plan Assessment (with target)

### Step 1: Load Plan

1. Read the plan index file and all subtask files
2. Read any referenced design docs or specs (from the plan's overview/requirements)
3. Build a mental model of the full initiative

### Step 2: Explore Context

Spawn an `explore` subagent to verify:
- Referenced files and directories actually exist
- Existing patterns match what the plan assumes
- No obvious conflicts with current codebase state

### Step 3: Evaluate Each Dimension

For each dimension, produce:
- A score (1-5)
- Specific findings (what's good, what's missing)
- Recommendations (actionable fixes if score < 5)

### Step 4: Validate Subtask Manifest

The Subtask Manifest in the index is the source of truth. For each row, verify:
- [ ] The listed file exists in the plan directory
- [ ] The subtask file's Metadata (Assigned Subagent, Dependencies) matches the manifest row
- [ ] The assigned subagent is appropriate for the work type (e.g. `integrity-expert` for audits, `generalPurpose` for implementation)
- [ ] No subtask depends on a higher-numbered subtask ID
- [ ] Phase assignments are consistent with dependencies (a subtask's phase must be higher than all its dependencies' phases)

### Step 5: Check Subtask Quality

For each subtask file, verify:
- [ ] Has clear, single-responsibility objective
- [ ] Deliverables checklist is concrete (not vague)
- [ ] Assigned subagent matches the work type
- [ ] Dependencies are correct (no missing or circular deps)
- [ ] Implementation notes provide enough guidance for the executing agent
- [ ] Testing strategy is defined
- [ ] No subtask is doing too much (should be decomposed further if > 5 deliverables)

### Step 6: Dependency Graph Audit

- Verify the mermaid graph matches the Subtask Manifest exactly (same edges, same nodes)
- Check for missing edges (subtask B uses output of subtask A but doesn't declare dependency in manifest)
- Check for unnecessary sequential constraints (tasks that could run in parallel but are in separate phases)
- Verify phase assignments align with dependency ordering
- Confirm subtask IDs are numbered in dependency order (lower IDs have no deps on higher IDs)

### Step 7: Risk Analysis

Identify:
- **Blocking risks**: Single points of failure, hard external dependencies
- **Scope risks**: Subtasks that are too large or vaguely defined
- **Integration risks**: Phases where many subtasks merge and could conflict
- **Convention risks**: Deviations from existing repo patterns

### Step 8: Generate Report

Write `assessment-[feature-name]-[yyyymmdd].md` to the plan's own directory.

## Report Format

### Report Location

| Mode | Output File |
|------|------------|
| Repo assessment | `plans/assessment-repo-[yyyymmdd].md` |
| Plan assessment | `plans/[plan-directory]/assessment-[feature-name]-[yyyymmdd].md` |

### Template

```markdown
# [Repo Assessment | Plan Assessment: [Feature Name]]

**Target**: `[repository root | plans/[directory]/plan-[name]-[yyyymmdd].md]`
**Assessed**: [YYYY-MM-DD]
**Verdict**: Approve | Conditional | Reject

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | X/5 | [brief note] |
| Feasibility | X/5 | [brief note] |
| Structure | X/5 | [brief note] |
| Specificity | X/5 | [brief note] |
| Risk Awareness | X/5 | [brief note] |
| Convention Compliance | X/5 | [brief note] |
| **Overall** | **X.X/5** | **[verdict]** |

## Findings

### Strengths
- [What the plan does well]

### Issues
| # | Severity | Subtask | Finding | Recommendation |
|---|----------|---------|---------|----------------|
| 1 | HIGH | 03 | Missing dependency on subtask 01 | Add dependency |
| 2 | MEDIUM | 05 | Vague deliverable "update tests" | Specify which test files |
| 3 | LOW | — | No rollback plan | Add rollback notes to index |

### Dependency Graph
- [Any issues with the graph]
- [Suggestions for parallelism improvements]

### Risk Summary
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [risk] | Low/Med/High | Low/Med/High | [suggestion] |

## Recommendation

[1-3 sentences: overall assessment and what to do next]
```

## What NOT to Do

- Do not modify the plan files — the judge is read-only
- Do not execute any subtasks — assessment only
- Do not modify code files
- Do not skip dimensions — score all six even if they look fine
- Do not rubber-stamp — provide genuine critical analysis
