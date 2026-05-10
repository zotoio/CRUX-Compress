---
id: "daab846"
title: "Plugin defaults with opt-out (enabledByDefault + --no-plugin) enable progressive enhancement"
description: "Plugins can be enabledByDefault: true for progressive enhancement without breaking existing workflows. Users who need the old behavior can opt out with --no-plugin <name>. Explicit --plugin flags override all defaults (explicit wins over implicit)."
type: "learning"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260404-memories-plugin-integration"
tags: [plugins, defaults, opt-out, architecture, extensibility]
---

The `enabledByDefault` plugin mechanism enables progressive enhancement with zero breaking changes:

1. **No flags** → default-enabled plugins load automatically
2. **`--plugin X`** → only explicitly named plugins load (overrides all defaults)
3. **`--no-plugin X`** → defaults minus the named plugin(s)

Design principles:
- **Explicit wins over implicit** — `--plugin` flags are authoritative
- **Existing scripts unchanged** — scripts that pass no plugin flags get enhanced behavior; scripts that pass `--plugin` flags get exactly what they asked for
- **Opt-out granularity** — `--no-plugin` disables a single default without losing others

This pattern is applicable to any extensible CLI where new capabilities should activate by default but users must retain the ability to disable them.
