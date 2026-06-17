---
crux: true
alwaysApply: true
---

# Zip Contents Protection Rule

**CRITICAL**: Do NOT add files to `scripts/create-crux-zip.py` unless the user explicitly instructs you to add a file to the distribution zip.

## Protected Script

The file `scripts/create-crux-zip.py` defines the exact contents of the CRUX Compress distribution package. Changes to this file directly affect:

1. What users receive when installing CRUX Compress
2. What triggers version bumps (via `.github/workflows/version-bump.yml` RELEASE_PATHS)
3. The size and scope of the distribution

## Rules

### NEVER automatically add files to the zip script when:
- Creating new cursor rules (`.cursor/rules/*.mdc`)
- Creating new skills (`.cursor/skills/*/`)
- Creating new scripts (`scripts/*.py`)
- Creating any other files in the repository

### ONLY modify the zip script when:
- The user explicitly says "add X to the distribution zip"
- The user explicitly says "include X in the release"
- The user asks to modify the zip contents

### When adding files to the zip (with explicit permission):
1. Update `scripts/create-crux-zip.py` with the new file/directory
2. Run `scripts/create-crux-zip.py` so `.crux/dist-manifest.json` records the new path
3. Update the "Release-Relevant Files" table in `CONTRIBUTORS.md`
4. Inform the user that adding files will trigger a version bump on next commit

## Current Zip Contents

These are the ONLY files that should be in the distribution:

```
CRUX.md
install.crux.md
.crux/crux.json
AGENTS.crux.md (extracted from AGENTS.md)
.cursor/hooks.json
.cursor/agents/crux/crux-cursor-rule-manager.md
.cursor/agents/crux/crux-cursor-memory-manager.md
.cursor/agents/crux/crux-cursor-meditation-guide.md
.cursor/commands/crux/crux-compress.md
.cursor/commands/crux/crux-amnesia.md
.cursor/commands/crux/crux-dream.md
.cursor/commands/crux/crux-forget.md
.cursor/commands/crux/crux-meditate.md
.cursor/commands/crux/crux-recall.md
.cursor/commands/crux/crux-remember.md
.cursor/hooks/crux-detect-changes.py
.cursor/hooks/crux-detect-memory-changes.py
.cursor/hooks/crux-session-start.py
.cursor/rules/crux/_CRUX-RULE.mdc
.cursor/rules/crux/crux-memories-integration.crux.mdc
.cursor/skills/crux/crux-utils/SKILL.md
.cursor/skills/crux/crux-utils/scripts/crux-utils.py
.cursor/skills/crux/crux-skill-memory-crud/SKILL.md
.cursor/skills/crux/crux-skill-memory-compress/SKILL.md
.cursor/skills/crux/crux-skill-memory-extract/SKILL.md
.cursor/skills/crux/crux-skill-memory-index/SKILL.md
.cursor/skills/crux/crux-skill-memory-index/scripts/memory-index.py
.cursor/skills/crux/crux-skill-memory-index/scripts/post-dream.py
.cursor/skills/crux/crux-skill-memory-rebalance/SKILL.md
.cursor/skills/crux/crux-skill-memory-reference-tracker/SKILL.md
.cursor/skills/crux/crux-skill-memory-meditation-research/SKILL.md
.cursor/skills/crux/crux-skill-memory-meditation-quick/SKILL.md
.cursor/skills/crux/crux-skill-memory-meditation-ensemble/SKILL.md
.cursor/skills/crux/crux-skill-memory-meditation-review/SKILL.md
.cursor/skills/crux/crux-skill-memory-meditation-report/SKILL.md
.cursor/skills/crux/crux-skill-memory-meditation-coordination/SKILL.md
.crux/crux-release-files.json
```

## Rationale

The distribution zip should remain minimal and focused. Additional files:
- Increase download size for users
- May conflict with user's existing configurations
- Require users to update more frequently
- Increase maintenance burden 
