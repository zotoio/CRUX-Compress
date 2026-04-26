---
id: "7144866"
title: "install.py: feature commands belong in RELEASE_FILES, not standard_files"
description: "install.py keeps two distinct file lists. standard_files is the install backup list and contains only foundational CRUX files (CRUX.md, AGENTS.md, install.crux.md, hooks, _CRUX-RULE.mdc, crux-utils, crux-compress.md, crux-cursor-rule-manager). Feature-scoped commands (memory commands like crux-dream/recall/remember/meditate/forget, plus any future feature command) belong only in RELEASE_FILES and the feature's DEFAULT_*_CONFIG template. Adding a feature command to standard_files breaks the architectural distinction and creates inconsistency with sibling commands."
type: "core"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260406-crux-forget"
tags: [installer, install.py, release-files, standard-files, architecture, distribution, memory-commands]
---

# install.py: feature commands belong in RELEASE_FILES, not standard_files

## The two lists

`install.py` defines two file lists with different roles:

| List | Role | Contents |
|------|------|----------|
| `standard_files` | Backup list created during install (so the user can roll back) | Only foundational CRUX files |
| `RELEASE_FILES` | Files included in release zips and `--with-*` install flags | Core files **plus** all feature files |

`standard_files` (canonical contents at the time of writing):

```
CRUX.md, AGENTS.md, install.crux.md,
.crux/crux.json, .crux/crux-release-files.json,
.cursor/hooks.json,
.cursor/agents/crux-cursor-rule-manager.md,
.cursor/commands/crux-compress.md,
.cursor/hooks/crux-detect-changes.py,
.cursor/hooks/crux-session-start.py,
.cursor/rules/_CRUX-RULE.mdc,
.cursor/skills/crux-utils/SKILL.md,
.cursor/skills/crux-utils/scripts/crux-utils.py,
```

## Where new feature commands go

When adding a new command (memory commands, future feature commands, etc.):

- **YES**: append to `RELEASE_FILES`
- **YES**: add an entry to the relevant `DEFAULT_*_CONFIG` template (e.g. `DEFAULT_MEMORIES_CONFIG.commands`)
- **NO**: do not add to `standard_files`
- **NO**: do not add to `scripts/create-crux-zip.py` or `.github/workflows/version-bump.yml RELEASE_PATHS` without explicit user request (zip-contents-protection rule)

## Verification

Existing memory commands `.cursor/commands/crux-dream.md` and `.cursor/commands/crux-mindreader.md` are in `RELEASE_FILES` only — they do **not** appear in `standard_files`. Any new memory or feature command should follow this same pattern.

## Anti-pattern

Adding a feature command to `standard_files` because it "looks like a core file." This is wrong:

- It creates inconsistency with sibling feature commands
- It bloats the user's install-backup with files they may not have opted into
- It implicitly marks a feature-scoped file as foundational

The first judge assessment of `spec-crux-forget-20260406` mistakenly believed the spec was doing this; the second judge corrected the record. Subtask 06 was authored correctly from the start.

## Related sync target

`install.crux.md`'s `M.standard_files(backup)` block must reflect the actual list in `install.py`. A pre-existing drift was observed where the CRUX block listed memory commands not actually in the source — this is a separate sync issue and should be repaired surgically when next encountered.
