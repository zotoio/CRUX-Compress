---
name: crux-create-plan
description: Guided workflow for creating engineering plans. Gathers requirements, explores the codebase, proposes a plan structure, and generates plan files in plans/. Use when planning a new feature, refactor, or multi-step initiative before implementation.
---

# CRUX Create Plan

Guided workflow for creating structured engineering plans in the CRUX-Compress project.

## When to Use

Use this skill when the user wants to plan a new feature, refactor, or multi-step initiative **before** writing code. The output is a set of plan files in `plans/` that can later be executed via the `crux-execute-plan` skill.

## Workflow

### Step 1: Gather Requirements

Ask the user clarifying questions to understand the scope. Ask one question at a time, up to 10 questions maximum. Stop asking when you have enough context to proceed.

Good questions to consider:
- What is the high-level goal?
- Are there specific files, directories, or subsystems involved?
- Are there constraints or non-goals?
- What does success look like?
- Is there a design doc or spec to reference? (e.g. in `docs/`)
- Should this work across platforms or is it Cursor-only?
- What testing strategy is expected?

### Step 2: Explore the Codebase

Before proposing a plan, understand what exists. Spawn an `explore` subagent to:

- Identify files and directories relevant to the feature
- Understand existing patterns (agents, skills, commands, hooks, tests)
- Find potential conflicts or dependencies with existing code
- Note conventions to follow (frontmatter format, file naming, directory structure)

### Step 3: Propose Key Decisions

Present the user with key architectural or structural decisions that affect the plan. Wait for confirmation before proceeding.

Format:

```
## Key Decisions

1. **[Decision]**: [Option A] vs [Option B]
   - Recommendation: [Your recommendation and why]

2. **[Decision]**: [Option A] vs [Option B]
   - Recommendation: [Your recommendation and why]
```

### Step 4: Determine Dependencies and Sequencing

Before creating any files, build the dependency graph:

1. **Identify all subtasks** and their inputs/outputs
2. **Map dependencies**: If subtask B requires output from subtask A, B depends on A
3. **Assign IDs in dependency order**: Lower IDs never depend on higher IDs. If subtask A must finish before B, A gets a lower ID than B
4. **Group into phases**: Subtasks with no unresolved dependencies form a phase. Within a phase, tasks can run in parallel. A new phase starts when all prior-phase tasks are complete
5. **Validate**: No circular dependencies. Every dependency target exists. No subtask depends on a higher-numbered subtask

### Step 5: Assign Subagents

For each subtask, assign the most appropriate subagent based on the work type:

| Work Type | Recommended Subagent |
|-----------|---------------------|
| Implementation (new files, features) | `generalPurpose` |
| Codebase exploration, research | `explore` |
| Command execution, git, test runs | `shell` |
| CRUX compression or validation | `crux-cursor-rule-manager` |
| Code quality audit, final review | `integrity-expert` |
| Documentation updates | `docs-sync-agent` |
| Memory system work | `crux-cursor-memory-manager` |

The assigned subagent must be recorded in both the index Subtask Manifest and the subtask file's Metadata section.

### Step 6: Create Plan Files

After dependencies and agents are determined, create the plan directory and files:

1. **Create directory**: `plans/[yyyymmdd]-[feature-name]/`
2. **Write index file**: `plan-[feature-name]-[yyyymmdd].md` with:
   - Status: `Draft`
   - Overview, key decisions, requirements
   - **Subtask Manifest** — complete table linking every subtask ID to its file, assigned subagent, dependencies, and phase
   - Subtask dependency graph (mermaid) — must match the manifest exactly
   - Execution order by phase — derived from the dependency graph
   - Definition of Done checklist
3. **Write subtask files**: One per subtask, following the subtask template from the `crux-planner` agent definition. Each file's Metadata section must include the assigned subagent and dependency list matching the index manifest

### Step 7: Review and Finalize

Present the complete plan to the user for review:

```
## Plan Summary

- **Feature**: [name]
- **Subtasks**: [count]
- **Phases**: [count]
- **Estimated complexity**: [Low / Medium / High]

### Subtask Manifest
| ID | File | Subagent | Dependencies | Phase |
|----|------|----------|-------------|-------|
| 01 | subtask-01-...-yyyymmdd.md | generalPurpose | — | 1 |
| 02 | subtask-02-...-yyyymmdd.md | generalPurpose | — | 1 |
| 03 | subtask-03-...-yyyymmdd.md | generalPurpose | 01, 02 | 2 |
| 04 | subtask-04-...-yyyymmdd.md | integrity-expert | 03 | 3 |

Ready to proceed? [Yes / Modify / Cancel]
```

After user approval, update the plan status from `Draft` to `Ready for Review`.

## Conventions

- Plan directory names: `[yyyymmdd]-[feature-name]` (lowercase, hyphens)
- Index file: `plan-[feature-name]-[yyyymmdd].md`
- Subtask files: `subtask-[NN]-[feature]-[subtask-name]-[yyyymmdd].md`
- Assessment files: `assessment-[feature-name]-[yyyymmdd].md` (from `/crux-judge`)
- Execution reports: `execution-report-[feature-name]-[yyyymmdd].md` (from `/crux-execute`)
- All dates use `YYYYMMDD` format
- Subtask IDs are zero-padded two-digit numbers (`01`, `02`, ... `99`)

## What NOT to Do

- Do not create or modify any code files — only plan markdown files
- Do not create files outside `plans/`
- Do not execute the plan — that is the `crux-execute-plan` skill's job
- Do not create knowledge or memory files from plans
- Do not skip the user confirmation step before finalizing
