---
crux: true
alwaysApply: true
---

# Zip Contents Protection Rule

**CRITICAL**: Do NOT add files to `scripts/create-crux-zip.sh` unless the user explicitly instructs you to add a file to the distribution zip.

## Protected Script

The file `scripts/create-crux-zip.sh` defines the exact contents of the CRUX Compress distribution package. Changes to this file directly affect:

1. What users receive when installing CRUX Compress
2. What triggers version bumps (via `.github/workflows/version-bump.yml` RELEASE_PATHS)
3. The size and scope of the distribution

## Rules

### NEVER automatically add files to the zip script when:
- Creating new cursor rules (`.cursor/rules/*.mdc`)
- Creating new skills (`.cursor/skills/*/`)
- Creating new scripts (`scripts/*.sh`)
- Creating any other files in the repository

### ONLY modify the zip script when:
- The user explicitly says "add X to the distribution zip"
- The user explicitly says "include X in the release"
- The user asks to modify the zip contents

### When adding files to the zip (with explicit permission):
1. Update `scripts/create-crux-zip.sh` with the new file/directory
2. Update `.github/workflows/version-bump.yml` RELEASE_PATHS to include the new path
3. Update the "Release-Relevant Files" table in `CONTRIBUTORS.md`
4. Inform the user that adding files will trigger a version bump on next commit

## Current Zip Contents

These are the ONLY files that should be in the distribution:

```
CRUX.md
VERSION
AGENTS.crux.md (extracted from AGENTS.md)
.cursor/hooks.json
.cursor/agents/crux-cursor-rule-manager.md
.cursor/commands/crux-compress.md
.cursor/hooks/detect-crux-changes.sh
.cursor/rules/_CRUX-RULE.mdc
.cursor/skills/CRUX-Utils/SKILL.md
.cursor/skills/CRUX-Utils/scripts/crux-utils.sh
```

## Rationale

The distribution zip should remain minimal and focused. Additional files:
- Increase download size for users
- May conflict with user's existing configurations
- Require users to update more frequently
- Increase maintenance burden
