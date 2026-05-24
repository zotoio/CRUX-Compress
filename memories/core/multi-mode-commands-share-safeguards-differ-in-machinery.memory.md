---
id: "27bf945"
title: "Multi-mode commands should share all user-facing safeguards and differ only in internal machinery"
description: "When a command supports multiple modes (e.g. Research vs Quick), the modes should share every user-facing safeguard — cost acknowledgment, quality gates, confirmation prompts, mandatory output artifacts — and differ only in internal machinery."
type: "core"
strength: 2
created: 2026-05-24
modified: 2026-05-24
source: "20260516-meditate-research-mode-overhaul"
tags: [architecture, command-design, multi-mode, safeguards, user-experience, consistency, meditate]
---

When a command supports multiple modes (e.g. Research vs Quick, verbose vs compact, full vs lite), the modes should share every user-facing safeguard — cost acknowledgment, quality gates, confirmation prompts, mandatory output artifacts — and differ only in internal machinery.

Validated by `/crux-meditate`'s Research/Quick split: both modes run the same three pre-spawn gates (Cost & Scope Acknowledgment, Theme Preflight, Facet Confirmation), the same adversarial review-and-fix cycle, the same mandatory HTML+PDF report generation, and the same content minimums. Quick mode only relaxes Research-specific internal machinery: no peer review, warn-only citation enforcement (vs strict respawn), no global facet registry (sibling-aware only), append aggregation (vs bottom-up rewrite), no `facet-registry.yml` or `citations-index.yml`.

This design principle ensures the user's experience is consistent regardless of which mode they pick — the same gates, the same output artifacts, the same quality floor. Mode selection becomes a performance/rigor trade-off rather than a quality trade-off.
