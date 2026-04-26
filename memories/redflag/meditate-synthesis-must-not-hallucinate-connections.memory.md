---
id: "3bf625d"
title: "Meditate synthesis must not hallucinate connections"
description: "The meditate synthesis phase combines recalled memories with fresh research. There is a risk of the agent creating false connections between unrelated facts during synthesis. The synthesis output should clearly distinguish 'recalled from memory' vs 'discovered in research' vs 'inferred connection'."
type: "redflag"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "spec:20260425-crux-meditate"
tags: [meditate, synthesis, hallucination, provenance, attribution, safety, anti-pattern]
---

# Meditate synthesis must not hallucinate connections

## The failure mode

The synthesis phase of `/crux-meditate` is precisely the step most exposed to hallucinated connections. By design it asks the LLM to:

- Combine multiple recalled memories
- Combine those memories with fresh research findings
- Cross 3 facets and 3 recursion depths into a single cohesive narrative
- Surface "non-obvious connections" and "emergent themes"

Every one of those instructions rewards the model for finding connections — including connections that do not actually exist. A synthesis that says "memory A and research finding B both point to pattern X" is high-value when X is real and dangerous when X is invented.

## Concrete failure shapes

- **Cross-domain false links** — a memory about test fixtures and a research finding about CI cache invalidation share the word "stale", and the synthesis claims a unified theme about staleness that neither source supports
- **Inferred causation** — recall mentions an issue, research mentions a refactor; synthesis presents the refactor as the fix even though no source links them
- **Aggregate statements** — synthesis generalises from two specific memories to a broad principle ("we always handle X this way") that the memory bodies do not actually claim
- **Phantom citations** — synthesis attributes an insight to memory A when memory A does not contain it; the insight came from the LLM's general training
- **Recursion amplification** — depth-3 returns are aggregated by depth-2, then by depth-1, then by depth-0; each aggregation step can introduce or amplify a hallucinated connection, and provenance is lost as it bubbles up

## The mitigation: provenance-aware synthesis

Every claim in the synthesis output should carry an explicit provenance label from one of three categories:

| Label | Meaning | Trust level |
|-------|---------|-------------|
| **Recalled** | Quoted or directly paraphrased from a specific memory file | High — verifiable against the file |
| **Discovered** | Found during this meditation's targeted-research phase, with a file path or grep result as evidence | Medium — verifiable against codebase state |
| **Inferred** | A connection the agent drew between recalled and discovered items | Low — must be flagged so the user can scrutinise |

A synthesis like:

> [Recalled — memories/learning/session-scope-subagent-patterns.memory.md] Subagents inherit session-scope flags via the parent's parentContext. [Discovered — `.cursor/rules/crux-memories-integration.md` lines 40–95] The amnesia override defines explicit-command exceptions. [Inferred] These two together imply the override list is the only path by which a child can break inheritance — verify before relying on this.

…lets the user immediately see which parts to trust and which to verify.

## Why "explicit inferred connections" is not enough

Tagging inferred connections is necessary but not sufficient. The agent must also resist the urge to invent connections in the first place. Concrete prompts that help:

- Treat absence of evidence as evidence of absence in synthesis: if no source supports a connection, do not include it
- Prefer stating that two facts are "related but independent" over "linked by mechanism X" when X is not in any source
- When recursive aggregation merges two children's findings, preserve their boundaries instead of weaving them into a single narrative
- When in doubt, surface the question to the user as an open question rather than an inferred conclusion

## Why "redflag" not "core"

This memory describes the failure mode and how to avoid it — that is the redflag shape. The corresponding positive invariant ("synthesis output must label provenance") could later be formalised as a core rule once the system has empirical evidence that the labelling discipline works.

## Heuristics for spotting a hallucinated synthesis at review time

- Pick three claims at random from the synthesis and check each against the cited source
- Look for synthesis sentences that say "this suggests", "implies", or "indicates" without an explicit source label
- Check that recursion-aggregated insights still trace back to a leaf-level recall or discovery
- Verify that "non-obvious connections" are in fact non-obvious — vague platitudes like "both relate to maintainability" are hallucination tells

## Generalises to any cross-source synthesis

Any agent workflow that combines stored knowledge with fresh investigation has this risk:

- Code review synthesis combining prior review comments with current diff
- Bug-investigation synthesis combining incident history with live logs
- Spec drafting synthesis combining prior specs with new requirements

The discipline is the same: provenance-aware claims, explicit "inferred" labels, no synthesis sentence without a source.

## Source

`spec-crux-meditate-20260425.md` and the `crux-cursor-memory-manager` Meditate Mode design principles ("open-minded: cast a wide net, unexpected connections are the goal"). The principle that creates value is exactly the principle that creates risk; the mitigation is structural, not motivational.
