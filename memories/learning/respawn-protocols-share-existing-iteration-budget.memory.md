---
id: "91b0e75"
title: "Respawn protocols that share an existing iteration budget avoid infinite loops without a separate cap"
description: "When extending an adversarial review cycle with a new respawn cause (e.g. report-skill respawn for missing sections, accepted finalisation enhancements), fold the respawn into the existing ≤N iteration cap rather than introducing a separate retry budget. Each respawn consumes one iteration slot; multiple respawn causes in the same iteration bundle into a single respawn with a list-typed 'respawn_reasons' field. At the final iteration, unresolved respawn-triggering findings become ESCALATE rather than retrying. This guarantees finite termination with a simple proof: max useful respawns = N-1."
type: "learning"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260523-meditate-richness"
tags: [respawn-protocol, iteration-budget, finite-termination, adversarial-review, report-generation, design-pattern, meditate]
---

When extending an adversarial review cycle with new respawn causes, fold the respawn into the existing ≤N iteration cap rather than introducing a separate retry budget.

## The pattern

1. **Single iteration counter** — the review-and-fix cycle has a cap (e.g. ≤3 iterations). A respawn (regeneration of the entire artifact by a different skill) consumes one iteration slot, same as an in-place fix pass.
2. **Bundled respawn causes** — if multiple respawn triggers fire in the same iteration (e.g. missing sections AND missing visualisations AND accepted enhancements), they bundle into a single respawn with a list-typed `respawn_reasons:` field. One respawn per iteration, regardless of how many causes triggered it.
3. **ESCALATE at cap** — at iteration N (the final allowed iteration), if respawn-triggering findings are still present, the verdict is ESCALATE rather than retrying. The ESCALATE surfaces unresolved findings to the user via the standard escalation path.

## Finite termination proof

For a ≤3 iteration cap:

| Iteration | Action | Next state |
|-----------|--------|------------|
| 1 | Apply Dim 1–11 fixes → construct respawn payload → respawn artifact → counter advances to 2 | Regenerated artifact reviewed by iter 2 reviewer |
| 2 | Apply fixes → respawn if needed → counter advances to 3 | Regenerated artifact reviewed by iter 3 reviewer |
| 3 | If respawn-triggering findings still fire → ESCALATE (no iter 4 exists) | Loop terminates |

**Maximum useful respawns = 2** (at iter 1 and iter 2). The Nth iteration's reviewer cannot trigger a useful respawn because no (N+1)th iteration exists to review the result. **Infinite loop impossible.**

## Validated by

The 20260523-meditate-richness spec's K9 respawn protocol (for missing init-suggestion sections) and K10b extension (for accepted finalisation enhancements) both share the existing ≤3 adversarial review iteration cap. The integrity review (subtask 09) independently reconstructed the worst-case scenario and confirmed finite termination.

## When to apply

Any workflow that extends a bounded retry loop with new failure/action causes should fold the new cause into the existing budget rather than creating a parallel budget. Parallel budgets create a multiplicative explosion risk (N × M iterations) and make finite-termination proofs harder to construct.
