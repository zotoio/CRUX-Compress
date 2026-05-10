---
branch: 2
depth: 2
subfocus_index: 3
subfocus: "Adversarial Verification as a Post-Hoc Failure Detection Mechanism"
parent_subfocus: "Failure Handling and Resilience in Multi-Agent Workflows"
timestamp: 2026-05-09T19:42:00+10:00
---

## Subfocus Rationale

Among the failure-handling strategies available to agent harnesses, adversarial verification occupies a unique niche — it doesn't prevent failures or retry them, it *discovers* them after the fact through independent cross-referencing. With a 25% empirical hit rate across 24 subtasks and documented cases of catching completely invisible failures (files that were never written, extensions that silently changed), adversarial verification demands dedicated analysis of its failure taxonomy, its decision boundaries, and its cost-benefit calculus.

## Discoveries

### The foundational principle

[memory:Agent-reported file creation must be verified on disk] The most important insight from the memory corpus is epistemological: **an agent's narrative is a hypothesis, not evidence.** Filesystem state is ground truth. An executing agent reported a file as created — with full contents, path, and verification steps in its work log — yet the file never existed on disk. The Write tool either failed silently or the content was emitted only to the chat UI. The agent had no way to know this because it "saw" the content in its own context window.

This inverts the default trust model. Without adversarial verification, the harness trusts the executor's self-report. With it, every claim is treated as falsifiable and checked against independent evidence.

### Empirical hit rate: 25% overall, 7-50% variance

[memory:Adversarial verification catches real documentation gaps] Across two plans:
- Plan 1 (crux-memories, 14 subtasks): 1 issue found (7%)
- Plan 2 (memories-plugin, 10 subtasks): 5 issues found (50%)
- Combined: 6 issues in 24 subtasks (25%)

The variance is the key signal. Plan 2 was an integration effort touching config, installer, docs, and distribution — exactly the cross-cutting pattern where failures hide at system boundaries. Plan 1 was mostly isolated skill implementations. The failure rate correlates with the degree of cross-cutting integration, not the number of subtasks.

### Failure categories: what adversarial verification excels at

Five distinct categories emerge from the memory corpus, all sharing the structural property of **cross-reference divergence across distributed sources of truth**:

1. **Silent persistence failures** — agent claims file was written; file doesn't exist ([memory:49303e0]). Adversarial advantage: fresh context means no confirmation bias.
2. **Documentation-reality drift** — docs reference `.sh` when actual files are `.py` ([memory:dbfd3ed]). Adversarial advantage: no muscle memory of historical filenames.
3. **Cross-file consistency violations** — spec index contradicts subtask details; command family expansion misses sibling cross-references ([memory:d944d7c]). Adversarial advantage: reads all layers simultaneously rather than relying on sequential recall.
4. **Default/spec misalignment** — tool hardcodes 20% compression target while spec says 25% ([memory:96a7410]). Adversarial advantage: approaches both files without assuming either is correct.
5. **Distribution completeness gaps** — file is in repo but missing from dist zip DIST_FILES ([memory:aba710d]). Adversarial advantage: checks delivery paths the developer workflow never exercises.

### Known weaknesses

Adversarial verification produces false positives when it lacks context about deliberate exceptions ([memory:62c0212] — 41 pre-existing SDK TypeScript errors flagged as new regressions; [memory:826c280] — judge demanded regeneration of a transient install artifact). It cannot detect semantic correctness, performance regressions, security vulnerabilities, or end-to-end integration flow failures — all of which require runtime execution rather than cross-reference inspection.

## Connections

**The cross-reference pattern**: All five "excels" categories involve a discrepancy between two independent sources of truth. Adversarial verification is fundamentally a cross-reference checker — it holds two documents side by side and reports divergence. Its structural advantage is that the verifier has no prior commitment to either source being correct.

**The false-positive / false-negative tradeoff**: A verifier with no historical context catches problems a biased executor would miss — but it also flags non-problems that an informed reviewer would ignore. The memory corpus contains both types: real catches (49303e0, dbfd3ed) and documented false-positive patterns (62c0212, 826c280). This suggests adversarial verification needs a **known exceptions manifest** — analogous to `.eslintignore` — that suppresses previously-triaged baseline noise.

**Specialization amplifies verification quality**: [memory:Specialized agents outperform generalPurpose] Specialized verifier agents carrying domain-specific checklists would catch more with fewer false positives than general-purpose reviewers. The typed checklist (distribution manifest check, path existence check, cross-reference check) is more effective than open-ended "verify correctness."

## Child Subfocuses

### Child 1 (depth-3-sub-7): Taxonomy of Failure Categories
**Rationale**: The aggregate 25% hit rate is uninformative for resource allocation. Mapping specific failure categories to their detection mechanisms reveals where verification effort yields the highest returns and where it's structurally blind.

### Child 2 (depth-3-sub-8): Recovery vs Escalation Boundary
**Rationale**: Catching a failure is only half the problem. The harness must then decide whether to retry silently or present the discrepancy to the user. Getting this boundary wrong in either direction degrades the system — over-escalation fatigues the user; over-recovery masks systematic rot.

### Child 3 (depth-3-sub-9): Verification Sampling Strategy
**Rationale**: Universal verification is wasteful at a 7% hit rate and insufficient at 50%. A risk-targeted sampling strategy grounded in empirical failure categories optimizes the cost-benefit tradeoff.

## Child Insights

### From depth-3-sub-7: Failure Taxonomy

The taxonomy reveals a clean structural pattern: adversarial verification excels at detecting **cross-reference divergence** — any failure where truth is distributed across multiple files and a single agent works on them sequentially. Five categories (persistence, documentation drift, cross-file consistency, default/spec alignment, distribution completeness) all share this property.

The taxonomy also identifies a critical counter-pattern: **false-positive inflation from missing context**. Pre-existing SDK errors, transient install artifacts, and spec-layer authority rules all produced confident-sounding CRITICAL findings that were categorically wrong. The mitigation is a "known exceptions manifest" — a pre-loaded set of patterns the verifier should not flag.

The structural insight is that self-verification fails because the agent's context window is a single thread (no cross-file comparison), while adversarial verification fails because its fresh context lacks institutional knowledge (no historical exceptions). The ideal system combines both: adversarial checks augmented with a baseline knowledge document.

### From depth-3-sub-8: Recovery vs Escalation Framework

The decision boundary decomposes along three axes:
1. **Failure mechanicity**: Mechanistic/tool-level failures (file not persisted) → auto-recover. Judgmental/semantic failures (spec index contradicts subtask) → escalate.
2. **Operation reversibility**: Idempotent operations → auto-recover is safe. Destructive operations → always escalate, even with high confidence.
3. **Verifier confidence**: High confidence (binary check via `ls`) → auto-recover. Low confidence (inferred discrepancy) → escalate.

The critical hidden risk is that auto-recovery **eats failure signals**, masking systemic problems. The mitigation is **advisory auto-recovery**: fix the problem AND log it prominently, with a circuit breaker (retry counter per failure category) that forces escalation when the same failure category recurs. This preserves both execution velocity and diagnostic visibility.

A fourth dimension — **retry cost** — gates even mechanistic failures: cheap retries (file writes, index rebuilds) are auto-recoverable, but expensive retries (multi-agent subtask re-execution) should always escalate because the cost asymmetry flips.

### From depth-3-sub-9: Verification Sampling Strategy

A three-tier graduated model optimizes the cost-benefit tradeoff:

| Tier | Scope | Cost | Trigger |
|------|-------|------|---------|
| 1 — Automated checks | ALL subtasks | Near-zero (shell commands: `ls`, `git status`, size checks) | Default |
| 2 — Targeted adversarial | HIGH-RISK subtasks | 1 agent invocation | Risk score ≥ 3 |
| 3 — Deep specialized audit | CRITICAL subtasks | Specialized verifier agent | Risk score ≥ 5 |

The risk heuristic assigns points based on empirically-observed failure categories: file creation (+3), cross-cutting registration (+3), documentation with paths (+2), first-time agent assignment (+2), spec/subtask misalignment (+2).

Key cost-reduction strategies: (1) run verifiers in parallel with the next phase's implementation agents — converts verification from a serial bottleneck to parallel overhead; (2) batch related checks into single agent passes using the shared-agent-runs pattern; (3) use advisory gates (`failClosed: false`) so only critical findings block progression.

The core economic insight: verification is a fixed bounded cost (one agent invocation) while undetected failure cost compounds across sessions and is potentially unbounded — making even moderate-hit-rate verification strongly positive expected value when targeted at high-risk subtasks.

## Summary

Adversarial verification is the most empirically-grounded failure detection mechanism in the memory corpus, with a 25% hit rate across 24 subtasks and documented catches of completely invisible failures. Its power comes from the **cross-reference divergence** structural pattern — an independent agent with no prior context can check claims against ground truth in ways the executing agent structurally cannot. Five failure categories are well-served (silent persistence, documentation-reality drift, cross-file consistency, default/spec alignment, distribution completeness); semantic correctness, performance, and security are not.

The system's three key design decisions are: (1) **graduated verification** — automated filesystem checks on all subtasks, targeted adversarial review on risk-scored high-value subtasks, deep specialized audits on critical ones; (2) **advisory auto-recovery** — fix mechanistic failures but log them with circuit-breaker escalation, always escalate judgmental failures and destructive operations; (3) **known exceptions manifest** — suppress false positives from pre-existing baseline noise, transient artifacts, and deliberate exceptions. Together, these transform adversarial verification from a uniform tax on all subtasks into a targeted, cost-effective quality amplifier.
