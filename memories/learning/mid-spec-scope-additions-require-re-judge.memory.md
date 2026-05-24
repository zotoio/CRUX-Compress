---
id: "89dcf19"
title: "Mid-spec scope additions require a dedicated re-judge pass before execution resumes"
description: "When substantial new scope (e.g. K10's 3-part finalisation-enhancement gate) is added to a spec after the initial judge assessment, the prior verdict does not cover the new scope. A dedicated re-judge pass is required before execution resumes, scoped to the new material plus its interaction with existing decisions. The 20260523 spec's K10 addition triggered a 19-priority re-judge that found 1 MUST_FIX (backwards-compat byte-for-byte tightening) and 4 SHOULD_FIX items specific to K10 that the original assessment could not have caught."
type: "learning"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260523-meditate-richness"
tags: [spec-system, judge, re-assessment, mid-spec-changes, scope-creep, quality-gates, methodology]
---

When substantial new scope is added to a spec after the initial judge assessment, the prior verdict does not cover the new scope. A dedicated re-judge pass is required before execution resumes.

## The problem

Spec judge assessments render a verdict against a specific set of key decisions and requirements. When new key decisions are added after the assessment (e.g. K10 added after K1–K9 were assessed), the verdict is stale for the new material. Issues specific to the new scope — schema completeness, backwards-compatibility gaps, cross-reference consistency with existing decisions — cannot be caught by the prior assessment.

## The evidence

The 20260523-meditate-richness spec's K10 addition (mixed-cost taxonomy, reflection rubric, ensemble layered cadence) was added after the initial `READY_WITH_FIXES` verdict that covered only K1–K9. A dedicated re-judge pass against K10 found:

- 1 MUST_FIX: backwards-compat byte-for-byte tightening for the skip-all path (8 specific pinned assertions needed)
- 4 SHOULD_FIX: Pattern-B handoff ensemble tightening, cost-ack subsystem enumeration, continuation-menu layered surfacing, resolved-OQ trail cleanup
- 4 NICE_TO_HAVE recommendations for the human reviewer

All 5 auto-fixable findings were specific to K10 and could not have been caught by the K1–K9 assessment. Without the re-judge, these would have surfaced only at integrity review (subtask 09) — later and more expensive to fix.

## The practice

1. **Trigger**: any addition of new Key Decisions, new Requirements, or new subtask deliverables after the initial judge pass
2. **Scope**: the re-judge covers (a) the new material's internal consistency, (b) its interaction with existing decisions, and (c) re-verification that previously-passed priorities still hold
3. **Timing**: before execution resumes — not after implementation, where fixes are more expensive
4. **Verdict granularity**: the re-judge renders its own verdict (`READY_WITH_FIXES` for the new scope) independently of the prior verdict

## Generalisation

The pattern applies beyond spec systems: any quality gate that renders a verdict over a scoped set of requirements becomes stale when requirements are added. The re-assessment cost is proportional to the new scope size, not the full scope — it is always cheaper than discovering the issues downstream.
