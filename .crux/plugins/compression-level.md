# Plugin: compression-level

**Registry entry**: `.crux/plugins/registry.json` → `compression-level`
**Enabled by default**: Yes
**Fail closed**: No (advisory — warns but does not block compression)
**Hooks**: `beforeCompress`, `afterCompress`

## Purpose

Enforce compression ratio targets and generate token metrics. This is the reference default-enabled plugin for the CRUX plugin architecture.

The plugin operates in two phases: it validates and prepares the compression target before compression begins, then measures the actual result afterward and injects metrics into the output frontmatter.

## Hook: `beforeCompress`

### Input Context

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `sourceFile` | string | orchestrator | Path to the source file being compressed |
| `compressionLevel` | number | orchestrator | Resolved level (1–100). Resolution order: CLI `--level` → frontmatter `cruxLevel` → default (25 for text/code, 80 for images) |
| `contentType` | string | orchestrator | `"text"`, `"code"`, `"url"`, or `"image"` |

### Behavior

1. Read `compressionLevel` from context
2. Validate range: `1 <= compressionLevel <= 100`. If invalid, emit warning and clamp to [1, 100]
3. If `crux: true` in source and no explicit level: resolve to 25 (text/code/url) or 80 (images)
4. Compute `targetRatio = compressionLevel / 100`
5. Return `{ targetRatio }` to merge into context

### Output Context

| Field | Type | Description |
|-------|------|-------------|
| `targetRatio` | number | `compressionLevel / 100` — the ratio the output must not exceed |

### Failure Mode

Advisory. If validation fails, log warning but do not block compression.

## Hook: `afterCompress`

### Input Context

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `sourceFile` | string | orchestrator | Path to source |
| `outputFile` | string | orchestrator | Path to compressed output |
| `compressionLevel` | number | orchestrator | Resolved level |
| `targetRatio` | number | from `beforeCompress` | Target ratio set earlier |

### Behavior

1. Run token counting on source file → `beforeTokens`
   - Method: `crux-utils.py --token-count <sourceFile>` (preferred)
   - Fallback: LLM-based estimation if utility unavailable
2. Run token counting on output file → `afterTokens`
3. Compute `ratio = afterTokens / beforeTokens * 100`
4. Compute `reducedBy = 100 - ratio`
5. Check `ratio <= compressionLevel`
6. Inject/update frontmatter fields in output:
   - `cruxLevel: <compressionLevel>`
   - `beforeTokens: <beforeTokens>`
   - `afterTokens: <afterTokens>`
   - `reducedBy: "<reducedBy>%"`
7. Return metrics to orchestrator

### Output Context

| Field | Type | Description |
|-------|------|-------------|
| `beforeTokens` | number | Token count of source |
| `afterTokens` | number | Token count of output |
| `reducedBy` | number | `100 - (afterTokens / beforeTokens * 100)` |
| `ratioMet` | boolean | Whether `afterTokens / beforeTokens * 100 <= compressionLevel` |
| `metricsInjected` | boolean | Whether frontmatter was updated with metrics |

### Failure Mode

Advisory (`failClosed: false`). If token counting fails or ratio exceeds target, log a warning. Compression output is still written — the plugin reports but does not block.

## CLI Integration

The `crux-utils.py` utility supports this plugin's token counting via:

```bash
# Default target (25%)
crux-utils.py --token-count --ratio <source> <crux>

# Custom target
crux-utils.py --token-count --ratio <source> <crux> --target <n>
```

The `--target` parameter accepts an integer 1-100 (default 25) and controls the pass/fail threshold shown in the compression summary.

## Default Compression Targets

| Content Type | Default Level | Rationale |
|-------------|--------------|-----------|
| Text (markdown, docs) | 25 | Aggressive compression for prose-heavy content |
| Code (rules, configs) | 25 | CRUX notation achieves high compression on structured rules |
| URL content | 25 | Fetched content is typically prose |
| Images | 80 | Limited compression potential for visual content descriptions |

## Interaction with Other Plugins

- **frontmatter-tagger**: Runs after `compression-level` in the `afterCompress` hook chain. Can read the metrics injected by this plugin.
- **quality-gate**: Operates on `afterValidate` hook (different phase). Can access `ratioMet` from context if needed.
- **release-notes**: Can aggregate `reducedBy` metrics across files for release summaries.
