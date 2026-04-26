/**
 * Test harness for CRUX Memories SDK-based evals.
 *
 * All tests run against an isolated git worktree so the real repo's
 * memories, config, and index are never modified.
 */

import type { Agent } from "@cursor/february/agent";
import { execSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { fileURLToPath } from "node:url";
import { getApiKey, loadConfig } from "./config.js";
import { getRunLogger } from "./logger.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export interface SDKMessage {
  type: string;
  [key: string]: unknown;
}

export interface CollectedRun {
  events: SDKMessage[];
  assistantText: string;
  toolCalls: Array<{ name: string; status: string; args?: unknown }>;
  status: string;
}

export function getRepoRoot(): string {
  return path.resolve(__dirname, "../../..");
}

export function requireApiKey(): string {
  loadConfig();
  return getApiKey();
}

// ---------------------------------------------------------------------------
// Isolated workspace via git worktree
// ---------------------------------------------------------------------------

export interface IsolatedWorkspace {
  /** Absolute path to the worktree root — pass this as Agent local.cwd */
  root: string;
  /** Call in afterAll to remove the worktree and temp branch */
  cleanup: () => void;
}

let worktreeCounter = 0;

/**
 * Create an isolated git worktree for a test suite.
 *
 * The worktree is a full shallow clone of HEAD so the agent sees the same
 * .cursor/ rules, commands, skills, and agents — but writes (memories,
 * index, config) are confined to a temp directory.
 */
export function createIsolatedWorkspace(): IsolatedWorkspace {
  const repoRoot = getRepoRoot();
  const id = `sdk-eval-${Date.now()}-${++worktreeCounter}`;
  const tmpDir = path.join(os.tmpdir(), id);
  const branchName = `tmp/${id}`;

  log(`🔧 Creating isolated worktree at ${tmpDir}`);

  execSync(`git worktree add -b "${branchName}" "${tmpDir}" HEAD`, {
    cwd: repoRoot,
    stdio: "pipe",
  });

  const memTypes = ["core", "redflag", "goal", "learning", "idea", "archived"];
  for (const t of memTypes) {
    fs.mkdirSync(path.join(tmpDir, "memories", t), { recursive: true });
  }
  fs.mkdirSync(path.join(tmpDir, "memories", "agents"), { recursive: true });
  fs.mkdirSync(path.join(tmpDir, ".crux", "reference-tracking"), { recursive: true });

  return {
    root: tmpDir,
    cleanup() {
      log(`🧹 Removing isolated worktree ${tmpDir}`);
      try {
        execSync(`git worktree remove --force "${tmpDir}"`, {
          cwd: repoRoot,
          stdio: "pipe",
        });
      } catch {
        // worktree may already be gone
      }
      try {
        execSync(`git branch -D "${branchName}"`, {
          cwd: repoRoot,
          stdio: "pipe",
        });
      } catch {
        // branch may already be gone
      }
    },
  };
}

// ---------------------------------------------------------------------------
// Debug logging
// ---------------------------------------------------------------------------

const LOG_TRUNCATE_LEN = 250;

function truncate(text: string, len: number): string {
  if (process.env.SDK_EVAL_NO_TRUNCATE === "true") return text;
  return text.length > len ? text.slice(0, len) + "…" : text;
}

function log(msg: string): void {
  const ts = new Date().toISOString().slice(11, 23);
  console.log(`  [${ts}] ${msg}`);
}

// ---------------------------------------------------------------------------
// Exponential backoff retry for rate-limit errors
// ---------------------------------------------------------------------------

const DEFAULT_MAX_RETRIES = 5;
const BASE_DELAY_MS = 2_000;
const MAX_DELAY_MS = 60_000;

function isRateLimitError(err: unknown): boolean {
  if (err instanceof Error) {
    const msg = err.message.toLowerCase();
    return (
      msg.includes("rate limit") ||
      msg.includes("rate_limit") ||
      msg.includes("429") ||
      msg.includes("too many requests") ||
      msg.includes("throttl")
    );
  }
  return false;
}

function backoffDelay(attempt: number): number {
  const jitter = Math.random() * 0.3 + 0.85; // 0.85-1.15x
  return Math.min(BASE_DELAY_MS * Math.pow(2, attempt) * jitter, MAX_DELAY_MS);
}

/**
 * Retry an async operation with exponential backoff on rate-limit errors.
 * Non-rate-limit errors are thrown immediately.
 */
export async function withRetry<T>(
  fn: () => Promise<T>,
  label = "operation",
  maxRetries = DEFAULT_MAX_RETRIES
): Promise<T> {
  for (let attempt = 0; ; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (!isRateLimitError(err) || attempt >= maxRetries) {
        throw err;
      }
      const delay = backoffDelay(attempt);
      log(
        `⚠️ Rate limited on ${label} (attempt ${attempt + 1}/${maxRetries + 1}), ` +
          `retrying in ${Math.round(delay / 1000)}s...`
      );
      await new Promise((r) => setTimeout(r, delay));
    }
  }
}

/**
 * Send a message to an agent with automatic rate-limit retry.
 * Wraps `agent.send()` with exponential backoff.
 */
export async function sendWithRetry(
  agent: Agent,
  message: string
): Promise<Awaited<ReturnType<Agent["send"]>>> {
  _lastPrompt = message;
  return withRetry(() => agent.send(message), `send("${message.slice(0, 60)}")`);
}

// ---------------------------------------------------------------------------
// Run collection
// ---------------------------------------------------------------------------

export interface RunContext {
  prompt: string;
  testName?: string;
  testFile?: string;
}

let _lastPrompt = "";

/**
 * Collect all events from a run stream into a structured result.
 * Logs each event type in real-time for debugging.
 *
 * When `ctx` is provided, writes a structured JSON log to the run's log
 * directory capturing the prompt, all events, thinking, tool calls,
 * assistant response, and timing.
 */
export async function collectRun(
  run: Awaited<ReturnType<Agent["send"]>>,
  promptOrCtx?: string | RunContext
): Promise<CollectedRun> {
  const ctx: RunContext | undefined =
    typeof promptOrCtx === "string"
      ? { prompt: promptOrCtx }
      : promptOrCtx ?? (_lastPrompt ? { prompt: _lastPrompt } : undefined);

  const events: SDKMessage[] = [];
  let assistantText = "";
  const toolCalls: CollectedRun["toolCalls"] = [];
  const thinking: string[] = [];
  let chunkCount = 0;
  let abortedByAskQuestion = false;
  const startTime = Date.now();

  log("⏳ Streaming agent response...");

  for await (const event of run.stream()) {
    events.push(event as SDKMessage);

    if (event.type === "assistant") {
      const msg = event as { message?: { content?: Array<{ type: string; text?: string }> } };
      for (const block of msg.message?.content ?? []) {
        if (block.type === "text" && block.text) {
          assistantText += block.text;
          chunkCount++;
        }
      }
    }

    if (event.type === "thinking") {
      const t = event as { text?: string };
      const raw = t.text ?? "";
      thinking.push(raw);
      log(`💭 thinking: ${truncate(raw.replace(/\n/g, " "), LOG_TRUNCATE_LEN)}`);
    }

    if (event.type === "tool_call") {
      const tc = event as { name?: string; status?: string; args?: unknown };
      const name = tc.name ?? "unknown";
      const status = tc.status ?? "unknown";
      toolCalls.push({ name, status, args: tc.args });
      log(`🔧 tool_call: ${name} [${status}]`);

      if (name === "AskQuestion" && status === "started") {
        log("⚠️ Agent used AskQuestion — aborting collectRun to prevent hang");
        abortedByAskQuestion = true;
        break;
      }
    }

    if (event.type === "status") {
      const s = event as { status?: string };
      log(`📡 status: ${s.status}`);
    }

    if (event.type === "task") {
      const t = event as { status?: string; text?: string };
      log(`📋 task: ${t.status ?? ""} ${(t.text ?? "").slice(0, 60)}`);
    }
  }

  const durationMs = Date.now() - startTime;
  let finalStatus: string;

  if (abortedByAskQuestion) {
    log("⚠️ Skipping run.wait() — agent is blocked on user input");
    finalStatus = "requires_input";
  } else {
    const result = await run.wait();
    finalStatus = result.status;
    log(`✅ Run finished: status=${finalStatus}, chunks=${chunkCount}, tools=${toolCalls.length}`);
    log(`📝 Output preview: ${truncate(assistantText.replace(/\n/g, "\\n"), LOG_TRUNCATE_LEN)}`);
  }

  if (ctx) {
    writeRunLog(ctx, {
      events,
      assistantText,
      toolCalls,
      thinking,
      status: finalStatus,
      durationMs,
    });
  }

  return {
    events,
    assistantText,
    toolCalls,
    status: finalStatus,
  };
}

/**
 * Send a prompt and collect the full run in one call.
 * Captures prompt, response, thinking, tools, and timing into structured logs.
 */
export async function sendAndCollect(
  agent: Agent,
  prompt: string,
  testName?: string
): Promise<CollectedRun> {
  const run = await agent.send(prompt);
  return collectRun(run, { prompt, testName });
}

function writeRunLog(
  ctx: RunContext,
  data: {
    events: SDKMessage[];
    assistantText: string;
    toolCalls: CollectedRun["toolCalls"];
    thinking: string[];
    status: string;
    durationMs: number;
  }
): void {
  const logger = getRunLogger();
  if (!logger) return;

  try {
    logger.logTest({
      testName: ctx.testName ?? inferTestName(),
      testFile: ctx.testFile ?? inferTestFile(),
      prompt: ctx.prompt,
      timestamp: new Date().toISOString(),
      durationMs: data.durationMs,
      status: data.status,
      thinking: data.thinking,
      toolCalls: data.toolCalls,
      assistantText: data.assistantText,
      eventCount: data.events.length,
      events: data.events,
    });
  } catch (err) {
    log(`⚠️ Failed to write test log: ${err}`);
  }
}

function inferTestFile(): string {
  const stack = new Error().stack ?? "";
  const match = stack.match(/tests\/([a-z0-9-]+\.test\.ts)/);
  return match?.[1] ?? "unknown";
}

function inferTestName(): string {
  try {
    const state = (globalThis as Record<string, unknown>).__vitest_worker__ as
      | { current?: { name?: string; fullName?: string } }
      | undefined;
    return state?.current?.fullName ?? state?.current?.name ?? "unknown";
  } catch {
    return "unknown";
  }
}

// ---------------------------------------------------------------------------
// Assertions
// ---------------------------------------------------------------------------

export function hasSubagentCall(
  toolCalls: CollectedRun["toolCalls"],
  subagentType: string
): boolean {
  return toolCalls.some((tc) => {
    if (tc.name !== "Task") return false;
    const args = tc.args as { subagent_type?: string } | undefined;
    return args?.subagent_type === subagentType;
  });
}

export function assertOutputContains(
  text: string,
  patterns: (string | RegExp)[],
  label: string
): void {
  for (const pattern of patterns) {
    const matches =
      typeof pattern === "string"
        ? text.toLowerCase().includes(pattern.toLowerCase())
        : pattern.test(text);
    if (!matches) {
      throw new Error(`${label}: Expected output to contain "${pattern}"\n\nActual output:\n${text.slice(0, 2000)}...`);
    }
  }
}

export function assertOutputExcludes(
  text: string,
  patterns: (string | RegExp)[],
  label: string
): void {
  for (const pattern of patterns) {
    const matches =
      typeof pattern === "string"
        ? text.toLowerCase().includes(pattern.toLowerCase())
        : pattern.test(text);
    if (matches) {
      throw new Error(`${label}: Output should NOT contain "${pattern}"\n\nActual output:\n${text.slice(0, 2000)}...`);
    }
  }
}

// ---------------------------------------------------------------------------
// Memory fixtures (write into an isolated workspace only)
// ---------------------------------------------------------------------------

export interface MemoryFixture {
  slug: string;
  type: "core" | "redflag" | "goal" | "learning" | "idea";
  title: string;
  description: string;
  tags: string[];
  body: string;
  strength?: number;
  source?: string;
}

export function createMemoryFixture(
  fixture: MemoryFixture,
  workspaceRoot: string
): string {
  const today = new Date().toISOString().split("T")[0];
  const strength = fixture.strength ?? 1;
  const source = fixture.source ?? "sdk-test";

  const content = `---
title: "${fixture.title}"
description: "${fixture.description}"
type: "${fixture.type}"
strength: ${strength}
created: ${today}
modified: ${today}
source: "${source}"
tags: [${fixture.tags.join(", ")}]
---

${fixture.body}
`;

  const memDir = path.join(workspaceRoot, "memories", fixture.type);
  fs.mkdirSync(memDir, { recursive: true });

  const filePath = path.join(memDir, `${fixture.slug}.memory.md`);
  fs.writeFileSync(filePath, content, "utf-8");

  return filePath;
}

export function fileExists(filePath: string): boolean {
  return fs.existsSync(filePath);
}

export function readFile(filePath: string): string {
  return fs.readFileSync(filePath, "utf-8");
}

export function readMemoryIndex(workspaceRoot: string): string {
  const indexPath = path.join(workspaceRoot, ".crux", "memory-index.yml");
  if (!fs.existsSync(indexPath)) {
    return "";
  }
  return fs.readFileSync(indexPath, "utf-8");
}

export function rebuildMemoryIndex(workspaceRoot: string): void {
  const scriptPath = path.join(
    workspaceRoot,
    ".cursor/skills/crux-skill-memory-index/scripts/memory-index.py"
  );
  if (fs.existsSync(scriptPath)) {
    execSync(`python3 "${scriptPath}"`, {
      cwd: workspaceRoot,
      stdio: "pipe",
    });
  }
}

export function listMemoryFiles(workspaceRoot: string): string[] {
  const memDir = path.join(workspaceRoot, "memories");
  if (!fs.existsSync(memDir)) {
    return [];
  }

  const files: string[] = [];
  const walk = (dir: string) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.name.endsWith(".memory.md") || entry.name.endsWith(".memory.crux.md")) {
        files.push(fullPath);
      }
    }
  };
  walk(memDir);
  return files;
}

// ---------------------------------------------------------------------------
// Spec fixtures (for Dream / Integration tests)
// ---------------------------------------------------------------------------

export interface CreateSpecFixtureOpts {
  alreadyDreamed?: boolean;
}

/**
 * Create a mock completed spec directory with realistic subtask execution notes.
 *
 * Produces a spec overview, `_execution-state.yml`, and two subtask files with
 * work logs rich enough for LLM-based Dream extraction. Optionally generates a
 * `dream-<slug>-<date>.md` summary when `opts.alreadyDreamed` is true.
 *
 * @returns The absolute path to the created spec directory.
 */
export function createSpecFixture(
  workspaceRoot: string,
  specSlug: string,
  opts?: CreateSpecFixtureOpts
): string {
  const today = new Date().toISOString().split("T")[0];
  const specDir = path.join(workspaceRoot, "specs", specSlug);
  fs.mkdirSync(specDir, { recursive: true });

  const featureName = specSlug.replace(/^\d{8}-/, "");

  // Spec overview
  const specOverview = `# Spec: ${featureName}

## Metadata
- **Created**: ${today}
- **Status**: complete

## Overview
End-to-end implementation of ${featureName} including API client improvements,
connection pool refactoring, and resilience patterns.

## Subtask Manifest
| ID | Title | Agent | Status |
|----|-------|-------|--------|
| 01 | API client retry logic | crux-software-engineer | complete |
| 02 | Connection pool refactoring | crux-software-engineer | complete |
`;
  fs.writeFileSync(
    path.join(specDir, `spec-${featureName}-${today}.md`),
    specOverview,
    "utf-8"
  );

  // Execution state
  const executionState = `status: complete
startedAt: "${today}T10:00:00Z"
completedAt: "${today}T14:30:00Z"
subtasks:
  - id: "01"
    status: complete
    agent: crux-software-engineer
  - id: "02"
    status: complete
    agent: crux-software-engineer
`;
  fs.writeFileSync(
    path.join(specDir, "_execution-state.yml"),
    executionState,
    "utf-8"
  );

  // Subtask 01
  const subtask01 = `# Subtask 01: API Client Retry Logic

## Metadata
- **Subtask ID**: 01
- **Assigned Subagent**: crux-software-engineer
- **Status**: complete

## Objective
Add retry logic with exponential backoff to the API client and implement a
circuit breaker pattern for resilience.

## Execution Notes

### Work Log
- Implemented retry logic with exponential backoff for the API client
- Discovered that the existing error handling silently swallowed connection timeouts
- Added circuit breaker pattern after observing cascading failures in staging
- Introduced structured error types to distinguish transient from permanent failures

### Blockers Encountered
- Silent timeout failures were masking real errors — added explicit timeout logging
- Rate limit headers were inconsistent across API versions — standardised parsing

### Files Modified
- src/api/client.ts (retry logic, circuit breaker)
- src/api/errors.ts (new structured error types)
- tests/api/client.test.ts (new retry tests)
`;
  fs.writeFileSync(
    path.join(specDir, `subtask-01-api-retry-${today}.md`),
    subtask01,
    "utf-8"
  );

  // Subtask 02
  const subtask02 = `# Subtask 02: Connection Pool Refactoring

## Metadata
- **Subtask ID**: 02
- **Assigned Subagent**: crux-software-engineer
- **Status**: complete

## Objective
Refactor the connection pool to use a singleton pattern and add resource
management to prevent leaks under load.

## Execution Notes

### Work Log
- Refactored the connection pool to use a singleton pattern to avoid resource leaks
- Added max-connection limits after profiling showed pool exhaustion under load
- Implemented graceful shutdown hooks to drain connections on process exit
- Added connection health checks with configurable intervals

### Blockers Encountered
- Connection pool exhaustion under load — resolved by adding max-connection limits
- Stale connections were not being recycled — added TTL-based eviction

### Files Modified
- src/api/connection-pool.ts (singleton, max connections, health checks)
- src/api/lifecycle.ts (graceful shutdown hooks)
- tests/api/connection-pool.test.ts (pool exhaustion tests)
`;
  fs.writeFileSync(
    path.join(specDir, `subtask-02-connection-pool-${today}.md`),
    subtask02,
    "utf-8"
  );

  // Optional dream summary
  if (opts?.alreadyDreamed) {
    const dreamSummary = `# Dream Summary: ${featureName}

## Extracted On
${today}

## Candidate Facts
- **Learning**: Exponential backoff is essential for API retry logic
- **Redflag**: Silent error swallowing masks real failures — always log timeouts explicitly
- **Idea**: Circuit breaker pattern prevents cascading failures
- **Learning**: Connection pools need max-connection limits to prevent exhaustion under load
`;
    fs.writeFileSync(
      path.join(specDir, `dream-${specSlug}-${today}.md`),
      dreamSummary,
      "utf-8"
    );
  }

  return specDir;
}

// ---------------------------------------------------------------------------
// Aged memory fixture
// ---------------------------------------------------------------------------

/**
 * Create a memory fixture with `created` and `modified` dates set to
 * `daysAgo` days in the past. Otherwise identical to `createMemoryFixture`.
 *
 * @returns The absolute path to the created memory file.
 */
export function seedAgedMemory(
  fixture: MemoryFixture,
  workspaceRoot: string,
  daysAgo: number
): string {
  const date = new Date();
  date.setDate(date.getDate() - daysAgo);
  const dateStr = date.toISOString().split("T")[0];

  const strength = fixture.strength ?? 1;
  const source = fixture.source ?? "sdk-test";

  const content = `---
title: "${fixture.title}"
description: "${fixture.description}"
type: "${fixture.type}"
strength: ${strength}
created: ${dateStr}
modified: ${dateStr}
source: "${source}"
tags: [${fixture.tags.join(", ")}]
---

${fixture.body}
`;

  const memDir = path.join(workspaceRoot, "memories", fixture.type);
  fs.mkdirSync(memDir, { recursive: true });

  const filePath = path.join(memDir, `${fixture.slug}.memory.md`);
  fs.writeFileSync(filePath, content, "utf-8");

  return filePath;
}

// ---------------------------------------------------------------------------
// Conflicting memory fixtures
// ---------------------------------------------------------------------------

export interface ConflictingMemoriesOpts {
  topic: string;
  memory1: { slug: string; type: MemoryFixture["type"]; title: string; body: string };
  memory2: { slug: string; type: MemoryFixture["type"]; title: string; body: string };
}

/**
 * Create two memory files with contradictory content on the same topic.
 *
 * Both memories receive `strength: 3` and share overlapping tags derived from
 * the topic string so they are likely to surface together during searches.
 *
 * @returns A tuple `[path1, path2]` of the created file paths.
 */
export function createConflictingMemories(
  workspaceRoot: string,
  opts: ConflictingMemoriesOpts
): [string, string] {
  const sharedTags = [opts.topic, "conflict-test"];

  const path1 = createMemoryFixture(
    {
      slug: opts.memory1.slug,
      type: opts.memory1.type,
      title: opts.memory1.title,
      description: `Position A on ${opts.topic}`,
      tags: sharedTags,
      body: opts.memory1.body,
      strength: 3,
      source: "sdk-test",
    },
    workspaceRoot
  );

  const path2 = createMemoryFixture(
    {
      slug: opts.memory2.slug,
      type: opts.memory2.type,
      title: opts.memory2.title,
      description: `Position B on ${opts.topic}`,
      tags: sharedTags,
      body: opts.memory2.body,
      strength: 3,
      source: "sdk-test",
    },
    workspaceRoot
  );

  return [path1, path2];
}

// ---------------------------------------------------------------------------
// Tracker fixtures
// ---------------------------------------------------------------------------

export interface CreateTrackerFixtureOpts {
  referenceCount?: number;
  lastReferenced?: string;
}

/**
 * Create a `.refs.yml` reference-tracker file for a given memory slug.
 *
 * @returns The absolute path to the created tracker file.
 */
export function createTrackerFixture(
  workspaceRoot: string,
  memorySlug: string,
  opts?: CreateTrackerFixtureOpts
): string {
  const refCount = opts?.referenceCount ?? 1;
  const lastRef = opts?.lastReferenced ?? new Date().toISOString().split("T")[0];

  const references = Array.from({ length: refCount }, (_, i) => {
    const refDate = i === 0 ? lastRef : new Date().toISOString().split("T")[0];
    return `  - agent: "test-agent"
    date: "${refDate}"
    context: "SDK eval fixture"`;
  }).join("\n");

  const content = `memory: "${memorySlug}"
reference_count: ${refCount}
last_referenced: "${lastRef}"
references:
${references}
`;

  const trackingDir = path.join(workspaceRoot, ".crux", "reference-tracking");
  fs.mkdirSync(trackingDir, { recursive: true });

  const filePath = path.join(trackingDir, `${memorySlug}.refs.yml`);
  fs.writeFileSync(filePath, content, "utf-8");

  return filePath;
}

/**
 * Create a `.refs.yml` tracker file that has NO matching memory file.
 * Useful for testing orphaned-tracker cleanup during REM sleep.
 *
 * @returns The absolute path to the created tracker file.
 */
export function createOrphanedTracker(
  workspaceRoot: string,
  slug: string
): string {
  return createTrackerFixture(workspaceRoot, slug);
}

// ---------------------------------------------------------------------------
// Assertion helpers
// ---------------------------------------------------------------------------

/**
 * Assert that at least one memory file in `memories/<type>/` matches the given
 * slug pattern. The pattern can be a plain string (substring match on the
 * filename) or a RegExp.
 *
 * @returns The content of the first matching file.
 * @throws If no matching memory file is found.
 */
export function assertMemoryExists(
  workspaceRoot: string,
  type: string,
  slugPattern: string | RegExp
): string {
  const memDir = path.join(workspaceRoot, "memories", type);
  if (!fs.existsSync(memDir)) {
    throw new Error(
      `assertMemoryExists: directory memories/${type}/ does not exist in ${workspaceRoot}`
    );
  }

  const entries = fs.readdirSync(memDir);
  const match = entries.find((name) => {
    if (typeof slugPattern === "string") {
      return name.includes(slugPattern);
    }
    return slugPattern.test(name);
  });

  if (!match) {
    throw new Error(
      `assertMemoryExists: no file in memories/${type}/ matches "${slugPattern}"\n` +
        `  Found: [${entries.join(", ")}]`
    );
  }

  return fs.readFileSync(path.join(memDir, match), "utf-8");
}

/**
 * Assert that NO memory file in `memories/<type>/` matches the given slug
 * pattern.
 *
 * @throws If a matching memory file is found.
 */
export function assertMemoryDeleted(
  workspaceRoot: string,
  type: string,
  slugPattern: string | RegExp
): void {
  const memDir = path.join(workspaceRoot, "memories", type);
  if (!fs.existsSync(memDir)) {
    return; // directory gone ⇒ memory definitely deleted
  }

  const entries = fs.readdirSync(memDir);
  const match = entries.find((name) => {
    if (typeof slugPattern === "string") {
      return name.includes(slugPattern);
    }
    return slugPattern.test(name);
  });

  if (match) {
    throw new Error(
      `assertMemoryDeleted: file "${match}" in memories/${type}/ still exists ` +
        `(matches "${slugPattern}")`
    );
  }
}

/**
 * Assert that the tracker file `<slug>.refs.yml` does NOT exist in
 * `.crux/reference-tracking/`.
 *
 * @throws If the tracker file still exists.
 */
export function assertTrackerDeleted(
  workspaceRoot: string,
  slug: string
): void {
  const trackerPath = path.join(
    workspaceRoot,
    ".crux",
    "reference-tracking",
    `${slug}.refs.yml`
  );
  if (fs.existsSync(trackerPath)) {
    throw new Error(
      `assertTrackerDeleted: tracker "${slug}.refs.yml" still exists at ${trackerPath}`
    );
  }
}

// ---------------------------------------------------------------------------
// Counting / listing helpers
// ---------------------------------------------------------------------------

/**
 * Count `.memory.md` and `.memory.crux.md` files, optionally scoped to a
 * specific type subdirectory.
 */
export function countMemoryFiles(
  workspaceRoot: string,
  type?: string
): number {
  const baseDir = type
    ? path.join(workspaceRoot, "memories", type)
    : path.join(workspaceRoot, "memories");

  if (!fs.existsSync(baseDir)) {
    return 0;
  }

  let count = 0;
  const walk = (dir: string) => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (
        entry.name.endsWith(".memory.md") ||
        entry.name.endsWith(".memory.crux.md")
      ) {
        count++;
      }
    }
  };
  walk(baseDir);
  return count;
}

/**
 * List all `.refs.yml` tracker files in `.crux/reference-tracking/`.
 *
 * @returns Array of absolute paths to tracker files.
 */
export function listTrackerFiles(workspaceRoot: string): string[] {
  const trackingDir = path.join(workspaceRoot, ".crux", "reference-tracking");
  if (!fs.existsSync(trackingDir)) {
    return [];
  }

  return fs
    .readdirSync(trackingDir)
    .filter((name) => name.endsWith(".refs.yml"))
    .map((name) => path.join(trackingDir, name));
}
