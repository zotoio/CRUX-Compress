---
id: "aba710d"
title: "Distribution zip can silently omit incrementally-built feature files"
description: "New user-facing files (commands, rules, hooks, skills) can be checked into the repository, registered in config, integrated into install.py, and documented across README/docs/web/evals — yet still be absent from the distribution zip's DIST_FILES list. The omission survives multiple sessions because the file works fine for repo-cloned developers; only users installing via the release zip are affected. Always verify new user-facing files are present in scripts/create-crux-zip.py DIST_FILES before declaring a feature complete."
type: "redflag"
strength: 1
created: 2026-04-26
modified: 2026-04-26
source: "20260425-crux-amnesia"
tags: [distribution, dist-files, release, completeness, installer, command-files, packaging]
---

# Distribution zip can silently omit incrementally-built feature files

## The trap

`scripts/create-crux-zip.py` defines a `DIST_FILES` list — the canonical set of files included in the `CRUX-Compress-v{version}.zip` release archive. New feature files (commands, rules, hooks, skills) are easy to forget here because:

- The file works fine for developers who cloned the repo (no zip path involved)
- Tests that read the file from disk pass without it being in `DIST_FILES`
- Config (`.crux/crux-memories.json`), installer (`install.py`), and docs all integrate the new file independently — none of them check `DIST_FILES`
- Sibling files in the same family may already be in `DIST_FILES`, so the omission looks like a typo gap rather than a missing entry

## Concrete example

`.cursor/commands/crux-amnesia.md` was created in an earlier session and integrated end-to-end:

- ✅ Config entry in `.crux/crux-memories.json` (`commands.amnesia`)
- ✅ `MEMORY_FILE_PREFIXES` in `install.py`
- ✅ Fallback list in `install.py:get_release_files()`
- ✅ `DEFAULT_MEMORIES_CONFIG` in `install.py`
- ✅ Rule integration in `.cursor/rules/crux-memories-integration.md` and the CRUX-compressed `.crux.mdc`
- ✅ README, `docs/crux-memories.md`, `web/compress.md/memories.html`, `evals/USER_EVAL_CHECKLISTS.md`
- ❌ **`scripts/create-crux-zip.py DIST_FILES` was missed**

The five sibling memory commands (`crux-dream`, `crux-recall`, `crux-remember`, `crux-meditate`, `crux-forget`) were already in `DIST_FILES`, so amnesia's absence was easy to miss. Users installing via the release zip would not have received the command despite the installer's `DEFAULT_MEMORIES_CONFIG` referencing it.

The session-day fix added the entry at line 35 of `scripts/create-crux-zip.py`, between `crux-compress.md` and `crux-dream.md`.

## Detection heuristic

Before declaring any spec that introduces a new user-facing file complete:

1. Open `scripts/create-crux-zip.py` and grep `DIST_FILES` for the new filename
2. If absent, verify whether it should be distributed (most user-facing commands/rules/hooks/skills should be)
3. Adding a file to `DIST_FILES` requires explicit user confirmation per `.cursor/rules/zip-contents-protection.md` — surface the omission to the user and ask before adding

## Required spec deliverable

For specs that add a new file under `.cursor/commands/`, `.cursor/rules/`, `.cursor/hooks/`, or `.cursor/skills/`, include a deliverable explicitly:

> Verify the new file is included in `scripts/create-crux-zip.py DIST_FILES`. If not, prompt the user to add it (per zip-contents-protection rule).

## Why this is a redflag

The gap survives multiple sessions because the loop "developer clones repo → file works" never tests the distribution path. By the time a user reports the missing command, the gap may have shipped through a release. A pre-merge checklist or hook to verify new `.cursor/**` files appear in `DIST_FILES` would prevent recurrence.
