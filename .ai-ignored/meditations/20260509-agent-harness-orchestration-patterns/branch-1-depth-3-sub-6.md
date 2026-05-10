---
branch: 1
depth: 3
subfocus_index: 6
subfocus: "The Knows-vs-Acts Gap"
parent_subfocus: "Session-Scope State Propagation"
timestamp: 2026-05-09T19:38:00+10:00
---

## Subfocus Rationale

State propagation mechanisms (alwaysApply rules, spawn-time arguments, shared config) are necessary but not sufficient for behavioral compliance. The deepest challenge is the gap between an agent *having access to* a directive and *acting on* it — a gap that is invisible without observability and independent verification.

## Discoveries

### 1. The Dual-MUST Conflict in Memory Rules

[Recalled — memories/learning/session-scope-subagent-patterns.memory.md, ba74013] The amnesia inheritance contract states: "subagents spawned for ordinary work inherit the amnesia state and **must** suppress ambient memory usage."

[Discovered — .cursor/rules/crux-memories-integration.md, line 30] The same alwaysApply rule also states: "you **MUST** include `[memory:{title}]` in your output."

These two MUSTs directly conflict when amnesia is active. The rule contains conditional logic (amnesia → suppress; enabled → annotate), but from the LLM's attention perspective, two MUST directives in the same loaded rule compete for priority. The "knows" (both directives are loaded) does not guarantee the "acts" (the conditional override is correctly evaluated). This is structural: the LLM must parse conditional precedence from natural language, which is not a reliable operation.

### 2. Output Absence as the Only Compliance Signal

[Discovered — evals/sdk/tests/p-amnesia.test.ts, P3 describe block] The eval test for amnesia subagent inheritance checks for the *absence* of `[memory:` annotations in subagent output. This is a negative assertion — proving something did NOT happen.

Negative assertions have a fundamental weakness: they succeed for two very different reasons — the agent correctly suppressed memory usage, OR the agent simply didn't find relevant memories. The test creates a memory fixture tagged with `["auth", "jwt", "scaling"]` and then asks the agent to "create a utility function that validates email addresses" — a deliberately unrelated task. But this means a passing test is ambiguous: did the agent suppress memories because of amnesia, or because no memory was relevant?

A stronger test would ask a question where a memory IS relevant (e.g., "How should I implement authentication?") after enabling amnesia, and verify the annotation is still absent. The P1 test does this partially (line 140-149 asks about authentication during amnesia), but P3 specifically tests subagent inheritance with an unrelated prompt, weakening the signal.

### 3. The afterAgentResponse Hook as Ground-Truth Observability

[Discovered — .cursor/hooks/crux-track-memory-references.py] The `afterAgentResponse` hook scans agent output for `[memory:{title}]` annotations and updates `.refs.yml` tracker files. This is an observability mechanism that produces ground-truth evidence: if tracker files are updated, the agent annotated; if not, it didn't.

This hook is the closest thing the system has to detecting the knows-vs-acts gap in production. During amnesia, the hook will find no annotations and produce no tracker updates — which is correct behavior. But critically, the hook cannot distinguish "amnesia correctly suppressed annotation" from "the agent forgot to annotate" (a separate compliance failure described in the next section).

### 4. Annotation Compliance Is Itself a Knows-vs-Acts Gap

The `[memory:{title}]` annotation requirement is itself subject to the knows-vs-acts gap. The integration rule says agents MUST annotate, but there is no mechanism to detect when an agent was influenced by a memory but failed to annotate. The hook only detects *present* annotations; absent annotations are invisible.

This creates a recursive observability problem: the mechanism for tracking memory usage (annotations) is itself unreliable because the agent may not comply with the annotation directive, and the mechanism for detecting non-compliance with annotations doesn't exist.

### 5. Ground-Truth Side Effects as the Only Reliable Verification

[Recalled — memories/learning/sdk-single-turn-requires-non-interactive-directives.memory.md, fcd2f69] The eval pattern of checking "ground-truth side effects" (files on disk, git status changes) rather than agent narratives is directly applicable. For behavioral compliance, the equivalent is: don't check whether the agent *says* it suppressed memories; check whether memory-related *artifacts* were modified.

[Recalled — memories/redflag/agent-reported-file-creation-must-be-verified-on-disk.memory.md, 49303e0] The canvas-file incident proves that agent self-reports are unreliable for verifying effects. The agent claimed creation; the file didn't exist. Applied to state propagation: a child agent might report "respecting amnesia mode" in its work log while still loading and using memories.

### 6. The Tooling-Defaults Drift Parallel

[Recalled — memories/redflag/tooling-defaults-must-align-with-spec.memory.crux.md, 96a7410] The compression-target drift (tool used 20%, spec said 25%) is structurally identical to the knows-vs-acts gap. The tool was built to implement the spec (it "knew" the correct default), but it "acted" with a different one. The mismatch was invisible until someone independently compared the two values.

This suggests that every interface between "specification" and "implementation" — whether between a spec and code, or between a rule and an LLM's behavior — is subject to silent drift. The LLM equivalent of "hardcoded wrong default" is "loaded the rule but applied a different behavior due to attention dynamics."

### 7. Multi-Layer State Drift

[Recalled — memories/redflag/spec-index-can-drift-from-subtask-details.memory.md, d944d7c] Spec index vs. subtask details is an exact structural parallel. The spec index (analogous to the parent's spawn-time prompt) says one thing; the subtask details (analogous to the child's loaded alwaysApply rules) may say something subtly different. The subtask/child is authoritative because it's closer to execution — but the parent/spec-index may override in the reader's mind because it was seen first.

For agent state propagation: the spawn-time prompt is the "spec index" (written once, may be stale), while the alwaysApply rules are the "subtask details" (loaded at runtime, closer to ground truth). If they conflict, which wins? The LLM has no formal precedence mechanism; it depends on attention weights, prompt position, and the specific phrasing used.

## Connections

### Connection 1: Observability as the Bridge

The pattern across all discovered evidence points to a single principle: **observability of effects is the only reliable way to bridge the knows-vs-acts gap.** Neither self-reports (memory 49303e0), nor rule loading (the alwaysApply mechanism), nor directive prompts (spawn-time arguments) provide guarantees. Only independent verification of observable side effects — filesystem checks, absence of annotations, tracker file state — can confirm that propagated state actually influenced behavior.

The `afterAgentResponse` hook (reference tracker) is a partial implementation of this principle: it observes actual annotations rather than trusting that the agent will annotate. But it only works in one direction (detecting presence, not detecting absence of expected annotations).

### Connection 2: The Compliance Testing Pyramid

The evidence suggests a hierarchy of compliance verification, from weakest to strongest:

1. **Directive compliance** (weakest): "I told the child to do X" — no verification that X happened
2. **Self-reported compliance**: "The child says it did X" — memory 49303e0 proves this is unreliable
3. **Output-pattern compliance**: "The child's output does/doesn't contain markers of X" — the P3 eval test, stronger but still ambiguous (negative assertions)
4. **Side-effect compliance**: "The filesystem/tracker state is consistent with X having happened" — the ground-truth assertion pattern from fcd2f69
5. **Adversarial verification** (strongest): "An independent agent verified that X happened by examining effects" — memory 6c16dc6, 25% issue detection rate

Each level costs more but catches more failures. The current system operates at levels 1-3 for most state propagation; only spec execution uses level 5.

### Connection 3: The Attention Competition Model

[Inferred] The knows-vs-acts gap may be modeled as an attention competition problem. When a child agent loads its context, multiple sources compete for behavioral influence:

- System prompt (highest implicit priority)
- AlwaysApply rules (loaded early, high salience)
- Spawn-time prompt directives (variable position, may be buried in a long Task description)
- Loaded skills and agent definitions (task-specific)

The amnesia rule places the override in an alwaysApply rule (highest propagation guarantee), but the annotation MUST directive is in the *same rule*. The conditional logic that determines which MUST applies depends on the LLM correctly tracking session state that was communicated via the spawn-time prompt — the least salient channel.

This implies a design principle: **state that needs to override default behavior should be communicated through the highest-salience channel available, not just the most architecturally correct one.** The alwaysApply rule is correct for defining the contract; the spawn-time prompt is correct for communicating the current state; but neither alone guarantees the child will correctly combine the two.

### Connection 4: Hallucination as a Knows-vs-Acts Instance

[Recalled — memories/redflag/meditate-synthesis-must-not-hallucinate-connections.memory.md, 3bf625d] The meditate hallucination redflag describes agents that "know" they should distinguish recalled vs. inferred content, yet fail to maintain that distinction in their output. This is the knows-vs-acts gap applied to behavioral constraints rather than state propagation — the agent loaded the rule about provenance labeling but deprioritized it in practice.

This generalizes the gap beyond state propagation: any behavioral constraint that an LLM is told to follow is subject to the same failure mode. State propagation is just the most visible case because it involves a boundary crossing (parent → child) where the gap becomes detectable.

## Summary

The knows-vs-acts gap is the fundamental challenge in agent state propagation: having a directive loaded into context does not guarantee behavioral compliance. This repository's own evidence demonstrates the gap in multiple forms — file creation claims without filesystem effects (49303e0), tooling defaults that drift from specifications (96a7410), and dual-MUST conflicts where conditional overrides compete with base directives in the same rule.

The only reliable detector is observability of effects, not of intentions. The reference tracking hook provides partial observability for memory usage, but negative compliance (suppression during amnesia) is inherently harder to verify than positive compliance. The eval suite tests amnesia inheritance (P3) using output absence checks, but these are weakened by ambiguous negative assertions.

A compliance testing pyramid emerges: directive < self-report < output-pattern < side-effect < adversarial verification. The current system operates mostly at levels 1-3; pushing more critical propagation checks to levels 4-5 would increase confidence that inherited state actually influences child behavior. The key design insight is that the highest-propagation-guarantee channel (alwaysApply rules) and the highest-salience channel (spawn-time prompt) may not be the same, and both are needed for reliable compliance.
