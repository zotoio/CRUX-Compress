---
id: "62c0212"
title: "@cursor/february SDK type definitions have pre-existing TS7053/TS2339 errors that must not be flagged as new regressions"
description: "The @cursor/february v1.0.5 SDK type definitions have two pre-existing TypeScript errors that affect every test file: TS7053 (Symbol.asyncDispose not indexable on Agent type — needs ES2024+ lib or polyfill) and TS2339 (Property 'send' does not exist on type 'Agent' — exists at runtime but not in the .d.ts). Reviewers, judges, and adversarial verifiers must count these as baseline noise (8 TS7053 + 33 TS2339 at last measurement) and distinguish them from genuinely new errors introduced by code under review. Document expected counts in execution notes so future PRs that bump those counts can be triaged confidently. Do NOT attempt to 'fix' these errors in test code — fixes belong in the SDK package or a tsconfig upgrade."
type: "redflag"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "20260426-sdk-eval-expansion"
tags: [sdk, typescript, type-definitions, pre-existing-errors, false-positive, review, evals, cursor-february]
---

# @cursor/february SDK type definitions have pre-existing errors

## The trap

Running `pnpm exec tsc --noEmit` in `evals/sdk/` produces ~41 TypeScript errors. None of them are caused by the test code under review. They are **pre-existing gaps in the `@cursor/february` v1.0.5 SDK type definitions** that surface in every test file because every test file imports from the SDK.

A first-time reviewer (human or adversarial agent) will reasonably interpret the error count as a regression and demand fixes. They will be wrong.

## The two error families

### TS7053 — `Symbol.asyncDispose` not indexable on `Agent`

Pattern: `agent[Symbol.asyncDispose]()` in test cleanup

```
TS7053: Element implicitly has an 'any' type because expression of type 'unique symbol' can't be used to index type 'Agent'.
```

Root cause: the SDK was declared before TypeScript libraries shipped `Symbol.asyncDispose`. Fixing it requires bumping `lib` to `ES2024+` or shipping a polyfill type. Approximate baseline count: **8 occurrences** (one per test file using `await using` or explicit `Symbol.asyncDispose` cleanup).

### TS2339 — `Property 'send' does not exist on type 'Agent'`

Pattern: `agent.send(prompt)` everywhere

```
TS2339: Property 'send' does not exist on type 'Agent'.
```

Root cause: the SDK exposes `send()` at runtime but the `.d.ts` type definitions don't declare it publicly. The harness compensates by typing return values as `Awaited<ReturnType<Agent["send"]>>`, but the call sites still error. Approximate baseline count: **33 occurrences** (every direct `agent.send()` call across the harness and existing test files).

## Why this is a redflag

The error count is large enough (41 total) that a casual `tsc` run looks alarming. Reviewers without context will:

1. Count errors and reject the PR for "introducing TypeScript regressions"
2. Demand fixes that belong in the SDK package, not in test code
3. Spend cycles trying to retype `Agent` locally and fail because the types are imported, not declared

All three failure modes have happened during adversarial verification of the SDK eval expansion spec.

## The detection heuristic

When a TypeScript error count appears to spike in `evals/sdk/`:

1. Categorise the errors by code: are they all `TS7053` and `TS2339`?
2. Check the affected files: do they all import from `@cursor/february`?
3. Compare the count to the documented baseline (8 + 33 = 41 at last measurement)
4. Only investigate as a real regression if the count exceeds the baseline OR the error codes are different

Subtask 09 of the SDK eval expansion spec explicitly recorded the baseline so future PRs can be triaged confidently. Update the recorded count whenever the SDK is upgraded.

## Mitigation, not fix

Workarounds that keep the test code safe without "fixing" the SDK:

- Use `try { agent[Symbol.asyncDispose]?.(); } catch {}` in cleanup, accepting the local TS error
- Type-only imports: `import type { Agent } from "@cursor/february/agent"` where possible
- Accept that `agent.send()` will always type-error; the harness wraps it via `sendWithRetry()` which has the cast in one place

A real fix requires upstream changes to `@cursor/february` (publishing complete `.d.ts` and bumping `lib`) or an `lib` upgrade in the eval package's `tsconfig.json`. Neither belongs in a feature spec's subtask deliverables.

## Implication for spec authors and reviewers

Spec authors should NOT add deliverables to "fix TypeScript errors" in the eval suite. Reviewers and adversarial verifiers should NOT count these errors as new regressions.

When the SDK is upgraded:

1. Re-run `tsc --noEmit` and record the new baseline counts
2. Update this memory's description with the new numbers
3. Update execution notes in any in-flight specs

## Source

Subtasks 04, 06, 07, 08, and especially 09 of `spec-sdk-eval-expansion-20260426.md`. Subtask 09's adversarial verification explicitly corrected the count from "42 (34+8)" to "41 (33+8)" — evidence that even careful reviewers miscount these errors. The baseline is recorded in `subtask-09-sdk-eval-validation-profiling-20260426.md` Execution Notes.
