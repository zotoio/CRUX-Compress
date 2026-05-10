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

**User input escalation — CRITICAL**: This command uses **Pattern B (work first, then escalate)** — the subagent must analyse artifacts and rank candidates before the user can make decisions. The subagent NEVER calls `AskQuestion` directly. ALL user-facing questions (accepting candidates, applying REM changes, resolving conflicts, archiving) are handled by the **parent agent** (you) using `AskQuestion`. The subagent returns its analysis and any `needs_user_input` sections; you collect answers from the user and resume the subagent with them.

**Foreground execution — CRITICAL**: The subagent MUST run in the **foreground** (`run_in_background: false`). Background subagents only return a truncated summary notification to the parent — the full analysis is lost. Foreground execution blocks the parent until the subagent completes and returns its **complete response**, which the parent then displays verbatim to the user.

**Full output relay — CRITICAL**: The parent agent MUST relay the subagent's complete response to the user **without summarizing, truncating, or paraphrasing**. The subagent's response contains the full spec analysis — artifact examination, candidate ranking, conflict reports, resolved bug detection — and all of this must be visible to the user before any decisions are requested. If the response is long, display it in full; do not condense it.

**Candidate visibility**: The subagent MUST return its ranked candidates (or REM recommendations) **and the full analysis that produced them** in its final response. This includes: verification results, diff analysis summary, artifact examination findings, comparison results against existing memories, and the ranked candidates with full rationale. The parent agent displays all of this, then asks the user for decisions using `AskQuestion` — never before the full analysis is displayed.

**User decisions**: Whenever user approval is needed (accepting candidates, applying REM changes, archiving), use the `AskQuestion` tool in the **parent agent** (not the subagent) to present structured multiple-choice options instead of free-text prompts. This ensures clean, single-click interaction.

### Argument Handling

- **No arguments** (just `/crux-dream`): The parent agent discovers available specs by scanning the configured `workDir` from `.crux/crux-memories.json` (`cruxMemories.dream.workDir`, default `specs`). It lists all subdirectories in that directory (excluding `.gitkeep` and hidden files), and presents them as structured options using `AskQuestion` so the user can select which spec to dream about. If the `workDir` is empty or contains no spec directories, inform the user and stop. **Do not accept spec names from other directories** — only specs present in the configured `workDir` are valid targets.
- **Spec name** (e.g. `20260403-crux-memories`): Validate that the named spec exists as a subdirectory of the configured `workDir`. If it does not exist there, report the error and show the available specs from `workDir` instead. Do not search other directories. Once validated, the manager runs the dream extraction workflow on the completed spec. Pass `$ARGUMENTS` to the subagent as the spec name.
- **`--rem`**: The manager runs REM sleep — a full rebalance of the memory corpus. It scans all memories and trackers, checks consistency, detects conflicts, recommends promotions/demotions/archival/consolidation, and presents a structured report for approval.
- **`--rem --yolo`**: Same as `--rem` but auto-applies all non-conflict recommendations. Conflicts still require manual resolution — they are never auto-resolved.

### What Happens

#### Dream Extraction (spec name)

1. Verifies the spec completed successfully (checks `_execution-state.yml`)
2. Analyses repository changes since spec start for scope assessment
3. Reads all spec artifacts (subtask files, execution reports, work logs, diffs)
4. Extracts candidate facts — learnings, red flags, goals, ideas, core patterns
5. Compares candidates against existing memories for novelty and conflicts
6. Subagent returns its **complete analysis and ranked candidates** in its response — the parent agent receives this because the subagent runs in the foreground
7. **Parent displays the full subagent response** verbatim to the user — do not summarize or omit any part of the analysis
8. Parent agent uses the `AskQuestion` tool to collect the user's accept/skip decision with structured options (e.g. "Accept all", "Select individually", "Skip all") and whether to archive the spec directory
9. Parent resumes the subagent with the user's decisions; subagent creates accepted memories via `crux-skill-memory-crud`
10. Writes a dream summary to the spec directory
11. Rebuilds the memory index
12. Archives the spec directory if the user opted in

#### REM Sleep (`--rem`)

1. Loads all memories and reference trackers
2. Verifies data consistency (orphaned trackers, broken strength chains)
3. Detects conflicts between existing memories
4. Evaluates promotions, demotions, archival, and consolidation candidates
5. Detects uncompressed memories for CRUX compression (when `enableMemoryCompression` is enabled)
6. Subagent returns its **complete analysis and recommendations** in its response — the parent agent receives this because the subagent runs in the foreground
7. **Parent displays the full subagent response** verbatim to the user; parent agent then uses the `AskQuestion` tool to collect the user's approval decision with structured options (e.g. "Apply all", "Select individually", "Skip all") — conflicts always require individual resolution
8. Parent resumes the subagent with the user's decisions; subagent applies confirmed changes (including compression via `crux-skill-memory-compress`)
9. Writes a REM summary
10. Rebuilds the memory index

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
