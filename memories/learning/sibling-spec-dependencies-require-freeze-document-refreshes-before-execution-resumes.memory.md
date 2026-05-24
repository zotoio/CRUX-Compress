---
id: "d7fafbd"
title: "Sibling-spec dependencies require freeze-document refreshes before execution resumes"
description: "When a spec's freeze line is captured before a sibling spec that modifies the same contract surfaces completes, the freeze becomes stale. Capture a superseding freeze incorporating the sibling's changes before resuming execution, and update all subtask references to point at the refreshed freeze."
type: "learning"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260517-meditate-agent-skill-decomposition"
tags: [spec-system, frozen-contract, cross-spec-dependency, coordination, refresh-protocol, staleness]
---

A spec captures its frozen contract at a point in time. If a sibling spec then completes and modifies the same files or contract surfaces, the frozen contract becomes stale — it no longer reflects the actual state of the artefacts the spec is about to restructure.

Executing subtasks against a stale freeze risks silently dropping surfaces that the sibling spec added.

## The concrete case

The decomposition spec (20260517) captured its frozen contract on 2026-05-17 against the pre-richness source state. The sibling richness spec (20260523) then completed on 2026-05-24 and added 13 new surfaces to the very files the decomposition spec was about to restructure:

- Merged cost-and-richness gate (`Q-Cost-and-Richness-Acknowledgment`)
- Read-only-richness variant gate (`Q-Cost-Acknowledgment-Expansion`)
- `comprehensiveness:` payload propagation
- `Q-Finalisation-Enhancements` gate (K10a multi-select, K10b taxonomy, K10c YAML update)
- Adversarial review dimensions 12 and 13
- Comprehensiveness Level Mapping (12×4 table)
- 4-mode `additional_focus_areas[]` reconciliation
- `init-suggestions-{ts}.yml` schema
- Peer-review report-side surfacing
- K10 layered ensemble cadence
- 28 new pytest classes + 4 new TS describe blocks

The original 20260517 freeze knew nothing about these 13 surfaces. Executing subtasks 02–12 against it would have silently dropped all of them.

## The resolution

A superseding freeze (`meditate-frozen-contract-20260524.md`) was captured at the working-tree state that included the richness changes:

1. Opened with an explicit **"Supersedes `meditate-frozen-contract-20260517.md`"** header
2. Listed all 13 new surfaces with their current source locations (file + line ranges)
3. Preserved the original freeze as an **audit-trail artefact only**
4. Updated the spec's Execution Notes to redirect all subtasks (02–12) to the new freeze
5. Recorded the git SHA and working-tree state at capture time

All subsequent subtasks traced against the 20260524 freeze. The integrity review verified all 41 items (including the 13 new surfaces) as PRESENT.

## The generalised rule

When a spec has a frozen contract and a sibling spec lands changes to the same contract surfaces:

1. **Pause execution** of the dependent spec
2. **Capture a superseding freeze** that incorporates the sibling's changes
3. **Mark the original freeze** as audit-trail-only (do not delete it)
4. **Update the spec's Execution Notes** to point at the new freeze
5. **Resume execution** against the refreshed freeze

Plan for this step in any spec whose execution may overlap with sibling specs that touch the same files.
