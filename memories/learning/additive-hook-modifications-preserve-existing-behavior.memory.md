---
id: "e5b0b4d"
title: "Additive hook modifications preserve existing behavior when extending feature surface"
description: "Extend hooks by adding self-contained conditional blocks guarded by feature flags rather than restructuring existing control flow. Each block can be independently enabled, disabled, or removed."
type: "learning"
strength: 1
created: 2026-05-10
modified: 2026-05-10
source: "20260403-crux-memories"
tags: [hooks, extensibility, backward-compatibility, additive-design]
---

The session-start hook (`crux-session-start.sh`) was extended by adding a separate conditional block for memory nudge logic alongside the existing pending-compression check, rather than restructuring the existing control flow. Each feature's hook logic is a self-contained conditional block guarded by its own config flag.

This prevents regressions in existing functionality when adding new features and allows each block to be independently enabled, disabled, or removed. The same additive approach was used for `hooks.json` registration.

The pattern applies broadly: when extending any shared entry point (hooks, middleware, init scripts), prefer appending isolated blocks over weaving new logic into existing conditions. This makes each feature's contribution visible, testable, and removable without understanding the full control flow.
