---
id: "6e2af68"
title: "Lazy creation and externalised per-entity tracking reduces overhead and contention"
description: "Tracker files created only on first reference (lazy) and stored in a separate directory (externalised) eliminate overhead for unused entries and prevent concurrent-write contention."
type: "learning"
strength: 1
created: 2026-05-10
modified: 2026-05-10
source: "20260403-crux-memories"
tags: [design-pattern, lazy-creation, externalised-state, concurrency, tracking]
---

The reference tracking system uses two complementary patterns: lazy creation (`.refs.yml` tracker files are only created on first memory reference, so unreferenced memories have zero tracking overhead) and externalised storage (trackers live in `.crux/reference-tracking/` rather than being embedded in memory frontmatter).

Together these eliminate per-entity overhead for unused entries and prevent concurrent-write contention when multiple agents reference different memories simultaneously.

The pattern generalizes to any system with optional per-entity metadata: externalize to separate files, create lazily, and let the aggregation layer (index rebuild) join the data. This keeps the primary data files clean and self-contained while allowing rich secondary metadata to accumulate over time without touching the originals.
