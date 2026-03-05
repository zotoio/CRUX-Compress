# [2026-03-05] feature idea

Status: Draft PR proposal

## Proposed feature

**Multi-target adapter export**: keep one canonical `.crux.md` source, then generate
assistant-ready outputs for Cursor, Claude, ChatGPT, Copilot, and other target
surfaces from that single source of truth.

CRUX already has a strong universal representation plus a Cursor adapter. This
proposal turns that pattern into a reusable distribution layer instead of a
single-IDE workflow.

## Why this is useful

Most teams do not use one assistant. They maintain slightly different prompt,
rule, or instruction files for multiple tools, which creates drift:

- Cursor rule files
- ChatGPT system prompts
- Claude project instructions
- Copilot repository instructions
- internal onboarding or policy snippets

When the source guidance changes, each target has to be updated manually.

## Quantifiable benefit

Example operating model:

- 4 assistant targets
- 12 instruction updates per month
- 8 minutes to manually update, review, and paste each target

Manual maintenance:

- `4 targets x 12 updates = 48 target edits/month`
- `48 edits x 8 minutes = 384 minutes/month`

With multi-target export:

- `1 canonical source x 12 updates = 12 source edits/month`
- duplicated edits avoided: `48 - 12 = 36 edits/month`
- maintenance reduction: `36 / 48 = 75%`
- time reclaimed: `36 x 8 minutes = 288 minutes/month`
- **time reclaimed: 4.8 hours per month**

The same math scales linearly. At 6 targets and 20 monthly updates, the same
workflow avoids 100 duplicated edits per month.

## Proposed product changes

### Code

1. Add a new export surface, either:
   - `/crux-export @file.md --targets cursor,claude,chatgpt,copilot`
   - or `/crux-compress ... --targets ...` if the team prefers one command
2. Generate target-specific outputs from the same canonical `.crux.md`
3. Add target templates and mapping rules for:
   - Cursor `.mdc`
   - Claude project instructions
   - ChatGPT system-prompt snippets
   - GitHub Copilot instruction files
4. Add parity validation so every target preserves:
   - core requirements
   - file paths
   - critical warnings
   - explicit quality gates
5. Report export summary:
   - targets generated
   - target paths
   - maintenance reduction estimate
   - parity validation status

### Website

1. Add a "Next Feature Idea" section to the landing page
2. Show one canonical CRUX source fanning out into 4 assistant targets
3. Include a small calculator for:
   - assistant count
   - monthly updates
   - minutes per target update
4. Display live savings:
   - duplicated edits avoided
   - monthly hours reclaimed
   - maintenance reduction percentage

### Documentation

1. Update `README.md` with:
   - the feature overview
   - quantifiable benefit
   - pros, cons, and alternatives
2. Update `CONTRIBUTORS.md` with review guidance for adapter/export proposals
3. Keep the website README aligned with the new interactive demo

## Example UX

```text
/crux-export @.cursor/rules/security-policy.md --targets cursor,claude,chatgpt,copilot
```

Example outputs:

```text
security-policy.crux.md
security-policy.cursor.crux.mdc
security-policy.claude.md
security-policy.chatgpt.md
.github/copilot-instructions.md
```

## Pros

- **One source of truth** for assistant instructions
- **Quantifiable maintenance savings** instead of vague productivity claims
- **Broadens CRUX beyond Cursor** into a cross-assistant workflow
- **Easy to explain on the website** with a strong before/after story
- **Reusable outside current themes** for onboarding packs, policy docs, support
  playbooks, and research handoff notes

## Cons

- every target has different formatting conventions and constraints
- target-specific behavior can drift even if the source stays correct
- validation is harder than single-output compression
- some teams may prefer one assistant-specific file that they hand-tune

## Risks

- overfitting adapters to unofficial prompt conventions
- giving users a false sense of parity when a target silently interprets
  instructions differently
- increasing maintenance burden if too many targets are supported too early

## Alternate similar approaches considered

| Approach | Benefit | Why not choose it first |
| --- | --- | --- |
| Context Budget Planner | Very measurable, easy to demo | Optimizes analysis, but does not solve cross-assistant instruction drift |
| Session Pack Builder | Expands CRUX into meetings, tickets, and handoffs | Broader scope, but much larger validation surface for a first expansion |
| Delta Compression for diffs/PRs | Very novel and efficient for iterative changes | Higher semantic risk and more complex to explain than adapters |
| Manual copy/paste templates | Simple and flexible | Preserves the duplication problem that CRUX is well-positioned to remove |

## Why this is the most useful next idea

This idea wins because it:

1. builds directly on a pattern the repo already understands: universal output
   plus adapter output
2. expands CRUX into a new product layer instead of only adding another input
   type
3. produces benefits that are easy to measure and easy to communicate
4. supports use cases beyond the current repository focus without abandoning the
   core CRUX value proposition

In short: it is more broadly useful than a planner, lower risk than delta
compression, and more obviously productizable than another one-off compressor.

## Validation plan

- create one canonical `.crux.md` fixture and export it to 4 targets
- compare generated outputs against a parity checklist
- verify critical instructions survive target conversion
- measure generated file counts and maintenance reduction math
- add at least one website example that shows the value without requiring repo
  internals

## Changes included in this draft PR

- draft PR description in this file
- README summary of the proposal
- contributor guidance for reviewing adapter/export proposals
- website feature-preview section with:
  - target tabs
  - quantified savings calculator
  - rationale and alternatives snapshot

## Open questions

- should this be a new `/crux-export` command or a `--targets` flag on
  `/crux-compress`?
- which target set should ship first: Cursor, Claude, ChatGPT, and Copilot, or
  a smaller initial trio?
- should parity validation be deterministic rule checks, LLM-based review, or a
  combination of both?
