# CRUX Memories SDK Evals

Automated end-to-end tests for the CRUX Memories system using the [Cursor TypeScript SDK](https://cursor.com/docs/api/sdk/typescript).

## Overview

These tests complement the existing Python unit tests in `evals/` by running actual agent interactions against the CRUX Memories commands (`/crux-recall`, `/crux-remember`, `/crux-amnesia`, etc.).

## Prerequisites

1. **Node.js 20+** installed
2. **Cursor API Key** from [cursor.com/dashboard/cloud-agents](https://cursor.com/dashboard/cloud-agents)
3. The CRUX-Compress repository with memories system configured

## Setup

```bash
cd evals/sdk
pnpm install
```

The platform-specific packages (`@cursor/february-{platform}-{arch}`) include bundled ripgrep for local file search.

Set your API key:

```bash
export CURSOR_API_KEY="your-key-here"
```

## Running Tests

```bash
# Run all SDK tests (expensive tests skipped by default)
pnpm test

# Run specific test suites
pnpm test:recall      # J-series: Recall tests
pnpm test:amnesia     # P-series: Amnesia tests  
pnpm test:remember    # O-series: Remember tests
pnpm test:dream       # B-series: Dream tests
pnpm test:rem         # C-series: REM Sleep tests
pnpm test:forget      # R-series: Forget tests
pnpm test:meditate    # Q-series: Meditate tests (expensive)
pnpm test:integration # N-series: Integration test (expensive)

# Run ALL tests including expensive ones
SDK_EVAL_SKIP_EXPENSIVE=false pnpm test

# Watch mode for development
pnpm test:watch
```

## Test Structure

```
evals/sdk/
├── helpers/
│   └── harness.ts      # Test utilities and fixtures
├── tests/
│   ├── j-recall.test.ts    # J1-J4: Recall command tests
│   ├── p-amnesia.test.ts   # P1-P3: Amnesia toggle tests
│   └── o-remember.test.ts  # O1-O2: Remember command tests
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

## Test Categories

| Suite | Scenarios | Coverage |
|-------|-----------|----------|
| J: Recall | J1-J4 | No-args contextual, query search, spec filtering, direct file display |
| P: Amnesia | P1-P3 | Toggle on/off, explicit commands during amnesia, subagent inheritance |
| O: Remember | O1-O2 | Interactive creation, one-shot with type flag, index rebuilding |

## How It Works

1. **Agent Creation**: Each test creates a local Cursor agent pointed at this repository
2. **Command Dispatch**: Tests send commands like `/crux-recall` via `agent.send()`
3. **Response Collection**: The `collectRun()` helper streams events and extracts:
   - Assistant text output
   - Tool calls (including subagent spawning)
   - Run status
4. **Assertions**: Tests verify expected patterns in output and file system state

## Adding New Tests

1. Create a new test file in `tests/` following the naming convention: `<letter>-<name>.test.ts`
2. Import helpers from `../helpers/harness.js`
3. Use `collectRun()` to capture agent output
4. Use `assertOutputContains()` / `assertOutputExcludes()` for pattern matching
5. Use `hasSubagentCall()` to verify subagent spawning

Example:

```typescript
import { Agent } from "@cursor/february/agent";
import { collectRun, assertOutputContains } from "../helpers/harness.js";

describe("My Test", () => {
  it("does something", async () => {
    const agent = Agent.create({
      apiKey: process.env.CURSOR_API_KEY!,
      model: { id: "composer-2" },
      local: { cwd: getWorkspaceRoot() },
    });

    const run = await agent.send("/my-command");
    const result = await collectRun(run);

    assertOutputContains(result.assistantText, ["expected", "patterns"], "Test label");

    await agent[Symbol.asyncDispose]();
  });
});
```

## Fixture Management

Test fixtures (temporary memories) are:
- Created in `beforeAll` with `createMemoryFixture()`
- Tagged with `source: "sdk-test"` for identification
- Cleaned up in `afterAll` with `cleanupSdkTestMemories()`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CURSOR_API_KEY` | (required) | API key from [cursor.com/dashboard/cloud-agents](https://cursor.com/dashboard/cloud-agents) |
| `RIPGREP_PATH` | — | Path to ripgrep binary for local file search |
| `SDK_EVAL_SKIP_EXPENSIVE` | `true` | Skip expensive tests (Meditate, Integration). Set to `"false"` to run them. |
| `SDK_EVAL_MAX_DURATION_MS` | `3600000` | Global max test execution duration in ms (60 minutes). Process terminates when exceeded. |
| `SDK_EVAL_NO_TRUNCATE` | — | Set to `"true"` to disable debug log truncation |

## Timeout Configuration

Tests have extended timeouts (240s default, up to 600s for integration) to accommodate:
- Agent initialization
- LLM response generation
- Subagent spawning and completion

A **global max duration** (default: 60 minutes) terminates the entire process if tests run too long, preventing unbounded API spend. Adjust via `SDK_EVAL_MAX_DURATION_MS`.

## Rate Limit Handling

The harness includes automatic **exponential backoff retry** for API rate-limit errors:
- Base delay: 2 seconds, doubling each retry
- Max delay: 60 seconds
- Max retries: 5
- Jitter applied to prevent thundering herd

Use `sendWithRetry(agent, message)` instead of `agent.send(message)` for automatic retry, or `withRetry(fn, label)` to wrap any async operation.

## Relationship to Python Tests

| Python Tests (`evals/*.py`) | SDK Tests (`evals/sdk/tests/*.ts`) |
|-----------------------------|------------------------------------|
| Unit tests for file structure | End-to-end agent interaction tests |
| Fast, no API calls | Requires API key, slower |
| Validates config/command definitions | Validates actual agent behavior |
| Run with `pytest` | Run with `yarn test` |

Both test suites should pass for full coverage of the CRUX Memories system.
