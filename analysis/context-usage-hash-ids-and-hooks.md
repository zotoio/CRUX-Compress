# Context usage tracking: hash IDs in front matter and hooks

Design notes for using **hash-like IDs** in front matter together with **Cursor hooks** to track **context usage**, including **memories**.

## What the repo already has

- **Memories** already carry a stable **`id`** in front matter (7-character hex, immutable), per `.cursor/skills/crux-skill-memory-crud/SKILL.md`; the memory index skill documents it.
- **Usage** is tracked in **sidecar** `.refs.yml` files (not in memory front matter), keyed by **slug**, with output hints like `[memory:{title}]` per `.cursor/skills/crux-skill-memory-reference-tracker/SKILL.md`.
- **Hooks** today (`.cursor/hooks.json`):
  - **`sessionStart`** — `crux-session-start.py` injects `additional_context` (pending compression, memory nudge from `.crux/crux-memories.json`).
  - **`afterFileEdit`** — `crux-detect-changes.py` queues rule sources for CRUX compression.

So the gap is not “we need hashes” for memories — it is **unifying identity**, **correlating sessions with what actually entered context**, and optionally **moving annotations from titles to ids**.

## Two layers of “hash ID”

| Layer | Role | Where it lives |
|--------|------|----------------|
| **Stable content id** | “This artifact is the same logical thing across renames/edits.” | Source front matter (rules, commands) *or* derived and stored in generated output (CRUX outputs already use `sourceChecksum`). |
| **Session / bundle id** | “This turn loaded this set of artifacts.” | Append-only log under `.crux/` (gitignored or committed per policy), written by hooks + optional agent step. |

Memories already use the first layer as **`id`**. Rules could use **`sourceChecksum`** (content) plus a **path** for disambiguation, or a dedicated `contextId:` if you want something independent of compression.

## What hooks can and cannot see

- **`sessionStart`** can run before the user message and emit `additional_context`. It does **not** automatically know Cursor’s final assembled prompt (rules, MCP, memories actually retrieved).
- **`afterFileEdit`** sees **which file** changed, not what the model read.

So **hooks alone** are best for: generating a **session id**, recording **repo/branch/time**, optionally listing **candidates** (e.g. always-applied rule paths from disk, memory index paths). **Proving** “this memory was in context” still needs either **model-visible telemetry** (annotations) or a **post-hoc agent step** that writes a manifest.

## Practical pattern: manifest + references

1. **`sessionStart` hook** (extend `crux-session-start.py` or a sibling script):
   - Generate `session_id` (e.g. ULID or `sha256(branch + timestamp + random)[:12]`).
   - Append one line to `.crux/context-usage/sessions.log` (or JSONL): `{ session_id, ts, cwd, git_head }`.
   - Optionally precompute **`context_fingerprint`** = hash of sorted list of `(kind, path_or_id, content_hash)` for *eligible* always-applied rules + top-N index rows — clearly labeled as **“candidates”**, not “loaded”.

2. **Agent contract** (small addition to AGENTS / memory rule):
   - When memories influence output, annotate with **`[memory:{id}]`** (or extend `referenceTracking.indicatorFormat` in `.crux/crux-memories.json` to support `{id}`) so logs and grep align with front matter.
   - Optionally end-of-turn: write `.crux/context-usage/{session_id}.yml` with **attested** `memory_ids[]`, `rule_paths[]`, `skills[]` — only what the agent knows it used.

3. **Reference tracker** (`crux-skill-memory-reference-tracker`):
   - Prefer **memory `id`** in tracker filenames or inside `recent_references` entries (`memory_id: a1b2c3d`) so renames/slug changes do not break history.
   - Keep slug for human paths; treat `id` as join key.

That gives **hook-grounded session identity** plus **honest usage** where the model explicitly ties output to ids.

## Stronger automation (if Cursor exposes more later)

If a hook or API ever receives **prompt text** or **attachment list**:

- Parse for embedded markers (`[memory:…]`, rule block markers, `sourceChecksum` in pasted rule text).
- Hash the **normalized** prompt snippet per artifact and increment counters — still approximate, but no agent step.

Until then, **id-based annotations + optional manifest** is the reliable path.

## Design choices to decide early

- **Privacy / repo hygiene**: put high-churn logs under `.crux/context-usage/` and add to `.gitignore`, or commit anonymized aggregates only.
- **Rules**: either require optional `contextId:` in **source** `.md` rules, or **derive** ids from `path + sourceChecksum` so generated `.mdc` stays the single source of truth.
- **Collisions**: memory `id` is truncated; document collision handling (rare) or lengthen to 8–12 hex for logging.

## Summary

- **Memories**: use existing front matter **`id`**; shift tracking and output indicators toward **`id`**; extend hooks to stamp **session_id** and optional **candidate fingerprint**.
- **Rules / other context**: reuse **`sourceChecksum`** (or add **`contextId`**) so hooks and manifests refer to stable hashes, not just paths.
- **Hooks** anchor **when/where** a session started; **attested manifests** and **`[memory:{id}]`** carry **what** actually influenced the model, because hooks alone cannot see the full context window.

## Suggested incremental implementation (optional)

1. Extend `crux-memories.json` / reference-tracker skill to prefer **`id`** in indicators and tracker entries.
2. Add session JSONL from `crux-session-start.py`.
3. Document the optional end-of-turn manifest in `AGENTS.md` or the memories integration rule.

## References in this repository

- `.cursor/hooks.json`, `.cursor/hooks/crux-session-start.py`, `.cursor/hooks/crux-detect-changes.py`
- `.crux/crux-memories.json` (`referenceTracking`, `hooks.sessionStartNudge`)
- `.cursor/skills/crux-skill-memory-crud/SKILL.md` (memory front matter including `id`)
- `.cursor/skills/crux-skill-memory-reference-tracker/SKILL.md` (`.refs.yml`, `[memory:{title}]`)
- `.cursor/skills/crux-skill-memory-index/SKILL.md` (index entries and `id`)
