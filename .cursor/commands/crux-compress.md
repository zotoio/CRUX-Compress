# crux-compress

Compress markdown rule files with `crux: true` frontmatter into CRUX notation for token efficiency.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-compress ALL                    - Compress all eligible rules in .cursor/rules/
/crux-compress @path/to/file.md       - Compress a specific file reference
/crux-compress @file1.md @file2.md    - Compress multiple file references
```

## Parallelism Limits

**Maximum parallel agents: 4**

When processing multiple files, spawn at most 4 `crux-cursor-rule-manager` subagent instances simultaneously. If there are more than 4 eligible files, process them in sequential batches:

- **Batch 1**: Files 1-4 (parallel)
- **Batch 2**: Files 5-8 (parallel, after Batch 1 completes)
- **Batch N**: Continue until all files processed

This prevents resource exhaustion and ensures reliable processing.

## Source Checksum Tracking

**CRUX files track the source file's checksum to avoid unnecessary updates.**

Each `.crux.mdc` file includes a `sourceChecksum` field in its frontmatter containing the checksum of the source file. Before processing:

1. Agent gets current checksum using `CRUX-Utils` skill (`--cksum` mode)
2. If existing CRUX file's `sourceChecksum` matches, the source is unchanged - **skip update**
3. If no match (or no existing CRUX file), proceed with compression
4. After compression, store the new `sourceChecksum` in the output frontmatter

This optimization prevents redundant recompression of unchanged files.

## Instructions

### When invoked with file reference(s) (`@path/to/file.md*`)

1. **For each file reference provided**, spawn a **fresh `crux-cursor-rule-manager` subagent instance**:
   - Each file gets its own dedicated agent instance
   - Process files in batches of up to 4 parallel agents
   - Wait for each batch to complete before starting the next
   - Task the subagent:
     ```
     Compress this rule file into CRUX notation:
     - Source: <file path>
     - Output: <file path with .crux.mdc extension>
     - Follow CRUX.md specification
     - Check source checksum vs existing CRUX sourceChecksum - skip if unchanged
     - Report before/after token counts using `CRUX-Utils` skill (or "skipped - source unchanged")
     - If source lacks `crux: true` frontmatter, add it first
     - Ensure source uses .md extension (rename from .mdc if needed)
     ```

2. **Pre-processing for each file** (if needed):
   - If the file is `.mdc` but not `.crux.mdc`, rename to `.md` first
   - If the file lacks `crux: true` in frontmatter, add it
   - Then proceed with compression

3. **After compression completes**, spawn a **fresh `crux-cursor-rule-manager` instance for validation**:
   - Task the validation agent:
     ```
     Perform semantic validation on this CRUX file:
     - Source: <source .md file path>
     - CRUX: <generated .crux.mdc file path>
     - DO NOT use the CRUX specification - evaluate purely on semantic understanding
     - Compare meaning and completeness between source and CRUX
     - Return confidence score (0-100%)
     - Flag any issues if confidence < 80%
     ```
   - The validation agent returns the confidence score
   - Update the `.crux.mdc` frontmatter with `confidence: XX%`

4. **Collect results** and report:
   - File processed or skipped (with reason: "source unchanged" or "compression not beneficial")
   - Token reduction achieved (if processed)
   - **Confidence score** from validation
   - Any issues encountered

### When invoked with `ALL`

1. **Find all eligible files**:
   - Search `.cursor/rules/**/*.md` and `.cursor/rules/**/*.mdc` for files with frontmatter `crux: true`
   - Exclude files that already have a `.crux.mdc` extension (they are outputs, not sources)
   - For `.mdc` files found: apply pre-processing (rename to `.md`, add `crux: true` if missing) before compression
   
2. **For each eligible file**, spawn a **separate `crux-cursor-rule-manager` subagent instance**:
   - Task the subagent to compress the source file
   - The subagent will:
     - Read the CRUX specification from `CRUX.md`
     - Compress the source file
     - Create/update the `[filename].crux.mdc` version
     - Report token reduction metrics
   - **Process in batches of up to 4 parallel agents**
   - Wait for each batch to complete before starting the next batch.

3. **After each compression completes**, spawn a **fresh validation agent**:
   - For each successfully compressed file, spawn a separate `crux-cursor-rule-manager` instance
   - Task: semantic validation (compare CRUX to source, produce confidence score)
   - Update the `.crux.mdc` frontmatter with the confidence score
   - Validation agents can run in parallel with other compression agents (within the 4-agent limit)

4. **Collect results** from all subagents and report summary:
   - Number of files processed
   - Files created/updated
   - Files skipped:
     - Source unchanged (commit hash matches)
     - Already compact (compression not beneficial)
   - Total token savings
   - **Confidence scores** for each file (with average)

## Eligibility Criteria

A file is eligible for CRUX compression if:
- Located in `.cursor/rules/` directory
- Has `.md` or `.mdc` extension
- Has `crux: true` in YAML frontmatter
- Is not already a `.crux.mdc` file (outputs are not recompressed)

**Note**: `.mdc` files with `crux: true` will be pre-processed (renamed to `.md`) before compression. The resulting `.crux.mdc` file will then become the active Cursor rule.

## Adding New Files for Compression

To make a rule file eligible for CRUX compression:

1. Ensure the source file uses `.md` extension (not `.mdc`)
2. Add `crux: true` to the YAML frontmatter:
   ```yaml
   ---
   crux: true
   alwaysApply: true  # or other frontmatter
   ---
   ```
3. Run `/crux-compress ALL` or `/crux-compress @path/to/file.md`

## Source vs Output Convention

| Type | Extension | Example |
|------|-----------|---------|
| Source (human-readable) | `.md` | `core-tenets.md` |
| Compressed (token-efficient) | `.crux.mdc` | `core-tenets.crux.mdc` |

**Important**: The CRUX header in compressed files references the source file:
```
«CRUX⟨core-tenets.md⟩»
```

## Example Batch Execution

### With `ALL` (≤4 files)
When `/crux-compress ALL` finds 4 or fewer eligible files:

```
Batch 1 (parallel, max 4):
├── crux-cursor-rule-manager → core-tenets.md → core-tenets.crux.mdc
├── crux-cursor-rule-manager → xfi-coding-standards.md → xfi-coding-standards.crux.mdc
├── crux-cursor-rule-manager → vscode-optimise.md → vscode-optimise.crux.mdc
└── crux-cursor-rule-manager → _IMPORTANT_CORE_MEMORY.md → _IMPORTANT_CORE_MEMORY.crux.mdc
```

### With `ALL` (>4 files)
When `/crux-compress ALL` finds 6 eligible files:

```
Batch 1 (parallel, max 4):
├── crux-cursor-rule-manager → file1.md → file1.crux.mdc
├── crux-cursor-rule-manager → file2.md → file2.crux.mdc
├── crux-cursor-rule-manager → file3.md → file3.crux.mdc
└── crux-cursor-rule-manager → file4.md → file4.crux.mdc

[Wait for Batch 1 to complete]

Batch 2 (parallel, remaining files):
├── crux-cursor-rule-manager → file5.md → file5.crux.mdc
└── crux-cursor-rule-manager → file6.md → file6.crux.mdc
```

### With file references (>4 files)
When `/crux-compress @file1.md @file2.md @file3.md @file4.md @file5.md`:

```
Batch 1 (parallel, max 4):
├── crux-cursor-rule-manager → file1.md
├── crux-cursor-rule-manager → file2.md
├── crux-cursor-rule-manager → file3.md
└── crux-cursor-rule-manager → file4.md

[Wait for Batch 1 to complete]

Batch 2 (parallel, remaining):
└── crux-cursor-rule-manager → file5.md
```

### Single file
When `/crux-compress @.cursor/rules/core-tenets.md`:

```
Compression:
└── crux-cursor-rule-manager → core-tenets.md → core-tenets.crux.mdc

Validation (after compression completes):
└── crux-cursor-rule-manager (fresh) → validate core-tenets.crux.mdc → confidence: 92%
```

## Semantic Validation

**Every compression is followed by validation** using a fresh agent instance:

1. Compression agent writes `.crux.mdc` (without confidence)
2. Fresh validation agent compares CRUX to source
3. Validation agent returns confidence score (0-100%)
4. Frontmatter is updated with `confidence: XX%`

### Confidence Score

The confidence score indicates how well the CRUX preserves the semantic meaning of the source:

| Score | Status | Action |
|-------|--------|--------|
| ≥90% | Excellent | Accept as-is |
| 80-89% | Good | Accept, minor improvements optional |
| 70-79% | Marginal | Review flagged issues, consider revision |
| <70% | Poor | Revise compression, re-validate |

### Why Fresh Agent for Validation?

Using a **separate agent instance** for validation ensures:
- No bias from the compression process
- Independent semantic evaluation
- The validator doesn't rely on CRUX specification knowledge
- True test of whether an LLM can understand the compressed notation

## Related

- `crux-cursor-rule-manager` subagent - The specialist that performs compression
- `CRUX.md` - The CRUX notation specification
- `.cursor/rules/_CRUX-RULE.mdc` - Rules for working with CRUX files
- `CRUX-Utils` skill - Token estimation and checksum utilities
