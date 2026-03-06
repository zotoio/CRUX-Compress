# [2026-03-06] feature idea

## Title

CRUX Memory Capsules for transcripts, incidents, and customer calls

## Status

Draft proposal. This change adds a proposal, example assets, and website framing for a future feature. It does **not** claim that transcript compression is fully implemented in the product today.

## Summary

CRUX should expand beyond rules, code, and images into a new class of high-value content: long-form conversational material such as:

- incident review transcripts
- customer research calls
- sales discovery calls
- planning meetings
- support escalations

The feature idea is a new output pattern called a **Memory Capsule**: a compact CRUX artifact optimized for agent handoff, retrieval, and reloading into context windows.

Instead of forcing an agent to reread a 45-90 minute transcript every time work resumes, CRUX would preserve the parts that matter most:

- decisions
- disagreements
- timeline
- metrics
- owners
- follow-up work
- unresolved risks

## Why this is useful

The largest untapped token waste in AI workflows is often not code or rules. It is operational and conversational history.

A single transcript can be larger than the code the agent is meant to reason about. Teams repeatedly reload those transcripts when they:

- resume incident response
- prepare executive summaries
- build retrospectives
- brief new teammates
- hand work between shifts or agents

This is a better next-step feature than another code-adjacent improvement because it opens a new use case where the token savings are both immediate and easy to measure.

## Quantifiable benefit

Projected benefits for a 60-minute transcript:

| Metric | Raw transcript | Memory Capsule target | Benefit |
| --- | --- | --- | --- |
| Context size | 12,000-16,000 tokens | 700-1,100 tokens | 91-95% reduction |
| 128k context capacity | 8-10 transcripts | 116-182 capsules | 14x-18x more historical sessions loaded |
| Handoff artifact length | 20-40 pages | 1-2 pages | Much faster re-entry for humans and agents |

Projected benefits for incident management:

- one agent can keep multiple incidents in context at once instead of one transcript at a time
- support and engineering can share the same compact artifact instead of rewriting separate summaries
- follow-up tasks become machine-readable enough to convert into tickets, runbooks, or checklists

The example added in this PR uses a smaller synthetic incident review transcript and shows the intended pattern in concrete form.

## Proposed feature

Add a future compression mode oriented around transcript-to-memory workflows.

Proposed command direction:

```bash
/crux-compress @incident-review-transcript.md --mode memory
```

Proposed output patterns:

- `M.session{}` for participants, date, scope, and constraints
- `Γ.timeline{}` for sequence of events
- `E.decisions{}` for committed choices and reversals
- `P.followup{}` for owners, due dates, and unresolved work
- `Ω.risks{}` for ambiguity, confidence, and caveats

## Pros

1. **New market surface area**
   - Expands CRUX beyond current content families into operational memory and knowledge transfer.
2. **Extremely high token return**
   - Transcripts are repetitive, speaker-heavy, and structurally compressible.
3. **High practical value**
   - Incident response, discovery synthesis, and support escalations are frequent, expensive workflows.
4. **Strong alignment with agent workflows**
   - Capsules can become reusable context objects rather than one-off summaries.
5. **Easy to explain**
   - "Turn a one-hour call into a one-page memory object" is a strong product story.

## Cons

1. **Loss of nuance**
   - Tone, hesitation, and side conversations may matter more than they appear.
2. **Speaker attribution risk**
   - Decisions can be less useful if ownership is compressed too aggressively.
3. **Privacy sensitivity**
   - Calls and support conversations often contain confidential details.
4. **Validation is harder**
   - Semantic correctness for conversational material is less binary than code or rules.
5. **Formatting variance**
   - Call transcripts arrive in many inconsistent formats and cleanup quality varies a lot.

## Similar approaches considered

### 1. Conventional meeting summarization

**What it is:** A plain-language summary, action list, and decisions block.

**Pros**
- Familiar to users
- Quick to generate

**Cons**
- Harder to make structurally reusable by agents
- Lower compression consistency
- Easier to omit edge-case detail

### 2. Chunking plus retrieval

**What it is:** Split transcripts into embeddings-friendly chunks and fetch relevant passages later.

**Pros**
- Good for source-grounded lookup
- Avoids aggressive lossy compression

**Cons**
- Still leaves long raw text in the system
- Weaker for compact handoff and session reload
- More infrastructure-heavy than a portable artifact

### 3. Decision-log extraction only

**What it is:** Capture decisions and owners without retaining the full session shape.

**Pros**
- Smaller and simpler
- Useful for executives

**Cons**
- Drops crucial context
- Weak for debugging, support, and disagreement replay

### 4. Timeline-only incident compression

**What it is:** Focus only on event chronology for outages and operational reviews.

**Pros**
- Good for postmortems
- Easy to measure

**Cons**
- Too narrow
- Misses customer calls and planning sessions

## Why this idea is the most useful

This idea wins because it balances three things at once:

1. **Novelty**
   - It expands CRUX into a domain not already emphasized in the codebase.
2. **Measurable value**
   - Transcript token counts are large enough that savings are obvious and repeatable.
3. **Platform leverage**
   - The same core CRUX concepts already map well to decisions, timelines, entities, and follow-up work.

In short: it opens a bigger category than another documentation feature while still feeling native to what CRUX is best at.

## Proposed code changes in this PR

This draft PR intentionally focuses on proposal assets and product framing, not a finished transcript parser.

Included in this draft:

- a dated proposal document in `docs/feature-ideas/`
- a synthetic transcript example under `web/compress.md/assets/transcript-example/`
- a matching CRUX Memory Capsule example
- a new landing-page section presenting the concept as a draft feature idea
- README updates that clearly label the idea as future-facing

Future implementation work, not included here:

- transcript-oriented compression guidance
- semantic validation criteria for conversational material
- support for transcript-specific block conventions
- optional redaction policies for sensitive content

## Proposed website changes

- Add a **Feature Idea - Draft** section after existing code compression examples.
- Show a before/after transcript-to-capsule example.
- Include projected savings and "why now" messaging.
- Keep the wording explicitly roadmap-oriented so the site does not overstate current functionality.

## Success metrics

If implemented later, the feature should be considered successful when it can reliably achieve:

- at least **85% token reduction** on messy real-world transcripts
- at least **90% semantic validation confidence** on synthetic transcript fixtures
- at least **80% evaluator agreement** that owners, decisions, and follow-ups were preserved
- at least **5x more prior sessions** fitting into the same context budget in user testing

## Rollout plan

1. Ship the concept publicly as a draft idea
2. Collect feedback on the structure of a Memory Capsule
3. Add fixtures for incident, sales, and support transcripts
4. Define transcript-specific CRUX guidance
5. Prototype a `--mode memory` path
6. Evaluate semantic fidelity before claiming product support

## Risks and guardrails

- Keep all copy labeled as a proposal until implementation exists
- Do not imply transcript support in install or quickstart paths yet
- Validate on multiple transcript types before locking a schema
- Consider redaction and privacy workflows before productionizing
