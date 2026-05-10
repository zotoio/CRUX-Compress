---
branch: 3
depth: 3
subfocus_index: 8
subfocus: "Hard-stop vs negotiable cap failure semantics"
parent_subfocus: "Hard resource caps composing with adaptive escalation strategies"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

The distinction between hard-stop and negotiable caps is the most fundamental design decision when adding a resource limit to an agent harness. The failure semantics that follow from this classification determine whether the system can self-recover, whether data is lost, and what the user experiences — making this taxonomy the prerequisite for any composition strategy.

## Discoveries

### Hard-Stop Caps Observed in the Corpus

| Cap | Mechanism | Failure Mode |
|-----|-----------|--------------|
| `maxDepth: 3` (meditate) | Agent simply does not recurse further | Graceful termination — depth-3 agents produce output normally, they just don't spawn children |
| Destructive op confirmation | No `--yolo` bypass exists; `c71c143` establishes this as permanent | Operation refuses to execute — the system halts at the gate and waits indefinitely for user input |
| `SDK_EVAL_MAX_DURATION_MS` (60min) | Process kill signal | Abrupt termination — in-flight work is lost, no cleanup |
| Read-only exploration contract (`31fec9d`) | No write-capable skills provided to child agents | Structural impossibility — the agent cannot violate the cap even if it "wants" to |

### Negotiable Caps Observed

| Cap | Mechanism | Failure Mode |
|-----|-----------|--------------|
| `compressionTarget: 33%` | Iterative reduction in 10pp steps down to 5% | Degraded quality — more aggressive compression trades readability for fit |
| `maxCandidateFacts: 5` | Configurable threshold | Soft truncation — excess candidates are ranked out, not destroyed |
| Advisory quality gates (`b0c02ea`) | `failClosed: false` → warn + preserve output | No data loss — operation completes but with a warning annotation |
| Per-test timeouts | Configurable, can be raised | Retry opportunity — the test can be re-run with a higher timeout |

### The `maxMemorySize` Hybrid

Memory `da3d798` reveals a fascinating hybrid: `maxMemorySize` (1000 lines) is a HARD cap — a file cannot exceed it — but the *path to compliance* is NEGOTIABLE (adaptive escalation from 33% → 23% → 13% → 5%). The cap itself is absolute; only the strategy for meeting it is flexible. When even maximum compression fails, the system escalates to the human ("flag for manual review") rather than truncating. This preserves the "never lose data silently" invariant even at the hard boundary.

## Connections

### Determining Factor: Reversibility of Violation

The pattern that emerges across all examples is: **a cap is hard when violating it would produce an irreversible harm that the system cannot self-correct**.

- **Destructive ops** → deletion is irreversible → hard gate
- **Recursion depth** → unbounded recursion exhausts resources irreversibly (cost, time, context windows) → hard stop
- **Wall-clock deadline** → unbounded cost accumulation is irreversible (money spent) → hard kill
- **Read-only contract** → unintended writes during exploration corrupt state irreversibly → structural enforcement

Conversely, a cap is negotiable when the degradation from violating the *target* is:
1. **Reversible** — output can be regenerated at a different quality level
2. **Bounded** — degradation gets worse gradually, not catastrophically
3. **Observable** — the system can detect it hasn't met the target and try again

### Failure Semantics Follow Classification

| Classification | Failure semantic | User experience |
|---------------|-----------------|-----------------|
| Hard-stop (structural) | Impossibility — the system lacks the capability to violate | Invisible — user never encounters the boundary |
| Hard-stop (gate) | Halt-and-wait — execution pauses indefinitely | Interactive — user must act to proceed |
| Hard-stop (kill) | Abort — in-flight work is lost | Disruptive — user must retry from scratch |
| Negotiable (iterative) | Degrade-and-retry — quality decreases, system retries at new level | Transparent — user sees degraded output but gets a result |
| Negotiable (advisory) | Warn-and-proceed — operation completes with annotation | Seamless — user may not even notice |

### The "Gate Hardness" Spectrum

Not all hard caps are equally hard. Within the hard category, there's a spectrum of *cost of encountering the boundary*:

1. **Structural impossibility** (cheapest) — the cap is never encountered because the system architecture prevents it. Example: read-only exploration agents that lack write tools.
2. **Graceful termination** — the cap is encountered but the system handles it cleanly. Example: depth-3 agents produce output and stop.
3. **Halt-and-wait** — execution blocks until human intervention. Example: destructive op confirmation.
4. **Abort** (most expensive) — the cap kills execution mid-flight. Example: wall-clock deadline.

Good harness design moves caps UPWARD on this spectrum where possible: prefer structural impossibility over graceful termination, prefer graceful termination over halt-and-wait, prefer halt-and-wait over abort.

### Classification Criteria (Decision Framework)

A resource limit should be classified as **hard-stop** when ANY of these hold:
- Violation causes irreversible data loss or corruption
- Violation's cost grows without bound (exponential cost, infinite recursion)
- The operation being bounded is inherently binary (user consent: yes/no, not "how much")
- External constraints mandate it (API cost budgets, regulatory requirements)

A resource limit should be classified as **negotiable** when ALL of these hold:
- Violation produces degraded-but-usable output
- The system can detect violation and retry with adjusted parameters
- The degradation path has a natural floor (there's a "most aggressive" setting)
- No irreversible harm occurs at any point on the degradation path

## Summary

Hard-stop caps protect against irreversible harms (data loss, unbounded cost, unauthorized state mutation) through mechanisms ranging from structural impossibility to process termination. Negotiable caps protect quality targets through iterative degradation-and-retry loops that always terminate (either successfully or by escalating to a hard gate like "flag for manual review"). The determining factor is reversibility: if violating a boundary produces harm that cannot be automatically undone, the cap must be hard. The `maxMemorySize` hybrid pattern — hard boundary with negotiable compliance path — represents the ideal composition: the system tries progressively harder to fit, but when all strategies fail, it escalates to the human rather than losing data. This taxonomy directly informs harness design: caps should be classified at definition time, and their failure semantics should be explicit in the interface contract, not emergent from implementation details.
