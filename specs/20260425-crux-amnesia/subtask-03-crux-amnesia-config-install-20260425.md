# Subtask: Config and Install Integration

## Metadata
- **Subtask ID**: 03
- **Feature**: crux-amnesia
- **Assigned Subagent**: crux-software-engineer
- **Dependencies**: 01, 02
- **Created**: 20260425

## Objective
Ensure the amnesia command is properly registered in the memory system configuration (`.crux/crux-memories.json`) and that the installer (`install.py`) includes amnesia-related files in its `MEMORY_FILE_PREFIXES` tuple, fallback file list, and default config template.

## Deliverables Checklist
- [x] `commands.amnesia` entry exists in `.crux/crux-memories.json` with correct `file`, `default`, and `description` fields
- [x] `commands.amnesia.file` points to `.cursor/commands/crux-amnesia.md`
- [x] `commands.amnesia.default` is `/crux-amnesia`
- [x] `commands.amnesia.description` reads "Toggle session-scoped ambient memory usage"
- [x] `install.py` `MEMORY_FILE_PREFIXES` tuple includes `.cursor/commands/crux-amnesia.md`
- [x] `install.py` fallback file list in `get_release_files()` includes `.cursor/commands/crux-amnesia.md`
- [x] `install.py` `DEFAULT_MEMORIES_CONFIG` dict includes `commands.amnesia` entry matching the config file

## Definition of Done
- [x] Config entry exists and is valid JSON
- [x] Installer `MEMORY_FILE_PREFIXES` includes the amnesia command path
- [x] Installer fallback list includes the amnesia command path
- [x] Installer default config template includes `commands.amnesia`
- [x] Config and installer are consistent (same file path, same description)
- [x] No JSON parse errors in `.crux/crux-memories.json`

## Implementation Notes
- The `commands.amnesia` entry in config follows the same schema as all other command entries (`dream`, `recall`, `remember`, `meditate`, `forget`): `file`, `default`, `description`
- The `MEMORY_FILE_PREFIXES` tuple in `install.py` is used by `is_memory_file()` to determine which files are memory-system-specific and should only be installed when `--with-memories` is used or memories are already installed
- The fallback file list in `get_release_files()` is used when the dist manifest cannot be fetched from CDN/GitHub — it must include all distributed files to ensure offline installations work
- The `DEFAULT_MEMORIES_CONFIG` template is used when `--with-memories` creates a fresh `.crux/crux-memories.json` — it must include the amnesia command entry so new installations have the command registered from the start

### Config Entry
```json
"amnesia": {
    "file": ".cursor/commands/crux-amnesia.md",
    "default": "/crux-amnesia",
    "description": "Toggle session-scoped ambient memory usage"
}
```

### MEMORY_FILE_PREFIXES Entry
```python
".cursor/commands/crux-amnesia.md",
```

## Testing Strategy
- Parse `.crux/crux-memories.json` as JSON and verify `commands.amnesia` exists with correct fields
- Grep `install.py` for `crux-amnesia` and verify it appears in `MEMORY_FILE_PREFIXES`, the fallback list, and `DEFAULT_MEMORIES_CONFIG`
- Verify consistency: the `file` path in config matches the path in `MEMORY_FILE_PREFIXES` and the fallback list

## Execution Notes

### Reverse-Engineered From
- `.crux/crux-memories.json` (current state as of 20260425)
- `install.py` (current state as of 20260425)

### Key Implementation Details
1. The config entry is the sixth command entry (after `dream`, `recall`, `remember`, `meditate`, `forget`) at lines 56-60 of `crux-memories.json`
2. In `install.py`, `MEMORY_FILE_PREFIXES` is a tuple at line 58-69, with amnesia at line 65
3. The fallback list in `get_release_files()` is at lines 493-512, with amnesia at line 504
4. The `DEFAULT_MEMORIES_CONFIG` dict has the amnesia entry at lines 808-812, with the same description string as the config file
5. All three locations use the exact path `.cursor/commands/crux-amnesia.md`

### Files Covered
- `.crux/crux-memories.json`
- `install.py`
