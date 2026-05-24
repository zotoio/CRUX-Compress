---
id: "6c63b56"
title: "Backwards-compatibility anchoring via a pinned 'legacy' level preserves opt-out while raising defaults"
description: "When introducing a multi-level richness/verbosity system to an existing command, dedicate one named level (e.g. 'compact') as a byte-for-byte reproduction of the pre-change behaviour with every numeric minimum, inclusion rule, and surfacing policy pinned to current values. The default-when-unspecified shifts to a richer level ('default'), so existing users who don't specify a level get the improved behaviour, while users who need the old behaviour can explicitly select the legacy level. Eval tests pin the legacy level's numeric values as regression assertions."
type: "learning"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260523-meditate-richness"
tags: [backwards-compatibility, versioning, richness-levels, defaults, regression-testing, user-experience, design-pattern, meditate]
---

When introducing a multi-level richness or verbosity system to an existing command, dedicate one named level as a byte-for-byte reproduction of the pre-change behaviour. Every numeric minimum, inclusion rule, and surfacing policy at that level is pinned to current values. The default-when-unspecified shifts to a richer level, so existing users who don't specify a level get the improved behaviour, while users who need the old behaviour can explicitly select the legacy level.

## Pattern

1. **Name the legacy level explicitly** — e.g. `compact`. The name signals that this is the conservative choice, not a reduced-quality afterthought.
2. **Pin every dimension** — chart minima, infographic minima, calculator minima, depth-3 leaf inclusion, per-branch section depth, peer-review surfacing. No dimension is left as "TBD" or "approximately matches".
3. **Shift the default** — the level selected when the user does not specify one is the new richer level (e.g. `default`), not the legacy level. This is the only "breaking" change: the default-when-unspecified value moves.
4. **Regression-test the pins** — eval tests pin the legacy level's numeric values as regression assertions (`TestMeditateBackwardsCompatibility`, `TestMeditateK10SkipAllBackwardsCompat`). Any future drift in the legacy level is caught loudly.

## Validated by

The `/crux-meditate` 20260523-meditate-richness spec introduced a 4-level comprehensiveness system (`compact` / `default` / `detailed` / `exhaustive`). The `compact` level reproduces the exact pre-spec behaviour — every chart/infographic/calculator minimum, depth-3 leaf inclusion, per-branch section depth, and peer-review surfacing rule pinned to current values. The eval suite includes byte-for-byte backwards-compat regression assertions. The only breaking change is the default-when-unspecified value shifting from `compact`-equivalent to `default`.

## Generalisation

The pattern applies to any feature that raises defaults while preserving opt-out:
- CLI verbosity levels where the old default becomes the quietest named level
- API response formats where a richer default is introduced alongside a `v1`-compatible mode
- Configuration presets where a legacy preset pins every setting to pre-migration values
