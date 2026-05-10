---
branch: 2
depth: 3
subfocus_index: 8
subfocus: "Drawing the Boundary Between Automatic Recovery and User Escalation"
parent_subfocus: "Adversarial Verification as a Post-Hoc Failure Detection Mechanism"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

The parent subfocus established that adversarial verification catches real failures at a ~25% rate. But catching a failure is only half the problem — the harness then faces a branching decision: retry silently or escalate to the user. Getting this boundary wrong in either direction degrades the system — over-escalation fatigues the user, while over-recovery masks systemic rot. This subfocus develops a concrete decision framework for that boundary.

## Discoveries

### A Three-Axis Decision Model

Memory queries reveal that the auto-recovery vs escalation decision decomposes along three orthogonal axes. Each axis is a continuous spectrum, but together they yield a clear quadrant structure.

**Axis 1: Failure Mechanicity** — Is the failure mechanistic (deterministic, tool-level) or judgmental (semantic, content-level)?

- [memory:49303e0] The silent Write tool failure is the archetype of a *mechanistic* failure. The file wasn't persisted — nothing is ambiguous about this. The fix is deterministic: re-invoke Write, verify with `ls`. Auto-recovery is safe because the retry is idempotent and the success criteria is binary (file exists or doesn't).
- [memory:d944d7c] Spec index drift from subtask details is the archetype of a *judgmental* failure. The verifier found a discrepancy between two layers of documentation, but determining which layer is authoritative required understanding authorial intent. Auto-recovery here would mean the harness guessing which source is correct — and the first judge got it wrong, producing a false-positive CRITICAL finding. Escalation was the right call.

**Axis 2: Operation Reversibility** — Is the failed operation idempotent/reversible or destructive/irreversible?

- [memory:c71c143] This core memory establishes the bright line: destructive operations (delete, bulk archive, cascade removal) *always* escalate, even when the input is unambiguous. The rationale is sound — the asymmetry of regret. A false positive on escalation costs the user 10 seconds of confirmation; a false negative on auto-recovery costs irrecoverable knowledge loss.
- Idempotent operations (file writes, config regeneration, index rebuilds) carry no regret asymmetry — a redundant retry wastes compute but can't corrupt state.

**Axis 3: Verifier Confidence** — How certain is the verifier that the discrepancy it found is real?

- [memory:3bf625d] Verifiers (like synthesis agents) can hallucinate connections and invent discrepancies that don't exist. The "inferred" trust level is low — the verifier's judgment is itself uncertain. A harness that auto-recovers based on a low-confidence finding may be "fixing" something that isn't broken.
- [memory:dbfd3ed] File path verification (docs reference `.sh` but files are `.py`) is high-confidence — the check is mechanical (`ls` confirms or denies), so the verifier's finding is reliable.

### The Decision Matrix

Combining these axes yields a practical decision rule:

| Mechanistic + Idempotent + High Confidence | → **Auto-recover** |
|---|---|
| *Example*: File not on disk after claimed write. Retry write, verify with `ls`. |

| Mechanistic + Idempotent + Low Confidence | → **Auto-recover with audit trail** |
|---|---|
| *Example*: Doc path references stale extension. Fix is mechanical, but log the correction for human review in the summary. |

| Judgmental + Any Reversibility + Any Confidence | → **Escalate** |
|---|---|
| *Example*: Spec index contradicts subtask. Harness cannot determine intent; present both versions to user. |

| Any Axis + Destructive | → **Always escalate** |
|---|---|
| *Example*: Verifier suggests a memory is obsolete. Even if confidence is high, deletion requires user confirmation per [memory:c71c143]. |

| Any Failure + Low Verifier Confidence | → **Escalate or skip** |
|---|---|
| *Example*: Verifier "infers" a connection is wrong but has no concrete evidence. Present the finding but don't act on it. |

### The Hidden Risk: Auto-Recovery Masking Systematic Problems

This is the most insidious dimension and the one the memory corpus illuminates most clearly.

**The signal-eating problem**: Every auto-recovered failure is a failure the user never sees. If the Write tool silently fails 20% of the time and the harness silently retries, the user has no visibility into a tool reliability problem that should be reported upstream. The harness is eating a signal that would otherwise drive a root-cause fix.

**The retry counter as a circuit breaker**: The mitigation is straightforward — auto-recovery should track retry counts per failure category. A single Write tool failure → auto-retry. Three Write tool failures in the same execution → escalate, because the pattern suggests a systemic issue (permissions, disk space, path resolution bug), not a transient glitch.

[memory:6c16dc6] The 25% adversarial hit rate itself is an important signal. If auto-recovery handled even half of those 25%, the reported hit rate would drop to ~12%, and the team might conclude adversarial verification is less valuable than it actually is. The perceived ROI of verification depends on the visibility of what it catches.

**The advisory gate pattern**: [memory:b0c02ea] Plugin design patterns offer a relevant analogy — `failClosed: false` means "warn but preserve output." Applied to auto-recovery: recover but log prominently. The recovery happens, the output is preserved, but the user sees a clear warning. This is the "advisory auto-recovery" pattern — the system fixes the problem AND tells you it fixed it, so you can spot patterns.

### Cost-of-Retry as a Gating Factor

Not all retries are cheap. [memory:e05030c] Recursive subagent commands can be 10x+ more expensive than single-turn operations. A harness that auto-retries a failed meditate branch (spawning 13+ agents) has just doubled the API cost. The decision framework must weight retry cost:

- **Cheap retry** (file write, index rebuild, single tool call): Auto-recover freely for mechanistic failures.
- **Expensive retry** (multi-agent subtask, full spec execution, integration test suite): Always escalate, even for mechanistic failures, because the cost asymmetry flips — a wasted expensive retry is worse than a 30-second user confirmation.

## Connections

**1. The reversibility principle generalises beyond memory operations.** [memory:c71c143] was written about memory deletion specifically, but the underlying logic — "irreversible operations always escalate" — applies to any harness decision. Git force-pushes, database migrations, production deployments, cache invalidations that drop warm state: all sit on the "always escalate" side regardless of verifier confidence.

**2. Verifier fallibility mirrors synthesis hallucination.** [memory:3bf625d] warns about synthesis agents hallucinating connections. Adversarial verifiers face the exact same risk — they can "discover" a discrepancy that doesn't exist. [memory:d944d7c] is the concrete proof: the first judge hallucinated a CRITICAL finding from an incomplete read. A harness that auto-recovers based on a verifier's judgment inherits the verifier's error rate. The decision boundary must account for the verifier being wrong, not just the executor being wrong.

**3. Advisory gates bridge the auto-recover/escalate gap.** The binary choice (auto-fix silently vs block-and-ask) has a useful middle ground: fix-and-report. The plugin advisory pattern [memory:b0c02ea] demonstrates this — warn but don't block. Applied here: auto-recover mechanistic failures but emit a structured recovery log that the parent agent (or user) can review. This preserves velocity while maintaining signal visibility.

**4. Retry budgets prevent cost spirals in bounded execution.** This connects to the sibling facet on resource governance (without drifting into its territory): the retry decision isn't just about correctness — it's about cost. The harness needs a per-subtask retry budget (count-based and cost-based) that, once exhausted, forces escalation regardless of failure type. This is the circuit breaker that prevents auto-recovery from consuming unbounded resources.

## Summary

The boundary between auto-recovery and user escalation after adversarial verification hinges on three axes: **failure mechanicity** (tool-level vs semantic), **operation reversibility** (idempotent vs destructive), and **verifier confidence** (binary check vs inferred judgment).

**Auto-recover** when all three align favorably: mechanistic failure, idempotent operation, high verifier confidence, cheap retry cost. The canonical example is a silent file-write failure caught by `ls` — just retry.

**Always escalate** when any axis is unfavorable: judgmental failure (intent-dependent), destructive operation (irreversible), low verifier confidence (inferred rather than observed), or expensive retry (multi-agent re-execution).

The critical hidden risk is that auto-recovery eats failure signals, masking systematic problems behind invisible retries. The mitigation is **advisory auto-recovery**: fix the problem AND log it prominently, with a circuit breaker (retry counter per failure category) that escalates when the same category recurs, preserving both velocity and diagnostic visibility.
