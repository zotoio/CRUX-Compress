---
id: "fc38ec6"
title: "Meditate could cache research results for repeat queries"
description: "When meditate performs deep codebase research on a topic, the research artifacts (file discoveries, pattern analysis) could be cached as lightweight research notes. Future meditate invocations on the same or related topics could start from cached research rather than re-exploring from scratch."
type: "idea"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "spec:20260425-crux-meditate"
tags: [meditate, caching, optimisation, research-notes, performance, future-work]
---

# Meditate could cache research results for repeat queries

## The observation

A meditate run on a non-trivial topic does substantial work:

- 3 facets × 3 recursion depths = up to 9 leaf explorations
- Each leaf reads files, runs greps, reads more files
- The targeted-research phase at each depth is the expensive part

A second meditate on the same or a related topic, run a day later, repeats most of that work from scratch. The memory corpus might have changed (new memories from intervening dreams), but the codebase has not changed dramatically over a day, and the gap-analysis output for similar seeds tends to converge on similar gaps.

This is exactly the shape that caching addresses: deterministic-ish work, repeatedly performed against an input space (codebase + memory corpus) that changes more slowly than queries arrive.

## Sketch of a cache

Each meditate run could emit a lightweight research-note artifact:

```yaml
# .ai-ignored/meditate-cache/<topic-hash>/<yyyymmdd>.yml
seed: "how do we handle session-scoped flags"
gaps_explored:
  - prompt: "how do flags compose when multiple are active"
    files_read:
      - .cursor/rules/crux-memories-integration.md (lines 40-95)
      - .crux/crux-memories.json (full)
    findings:
      - "Φ.amnesia takes precedence over Φ.enabled per phase-block ordering"
      - "subagents inherit session state via parentContext parameter"
codebase_commit: <sha>
memory_index_timestamp: 2026-04-26T14:22:00Z
```

A future meditate on a topic with a high-similarity seed could:

1. Look up cached research-notes whose `seed` matches semantically
2. Compare `codebase_commit` and `memory_index_timestamp` against current state
3. If unchanged, treat the cache as starting research findings (skip re-discovery)
4. If changed, re-run only the gaps whose covered files have moved

## What this would buy

- **Faster repeat meditations** — interactive continuation in particular benefits because the user often expands along directions the previous run already touched
- **Cheaper iterative refinement** — a user who runs meditate, picks a tangent direction, then re-meditates would skip rediscovering the original facets
- **Cross-session warm starts** — meditate sessions on related topics over a week converge faster as the cache grows
- **Eval-ready artifacts** — cached research notes are inspectable, which makes meditate quality measurable rather than ephemeral

## What this risks (the open questions)

- **Topic-similarity is hard** — semantic match between seeds is fuzzy; false positives serve stale findings
- **Codebase staleness detection** — `codebase_commit` is a coarse signal; finer per-file invalidation needs more bookkeeping
- **Cache hygiene** — `.ai-ignored/` would grow unboundedly without an eviction policy (TTL? LRU? Strength-derived like memories?)
- **Confused with memories** — research notes are not memories. The line must stay sharp; otherwise meditate would silently start authoring durable knowledge, violating the read-only-with-explicit-save invariant
- **Privacy / staleness leakage** — cached findings could capture transient bug-state that has since been fixed, then get surfaced as if current

## How this is distinct from existing memory caching

Memories cache _conclusions_ — durable, vetted insights. Research notes would cache _intermediate findings_ — file paths, grep matches, partial pattern observations that are useful only inside a meditation. The two have different lifecycles, different validation criteria, and different surface areas in the agent definition.

## Why this is "idea" not "learning"

This is speculative future work. Nothing in the current meditate implementation persists research artifacts; the value above is hypothetical. Promote to learning if and when an experiment shows a measurable speedup or quality gain on real meditate sessions.

## First experiment to try

Add a feature flag `flags.enableMeditateResearchCache`. Implement the simplest possible cache: dump the gap-analysis output and the targeted-research prompts/findings to a file per facet at meditate completion. On the next meditate invocation with a high-overlap seed (string-match for a first pass), surface the cache to the user and let them decide whether to use it. Keep it manual until the auto-similarity heuristic is good enough.

## Source

`spec-crux-meditate-20260425.md`. The spec implements meditate as fully ephemeral — every run starts from scratch. This idea is the natural next-step optimisation observed while reading the recursive-exploration protocol; not part of the as-shipped feature.
