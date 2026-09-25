---
description: Ensures engineering specs use CRUX-specific agents instead of generalPurpose
alwaysApply: false
---

# Spec Agent Allocation

When creating or executing engineering specs (`/zoto-spec-create`, `/zoto-spec-execute`) in this repository, assign subtasks to CRUX agents — never use `generalPurpose`.

## Allocation Rules

1. **Architecture, design, documentation, and eval strategy** → `crux-platform-architect`
2. **Code implementation, bug fixes, refactoring, writing evals/tests** → `crux-software-engineer`
3. **CRUX compression/decompression** → `crux-cursor-rule-manager`
4. **Memory lifecycle** → mode-scoped thin agents:
   - Dream extraction → `crux-memory-dream`
   - REM Sleep rebalance → `crux-memory-rem`
   - Recall / query / display (incl. `--total` Canvas) → `crux-memory-recall`
   - Ad-hoc create → `crux-memory-remember`
   - Delete → `crux-memory-forget`
5. **Code quality audits, security, CI/CD** → `integrity-expert`
6. **Documentation sync after source changes** → `docs-sync-agent`

## When Building Specs

During `/zoto-spec-create`, populate the `Assigned Subagent` field in each subtask with the appropriate CRUX agent name from the table above based on the subtask's nature.

## When Executing Specs

During `/zoto-spec-execute`, the executor must spawn the agent type specified in each subtask's metadata. If a subtask says `generalPurpose`, remap it to the correct CRUX agent before spawning.

## Rationale

CRUX agents carry domain-specific system prompts, repository conventions, and CRUX notation fluency that `generalPurpose` agents lack. Using them produces higher-quality output with fewer iterations.
