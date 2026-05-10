---
id: "a97d331"
title: "Advisory quality gates (failClosed: false) preserve output while warning on target misses"
description: "The compression-level plugin uses failClosed: false — compression output is written even if the ratio target is missed, with a warning instead of a hard block. This prioritizes not losing work over enforcing targets. Users who need hard gates can opt out with --no-plugin."
type: "learning"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260404-memories-plugin-integration"
tags: [plugins, quality-gates, advisory, user-experience, policy]
---

Advisory quality gates (`failClosed: false`) are a design pattern for validation plugins where:

- **Output is always written** — work is never lost due to a quality check
- **Warnings are logged** — the user sees that the target was not met
- **Users can opt into strict mode** — via `--no-plugin <name>` or `failClosed: true`

This pattern is appropriate when:
1. The quality target is a guideline, not a hard constraint
2. Losing the output (not writing the file) is more costly than missing the target
3. The user can iterate on the output to improve quality

The `compression-level` plugin demonstrated this: CRUX files are written with a warning if the ratio target is not met, rather than blocking the write entirely.
