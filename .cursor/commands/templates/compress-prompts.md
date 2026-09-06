# /crux-compress — per-source-type dispatch prompts

This file holds the five per-source-type dispatch bodies for the `/crux-compress` command. It is a plain markdown data file — **not** a Cursor command file (no frontmatter, no IDE registration). The loadable command `.cursor/commands/crux-compress.md` (generated from `crux-compress.source.mdx`) loads only the section matching the resolved source type of a given invocation.

## Shared Preamble

Every dispatch body below assumes the command file has already:

1. Resolved the compression level (`Compression Level Resolution` in the command file — CLI `--<n>` > source frontmatter `crux: <n>` > default 25 for text/code/url, 80 for images).
2. Resolved the active plugin set (`Plugin Resolution` in the command file), with the resulting `pluginsByHook.{beforeFetch, beforeCompress, afterCompress, afterValidate}` arrays available.
3. Applied the `--force` pre-processing branch when `--force` was passed (delete pre-existing `.crux.md` / `.crux.mdc` output(s) for the target source(s) before invoking a dispatch below).
4. Honored the **parallelism cap of 4** `crux-cursor-rule-manager` subagent instances per batch. Every dispatch below inherits this cap — no dispatch may spawn more than 4 concurrent subagents.
5. Read the `Semantic Validation` and `Source Checksum Tracking` sections in the command file for the invariants each dispatch's validation step must honor.

The `--minified` flag applies to text/code/URL dispatches only. `sourceChecksum` skip-if-unchanged applies to markdown and code dispatches only. Images use `.crux.md` output with no checksum tracking; URLs use `sourceUrl` in place of `sourceChecksum`.

## markdown

1. **If `--force` flag is passed**, delete existing CRUX output files first (see above)

2. **For each file reference provided**, spawn a **fresh `crux-cursor-rule-manager` subagent instance**:
   - Each file gets its own dedicated agent instance
   - Process files in batches of up to 4 parallel agents
   - Wait for each batch to complete before starting the next
   - Run enabled `beforeCompress` plugins for each markdown source
   - Task the subagent:
     ```
     Compress this rule file into CRUX notation:
     - Source: <file path>
     - Output: rules→.crux.mdc; commands/agents .source.mdx→<name>.md; skills SKILL.mdx→SKILL.md; else→.crux.md
     - For .cursor/rules/ sources: include alwaysApply from source frontmatter in output
     - For commands/agents/skills: preserve Cursor registration frontmatter (name, model, description, …); body is CRUX
     - For other sources: do NOT include alwaysApply or IDE-specific frontmatter
     - Format: <formatted (default) OR minified if --minified flag was passed>
     - Compression level: <resolved level, default 25>
     - Follow CRUX.md specification
     - Check source checksum vs existing CRUX sourceChecksum - skip if unchanged
     - Report before/after token counts using `crux-utils` skill (or "skipped - source unchanged")
     - If source lacks `crux: true` or `crux: <n>` frontmatter, add `crux: true` first (rules)
     - SoT extensions: rules `.md` (rename from `.mdc` if needed); commands/agents `<name>.source.mdx` → loadable `<name>.md`; skills `SKILL.mdx` → loadable `SKILL.md`
     ```

3. **Pre-processing for each file** (if needed):
   - Rules: if `.mdc` but not `.crux.mdc`, rename to `.md` SoT first; add `crux: true` if missing
   - Commands/agents: SoT must be `<name>.source.mdx`; output is compressed loadable `<name>.md` (preserve registration frontmatter)
   - Skills: SoT must be `SKILL.mdx`; output is compressed loadable `SKILL.md`
   - Then proceed with compression

4. **After compression completes**, spawn a **fresh `crux-cursor-rule-manager` instance for validation**:
   - Task the validation agent:
     ```
     Perform semantic validation on this CRUX file:
     - Source: <SoT path: .md / .source.mdx / SKILL.mdx>
     - CRUX: <loadable output: .crux.mdc | <name>.md | SKILL.md | .crux.md>
     - DO NOT use the CRUX specification - evaluate purely on semantic understanding
     - Compare meaning and completeness between source and CRUX
     - Return confidence score (0-100%)
     - Flag any issues if confidence < 80%
     ```
   - The validation agent returns the confidence score
   - Update the CRUX output file's frontmatter with `confidence: XX%`
   - Run enabled `afterCompress` plugins after each successful compression
   - Run enabled `afterValidate` plugins after each validation result

5. **Collect results** and report:
   - File processed or skipped (with reason: "source unchanged" or "compression not beneficial")
   - Token reduction achieved (if processed)
   - **Confidence score** from validation
   - Plugin execution results (if plugins were enabled)
   - Any issues encountered
   - If `--force` was used, note files that were deleted before recompression

6. **Clear processed files from pending-compression.json**:
   - Read `.crux/pending-compression.json` if it exists
   - Remove any files from the `files` array that were just processed (successfully compressed or skipped)
   - Do NOT remove files that were not part of this compression run (preserve newly added pending files)
   - Write the updated JSON back to the file
   - If the `files` array is now empty, write `{"files": []}` (omit the `updated` field)

## image

1. **If `--force` flag is passed**, delete existing `.crux.md` files for the images first

2. **For each image file**, spawn a **fresh `crux-cursor-rule-manager` subagent instance**:
   - Process images in batches of up to 4 parallel agents
   - Run enabled `beforeCompress` plugins for the image context
   - Task the subagent:
     ```
     Compress this image into CRUX notation (semantic visual description):
     - Source: <image file path>
     - Output: <image path with extension replaced by .crux.md>
     - Compression level: <resolved level, default 80>
     - Use vision capabilities to analyze the image
     - Describe semantic content using CRUX blocks (Ρ, Κ, Π.layout, E.element, Ω.metaphor)
     - Preserve all visible text/labels verbatim
     - Capture spatial relationships, visual style, and conceptual meaning
     - Detail retention: level controls how much visual detail to describe
       (100 = maximum detail, every element; 80 = detailed with textures and secondary elements;
        25 = key elements and meaning; 10 = essential concept only)
     - Follow CRUX.md specification for notation
     - Report original file size and .crux.md file size
     ```

3. **Collect results** and report:
   - Image file processed
   - Original file size vs `.crux.md` file size
   - Plugin execution results (if plugins were enabled)
   - Any issues encountered

**Note**: Image compression does not use `sourceChecksum` tracking, `crux: true` frontmatter, or the `--minified` flag. Semantic validation is not automated for images — visual fidelity must be verified manually by feeding the `.crux.md` file to an LLM with image generation.

## url

1. **If `--force` flag is passed**, delete existing `.crux.md` files in `.crux/out/` for matching URL-derived filenames first

2. **For each URL**, spawn a **fresh `crux-cursor-rule-manager` subagent instance**:
   - Process URLs in batches of up to 4 parallel agents
   - Run enabled `beforeFetch` plugins before `WebFetch`
   - **Before spawning**: fetch the webpage content using the `WebFetch` tool
   - Run enabled `beforeCompress` plugins with fetched content metadata
   - **Derive output filename** from the URL: strip protocol, replace `/` and special chars with `-`, remove trailing `-`, append `.crux.md`
     - `https://agents.md/` → `agents-md.crux.md`
     - `https://example.com/docs/api` → `example-com-docs-api.crux.md`
   - **Output directory**: `.crux/out/` (create if it doesn't exist)
   - Task the subagent:
     ```
     Compress this webpage content into CRUX notation:
     - Source URL: <url>
     - Content: <fetched webpage content>
     - Output: .crux/out/<derived-filename>.crux.md
     - Format: <formatted (default) OR minified if --minified flag was passed>
     - Compression level: <resolved level, default 25>
     - Use sourceUrl in frontmatter instead of sourceChecksum
     - Include reducedBy percentage and cruxLevel in frontmatter
     - Follow CRUX.md specification for notation
     - Report before/after token counts
     ```

3. **After compression completes**, spawn a **fresh validation agent** (same as for markdown)
   - Run enabled `afterCompress` plugins after each successful compression
   - Run enabled `afterValidate` plugins after each validation result

4. **Collect results** and report:
   - URL processed
   - Output file path (in `.crux/out/`)
   - Token reduction achieved and `reducedBy` percentage
   - Confidence score from validation
   - Plugin execution results (if plugins were enabled)
   - Any issues encountered

**Note**: URL compression uses `sourceUrl` instead of `sourceChecksum` in frontmatter. No Cursor adapter (`.crux.mdc`) is produced for URL sources. URLs are NOT included in `ALL` scans — they must be explicitly provided.

## code

1. **If `--force` flag is passed**, delete existing `.crux.md` files for the code files first

2. **For each code file**, spawn a **fresh `crux-cursor-rule-manager` subagent instance**:
   - Process code files in batches of up to 4 parallel agents
   - Run enabled `beforeCompress` plugins for the code context
   - Task the subagent:
     ```
     Compress this code file into CRUX notation:
     - Source: <code file path>
     - Output: <code path with extension replaced by .crux.md>
     - Format: <formatted (default) OR minified if --minified flag was passed>
     - Compression level: <resolved level, default 25>
     - Use code block mappings: Λ for functions, Γ for orchestration, Φ for config
     - Preserve function names verbatim, type signatures for public interfaces
     - Encode IO semantics explicitly (stdout vs stderr, return channels)
     - Generate Ω.decomp block with emulate= and focus= fields
     - Follow CRUX.md specification for notation
     - Check source checksum vs existing CRUX sourceChecksum - skip if unchanged
     - Report before/after token counts
     ```

3. **After compression completes**, spawn a **fresh validation agent** (same as for markdown)
   - Run enabled `afterCompress` plugins after each successful compression
   - Run enabled `afterValidate` plugins after each validation result

4. **Collect results** and report:
   - File processed or skipped
   - Token reduction achieved
   - Confidence score from validation
   - Plugin execution results (if plugins were enabled)
   - Any issues encountered

**Note**: Code compression does not use `alwaysApply` frontmatter, `crux: true` opt-in, or the Cursor adapter step. Code files are not included in `ALL` scans — they must be explicitly referenced. No Cursor adapter (`.crux.mdc`) is produced for code files.

## all

1. **If `--force` flag is passed**, delete all existing CRUX output files first:
   - Find all `.crux.mdc` files in `.cursor/rules/` (excluding `_CRUX-RULE.mdc`)
   - Also delete any leftover `.crux.md` intermediary files in `.cursor/rules/` (legacy cleanup)
   - Delete each one and log the deletion
   - This ensures all eligible sources will be freshly compressed

2. **Find all eligible files**:
   - Search `.cursor/rules/**/*.md` and `.cursor/rules/**/*.mdc` for files with frontmatter `crux: true` or `crux: <n>`
   - Exclude files that already have a `.crux.md` or `.crux.mdc` extension (they are outputs, not sources)
   - For `.mdc` files found: apply pre-processing (rename to `.md`, add `crux: true` if missing) before compression
   - Extract numeric `crux` value from frontmatter if present (used as per-file compression level unless CLI `--<n>` overrides)

3. **For each eligible file**, spawn a **separate `crux-cursor-rule-manager` subagent instance**:
   - Task the subagent to compress the source file
   - The subagent will:
     - Read the CRUX specification from `CRUX.md`
     - Compress the source file
     - Create/update the `[filename].crux.mdc` output directly (with `alwaysApply` from source frontmatter)
     - Report token reduction metrics
     - Apply enabled `beforeCompress` and `afterCompress` plugin hooks
   - **Process in batches of up to 4 parallel agents**
   - Wait for each batch to complete before starting the next batch.

4. **After each compression completes**, spawn a **fresh validation agent**:
   - For each successfully compressed file, spawn a separate `crux-cursor-rule-manager` instance
   - Task: semantic validation (compare CRUX to source, produce confidence score)
   - Update the `.crux.md` frontmatter with the confidence score
   - **Cursor adapter**: Copy `.crux.md` to `.crux.mdc` with `alwaysApply` injected from source
   - Apply enabled `afterValidate` plugin hooks
   - Validation agents can run in parallel with other compression agents (within the 4-agent limit)

5. **Collect results** from all subagents and report summary:
   - Number of files processed
   - Files created/updated
   - Files skipped:
     - Source unchanged (checksum matches) - **Note**: with `--force`, no files are skipped for this reason
     - Already compact (compression not beneficial)
   - If `--force` was used, list files that were deleted before recompression
   - Total token savings
   - **Confidence scores** for each file (with average)
   - Plugin execution summary:
     - Plugins requested
     - Hooks executed
     - Any plugin failures (and whether they were fail-open or fail-closed)

6. **Clear processed files from pending-compression.json**:
   - Read `.crux/pending-compression.json` if it exists
   - Remove any files from the `files` array that were just processed (successfully compressed or skipped)
   - Do NOT remove files that were not part of this compression run (preserve newly added pending files)
   - Write the updated JSON back to the file
   - If the `files` array is now empty, write `{"files": []}` (omit the `updated` field)
