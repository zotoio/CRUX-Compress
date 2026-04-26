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
  return withRetry(() => agent.send(message), `send("${message.slice(0, 60)}")`);
}

// ---------------------------------------------------------------------------
// Run collection
// ---------------------------------------------------------------------------

/**
 * Collect all events from a run stream into a structured result.
 * Logs each event type in real-time for debugging.
 */
export async function collectRun(
  run: Awaited<ReturnType<Agent["send"]>>
): Promise<CollectedRun> {
  const events: SDKMessage[] = [];
  let assistantText = "";
  const toolCalls: CollectedRun["toolCalls"] = [];
  let chunkCount = 0;

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
      const raw = (t.text ?? "").replace(/\n/g, " ");
      log(`💭 thinking: ${truncate(raw, LOG_TRUNCATE_LEN)}`);
    }

    if (event.type === "tool_call") {
      const tc = event as { name?: string; status?: string; args?: unknown };
      const name = tc.name ?? "unknown";
      const status = tc.status ?? "unknown";
      toolCalls.push({ name, status, args: tc.args });
      log(`🔧 tool_call: ${name} [${status}]`);
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

  const result = await run.wait();

  log(`✅ Run finished: status=${result.status}, chunks=${chunkCount}, tools=${toolCalls.length}`);
  log(`📝 Output preview: ${truncate(assistantText.replace(/\n/g, "\\n"), LOG_TRUNCATE_LEN)}`);

  return {
    events,
    assistantText,
    toolCalls,
    status: result.status,
  };
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
