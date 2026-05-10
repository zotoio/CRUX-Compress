---
branch: 2
depth: 3
subfocus_index: 5
subfocus: "Phantom Completions and Silent Failures"
parent_subfocus: "Timeout Detection, Hang Recovery, and Graceful Degradation"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

Phantom completions are the hardest failure mode in agent orchestration because they defeat every time-based defence. A hanging agent eventually trips a timeout; a phantom completer exits cleanly, reports success, and leaves no artifact on disk. The only defence is ground-truth verification that doesn't trust the agent's self-report — a fundamentally different class of check that warrants dedicated analysis.

## Discoveries

### 1. Taxonomy of Phantom Completions

Memory `49303e0` documents the canonical case, but the codebase and memory corpus reveal at least four distinct phantom subtypes:

| Subtype | Mechanism | Detectable by timeout? | Example |
|---------|-----------|----------------------|---------|
| **Silent Write failure** | Write tool returns success but no-ops (permission, path resolution, transient I/O error) | No — agent continues normally | Subtask 06 canvas file (memory 49303e0) |
| **Narrative hallucination** | Agent narrates "I created the file at X" without ever invoking the Write tool — self-deception in the work log | No — no tool call at all | Agent describes file contents in assistantText but toolCalls array has no Write entry |
| **UI-only emission** | Content rendered in chat UI (canvas preview, inline code block) rather than persisted to disk | No — appears successful in the chat | Canvas artifacts shown in Cursor's preview pane but never written to filesystem |
| **Partial Write** | File created but content is truncated, empty, or a placeholder (e.g., "TODO: implement") — passes existence checks but fails content checks | No — file exists on disk | Agent creates the file but context window truncation drops the body |

Each subtype requires a different verification strategy. A naive `fileExists()` catches subtypes 1-3 but misses subtype 4. Content validation catches all four.

### 2. The Existing Ground-Truth Layer

The harness already implements a layered verification architecture that, when fully applied, catches all four phantom subtypes:

**Layer 1 — Filesystem existence** (`fileExists`, `assertMemoryExists`, `listMemoryFiles`): These functions in `harness.ts` use Node.js `fs.existsSync` and `fs.readdirSync` directly against the isolated worktree. They never trust agent output — they read the actual disk. `assertMemoryExists` goes further: it returns the file *content*, enabling Layer 2.

**Layer 2 — Content validation** (`assertOutputContains`, `readFile`, frontmatter inspection): Tests like O1's "sets source to adhoc" read the created file and check `expect(content).toContain('source: "adhoc"')`. This catches partial writes and wrong-content phantoms. The dream test's `countMemoryFiles` before/after pattern catches the case where the agent *claims* creation but the count doesn't change.

**Layer 3 — Tool-call stream inspection** (`toolCalls` array from `collectRun`): The harness captures every tool call with name and status. Test O1 checks `result.toolCalls.some(tc => tc.name === "edit" || tc.name === "write")` — this is a streaming-level signal that the agent at least *attempted* a write. Absence of a Write tool call in the stream while the agent claims file creation is a strong phantom signal.

**Layer 4 — Adversarial re-verification** (separate agent, independent checks): Memory `6c16dc6` documents the 25% hit rate. The spec judge (`zoto-spec-judge`) runs `ls`, Read, and `git status` against every claimed artifact. This is the only layer that caught the original phantom completion in subtask 06.

### 3. The Tool-Call Stream as Real-Time Phantom Detector

The `collectRun` function already captures `{ name, status, args }` for every tool call event. This creates an opportunity for *streaming phantom detection* that doesn't require waiting for the agent to finish:

- **Write tool_call with status "completed" → no subsequent file on disk**: Detectable by comparing the Write tool call's target path argument against a post-run `fileExists` check. The harness could assert: "for every Write tool call with status 'completed', the target file must exist on disk."
- **No Write tool_call at all, but assistantText claims file creation**: A regex scan of `assistantText` for phrases like "created", "wrote", "generated" combined with path-like strings, cross-referenced against `toolCalls` for Write entries. If the text claims creation but no Write tool call exists, flag as narrative hallucination.
- **AskQuestion abort masking a Write**: The harness already detects AskQuestion-triggered aborts (`abortedByAskQuestion = true`). If a Write tool call appeared *before* the abort but the run was terminated before the filesystem committed, the Write may be phantom. The `requires_input` status already signals this risk.

### 4. Structural Output Schemas for Non-Vacuous Responses

Memory `d944d7c` (spec index drift) reveals a deeper problem: even when a harness *does* check output, the check can be too lenient. The test `expect(result.assistantText.toLowerCase()).toMatch(/verif|check|confirm|status|complete|execution|review/i)` matches so many words that almost any agent response passes. A phantom completer that says "I've reviewed the requirements and completed the task" passes all keyword checks while doing nothing.

**Structural schemas** address this by requiring the agent's output to contain specific structured artifacts, not just keywords:

- **Manifest of claimed artifacts**: The agent must list every file it claims to have created/modified, with paths and content summaries. The harness cross-checks each entry against disk.
- **Tool-call coverage assertion**: For every claimed file, there must exist a corresponding Write tool call in the stream. No Write tool call = no claim allowed.
- **Content-hash validation**: The agent produces a hash of the content it intended to write; the harness computes the hash of what's actually on disk. Mismatch = partial write or corruption.

### 5. The Adversarial Verification Cost-Benefit

Memory `6c16dc6` quantifies the ROI: 25% hit rate across 24 subtasks, meaning 1 in 4 subtasks had an issue only the adversarial verifier caught. But adversarial verification has a steep cost:

- **API cost**: Running a separate agent per subtask roughly doubles the LLM spend. Memory `6415c52` notes the cascade effect — if the shared verification run fails, all N checks fail together.
- **Wall-clock time**: Each adversarial check is another 60-90s agent call.
- **False positives from spec drift**: Memory `d944d7c` shows that the judge itself can produce false findings when the spec index contradicts subtask details.

The optimal strategy is a **tiered verification pyramid**:

1. **Always** (zero marginal cost): Tool-call stream inspection — assert Write tool calls exist for claimed artifacts
2. **Always** (cheap): Filesystem assertions — `fileExists` + `readFile` + content pattern matching
3. **On suspicious signals** (targeted): Content-hash validation — when Layer 1-2 pass but the output seems thin
4. **Periodically or on critical paths** (expensive): Full adversarial re-verification by a separate agent

### 6. Cross-Reference: The "Multiple Layers of Truth" Problem

Memory `d944d7c` (spec index drift) and memory `49303e0` (phantom completion) are manifestations of the same underlying failure: **the system has multiple representations of truth that can diverge silently**. In spec drift, the index and subtask files diverge. In phantom completions, the agent's narrative and the filesystem diverge. In both cases, the fix is the same: designate one representation as ground truth and verify all others against it.

For phantom completions: **the filesystem is ground truth**. The agent's assistantText, tool call log, work log, and status report are all hypotheses until confirmed against disk.

For spec drift: **the subtask is ground truth**. The spec index is a hypothesis until confirmed against subtask content.

This "ground truth designation" pattern is a generalizable principle: in any system with multiple state representations, explicitly designate which one is authoritative and build automated verification that checks all others against it.

## Connections

1. **Memory 49303e0 ↔ harness `assertMemoryExists`**: The verification protocol described in the memory (run `ls`, Read the file, check `git status`) is exactly what the harness assertion helpers implement programmatically. The harness has *already generalized* the ad-hoc verification protocol into reusable functions — but only for memory files. The pattern should extend to any agent-claimed artifact.

2. **Memory 6c16dc6 (adversarial 25% hit rate) ↔ Memory 6415c52 (shared-run cascade)**: These are in tension. Adversarial verification is high-value (25% find rate) but sharing the verification agent run across multiple checks creates cascade risk. The resolution: use cheap structural checks (Layers 1-2) for breadth and reserve expensive adversarial verification (Layer 4) for depth on critical paths.

3. **Tool-call stream ↔ filesystem assertions**: The `collectRun` function already captures the data needed for streaming phantom detection, but no test currently cross-references tool calls against filesystem state. The gap: a "Write tool call with status completed" is treated as evidence of success, but the harness doesn't verify that the Write actually materialized. This is the exact gap that enables phantom completions.

4. **The `assertOutputContains` lenience problem ↔ structural schemas**: The current regex-based output assertions accept almost any response that mentions the right keywords. Memory `3bf625d` (meditate synthesis must not hallucinate connections) flags the same pattern in a different context — agents can produce plausible-sounding text that doesn't reflect reality. Structural output schemas force the agent to make falsifiable claims (specific file paths, specific content) rather than vague assertions.

5. **Multiple-layers-of-truth ↔ tooling defaults drift (memory 96a7410)**: The pattern where the crux-utils.py default diverged from CRUX.md's default is another instance of the same multiple-representations-of-truth problem. Ground truth designation + automated verification is the universal remedy.

## Summary

Phantom completions are the most insidious agent failure mode because they bypass all time-based defences and exploit the gap between an agent's self-report and filesystem reality. The CRUX harness already has the primitives for a robust defence — `fileExists`, `assertMemoryExists`, `readFile`, `collectRun`'s tool-call capture, and adversarial judge agents — but these layers are not yet wired into a systematic "completion verifier" that cross-references tool-call streams against disk state.

The key insight is a **four-layer verification pyramid**: (1) tool-call stream inspection (did a Write even occur?), (2) filesystem existence and content checks (did the file materialize with correct content?), (3) structural output schemas (does the agent's response make falsifiable claims we can check?), and (4) adversarial re-verification by a separate agent (does an independent observer confirm the artifacts?). Each layer catches phantom subtypes that lower layers miss, and the cost scales with the layer — making it practical to apply layers 1-2 universally and layers 3-4 selectively.

The deeper principle connecting phantom completions to spec drift (memory d944d7c) and tooling defaults drift (memory 96a7410) is: **when a system has multiple representations of the same truth, silently divergent representations are inevitable; the remedy is to designate ground truth and automate verification of all other representations against it**. For agent output, the filesystem is always ground truth. The agent's narrative is always a hypothesis.
