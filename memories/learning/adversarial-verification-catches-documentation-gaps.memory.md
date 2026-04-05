---
title: "Adversarial verification catches real documentation gaps that slip through initial implementation"
description: "Across two plans, adversarial verification caught 6 issues in 24 subtasks (25% hit rate). Independent verification by a separate agent consistently finds documentation gaps, stale references, and backward-compatibility oversights that implementing agents miss."
type: "learning"
strength: 2
created: 2026-04-05
modified: 2026-04-05
source: "20260403-crux-memories"
tags: [verification, adversarial, documentation, quality, multi-plan]
---

Adversarial verification by an independent judge agent (separate from the implementing agent) catches real issues that would otherwise ship.

**Evidence across plans**:

| Plan | Subtasks | Issues Found | Hit Rate |
|------|----------|-------------|----------|
| `20260403-crux-memories` (14 subtasks) | 14 | 1 (compress skill missing deletion step) | 7% |
| `20260404-memories-plugin-integration` (10 subtasks) | 10 | 5 (README anchors, website `.sh` refs, backward compat docs, stale checksums, TOC alignment) | 50% |
| **Total** | **24** | **6** | **25%** |

The overhead of running a separate verification pass is consistently justified by the quality improvement. This pattern should be standard for any multi-subtask plan execution.
