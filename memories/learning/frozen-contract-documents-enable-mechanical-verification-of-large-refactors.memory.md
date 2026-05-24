---
id: "a096c3d"
title: "Frozen-contract documents enable mechanical verification of large refactors"
description: "When a spec must preserve all existing functionality while restructuring artefacts, capture a single frozen-contract document before execution that records every mode, gate, prompt, safeguard, and subagent contract with traceable source locations. The integrity-review subtask then mechanically diffs each contract item against the post-refactor repository."
type: "learning"
strength: 1
created: 2026-05-24
modified: 2026-05-24
source: "20260517-meditate-agent-skill-decomposition"
tags: [verification, frozen-contract, refactoring, integrity-review, functional-preservation, spec-system]
---

Before executing a refactoring spec that must preserve existing functionality, capture a single frozen-contract document inside the spec directory. This document records every verifiable contract item — modes, gates, prompts, safeguards, report elements, subagent contracts, coordination conventions, cross-repo touchpoints — with traceable source locations (file path + line range or section heading) in the pre-refactor repository.

The integrity-review subtask at the end of the spec then mechanically diffs each contract item against the post-refactor repository: PRESENT / MISSING / DIVERGED. This makes functional preservation binary and auditable rather than subjective.

## Key properties of effective frozen contracts

1. **Granular items**: each contract item is a single verifiable assertion (e.g. "Q-Cost-and-Richness-Acknowledgment gate exists at command line 123"), not a vague goal like "cost gate preserved"
2. **Source-of-truth map**: a concordance section mapping every contract block to its pre-refactor location and its intended post-refactor destination — the integrity subtask uses this as its verification script
3. **Refresh protocol**: when sibling specs change the contract surface mid-flight, capture a superseding freeze with an explicit "Supersedes" header. Preserve the original for audit trail. Update spec Execution Notes to redirect all subtasks to the refreshed freeze
4. **Mechanical verification**: the integrity subtask's diff is binary (PRESENT / MISSING / DIVERGED), not a subjective quality assessment. This means the freeze document must be specific enough that "PRESENT" can be confirmed by searching for a substring or verifying a section heading exists at the expected location

## Validated results

The meditate decomposition spec used a 1,558-line frozen contract with 41 verifiable items. The integrity review checked all 41 mechanically:

- **41/41 PRESENT** — zero functionality loss across a 100+ file, 30K+ line refactor
- **0 MISSING, 0 DIVERGED**
- The verification took a single subtask (S12) by a dedicated `integrity-expert` agent

Without the frozen contract, the integrity review would have been a subjective "does this look right?" assessment — precisely the kind of review that misses subtle surface drops in large refactors.

## When to use

- Any spec that restructures files while requiring functional preservation
- Any spec that touches >10 files or >1,000 lines
- Any spec where the same contract surfaces are spread across multiple files (command + agent + skills + docs)
- NOT needed for simple additive specs that don't move or restructure existing content

## Relationship to adversarial verification

Frozen contracts complement adversarial verification. The contract provides the verification *baseline* (what to check); adversarial review provides the verification *process* (independent reviewer, multi-dimensional audit, severity classification). Both are valuable; the contract makes the review mechanical rather than exploratory.
