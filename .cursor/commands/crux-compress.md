# crux-compress

Compress markdown rule files, code files, and images into CRUX notation for token/size efficiency.

**Repository**: [github.com/zotoio/CRUX-Compress](https://github.com/zotoio/CRUX-Compress)

## Usage

```
/crux-compress ALL                    - Compress all eligible rules (formatted output)
/crux-compress @path/to/file.md       - Compress a specific file (formatted output)
/crux-compress @file1.md @file2.md    - Compress multiple files (formatted output)
/crux-compress @file.md --minified    - Compress with single-line output
/crux-compress ALL --minified         - Compress all with single-line output
/crux-compress ALL --force            - Force recompression (delete existing CRUX files first)
/crux-compress @file.md --force       - Force recompression of specific file
/crux-compress @file.md --40          - Compress targeting 40% of original size
/crux-compress @file.md --10          - Aggressive compression targeting 10%
/crux-compress @script.sh              - Compress a code file
/crux-compress @src/app.ts @lib/utils.py - Compress multiple code files
/crux-compress @image.png             - Compress an image (semantic visual description)
/crux-compress @image.png --80        - Compress image retaining 80% detail
/crux-compress @img1.png @img2.jpg    - Compress multiple images
/crux-compress https://example.com/page  - Compress a webpage (URL source)
/crux-compress https://a.com https://b.com - Compress multiple URLs
/crux-compress @file.md --plugin=frontmatter-tagger - Run a plugin while compressing
/crux-compress ALL --plugin quality-gate --plugin release-notes - Run multiple plugins
/crux-compress @file.md --no-plugin compression-level  - Disable a default-enabled plugin
```

### Flags

| Flag | Description | Use Case |
|------|-------------|----------|
| `--minified` | Single-line output, no spaces, max compression | Copy-paste demos, LLM testing |
| `--force` | Delete existing CRUX output files (`.crux.mdc` or `.crux.md`) before compression | Force fresh recompression, bypass checksum skip |
| `--<n>` | Set compression level to `n`% (1-100). Overrides frontmatter `crux: <n>`. Default: 25 | `--40` for 40% target, `--10` for aggressive compression |
| `--plugin <name>` / `--plugin=<name>` | Enable a named plugin from the plugin registry | Add optional feature behavior without changing core command flow |
| `--no-plugin <name>` | Disable a specific default-enabled plugin | Opt out of a default plugin without switching to fully-explicit mode |

**Note**: Flags can be combined: `/crux-compress ALL --force --minified --40 --plugin quality-gate`

### Compression Level

The compression level controls the target output size as a percentage of the original:

| Level | Target | Effect |
|-------|--------|--------|
| `--10` | ≤10% of original | Very aggressive — heavy abbreviation, symbols only |
| `--25` (default) | ≤25% of original | Standard compression |
| `--40` | ≤40% of original | Moderate — more prose preserved |
| `--80` | ≤80% of original | Light — close to original structure |

The level can also be set in the source file's frontmatter as `crux: <n>` (e.g., `crux: 40`). The CLI flag overrides frontmatter when both are present.

For **images**, the level controls detail retention (100 = maximum detail, 1 = minimal; default 80). For **text sources**, it controls the token ratio target (default 25).

### Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| **Formatted** (default) | Multi-line, indented, ~80 char lines | `.crux.md` files for readability |
| **Minified** (`--minified`) | Single-line, no spaces, max compression | Copy-paste demos, LLM testing |

### Plugin Parameter System

`/crux-compress` supports optional plugins to add feature-specific behavior via command parameters.

- **Parameter format**: `--plugin <name>` or `--plugin=<name>`
- **Repeatable**: multiple plugins can be enabled in one run
- **Execution model**: plugins run at predefined lifecycle hooks
- **Isolation**: plugin failures are reported per plugin and should not block base compression unless explicitly configured in the plugin

#### Plugin Registry

Plugins are resolved from `.crux/plugins/registry.json` (if present). Minimal shape:

```json
{
  "plugins": {
    "compression-level": {
      "description": "Enforce compression ratio targets and generate token metrics.",
      "hooks": ["beforeCompress", "afterCompress"],
      "failClosed": false,
      "enabledByDefault": true
    },
    "frontmatter-tagger": {
      "description": "Add standardized metadata after compression.",
      "hooks": ["afterCompress"],
      "failClosed": false,
      "enabledByDefault": false
    }
  }
}
```

Plugins with `enabledByDefault: true` load automatically when no `--plugin` flags are given. See [Default Plugin Loading](#default-plugin-loading) below.

#### Standard Plugin Hooks

- `beforeFetch` - URL sources only, before `WebFetch`
- `beforeCompress` - after source resolution, before compression subagent prompt
- `afterCompress` - after CRUX output is generated
- `afterValidate` - after semantic validation completes

## Parallelism Limits

**Maximum parallel agents: 4**

When processing multiple files, spawn at most 4 `crux-cursor-rule-manager` subagent instances simultaneously. If there are more than 4 eligible files, process them in sequential batches:

- **Batch 1**: Files 1-4 (parallel)
- **Batch 2**: Files 5-8 (parallel, after Batch 1 completes)
- **Batch N**: Continue until all files processed

This prevents resource exhaustion and ensures reliable processing.

## Source Checksum Tracking

**CRUX files track the source file's checksum to avoid unnecessary updates.**

Each CRUX output file (`.crux.mdc` or `.crux.md`) includes a `sourceChecksum` field in its frontmatter containing the checksum of the source file. Before processing:

1. Agent gets current checksum using `crux-utils` skill (`--cksum` mode)
2. If existing CRUX file's `sourceChecksum` matches, the source is unchanged - **skip update**
3. If no match (or no existing CRUX file), proceed with compression
4. After compression, store the new `sourceChecksum` in the output frontmatter

This optimization prevents redundant recompression of unchanged files.

## Instructions

### Compression Level Resolution

Before processing any files, resolve the compression level:

1. **Check CLI flags** for `--<n>` where `n` is 1-100 (e.g., `--40`, `--10`). This is the highest priority.
2. **Check source frontmatter** for `crux: <n>` where `n` is a number. `crux: true` is equivalent to `crux: 25`.
3. **Default**: 25 for text sources, 80 for images (if neither CLI flag nor numeric frontmatter is present)

The resolved level is:
- Passed to each `crux-cursor-rule-manager` subagent as `compressionLevel: <n>`
- Recorded in output frontmatter as `cruxLevel: <n>`
- Used to set the target ratio: `target_ratio = level / 100`

**Validation**: If the level is outside 1-100, reject with an error message and do not proceed.

### Plugin Resolution (`--plugin`, `--no-plugin`)

Before source-type routing, resolve enabled plugins:

1. Parse all plugin flags from both forms:
   - `--plugin <name>` / `--plugin=<name>` (explicit enable)
   - `--no-plugin <name>` (disable a default-enabled plugin)
2. Normalize plugin names to lowercase and de-duplicate while preserving order.
3. Determine the active plugin set using one of two modes:

#### Default Plugin Loading

When **no `--plugin` flags** are present:

1. Read `.crux/plugins/registry.json` (if present).
2. Collect all plugins with `enabledByDefault: true`. These load automatically in registry order.
3. Remove any plugins named in `--no-plugin` flags.
   - `--no-plugin compression-level` → load defaults minus `compression-level`
   - `--no-plugin` on a non-default plugin → no-op (it was not going to load)
   - `--no-plugin` on a nonexistent plugin → warning, no error
4. If no default-enabled plugins exist and no `--no-plugin` flags are given, continue with the base compression flow (backward-compatible no-plugin path).

#### Explicit Plugin Mode

When **one or more `--plugin` flags** are present:

1. Load **only** the explicitly named plugins. Default-enabled plugins are **not** implicitly added.
   - `--plugin frontmatter-tagger` loads *only* `frontmatter-tagger`, even if `compression-level` is `enabledByDefault: true`
   - To get defaults plus extras: `--plugin compression-level --plugin frontmatter-tagger`
2. `--no-plugin` flags are ignored in explicit mode (the explicit list is authoritative). Emit a warning if both are provided.

This ensures full backward compatibility: existing scripts that pass `--plugin` flags get exactly the same behavior as before.

#### Common Validation (Both Modes)

4. Read `.crux/plugins/registry.json` (if not already loaded).
5. Validate each active plugin exists in `plugins`.
6. Validate each plugin declares at least one supported hook:
   `beforeFetch`, `beforeCompress`, `afterCompress`, `afterValidate`
7. If a requested plugin is unknown, fail fast with an actionable message:
   `"Unknown plugin: <name>. Add it to .crux/plugins/registry.json or remove the flag."`
8. Build an in-memory execution plan:
   - `pluginsByHook.beforeFetch[]`
   - `pluginsByHook.beforeCompress[]`
   - `pluginsByHook.afterCompress[]`
   - `pluginsByHook.afterValidate[]`

Pass the enabled plugin list to each compression and validation task so plugins can apply consistently across single-file and batch workflows.

### Plugin Execution Contract

When plugin hooks are present, execute them in this order:

1. `beforeFetch` (URL sources only)
2. `beforeCompress` (all source types)
3. Base compression workflow
4. `afterCompress` (if compression produced output)
5. Base semantic validation workflow (when applicable)
6. `afterValidate` (if validation produced a score)

Execution rules:
- When using default plugin loading, run plugins in registry order. When using explicit mode, run plugins in CLI order (first `--plugin` runs first for each hook).
- Provide each plugin with a structured context object:
  `sourcePath|sourceUrl`, `sourceType`, `outputPath`, `compressionLevel`,
  `format`, `force`, and current lifecycle data (`beforeTokens`, `afterTokens`,
  `confidence` when available).
- For the `compression-level` plugin specifically, the context also includes `contentType` (`"text"`, `"code"`, `"url"`, or `"image"`) so it can resolve default targets. See `.crux/plugins/compression-level.md` for full context schema.
- Plugin failures are recorded per plugin and hook in the final report.
- Continue base compression unless the plugin explicitly declares `failClosed: true`
  in the registry entry.
- Plugin hooks must not mutate `CRUX.md` or bypass core quality gates.

### Force Flag Pre-processing (`--force`)

When the `--force` flag is passed, **before any compression**:

1. **Identify target CRUX files**:
   - For sources in `.cursor/rules/`: the output is `[name].crux.mdc`
   - For sources elsewhere: the output is `[name].crux.md`
   - Also check for any leftover intermediary files (e.g., `.crux.md` in `.cursor/rules/`) and delete those too

2. **Delete existing CRUX files**:
   - Delete the CRUX output file for each source
   - Delete any leftover intermediary `.crux.md` files in `.cursor/rules/` (legacy cleanup)
   - This removes the cached `sourceChecksum`, forcing fresh compression
   - Log each deletion: "Deleted: rules/docs-sync.crux.mdc (--force)"

3. **Proceed with normal compression** (steps below)

This ensures compression agents always perform full recompression rather than skipping due to checksum match.

### When invoked with image file reference(s) (`@path/to/image.png`)

When any referenced file has a supported image extension (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`):

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

### When invoked with URL(s) (`https://...`)

When any argument is a URL (starts with `http://` or `https://`):

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

### When invoked with code file reference(s) (`@path/to/file.sh`, `@path/to/file.ts`, etc.)

When any referenced file has a supported code extension (`.sh`, `.bash`, `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.rs`, `.go`, `.java`, `.sql`, `.css`, `.scss`):

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

**Note**: Code compression does not use `alwaysApply` frontmatter, `crux: true` opt-in, or the Cursor adapter step. Code files are not included in `ALL` scans — they must be explicitly referenced.

### When invoked with markdown file reference(s) (`@path/to/file.md*`)

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
     - Output: <.crux.mdc if source is in .cursor/rules/, otherwise .crux.md>
     - For .cursor/rules/ sources: include alwaysApply from source frontmatter in output
     - For other sources: do NOT include alwaysApply or IDE-specific frontmatter
     - Format: <formatted (default) OR minified if --minified flag was passed>
     - Compression level: <resolved level, default 25>
     - Follow CRUX.md specification
     - Check source checksum vs existing CRUX sourceChecksum - skip if unchanged
     - Report before/after token counts using `crux-utils` skill (or "skipped - source unchanged")
     - If source lacks `crux: true` or `crux: <n>` frontmatter, add `crux: true` first
     - Ensure source uses .md extension (rename from .mdc if needed)
     ```

3. **Pre-processing for each file** (if needed):
   - If the file is `.mdc` but not `.crux.mdc`, rename to `.md` first
   - If the file lacks `crux: true` in frontmatter, add it
   - Then proceed with compression

4. **After compression completes**, spawn a **fresh `crux-cursor-rule-manager` instance for validation**:
   - Task the validation agent:
     ```
     Perform semantic validation on this CRUX file:
     - Source: <source .md file path>
     - CRUX: <generated CRUX output file path (.crux.mdc or .crux.md)>
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

### When invoked with `ALL`

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

## Eligibility Criteria

### Markdown Rules

A markdown file is eligible for CRUX compression if:
- Has `.md` or `.mdc` extension
- Has `crux: true` or `crux: <n>` (where `n` is 1-100) in YAML frontmatter
- Is not already a `.crux.md` or `.crux.mdc` file (outputs are not recompressed)
- For `ALL` scans: must be in `.cursor/rules/` directory
- For explicit file references: can be located anywhere

**Note**: `.mdc` files with `crux: true` or `crux: <n>` will be pre-processed (renamed to `.md`) before compression. The resulting `.crux.md` is the universal output. If the source is in `.cursor/rules/`, a `.crux.mdc` Cursor adapter file is also produced.

### Code Files

A code file is eligible for CRUX compression if:
- Has a supported code extension: `.sh`, `.bash`, `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.rs`, `.go`, `.java`, `.sql`, `.css`, `.scss`
- Is explicitly provided as a file reference (`@path/to/file.sh`)
- Is not already accompanied by a `.crux.md` file (unless `--force` is used)
- Can be located anywhere in the project

**Note**: Code files are NOT included in `ALL` scans. They must always be explicitly referenced. No `crux: true` frontmatter opt-in is needed. No Cursor adapter (`.crux.mdc`) is produced for code files.

### URLs (Webpages)

A URL is eligible for CRUX compression if:
- Starts with `http://` or `https://`
- Returns fetchable text content (HTML/markdown)
- Is explicitly provided as an argument (not via file reference)

**Note**: URL compression always outputs to `.crux/out/`. No `sourceChecksum` is used — `sourceUrl` replaces it in frontmatter. No Cursor adapter (`.crux.mdc`) is produced. URLs are NOT included in `ALL` scans.

### Images

An image file is eligible for CRUX compression if:
- Has a supported extension: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`
- Is not already accompanied by a `.crux.md` file (unless `--force` is used)
- Can be located anywhere in the project (not restricted to `.cursor/rules/`)

**Note**: Image compression is always invoked via direct file reference (`@path/to/image.png`). Images are NOT included in `ALL` scans, which only process markdown rules. Image compression produces a `.crux.md` file (not `.crux.mdc`).

## Adding New Files for Compression

To make a rule file eligible for CRUX compression:

1. Ensure the source file uses `.md` extension (not `.mdc`)
2. Add `crux: true` (or `crux: <n>` for a specific compression level) to the YAML frontmatter:
   ```yaml
   ---
   crux: true          # default 25% target
   alwaysApply: true   # or other frontmatter
   ---
   ```
   Or with a specific level:
   ```yaml
   ---
   crux: 40            # 40% target (more verbose output)
   alwaysApply: true
   ---
   ```
3. Run `/crux-compress ALL` or `/crux-compress @path/to/file.md`

## Source vs Output Convention

| Type | Extension | Example |
|------|-----------|---------|
| Source markdown (human-readable) | `.md` | `core-tenets.md` |
| Compressed Cursor rule (`.cursor/rules/` sources) | `.crux.mdc` | `core-tenets.crux.mdc` |
| Compressed (universal, non-rule sources) | `.crux.md` | `core-tenets.crux.md` |
| Source code | `.sh`, `.ts`, `.py`, etc. | `install.sh` |
| Compressed code (semantic structure) | `.crux.md` | `install.crux.md` |
| Source image | `.png`, `.jpg`, etc. | `diagram.png` |
| Compressed image (semantic description) | `.crux.md` | `diagram.crux.md` |
| Source URL (webpage) | URL | `https://agents.md/` |
| Compressed URL (webpage content) | `.crux.md` | `.crux/out/agents-md.crux.md` |

## Output Path Rules

| Source Type | Output Location | Example |
|-------------|----------------|---------|
| Local file (`@path/to/file.md`) | Same directory as source | `path/to/file.crux.md` |
| URL (`https://...`) | `.crux/out/` | `.crux/out/agents-md.crux.md` |
| No implied location | `.crux/out/` | `.crux/out/content.crux.md` |

The `.crux/out/` directory is created automatically if it does not exist. This provides a consistent default location for compression output when there's no local source file to place the output alongside.

**Direct output**: For sources in `.cursor/rules/`, compression produces `.crux.mdc` directly (with `alwaysApply` injected from source frontmatter). No intermediary `.crux.md` is created. For all other sources, compression produces `.crux.md`.

**Important**: The CRUX header in compressed files references the source file:
```
⟦CRUX:core-tenets.md
...content...
⟧
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
Compression (source in .cursor/rules/ → direct .crux.mdc):
└── crux-cursor-rule-manager → core-tenets.md → core-tenets.crux.mdc

Validation (after compression completes):
└── crux-cursor-rule-manager (fresh) → validate core-tenets.crux.mdc → confidence: 92%
```

### With URL(s)
When `/crux-compress https://agents.md/specification`:

```
Fetch URL content:
└── WebFetch → https://agents.md/specification → markdown content

Compression:
└── crux-cursor-rule-manager → agents-md-specification content → .crux/out/agents-md-specification.crux.md

Validation (after compression completes):
└── crux-cursor-rule-manager (fresh) → validate .crux/out/agents-md-specification.crux.md → confidence: 94%
```

### With `--force` flag
When `/crux-compress ALL --force`:

```
Force delete (pre-processing):
├── Deleted: .cursor/rules/docs-sync.crux.mdc
├── Deleted: .cursor/rules/version-bump.crux.mdc
├── Deleted: .cursor/rules/ignore-example-rules.crux.mdc
└── Deleted: .cursor/rules/example/coding-standards-demo.crux.mdc

Batch 1 (parallel, max 4):
├── crux-cursor-rule-manager → docs-sync.md → docs-sync.crux.mdc
├── crux-cursor-rule-manager → version-bump.md → version-bump.crux.mdc
├── crux-cursor-rule-manager → ignore-example-rules.md → ignore-example-rules.crux.mdc
└── crux-cursor-rule-manager → coding-standards-demo.md → coding-standards-demo.crux.mdc
```

**Note**: With `--force`, no files are skipped due to "source unchanged" since all CRUX files are deleted first.

## Semantic Validation

**Every compression is followed by validation** using a fresh agent instance:

1. Compression agent writes the CRUX output (`.crux.mdc` for `.cursor/rules/` sources, `.crux.md` otherwise) without confidence
2. Fresh validation agent compares CRUX output to source
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
- `crux-utils` skill - Token estimation and checksum utilities
