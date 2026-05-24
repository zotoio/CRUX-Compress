---
id: "d55bdbd"
title: "Cross-surface field-name consistency requires canonical-name-wins enforcement across read, write, and schema layers"
description: "When a structured payload (e.g. YAML artefact) is written by one agent surface and read by another, the field name must be identical across three layers: the write-side prose (agent definition), the schema definition (canonical), and the read-side contract (command/skill). The 20260523 spec's W1 finding showed that a divergence between the write-side prose ('additional_focus_areas_accepted[]') and the canonical schema ('additional_focus_areas[]') caused the report-side read contract to silently no-op. The integrity reviewer caught it; the judge upgraded it to soft-BLOCKER. Fix: always grep the canonical field name across all three surfaces after any schema-touching subtask completes."
type: "learning"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260523-meditate-richness"
tags: [field-names, schema-consistency, canonical-name, cross-surface, integrity-review, silent-failure, yaml, meditate]
---

When a structured payload (e.g. YAML artefact) is written by one agent surface and read by another, the field name must be identical across three layers:

1. **Write-side prose** — the agent definition or skill that produces the YAML
2. **Schema definition** — the canonical field name in the architecture design or schema block
3. **Read-side contract** — the command or skill that consumes the YAML

## The failure mode

The 20260523-meditate-richness spec's W1 finding demonstrated the failure:

- The canonical schema (subtask 02 architecture-design, subtask 04 agent file schema block, eval tests) used `additional_focus_areas[]` with a per-item `treatment:` field
- The write-side prose (agent file line 512) used `additional_focus_areas_accepted` (divergent name)
- The read-side contract (command file line 1815) used `additional_focus_areas_accepted[]` (matching the divergent write-side, not the canonical schema)

Result: the report skill's honour check for `report_section_only` focus areas searched for a field name that didn't exist in the on-disk YAML. The feature appeared to work in the default case (where `report_section_only` is never selected) but silently no-oped when actually used.

The integrity reviewer (subtask 09) caught it as W1 (WARNING). The integrity-review judge upgraded it to soft-BLOCKER. Two surgical fixes were needed (W1 + W1b).

## Prevention

After any subtask that defines or modifies a YAML schema:

1. `grep` the canonical field name across all source files that write or read the payload
2. Verify zero matches for variant spellings (e.g. `_accepted`, `_confirmed`, `_pending` suffixes)
3. If the schema block and prose diverge, the schema block wins — it is the single source of truth

This is structurally similar to the "spec index can drift from subtask details" redflag, but at a finer granularity — field names within a single artefact's lifecycle rather than spec-level prose.
