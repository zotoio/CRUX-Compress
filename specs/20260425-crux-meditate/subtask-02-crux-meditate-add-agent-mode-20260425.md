# Subtask: Add Meditate Mode to Agent Definition

## Metadata
- **Subtask ID**: 02
- **Feature**: crux-meditate
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: None
- **Created**: 20260425

## Objective
Add Meditate Mode to `.cursor/agents/crux-cursor-memory-manager.md` — a new operating mode that implements recursive memory-informed exploration through self-spawning agent inception. Also add "Meditate" to the agent's expertise bullets.

## Deliverables Checklist
- [x] Meditate Mode section added to `.cursor/agents/crux-cursor-memory-manager.md` under Operating Modes
- [x] Invocation variants table: no args, quoted text, file/folder refs, internal child invocation with `meditateDepth` and `meditateFacet`
- [x] Top-level workflow (depth 0): feature guard, derive facets, spawn 3 parallel explorers, consolidate, present, interactive continuation
- [x] Recursive exploration protocol (depths 1–2): query memories, expand, craft queries, recurse, aggregate
- [x] Depth 3 base case: query, expand, craft queries, return (no further recursion)
- [x] Design principles: light and quick, open-minded, concise returns
- [x] "Meditate" added to Your Expertise bullets
- [x] Agent description in frontmatter unchanged (already covers the scope)

## Definition of Done
- [x] Meditate Mode section exists in the agent definition
- [x] Self-recursive pattern documented: `crux-cursor-memory-manager` spawns child `crux-cursor-memory-manager` instances
- [x] Recursion parameters documented: `meditateDepth`, `meditateFacet`, `maxDepth`, `parentContext`
- [x] Interactive continuation via `AskQuestion` documented with multi-select options
- [x] No linter errors

## Implementation Notes
- **Key architectural decision**: Use the same agent type for both orchestrator and recursive children. The `meditateDepth` and `meditateFacet` parameters control recursion behavior rather than introducing separate agent definitions. This works because the memory manager already has all the skills needed (memory index, CRUD, search).
- The Meditate Mode section should follow the existing pattern of other modes (Dream, REM Sleep, Recall, Remember, Forget) with invocation variants table, numbered workflow steps, and clear behavioral descriptions
- The recursive exploration protocol is an inner section describing child agent behavior at depths 1–3
- Design principles section keeps the exploration lightweight — each level queries, thinks, and passes along rather than producing exhaustive analysis

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify Meditate Mode section exists in the agent file
- Verify "Meditate" appears in the expertise list
- Verify all invocation variants are documented
- Verify recursion parameters are specified
- Verify the section follows the formatting pattern of existing modes

## Execution Notes

### Agent Session Info
- Agent: crux-software-engineer
- Completed: 2026-04-25

### Work Log
1. Read `.cursor/agents/crux-cursor-memory-manager.md` to understand existing mode structure
2. Added "Meditate" to the Your Expertise bullets list with description "Recursive memory-informed exploration and insight synthesis"
3. Added complete Meditate Mode section following the pattern of existing modes (Dream, REM, Recall, Remember, Forget)
4. Documented invocation variants table with 4 rows (no args, quoted text, file/folder refs, internal child invocation)
5. Wrote top-level workflow (8 steps) covering feature guard through interactive continuation
6. Wrote recursive exploration protocol for depths 1–2 (5 steps: query, expand, craft queries, recurse, aggregate)
7. Documented depth 3 base case (steps 1–3 only, no recursion)
8. Added design principles section (light and quick, open-minded, concise returns)
9. Verified the self-recursive pattern documentation: same agent type with `meditateDepth` and `meditateFacet` parameters

### Blockers Encountered
None.

### Files Modified
- `.cursor/agents/crux-cursor-memory-manager.md` (Meditate Mode section added, expertise bullet added)
