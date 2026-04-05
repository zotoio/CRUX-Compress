---
title: "Tooling defaults must align with specification defaults — drift causes silent mismatches"
description: "The crux-utils.py default compression target was 20% while the CRUX.md specification said 25%. This drift went unnoticed until a dedicated plugin refactor. Tools that implement spec behavior must track and match spec defaults."
type: "redflag"
strength: 1
created: 2026-04-05
modified: 2026-04-05
source: "20260404-memories-plugin-integration"
tags: [tooling, specification, defaults, drift, alignment]
---

**Anti-pattern**: Tool hardcodes a default value that differs from the specification it implements.

**Example**: `crux-utils.py --ratio` used a hardcoded 20% target, while `CRUX.md` specifies 25% as the default compression level. The mismatch went unnoticed because both values were "close enough" and the tool was rarely used with the default.

**Detection**: Only discovered during the compression-level plugin refactor (subtask 06) when the spec was re-read to implement configurable targets.

**Prevention**:
1. When implementing spec behavior, reference the spec constant explicitly (comment or config)
2. If the spec defines a default, the tool must use that same value
3. Add a test that asserts the tool's default matches the spec's documented default
4. When changing a spec default, grep for hardcoded uses of the old value
