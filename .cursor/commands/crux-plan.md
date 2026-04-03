# crux-plan

Generate structured engineering plans for complex features and multi-step initiatives.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-plan                           - Start interactive planning (guided questions)
/crux-plan @docs/crux-memories.md    - Plan implementation from a design doc
/crux-plan "add memory system"       - Plan a feature by description
```

## Instructions

When this command is invoked, spawn a `crux-planner` subagent to create an engineering plan. The planner uses the `crux-create-plan` skill to guide the workflow.

### Argument Handling

- **No arguments**: Start the guided planning workflow — the planner asks clarifying questions to understand scope before creating a plan
- **File reference(s)**: The planner reads the referenced file(s) as design docs / specs and uses them as the basis for the plan. It may still ask clarifying questions
- **Text description**: The planner uses the description as the feature scope. Pass `$ARGUMENTS` to the subagent as the feature description

### What Happens

1. The planner gathers requirements (questions or from the referenced doc)
2. Explores the codebase to understand existing patterns and potential conflicts
3. Proposes key decisions for user confirmation
4. Creates plan files in `plans/[yyyymmdd]-[feature-name]/`:
   - `plan-[feature-name]-[yyyymmdd].md` — coordination index with dependency graph, phases, and DoD
   - `subtask-NN-[feature]-[name]-[yyyymmdd].md` — one per subtask with objectives, deliverables, and agent assignments
5. Presents the plan summary for user review
6. Sets plan status to `Ready for Review`

### After Planning

Once a plan is created:
- Run `/crux-judge` to get an independent assessment of the plan's quality and feasibility
- Run `/crux-execute` to begin guided execution of the plan

## Plan Output Structure

```
plans/
└── 20260403-memory-system/
    ├── plan-memory-system-20260403.md
    ├── subtask-01-memory-system-foundation-20260403.md
    ├── subtask-02-memory-system-skills-20260403.md
    ├── subtask-03-memory-system-agent-20260403.md
    └── ...
```

## Related

- `crux-planner` agent — The specialist that creates and manages plans
- `crux-create-plan` skill — The guided planning workflow
- `/crux-judge` — Assess a plan before execution
- `/crux-execute` — Execute a plan with guided coordination
