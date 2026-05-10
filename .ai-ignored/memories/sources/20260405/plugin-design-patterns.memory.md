---
id: "b0c02ea"
title: "Plugin design patterns: advisory gates and progressive enhancement defaults"
description: "Plugins should use advisory quality gates (failClosed: false) that warn but preserve output, combined with enabledByDefault for progressive enhancement. Users retain full control via --no-plugin for opt-out or explicit --plugin flags which override all defaults."
type: "learning"
strength: 2
created: 2026-04-05
modified: 2026-04-05
source: "20260404-memories-plugin-integration"
tags: [plugins, quality-gates, advisory, user-experience, policy, defaults, opt-out, architecture, extensibility]
consolidated_from: ["a97d331", "daab846"]
---

## Advisory Quality Gates

Advisory quality gates (`failClosed: false`) are a design pattern for validation plugins where:

- **Output is always written** — work is never lost due to a quality check
- **Warnings are logged** — the user sees that the target was not met
- **Users can opt into strict mode** — via `--no-plugin <name>` or `failClosed: true`

This pattern is appropriate when:
1. The quality target is a guideline, not a hard constraint
2. Losing the output (not writing the file) is more costly than missing the target
3. The user can iterate on the output to improve quality

## Progressive Enhancement Defaults

The `enabledByDefault` plugin mechanism enables progressive enhancement with zero breaking changes:

1. **No flags** → default-enabled plugins load automatically
2. **`--plugin X`** → only explicitly named plugins load (overrides all defaults)
3. **`--no-plugin X`** → defaults minus the named plugin(s)

Design principles:
- **Explicit wins over implicit** — `--plugin` flags are authoritative
- **Existing scripts unchanged** — scripts that pass no plugin flags get enhanced behavior
- **Opt-out granularity** — `--no-plugin` disables a single default without losing others

This pattern is applicable to any extensible CLI where new capabilities should activate by default but users must retain the ability to disable them.
