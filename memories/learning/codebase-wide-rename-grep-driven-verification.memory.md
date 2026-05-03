---
id: "b40e02b"
title: "Codebase-wide renames require systematic grep-driven multi-file verification"
description: "Renaming `/crux-mindreader` to `/crux-recall` touched 20+ files across commands, agents, config, rules, documentation, install scripts, and evals. Success required: project-wide case-insensitive grep to find all references, preserving historical entries (old filenames in release manifests), `git mv` for history preservation, and regenerating derived CRUX files from updated sources."
type: "learning"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "20260425-crux-recall"
tags: [rename, grep-driven, verification, cross-cutting, derived-files, historical-entries]
---

# Codebase-wide renames require systematic grep-driven multi-file verification

## Why renames are deceptively expensive

A rename feels like a one-line change ("change name X to name Y") but in a project with rules, agents, configs, derived files, and historical records, a single rename routinely touches every layer of the codebase. Partial renames produce silent inconsistencies that survive tests because they live in non-executable artifacts (docs, comments, release manifests, evals). The fix is a systematic grep-driven protocol.

## Concrete inventory: `crux-mindreader` → `crux-recall`

The crux-recall rename touched at least 20 files across these classes:

| Class | Examples | Count |
|-------|----------|-------|
| Command files | `.cursor/commands/crux-recall.md` (renamed from `crux-mindreader.md`) | 1 |
| Agent definitions | `.cursor/agents/crux-cursor-memory-manager.md` (mode names, expertise, invocation table) | 1 |
| Config (JSON) | `.crux/crux-memories.json` (key rename `mindReader` → `recall`, not just value) | 1 |
| Rules | source `.md` AND derived `.crux.mdc` (regenerate with new sourceChecksum) | 2+ |
| Documentation | `README.md`, `CONTRIBUTORS.md`, `docs/crux-memories.md`, `web/compress.md` pages | 4+ |
| Install scripts | `install.py` + regenerated `install.crux.md` | 2 |
| Evals | one file alone needed 38 replacements | 1+ |
| Cross-references | Sibling commands (`crux-dream.md`, `crux-remember.md`, etc.) referencing the renamed command | several |
| Dist/release | `.crux/crux-release-files.json` (current entries updated, historical entries preserved) | 1 |

The initial project-wide `rg -i "mindreader"` returned 17 files; one of those required 38 individual replacements.

## The protocol

### 1. Start with a project-wide case-insensitive grep

```bash
rg -i "<old-name>" --glob '!specs/**' --glob '!.git/**' --glob '!.ai-ignored/**'
```

Use `-i` to catch every casing (`MindReader`, `mindReader`, `mindreader`, `MINDREADER`, `mind-reader`). Exclude historical or generated dirs that should not be touched.

### 2. Generate a casing-aware replacement plan

Different sites need different replacements:

- `mindReader` (camelCase JSON key) → `recall`
- `mind-reader` / `mindreader` (kebab-case file/command) → `recall`
- `MindReader` (PascalCase, agent/class names if any) → `Recall`
- `MINDREADER` (env vars, constants) → `RECALL`
- Plain English ("mindreader command", "mind reader") → "recall command"

A blind global replace will mangle some sites (e.g. compounds, partial matches inside unrelated words). Plan per-casing.

### 3. Use `git mv` for file renames

```bash
git mv .cursor/commands/crux-mindreader.md .cursor/commands/crux-recall.md
```

Preserves git blame and history. Subsequent edits to the file are diffed against the rename, not against an unrelated `add` + `delete`.

### 4. Preserve historical entries

Some files are append-only logs of past state:

- Release manifests (`.crux/crux-release-files.json`)
- Changelogs
- Migration records
- Old spec/dream summaries

These contain old names **as historical fact**. Do not modify them — they are accurate for the version they describe. Restrict the rename to active references only.

### 5. Regenerate derived CRUX files

For every source file with a `.crux.md` or `.crux.mdc` derivative:

1. Edit the source (`.md`)
2. Regenerate the derivative via the appropriate tool (e.g. `crux-cursor-rule-manager`)
3. Confirm the new `sourceChecksum` matches the updated source

Editing the derivative directly will be silently overwritten on the next regeneration and triggers checksum drift warnings.

### 6. Verify zero residual references

After all edits:

```bash
rg -i "<old-name>" --glob '!specs/**' --glob '!.git/**' --glob '!.ai-ignored/**' --glob '!.crux/crux-release-files.json'
```

Expect zero hits in active code. If any remain, classify each:

- **Legitimate historical** — exclude from future scans
- **Missed reference** — fix
- **Compound that resembles the old name** — false positive, document

### 7. Run the full test suite

The rename is complete only when tests pass. In this spec: 296/296 tests passing was the final acceptance signal.

## Why partial renames are the silent failure mode

Renames that fail tests are caught immediately. Renames that leave stale references in:

- README files
- Agent prompt sections
- Eval fixtures (especially expected-output strings)
- Generated docs

…will pass tests for weeks before someone notices. The grep step exists precisely to surface these non-executable inconsistencies before they ship.

## Source

`spec-crux-recall-20260425.md` and `execution-report-crux-recall-20260425.md`. Subtask 04 (documentation) found 17 files via project-wide grep, with 38 replacements concentrated in a single evals file. Subtask 03 demonstrated the JSON-key-rename + CRUX-regeneration pattern (with independent checksum verification by the adversarial judge).
