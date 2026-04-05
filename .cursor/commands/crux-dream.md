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
6. Presents the top candidates ranked by value for user review
7. Creates accepted memories via `crux-skill-memory-crud`
8. Writes a dream summary to the spec directory
9. Rebuilds the memory index
10. Offers to archive the completed spec directory

#### REM Sleep (`--rem`)

1. Loads all memories and reference trackers
2. Verifies data consistency (orphaned trackers, broken strength chains)
3. Detects conflicts between existing memories
4. Evaluates promotions, demotions, archival, and consolidation candidates
5. Detects uncompressed memories for CRUX compression (when `enableMemoryCompression` is enabled)
6. Presents a structured report for user approval
7. Applies confirmed changes (including compression via `crux-skill-memory-compress`)
8. Writes a REM summary
9. Rebuilds the memory index

### After Dreaming

- Use `/crux-mindreader` to view created or modified memories
- Run `/crux-dream --rem` periodically to keep the memory corpus healthy
- Memories with high reference counts may be flagged for promotion to permanent rules

## Related

- `crux-cursor-memory-manager` agent — The specialist that manages the memory lifecycle
- `crux-skill-memory-extract` skill — Dream extraction analysis
- `crux-skill-memory-rebalance` skill — REM sleep rebalancing
- `/crux-mindreader` — View and query memories
