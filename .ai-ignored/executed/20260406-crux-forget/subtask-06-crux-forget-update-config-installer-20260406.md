# Subtask: Update Config and Installer

## Metadata
- **Subtask ID**: 06
- **Feature**: crux-forget
- **Assigned Subagent**: generalPurpose
- **Dependencies**: 01
- **Created**: 20260406

## Objective
Update the memories configuration file (`.crux/crux-memories.json`), the installer script (`install.py`), and regenerate the compressed installer spec (`install.crux.md`) to include the new `/crux-forget` command.

## Deliverables Checklist
- [x] `.crux/crux-memories.json` — `forget` command entry added to the `commands` section
- [x] `install.py` — `DEFAULT_MEMORIES_CONFIG` template updated to include `/crux-forget` in commands
- [x] `install.py` — `RELEASE_FILES` list updated to include `.cursor/commands/crux-forget.md`
- [x] `install.py` — `standard_files` (backup list) NOT modified (memory commands are not in this list — only core CRUX files are)
- [x] `install.crux.md` — Regenerated from updated `install.py` (surgical diff update to CRUX notation)
- [x] **FLAG**: `scripts/create-crux-zip.py` and `.github/workflows/version-bump.yml` NOT modified — user must explicitly request this per zip-contents-protection rule

## Definition of Done
- [x] Config file includes forget command entry
- [x] Installer script includes the new command file in all relevant lists
- [x] `install.crux.md` is in sync with `install.py`
- [x] No linter errors in modified files
- [x] Warning logged about zip/workflow files needing manual update

## Implementation Notes

### File 1: `.crux/crux-memories.json`

**Add to `commands` section (after the `mindReader` entry, around line 38):**

```json
"forget": {
  "file": ".cursor/commands/crux-forget.md",
  "default": "/crux-forget",
  "description": "Remove incorrect or unwanted memories"
}
```

### File 2: `install.py`

**Three changes needed:**

**A. `RELEASE_FILES` list:**
Find the list that defines files included in releases. Add:
```python
".cursor/commands/crux-forget.md",
```
Place it after the existing `crux-mindreader.md` entry.

**B. `standard_files` (backup list):**
Do NOT add to `standard_files`. This list only contains core CRUX files (CRUX.md, AGENTS.md, hooks, rules, crux-utils). The existing memory commands (`crux-dream.md`, `crux-mindreader.md`) are not in `standard_files` — they are only in `RELEASE_FILES`. Follow the same pattern.

**C. `DEFAULT_MEMORIES_CONFIG` template:**
Find the `DEFAULT_MEMORIES_CONFIG` dictionary/string that serves as the template for new `.crux/crux-memories.json` files created by `--with-memories`. Currently the commands list includes `/crux-dream` and `/crux-mindreader`. Add `/crux-forget`:

The config template should have a `forget` command entry matching the structure of `dream` and `mindReader`:
```python
"forget": {
    "file": ".cursor/commands/crux-forget.md",
    "default": "/crux-forget",
    "description": "Remove incorrect or unwanted memories"
}
```

### File 3: `install.crux.md`

**CRITICAL**: This file is generated from `install.py` (has `sourceChecksum` in frontmatter). After editing `install.py`:

1. Apply surgical diff updates to the CRUX notation in `install.crux.md` to match the changes:
   - In `M.RELEASE_FILES` — add `crux-forget.md` to the commands list
   - In `M.standard_files(backup)` — do NOT add (memory commands are not in this list)
   - In `E.DEFAULT_MEMORIES_CONFIG` — add `/crux-forget` to the commands list
2. Update the `sourceChecksum` in the frontmatter to reflect the new `install.py` checksum
3. Use the `crux-utils` skill to compute the new checksum

### ZIP PROTECTION WARNING

**DO NOT** modify:
- `scripts/create-crux-zip.py`
- `.github/workflows/version-bump.yml`

Per the `zip-contents-protection` rule, adding files to the distribution zip requires explicit user request. After completing this subtask, report to the user:

> "The new command file `.cursor/commands/crux-forget.md` has been added to the installer's file lists but is NOT yet included in the release zip or CI workflow. To distribute this file in releases, you need to explicitly request adding it to `scripts/create-crux-zip.py` and `.github/workflows/version-bump.yml RELEASE_PATHS`."

## Testing Strategy
**IMPORTANT**: Do NOT trigger global test suites during parallel execution. Instead:
- Verify `.crux/crux-memories.json` is valid JSON after editing
- Verify `install.py` syntax is valid (run `python3 -c "import py_compile; py_compile.compile('install.py')"`)
- Verify `install.crux.md` CRUX notation includes the new file references
- Verify RELEASE_FILES and DEFAULT_MEMORIES_CONFIG reference `crux-forget` (standard_files should NOT be modified)

## Execution Notes

### Agent Session Info
- Agent: generalPurpose (subtask-06 executor)
- Started: 2026-04-07
- Completed: 2026-04-07

### Work Log
1. Added `forget` command entry to `.crux/crux-memories.json` after `mindReader`
2. Added `.cursor/commands/crux-forget.md` to `RELEASE_FILES` in `install.py` (after `crux-mindreader.md`)
3. Added `forget` command dict to `DEFAULT_MEMORIES_CONFIG` in `install.py` (after `mindReader`)
4. Did NOT modify `standard_files` (backup list) — follows existing pattern where memory commands are only in `RELEASE_FILES`
5. Applied surgical CRUX diffs to `install.crux.md`:
   - `M.RELEASE_FILES` commands list: added `crux-forget.md`
   - `E.DEFAULT_MEMORIES_CONFIG` commands list: added `/crux-forget`
   - `M.standard_files(backup)`: NOT modified (correct — memory commands not in this list)
6. Updated `sourceChecksum` in `install.crux.md` frontmatter from `3375235347` to `1533497645`
7. Verified: JSON valid, Python syntax valid, no linter errors

### Blockers Encountered
None.

### Files Modified
- `.crux/crux-memories.json`
- `install.py`
- `install.crux.md`

### ZIP Protection Notice
`scripts/create-crux-zip.py` and `.github/workflows/version-bump.yml` were NOT modified per the zip-contents-protection rule. The user must explicitly request adding `.cursor/commands/crux-forget.md` to these files to include it in releases.

### Adversarial Verification (Judge)
- **Verifier**: zoto-spec-judge
- **Date**: 2026-04-07
- **Verdict**: **Verified**

**Deliverables Checklist — independently confirmed:**

`.crux/crux-memories.json`:
- [x] `forget` command entry exists with correct file, default, and description (lines 42-46)
- [x] JSON is valid (verified via `json.load()`)

`install.py`:
- [x] `RELEASE_FILES` includes `.cursor/commands/crux-forget.md` (line 434, after mindreader)
- [x] `standard_files` does NOT include crux-forget.md — only `crux-compress.md` is in standard_files (lines 228-236); memory commands follow existing pattern of being RELEASE_FILES-only
- [x] `DEFAULT_MEMORIES_CONFIG` includes `forget` command entry with matching structure (lines 637-641)
- [x] Python syntax is valid (verified via `py_compile.compile()`)

`install.crux.md`:
- [x] `M.RELEASE_FILES` includes `crux-forget.md` in commands list (line 208)
- [x] `M.standard_files(backup)` does NOT include `crux-forget.md` (line 224 — lists `crux-compress.md,crux-dream.md,crux-mindreader.md` only)
- [x] `sourceChecksum` updated to `1533497645` — independently verified by running `crux-utils.py --cksum install.py`, output matches
- [x] `E.DEFAULT_MEMORIES_CONFIG` includes `/crux-forget` in commands list (line 155)

Protected files:
- [x] `scripts/create-crux-zip.py` does NOT contain any `crux-forget` references (verified via grep)
- [x] `.github/workflows/version-bump.yml` does NOT contain any `crux-forget` references (verified via grep)

**Definition of Done — independently confirmed:**
- [x] Config file includes forget command entry
- [x] Installer script includes the new command file in all relevant lists
- [x] `install.crux.md` is in sync with `install.py` (sourceChecksum verified)
- [x] No linter errors (verified via ReadLints)
- [x] ZIP protection warning logged in execution notes

**Observation (pre-existing, not introduced by this subtask):**
The `M.standard_files(backup)` section in `install.crux.md` lists files (`crux-dream.md`, `crux-mindreader.md`, memory skills, `crux-cursor-memory-manager.md`) that are NOT actually in the `standard_files` list in `install.py`. This is a pre-existing inaccuracy in the CRUX notation — the standard_files backup list in install.py only contains core CRUX files, not memory commands or skills. This was not introduced by subtask 06.
