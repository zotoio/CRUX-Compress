---
name: crux-execute-plan
description: Executes an engineering plan by spawning subagents for each subtask, tracking progress, and verifying completion. Use when a plan exists in plans/ and is ready for execution.
---

# CRUX Execute Plan

Executes an existing engineering plan by coordinating subagents, tracking progress, and verifying completion.

## When to Use

Use this skill when a plan exists in `plans/` with status `Ready for Review` (or the user explicitly requests execution of a `Draft` plan). The plan must have been created by the `crux-create-plan` skill or follow the same file format.

## Workflow

### Step 1: Load Plan and Validate Manifest

1. Read the plan index file (`plan-[feature-name]-[yyyymmdd].md`)
2. Parse the **Subtask Manifest** table — this is the source of truth for subtask-to-agent mapping and dependency ordering
3. For each row in the manifest:
   - Verify the subtask file exists at the listed path
   - Read the subtask file and confirm its Metadata section matches the manifest (same subagent, same dependencies)
   - Confirm no subtask depends on a higher-numbered subtask ID
4. Build the execution order from the manifest's Phase column
5. If any inconsistencies are found (missing files, mismatched agents, dependency violations), report them and stop

### Step 2: Confirm Execution

Present the manifest as the execution summary and wait for user approval:

```
## Execution Summary

- **Plan**: [feature name]
- **Subtasks**: [total count]
- **Phases**: [phase count]

### Subtask Manifest
| ID | File | Subagent | Dependencies | Phase |
|----|------|----------|-------------|-------|
| 01 | subtask-01-...-yyyymmdd.md | generalPurpose | — | 1 |
| 02 | subtask-02-...-yyyymmdd.md | generalPurpose | — | 1 |
| 03 | subtask-03-...-yyyymmdd.md | generalPurpose | 01, 02 | 2 |
| 04 | subtask-04-...-yyyymmdd.md | integrity-expert | 03 | 3 |

Proceed with execution? [Yes / No]
```

### Step 3: Execute Subtasks

For each phase in order:

1. **Spawn the subagent listed in the manifest** for each subtask in the current phase (up to 4 in parallel). The subagent type comes from the manifest's Subagent column — do not override or reassign. The manifest is the single source of truth for agent assignment
2. **Provide each subagent** with:
   - The full subtask file content (read from the File column path)
   - Any relevant context from the plan index (key decisions, requirements)
   - **Explicit instructions to update the subtask file as work progresses** (see checklist tracking below)
   - Instructions to record files modified and any blockers in Execution Notes
3. **Wait for all phase subtasks** to complete before starting the next phase

**Checklist Tracking (executing agent)**: Each executing subagent MUST update the subtask file in real-time:
- **Deliverables Checklist**: Tick `- [ ]` → `- [x]` for each item **as it is completed** — not all at once at the end. Each tick should correspond to a verifiable deliverable that now exists.
- **Definition of Done**: Tick each item as the condition is met (e.g., tick "No linter errors" after running lints and confirming clean).
- **Execution Notes**: Fill in Agent Session Info (agent type, start time), Work Log (what was done), and Files Modified (list of created/changed files).
- The orchestrator must verify the subtask file was updated by the executing agent before proceeding to verification.

### Step 4: Adversarial Verification (per subtask)

After each subtask's assigned agent completes, spawn a **fresh, separate `integrity-expert` subagent** to adversarially verify the work. This agent did not perform the subtask and has no bias toward its output.

For each completed subtask, the adversarial verifier must:

1. **Read the subtask file** — examine both the Deliverables Checklist and Definition of Done sections
2. **Reset all checkboxes**: Set every `- [x]` back to `- [ ]` in both the Deliverables Checklist and Definition of Done. The verifier starts from a clean slate — executing agent ticks are not trusted.
3. **Inspect every deliverable**: For each checklist item, verify the deliverable actually exists and is correct:
   - Files listed as created → verify they exist and have expected content
   - Code changes → verify they compile / pass linter checks (ReadLints on modified files)
   - Tests added → verify test files exist and are syntactically valid
   - Config changes → verify JSON/YAML is valid and references resolve
4. **Re-tick only verified items**: Update the subtask file's Deliverables Checklist and Definition of Done — only tick `- [x]` for items the verifier independently confirms are complete
5. **Flag failures**: If any deliverable is missing, incomplete, or incorrect, leave it unchecked and add a note in the subtask's Execution Notes explaining what is missing
6. **Report verdict**: Return one of:
   - **Verified** — all deliverables and DoD items confirmed, all checkboxes ticked
   - **Partial** — some items incomplete (list which remain unchecked)
   - **Failed** — critical deliverables missing

**The subtask file is the persistent audit trail** — after verification, its checkboxes reflect independently verified state, not self-reported state.

After adversarial verification:
- **Update the index manifest** Status column:
  - `Verified` → set status to `Done`
  - `Partial` → set status to `Partial` and report to user for decision (fix and re-verify, or accept)
  - `Failed` → set status to `Failed` and stop dependent subtasks
- Add verification notes to the Execution Notes section

**The adversarial verifier must be a different agent instance from the one that executed the subtask.** This ensures independent validation.

### Step 5: Final Verification

After all phases complete and all subtasks have been adversarially verified:

1. **Confirm all subtasks are `Done`**: Every row in the manifest must have status `Done`. If any are `Partial` or `Failed`, report and ask the user before proceeding
2. **Run tests**: Execute `./scripts/test.sh` via a `shell` subagent
3. **Check linter errors**: Run ReadLints on all files modified during execution
4. **Integrity audit**: Spawn `integrity-expert` to audit changed files (shell quality, CRUX sync, config consistency)
5. **Documentation sync**: Spawn `docs-sync-agent` if any trigger files (agents, skills, commands, hooks, scripts) were modified

### Step 6: Write Execution Report

Write a persistent execution report to the plan directory as `execution-report-[feature-name]-[yyyymmdd].md`. This is a durable record of the execution — not just a chat summary.

```markdown
# Execution Report: [Feature Name]

**Plan**: `plan-[feature-name]-[yyyymmdd].md`
**Executed**: [YYYY-MM-DD]
**Status**: Completed | Completed with exceptions

## Summary

[1-3 sentence overview of what was accomplished]

## Subtask Results

| ID | Subtask | Subagent | Verification | Files Modified | Notes |
|----|---------|----------|-------------|----------------|-------|
| 01 | [name] | generalPurpose | Verified | [count] | [brief note] |
| 02 | [name] | generalPurpose | Verified | [count] | [brief note] |
| 03 | [name] | integrity-expert | Verified | [count] | [brief note] |

## Verification Results

### Adversarial Verification
- Subtasks verified: [N/N]
- Issues found during verification: [count]
- Issues resolved: [count]

### Test Suite
- Status: [PASS / FAIL]
- Tests run: [count]
- [details if failures]

### Linter
- Status: [CLEAN / N errors]
- [details if errors]

### Integrity Audit
- Status: [PASS / WARN / FAIL]
- [findings if any]

### Documentation Sync
- Status: [Updated / No changes needed / Skipped]
- [files updated if any]

## Files Modified (all subtasks combined)

[Deduplicated list of all files created or modified across all subtasks]

## Outstanding Items

- [Any items requiring manual follow-up]

## Lessons Learned

[Optional: blockers encountered, unexpected issues, process improvements]
```

### Step 7: Final Review

Present the execution report to the user for approval:

```
Execution report written to: plans/[directory]/execution-report-[feature-name]-[yyyymmdd].md

All [N] subtasks verified. Tests: PASS. Linter: CLEAN.

Approve and mark plan as Completed? [Yes / No]
```

### Step 8: Mark Complete

After user approval:

1. Update the plan index status to `Completed`
2. Fill in final execution notes in the index
3. Report completion

## Execution Rules

### Dependency Management

- Never start a subtask before all its listed dependencies are complete
- If a dependency fails, stop and report — do not continue with dependent subtasks
- Independent subtasks within a phase may run in parallel

### Parallel Limits

- Maximum 4 subagents running simultaneously
- If a phase has more than 4 subtasks, batch them (4 at a time)
- Wait for each batch to complete before starting the next

### Error Handling

- If a subtask fails, update its status in the index and report to the user
- Ask the user how to proceed: retry, skip, or abort the plan
- Never silently skip a failed subtask

### Progress Updates

- Update the index file after each subtask completes (not just at the end)
- Include: subtask status, files modified, any blockers, time taken
- Keep the user informed between phases

### Testing During Execution

- Individual subtasks should only run targeted tests on files they modified
- The global test suite (`./scripts/test.sh`) runs only during the final verification phase
- This prevents test failures from parallel file modifications

## Resuming Execution

If execution is interrupted (e.g. session ends):

1. Read the plan index to determine which subtasks are complete
2. Identify the next incomplete subtask based on the dependency graph
3. Resume from that point — do not re-execute completed subtasks
4. Verify completed subtask deliverables still hold (files exist, no regressions)

## What NOT to Do

- Do not modify code files directly — only subagents modify code
- Do not skip the user confirmation step before starting execution
- Do not run the global test suite during parallel subtask execution
- Do not mark a subtask complete if any deliverable is missing
- Do not continue past a failed dependency without user approval
- Do not create knowledge or memory artifacts from plan execution
