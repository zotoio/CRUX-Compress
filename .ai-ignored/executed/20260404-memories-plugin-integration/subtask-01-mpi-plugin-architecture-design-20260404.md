# Subtask: Plugin Architecture Design — Default-Enabled Mechanism

## Metadata
- **Subtask ID**: 01
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: None
- **Created**: 20260404

## Objective

Design and document the `enabledByDefault` extension to the existing CRUX plugin architecture. This design becomes the foundation for subtask 06 (implementing the `compression-level` reference plugin) and subtask 07 (updating command/agent specs).

## Deliverables Checklist
- [x] Design document (in this subtask's Execution Notes) covering:
  - Registry schema extension (`enabledByDefault` field)
  - Default plugin loading behavior when no `--plugin` flags are present
  - Interaction between explicit `--plugin` flags and defaults
  - Optional `--no-plugin <name>` mechanism for disabling defaults
  - Plugin context object extensions for compression-level data
- [x] Updated `.crux/plugins/registry.json` with `enabledByDefault` field on existing plugins (all set to `false` for backward compat) and the new `compression-level` entry (set to `true`)
- [x] `compression-level` plugin hook specification: what `beforeCompress` and `afterCompress` do

## Definition of Done
- [x] Registry schema extension is documented and consistent
- [x] Existing 3 plugins have `enabledByDefault: false` (no behavior change)
- [x] `compression-level` plugin entry specifies hooks and `enabledByDefault: true`
- [x] No changes to any agent/command spec files (those happen in subtask 07)
- [x] No linter errors in modified files

### Adversarial Verification (integrity-expert) — 2026-04-04

**Verdict: VERIFIED**

All 3 deliverables and 5 definition-of-done items independently confirmed.

| # | Item | Evidence | Result |
|---|------|----------|--------|
| D1 | Design document covers all 5 required topics | Sections 1–5 in Execution Notes (lines 122–253) cover: schema extension, default loading, explicit override, `--no-plugin`, context extensions | PASS |
| D2 | `registry.json` updated correctly | `git diff HEAD` confirms: 3 existing plugins gained `enabledByDefault: false` only; new `compression-level` entry with `enabledByDefault: true`; all pre-existing `description`, `hooks`, `failClosed` values untouched; `python3 -m json.tool` validates JSON | PASS |
| D3 | Hook specification for `compression-level` | `beforeCompress` (validate range, compute `targetRatio`) and `afterCompress` (token count, ratio check, frontmatter injection) fully specified | PASS |
| DoD1 | Schema documented & consistent | Design doc table (line 134) matches actual registry fields | PASS |
| DoD2 | Existing 3 plugins `enabledByDefault: false` | Confirmed in file lines 13, 19, 25 | PASS |
| DoD3 | `compression-level` has hooks + `enabledByDefault: true` | Confirmed in file lines 4–8 | PASS |
| DoD4 | No spec file changes | `git diff --name-only HEAD -- .cursor/commands/crux-compress.md .cursor/agents/crux-cursor-rule-manager.md` returned empty | PASS |
| DoD5 | No linter errors | `ReadLints` on `.crux/plugins/registry.json` returned zero errors | PASS |

## Implementation Notes

### Current State
- `.crux/plugins/registry.json` has 3 plugins: `frontmatter-tagger`, `quality-gate`, `release-notes`
- Each has `description`, `hooks[]`, `failClosed`
- No `enabledByDefault` field exists
- Plugins are only loaded when `--plugin <name>` is explicitly passed

### Design Constraints
- Zero breaking changes: existing `--plugin` usage must work identically
- When no `--plugin` flags: load `enabledByDefault: true` plugins silently
- When `--plugin` flags present: load ONLY those (explicit overrides defaults)
- `--no-plugin <name>`: disable a specific default (optional, design only)

### What the `compression-level` Plugin Does

**Hook: `beforeCompress`**
- Receive `compressionLevel` from orchestrator context
- Validate range (1-100), reject invalid
- Resolve `crux: true` → 25 (text/code/URL) or 80 (images) if not already resolved
- Set `targetRatio = compressionLevel / 100` in plugin context

**Hook: `afterCompress`**
- Run `crux-utils --token-count` on source and output (or use LLM estimate)
- Calculate `ratio = afterTokens / beforeTokens * 100`
- Calculate `reducedBy = 100 - ratio`
- Check `ratio <= compressionLevel`
- Inject/update frontmatter: `cruxLevel`, `beforeTokens`, `afterTokens`, `reducedBy`
- Report pass/fail for quality gate (advisory; `failClosed: false`)

### Registry Schema After This Subtask

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
    },
    "quality-gate": {
      "description": "Apply additional policy checks after validation.",
      "hooks": ["afterValidate"],
      "failClosed": false,
      "enabledByDefault": false
    },
    "release-notes": {
      "description": "Collect per-file reduction metrics for release summaries.",
      "hooks": ["afterCompress", "afterValidate"],
      "failClosed": false,
      "enabledByDefault": false
    }
  }
}
```

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Validate registry.json is well-formed JSON after edit
- Verify all existing plugins retain their original fields
- Defer full test suite execution to subtask 08

## Execution Notes

### Agent Session Info
- Agent: generalPurpose (subtask executor)
- Started: 2026-04-04
- Completed: 2026-04-04

### Work Log

1. Read current `.crux/plugins/registry.json` — confirmed 3 existing plugins without `enabledByDefault`
2. Updated registry with `enabledByDefault` field on all 4 plugins (3 existing → `false`, 1 new `compression-level` → `true`)
3. Validated JSON well-formedness and field correctness via assertions
4. Wrote design document (below)

### Blockers Encountered
None.

### Files Modified
- `.crux/plugins/registry.json` — added `enabledByDefault` to 3 existing plugins; added `compression-level` entry

---

## Design Document: `enabledByDefault` Plugin Extension

### 1. Registry Schema Extension

Each plugin entry in `.crux/plugins/registry.json` gains a new required field:

```json
"enabledByDefault": true | false
```

**Full schema per plugin entry:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | yes | Human-readable purpose |
| `hooks` | string[] | yes | Hook points: `beforeCompress`, `afterCompress`, `afterValidate` |
| `failClosed` | boolean | yes | If `true`, plugin failure aborts compression |
| `enabledByDefault` | boolean | yes | If `true`, plugin loads automatically when no explicit `--plugin` flags are given |

Backward compatibility: all three existing plugins have `enabledByDefault: false`, so behavior is identical to the pre-extension state.

### 2. Default Plugin Loading Behavior

**When no `--plugin` flags are present:**

```
active_plugins = [p for p in registry if p.enabledByDefault == true]
```

The orchestrator collects all `enabledByDefault: true` plugins from the registry and loads them in registry order. No user action needed — default plugins activate silently.

**When one or more `--plugin <name>` flags are present:**

```
active_plugins = [explicitly named plugins only]
```

Explicit flags **completely override** defaults. This means:
- `--plugin frontmatter-tagger` loads *only* `frontmatter-tagger` (even though `compression-level` is `enabledByDefault: true`)
- To get defaults *plus* extras: `--plugin compression-level --plugin frontmatter-tagger`

This design is zero-breaking-change: existing scripts that pass `--plugin` flags get exactly the same behavior.

### 3. `--no-plugin <name>` Mechanism

Optional opt-out for disabling specific defaults without switching to fully-explicit mode.

**Behavior:**

```
active_plugins = [p for p in registry if p.enabledByDefault] - [names from --no-plugin]
```

- `--no-plugin compression-level` → load defaults minus `compression-level`
- `--no-plugin` only applies when no `--plugin` flags are present
- If both `--plugin` and `--no-plugin` are given, `--plugin` takes precedence (explicit mode); `--no-plugin` is ignored with a warning

**Edge cases:**
- `--no-plugin nonexistent` → warning, no error
- `--no-plugin` on a non-default plugin → no-op (it wasn't going to load anyway)

### 4. Plugin Context Object Extensions

The orchestrator already passes a context object to plugin hooks. For the `compression-level` plugin, the context is extended:

**`beforeCompress` context (input to plugin):**

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `sourceFile` | string | orchestrator | Path to the source file being compressed |
| `compressionLevel` | number | orchestrator | Resolved level (1–100). Resolved by core: CLI `--level` → frontmatter `cruxLevel` → default (25 for text/code, 80 for images) |
| `contentType` | string | orchestrator | `"text"`, `"code"`, `"url"`, or `"image"` |

**`beforeCompress` context (output from plugin, merged back):**

| Field | Type | Description |
|-------|------|-------------|
| `targetRatio` | number | `compressionLevel / 100` — the ratio the output must not exceed |

**`afterCompress` context (input to plugin):**

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `sourceFile` | string | orchestrator | Path to source |
| `outputFile` | string | orchestrator | Path to compressed output |
| `compressionLevel` | number | orchestrator | Resolved level |
| `targetRatio` | number | from `beforeCompress` | Target ratio set earlier |

**`afterCompress` context (output from plugin, merged back):**

| Field | Type | Description |
|-------|------|-------------|
| `beforeTokens` | number | Token count of source |
| `afterTokens` | number | Token count of output |
| `reducedBy` | number | `100 - (afterTokens / beforeTokens * 100)` |
| `ratioMet` | boolean | Whether `afterTokens / beforeTokens * 100 <= compressionLevel` |
| `metricsInjected` | boolean | Whether frontmatter was updated with metrics |

### 5. `compression-level` Plugin Hook Specification

#### `beforeCompress` Hook

**Purpose:** Validate and prepare compression target.

**Steps:**
1. Read `compressionLevel` from context
2. Validate range: `1 <= compressionLevel <= 100`. If invalid, emit warning and clamp to [1, 100]
3. Compute `targetRatio = compressionLevel / 100`
4. Return `{ targetRatio }` to merge into context

**Failure mode:** Advisory (`failClosed: false`). If validation fails, log warning but do not block compression.

#### `afterCompress` Hook

**Purpose:** Measure actual compression and inject metrics into frontmatter.

**Steps:**
1. Run token counting on source file → `beforeTokens`
2. Run token counting on output file → `afterTokens`
3. Compute `ratio = afterTokens / beforeTokens * 100`
4. Compute `reducedBy = 100 - ratio`
5. Check `ratio <= compressionLevel`
6. Inject/update frontmatter fields in output:
   - `cruxLevel: <compressionLevel>`
   - `beforeTokens: <beforeTokens>`
   - `afterTokens: <afterTokens>`
   - `reducedBy: "<reducedBy>%"`
7. Return `{ beforeTokens, afterTokens, reducedBy, ratioMet, metricsInjected: true }`

**Failure mode:** Advisory (`failClosed: false`). If token counting fails or ratio exceeds target, log a warning. Compression output is still written — the plugin reports but does not block.

**Token counting method:** Use `crux-utils.py --token-count <file>` (preferred) or fall back to LLM-based estimation if the utility is unavailable. Subtask 06 implements the actual mechanism.
