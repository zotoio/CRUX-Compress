# [2026-03-06] feature idea

## Summary

This draft proposes **CRUX Review Packs**: audience-specific compressed briefs
generated from a single source document, spec, transcript, incident report, or
change summary.

Instead of producing one generic summary, CRUX would generate multiple focused
artifacts such as:

- `product.crux.md`
- `security.crux.md`
- `support.crux.md`
- `exec.crux.md`

That moves CRUX beyond its current codebase themes of rules, code, and images,
and into cross-functional review workflows where each audience needs a different
slice of the same truth.

## Problem

Most launch briefs, design docs, incident reports, and customer escalations are
reviewed by several functions at once. The raw source is usually bloated for at
least half of those reviewers:

- product wants scope, tradeoffs, and rollout
- security wants trust boundaries and risk
- support wants user impact and known failure modes
- leadership wants outcome, timeline, and risk

Today, teams either:

1. send everyone the same long source document, or
2. manually rewrite several versions of the same information

Both paths waste time and create drift.

## Proposed feature

Add a new workflow:

```text
/crux-pack @launch-brief.md --for product,security,support,exec
```

Proposed outputs:

```text
.crux/packs/launch-brief.product.crux.md
.crux/packs/launch-brief.security.crux.md
.crux/packs/launch-brief.support.crux.md
.crux/packs/launch-brief.exec.crux.md
```

Each pack would preserve the same factual source, but optimize ordering,
emphasis, terminology, and examples for a specific audience.

## Quantifiable benefit

### Modeled benchmark

For a **6,000-token launch brief** reviewed by four groups:

| Audience | Current input | Target pack size | Reduction |
| --- | ---: | ---: | ---: |
| Product | 6,000 tokens | 900 tokens | 85% |
| Security | 6,000 tokens | 750 tokens | 88% |
| Support | 6,000 tokens | 800 tokens | 87% |
| Exec | 6,000 tokens | 600 tokens | 90% |

### Time impact

Assuming reviewers spend 12 to 15 minutes scanning irrelevant sections before
getting to what matters, Review Packs can reasonably target:

- **8 to 12 minutes saved per reviewer**
- **32 to 48 minutes saved per cross-functional review cycle**
- **70% to 90% less irrelevant context per audience**

These are modeled estimates, not production claims, and should be validated with
real pack-generation benchmarks after implementation.

## Why this is useful

This is the strongest next feature because it expands CRUX from an
"authoring-time compression tool" into a **cross-functional decision-delivery
tool**.

That matters because the biggest coordination bottleneck in modern teams is not
creating another document. It is getting the *right* people the *right level of
detail* quickly enough to make a decision.

CRUX already does semantic reduction well. Review Packs apply that same strength
to a larger and more valuable workflow surface.

## Proposed code changes

This PR draft does **not** implement Review Packs yet. It proposes the following
future code changes:

### 1. New command

- Add `.cursor/commands/crux-pack.md`
- Support:
  - one source, many audiences
  - explicit audience list via `--for`
  - optional tone presets like `--depth concise|standard|deep`

Example:

```text
/crux-pack @incident.md --for security,support
```

### 2. Agent workflow extension

- Extend `.cursor/agents/crux-cursor-rule-manager.md`
- Add a pack-generation mode that:
  - loads source once
  - extracts shared facts once
  - emits audience-specific prioritization layers
  - validates that no audience pack invents facts not present in the source

### 3. Output conventions

- Store outputs in `.crux/packs/`
- File naming pattern:
  - `<basename>.<audience>.crux.md`
- Frontmatter additions:
  - `audience: product|security|support|exec`
  - `sourceChecksum: ...`
  - `sharedFactsChecksum: ...`
  - `relevanceScore: XX%`

### 4. Validation

- Add tests in `tests/test_crux_pack.bats`
- Verify:
  - stable file naming
  - audience selection parsing
  - no hallucinated facts
  - pack size stays below configured thresholds
  - unchanged sources can be skipped via checksum

### 5. Optional future UI work

- Add website examples showing one source transformed into four audience packs
- Add a measurable "review time saved" calculator using real token counts

## Proposed website changes

This draft includes a website update that presents Review Packs as a
forward-looking idea rather than a shipped feature.

Suggested messaging:

- label it clearly as **feature idea**
- show one quantified benchmark
- list pros, cons, and alternatives
- explain why it is the most useful next expansion

## Pros

1. **Broadens CRUX beyond current themes**
   - useful for launch reviews, incident handoffs, onboarding, vendor reviews,
     and executive updates
2. **Quantifiable value**
   - token reduction, reading-time savings, and review-cycle time can all be
     measured
3. **High reuse of current architecture**
   - command-driven workflow, checksum logic, CRUX outputs, and validation ideas
     already match the repository's shape
4. **Improves adoption**
   - reviewers, not just authors, now get direct value from CRUX

## Cons

1. **Higher validation burden**
   - audience-specific emphasis increases the risk of accidental omission
2. **More output files**
   - one source may generate four or more artifacts
3. **Audience design can sprawl**
   - too many presets could make the feature harder to understand
4. **Benchmarking needs discipline**
   - time-saved claims should be backed by observed reviewer behavior

## Alternate similar approaches

### A. One-size-fits-all summary mode

Generate a single compressed brief for everyone.

**Pros**
- simplest to build
- lowest file-count increase

**Cons**
- still forces each audience to scan irrelevant material
- less differentiated than what CRUX could uniquely offer

### B. Manual prompt templates per audience

Ship prompt recipes and ask users to create packs themselves.

**Pros**
- almost no engineering work
- quick to experiment with

**Cons**
- inconsistent quality
- no checksum tracking, structure, or validation
- weak product story

### C. Retrieval over the original source

Keep the full document and let each reviewer ask questions with RAG/search.

**Pros**
- flexible
- no extra output files

**Cons**
- reactive instead of proactive
- depends on reviewers knowing what to ask
- does not reduce review overhead up front

## Why Review Packs wins

Review Packs is the most useful option because it combines:

- the **clarity** of a delivered artifact
- the **measurability** of token and time savings
- the **architecture fit** of CRUX-style outputs
- the **market expansion** of serving product, security, support, and exec
  workflows in addition to engineering

It is more differentiated than a generic summary, more reliable than manual
templates, and more proactive than retrieval alone.

## Success metrics

If implemented, success should be measured against:

- median tokens per reviewer
- review completion time per audience
- number of follow-up clarification questions
- time from document share to sign-off
- factual retention score versus source

## Scope of this draft PR

Included now:

- draft PR body
- website section for the feature idea
- supporting website docs updates

Not included now:

- `/crux-pack` command implementation
- agent changes
- tests for pack generation
- release/distribution changes

## Recommended next step

If this idea is accepted, the next implementation PR should focus narrowly on:

1. `.cursor/commands/crux-pack.md`
2. `.cursor/agents/crux-cursor-rule-manager.md`
3. `tests/test_crux_pack.bats`
4. one end-to-end example in `web/compress.md/`
