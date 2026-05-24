---
id: "a2042b2"
title: "Deterministic payload propagation (structured YAML mirroring theming) eliminates ambiguity in multi-agent richness delivery"
description: "When a user-selected configuration (like comprehensiveness level) must flow unchanged through a multi-agent tree (depth-0 → branch agents → leaf agents → report skill → adversarial reviewer), encode it as a structured YAML payload with per-field deterministic mappings rather than prose instructions. The calling agent constructs the payload once at gate time; every downstream agent reads it verbatim and aborts if it's missing. This mirrors the existing 'theming' payload pattern and eliminates the ambiguity of prose-based richness propagation where each agent could interpret 'detailed' differently."
type: "learning"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260523-meditate-richness"
tags: [payload-propagation, structured-data, deterministic, multi-agent, configuration, yaml, design-pattern, meditate]
---

When a user-selected configuration must flow unchanged through a multi-agent tree, encode it as a structured YAML payload with per-field deterministic mappings rather than prose instructions.

## The pattern

1. **Single construction point** — the calling agent constructs the payload once at gate time from the user's selection. The payload is a structured object (not a string label) with every downstream-relevant dimension resolved to a concrete value.
2. **Unchanged propagation** — the payload is passed verbatim from the calling agent into the depth-0 subagent's spawn prompt and propagated unchanged to every child agent in the tree. No agent interprets or modifies it.
3. **Abort-if-missing** — every downstream consumer aborts with a clear error if the payload is missing from its spawn prompt. This makes misconfigured spawns fail fast rather than producing silently wrong output.
4. **Per-field determinism** — the payload carries concrete values for every dimension (e.g. `minima.charts.count: 4`, `depth3_leaf_inclusion: "summary"`, `peer_review_surfacing: "named_section"`) rather than a label like `"detailed"` that each consumer would interpret independently.

## Validated by

The 20260523-meditate-richness spec's K5 introduced a `comprehensiveness:` structured payload, explicitly modelled after the existing `theming:` payload pattern. Both use the same abort-if-missing rule and unchanged-propagation contract. The architecture design (subtask 02) produced a 12-dimension × 4-level mapping table that made every downstream consumer deterministic — the report skill, adversarial reviewer, and every branch/leaf agent all read the same concrete values.

## Shape example

```yaml
comprehensiveness:
  level: "detailed"
  minima:
    charts: { count: 6, types_required: ["bar", "line", "radar", "scatter", "sankey", "treemap"] }
    infographics: { count: 5, types_required: ["timeline", "flowchart", "comparison", "hierarchy", "process"] }
    calculators: { count: 2, scenarios_per: 5 }
  depth3_leaf_inclusion: "verbatim_quotes"
  per_branch_section_depth: "per_leaf_detail"
  citation_density: "mandatory"
  peer_review_surfacing: "per_branch_dedicated"
  section_length_budget_tokens: { hero: 3000, per_facet: 2500, citations: 1500 }
  ensemble_cross_model_depth: "per_facet_cards"
```

## When to apply

Any multi-agent workflow where a user-selected configuration must be consumed identically by N downstream agents. The alternatives — prose instructions ("make it detailed") or per-agent interpretation of a label — create ambiguity that scales with tree depth. The structured payload eliminates this class of drift entirely.
