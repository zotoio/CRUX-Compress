/**
 * Structured logging for SDK eval runs.
 *
 * Captures input prompts, agent responses, thinking, tool calls, and timing
 * into per-test JSON files under `evals/sdk/logs/<run-timestamp>/`.
 *
 * Usage:
 *   - The vitest.setup.ts initialises a shared run logger via `initRunLogger()`
 *   - `collectRun(run, { prompt })` writes a log entry automatically
 *   - `getRunLogger().writeSummary()` produces an aggregated summary
 */

import * as fs from "node:fs";
import * as path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export interface TestLogEntry {
  testName: string;
  testFile: string;
  prompt: string;
  timestamp: string;
  durationMs: number;
  status: string;
  thinking: string[];
  toolCalls: Array<{
    name: string;
    status: string;
    args?: unknown;
  }>;
  assistantText: string;
  eventCount: number;
  events: unknown[];
}

export interface RunSummary {
  runId: string;
  startedAt: string;
  completedAt: string;
  durationMs: number;
  testCount: number;
  passed: number;
  failed: number;
  timedOut: number;
  tests: Array<{
    testName: string;
    testFile: string;
    status: string;
    durationMs: number;
    toolCallCount: number;
    thinkingChunks: number;
    prompt: string;
    assistantText: string;
  }>;
}

class TestRunLogger {
  readonly runDir: string;
  readonly runId: string;
  private startedAt: string;
  private entries: TestLogEntry[] = [];

  constructor() {
    const now = new Date();
    this.runId = now.toISOString().replace(/[:.]/g, "-").slice(0, 19);
    this.startedAt = now.toISOString();

    const logsRoot = path.resolve(__dirname, "..", "logs");
    this.runDir = path.join(logsRoot, this.runId);
    fs.mkdirSync(this.runDir, { recursive: true });
  }

  logTest(entry: TestLogEntry): void {
    this.entries.push(entry);

    const slug = this.slugify(entry.testName);
    const filename = `${slug}.json`;
    const filePath = path.join(this.runDir, filename);

    fs.writeFileSync(filePath, JSON.stringify(entry, null, 2), "utf-8");
    this.writeSummary();
  }

  writeSummary(): string {
    const now = new Date();
    const summary: RunSummary = {
      runId: this.runId,
      startedAt: this.startedAt,
      completedAt: now.toISOString(),
      durationMs: now.getTime() - new Date(this.startedAt).getTime(),
      testCount: this.entries.length,
      passed: this.entries.filter((e) => e.status === "finished").length,
      failed: this.entries.filter(
        (e) => e.status !== "finished" && e.status !== "requires_input"
      ).length,
      timedOut: this.entries.filter((e) => e.status === "requires_input").length,
      tests: this.entries.map((e) => ({
        testName: e.testName,
        testFile: e.testFile,
        status: e.status,
        durationMs: e.durationMs,
        toolCallCount: e.toolCalls.length,
        thinkingChunks: e.thinking.length,
        prompt: e.prompt,
        assistantText: e.assistantText,
      })),
    };

    const summaryPath = path.join(this.runDir, "_summary.json");
    fs.writeFileSync(summaryPath, JSON.stringify(summary, null, 2), "utf-8");
    return summaryPath;
  }

  private slugify(name: string): string {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "")
      .slice(0, 120);
  }
}

let _logger: TestRunLogger | null = null;

export function initRunLogger(): TestRunLogger {
  _logger = new TestRunLogger();
  return _logger;
}

export function getRunLogger(): TestRunLogger | null {
  return _logger;
}
