# Subtask: Update Command & Agent Specs for Default Plugins

## Metadata
- **Subtask ID**: 07
- **Feature**: Memories & Plugin Integration
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 06
- **Created**: 20260404

## Objective

Update the `/crux-compress` command spec and the `crux-cursor-rule-manager` agent spec to support the new default-plugin loading mechanism and to delegate ratio enforcement/metrics to the `compression-level` plugin when active.

## Deliverables Checklist
- [x] `.cursor/commands/crux-compress.md` updated:
  - Plugin Resolution section covers default-enabled plugins
  - When no `--plugin` flags: load `enabledByDefault: true` plugins from registry
  - When `--plugin` flags present: load only those (explicit overrides defaults)
  - Optional `--no-plugin <name>` to disable a specific default
  - Plugin context object includes `compressionLevel` for `compression-level` plugin
- [x] `.cursor/agents/crux-cursor-rule-manager.md` updated:
  - When `compression-level` plugin is active: delegate ratio checking and metrics to plugin
  - When no plugin active: agent performs ratio checking and metrics itself (backward compat)
  - Clear delineation of what the agent does vs what the plugin does
- [ ] Both specs maintain full backward compatibility — existing commands work identically
- [x] CRUX compressed versions updated if `.crux.md`/`.crux.mdc` files exist for these sources

## Definition of Done
- [x] Command spec clearly documents default plugin loading
- [x] Agent spec clearly documents plugin delegation
- [ ] A user running `/crux-compress @file.md --40` gets identical results as before
- [ ] A user running `/crux-compress @file.md` (no flags) gets identical results as before
- [x] CRUX files for modified sources are regenerated
- [x] No linter errors in modified files

## Implementation Notes

### Command Spec Changes (`crux-compress.md`)

**Plugin Resolution section** (currently lines ~140-162) needs an addition before step 3:

```
### Default Plugin Loading

Before source-type routing, resolve enabled plugins:

1. Parse all `--plugin` and `--no-plugin` flags.
2. If NO `--plugin` flags are present:
   a. Read `.crux/plugins/registry.json`
   b. Load all plugins with `enabledByDefault: true`
   c. Remove any plugins named in `--no-plugin` flags
3. If `--plugin` flags ARE present:
   a. Load only explicitly named plugins
   b. Ignore `enabledByDefault` settings
   c. `--no-plugin` has no effect (explicit list is authoritative)
4. Continue with existing validation (check registry, validate hooks, etc.)
```

### Agent Spec Changes (`crux-cursor-rule-manager.md`)

Add a section on plugin awareness:

```
### Plugin-Aware Behavior

When the `compression-level` plugin is active (indicated by orchestrator context):
- Do NOT perform ratio checking or generate token metrics yourself
- Compress toward the target `compressionLevel` as usual
- The plugin will handle: token counting, ratio validation, and frontmatter injection
  for `cruxLevel`, `beforeTokens`, `afterTokens`, `reducedBy`

When NO `compression-level` plugin is active:
- Perform all ratio checking and metrics generation as currently specified
- This ensures backward compatibility if the plugin is disabled
```

### CRUX File Updates
Check if these source files have corresponding `.crux.md`/`.crux.mdc`:
- `.cursor/commands/crux-compress.md` → likely `.cursor/commands/crux-compress.crux.md`?
- `.cursor/agents/crux-cursor-rule-manager.md` → check for `.crux.md`/`.crux.mdc`

If CRUX files exist, they must be regenerated after source edits (per foundational rule 4).

### Files to Read Before Editing
- `.cursor/commands/crux-compress.md` — full file
- `.cursor/agents/crux-cursor-rule-manager.md` — full file
- Subtask 01 output — design decisions for default-enabled mechanism
- Subtask 06 output — plugin behavior spec

### Backward Compatibility Verification
The key invariant: without any new flags, the compression output (file content and frontmatter) must be identical. The `compression-level` plugin produces the same metrics the agent previously produced itself. Verify by tracing the data flow:
1. Level resolved: same (CLI → frontmatter → default)
2. Compression: same (agent compresses to target)
3. Metrics: same values, now produced by plugin instead of agent
4. Output frontmatter: same fields and values

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Read modified specs for internal consistency
- Verify CRUX files are regenerated if they exist
- Defer full backward-compat testing to subtask 08

## Execution Notes

### Agent Session Info
- Agent: generalPurpose (subtask executor)
- Started: 2026-04-04
- Completed: 2026-04-04

### Work Log

1. **Read all dependency context** — subtask 01 (design document), subtask 06 (implementation details), `.crux/plugins/compression-level.md` (plugin behavior spec).

2. **Updated `.cursor/commands/crux-compress.md`**:
   - Added `--no-plugin compression-level` usage example to the Usage block
   - Added `--no-plugin <name>` row to the Flags table
   - Updated Plugin Registry example JSON to show `enabledByDefault` field and the `compression-level` plugin entry
   - Added note linking to Default Plugin Loading section
   - Rewrote Plugin Resolution section (`--plugin`, `--no-plugin`) with two clearly separated modes:
     - **Default Plugin Loading**: when no `--plugin` flags, loads `enabledByDefault: true` plugins from registry, supports `--no-plugin` to opt out
     - **Explicit Plugin Mode**: when `--plugin` flags present, only those plugins load (overrides defaults), `--no-plugin` ignored with warning
   - Added Common Validation subsection for registry lookup, hook validation, and execution plan building
   - Updated Plugin Execution Contract: default plugins run in registry order, explicit plugins run in CLI order
   - Added `contentType` context note for `compression-level` plugin specifically, referencing `.crux/plugins/compression-level.md`

3. **Updated `.cursor/agents/crux-cursor-rule-manager.md`**:
   - Added "Plugin-Aware Behavior" section between step 3 (compression) and step 4 (plugin hooks)
   - Documented "With plugin active" behavior: agent skips ratio checking, token counting, and metrics frontmatter injection — plugin handles those
   - Documented "Without plugin" behavior: agent performs all ratio checking and metrics generation itself (backward compat)
   - Explained the delegation model and backward compatibility guarantee
   - Updated Compression Checklist: annotated `Target ratio met`, `beforeTokens`, `afterTokens`, and `reducedBy` items with "*skip if `compression-level` plugin is active*"

4. **Checked for CRUX compressed files** — no `.crux.md` or `.crux.mdc` exists for either `crux-compress.md` or `crux-cursor-rule-manager.md`. No regeneration needed.

5. **Ran linter checks** — no errors in either modified file.

### Backward Compatibility Analysis

Traced the data flow to verify backward compatibility:

| Scenario | Before | After | Result |
|----------|--------|-------|--------|
| `/crux-compress @file.md --40` (ratio met) | Agent resolves level, compresses, checks ratio (hard gate), injects metrics | `compression-level` plugin loads as default, produces same metrics | Identical output |
| `/crux-compress @file.md --40` (ratio NOT met) | Agent blocks file writing (hard gate) | Plugin writes file with warning (`failClosed: false`) | **Intentional change**: advisory enforcement is more permissive |
| `/crux-compress @file.md` (no flags, ratio met) | Agent uses default level 25 | `compression-level` plugin loads by default, validates, injects metrics | Identical output |
| `/crux-compress @file.md --plugin frontmatter-tagger` | Agent loads frontmatter-tagger only | Same — explicit mode, only named plugins load | Identical output |
| `/crux-compress @file.md --no-plugin compression-level` | N/A (new flag) | Defaults minus compression-level → agent does metrics itself (hard gate) | Same as pre-plugin behavior |

**Note**: The quality gate behavioral change (hard gate → advisory) when the default `compression-level` plugin is active is intentional per the plan's decision to use `failClosed: false`. Users who need the hard gate can use `--no-plugin compression-level` to restore the pre-plugin enforcement.

### Blockers Encountered
None.

### Files Modified
- `.cursor/commands/crux-compress.md` — default plugin loading, `--no-plugin` flag, updated registry example, plugin resolution rewrite
- `.cursor/agents/crux-cursor-rule-manager.md` — plugin-aware behavior section, updated compression checklist

---

### Adversarial Verification (integrity-expert)
- **Verifier**: integrity-expert subagent
- **Date**: 2026-04-05
- **Verdict**: **Partial** — 10 of 12 items verified; 2 backward-compatibility items remain unchecked

#### Independently Verified Items

| # | Item | Status | Evidence |
|---|------|--------|----------|
| D1 | Command spec: Plugin Resolution covers defaults | ✅ | Lines 148–195 rewritten with Default Plugin Loading + Explicit Plugin Mode subsections |
| D2 | Command spec: No `--plugin` → load `enabledByDefault` | ✅ | Lines 160–168: reads registry, collects `enabledByDefault: true`, supports `--no-plugin` removal |
| D3 | Command spec: `--plugin` → explicit only | ✅ | Lines 172–178: "Load only the explicitly named plugins. Default-enabled plugins are not implicitly added." |
| D4 | Command spec: `--no-plugin <name>` flag | ✅ | Usage example (line 28), flags table (line 39), Default Plugin Loading section (lines 163–167) |
| D5 | Command spec: Plugin context includes `compressionLevel` + `contentType` | ✅ | Lines 211–214: context object lists `compressionLevel`; line 214 adds `contentType` for `compression-level` specifically |
| D6 | Command spec: `compression-level` in registry example | ✅ | Lines 81–86: `compression-level` entry with `enabledByDefault: true`, `hooks: ["beforeCompress", "afterCompress"]` |
| D7 | Agent spec: Plugin-Aware Behavior section | ✅ | Lines 74–91: new section inserted between compression steps and plugin hook tasks |
| D8 | Agent spec: Plugin-active delegation | ✅ | Lines 78–84: agent skips ratio checking, token counting, metrics injection; plugin handles all |
| D9 | Agent spec: No-plugin backward compat | ✅ | Lines 86–89: agent performs all ratio checking and metrics generation itself |
| D10 | Agent spec: Clear delineation | ✅ | Prose section (74–91) + compression checklist annotations at lines 193, 198–200 with "*skip if plugin active*" |
| D11 | CRUX compressed files | ✅ | No `.crux.md` or `.crux.mdc` exists for either `crux-compress.md` or `crux-cursor-rule-manager.md`. Confirmed via glob search. No regeneration needed. |
| D12 | No linter errors | ✅ | `ReadLints` returned clean for both files |
| DoD1 | Command spec documents default plugin loading | ✅ | Comprehensive — Default Plugin Loading subsection with 4 numbered steps |
| DoD2 | Agent spec documents plugin delegation | ✅ | Clear with/without sections and annotated checklist |
| DoD5 | CRUX files regenerated | ✅ | N/A — no CRUX files exist for these sources |
| DoD6 | No linter errors | ✅ | Confirmed clean |

#### Unchecked Items — Quality Gate Behavioral Regression

| # | Item | Status | Finding |
|---|------|--------|---------|
| D_compat | Both specs maintain full backward compatibility | ⚠️ UNCHECKED | See finding below |
| DoD3 | `/crux-compress @file.md --40` identical results | ⚠️ UNCHECKED | Identical when ratio IS met; differs when ratio is NOT met |
| DoD4 | `/crux-compress @file.md` (no flags) identical results | ⚠️ UNCHECKED | Same edge case as above |

**Finding: Quality gate enforcement weakened by default plugin**

The pre-plugin agent behavior (still present in agent spec line 72) states:

> "If target ratio not achieved, DO NOT write the CRUX file"

This is a **hard gate** — no output is produced if compression doesn't hit the target.

With the `compression-level` plugin now loading by default, the agent **skips this check** (checklist line 193: "*skip if `compression-level` plugin is active*"). The plugin's `afterCompress` hook performs the ratio check, but the plugin spec (`.crux/plugins/compression-level.md`, lines 79–81) states:

> "Advisory (`failClosed: false`). If token counting fails or ratio exceeds target, log a warning. Compression output is still written — the plugin reports but does not block."

This means:
- **Before** (no plugins): ratio not met → CRUX file NOT written (hard gate)
- **After** (default plugin active): ratio not met → CRUX file IS written + warning logged (advisory)

This is a **behavioral regression** for the edge case where compressed output exceeds the target ratio. The subtask's backward compatibility analysis only traces the happy path (ratio met) and does not acknowledge this difference.

**Impact**: Low (this edge case is relatively rare and the advisory behavior may be intentionally more permissive), but the backward-compatibility claim is technically inaccurate. The subtask should either:
1. Acknowledge the behavioral change explicitly and document it as intentional, OR
2. Set `failClosed: true` on the `compression-level` plugin to match the hard-gate behavior, OR
3. Have the agent retain its own quality gate as a fallback even when the plugin is active

#### Minor Observation — Redundant `cruxLevel` Injection

Both the agent (line 82: "Do still add ... `cruxLevel` ... to frontmatter") and the plugin (`afterCompress` step 6: "Inject/update ... `cruxLevel`") write the `cruxLevel` field. Since both set the same value (`compressionLevel`), this is functionally harmless but represents duplicated work. The spec could clarify that the agent writes `cruxLevel` first and the plugin leaves it as-is, or that the agent omits it when the plugin is active.
