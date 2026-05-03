# specs/current — Unprocessed work inbox

This directory is the `workDir` watched by the `zoto-spec-system` session-start hook (see `.zoto-spec-system/config.json`).

## Purpose

Drop short notes, design fragments, or rough briefs here while you are still scoping a piece of work. The session-start hook counts entries and nudges you to run `/zoto-spec-create` once the backlog crosses the configured `threshold` (default 20).

## Suggested workflow

1. Capture a rough idea as a markdown file in this folder (one file per work item).
2. When ready, run `/zoto-spec-create @specs/current/<your-note>.md` (or pass a free-text description).
3. The generator writes a structured spec under `specs/[yyyymmdd]-[feature-name]/` and you can delete or archive the rough note.

## Notes

- Do not commit secrets or transient scratch data — anything here is shared with the team.
- Subdirectories under `specs/[yyyymmdd]-...` are the durable artifacts; this folder is intentionally a scratch inbox.
