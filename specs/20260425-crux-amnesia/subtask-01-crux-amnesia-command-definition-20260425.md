# Subtask: Command File Definition

## Metadata
- **Subtask ID**: 01
- **Feature**: crux-amnesia
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260425

## Objective
Define the `/crux-amnesia` command at `.cursor/commands/crux-amnesia.md` as a session-scoped toggle that suppresses ambient CRUX memory usage. Unlike other memory commands, amnesia must NOT spawn the `crux-cursor-memory-manager` subagent — it operates directly in the parent agent's context.

## Deliverables Checklist
- [x] Command file exists at `.cursor/commands/crux-amnesia.md`
- [x] Title and description clearly state session-scoped behavior
- [x] Usage section documents all four invocation modes: toggle, `on`, `off`, `status`
- [x] "What Amnesia ON Means" section lists all six suppressed behaviors (discovery, loading, annotation, reference tracking, dream nudges, subagent inheritance)
- [x] "What Amnesia OFF Means" section describes return to config-driven behavior
- [x] Explicit memory commands listed as exceptions: `/crux-dream`, `/crux-recall`, `/crux-forget`, `/crux-remember`, `/crux-meditate`
- [x] Response format section specifies the four status fields
- [x] Related section cross-references all five sibling memory commands
- [x] No reference to spawning `crux-cursor-memory-manager`
- [x] Explicit prohibition on modifying `.crux/crux-memories.json`, memory files, trackers, or the memory index

## Definition of Done
- [x] File exists at `.cursor/commands/crux-amnesia.md`
- [x] All four invocation modes documented (toggle, on, off, status)
- [x] All six suppressed behaviors enumerated
- [x] All five explicit memory commands listed as exceptions
- [x] No agent spawn directive present
- [x] Persistent state modification explicitly prohibited
- [x] No linter errors

## Implementation Notes
- The command file is a markdown document that serves as a system prompt extension when the user types `/crux-amnesia`
- The key architectural decision: amnesia is handled by the parent agent directly, not delegated to the memory manager agent. This keeps the toggle lightweight and avoids unnecessary agent spawning overhead
- The six suppressed behaviors map directly to the `Φ.enabled` behaviors in the memories integration rule
- The exceptions list ensures that explicit user intent always takes precedence over the session override
- The `status` mode allows the user to check the current state without toggling

## Testing Strategy
- Verify file exists at the expected path
- Verify all four invocation modes are documented
- Grep for all five exception commands (`/crux-dream`, `/crux-recall`, `/crux-forget`, `/crux-remember`, `/crux-meditate`)
- Verify no reference to spawning a subagent or memory manager
- Verify explicit prohibition on modifying persistent state

## Execution Notes

### Reverse-Engineered From
- `.cursor/commands/crux-amnesia.md` (current state as of 20260425)

### Key Implementation Details
1. The command file is 64 lines covering usage, argument handling, amnesia-on behavior, amnesia-off behavior, response format, and related commands
2. The six suppressed behaviors are listed as a numbered list under "What Amnesia ON Means"
3. The exceptions clause uses the phrasing "direct user intent to interact with the memory system"
4. The response format specifies four fields: session memory mode, scope, subagents, repo config
5. The Related section lists all five sibling commands with brief descriptions and the word "intentionally" to contrast with amnesia's ambient suppression

### Files Covered
- `.cursor/commands/crux-amnesia.md`
