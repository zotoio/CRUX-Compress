# CRUX Memories — User Evaluation Checklists

Manual and agent-driven testing scenarios for the CRUX Memories system. Each scenario is self-contained and can be followed without prior knowledge of the system internals.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

---

## General Prerequisites

These apply to all scenarios unless overridden by a specific scenario's prerequisites.

1. You are working in a clone of the CRUX-Compress repository on the `feat/memories` branch
2. `.crux/crux-memories.json` exists and has `enableMemories` set to `"true"`:
   ```json
   "flags": [
     { "enableMemories": "true" }
   ]
   ```
3. The `memories/` directory tree exists with type subdirectories (`core/`, `redflag/`, `goal/`, `learning/`, `idea/`, `archived/`, `agents/`)
4. The memory index script is available at `.cursor/skills/crux-skill-memory-index/scripts/memory-index.py`
5. Python 3 is installed and available

---

## B. Dream Interactive Flow

### B1. Dream with No Arguments — List Unprocessed Plans

**Category**: B — Dream Workflow (Interactive)

**Prerequisites**:
- General prerequisites above
- At least one completed spec directory exists under `specs/` with a valid `_execution-state.yml` file whose `status` is `complete`
- At least one spec directory exists that has NOT been dreamed yet (no `dream-*.md` summary file present)

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-dream` with no arguments and send
3. Observe the agent's response

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 2 | The agent spawns a `crux-cursor-memory-manager` subagent | A subagent is invoked (visible in chat or agent logs) |
| 3 | The agent lists unprocessed spec directories found under `specs/` | Output contains a numbered list of spec directory names that have NOT been dreamed |
| 3 | The agent asks which spec to process | A prompt or question asking the user to select a spec appears |
| 3 | Already-dreamed specs (those with a `dream-*.md` file) are NOT listed | Only specs without a dream summary appear in the list |

**Pass/Fail**: PASS if all expected outcomes are met. FAIL if the agent crashes, lists no specs when unprocessed ones exist, or lists already-dreamed specs.

---

### B2. Dream with Spec Name — Full Flow

**Category**: B — Dream Workflow (Interactive)

**Prerequisites**:
- General prerequisites above
- A completed spec exists at `specs/<spec-name>/` (e.g. `specs/20260403-crux-memories/`)
- The spec has `_execution-state.yml` with `status: complete`
- The spec has at least two subtask files with execution notes
- Some existing memories exist in `memories/` (to test comparison and conflict detection)

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-dream <spec-name>` (e.g. `/crux-dream 20260403-crux-memories`) and send
3. Observe the **execution verification** step
4. Observe the **diff analysis** step
5. Observe the **candidate fact presentation**
6. When prompted, accept the candidate facts (type `all` or confirm individually)
7. Observe **memory creation** output
8. Observe the **dream summary** being written
9. Observe the **archival offer**

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | Agent verifies spec execution by checking `_execution-state.yml` | Output confirms execution status (e.g. "✅ Execution verified: X/Y subtasks complete") |
| 4 | Agent reports the number of repository changes since spec start | Output includes a change count and states whether it is within the `maxUnrelatedChanges` threshold (default 50) |
| 5 | Agent presents ranked candidate facts (up to `maxCandidateFacts`, default 5) | Each candidate shows: a rank number, a type label (`[learning]`, `[redflag]`, `[idea]`, `[goal]`, `[core]`), and a descriptive title/body |
| 5 | Candidates are ranked by type priority, measurability, recurrence, actionability, and novelty | Higher-priority types appear first; duplicates of existing memories are excluded |
| 6 | Agent asks for acceptance (`all`, `individual`, or `skip`) | A clear prompt with options appears |
| 7 | Accepted memories are created as `*.memory.md` files in the correct type subdirectory under `memories/` | Files exist at `memories/<type>/<slug>.memory.md` with valid frontmatter (title, description, type, strength=1, created, modified, source=`<spec-name>`, tags) |
| 8 | A dream summary file is written to the spec directory | File exists at `specs/<spec-name>/dream-<slug>-<yyyymmdd>.md` and contains: candidates extracted, accepted, rejected, and memories created |
| 9 | Agent offers to archive the spec directory | Three options are presented: move to `.ai-ignored/executed/`, leave in place, or delete |

**Pass/Fail**: PASS if all steps produce the expected outcomes in order. FAIL if any step is skipped, produces incorrect output, or the agent deviates from the workflow.

---

### B3. Dream Conflict Detection

**Category**: B — Dream Workflow (Conflict Detection)

**Prerequisites**:
- General prerequisites above
- A completed spec exists that would produce a candidate fact about a specific topic (e.g. "prefer X approach for caching")
- A memory already exists in `memories/` that **contradicts** what the spec's candidate would say (e.g. an existing `core` or `learning` memory stating "avoid X approach for caching, use Y instead")
- If no natural conflict exists, manually create one:
  1. Create a memory file at `memories/learning/test-conflict-memory.memory.md`:
     ```yaml
     ---
     title: "Always use write-through caching for user sessions"
     description: "Write-through caching ensures consistency for session data. Read-through causes stale reads."
     type: "learning"
     strength: 3
     created: 2026-03-01
     modified: 2026-03-15
     source: "20260301-caching-design"
     tags: [caching, sessions, consistency]
     ---

     Write-through caching is the only safe approach for user session data.
     Read-through or cache-aside patterns cause stale reads under concurrent writes.
     ```
  2. Ensure the spec under test would extract a candidate fact recommending the opposite pattern (e.g. "cache-aside is preferred for session data")

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-dream <spec-name>` and send
3. Wait for the candidate fact presentation step
4. Observe how the agent handles the conflicting candidate

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3-4 | The agent detects a contradiction between the candidate fact and the existing memory | Output explicitly identifies the conflict, showing both the candidate and the existing memory side by side |
| 4 | The agent presents resolution options | Options include at minimum: keep existing, replace with new, merge both, keep both with disambiguation |
| 4 | The agent does NOT auto-resolve the conflict — it waits for user input | No memory is created or modified for the conflicting candidate until the user explicitly chooses a resolution |
| 4 | Non-conflicting candidates are presented normally (conflict handling does not block other candidates) | Other candidates appear with their normal accept/skip flow |

**Pass/Fail**: PASS if the conflict is detected, both sides are presented, resolution options are offered, and the agent waits for user input. FAIL if the conflict is silently ignored, auto-resolved, or causes the dream to abort.

---

## C. REM Sleep Interactive Flow

### C1. REM Sleep — Interactive Recommendations

**Category**: C — REM Sleep (Interactive)

**Prerequisites**:
- General prerequisites above
- Multiple memories exist across different types in `memories/` (at least 5-10 to produce meaningful recommendations)
- At least one memory has strength meeting or exceeding its type's `promoteAt` threshold (e.g. an `idea` with strength ≥ 5, or a `learning` with strength ≥ 15)
- At least one memory has not been referenced for longer than `demoteAfterDaysUnreferenced` (90 days) — set `modified` and tracker `last_referenced` to a date > 90 days ago
- At least one orphaned tracker file exists in `.crux/reference-tracking/` with no matching memory file
- Optionally: two memories with semantically contradictory content exist to trigger conflict detection

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-dream --rem` and send
3. Observe the REM sleep analysis report

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | The agent presents a structured REM sleep report | Report is clearly organized with distinct sections |
| 3 | **Promotions** section lists memories whose strength meets the `promoteAt` threshold for their type | Each promotion shows: current type, proposed type, memory title, current strength, threshold that triggered it |
| 3 | **Demotions** section lists memories unreferenced for > `demoteAfterDaysUnreferenced` days | Each demotion shows: memory title, days since last reference, proposed action |
| 3 | **Archival** section lists memories unreferenced for > `archiveAfterDaysUnreferenced` days | Each archival candidate shows: memory title, days since last reference |
| 3 | **Consolidation** section lists near-duplicate memories that could be merged | Duplicates are identified with both titles shown |
| 3 | **Conflicts** section lists contradicting memories (if any) | Each conflict shows both memories with their content and asks for resolution |
| 3 | **Cleanup** section lists orphaned tracker files | Each orphan shows the tracker filename and notes that no matching memory exists |
| 3 | The agent asks for confirmation before applying any changes | A prompt appears asking the user to approve all, select specific, or skip |

**Pass/Fail**: PASS if the report contains all applicable sections with clear, actionable recommendations and waits for user confirmation. FAIL if sections are missing, recommendations don't match the seeded data, or changes are applied without confirmation.

---

### C2. REM Sleep — `--yolo` Mode Auto-Apply

**Category**: C — REM Sleep (`--yolo`)

**Prerequisites**:
- Same as C1, with the same seeded data producing at least promotions, demotions, and cleanup recommendations
- At least one pair of conflicting memories exists to test that conflicts are NOT auto-resolved

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-dream --rem --yolo` and send
3. Observe which changes are auto-applied and which require user input

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | **Non-conflict changes are auto-applied** without asking for confirmation | Promotions, demotions, archival, consolidations, cleanup, and rebalances are applied automatically. Output confirms each action taken (e.g. "✅ Promoted idea → learning: <title>") |
| 3 | **Conflicts are NOT auto-applied** — user is prompted | Any detected conflicts are presented with both sides and resolution options. The agent waits for user input before proceeding |
| 3 | Auto-applied promotions result in files moving to the new type directory | Verify: a promoted `idea` memory file now lives under `memories/learning/` and its frontmatter shows `type: "learning"` and `promoted_from: "idea"` |
| 3 | Auto-applied demotions update memory metadata accordingly | Verify: demoted memory files are moved or flagged as expected |
| 3 | Orphaned tracker files are cleaned up automatically | Verify: the orphaned `.refs.yml` file in `.crux/reference-tracking/` is deleted or moved |
| 3 | A REM summary is written | File exists at `.ai-ignored/executed/rem-<yyyymmdd>.md` documenting all changes |
| 3 | The memory index is rebuilt after all changes | `.crux/memory-index.yml` timestamp is updated and contents reflect the new state |

**Pass/Fail**: PASS if all non-conflict changes are auto-applied, conflicts require user input, and post-REM artifacts (summary, index) are correct. FAIL if conflicts are auto-resolved or non-conflict changes prompt for confirmation.

---

### C3. REM Sleep — Conflict Resolution Requires User Input

**Category**: C — REM Sleep (Conflict Handling)

**Prerequisites**:
- General prerequisites above
- Two memories exist with contradictory content. Example:
  - `memories/learning/prefer-sql-joins.memory.md` with body: "Always prefer SQL JOINs over multiple queries for related data"
  - `memories/learning/avoid-sql-joins.memory.md` with body: "Avoid SQL JOINs for large tables — use application-level joins for better cache utilization"

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-dream --rem --yolo` and send
3. Observe how conflicts are handled

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | Conflicts are detected and presented separately from auto-applied changes | Output clearly separates "Auto-applied changes" from "Conflicts requiring resolution" |
| 3 | Each conflict shows both memories with enough context to make a decision | Both titles, descriptions, and relevant body content are displayed |
| 3 | Resolution options are presented | At minimum: keep one, keep the other, merge, keep both with disambiguation |
| 3 | The agent blocks on conflict resolution — does not proceed until user responds | No memory is modified or deleted for the conflicting pair until the user explicitly chooses |
| 3 | After user resolves conflict, the chosen action is applied | The selected resolution takes effect (memory updated, deleted, or merged as chosen) |

**Pass/Fail**: PASS if `--yolo` mode correctly auto-applies everything except conflicts, and conflicts block until user input is received. FAIL if conflicts are auto-resolved or skipped silently.

---

## J. Recall All Invocation Modes

### J1. Recall — No Arguments (Contextual Memories)

**Category**: J — Recall

**Prerequisites**:
- General prerequisites above
- At least 3-5 memories exist in `memories/` with varied types and tags
- The memory index at `.crux/memory-index.yml` is up to date (run the index script if needed)
- Optionally: the current chat session has already referenced some memories (e.g. by running a task where a memory influenced output)

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Have a brief conversation related to topics covered by existing memories (e.g. discuss performance optimization if a memory about React.memo exists)
3. Type `/crux-recall` with no arguments and send
4. Observe the output

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 4 | The agent loads `.crux/memory-index.yml` | The agent reads the index file (visible in tool calls or agent output) |
| 4 | Memories relevant to the current session context are displayed | At least one memory is shown that relates to the topics discussed in step 2 |
| 4 | Each displayed memory includes: title, type, strength, reference count | All four fields are present in the output for each memory |
| 4 | Each displayed memory includes a **rationale** explaining why it was surfaced | A sentence or phrase explains what matched (e.g. "Matched tag 'performance' from current discussion") |
| 4 | The display format follows the documented template | Output uses the format: `─── [{type}] {title} ───` followed by metadata and body |
| 4 | If no memories were referenced yet, the top memories from the index by priority are shown | Memories appear ordered by type priority (core first), then strength, then reference count |

**Pass/Fail**: PASS if contextually relevant memories are displayed with rationale. FAIL if no memories are shown when relevant ones exist, or if rationale is missing.

---

### J2. Recall — Query Mode (Influence Identification)

**Category**: J — Recall

**Prerequisites**:
- General prerequisites above
- At least one memory exists that would influence a coding suggestion (e.g. a memory about memoization patterns)
- A prior conversation exists where the agent made a suggestion that was influenced by a memory (or simulate this by discussing a topic that a memory covers)

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Have a conversation where the agent gives advice on a topic covered by a memory (e.g. ask "How should I optimize my React list component?")
3. Note a specific suggestion the agent made
4. Type `/crux-recall "why did you suggest <specific suggestion>?"` (e.g. `/crux-recall "why did you suggest using React.memo?"`) and send
5. Observe the output

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 5 | The agent identifies which memory (or memories) influenced the suggestion | Output names the specific memory by title |
| 5 | The agent explains the connection between the memory and the suggestion | A clear rationale links the memory's content to the suggestion that was made |
| 5 | The identified memory's content is displayed (decompressed if needed) | Full or relevant excerpt of the memory body is shown |
| 5 | If no memory influenced the suggestion, the agent says so clearly | Output states that the suggestion came from general knowledge, not a specific memory |

**Pass/Fail**: PASS if the agent correctly identifies the influencing memory and explains the connection. FAIL if it fabricates a memory connection or fails to search.

---

### J3. Recall — Spec Name(s) (Source Filtering)

**Category**: J — Recall

**Prerequisites**:
- General prerequisites above
- At least 2-3 memories exist with the `source` field set to a specific spec slug (e.g. `source: "20260403-crux-memories"`)
- At least 1 memory exists with a different `source` to verify filtering

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-recall <spec-name>` (e.g. `/crux-recall 20260403-crux-memories`) and send
3. Observe the output

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | Only memories whose `source` matches the given spec slug are displayed | All displayed memories have `source: "<spec-name>"` in their frontmatter |
| 3 | Memories from other sources are NOT displayed | No memory with a different `source` value appears |
| 3 | Results are grouped by type | Memories are organized under type headings (e.g. "Core", "Learning", "Idea") |
| 3 | Each memory shows full metadata and body content | Title, type, strength, references, tags, created/modified dates, and body are all displayed |
| 3 | Compressed memories are decompressed for display | If any matching memory is a `.memory.crux.md` file, its body is shown in readable natural language |

**Pass/Fail**: PASS if only memories from the specified spec are shown, grouped by type. FAIL if unrelated memories appear or filtering is incorrect.

---

### J4. Recall — Memory File(s) (Direct Display)

**Category**: J — Recall

**Prerequisites**:
- General prerequisites above
- At least one uncompressed memory file exists (e.g. `memories/learning/some-memory.memory.md`)
- At least one compressed memory file exists (e.g. `memories/core/some-memory.memory.crux.md`) — if compression is enabled; otherwise test with uncompressed only

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-recall memories/learning/some-memory.memory.md` and send (use an actual existing path)
3. Observe the output for the uncompressed file
4. If a compressed file exists, type `/crux-recall memories/core/some-memory.memory.crux.md` and send
5. Observe the output for the compressed file

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | The uncompressed memory is displayed with full frontmatter and body | All frontmatter fields (title, description, type, strength, created, modified, source, tags) are shown, followed by the body content |
| 3 | The display format matches the documented template | Uses `─── [{type}] {title} ───` header format |
| 5 | The compressed memory's body is **decompressed** for display | CRUX notation in the body is expanded to terse natural language — the output is human-readable, not raw CRUX symbols |
| 5 | The original `.memory.crux.md` file on disk is NOT modified | Verify with `git status` or `ls -la` — the file's modification time and content have not changed |
| 5 | Frontmatter is displayed identically to uncompressed memories | Title, description, type, etc. appear the same way regardless of compression state |

**Pass/Fail**: PASS if both compressed and uncompressed memories are displayed correctly, with compressed bodies decompressed in-chat only. FAIL if CRUX notation is shown raw, or if the file on disk is modified.

---

## O. Remember Interactive Flow

### O1. Remember — Interactive Creation

**Category**: O — Remember Workflow (Interactive)

**Prerequisites**:
- General prerequisites above
- `enableMemories` is set to `"true"` in `.crux/crux-memories.json`

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-remember` with no arguments and send
3. When prompted, provide insight text (e.g. "Always validate checksums before overwriting files")
4. When prompted, select a memory type (e.g. `learning`)
5. When prompted, provide tags (e.g. `validation, files, safety`)
6. Observe the memory creation output

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 2 | The agent spawns a `crux-cursor-memory-manager` subagent | A subagent is invoked (visible in chat or agent logs) |
| 2 | The agent prompts for the memory content | A question asking what the user wants to remember appears |
| 4 | The agent presents type options from config `typeTransitions` keys | Options include at minimum: idea, learning, redflag, core, goal |
| 6 | A memory file is created in the correct type subdirectory | File exists at `memories/<type>/<slug>.memory.md` with valid frontmatter |
| 6 | Frontmatter contains `source: "adhoc"` | The source field distinguishes ad-hoc from spec-extracted memories |
| 6 | The memory index is rebuilt | `.crux/memory-index.yml` timestamp is updated; new memory appears in the index |
| 6 | Confirmation shows the memory's hash ID, title, type, and file path | All four fields are present in the confirmation message |

**Pass/Fail**: PASS if the interactive flow collects content, type, and tags, creates the memory file correctly, and rebuilds the index. FAIL if any step is skipped, the file is malformed, or the index is not rebuilt.

---

### O2. Remember — One-Shot with Type Flag

**Category**: O — Remember Workflow (One-Shot)

**Prerequisites**:
- General prerequisites above

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-remember "Cache TTLs should match the data refresh interval" --type redflag` and send
3. Observe the output

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | The type selection prompt is skipped | The agent does not ask for type selection — it uses `redflag` directly |
| 3 | A memory file is created at `memories/redflag/<slug>.memory.md` | File exists with `type: "redflag"` in frontmatter |
| 3 | The agent still asks for optional tags and description | Tag and description prompts appear (or sensible defaults are generated) |
| 3 | Confirmation includes the memory's hash ID | Output shows the short hash for future reference |

**Pass/Fail**: PASS if the `--type` flag bypasses type selection and the memory is created in the correct directory. FAIL if the flag is ignored or the memory goes to the wrong directory.

---

## Q. Meditate Interactive Flow

### Q1. Meditate — No Arguments (Context-Derived Facets)

**Category**: Q — Meditate Workflow (Context-Derived)

**Prerequisites**:
- General prerequisites above
- At least 5-10 memories exist in `memories/` with varied types and tags
- The memory index at `.crux/memory-index.yml` is up to date

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Have a brief conversation about a topic covered by existing memories (e.g. discuss performance optimization)
3. Type `/crux-meditate` with no arguments and send
4. Observe the facet derivation
5. Observe the recursive exploration
6. Review the consolidated insights
7. Respond to the interactive continuation menu

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | The agent spawns a `crux-cursor-meditation-guide` subagent | A subagent is invoked (visible in chat or agent logs) |
| 3 | The spawned subagent loads `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md` (or `meditation-quick` in Quick mode) before executing the workflow | Agent output mentions the skill or the Read tool log shows the skill path |
| 3 | If the user accepts the default Research mode at the Cost-and-Richness gate, the agent runs through Phases A–G; if the user switches to Quick via `switch_to_quick`, the agent runs the 6-step protocol | Mode routing is correctly applied based on user's richness-gate response |
| 4 | The agent derives 3 distinct exploration facets from the current conversation context | Output shows 3 labelled facets (e.g. theme, topic, intent) derived from step 2 |
| 4 | 3 parallel Level 1 agents are spawned, one per facet | Agent spawning visible in chat or agent logs |
| 5 | Each Level 1 agent queries memories relevant to its facet | Evidence of memory index or MCP search in agent output |
| 5 | Each Level 1 agent spawns a Level 2 child with refined queries | Recursive spawning visible |
| 5 | Each Level 2 agent spawns a Level 3 child (terminal depth) | Level 3 agents do NOT recurse further |
| 6 | Insights consolidate back: Level 3 → Level 2 → Level 1 → Level 0 | Consolidated output organized by branch with cross-branch connections highlighted |
| 7 | Interactive menu offers: expansion directions, "Save as draft spec", "End meditation" | All three option types present |

**Pass/Fail**: PASS if all three levels of recursion execute, memories are queried at each level, insights consolidate correctly, and the interactive menu is presented. FAIL if recursion does not occur, no memories are queried, or the flow crashes.

---

### Q2. Meditate — Topic Argument

**Category**: Q — Meditate Workflow (Topic-Driven)

**Prerequisites**:
- General prerequisites above
- At least 3-5 memories exist related to the chosen topic

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-meditate "how should we handle caching strategies"` and send
3. Observe the facet derivation from the provided topic
4. Wait for the 3-level recursive exploration to complete
5. Review the consolidated insights
6. Select "Save meditation as draft spec" from the continuation menu

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | The agent derives 3 facets from the provided topic text | Facets are clearly related to "caching strategies" |
| 3 | The `Q-Cost-and-Richness-Acknowledgment` gate fires before depth-0 spawn: 4 richness levels visible (`compact`, `default`, `detailed`, `exhaustive`); `default` preselected | User sees the merged cost+richness gate with 4 options before the exploration begins |
| 4 | All three recursion levels execute to completion | Evidence of Level 1, Level 2, and Level 3 agents running |
| 5 | Consolidated insights reference relevant existing memories | At least one memory is cited in the output |
| 5 | Cross-branch connections and emergent themes are highlighted | Output explicitly identifies patterns or connections across the 3 branches |
| 5 | After consolidation completes, the `Q-Finalisation-Enhancements` multi-select gate fires (0–5 options); selecting 0 reproduces today's behaviour and proceeds to adversarial review | Enhancement gate is presented before adversarial review begins |
| 6 | A draft spec outline is written to `specs/` | File exists under `specs/` with a recognizable name derived from the topic |

**Pass/Fail**: PASS if the topic drives facet derivation, all levels recurse, and "Save as draft spec" produces a file. FAIL if facets are unrelated to the topic, recursion stalls, or the spec save fails.

---

### Q3. Meditate — File/Folder References

**Category**: Q — Meditate Workflow (Code-Referenced)

**Prerequisites**:
- General prerequisites above
- At least one source file or directory exists in the repository

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-meditate @src/auth/` (use an actual directory in the repo) and send
3. Observe the facet derivation from the referenced code
4. Wait for the exploration to complete
5. Select "End meditation" from the continuation menu

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 2 | The **Theme Preflight Q1b repo-scan** fires when `@`/file references are present | A preliminary repo-scan step is visible before facet derivation proceeds |
| 3 | The agent examines the referenced code to derive facets | Facets relate to architecture, patterns, or purpose of the referenced code |
| 4 | Recursive exploration queries memories relevant to the code's domain | Memory queries are contextually appropriate |
| 5 | Session concludes cleanly with no errors | No crashes or orphaned subagents |

**Pass/Fail**: PASS if code references produce relevant facets and the session ends cleanly. FAIL if the agent ignores the file references or the session hangs.

---

## P. Amnesia Interactive Flow

### P1. Amnesia — Toggle Mode

**Category**: P — Amnesia (Session Override)

**Prerequisites**:
- General prerequisites above
- `enableMemories` is set to `"true"` in `.crux/crux-memories.json`
- At least 1-2 memories exist in `memories/` (to verify they are NOT loaded during amnesia)

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-amnesia` with no arguments and send
3. Observe the response
4. Have a brief conversation about a topic covered by existing memories
5. Observe whether memories are surfaced or referenced
6. Type `/crux-amnesia` again to toggle back
7. Have the same conversation topic again
8. Observe whether memories are now surfaced

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | Agent confirms amnesia mode is ON | Response shows `amnesia-on` and `current chat session only` |
| 3 | Config file is NOT modified | `.crux/crux-memories.json` content is unchanged (verify with `git diff`) |
| 4-5 | No memories are discovered, loaded, annotated, or referenced | No `[memory:{title}]` annotations appear; no dream nudge is suggested |
| 6 | Agent confirms amnesia mode is OFF | Response shows `config-driven` |
| 7-8 | Memories are now surfaced normally | `[memory:{title}]` annotations appear if relevant memories exist |

**Pass/Fail**: PASS if toggling amnesia on/off correctly suppresses/restores ambient memory usage without modifying config. FAIL if config is modified, memories leak during amnesia, or restoration does not work.

---

### P2. Amnesia — Explicit Memory Commands Still Work

**Category**: P — Amnesia (Command Override)

**Prerequisites**:
- General prerequisites above
- Amnesia mode is ON (run `/crux-amnesia on` first)
- At least 3-5 memories exist in `memories/`

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-amnesia on` and confirm amnesia is active
3. Type `/crux-recall` and send
4. Observe whether memories are displayed
5. Type `/crux-remember "test memory during amnesia"` and send
6. Observe whether the memory is created

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3-4 | `/crux-recall` works normally despite amnesia | Memories are displayed with full metadata and body content |
| 5-6 | `/crux-remember` creates a memory despite amnesia | A new `.memory.md` file is created with `source: "adhoc"` |
| all | Explicit commands are treated as user intent | The agent does not refuse or warn about amnesia when explicit commands are used |

**Pass/Fail**: PASS if explicit memory commands work normally during amnesia. FAIL if any explicit command is blocked, refused, or degraded.

---

### P3. Amnesia — Subagent Inheritance

**Category**: P — Amnesia (Subagent Behavior)

**Prerequisites**:
- General prerequisites above
- Amnesia mode is ON

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-amnesia on` and confirm amnesia is active
3. Ask the agent to perform a task that spawns subagents (e.g. "Refactor this function" or run a spec)
4. Observe subagent output for memory annotations

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 4 | Subagents do NOT use ambient memories | No `[memory:{title}]` annotations from subagents |
| 4 | Subagents are explicitly told memories are disabled | Subagent prompt includes amnesia state context |

**Pass/Fail**: PASS if subagents inherit amnesia state. FAIL if subagents use memories despite parent being in amnesia mode.

---

## R. Forget Interactive Flow

### R1. Forget — By Memory ID

**Category**: R — Forget Workflow

**Prerequisites**:
- General prerequisites above
- At least 2-3 memories exist (run `/crux-recall` first to get IDs)

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Run `/crux-recall` to see existing memories and note a memory's short hash ID
3. Type `/crux-forget <memory-id>` and send
4. Observe the confirmation prompt
5. Confirm deletion
6. Observe the result

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 4 | Agent shows the memory details and asks for confirmation | Memory title, type, and content are displayed with a yes/no prompt |
| 4 | Agent does NOT delete without confirmation | No file is removed before user confirms |
| 6 | The memory file is deleted | File no longer exists at `memories/<type>/<slug>.memory.md` |
| 6 | The reference tracker is deleted if it existed | `<slug>.refs.yml` no longer exists in `.crux/reference-tracking/` |
| 6 | The memory index is rebuilt | `.crux/memory-index.yml` no longer contains the deleted memory |

**Pass/Fail**: PASS if deletion requires confirmation, removes both the memory file and tracker, and rebuilds the index. FAIL if deletion happens without confirmation, leaves orphaned files, or the index is stale.

---

### R2. Forget — Search and Select

**Category**: R — Forget Workflow (Search)

**Prerequisites**:
- General prerequisites above
- At least 3-5 memories exist with varied tags

**Steps**:

1. Open a new Cursor chat session (agent mode with a thinking model)
2. Type `/crux-forget "performance"` and send
3. Observe search results
4. Select one or more memories to forget
5. Confirm deletion

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 3 | Matching memories are displayed with relevance ranking | Results are ordered by relevance with title, type, and strength shown |
| 3 | User is prompted to select which to forget | A multi-select interface or numbered list is presented |
| 5 | Only selected memories are deleted | Non-selected memories remain intact |
| 5 | Index is rebuilt after all deletions | Index reflects the new state |

**Pass/Fail**: PASS if search returns relevant results, allows selection, and deletes only selected memories. FAIL if wrong memories are deleted or search returns no results when matches exist.

---

## N. Cross-Platform Flows

### N1. Cursor — Full Dream/REM/Recall Flow (Primary Platform)

**Category**: N — Cross-Platform

**Prerequisites**:
- Working in Cursor IDE
- `.crux/crux-memories.json` has `"platform": "cursor"`
- The following Cursor-specific files exist:
  - `.cursor/commands/crux-dream.md`
  - `.cursor/commands/crux-recall.md`
  - `.cursor/commands/crux-remember.md`
  - `.cursor/commands/crux-meditate.md`
  - `.cursor/agents/crux-cursor-memory-manager.md`
  - `.cursor/rules/crux-memories-integration.crux.mdc`
  - `.cursor/hooks/crux-session-start.py`
  - `.cursor/skills/crux-skill-memory-index/scripts/post-dream.py`
- `enableMemories` is set to `"true"` in the config
- At least one completed spec exists for dream testing
- At least 3-5 memories exist for REM and Recall testing

**Steps**:

1. **Session hook**: Start a new Cursor chat session. If the number of spec directories under `specs/` exceeds the `sessionStartNudge.threshold` (default 20), verify the nudge message appears
2. **Dream**: Type `/crux-dream <spec-name>` and run through the full dream flow (see scenario B2 for detailed steps)
3. **Post-dream rebuild**: After dream completes, verify the post-dream script runs (`.cursor/skills/crux-skill-memory-index/scripts/post-dream.py` — rebuilds the memory index)
4. **REM sleep**: Type `/crux-dream --rem` and observe the REM analysis (see scenario C1)
5. **Recall (no args)**: Type `/crux-recall` and verify contextual memories are shown (see scenario J1)
6. **Recall (query)**: Type `/crux-recall "what memories exist?"` and verify search works (see scenario J2)
7. **Recall (file)**: Type `/crux-recall memories/<type>/<slug>.memory.md` for a memory created in step 2 and verify display (see scenario J4)
8. **Meditate**: Type `/crux-meditate "performance patterns"` and verify the 3-level recursive exploration runs, queries memories at each level, and presents consolidated insights (see scenario Q1)

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 1 | Session hook detects `enableMemories=true` and checks spec count | If threshold exceeded: nudge message appears. If not: session starts normally |
| 2 | Full dream flow works as documented | All B2 criteria are met |
| 3 | `.crux/memory-index.yml` is rebuilt after dream | Index file timestamp is updated; new memories from dream appear in the index |
| 4 | REM sleep analysis runs and presents recommendations | All C1 criteria are met |
| 5-7 | All Recall modes work correctly | J1, J2, J4 criteria are met respectively |
| 8 | Meditate explores memories recursively and presents insights | Q1 criteria are met |
| all | The `crux-cursor-memory-manager` subagent is spawned for each command | Agent spawning is visible in Cursor's agent/subagent panel or logs |

**Pass/Fail**: PASS if the complete Cursor workflow (hook → dream → post-dream → REM → Recall → Remember → Meditate) functions end-to-end. FAIL if any command fails to invoke, the subagent is not spawned, or platform-specific wiring is broken.

---

### N2. Claude Code — Wiring Verification

**Category**: N — Cross-Platform

**Prerequisites**:
- Access to a Claude Code environment (or ability to verify file structure)
- The CRUX-Compress repository is cloned
- Familiarity with the Claude Code wiring spec from `docs/crux-memories.md` Section 3b

**Steps**:

1. **Verify config platform**: Confirm `.crux/crux-memories.json` can be set to `"platform": "claude-code"` — the config is valid and parsed correctly
2. **Verify `.claude/` directory structure**: Check that the following files would be created or documented:
   - `.claude/commands/crux-dream.md` — dream command definition
   - `.claude/commands/crux-recall.md` — Recall command definition
   - `.claude/hooks/session-start.sh` — session start hook
3. **Verify `CLAUDE.md` rule content**: The `CLAUDE.md` file (or `.claude/memories-rule.md`) should contain the agent rule text described in the spec:
   - Instructs agents to read `.crux/memory-index.yml` when `enableMemories` is true
   - Instructs agents to annotate output with `[memory:{title}]`
   - Instructs agents to suggest `/crux-dream` after spec execution
4. **Verify command definitions**: The dream command definition should:
   - Reference `.crux/crux-memories.json` for config
   - Accept `$ARGUMENTS` for spec name or `--rem`/`--yolo` flags
   - Describe the dream workflow steps
5. **Verify session hook**: `.claude/hooks/session-start.sh` should:
   - Read config from `.crux/crux-memories.json`
   - Check `enableMemories` flag
   - Count directories in `watchDir`
   - Print nudge message if count exceeds threshold
6. **Verify MCP config**: If MCP is enabled, `.mcp.json` at project root should contain:
   ```json
   {
     "mcpServers": {
       "crux-memories": {
         "command": "python",
         "args": ["-m", "crux_mcp_server", "-t", "stdio", "--config", ".crux/crux-memories.json"]
       }
     }
   }
   ```

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 1 | Config with `"platform": "claude-code"` is valid JSON and can be parsed | No parse errors; `commands.dream.file` would resolve to `.claude/commands/crux-dream.md` |
| 2 | Claude Code directory structure is documented in the spec | `docs/crux-memories.md` Section 3b describes all required files |
| 3 | Agent rule content matches the spec | All five behavioral instructions are present (discover, load, indicate, increment, suggest dream) |
| 4 | Command definitions are functionally equivalent to Cursor commands | Same workflow steps, same argument handling |
| 5 | Session hook follows the same logic as the Cursor hook | Same config keys read, same threshold check, same nudge message |
| 6 | MCP config follows Claude Code conventions | Uses `.mcp.json` at project root (not `.cursor/mcp.json`) |

**Pass/Fail**: PASS if all Claude Code wiring points are correctly documented/structured per the spec. FAIL if any wiring point is missing, incorrectly structured, or incompatible with Claude Code conventions.

---

### N3. Generic Platform — Shell Script Verification

**Category**: N — Cross-Platform

**Prerequisites**:
- A terminal (bash) environment
- The CRUX-Compress repository is cloned
- Python 3 and `jq` are installed
- `.crux/crux-memories.json` exists with `"platform": "generic"` (or verify the spec describes generic wiring)

**Steps**:

1. **Verify agent rule file**: Check that `memories/MEMORIES_AGENT_RULE.md` is documented in the spec as the agent rule location for generic platforms
2. **Verify session hook**: The spec should describe a git-hook or manual script approach:
   ```bash
   crux-memories check-session --config .crux/crux-memories.json
   ```
   Or a standalone bash script equivalent that:
   - Reads config
   - Checks `enableMemories` flag
   - Counts directories in `watchDir`
   - Prints nudge message if threshold exceeded
3. **Verify shell-based commands**: The spec should describe shell-invocable equivalents:
   ```bash
   crux-dream --config .crux/crux-memories.json             # Interactive dream
   crux-dream --rem --config .crux/crux-memories.json        # REM sleep
   crux-dream --rem --yolo --config .crux/crux-memories.json # Unattended REM
   crux-recall --config .crux/crux-memories.json              # Recall
   ```
4. **Verify MCP server can start in stdio mode**: Run the MCP server directly:
   ```bash
   python -m crux_mcp_server -t stdio --config .crux/crux-memories.json
   ```
   Verify it starts without errors and accepts stdio input
5. **Verify index script runs standalone**:
   ```bash
   python .cursor/skills/crux-skill-memory-index/scripts/memory-index.py
   ```
   Verify it produces `.crux/memory-index.yml`

**Expected Outcomes**:

| Step | Expected | Pass Criteria |
|------|----------|---------------|
| 1 | Generic platform rule file location is documented | `docs/crux-memories.md` Section 3c specifies `memories/MEMORIES_AGENT_RULE.md` |
| 2 | Session hook approach is documented for non-IDE environments | Manual or git-hook approach described with config reading logic |
| 3 | Shell commands are documented with `--config` flag | All four command variants (dream, dream --rem, dream --rem --yolo, recall) are described |
| 4 | MCP server starts in stdio mode | Process starts, no import errors or crashes. Server responds to MCP protocol handshake |
| 5 | Index script runs and produces valid YAML | `.crux/memory-index.yml` is created/updated with a valid `memories:` list |

**Pass/Fail**: PASS if all generic platform wiring is documented and the standalone tools (MCP server, index script) function correctly. FAIL if shell-based workflows are undocumented or tools fail to run outside of an IDE.

---

## Appendix: Quick Reference

### Commands

| Command | Description |
|---------|-------------|
| `/crux-dream` | List unprocessed specs, select one to dream |
| `/crux-dream <spec-name>` | Extract memories from a specific completed spec |
| `/crux-dream --rem` | Run REM sleep — rebalance all memories interactively |
| `/crux-dream --rem --yolo` | Run REM sleep — auto-apply non-conflict changes |
| `/crux-recall` | Show contextually relevant memories |
| `/crux-recall "query"` | Search memories by keyword |
| `/crux-recall <spec-name>` | Show memories from a specific spec |
| `/crux-recall <file-path>` | Display a specific memory file |
| `/crux-forget <memory-id>` | Forget a specific memory by ID |
| `/crux-forget "query"` | Search and select memories to forget |
| `/crux-remember` | Interactively create a new ad-hoc memory |
| `/crux-remember "insight"` | Create a memory from provided text |
| `/crux-remember "insight" --type learning` | Create with a specific type |
| `/crux-amnesia` | Toggle session-scoped ambient memory suppression |
| `/crux-amnesia on` | Enable amnesia mode for the current chat session |
| `/crux-amnesia off` | Restore config-driven memory behavior |
| `/crux-amnesia status` | Show the current session memory mode |
| `/crux-meditate` | Recursive memory-informed exploration of current context |
| `/crux-meditate "topic"` | Explore a specific theme with 3-level deep memory search |

### Key Files

| File | Purpose |
|------|---------|
| `.crux/crux-memories.json` | Main configuration |
| `.crux/memory-index.yml` | Prioritised memory index |
| `.crux/reference-tracking/*.refs.yml` | Per-memory reference trackers |
| `memories/{type}/*.memory.md` | Memory files (uncompressed) |
| `memories/{type}/*.memory.crux.md` | Memory files (compressed) |
| `.cursor/agents/crux-cursor-memory-manager.md` | Memory lifecycle agent (Dream, REM, Recall, Remember, Forget) |
| `.cursor/agents/crux-cursor-meditation-guide.md` | Meditation guide agent — owns Meditate persona, Research Phases A–G, Quick 6-step protocol, 13-dim adversarial review, K10 ensemble aggregation |
| `.cursor/commands/crux-dream.md` | Dream command definition (Cursor) |
| `.cursor/commands/crux-recall.md` | Recall command definition (Cursor) |
| `.cursor/commands/crux-forget.md` | Forget command definition (Cursor) |
| `.cursor/commands/crux-remember.md` | Remember command definition (Cursor) |
| `.cursor/commands/crux-meditate.md` | Meditate command definition (Cursor) |
| `.cursor/skills/crux-skill-memory-meditation-research/SKILL.md` | Research-mode Phases A–G protocol |
| `.cursor/skills/crux-skill-memory-meditation-quick/SKILL.md` | Quick-mode 6-step protocol |
| `.cursor/skills/crux-skill-memory-meditation-ensemble/SKILL.md` | Ensemble Aggregation function |
| `.cursor/skills/crux-skill-memory-meditation-review/SKILL.md` | 13-dimension adversarial review |
| `.cursor/skills/crux-skill-memory-meditation-report/SKILL.md` | Paired HTML+PDF report generation |
| `.cursor/skills/crux-skill-memory-meditation-coordination/SKILL.md` | File-based coordination (18-row filename grammar) |
| `.cursor/hooks/crux-session-start.py` | Session start hook |
| `.cursor/skills/crux-skill-memory-index/scripts/post-dream.py` | Post-dream index rebuild |

### Config Thresholds (Defaults)

| Setting | Default | Purpose |
|---------|---------|---------|
| `maxCandidateFacts` | 5 | Max candidate facts presented during dream |
| `maxUnrelatedChanges` | 50 | Warn if repo changes exceed this count |
| `demoteAfterDaysUnreferenced` | 90 | Days before unreferenced memory is demoted |
| `archiveAfterDaysUnreferenced` | 180 | Days before unreferenced memory is archived |
| `promotionToRuleThreshold` | 30 | References before suggesting rule promotion |
| `sessionStartNudge.threshold` | 20 | Spec count before nudge message appears |
