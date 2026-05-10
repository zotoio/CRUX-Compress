# Subtask: Eval Categories F-M

## Metadata
- **Subtask ID**: 12
- **Feature**: CRUX Memories
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 11
- **Created**: 20260403

## Objective

Implement automated pytest tests for eval categories F-M: Type Transitions, Compression, Agent Scoping, Scope Ranking, Session Hook, MCP Server, and Config Validation. Uses the shared test infrastructure (conftest, fixtures) created by subtask 11.

## Deliverables Checklist

### Dev Eval Tests (pytest)

- [ ] **F. Type Transitions** (`test_f_type_transitions.py`):
  - Set strength to `promoteAt`, verify promotion recommended
  - After promotion, verify file moved and frontmatter updated
  - Verify `demoteAfterDaysUnreferenced` triggers demotion
  - Verify `archiveAfterDaysUnreferenced` triggers archival

- [ ] **G. Compression** (`test_g_compression.py`):
  - Enable compression, verify `*.memory.crux.md` produced within size limit
  - Verify frontmatter never compressed
  - Verify `compressionTarget` respected
  - Verify migration offer and source archival

- [ ] **H. Agent Scoping** (`test_h_agent_scoping.py`):
  - Verify agent-specific memory goes to `agents/{id}/{type}/`
  - Verify general-purpose memory goes to base
  - Verify agent cannot read other agent directories
  - Verify agent memories only written during dream

- [ ] **I. Scope Ranking** (`test_i_scope_ranking.py`):
  - Configure shared symlink, verify shared memories in index as read-only
  - Verify `scopeRanking` order respected
  - Verify write to shared scope rejected

- [ ] **K. Session Hook** (`test_k_session_hook.py`):
  - Set threshold=2, create 3 plan dirs, verify nudge message
  - Set `enableMemories` false, verify no nudge

- [ ] **L. MCP Server** (`test_l_mcp_server.py`):
  - Start server, call `memory-search`, verify results
  - Test `includeContent` true/false
  - Test `agentId` filtering
  - Test `memory-read` by slug
  - Test `memory-stats` accuracy

- [ ] **M. Config Validation** (`test_m_config_validation.py`):
  - Load config with missing required fields, verify errors
  - Verify `unitOfWork` interpolation in nudge message
  - Verify platform-specific paths resolve correctly
  - Verify `typePriority` ordering used (not alphabetical)

## Definition of Done
- [ ] All F-M test files created with test functions covering spec requirements
- [ ] Tests pass: `pytest evals/test_f*.py evals/test_g*.py evals/test_h*.py evals/test_i*.py evals/test_k*.py evals/test_l*.py evals/test_m*.py`
- [ ] No Python linter errors

## Implementation Notes

Reference `docs/crux-memories.md` Section 8 "Evaluations" for the complete list of eval requirements per category.

Key testing principles:
- Reuse fixtures from `conftest.py` (created in subtask 11)
- Each test should be independently runnable with a clean fixture directory
- Tests should never modify the actual repo — use `tmp_path` fixtures
- For the MCP server tests, start the server in a subprocess and communicate via its transport
- Session hook tests should invoke `.cursor/hooks/crux-session-start.sh` as a subprocess with appropriate environment

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Run only the F-M test files for this subtask's tests
- Defer full test suite execution to the final verification phase

## Execution Notes
[To be filled by executing agent]

### Agent Session Info
- Agent: [Not yet assigned]
- Started: [Not yet started]
- Completed: [Not yet completed]

### Work Log
[Agent adds notes here during execution]

### Blockers Encountered
[Any blockers or issues]

### Files Modified
[List of files changed]
