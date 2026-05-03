# crux-meditate

Recursive memory-informed exploration of themes, topics, and intent through 3-level deep agent inception.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-meditate                          - Explore facets derived from current chat context
/crux-meditate "topic or question"      - Explore a specific theme
/crux-meditate @file.ts @folder/        - Explore facets around referenced code
```

## Instructions

When this command is invoked, spawn a `crux-cursor-memory-manager` subagent in Meditate mode. The manager orchestrates a 3-level recursive exploration by spawning child instances of itself, each querying memories, expanding on discoveries, and passing consolidated insights back up to the parent.

**Critical**: The subagent performs steps 1–6 and **returns** the full consolidation result to you (the calling agent). You then handle steps 7–9 directly with the user — subagents cannot interact with the user, so presentation and interactive continuation must happen in the calling agent.

### Argument Handling

- **No arguments**: The manager examines the current chat context — conversation history, open files, recent activity — to derive three exploration facets (theme, topic, intent). Pass `$ARGUMENTS` to the subagent.
- **Quoted text** (e.g. `"how should we handle caching"`): Use the provided text as the seed topic. The manager derives three facets from it. Pass `$ARGUMENTS` to the subagent.
- **File/folder references** (e.g. `@src/auth/ @config.ts`): The manager examines the referenced code to derive facets around its architecture, patterns, and purpose. Pass `$ARGUMENTS` to the subagent.
- **Mixed input**: Any combination of text, files, folders, images, or past chat references. The manager synthesizes all inputs to derive facets.

### What Happens

**Steps 1–6: Performed by the subagent**

1. The manager reads `.crux/crux-memories.json` to load configuration (check `enableMemories` flag)
2. **Derive facets**: From the input (or chat context if no args), identify three distinct exploration facets — e.g. theme, topic, and intent. Each facet becomes a branch of exploration.
3. **Spawn Level 1**: Launch 3 background `crux-cursor-memory-manager` subagents in Meditate mode, one per facet, each with `meditateDepth: 1` and `maxDepth: 3`. All three run in parallel.
4. **Recursive exploration** (each agent at depth 1 and 2):
   a. Query memories relevant to its assigned facet using the memory index and search
   b. Expand on the facet in light of discovered memories — draw connections, identify patterns, surface non-obvious relationships
   c. Craft refined queries based on notions in the expansion
   d. Spawn a child `crux-cursor-memory-manager` at `depth + 1` with the refined queries and accumulated context
   e. Receive child's insights, aggregate with own expansion, return consolidated result to parent
5. **Level 3** (deepest): Performs steps a–c only — no further recursion. Returns insights directly to parent.
6. **Consolidation**: Level 0 receives consolidated ruminations from all 3 branches. Synthesizes a cohesive summary of discoveries, patterns, connections, and potential directions. **The subagent must return this full consolidation — organized by branch with all discoveries, patterns, connections, potential directions, and suggested tangent directions for further exploration — as its final response to the calling agent.**

**Steps 7–9: Performed by you (the calling agent) upon receiving the consolidation**

7. **Present to user**: Display the consolidated insights organized by branch, highlighting cross-branch connections and emergent themes.
8. **Interactive continuation**: Use `AskQuestion` with multi-select options:
   - Discovered tangent directions (derived from the exploration) as expansion options
   - "Save meditation as draft spec" — write insights as a draft spec outline to `specs/`
   - "End meditation" — complete the session
9. If the user selects expansion directions, augment context with the new directions and user input, then repeat from step 2 (spawning a new subagent with the expanded context). If "Save", write a draft spec file. If "End", finish.

## Related

- `crux-cursor-memory-manager` agent — The specialist that orchestrates the recursive meditation
- `crux-skill-memory-index` skill — Memory index used for facet-relevant memory discovery
- `crux-skill-memory-crud` skill — Read operations for loading memory content during exploration
- `/crux-dream` — Extract and create memories from completed work
- `/crux-recall` — View and query memories
- `/crux-remember` — Create ad-hoc memories outside of spec workflows
- `/crux-forget` — Remove memories from the corpus
