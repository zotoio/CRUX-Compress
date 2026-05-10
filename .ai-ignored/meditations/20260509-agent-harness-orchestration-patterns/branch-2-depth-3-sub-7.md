---
branch: 2
depth: 3
subfocus_index: 7
subfocus: "Taxonomy of Failure Categories That Adversarial Verification Excels At"
parent_subfocus: "Adversarial Verification as a Post-Hoc Failure Detection Mechanism"
timestamp: 2026-05-09T19:36:00+10:00
---

## Subfocus Rationale

The 25% empirical hit rate for adversarial verification is an aggregate — it says nothing about *which* failures are caught. A taxonomy that maps failure categories to their detection mechanisms reveals where adversarial verification is structurally superior to self-verification, and — crucially — where it contributes little. This enables smarter allocation of verification effort.

## Discoveries

### Taxonomy of Failures Where Adversarial Verification Excels

**Category 1: Silent Persistence Failures**
- *Evidence*: Memory `49303e0` — subtask 06's canvas file was reported as created (with full contents and path in the work log) but never persisted to disk. The Write tool failed silently or emitted to the chat UI only.
- *Why adversarial beats self-verification*: The executing agent's narrative IS the failure. The agent "sees" the file because it generated the content in its context window. Self-verification would re-read its own context and confirm success. Only an independent agent with no prior context, running `ls` and `git status` on the filesystem, can detect the gap between claimed and actual state. The agent's narrative is a hypothesis; filesystem state is ground truth.
- *Structural advantage*: Fresh context = no confirmation bias. The adversarial verifier doesn't know what "should" exist — it checks what DOES exist.

**Category 2: Documentation-Reality Drift**
- *Evidence*: Memory `dbfd3ed` — web documentation listed hook files as `.sh` when actual files were `.py`. Memory `6c16dc6` — 25% of subtasks across two plans had documentation gaps caught by adversarial review.
- *Why adversarial beats self-verification*: Implementing agents update documentation based on their mental model of the codebase, which may be stale. They write ".sh" because hooks WERE shell scripts, not because they checked. An adversarial verifier with no historical context reads the documentation and compares paths against `ls` output — they have no reason to believe `.sh` is correct.
- *Structural advantage*: No knowledge of historical file names means no muscle-memory errors. The verifier treats every path claim as needing proof.

**Category 3: Cross-File / Cross-Layer Consistency Violations**
- *Evidence*: Memory `d944d7c` — spec index text drifted from subtask details, causing the first judge to produce a false-positive CRITICAL finding. Memory `00a6d09` — command-family expansion missed updating sibling Related sections and override exception lists across multiple files.
- *Why adversarial beats self-verification*: The implementing agent works on one file at a time and "forgets" what it wrote in sibling files earlier in the session. Cross-file consistency requires reading N files simultaneously and comparing claims — exactly what a fresh agent with no working-memory fatigue does. The verifier reads spec index AND subtask files and catches contradictions.
- *Structural advantage*: Independent agent reads ALL layers rather than relying on the implementing agent's recall of what it wrote 15 subtasks ago.

**Category 4: Default/Spec Misalignment**
- *Evidence*: Memory `96a7410` — crux-utils.py used 20% compression target while CRUX.md spec said 25%. Drift went unnoticed across multiple sessions until a dedicated plugin refactor.
- *Why adversarial beats self-verification*: The implementing agent copies the default from an existing file or its own memory. It never re-reads the specification to cross-check. An adversarial verifier compares the tool's hardcoded default against the spec document — a specific cross-reference the implementer has no incentive to perform.
- *Structural advantage*: The verifier approaches both files without knowing which is "right" and surfaces the discrepancy, whereas the implementer assumes their value is correct.

**Category 5: Distribution Completeness Gaps**
- *Evidence*: Memory `aba710d` — `crux-amnesia.md` was fully integrated (config, installer, documentation, evals) but absent from `scripts/create-crux-zip.py DIST_FILES`. The gap survived multiple sessions because the developer workflow (repo clone) never exercises the distribution path.
- *Why adversarial beats self-verification*: This is an "integration boundary" failure — the file works in the developer's context but not in the user's. The implementing agent tests in its own context (repo-cloned) and succeeds. An adversarial verifier can systematically enumerate "all user-facing files" and check each against the distribution manifest — a sweep the implementer never performs because all their tests pass.
- *Structural advantage*: The verifier checks delivery paths the implementer never exercises.

### Failures Where Adversarial Verification Has KNOWN WEAKNESSES

**Weakness 1: False-Positive Inflation from Missing Context**
- *Evidence*: Memory `62c0212` — 41 pre-existing TypeScript errors in the SDK type definitions were flagged as new regressions by adversarial verifiers. Memory `826c280` — a judge demanded regeneration of `AGENTS.crux.md`, which is a transient install artifact that doesn't persist in the repo.
- *The trap*: Adversarial verifiers lack historical context about known baseline issues, transient artifacts, and deliberate exceptions. Without a "known issues" manifest, they produce confident-sounding CRITICAL findings that are categorically wrong. The cost of triaging false positives partially offsets the 25% true-positive rate.

**Weakness 2: Semantic Correctness**
- Adversarial verification checks structural properties (files exist, paths match, lists are complete) but cannot verify semantic correctness of logic. Whether a compression algorithm produces correct output, whether a force simulation converges, whether a memory consolidation actually groups related memories — these require domain-specific test execution, not independent review.

**Weakness 3: Performance Regressions**
- Structural verification cannot detect that an operation took 10x longer after a refactor. Performance requires runtime measurement under controlled conditions, not document inspection.

**Weakness 4: Security Vulnerabilities**
- Adversarial verification as practiced here checks consistency (do docs match code?) not safety (can this be exploited?). Security review requires threat modeling and attack surface analysis — a fundamentally different skill from cross-reference checking.

**Weakness 5: Interaction Correctness**
- Multi-step workflows (dream → REM → recall) can be individually correct at each step but fail when composed. Adversarial verification checks each subtask independently, not the end-to-end flow. Integration testing fills this gap.

## Connections

**The structural pattern**: All five "excels" categories share a common trait — the failure is a **discrepancy between two sources of truth** (agent narrative vs. filesystem, documentation vs. disk, spec index vs. subtask, tool default vs. spec, integration list vs. distribution manifest). Adversarial verification is fundamentally a cross-reference checker: it holds two documents side-by-side and checks for divergence. It excels wherever truth is distributed across multiple files and a single agent works on them sequentially.

**The false-positive pattern**: All adversarial weaknesses share an inverse trait — the verifier lacks context about **deliberate exceptions** to general rules. Pre-existing SDK errors, transient install artifacts, and spec-index-vs-subtask authority rules are all exceptions that require institutional knowledge. This suggests adversarial verification needs a "known exceptions manifest" to suppress false positives — a pre-loaded set of "do not flag" patterns analogous to a `.eslintignore`.

**The asymmetry**: Self-verification fails at cross-file consistency because the agent's context window is a single thread. Adversarial verification fails at temporal knowledge because the verifier's fresh context is also its limitation. The ideal harness would combine adversarial verification (no confirmation bias) with a baseline knowledge document (no false positives from ignorance).

**Connection to distribution completeness (memory `aba710d`)**: This failure is particularly insidious because it survives arbitrarily many "works on my machine" tests. The developer path and the user path diverge at the distribution boundary. Adversarial verification catches this only if it's explicitly instructed to check distribution manifests — suggesting the verifier needs a typed checklist, not just general "verify correctness."

## Summary

Adversarial verification excels at five failure categories, all sharing the structural property of **cross-reference divergence across distributed sources of truth**: (1) silent persistence failures (agent narrative vs. filesystem), (2) documentation-reality drift (docs vs. disk), (3) cross-file consistency violations (spec layers vs. each other), (4) default/spec misalignment (tool code vs. specification), and (5) distribution completeness gaps (integration vs. packaging). In all cases, the verifier's fresh context eliminates the confirmation bias that makes self-verification structurally blind. However, adversarial verification produces significant false positives when it lacks knowledge of deliberate exceptions (pre-existing errors, transient artifacts), and it cannot detect semantic correctness, performance regressions, security vulnerabilities, or integration-flow failures — all of which require runtime execution rather than cross-reference inspection. The optimal design pattern is adversarial verification augmented with a "known exceptions manifest" and a typed verification checklist, not open-ended review.
