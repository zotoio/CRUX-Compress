# crux-dream

Post-execution memory extraction and REM sleep rebalancing.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-dream <spec-name>              - Extract memories from a completed spec
/crux-dream --rem                    - Run REM sleep (rebalance all memories)
/crux-dream --rem --yolo             - Run REM sleep, auto-apply non-conflict changes
```

## Instructions

When this command is invoked, spawn a `crux-cursor-memory-manager` subagent to handle the memory workflow. The manager orchestrates the six memory skills to perform extraction or rebalancing.

**Candidate visibility**: The subagent MUST return its ranked candidates (or REM recommendations) in its final response so they are visible to the user in the chat. The parent agent then asks the user for decisions using `AskQuestion` — never before the candidates are displayed. This ensures the user can read what was extracted before being asked to accept or reject.

**User decisions**: Whenever user approval is needed (accepting candidates, applying REM changes, archiving), use the `AskQuestion` tool in the **parent agent** (not the subagent) to present structured multiple-choice options instead of free-text prompts. This ensures clean, single-click interaction.

### Argument Handling

- **Spec name** (e.g. `20260403-crux-memories`): The manager runs the dream extraction workflow on the completed spec. It verifies execution, analyses artifacts, compares with existing memories, detects conflicts, presents ranked candidates, and creates accepted memories. Pass `$ARGUMENTS` to the subagent as the spec name.
- **`--rem`**: The manager runs REM sleep — a full rebalance of the memory corpus. It scans all memories and trackers, checks consistency, detects conflicts, recommends promotions/demotions/archival/consolidation, and presents a structured report for approval.
- **`--rem --yolo`**: Same as `--rem` but auto-applies all non-conflict recommendations. Conflicts still require manual resolution — they are never auto-resolved.

### What Happens

#### Dream Extraction (spec name)

1. Verifies the spec completed successfully (checks `_execution-state.yml`)
2. Analyses repository changes since spec start for scope assessment
3. Reads all spec artifacts (subtask files, execution reports, work logs, diffs)
4. Extracts candidate facts — learnings, red flags, goals, ideas, core patterns
5. Compares candidates against existing memories for novelty and conflicts
6. Returns the top candidates ranked by value in the subagent response (user-visible)
7. Parent agent uses the `AskQuestion` tool to collect the user's accept/skip decision with structured options (e.g. "Accept all", "Select individually", "Skip all") and whether to archive the spec directory
8. Parent resumes the subagent with the user's decisions; subagent creates accepted memories via `crux-skill-memory-crud`
9. Writes a dream summary to the spec directory
10. Rebuilds the memory index
11. Archives the spec directory if the user opted in

#### REM Sleep (`--rem`)

1. Loads all memories and reference trackers
2. Verifies data consistency (orphaned trackers, broken strength chains)
3. Detects conflicts between existing memories
4. Evaluates promotions, demotions, archival, and consolidation candidates
5. Detects uncompressed memories for CRUX compression (when `enableMemoryCompression` is enabled)
6. Returns recommendations in the subagent response (user-visible); parent agent uses the `AskQuestion` tool to collect the user's approval decision with structured options (e.g. "Apply all", "Select individually", "Skip all") — conflicts always require individual resolution
7. Parent resumes the subagent with the user's decisions; subagent applies confirmed changes (including compression via `crux-skill-memory-compress`)
8. Writes a REM summary
9. Rebuilds the memory index

### After Dreaming

- Use `/crux-recall` to view created or modified memories
- Run `/crux-dream --rem` periodically to keep the memory corpus healthy
- Memories with high reference counts may be flagged for promotion to permanent rules

## Related

- `crux-cursor-memory-manager` agent — The specialist that manages the memory lifecycle
- `crux-skill-memory-extract` skill — Dream extraction analysis
- `crux-skill-memory-rebalance` skill — REM sleep rebalancing
- `/crux-recall` — View and query memories
- `/crux-forget` — Remove memories from the corpus
- `/crux-remember` — Create ad-hoc memories outside of spec workflows
- `/crux-meditate` — Recursive memory-informed exploration
