---
branch: 2
depth: 3
subfocus_index: 9
subfocus: "Cost-Benefit Calculus of Universal vs Sampled Adversarial Verification"
parent_subfocus: "Adversarial Verification as a Post-Hoc Failure Detection Mechanism"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

The 25% overall hit rate masks extreme variance (7% vs 50%) across plans, which means universal verification wastes budget on low-risk plans while under-investing in high-risk ones. A risk-based sampling strategy needs concrete heuristics grounded in the failure modes we've actually observed.

## Discoveries

### The empirical cost model

From memory `6c16dc6`: across 24 subtasks in two plans, adversarial verification caught 6 issues (25% aggregate). But the per-plan breakdown is the actionable signal:

| Plan | Subtasks | Issues found | Hit rate |
|------|----------|-------------|----------|
| 20260403-crux-memories | 14 | 1 | 7% |
| 20260404-memories-plugin | 10 | 5 | 50% |

The cost of verification is one additional agent invocation per subtask (~60-120s wall-clock, ~1x the implementation cost). Universal verification on the first plan spent 13 verifier invocations to find 1 issue — a 7% yield. On the second plan, every second verification found something. The question is: what distinguishes the two plans *ex ante*?

### Risk signals from the memory corpus — five high-risk subtask categories

Cross-referencing the failure modes captured in memories reveals empirically-grounded risk categories:

**1. File-creation subtasks** (memory `49303e0`): The Write tool can silently fail. An agent can report a file as created with a complete work log while the file doesn't exist on disk. This was caught *only* by adversarial verification — the executing agent's self-report was a detailed false positive. File-creation subtasks have the highest observed failure severity (complete deliverable missing, zero partial credit). **Risk: CRITICAL — mandatory verification.**

**2. Cross-cutting completeness changes** (memory `aba710d`): When a new feature file must be registered in multiple independent systems (config, installer, docs, dist zip, evals), omissions in one system survive multiple sessions because the other systems don't cross-check. The dist-zip omission survived config integration, installer integration, docs integration, and eval integration — five checkpoints, all passing, one system missed. **Risk: HIGH — verify any subtask whose deliverable touches 3+ independent registration points.**

**3. Documentation path references** (memory `dbfd3ed`): Documentation that references file paths (file trees, installation guides, hook listings) can silently drift when files are renamed or re-extensioned. The `.sh` → `.py` rename was invisible to the implementing agent. **Risk: MODERATE-HIGH — verify documentation subtasks that include file trees or path references.**

**4. First-time agent assignments** (memory `e3c5837`, inverted): Specialized agents outperform generalPurpose agents, but the *first* time a specialized agent is assigned a new task category, the risk of miscalibrated domain context is elevated. This is inferred rather than directly observed — no memory captures a first-assignment failure, but the specialization advantage implicitly means the first run lacks the tuning benefit. **Risk: MODERATE — verify first-time pairings.**

**5. Spec-to-subtask drift** (memory `d944d7c`): Spec index text can contradict subtask details. When a subtask implements based on one layer while verification checks the other, false positives result. But when the subtask itself is the drifted artifact, the implementation may be subtly wrong. **Risk: MODERATE — verify subtasks whose requirements differ between the spec index and the subtask file.**

### The graduated verification model

Combining the skip-by-default cost gating pattern (memory `e05030c`) with the advisory quality gate pattern (memory `b0c02ea`) suggests a three-tier verification architecture:

**Tier 1 — Lightweight automated checks (ALL subtasks, zero marginal agent cost):**
- `ls` existence check on every claimed file output
- `git status` confirms expected files appear as new/modified
- Byte-count sanity check (non-zero size, within expected range)
- These are shell commands, not agent invocations — near-zero cost

**Tier 2 — Targeted adversarial verification (HIGH-RISK subtasks, one agent per subtask):**
- Full independent agent review with filesystem cross-checks
- Applied when risk heuristics flag the subtask (see below)
- This is the current adversarial verification model, but applied selectively

**Tier 3 — Deep structural audit (CRITICAL subtasks, specialized verifier agent):**
- Specialized verifier agent with domain-specific checklists
- Applied to file-creation subtasks and cross-cutting registration subtasks
- Could use the batching pattern (memory `6415c52`) to verify multiple related subtasks in a single agent pass — e.g., all subtasks in a phase that produce files could be batch-verified by one agent

### Risk-based heuristic scoring

Each subtask gets a risk score. If the score exceeds a threshold, it gets Tier 2 or Tier 3 verification:

| Signal | Points | Source |
|--------|--------|--------|
| Subtask creates new files | +3 | memory `49303e0` — silent Write failures |
| Subtask touches 3+ registration points | +3 | memory `aba710d` — dist-zip omission pattern |
| Subtask updates documentation with file paths | +2 | memory `dbfd3ed` — stale path references |
| First-time agent type for this task category | +2 | inferred from memory `e3c5837` |
| Subtask has spec-index/subtask-detail misalignment | +2 | memory `d944d7c` |
| Subtask modifies cross-cutting config files | +1 | general risk signal |
| Subtask is in the plan's final phase | +1 | integration-phase errors compound |

**Threshold**: score ≥ 3 → Tier 2 verification. Score ≥ 5 → Tier 3 verification. Score < 3 → Tier 1 only.

### The cost-of-undetected-failure asymmetry

The core economic argument: the cost of one verification agent (~60-120s, ~1x implementation cost) vs the cost of an undetected failure:

- **File not persisted** (memory `49303e0`): Required a separate remediation subtask. Cost: 1x implementation + coordination overhead + re-verification. The verification would have cost 1x; the fix cost 2-3x.
- **Dist-zip omission** (memory `aba710d`): Survived *multiple sessions*. Cost: every user who installed via zip lacked the feature, plus eventual debugging time. Verification cost: 1x agent. Failure cost: unbounded user impact.
- **Stale doc paths** (memory `dbfd3ed`): Silently wrong documentation erodes trust. Verification cost: 1x. Failure cost: user confusion, support burden, credibility loss.

The ratio is asymmetric: verification is a fixed, bounded cost (one agent invocation). Undetected failure cost is variable and can compound across sessions. For high-risk categories, the expected value of verification is strongly positive even at a 25% hit rate.

### Parallelism absorbs verification cost

Memory `efc4c24` shows that within-phase parallelism achieves near-linear speedup. Verification agents can run in parallel with the *next phase's* implementation agents — the verification doesn't need to gate the pipeline if it's advisory (memory `b0c02ea`). This converts verification from a serial bottleneck into a parallel overhead that adds minimal wall-clock time. The advisory model means: if verification finds an issue, flag it as a warning and let the orchestrator decide whether to block or continue. Blocking is reserved for Tier 3 (critical) findings.

## Connections

**Skip-by-default maps directly to verification tiers.** The expensive-eval gating pattern (memory `e05030c`) — skip by default, opt in explicitly — is structurally identical to the verification sampling problem. Tier 1 (cheap automated checks) runs by default on everything. Tier 2 and 3 (expensive agent-based checks) are gated behind risk heuristics, analogous to `SDK_EVAL_SKIP_EXPENSIVE`. The heuristic scoring replaces the manual env-var toggle with an automated risk assessment.

**Batched verification reduces marginal cost.** The shared-agent-runs pattern (memory `6415c52`) collapses N agent calls to 1 when assertions are independent. Applied to verification: a single verifier agent could check all file-creation subtasks in a phase simultaneously, collapsing 3-5 individual verifications into 1 batch pass. This is especially effective when Tier 3 checks are needed on multiple subtasks in the same phase.

**Advisory gates prevent verification from becoming a bottleneck.** The plugin design pattern (memory `b0c02ea`) — `failClosed: false`, warn but preserve output — maps to verification that flags issues without blocking the pipeline. Only critical findings (missing files, broken paths) should gate progression; stylistic or documentation completeness findings can be advisory warnings resolved in a cleanup pass.

**The 50% plan was integration-heavy.** The 20260404-memories-plugin plan was a plugin integration effort touching config, installer, docs, and distribution — exactly the cross-cutting registration pattern that memory `aba710d` warns about. The 7% plan was mostly isolated skill implementations. The risk heuristic would have correctly assigned higher verification budgets to the integration plan's subtasks.

## Summary

Universal adversarial verification is wasteful at a 7% hit rate and insufficient context at a 50% hit rate — the right answer is **graduated, risk-targeted verification**. Three tiers: (1) automated filesystem checks on all subtasks at near-zero cost, (2) targeted adversarial review on subtasks scoring ≥3 on a risk heuristic (file creation, cross-cutting registration, documentation paths, first-time agent assignments), (3) deep specialized audit on subtasks scoring ≥5. The risk heuristic is grounded in five empirically-observed failure categories from the memory corpus. Verification cost is further amortized by running verifiers in parallel with the next phase and batching related checks into single agent passes. The key economic insight: verification is a fixed bounded cost while undetected failure cost compounds across sessions — making targeted verification strongly positive expected value even at moderate hit rates.
