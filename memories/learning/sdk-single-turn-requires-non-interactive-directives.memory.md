---
id: "fcd2f69"
title: "SDK single-turn agent.send() requires non-interactive directive prompts for inherently interactive commands"
description: "The TypeScript SDK's agent.send() is single-turn — there is no follow-up user input. Commands like /crux-dream, /crux-forget, and /crux-dream --rem have inherently interactive flows (accept/reject candidates, confirm deletions, conflict resolution). To test them via the SDK, embed acceptance/rejection intent directly in the prompt as a directive (e.g. '/crux-dream <spec> — accept all candidate facts and write the dream summary'). Focus assertions on ground-truth side effects (memory files created, dream summaries written, files deleted) rather than the conversational accept/reject flow. Conflicts must still surface in output; the directive should explicitly say 'do not auto-resolve' when conflict detection is being verified."
type: "learning"
strength: 1
created: 2026-04-27
modified: 2026-04-27
source: "20260426-sdk-eval-expansion"
tags: [sdk, evals, single-turn, prompt-engineering, non-interactive, ground-truth-assertions, dream, forget, rem]
---

# SDK single-turn requires non-interactive directive prompts

## The constraint

The TypeScript Cursor SDK exposes a single-turn primitive: `agent.send(message)` returns a stream and resolves once the agent's response completes. There is no built-in way to send a follow-up turn within the same logical "conversation step" before the agent finishes, and there is no user-input channel from inside a test.

Several CRUX commands are designed around interactive multi-turn flows:

- **`/crux-dream <spec>`** — present candidate facts → wait for accept/reject → create memory files → write dream summary → offer archival
- **`/crux-dream --rem`** — present recommendations → wait for confirmation → apply changes
- **`/crux-forget <id>`** — present matched memories → require explicit confirmation → delete
- **REM conflict resolution** — present conflicting memories → wait for keep/replace/merge selection

Asking the agent to perform any of these via a literal command string (e.g. `/crux-dream 20260420-test-feature`) under the SDK leaves the agent in one of three states:
1. Auto-accept and complete the flow (depends on agent interpretation)
2. Present candidates and stop, waiting for input that will never arrive
3. Treat it as implicit acceptance — varies between runs

State 2 is the failure mode that makes evals flaky.

## The pattern

**Embed the entire flow's intent in the initial prompt as a directive.** The agent reads the prompt as a complete instruction set and performs every step without pausing for input.

Examples used across the SDK eval suite:

```text
/crux-dream 20260420-test-feature — accept all candidate facts and write the dream summary
/crux-dream 20260420-test-feature — present any conflicts for review but do not auto-resolve
/crux-dream --rem — analyze and present recommendations without waiting for confirmation
/crux-dream --rem --yolo — present any conflicts for review but do not auto-resolve
/crux-forget sdk-test-forget-perf
```

The em-dash and natural-language clause are deliberate — they signal "complete the flow with this disposition" rather than "follow this command literally and wait."

## Assertion strategy

Because the directive collapses the multi-turn flow into a single agent turn, tests cannot verify the conversational flow itself (accept/reject UI, confirmation prompts). Replace conversational-flow assertions with **ground-truth side-effect assertions**:

| Concern | Replace with |
|---------|--------------|
| "Agent presented candidates and waited for accept" | New memory files exist on disk after the run |
| "Agent confirmed before deleting" | Output contains "delete"/"remove" + target file is absent on disk |
| "Agent asked which conflict resolution to apply" | Both conflicting memory files still exist on disk after a `--yolo` run |
| "Agent offered archival" | Dream summary file exists in the spec directory |

The agent's output text is still checked for keyword presence (resilient OR-pattern matching), but the source of truth for "did the work happen" is the file system.

## When directive prompts must NOT auto-resolve

Conflict detection is the one case where the directive explicitly disables completion. Conflicts are user decisions by definition; even in `--yolo` mode the manager must not pick a resolution. The directive must say so:

```text
/crux-dream --rem --yolo — present any conflicts for review but do not auto-resolve
```

Tests then assert both that conflicts appear in the output AND that the disputed memory files remain unmodified on disk.

## Why this is not a workaround

The directive prompt is not a trick — it is the correct semantics for non-interactive automation. Interactive UX exists for human users with judgement; a test harness has pre-decided the disposition before sending the prompt. Encoding that disposition in the prompt is more honest than mocking out an `AskQuestion` that the SDK has no way to answer.

## Source

Decision 11 of `spec-sdk-eval-expansion-20260426.md`, codified in subtasks 04 (Dream), 05 (REM), 06 (Forget), 07 (Meditate), and 08 (Integration). Originated as finding F8 in the spec assessment ("Dream B2 'full flow' assumes the agent completes all steps in a single turn") and resolved by adding the SDK Single-Turn Non-Interactive Strategy section to each affected subtask.
